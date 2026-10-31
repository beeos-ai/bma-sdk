// Package facadeext is the Go client for the BMA extensions to the Anthropic
// Managed Agents API.
//
// The standard facade routes (/v1/agents, /v1/environments, /v1/sessions,
// events, events/stream, /v1/files, /v1/memory_stores) are served by the
// official Anthropic SDKs pointed at a BMA deployment. Everything in this
// package is a BMA extension that is NOT part of the Anthropic contract:
//
//   - GET  /v1/sessions/{id}/desktop/stream: desktop watch ticket
//   - POST /v1/sessions/{id}/files: multipart session file upload
//   - GET  /v1/sessions/{id}/files: session file listing
//   - POST/GET /v1/sessions/{id}/resources and
//     DELETE /v1/sessions/{id}/resources/{resource_id}: mount a project file
//     into an existing session
//   - the bma_sequence, Idempotency-Key, mcp_servers[].bma_auth and model
//     credential override fields (types ModelConfigOverride, MCPServerBMAAuth,
//     BMASequence)
//
// generated.go is generated from contracts/bma/facade-extensions.openapi.yaml;
// this file adds authentication, error decoding, and multipart encoding.
package facadeext

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"mime"
	"mime/multipart"
	"net/http"
	"net/url"
	"strings"
)

const (
	// IdempotencyKeyHeader is the BMA extension header forwarded on
	// POST /v1/sessions and POST /v1/sessions/{id}/events.
	IdempotencyKeyHeader = "Idempotency-Key"
	// MaxSessionFileBytes is the facade limit for one uploaded session file.
	MaxSessionFileBytes = 8 << 20

	userAgent    = "bma-sdks-go/0.4.0"
	maxErrorBody = 1 << 20
)

// Options configures a Client.
type Options struct {
	// BaseURL is the facade origin without /v1, for example
	// https://api.bma.beeos.ai.
	BaseURL string
	// APIKey is the BMA organization API key, sent as x-api-key.
	APIKey string
	// ProjectID selects the project (x-bma-project-id). Required when the key
	// can read more than one project and the deployment has no default.
	ProjectID string
	// HTTPClient is optional and defaults to http.DefaultClient.
	HTTPClient *http.Client
}

// Client calls the BMA extension routes of the facade.
type Client struct {
	generated *ClientWithResponses
	apiKey    string
	projectID string
}

// New validates options and returns a client.
func New(options Options) (*Client, error) {
	apiKey := strings.TrimSpace(options.APIKey)
	if apiKey == "" {
		return nil, errors.New("facadeext: APIKey is required")
	}
	baseURL := strings.TrimRight(strings.TrimSpace(options.BaseURL), "/")
	parsed, err := url.Parse(baseURL)
	if err != nil || (parsed.Scheme != "http" && parsed.Scheme != "https") || parsed.Host == "" {
		return nil, errors.New("facadeext: BaseURL must be an http or https origin")
	}
	if strings.HasSuffix(baseURL, "/v1") {
		return nil, errors.New("facadeext: BaseURL must not include /v1")
	}
	httpClient := options.HTTPClient
	if httpClient == nil {
		httpClient = http.DefaultClient
	}
	client := &Client{apiKey: apiKey, projectID: strings.TrimSpace(options.ProjectID)}
	generated, err := NewClientWithResponses(baseURL,
		WithHTTPClient(httpClient), WithRequestEditorFn(client.authenticate))
	if err != nil {
		return nil, fmt.Errorf("facadeext: create client: %w", err)
	}
	client.generated = generated
	return client, nil
}

func (c *Client) authenticate(_ context.Context, req *http.Request) error {
	req.Header.Set("x-api-key", c.apiKey)
	req.Header.Set("User-Agent", userAgent)
	if c.projectID != "" {
		req.Header.Set("x-bma-project-id", c.projectID)
	}
	return nil
}

// Generated returns the low-level generated client for callers that need the
// raw responses.
func (c *Client) Generated() *ClientWithResponses { return c.generated }

// DesktopStreamOptions are the query parameters of GetSessionDesktopStream.
type DesktopStreamOptions struct {
	DesktopSessionID string
	// TTLSeconds is 15..120; zero keeps the server default.
	TTLSeconds int
	// Origin binds the ticket to a browser origin.
	Origin string
}

// GetSessionDesktopStream mints a single-use desktop watch ticket for a
// session (BMA extension). The returned Ticket is a credential.
func (c *Client) GetSessionDesktopStream(ctx context.Context, sessionID string, options DesktopStreamOptions) (*DesktopStream, error) {
	params := &GetSessionDesktopStreamParams{DesktopSessionId: options.DesktopSessionID}
	if options.TTLSeconds != 0 {
		params.TtlSeconds = &options.TTLSeconds
	}
	if options.Origin != "" {
		params.Origin = &options.Origin
	}
	resp, err := c.generated.GetSessionDesktopStreamWithResponse(ctx, sessionID, params)
	if err != nil {
		return nil, fmt.Errorf("facadeext: desktop stream: %w", err)
	}
	if err := CheckResponse(resp.HTTPResponse, resp.Body); err != nil {
		return nil, err
	}
	if resp.JSON200 == nil {
		return nil, errors.New("facadeext: desktop stream response has no body")
	}
	return resp.JSON200, nil
}

// UploadSessionFile stores one file in the session (BMA extension). The
// content is buffered and must be 1..MaxSessionFileBytes bytes.
func (c *Client) UploadSessionFile(ctx context.Context, sessionID, filename string, content io.Reader) (*SessionFile, error) {
	data, err := io.ReadAll(io.LimitReader(content, MaxSessionFileBytes+1))
	if err != nil {
		return nil, fmt.Errorf("facadeext: read session file: %w", err)
	}
	if len(data) == 0 || len(data) > MaxSessionFileBytes {
		return nil, fmt.Errorf("facadeext: session file must be 1..%d bytes", MaxSessionFileBytes)
	}
	var body bytes.Buffer
	writer := multipart.NewWriter(&body)
	part, err := writer.CreateFormFile("file", filename)
	if err != nil {
		return nil, fmt.Errorf("facadeext: encode session file: %w", err)
	}
	if _, err := part.Write(data); err != nil {
		return nil, fmt.Errorf("facadeext: encode session file: %w", err)
	}
	if err := writer.Close(); err != nil {
		return nil, fmt.Errorf("facadeext: encode session file: %w", err)
	}
	resp, err := c.generated.UploadSessionFileWithBodyWithResponse(
		ctx, sessionID, &UploadSessionFileParams{}, writer.FormDataContentType(), &body)
	if err != nil {
		return nil, fmt.Errorf("facadeext: upload session file: %w", err)
	}
	if err := CheckResponse(resp.HTTPResponse, resp.Body); err != nil {
		return nil, err
	}
	if resp.JSON200 == nil {
		return nil, errors.New("facadeext: upload response has no body")
	}
	return resp.JSON200, nil
}

// ListSessionFiles returns one page of session files (BMA extension). limit
// is 1..100 (zero keeps the server default); page is the previous NextPage.
func (c *Client) ListSessionFiles(ctx context.Context, sessionID string, limit int, page string) (*SessionFilePage, error) {
	params := &ListSessionFilesParams{}
	if limit != 0 {
		params.Limit = &limit
	}
	if page != "" {
		params.Page = &page
	}
	resp, err := c.generated.ListSessionFilesWithResponse(ctx, sessionID, params)
	if err != nil {
		return nil, fmt.Errorf("facadeext: list session files: %w", err)
	}
	if err := CheckResponse(resp.HTTPResponse, resp.Body); err != nil {
		return nil, err
	}
	if resp.JSON200 == nil {
		return nil, errors.New("facadeext: list response has no body")
	}
	return resp.JSON200, nil
}

// SessionFileContent is one downloaded session file: the uploaded bytes or an
// agent artifact of the session.
type SessionFileContent struct {
	Content     []byte
	ContentType string
	Filename    string
	Digest      string
}

// DownloadSessionFile returns one session file (BMA extension). fileID is the
// SessionFile.ID returned by upload or list; a file of another session is a
// 404. Digest is the sha256 of Content when the deployment sends it.
func (c *Client) DownloadSessionFile(ctx context.Context, sessionID, fileID string) (*SessionFileContent, error) {
	resp, err := c.generated.DownloadSessionFileWithResponse(ctx, sessionID, fileID, &DownloadSessionFileParams{})
	if err != nil {
		return nil, fmt.Errorf("facadeext: download session file: %w", err)
	}
	if err := CheckResponse(resp.HTTPResponse, resp.Body); err != nil {
		return nil, err
	}
	content := &SessionFileContent{Content: resp.Body}
	if resp.HTTPResponse != nil {
		header := resp.HTTPResponse.Header
		content.ContentType = header.Get("Content-Type")
		content.Filename = filenameFromDisposition(header.Get("Content-Disposition"))
		content.Digest = header.Get("X-BMA-File-Digest")
	}
	return content, nil
}

// SessionResourceOptions are the fields of AddSessionResource.
type SessionResourceOptions struct {
	// FileID is the project file (file_...) to mount.
	FileID string
	// MountPath is an absolute path below /mnt/session/uploads. Empty keeps
	// the server default /mnt/session/uploads/<file_id>.
	MountPath string
}

// AddSessionResource mounts one project file into a session (BMA extension).
// The returned FileID is the session instance created for the mount.
func (c *Client) AddSessionResource(ctx context.Context, sessionID string, options SessionResourceOptions) (*FileResource, error) {
	body := FileResourceParams{Type: FileResourceParamsTypeFile, FileId: options.FileID}
	if options.MountPath != "" {
		body.MountPath = &options.MountPath
	}
	resp, err := c.generated.AddSessionResourceWithResponse(ctx, sessionID, &AddSessionResourceParams{}, body)
	if err != nil {
		return nil, fmt.Errorf("facadeext: add session resource: %w", err)
	}
	if err := CheckResponse(resp.HTTPResponse, resp.Body); err != nil {
		return nil, err
	}
	if resp.JSON200 == nil {
		return nil, errors.New("facadeext: add session resource response has no body")
	}
	return resp.JSON200, nil
}

// ListSessionResources returns the session's mounted file resources (BMA
// extension).
func (c *Client) ListSessionResources(ctx context.Context, sessionID string) (*FileResourcePage, error) {
	resp, err := c.generated.ListSessionResourcesWithResponse(ctx, sessionID, &ListSessionResourcesParams{})
	if err != nil {
		return nil, fmt.Errorf("facadeext: list session resources: %w", err)
	}
	if err := CheckResponse(resp.HTTPResponse, resp.Body); err != nil {
		return nil, err
	}
	if resp.JSON200 == nil {
		return nil, errors.New("facadeext: list session resources response has no body")
	}
	return resp.JSON200, nil
}

// DeleteSessionResource unmounts one file resource from a session (BMA
// extension). The project file itself is kept.
func (c *Client) DeleteSessionResource(ctx context.Context, sessionID, resourceID string) (*DeletedSessionResource, error) {
	resp, err := c.generated.DeleteSessionResourceWithResponse(
		ctx, sessionID, resourceID, &DeleteSessionResourceParams{})
	if err != nil {
		return nil, fmt.Errorf("facadeext: delete session resource: %w", err)
	}
	if err := CheckResponse(resp.HTTPResponse, resp.Body); err != nil {
		return nil, err
	}
	if resp.JSON200 == nil {
		return nil, errors.New("facadeext: delete session resource response has no body")
	}
	return resp.JSON200, nil
}

func filenameFromDisposition(value string) string {
	if value == "" {
		return ""
	}
	if _, params, err := mime.ParseMediaType(value); err == nil {
		return params["filename"]
	}
	return ""
}

// APIError is an Anthropic-style error returned by a facade route.
type APIError struct {
	StatusCode int
	Type       string
	Code       string
	Message    string
}

func (e *APIError) Error() string {
	if e.Code != "" {
		return fmt.Sprintf("facadeext: HTTP %d %s (%s): %s", e.StatusCode, e.Type, e.Code, e.Message)
	}
	return fmt.Sprintf("facadeext: HTTP %d %s: %s", e.StatusCode, e.Type, e.Message)
}

// CheckResponse returns nil for 2xx responses and an *APIError otherwise.
func CheckResponse(resp *http.Response, body []byte) error {
	if resp.StatusCode >= 200 && resp.StatusCode < 300 {
		return nil
	}
	apiErr := &APIError{StatusCode: resp.StatusCode, Type: "api_error"}
	if len(body) > maxErrorBody {
		body = body[:maxErrorBody]
	}
	var envelope ErrorEnvelope
	if json.Unmarshal(body, &envelope) == nil {
		if envelope.Error.Type != "" {
			apiErr.Type = envelope.Error.Type
		}
		apiErr.Message = envelope.Error.Message
		if envelope.Error.Code != nil {
			apiErr.Code = *envelope.Error.Code
		}
	}
	if apiErr.Message == "" {
		apiErr.Message = http.StatusText(resp.StatusCode)
	}
	return apiErr
}

// EventBMASequence returns the BMA extension bma_sequence of a raw facade
// session event, or false for preview and synthetic events. Send it as
// Last-Event-ID to resume GET /v1/sessions/{id}/events/stream.
func EventBMASequence(event json.RawMessage) (BMASequence, bool) {
	var probe struct {
		Sequence *BMASequence `json:"bma_sequence"`
	}
	if json.Unmarshal(event, &probe) != nil || probe.Sequence == nil || *probe.Sequence <= 0 {
		return 0, false
	}
	return *probe.Sequence, true
}
