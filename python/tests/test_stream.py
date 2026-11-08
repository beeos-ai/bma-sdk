from __future__ import annotations

import pytest

from bma_sdk import AsyncBma, Bma, NotFoundError, StreamNotResumedError
from conftest import frame


def handler_for(frames_by_connection):
    def handler(r, req, n):
        frames = frames_by_connection(n)
        if frames is None:
            r.json(404, {"type": "error", "error": {"type": "not_found_error", "message": "gone"}})
        else:
            r.sse(*frames)

    return handler


def script(n):
    if n == 1:  # two events of sequence 1, an announcement, then the connection ends
        return [frame("session.status_running", "sesst_1_run", 1), frame("user.message", "evt_1", 1), frame("session.status_idle", "sesst_x", 0)]
    if n == 2:  # the server resumes after sequence 0: replays sequence 1
        return [frame("session.status_running", "sesst_1_run", 1), frame("user.message", "evt_1", 1), frame("session.status_idle", "sesst_x", 1), frame("agent.message", "evt_2", 2), "event: ping\ndata: {}\n\n"]
    if n == 3:
        return [frame("session.status_idle", "sesst_2_idle", 2)]
    return None


EXPECTED = ["sesst_1_run", "evt_1", "sesst_x", "evt_2", "sesst_2_idle"]


def check_requests(s):
    assert len(s.seen) == 4
    assert [r.headers.get("last-event-id") for r in s.seen[:3]] == [None, "0", "1"]
    assert s.seen[0].headers["anthropic-beta"] == "managed-agents-2026-04-01"
    assert s.seen[0].path == "/v1/sessions/ses_1/events/stream"


def test_resumes_with_last_event_id_and_returns_every_event_once(serve):
    s = serve(handler_for(script))
    stream = Bma(api_key="k", base_url=s.url, max_retries=0).beta.sessions.events.stream("ses_1")
    got: list[str] = []
    with pytest.raises(NotFoundError):
        for event in stream:
            got.append(event.id)  # type: ignore[union-attr]
    assert got == EXPECTED
    check_requests(s)


async def test_async_resumes_with_last_event_id(serve):
    s = serve(handler_for(script))
    client = AsyncBma(api_key="k", base_url=s.url, max_retries=0)
    stream = await client.beta.sessions.events.stream("ses_1")
    got: list[str] = []
    with pytest.raises(NotFoundError):
        async for event in stream:
            got.append(event.id)  # type: ignore[union-attr]
    assert got == EXPECTED
    check_requests(s)
    await client.close()


def test_gives_up_after_max_reconnects(serve):
    s = serve(lambda r, req, n: r.sse())
    stream = Bma(api_key="k", base_url=s.url, max_retries=0).beta.sessions.events.stream("ses_1")
    with pytest.raises(StreamNotResumedError, match="not resumed after 5 attempts"):
        list(stream)
    assert len(s.seen) == 1 + 5


async def test_async_gives_up_after_max_reconnects(serve):
    s = serve(lambda r, req, n: r.sse())
    client = AsyncBma(api_key="k", base_url=s.url, max_retries=0)
    stream = await client.beta.sessions.events.stream("ses_1")
    with pytest.raises(StreamNotResumedError):
        async for _ in stream:
            pass
    assert len(s.seen) == 1 + 5
    await client.close()


def test_close_stops_the_stream(serve, monkeypatch):
    from bma_sdk import _resume

    monkeypatch.setattr(_resume.CONFIG, "backoff", 60.0)
    s = serve(lambda r, req, n: r.sse(frame("user.message", "evt_1", 1)))
    stream = Bma(api_key="k", base_url=s.url, max_retries=0).beta.sessions.events.stream("ses_1")
    got = []
    for event in stream:
        got.append(event.id)  # type: ignore[union-attr]
        stream.close()
    assert got == ["evt_1"] and len(s.seen) == 1
