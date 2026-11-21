package bmasdk

import (
	"context"
	"crypto/rand"
	"encoding/hex"
	"iter"
	"net/url"
	"slices"

	"github.com/anthropics/anthropic-sdk-go/v2"
	"github.com/anthropics/anthropic-sdk-go/v2/option"
)

// execute sends one extension request through the official client, so the
// base URL, credentials, headers, retries, timeouts, middleware and the
// *anthropic.Error type are the official ones.
func execute(ctx context.Context, method, path string, params, res any, opts ...option.RequestOption) error {
	var client anthropic.Client
	return client.Execute(ctx, method, path, params, res, opts...)
}

// autoIdempotencyKey is the default Idempotency-Key of an extension create;
// a later WithIdempotencyKey replaces it.
func autoIdempotencyKey() option.RequestOption {
	var b [16]byte
	if _, err := rand.Read(b[:]); err != nil {
		panic(err) // crypto/rand.Read never fails on supported platforms
	}
	return WithIdempotencyKey(hex.EncodeToString(b[:]))
}

// query is the URL query of a list or a lookup; it implements the URLQuery
// method the official client serializes.
type query url.Values

func (q query) URLQuery() (url.Values, error) { return url.Values(q), nil }

// Page is one page of an extension list: {"data": [...], "next_page": ...},
// the shape of the official pagination.PageCursor.
type Page[T any] struct {
	Data     []T    `json:"data"`
	NextPage string `json:"next_page"`

	fetch func(page string) (*Page[T], error)
}

// GetNextPage returns the next page, or nil without an error after the last.
func (r *Page[T]) GetNextPage() (*Page[T], error) {
	if r == nil || r.NextPage == "" || r.fetch == nil {
		return nil, nil
	}
	return r.fetch(r.NextPage)
}

// listPage fetches one page of path with q plus page, and remembers how to
// fetch the next one.
func listPage[T any](ctx context.Context, path string, q query, page string, opts []option.RequestOption) (*Page[T], error) {
	values := url.Values{}
	for k, v := range q {
		values[k] = slices.Clone(v)
	}
	if page != "" {
		values.Set("page", page)
	}
	var res Page[T]
	if err := execute(ctx, "GET", path, query(values), &res, opts...); err != nil {
		return nil, err
	}
	res.fetch = func(next string) (*Page[T], error) { return listPage[T](ctx, path, q, next, opts) }
	return &res, nil
}

// PageAutoPager iterates every item of an extension list across pages, with
// the method set of the official pagination.PageCursorAutoPager.
type PageAutoPager[T any] struct {
	page *Page[T]
	cur  T
	idx  int
	run  int
	err  error
}

// NewPageAutoPager returns an iterator starting at page.
func NewPageAutoPager[T any](page *Page[T], err error) *PageAutoPager[T] {
	return &PageAutoPager[T]{page: page, err: err}
}

// Next advances to the next item, fetching pages as needed.
func (r *PageAutoPager[T]) Next() bool {
	if r.page == nil || r.err != nil {
		return false
	}
	for r.idx >= len(r.page.Data) {
		r.idx = 0
		r.page, r.err = r.page.GetNextPage()
		if r.err != nil || r.page == nil {
			return false
		}
	}
	r.cur = r.page.Data[r.idx]
	r.idx++
	r.run++
	return true
}

// Current is the item Next advanced to.
func (r *PageAutoPager[T]) Current() T { return r.cur }

// Err is the error that stopped the iteration, if any.
func (r *PageAutoPager[T]) Err() error { return r.err }

// Index is the number of items returned so far.
func (r *PageAutoPager[T]) Index() int { return r.run }

// All returns the remaining items as an iterator.
func (r *PageAutoPager[T]) All() iter.Seq[T] {
	return func(yield func(T) bool) {
		for r.Next() {
			if !yield(r.Current()) {
				break
			}
		}
	}
}
