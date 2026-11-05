"""Request runtime shared by every generated resource method: scope defaults,
request encoding, retries with idempotency keys, timeouts, error decoding,
pagination and event streams. Same rules as typescript/src/core.ts; the
defaults are ADR 0012 decision D3."""

from __future__ import annotations

import asyncio
import email.utils
import json
import random
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import (
    Any,
    AsyncIterator,
    Callable,
    Dict,
    Iterator,
    List,
    Mapping,
    Optional,
    Tuple,
    TypeVar,
    Union,
    cast,
)
from urllib.parse import quote

import httpx

from ._errors import APIConnectionError, APIConnectionTimeoutError, BmaApiError, BmaError, EventStreamError
from ._models import BaseModel, construct
from ._pagination import AsyncCursorPage, AsyncPaginator, SyncCursorPage
from ._streaming import AsyncStream, Stream, iter_sse, aiter_sse
from ._types import NOT_GIVEN, Headers, NotGiven, Query

__all__ = ["DEFAULT_MAX_RETRIES", "DEFAULT_TIMEOUT", "OperationDescriptor", "RequestOptions"]

DEFAULT_TIMEOUT = 60.0
"""Default per-attempt timeout in seconds (D3). Streams are bounded only until headers arrive."""
DEFAULT_MAX_RETRIES = 2
"""Default retries after the first attempt (D3; the Anthropic SDKs use 2)."""

T = TypeVar("T")
E = TypeVar("E")


@dataclass(frozen=True)
class OperationDescriptor:
    """Generated description of one contract operation."""

    id: str
    method: str
    path: str
    path_params: Mapping[str, str] = field(default_factory=dict)
    """Path template name -> params key (scope params) or positional name."""
    query: Mapping[str, str] = field(default_factory=dict)
    """Query name -> serialization style."""
    headers: Mapping[str, str] = field(default_factory=dict)
    """Header name -> params key."""
    body: Optional[str] = None  # json | binary | multipart
    body_required: bool = False
    multipart_json: Tuple[str, ...] = ()
    multipart_files: Tuple[str, ...] = ()
    response: str = "json"  # json | void | binary | sse
    idempotency: bool = False


@dataclass(frozen=True)
class RequestOptions:
    extra_headers: Optional[Headers] = None
    extra_query: Optional[Query] = None
    timeout: Union[float, NotGiven] = NOT_GIVEN
    idempotency_key: Optional[str] = None


@dataclass
class _Built:
    method: str
    url: str
    params: List[Tuple[str, str]]
    headers: Dict[str, str]
    content: Optional[Any] = None
    data: Optional[Dict[str, str]] = None
    files: Optional[List[Tuple[str, Any]]] = None


def _scalar(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)


def _json_default(value: object) -> object:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, BaseModel):
        return value.to_dict()
    raise TypeError(f"bma: cannot encode {type(value).__name__} as JSON")


def _backoff(retry: int) -> float:
    # Exponential backoff with up to 25% jitter: 0.5s, 1s, 2s ... capped at 8s
    # (@anthropic-ai/sdk calculateDefaultRetryTimeoutMillis).
    return min(0.5 * 2**retry, 8.0) * (1 - random.random() * 0.25)


def _retry_after(headers: httpx.Headers) -> Optional[float]:
    # retry-after-ms, then retry-after (seconds or HTTP date), honoured when
    # between 0 and 60 seconds, as in @anthropic-ai/sdk.
    try:
        ms = float(headers.get("retry-after-ms", ""))
        if 0 <= ms < 60_000:
            return ms / 1000
    except ValueError:
        pass
    raw = headers.get("retry-after")
    if raw:
        try:
            delay = float(raw)
        except ValueError:
            parsed = email.utils.parsedate_to_datetime(raw) if raw else None
            delay = parsed.timestamp() - time.time() if parsed else -1
        if 0 <= delay < 60:
            return delay
    return None


def _should_retry(response: httpx.Response, safe: bool) -> bool:
    hint = response.headers.get("x-should-retry")
    if hint == "false":
        return False
    s = response.status_code
    if not safe:
        return s in (429, 503)
    if hint == "true":
        return True
    return s in (408, 429) or s >= 500


def _error_from(response: httpx.Response) -> BmaApiError:
    try:
        body: object = json.loads(response.content) if response.content else None
    except ValueError:
        body = None
    return BmaApiError.generate(response.status_code, body, response.headers)


class _BaseCore:
    def __init__(
        self,
        *,
        base_url: str,
        headers: Dict[str, str],
        scope: Dict[str, Optional[str]],
        scope_option: Dict[str, str],
        timeout: float,
        max_retries: int,
    ) -> None:
        base_url = base_url.strip().rstrip("/")
        if httpx.URL(base_url).scheme not in ("http", "https"):
            raise BmaError("bma: base_url must use http or https")
        self.base_url = base_url
        self._headers = headers
        self._scope = scope
        self._scope_option = scope_option
        self.timeout = timeout
        self.max_retries = max_retries

    def _build(self, op: OperationDescriptor, path: Mapping[str, str], params: Mapping[str, object], options: RequestOptions) -> _Built:
        rest: Dict[str, object] = {k: v for k, v in params.items() if not isinstance(v, NotGiven)}
        url = op.path
        for name, key in op.path_params.items():
            value: object = path.get(name)
            if value is None:
                value = rest.pop(key, None) or self._scope.get(key)
                if not isinstance(value, str) or not value:
                    option = self._scope_option.get(key, key)
                    raise BmaError(f"bma: {op.id} needs {key}; set the client option {option} or pass {key}=")
            url = url.replace("{" + name + "}", quote(str(value), safe=""))

        query: List[Tuple[str, str]] = []
        for name, style in op.query.items():
            value = rest.pop(name, None)
            if value is None:
                continue
            if style == "deepObject" and isinstance(value, Mapping):
                for k, v in cast(Mapping[str, object], value).items():
                    query.append((f"{name}[{k}]", _scalar(v)))
            elif isinstance(value, (list, tuple)):
                query.extend((name, _scalar(v)) for v in cast(List[object], value))
            else:
                query.append((name, _scalar(value)))
        for k, v in (options.extra_query or {}).items():
            query.append((k, _scalar(v)))

        headers = dict(self._headers)
        for name, key in op.headers.items():
            value = rest.pop(key, None)
            if value is None and key in self._scope:
                value = self._scope[key]
            if value is not None:
                headers[name] = _scalar(value)

        if op.idempotency:
            headers["Idempotency-Key"] = options.idempotency_key or f"bma-sdk-retry-{uuid.uuid4()}"
        elif options.idempotency_key is not None:
            raise BmaError(f"bma: {op.id} does not accept an Idempotency-Key")

        built = _Built(op.method, self.base_url + url, query, headers)
        if op.body == "json":
            if op.body_required or rest:
                built.content = json.dumps(rest, default=_json_default).encode()
                headers["Content-Type"] = "application/json"
        elif op.body == "binary":
            raw = rest.get("body")
            if raw is not None:
                built.content = raw.encode() if isinstance(raw, str) else raw
                headers["Content-Type"] = "application/octet-stream"
        elif op.body == "multipart":
            data: Dict[str, str] = {}
            files: List[Tuple[str, Any]] = []
            for key, value in rest.items():
                if key in op.multipart_files:
                    files.append((key, value if isinstance(value, tuple) else (key, value)))
                elif key in op.multipart_json or isinstance(value, (dict, list)):
                    data[key] = json.dumps(value, default=_json_default)
                else:
                    data[key] = _scalar(value)
            built.data, built.files = data, files
        for k, v in (options.extra_headers or {}).items():
            headers[k] = v
        return built

    def _timeout(self, options: RequestOptions) -> float:
        return self.timeout if isinstance(options.timeout, NotGiven) else options.timeout

    def _decode(self, op: OperationDescriptor, response: httpx.Response, cast_to: Any) -> Any:
        if op.response == "binary":
            return response
        if response.status_code == 204 or op.response == "void" or cast_to is None:
            return None
        return construct(cast_to, response.json())

    @staticmethod
    def _resume_key(op: OperationDescriptor) -> Optional[str]:
        return next((key for name, key in op.headers.items() if name.lower() == "last-event-id"), None)


def _frame(raw_event: str, raw_id: Optional[str], data: object, events: Mapping[str, type[BaseModel]]) -> Optional[BaseModel]:
    cls = events.get(raw_event)
    if cls is None:
        return None  # an event kind newer than this SDK
    frame: Dict[str, object] = {"event": raw_event, "data": data}
    if raw_id is not None:
        if not raw_id.isdigit():
            raise BmaError(f"bma: invalid event id {raw_id!r}")
        frame["id"], frame["sequence"] = raw_id, int(raw_id)
    return cls.construct_from(frame)


class _Reconnect(Exception):
    def __init__(self, error: BmaApiError) -> None:
        self.error = error


class SyncClientCore(_BaseCore):
    """@private The transport every synchronous resource calls."""

    def __init__(self, *, http_client: Optional[httpx.Client] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._http = http_client or httpx.Client()

    def close(self) -> None:
        self._http.close()

    def _send(self, op: OperationDescriptor, built: _Built, options: RequestOptions, stream: bool = False) -> httpx.Response:
        """Sends with retries. GET and operations with an Idempotency-Key retry
        408/429/5xx and connection errors; other writes retry only requests
        that never reached the server, 429 and 503 (D3). 409 is never retried."""
        safe = op.method == "GET" or op.idempotency
        timeout = self._timeout(options)
        used = 0
        while True:
            request = self._http.build_request(
                built.method, built.url, params=tuple(built.params), headers=built.headers,
                content=built.content, data=built.data, files=built.files,
                timeout=httpx.Timeout(timeout, read=None) if stream else timeout,
            )
            try:
                response = self._http.send(request, stream=stream)
            except httpx.TimeoutException as e:
                undelivered = isinstance(e, httpx.ConnectTimeout)
                if used < self.max_retries and (safe or undelivered):
                    time.sleep(_backoff(used))
                    used += 1
                    continue
                raise APIConnectionTimeoutError() from e
            except httpx.TransportError as e:
                if used < self.max_retries and (safe or isinstance(e, httpx.ConnectError)):
                    time.sleep(_backoff(used))
                    used += 1
                    continue
                raise APIConnectionError(f"bma: connection error: {e}") from e
            if response.is_success:
                return response
            response.read()
            response.close()
            error = _error_from(response)
            if used < self.max_retries and _should_retry(response, safe):
                delay = _retry_after(response.headers)
                time.sleep(_backoff(used) if delay is None else delay)
                used += 1
                continue
            raise error

    def _request(self, op: OperationDescriptor, path: Mapping[str, str], params: Mapping[str, object], options: RequestOptions, cast_to: Any) -> Any:
        built = self._build(op, path, params, options)
        return self._decode(op, self._send(op, built, options), cast_to)

    def _open(self, op: OperationDescriptor, path: Mapping[str, str], params: Mapping[str, object], options: RequestOptions) -> httpx.Response:
        """A successful response whose body is not read yet; close it."""
        return self._send(op, self._build(op, path, params, options), options, stream=True)

    def _page(self, op: OperationDescriptor, path: Mapping[str, str], params: Mapping[str, object], options: RequestOptions, item: Any) -> SyncCursorPage[Any]:
        def fetch(cursor: Optional[str]) -> SyncCursorPage[Any]:
            current = dict(params) if cursor is None else {**params, "cursor": cursor}
            body = self._send(op, self._build(op, path, current, options), options).json()
            return SyncCursorPage(construct(List[item], body.get("data") or []), body.get("next_cursor"), fetch)

        return fetch(None)

    def _stream(
        self,
        op: OperationDescriptor,
        path: Mapping[str, str],
        params: Mapping[str, object],
        options: RequestOptions,
        events: Mapping[str, type[BaseModel]],
        on_open: Optional[Callable[[], None]] = None,
    ) -> Stream[Any]:
        """Event stream with the reconnect rule of the contract: an ``error``
        frame with code ``service_unavailable`` (or a dropped connection)
        reconnects with Last-Event-ID set to the last durable frame; any
        other error frame ends the stream with EventStreamError."""
        resume_key = self._resume_key(op)
        holder: List[httpx.Response] = []

        def iterate() -> Iterator[Any]:
            current: Dict[str, object] = dict(params)
            last_id: Optional[str] = None
            failures = 0
            while True:
                built = self._build(op, path, current, options)
                built.headers["Accept"] = "text/event-stream"
                response = self._send(op, built, options, stream=True)
                holder[:] = [response]
                if on_open is not None:
                    on_open()
                try:
                    for raw in iter_sse(response.iter_lines()):
                        data = json.loads(raw.data)
                        if raw.event == "error":
                            error = EventStreamError(data)
                            if error.code != "service_unavailable":
                                raise error
                            raise _Reconnect(error)
                        failures = 0
                        frame = _frame(raw.event, raw.id, data, events)
                        if raw.id is not None:
                            last_id = raw.id
                        if frame is not None:
                            yield frame
                    return
                except _Reconnect as r:
                    last_error: BmaApiError = r.error
                except httpx.TransportError as e:
                    if stream_obj.closed:
                        return
                    last_error = APIConnectionError(f"bma: event stream dropped: {e}")
                finally:
                    response.close()
                if failures >= self.max_retries:
                    raise last_error
                time.sleep(_backoff(failures))
                failures += 1
                if last_id is not None and resume_key:
                    current = {**params, resume_key: int(last_id)}
                    # Last-Event-ID is the resume point; after_sequence would replay older events.
                    current.pop("after_sequence", None)

        stream_obj: Stream[Any] = Stream(iterate, lambda: [r.close() for r in holder])
        return stream_obj


class AsyncClientCore(_BaseCore):
    """@private The transport every asynchronous resource calls."""

    def __init__(self, *, http_client: Optional[httpx.AsyncClient] = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._http = http_client or httpx.AsyncClient()

    async def close(self) -> None:
        await self._http.aclose()

    async def _send(self, op: OperationDescriptor, built: _Built, options: RequestOptions, stream: bool = False) -> httpx.Response:
        safe = op.method == "GET" or op.idempotency
        timeout = self._timeout(options)
        used = 0
        while True:
            request = self._http.build_request(
                built.method, built.url, params=tuple(built.params), headers=built.headers,
                content=built.content, data=built.data, files=built.files,
                timeout=httpx.Timeout(timeout, read=None) if stream else timeout,
            )
            try:
                response = await self._http.send(request, stream=stream)
            except httpx.TimeoutException as e:
                if used < self.max_retries and (safe or isinstance(e, httpx.ConnectTimeout)):
                    await asyncio.sleep(_backoff(used))
                    used += 1
                    continue
                raise APIConnectionTimeoutError() from e
            except httpx.TransportError as e:
                if used < self.max_retries and (safe or isinstance(e, httpx.ConnectError)):
                    await asyncio.sleep(_backoff(used))
                    used += 1
                    continue
                raise APIConnectionError(f"bma: connection error: {e}") from e
            if response.is_success:
                return response
            await response.aread()
            await response.aclose()
            error = _error_from(response)
            if used < self.max_retries and _should_retry(response, safe):
                delay = _retry_after(response.headers)
                await asyncio.sleep(_backoff(used) if delay is None else delay)
                used += 1
                continue
            raise error

    async def _request(self, op: OperationDescriptor, path: Mapping[str, str], params: Mapping[str, object], options: RequestOptions, cast_to: Any) -> Any:
        built = self._build(op, path, params, options)
        response = await self._send(op, built, options)
        return self._decode(op, response, cast_to)

    async def _open(self, op: OperationDescriptor, path: Mapping[str, str], params: Mapping[str, object], options: RequestOptions) -> httpx.Response:
        return await self._send(op, self._build(op, path, params, options), options, stream=True)

    def _page(self, op: OperationDescriptor, path: Mapping[str, str], params: Mapping[str, object], options: RequestOptions, item: Any) -> AsyncPaginator[Any]:
        async def fetch(cursor: Optional[str]) -> AsyncCursorPage[Any]:
            current = dict(params) if cursor is None else {**params, "cursor": cursor}
            response = await self._send(op, self._build(op, path, current, options), options)
            body = response.json()
            return AsyncCursorPage(construct(List[item], body.get("data") or []), body.get("next_cursor"), fetch)

        return AsyncPaginator(fetch)

    def _stream(
        self,
        op: OperationDescriptor,
        path: Mapping[str, str],
        params: Mapping[str, object],
        options: RequestOptions,
        events: Mapping[str, type[BaseModel]],
        on_open: Optional[Callable[[], None]] = None,
    ) -> AsyncStream[Any]:
        resume_key = self._resume_key(op)

        async def iterate() -> AsyncIterator[Any]:
            current: Dict[str, object] = dict(params)
            last_id: Optional[str] = None
            failures = 0
            while True:
                built = self._build(op, path, current, options)
                built.headers["Accept"] = "text/event-stream"
                response = await self._send(op, built, options, stream=True)
                if on_open is not None:
                    on_open()
                try:
                    async for raw in aiter_sse(response.aiter_lines()):
                        data = json.loads(raw.data)
                        if raw.event == "error":
                            error = EventStreamError(data)
                            if error.code != "service_unavailable":
                                raise error
                            raise _Reconnect(error)
                        failures = 0
                        frame = _frame(raw.event, raw.id, data, events)
                        if raw.id is not None:
                            last_id = raw.id
                        if frame is not None:
                            yield frame
                    return
                except _Reconnect as r:
                    last_error: BmaApiError = r.error
                except httpx.TransportError as e:
                    last_error = APIConnectionError(f"bma: event stream dropped: {e}")
                finally:
                    await response.aclose()
                if failures >= self.max_retries:
                    raise last_error
                await asyncio.sleep(_backoff(failures))
                failures += 1
                if last_id is not None and resume_key:
                    current = {**params, resume_key: int(last_id)}
                    current.pop("after_sequence", None)

        return AsyncStream(iterate)
