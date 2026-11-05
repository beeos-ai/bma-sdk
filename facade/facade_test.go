package facade_test

import (
	"context"
	"encoding/json"
	"errors"
	"strings"
	"testing"

	"github.com/beeos-ai/bma-sdk"
	"github.com/beeos-ai/bma-sdk/facade"
	"github.com/beeos-ai/bma-sdk/internal/contracttest"
	"github.com/beeos-ai/bma-sdk/option"
)

func contractClient(t *testing.T, name string) (*facade.Client, map[string]string) {
	t.Helper()
	fixtures := contracttest.Load(t)
	c := contracttest.Find(t, fixtures.Facade, name)
	server := contracttest.Serve(t, c, "")
	client := facade.NewClient(option.WithBaseURL(server.URL), option.WithAPIKey("test-key"),
		option.WithProject(fixtures.Scope["project"]), option.WithMaxRetries(0))
	return client, fixtures.Scope
}

func TestDesktopStream(t *testing.T) {
	client, s := contractClient(t, "desktop_stream")
	stream, err := client.Sessions.Desktop.Stream(context.Background(), s["session"], facade.SessionDesktopStreamParams{
		DesktopSessionId: s["desktop_session"], TtlSeconds: bma.Ptr(60), Origin: bma.Ptr("https://app.example.com"),
	})
	if err != nil || stream.Ticket != "watch-ticket" || stream.MachineId != s["machine"] {
		t.Fatalf("stream = %+v, %v", stream, err)
	}
}

func TestSessionFiles(t *testing.T) {
	ctx := context.Background()
	client, s := contractClient(t, "upload_session_file")
	file, err := client.Sessions.Files.Upload(ctx, s["session"], facade.SessionFileUploadParams{File: bma.NewFile(strings.NewReader("meeting notes"), "notes.txt")})
	if err != nil || file.Filename != "notes.txt" || file.SizeBytes != 13 {
		t.Fatalf("file = %+v, %v", file, err)
	}
	client, _ = contractClient(t, "list_session_files")
	page, err := client.Sessions.Files.List(ctx, s["session"], facade.SessionFileListParams{Limit: bma.Ptr(1)})
	if err != nil || len(page.Data) != 1 || page.NextPage == nil || *page.NextPage != "1" {
		t.Fatalf("page = %+v, %v", page, err)
	}
	client, _ = contractClient(t, "upload_session_file_conflict")
	_, err = client.Sessions.Files.Upload(ctx, s["session"], facade.SessionFileUploadParams{File: bma.NewFile(strings.NewReader("again"), "dup.txt")})
	var apiErr *bma.Error
	if !errors.As(err, &apiErr) || apiErr.StatusCode != 409 || apiErr.Code != "file_already_exists" {
		t.Fatalf("error = %v", err)
	}
}

func TestSessionResources(t *testing.T) {
	ctx := context.Background()
	client, s := contractClient(t, "add_session_resource")
	resource, err := client.Sessions.Resources.Add(ctx, s["session"], facade.SessionResourceAddParams{
		Type: facade.FileResourceParamsTypeFile, FileId: s["file"], MountPath: bma.Ptr("reports/report.pdf"),
	})
	if err != nil || resource.Id != s["resource"] || resource.MountPath != "reports/report.pdf" {
		t.Fatalf("resource = %+v, %v", resource, err)
	}
	client, _ = contractClient(t, "list_session_resources")
	page, err := client.Sessions.Resources.List(ctx, s["session"])
	if err != nil || len(page.Data) != 1 || page.Data[0].Id != s["resource"] {
		t.Fatalf("page = %+v, %v", page, err)
	}
	client, _ = contractClient(t, "delete_session_resource")
	deleted, err := client.Sessions.Resources.Delete(ctx, s["session"], s["resource"])
	if err != nil || deleted.Id != s["resource"] {
		t.Fatalf("deleted = %+v, %v", deleted, err)
	}
}

func TestRejectsV1BaseURL(t *testing.T) {
	client := facade.NewClient(option.WithBaseURL("https://api.example.com/v1"), option.WithAPIKey("k"))
	if _, err := client.Sessions.Resources.List(context.Background(), "ses_x"); err == nil || !strings.Contains(err.Error(), "/v1") {
		t.Fatalf("err = %v", err)
	}
}

func TestEventBMASequence(t *testing.T) {
	if seq, ok := facade.EventBMASequence(json.RawMessage(`{"type":"agent.message","bma_sequence":42}`)); !ok || seq != 42 {
		t.Fatalf("sequence = %d, %v", seq, ok)
	}
	if _, ok := facade.EventBMASequence(json.RawMessage(`{"type":"agent.message"}`)); ok {
		t.Fatal("missing bma_sequence reported as present")
	}
}
