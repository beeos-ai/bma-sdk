package apicore

import (
	"bufio"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"strconv"
	"strings"
	"sync/atomic"
)

// Decoder turns one SSE frame into T; ok=false skips an event kind newer
// than this SDK.
type Decoder[T any] func(event, id string, sequence int64, data []byte) (value T, ok bool, err error)

// Stream is a typed server-sent event stream with the reconnect rule of the
// contract: an `error` frame with code service_unavailable (or a dropped
// connection) reconnects with Last-Event-ID set to the last durable frame,
// up to MaxRetries times in a row; any other error frame ends the stream with
// the client's StreamError.
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
	retries  int
	closed   atomic.Bool
	lastID   string
	failures int
	current  T
	err      error
	done     bool
}

// OpenStream returns a lazily connecting stream. build(resume) returns a
// fresh request; resume is the Last-Event-ID to send ("" on first connect).
// onOpen, if set, runs after every (re)connection.
func OpenStream[T any](ctx context.Context, build func(resume string) *Request, decode Decoder[T], onOpen func()) *Stream[T] {
	ctx, cancel := context.WithCancel(ctx)
	return &Stream[T]{ctx: ctx, cancel: cancel, build: build, decode: decode, onOpen: onOpen}
}

type reconnect struct{ err error }

func (r reconnect) Error() string { return r.err.Error() }

// Next reads the next frame, reconnecting as the contract requires.
func (s *Stream[T]) Next() bool {
	for !s.done {
		if s.attempt == nil {
			r := s.build(s.lastID)
			s.client, s.retries = r.client, r.cfg.MaxRetries
			a, err := r.send(s.ctx, "text/event-stream")
			if err != nil {
				return s.fail(err)
			}
			a.timer.Stop()
			s.attempt = a
			s.scanner = bufio.NewScanner(a.resp.Body)
			s.scanner.Buffer(make([]byte, 64<<10), 16<<20)
			if s.onOpen != nil {
				s.onOpen()
			}
		}
		value, ok, err := s.read()
		if err == nil && ok {
			s.current = value
			return true
		}
		if err == nil { // clean end of stream
			s.closeAttempt()
			s.done = true
			return false
		}
		s.closeAttempt()
		var rc reconnect
		if s.ctx.Err() != nil || !errors.As(err, &rc) {
			if s.ctx.Err() != nil {
				err = s.ctx.Err()
			}
			return s.fail(err)
		}
		if s.failures >= s.retries {
			return s.fail(rc.err)
		}
		if err := sleep(s.ctx, backoff(s.failures)); err != nil {
			return s.fail(err)
		}
		s.failures++
	}
	return false
}

// read returns the next known frame; (zero, false, nil) at the end.
func (s *Stream[T]) read() (T, bool, error) {
	var zero T
	event, id := "", ""
	var data []string
	for {
		more := s.scanner.Scan()
		line := s.scanner.Text()
		if !more {
			if err := s.scanner.Err(); err != nil {
				return zero, false, reconnect{fmt.Errorf("bma: event stream dropped: %w", err)}
			}
			line = ""
		}
		if line == "" {
			if len(data) > 0 {
				value, ok, err := s.dispatch(event, id, strings.Join(data, "\n"))
				if err != nil || ok {
					return value, ok, err
				}
			}
			event, id, data = "", "", nil
			if !more {
				return zero, false, nil
			}
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
	s.failures = 0
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

// Err is the error that ended the stream; nil after a clean end or Close.
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
