package bmasdk

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"net/url"
	"slices"
	"strconv"
	"strings"
	"time"

	"github.com/anthropics/anthropic-sdk-go/v2"
	"github.com/anthropics/anthropic-sdk-go/v2/option"
	"github.com/anthropics/anthropic-sdk-go/v2/packages/param"
	"github.com/anthropics/anthropic-sdk-go/v2/packages/ssestream"
)

// SessionService is client.Beta.Sessions: the official service (New, Get,
// Update, List, ListAutoPaging, Delete, Archive, Resources, Threads) whose
// Events resume a dropped stream.
type SessionService struct {
	anthropic.BetaSessionService
	Events SessionEventService
}

func newSessionService(official anthropic.BetaSessionService, opts []option.RequestOption) SessionService {
	return SessionService{
		BetaSessionService: official,
		Events:             SessionEventService{BetaSessionEventService: official.Events, options: opts},
	}
}

// SessionEventService is client.Beta.Sessions.Events: the official List,
// ListAutoPaging, Send and NewToolRunner, and a StreamEvents that resumes.
type SessionEventService struct {
	anthropic.BetaSessionEventService
	options []option.RequestOption
}

// Stream resumption: a dropped stream reconnects with Last-Event-ID (see
// StreamEvents), up to maxReconnects attempts in a row with exponential
// backoff from reconnectBackoff to maxReconnectBackoff.
var (
	maxReconnects       = 5
	reconnectBackoff    = 500 * time.Millisecond
	maxReconnectBackoff = 8 * time.Second
)

// StreamEvents has the signature and the frames of the official method. When
// the connection drops or the server ends the stream, it reconnects with
// Last-Event-ID set to the bma_sequence before the one of the last frame (one
// durable BMA event projects into several frames that share its sequence, and
// the server resumes after a whole sequence) and skips the frames it already
// returned, so no event is lost or repeated. It stops when ctx ends, after
// maxReconnects failed attempts in a row, or on an API error other than 408,
// 409, 429 and 5xx (which the official client retries first). The official,
// non-resuming stream is Events.BetaSessionEventService.StreamEvents.
func (r *SessionEventService) StreamEvents(ctx context.Context, sessionID string, params anthropic.BetaSessionEventStreamParams, opts ...option.RequestOption) *ssestream.Stream[anthropic.BetaManagedAgentsStreamSessionEventsUnion] {
	return r.stream(ctx, sessionID, params, liveOnly, opts)
}

// liveOnly opens a stream at the server's default position: new events only.
const liveOnly int64 = -1

// stream opens a resuming stream whose first connection sends Last-Event-ID
// after (liveOnly sends none). A reconnect before any durable frame arrives
// reuses after, so the anchor survives a drop.
func (r *SessionEventService) stream(ctx context.Context, sessionID string, params anthropic.BetaSessionEventStreamParams, after int64, opts []option.RequestOption) *ssestream.Stream[anthropic.BetaManagedAgentsStreamSessionEventsUnion] {
	if sessionID == "" {
		return ssestream.NewStream[anthropic.BetaManagedAgentsStreamSessionEventsUnion](nil, errors.New("missing required session_id parameter"))
	}
	opts = slices.Concat(r.options, streamHeaders(params), opts)
	path := "v1/sessions/" + url.PathEscape(sessionID) + "/events/stream"
	// connect opens a connection that resumes after lastSequence; liveOnly
	// opens at the server's default position (new events only).
	connect := func(lastSequence int64) (*http.Response, error) {
		attempt := opts
		if lastSequence >= 0 {
			attempt = append(slices.Clone(opts), option.WithHeader("Last-Event-ID", strconv.FormatInt(lastSequence, 10)))
		}
		var res *http.Response
		err := execute(ctx, http.MethodGet, path, params, &res, attempt...)
		return res, err
	}
	res, err := connect(after)
	if err != nil {
		return ssestream.NewStream[anthropic.BetaManagedAgentsStreamSessionEventsUnion](nil, err)
	}
	return ssestream.NewStream[anthropic.BetaManagedAgentsStreamSessionEventsUnion](&resumingDecoder{
		ctx:     ctx,
		connect: connect,
		current: ssestream.NewDecoder(res),
		after:   after,
		seen:    map[string]struct{}{},
	}, nil)
}

// SentStream is the result of SendAndStream.
type SentStream struct {
	// Sent is the send response.
	Sent *anthropic.BetaManagedAgentsSendSessionEvents
	// Stream starts at the cursor read before the send: its first frames are
	// the sent user.message and its turn, whatever an executor wrote before
	// the stream opened.
	Stream *ssestream.Stream[anthropic.BetaManagedAgentsStreamSessionEventsUnion]
	// Replayed is true when the server gave no bma_resume_cursor for a
	// user.message (no safe cursor is known, such as an idempotent replay whose
	// input is not admitted yet): Stream then starts at Last-Event-ID 0 and
	// replays the session from its first event, so it can carry events that
	// precede the send; pick this one's turn by EventExt.InputID.
	Replayed bool
}

// SendAndStream sends events (BetaSessionEventSendParams, user.message and
// so on) and opens the resuming stream at the cursor the send returned
// (bma_resume_cursor: the session's last sequence before the send), so a
// frame an executor wrote before the stream opened is not lost. The official
// pattern, a stream opened before the send, needs no cursor; this one is for
// a caller that sends first. Without a cursor for a user.message the stream
// starts at Last-Event-ID 0 (see SentStream.Replayed). A send that carries no
// user.message streams from the server's default position: new events only.
// A send error is returned with no stream; an error opening the stream comes
// back with Sent set, as the message was accepted.
func (r *SessionEventService) SendAndStream(ctx context.Context, sessionID string, send anthropic.BetaSessionEventSendParams, params anthropic.BetaSessionEventStreamParams, opts ...option.RequestOption) (*SentStream, error) {
	sent, err := r.Send(ctx, sessionID, send, opts...)
	if err != nil {
		return nil, err
	}
	after, replayed := resumeCursor(sent.RawJSON())
	stream := r.stream(ctx, sessionID, params, after, opts)
	result := &SentStream{Sent: sent, Stream: stream, Replayed: replayed}
	if err := stream.Err(); err != nil {
		return result, err
	}
	return result, nil
}

// resumeCursor is the Last-Event-ID for a stream opened after a send: the
// smallest bma_resume_cursor of the response's user.message events, 0 and
// replayed when one of them has none, liveOnly when the response has no
// user.message.
func resumeCursor(raw string) (after int64, replayed bool) {
	var response struct {
		Data []struct {
			Type   string `json:"type"`
			Cursor *int64 `json:"bma_resume_cursor"`
		} `json:"data"`
	}
	_ = json.Unmarshal([]byte(raw), &response)
	after = liveOnly
	for _, event := range response.Data {
		if event.Type != "user.message" {
			continue
		}
		if event.Cursor == nil {
			return 0, true
		}
		if after == liveOnly || *event.Cursor < after {
			after = *event.Cursor
		}
	}
	return after, false
}

// streamHeaders are the headers the official StreamEvents sends.
func streamHeaders(params anthropic.BetaSessionEventStreamParams) []option.RequestOption {
	betas := []string{"managed-agents-2026-04-01"}
	for _, b := range params.Betas {
		betas = append(betas, string(b))
	}
	opts := []option.RequestOption{option.WithHeader("anthropic-beta", strings.Join(betas, ","))}
	if !param.IsOmitted(params.WorkspaceID) {
		opts = append(opts, option.WithHeader("anthropic-workspace-id", params.WorkspaceID.Value))
	}
	return opts
}

// resumingDecoder is an ssestream.Decoder over successive connections.
type resumingDecoder struct {
	ctx      context.Context
	connect  func(lastSequence int64) (*http.Response, error)
	current  ssestream.Decoder
	event    ssestream.Event
	sequence int64               // bma_sequence of the last durable frame
	after    int64               // Last-Event-ID a reconnect sends; liveOnly: none
	seen     map[string]struct{} // event ids returned at sequence
	failures int
	err      error
	closed   bool
}

func (d *resumingDecoder) Next() bool {
	for {
		if d.err != nil || d.closed {
			return false
		}
		if d.current != nil && d.current.Next() {
			event := d.current.Event()
			if seq, id := eventPosition(event.Data); seq > 0 {
				switch {
				case seq < d.sequence:
					continue // replayed after a reconnect
				case seq == d.sequence:
					if _, dup := d.seen[id]; dup {
						continue
					}
				default:
					d.sequence = seq
					d.after = seq - 1
					clear(d.seen)
				}
				d.seen[id] = struct{}{}
			} else if id != "" {
				// An announcement ahead of its durable copy (such as the
				// session.status_idle of requires_action): a replay of the
				// current sequence must not return it twice.
				if _, dup := d.seen[id]; dup {
					continue
				}
				d.seen[id] = struct{}{}
			}
			d.failures = 0
			d.event = event
			return true
		}
		cause := errors.New("stream ended")
		if d.current != nil {
			if err := d.current.Err(); err != nil {
				cause = err
			}
			_ = d.current.Close()
			d.current = nil
		}
		if !d.reconnect(cause) {
			return false
		}
	}
}

// reconnect waits and opens the next connection; false when it gave up.
func (d *resumingDecoder) reconnect(cause error) bool {
	for {
		if d.closed {
			return false
		}
		if err := d.ctx.Err(); err != nil {
			d.err = err
			return false
		}
		if d.failures >= maxReconnects {
			d.err = fmt.Errorf("bmasdk: event stream not resumed after %d attempts: %w", d.failures, cause)
			return false
		}
		delay := min(reconnectBackoff<<d.failures, maxReconnectBackoff)
		d.failures++
		select {
		case <-d.ctx.Done():
			d.err = d.ctx.Err()
			return false
		case <-time.After(delay):
		}
		// One durable BMA event (a bma_sequence) projects into several
		// Anthropic events, and the server resumes after the whole sequence:
		// resume after the previous one and skip the frames already returned.
		res, err := d.connect(d.after)
		if err == nil {
			d.current = ssestream.NewDecoder(res)
			return true
		}
		var apiErr *anthropic.Error
		if errors.As(err, &apiErr) && !retryableStatus(apiErr.StatusCode) {
			d.err = err
			return false
		}
		cause = err
	}
}

func retryableStatus(code int) bool {
	return code == http.StatusRequestTimeout || code == http.StatusConflict || code == http.StatusTooManyRequests || code >= 500
}

// eventPosition is the durable position of a frame: its bma_sequence (0 for
// an ephemeral frame such as a delta) and its event id.
func eventPosition(data []byte) (int64, string) {
	var frame struct {
		ID       string `json:"id"`
		Sequence int64  `json:"bma_sequence"`
	}
	if json.Unmarshal(data, &frame) != nil {
		return 0, ""
	}
	return frame.Sequence, frame.ID
}

func (d *resumingDecoder) Event() ssestream.Event { return d.event }

func (d *resumingDecoder) Err() error { return d.err }

func (d *resumingDecoder) Close() error {
	d.closed = true
	if d.current == nil {
		return nil
	}
	err := d.current.Close()
	d.current = nil
	return err
}
