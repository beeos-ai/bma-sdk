package apicore

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"math"
	"math/rand/v2"
	"net"
	"net/http"
	"strconv"
	"time"
)

// errTimedOut marks an attempt ended by the per-attempt timeout.
var errTimedOut = errors.New("bma: request timed out")

type attempt struct {
	resp   *http.Response
	cancel context.CancelCauseFunc
	timer  *time.Timer
}

// done releases the attempt's timer and context; call after the body is read.
func (a *attempt) done() {
	a.timer.Stop()
	a.cancel(context.Canceled)
}

// send performs the request with retries. GET and operations with an
// Idempotency-Key retry 408/429/5xx and connection errors; other writes retry
// only requests that never reached the server, 429 and 503 (D3). 409 is
// never retried. For streams the timeout stops once headers arrive.
func (r *Request) send(ctx context.Context, accept string) (*attempt, error) {
	if r.err != nil {
		return nil, r.err
	}
	key := ""
	if r.op.Idempotency {
		key = r.cfg.IdempotencyKey
		if key == "" {
			key = newIdempotencyKey()
		}
	}
	safe := r.op.Method == http.MethodGet || r.op.Idempotency
	httpClient := r.cfg.HTTPClient
	if httpClient == nil {
		httpClient = http.DefaultClient
	}
	timeout := r.cfg.Timeout
	if timeout <= 0 {
		timeout = DefaultTimeout
	}
	for used := 0; ; used++ {
		actx, cancel := context.WithCancelCause(ctx)
		timer := time.AfterFunc(timeout, func() { cancel(errTimedOut) })
		req, err := r.build(actx, key)
		if err != nil {
			timer.Stop()
			cancel(nil)
			return nil, err
		}
		if accept != "" {
			req.Header.Set("Accept", accept)
		}
		resp, err := httpClient.Do(req)
		if err != nil {
			timedOut := context.Cause(actx) == errTimedOut && ctx.Err() == nil
			timer.Stop()
			cancel(nil)
			if ctx.Err() != nil {
				return nil, ctx.Err()
			}
			if used < r.cfg.MaxRetries && (safe || (!timedOut && undelivered(err))) {
				if err := sleep(ctx, backoff(used)); err != nil {
					return nil, err
				}
				continue
			}
			if timedOut {
				return nil, fmt.Errorf("bma: %s timed out after %s: %w (%w)", r.op.ID, timeout, context.DeadlineExceeded, err)
			}
			return nil, fmt.Errorf("bma: %s: connection error: %w", r.op.ID, err)
		}
		if resp.StatusCode >= 200 && resp.StatusCode < 300 {
			return &attempt{resp: resp, cancel: cancel, timer: timer}, nil
		}
		raw, _ := io.ReadAll(io.LimitReader(resp.Body, maxErrorBody))
		resp.Body.Close()
		timer.Stop()
		cancel(nil)
		apiErr := r.client.NewError(resp.StatusCode, raw, resp.Header)
		if used < r.cfg.MaxRetries && shouldRetry(resp, safe) {
			delay, ok := retryAfter(resp.Header)
			if !ok {
				delay = backoff(used)
			}
			if err := sleep(ctx, delay); err != nil {
				return nil, err
			}
			continue
		}
		return nil, apiErr
	}
}

// undelivered: the request provably never reached the server (resolution,
// refusal, connect timeout).
func undelivered(err error) bool {
	var dns *net.DNSError
	if errors.As(err, &dns) {
		return true
	}
	var op *net.OpError
	return errors.As(err, &op) && op.Op == "dial"
}

func shouldRetry(resp *http.Response, safe bool) bool {
	hint := resp.Header.Get("x-should-retry")
	if hint == "false" {
		return false
	}
	s := resp.StatusCode
	if !safe {
		return s == 429 || s == 503
	}
	if hint == "true" {
		return true
	}
	return s == 408 || s == 429 || s >= 500
}

// Exponential backoff with up to 25% jitter: 0.5s, 1s, 2s ... capped at 8s
// (@anthropic-ai/sdk calculateDefaultRetryTimeoutMillis).
func backoff(retry int) time.Duration {
	seconds := math.Min(0.5*math.Pow(2, float64(retry)), 8) * (1 - rand.Float64()*0.25)
	return time.Duration(seconds * float64(time.Second))
}

// retry-after-ms, then retry-after (seconds or HTTP date), honoured between 0 and 60s.
func retryAfter(h http.Header) (time.Duration, bool) {
	if ms, err := strconv.ParseFloat(h.Get("retry-after-ms"), 64); err == nil && ms >= 0 && ms < 60_000 {
		return time.Duration(ms * float64(time.Millisecond)), true
	}
	if raw := h.Get("retry-after"); raw != "" {
		if s, err := strconv.ParseFloat(raw, 64); err == nil && s >= 0 && s < 60 {
			return time.Duration(s * float64(time.Second)), true
		}
		if t, err := http.ParseTime(raw); err == nil {
			if d := time.Until(t); d >= 0 && d < time.Minute {
				return d, true
			}
		}
	}
	return 0, false
}

func sleep(ctx context.Context, d time.Duration) error {
	t := time.NewTimer(d)
	defer t.Stop()
	select {
	case <-ctx.Done():
		return ctx.Err()
	case <-t.C:
		return nil
	}
}

// Do sends the request and decodes a JSON response into T.
func Do[T any](ctx context.Context, r *Request) (*T, error) {
	a, err := r.send(ctx, "")
	if err != nil {
		return nil, err
	}
	defer a.done()
	defer a.resp.Body.Close()
	raw, err := io.ReadAll(a.resp.Body)
	if err != nil {
		return nil, fmt.Errorf("bma: %s: read response: %w", r.op.ID, err)
	}
	out := new(T)
	if err := json.Unmarshal(raw, out); err != nil {
		return nil, fmt.Errorf("bma: %s: decode response: %w", r.op.ID, err)
	}
	return out, nil
}

// DoBytes sends the request and returns the success status and body.
func DoBytes(ctx context.Context, r *Request) (int, []byte, error) {
	a, err := r.send(ctx, "")
	if err != nil {
		return 0, nil, err
	}
	defer a.done()
	defer a.resp.Body.Close()
	raw, err := io.ReadAll(a.resp.Body)
	if err != nil {
		return 0, nil, fmt.Errorf("bma: %s: read response: %w", r.op.ID, err)
	}
	return a.resp.StatusCode, raw, nil
}

// DoVoid sends a request whose success response has no body.
func DoVoid(ctx context.Context, r *Request) error {
	a, err := r.send(ctx, "")
	if err != nil {
		return err
	}
	defer a.done()
	_, _ = io.Copy(io.Discard, a.resp.Body)
	return a.resp.Body.Close()
}

// DoRaw returns the successful response with its body unread; the caller
// closes it. The per-attempt timeout no longer applies to the body.
func DoRaw(ctx context.Context, r *Request) (*http.Response, error) {
	a, err := r.send(ctx, "")
	if err != nil {
		return nil, err
	}
	a.timer.Stop()
	a.resp.Body = &closer{ReadCloser: a.resp.Body, cancel: a.cancel}
	return a.resp, nil
}

type closer struct {
	io.ReadCloser
	cancel context.CancelCauseFunc
}

func (c *closer) Close() error {
	err := c.ReadCloser.Close()
	c.cancel(context.Canceled)
	return err
}
