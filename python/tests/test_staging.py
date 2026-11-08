"""Live test against a BMA deployment. Runs only with BMA_INTEGRATION=1 and
BMA_API_KEY, BMA_BASE_URL (origin), BMA_PROJECT_ID and BMA_ORG_ID set:

    BMA_INTEGRATION=1 pytest tests/test_staging.py -s

It creates an environment (deleted at the end), an agent and a session
(archived at the end), so it runs against staging, never production.
"""
from __future__ import annotations

import os
import time
from typing import Any, Iterator, Optional

import httpx2
import pytest

import bma_sdk
from bma_sdk import Bma, NotFoundError, error_code

pytestmark = pytest.mark.skipif(os.environ.get("BMA_INTEGRATION") != "1", reason="set BMA_INTEGRATION=1 to run against a BMA deployment")

MODEL = "deepseek-flash"


class CutStream(httpx2.SyncByteStream):
    """A response body that fails after `frames` SSE data frames."""

    def __init__(self, inner: httpx2.SyncByteStream, frames: int) -> None:
        self.inner, self.frames, self.pending = inner, frames, b""

    def __iter__(self) -> Iterator[bytes]:
        for chunk in self.inner:
            self.pending += chunk
            out = b""
            while (i := self.pending.find(b"\n\n")) >= 0 and self.frames > 0:
                frame, self.pending = self.pending[: i + 2], self.pending[i + 2 :]
                out += frame
                if b"data:" in frame:
                    self.frames -= 1
            if out:
                yield out
            if self.frames <= 0:
                raise httpx2.ReadError("cut by the test")

    def close(self) -> None:
        self.inner.close()


class CuttingTransport(httpx2.HTTPTransport):
    """Cuts the first event-stream connection and records the Last-Event-ID of later ones."""

    def __init__(self, cut_after: int) -> None:
        super().__init__()
        self.cut_after, self.conns, self.resumes = cut_after, 0, []

    def handle_request(self, request: httpx2.Request) -> httpx2.Response:
        res = super().handle_request(request)
        if not request.url.path.endswith("/events/stream"):
            return res
        self.conns += 1
        if self.conns > 1:
            self.resumes.append(request.headers.get("last-event-id", ""))
            return res
        assert isinstance(res.stream, httpx2.SyncByteStream)
        return httpx2.Response(res.status_code, headers=res.headers, stream=CutStream(res.stream, self.cut_after), extensions=res.extensions)


def wait_for(events: Iterator[Any], type: str, timeout: float, seen: Optional[Any] = None) -> Any:
    deadline = time.time() + timeout
    for event in events:
        if seen:
            seen(event)
        if event.type == "session.error":
            raise AssertionError(f"session.error: {event.to_json()} (bma_error_code {bma_sdk.event_extensions(event).error_code})")
        if event.type == type:
            return event
        if time.time() > deadline:
            break
    raise AssertionError(f"timed out or stream ended waiting for {type}")


def text(t: str) -> Any:
    return [{"type": "user.message", "content": [{"type": "text", "text": t}]}]


def test_staging() -> None:
    for k in ("BMA_API_KEY", "BMA_BASE_URL", "BMA_PROJECT_ID", "BMA_ORG_ID"):
        if not os.environ.get(k):
            pytest.fail(f"{k} is not set")
    assert "api.bma.beeos.ai" not in os.environ["BMA_BASE_URL"], "refusing to run the live test against production"
    suffix = f"sdk-py2-it-{int(time.time())}"
    cut = CuttingTransport(3)
    c = Bma(http_client=httpx2.Client(transport=cut, timeout=httpx2.Timeout(600)))
    plain = Bma()

    # error: the official error type plus BMA's reason
    with pytest.raises(NotFoundError) as info:
        c.beta.machines.retrieve("mch_doesnotexist0000000000000")
    assert info.value.status_code == 404 and info.value.request_id
    print(f"404 not_found_error request_id={info.value.request_id} code={error_code(info.value)}")

    env = c.beta.environments.create(name=suffix, config={"type": "cloud"})
    session_id = agent_id = None
    try:
        bma_sdk.environment_extensions(env)
        print(f"environment {env.id}")
        agent = c.beta.agents.create(
            name=suffix,
            model={"id": MODEL},
            system="You are a test agent. Follow the user's instructions exactly and keep answers to one sentence.",
            tools=[
                {"type": "agent_toolset_20260401"},
                {
                    "type": "custom",
                    "name": "get_weather",
                    "description": "Returns the current weather of a city.",
                    "input_schema": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]},
                },
            ],
            extra_headers={"Idempotency-Key": f"{suffix}-agent"},
        )
        agent_id = agent.id
        bma_sdk.agent_extensions(agent)
        print(f"agent {agent.id}")
        session = c.beta.sessions.create(agent=agent.id, environment_id=env.id, title=suffix, extra_headers={"Idempotency-Key": f"{suffix}-session"})
        session_id = session.id
        ext = bma_sdk.session_extensions(session)
        print(f"session {session.id} status {session.status} model_override={ext.model_override is not None}")

        # custom tool round trip and stream resumption: the first connection is
        # cut after a few frames; stream() must reconnect and lose nothing.
        stream = c.beta.sessions.events.stream(session.id)
        got: list[str] = []
        streamed: set[str] = set()
        seqs: list[int] = []

        def record(ev: Any) -> None:
            seq = bma_sdk.event_extensions(ev).sequence or 0
            print(f"frame {ev.type} bma_sequence={seq} id={getattr(ev, 'id', None)}")
            if seq == 0:
                if getattr(ev, "id", None):
                    assert ev.id not in streamed, f"event {ev.id} returned twice"
                    streamed.add(ev.id)
                    got.append(ev.id)
                return
            assert (not seqs or seq >= seqs[-1]) and ev.id not in streamed, f"event {ev.id} duplicate or out of order"
            seqs.append(seq)
            streamed.add(ev.id)
            got.append(ev.id)

        with stream:
            events = iter(stream)
            c.beta.sessions.events.send(session.id, events=text("Call the get_weather tool for the city Paris. After you get the result, reply with one sentence that repeats it."))
            use = wait_for(events, "agent.custom_tool_use", 240, record)
            assert use.name == "get_weather"
            print(f"agent.custom_tool_use {use.id} input={use.input}")
            c.beta.sessions.events.send(
                session.id,
                events=[{"type": "user.custom_tool_result", "custom_tool_use_id": use.id, "content": [{"type": "text", "text": "Sunny, 21 degrees Celsius."}]}],
            )
            wait_for(events, "agent.message", 240, record)
            wait_for(events, "session.status_idle", 120, record)
        assert cut.conns >= 2 and cut.resumes, f"stream was not resumed: connections {cut.conns}, Last-Event-ID {cut.resumes}"
        first, last = seqs[0], seqs[-1]
        listed = [
            ev.id
            for ev in c.beta.sessions.events.list(session.id)
            if first <= (bma_sdk.event_extensions(ev).sequence or 0) <= last and ((bma_sdk.event_extensions(ev).sequence or 0) > first or ev.id in streamed)
        ]
        for ident in got:
            assert ident in listed, f"streamed event {ident} is not in the list"
        # Known server gap: a resumed stream replays durable events but not the
        # derived session.status_* events (sesst_ ids) of the list.
        missing = [i for i in listed if i not in streamed]
        assert all(i.startswith("sesst_") for i in missing), f"events not streamed: {missing}"
        print(f"resumed after cut: connections={cut.conns} Last-Event-ID={cut.resumes}; {len(got)} durable events (sequences {first}..{last}) streamed once each; omitted derived {missing}")

        # interrupt
        with plain.beta.sessions.events.stream(session.id) as s2:
            events = iter(s2)
            plain.beta.sessions.events.send(session.id, events=text("Use the bash tool to run exactly: sleep 120 && echo finished"))
            wait_for(events, "agent.tool_use", 240)
            start = time.time()
            plain.beta.sessions.events.send(session.id, events=[{"type": "user.interrupt"}])
            idle = wait_for(events, "session.status_idle", 90)
            print(f"interrupted: session.status_idle after {int((time.time() - start) * 1000)}ms (stop_reason {idle.stop_reason.type})")

        # files
        content = f"hello from bma-sdk py 2.0 {suffix}"
        meta = c.beta.files.upload(file=(f"{suffix}.txt", content.encode(), "text/plain"))
        try:
            assert c.beta.files.retrieve_metadata(meta.id).filename == f"{suffix}.txt"
            assert c.beta.files.download(meta.id).read().decode() == content
            resource = c.beta.sessions.resources.add(session.id, type="file", file_id=meta.id)
            c.beta.sessions.resources.delete(resource.id, session_id=session.id)
            print(f"file {meta.id} uploaded, read back, mounted as {resource.id} and unmounted")
        finally:
            c.beta.files.delete(meta.id)

        # organization and pools
        projects = c.beta.organization.projects.list(os.environ["BMA_ORG_ID"])
        pools = c.beta.machine_pools.list()
        print(f"projects page {len(projects.data)}, machine pools page {len(pools.data)}")

        # machines, terminal and desktop
        online = [m for m in c.beta.machines.list(limit=20) if getattr(m, "connection_state", None) == "online"]
        if not online:
            print("no online machine in the project")
            return
        m = c.beta.machines.retrieve(online[0].id)
        print(f"machine {m.id} online ({len(online)} online of the listed)")
        term = c.beta.terminal_sessions.create(machine_id=m.id)
        ticket = c.beta.terminal_sessions.tickets.create(term.id)
        assert ticket.ticket and ticket.ws_url and ticket.purpose == "connect", f"terminal ticket purpose {ticket.purpose}"
        closed = c.beta.terminal_sessions.close(term.id)
        print(f"terminal {term.id}: ticket purpose={ticket.purpose} ws_url={ticket.ws_url}; closed state={closed.state}")
        no_retry = c.with_options(max_retries=0)
        desk = None
        refusals: list[str] = []
        for cand in online:
            try:
                desk = no_retry.beta.desktop_sessions.create(machine_id=cand.id, read_only=True)
                break
            except bma_sdk.APIStatusError as err:
                refusals.append(f"{cand.id}: {error_code(err)}")
        if desk is None:
            print(f"no online machine provides a desktop ({refusals})")
            return
        dt = c.beta.desktop_sessions.tickets.create(desk.id)
        assert dt.ticket and dt.purpose == "watch"
        c.beta.desktop_sessions.retrieve(desk.id)
        c.beta.desktop_sessions.close(desk.id)
        print(f"desktop {desk.id}: watch ticket ws_url={dt.ws_url}; closed")
    finally:
        # Delete, not archive: each environment is a machine pool.
        for what, fn in (
            ("session", lambda: session_id and c.beta.sessions.archive(session_id)),
            ("agent", lambda: agent_id and c.beta.agents.archive(agent_id)),
            ("environment", lambda: c.beta.environments.delete(env.id)),
        ):
            try:
                fn()
            except Exception as err:  # noqa: BLE001
                print(f"cleanup {what}: {err}")
