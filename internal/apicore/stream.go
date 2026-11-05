package apicore

import (
	"bufio"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"net/url"
	"strconv"
	"strings"
	"sync/atomic"
)

// Decoder turns one SSE frame into T; ok=false skips an event kind newer
// than this SDK.
type Decoder[T any] func(event, id string, sequence int64, data []byte) (value T, ok bool, err error)

// errStreamEnded is the reconnect cause when the server ends the response.
var errStreamEnded = errors.New("bma: event stream ended by the server")

// Stream is a typed server-sent event stream with EventSource reconnection:
// when the connection drops or the server ends the response (a rolling
// restart), or sends an `error` frame with code service_unavailable, the
// stream reconnects with Last-Event-ID set to the last durable frame. A frame
// not terminated before the end is discarded. Reconnects are bounded by the
// reconnect budget (MaxRetries unless set) counted in a row without
// receiving data; any other error frame ends the stream with the client's
// StreamError. The stream only ends with Close or an error.
//
//	for stream.Next() { ev := stream.Current() }
//	err := stream.Err()
type Stream[T any] struct {
	ctx      context.Context
	cancel   context.CancelFunc
	build    func(resume string) *Request
	decode   Decoder[T]
	onOpen   func()
	attempt  *attempt
	scanner  *bufio.Scanner
	client   *Client
	budget   int // reconnects in a row without data; <0: unlimited
	set      bool
	closed   atomic.Bool
	lastID   string
	failures int
	current  T
	err      error
	done     bool
}

// OpenStream returns a lazily connecting stream. build(resume) returns a
// fresh request; resume is the Last-Event-ID to send ("" on first connect).
// onOpen, if set, runs after every (re)connection. maxReconnects bounds the
// reconnects in a row that receive no data: <0 means unlimited, and
// UseMaxRetries takes the request's MaxRetries.
func OpenStream[T any](ctx context.Context, build func(resume string) *Request, decode Decoder[T], onOpen func(), maxReconnects int) *Stream[T] {
	ctx, cancel := context.WithCancel(ctx)
	s := &Stream[T]{ctx: ctx, cancel: cancel, build: build, decode: decode, onOpen: onOpen}
	if maxReconnects != UseMaxRetries {
		s.budget, s.set = maxReconnects, true
	}
	return s
}

// UseMaxRetries makes a stream's reconnect budget the request's MaxRetries.
const UseMaxRetries = -2

type reconnect struct{ err error }

func (r reconnect) Error() string { return r.err.Error() }

// Next reads the next frame, reconnecting as the contract requires.
func (s *Stream[T]) Next() bool {
	for !s.done {
		var err error
		if s.attempt == nil {
			err = s.connect()
		}
		if err == nil {
			var value T
			var ok bool
			value, ok, err = s.read()
			if err == nil && ok {
				s.current = value
				return true
			}
		}
		s.closeAttempt()
		if s.ctx.Err() != nil {
			return s.fail(s.ctx.Err())
		}
		var rc reconnect
		if !errors.As(err, &rc) {
			return s.fail(err)
		}
		if s.budget >= 0 && s.failures >= s.budget {
			return s.fail(rc.err)
		}
		if err := sleep(s.ctx, backoff(min(s.failures, 8))); err != nil {
			return s.fail(err)
		}
		s.failures++
	}
	return false
}

// connect opens one connection; a failure the stream may retry is a reconnect.
func (s *Stream[T]) connect() error {
	r := s.build(s.lastID)
	s.client = r.client
	if !s.set {
		s.budget, s.set = r.cfg.MaxRetries, true
	}
	r.cfg.MaxRetries = 0 // the stream owns the retry budget
	a, err := r.send(s.ctx, "text/event-stream")
	if err != nil {
		var retryable interface{ Retryable() bool }
		var transport *url.Error
		switch {
		case s.ctx.Err() != nil:
			return s.ctx.Err()
		case errors.As(err, &retryable):
			if retryable.Retryable() {
				return reconnect{err}
			}
			return err
		case errors.As(err, &transport), errors.Is(err, context.DeadlineExceeded):
			return reconnect{err}
		}
		return err
	}
	a.deadline.stop()
	s.attempt = a
	s.scanner = bufio.NewScanner(a.resp.Body)
	s.scanner.Buffer(make([]byte, 64<<10), 16<<20)
	if s.onOpen != nil {
		s.onOpen()
	}
	return nil
}

// read returns the next known frame. The end of the body, with or without
// an unterminated frame, is a reconnect.
func (s *Stream[T]) read() (T, bool, error) {
	var zero T
	event, id := "", ""
	var data []string
	for {
		if !s.scanner.Scan() {
			if err := s.scanner.Err(); err != nil {
				return zero, false, reconnect{fmt.Errorf("bma: event stream dropped: %w", err)}
			}
			return zero, false, reconnect{errStreamEnded}
		}
		s.failures = 0 // data, a heartbeat included, resets the budget
		line := s.scanner.Text()
		if line == "" {
			if len(data) > 0 {
				value, ok, err := s.dispatch(event, id, strings.Join(data, "\n"))
				if err != nil || ok {
					return value, ok, err
				}
			}
			event, id, data = "", "", nil
			continue
		}
		if strings.HasPrefix(line, ":") {
			continue
		}
		name, value, _ := strings.Cut(line, ":")
		value = strings.TrimPrefix(value, " ")
		switch name {
		case "event":
			event = value
		case "id":
			id = value
		case "data":
			data = append(data, value)
		}
	}
}

func (s *Stream[T]) dispatch(event, id, data string) (T, bool, error) {
	var zero T
	if event == "" {
		event = "message"
	}
	if event == "error" {
		var frame struct {
			Code string `json:"code"`
		}
		_ = json.Unmarshal([]byte(data), &frame)
		err := s.client.StreamError([]byte(data))
		if frame.Code == "service_unavailable" {
			return zero, false, reconnect{err}
		}
		return zero, false, err
	}
	var sequence int64
	if id != "" {
		n, err := strconv.ParseInt(id, 10, 64)
		if err != nil {
			return zero, false, fmt.Errorf("bma: invalid event id %q", id)
		}
		sequence, s.lastID = n, id
	}
	return s.decode(event, id, sequence, []byte(data))
}

func (s *Stream[T]) fail(err error) bool {
	s.err, s.done = err, true
	return false
}

func (s *Stream[T]) closeAttempt() {
	if s.attempt != nil {
		s.attempt.resp.Body.Close()
		s.attempt.done()
		s.attempt = nil
	}
}

// Current is the frame Next moved to.
func (s *Stream[T]) Current() T { return s.current }

// Err is the error that ended the stream; nil after Close.
func (s *Stream[T]) Err() error {
	if s.closed.Load() && errors.Is(s.err, context.Canceled) {
		return nil
	}
	return s.err
}

// Close ends the stream; safe to call from another goroutine while Next
// blocks (Next then returns false). Call it when done iterating.
func (s *Stream[T]) Close() error {
	s.closed.Store(true)
	s.cancel()
	return nil
}
