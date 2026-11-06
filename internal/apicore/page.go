package apicore

import (
	"context"
	"encoding/json"
	"strings"
)

// CursorPage is one page of a paginated list: a response {data, next_<param>}
// for a query parameter <param> (cursor, page, before_id/after_id,
// before_sequence/after_sequence).
type CursorPage[T any] struct {
	Data []T `json:"data"`
	// NextCursor is the value the next request sends in the list's cursor
	// parameter; nil on the last page.
	NextCursor *string `json:"-"`
	// Raw is the whole response body, for fields beyond data.
	Raw json.RawMessage `json:"-"`

	ctx   context.Context
	build func() *Request
	param string
	field string
}

// HasNextPage reports whether GetNextPage has a page to fetch.
func (p *CursorPage[T]) HasNextPage() bool {
	return p.NextCursor != nil && len(p.Data) > 0
}

// GetNextPage fetches the following page; ErrNoPage after the last one.
func (p *CursorPage[T]) GetNextPage() (*CursorPage[T], error) {
	if !p.HasNextPage() {
		return nil, ErrNoPage
	}
	return FetchPage[T](p.ctx, p.build, p.param, p.field, *p.NextCursor)
}

// FetchPage fetches one page; build returns a fresh request each time. param
// is the cursor query parameter and field the response member holding its
// next value; cursor "" keeps the request's own parameters.
func FetchPage[T any](ctx context.Context, build func() *Request, param, field, cursor string) (*CursorPage[T], error) {
	r := build()
	if cursor != "" {
		r.SetQuery(param, cursor)
	}
	raw, err := Do[json.RawMessage](ctx, r)
	if err != nil {
		return nil, err
	}
	page := &CursorPage[T]{Raw: *raw, ctx: ctx, build: build, param: param, field: field}
	if err := json.Unmarshal(*raw, page); err != nil {
		return nil, err
	}
	var members map[string]json.RawMessage
	if err := json.Unmarshal(*raw, &members); err != nil {
		return nil, err
	}
	var hasMore *bool
	if m, ok := members["has_more"]; ok {
		_ = json.Unmarshal(m, &hasMore)
	}
	if next := strings.TrimSpace(string(members[field])); next != "" && next != "null" && next != `""` && (hasMore == nil || *hasMore) {
		var s string
		if json.Unmarshal([]byte(next), &s) != nil {
			s = next // a number
		}
		page.NextCursor = &s
	}
	return page, nil
}

// AutoPager walks every item across pages:
//
//	for pager.Next() { item := pager.Current() }
//	if err := pager.Err(); err != nil { ... }
type AutoPager[T any] struct {
	ctx          context.Context
	build        func() *Request
	param, field string
	page         *CursorPage[T]
	index        int
	current      T
	err          error
	started      bool
}

// NewAutoPager returns a pager that fetches lazily.
func NewAutoPager[T any](ctx context.Context, build func() *Request, param, field string) *AutoPager[T] {
	return &AutoPager[T]{ctx: ctx, build: build, param: param, field: field}
}

// Next advances to the next item, fetching pages as needed.
func (a *AutoPager[T]) Next() bool {
	if a.err != nil {
		return false
	}
	if !a.started {
		a.started = true
		a.page, a.err = FetchPage[T](a.ctx, a.build, a.param, a.field, "")
		if a.err != nil {
			return false
		}
	}
	for a.index >= len(a.page.Data) {
		if !a.page.HasNextPage() {
			return false
		}
		a.page, a.err = a.page.GetNextPage()
		if a.err != nil {
			return false
		}
		a.index = 0
	}
	a.current = a.page.Data[a.index]
	a.index++
	return true
}

// Current is the item Next moved to.
func (a *AutoPager[T]) Current() T { return a.current }

// Err is the error that stopped iteration, if any.
func (a *AutoPager[T]) Err() error { return a.err }
