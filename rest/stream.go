package rest

import (
	"bufio"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"mime"
	"net/http"
	"strconv"
	"strings"
)

// EventStream reads the agent server-sent event stream.
type EventStream struct {
	body   io.ReadCloser
	reader *bufio.Reader
}

// StreamFrame is one SSE data frame. Exactly one of AgentEvent,
// ToolCallUpdate, ModelOutputDelta, or Error is set for frames the contract
// knows; Data always carries the raw JSON payload for forward compatibility.
type StreamFrame struct {
	Event    string
	ID       string
	Data     json.RawMessage
	Sequence int64

	AgentEvent       *AgentEvent
	ToolCallUpdate   *ToolCallUpdate
	ModelOutputDelta *ModelOutputDelta
	Error            *APIError
}

// OpenEventStream opens the agent's server-sent event stream. The caller must
// close the returned stream.
func (c *Client) OpenEventStream(ctx context.Context, orgID, projectID, agentID string, params *StreamEventsParams) (*EventStream, error) {
	req, err := NewStreamEventsRequest(c.server, orgID, projectID, agentID, params)
	if err != nil {
		return nil, fmt.Errorf("rest: build event stream request: %w", err)
	}
	if err := c.authenticate(ctx, req); err != nil {
		return nil, err
	}
	req.Header.Set("Accept", "text/event-stream")

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("rest: open event stream: %w", err)
	}
	if resp.StatusCode != http.StatusOK {
		return nil, newAPIErrorFromResponse(resp)
	}
	media, _, err := mime.ParseMediaType(resp.Header.Get("Content-Type"))
	if err != nil || media != "text/event-stream" {
		resp.Body.Close()
		return nil, fmt.Errorf("rest: event stream content type = %q", resp.Header.Get("Content-Type"))
	}
	return &EventStream{body: resp.Body, reader: bufio.NewReader(resp.Body)}, nil
}

// Close releases the stream response body.
func (s *EventStream) Close() error {
	if s == nil || s.body == nil {
		return nil
	}
	return s.body.Close()
}

// Next returns the next data frame. Heartbeats and other SSE comments are
// skipped. It returns io.EOF when the server closes the stream.
func (s *EventStream) Next() (StreamFrame, error) {
	var (
		eventName string
		id        string
		data      []string
	)
	for {
		line, err := s.reader.ReadString('\n')
		if err != nil {
			if err == io.EOF {
				if len(data) > 0 {
					return s.dispatch(eventName, id, data)
				}
				return StreamFrame{}, io.EOF
			}
			return StreamFrame{}, err
		}
		line = strings.TrimSuffix(line, "\n")
		line = strings.TrimSuffix(line, "\r")

		if line == "" {
			if len(data) == 0 {
				eventName, id = "", ""
				continue
			}
			return s.dispatch(eventName, id, data)
		}
		if strings.HasPrefix(line, ":") {
			continue
		}
		field, value, found := strings.Cut(line, ":")
		if !found {
			continue
		}
		value = strings.TrimPrefix(value, " ")
		switch field {
		case "event":
			eventName = value
		case "id":
			id = value
		case "data":
			data = append(data, value)
		}
	}
}

func (s *EventStream) dispatch(eventName, id string, data []string) (StreamFrame, error) {
	raw := []byte(strings.Join(data, "\n"))
	name := eventName
	if name == "" {
		name = "message"
	}
	frame := StreamFrame{Event: name, ID: id, Data: raw}
	if id != "" {
		sequence, err := strconv.ParseInt(id, 10, 64)
		if err != nil {
			return StreamFrame{}, fmt.Errorf("rest: decode event id %q: %w", id, err)
		}
		frame.Sequence = sequence
	}

	switch name {
	case "agent_input", "model_output", "tool_result", "context_checkpoint":
		var event AgentEvent
		if err := json.Unmarshal(raw, &event); err != nil {
			return StreamFrame{}, fmt.Errorf("rest: decode %s frame: %w", name, err)
		}
		frame.AgentEvent = &event
	case "tool_call_update":
		var update ToolCallUpdate
		if err := json.Unmarshal(raw, &update); err != nil {
			return StreamFrame{}, fmt.Errorf("rest: decode tool_call_update frame: %w", err)
		}
		frame.ToolCallUpdate = &update
	case "model_output_delta":
		var delta ModelOutputDelta
		if err := json.Unmarshal(raw, &delta); err != nil {
			return StreamFrame{}, fmt.Errorf("rest: decode model_output_delta frame: %w", err)
		}
		frame.ModelOutputDelta = &delta
	case "error":
		var body Error
		if err := json.Unmarshal(raw, &body); err != nil {
			return StreamFrame{}, fmt.Errorf("rest: decode error frame: %w", err)
		}
		apiErr := &APIError{Code: body.Code, Message: body.Error}
		if body.CurrentDigest != nil {
			apiErr.CurrentDigest = *body.CurrentDigest
		}
		if body.Issues != nil {
			apiErr.Issues = *body.Issues
		}
		frame.Error = apiErr
	}
	return frame, nil
}
