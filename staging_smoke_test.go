package bma_test

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"testing"
	"time"

	"github.com/beeos-ai/bma-sdk"
	"github.com/beeos-ai/bma-sdk/option"
)

// TestStagingSmoke runs the TypeScript/Python staging smoke against a live
// deployment: list pages, create an agent with a custom tool, answer it with
// the tool runner, stream the turn, list tool calls and events, a typed 404,
// then archive the agent. It runs only when BMA_BASE_URL (API root, e.g.
// https://host/api/v1), BMA_ORG_API_KEY, BMA_ORG_ID and BMA_PROJECT_ID are set.
func TestStagingSmoke(t *testing.T) {
	base, key := os.Getenv("BMA_BASE_URL"), os.Getenv("BMA_ORG_API_KEY")
	if base == "" || key == "" || os.Getenv("BMA_ORG_ID") == "" || os.Getenv("BMA_PROJECT_ID") == "" {
		t.Skip("set BMA_BASE_URL, BMA_ORG_API_KEY, BMA_ORG_ID and BMA_PROJECT_ID to run")
	}
	ctx, cancel := context.WithTimeout(context.Background(), 4*time.Minute)
	defer cancel()
	client := bma.NewClient(option.WithBaseURL(base), option.WithToken(key))

	first, err := client.Agents.List(ctx, bma.AgentListParams{Limit: bma.Ptr(bma.PageLimit(1))})
	if err != nil {
		t.Fatal(err)
	}
	walked := 0
	pager := client.Agents.ListAutoPaging(ctx, bma.AgentListParams{Limit: bma.Ptr(bma.PageLimit(1))})
	for walked < 3 && pager.Next() {
		walked++
	}
	t.Logf("agents.list first=%d has_next=%v walked=%d err=%v", len(first.Data), first.HasNextPage(), walked, pager.Err())

	tool := bma.DefineTool("get_weather", "Returns the current weather for a city.",
		map[string]any{"type": "object", "properties": map[string]any{"city": map[string]any{"type": "string"}}, "required": []string{"city"}},
		func(ctx context.Context, in struct {
			City string `json:"city"`
		}, call bma.ToolCall) (bma.ToolContent, error) {
			return bma.ToolText("Sunny, 21C in " + in.City), nil
		})
	text, _ := json.Marshal(map[string]any{
		"instruction": "When asked about weather, call get_weather exactly once and repeat its result verbatim.",
		"model":       map[string]any{"provider_config": "uhp-smoke", "name": "deepseek-flash"},
		"tools":       map[string]any{"get_weather": tool.Definition()},
	})
	var source bma.AgentConfigSourceInput
	if err := source.FromAgentConfigSourceInput0(string(text)); err != nil {
		t.Fatal(err)
	}
	created, err := client.Agents.New(ctx, bma.AgentNewParams{
		Name:         bma.Ptr(bma.AgentName(fmt.Sprintf("typed-sdk-smoke-go-%d", time.Now().Unix()))),
		ConfigSource: &bma.CreateAgentConfigRequest{SourceFormat: bma.CreateAgentConfigRequestSourceFormatJson, Source: source},
	})
	if err != nil {
		t.Fatal(err)
	}
	agent := created.LaunchAgentResponse.Agent.Id
	t.Logf("agents.new %s", agent)
	defer func() {
		archived, err := client.Agents.Archive(context.Background(), agent)
		if err != nil {
			t.Errorf("archive: %v", err)
			return
		}
		t.Logf("agents.archive state=%s", archived.Agent.State)
	}()

	runCtx, stopRunner := context.WithCancel(ctx)
	runErr := make(chan error, 1)
	go func() { runErr <- client.Agents.ToolCalls.Runner(agent, bma.ToolRunnerParams{Tools: []bma.RunnableTool{tool}}).Run(runCtx) }()

	input, err := client.Agents.Inputs.New(ctx, agent, bma.AgentInputNewParams{
		ContentBlocks: []bma.CreateAgentInputContentBlock{bma.NewTextInputBlock("What is the weather in Paris?")},
	})
	if err != nil {
		t.Fatal(err)
	}
	t.Logf("agents.inputs.new %s state=%s", input.AgentInput.Id, input.AgentInput.State)

	stream := client.Agents.Events.Stream(ctx, agent, bma.AgentEventStreamParams{StreamDeltas: bma.Ptr(false)})
	var kinds []string
	sawResult, answered := false, false
	for !answered && stream.Next() {
		ev := stream.Current()
		kinds = append(kinds, ev.Event)
		switch v := ev.AsAny().(type) {
		case bma.ToolResultEvent:
			sawResult = true
		case bma.ModelOutputEvent:
			if sawResult {
				answered = true
				t.Logf("answer blocks=%d", len(v.ContentBlocks))
			}
		}
	}
	stream.Close()
	if !answered {
		t.Fatalf("no answer; frames=%v err=%v", kinds, stream.Err())
	}
	t.Logf("agents.events.stream frames=%v", kinds)

	calls, err := client.Agents.ToolCalls.List(ctx, agent, bma.AgentToolCallListParams{Limit: bma.Ptr(bma.PageLimit(5))})
	if err != nil {
		t.Fatal(err)
	}
	succeeded := 0
	for _, c := range calls.Data {
		t.Logf("tool call %s %s state=%s outcome=%v input=%v", c.Id, c.Name, c.State, c.Outcome, c.Input)
		if c.Name == "get_weather" && c.Outcome != nil && *c.Outcome == "succeeded" {
			succeeded++
		}
	}
	if succeeded == 0 {
		t.Fatal("no succeeded get_weather call")
	}
	events, err := client.Agents.Events.List(ctx, agent, bma.AgentEventListParams{Limit: bma.Ptr(bma.PageLimit(50))})
	if err != nil {
		t.Fatal(err)
	}
	t.Logf("agents.events.list count=%d", len(events.Data))

	_, err = client.Agents.Get(ctx, "agt_zzzzzzzzzzzzzzzzzzzzzzzzzz")
	var apiErr *bma.Error
	if !errors.As(err, &apiErr) || apiErr.StatusCode != 404 || apiErr.Code != bma.ErrorCodeNotFound {
		t.Fatalf("404 = %v", err)
	}
	stopRunner()
	if err := <-runErr; err != nil {
		t.Fatalf("runner: %v", err)
	}
}
