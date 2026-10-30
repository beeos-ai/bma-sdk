// Package bmarest is a typed Go client for the BMA public REST API. It covers
// the agent execution surface needed by Beework: launching and reading agents,
// sending inputs, streaming and paging events, resolving interactions, working
// with custom tool calls, and downloading artifacts.
package bmarest

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"strconv"
	"strings"
)

const (
	// DefaultBaseURL is the hosted BMA API root, including the /v1 prefix.
	DefaultBaseURL = "https://api.bma.beeos.ai/v1"
	userAgent      = "bma-sdks-go/0.1.0"
	maxErrorBody   = 1 << 20
)

// Options configures a Client.
type Options struct {
	// BaseURL is the API root, for example https://api.bma.beeos.ai/v1.
	// It defaults to DefaultBaseURL.
	BaseURL string
	// Token is a BMA personal or organization bearer token.
	Token string
	// HTTPClient is optional. The zero value uses http.DefaultClient; callers
	// control request lifetime through the context.
	HTTPClient *http.Client
}

// Client calls the BMA REST API.
type Client struct {
	baseURL    string
	token      string
	httpClient *http.Client
}

// NewClient validates options and returns a client.
func NewClient(options Options) (*Client, error) {
	if strings.TrimSpace(options.Token) == "" {
		return nil, fmt.Errorf("bmarest: Token is required")
	}
	baseURL := strings.TrimRight(strings.TrimSpace(options.BaseURL), "/")
	if baseURL == "" {
		baseURL = DefaultBaseURL
	}
	parsed, err := url.Parse(baseURL)
	if err != nil {
		return nil, fmt.Errorf("bmarest: invalid BaseURL: %w", err)
	}
	if parsed.Scheme != "http" && parsed.Scheme != "https" {
		return nil, fmt.Errorf("bmarest: BaseURL must use http or https")
	}
	httpClient := options.HTTPClient
	if httpClient == nil {
		httpClient = http.DefaultClient
	}
	return &Client{baseURL: baseURL, token: options.Token, httpClient: httpClient}, nil
}

// ErrorCode is a stable BMA error code.
type ErrorCode string

const (
	ErrorCodeInvalidRequest             ErrorCode = "invalid_request"
	ErrorCodeUnauthorized               ErrorCode = "unauthorized"
	ErrorCodeForbidden                  ErrorCode = "forbidden"
	ErrorCodeNotFound                   ErrorCode = "not_found"
	ErrorCodeConflict                   ErrorCode = "conflict"
	ErrorCodeFileContentConflict        ErrorCode = "file_content_conflict"
	ErrorCodeFileReadOnly               ErrorCode = "file_read_only"
	ErrorCodeExpectedDigestRequired     ErrorCode = "expected_digest_required"
	ErrorCodeNotAFile                   ErrorCode = "not_a_file"
	ErrorCodeGone                       ErrorCode = "gone"
	ErrorCodeRequestTooLarge            ErrorCode = "request_too_large"
	ErrorCodeUnsupportedMediaType       ErrorCode = "unsupported_media_type"
	ErrorCodeUnprocessable              ErrorCode = "unprocessable"
	ErrorCodeUpstreamUnavailable        ErrorCode = "upstream_unavailable"
	ErrorCodeRateLimited                ErrorCode = "rate_limited"
	ErrorCodeInternalError              ErrorCode = "internal_error"
	ErrorCodeServiceUnavailable         ErrorCode = "service_unavailable"
	ErrorCodeIdempotencyKeyConflict     ErrorCode = "idempotency_key_conflict"
	ErrorCodeAgentBacklogFull           ErrorCode = "agent_backlog_full"
	ErrorCodeStateTransitionConflict    ErrorCode = "state_transition_conflict"
	ErrorCodeManagedWorkAdmissionDenied ErrorCode = "managed_work_admission_denied"
	ErrorCodePendingWork                ErrorCode = "pending_work"
	ErrorCodeNotWakeCapable             ErrorCode = "not_wake_capable"
	ErrorCodeDaemonRuntimeUnregistered  ErrorCode = "daemon_runtime_unregistered"
	ErrorCodeValidationFailed           ErrorCode = "validation_failed"
	ErrorCodeCSRFCheckFailed            ErrorCode = "csrf_check_failed"
	ErrorCodeAuthenticationUnavailable  ErrorCode = "authentication_unavailable"
)

// AgentConfigErrorIssue describes one field-level validation failure.
type AgentConfigErrorIssue struct {
	Path    string `json:"path"`
	Message string `json:"message"`
	Line    int    `json:"line,omitempty"`
	Column  int    `json:"column,omitempty"`
}

// APIError is a non-2xx response from the BMA API.
type APIError struct {
	StatusCode    int
	Code          ErrorCode
	Message       string
	CurrentDigest string
	Issues        []AgentConfigErrorIssue
}

// Error implements error.
func (e *APIError) Error() string {
	code := string(e.Code)
	if code == "" {
		code = "unknown"
	}
	if e.Message == "" {
		return fmt.Sprintf("bmarest: HTTP %d %s", e.StatusCode, code)
	}
	return fmt.Sprintf("bmarest: HTTP %d %s: %s", e.StatusCode, code, e.Message)
}

// Retryable reports whether a retry may succeed without changing the request.
func (e *APIError) Retryable() bool {
	return e.StatusCode == http.StatusTooManyRequests ||
		e.StatusCode == http.StatusServiceUnavailable ||
		e.Code == ErrorCodeServiceUnavailable ||
		e.Code == ErrorCodeRateLimited
}

func newAPIError(resp *http.Response) *APIError {
	apiErr := &APIError{StatusCode: resp.StatusCode}
	raw, err := io.ReadAll(io.LimitReader(resp.Body, maxErrorBody))
	if err == nil && len(raw) > 0 {
		var body struct {
			Error         string                  `json:"error"`
			Code          ErrorCode               `json:"code"`
			CurrentDigest string                  `json:"current_digest"`
			Issues        []AgentConfigErrorIssue `json:"issues"`
		}
		if json.Unmarshal(raw, &body) == nil {
			apiErr.Message = body.Error
			apiErr.Code = body.Code
			apiErr.CurrentDigest = body.CurrentDigest
			apiErr.Issues = body.Issues
		}
	}
	if apiErr.Message == "" {
		apiErr.Message = http.StatusText(resp.StatusCode)
	}
	return apiErr
}

func (c *Client) do(ctx context.Context, method, path string, query url.Values, body any, headers http.Header) (*http.Response, error) {
	endpoint := c.baseURL + path
	if len(query) > 0 {
		endpoint += "?" + query.Encode()
	}

	var reader io.Reader
	if body != nil {
		raw, err := json.Marshal(body)
		if err != nil {
			return nil, fmt.Errorf("bmarest: encode request: %w", err)
		}
		reader = bytes.NewReader(raw)
	}

	req, err := http.NewRequestWithContext(ctx, method, endpoint, reader)
	if err != nil {
		return nil, fmt.Errorf("bmarest: create request: %w", err)
	}
	req.Header.Set("Authorization", "Bearer "+c.token)
	req.Header.Set("User-Agent", userAgent)
	req.Header.Set("Accept", "application/json")
	if body != nil {
		req.Header.Set("Content-Type", "application/json")
	}
	for key, values := range headers {
		req.Header.Del(key)
		for _, value := range values {
			req.Header.Add(key, value)
		}
	}

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("bmarest: %s %s: %w", method, path, err)
	}
	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		defer resp.Body.Close()
		return nil, newAPIError(resp)
	}
	return resp, nil
}

func (c *Client) doJSON(ctx context.Context, method, path string, query url.Values, body any, headers http.Header, out any) error {
	resp, err := c.do(ctx, method, path, query, body, headers)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	if out == nil {
		_, _ = io.Copy(io.Discard, resp.Body)
		return nil
	}
	if err := json.NewDecoder(resp.Body).Decode(out); err != nil {
		return fmt.Errorf("bmarest: decode response: %w", err)
	}
	return nil
}

func (s ProjectScope) validate() error {
	if strings.TrimSpace(s.OrgID) == "" {
		return fmt.Errorf("bmarest: ProjectScope.OrgID is required")
	}
	if strings.TrimSpace(s.ProjectID) == "" {
		return fmt.Errorf("bmarest: ProjectScope.ProjectID is required")
	}
	return nil
}

func (s AgentScope) validate() error {
	if err := (ProjectScope{OrgID: s.OrgID, ProjectID: s.ProjectID}).validate(); err != nil {
		return err
	}
	if strings.TrimSpace(s.AgentID) == "" {
		return fmt.Errorf("bmarest: AgentScope.AgentID is required")
	}
	return nil
}

func projectPath(scope ProjectScope) string {
	return "/orgs/" + url.PathEscape(scope.OrgID) + "/projects/" + url.PathEscape(scope.ProjectID)
}

func agentPath(scope AgentScope) string {
	return projectPath(ProjectScope{OrgID: scope.OrgID, ProjectID: scope.ProjectID}) +
		"/agents/" + url.PathEscape(scope.AgentID)
}

func addString(query url.Values, key, value string) {
	if value != "" {
		query.Set(key, value)
	}
}

func addBool(query url.Values, key string, value bool) {
	if value {
		query.Set(key, "true")
	}
}

func addInt(query url.Values, key string, value int) {
	if value > 0 {
		query.Set(key, strconv.Itoa(value))
	}
}

func addInt64(query url.Values, key string, value int64) {
	if value > 0 {
		query.Set(key, strconv.FormatInt(value, 10))
	}
}

// CreateAgent launches an agent. Reuse RequestOptions.IdempotencyKey to make a
// retry return the already-created agent.
func (c *Client) CreateAgent(ctx context.Context, scope ProjectScope, request CreateAgentRequest, options RequestOptions) (*LaunchAgentResponse, error) {
	if err := scope.validate(); err != nil {
		return nil, err
	}
	headers := idempotencyHeaders(options)
	var response LaunchAgentResponse
	if err := c.doJSON(ctx, http.MethodPost, projectPath(scope)+"/agents", nil, request, headers, &response); err != nil {
		return nil, err
	}
	return &response, nil
}

// ListAgents lists the project's agents.
func (c *Client) ListAgents(ctx context.Context, scope ProjectScope, options ListAgentsOptions) (*ListAgentsResponse, error) {
	if err := scope.validate(); err != nil {
		return nil, err
	}
	query := url.Values{}
	addString(query, "name", options.Name)
	addString(query, "agent_profile_id", options.AgentProfileID)
	addString(query, "parent_agent_id", options.ParentAgentID)
	addBool(query, "include_subagents", options.IncludeSubagents)
	addBool(query, "include_archived", options.IncludeArchived)
	addBool(query, "include_usage", options.IncludeUsage)
	addString(query, "sort", options.Sort)
	addInt(query, "limit", options.Limit)
	addString(query, "cursor", options.Cursor)

	var response ListAgentsResponse
	if err := c.doJSON(ctx, http.MethodGet, projectPath(scope)+"/agents", query, nil, nil, &response); err != nil {
		return nil, err
	}
	return &response, nil
}

// GetAgent returns one agent with its machines and MCP connections.
func (c *Client) GetAgent(ctx context.Context, scope AgentScope) (*GetAgentResponse, error) {
	if err := scope.validate(); err != nil {
		return nil, err
	}
	var response GetAgentResponse
	if err := c.doJSON(ctx, http.MethodGet, agentPath(scope), nil, nil, nil, &response); err != nil {
		return nil, err
	}
	return &response, nil
}

// ArchiveAgent archives an agent.
func (c *Client) ArchiveAgent(ctx context.Context, scope AgentScope, options RequestOptions) (*CurrentAgentResponse, error) {
	if err := scope.validate(); err != nil {
		return nil, err
	}
	var response CurrentAgentResponse
	if err := c.doJSON(ctx, http.MethodPost, agentPath(scope)+"/archive", nil, nil, idempotencyHeaders(options), &response); err != nil {
		return nil, err
	}
	return &response, nil
}

// CancelAgent stops the current turn. request may be nil.
func (c *Client) CancelAgent(ctx context.Context, scope AgentScope, request *CancelAgentRequest) (*CancelAgentResponse, error) {
	if err := scope.validate(); err != nil {
		return nil, err
	}
	var body any
	if request != nil {
		body = request
	}
	var response CancelAgentResponse
	if err := c.doJSON(ctx, http.MethodPost, agentPath(scope)+"/cancel", nil, body, nil, &response); err != nil {
		return nil, err
	}
	return &response, nil
}

// CreateAgentInput sends content to an agent.
func (c *Client) CreateAgentInput(ctx context.Context, scope AgentScope, request CreateAgentInputRequest, options RequestOptions) (*AgentInputEnvelope, error) {
	if err := scope.validate(); err != nil {
		return nil, err
	}
	var response AgentInputEnvelope
	if err := c.doJSON(ctx, http.MethodPost, agentPath(scope)+"/inputs", nil, request, idempotencyHeaders(options), &response); err != nil {
		return nil, err
	}
	return &response, nil
}

// ListBacklogInputs lists waiting steering and queued inputs.
func (c *Client) ListBacklogInputs(ctx context.Context, scope AgentScope, options PageOptions) (*ListAgentInputsResponse, error) {
	if err := scope.validate(); err != nil {
		return nil, err
	}
	query := url.Values{}
	addInt(query, "limit", options.Limit)
	addString(query, "cursor", options.Cursor)

	var response ListAgentInputsResponse
	if err := c.doJSON(ctx, http.MethodGet, agentPath(scope)+"/inputs/backlog", query, nil, nil, &response); err != nil {
		return nil, err
	}
	return &response, nil
}

// CancelBacklogInput cancels one queued input.
func (c *Client) CancelBacklogInput(ctx context.Context, scope AgentScope, inputID string) (*OKResponse, error) {
	if err := scope.validate(); err != nil {
		return nil, err
	}
	var response OKResponse
	if err := c.doJSON(ctx, http.MethodPost, agentPath(scope)+"/inputs/"+url.PathEscape(inputID)+"/cancel", nil, nil, nil, &response); err != nil {
		return nil, err
	}
	return &response, nil
}

// MoveBacklogInput moves one queued input.
func (c *Client) MoveBacklogInput(ctx context.Context, scope AgentScope, inputID string, request MoveQueuedBacklogInputRequest) (*OKResponse, error) {
	if err := scope.validate(); err != nil {
		return nil, err
	}
	var response OKResponse
	if err := c.doJSON(ctx, http.MethodPost, agentPath(scope)+"/inputs/"+url.PathEscape(inputID)+"/move", nil, request, nil, &response); err != nil {
		return nil, err
	}
	return &response, nil
}

// PromoteBacklogInputToSteering promotes one queued input.
func (c *Client) PromoteBacklogInputToSteering(ctx context.Context, scope AgentScope, inputID string, request PromoteQueuedInputToSteeringRequest) (*OKResponse, error) {
	if err := scope.validate(); err != nil {
		return nil, err
	}
	var response OKResponse
	if err := c.doJSON(ctx, http.MethodPost, agentPath(scope)+"/inputs/"+url.PathEscape(inputID)+"/promote_to_steering", nil, request, nil, &response); err != nil {
		return nil, err
	}
	return &response, nil
}

// DemoteBacklogInputToQueued demotes one steering input.
func (c *Client) DemoteBacklogInputToQueued(ctx context.Context, scope AgentScope, inputID string) (*OKResponse, error) {
	if err := scope.validate(); err != nil {
		return nil, err
	}
	var response OKResponse
	if err := c.doJSON(ctx, http.MethodPost, agentPath(scope)+"/inputs/"+url.PathEscape(inputID)+"/demote_to_queued", nil, nil, nil, &response); err != nil {
		return nil, err
	}
	return &response, nil
}

// ListEvents returns one page of durable agent events.
func (c *Client) ListEvents(ctx context.Context, scope AgentScope, options ListEventsOptions) (*ListAgentEventsResponse, error) {
	if err := scope.validate(); err != nil {
		return nil, err
	}
	query := url.Values{}
	addInt64(query, "after_sequence", options.AfterSequence)
	addInt64(query, "before_sequence", options.BeforeSequence)
	addInt(query, "limit", options.Limit)

	var response ListAgentEventsResponse
	if err := c.doJSON(ctx, http.MethodGet, agentPath(scope)+"/events", query, nil, nil, &response); err != nil {
		return nil, err
	}
	return &response, nil
}

// ListTurns returns one page of turns, newest first.
func (c *Client) ListTurns(ctx context.Context, scope AgentScope, options ListTurnsOptions) (*ListAgentTurnsResponse, error) {
	if err := scope.validate(); err != nil {
		return nil, err
	}
	query := url.Values{}
	addInt64(query, "before_turn_sequence", options.BeforeTurnSequence)
	addInt(query, "limit", options.Limit)

	var response ListAgentTurnsResponse
	if err := c.doJSON(ctx, http.MethodGet, agentPath(scope)+"/turns", query, nil, nil, &response); err != nil {
		return nil, err
	}
	return &response, nil
}

// ListTurnEvents returns one page of events for a turn.
func (c *Client) ListTurnEvents(ctx context.Context, scope AgentScope, turnID string, options ListTurnEventsOptions) (*ListTurnEventsResponse, error) {
	if err := scope.validate(); err != nil {
		return nil, err
	}
	query := url.Values{}
	addInt64(query, "before_sequence", options.BeforeSequence)
	addInt(query, "limit", options.Limit)

	var response ListTurnEventsResponse
	path := agentPath(scope) + "/turns/" + url.PathEscape(turnID) + "/events"
	if err := c.doJSON(ctx, http.MethodGet, path, query, nil, nil, &response); err != nil {
		return nil, err
	}
	return &response, nil
}

// StreamEvents opens the agent's server-sent event stream. The caller must
// close the returned stream.
func (c *Client) StreamEvents(ctx context.Context, scope AgentScope, options StreamEventsOptions) (*EventStream, error) {
	if err := scope.validate(); err != nil {
		return nil, err
	}
	query := url.Values{}
	addInt64(query, "after_sequence", options.AfterSequence)
	addBool(query, "stream_deltas", options.StreamDeltas)

	headers := http.Header{}
	headers.Set("Accept", "text/event-stream")
	if options.LastEventID > 0 {
		headers.Set("Last-Event-ID", strconv.FormatInt(options.LastEventID, 10))
	}
	resp, err := c.do(ctx, http.MethodGet, agentPath(scope)+"/events/stream", query, nil, headers)
	if err != nil {
		return nil, err
	}
	return newEventStream(resp.Body), nil
}

// ListInteractions returns one page of an agent's interactions.
func (c *Client) ListInteractions(ctx context.Context, scope AgentScope, options ListInteractionsOptions) (*ListAgentInteractionsResponse, error) {
	if err := scope.validate(); err != nil {
		return nil, err
	}
	query := url.Values{}
	if options.State != "" {
		query.Set("state", string(options.State))
	}
	addBool(query, "include_subagents", options.IncludeSubagents)
	addInt(query, "limit", options.Limit)
	addString(query, "cursor", options.Cursor)

	var response ListAgentInteractionsResponse
	if err := c.doJSON(ctx, http.MethodGet, agentPath(scope)+"/interactions", query, nil, nil, &response); err != nil {
		return nil, err
	}
	return &response, nil
}

// ResolveInteraction answers an open permission prompt or question.
func (c *Client) ResolveInteraction(ctx context.Context, scope AgentScope, interactionID string, request ResolveAgentInteractionRequest, options RequestOptions) (*AgentInteraction, error) {
	if err := scope.validate(); err != nil {
		return nil, err
	}
	var response AgentInteraction
	path := agentPath(scope) + "/interactions/" + url.PathEscape(interactionID) + "/resolve"
	if err := c.doJSON(ctx, http.MethodPost, path, nil, request, idempotencyHeaders(options), &response); err != nil {
		return nil, err
	}
	return &response, nil
}

// ListToolCalls returns one page of an agent's tool calls.
func (c *Client) ListToolCalls(ctx context.Context, scope AgentScope, options ListToolCallsOptions) (*ListToolCallsResponse, error) {
	if err := scope.validate(); err != nil {
		return nil, err
	}
	query := url.Values{}
	if options.State != "" {
		query.Set("state", string(options.State))
	}
	if options.Type != "" {
		query.Set("type", string(options.Type))
	}
	addBool(query, "include_subagents", options.IncludeSubagents)
	addInt(query, "limit", options.Limit)
	addString(query, "cursor", options.Cursor)

	var response ListToolCallsResponse
	if err := c.doJSON(ctx, http.MethodGet, agentPath(scope)+"/tool-calls", query, nil, nil, &response); err != nil {
		return nil, err
	}
	return &response, nil
}

// SubmitToolCallResult completes a ready custom tool call.
func (c *Client) SubmitToolCallResult(ctx context.Context, scope AgentScope, toolCallID string, request SubmitToolCallResultRequest) (*SubmitToolCallResultResponse, error) {
	if err := scope.validate(); err != nil {
		return nil, err
	}
	var response SubmitToolCallResultResponse
	path := agentPath(scope) + "/tool-calls/" + url.PathEscape(toolCallID) + "/result"
	if err := c.doJSON(ctx, http.MethodPost, path, nil, request, nil, &response); err != nil {
		return nil, err
	}
	return &response, nil
}

// GetArtifact returns artifact metadata.
func (c *Client) GetArtifact(ctx context.Context, scope AgentScope, artifactID string) (*Artifact, error) {
	if err := scope.validate(); err != nil {
		return nil, err
	}
	var response Artifact
	path := agentPath(scope) + "/artifacts/" + url.PathEscape(artifactID)
	if err := c.doJSON(ctx, http.MethodGet, path, nil, nil, nil, &response); err != nil {
		return nil, err
	}
	return &response, nil
}

// GetArtifactContent downloads artifact bytes. The caller must close the body.
func (c *Client) GetArtifactContent(ctx context.Context, scope AgentScope, artifactID string) (*ArtifactContent, error) {
	if err := scope.validate(); err != nil {
		return nil, err
	}
	headers := http.Header{}
	headers.Set("Accept", "*/*")
	path := agentPath(scope) + "/artifacts/" + url.PathEscape(artifactID) + "/content"
	resp, err := c.do(ctx, http.MethodGet, path, nil, nil, headers)
	if err != nil {
		return nil, err
	}
	return &ArtifactContent{ContentType: resp.Header.Get("Content-Type"), Body: resp.Body}, nil
}

func idempotencyHeaders(options RequestOptions) http.Header {
	if options.IdempotencyKey == "" {
		return nil
	}
	headers := http.Header{}
	headers.Set("Idempotency-Key", options.IdempotencyKey)
	return headers
}
