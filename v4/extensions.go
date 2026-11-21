package bmasdk

import (
	"encoding/json"
	"errors"
	"fmt"

	"github.com/anthropics/anthropic-sdk-go/v2"
	"github.com/anthropics/anthropic-sdk-go/v2/option"
)

// BMA extension fields on the shared (Claude Managed Agents) objects: top-level
// bma_* properties (inventory N1). The official types keep them in their raw
// JSON; the functions below decode them into typed values, and the With...
// options write them into a request of the official method.
//
// bma_model_override is declared by the contract (x-bma-extension-fields) and
// uses its generated types; the other fields follow the facade's current JSON
// until the contract lists them.

// Harness is bma_harness: a non-default brain for an agent or a session.
type Harness struct {
	Kind  string `json:"kind"`
	Agent string `json:"agent,omitempty"`
	// Placement is where the environment runs the brain (sessions only).
	Placement string `json:"placement,omitempty"`
}

// EnvironmentDesktop is bma_desktop of an environment.
type EnvironmentDesktop struct {
	Wallpaper *EnvironmentWallpaper `json:"wallpaper"`
}

// EnvironmentWallpaper is the default wallpaper of new desktops: a file of
// the Files API.
type EnvironmentWallpaper struct {
	FileID string `json:"file_id"`
}

// EnvironmentMachine is bma_machine: present on the environment BMA projects
// from a machine.
type EnvironmentMachine struct {
	MachineID  string                  `json:"machine_id"`
	SourceKind string                  `json:"source_kind"`
	Lease      EnvironmentMachineLease `json:"lease"`
}

// EnvironmentMachineLease reports who runs on a persistent machine: sessions
// borrowing it run their turns one at a time and the rest wait.
type EnvironmentMachineLease struct {
	SessionID      *string `json:"session_id"`
	QueuedSessions int     `json:"queued_sessions"`
}

// SessionExt is the BMA extension fields of a session.
type SessionExt struct {
	// ModelOverride is the active model override (no key) or nil.
	ModelOverride *AgentModelOverride `json:"bma_model_override"`
	Harness       *Harness            `json:"bma_harness"`
}

// AgentExt is the BMA extension fields of an agent.
type AgentExt struct {
	Harness *Harness `json:"bma_harness"`
}

// EnvironmentExt is the BMA extension fields of an environment.
type EnvironmentExt struct {
	Desktop *EnvironmentDesktop `json:"bma_desktop"`
	Machine *EnvironmentMachine `json:"bma_machine"`
}

// EventExt is the BMA extension fields of a session event, from a list or a
// stream.
type EventExt struct {
	// Sequence orders the events of a session; Last-Event-ID and the history
	// cursor use it (the SSE id stays the opaque event id).
	Sequence int64 `json:"bma_sequence"`
	// InputID is the BMA input of a user.message.
	InputID string `json:"bma_input_id"`
	// ErrorCode is BMA's reason on a session.error.
	ErrorCode string `json:"bma_error_code"`
}

type rawJSON interface{ RawJSON() string }

func decodeExt[T any](v rawJSON) (T, error) {
	var ext T
	raw := v.RawJSON()
	if raw == "" {
		return ext, errors.New("bmasdk: object has no raw JSON (not decoded from a response)")
	}
	if err := json.Unmarshal([]byte(raw), &ext); err != nil {
		return ext, fmt.Errorf("bmasdk: decode extension fields: %w", err)
	}
	return ext, nil
}

// SessionExtensions returns the BMA fields of a session returned by
// client.Beta.Sessions.
func SessionExtensions(s *anthropic.BetaManagedAgentsSession) (SessionExt, error) {
	return decodeExt[SessionExt](s)
}

// AgentExtensions returns the BMA fields of an agent returned by
// client.Beta.Agents.
func AgentExtensions(a *anthropic.BetaManagedAgentsAgent) (AgentExt, error) {
	return decodeExt[AgentExt](a)
}

// EnvironmentExtensions returns the BMA fields of an environment returned by
// client.Beta.Environments.
func EnvironmentExtensions(e *anthropic.BetaEnvironment) (EnvironmentExt, error) {
	return decodeExt[EnvironmentExt](e)
}

// EventExtensions returns the BMA fields of a session event: an item of
// client.Beta.Sessions.Events.List or a frame of StreamEvents.
func EventExtensions[E anthropic.BetaManagedAgentsSessionEventUnion | anthropic.BetaManagedAgentsStreamSessionEventsUnion](event E) (EventExt, error) {
	switch e := any(event).(type) {
	case anthropic.BetaManagedAgentsSessionEventUnion:
		return decodeExt[EventExt](e)
	case anthropic.BetaManagedAgentsStreamSessionEventsUnion:
		return decodeExt[EventExt](e)
	}
	panic("unreachable")
}

// WithSessionModelOverride sets bma_model_override on Sessions.New (the
// override lasts for the session) or Sessions.Update (replaces the active
// override). APIKey is write-only.
func WithSessionModelOverride(override AgentModelOverrideInput) option.RequestOption {
	return option.WithJSONSet("bma_model_override", override)
}

// WithSessionModelOverridePatch changes fields of the active override on
// Sessions.Update.
func WithSessionModelOverridePatch(patch AgentModelOverridePatch) option.RequestOption {
	return option.WithJSONSet("bma_model_override", patch)
}

// WithSessionModelOverrideRevoke revokes the active override on
// Sessions.Update (bma_model_override: null).
func WithSessionModelOverrideRevoke() option.RequestOption {
	return option.WithJSONSet("bma_model_override", nil)
}

// WithHarness sets bma_harness on Agents.New/Update or Sessions.New.
func WithHarness(h Harness) option.RequestOption {
	return option.WithJSONSet("bma_harness", h)
}

// WithEnvironmentDesktop sets bma_desktop on Environments.New/Update.
func WithEnvironmentDesktop(d EnvironmentDesktop) option.RequestOption {
	return option.WithJSONSet("bma_desktop", d)
}
