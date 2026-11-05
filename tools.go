package bma

// Custom tools (ADR 0012 D7). A BMA custom tool call stays ready until a
// consumer submits its result; DefineTool and Agents.ToolCalls.Runner give
// that consumer a typed shape, after the Anthropic SDKs' tool helpers and
// sessions.events.toolRunner.

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"sync"

	"github.com/beeos-ai/bma-sdk/internal/apicore"
	"github.com/beeos-ai/bma-sdk/option"
)

// ToolContent is what a tool returns to the model.
type ToolContent []SubmitToolResultContentBlock

// ToolText is a ToolContent of one text block.
func ToolText(text string) ToolContent {
	var block SubmitToolResultContentBlock
	_ = block.FromTextContentBlock(NewTextContentBlock(text))
	return ToolContent{block}
}

// ToolCallError is a tool-level failure reported to the model.
type ToolCallError struct{ Content ToolContent }

func (e *ToolCallError) Error() string { return "tool error" }

// ToolError returns an error that reports text to the model as a failed call.
func ToolError(text string) error { return &ToolCallError{Content: ToolText(text)} }

// RunnableTool is a custom tool for Agents.ToolCalls.Runner.
type RunnableTool interface {
	Name() string
	// Definition is the agent config entry of tools.<name>.
	Definition() AgentConfigDefinitionTool
	run(ctx context.Context, call ToolCall) (ToolContent, error)
}

type definedTool[In any] struct {
	name, description string
	schema            map[string]any
	fn                func(context.Context, In, ToolCall) (ToolContent, error)
}

// DefineTool defines a custom tool. inputSchema is the JSON Schema of the
// input object; the call input is decoded into In (a decoding error is
// reported to the model; unknown members are ignored) before fn runs. Return ToolError for a
// failure the model should see; any other error is reported the same way.
func DefineTool[In any](name, description string, inputSchema map[string]any, fn func(ctx context.Context, input In, call ToolCall) (ToolContent, error)) RunnableTool {
	return &definedTool[In]{name: name, description: description, schema: inputSchema, fn: fn}
}

func (t *definedTool[In]) Name() string { return t.name }

func (t *definedTool[In]) Definition() AgentConfigDefinitionTool {
	var def AgentConfigDefinitionTool
	raw, _ := json.Marshal(map[string]any{"type": "custom", "description": t.description, "input_schema": t.schema})
	_ = json.Unmarshal(raw, &def)
	return def
}

func (t *definedTool[In]) run(ctx context.Context, call ToolCall) (ToolContent, error) {
	raw, err := json.Marshal(call.Input)
	if err != nil {
		return nil, err
	}
	// Unknown members are ignored, as zod objects and pydantic models do in
	// the TypeScript and Python runners.
	var in In
	if err := json.Unmarshal(raw, &in); err != nil {
		return nil, ToolError(fmt.Sprintf("invalid input for %s: %v", t.name, err))
	}
	return t.fn(ctx, in, call)
}

// ToolRunnerParams selects the calls a runner handles.
type ToolRunnerParams struct {
	// SessionID limits the agent's own calls to one session; calls of
	// subagents are always handled.
	SessionID string
	Tools     []RunnableTool
}

// ToolRunner answers custom tool calls of one agent.
type ToolRunner struct {
	service *AgentToolCallService
	agentID string
	params  ToolRunnerParams
	opts    []option.RequestOption
}

// Runner returns a runner for agentID; call Run.
func (s *AgentToolCallService) Runner(agentID string, params ToolRunnerParams, opts ...option.RequestOption) *ToolRunner {
	return &ToolRunner{service: s, agentID: agentID, params: params, opts: opts}
}

// Run handles every ready custom call (of the agent and its subagents) whose
// name matches a tool: it decodes the input, runs the tool and submits the
// result. Ready calls are listed on every (re)connection of the event
// stream, so calls that became ready while disconnected are not lost. Run
// returns when the stream ends, nil when ctx is canceled, or the first
// error; it waits for running tools before returning.
func (r *ToolRunner) Run(ctx context.Context) error {
	tools := map[string]RunnableTool{}
	for _, t := range r.params.Tools {
		if _, dup := tools[t.Name()]; dup {
			return fmt.Errorf("bma: tool names must be unique: %s", t.Name())
		}
		tools[t.Name()] = t
	}
	ctx, cancel := context.WithCancelCause(ctx)
	defer cancel(nil)
	var (
		mu      sync.Mutex
		seen    = map[string]bool{}
		running sync.WaitGroup
	)
	fail := func(err error) { cancel(err) }
	handle := func(call ToolCall) {
		tool := tools[call.Name]
		if call.Type != ToolCallTypeCustom || call.State != ToolCallStateReady || tool == nil {
			return
		}
		if r.params.SessionID != "" && call.AgentId == r.agentID && call.SessionId != r.params.SessionID {
			return
		}
		mu.Lock()
		if seen[call.Id] {
			mu.Unlock()
			return
		}
		seen[call.Id] = true
		mu.Unlock()
		running.Add(1)
		go func() {
			defer running.Done()
			outcome := SubmitToolCallResultRequestOutcomeSucceeded
			output, err := tool.run(ctx, call)
			if err != nil {
				outcome = SubmitToolCallResultRequestOutcomeFailed
				var te *ToolCallError
				if errors.As(err, &te) {
					output = te.Content
				} else {
					output = ToolText(err.Error())
				}
			}
			_, err = r.service.SubmitResult(context.WithoutCancel(ctx), call.AgentId, call.Id,
				AgentToolCallSubmitResultParams{Outcome: outcome, ContentBlocks: output}, r.opts...)
			if err != nil {
				fail(err)
			}
		}()
	}
	sweep := func() {
		running.Add(1)
		go func() {
			defer running.Done()
			ready, custom := ToolCallStateReady, ToolCallTypeCustom
			pager := r.service.ListAutoPaging(ctx, r.agentID, AgentToolCallListParams{State: &ready, Type: &custom, IncludeSubagents: Ptr(true)}, r.opts...)
			for pager.Next() {
				handle(pager.Current())
			}
			if err := pager.Err(); err != nil && ctx.Err() == nil {
				fail(err)
			}
		}()
	}
	params := AgentEventStreamParams{}
	if r.params.SessionID != "" {
		params.SessionId = Ptr(r.params.SessionID)
	}
	events := &AgentEventService{core: r.service.core}
	stream := apicore.OpenStream(ctx, events.streamRequest(r.agentID, params, r.opts), decodeStreamEventsEvent, sweep)
	for stream.Next() {
		update, ok := stream.Current().AsAny().(ToolCallUpdate)
		if !ok || update.State != ToolCallStateReady {
			continue
		}
		agentID := r.agentID
		if update.AgentId != nil {
			agentID = *update.AgentId
		}
		envelope, err := r.service.Get(ctx, agentID, update.ToolCallId, r.opts...)
		if err != nil {
			fail(err)
			break
		}
		handle(envelope.ToolCall)
	}
	streamErr := stream.Err()
	stream.Close()
	running.Wait()
	if cause := context.Cause(ctx); cause != nil && !errors.Is(cause, context.Canceled) {
		return cause
	}
	if streamErr != nil && !errors.Is(streamErr, context.Canceled) {
		return streamErr
	}
	return nil
}
