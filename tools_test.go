package bma_test

// bma.DefineTool + Agents.ToolCalls.Runner (ADR 0012 D7); mirrors
// typescript/test/tools.test.ts.

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"regexp"
	"strings"
	"sync"
	"testing"
	"time"

	"github.com/beeos-ai/bma-sdk"
	"github.com/beeos-ai/bma-sdk/option"
)

type weatherInput struct {
	City string `json:"city"`
}

var weather = bma.DefineTool("get_weather", "Current weather",
	map[string]any{"type": "object", "properties": map[string]any{"city": map[string]any{"type": "string"}}, "required": []string{"city"}},
	func(ctx context.Context, in weatherInput, call bma.ToolCall) (bma.ToolContent, error) {
		if in.City == "" {
			return nil, bma.ToolError("invalid input for get_weather: city is required")
		}
		if in.City == "Atlantis" {
			return nil, bma.ToolError("no such city")
		}
		return bma.ToolText("Sunny in " + in.City), nil
	})

func toolCallJSON(id, name, input, agent string) string {
	return fmt.Sprintf(`{"id":%q,"agent_id":%q,"session_id":%q,"turn_id":"turn_1","provider_call_id":"p","name":%q,"input":%s,"type":"custom","state":"ready","created_at":"2026-11-06T00:00:00Z"}`,
		id, agent, testSession, name, input)
}

func TestDefineToolDefinition(t *testing.T) {
	def := weather.Definition()
	raw, _ := json.Marshal(def)
	if !strings.Contains(string(raw), `"type":"custom"`) || !strings.Contains(string(raw), `"required":["city"]`) {
		t.Fatalf("definition = %s", raw)
	}
}

func TestToolRunner(t *testing.T) {
	const sub = "agt_bbbbbbbbbbbbbbbbbbbbbbbbbb"
	var mu sync.Mutex
	submitted := map[string]map[string]any{}
	base := "/v1/orgs/" + testOrg + "/projects/" + testProject + "/agents"
	resultPath := regexp.MustCompile(`/agents/(agt_\w+)/tool-calls/(tc_\d)/result$`)
	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		p := r.URL.Path
		switch {
		case p == base+"/"+testAgent+"/events/stream":
			w.Header().Set("Content-Type", "text/event-stream")
			for _, d := range []string{`{"tool_call_id":"tc_2","agent_id":"` + sub + `","state":"ready"}`, `{"tool_call_id":"tc_3","state":"ready"}`, `{"tool_call_id":"tc_4","state":"running"}`} {
				fmt.Fprintf(w, "event: tool_call_update\ndata: %s\n\n", d)
			}
		case p == base+"/"+testAgent+"/tool-calls":
			if r.URL.Query().Get("state") != "ready" || r.URL.Query().Get("type") != "custom" {
				t.Errorf("list query = %v", r.URL.Query())
			}
			fmt.Fprintf(w, `{"data":[%s,%s],"next_cursor":null}`, toolCallJSON("tc_1", "get_weather", `{"city":"Paris"}`, testAgent), toolCallJSON("tc_9", "other", `{}`, testAgent))
		case p == base+"/"+sub+"/tool-calls/tc_2":
			fmt.Fprintf(w, `{"tool_call":%s}`, toolCallJSON("tc_2", "get_weather", `{"city":"Atlantis"}`, sub))
		case p == base+"/"+testAgent+"/tool-calls/tc_3":
			fmt.Fprintf(w, `{"tool_call":%s}`, toolCallJSON("tc_3", "get_weather", `{"town":1}`, testAgent))
		case resultPath.MatchString(p) && r.Method == "POST":
			m := resultPath.FindStringSubmatch(p)
			raw, _ := io.ReadAll(r.Body)
			var body map[string]any
			_ = json.Unmarshal(raw, &body)
			body["agent"] = m[1]
			mu.Lock()
			submitted[m[2]] = body
			mu.Unlock()
			w.WriteHeader(201)
			fmt.Fprint(w, `{"tool_call":{},"tool_result":{}}`)
		default:
			t.Errorf("unexpected %s %s", r.Method, p)
			w.WriteHeader(500)
		}
	})
	client := bma.NewClient(option.WithToken("t"), option.WithBaseURL("https://bma.test/v1"), option.WithOrg(testOrg), option.WithProject(testProject),
		option.WithHTTPClient(&http.Client{Transport: handlerTransport{handler}}))
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	go func() { // the runner runs until canceled; stop it once all three are in
		for {
			mu.Lock()
			n := len(submitted)
			mu.Unlock()
			if n == 3 {
				cancel()
				return
			}
			time.Sleep(5 * time.Millisecond)
		}
	}()
	err := client.Agents.ToolCalls.Runner(testAgent, bma.ToolRunnerParams{SessionID: testSession, Tools: []bma.RunnableTool{weather}}).Run(ctx)
	if err != nil {
		t.Fatal(err)
	}
	text := func(id string) string {
		blocks := submitted[id]["content_blocks"].([]any)
		return blocks[0].(map[string]any)["text"].(string)
	}
	if submitted["tc_1"]["outcome"] != "succeeded" || text("tc_1") != "Sunny in Paris" || submitted["tc_1"]["agent"] != testAgent {
		t.Fatalf("tc_1 = %v", submitted["tc_1"])
	}
	if submitted["tc_2"]["outcome"] != "failed" || text("tc_2") != "no such city" || submitted["tc_2"]["agent"] != sub {
		t.Fatalf("tc_2 = %v", submitted["tc_2"])
	}
	if submitted["tc_3"]["outcome"] != "failed" || !strings.Contains(text("tc_3"), "invalid input for get_weather") {
		t.Fatalf("tc_3 = %v", submitted["tc_3"])
	}
	if len(submitted) != 3 {
		t.Fatalf("submitted = %v", submitted)
	}
}

func TestRunnerRejectsDuplicateNames(t *testing.T) {
	client := bma.NewClient(option.WithToken("t"), option.WithOrg(testOrg), option.WithProject(testProject))
	err := client.Agents.ToolCalls.Runner(testAgent, bma.ToolRunnerParams{Tools: []bma.RunnableTool{weather, weather}}).Run(context.Background())
	if err == nil || errors.Is(err, context.Canceled) {
		t.Fatalf("err = %v", err)
	}
}

type handlerTransport struct{ h http.Handler }

func (t handlerTransport) RoundTrip(r *http.Request) (*http.Response, error) {
	rec := newRecorder()
	t.h.ServeHTTP(rec, r)
	return rec.result(r), nil
}
