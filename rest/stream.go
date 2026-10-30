package bmarest

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io"
	"strings"
)

// EventStream reads the agent server-sent event stream.
type EventStream struct {
	body   io.ReadCloser
	reader *bufio.Reader
}

func newEventStream(body io.ReadCloser) *EventStream {
	return &EventStream{body: body, reader: bufio.NewReader(body)}
}

// Close releases the stream response body.
func (s *EventStream) Close() error {
	if s == nil || s.body == nil {
		return nil
	}
	return s.body.Close()
}

// StreamFrame is one SSE data frame. Exactly one of AgentEvent,
// ToolCallUpdate, ModelOutputDelta, or Error is set for frames the SDK knows;
// Data always carries the raw JSON payload for forward compatibility.
type StreamFrame struct {
	Event            string
	ID               string
	Data             json.RawMessage
	AgentEvent       *AgentEvent
	ToolCallUpdate   *ToolCallUpdate
	ModelOutputDelta *ModelOutputDelta
	Error            *APIError
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

	switch name {
	case "agent_input", "model_output", "tool_result", "context_checkpoint":
		var event AgentEvent
		if err := json.Unmarshal(raw, &event); err != nil {
			return StreamFrame{}, fmt.Errorf("bmarest: decode %s frame: %w", name, err)
		}
		frame.AgentEvent = &event
	case "tool_call_update":
		var update ToolCallUpdate
		if err := json.Unmarshal(raw, &update); err != nil {
			return StreamFrame{}, fmt.Errorf("bmarest: decode tool_call_update frame: %w", err)
		}
		frame.ToolCallUpdate = &update
	case "model_output_delta":
		var delta ModelOutputDelta
		if err := json.Unmarshal(raw, &delta); err != nil {
			return StreamFrame{}, fmt.Errorf("bmarest: decode model_output_delta frame: %w", err)
		}
		frame.ModelOutputDelta = &delta
	case "error":
		var body struct {
			Error         string    `json:"error"`
			Code          ErrorCode `json:"code"`
			CurrentDigest string    `json:"current_digest"`
		}
		if err := json.Unmarshal(raw, &body); err != nil {
			return StreamFrame{}, fmt.Errorf("bmarest: decode error frame: %w", err)
		}
		frame.Error = &APIError{
			Code:          body.Code,
			Message:       body.Error,
			CurrentDigest: body.CurrentDigest,
		}
	}
	return frame, nil
}
