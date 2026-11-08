package bmasdk

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
	"sync"
	"testing"
	"time"

	"github.com/anthropics/anthropic-sdk-go/v2"
	"github.com/anthropics/anthropic-sdk-go/v2/option"
)

// request is what the test server saw.
type request struct {
	Method, Path, Query string
	Header              http.Header
	Body                string
}

type recorder struct {
	mu   sync.Mutex
	reqs []request
}

func (r *recorder) add(req *http.Request) request {
	body, _ := io.ReadAll(req.Body)
	got := request{Method: req.Method, Path: req.URL.Path, Query: req.URL.RawQuery, Header: req.Header.Clone(), Body: string(body)}
	r.mu.Lock()
	r.reqs = append(r.reqs, got)
	r.mu.Unlock()
	return got
}

func (r *recorder) all() []request {
	r.mu.Lock()
	defer r.mu.Unlock()
	return append([]request(nil), r.reqs...)
}

func newTestClient(t *testing.T, handler func(w http.ResponseWriter, req request)) (*Client, *recorder) {
	t.Helper()
	rec := &recorder{}
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		handler(w, rec.add(r))
	}))
	t.Cleanup(srv.Close)
	t.Setenv("BMA_API_KEY", "")
	t.Setenv("BMA_BASE_URL", "")
	t.Setenv("BMA_PROJECT_ID", "")
	return NewClient(option.WithBaseURL(srv.URL), option.WithAPIKey("bma-key"), option.WithMaxRetries(2)), rec
}

func writeJSON(w http.ResponseWriter, status int, v any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(v)
}

func TestNewClientUsesBMAEnvironmentOnly(t *testing.T) {
	rec := &recorder{}
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		rec.add(r)
		writeJSON(w, 200, map[string]any{"data": []any{}, "next_page": nil})
	}))
	defer srv.Close()
	t.Setenv("ANTHROPIC_API_KEY", "anthropic-key")
	t.Setenv("ANTHROPIC_BASE_URL", "http://127.0.0.1:1")
	t.Setenv("BMA_API_KEY", "bma-key")
	t.Setenv("BMA_BASE_URL", srv.URL)
	t.Setenv("BMA_PROJECT_ID", "proj_1")

	c := NewClient()
	if _, err := c.Beta.Machines.List(context.Background(), MachineListParams{}); err != nil {
		t.Fatal(err)
	}
	if _, err := c.Beta.Agents.List(context.Background(), anthropic.BetaAgentListParams{}); err != nil {
		t.Fatal(err)
	}
	for _, r := range rec.all() {
		// anthropic-sdk-go 2.x sends option.WithAPIKey as a bearer token.
		if got := r.Header.Get("Authorization"); got != "Bearer bma-key" {
			t.Errorf("%s: authorization %q", r.Path, got)
		}
		if got := r.Header.Get("X-Bma-Project-Id"); got != "proj_1" {
			t.Errorf("%s: x-bma-project-id %q", r.Path, got)
		}
		if got := r.Header.Get("X-Bma-Sdk"); got != "bma-sdk-go/"+SDKVersion {
			t.Errorf("%s: X-BMA-SDK %q", r.Path, got)
		}
	}
	if paths := fmt.Sprint(rec.all()[0].Path, " ", rec.all()[1].Path); paths != "/v1/machines /v1/agents" {
		t.Fatalf("paths %s", paths)
	}
}

func TestDefaultBaseURLIsBMA(t *testing.T) {
	t.Setenv("BMA_BASE_URL", "")
	t.Setenv("ANTHROPIC_BASE_URL", "https://example.invalid")
	var host string
	c := NewClient(option.WithAPIKey("k"), option.WithMaxRetries(0), option.WithMiddleware(func(r *http.Request, next option.MiddlewareNext) (*http.Response, error) {
		host = r.URL.Host
		return nil, errors.New("stop")
	}))
	_, _ = c.Beta.Machines.Get(context.Background(), "mch_1")
	if host != "api.bma.beeos.ai" {
		t.Fatalf("default host %q", host)
	}
}

func TestExtensionCreateRetriesWithOneIdempotencyKey(t *testing.T) {
	calls := 0
	c, rec := newTestClient(t, func(w http.ResponseWriter, r request) {
		calls++
		if calls == 1 {
			writeJSON(w, 500, map[string]any{"type": "error", "error": map[string]any{"type": "api_error", "message": "boom"}})
			return
		}
		writeJSON(w, 200, map[string]any{"type": "terminal_session", "id": "tsn_1", "machine_id": "mch_1", "state": "starting"})
	})
	term, err := c.Beta.TerminalSessions.New(context.Background(), TerminalSessionNewParams{MachineID: "mch_1", Cols: Ptr[int32](80)})
	if err != nil {
		t.Fatal(err)
	}
	if term.ID != "tsn_1" {
		t.Fatalf("id %q", term.ID)
	}
	reqs := rec.all()
	if len(reqs) != 2 {
		t.Fatalf("%d requests", len(reqs))
	}
	k1, k2 := reqs[0].Header.Get("Idempotency-Key"), reqs[1].Header.Get("Idempotency-Key")
	if k1 == "" || k1 != k2 {
		t.Fatalf("idempotency keys %q %q", k1, k2)
	}
	if reqs[0].Method != "POST" || reqs[0].Path != "/v1/terminal_sessions" || strings.TrimSpace(reqs[0].Body) != `{"cols":80,"machine_id":"mch_1"}` {
		t.Fatalf("request %+v", reqs[0])
	}

	if _, err := c.Beta.TerminalSessions.New(context.Background(), TerminalSessionNewParams{MachineID: "mch_1"}, WithIdempotencyKey("mine")); err != nil {
		t.Fatal(err)
	}
	if got := rec.all()[2].Header.Get("Idempotency-Key"); got != "mine" {
		t.Fatalf("explicit key %q", got)
	}
}

func TestPathsQueriesAndAutoPaging(t *testing.T) {
	c, rec := newTestClient(t, func(w http.ResponseWriter, r request) {
		switch {
		case r.Path == "/v1/machine_pools/mpo_1/grants" && !strings.Contains(r.Query, "page="):
			writeJSON(w, 200, map[string]any{"data": []any{map[string]any{"id": "g1"}, map[string]any{"id": "g2"}}, "next_page": "p2"})
		case r.Path == "/v1/machine_pools/mpo_1/grants":
			writeJSON(w, 200, map[string]any{"data": []any{map[string]any{"id": "g3"}}, "next_page": nil})
		case r.Path == "/v1/desktop_sessions/dsk_1/pending_actions/pa%2F1/confirm" || r.Path == "/v1/desktop_sessions/dsk_1/pending_actions/pa/1/confirm":
			writeJSON(w, 200, map[string]any{"type": "desktop_action_result"})
		default:
			writeJSON(w, 404, map[string]any{"type": "error", "error": map[string]any{"type": "not_found_error", "message": "nope", "code": "machine_not_found"}})
		}
	})
	ctx := context.Background()
	var ids []string
	pager := c.Beta.MachinePools.Grants.ListAutoPaging(ctx, "mpo_1", MachinePoolGrantListParams{Limit: Ptr[int64](2), Sort: Ptr("created_at")})
	for pager.Next() {
		ids = append(ids, pager.Current().ID)
	}
	if err := pager.Err(); err != nil {
		t.Fatal(err)
	}
	if fmt.Sprint(ids) != "[g1 g2 g3]" || pager.Index() != 3 {
		t.Fatalf("ids %v index %d", ids, pager.Index())
	}
	reqs := rec.all()
	if reqs[0].Query != "limit=2&sort=created_at" || reqs[1].Query != "limit=2&page=p2&sort=created_at" {
		t.Fatalf("queries %q %q", reqs[0].Query, reqs[1].Query)
	}

	if _, err := c.Beta.DesktopSessions.ConfirmAction(ctx, "dsk_1", "pa/1", DesktopSessionConfirmActionParams{}); err != nil {
		t.Fatalf("escaped path: %v", err)
	}

	_, err := c.Beta.Machines.Get(ctx, "mch_x")
	var apiErr *Error
	if !errors.As(err, &apiErr) || apiErr.StatusCode != 404 || apiErr.Type() != "not_found_error" || ErrorCode(err) != "machine_not_found" {
		t.Fatalf("error %v code %q", err, ErrorCode(err))
	}
	if _, err := c.Beta.Machines.Get(ctx, ""); err == nil || !strings.Contains(err.Error(), "machine_id") {
		t.Fatalf("empty id: %v", err)
	}
	if ErrorCode(errors.New("plain")) != "" {
		t.Fatal("ErrorCode of a non-API error")
	}
}

func TestExtensionFields(t *testing.T) {
	c, rec := newTestClient(t, func(w http.ResponseWriter, r request) {
		w.Header().Set("Content-Type", "application/json")
		_, _ = io.WriteString(w, `{"id":"ses_1","type":"session","status":"idle",
			"bma_harness":{"kind":"acp","agent":"claude-code","placement":"sandbox"},
			"bma_model_override":{"agent_id":"agt_1","api_format":"openai","model":"m1","provider_id":"p","expires_with_session":true}}`)
	})
	ctx := context.Background()
	s, err := c.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
		Agent:         anthropic.BetaSessionNewParamsAgentUnion{OfString: anthropic.String("aprf_1")},
		EnvironmentID: "env_1",
	}, WithSessionModelOverride(AgentModelOverrideInput{Model: "m1", APIKey: Ptr("secret")}), WithHarness(Harness{Kind: "acp"}))
	if err != nil {
		t.Fatal(err)
	}
	var body map[string]json.RawMessage
	if err := json.Unmarshal([]byte(rec.all()[0].Body), &body); err != nil {
		t.Fatal(err)
	}
	if string(body["bma_harness"]) != `{"kind":"acp"}` || !strings.Contains(string(body["bma_model_override"]), `"model":"m1"`) || string(body["environment_id"]) != `"env_1"` {
		t.Fatalf("request body %s", rec.all()[0].Body)
	}
	ext, err := SessionExtensions(s)
	if err != nil {
		t.Fatal(err)
	}
	if ext.Harness == nil || ext.Harness.Placement != "sandbox" || ext.ModelOverride == nil || ext.ModelOverride.Model != "m1" {
		t.Fatalf("extensions %+v", ext)
	}

	if _, err := c.Beta.Sessions.Update(ctx, "ses_1", anthropic.BetaSessionUpdateParams{}, WithSessionModelOverrideRevoke()); err != nil {
		t.Fatal(err)
	}
	if body := rec.all()[1].Body; !strings.Contains(body, `"bma_model_override":null`) {
		t.Fatalf("revoke body %s", body)
	}
	if _, err := SessionExtensions(&anthropic.BetaManagedAgentsSession{}); err == nil {
		t.Fatal("want an error for an object not decoded from a response")
	}
}

// sse writes frames and flushes.
func sse(w http.ResponseWriter, frames ...string) {
	for _, f := range frames {
		_, _ = io.WriteString(w, f)
	}
	w.(http.Flusher).Flush()
}

func frame(typ, id string, seq int) string {
	data := fmt.Sprintf(`{"type":%q,"id":%q,"bma_sequence":%d,"processed_at":"2026-11-08T00:00:00Z"}`, typ, id, seq)
	if seq == 0 {
		data = fmt.Sprintf(`{"type":%q,"id":%q}`, typ, id)
	}
	return fmt.Sprintf("event: %s\ndata: %s\n\n", typ, data)
}

func TestStreamEventsResumes(t *testing.T) {
	reconnectBackoff, maxReconnectBackoff = time.Millisecond, time.Millisecond
	conn := 0
	c, rec := newTestClient(t, func(w http.ResponseWriter, r request) {
		conn++
		w.Header().Set("Content-Type", "text/event-stream")
		switch conn {
		case 1: // two events of sequence 1, an announcement, then the connection drops
			sse(w, frame("session.status_running", "sesst_1_run", 1), frame("user.message", "evt_1", 1), frame("session.status_idle", "sesst_x", 0))
		case 2: // the server resumes after sequence 0: replays sequence 1
			sse(w, frame("session.status_running", "sesst_1_run", 1), frame("user.message", "evt_1", 1),
				frame("session.status_idle", "sesst_x", 1), frame("agent.message", "evt_2", 2), "event: ping\ndata: {}\n\n")
		case 3:
			sse(w, frame("session.status_idle", "sesst_2_idle", 2))
		default:
			writeJSON(w, 404, map[string]any{"type": "error", "error": map[string]any{"type": "not_found_error", "message": "gone"}})
		}
	})
	stream := c.Beta.Sessions.Events.StreamEvents(context.Background(), "ses_1", anthropic.BetaSessionEventStreamParams{})
	var got []string
	for stream.Next() {
		got = append(got, stream.Current().ID)
	}
	var apiErr *Error
	if !errors.As(stream.Err(), &apiErr) || apiErr.StatusCode != 404 {
		t.Fatalf("stream error %v", stream.Err())
	}
	if fmt.Sprint(got) != "[sesst_1_run evt_1 sesst_x evt_2 sesst_2_idle]" {
		t.Fatalf("events %v", got)
	}
	reqs := rec.all()
	if len(reqs) != 4 || reqs[0].Header.Get("Last-Event-ID") != "" || reqs[1].Header.Get("Last-Event-ID") != "0" || reqs[2].Header.Get("Last-Event-ID") != "1" {
		t.Fatalf("Last-Event-ID %q %q %q (%d requests)", reqs[0].Header.Get("Last-Event-ID"), reqs[1].Header.Get("Last-Event-ID"), reqs[2].Header.Get("Last-Event-ID"), len(reqs))
	}
	if got := reqs[0].Header.Get("Anthropic-Beta"); got != "managed-agents-2026-04-01" || reqs[0].Path != "/v1/sessions/ses_1/events/stream" {
		t.Fatalf("anthropic-beta %q path %s", got, reqs[0].Path)
	}
}

func TestStreamEventsGivesUp(t *testing.T) {
	reconnectBackoff, maxReconnectBackoff = time.Millisecond, time.Millisecond
	c, rec := newTestClient(t, func(w http.ResponseWriter, r request) {
		w.Header().Set("Content-Type", "text/event-stream")
		sse(w) // every connection ends at once
	})
	stream := c.Beta.Sessions.Events.StreamEvents(context.Background(), "ses_1", anthropic.BetaSessionEventStreamParams{})
	if stream.Next() {
		t.Fatal("unexpected event")
	}
	if err := stream.Err(); err == nil || !strings.Contains(err.Error(), "not resumed after 5 attempts") {
		t.Fatalf("err %v", err)
	}
	if n := len(rec.all()); n != 1+maxReconnects {
		t.Fatalf("%d connections", n)
	}
}

func TestStreamEventsStopsOnContext(t *testing.T) {
	reconnectBackoff, maxReconnectBackoff = time.Hour, time.Hour
	ctx, cancel := context.WithCancel(context.Background())
	c, _ := newTestClient(t, func(w http.ResponseWriter, r request) {
		w.Header().Set("Content-Type", "text/event-stream")
		sse(w, frame("user.message", "evt_1", 1))
		cancel()
	})
	stream := c.Beta.Sessions.Events.StreamEvents(ctx, "ses_1", anthropic.BetaSessionEventStreamParams{})
	for stream.Next() {
	}
	if !errors.Is(stream.Err(), context.Canceled) {
		t.Fatalf("err %v", stream.Err())
	}
}
