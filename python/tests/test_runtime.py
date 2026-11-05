"""Runtime behaviour of the resource client: scope defaults, request shape,
retries and idempotency keys (ADR 0012 D3), errors, pagination and the event
stream. Mirrors typescript/test/runtime.test.ts with an httpx MockTransport;
test_contract.py replays the recorded contract fixtures over HTTP.
"""

from __future__ import annotations

import io
import json
from collections.abc import Callable
from typing import Any, Union

import httpx
import pytest

from bma_sdk import (
    APIConnectionError,
    APIConnectionTimeoutError,
    AsyncBma,
    AuthenticationError,
    Bma,
    BmaApiError,
    BmaError,
    ConflictError,
    EventStreamError,
    InternalServerError,
    NotFoundError,
    RateLimitError,
    ServiceUnavailableError,
)
from bma_sdk.types import AgentStreamEvent

BASE = "https://bma.test/api/v1"
ORG = "org_aaaaaaaaaaaaaaaaaaaaaaaaaa"
PROJECT = "prj_aaaaaaaaaaaaaaaaaaaaaaaaaa"
AGENT = "agt_aaaaaaaaaaaaaaaaaaaaaaaaaa"
SESSION = "ses_aaaaaaaaaaaaaaaaaaaaaaaaaa"

Reply = Union[httpx.Response, Exception, Callable[[httpx.Request], Union[httpx.Response, Exception]]]


class Stub:
    def __init__(self, replies: list[Reply]) -> None:
        self.replies = list(replies)
        self.calls: list[httpx.Request] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        request.read()
        self.calls.append(request)
        if not self.replies:
            raise AssertionError(f"unexpected request {request.method} {request.url}")
        reply = self.replies.pop(0)
        if callable(reply) and not isinstance(reply, (httpx.Response, Exception)):
            reply = reply(request)
        if isinstance(reply, Exception):
            raise reply
        return reply


@pytest.fixture(autouse=True)
def no_backoff(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("bma_sdk._core._backoff", lambda retry: 0.0)


def take(iterable: Any, n: int) -> list[Any]:
    out: list[Any] = []
    for item in iterable:
        out.append(item)
        if len(out) == n:
            break
    return out


def client(replies: list[Reply], **extra: Any) -> tuple[Bma, Stub]:
    stub = Stub(replies)
    options: dict[str, Any] = {"org_id": ORG, "project_id": PROJECT, **extra}
    bma = Bma(token="t", base_url=BASE, http_client=httpx.Client(transport=httpx.MockTransport(stub)), **options)
    return bma, stub


def reply_json(status: int, body: Any, headers: dict[str, str] | None = None) -> httpx.Response:
    return httpx.Response(status, json=body, headers=headers)


def api_error(status: int, code: str, headers: dict[str, str] | None = None) -> httpx.Response:
    return reply_json(status, {"error": f"{code} happened", "code": code}, headers)


def refused() -> Exception:
    return httpx.ConnectError("connection refused")


def reset() -> Exception:
    return httpx.ReadError("connection reset")


def test_scope_defaults_fill_the_path_and_params_override_them() -> None:
    bma, stub = client([reply_json(200, {"agent": {}}), reply_json(200, {"agent": {}})])
    bma.agents.retrieve(AGENT)
    bma.agents.retrieve(AGENT, project_id="prj_bbbbbbbbbbbbbbbbbbbbbbbbbb")
    assert stub.calls[0].url.path == f"/api/v1/orgs/{ORG}/projects/{PROJECT}/agents/{AGENT}"
    assert stub.calls[1].url.path == f"/api/v1/orgs/{ORG}/projects/prj_bbbbbbbbbbbbbbbbbbbbbbbbbb/agents/{AGENT}"
    assert stub.calls[0].headers["authorization"] == "Bearer t"


def test_missing_scope_is_a_client_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("BMA_ORG_ID", raising=False)
    monkeypatch.delenv("BMA_PROJECT_ID", raising=False)
    bma, stub = client([], org_id=None, project_id=None)
    with pytest.raises(BmaError, match="org_id"):
        bma.agents.list()
    assert stub.calls == []


def test_scope_defaults_come_from_the_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BMA_ORG_ID", ORG)
    monkeypatch.setenv("BMA_PROJECT_ID", PROJECT)
    stub = Stub([reply_json(200, {"data": [], "next_cursor": None})])
    bma = Bma(token="t", base_url=BASE, http_client=httpx.Client(transport=httpx.MockTransport(stub)))
    bma.agents.list()
    assert stub.calls[0].url.path == f"/api/v1/orgs/{ORG}/projects/{PROJECT}/agents"


def test_params_split_into_query_header_and_json_body() -> None:
    bma, stub = client([reply_json(201, {"agent_input": {}})])
    bma.agents.inputs.create(
        AGENT,
        session_id=SESSION,
        content_blocks=[{"type": "text", "text": "hi"}],
        delivery_mode="queued",
        idempotency_key="input-1",
    )
    c = stub.calls[0]
    assert c.method == "POST"
    assert c.url.params["session_id"] == SESSION
    assert c.headers["idempotency-key"] == "input-1"
    assert c.headers["content-type"] == "application/json"
    assert json.loads(c.content) == {"content_blocks": [{"type": "text", "text": "hi"}], "delivery_mode": "queued"}


def test_array_and_deep_object_query_parameters() -> None:
    bma, stub = client([reply_json(200, {}), reply_json(200, {"data": [], "next_cursor": None})])
    bma.orgs.usage(include_project_ids=[PROJECT, "prj_bbbbbbbbbbbbbbbbbbbbbbbbbb"])
    bma.orgs.secrets.list(metadata={"team": "a", "env": "b"})
    assert stub.calls[0].url.params.get_list("include_project_ids") == [PROJECT, "prj_bbbbbbbbbbbbbbbbbbbbbbbbbb"]
    assert stub.calls[1].url.params["metadata[team]"] == "a"
    assert stub.calls[1].url.params["metadata[env]"] == "b"


def test_binary_upload_and_download() -> None:
    bma, stub = client([reply_json(201, {"id": "file_1"}), httpx.Response(200, content=b"bytes")])
    bma.files.upload(filename="a.txt", body=b"hello", file_metadata='{"k":"v"}', idempotency_key="u-1")
    assert stub.calls[0].headers["content-type"] == "application/octet-stream"
    assert stub.calls[0].headers["x-bma-file-metadata"] == '{"k":"v"}'
    assert stub.calls[0].content == b"hello"
    assert bma.files.download("file_1").content == b"bytes"


def test_multipart_bodies() -> None:
    bma, stub = client([reply_json(201, {"id": "skl_1"})])
    bma.orgs.skills.create(owner={"kind": "org"}, archive=("skill.zip", b"zip"))
    body = stub.calls[0].content
    assert stub.calls[0].headers["content-type"].startswith("multipart/form-data; boundary=")
    assert b'name="owner"\r\nContent-Type: application/json\r\n\r\n{"kind": "org"}' in body
    assert b'name="archive"; filename="skill.zip"' in body


def test_204_returns_none() -> None:
    bma, _ = client([httpx.Response(204)])
    assert bma.agents.machines.delete(AGENT, "mch_1") is None


@pytest.mark.parametrize(
    "status,code,cls",
    [(401, "unauthorized", AuthenticationError), (404, "not_found", NotFoundError), (409, "state_transition_conflict", ConflictError)],
)
def test_errors_map_to_status_subclasses(status: int, code: str, cls: type[BmaApiError]) -> None:
    bma, _ = client([api_error(status, code)])
    with pytest.raises(cls) as excinfo:
        bma.agents.retrieve(AGENT)
    assert isinstance(excinfo.value, BmaApiError)
    assert excinfo.value.status == status
    assert excinfo.value.code == code


def test_get_retries_5xx_and_connection_errors() -> None:
    bma, stub = client([api_error(500, "internal_error", {"retry-after-ms": "1"}), reset(), reply_json(200, {"agent": {}})])
    bma.agents.retrieve(AGENT)
    assert len(stub.calls) == 3


def test_max_retries_bounds_the_attempts() -> None:
    bma, stub = client(
        [
            api_error(503, "service_unavailable", {"retry-after-ms": "1"}),
            api_error(503, "service_unavailable", {"retry-after-ms": "1"}),
        ],
        max_retries=1,
    )
    with pytest.raises(ServiceUnavailableError):
        bma.agents.retrieve(AGENT)
    assert len(stub.calls) == 2


def test_with_options_overrides_max_retries() -> None:
    bma, stub = client([api_error(503, "service_unavailable", {"retry-after-ms": "1"})])
    with pytest.raises(ServiceUnavailableError):
        bma.with_options(max_retries=0).agents.retrieve(AGENT)
    assert len(stub.calls) == 1


def test_409_is_never_retried() -> None:
    bma, stub = client([api_error(409, "idempotency_key_conflict")])
    with pytest.raises(ConflictError):
        bma.agents.create(name="a")
    assert len(stub.calls) == 1


def test_idempotent_writes_reuse_one_generated_key() -> None:
    bma, stub = client([api_error(500, "internal_error", {"retry-after-ms": "1"}), reset(), reply_json(201, {"agent": {}})])
    bma.agents.create(name="a")
    keys = [c.headers["idempotency-key"] for c in stub.calls]
    assert len(keys) == 3
    assert keys[0].startswith("bma-sdk-retry-") and len(keys[0]) == len("bma-sdk-retry-") + 36
    assert keys == [keys[0]] * 3


def test_writes_without_idempotency_key_retry_only_undelivered_429_503() -> None:
    a, sa = client([api_error(500, "internal_error")])
    with pytest.raises(InternalServerError):
        a.agents.sessions.create(AGENT)
    assert len(sa.calls) == 1

    b, sb = client([reset()])
    with pytest.raises(APIConnectionError):
        b.agents.sessions.create(AGENT)
    assert len(sb.calls) == 1

    c, sc = client([refused(), api_error(429, "rate_limited", {"retry-after-ms": "1"}), reply_json(201, {"session": {"id": SESSION}})])
    assert c.agents.sessions.create(AGENT).session.id == SESSION
    assert len(sc.calls) == 3

    d, sd = client([api_error(429, "rate_limited", {"retry-after-ms": "1"})], max_retries=0)
    with pytest.raises(RateLimitError):
        d.agents.sessions.create(AGENT)
    assert len(sd.calls) == 1


def test_timeout() -> None:
    bma, _ = client([httpx.ReadTimeout("slow")], max_retries=0)
    with pytest.raises(APIConnectionTimeoutError):
        bma.agents.retrieve(AGENT)


def test_cursor_pages() -> None:
    def page(ids: list[str], nxt: str | None) -> httpx.Response:
        return reply_json(200, {"data": [{"id": i} for i in ids], "next_cursor": nxt})

    bma, stub = client([page(["a", "b"], "c1"), page(["a", "b"], "c1"), page(["c"], None)])
    first = bma.agents.list(limit=2)
    assert [a.id for a in first.data] == ["a", "b"]
    assert first.has_next_page()
    assert [a.id for a in bma.agents.list(limit=2)] == ["a", "b", "c"]
    assert stub.calls[2].url.params["cursor"] == "c1"
    assert stub.calls[2].url.params["limit"] == "2"


def sse(frames: list[dict[str, Any]], status: int = 200) -> httpx.Response:
    body = "".join(
        f": keep-alive\n\nevent: {f['event']}\n" + (f"id: {f['id']}\n" if "id" in f else "") + f"data: {json.dumps(f['data'])}\n\n"
        for f in frames
    )
    return httpx.Response(status, content=body.encode(), headers={"content-type": "text/event-stream"})


def test_event_stream_reconnects_with_last_event_id() -> None:
    bma, stub = client(
        [
            sse(
                [
                    {"event": "agent_input", "id": "5", "data": {"sequence": 5, "event_kind": "agent_input"}},
                    {"event": "tool_call_update", "data": {"tool_call_id": "tc_1", "state": "ready"}},
                    {"event": "error", "data": {"error": "restarting", "code": "service_unavailable"}},
                ]
            ),
            sse([{"event": "model_output", "id": "6", "data": {"sequence": 6, "event_kind": "model_output"}}]),
        ]
    )
    seen: list[AgentStreamEvent] = take(bma.agents.events.stream(AGENT, session_id=SESSION, after_sequence=2), 3)
    got: list[tuple[str, int | None]] = []
    for ev in seen:
        if ev.event == "tool_call_update":
            assert ev.data.tool_call_id == "tc_1"
            got.append((ev.event, None))
        elif ev.event in ("agent_input", "model_output"):
            got.append((ev.event, ev.sequence))
    assert got == [("agent_input", 5), ("tool_call_update", None), ("model_output", 6)]
    assert stub.calls[0].headers["accept"] == "text/event-stream"
    assert stub.calls[0].url.params["after_sequence"] == "2"
    assert stub.calls[1].headers["last-event-id"] == "5"
    assert stub.calls[1].url.params["session_id"] == SESSION
    assert "after_sequence" not in stub.calls[1].url.params


def test_event_stream_terminal_error_frame() -> None:
    bma, stub = client([sse([{"event": "error", "data": {"error": "gone", "code": "forbidden"}}])])
    with pytest.raises(EventStreamError) as excinfo:
        for _ in bma.agents.events.stream(AGENT):
            pass
    assert excinfo.value.code == "forbidden"
    assert len(stub.calls) == 1


async def test_async_client_pages_and_stream() -> None:
    replies: list[Reply] = [
        reply_json(200, {"data": [{"id": "a"}], "next_cursor": "c1"}),
        reply_json(200, {"data": [{"id": "b"}], "next_cursor": None}),
        sse([{"event": "model_output", "id": "7", "data": {"sequence": 7, "event_kind": "model_output"}}]),
        api_error(404, "not_found"),
    ]
    stub = Stub(replies)

    async def handler(request: httpx.Request) -> httpx.Response:
        return stub(request)

    async with AsyncBma(
        token="t", base_url=BASE, org_id=ORG, project_id=PROJECT,
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    ) as bma:
        assert [a.id async for a in bma.agents.list()] == ["a", "b"]
        async for ev in bma.agents.events.stream(AGENT):
            assert ev.event == "model_output" and ev.sequence == 7
            break
        with pytest.raises(NotFoundError):
            await bma.agents.retrieve(AGENT)


# --- Review typed-sdk-review-1.0: EventSource reconnection, timeouts, pages ---


def raw_sse(text: str) -> httpx.Response:
    return httpx.Response(200, content=text.encode(), headers={"content-type": "text/event-stream"})


def test_event_stream_clean_end_reconnects_with_last_event_id() -> None:
    bma, stub = client([
        raw_sse('event: model_output\nid: 5\ndata: {"sequence":5,"event_kind":"model_output"}\n\n'),
        raw_sse('event: model_output\nid: 6\ndata: {"sequence":6,"event_kind":"model_output"}\n\n'),
    ])
    seen = take(bma.agents.events.stream(AGENT, after_sequence=1), 2)
    assert [ev.sequence for ev in seen] == [5, 6]
    assert stub.calls[1].headers["last-event-id"] == "5"
    assert "after_sequence" not in stub.calls[1].url.params


def test_event_stream_partial_frame_is_discarded_and_reconnects() -> None:
    bma, stub = client([
        raw_sse('event: model_output\nid: 6\ndata: {"sequence":6,"event_kind":"model_output"}\n\nevent: model_output\nid: 7\ndata: {"seq'),
        raw_sse('event: model_output\nid: 7\ndata: {"sequence":7,"event_kind":"model_output"}\n\n'),
    ])
    assert [ev.sequence for ev in take(bma.agents.events.stream(AGENT), 2)] == [6, 7]
    assert stub.calls[1].headers["last-event-id"] == "6"


def test_event_stream_reconnects_without_data_spend_max_retries() -> None:
    bma, stub = client([raw_sse(""), api_error(503, "service_unavailable"), refused()], max_retries=2)
    with pytest.raises(APIConnectionError):
        take(bma.agents.events.stream(AGENT), 1)
    assert len(stub.calls) == 3


def test_event_stream_heartbeat_resets_the_budget() -> None:
    bma, stub = client(
        [raw_sse(": heartbeat\n\n"), raw_sse(": heartbeat\n\n"),
         raw_sse('event: model_output\nid: 9\ndata: {"sequence":9,"event_kind":"model_output"}\n\n')],
        max_retries=1,
    )
    assert len(take(bma.agents.events.stream(AGENT), 1)) == 1
    assert len(stub.calls) == 3


async def test_async_event_stream_clean_end_reconnects() -> None:
    stub = Stub([
        raw_sse('event: model_output\nid: 5\ndata: {"sequence":5,"event_kind":"model_output"}\n\nid: 6\ndata: {"tr'),
        raw_sse('event: model_output\nid: 6\ndata: {"sequence":6,"event_kind":"model_output"}\n\n'),
    ])
    bma = AsyncBma(token="t", base_url=BASE, org_id=ORG, project_id=PROJECT,
                   http_client=httpx.AsyncClient(transport=httpx.MockTransport(stub)))
    seen: list[int] = []
    async for ev in bma.agents.events.stream(AGENT):
        if ev.event == "model_output":
            seen.append(ev.sequence)
        if len(seen) == 2:
            break
    assert seen == [5, 6]
    assert stub.calls[1].headers["last-event-id"] == "5"


def test_timeout_none_disables_and_accepts_httpx_timeout() -> None:
    seen: list[Any] = []

    def capture(request: httpx.Request) -> httpx.Response:
        seen.append(request.extensions["timeout"])
        return reply_json(200, {"agent": {}})

    bma, _ = client([capture, capture, capture], timeout=None)
    bma.agents.retrieve(AGENT)
    bma.agents.retrieve(AGENT, timeout=httpx.Timeout(5.0, connect=1.0))
    bma.with_options(timeout=7.0).agents.retrieve(AGENT)
    assert seen[0] == {"connect": None, "read": None, "write": None, "pool": None}
    assert seen[1] == {"connect": 1.0, "read": 5.0, "write": 5.0, "pool": 5.0}
    assert seen[2]["read"] == 7.0


def test_seekable_upload_body_is_replayed_on_retry() -> None:
    sizes: list[tuple[int, str | None]] = []

    def record(status: int) -> Callable[[httpx.Request], httpx.Response]:
        def handler(request: httpx.Request) -> httpx.Response:
            sizes.append((len(request.content), request.headers.get("idempotency-key")))
            return api_error(503, "service_unavailable") if status == 503 else reply_json(201, {"id": "file_1"})
        return handler

    bma, _ = client([record(503), record(201)])
    body = io.BytesIO(b"pre" + b"x" * 100000)
    body.read(3)  # the upload starts at the current position
    bma.files.upload(filename="a.bin", body=body)
    assert [n for n, _ in sizes] == [100000, 100000]
    assert sizes[0][1] == sizes[1][1]


def test_unseekable_upload_body_is_not_retried() -> None:
    class Pipe(io.RawIOBase):
        def __init__(self) -> None:
            self.data = b"y" * 1000

        def readable(self) -> bool:
            return True

        def readinto(self, b: Any) -> int:
            n = min(len(b), len(self.data))
            b[:n] = self.data[:n]
            self.data = self.data[n:]
            return n

    bma, stub = client([api_error(503, "service_unavailable"), reply_json(201, {"id": "file_1"})])
    with pytest.raises(ServiceUnavailableError):
        bma.files.upload(filename="a.bin", body=Pipe())
    assert len(stub.calls) == 1
    assert len(stub.calls[0].content) == 1000


def test_multipart_json_field_has_json_content_type() -> None:
    bma, stub = client([reply_json(201, {"id": "skl_1"})])
    bma.orgs.skills.create(owner={"kind": "org"}, archive=("skill.zip", b"zip"))
    body = stub.calls[0].content
    assert b'name="owner"\r\nContent-Type: application/json\r\n\r\n{"kind": "org"}' in body


def test_token_and_base_url_from_the_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    stub = Stub([reply_json(200, {"agent": {}})])
    monkeypatch.setenv("BMA_TOKEN", "env-token")
    monkeypatch.setenv("BMA_BASE_URL", "https://env.test/api/v1")
    bma = Bma(org_id=ORG, project_id=PROJECT, http_client=httpx.Client(transport=httpx.MockTransport(stub)))
    bma.agents.retrieve(AGENT)
    assert stub.calls[0].headers["authorization"] == "Bearer env-token"
    assert stub.calls[0].url.host == "env.test"
    monkeypatch.delenv("BMA_TOKEN")
    with pytest.raises(BmaError):
        Bma(base_url=BASE)


def test_lists_with_next_param_paginate() -> None:
    bma, stub = client([
        reply_json(200, {"data": [{"sequence": 1, "event_kind": "model_output"}, {"sequence": 2, "event_kind": "model_output"}], "next_after_sequence": 2, "next_before_sequence": None, "has_more": True}),
        reply_json(200, {"data": [{"sequence": 3, "event_kind": "model_output"}], "next_after_sequence": 3, "next_before_sequence": None, "has_more": False}),
        reply_json(200, {"data": [{"sequence": 9, "event_kind": "model_output"}], "next_after_sequence": 9, "next_before_sequence": 8, "has_more": True}),
        reply_json(200, {"data": [{"sequence": 8, "event_kind": "model_output"}], "next_after_sequence": 8, "next_before_sequence": None, "has_more": False}),
        reply_json(200, {"data": [{"id": "ses_1"}], "next_before_id": "ses_1"}),
        reply_json(200, {"data": [], "next_before_id": None}),
        reply_json(200, {"data": [{"id": "file_1"}], "next_page": "p2"}),
        reply_json(200, {"data": [{"id": "file_2"}], "next_page": None}),
    ])
    assert [e.sequence for e in bma.agents.events.list(AGENT, session_id=SESSION)] == [1, 2, 3]
    assert stub.calls[1].url.params["after_sequence"] == "2"
    assert [e.sequence for e in bma.agents.events.list(AGENT, before_sequence=0)] == [9, 8]
    assert stub.calls[3].url.params["before_sequence"] == "8"
    assert [s.id for s in bma.agents.sessions.list(AGENT)] == ["ses_1"]
    assert stub.calls[5].url.params["before_id"] == "ses_1"
    page = bma.files.list()
    assert page.has_next_page()
    assert page.get_next_page().data[0].id == "file_2"
    assert stub.calls[7].url.params["page"] == "p2"
