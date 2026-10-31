package rest_test

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"io"
	"testing"

	"github.com/beeos-ai/bma-sdks/go/internal/contracttest"
	bmarest "github.com/beeos-ai/bma-sdks/go/rest"
)

func ptr[T any](value T) *T { return &value }

// contractClient replays one recorded exchange from the shared fixtures.
func contractClient(t *testing.T, name string) (*bmarest.Client, contracttest.Case, map[string]string) {
	t.Helper()
	fixtures := contracttest.Load(t)
	c := contracttest.Find(t, fixtures.REST, name)
	server := contracttest.Serve(t, c, "/api/v1")
	client, err := bmarest.New(bmarest.Options{BaseURL: server.URL + "/api/v1", Token: "test-token"})
	if err != nil {
		t.Fatal(err)
	}
	return client, c, fixtures.Scope
}

func overrideInput() *bmarest.AgentModelOverrideInput {
	return &bmarest.AgentModelOverrideInput{
		Model: "deepseek-flash",
		Provider: &bmarest.AgentModelOverrideProvider{
			ApiFormat:    "openai-chat-completions",
			BaseUrl:      "https://llm.example.com",
			ApiVariant:   ptr(bmarest.AgentModelOverrideProviderApiVariant("default")),
			EndpointPath: ptr("/v1/chat/completions"),
		},
		ApiKey:             ptr("sk-test-0000000000"),
		TtlSeconds:         ptr(3600),
		ExpiresWithSession: ptr(true),
	}
}

func TestContractSessionLifecycle(t *testing.T) {
	ctx := context.Background()

	client, _, s := contractClient(t, "create_session")
	created, err := client.CreateAgentSessionWithResponse(ctx, s["org"], s["project"], s["agent"],
		bmarest.CreateAgentSessionJSONRequestBody{
			AgentConfigId:  ptr(s["config"]),
			IdempotencyKey: ptr("beework-task-1"),
			Metadata:       &map[string]any{"title": "Quarterly report"},
			ModelOverride:  overrideInput(),
		})
	if err != nil {
		t.Fatal(err)
	}
	if err := bmarest.CheckResponse(created.HTTPResponse, created.Body); err != nil {
		t.Fatal(err)
	}
	if created.JSON201 == nil || created.JSON201.Session.Id != s["session"] || created.JSON201.Session.ConfigOrigin != "session" {
		t.Fatalf("created = %+v", created.JSON201)
	}

	client, _, _ = contractClient(t, "get_session")
	got, err := client.GetAgentSessionWithResponse(ctx, s["org"], s["project"], s["agent"], s["session"])
	if err != nil || got.JSON200 == nil || got.JSON200.Session.NextEventSequence != 5 {
		t.Fatalf("get = %+v, %v", got, err)
	}

	client, _, _ = contractClient(t, "list_sessions")
	listed, err := client.ListAgentSessionsWithResponse(ctx, s["org"], s["project"], s["agent"],
		&bmarest.ListAgentSessionsParams{IncludeArchived: ptr(true), Limit: ptr(int32(10))})
	if err != nil || listed.JSON200 == nil || len(listed.JSON200.Data) != 1 || listed.JSON200.NextBeforeId != nil {
		t.Fatalf("list = %+v, %v", listed, err)
	}

	client, _, _ = contractClient(t, "archive_session")
	archived, err := client.ArchiveAgentSessionWithResponse(ctx, s["org"], s["project"], s["agent"], s["session"])
	if err != nil || archived.JSON200 == nil || archived.JSON200.Session.State != "archived" || archived.JSON200.Session.ArchivedAt == nil {
		t.Fatalf("archive = %+v, %v", archived, err)
	}

	client, _, _ = contractClient(t, "put_session_model_override")
	override, err := client.PutAgentSessionModelOverrideWithResponse(ctx, s["org"], s["project"], s["agent"], s["session"],
		*overrideInput())
	if err != nil || override.JSON200 == nil {
		t.Fatalf("override = %+v, %v", override, err)
	}
	if mo := override.JSON200.ModelOverride; !mo.ExpiresWithSession || mo.ExpiresAt != nil || mo.SessionId != s["session"] {
		t.Fatalf("override = %+v", mo)
	}
}

func TestContractSessionInputAndStream(t *testing.T) {
	ctx := context.Background()

	client, _, s := contractClient(t, "create_session_input")
	input, err := client.CreateAgentInputWithResponse(ctx, s["org"], s["project"], s["agent"],
		&bmarest.CreateAgentInputParams{SessionId: ptr(s["session"]), IdempotencyKey: ptr(bmarest.IdempotencyKey("turn-1"))},
		bmarest.CreateAgentInputJSONRequestBody{
			ContentBlocks: []bmarest.CreateAgentInputContentBlock{bmarest.NewTextInputBlock("Summarize the report.")},
			DeliveryMode:  ptr(bmarest.CreateAgentInputDeliveryMode("queued")),
		})
	if err != nil || input.JSON200 == nil || input.JSON200.AgentInput.State != "queued" {
		t.Fatalf("input = %+v, %v", input, err)
	}

	client, _, _ = contractClient(t, "stream_session_events")
	stream, err := client.OpenEventStream(ctx, s["org"], s["project"], s["agent"], &bmarest.StreamEventsParams{
		SessionId: ptr(s["session"]), StreamDeltas: ptr(true), LastEventID: ptr(int64(4)),
	})
	if err != nil {
		t.Fatal(err)
	}
	defer stream.Close()

	frame, err := stream.Next()
	if err != nil || frame.AgentEvent == nil || frame.Sequence != 5 {
		t.Fatalf("frame 1 = %+v, %v", frame, err)
	}
	if kind, _ := frame.AgentEvent.Discriminator(); kind != "agent_input" {
		t.Fatalf("frame 1 kind = %q", kind)
	}
	frame, err = stream.Next()
	if err != nil || frame.ToolCallUpdate == nil || frame.ToolCallUpdate.State != "running" {
		t.Fatalf("frame 2 = %+v, %v", frame, err)
	}
	frame, err = stream.Next()
	if err != nil || frame.Error == nil || !frame.Error.Retryable() {
		t.Fatalf("frame 3 = %+v, %v", frame, err)
	}
	if _, err := stream.Next(); !errors.Is(err, io.EOF) {
		t.Fatalf("end = %v", err)
	}
}

func TestContractArtifactDownload(t *testing.T) {
	fixtures := contracttest.Load(t)
	var artifact bmarest.Artifact
	if err := json.Unmarshal(contracttest.Find(t, fixtures.REST, "get_artifact").Response.JSON, &artifact); err != nil {
		t.Fatal(err)
	}
	client, c, _ := contractClient(t, "get_artifact_content")
	var out bytes.Buffer
	if err := client.DownloadArtifact(context.Background(), artifact, 1024, &out); err != nil {
		t.Fatal(err)
	}
	if out.String() != c.Response.Text {
		t.Fatalf("content = %q", out.String())
	}

	tampered := artifact
	tampered.Digest = ptr("sha256:" + string(bytes.Repeat([]byte("0"), 64)))
	client, _, _ = contractClient(t, "get_artifact_content")
	if err := client.DownloadArtifact(context.Background(), tampered, 1024, io.Discard); err == nil {
		t.Fatal("digest mismatch was accepted")
	}
}

func TestContractMachineDesktopAndTerminal(t *testing.T) {
	ctx := context.Background()

	client, _, s := contractClient(t, "create_desktop_session")
	desktop, err := client.CreateDesktopSessionWithResponse(ctx, s["org"], s["project"], s["machine"],
		bmarest.CreateDesktopSessionJSONRequestBody{AgentId: ptr(s["agent"]), ReadOnly: ptr(true)})
	if err != nil || desktop.JSON201 == nil || desktop.JSON201.Capabilities.Width != 1920 {
		t.Fatalf("desktop = %+v, %v", desktop, err)
	}

	client, _, _ = contractClient(t, "create_terminal_ticket")
	ticket, err := client.CreateTerminalConnectionTicketWithResponse(ctx, s["org"], s["project"], s["machine"], s["terminal_session"],
		bmarest.CreateTerminalConnectionTicketJSONRequestBody{TtlSeconds: ptr(int32(60))})
	if err != nil || ticket.JSON201 == nil || ticket.JSON201.Purpose != "terminal_connect" {
		t.Fatalf("ticket = %+v, %v", ticket, err)
	}

	client, _, _ = contractClient(t, "get_agent_not_found")
	missing, err := client.GetAgentWithResponse(ctx, s["org"], s["project"], "agt_zzzzzzzzzzzzzzzzzzzzzzzzzz")
	if err != nil {
		t.Fatal(err)
	}
	var apiErr *bmarest.APIError
	if err := bmarest.CheckResponse(missing.HTTPResponse, missing.Body); !errors.As(err, &apiErr) || apiErr.Code != bmarest.ErrorCodeNotFound {
		t.Fatalf("error = %v", err)
	}
}
