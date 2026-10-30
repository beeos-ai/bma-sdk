package rest

import (
	"bytes"
	"context"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"io"
	"net/http"
	"net/http/httptest"
	"reflect"
	"strings"
	"testing"
)

func newTestClient(t *testing.T, handler http.HandlerFunc) (*Client, *httptest.Server) {
	t.Helper()
	server := httptest.NewServer(handler)
	t.Cleanup(server.Close)
	client, err := New(Options{BaseURL: server.URL, Token: "test_token"})
	if err != nil {
		t.Fatalf("New: %v", err)
	}
	return client, server
}

func writeJSON(t *testing.T, w http.ResponseWriter, status int, body string) {
	t.Helper()
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	if _, err := io.WriteString(w, body); err != nil {
		t.Errorf("write response: %v", err)
	}
}

func TestNewValidation(t *testing.T) {
	if _, err := New(Options{}); err == nil {
		t.Fatal("expected missing token error")
	}
	if _, err := New(Options{Token: "t", BaseURL: "ftp://example.com"}); err == nil {
		t.Fatal("expected invalid scheme error")
	}
	client, err := New(Options{Token: "t"})
	if err != nil {
		t.Fatalf("New defaults: %v", err)
	}
	if client.Server() != DefaultBaseURL {
		t.Fatalf("server = %q, want %q", client.Server(), DefaultBaseURL)
	}
}

// TestGeneratedOperationCoverage pins the generated methods used by the
// Beework BMA transport and by the previous hand-written REST surface.
func TestGeneratedOperationCoverage(t *testing.T) {
	operations := map[string]any{
		"CreateAgent":                   (*ClientWithResponses).CreateAgentWithResponse,
		"GetAgent":                      (*ClientWithResponses).GetAgentWithResponse,
		"CreateAgentInput":              (*ClientWithResponses).CreateAgentInputWithResponse,
		"CancelAgent":                   (*ClientWithResponses).CancelAgentWithResponse,
		"ArchiveAgent":                  (*ClientWithResponses).ArchiveAgentWithResponse,
		"ListAgentInteractions":         (*ClientWithResponses).ListAgentInteractionsWithResponse,
		"ResolveAgentInteraction":       (*ClientWithResponses).ResolveAgentInteractionWithResponse,
		"ListEvents":                    (*ClientWithResponses).ListEventsWithResponse,
		"ListTurns":                     (*ClientWithResponses).ListTurnsWithResponse,
		"ListTurnEvents":                (*ClientWithResponses).ListTurnEventsWithResponse,
		"StreamEvents":                  (*ClientWithResponses).StreamEventsWithResponse,
		"ListToolCalls":                 (*ClientWithResponses).ListToolCallsWithResponse,
		"SubmitToolCallResult":          (*ClientWithResponses).SubmitToolCallResultWithResponse,
		"GetArtifact":                   (*ClientWithResponses).GetArtifactWithResponse,
		"GetArtifactContent":            (*ClientWithResponses).GetArtifactContentWithResponse,
		"ListAgents":                    (*ClientWithResponses).ListAgentsWithResponse,
		"ListQueuedBacklogInputs":       (*ClientWithResponses).ListQueuedBacklogInputsWithResponse,
		"CancelQueuedBacklogInput":      (*ClientWithResponses).CancelQueuedBacklogInputWithResponse,
		"MoveQueuedBacklogInput":        (*ClientWithResponses).MoveQueuedBacklogInputWithResponse,
		"PromoteQueuedInputToSteering":  (*ClientWithResponses).PromoteQueuedInputToSteeringWithResponse,
		"DemoteSteeringInputToQueued":   (*ClientWithResponses).DemoteSteeringInputToQueuedWithResponse,
		"CreateProject":                 (*ClientWithResponses).CreateProjectWithResponse,
		"CreateSecret":                  (*ClientWithResponses).CreateSecretWithResponse,
		"CreateSecretVersion":           (*ClientWithResponses).CreateSecretVersionWithResponse,
		"CreateModelProviderConfig":     (*ClientWithResponses).CreateModelProviderConfigWithResponse,
		"CreateConfiguredModel":         (*ClientWithResponses).CreateConfiguredModelWithResponse,
		"CreateProjectModelGrant":       (*ClientWithResponses).CreateProjectModelGrantWithResponse,
		"DeleteProjectModelGrant":       (*ClientWithResponses).DeleteProjectModelGrantWithResponse,
		"DeleteConfiguredModel":         (*ClientWithResponses).DeleteConfiguredModelWithResponse,
		"DeleteModelProviderConfig":     (*ClientWithResponses).DeleteModelProviderConfigWithResponse,
		"DeleteSecret":                  (*ClientWithResponses).DeleteSecretWithResponse,
		"CreateProjectMachinePoolGrant": (*ClientWithResponses).CreateProjectMachinePoolGrantWithResponse,
	}
	if len(operations) < 21 {
		t.Fatalf("coverage table has %d operations, want at least 21", len(operations))
	}
}

type operationCase struct {
	name    string
	method  string
	path    string
	status  int
	headers map[string]string
	call    func(context.Context, *Client) (*http.Response, error)
}

func TestGeneratedOperations(t *testing.T) {
	const (
		org  = "org_1"
		proj = "proj_1"
		agt  = "agt_1"
	)
	cases := []operationCase{
		{"CreateAgent", http.MethodPost, "/orgs/org_1/projects/proj_1/agents", http.StatusCreated, map[string]string{"Idempotency-Key": "launch-1"}, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.CreateAgentWithResponse(ctx, org, proj, &CreateAgentParams{IdempotencyKey: ptr(IdempotencyKey("launch-1"))}, CreateAgentJSONRequestBody{})
			if err != nil {
				return nil, err
			}
			if r.JSON201 == nil {
				return nil, errors.New("missing 201 launch response")
			}
			return r.HTTPResponse, nil
		}},
		{"ListAgents", http.MethodGet, "/orgs/org_1/projects/proj_1/agents", http.StatusOK, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.ListAgentsWithResponse(ctx, org, proj, &ListAgentsParams{})
			return response(r, err)
		}},
		{"GetAgent", http.MethodGet, "/orgs/org_1/projects/proj_1/agents/agt_1", http.StatusOK, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.GetAgentWithResponse(ctx, org, proj, agt)
			return response(r, err)
		}},
		{"ArchiveAgent", http.MethodPost, "/orgs/org_1/projects/proj_1/agents/agt_1/archive", http.StatusOK, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.ArchiveAgentWithResponse(ctx, org, proj, agt)
			return response(r, err)
		}},
		{"CancelAgent", http.MethodPost, "/orgs/org_1/projects/proj_1/agents/agt_1/cancel", http.StatusOK, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.CancelAgentWithResponse(ctx, org, proj, agt, CancelAgentJSONRequestBody{})
			return response(r, err)
		}},
		{"CreateAgentInput", http.MethodPost, "/orgs/org_1/projects/proj_1/agents/agt_1/inputs", http.StatusCreated, map[string]string{"Idempotency-Key": "input-1"}, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.CreateAgentInputWithResponse(ctx, org, proj, agt, &CreateAgentInputParams{IdempotencyKey: ptr(IdempotencyKey("input-1"))}, CreateAgentInputJSONRequestBody{
				ContentBlocks: []CreateAgentInputContentBlock{NewTextInputBlock("hello")},
			})
			return response(r, err)
		}},
		{"ListQueuedBacklogInputs", http.MethodGet, "/orgs/org_1/projects/proj_1/agents/agt_1/inputs/backlog", http.StatusOK, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.ListQueuedBacklogInputsWithResponse(ctx, org, proj, agt, &ListQueuedBacklogInputsParams{})
			return response(r, err)
		}},
		{"CancelQueuedBacklogInput", http.MethodPost, "/orgs/org_1/projects/proj_1/agents/agt_1/inputs/ain_1/cancel", http.StatusOK, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.CancelQueuedBacklogInputWithResponse(ctx, org, proj, agt, "ain_1")
			return response(r, err)
		}},
		{"MoveQueuedBacklogInput", http.MethodPost, "/orgs/org_1/projects/proj_1/agents/agt_1/inputs/ain_1/move", http.StatusOK, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.MoveQueuedBacklogInputWithResponse(ctx, org, proj, agt, "ain_1", MoveQueuedBacklogInputJSONRequestBody{})
			return response(r, err)
		}},
		{"PromoteQueuedInputToSteering", http.MethodPost, "/orgs/org_1/projects/proj_1/agents/agt_1/inputs/ain_1/promote_to_steering", http.StatusOK, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.PromoteQueuedInputToSteeringWithResponse(ctx, org, proj, agt, "ain_1", PromoteQueuedInputToSteeringJSONRequestBody{})
			return response(r, err)
		}},
		{"DemoteSteeringInputToQueued", http.MethodPost, "/orgs/org_1/projects/proj_1/agents/agt_1/inputs/ain_1/demote_to_queued", http.StatusOK, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.DemoteSteeringInputToQueuedWithResponse(ctx, org, proj, agt, "ain_1")
			return response(r, err)
		}},
		{"ListEvents", http.MethodGet, "/orgs/org_1/projects/proj_1/agents/agt_1/events", http.StatusOK, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.ListEventsWithResponse(ctx, org, proj, agt, &ListEventsParams{})
			return response(r, err)
		}},
		{"ListTurns", http.MethodGet, "/orgs/org_1/projects/proj_1/agents/agt_1/turns", http.StatusOK, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.ListTurnsWithResponse(ctx, org, proj, agt, &ListTurnsParams{})
			return response(r, err)
		}},
		{"ListTurnEvents", http.MethodGet, "/orgs/org_1/projects/proj_1/agents/agt_1/turns/trn_1/events", http.StatusOK, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.ListTurnEventsWithResponse(ctx, org, proj, agt, "trn_1", &ListTurnEventsParams{})
			return response(r, err)
		}},
		{"ListAgentInteractions", http.MethodGet, "/orgs/org_1/projects/proj_1/agents/agt_1/interactions", http.StatusOK, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.ListAgentInteractionsWithResponse(ctx, org, proj, agt, &ListAgentInteractionsParams{})
			return response(r, err)
		}},
		{"ResolveAgentInteraction", http.MethodPost, "/orgs/org_1/projects/proj_1/agents/agt_1/interactions/int_1/resolve", http.StatusOK, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.ResolveAgentInteractionWithResponse(ctx, org, proj, agt, "int_1", ResolveAgentInteractionJSONRequestBody{})
			return response(r, err)
		}},
		{"ListToolCalls", http.MethodGet, "/orgs/org_1/projects/proj_1/agents/agt_1/tool-calls", http.StatusOK, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.ListToolCallsWithResponse(ctx, org, proj, agt, &ListToolCallsParams{})
			return response(r, err)
		}},
		{"SubmitToolCallResult", http.MethodPost, "/orgs/org_1/projects/proj_1/agents/agt_1/tool-calls/tcl_1/result", http.StatusOK, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.SubmitToolCallResultWithResponse(ctx, org, proj, agt, "tcl_1", SubmitToolCallResultJSONRequestBody{})
			return response(r, err)
		}},
		{"GetArtifact", http.MethodGet, "/orgs/org_1/projects/proj_1/agents/agt_1/artifacts/art_1", http.StatusOK, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.GetArtifactWithResponse(ctx, org, proj, agt, "art_1")
			return response(r, err)
		}},
		{"GetArtifactContent", http.MethodGet, "/orgs/org_1/projects/proj_1/agents/agt_1/artifacts/art_1/content", http.StatusOK, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.GetArtifactContentWithResponse(ctx, org, proj, agt, "art_1")
			if err != nil {
				return nil, err
			}
			return r.HTTPResponse, nil
		}},
		{"CreateProject", http.MethodPost, "/orgs/org_1/projects", http.StatusOK, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.CreateProjectWithResponse(ctx, org, &CreateProjectParams{}, CreateProjectJSONRequestBody{})
			return response(r, err)
		}},
		{"CreateSecret", http.MethodPost, "/orgs/org_1/secrets", http.StatusOK, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.CreateSecretWithResponse(ctx, org, CreateSecretJSONRequestBody{})
			return response(r, err)
		}},
		{"CreateSecretVersion", http.MethodPost, "/orgs/org_1/secrets/sec_1/versions", http.StatusOK, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.CreateSecretVersionWithResponse(ctx, org, "sec_1", CreateSecretVersionJSONRequestBody{})
			return response(r, err)
		}},
		{"CreateModelProviderConfig", http.MethodPost, "/orgs/org_1/model-provider-configs", http.StatusOK, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.CreateModelProviderConfigWithResponse(ctx, org, CreateModelProviderConfigJSONRequestBody{})
			return response(r, err)
		}},
		{"CreateConfiguredModel", http.MethodPost, "/orgs/org_1/model-provider-configs/mpc_1/models", http.StatusOK, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.CreateConfiguredModelWithResponse(ctx, org, "mpc_1", CreateConfiguredModelJSONRequestBody{})
			return response(r, err)
		}},
		{"CreateProjectModelGrant", http.MethodPost, "/orgs/org_1/projects/proj_1/model-grants", http.StatusOK, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.CreateProjectModelGrantWithResponse(ctx, org, proj, CreateProjectModelGrantJSONRequestBody{})
			return response(r, err)
		}},
		{"DeleteProjectModelGrant", http.MethodDelete, "/orgs/org_1/projects/proj_1/model-grants/mgr_1", http.StatusNoContent, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.DeleteProjectModelGrantWithResponse(ctx, org, proj, "mgr_1")
			return response(r, err)
		}},
		{"DeleteConfiguredModel", http.MethodDelete, "/orgs/org_1/model-provider-configs/mpc_1/models/mdl_1", http.StatusNoContent, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.DeleteConfiguredModelWithResponse(ctx, org, "mpc_1", "mdl_1")
			return response(r, err)
		}},
		{"DeleteModelProviderConfig", http.MethodDelete, "/orgs/org_1/model-provider-configs/mpc_1", http.StatusNoContent, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.DeleteModelProviderConfigWithResponse(ctx, org, "mpc_1")
			return response(r, err)
		}},
		{"DeleteSecret", http.MethodDelete, "/orgs/org_1/secrets/sec_1", http.StatusNoContent, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.DeleteSecretWithResponse(ctx, org, "sec_1")
			return response(r, err)
		}},
		{"CreateProjectMachinePoolGrant", http.MethodPost, "/orgs/org_1/projects/proj_1/machine-pool-grants", http.StatusOK, nil, func(ctx context.Context, c *Client) (*http.Response, error) {
			r, err := c.CreateProjectMachinePoolGrantWithResponse(ctx, org, proj, &CreateProjectMachinePoolGrantParams{}, CreateProjectMachinePoolGrantJSONRequestBody{})
			return response(r, err)
		}},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			client, _ := newTestClient(t, func(w http.ResponseWriter, r *http.Request) {
				if r.Method != tc.method {
					t.Errorf("method = %s, want %s", r.Method, tc.method)
				}
				if r.URL.Path != tc.path {
					t.Errorf("path = %s, want %s", r.URL.Path, tc.path)
				}
				if got := r.Header.Get("Authorization"); got != "Bearer test_token" {
					t.Errorf("authorization = %q", got)
				}
				if got := r.Header.Get("User-Agent"); !strings.HasPrefix(got, "bma-sdks-go/") {
					t.Errorf("user agent = %q", got)
				}
				for key, want := range tc.headers {
					if got := r.Header.Get(key); got != want {
						t.Errorf("%s = %q, want %q", key, got, want)
					}
				}
				if tc.status == http.StatusNoContent {
					w.WriteHeader(tc.status)
					return
				}
				writeJSON(t, w, tc.status, `{}`)
			})
			resp, err := tc.call(context.Background(), client)
			if err != nil {
				t.Fatalf("%s: %v", tc.name, err)
			}
			if resp.StatusCode != tc.status {
				t.Fatalf("status = %d, want %d", resp.StatusCode, tc.status)
			}
		})
	}
}

func response(value any, err error) (*http.Response, error) {
	if err != nil {
		return nil, err
	}
	structValue := reflect.ValueOf(value)
	if structValue.Kind() == reflect.Pointer {
		structValue = structValue.Elem()
	}
	if structValue.Kind() != reflect.Struct {
		return nil, errors.New("response is not a struct")
	}
	field := structValue.FieldByName("HTTPResponse")
	if !field.IsValid() {
		return nil, errors.New("response has no HTTPResponse field")
	}
	resp, ok := field.Interface().(*http.Response)
	if !ok || resp == nil {
		return nil, errors.New("response has no HTTP response")
	}
	return resp, nil
}

func TestOpenEventStream(t *testing.T) {
	client, _ := newTestClient(t, func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/orgs/org_1/projects/proj_1/agents/agt_1/events/stream" {
			t.Errorf("path = %s", r.URL.Path)
		}
		if got := r.Header.Get("Accept"); got != "text/event-stream" {
			t.Errorf("accept = %q", got)
		}
		if got := r.Header.Get("Last-Event-ID"); got != "7" {
			t.Errorf("last event id = %q", got)
		}
		w.Header().Set("Content-Type", "text/event-stream")
		_, _ = io.WriteString(w, ": keepalive\n\n")
		_, _ = io.WriteString(w, "event: agent_input\nid: 8\ndata: {\"id\":\"evt_1\"}\n\n")
		_, _ = io.WriteString(w, "event: tool_call_update\nid: 9\ndata: {\"tool_call_id\":\"tcl_1\",\"state\":\"running\"}\n\n")
		_, _ = io.WriteString(w, "event: error\ndata: {\"code\":\"service_unavailable\",\"error\":\"retry\"}\n\n")
	})

	stream, err := client.OpenEventStream(context.Background(), "org_1", "proj_1", "agt_1", &StreamEventsParams{
		StreamDeltas: ptr(true),
		LastEventID:  ptr(int64(7)),
	})
	if err != nil {
		t.Fatalf("OpenEventStream: %v", err)
	}
	defer stream.Close()

	frame, err := stream.Next()
	if err != nil {
		t.Fatalf("Next: %v", err)
	}
	if frame.Event != "agent_input" || frame.Sequence != 8 || frame.AgentEvent == nil {
		t.Fatalf("frame = %+v", frame)
	}
	if _, err := frame.AgentEvent.AsAgentInputEvent(); err != nil {
		t.Fatalf("AsAgentInputEvent: %v", err)
	}

	frame, err = stream.Next()
	if err != nil {
		t.Fatalf("Next: %v", err)
	}
	if frame.ToolCallUpdate == nil || frame.ToolCallUpdate.ToolCallId != "tcl_1" {
		t.Fatalf("tool call frame = %+v", frame.ToolCallUpdate)
	}

	frame, err = stream.Next()
	if err != nil {
		t.Fatalf("Next: %v", err)
	}
	if frame.Error == nil || frame.Error.Code != ErrorCodeServiceUnavailable || !frame.Error.Retryable() {
		t.Fatalf("error frame = %+v", frame.Error)
	}
}

func TestDownloadArtifact(t *testing.T) {
	payload := []byte("artifact-bytes")
	sum := sha256.Sum256(payload)
	digest := "sha256:" + hex.EncodeToString(sum[:])

	client, _ := newTestClient(t, func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/orgs/org_1/projects/proj_1/agents/agt_1/artifacts/art_1/content" {
			t.Errorf("path = %s", r.URL.Path)
		}
		if got := r.Header.Get("Accept"); got != "application/octet-stream" {
			t.Errorf("accept = %q", got)
		}
		w.Header().Set("Content-Type", "application/octet-stream")
		_, _ = w.Write(payload)
	})

	artifact := Artifact{
		Id:        "art_1",
		OrgId:     "org_1",
		ProjectId: "proj_1",
		AgentId:   "agt_1",
		SizeBytes: ptr(int64(len(payload))),
		Digest:    ptr(digest),
	}
	var out bytes.Buffer
	if err := client.DownloadArtifact(context.Background(), artifact, int64(len(payload)), &out); err != nil {
		t.Fatalf("DownloadArtifact: %v", err)
	}
	if !bytes.Equal(out.Bytes(), payload) {
		t.Fatalf("artifact = %q", out.Bytes())
	}

	bad := artifact
	bad.Digest = ptr("sha256:" + strings.Repeat("00", sha256.Size))
	out.Reset()
	if err := client.DownloadArtifact(context.Background(), bad, int64(len(payload)), &out); err == nil {
		t.Fatal("expected digest mismatch")
	}
}

func TestAPIError(t *testing.T) {
	client, _ := newTestClient(t, func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusTooManyRequests)
		_ = json.NewEncoder(w).Encode(map[string]string{"code": "rate_limited", "error": "slow down"})
	})
	resp, err := client.ListAgentsWithResponse(context.Background(), "org_1", "proj_1", &ListAgentsParams{})
	if err != nil {
		t.Fatalf("ListAgentsWithResponse: %v", err)
	}
	err = CheckResponse(resp.HTTPResponse, resp.Body)
	var apiErr *APIError
	if !errors.As(err, &apiErr) {
		t.Fatalf("error = %v, want *APIError", err)
	}
	if apiErr.Code != ErrorCodeRateLimited || !apiErr.Retryable() {
		t.Fatalf("api error = %+v", apiErr)
	}
}

func ptr[T any](v T) *T { return &v }
