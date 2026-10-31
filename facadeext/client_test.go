package facadeext_test

import (
	"context"
	"encoding/json"
	"errors"
	"strings"
	"testing"

	"github.com/beeos-ai/bma-sdks/go/facadeext"
	"github.com/beeos-ai/bma-sdks/go/internal/contracttest"
)

func contractClient(t *testing.T, name string) (*facadeext.Client, contracttest.Case, map[string]string) {
	t.Helper()
	fixtures := contracttest.Load(t)
	c := contracttest.Find(t, fixtures.Facade, name)
	server := contracttest.Serve(t, c, "")
	client, err := facadeext.New(facadeext.Options{
		BaseURL: server.URL, APIKey: "test-key", ProjectID: fixtures.Scope["project"],
	})
	if err != nil {
		t.Fatal(err)
	}
	return client, c, fixtures.Scope
}

func TestDesktopStream(t *testing.T) {
	client, _, s := contractClient(t, "desktop_stream")
	stream, err := client.GetSessionDesktopStream(context.Background(), s["session"], facadeext.DesktopStreamOptions{
		DesktopSessionID: s["desktop_session"], TTLSeconds: 60, Origin: "https://app.example.com",
	})
	if err != nil {
		t.Fatal(err)
	}
	if stream.Type != facadeext.BmaDesktopStream || stream.Ticket != "watch-ticket" || stream.MachineId != s["machine"] {
		t.Fatalf("stream = %+v", stream)
	}
}

func TestSessionFiles(t *testing.T) {
	client, _, s := contractClient(t, "upload_session_file")
	file, err := client.UploadSessionFile(context.Background(), s["session"], "notes.txt", strings.NewReader("meeting notes"))
	if err != nil {
		t.Fatal(err)
	}
	if file.Filename != "notes.txt" || file.SizeBytes != 13 {
		t.Fatalf("file = %+v", file)
	}

	client, _, _ = contractClient(t, "list_session_files")
	page, err := client.ListSessionFiles(context.Background(), s["session"], 1, "")
	if err != nil {
		t.Fatal(err)
	}
	if len(page.Data) != 1 || page.NextPage == nil || *page.NextPage != "1" {
		t.Fatalf("page = %+v", page)
	}

	client, _, _ = contractClient(t, "upload_session_file_conflict")
	_, err = client.UploadSessionFile(context.Background(), s["session"], "dup.txt", strings.NewReader("again"))
	var apiErr *facadeext.APIError
	if !errors.As(err, &apiErr) || apiErr.StatusCode != 409 || apiErr.Code != "file_already_exists" {
		t.Fatalf("error = %v", err)
	}
}

func TestUploadRejectsEmptyFile(t *testing.T) {
	client, err := facadeext.New(facadeext.Options{BaseURL: "http://127.0.0.1:1", APIKey: "k"})
	if err != nil {
		t.Fatal(err)
	}
	if _, err := client.UploadSessionFile(context.Background(), "ses_x", "a.txt", strings.NewReader("")); err == nil {
		t.Fatal("empty upload was accepted")
	}
}

func TestNewRejectsV1BaseURL(t *testing.T) {
	if _, err := facadeext.New(facadeext.Options{BaseURL: "https://api.example.com/v1", APIKey: "k"}); err == nil {
		t.Fatal("BaseURL with /v1 was accepted")
	}
}

func TestEventBMASequence(t *testing.T) {
	if seq, ok := facadeext.EventBMASequence(json.RawMessage(`{"type":"agent.message","bma_sequence":42}`)); !ok || seq != 42 {
		t.Fatalf("sequence = %d, %v", seq, ok)
	}
	if _, ok := facadeext.EventBMASequence(json.RawMessage(`{"type":"agent.message"}`)); ok {
		t.Fatal("missing bma_sequence reported as present")
	}
}
