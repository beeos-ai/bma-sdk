// Package apicore is the request runtime shared by every generated resource
// method of package bma and package facade: scope defaults, request
// encoding, retries with idempotency keys, timeouts, error decoding,
// pagination and event streams. The rules match typescript/src/core.ts; the
// defaults are ADR 0012 decision D3.
package apicore

import (
	"bytes"
	"context"
	"crypto/rand"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
	"net/textproto"
	"net/url"
	"path"
	"reflect"
	"sort"
	"strconv"
	"strings"
	"time"

	"github.com/beeos-ai/bma-sdk/internal/requestconfig"
)

const (
	// DefaultTimeout is the per-attempt timeout (D3). For uploads it bounds
	// the wait for the response after the body is sent.
	DefaultTimeout = 60 * time.Second
	// DefaultMaxRetries is the number of retries after the first attempt (D3).
	DefaultMaxRetries = 2
	maxErrorBody      = 1 << 20
)

// Op describes one contract operation; generated per operation.
type Op struct {
	ID     string
	Method string
	Path   string
	// Scope maps a path parameter to "org" or "project" when the client
	// default fills it.
	Scope map[string]string
	// ScopeHeader is a header filled with the project default (facade).
	ScopeHeader string
	// Idempotency: the operation accepts an Idempotency-Key header.
	Idempotency bool
}

// Client is the transport of one API surface.
type Client struct {
	Config requestconfig.Config
	// NewError decodes a non-2xx response; StreamError an SSE error frame.
	NewError    func(status int, body []byte, header http.Header) error
	StreamError func(body []byte) error
	UserAgent   string
	// Validate checks the effective config of every request.
	Validate func(*requestconfig.Config) error
}

// Request is built by a generated method, then sent with Do, DoVoid, DoRaw,
// FetchPage or OpenStream.
type Request struct {
	client      *Client
	op          *Op
	cfg         requestconfig.Config
	err         error
	path        map[string]string
	query       url.Values
	header      http.Header
	body        []byte
	contentType string
	form        *multipart.Writer
	formBuf     *bytes.Buffer
	formClosed  bool
	// upload: a binary or multipart body; its timeout starts once it is sent.
	upload bool
	// stream is a binary body read while sending; a seekable one is
	// rewound to streamStart for a retry, any other is sent once.
	stream      io.Reader
	seekable    bool
	streamStart int64
	streamLen   int64
}

// NewRequest starts a request for op with per-call options.
func (c *Client) NewRequest(op *Op, opts []requestconfig.RequestOption) *Request {
	cfg, err := requestconfig.Apply(c.Config, opts)
	r := &Request{client: c, op: op, cfg: cfg, err: err, path: map[string]string{}, query: url.Values{}, header: http.Header{}}
	if err == nil && c.Validate != nil {
		r.err = c.Validate(&r.cfg)
	}
	if r.err == nil && !op.Idempotency && cfg.IdempotencyKey != "" {
		r.err = fmt.Errorf("bma: %s does not accept an Idempotency-Key", op.ID)
	}
	return r
}

// Path sets a positional path parameter.
func (r *Request) Path(name, value string) {
	if value == "" && r.err == nil {
		r.err = fmt.Errorf("bma: %s needs a non-empty %s", r.op.ID, name)
	}
	r.path[name] = value
}

// Query adds a query parameter; nil pointers and empty optional values are skipped.
func (r *Request) Query(name, style string, value any) {
	v, ok := deref(value)
	if !ok {
		return
	}
	switch {
	case style == "deepObject" && v.Kind() == reflect.Map:
		iter := v.MapRange()
		for iter.Next() {
			r.query.Add(fmt.Sprintf("%s[%v]", name, iter.Key().Interface()), scalar(iter.Value()))
		}
	case v.Kind() == reflect.Slice && v.Type().Elem().Kind() != reflect.Uint8:
		for i := 0; i < v.Len(); i++ {
			r.query.Add(name, scalar(v.Index(i)))
		}
	default:
		r.query.Set(name, scalar(v))
	}
}

// SetQuery replaces a query parameter (the page cursor).
func (r *Request) SetQuery(name, value string) { r.query.Set(name, value) }

// DelQuery removes a query parameter.
func (r *Request) DelQuery(name string) { r.query.Del(name) }

// Header sets a header parameter; nil pointers are skipped.
func (r *Request) Header(name string, value any) {
	if v, ok := deref(value); ok {
		r.header.Set(name, scalar(v))
	}
}

// JSON sets a JSON body, applying option.WithJSONSet members.
func (r *Request) JSON(body any) {
	raw, err := json.Marshal(body)
	if err == nil && len(r.cfg.JSONSet) > 0 {
		var members map[string]json.RawMessage
		if err = json.Unmarshal(raw, &members); err == nil {
			for k, v := range r.cfg.JSONSet {
				if members[k], err = json.Marshal(v); err != nil {
					break
				}
			}
			if err == nil {
				raw, err = json.Marshal(members)
			}
		}
	}
	if err != nil && r.err == nil {
		r.err = fmt.Errorf("bma: encode %s body: %w", r.op.ID, err)
	}
	r.body, r.contentType = raw, "application/json"
}

// Binary sets a raw body, streamed from body while sending. An io.Seeker
// (os.File, bytes.Reader) is sent with its length from the current offset
// and rewound for retries; any other reader is sent once and not retried.
func (r *Request) Binary(body io.Reader) {
	if body == nil {
		return
	}
	r.stream, r.contentType, r.upload = body, "application/octet-stream", true
	if s, ok := body.(io.Seeker); ok {
		start, err := s.Seek(0, io.SeekCurrent)
		var end int64
		if err == nil {
			end, err = s.Seek(0, io.SeekEnd)
		}
		if err == nil {
			_, err = s.Seek(start, io.SeekStart)
		}
		if err != nil && r.err == nil {
			r.err = fmt.Errorf("bma: seek %s body: %w", r.op.ID, err)
		}
		r.seekable, r.streamStart, r.streamLen = true, start, end-start
	}
}

// replayable reports whether the body can be sent again.
func (r *Request) replayable() bool { return r.stream == nil || r.seekable }

// sentBody starts the deadline once the body has been read to the end.
type sentBody struct {
	io.Reader
	deadline *deadline
}

func (b *sentBody) Read(p []byte) (int, error) {
	n, err := b.Reader.Read(p)
	if err == io.EOF {
		b.deadline.start()
	}
	return n, err
}

func (r *Request) multipartWriter() *multipart.Writer {
	r.upload = true
	if r.form == nil {
		r.formBuf = &bytes.Buffer{}
		r.form = multipart.NewWriter(r.formBuf)
	}
	return r.form
}

// MultipartFile adds a file part; nil readers are skipped. The filename comes
// from a Name() method (os.File, bma.NewFile), else the field name.
func (r *Request) MultipartFile(name string, file io.Reader) {
	if file == nil {
		return
	}
	filename, contentType := name, "application/octet-stream"
	if named, ok := file.(interface{ Name() string }); ok && named.Name() != "" {
		filename = path.Base(named.Name())
	}
	if typed, ok := file.(interface{ ContentType() string }); ok && typed.ContentType() != "" {
		contentType = typed.ContentType()
	}
	h := textproto.MIMEHeader{}
	h.Set("Content-Disposition", fmt.Sprintf(`form-data; name=%q; filename=%q`, name, filename))
	h.Set("Content-Type", contentType)
	part, err := r.multipartWriter().CreatePart(h)
	if err == nil {
		_, err = io.Copy(part, file)
	}
	if err != nil && r.err == nil {
		r.err = fmt.Errorf("bma: read %s part %s: %w", r.op.ID, name, err)
	}
}

// MultipartField adds a form field; asJSON encodes it as JSON.
func (r *Request) MultipartField(name string, value any, asJSON bool) {
	v, ok := deref(value)
	if !ok {
		return
	}
	var text string
	if asJSON || v.Kind() == reflect.Struct || v.Kind() == reflect.Map || v.Kind() == reflect.Slice {
		raw, err := json.Marshal(v.Interface())
		if err != nil && r.err == nil {
			r.err = fmt.Errorf("bma: encode %s part %s: %w", r.op.ID, name, err)
		}
		text = string(raw)
	} else {
		text = scalar(v)
	}
	h := textproto.MIMEHeader{}
	h.Set("Content-Disposition", fmt.Sprintf(`form-data; name=%q`, name))
	if asJSON {
		h.Set("Content-Type", "application/json") // the contract's multipart encoding
	}
	part, err := r.multipartWriter().CreatePart(h)
	if err == nil {
		_, err = io.WriteString(part, text)
	}
	if err != nil && r.err == nil {
		r.err = err
	}
}

func deref(value any) (reflect.Value, bool) {
	v := reflect.ValueOf(value)
	for v.IsValid() && (v.Kind() == reflect.Pointer || v.Kind() == reflect.Interface) {
		if v.IsNil() {
			return v, false
		}
		v = v.Elem()
	}
	return v, v.IsValid()
}

func scalar(v reflect.Value) string {
	for v.Kind() == reflect.Pointer || v.Kind() == reflect.Interface {
		v = v.Elem()
	}
	if t, ok := v.Interface().(time.Time); ok {
		return t.Format(time.RFC3339Nano)
	}
	if s, ok := v.Interface().(fmt.Stringer); ok && v.Kind() != reflect.String {
		return s.String()
	}
	switch v.Kind() {
	case reflect.String:
		return v.String()
	case reflect.Bool:
		return strconv.FormatBool(v.Bool())
	case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32, reflect.Int64:
		return strconv.FormatInt(v.Int(), 10)
	case reflect.Uint, reflect.Uint8, reflect.Uint16, reflect.Uint32, reflect.Uint64:
		return strconv.FormatUint(v.Uint(), 10)
	case reflect.Float32, reflect.Float64:
		return strconv.FormatFloat(v.Float(), 'f', -1, 64)
	}
	return fmt.Sprint(v.Interface())
}

func (r *Request) build(ctx context.Context, idempotencyKey string, attempt int, timer *deadline) (*http.Request, error) {
	u := r.op.Path
	names := make([]string, 0, len(r.op.Scope))
	for name := range r.op.Scope {
		names = append(names, name)
	}
	sort.Slice(names, func(i, j int) bool { return r.op.Scope[names[i]] < r.op.Scope[names[j]] }) // org before project
	for _, name := range names {
		scope := r.op.Scope[name]
		value := r.cfg.Org
		option := "option.WithOrg (or BMA_ORG_ID)"
		if scope == "project" {
			value, option = r.cfg.Project, "option.WithProject (or BMA_PROJECT_ID)"
		}
		if value == "" {
			return nil, fmt.Errorf("bma: %s needs the %s; set %s", r.op.ID, scope, option)
		}
		u = strings.ReplaceAll(u, "{"+name+"}", url.PathEscape(value))
	}
	for name, value := range r.path {
		u = strings.ReplaceAll(u, "{"+name+"}", url.PathEscape(value))
	}
	full := r.cfg.BaseURL + u
	if q := r.query.Encode(); q != "" {
		full += "?" + q
	}
	var body io.Reader
	length := int64(-1)
	contentType := r.contentType
	switch {
	case r.form != nil:
		if !r.formClosed {
			r.formClosed = true
			if err := r.form.Close(); err != nil {
				return nil, err
			}
		}
		body, contentType, length = bytes.NewReader(r.formBuf.Bytes()), r.form.FormDataContentType(), int64(r.formBuf.Len())
	case r.stream != nil:
		if r.seekable {
			if attempt > 0 {
				if _, err := r.stream.(io.Seeker).Seek(r.streamStart, io.SeekStart); err != nil {
					return nil, fmt.Errorf("bma: rewind %s body: %w", r.op.ID, err)
				}
			}
			length = r.streamLen
		}
		body = r.stream
	case r.body != nil:
		body, length = bytes.NewReader(r.body), int64(len(r.body))
	}
	if body != nil {
		// Not an io.Closer, so the transport never closes the caller's file.
		body = &sentBody{Reader: body, deadline: timer}
	}
	req, err := http.NewRequestWithContext(ctx, r.op.Method, full, body)
	if err != nil {
		return nil, err
	}
	if body != nil {
		req.ContentLength = length
		if length == 0 {
			req.Body = http.NoBody
			timer.start()
		}
	}
	for k, v := range r.header {
		req.Header[k] = v
	}
	if contentType != "" {
		req.Header.Set("Content-Type", contentType)
	}
	if r.cfg.Token != "" {
		req.Header.Set("Authorization", "Bearer "+r.cfg.Token)
	}
	if r.cfg.APIKey != "" {
		req.Header.Set("x-api-key", r.cfg.APIKey)
	}
	if r.op.ScopeHeader != "" && r.cfg.Project != "" {
		req.Header.Set(r.op.ScopeHeader, r.cfg.Project)
	}
	if idempotencyKey != "" {
		req.Header.Set("Idempotency-Key", idempotencyKey)
	}
	if r.client.UserAgent != "" {
		req.Header.Set("User-Agent", r.client.UserAgent)
	}
	for k, v := range r.cfg.Headers {
		req.Header[k] = v
	}
	return req, nil
}

func newIdempotencyKey() string {
	var b [16]byte
	_, _ = rand.Read(b[:])
	b[6] = b[6]&0x0f | 0x40
	b[8] = b[8]&0x3f | 0x80
	return fmt.Sprintf("bma-sdk-retry-%x-%x-%x-%x-%x", b[0:4], b[4:6], b[6:8], b[8:10], b[10:16])
}

// ErrNoPage is returned by GetNextPage after the last page.
var ErrNoPage = errors.New("bma: no next page; check HasNextPage first")

// CheckBaseURL validates an API root.
func CheckBaseURL(base string) error {
	u, err := url.Parse(base)
	if err != nil || (u.Scheme != "http" && u.Scheme != "https") || u.Host == "" {
		return fmt.Errorf("bma: base URL %q must be an http or https URL", base)
	}
	return nil
}
