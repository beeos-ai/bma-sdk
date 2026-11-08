package bmasdk

import (
	"encoding/json"
	"errors"

	"github.com/anthropics/anthropic-sdk-go/v2"
)

// Error is the API error type of every call: the official *anthropic.Error
// (StatusCode, RequestID, Type(), Message, RawJSON()).
type Error = anthropic.Error

// ErrorCode returns BMA's reason for an API error (error.code of the
// Anthropic error envelope, e.g. "idempotency_key_reused"), or "" when err
// is not an API error or has no code. Branch on it rather than on Message.
func ErrorCode(err error) string {
	var apiErr *anthropic.Error
	if !errors.As(err, &apiErr) {
		return ""
	}
	var body struct {
		Error struct {
			Code string `json:"code"`
		} `json:"error"`
	}
	if json.Unmarshal([]byte(apiErr.RawJSON()), &body) != nil {
		return ""
	}
	return body.Error.Code
}
