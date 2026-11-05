// Package option configures a bma.Client, a facade.Client, or one request.
// Every option works in both places: passed to NewClient it sets a default,
// passed to a method it applies to that call only.
//
//	client := bma.NewClient(option.WithToken(token), option.WithBaseURL(base),
//		option.WithOrg(org), option.WithProject(project))
//	client.Agents.Get(ctx, agentID, option.WithProject(otherProject))
package option

import (
	"fmt"
	"net/http"
	"strings"
	"time"

	"github.com/beeos-ai/bma-sdk/internal/requestconfig"
)

// RequestOption changes a client default or one request.
type RequestOption = requestconfig.RequestOption

// WithBaseURL sets the API root: for the native API including /api/v1 (for
// example https://host/api/v1); for the facade extensions the origin without /v1.
func WithBaseURL(base string) RequestOption {
	return func(c *requestconfig.Config) error {
		c.BaseURL = strings.TrimRight(strings.TrimSpace(base), "/")
		return nil
	}
}

// WithToken sets the BMA personal or organization token (Authorization:
// Bearer). The client default is read from BMA_TOKEN.
func WithToken(token string) RequestOption {
	return func(c *requestconfig.Config) error {
		c.Token = strings.TrimSpace(token)
		return nil
	}
}

// WithAPIKey sets the organization API key sent as x-api-key (facade extensions).
func WithAPIKey(key string) RequestOption {
	return func(c *requestconfig.Config) error {
		c.APIKey = strings.TrimSpace(key)
		return nil
	}
}

// WithOrg sets the organization (org_...) of org- and project-scoped methods.
// The client default is read from BMA_ORG_ID.
func WithOrg(orgID string) RequestOption {
	return func(c *requestconfig.Config) error {
		c.Org = orgID
		return nil
	}
}

// WithProject sets the project (prj_...) of project-scoped methods (the
// x-bma-project-id header on facade extensions). The client default is read
// from BMA_PROJECT_ID.
func WithProject(projectID string) RequestOption {
	return func(c *requestconfig.Config) error {
		c.Project = projectID
		return nil
	}
}

// WithHTTPClient sets the HTTP client; the default is http.DefaultClient.
func WithHTTPClient(client *http.Client) RequestOption {
	return func(c *requestconfig.Config) error {
		c.HTTPClient = client
		return nil
	}
}

// WithMaxRetries sets the retries after the first attempt (default 2).
func WithMaxRetries(retries int) RequestOption {
	return func(c *requestconfig.Config) error {
		if retries < 0 {
			return fmt.Errorf("bma: max retries must be >= 0")
		}
		c.MaxRetries = retries
		return nil
	}
}

// WithRequestTimeout sets the per-attempt timeout (default 60s); 0 disables
// it. It covers a request until its response is read; for uploads (binary
// and multipart bodies) it starts once the body is sent, and event streams
// and downloads are bounded only until the response headers arrive.
func WithRequestTimeout(timeout time.Duration) RequestOption {
	return func(c *requestconfig.Config) error {
		if timeout < 0 {
			return fmt.Errorf("bma: request timeout must be >= 0")
		}
		c.Timeout = timeout
		return nil
	}
}

// WithHeader sets a request header.
func WithHeader(name, value string) RequestOption {
	return func(c *requestconfig.Config) error {
		c.Headers.Set(name, value)
		return nil
	}
}

// WithIdempotencyKey sets the Idempotency-Key of an operation that declares
// it. Without it the SDK generates one and reuses it across the retries of
// the call. Operations without the header reject the option.
func WithIdempotencyKey(key string) RequestOption {
	return func(c *requestconfig.Config) error {
		c.IdempotencyKey = key
		return nil
	}
}

// WithJSONSet sets a top-level member of the JSON request body, after the
// params are encoded; a nil value sends JSON null (params omit nil fields,
// so this is how a merge update clears a stored value). Same role as
// option.WithJSONSet of the Stainless Go SDKs, for top-level keys.
func WithJSONSet(key string, value any) RequestOption {
	return func(c *requestconfig.Config) error {
		if c.JSONSet == nil {
			c.JSONSet = map[string]any{}
		}
		c.JSONSet[key] = value
		return nil
	}
}
