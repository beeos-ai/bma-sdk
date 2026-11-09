from __future__ import annotations

import pytest

from bma_sdk import AsyncBma, BadRequestError, Bma, NotFoundError, StreamNotResumedError, _resume
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


# A queued input's executor frames are written before the caller subscribes:
# POST events appends them to a log and answers with the cursor (None: none);
# the stream replays the log after Last-Event-ID, and with no header it sends
# nothing (a live-only stream opened after the send sees no past frame).
def anchor_handler(cursor=None, drops=0, old=0, send_type="user.message"):
    log = [frame("agent.message", f"old_{i + 1}", i + 1) for i in range(old)]
    streams = [0]

    def handler(r, req, n):
        if req.method == "POST":
            before = len(log)
            log.extend([frame("user.message", "evt_in", before + 1), frame("agent.message", "evt_out", before + 2)])
            event = {"type": send_type, "id": "evt_in", "processed_at": "2026-11-08T00:00:00Z"}
            if send_type == "user.message":
                event["content"] = [{"type": "text", "text": "hi"}]
            if cursor is not None:
                event["bma_resume_cursor"] = cursor
            return r.json(200, {"data": [event]})
        streams[0] += 1
        last = req.headers.get("last-event-id")
        if streams[0] <= drops or last is None:
            return r.sse()  # a drop, or live only: the frames were written before
        r.sse(*log[int(last):])

    return handler


USER_MESSAGE = [{"type": "user.message", "content": [{"type": "text", "text": "hi"}]}]


def first_two(stream):
    got = []
    for event in stream:
        got.append(event.id)  # type: ignore[union-attr]
        if len(got) == 2:
            break
    return got


def test_send_and_stream_keeps_frames_written_before_the_subscribe(serve, monkeypatch):
    s = serve(anchor_handler(cursor=0))
    client = Bma(api_key="k", base_url=s.url, max_retries=0)
    client.beta.sessions.events.send("ses_1", events=USER_MESSAGE)
    monkeypatch.setattr(_resume.CONFIG, "max_reconnects", 1)
    with pytest.raises(StreamNotResumedError):  # a live-only stream after the send gets nothing
        first_two(client.beta.sessions.events.stream("ses_1"))
    monkeypatch.setattr(_resume.CONFIG, "max_reconnects", 5)
    s.seen.clear()

    result = client.beta.sessions.events.send_and_stream("ses_1", events=USER_MESSAGE)
    assert result.replayed is False
    assert result.sent.data[0].id == "evt_in"
    assert first_two(result.stream) == ["evt_in", "evt_out"]
    assert [r.method for r in s.seen] == ["POST", "GET"]
    assert s.seen[1].headers.get("last-event-id") == "0"  # cursor 0 is still sent


def test_send_and_stream_reconnect_keeps_the_cursor(serve):
    s = serve(anchor_handler(cursor=7, drops=2, old=7))
    result = Bma(api_key="k", base_url=s.url, max_retries=0).beta.sessions.events.send_and_stream("ses_1", events=USER_MESSAGE)
    assert first_two(result.stream) == ["evt_in", "evt_out"]
    assert [r.headers.get("last-event-id") for r in s.seen[1:]] == ["7", "7", "7"]


def test_send_and_stream_without_cursor_replays_from_the_start(serve):
    s = serve(anchor_handler())
    result = Bma(api_key="k", base_url=s.url, max_retries=0).beta.sessions.events.send_and_stream("ses_1", events=USER_MESSAGE)
    assert result.replayed is True
    assert first_two(result.stream) == ["evt_in", "evt_out"]
    assert s.seen[1].headers.get("last-event-id") == "0"


def test_send_and_stream_without_user_message_is_live_only(serve):
    s = serve(anchor_handler(send_type="user.interrupt"))
    result = Bma(api_key="k", base_url=s.url, max_retries=0).beta.sessions.events.send_and_stream(
        "ses_1", events=[{"type": "user.interrupt"}]
    )
    assert result.replayed is False
    assert s.seen[1].headers.get("last-event-id") is None
    result.stream.close()


def test_send_and_stream_send_error_opens_no_stream(serve):
    s = serve(lambda r, req, n: r.json(400, {"type": "error", "error": {"type": "invalid_request_error", "message": "bad"}}))
    with pytest.raises(BadRequestError):
        Bma(api_key="k", base_url=s.url, max_retries=0).beta.sessions.events.send_and_stream("ses_1", events=USER_MESSAGE)
    assert len(s.seen) == 1


async def test_async_send_and_stream_keeps_frames_written_before_the_subscribe(serve):
    s = serve(anchor_handler(cursor=3, drops=1, old=3))
    client = AsyncBma(api_key="k", base_url=s.url, max_retries=0)
    result = await client.beta.sessions.events.send_and_stream("ses_1", events=USER_MESSAGE)
    got = []
    async for event in result.stream:
        got.append(event.id)  # type: ignore[union-attr]
        if len(got) == 2:
            break
    assert got == ["evt_in", "evt_out"]
    assert [r.headers.get("last-event-id") for r in s.seen[1:]] == ["3", "3"]
    await client.close()
