// Package requestconfig holds the settings that client options and
// per-request options change. Users set them through package option.
package requestconfig

import (
	"net/http"
	"time"
)

// Config is the client's defaults, copied and changed per request.
type Config struct {
	BaseURL        string
	Token          string // Authorization: Bearer (native API)
	APIKey         string // x-api-key (facade extensions)
	Org            string
	Project        string
	HTTPClient     *http.Client
	MaxRetries     int
	Timeout        time.Duration
	Headers        http.Header
	IdempotencyKey string
	// JSONSet overrides top-level members of a JSON request body.
	JSONSet map[string]any
}

// RequestOption changes a Config; an error fails the request.
type RequestOption func(*Config) error

// Apply returns a copy of base with opts applied.
func Apply(base Config, opts []RequestOption) (Config, error) {
	cfg := base
	cfg.Headers = base.Headers.Clone()
	if base.JSONSet != nil {
		cfg.JSONSet = make(map[string]any, len(base.JSONSet))
		for k, v := range base.JSONSet {
			cfg.JSONSet[k] = v
		}
	}
	if cfg.Headers == nil {
		cfg.Headers = http.Header{}
	}
	for _, opt := range opts {
		if err := opt(&cfg); err != nil {
			return cfg, err
		}
	}
	return cfg, nil
}
