package rest_test

import (
	"context"
	"os"
	"testing"
	"time"

	bmarest "github.com/beeos-ai/bma-sdks/go/rest"
)

// TestStagingReadOnlySmoke calls a live deployment with read-only operations.
// It runs only when BMA_BASE_URL (API root, e.g. https://host/api/v1),
// BMA_ORG_API_KEY, BMA_ORG_ID and BMA_PROJECT_ID are set.
func TestStagingReadOnlySmoke(t *testing.T) {
	base, key := os.Getenv("BMA_BASE_URL"), os.Getenv("BMA_ORG_API_KEY")
	org, project := os.Getenv("BMA_ORG_ID"), os.Getenv("BMA_PROJECT_ID")
	if base == "" || key == "" || org == "" || project == "" {
		t.Skip("set BMA_BASE_URL, BMA_ORG_API_KEY, BMA_ORG_ID and BMA_PROJECT_ID to run")
	}
	client, err := bmarest.New(bmarest.Options{BaseURL: base, Token: key})
	if err != nil {
		t.Fatal(err)
	}
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	list, err := client.ListAgentsWithResponse(ctx, org, project, &bmarest.ListAgentsParams{Limit: ptr(int32(5))})
	if err != nil {
		t.Fatal(err)
	}
	if err := bmarest.CheckResponse(list.HTTPResponse, list.Body); err != nil {
		t.Fatal(err)
	}
	if list.JSON200 == nil {
		t.Fatalf("ListAgents: HTTP %d without a decoded body", list.StatusCode())
	}
	t.Logf("ListAgents: %d agents", len(list.JSON200.Data))
	if len(list.JSON200.Data) == 0 {
		t.Skip("no agents to GetAgent")
	}
	id := list.JSON200.Data[0].Id
	got, err := client.GetAgentWithResponse(ctx, org, project, id)
	if err != nil {
		t.Fatal(err)
	}
	if err := bmarest.CheckResponse(got.HTTPResponse, got.Body); err != nil {
		t.Fatal(err)
	}
	if got.JSON200 == nil || got.JSON200.Agent.Id != id {
		t.Fatalf("GetAgent: %+v", got.JSON200)
	}
}
