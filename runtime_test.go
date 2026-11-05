package bma_test

// Runtime behaviour of the resource client: scope defaults, request shape,
// retries and idempotency keys (ADR 0012 D3), errors, pagination and the
// event stream. Mirrors typescript/test/runtime.test.ts with a stub
// RoundTripper; contract_test.go replays the recorded fixtures over HTTP.

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"mime"
	"mime/multipart"
	"net"
	"net/http"
	"strings"
	"sync"
	"syscall"
	"testing"
	"time"

	"github.com/beeos-ai/bma-sdk"
	"github.com/beeos-ai/bma-sdk/option"
)

const (
	testBase    = "https://bma.test"
	testOrg     = "org_aaaaaaaaaaaaaaaaaaaaaaaaaa"
	testProject = "prj_aaaaaaaaaaaaaaaaaaaaaaaaaa"
	testAgent   = "agt_aaaaaaaaaaaaaaaaaaaaaaaaaa"
	testSession = "ses_aaaaaaaaaaaaaaaaaaaaaaaaaa"
)

type call struct {
	method string
	path   string
	query  map[string][]string
	header http.Header
	body   []byte
}

type reply func(*http.Request) (*http.Response, error)

type stub struct {
	mu      sync.Mutex
	replies []reply
	calls   []call
}

func (s *stub) RoundTrip(r *http.Request) (*http.Response, error) {
	var body []byte
	if r.Body != nil {
		body, _ = io.ReadAll(r.Body)
	}
	s.mu.Lock()
	s.calls = append(s.calls, call{r.Method, r.URL.Path, r.URL.Query(), r.Header.Clone(), body})
	if len(s.replies) == 0 {
		s.mu.Unlock()
		return nil, fmt.Errorf("unexpected request %s %s", r.Method, r.URL)
	}
	next := s.replies[0]
	s.replies = s.replies[1:]
	s.mu.Unlock()
	return next(r)
}

func respond(status int, body string, headers ...string) reply {
	return func(r *http.Request) (*http.Response, error) {
		h := http.Header{"Content-Type": {"application/json"}}
		for i := 0; i+1 < len(headers); i += 2 {
			h.Set(headers[i], headers[i+1])
		}
		return &http.Response{StatusCode: status, Header: h, Body: io.NopCloser(strings.NewReader(body)), Request: r}, nil
	}
}

func apiError(status int, code string, headers ...string) reply {
	return respond(status, fmt.Sprintf(`{"error":"%s happened","code":"%s"}`, code, code), headers...)
}

func fail(err error) reply { return func(*http.Request) (*http.Response, error) { return nil, err } }

func refused() error {
	return &net.OpError{Op: "dial", Net: "tcp", Err: &net.DNSError{Err: "refused"}}
}
func reset() error { return &net.OpError{Op: "read", Net: "tcp", Err: syscall.ECONNRESET} }

func newClient(t *testing.T, replies []reply, opts ...option.RequestOption) (*bma.Client, *stub) {
	t.Helper()
	s := &stub{replies: replies}
	base := []option.RequestOption{
		option.WithToken("t"), option.WithBaseURL(testBase), option.WithOrg(testOrg), option.WithProject(testProject),
		option.WithHTTPClient(&http.Client{Transport: s}),
	}
	return bma.NewClient(append(base, opts...)...), s
}

func TestScopeDefaultsAndOverride(t *testing.T) {
	ctx := context.Background()
	client, s := newClient(t, []reply{respond(200, `{"agent":{}}`), respond(200, `{"agent":{}}`)})
	if _, err := client.Agents.Get(ctx, testAgent); err != nil {
		t.Fatal(err)
	}
	if _, err := client.Agents.Get(ctx, testAgent, option.WithProject("prj_bbbbbbbbbbbbbbbbbbbbbbbbbb")); err != nil {
		t.Fatal(err)
	}
	if want := "/api/v1/orgs/" + testOrg + "/projects/" + testProject + "/agents/" + testAgent; s.calls[0].path != want {
		t.Fatalf("path = %s, want %s", s.calls[0].path, want)
	}
	if !strings.Contains(s.calls[1].path, "/projects/prj_bbbbbbbbbbbbbbbbbbbbbbbbbb/") {
		t.Fatalf("override path = %s", s.calls[1].path)
	}
	if got := s.calls[0].header.Get("Authorization"); got != "Bearer t" {
		t.Fatalf("authorization = %q", got)
	}
}

func TestMissingScopeIsAClientError(t *testing.T) {
	t.Setenv("BMA_ORG_ID", "")
	t.Setenv("BMA_PROJECT_ID", "")
	s := &stub{}
	client := bma.NewClient(option.WithToken("t"), option.WithBaseURL(testBase), option.WithHTTPClient(&http.Client{Transport: s}))
	_, err := client.Agents.List(context.Background(), bma.AgentListParams{})
	if err == nil || !strings.Contains(err.Error(), "WithOrg") {
		t.Fatalf("err = %v", err)
	}
	if len(s.calls) != 0 {
		t.Fatalf("calls = %d", len(s.calls))
	}
}

func TestScopeFromEnvironment(t *testing.T) {
	t.Setenv("BMA_ORG_ID", testOrg)
	t.Setenv("BMA_PROJECT_ID", testProject)
	s := &stub{replies: []reply{respond(200, `{"data":[],"next_cursor":null}`)}}
	client := bma.NewClient(option.WithToken("t"), option.WithBaseURL(testBase), option.WithHTTPClient(&http.Client{Transport: s}))
	if _, err := client.Agents.List(context.Background(), bma.AgentListParams{}); err != nil {
		t.Fatal(err)
	}
	if want := "/api/v1/orgs/" + testOrg + "/projects/" + testProject + "/agents"; s.calls[0].path != want {
		t.Fatalf("path = %s", s.calls[0].path)
	}
}

func TestParamsSplitIntoQueryHeaderAndBody(t *testing.T) {
	client, s := newClient(t, []reply{respond(201, `{"agent_input":{}}`)})
	_, err := client.Agents.Inputs.New(context.Background(), testAgent, bma.AgentInputNewParams{
		SessionID:     bma.Ptr(testSession),
		ContentBlocks: []bma.CreateAgentInputContentBlock{bma.NewTextInputBlock("hi")},
		DeliveryMode:  bma.Ptr(bma.CreateAgentInputDeliveryModeQueued),
	}, option.WithIdempotencyKey("input-1"))
	if err != nil {
		t.Fatal(err)
	}
	c := s.calls[0]
	if c.method != "POST" || c.query["session_id"][0] != testSession || c.header.Get("Idempotency-Key") != "input-1" {
		t.Fatalf("call = %+v", c)
	}
	var body map[string]any
	if err := json.Unmarshal(c.body, &body); err != nil {
		t.Fatal(err)
	}
	if fmt.Sprint(body) != fmt.Sprint(map[string]any{"content_blocks": []any{map[string]any{"type": "text", "text": "hi"}}, "delivery_mode": "queued"}) {
		t.Fatalf("body = %s", c.body)
	}
}

func TestArrayAndDeepObjectQuery(t *testing.T) {
	client, s := newClient(t, []reply{respond(200, `{}`), respond(200, `{"data":[],"next_cursor":null}`)})
	ids := bma.UsageIncludeProjectIDs{testProject, "prj_bbbbbbbbbbbbbbbbbbbbbbbbbb"}
	if _, err := client.Orgs.Usage(context.Background(), bma.OrgUsageParams{IncludeProjectIDs: &ids}); err != nil {
		t.Fatal(err)
	}
	meta := bma.SecretMetadataFilter{"team": "a", "env": "b"}
	if _, err := client.Orgs.Secrets.List(context.Background(), bma.OrgSecretListParams{Metadata: &meta}); err != nil {
		t.Fatal(err)
	}
	if got := s.calls[0].query["include_project_ids"]; len(got) != 2 || got[1] != "prj_bbbbbbbbbbbbbbbbbbbbbbbbbb" {
		t.Fatalf("include_project_ids = %v", got)
	}
	if s.calls[1].query["metadata[team]"][0] != "a" || s.calls[1].query["metadata[env]"][0] != "b" {
		t.Fatalf("metadata = %v", s.calls[1].query)
	}
}

func TestBinaryUploadAndDownload(t *testing.T) {
	client, s := newClient(t, []reply{respond(201, `{"id":"file_1"}`), respond(200, "bytes")})
	_, err := client.Files.Upload(context.Background(), bma.FileUploadParams{
		Filename: "a.txt", Body: strings.NewReader("hello"), XBMAFileMetadata: bma.Ptr(`{"k":"v"}`),
	}, option.WithIdempotencyKey("u-1"))
	if err != nil {
		t.Fatal(err)
	}
	c := s.calls[0]
	if c.header.Get("Content-Type") != "application/octet-stream" || c.header.Get("X-BMA-File-Metadata") != `{"k":"v"}` || string(c.body) != "hello" {
		t.Fatalf("upload = %+v", c)
	}
	res, err := client.Files.Download(context.Background(), "file_1")
	if err != nil {
		t.Fatal(err)
	}
	defer res.Body.Close()
	if raw, _ := io.ReadAll(res.Body); string(raw) != "bytes" {
		t.Fatalf("content = %q", raw)
	}
}

func TestMultipartBody(t *testing.T) {
	client, s := newClient(t, []reply{respond(201, `{"id":"skl_1"}`)})
	var owner bma.SkillOwnerInput
	if err := owner.FromOrgSkillOwnerInput(bma.OrgSkillOwnerInput{Kind: "org"}); err != nil {
		t.Fatal(err)
	}
	_, err := client.Orgs.Skills.New(context.Background(), bma.OrgSkillNewParams{Owner: owner, Archive: bma.NewFile(strings.NewReader("zip"), "skill.zip")})
	if err != nil {
		t.Fatal(err)
	}
	_, ps, _ := mime.ParseMediaType(s.calls[0].header.Get("Content-Type"))
	form, err := multipart.NewReader(strings.NewReader(string(s.calls[0].body)), ps["boundary"]).ReadForm(1 << 20)
	if err != nil {
		t.Fatal(err)
	}
	if form.Value["owner"][0] != `{"kind":"org"}` || form.File["archive"][0].Filename != "skill.zip" {
		t.Fatalf("form = %+v", form)
	}
}

func Test204(t *testing.T) {
	client, _ := newClient(t, []reply{respond(204, "")})
	if err := client.Agents.Machines.Delete(context.Background(), testAgent, "mch_1"); err != nil {
		t.Fatal(err)
	}
}

func TestErrorsCarryStatusAndCode(t *testing.T) {
	for _, tc := range []struct {
		status int
		code   bma.ErrorCode
	}{{401, bma.ErrorCodeUnauthorized}, {404, bma.ErrorCodeNotFound}, {409, bma.ErrorCodeStateTransitionConflict}} {
		client, _ := newClient(t, []reply{apiError(tc.status, string(tc.code))})
		_, err := client.Agents.Get(context.Background(), testAgent)
		var apiErr *bma.Error
		if !errors.As(err, &apiErr) || apiErr.StatusCode != tc.status || apiErr.Code != tc.code {
			t.Fatalf("err = %#v", err)
		}
	}
}

func TestGetRetries5xxAndConnectionErrors(t *testing.T) {
	client, s := newClient(t, []reply{apiError(500, "internal_error", "retry-after-ms", "1"), fail(reset()), respond(200, `{"agent":{}}`)})
	if _, err := client.Agents.Get(context.Background(), testAgent); err != nil {
		t.Fatal(err)
	}
	if len(s.calls) != 3 {
		t.Fatalf("calls = %d", len(s.calls))
	}
}

func TestMaxRetriesBoundsAttempts(t *testing.T) {
	client, s := newClient(t, []reply{
		apiError(503, "service_unavailable", "retry-after-ms", "1"), apiError(503, "service_unavailable", "retry-after-ms", "1"),
	}, option.WithMaxRetries(1))
	_, err := client.Agents.Get(context.Background(), testAgent)
	var apiErr *bma.Error
	if !errors.As(err, &apiErr) || apiErr.StatusCode != 503 || len(s.calls) != 2 {
		t.Fatalf("err = %v calls = %d", err, len(s.calls))
	}
}

func Test409IsNeverRetried(t *testing.T) {
	client, s := newClient(t, []reply{apiError(409, "idempotency_key_conflict")})
	_, err := client.Agents.New(context.Background(), bma.AgentNewParams{Name: bma.Ptr(bma.AgentName("a"))})
	if err == nil || len(s.calls) != 1 {
		t.Fatalf("err = %v calls = %d", err, len(s.calls))
	}
}

func TestIdempotentWritesReuseOneGeneratedKey(t *testing.T) {
	client, s := newClient(t, []reply{apiError(500, "internal_error", "retry-after-ms", "1"), fail(reset()), respond(201, `{"agent":{}}`)})
	if _, err := client.Agents.New(context.Background(), bma.AgentNewParams{Name: bma.Ptr(bma.AgentName("a"))}); err != nil {
		t.Fatal(err)
	}
	key := s.calls[0].header.Get("Idempotency-Key")
	if !strings.HasPrefix(key, "bma-sdk-retry-") || len(key) != len("bma-sdk-retry-")+36 {
		t.Fatalf("key = %q", key)
	}
	for _, c := range s.calls {
		if c.header.Get("Idempotency-Key") != key {
			t.Fatalf("keys differ: %q", c.header.Get("Idempotency-Key"))
		}
	}
}

func TestWritesWithoutIdempotencyKeyRetryOnlyUndelivered429And503(t *testing.T) {
	ctx := context.Background()
	a, sa := newClient(t, []reply{apiError(500, "internal_error")})
	if _, err := a.Agents.Sessions.New(ctx, testAgent, bma.AgentSessionNewParams{}); err == nil || len(sa.calls) != 1 {
		t.Fatalf("500: err = %v calls = %d", err, len(sa.calls))
	}
	b, sb := newClient(t, []reply{fail(reset())})
	if _, err := b.Agents.Sessions.New(ctx, testAgent, bma.AgentSessionNewParams{}); err == nil || len(sb.calls) != 1 {
		t.Fatalf("reset: err = %v calls = %d", err, len(sb.calls))
	}
	c, sc := newClient(t, []reply{fail(refused()), apiError(429, "rate_limited", "retry-after-ms", "1"), respond(201, `{"session":{"id":"`+testSession+`"}}`)})
	created, err := c.Agents.Sessions.New(ctx, testAgent, bma.AgentSessionNewParams{})
	if err != nil || created.Session.ID != testSession || len(sc.calls) != 3 {
		t.Fatalf("refused+429: err = %v calls = %d", err, len(sc.calls))
	}
	d, sd := newClient(t, []reply{apiError(429, "rate_limited", "retry-after-ms", "1")}, option.WithMaxRetries(0))
	if _, err := d.Agents.Sessions.New(ctx, testAgent, bma.AgentSessionNewParams{}); err == nil || len(sd.calls) != 1 {
		t.Fatalf("429 no retries: err = %v calls = %d", err, len(sd.calls))
	}
}

func TestExplicitIdempotencyKeyOnOperationWithoutHeader(t *testing.T) {
	client, s := newClient(t, nil)
	_, err := client.Agents.Sessions.New(context.Background(), testAgent, bma.AgentSessionNewParams{}, option.WithIdempotencyKey("x"))
	if err == nil || len(s.calls) != 0 {
		t.Fatalf("err = %v", err)
	}
}

func TestTimeout(t *testing.T) {
	slow := func(r *http.Request) (*http.Response, error) {
		<-r.Context().Done()
		return nil, r.Context().Err()
	}
	client, _ := newClient(t, []reply{slow}, option.WithMaxRetries(0), option.WithRequestTimeout(20*time.Millisecond))
	_, err := client.Agents.Get(context.Background(), testAgent)
	if !errors.Is(err, context.DeadlineExceeded) {
		t.Fatalf("err = %v", err)
	}
}

func TestCursorPages(t *testing.T) {
	page := func(ids []string, next string) reply {
		items := make([]string, len(ids))
		for i, id := range ids {
			items[i] = `{"id":"` + id + `"}`
		}
		cursor := "null"
		if next != "" {
			cursor = `"` + next + `"`
		}
		return respond(200, `{"data":[`+strings.Join(items, ",")+`],"next_cursor":`+cursor+`}`)
	}
	client, s := newClient(t, []reply{page([]string{"a", "b"}, "c1"), page([]string{"a", "b"}, "c1"), page([]string{"c"}, "")})
	ctx := context.Background()
	first, err := client.Agents.List(ctx, bma.AgentListParams{Limit: bma.Ptr(bma.PageLimit(2))})
	if err != nil || len(first.Data) != 2 || first.Data[0].ID != "a" || !first.HasNextPage() {
		t.Fatalf("first = %+v err = %v", first, err)
	}
	var ids []string
	pager := client.Agents.ListAutoPaging(ctx, bma.AgentListParams{Limit: bma.Ptr(bma.PageLimit(2))})
	for pager.Next() {
		ids = append(ids, pager.Current().ID)
	}
	if err := pager.Err(); err != nil || strings.Join(ids, ",") != "a,b,c" {
		t.Fatalf("ids = %v err = %v", ids, err)
	}
	if s.calls[2].query["cursor"][0] != "c1" || s.calls[2].query["limit"][0] != "2" {
		t.Fatalf("page 2 query = %v", s.calls[2].query)
	}
}

func sse(frames ...[3]string) reply {
	var b strings.Builder
	for _, f := range frames {
		b.WriteString(": keep-alive\n\nevent: " + f[0] + "\n")
		if f[1] != "" {
			b.WriteString("id: " + f[1] + "\n")
		}
		b.WriteString("data: " + f[2] + "\n\n")
	}
	body := b.String()
	return func(r *http.Request) (*http.Response, error) {
		return &http.Response{StatusCode: 200, Header: http.Header{"Content-Type": {"text/event-stream"}}, Body: io.NopCloser(strings.NewReader(body)), Request: r}, nil
	}
}

func TestEventStreamReconnectsWithLastEventID(t *testing.T) {
	client, s := newClient(t, []reply{
		sse(
			[3]string{"agent_input", "5", `{"event_kind":"agent_input","sequence":5}`},
			[3]string{"tool_call_update", "", `{"tool_call_id":"tc_1","state":"ready"}`},
			[3]string{"error", "", `{"error":"restarting","code":"service_unavailable"}`},
		),
		sse([3]string{"model_output", "6", `{"event_kind":"model_output","sequence":6}`}),
	})
	stream := client.Agents.Events.Stream(context.Background(), testAgent, bma.AgentEventStreamParams{
		SessionID: bma.Ptr(testSession), AfterSequence: bma.Ptr(int64(2)),
	})
	defer stream.Close()
	var got []string
	for stream.Next() {
		ev := stream.Current()
		switch v := ev.AsAny().(type) {
		case bma.AgentInputEvent:
			got = append(got, fmt.Sprintf("agent_input:%d", ev.Sequence))
		case bma.ToolCallUpdate:
			got = append(got, "tool_call_update:"+v.ToolCallID)
		case bma.ModelOutputEvent:
			got = append(got, fmt.Sprintf("model_output:%d", ev.Sequence))
		default:
			t.Fatalf("unexpected %T", v)
		}
		if len(got) == 3 {
			break
		}
	}
	if err := stream.Err(); err != nil {
		t.Fatal(err)
	}
	if strings.Join(got, " ") != "agent_input:5 tool_call_update:tc_1 model_output:6" {
		t.Fatalf("got %v", got)
	}
	if s.calls[0].header.Get("Accept") != "text/event-stream" || s.calls[0].query["after_sequence"][0] != "2" {
		t.Fatalf("first = %+v", s.calls[0])
	}
	if s.calls[1].header.Get("Last-Event-ID") != "5" || s.calls[1].query["session_id"][0] != testSession || s.calls[1].query["after_sequence"] != nil {
		t.Fatalf("second = %+v", s.calls[1])
	}
}

func TestEventStreamTerminalErrorFrame(t *testing.T) {
	client, s := newClient(t, []reply{sse([3]string{"error", "", `{"error":"gone","code":"forbidden"}`})})
	stream := client.Agents.Events.Stream(context.Background(), testAgent, bma.AgentEventStreamParams{})
	for stream.Next() {
	}
	var apiErr *bma.Error
	if !errors.As(stream.Err(), &apiErr) || apiErr.Code != bma.ErrorCodeForbidden || len(s.calls) != 1 {
		t.Fatalf("err = %v", stream.Err())
	}
}

func TestWithJSONSetSendsExplicitNull(t *testing.T) {
	client, s := newClient(t, []reply{respond(200, `{}`)})
	_, err := client.Orgs.MachinePools.Update(context.Background(), "mpo_1", bma.OrgMachinePoolUpdateParams{PauseAfterIdleMinutes: bma.Ptr(int32(10))},
		option.WithJSONSet("delete_after_idle_minutes", nil))
	if err != nil {
		t.Fatal(err)
	}
	if got := string(s.calls[0].body); got != `{"delete_after_idle_minutes":null,"pause_after_idle_minutes":10}` {
		t.Fatalf("body = %s", got)
	}
}
