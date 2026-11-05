// Package facade is the client of the BMA extensions to the Anthropic
// Managed Agents API. The standard routes (/v1/agents, /v1/sessions, events,
// /v1/files, /v1/memory_stores ...) are served by the official Anthropic SDK
// pointed at a BMA deployment; this package covers only what BMA adds:
//
//	ext := facade.NewClient(option.WithAPIKey(key), option.WithBaseURL(origin), option.WithProject(project))
//	page, err := ext.Sessions.Files.List(ctx, sessionID, facade.SessionFileListParams{})
//
// Errors are *bma.Error. Models are generated from
// contracts/bma/facade-extensions.openapi.yaml.
package facade

import (
	"encoding/json"
	"errors"
	"net/http"
	"strings"

	"github.com/beeos-ai/bma-sdk"
	"github.com/beeos-ai/bma-sdk/internal/apicore"
	"github.com/beeos-ai/bma-sdk/internal/requestconfig"
	"github.com/beeos-ai/bma-sdk/option"
)

// Client is the facade extensions client. Its fields are the resources.
type Client struct {
	resources
}

// NewClient returns a client. option.WithAPIKey (the organization API key,
// sent as x-api-key) and option.WithBaseURL (the facade origin, without /v1)
// are required; option.WithProject sets x-bma-project-id (required for
// multi-project keys).
func NewClient(opts ...option.RequestOption) *Client {
	defaults := requestconfig.Config{MaxRetries: apicore.DefaultMaxRetries, Timeout: apicore.DefaultTimeout}
	cfg, err := requestconfig.Apply(defaults, opts)
	core := &apicore.Client{
		Config:      cfg,
		NewError:    func(status int, body []byte, header http.Header) error { return bma.NewError(status, body, header) },
		StreamError: func(body []byte) error { return bma.NewError(0, body, nil) },
		UserAgent:   "bma-sdk-go/" + bma.SDKVersion,
		Validate: func(c *requestconfig.Config) error {
			if err != nil {
				return err
			}
			if c.APIKey == "" {
				return errors.New("bma facade: API key is required; use option.WithAPIKey")
			}
			if strings.HasSuffix(c.BaseURL, "/v1") {
				return errors.New("bma facade: base URL must be the origin without /v1")
			}
			return apicore.CheckBaseURL(c.BaseURL)
		},
	}
	return &Client{resources: newResources(core)}
}

// EventBMASequence returns the BMA extension bma_sequence of a facade
// session event (the raw JSON of an Anthropic SDK event). Send it as
// Last-Event-ID to resume GET /v1/sessions/{id}/events/stream.
func EventBMASequence(event json.RawMessage) (int64, bool) {
	var wire struct {
		Sequence *int64 `json:"bma_sequence"`
	}
	if json.Unmarshal(event, &wire) != nil || wire.Sequence == nil || *wire.Sequence <= 0 {
		return 0, false
	}
	return *wire.Sequence, true
}
