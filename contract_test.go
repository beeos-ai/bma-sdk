package bma_test

// Replays contracts/bma/fixtures/sdk-contract.json against the resource
// client; tools/check_contract.py validates the fixtures against the contract.

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"io"
	"strings"
	"testing"

	"github.com/beeos-ai/bma-sdk"
	"github.com/beeos-ai/bma-sdk/internal/contracttest"
	"github.com/beeos-ai/bma-sdk/option"
)

func contractClient(t *testing.T, name string) (*bma.Client, contracttest.Case, map[string]string) {
	t.Helper()
	fixtures := contracttest.Load(t)
	c := contracttest.Find(t, fixtures.REST, name)
	server := contracttest.Serve(t, c, "/api/v1")
	s := fixtures.Scope
	client := bma.NewClient(option.WithBaseURL(server.URL), option.WithToken("test-token"),
		option.WithOrg(s["org"]), option.WithProject(s["project"]), option.WithMaxRetries(0))
	return client, c, s
}

func overrideInput() *bma.AgentModelOverrideInput {
	return &bma.AgentModelOverrideInput{
		Model: "deepseek-flash",
		Provider: &bma.AgentModelOverrideProvider{
			APIFormat:    "openai-chat-completions",
			BaseURL:      "https://llm.example.com",
			APIVariant:   bma.Ptr(bma.AgentModelOverrideProviderAPIVariant("default")),
			EndpointPath: bma.Ptr("/v1/chat/completions"),
		},
		APIKey:             bma.Ptr("sk-test-0000000000"),
		TTLSeconds:         bma.Ptr(3600),
		ExpiresWithSession: bma.Ptr(true),
	}
}

func TestContractSessionLifecycle(t *testing.T) {
	ctx := context.Background()
	client, _, s := contractClient(t, "create_session")
	created, err := client.Agents.Sessions.New(ctx, s["agent"], bma.AgentSessionNewParams{
		AgentConfigID:  bma.Ptr(s["config"]),
		IdempotencyKey: bma.Ptr("beework-task-1"),
		Metadata:       &map[string]any{"title": "Quarterly report"},
		ModelOverride:  overrideInput(),
	})
	if err != nil || created.Session.ID != s["session"] || created.Session.Status != bma.AgentSessionStatusIdle {
		t.Fatalf("created = %+v, %v", created, err)
	}

	client, _, _ = contractClient(t, "get_session")
	got, err := client.Agents.Sessions.Get(ctx, s["agent"], s["session"])
	if err != nil || got.Session.NextEventSequence != 5 || got.Session.Status != bma.AgentSessionStatusRunning {
		t.Fatalf("get = %+v, %v", got, err)
	}

	client, _, _ = contractClient(t, "list_sessions")
	listed, err := client.Agents.Sessions.List(ctx, s["agent"], bma.AgentSessionListParams{IncludeArchived: bma.Ptr(true), Limit: bma.Ptr(int32(10))})
	if err != nil || len(listed.Data) != 1 || listed.NextCursor != nil {
		t.Fatalf("list = %+v, %v", listed, err)
	}

	client, _, _ = contractClient(t, "archive_session")
	archived, err := client.Agents.Sessions.Archive(ctx, s["agent"], s["session"])
	if err != nil || archived.Session.State != "archived" || archived.Session.Status != bma.AgentSessionStatusTerminated {
		t.Fatalf("archive = %+v, %v", archived, err)
	}

	client, _, _ = contractClient(t, "put_session_model_override")
	mo, err := client.Agents.Sessions.ModelOverride.Set(ctx, s["agent"], s["session"], bma.AgentSessionModelOverrideSetParams(*overrideInput()))
	if err != nil || !mo.ModelOverride.ExpiresWithSession || mo.ModelOverride.ExpiresAt != nil {
		t.Fatalf("override = %+v, %v", mo, err)
	}
}

func TestContractSessionInputAndStream(t *testing.T) {
	ctx := context.Background()
	client, _, s := contractClient(t, "create_session_input")
	input, err := client.Agents.Inputs.New(ctx, s["agent"], bma.AgentInputNewParams{
		SessionID:     bma.Ptr(s["session"]),
		ContentBlocks: []bma.CreateAgentInputContentBlock{bma.NewTextInputBlock("Summarize the report.")},
		DeliveryMode:  bma.Ptr(bma.CreateAgentInputDeliveryModeQueued),
	}, option.WithIdempotencyKey("turn-1"))
	if err != nil || input.AgentInput.State != "queued" {
		t.Fatalf("input = %+v, %v", input, err)
	}

	// The recording ends with a service_unavailable frame; without retries
	// it surfaces as the stream error.
	client, _, _ = contractClient(t, "stream_session_events")
	stream := client.Agents.Events.Stream(ctx, s["agent"], bma.AgentEventStreamParams{
		SessionID: bma.Ptr(s["session"]), StreamDeltas: bma.Ptr(true), LastEventID: bma.Ptr(int64(4)),
	})
	defer stream.Close()
	var frames []string
	for stream.Next() {
		frames = append(frames, stream.Current().Event)
	}
	var apiErr *bma.Error
	if !errors.As(stream.Err(), &apiErr) || apiErr.Code != bma.ErrorCodeServiceUnavailable {
		t.Fatalf("stream err = %v", stream.Err())
	}
	if strings.Join(frames, ",") != "agent_input,tool_call_update" {
		t.Fatalf("frames = %v", frames)
	}
}

func TestContractArtifactDownload(t *testing.T) {
	fixtures := contracttest.Load(t)
	var artifact bma.Artifact
	if err := json.Unmarshal(contracttest.Find(t, fixtures.REST, "get_artifact").Response.JSON, &artifact); err != nil {
		t.Fatal(err)
	}
	client, c, _ := contractClient(t, "get_artifact_content")
	var out bytes.Buffer
	if err := client.Agents.Artifacts.DownloadVerified(context.Background(), artifact, 1024, &out); err != nil {
		t.Fatal(err)
	}
	if out.String() != c.Response.Text {
		t.Fatalf("content = %q", out.String())
	}
	tampered := artifact
	tampered.Digest = bma.Ptr("sha256:" + strings.Repeat("0", 64))
	client, _, _ = contractClient(t, "get_artifact_content")
	if err := client.Agents.Artifacts.DownloadVerified(context.Background(), tampered, 1024, io.Discard); err == nil {
		t.Fatal("digest mismatch was accepted")
	}
}

func TestContractMachineDesktopTerminalAndErrors(t *testing.T) {
	ctx := context.Background()
	client, _, s := contractClient(t, "create_desktop_session")
	desktop, err := client.Machines.DesktopSessions.New(ctx, s["machine"], bma.MachineDesktopSessionNewParams{AgentID: bma.Ptr(s["agent"]), ReadOnly: bma.Ptr(true)})
	if err != nil || desktop.Capabilities.Width != 1920 {
		t.Fatalf("desktop = %+v, %v", desktop, err)
	}
	client, _, _ = contractClient(t, "create_terminal_ticket")
	ticket, err := client.Machines.TerminalSessions.ConnectionTicket(ctx, s["machine"], s["terminal_session"],
		bma.MachineTerminalSessionConnectionTicketParams{TTLSeconds: bma.Ptr(int32(60))})
	if err != nil || ticket.Purpose != "terminal_connect" {
		t.Fatalf("ticket = %+v, %v", ticket, err)
	}
	client, _, _ = contractClient(t, "get_agent_not_found")
	_, err = client.Agents.Get(ctx, "agt_zzzzzzzzzzzzzzzzzzzzzzzzzz")
	var apiErr *bma.Error
	if !errors.As(err, &apiErr) || apiErr.StatusCode != 404 || apiErr.Code != bma.ErrorCodeNotFound {
		t.Fatalf("error = %v", err)
	}
}

func TestContractFilesUploadMountOutputs(t *testing.T) {
	ctx := context.Background()
	client, c, s := contractClient(t, "upload_file")
	uploaded, err := client.Files.Upload(ctx, bma.FileUploadParams{Filename: "report.pdf", Body: strings.NewReader(*c.Request.Text)},
		option.WithIdempotencyKey("upload-report-1"))
	if err != nil || uploaded.ID != s["file"] || uploaded.Scope != nil {
		t.Fatalf("upload = %+v, %v", uploaded, err)
	}
	client, _, _ = contractClient(t, "add_session_file_resource")
	mounted, err := client.Agents.Sessions.Resources.Add(ctx, s["agent"], s["session"], bma.AgentSessionResourceAddParams{
		Type: bma.FileResourceParamsTypeFile, FileID: uploaded.ID, MountPath: bma.Ptr("/mnt/session/uploads/reports/report.pdf"),
	})
	if err != nil || mounted.FileID != s["mounted_file"] {
		t.Fatalf("mount = %+v, %v", mounted, err)
	}
	client, _, _ = contractClient(t, "list_session_outputs")
	outputs, err := client.Files.List(ctx, bma.FileListParams{ScopeID: bma.Ptr(s["session"])})
	if err != nil || len(outputs.Data) != 1 || outputs.Data[0].ID != s["output_file"] || outputs.NextCursor != nil {
		t.Fatalf("outputs = %+v, %v", outputs, err)
	}
}

func TestContractAgentMachines(t *testing.T) {
	ctx := context.Background()
	client, _, s := contractClient(t, "create_agent_machine")
	created, err := client.Agents.Machines.New(ctx, s["agent"], bma.AgentMachineNewParams{
		Template: "base-2c4g", MachinePoolID: bma.Ptr(s["pool"]), DisplayName: bma.Ptr("Ada's workstation"),
	}, option.WithIdempotencyKey("machine-ada-1"))
	if err != nil || created.Kind != bma.AgentMachineKindPersistent || created.CPU != nil {
		t.Fatalf("create = %+v, %v", created, err)
	}
	client, _, _ = contractClient(t, "list_agent_machines")
	listed, err := client.Agents.Machines.List(ctx, s["agent"])
	if err != nil || len(listed.Data) != 1 || listed.Data[0].CPU == nil || *listed.Data[0].CPU != 2 {
		t.Fatalf("list = %+v, %v", listed, err)
	}
	client, _, _ = contractClient(t, "delete_agent_machine")
	if err := client.Agents.Machines.Delete(ctx, s["agent"], s["machine"]); err != nil {
		t.Fatal(err)
	}
}
