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
	if sessionID == "" {
		return ssestream.NewStream[anthropic.BetaManagedAgentsStreamSessionEventsUnion](nil, errors.New("missing required session_id parameter"))
	}
	opts = slices.Concat(r.options, streamHeaders(params), opts)
	path := "v1/sessions/" + url.PathEscape(sessionID) + "/events/stream"
	// connect opens a connection that resumes after lastSequence; -1 opens
	// at the server's default position (new events only).
	connect := func(lastSequence int64) (*http.Response, error) {
		attempt := opts
		if lastSequence >= 0 {
			attempt = append(slices.Clone(opts), option.WithHeader("Last-Event-ID", strconv.FormatInt(lastSequence, 10)))
		}
		var res *http.Response
		err := execute(ctx, http.MethodGet, path, params, &res, attempt...)
		return res, err
	}
	res, err := connect(-1)
	if err != nil {
		return ssestream.NewStream[anthropic.BetaManagedAgentsStreamSessionEventsUnion](nil, err)
	}
	return ssestream.NewStream[anthropic.BetaManagedAgentsStreamSessionEventsUnion](&resumingDecoder{
		ctx:     ctx,
		connect: connect,
		current: ssestream.NewDecoder(res),
		seen:    map[string]struct{}{},
	}, nil)
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
		res, err := d.connect(d.sequence - 1)
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
