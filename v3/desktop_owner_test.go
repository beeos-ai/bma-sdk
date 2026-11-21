package bmasdk_test

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strconv"
	"testing"

	"github.com/anthropics/anthropic-sdk-go/v2/option"
	bmasdk "github.com/beeos-ai/bma-sdk/v3"
)

func TestDesktopSessionTypedOwnerRoundTrip(t *testing.T) {
	for _, owner := range []string{"0195f1c0-0000-7000-8000-000000000001", "oak_test_owner"} {
		for _, method := range []string{http.MethodPost, http.MethodGet} {
			t.Run(method+"/"+owner, func(t *testing.T) {
				srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
					if r.Method != method {
						t.Errorf("method = %s, want %s", r.Method, method)
					}
					w.Header().Set("Content-Type", "application/json")
					if err := json.NewEncoder(w).Encode(map[string]any{
						"type": "desktop_session", "id": "dsn_test", "machine_id": "mch_test",
						"org_id": "org_test", "project_id": "proj_test", "owner_id": owner,
						"read_only": true, "closed": false, "created_at": "2026-11-16T00:00:00Z",
						"capabilities": map[string]any{"width": 1920, "height": 1080},
						"control":      map[string]any{"mode": "paused", "epoch": 1, "generation": 1},
					}); err != nil {
						t.Error(err)
					}
				}))
				defer srv.Close()
				client := bmasdk.NewClient(option.WithBaseURL(srv.URL), option.WithAPIKey("test"))
				var session *bmasdk.DesktopSession
				var err error
				if method == http.MethodPost {
					session, err = client.Beta.DesktopSessions.New(context.Background(), bmasdk.DesktopSessionNewParams{
						MachineID: "mch_test",
					})
				} else {
					session, err = client.Beta.DesktopSessions.Get(context.Background(), "dsn_test")
				}
				if err != nil {
					t.Fatal(err)
				}
				encoded, err := json.Marshal(session.OwnerID)
				if err != nil {
					t.Fatal(err)
				}
				if string(encoded) != strconv.Quote(owner) {
					t.Fatalf("owner ID lost: %s, want %q", encoded, owner)
				}
			})
		}
	}
}
