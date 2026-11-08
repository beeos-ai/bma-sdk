package bmasdk_test

// Live test against a BMA deployment. Runs only with BMA_INTEGRATION=1 and
// BMA_API_KEY, BMA_BASE_URL (origin), BMA_PROJECT_ID and BMA_ORG_ID set:
//
//	BMA_INTEGRATION=1 go test -run TestStaging -v -timeout 20m ./...
//
// It creates an environment (deleted at the end), an agent and a session
// (archived at the end),
// so it runs against staging, never production.

import (
	"bytes"
	"context"
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
	"sync"
	"testing"
	"time"

	"github.com/anthropics/anthropic-sdk-go/v2"
	"github.com/anthropics/anthropic-sdk-go/v2/option"
	"github.com/anthropics/anthropic-sdk-go/v2/packages/ssestream"

	bmasdk "github.com/beeos-ai/bma-sdk/v2"
)

const stagingModel = "deepseek-flash"

func stagingClient(t *testing.T) *bmasdk.Client {
	t.Helper()
	if os.Getenv("BMA_INTEGRATION") != "1" {
		t.Skip("set BMA_INTEGRATION=1 to run against a BMA deployment")
	}
	for _, k := range []string{"BMA_API_KEY", "BMA_BASE_URL", "BMA_PROJECT_ID", "BMA_ORG_ID"} {
		if os.Getenv(k) == "" {
			t.Fatalf("%s is not set", k)
		}
	}
	if strings.Contains(os.Getenv("BMA_BASE_URL"), "api.bma.beeos.ai") {
		t.Fatal("refusing to run the live test against production")
	}
	return bmasdk.NewClient()
}

// stream reads events of one StreamEvents call on its own goroutine.
type stream struct {
	events chan anthropic.BetaManagedAgentsStreamSessionEventsUnion
	done   chan error
	s      *ssestream.Stream[anthropic.BetaManagedAgentsStreamSessionEventsUnion]
}

func openStream(ctx context.Context, t *testing.T, c *bmasdk.Client, sessionID string, opts ...option.RequestOption) *stream {
	t.Helper()
	s := c.Beta.Sessions.Events.StreamEvents(ctx, sessionID, anthropic.BetaSessionEventStreamParams{}, opts...)
	if err := s.Err(); err != nil {
		t.Fatalf("StreamEvents: %v", err)
	}
	st := &stream{events: make(chan anthropic.BetaManagedAgentsStreamSessionEventsUnion, 256), done: make(chan error, 1), s: s}
	go func() {
		for s.Next() {
			st.events <- s.Current()
		}
		st.done <- s.Err()
	}()
	return st
}

// waitFor returns the first event of type typ (and matching ok), failing the
// test on timeout, stream end or a session.error. seen gets every event.
func (st *stream) waitFor(t *testing.T, typ string, timeout time.Duration, seen func(anthropic.BetaManagedAgentsStreamSessionEventsUnion)) anthropic.BetaManagedAgentsStreamSessionEventsUnion {
	t.Helper()
	deadline := time.After(timeout)
	for {
		select {
		case ev := <-st.events:
			if seen != nil {
				seen(ev)
			}
			if ev.Type == "session.error" {
				ext, _ := bmasdk.EventExtensions(ev)
				t.Fatalf("session.error: %s (bma_error_code %q)", ev.RawJSON(), ext.ErrorCode)
			}
			if ev.Type == typ {
				return ev
			}
		case err := <-st.done:
			t.Fatalf("stream ended while waiting for %s: %v", typ, err)
		case <-deadline:
			t.Fatalf("timed out after %s waiting for %s", timeout, typ)
		}
	}
}

// cutTransport ends the body of the first stream connection after cutAfter
// SSE frames with an unexpected EOF, and records the Last-Event-ID of later
// connections.
type cutTransport struct {
	cutAfter int
	mu       sync.Mutex
	conns    int
	resumes  []string
}

func (c *cutTransport) RoundTrip(req *http.Request) (*http.Response, error) {
	res, err := http.DefaultTransport.RoundTrip(req)
	if err != nil || !strings.HasSuffix(req.URL.Path, "/events/stream") {
		return res, err
	}
	c.mu.Lock()
	defer c.mu.Unlock()
	c.conns++
	if c.conns == 1 {
		res.Body = &cutBody{rc: res.Body, frames: c.cutAfter}
	} else {
		c.resumes = append(c.resumes, req.Header.Get("Last-Event-ID"))
	}
	return res, nil
}

type cutBody struct {
	rc     io.ReadCloser
	frames int
	buf    []byte
}

func (b *cutBody) Read(p []byte) (int, error) {
	if b.frames <= 0 {
		return 0, io.ErrUnexpectedEOF
	}
	n, err := b.rc.Read(p)
	b.buf = append(b.buf, p[:n]...)
	for {
		i := bytes.Index(b.buf, []byte("\n\n"))
		if i < 0 {
			break
		}
		if strings.Contains(string(b.buf[:i]), "data:") {
			b.frames--
		}
		b.buf = b.buf[i+2:]
		if b.frames <= 0 {
			// Deliver up to the end of this frame, then fail.
			cut := n - len(b.buf)
			return cut, nil
		}
	}
	return n, err
}

func (b *cutBody) Close() error { return b.rc.Close() }

func textMessage(text string) anthropic.BetaManagedAgentsEventParamsUnion {
	return anthropic.BetaManagedAgentsEventParamsUnion{OfUserMessage: &anthropic.BetaManagedAgentsUserMessageEventParams{
		Content: []anthropic.BetaManagedAgentsUserMessageEventParamsContentUnion{{OfText: &anthropic.BetaManagedAgentsTextBlockParam{Text: text}}},
	}}
}

func TestStaging(t *testing.T) {
	c := stagingClient(t)
	ctx, cancel := context.WithTimeout(context.Background(), 15*time.Minute)
	defer cancel()
	suffix := fmt.Sprintf("sdk-go2-it-%d", time.Now().Unix())

	// Errors: the official error type plus BMA's reason.
	t.Run("error", func(t *testing.T) {
		_, err := c.Beta.Machines.Get(ctx, "mch_doesnotexist0000000000000")
		var apiErr *bmasdk.Error
		if !errors.As(err, &apiErr) {
			t.Fatalf("want *anthropic.Error, got %T %v", err, err)
		}
		if apiErr.StatusCode != http.StatusNotFound || apiErr.Type() != "not_found_error" || apiErr.RequestID == "" {
			t.Fatalf("status %d type %q request_id %q", apiErr.StatusCode, apiErr.Type(), apiErr.RequestID)
		}
		t.Logf("404 not_found_error request_id=%s code=%q", apiErr.RequestID, bmasdk.ErrorCode(err))
	})

	env, err := c.Beta.Environments.New(ctx, anthropic.BetaEnvironmentNewParams{
		Name:   suffix,
		Config: anthropic.BetaEnvironmentNewParamsConfigUnion{OfCloud: &anthropic.BetaCloudConfigParams{}},
	})
	if err != nil {
		t.Fatalf("Environments.New: %v", err)
	}
	t.Cleanup(func() {
		// Delete, not archive: each environment is a machine pool.
		if _, err := c.Beta.Environments.Delete(context.Background(), env.ID, anthropic.BetaEnvironmentDeleteParams{}); err != nil {
			t.Errorf("delete environment %s: %v", env.ID, err)
		}
	})
	if _, err := bmasdk.EnvironmentExtensions(env); err != nil {
		t.Fatalf("EnvironmentExtensions: %v", err)
	}
	t.Logf("environment %s", env.ID)

	agent, err := c.Beta.Agents.New(ctx, anthropic.BetaAgentNewParams{
		Name:   suffix,
		Model:  anthropic.BetaManagedAgentsModelConfigParams{ID: stagingModel},
		System: anthropic.String("You are a test agent. Follow the user's instructions exactly and keep answers to one sentence."),
		Tools: []anthropic.BetaAgentNewParamsToolUnion{
			{OfAgentToolset20260401: &anthropic.BetaManagedAgentsAgentToolset20260401Params{}},
			{OfCustom: &anthropic.BetaManagedAgentsCustomToolParams{
				Name:        "get_weather",
				Description: "Returns the current weather of a city.",
				InputSchema: anthropic.BetaManagedAgentsCustomToolInputSchemaParam{
					Properties: map[string]any{"city": map[string]any{"type": "string"}},
					Required:   []string{"city"},
				},
			}},
		},
	}, bmasdk.WithIdempotencyKey(suffix+"-agent"))
	if err != nil {
		t.Fatalf("Agents.New: %v", err)
	}
	t.Cleanup(func() {
		if _, err := c.Beta.Agents.Archive(context.Background(), agent.ID, anthropic.BetaAgentArchiveParams{}); err != nil {
			t.Logf("archive agent %s: %v", agent.ID, err)
		}
	})
	if _, err := bmasdk.AgentExtensions(agent); err != nil {
		t.Fatalf("AgentExtensions: %v", err)
	}
	t.Logf("agent %s", agent.ID)

	session, err := c.Beta.Sessions.New(ctx, anthropic.BetaSessionNewParams{
		Agent:         anthropic.BetaSessionNewParamsAgentUnion{OfString: anthropic.String(agent.ID)},
		EnvironmentID: env.ID,
		Title:         anthropic.String(suffix),
	}, bmasdk.WithIdempotencyKey(suffix+"-session"))
	if err != nil {
		t.Fatalf("Sessions.New: %v", err)
	}
	t.Cleanup(func() {
		if _, err := c.Beta.Sessions.Archive(context.Background(), session.ID, anthropic.BetaSessionArchiveParams{}); err != nil {
			t.Logf("archive session %s: %v", session.ID, err)
		}
	})
	sessionExt, err := bmasdk.SessionExtensions(session)
	if err != nil {
		t.Fatalf("SessionExtensions: %v", err)
	}
	t.Logf("session %s status %s model_override=%v", session.ID, session.Status, sessionExt.ModelOverride != nil)

	// Message, custom tool round trip and stream resumption: the first
	// connection is cut after a few frames; StreamEvents must reconnect with
	// Last-Event-ID and lose nothing.
	t.Run("custom_tool_and_resume", func(t *testing.T) {
		cut := &cutTransport{cutAfter: 3}
		st := openStream(ctx, t, c, session.ID, option.WithHTTPClient(&http.Client{Transport: cut}))
		defer st.s.Close()
		var got []string // event ids of the frames that carry one
		var firstSeq, lastSeq int64
		streamed := map[string]bool{}
		record := func(ev anthropic.BetaManagedAgentsStreamSessionEventsUnion) {
			ext, err := bmasdk.EventExtensions(ev)
			if err != nil {
				t.Fatalf("EventExtensions: %v", err)
			}
			t.Logf("frame %s bma_sequence=%d id=%s", ev.Type, ext.Sequence, ev.ID)
			if ext.Sequence == 0 {
				if ev.ID != "" {
					if streamed[ev.ID] {
						t.Fatalf("event %s returned twice", ev.ID)
					}
					streamed[ev.ID] = true
					got = append(got, ev.ID)
				}
				return
			}
			if ext.Sequence < lastSeq || streamed[ev.ID] {
				t.Fatalf("event %s (sequence %d after %d): duplicate or out of order", ev.ID, ext.Sequence, lastSeq)
			}
			if firstSeq == 0 {
				firstSeq = ext.Sequence
			}
			lastSeq = ext.Sequence
			streamed[ev.ID] = true
			got = append(got, ev.ID)
		}
		if _, err := c.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
			Events: []anthropic.BetaManagedAgentsEventParamsUnion{textMessage("Call the get_weather tool for the city Paris. After you get the result, reply with one sentence that repeats it.")},
		}); err != nil {
			t.Fatalf("Events.Send: %v", err)
		}
		use := st.waitFor(t, "agent.custom_tool_use", 4*time.Minute, record)
		if use.Name != "get_weather" {
			t.Fatalf("custom tool %q", use.Name)
		}
		t.Logf("agent.custom_tool_use %s input=%v", use.ID, use.Input)
		if _, err := c.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
			Events: []anthropic.BetaManagedAgentsEventParamsUnion{{OfUserCustomToolResult: &anthropic.BetaManagedAgentsUserCustomToolResultEventParams{
				CustomToolUseID: use.ID,
				Content: []anthropic.BetaManagedAgentsUserCustomToolResultEventParamsContentUnion{
					{OfText: &anthropic.BetaManagedAgentsTextBlockParam{Text: "Sunny, 21 degrees Celsius."}},
				},
			}}},
		}); err != nil {
			t.Fatalf("send custom tool result: %v", err)
		}
		st.waitFor(t, "agent.message", 4*time.Minute, record)
		st.waitFor(t, "session.status_idle", 2*time.Minute, record)

		cut.mu.Lock()
		conns, resumes := cut.conns, append([]string(nil), cut.resumes...)
		cut.mu.Unlock()
		if conns < 2 || len(resumes) == 0 {
			t.Fatalf("stream was not resumed: connections %d, Last-Event-ID %v", conns, resumes)
		}
		// Every persisted event from the first streamed one on must have
		// arrived exactly once.
		var listed []string
		pager := c.Beta.Sessions.Events.ListAutoPaging(ctx, session.ID, anthropic.BetaSessionEventListParams{})
		for pager.Next() {
			ext, err := bmasdk.EventExtensions(pager.Current())
			if err != nil {
				t.Fatal(err)
			}
			if ext.Sequence >= firstSeq && ext.Sequence <= lastSeq && (ext.Sequence > firstSeq || streamed[pager.Current().ID]) {
				listed = append(listed, pager.Current().ID)
			}
		}
		if err := pager.Err(); err != nil {
			t.Fatalf("Events.ListAutoPaging: %v", err)
		}
		cut.mu.Lock()
		t.Logf("connections=%d Last-Event-ID=%v", cut.conns, cut.resumes)
		cut.mu.Unlock()
		// Known server gap: a stream resumed with Last-Event-ID replays the
		// durable events but not the session.status_* events the list
		// derives for them (sesst_ ids, e.g. the idle of requires_action), so
		// those are compared only when they were streamed.
		var missing []string
		for _, id := range listed {
			if !streamed[id] {
				missing = append(missing, id)
			}
		}
		listedSet := map[string]bool{}
		for _, id := range listed {
			listedSet[id] = true
		}
		for _, id := range got {
			if !listedSet[id] {
				t.Fatalf("streamed event %s is not in the list", id)
			}
		}
		for _, id := range missing {
			if !strings.HasPrefix(id, "sesst_") {
				t.Fatalf("event %s was not streamed (streamed %v, listed %v)", id, got, listed)
			}
		}
		if len(missing) > 0 {
			t.Logf("server replay omitted derived status events %v", missing)
		}
		t.Logf("resumed after cut: connections=%d Last-Event-ID=%v; %d durable events (sequences %d..%d) streamed once each and found in the list", conns, resumes, len(got), firstSeq, lastSeq)
	})

	t.Run("interrupt", func(t *testing.T) {
		st := openStream(ctx, t, c, session.ID)
		defer st.s.Close()
		if _, err := c.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
			Events: []anthropic.BetaManagedAgentsEventParamsUnion{textMessage("Use the bash tool to run exactly: sleep 120 && echo finished")},
		}); err != nil {
			t.Fatalf("Events.Send: %v", err)
		}
		st.waitFor(t, "agent.tool_use", 4*time.Minute, nil)
		start := time.Now()
		if _, err := c.Beta.Sessions.Events.Send(ctx, session.ID, anthropic.BetaSessionEventSendParams{
			Events: []anthropic.BetaManagedAgentsEventParamsUnion{{OfUserInterrupt: &anthropic.BetaManagedAgentsUserInterruptEventParams{}}},
		}); err != nil {
			t.Fatalf("send interrupt: %v", err)
		}
		idle := st.waitFor(t, "session.status_idle", 90*time.Second, nil)
		t.Logf("interrupted: session.status_idle after %s (stop_reason %s)", time.Since(start).Round(time.Millisecond), idle.StopReason.Type)
	})

	t.Run("files", func(t *testing.T) {
		content := "hello from bma-sdk go 2.0 " + suffix
		meta, err := c.Beta.Files.Upload(ctx, anthropic.BetaFileUploadParams{
			File: anthropic.File(strings.NewReader(content), suffix+".txt", "text/plain"),
		})
		if err != nil {
			t.Fatalf("Files.Upload: %v", err)
		}
		defer func() {
			if _, err := c.Beta.Files.Delete(context.Background(), meta.ID, anthropic.BetaFileDeleteParams{}); err != nil {
				t.Errorf("Files.Delete: %v", err)
			}
		}()
		got, err := c.Beta.Files.GetMetadata(ctx, meta.ID, anthropic.BetaFileGetMetadataParams{})
		if err != nil || got.Filename != suffix+".txt" {
			t.Fatalf("Files.GetMetadata: %v %+v", err, got)
		}
		res, err := c.Beta.Files.Download(ctx, meta.ID, anthropic.BetaFileDownloadParams{})
		if err != nil {
			t.Fatalf("Files.Download: %v", err)
		}
		body, _ := io.ReadAll(res.Body)
		res.Body.Close()
		if string(body) != content {
			t.Fatalf("downloaded %q", body)
		}
		resource, err := c.Beta.Sessions.Resources.Add(ctx, session.ID, anthropic.BetaSessionResourceAddParams{
			BetaManagedAgentsFileResourceParams: anthropic.BetaManagedAgentsFileResourceParams{FileID: meta.ID},
		})
		if err != nil {
			t.Fatalf("Sessions.Resources.Add: %v", err)
		}
		if _, err := c.Beta.Sessions.Resources.Delete(ctx, resource.ID, anthropic.BetaSessionResourceDeleteParams{SessionID: session.ID}); err != nil {
			t.Fatalf("Sessions.Resources.Delete: %v", err)
		}
		t.Logf("file %s uploaded, read back, mounted as %s and unmounted", meta.ID, resource.ID)
	})

	t.Run("organization_and_pools", func(t *testing.T) {
		projects, err := c.Beta.Organization.Projects.List(ctx, os.Getenv("BMA_ORG_ID"), bmasdk.OrganizationProjectListParams{})
		if err != nil {
			t.Fatalf("Organization.Projects.List: %v", err)
		}
		pools, err := c.Beta.MachinePools.List(ctx, bmasdk.MachinePoolListParams{})
		if err != nil {
			t.Fatalf("MachinePools.List: %v", err)
		}
		t.Logf("projects page %d, machine pools page %d", len(projects.Data), len(pools.Data))
	})

	t.Run("machines_terminal_desktop", func(t *testing.T) {
		var online []bmasdk.Machine
		pager := c.Beta.Machines.ListAutoPaging(ctx, bmasdk.MachineListParams{Limit: bmasdk.Ptr[int64](20)})
		for pager.Next() {
			m := pager.Current()
			if m.ConnectionState != nil && *m.ConnectionState == "online" {
				online = append(online, m)
			}
		}
		if err := pager.Err(); err != nil {
			t.Fatalf("Machines.ListAutoPaging: %v", err)
		}
		if len(online) == 0 {
			t.Skip("no online machine in the project")
		}
		m, err := c.Beta.Machines.Get(ctx, online[0].ID)
		if err != nil {
			t.Fatalf("Machines.Get: %v", err)
		}
		t.Logf("machine %s online (%d online of the listed)", m.ID, len(online))

		term, err := c.Beta.TerminalSessions.New(ctx, bmasdk.TerminalSessionNewParams{MachineID: m.ID})
		if err != nil {
			t.Fatalf("TerminalSessions.New: %v", err)
		}
		ticket, err := c.Beta.TerminalSessions.Tickets.New(ctx, term.ID, bmasdk.TerminalSessionTicketNewParams{})
		if err != nil {
			t.Fatalf("TerminalSessions.Tickets.New: %v", err)
		}
		if ticket.Ticket == "" || ticket.WsURL == "" || ticket.Purpose != "connect" {
			t.Fatalf("terminal ticket purpose %q ws_url %q empty ticket %v", ticket.Purpose, ticket.WsURL, ticket.Ticket == "")
		}
		closed, err := c.Beta.TerminalSessions.Close(ctx, term.ID)
		if err != nil {
			t.Fatalf("TerminalSessions.Close: %v", err)
		}
		t.Logf("terminal %s: ticket purpose=%s ws_url=%s; closed state=%s", term.ID, ticket.Purpose, ticket.WsURL, closed.State)

		var desk *bmasdk.DesktopSession
		var desktopMachine string
		var refusals []string
		for _, cand := range online {
			d, err := c.Beta.DesktopSessions.New(ctx, bmasdk.DesktopSessionNewParams{MachineID: cand.ID, ReadOnly: bmasdk.Ptr(true)})
			if err == nil {
				desk, desktopMachine = d, cand.ID
				break
			}
			refusals = append(refusals, fmt.Sprintf("%s: %s", cand.ID, bmasdk.ErrorCode(err)))
		}
		if desk == nil {
			t.Skipf("no online machine provides a desktop (%v)", refusals)
		}
		dt, err := c.Beta.DesktopSessions.Tickets.New(ctx, desk.ID, bmasdk.DesktopSessionTicketNewParams{})
		if err != nil {
			t.Fatalf("DesktopSessions.Tickets.New: %v", err)
		}
		if dt.Ticket == "" || dt.Purpose != "watch" {
			t.Fatalf("desktop ticket purpose %q empty %v", dt.Purpose, dt.Ticket == "")
		}
		if _, err := c.Beta.DesktopSessions.Get(ctx, desk.ID); err != nil {
			t.Fatalf("DesktopSessions.Get: %v", err)
		}
		if _, err := c.Beta.DesktopSessions.Close(ctx, desk.ID); err != nil {
			t.Fatalf("DesktopSessions.Close: %v", err)
		}
		t.Logf("desktop %s on %s: watch ticket ws_url=%s; closed", desk.ID, desktopMachine, dt.WsURL)
	})
}
