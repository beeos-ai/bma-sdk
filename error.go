package bma

import (
	"encoding/json"
	"fmt"
	"net/http"
)

// Error is a non-2xx response, or an error frame of an event stream
// (StatusCode 0). Match it with errors.As and switch on Code.
type Error struct {
	StatusCode int
	// Code is the contract's stable error code (ErrorCode constants); the
	// facade extensions also use their own codes such as file_already_exists.
	Code    ErrorCode
	Message string
	// Type is the Anthropic-style error.type of facade extension errors.
	Type string
	// CurrentDigest is set for file_content_conflict and expected_digest_required.
	CurrentDigest string
	// Issues are field-level problems of agent config validation errors.
	Issues []AgentConfigErrorIssue
	Header http.Header
	// Body is the raw response body (at most 1 MiB).
	Body []byte
}

func (e *Error) Error() string {
	code := string(e.Code)
	if code == "" {
		code = e.Type
	}
	if code == "" {
		code = "unknown"
	}
	if e.StatusCode == 0 {
		return fmt.Sprintf("bma: event stream error %s: %s", code, e.Message)
	}
	return fmt.Sprintf("bma: %d %s: %s", e.StatusCode, code, e.Message)
}

// Retryable reports whether the same request may succeed later.
func (e *Error) Retryable() bool {
	return e.StatusCode == http.StatusRequestTimeout || e.StatusCode == http.StatusTooManyRequests ||
		e.StatusCode >= 500 || e.Code == ErrorCodeServiceUnavailable || e.Code == ErrorCodeRateLimited
}

// NewError decodes an error body of the native API ({error, code}) or of the
// facade extensions ({type: "error", error: {type, message, code}}).
func NewError(status int, body []byte, header http.Header) *Error {
	e := &Error{StatusCode: status, Header: header, Body: body}
	var wire struct {
		Error         json.RawMessage         `json:"error"`
		Code          string                  `json:"code"`
		CurrentDigest string                  `json:"current_digest"`
		Issues        []AgentConfigErrorIssue `json:"issues"`
	}
	if json.Unmarshal(body, &wire) == nil {
		var nested struct {
			Type    string `json:"type"`
			Message string `json:"message"`
			Code    string `json:"code"`
		}
		if json.Unmarshal(wire.Error, &nested) == nil && (nested.Type != "" || nested.Message != "") {
			e.Type, e.Message, e.Code = nested.Type, nested.Message, ErrorCode(nested.Code)
		} else {
			_ = json.Unmarshal(wire.Error, &e.Message)
			e.Code = ErrorCode(wire.Code)
		}
		e.CurrentDigest, e.Issues = wire.CurrentDigest, wire.Issues
	}
	if e.Message == "" && status != 0 {
		e.Message = http.StatusText(status)
	}
	return e
}

func newAPIError(status int, body []byte, header http.Header) error { return NewError(status, body, header) }

func newStreamError(body []byte) error { return NewError(0, body, nil) }
