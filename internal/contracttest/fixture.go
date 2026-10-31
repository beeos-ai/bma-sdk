// Package contracttest serves the recorded SDK contract fixtures in
// contracts/bma/fixtures/sdk-contract.json to package tests. The same file is
// replayed by the TypeScript and Python SDK tests, and
// tools/check_contract.py validates it against the OpenAPI contracts.
package contracttest

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"mime"
	"mime/multipart"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"reflect"
	"runtime"
	"strings"
	"testing"
)

// Fixtures is the decoded fixture file.
type Fixtures struct {
	Scope  map[string]string `json:"scope"`
	REST   []Case            `json:"rest"`
	Facade []Case            `json:"facade"`
}

// Case is one recorded exchange.
type Case struct {
	Name        string   `json:"name"`
	OperationID string   `json:"operationId"`
	Request     Request  `json:"request"`
	Response    Response `json:"response"`
}

type Request struct {
	Method    string            `json:"method"`
	Path      string            `json:"path"`
	Query     map[string]string `json:"query"`
	Headers   map[string]string `json:"headers"`
	JSON      json.RawMessage   `json:"json"`
	Text      *string           `json:"text"` // raw application/octet-stream body
	Multipart *Multipart        `json:"multipart"`
}

type Multipart struct {
	Field    string `json:"field"`
	Filename string `json:"filename"`
	Text     string `json:"text"`
}

type Response struct {
	Status      int             `json:"status"`
	JSON        json.RawMessage `json:"json"`
	Text        string          `json:"text"`
	ContentType string          `json:"content_type"`
	SSE         []SSEFrame      `json:"sse"`
}

type SSEFrame struct {
	Comment string          `json:"comment"`
	Event   string          `json:"event"`
	ID      string          `json:"id"`
	Data    json.RawMessage `json:"data"`
}

// Load reads the fixture file from the repository checkout.
func Load(t *testing.T) Fixtures {
	t.Helper()
	_, file, _, _ := runtime.Caller(0)
	path := filepath.Join(filepath.Dir(file), "..", "..", "..", "contracts", "bma", "fixtures", "sdk-contract.json")
	raw, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("read contract fixtures: %v", err)
	}
	var fixtures Fixtures
	if err := json.Unmarshal(raw, &fixtures); err != nil {
		t.Fatalf("decode contract fixtures: %v", err)
	}
	return fixtures
}

// Find returns the named case.
func Find(t *testing.T, cases []Case, name string) Case {
	t.Helper()
	for _, c := range cases {
		if c.Name == name {
			return c
		}
	}
	t.Fatalf("contract fixture %q not found", name)
	return Case{}
}

// Serve starts a server that accepts exactly the recorded request of c,
// replies with the recorded response, and fails t on any mismatch.
func Serve(t *testing.T, c Case, prefix string) *httptest.Server {
	t.Helper()
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if err := match(c.Request, prefix, r); err != nil {
			t.Errorf("%s: %v", c.Name, err)
			http.Error(w, err.Error(), http.StatusTeapot)
			return
		}
		write(w, c.Response)
	}))
	t.Cleanup(server.Close)
	return server
}

func match(want Request, prefix string, r *http.Request) error {
	if r.Method != want.Method {
		return fmt.Errorf("method = %s, want %s", r.Method, want.Method)
	}
	if r.URL.Path != prefix+want.Path {
		return fmt.Errorf("path = %s, want %s", r.URL.Path, prefix+want.Path)
	}
	query := map[string]string{}
	for key, values := range r.URL.Query() {
		query[key] = strings.Join(values, ",")
	}
	if len(query) != len(want.Query) || (len(want.Query) > 0 && !reflect.DeepEqual(query, want.Query)) {
		return fmt.Errorf("query = %v, want %v", query, want.Query)
	}
	for key, value := range want.Headers {
		if got := r.Header.Get(key); got != value {
			return fmt.Errorf("header %s = %q, want %q", key, got, value)
		}
	}
	body, err := io.ReadAll(r.Body)
	if err != nil {
		return err
	}
	switch {
	case want.JSON != nil:
		var got, expected any
		if err := json.Unmarshal(body, &got); err != nil {
			return fmt.Errorf("decode request body: %w", err)
		}
		_ = json.Unmarshal(want.JSON, &expected)
		if !reflect.DeepEqual(got, expected) {
			return fmt.Errorf("body = %s, want %s", body, want.JSON)
		}
	case want.Text != nil:
		if ct := r.Header.Get("Content-Type"); ct != "application/octet-stream" {
			return fmt.Errorf("content type = %q, want application/octet-stream", ct)
		}
		if string(body) != *want.Text {
			return fmt.Errorf("body = %q, want %q", body, *want.Text)
		}
	case want.Multipart != nil:
		return matchMultipart(*want.Multipart, r.Header.Get("Content-Type"), body)
	case len(bytes.TrimSpace(body)) > 0 && string(bytes.TrimSpace(body)) != "{}":
		return fmt.Errorf("unexpected body %s", body)
	}
	return nil
}

func matchMultipart(want Multipart, contentType string, body []byte) error {
	media, params, err := mime.ParseMediaType(contentType)
	if err != nil || media != "multipart/form-data" {
		return fmt.Errorf("content type = %q, want multipart/form-data", contentType)
	}
	reader := multipart.NewReader(bytes.NewReader(body), params["boundary"])
	part, err := reader.NextPart()
	if err != nil {
		return fmt.Errorf("read multipart: %w", err)
	}
	content, _ := io.ReadAll(part)
	if part.FormName() != want.Field || part.FileName() != want.Filename || string(content) != want.Text {
		return fmt.Errorf("multipart part = %s/%s/%q, want %s/%s/%q",
			part.FormName(), part.FileName(), content, want.Field, want.Filename, want.Text)
	}
	if _, err := reader.NextPart(); err != io.EOF {
		return fmt.Errorf("multipart has more than one part")
	}
	return nil
}

func write(w http.ResponseWriter, response Response) {
	switch {
	case response.SSE != nil:
		w.Header().Set("Content-Type", "text/event-stream")
		w.WriteHeader(response.Status)
		for _, frame := range response.SSE {
			if frame.Comment != "" {
				fmt.Fprintf(w, ": %s\n\n", frame.Comment)
				continue
			}
			if frame.Event != "" {
				fmt.Fprintf(w, "event: %s\n", frame.Event)
			}
			if frame.ID != "" {
				fmt.Fprintf(w, "id: %s\n", frame.ID)
			}
			var compact bytes.Buffer
			_ = json.Compact(&compact, frame.Data)
			fmt.Fprintf(w, "data: %s\n\n", compact.Bytes())
		}
	case response.JSON != nil:
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(response.Status)
		_, _ = w.Write(response.JSON)
	default:
		w.Header().Set("Content-Type", response.ContentType)
		w.WriteHeader(response.Status)
		_, _ = io.WriteString(w, response.Text)
	}
}
