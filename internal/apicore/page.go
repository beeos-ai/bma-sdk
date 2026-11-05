package apicore

import (
	"context"
	"encoding/json"
)

// CursorPage is one page of a cursor-paginated list ({data, next_cursor}).
type CursorPage[T any] struct {
	Data       []T     `json:"data"`
	NextCursor *string `json:"next_cursor"`
	// Raw is the whole response body, for fields beyond data and next_cursor.
	Raw json.RawMessage `json:"-"`

	ctx   context.Context
	build func() *Request
}

// HasNextPage reports whether GetNextPage has a page to fetch.
func (p *CursorPage[T]) HasNextPage() bool {
	return p.NextCursor != nil && *p.NextCursor != "" && len(p.Data) > 0
}

// GetNextPage fetches the following page; ErrNoPage after the last one.
func (p *CursorPage[T]) GetNextPage() (*CursorPage[T], error) {
	if !p.HasNextPage() {
		return nil, ErrNoPage
	}
	return FetchPage[T](p.ctx, p.build, *p.NextCursor)
}

// FetchPage fetches one page; build returns a fresh request each time.
func FetchPage[T any](ctx context.Context, build func() *Request, cursor string) (*CursorPage[T], error) {
	r := build()
	if cursor != "" {
		r.SetQuery("cursor", cursor)
	}
	raw, err := Do[json.RawMessage](ctx, r)
	if err != nil {
		return nil, err
	}
	page := &CursorPage[T]{Raw: *raw, ctx: ctx, build: build}
	if err := json.Unmarshal(*raw, page); err != nil {
		return nil, err
	}
	return page, nil
}

// AutoPager walks every item across pages:
//
//	for pager.Next() { item := pager.Current() }
//	if err := pager.Err(); err != nil { ... }
type AutoPager[T any] struct {
	ctx     context.Context
	build   func() *Request
	page    *CursorPage[T]
	index   int
	current T
	err     error
	started bool
}

// NewAutoPager returns a pager that fetches lazily.
func NewAutoPager[T any](ctx context.Context, build func() *Request) *AutoPager[T] {
	return &AutoPager[T]{ctx: ctx, build: build}
}

// Next advances to the next item, fetching pages as needed.
func (a *AutoPager[T]) Next() bool {
	if a.err != nil {
		return false
	}
	if !a.started {
		a.started = true
		a.page, a.err = FetchPage[T](a.ctx, a.build, "")
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
