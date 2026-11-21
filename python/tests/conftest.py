from __future__ import annotations

import json
import os
import threading
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Callable, Iterator
from urllib.parse import urlsplit

import pytest

from bma_sdk import _resume


@dataclass
class Seen:
    method: str
    path: str
    query: str
    headers: dict[str, str]
    body: str


class Reply:
    """What a handler writes: a JSON body, or raw SSE frames (optionally cut off)."""

    def __init__(self, handler: BaseHTTPRequestHandler) -> None:
        self.h = handler

    def json(self, status: int, body: Any) -> None:
        data = json.dumps(body).encode()
        self.h.send_response(status)
        self.h.send_header("content-type", "application/json")
        self.h.send_header("content-length", str(len(data)))
        self.h.end_headers()
        self.h.wfile.write(data)

    def sse(self, *frames: str, cut: bool = False) -> None:
        self.h.send_response(200)
        self.h.send_header("content-type", "text/event-stream")
        self.h.send_header("connection", "close")
        self.h.end_headers()
        for frame in frames:
            self.h.wfile.write(frame.encode())
        self.h.wfile.flush()
        self.h.close_connection = True


Handler = Callable[[Reply, Seen, int], None]


class Server:
    def __init__(self, handler: Handler) -> None:
        self.seen: list[Seen] = []
        outer = self

        class H(BaseHTTPRequestHandler):
            def log_message(self, format: str, *args: Any) -> None:
                pass

            def handle_any(self) -> None:
                length = int(self.headers.get("content-length") or 0)
                body = self.rfile.read(length).decode() if length else ""
                url = urlsplit(self.path)
                seen = Seen(self.command, url.path, url.query, {k.lower(): v for k, v in self.headers.items()}, body)
                outer.seen.append(seen)
                handler(Reply(self), seen, len(outer.seen))

            do_GET = do_POST = do_DELETE = do_PUT = handle_any

        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.url = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def close(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()


@pytest.fixture
def serve() -> Iterator[Callable[[Handler], Server]]:
    servers: list[Server] = []

    def start(handler: Handler) -> Server:
        servers.append(Server(handler))
        return servers[-1]

    yield start
    for s in servers:
        s.close()


@pytest.fixture(autouse=True)
def fast_resume(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(_resume.CONFIG, "backoff", 0.001)
    monkeypatch.setattr(_resume.CONFIG, "max_backoff", 0.001)
    if os.environ.get("BMA_INTEGRATION") == "1":
        return  # the live test reads the BMA_* settings
    for name in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL", "BMA_API_KEY", "BMA_BASE_URL", "BMA_PROJECT_ID"):
        monkeypatch.delenv(name, raising=False)


def frame(type: str, id: str, sequence: int) -> str:
    data: dict[str, Any] = {"type": type, "id": id}
    if sequence:
        data.update(bma_sequence=sequence, processed_at="2026-11-08T00:00:00Z")
    return f"event: {type}\ndata: {json.dumps(data)}\n\n"
