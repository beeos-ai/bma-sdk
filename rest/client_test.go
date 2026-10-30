package bmarest

import (
	"context"
	"encoding/base64"
	"encoding/json"
	"errors"
	"io"
	"net/http"
	"net/http/httptest"
	"testing"
)

func newTestClient(t *testing.T, handler http.HandlerFunc) *Client {
	t.Helper()
	server := httptest.NewServer(handler)
	t.Cleanup(server.Close)
	client, err := NewClient(Options{BaseURL: server.URL, Token: "test_token"})
	if err != nil {
		t.Fatalf("NewClient: %v", err)
	}
	return client
}

func TestNewClientValidation(t *testing.T) {
	if _, err := NewClient(Options{}); err == nil {
		t.Fatal("expected missing token error")
	}
	if _, err := NewClient(Options{Token: "t", BaseURL: "ftp://example.com"}); err == nil {
		t.Fatal("expected invalid scheme error")
	}
	client, err := NewClient(Options{Token: "t"})
	if err != nil {
		t.Fatalf("NewClient defaults: %v", err)
	}
	if client.baseURL != DefaultBaseURL {
		t.Fatalf("base URL = %q, want %q", client.baseURL, DefaultBaseURL)
	}
}

func TestCreateAgent(t *testing.T) {
	client := newTestClient(t, func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			t.Errorf("method = %s", r.Method)
		}
		if r.URL.Path != "/orgs/org_1/projects/proj_1/agents" {
			t.Errorf("path = %s", r.URL.Path)
		}
		if got := r.Header.Get("Authorization"); got != "Bearer test_token" {
			t.Errorf("authorization = %q", got)
		}
		if got := r.Header.Get("Idempotency-Key"); got != "launch-1" {
			t.Errorf("idempotency key = %q", got)
		}
		if got := r.Header.Get("Content-Type"); got != "application/json" {
			t.Errorf("content type = %q", got)
		}
		var request CreateAgentRequest
		if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
			t.Errorf("decode request: %v", err)
		}
		if request.Profile != "aprf_1" || request.Name == nil || *request.Name != "Beework" {
			t.Errorf("request = %+v", request)
		}
		if request.InitialInput == nil || len(request.InitialInput.ContentBlocks) != 1 || request.InitialInput.ContentBlocks[0].Text == nil {
			t.Errorf("initial input = %+v", request.InitialInput)
		}
		writeJSON(t, w, http.StatusCreated, `{
			"agent": {
				"id": "agt_1", "org_id": "org_1", "project_id": "proj_1",
				"state": "active", "name": "Beework",
				"created_at": "2026-10-30T12:00:00Z", "updated_at": "2026-10-30T12:00:01Z"
			},
			"agent_config": {
				"id": "acfg_1", "org_id": "org_1", "project_id": "proj_1",
				"effective_definition_hash": "sha256:abc", "created_at": "2026-10-30T12:00:00Z"
			},
			"machine_bindings": []
		}`)
	})

	response, err := client.CreateAgent(context.Background(), ProjectScope{OrgID: "org_1", ProjectID: "proj_1"}, CreateAgentRequest{
		Profile:      "aprf_1",
		Name:         stringPtr("Beework"),
		InitialInput: &AgentLaunchInitialInput{ContentBlocks: []ContentBlock{TextBlock("hello")}},
	}, RequestOptions{IdempotencyKey: "launch-1"})
	if err != nil {
		t.Fatalf("CreateAgent: %v", err)
	}
	if response.Agent == nil || response.Agent.ID != "agt_1" || response.Agent.State != AgentStateActive {
		t.Fatalf("response agent = %+v", response.Agent)
	}
	if response.AgentConfig == nil || response.AgentConfig.ID != "acfg_1" {
		t.Fatalf("response config = %+v", response.AgentConfig)
	}
}

func TestCreateAgentInputEncodesMedia(t *testing.T) {
	media := []byte{0x89, 0x50, 0x4e, 0x47}
	client := newTestClient(t, func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/orgs/org_1/projects/proj_1/agents/agt_1/inputs" {
			t.Errorf("path = %s", r.URL.Path)
		}
		var request struct {
			ContentBlocks []map[string]any `json:"content_blocks"`
			DeliveryMode  string           `json:"delivery_mode"`
		}
		if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
			t.Errorf("decode request: %v", err)
		}
		if request.DeliveryMode != "steering" {
			t.Errorf("delivery mode = %q", request.DeliveryMode)
		}
		if len(request.ContentBlocks) != 2 {
			t.Errorf("content blocks = %d", len(request.ContentBlocks))
			return
		}
		if request.ContentBlocks[0]["type"] != "text" || request.ContentBlocks[0]["text"] != "hi" {
			t.Errorf("text block = %+v", request.ContentBlocks[0])
		}
		if request.ContentBlocks[1]["type"] != "media" {
			t.Errorf("media block = %+v", request.ContentBlocks[1])
		}
		if got, want := request.ContentBlocks[1]["data"], base64.StdEncoding.EncodeToString(media); got != want {
			t.Errorf("media data = %v, want %s", got, want)
		}
		writeJSON(t, w, http.StatusCreated, `{
			"agent_input": {
				"id": "ain_1", "agent_id": "agt_1", "state": "queued",
				"delivery_mode": "steering", "input_kind": "content",
				"queued_at": "2026-10-30T12:00:00Z"
			}
		}`)
	})

	envelope, err := client.CreateAgentInput(context.Background(), AgentScope{OrgID: "org_1", ProjectID: "proj_1", AgentID: "agt_1"}, CreateAgentInputRequest{
		ContentBlocks: []ContentBlock{TextBlock("hi"), MediaBlock("image/png", "pixel.png", media)},
		DeliveryMode:  AgentInputDeliverySteering,
	}, RequestOptions{IdempotencyKey: "input-1"})
	if err != nil {
		t.Fatalf("CreateAgentInput: %v", err)
	}
	if envelope.AgentInput == nil || envelope.AgentInput.ID != "ain_1" || envelope.AgentInput.DeliveryMode != AgentInputDeliverySteering {
		t.Fatalf("agent input = %+v", envelope.AgentInput)
	}
}

func TestListEventsDecodesContentBlocks(t *testing.T) {
	client := newTestClient(t, func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodGet {
			t.Errorf("method = %s", r.Method)
		}
		if r.URL.Path != "/orgs/org_1/projects/proj_1/agents/agt_1/events" {
			t.Errorf("path = %s", r.URL.Path)
		}
		query := r.URL.Query()
		if query.Get("after_sequence") != "41" || query.Get("limit") != "25" {
			t.Errorf("query = %s", r.URL.RawQuery)
		}
		if query.Has("before_sequence") {
			t.Errorf("unexpected before_sequence: %s", r.URL.RawQuery)
		}
		writeJSON(t, w, http.StatusOK, `{
			"data": [{
				"id": "evt_1", "org_id": "org_1", "project_id": "proj_1", "agent_id": "agt_1",
				"turn_id": "trn_1", "turn_sequence": 1, "is_opening_event": true,
				"sequence": 42, "event_kind": "agent_input", "agent_input_id": "ain_1",
				"input_kind": "content", "content_blocks": [{"type": "text", "text": "hi"}],
				"created_at": "2026-10-30T12:00:00Z"
			}],
			"next_after_sequence": 42,
			"next_before_sequence": null,
			"has_more": false
		}`)
	})

	response, err := client.ListEvents(context.Background(), AgentScope{OrgID: "org_1", ProjectID: "proj_1", AgentID: "agt_1"}, ListEventsOptions{AfterSequence: 41, Limit: 25})
	if err != nil {
		t.Fatalf("ListEvents: %v", err)
	}
	if len(response.Data) != 1 || response.Data[0].EventKind != AgentEventKindInput {
		t.Fatalf("events = %+v", response.Data)
	}
	if response.Data[0].ContentBlocks[0].Text == nil || *response.Data[0].ContentBlocks[0].Text != "hi" {
		t.Fatalf("content block = %+v", response.Data[0].ContentBlocks[0])
	}
	if response.NextAfterSequence != 42 || response.NextBeforeSequence != nil || response.HasMore {
		t.Fatalf("response = %+v", response)
	}
}

func TestAPIError(t *testing.T) {
	client := newTestClient(t, func(w http.ResponseWriter, r *http.Request) {
		writeJSON(t, w, http.StatusNotFound, `{"error": "agent not found", "code": "not_found"}`)
	})

	_, err := client.GetAgent(context.Background(), AgentScope{OrgID: "org_1", ProjectID: "proj_1", AgentID: "agt_missing"})
	if err == nil {
		t.Fatal("expected error")
	}
	var apiErr *APIError
	if !errors.As(err, &apiErr) {
		t.Fatalf("error type = %T: %v", err, err)
	}
	if apiErr.StatusCode != http.StatusNotFound || apiErr.Code != ErrorCodeNotFound || apiErr.Message != "agent not found" {
		t.Fatalf("api error = %+v", apiErr)
	}
	if apiErr.Retryable() {
		t.Fatal("not_found must not be retryable")
	}
}

func TestGetArtifactContent(t *testing.T) {
	body := []byte("pdf-bytes")
	client := newTestClient(t, func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/orgs/org_1/projects/proj_1/agents/agt_1/artifacts/art_1/content" {
			t.Errorf("path = %s", r.URL.Path)
		}
		w.Header().Set("Content-Type", "application/pdf")
		_, _ = w.Write(body)
	})

	content, err := client.GetArtifactContent(context.Background(), AgentScope{OrgID: "org_1", ProjectID: "proj_1", AgentID: "agt_1"}, "art_1")
	if err != nil {
		t.Fatalf("GetArtifactContent: %v", err)
	}
	defer content.Close()
	if content.ContentType != "application/pdf" {
		t.Fatalf("content type = %q", content.ContentType)
	}
	got, err := io.ReadAll(content.Body)
	if err != nil {
		t.Fatalf("read body: %v", err)
	}
	if string(got) != string(body) {
		t.Fatalf("body = %q", got)
	}
}

func TestStreamEvents(t *testing.T) {
	client := newTestClient(t, func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/orgs/org_1/projects/proj_1/agents/agt_1/events/stream" {
			t.Errorf("path = %s", r.URL.Path)
		}
		if got := r.Header.Get("Accept"); got != "text/event-stream" {
			t.Errorf("accept = %q", got)
		}
		if got := r.Header.Get("Last-Event-ID"); got != "6" {
			t.Errorf("last event id = %q", got)
		}
		if got := r.URL.Query().Get("stream_deltas"); got != "true" {
			t.Errorf("stream_deltas = %q", got)
		}
		w.Header().Set("Content-Type", "text/event-stream")
		_, _ = io.WriteString(w, ": heartbeat\n\n")
		_, _ = io.WriteString(w, "id: 7\nevent: model_output\n")
		_, _ = io.WriteString(w, `data: {"id":"evt_1","event_kind":"model_output","sequence":7,"content_blocks":[{"type":"tool_call","tool_call_id":"tcl_1","tool_type":"custom","name":"lookup","input":{"q":"x"}}]}`+"\n\n")
		_, _ = io.WriteString(w, "event: tool_call_update\n")
		_, _ = io.WriteString(w, `data: {"tool_call_id":"tcl_1",`+"\n")
		_, _ = io.WriteString(w, `data: "state":"running"}`+"\n\n")
		_, _ = io.WriteString(w, "event: model_output_delta\n")
		_, _ = io.WriteString(w, `data: {"turn_id":"trn_1","model_call_context_id":"mcc_1","seq":1,"source_seq_start":1,"source_seq_end":1,"coalesced_count":1,"event":{"kind":"text_delta","block_index":0,"delta":"Hel"}}`+"\n\n")
		_, _ = io.WriteString(w, "event: error\n")
		_, _ = io.WriteString(w, `data: {"error":"try later","code":"service_unavailable"}`+"\n\n")
	})

	stream, err := client.StreamEvents(context.Background(), AgentScope{OrgID: "org_1", ProjectID: "proj_1", AgentID: "agt_1"}, StreamEventsOptions{LastEventID: 6, StreamDeltas: true})
	if err != nil {
		t.Fatalf("StreamEvents: %v", err)
	}
	defer stream.Close()

	frame, err := stream.Next()
	if err != nil {
		t.Fatalf("Next event: %v", err)
	}
	if frame.Event != "model_output" || frame.ID != "7" || frame.AgentEvent == nil || frame.AgentEvent.Sequence != 7 {
		t.Fatalf("event frame = %+v", frame)
	}
	if len(frame.AgentEvent.ContentBlocks) != 1 || frame.AgentEvent.ContentBlocks[0].ToolCallID != "tcl_1" {
		t.Fatalf("content blocks = %+v", frame.AgentEvent.ContentBlocks)
	}

	frame, err = stream.Next()
	if err != nil {
		t.Fatalf("Next update: %v", err)
	}
	if frame.ToolCallUpdate == nil || frame.ToolCallUpdate.ToolCallID != "tcl_1" || frame.ToolCallUpdate.State != ToolCallStateRunning {
		t.Fatalf("update frame = %+v", frame)
	}

	frame, err = stream.Next()
	if err != nil {
		t.Fatalf("Next delta: %v", err)
	}
	if frame.ModelOutputDelta == nil || frame.ModelOutputDelta.Event.Kind != "text_delta" || frame.ModelOutputDelta.Event.Delta != "Hel" {
		t.Fatalf("delta frame = %+v", frame)
	}

	frame, err = stream.Next()
	if err != nil {
		t.Fatalf("Next error: %v", err)
	}
	if frame.Error == nil || frame.Error.Code != ErrorCodeServiceUnavailable || !frame.Error.Retryable() {
		t.Fatalf("error frame = %+v", frame)
	}

	if _, err := stream.Next(); !errors.Is(err, io.EOF) {
		t.Fatalf("stream end = %v", err)
	}
}

func TestCancelAgentWithNoBody(t *testing.T) {
	client := newTestClient(t, func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/orgs/org_1/projects/proj_1/agents/agt_1/cancel" {
			t.Errorf("path = %s", r.URL.Path)
		}
		if r.ContentLength != 0 {
			t.Errorf("content length = %d", r.ContentLength)
		}
		writeJSON(t, w, http.StatusOK, `{"event": null, "runtime_cancel_requested": false, "affected": false}`)
	})

	response, err := client.CancelAgent(context.Background(), AgentScope{OrgID: "org_1", ProjectID: "proj_1", AgentID: "agt_1"}, nil)
	if err != nil {
		t.Fatalf("CancelAgent: %v", err)
	}
	if response.Affected || response.Event != nil {
		t.Fatalf("response = %+v", response)
	}
}

func writeJSON(t *testing.T, w http.ResponseWriter, status int, body string) {
	t.Helper()
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_, _ = io.WriteString(w, body)
}

func stringPtr(value string) *string {
	return &value
}
