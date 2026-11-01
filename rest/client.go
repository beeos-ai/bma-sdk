// Package rest is the Go client for the BMA public REST API. Every operation
// and model in generated.go is generated from contracts/bma/rest.openapi.yaml;
// this file adds only the transport policy the contract does not describe:
// bearer authentication, error decoding, and the server-sent event stream.
package rest

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"strings"
)

const (
	// DefaultBaseURL is the hosted BMA API root, including the /v1 prefix.
	DefaultBaseURL = "https://api.bma.beeos.ai/v1"
	userAgent      = "bma-sdks-go/0.4.1"
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

// Client is the generated REST client with bearer authentication attached.
// The generated *ClientWithResponses methods are promoted, so operations are
// called as client.CreateAgentWithResponse, client.ListEventsWithResponse,
// and so on. Use OpenEventStream for the SSE endpoint and DownloadArtifact
// for artifact bytes.
type Client struct {
	*ClientWithResponses

	server     string // API root with a trailing slash, as the generated request builders require
	token      string
	httpClient *http.Client
}

// New validates options and returns an authenticated client.
func New(options Options) (*Client, error) {
	token := strings.TrimSpace(options.Token)
	if token == "" {
		return nil, fmt.Errorf("rest: Token is required")
	}
	baseURL := strings.TrimRight(strings.TrimSpace(options.BaseURL), "/")
	if baseURL == "" {
		baseURL = DefaultBaseURL
	}
	parsed, err := url.Parse(baseURL)
	if err != nil {
		return nil, fmt.Errorf("rest: invalid BaseURL: %w", err)
	}
	if parsed.Scheme != "http" && parsed.Scheme != "https" {
		return nil, fmt.Errorf("rest: BaseURL must use http or https")
	}
	httpClient := options.HTTPClient
	if httpClient == nil {
		httpClient = http.DefaultClient
	}

	// The generated New*Request builders resolve operation paths relative to
	// the server URL; without a trailing slash the last segment (/v1) is lost.
	client := &Client{server: baseURL + "/", token: token, httpClient: httpClient}
	generated, err := NewClientWithResponses(
		baseURL,
		WithHTTPClient(httpClient),
		WithRequestEditorFn(client.authenticate),
	)
	if err != nil {
		return nil, fmt.Errorf("rest: create client: %w", err)
	}
	client.ClientWithResponses = generated
	return client, nil
}

// NewClientWithToken is a convenience wrapper around New.
func NewClientWithToken(baseURL, token string, httpClient *http.Client) (*Client, error) {
	return New(Options{BaseURL: baseURL, Token: token, HTTPClient: httpClient})
}

func (c *Client) authenticate(_ context.Context, req *http.Request) error {
	req.Header.Set("Authorization", "Bearer "+c.token)
	req.Header.Set("User-Agent", userAgent)
	return nil
}

// Server returns the API root the client was configured with.
func (c *Client) Server() string { return strings.TrimSuffix(c.server, "/") }

// ErrorCode is a stable BMA error code.
type ErrorCode = string

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
	code := e.Code
	if code == "" {
		code = "unknown"
	}
	if e.Message == "" {
		return fmt.Sprintf("rest: HTTP %d %s", e.StatusCode, code)
	}
	return fmt.Sprintf("rest: HTTP %d %s: %s", e.StatusCode, code, e.Message)
}

// Retryable reports whether a retry may succeed without changing the request.
func (e *APIError) Retryable() bool {
	return e.StatusCode == http.StatusRequestTimeout ||
		e.StatusCode == http.StatusTooManyRequests ||
		e.StatusCode >= http.StatusInternalServerError ||
		e.Code == ErrorCodeServiceUnavailable ||
		e.Code == ErrorCodeRateLimited
}

// NewAPIError decodes a BMA error body. It never returns nil.
func NewAPIError(statusCode int, body []byte) *APIError {
	apiErr := &APIError{StatusCode: statusCode}
	if len(body) > 0 {
		var wire Error
		if json.Unmarshal(body, &wire) == nil {
			apiErr.Code = wire.Code
			apiErr.Message = wire.Error
			if wire.CurrentDigest != nil {
				apiErr.CurrentDigest = *wire.CurrentDigest
			}
			if wire.Issues != nil {
				apiErr.Issues = *wire.Issues
			}
		}
	}
	if apiErr.Message == "" {
		apiErr.Message = http.StatusText(statusCode)
	}
	return apiErr
}

// CheckResponse returns nil for 2xx status codes and an *APIError otherwise.
// Generated WithResponse methods return both success and error responses; pass
// their Body and HTTPResponse here.
func CheckResponse(resp *http.Response, body []byte) error {
	if resp.StatusCode >= 200 && resp.StatusCode < 300 {
		return nil
	}
	return NewAPIError(resp.StatusCode, body)
}

func newAPIErrorFromResponse(resp *http.Response) *APIError {
	defer resp.Body.Close()
	raw, err := io.ReadAll(io.LimitReader(resp.Body, maxErrorBody))
	if err != nil {
		return NewAPIError(resp.StatusCode, nil)
	}
	return NewAPIError(resp.StatusCode, raw)
}

// NewTextContentBlock builds a text content block.
func NewTextContentBlock(text string) TextContentBlock {
	return TextContentBlock{Type: TextContentBlockType("text"), Text: text}
}

// NewInlineMediaContentBlock builds an inline media content block. Data is the
// raw file content; it is base64-encoded on the wire by encoding/json.
func NewInlineMediaContentBlock(mediaType, filename string, data []byte) InlineMediaContentBlock {
	block := InlineMediaContentBlock{
		Type:      InlineMediaContentBlockType("media"),
		MediaType: InlineMediaContentBlockMediaType(mediaType),
		Data:      data,
	}
	if filename != "" {
		block.Filename = &filename
	}
	return block
}

// NewTextInputBlock builds a text block accepted by CreateAgentInputRequest.
func NewTextInputBlock(text string) CreateAgentInputContentBlock {
	var block CreateAgentInputContentBlock
	_ = block.FromTextContentBlock(NewTextContentBlock(text))
	return block
}

// NewMediaInputBlock builds an inline media block accepted by
// CreateAgentInputRequest.
func NewMediaInputBlock(mediaType, filename string, data []byte) CreateAgentInputContentBlock {
	var block CreateAgentInputContentBlock
	_ = block.FromInlineMediaContentBlock(NewInlineMediaContentBlock(mediaType, filename, data))
	return block
}
