package bmarest

import (
	"encoding/json"
	"io"
	"time"
)

// ProjectScope identifies a BMA project.
type ProjectScope struct {
	OrgID     string
	ProjectID string
}

// AgentScope identifies one agent inside a project.
type AgentScope struct {
	OrgID     string
	ProjectID string
	AgentID   string
}

// RequestOptions carries optional headers for one request.
type RequestOptions struct {
	// IdempotencyKey makes a mutating request replay-safe. The server returns
	// the original result when the same key is reused.
	IdempotencyKey string
}

// PageOptions controls cursor pagination.
type PageOptions struct {
	// Limit is the maximum number of items to return. Zero uses the server default.
	Limit int
	// Cursor is the opaque next_cursor from a previous response.
	Cursor string
}

// ContentBlockType discriminates a content block on the wire.
type ContentBlockType string

const (
	ContentBlockTypeText           ContentBlockType = "text"
	ContentBlockTypeMedia          ContentBlockType = "media"
	ContentBlockTypeMediaRef       ContentBlockType = "media_ref"
	ContentBlockTypeStructuredData ContentBlockType = "structured_data"
	ContentBlockTypeReasoning      ContentBlockType = "reasoning"
	ContentBlockTypeToolCall       ContentBlockType = "tool_call"
	ContentBlockTypeError          ContentBlockType = "error"
)

// ContentBlock is the shared flat representation of the contract's content
// block variants. The Type field selects which optional fields are meaningful,
// matching the executor SDK and keeping Go decoding simple.
type ContentBlock struct {
	Type ContentBlockType `json:"type"`

	// Text is set for text, reasoning, and error blocks.
	Text *string `json:"text,omitempty"`
	// MediaType, Filename, and Data are set for inline media blocks.
	MediaType string `json:"media_type,omitempty"`
	Filename  string `json:"filename,omitempty"`
	Data      []byte `json:"data,omitempty"`
	// ArtifactID is set for media_ref blocks.
	ArtifactID string `json:"artifact_id,omitempty"`
	// ExcludeFromModelContext applies to media_ref blocks.
	ExcludeFromModelContext bool `json:"exclude_from_model_context,omitempty"`
	// Value is set for structured_data blocks.
	Value json.RawMessage `json:"value,omitempty"`
	// ToolCallID, ToolType, Name, and Input are set for tool call blocks.
	ToolCallID string          `json:"tool_call_id,omitempty"`
	ToolType   string          `json:"tool_type,omitempty"`
	Name       string          `json:"name,omitempty"`
	Input      json.RawMessage `json:"input,omitempty"`

	Metadata map[string]string `json:"metadata,omitempty"`
}

// TextBlock builds a text content block.
func TextBlock(text string) ContentBlock {
	return ContentBlock{Type: ContentBlockTypeText, Text: &text}
}

// MediaBlock builds an inline media content block. data is the raw file
// content; it is base64-encoded when the request is sent.
func MediaBlock(mediaType, filename string, data []byte) ContentBlock {
	return ContentBlock{
		Type:      ContentBlockTypeMedia,
		MediaType: mediaType,
		Filename:  filename,
		Data:      data,
	}
}

// MediaRefBlock builds a content block that references an uploaded artifact.
func MediaRefBlock(artifactID string) ContentBlock {
	return ContentBlock{Type: ContentBlockTypeMediaRef, ArtifactID: artifactID}
}

// ExternalActorParams attributes an input or resolution to an external user.
type ExternalActorParams struct {
	ProviderTenantID string            `json:"provider_tenant_id,omitempty"`
	ProviderUserID   string            `json:"provider_user_id"`
	DisplayName      string            `json:"display_name,omitempty"`
	Metadata         map[string]string `json:"metadata,omitempty"`
}

// AgentState is the durable lifecycle state of an agent.
type AgentState string

const (
	AgentStateActive   AgentState = "active"
	AgentStateArchived AgentState = "archived"
)

// AgentActivityState is the agent's current activity.
type AgentActivityState string

const (
	AgentActivityRunning              AgentActivityState = "running"
	AgentActivityIdle                 AgentActivityState = "idle"
	AgentActivityWaitingOnInteraction AgentActivityState = "waiting_on_interaction"
	AgentActivityArchived             AgentActivityState = "archived"
)

// AgentModel names the configured model and provider config used by an agent.
type AgentModel struct {
	ProviderConfig string `json:"provider_config"`
	Name           string `json:"name"`
}

// AgentActivity reports what the agent is doing now.
type AgentActivity struct {
	State          AgentActivityState `json:"state"`
	LastActivityAt time.Time          `json:"last_activity_at"`
}

// Agent is one BMA agent.
type Agent struct {
	ID              string         `json:"id"`
	OrgID           string         `json:"org_id"`
	ProjectID       string         `json:"project_id"`
	AgentProfileID  string         `json:"agent_profile_id,omitempty"`
	State           AgentState     `json:"state"`
	Name            string         `json:"name"`
	CurrentConfigID string         `json:"current_config_id,omitempty"`
	Model           *AgentModel    `json:"model,omitempty"`
	ParentAgentID   string         `json:"parent_agent_id,omitempty"`
	SubagentKey     string         `json:"subagent_key,omitempty"`
	Activity        *AgentActivity `json:"activity,omitempty"`
	CreatedAt       time.Time      `json:"created_at"`
	UpdatedAt       time.Time      `json:"updated_at"`
	ArchivedAt      *time.Time     `json:"archived_at,omitempty"`
}

// AgentConfigModel identifies the model stored on an agent config.
type AgentConfigModel struct {
	ProviderConfig    string `json:"provider_config"`
	Name              string `json:"name"`
	ProviderModelSlug string `json:"provider_model_slug,omitempty"`
}

// AgentConfig is the pinned configuration returned at launch.
type AgentConfig struct {
	ID                      string            `json:"id"`
	OrgID                   string            `json:"org_id"`
	ProjectID               string            `json:"project_id"`
	Source                  string            `json:"source,omitempty"`
	SourceFormat            string            `json:"source_format,omitempty"`
	EffectiveDefinitionHash string            `json:"effective_definition_hash"`
	Model                   *AgentConfigModel `json:"model,omitempty"`
	InstructionHash         string            `json:"instruction_hash,omitempty"`
	CreatedAt               time.Time         `json:"created_at"`
	CompiledDefinition      json.RawMessage   `json:"compiled_definition,omitempty"`
}

// AgentMCPConnection is one MCP server connection of an agent.
type AgentMCPConnection struct {
	ServerKey       string    `json:"server_key"`
	EndpointURL     string    `json:"endpoint_url"`
	State           string    `json:"state"`
	ProtocolVersion string    `json:"protocol_version,omitempty"`
	InitializeError string    `json:"initialize_error,omitempty"`
	CreatedAt       time.Time `json:"created_at"`
	UpdatedAt       time.Time `json:"updated_at"`
}

// AgentMachineBinding is a machine attached to an agent at launch.
type AgentMachineBinding struct {
	ID          string    `json:"id"`
	ProjectID   string    `json:"project_id"`
	AgentID     string    `json:"agent_id"`
	MachineID   string    `json:"machine_id"`
	BindingKind string    `json:"binding_kind"`
	State       string    `json:"state"`
	Description string    `json:"description"`
	CWD         string    `json:"cwd"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
}

// CreateAgentRequest launches an agent from a profile, a saved config, or a
// config source. Send exactly one of Profile, Config, or ConfigSource.
type CreateAgentRequest struct {
	Profile      string          `json:"profile,omitempty"`
	Config       string          `json:"config,omitempty"`
	ConfigSource json.RawMessage `json:"config_source,omitempty"`

	// Name is optional. Omit it to inherit the profile name; send a pointer to
	// the empty string to leave the agent unnamed.
	Name    *string `json:"name,omitempty"`
	Message string  `json:"message,omitempty"`

	Tools               map[string]json.RawMessage `json:"tools,omitempty"`
	Subscriptions       []json.RawMessage          `json:"subscriptions,omitempty"`
	InteractionHandlers map[string]json.RawMessage `json:"interaction_handlers,omitempty"`

	InitialInput *AgentLaunchInitialInput `json:"initial_input,omitempty"`
}

// AgentLaunchInitialInput admits an initial queued text input atomically with
// the launch.
type AgentLaunchInitialInput struct {
	ContentBlocks []ContentBlock       `json:"content_blocks"`
	Actor         *ExternalActorParams `json:"actor,omitempty"`
}

// LaunchAgentResponse is returned when a new agent is launched.
type LaunchAgentResponse struct {
	Agent           *Agent                `json:"agent"`
	AgentConfig     *AgentConfig          `json:"agent_config"`
	MachineBindings []AgentMachineBinding `json:"machine_bindings"`
	AgentInput      *AgentInput           `json:"agent_input,omitempty"`
}

// CurrentAgentResponse wraps an agent in responses that return current state.
type CurrentAgentResponse struct {
	Agent *Agent `json:"agent"`
}

// GetAgentResponse adds the agent's attached machines and MCP connections.
type GetAgentResponse struct {
	Agent          *Agent               `json:"agent"`
	MachineIDs     []string             `json:"machine_ids"`
	MCPConnections []AgentMCPConnection `json:"mcp_connections"`
}

// ListAgentsResponse is one page of agents.
type ListAgentsResponse struct {
	Data       []Agent `json:"data"`
	NextCursor *string `json:"next_cursor"`
}

// ListAgentsOptions filters and paginates agents.
type ListAgentsOptions struct {
	Name             string
	AgentProfileID   string
	ParentAgentID    string
	IncludeSubagents bool
	IncludeArchived  bool
	IncludeUsage     bool
	Sort             string
	Limit            int
	Cursor           string
}

// AgentInputDeliveryMode controls when an input reaches the agent.
type AgentInputDeliveryMode string

const (
	AgentInputDeliveryQueued    AgentInputDeliveryMode = "queued"
	AgentInputDeliverySteering  AgentInputDeliveryMode = "steering"
	AgentInputDeliveryImmediate AgentInputDeliveryMode = "immediate"
)

// AgentInputKind describes how an input entered the timeline.
type AgentInputKind string

const (
	AgentInputKindContent             AgentInputKind = "content"
	AgentInputKindControl             AgentInputKind = "control"
	AgentInputKindInteractionResponse AgentInputKind = "interaction_response"
	AgentInputKindConfigChange        AgentInputKind = "config_change"
)

// CreateAgentInputRequest sends content to an agent.
type CreateAgentInputRequest struct {
	ContentBlocks []ContentBlock `json:"content_blocks"`

	DeliveryMode           AgentInputDeliveryMode `json:"delivery_mode,omitempty"`
	CancelOpenInteractions bool                   `json:"cancel_open_interactions,omitempty"`
	Actor                  *ExternalActorParams   `json:"actor,omitempty"`
	// ModelOverride is an optional one-turn model override. It is kept raw
	// because the override embeds provider credentials and is not part of the
	// Beework launch path.
	ModelOverride json.RawMessage `json:"model_override,omitempty"`
}

// AgentInput is a stored input.
type AgentInput struct {
	ID                  string                 `json:"id"`
	AgentID             string                 `json:"agent_id"`
	State               string                 `json:"state"`
	DeliveryMode        AgentInputDeliveryMode `json:"delivery_mode"`
	InputKind           AgentInputKind         `json:"input_kind"`
	ActorID             string                 `json:"actor_id,omitempty"`
	InputIdempotencyKey string                 `json:"input_idempotency_key,omitempty"`
	ContentBlocks       []ContentBlock         `json:"content_blocks,omitempty"`
	QueuedAt            time.Time              `json:"queued_at"`
}

// AgentInputEnvelope wraps a created or replayed agent input.
type AgentInputEnvelope struct {
	AgentInput *AgentInput `json:"agent_input"`
}

// ListAgentInputsResponse is one page of backlog inputs.
type ListAgentInputsResponse struct {
	Data       []AgentInput `json:"data"`
	NextCursor *string      `json:"next_cursor"`
}

// MovePosition is the position used when moving a queued input.
type MovePosition string

const (
	MovePositionFront  MovePosition = "front"
	MovePositionBack   MovePosition = "back"
	MovePositionBefore MovePosition = "before"
	MovePositionAfter  MovePosition = "after"
)

// MoveQueuedBacklogInputRequest moves a queued input.
type MoveQueuedBacklogInputRequest struct {
	Position      MovePosition `json:"position"`
	AnchorInputID string       `json:"anchor_input_id,omitempty"`
}

// PromoteQueuedInputToSteeringRequest promotes a queued input.
type PromoteQueuedInputToSteeringRequest struct {
	CancelOpenInteractions bool `json:"cancel_open_interactions,omitempty"`
}

// CancelAgentRequest optionally attributes the cancellation.
type CancelAgentRequest struct {
	Actor *ExternalActorParams `json:"actor,omitempty"`
}

// CancelAgentResponse reports whether cancellation changed any work.
type CancelAgentResponse struct {
	Event                  *AgentEvent `json:"event"`
	RuntimeCancelRequested bool        `json:"runtime_cancel_requested"`
	Affected               bool        `json:"affected"`
	ActorID                string      `json:"actor_id,omitempty"`
}

// OKResponse is returned by endpoints that only report success.
type OKResponse struct {
	OK bool `json:"ok"`
}

// AgentEventKind discriminates durable timeline events.
type AgentEventKind string

const (
	AgentEventKindInput             AgentEventKind = "agent_input"
	AgentEventKindModelOutput       AgentEventKind = "model_output"
	AgentEventKindToolResult        AgentEventKind = "tool_result"
	AgentEventKindContextCheckpoint AgentEventKind = "context_checkpoint"
)

// AgentEvent is the shared flat representation of the four durable event
// variants. EventKind selects which optional fields are meaningful.
type AgentEvent struct {
	ID             string         `json:"id"`
	OrgID          string         `json:"org_id"`
	ProjectID      string         `json:"project_id"`
	AgentID        string         `json:"agent_id"`
	TurnID         string         `json:"turn_id"`
	TurnSequence   int64          `json:"turn_sequence"`
	IsOpeningEvent bool           `json:"is_opening_event"`
	Sequence       int64          `json:"sequence"`
	EventKind      AgentEventKind `json:"event_kind"`
	CreatedAt      time.Time      `json:"created_at"`

	// agent_input fields
	AgentInputID        string         `json:"agent_input_id,omitempty"`
	InputKind           AgentInputKind `json:"input_kind,omitempty"`
	ActorID             string         `json:"actor_id,omitempty"`
	InputIdempotencyKey string         `json:"input_idempotency_key,omitempty"`
	ControlType         string         `json:"control_type,omitempty"`
	InteractionID       string         `json:"interaction_id,omitempty"`
	AgentConfigID       string         `json:"agent_config_id,omitempty"`
	ContentBlocks       []ContentBlock `json:"content_blocks,omitempty"`

	// model_output fields
	ModelCallContextID string          `json:"model_call_context_id,omitempty"`
	StopReason         string          `json:"stop_reason,omitempty"`
	Usage              *ModelUsage     `json:"usage,omitempty"`
	ProviderMetadata   json.RawMessage `json:"provider_metadata,omitempty"`

	// tool_result fields
	ToolCallID string          `json:"tool_call_id,omitempty"`
	Outcome    ToolCallOutcome `json:"outcome,omitempty"`

	// context_checkpoint fields
	ContextCheckpointID            string `json:"context_checkpoint_id,omitempty"`
	SummarizedThroughEventSequence int64  `json:"summarized_through_event_sequence,omitempty"`
	Summary                        string `json:"summary,omitempty"`
}

// ModelUsage reports token counts for one model call.
type ModelUsage struct {
	InputTokensTotal      int64 `json:"input_tokens_total,omitempty"`
	UncachedInputTokens   int64 `json:"uncached_input_tokens,omitempty"`
	OutputTokensTotal     int64 `json:"output_tokens_total,omitempty"`
	ReasoningOutputTokens int64 `json:"reasoning_output_tokens,omitempty"`
	CacheReadInputTokens  int64 `json:"cache_read_input_tokens,omitempty"`
	CacheWriteInputTokens int64 `json:"cache_write_input_tokens,omitempty"`
}

// ListAgentEventsResponse is one page of the agent timeline.
type ListAgentEventsResponse struct {
	Data               []AgentEvent `json:"data"`
	NextAfterSequence  int64        `json:"next_after_sequence"`
	NextBeforeSequence *int64       `json:"next_before_sequence"`
	HasMore            bool         `json:"has_more"`
}

// AgentTurn is one turn summary.
type AgentTurn struct {
	ID                  string       `json:"id"`
	AgentID             string       `json:"agent_id"`
	TurnSequence        int64        `json:"turn_sequence"`
	EventCount          int64        `json:"event_count"`
	OpeningEvents       []AgentEvent `json:"opening_events"`
	LatestEvent         *AgentEvent  `json:"latest_event,omitempty"`
	LatestSemanticEvent *AgentEvent  `json:"latest_semantic_event,omitempty"`
	StartedAt           time.Time    `json:"started_at"`
	UpdatedAt           time.Time    `json:"updated_at"`
}

// ListAgentTurnsResponse is one page of turns.
type ListAgentTurnsResponse struct {
	Data                   []AgentTurn `json:"data"`
	NextBeforeTurnSequence *int64      `json:"next_before_turn_sequence"`
}

// ListTurnEventsResponse is one page of events for a turn.
type ListTurnEventsResponse struct {
	Data               []AgentEvent `json:"data"`
	NextBeforeSequence *int64       `json:"next_before_sequence"`
}

// ListEventsOptions selects a page of agent events.
type ListEventsOptions struct {
	AfterSequence  int64
	BeforeSequence int64
	Limit          int
}

// ListTurnsOptions selects a page of turns.
type ListTurnsOptions struct {
	BeforeTurnSequence int64
	Limit              int
}

// ListTurnEventsOptions selects a page of events within a turn.
type ListTurnEventsOptions struct {
	BeforeSequence int64
	Limit          int
}

// StreamEventsOptions controls the SSE event stream.
type StreamEventsOptions struct {
	AfterSequence int64
	StreamDeltas  bool
	// LastEventID replays from the last durable sequence a client observed.
	LastEventID int64
}

// AgentInteractionState is the lifecycle state of an interaction.
type AgentInteractionState string

const (
	AgentInteractionStateOpen     AgentInteractionState = "open"
	AgentInteractionStateResolved AgentInteractionState = "resolved"
	AgentInteractionStateCanceled AgentInteractionState = "canceled"
)

// AgentInteractionKind distinguishes permission prompts from questions.
type AgentInteractionKind string

const (
	AgentInteractionKindPermission AgentInteractionKind = "permission"
	AgentInteractionKindQuestion   AgentInteractionKind = "question"
)

// InteractionForm is the form shown for an interaction.
type InteractionForm struct {
	Title     string                    `json:"title"`
	Context   []json.RawMessage         `json:"context,omitempty"`
	Questions []InteractionFormQuestion `json:"questions"`
}

// InteractionFormQuestion is one question in an interaction form.
type InteractionFormQuestion struct {
	Prompt   string                  `json:"prompt"`
	Multiple bool                    `json:"multiple,omitempty"`
	Options  []InteractionFormOption `json:"options"`
}

// InteractionFormOption is one selectable option.
type InteractionFormOption struct {
	Label      string `json:"label"`
	AllowsText bool   `json:"allows_text,omitempty"`
}

// InteractionAnswer answers one question. Option indices are zero-based;
// permission prompts use 0 for allow and 1 for deny.
type InteractionAnswer struct {
	OptionIndices []int  `json:"option_indices"`
	Text          string `json:"text,omitempty"`
}

// InteractionResolution records the answers of a resolved interaction.
type InteractionResolution struct {
	Answers []InteractionAnswer `json:"answers"`
}

// AgentInteraction is a permission prompt or question.
type AgentInteraction struct {
	ID                string                 `json:"id"`
	OrgID             string                 `json:"org_id"`
	ProjectID         string                 `json:"project_id"`
	AgentID           string                 `json:"agent_id"`
	ToolCallID        string                 `json:"tool_call_id"`
	ToolName          string                 `json:"tool_name,omitempty"`
	AgentName         string                 `json:"agent_name,omitempty"`
	SubagentKey       string                 `json:"subagent_key,omitempty"`
	InteractionKind   AgentInteractionKind   `json:"interaction_kind"`
	State             AgentInteractionState  `json:"state"`
	Request           *InteractionForm       `json:"request"`
	Resolution        *InteractionResolution `json:"resolution,omitempty"`
	ResolvedByInputID string                 `json:"resolved_by_input_id,omitempty"`
	CreatedAt         time.Time              `json:"created_at"`
	ResolvedAt        *time.Time             `json:"resolved_at,omitempty"`
}

// ListAgentInteractionsResponse is one page of interactions.
type ListAgentInteractionsResponse struct {
	Data       []AgentInteraction `json:"data"`
	NextCursor *string            `json:"next_cursor"`
}

// ListInteractionsOptions filters and paginates interactions.
type ListInteractionsOptions struct {
	State            AgentInteractionState
	IncludeSubagents bool
	Limit            int
	Cursor           string
}

// ResolveAgentInteractionRequest answers an open interaction.
type ResolveAgentInteractionRequest struct {
	Answers []InteractionAnswer  `json:"answers"`
	Actor   *ExternalActorParams `json:"actor,omitempty"`
}

// ToolCallState is the current lifecycle state of a tool call.
type ToolCallState string

const (
	ToolCallStateAwaitingAuthorization ToolCallState = "awaiting_authorization"
	ToolCallStateAwaitingPermission    ToolCallState = "awaiting_permission"
	ToolCallStateReady                 ToolCallState = "ready"
	ToolCallStateRunning               ToolCallState = "running"
	ToolCallStateWaiting               ToolCallState = "waiting"
	ToolCallStateCompleted             ToolCallState = "completed"
)

// ToolCallType says who manages execution.
type ToolCallType string

const (
	ToolCallTypeBuiltIn ToolCallType = "built_in"
	ToolCallTypeCustom  ToolCallType = "custom"
	ToolCallTypeMCP     ToolCallType = "mcp"
)

// ToolCallOutcome is a terminal tool call outcome.
type ToolCallOutcome string

const (
	ToolCallOutcomeSucceeded ToolCallOutcome = "succeeded"
	ToolCallOutcomeFailed    ToolCallOutcome = "failed"
	ToolCallOutcomeDenied    ToolCallOutcome = "denied"
	ToolCallOutcomeCanceled  ToolCallOutcome = "canceled"
)

// ToolCall is a model-emitted tool call with its current state.
type ToolCall struct {
	ID             string          `json:"id"`
	AgentID        string          `json:"agent_id"`
	TurnID         string          `json:"turn_id"`
	ProviderCallID string          `json:"provider_call_id"`
	Name           string          `json:"name"`
	Input          json.RawMessage `json:"input"`
	Type           ToolCallType    `json:"type"`
	State          ToolCallState   `json:"state"`
	Outcome        ToolCallOutcome `json:"outcome,omitempty"`
	CompletedAt    *time.Time      `json:"completed_at,omitempty"`
	CreatedAt      time.Time       `json:"created_at"`
}

// ToolResult is the durable result of a tool call.
type ToolResult struct {
	EventID       string          `json:"event_id"`
	AgentID       string          `json:"agent_id"`
	ToolCallID    string          `json:"tool_call_id"`
	Outcome       ToolCallOutcome `json:"outcome"`
	ContentBlocks []ContentBlock  `json:"content_blocks"`
	CreatedAt     time.Time       `json:"created_at"`
}

// SubmitToolCallResultRequest completes a ready custom tool call.
type SubmitToolCallResultRequest struct {
	Outcome       ToolCallOutcome `json:"outcome"`
	ContentBlocks []ContentBlock  `json:"content_blocks"`
}

// SubmitToolCallResultResponse returns the completed call and its result.
type SubmitToolCallResultResponse struct {
	ToolCall   *ToolCall   `json:"tool_call"`
	ToolResult *ToolResult `json:"tool_result"`
}

// ListToolCallsResponse is one page of tool calls.
type ListToolCallsResponse struct {
	Data       []ToolCall `json:"data"`
	NextCursor *string    `json:"next_cursor"`
}

// ListToolCallsOptions filters and paginates tool calls.
type ListToolCallsOptions struct {
	State            ToolCallState
	Type             ToolCallType
	IncludeSubagents bool
	Limit            int
	Cursor           string
}

// ToolCallUpdate is an ephemeral tool lifecycle notification on the stream.
type ToolCallUpdate struct {
	ToolCallID        string                  `json:"tool_call_id"`
	AgentID           string                  `json:"agent_id,omitempty"`
	State             ToolCallState           `json:"state"`
	InteractionUpdate *AgentInteractionUpdate `json:"interaction_update,omitempty"`
}

// AgentInteractionUpdate accompanies a tool lifecycle change that opens,
// resolves, or cancels an interaction.
type AgentInteractionUpdate struct {
	ID              string                `json:"id"`
	InteractionKind AgentInteractionKind  `json:"interaction_kind"`
	State           AgentInteractionState `json:"state"`
}

// ModelOutputDelta is an ephemeral preview frame for an in-flight model call.
type ModelOutputDelta struct {
	TurnID             string                `json:"turn_id"`
	ModelCallContextID string                `json:"model_call_context_id"`
	Seq                int64                 `json:"seq"`
	SourceSeqStart     int64                 `json:"source_seq_start"`
	SourceSeqEnd       int64                 `json:"source_seq_end"`
	CoalescedCount     int64                 `json:"coalesced_count"`
	Event              ModelOutputDeltaEvent `json:"event"`
}

// ModelOutputDeltaEvent is the shared flat representation of the delta event
// variants. Kind selects which fields are meaningful.
type ModelOutputDeltaEvent struct {
	Kind       string                 `json:"kind"`
	BlockIndex int                    `json:"block_index,omitempty"`
	Delta      string                 `json:"delta,omitempty"`
	Block      json.RawMessage        `json:"block,omitempty"`
	Stop       *ModelOutputStop       `json:"stop,omitempty"`
	Error      *ModelOutputDeltaError `json:"error,omitempty"`
}

// ModelOutputStop is the message stop payload of a delta.
type ModelOutputStop struct {
	Reason string     `json:"reason"`
	Usage  ModelUsage `json:"usage"`
}

// ModelOutputDeltaError is the error payload of a delta.
type ModelOutputDeltaError struct {
	Message string `json:"message"`
}

// Artifact is an uploaded agent artifact.
type Artifact struct {
	ID          string    `json:"id"`
	OrgID       string    `json:"org_id"`
	ProjectID   string    `json:"project_id"`
	AgentID     string    `json:"agent_id"`
	ContentType string    `json:"content_type,omitempty"`
	Filename    string    `json:"filename,omitempty"`
	Digest      string    `json:"digest,omitempty"`
	SizeBytes   int64     `json:"size_bytes,omitempty"`
	CreatedAt   time.Time `json:"created_at"`
}

// ArtifactContent is the byte stream of an artifact. Close it when done.
type ArtifactContent struct {
	ContentType string
	Body        io.ReadCloser
}

// Close releases the artifact response body.
func (a *ArtifactContent) Close() error {
	if a == nil || a.Body == nil {
		return nil
	}
	return a.Body.Close()
}
