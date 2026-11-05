package bma_test

// Regressions of research/typed-sdk-review-p12.md and typed-sdk-review-1.0.md:
// EventSource reconnection, runner robustness, pagination of {data, next_X}
// lists, timeouts (0 = none, uploads bounded only after the body is sent),
// replayable upload bodies and environment defaults.

import (
	"bytes"
	"context"
	"errors"
	"fmt"
	"io"
	"net/http"
	"strings"
	"sync/atomic"
	"testing"
	"time"

	"github.com/beeos-ai/bma-sdk"
	"github.com/beeos-ai/bma-sdk/option"
)

func rawSSE(text string) reply {
	return func(r *http.Request) (*http.Response, error) {
		return &http.Response{StatusCode: 200, Header: http.Header{"Content-Type": {"text/event-stream"}}, Body: io.NopCloser(strings.NewReader(text)), Request: r}, nil
	}
}

func sequences(t *testing.T, stream *bma.Stream[bma.AgentStreamEvent], n int) []int64 {
	t.Helper()
	var out []int64
	for len(out) < n && stream.Next() {
		out = append(out, stream.Current().Sequence)
	}
	return out
}

func TestEventStreamCleanEndReconnectsWithLastEventID(t *testing.T) {
	client, s := newClient(t, []reply{
		rawSSE("event: model_output\nid: 5\ndata: {\"event_kind\":\"model_output\",\"sequence\":5}\n\n"),
		rawSSE("event: model_output\nid: 6\ndata: {\"event_kind\":\"model_output\",\"sequence\":6}\n\n"),
	})
	stream := client.Agents.Events.Stream(context.Background(), testAgent, bma.AgentEventStreamParams{AfterSequence: bma.Ptr(int64(1))})
	defer stream.Close()
	if got := sequences(t, stream, 2); fmt.Sprint(got) != "[5 6]" {
		t.Fatalf("got %v err %v", got, stream.Err())
	}
	if s.calls[1].header.Get("Last-Event-ID") != "5" || s.calls[1].query["after_sequence"] != nil {
		t.Fatalf("second = %+v", s.calls[1])
	}
}

func TestEventStreamPartialFrameIsDiscardedAndReconnects(t *testing.T) {
	client, s := newClient(t, []reply{
		rawSSE("event: model_output\nid: 6\ndata: {\"event_kind\":\"model_output\",\"sequence\":6}\n\nevent: model_output\nid: 7\ndata: {\"seq"),
		rawSSE("event: model_output\nid: 7\ndata: {\"event_kind\":\"model_output\",\"sequence\":7}\n\n"),
	})
	stream := client.Agents.Events.Stream(context.Background(), testAgent, bma.AgentEventStreamParams{})
	defer stream.Close()
	if got := sequences(t, stream, 2); fmt.Sprint(got) != "[6 7]" {
		t.Fatalf("got %v err %v", got, stream.Err())
	}
	if s.calls[1].header.Get("Last-Event-ID") != "6" {
		t.Fatalf("second = %+v", s.calls[1])
	}
}

func TestEventStreamReconnectsWithoutDataSpendTheBudget(t *testing.T) {
	client, s := newClient(t, []reply{rawSSE(""), apiError(503, "service_unavailable"), fail(refused())}, option.WithMaxRetries(2))
	stream := client.Agents.Events.Stream(context.Background(), testAgent, bma.AgentEventStreamParams{})
	for stream.Next() {
	}
	if stream.Err() == nil || len(s.calls) != 3 {
		t.Fatalf("err = %v calls = %d", stream.Err(), len(s.calls))
	}
}

func TestEventStreamHeartbeatResetsTheBudget(t *testing.T) {
	client, s := newClient(t, []reply{
		rawSSE(": heartbeat\n\n"), rawSSE(": heartbeat\n\n"),
		rawSSE("event: model_output\nid: 9\ndata: {\"event_kind\":\"model_output\",\"sequence\":9}\n\n"),
	}, option.WithMaxRetries(1))
	stream := client.Agents.Events.Stream(context.Background(), testAgent, bma.AgentEventStreamParams{})
	defer stream.Close()
	if got := sequences(t, stream, 1); fmt.Sprint(got) != "[9]" || len(s.calls) != 3 {
		t.Fatalf("got %v calls %d err %v", got, len(s.calls), stream.Err())
	}
}

func TestRunnerRidesOutCleanStreamEndsAndTreats409AsHandled(t *testing.T) {
	var connects, submits atomic.Int32
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	base := "/api/v1/orgs/" + testOrg + "/projects/" + testProject + "/agents/" + testAgent
	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		switch p := r.URL.Path; p {
		case base + "/events/stream":
			w.Header().Set("Content-Type", "text/event-stream")
			switch connects.Add(1) { // every response ends cleanly
			case 2:
				fmt.Fprint(w, "event: tool_call_update\ndata: {\"tool_call_id\":\"tc_5\",\"state\":\"ready\"}\n\n")
			case 4:
				cancel()
			}
		case base + "/tool-calls":
			fmt.Fprint(w, `{"data":[],"next_cursor":null}`)
		case base + "/tool-calls/tc_5":
			fmt.Fprintf(w, `{"tool_call":%s}`, toolCallJSON("tc_5", "get_weather", `{"city":"Oslo"}`, testAgent))
		case base + "/tool-calls/tc_5/result":
			submits.Add(1)
			w.WriteHeader(409)
			fmt.Fprint(w, `{"error":"already answered","code":"conflict"}`)
		default:
			t.Errorf("unexpected %s", p)
		}
	})
	client := bma.NewClient(option.WithToken("t"), option.WithBaseURL("https://bma.test"), option.WithOrg(testOrg), option.WithProject(testProject),
		option.WithMaxRetries(0), option.WithHTTPClient(&http.Client{Transport: handlerTransport{handler}}))
	if err := client.Agents.ToolCalls.Runner(testAgent, bma.ToolRunnerParams{Tools: []bma.RunnableTool{weather}}).Run(ctx); err != nil {
		t.Fatal(err)
	}
	if connects.Load() < 4 || submits.Load() != 1 {
		t.Fatalf("connects %d submits %d", connects.Load(), submits.Load())
	}
}

func TestRunnerWithAFiniteBudgetReturnsAnError(t *testing.T) {
	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if strings.HasSuffix(r.URL.Path, "/events/stream") {
			w.Header().Set("Content-Type", "text/event-stream")
			return
		}
		fmt.Fprint(w, `{"data":[],"next_cursor":null}`)
	})
	client := bma.NewClient(option.WithToken("t"), option.WithBaseURL("https://bma.test"), option.WithOrg(testOrg), option.WithProject(testProject),
		option.WithHTTPClient(&http.Client{Transport: handlerTransport{handler}}))
	err := client.Agents.ToolCalls.Runner(testAgent, bma.ToolRunnerParams{Tools: []bma.RunnableTool{weather}, MaxReconnects: 1}).Run(context.Background())
	if err == nil || !strings.Contains(err.Error(), "event stream ended") {
		t.Fatalf("err = %v", err)
	}
}

func slowly(d time.Duration, body string) reply {
	return func(r *http.Request) (*http.Response, error) {
		if r.Body != nil {
			_, _ = io.Copy(io.Discard, r.Body)
		}
		select {
		case <-time.After(d):
			return respond(200, body)(r)
		case <-r.Context().Done():
			return nil, r.Context().Err()
		}
	}
}

func TestRequestTimeoutZeroMeansNone(t *testing.T) {
	client, _ := newClient(t, []reply{slowly(30*time.Millisecond, `{"agent":{}}`), slowly(30*time.Millisecond, `{"agent":{}}`)},
		option.WithRequestTimeout(5*time.Millisecond), option.WithMaxRetries(0))
	if _, err := client.Agents.Get(context.Background(), testAgent, option.WithRequestTimeout(0)); err != nil {
		t.Fatal(err)
	}
	if _, err := client.Agents.Get(context.Background(), testAgent); !errors.Is(err, context.DeadlineExceeded) {
		t.Fatalf("err = %v", err)
	}
}

// slowBody is an upload that takes longer than the request timeout to send.
type slowBody struct {
	io.ReadSeeker
	delay time.Duration
}

func (b *slowBody) Read(p []byte) (int, error) {
	time.Sleep(b.delay)
	return b.ReadSeeker.Read(p[:min(len(p), 4)])
}

func TestUploadTimeoutStartsAfterTheBodyIsSent(t *testing.T) {
	alive := func(r *http.Request) (*http.Response, error) {
		if err := r.Context().Err(); err != nil {
			return nil, err // the timeout fired while the body was being sent
		}
		return respond(201, `{"id":"file_1"}`)(r)
	}
	client, s := newClient(t, []reply{alive}, option.WithRequestTimeout(20*time.Millisecond), option.WithMaxRetries(0))
	body := &slowBody{ReadSeeker: bytes.NewReader(bytes.Repeat([]byte("x"), 40)), delay: 5 * time.Millisecond} // ~50ms to send
	if _, err := client.Files.Upload(context.Background(), bma.FileUploadParams{Filename: "a.bin", Body: body}); err != nil {
		t.Fatal(err)
	}
	if len(s.calls[0].body) != 40 {
		t.Fatalf("sent %d bytes", len(s.calls[0].body))
	}
}

func TestSeekableUploadIsReplayedUnseekableIsSentOnce(t *testing.T) {
	client, s := newClient(t, []reply{apiError(503, "service_unavailable", "retry-after-ms", "1"), respond(201, `{"id":"file_1"}`)})
	body := bytes.NewReader(append([]byte("pre"), bytes.Repeat([]byte("x"), 1000)...))
	_, _ = body.Seek(3, io.SeekStart)
	if _, err := client.Files.Upload(context.Background(), bma.FileUploadParams{Filename: "a.bin", Body: body}); err != nil {
		t.Fatal(err)
	}
	if len(s.calls) != 2 || len(s.calls[0].body) != 1000 || len(s.calls[1].body) != 1000 ||
		s.calls[0].header.Get("Idempotency-Key") != s.calls[1].header.Get("Idempotency-Key") {
		t.Fatalf("calls = %d %d", len(s.calls[0].body), len(s.calls[1].body))
	}

	client, s = newClient(t, []reply{apiError(503, "service_unavailable", "retry-after-ms", "1"), respond(201, `{"id":"file_1"}`)})
	pipe := io.MultiReader(strings.NewReader(strings.Repeat("y", 1000)))
	_, err := client.Files.Upload(context.Background(), bma.FileUploadParams{Filename: "a.bin", Body: pipe})
	var apiErr *bma.Error
	if !errors.As(err, &apiErr) || apiErr.StatusCode != 503 || len(s.calls) != 1 || len(s.calls[0].body) != 1000 {
		t.Fatalf("err = %v calls = %d", err, len(s.calls))
	}
}

func TestTokenAndBaseURLFromTheEnvironment(t *testing.T) {
	t.Setenv("BMA_TOKEN", "env-token")
	t.Setenv("BMA_BASE_URL", "https://env.test/")
	s := &stub{replies: []reply{respond(200, `{"agent":{}}`)}}
	client := bma.NewClient(option.WithOrg(testOrg), option.WithProject(testProject), option.WithHTTPClient(&http.Client{Transport: s}))
	if _, err := client.Agents.Get(context.Background(), testAgent); err != nil {
		t.Fatal(err)
	}
	if s.calls[0].header.Get("Authorization") != "Bearer env-token" || !strings.HasPrefix(s.calls[0].path, "/api/v1/") {
		t.Fatalf("call = %+v", s.calls[0])
	}
}

func TestBaseURLIsTheOrigin(t *testing.T) {
	if bma.DefaultBaseURL != "https://api.bma.beeos.ai" {
		t.Fatalf("DefaultBaseURL = %q", bma.DefaultBaseURL)
	}
	want := "/api/v1/orgs/" + testOrg + "/projects/" + testProject + "/agents/" + testAgent
	for base, prefix := range map[string]string{
		"https://bma.test": "", "https://bma.test/": "", "https://bma.test/api/v1": "", "https://bma.test/api/v1/": "",
		"https://gw.test/bma": "/bma",
	} {
		s := &stub{replies: []reply{respond(200, `{"agent":{}}`)}}
		client := bma.NewClient(option.WithToken("t"), option.WithBaseURL(base), option.WithOrg(testOrg), option.WithProject(testProject),
			option.WithHTTPClient(&http.Client{Transport: s}))
		if _, err := client.Agents.Get(context.Background(), testAgent); err != nil {
			t.Fatal(base, err)
		}
		if s.calls[0].path != prefix+want {
			t.Fatalf("%s: path = %s", base, s.calls[0].path)
		}
	}
}

func TestListsWithNextParamPaginate(t *testing.T) {
	client, s := newClient(t, []reply{
		respond(200, `{"data":[{"event_kind":"model_output","sequence":1},{"event_kind":"model_output","sequence":2}],"next_after_sequence":2,"next_before_sequence":null,"has_more":true}`),
		respond(200, `{"data":[{"event_kind":"model_output","sequence":3}],"next_after_sequence":3,"next_before_sequence":null,"has_more":false}`),
		respond(200, `{"data":[{"event_kind":"model_output","sequence":9}],"next_after_sequence":9,"next_before_sequence":8,"has_more":true}`),
		respond(200, `{"data":[{"event_kind":"model_output","sequence":8}],"next_after_sequence":8,"next_before_sequence":null,"has_more":false}`),
		respond(200, `{"data":[{"id":"ses_1"}],"next_before_id":"ses_1"}`),
		respond(200, `{"data":[],"next_before_id":null}`),
	})
	forward := client.Agents.Events.ListAutoPaging(context.Background(), testAgent, bma.AgentEventListParams{SessionID: bma.Ptr(testSession)})
	n := 0
	for forward.Next() {
		n++
	}
	if forward.Err() != nil || n != 3 || s.calls[1].query["after_sequence"][0] != "2" {
		t.Fatalf("forward n=%d err=%v", n, forward.Err())
	}
	backward := client.Agents.Events.ListAutoPaging(context.Background(), testAgent, bma.AgentEventListParams{BeforeSequence: bma.Ptr(int64(0))})
	n = 0
	for backward.Next() {
		n++
	}
	if backward.Err() != nil || n != 2 || s.calls[3].query["before_sequence"][0] != "8" {
		t.Fatalf("backward n=%d err=%v", n, backward.Err())
	}
	sessions := client.Agents.Sessions.ListAutoPaging(context.Background(), testAgent, bma.AgentSessionListParams{})
	for sessions.Next() {
	}
	if sessions.Err() != nil || s.calls[5].query["before_id"][0] != "ses_1" {
		t.Fatalf("sessions err=%v", sessions.Err())
	}
}
