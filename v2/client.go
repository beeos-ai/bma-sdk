// Package bmasdk is the Go client for BMA (bma-sdk 2.0, ADR 0025).
//
// The resources BMA shares with Claude Managed Agents are the official
// anthropic-sdk-go services, unchanged: client.Beta.Agents, Sessions,
// Sessions.Events, Environments, Files, Skills, Vaults, MemoryStores... take
// and return the official types, so code moves between the two SDKs as is.
// The BMA extensions (machines, machine pools, desktop and terminal sessions
// and their tickets, organization projects) are generated from the BMA
// extension contract and live next to them under client.Beta. Extension
// fields on the shared objects (bma_*) are read with SessionExtensions,
// EnvironmentExtensions, AgentExtensions and EventExtensions and written with
// the typed With... request options of this package.
//
//	client := bmasdk.NewClient() // BMA_API_KEY, BMA_BASE_URL, BMA_PROJECT_ID
//	client := bmasdk.NewClient(option.WithAPIKey(key), option.WithBaseURL(origin), bmasdk.WithProject(project))
//	session, err := client.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{...})
//	machines := client.Beta.Machines.ListAutoPaging(ctx, bmasdk.MachineListParams{})
//
// Errors are *anthropic.Error (errors.As); ErrorCode returns BMA's reason.
// Only use this package on a server: the API key is a tenant credential
// (ADR 0025 B1). End-user clients get single-use tickets instead.
package bmasdk

import (
	"os"
	"slices"
	"strings"

	"github.com/anthropics/anthropic-sdk-go/v2"
	"github.com/anthropics/anthropic-sdk-go/v2/option"
)

const (
	// DefaultBaseURL is the hosted BMA origin (the paths carry /v1).
	DefaultBaseURL = "https://api.bma.beeos.ai"
	// SDKVersion is the version of this module, sent as X-BMA-SDK.
	SDKVersion = "2.2.0"
)

// Client is the BMA client: the official Anthropic client with the BMA
// defaults, whose Beta service adds the BMA extensions.
type Client struct {
	anthropic.Client
	Beta BetaService
}

// NewClient returns a client. It never reads the ANTHROPIC_* environment:
// the API key defaults to BMA_API_KEY, the base URL (the deployment origin)
// to BMA_BASE_URL and else DefaultBaseURL, and the project scope header
// bma-workspace-id to BMA_PROJECT_ID. Options are the official option
// package's (option.WithAPIKey, option.WithBaseURL, option.WithHeader,
// option.WithMaxRetries, option.WithMiddleware, ...) plus WithProject and
// WithIdempotencyKey.
func NewClient(opts ...option.RequestOption) *Client {
	base := strings.TrimSpace(os.Getenv("BMA_BASE_URL"))
	if base == "" {
		base = DefaultBaseURL
	}
	defaults := []option.RequestOption{
		option.WithoutEnvironmentDefaults(),
		option.WithBaseURL(base),
		option.WithHeader("X-BMA-SDK", "bma-sdk-go/"+SDKVersion),
	}
	if key := strings.TrimSpace(os.Getenv("BMA_API_KEY")); key != "" {
		defaults = append(defaults, option.WithAPIKey(key))
	}
	if project := strings.TrimSpace(os.Getenv("BMA_PROJECT_ID")); project != "" {
		defaults = append(defaults, WithProject(project))
	}
	inner := anthropic.NewClient(slices.Concat(defaults, opts)...)
	return &Client{Client: inner, Beta: newBetaService(inner.Options)}
}

// BetaService is client.Beta: the official Beta resources plus the BMA
// extensions (ADR 0025, review D-3: extensions sit next to the official
// resources under beta).
type BetaService struct {
	anthropic.BetaService
	// Sessions is the official session service whose Events.StreamEvents
	// resumes after a dropped connection.
	Sessions SessionService
	// Organization is the official organization service plus Projects.
	Organization OrganizationService
	extensionServices
}

func newBetaService(opts []option.RequestOption) BetaService {
	official := anthropic.NewBetaService(opts...)
	return BetaService{
		BetaService:       official,
		Sessions:          newSessionService(official.Sessions, opts),
		Organization:      OrganizationService{BetaOrganizationService: official.Organization, Projects: newOrganizationProjectService(opts)},
		extensionServices: newExtensionServices(opts),
	}
}

// OrganizationService is client.Beta.Organization.
type OrganizationService struct {
	anthropic.BetaOrganizationService
	Projects OrganizationProjectService
}

// WithProject sets the scope header bma-workspace-id (ADR 0032), required when
// the API key can see more than one project.
func WithProject(projectID string) option.RequestOption {
	return option.WithHeader("bma-workspace-id", projectID)
}

// WithIdempotencyKey sets the Idempotency-Key header of one call. The header
// is set once per call, so the automatic retries resend the same key and the
// server replays the first result. Extension creates send a random key
// unless this option is given.
func WithIdempotencyKey(key string) option.RequestOption {
	return option.WithHeader("Idempotency-Key", key)
}

// Ptr returns a pointer to v, for the optional fields of the extension types
// (the official types use anthropic.String, anthropic.Int, ... instead).
func Ptr[T any](v T) *T { return &v }
