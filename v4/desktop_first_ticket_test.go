package bmasdk_test

import (
	"context"
	"encoding/json"
	"io"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/anthropics/anthropic-sdk-go/v2/option"
	bmasdk "github.com/beeos-ai/bma-sdk/v4"
)

// Creating a desktop session can ask for the first ticket in the same call; the
// answer carries it in `ticket` (no second POST .../tickets round trip).
func TestDesktopSessionCreateReturnsFirstTicket(t *testing.T) {
	var sent map[string]any
	srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		raw, _ := io.ReadAll(r.Body)
		if err := json.Unmarshal(raw, &sent); err != nil {
			t.Error(err)
		}
		w.Header().Set("Content-Type", "application/json")
		_ = json.NewEncoder(w).Encode(map[string]any{
			"type": "desktop_session", "id": "dsn_test", "machine_id": "mch_test",
			"org_id": "org_test", "project_id": "proj_test", "owner_id": "oak_test_owner",
			"read_only": true, "closed": false, "created_at": "2026-11-16T00:00:00Z",
			"capabilities": map[string]any{"width": 1920, "height": 1080},
			"control":      map[string]any{"mode": "paused", "epoch": 1, "generation": 1},
			"ticket": map[string]any{
				"type": "ticket", "purpose": "watch", "ticket": "tok_first",
				"ws_url": "wss://x.test/ws", "desktop_session_id": "dsn_test", "viewer": "viewer_1",
			},
		})
	}))
	defer srv.Close()
	client := bmasdk.NewClient(option.WithBaseURL(srv.URL), option.WithAPIKey("test"))
	viewer := bmasdk.DesktopViewerID("viewer_1")
	session, err := client.Beta.DesktopSessions.New(context.Background(), bmasdk.DesktopSessionNewParams{
		MachineID: "mch_test",
		Ticket:    &bmasdk.CreateDesktopTicketRequest{Viewer: &viewer},
	})
	if err != nil {
		t.Fatal(err)
	}
	if tk, _ := sent["ticket"].(map[string]any); tk["viewer"] != "viewer_1" {
		t.Fatalf("request ticket body = %v", sent["ticket"])
	}
	if session.Ticket == nil || session.Ticket.Ticket != "tok_first" || session.Ticket.WsURL != "wss://x.test/ws" {
		t.Fatalf("first ticket lost: %+v", session.Ticket)
	}
}
