package bma_test

import (
	"bytes"
	"io"
	"net/http"
)

type recorder struct {
	header http.Header
	status int
	body   bytes.Buffer
}

func newRecorder() *recorder                    { return &recorder{header: http.Header{}, status: 200} }
func (r *recorder) Header() http.Header         { return r.header }
func (r *recorder) Write(b []byte) (int, error) { return r.body.Write(b) }
func (r *recorder) WriteHeader(status int)      { r.status = status }
func (r *recorder) result(req *http.Request) *http.Response {
	if r.header.Get("Content-Type") == "" {
		r.header.Set("Content-Type", "application/json")
	}
	return &http.Response{StatusCode: r.status, Header: r.header, Body: io.NopCloser(&r.body), Request: req}
}
