"""Replay contracts/bma/fixtures/sdk-contract.json against the SDK.

tools/check_contract.py validates the fixtures against the OpenAPI contracts.
"""

from __future__ import annotations

import email.parser
import email.policy
import json
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlsplit

import pytest

from bma_sdk import Bma, BmaError, ConflictError, EventStreamError, NotFoundError
from bma_sdk.facade_extensions import FacadeExtensions, bma_sequence
from bma_sdk.types import AgentModelOverrideInputParam, Artifact

FIXTURES = json.loads(
    (Path(__file__).resolve().parents[2] / "contracts" / "bma" / "fixtures" / "sdk-contract.json").read_text()
)
S = FIXTURES["scope"]


def find(group: str, name: str) -> dict[str, Any]:
    return next(c for c in FIXTURES[group] if c["name"] == name)


def check_request(case: dict[str, Any], prefix: str, method: str, path: str, headers: Any, body: bytes) -> None:
    want = case["request"]
    url = urlsplit(path)
    assert method == want["method"]
    assert url.path == prefix + want["path"]
    assert dict(parse_qsl(url.query)) == want.get("query", {})
    for key, value in want.get("headers", {}).items():
        assert headers.get(key) == value, key
    if "json" in want:
        assert json.loads(body) == want["json"]
    elif "text" in want:
        assert headers["Content-Type"] == "application/octet-stream"
        assert body.decode() == want["text"]
    elif "multipart" in want:
        part = want["multipart"]
        message = email.parser.BytesParser(policy=email.policy.HTTP).parsebytes(
            b"Content-Type: " + headers["Content-Type"].encode() + b"\r\n\r\n" + body
        )
        parts = list(message.iter_parts())
        assert len(parts) == 1
        assert parts[0].get_param("name", header="content-disposition") == part["field"]
        assert parts[0].get_filename() == part["filename"]
        assert parts[0].get_payload(decode=True).decode() == part["text"]
    else:
        assert body in (b"", b"{}")


def write_response(handler: BaseHTTPRequestHandler, response: dict[str, Any]) -> None:
    if "sse" in response:
        payload = ""
        for frame in response["sse"]:
            if "comment" in frame:
                payload += f": {frame['comment']}\n\n"
                continue
            if "event" in frame:
                payload += f"event: {frame['event']}\n"
            if "id" in frame:
                payload += f"id: {frame['id']}\n"
            payload += f"data: {json.dumps(frame['data'])}\n\n"
        raw, content_type = payload.encode(), "text/event-stream"
    elif "json" in response:
        raw, content_type = json.dumps(response["json"]).encode(), "application/json"
    else:
        raw, content_type = response.get("text", "").encode(), response.get("content_type", "application/octet-stream")
    handler.send_response(response["status"])
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Length", str(len(raw)))
    handler.end_headers()
    handler.wfile.write(raw)


@contextmanager
def serve(case: dict[str, Any], prefix: str) -> Iterator[str]:
    """Serve exactly one recorded exchange; fail the test on any mismatch."""
    failures: list[BaseException] = []

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args: object) -> None:
            pass

        def handle_one(self) -> None:
            body = self.rfile.read(int(self.headers.get("Content-Length") or 0))
            try:
                check_request(case, prefix, self.command, self.path, self.headers, body)
            except AssertionError as error:
                failures.append(error)
                self.send_response(418)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            write_response(self, case["response"])

        do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = handle_one

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()
    if failures:
        raise failures[0]


@contextmanager
def rest(name: str) -> Iterator[Bma]:
    with serve(find("rest", name), "/api/v1") as url, Bma(
        token="test-token", base_url=url, org_id=S["org"], project_id=S["project"], max_retries=0
    ) as client:
        yield client


@contextmanager
def facade(name: str) -> Iterator[FacadeExtensions]:
    with serve(find("facade", name), "") as url, FacadeExtensions(
        api_key="test-key", base_url=url, project_id=S["project"], max_retries=0
    ) as client:
        yield client


def override() -> AgentModelOverrideInputParam:
    return {
        "model": "deepseek-flash",
        "provider": {
            "api_format": "openai-chat-completions",
            "base_url": "https://llm.example.com",
            "api_variant": "default",
            "endpoint_path": "/v1/chat/completions",
        },
        "api_key": "sk-test-0000000000",
        "ttl_seconds": 3600,
        "expires_with_session": True,
    }


def test_session_lifecycle() -> None:
    with rest("create_session") as bma:
        created = bma.agents.sessions.create(
            S["agent"],
            agent_config_id=S["config"],
            idempotency_key="beework-task-1",
            metadata={"title": "Quarterly report"},
            model_override=override(),
        )
    assert created.session.id == S["session"] and created.session.status == "idle"

    with rest("get_session") as bma:
        got = bma.agents.sessions.retrieve(S["agent"], S["session"])
    assert got.session.next_event_sequence == 5 and got.session.status == "running"

    with rest("list_sessions") as bma:
        listed = bma.agents.sessions.list(S["agent"], include_archived=True, limit=10)
    assert len(listed.data) == 1 and listed.next_cursor is None

    with rest("archive_session") as bma:
        archived = bma.agents.sessions.archive(S["agent"], S["session"])
    assert archived.session.state == "archived" and archived.session.status == "terminated"

    with rest("put_session_model_override") as bma:
        mo = bma.agents.sessions.model_override.set(S["agent"], S["session"], **override())
    assert mo.model_override.expires_with_session is True and mo.model_override.expires_at is None


def test_session_input_and_stream() -> None:
    with rest("create_session_input") as bma:
        created = bma.agents.inputs.create(
            S["agent"],
            session_id=S["session"],
            content_blocks=[{"type": "text", "text": "Summarize the report."}],
            delivery_mode="queued",
            idempotency_key="turn-1",
        )
    assert created.agent_input.state == "queued"

    # The recorded stream ends with a terminal (non service_unavailable) error frame.
    frames: list[tuple[str, int | None]] = []
    with rest("stream_session_events") as bma, pytest.raises(EventStreamError):
        for ev in bma.agents.events.stream(S["agent"], session_id=S["session"], stream_deltas=True, last_event_id=4):
            frames.append((ev.event, ev.sequence if ev.event == "agent_input" else None))
    assert frames == [("agent_input", 5), ("tool_call_update", None)]


def test_artifact_download_verifies_digest() -> None:
    artifact = Artifact.construct_from(find("rest", "get_artifact")["response"]["json"])
    with rest("get_artifact_content") as bma:
        assert bma.agents.artifacts.download_verified(artifact, max_bytes=1024) == b"hello world"

    bad = artifact.model_copy(update={"digest": "sha256:" + "0" * 64})
    with rest("get_artifact_content") as bma, pytest.raises(BmaError, match="digest mismatch"):
        bma.agents.artifacts.download_verified(bad, max_bytes=1024)


def test_machine_desktop_terminal_and_errors() -> None:
    with rest("create_desktop_session") as bma:
        desktop = bma.machines.desktop_sessions.create(S["machine"], agent_id=S["agent"], read_only=True)
    assert desktop.capabilities.width == 1920

    with rest("create_terminal_ticket") as bma:
        ticket = bma.machines.terminal_sessions.connection_ticket(S["machine"], S["terminal_session"], ttl_seconds=60)
    assert ticket.purpose == "terminal_connect"

    with rest("get_agent_not_found") as bma, pytest.raises(NotFoundError) as excinfo:
        bma.agents.retrieve("agt_zzzzzzzzzzzzzzzzzzzzzzzzzz")
    assert excinfo.value.status == 404 and excinfo.value.code == "not_found"


def test_files_upload_mount_outputs() -> None:
    """The README files example: upload, mount into a session, list outputs."""
    content = find("rest", "upload_file")["request"]["text"].encode()
    with rest("upload_file") as bma:
        uploaded = bma.files.upload(filename="report.pdf", body=content, idempotency_key="upload-report-1")
    assert uploaded.id == S["file"] and uploaded.scope is None

    with rest("add_session_file_resource") as bma:
        mounted = bma.agents.sessions.resources.add(
            S["agent"], S["session"], type="file", file_id=uploaded.id, mount_path="/mnt/session/uploads/reports/report.pdf"
        )
    assert mounted.file_id == S["mounted_file"] and mounted.mount_path == "/mnt/session/uploads/reports/report.pdf"

    with rest("list_session_outputs") as bma:
        outputs = bma.files.list(scope_id=S["session"])
    assert [(f.id, f.scope.id if f.scope else None) for f in outputs.data] == [(S["output_file"], S["session"])]
    assert outputs.next_cursor is None


def test_agent_machines() -> None:
    with rest("create_agent_machine") as bma:
        created = bma.agents.machines.create(
            S["agent"], template="base-2c4g", machine_pool_id=S["pool"], display_name="Ada's workstation",
            idempotency_key="machine-ada-1",
        )
    assert created.kind == "persistent" and created.cpu is None

    with rest("list_agent_machines") as bma:
        listed = bma.agents.machines.list(S["agent"])
    assert [(m.id, m.connection_state, m.cpu) for m in listed.data] == [(S["machine"], "online", 2)]

    with rest("delete_agent_machine") as bma:
        assert bma.agents.machines.delete(S["agent"], S["machine"]) is None


def test_facade_extensions() -> None:
    with facade("desktop_stream") as ext:
        stream = ext.sessions.desktop.stream(
            S["session"], desktop_session_id=S["desktop_session"], ttl_seconds=60, origin="https://app.example.com"
        )
    assert stream.type == "bma.desktop_stream" and stream.ticket == "watch-ticket"

    with facade("upload_session_file") as ext:
        file = ext.sessions.files.upload(S["session"], file=("notes.txt", b"meeting notes"))
    assert file.size_bytes == 13

    with facade("list_session_files") as ext:
        page = ext.sessions.files.list(S["session"], limit=1)
    assert page.next_cursor == "1" and len(page.data) == 1

    with facade("upload_session_file_conflict") as ext, pytest.raises(ConflictError) as excinfo:
        ext.sessions.files.upload(S["session"], file=("dup.txt", b"again"))
    assert excinfo.value.status == 409 and excinfo.value.code == "file_already_exists"

    assert bma_sequence({"type": "agent.message", "bma_sequence": 42}) == 42
    assert bma_sequence({"type": "agent.message"}) is None
    with pytest.raises(BmaError):
        FacadeExtensions(api_key="k", base_url="https://x.example/v1")
    with FacadeExtensions(api_key="k", base_url="https://x.example/api/v1/") as ext:
        assert ext.base_url == "https://x.example"


def test_facade_session_resources() -> None:
    with facade("add_session_resource") as ext:
        resource = ext.sessions.resources.add(S["session"], type="file", file_id=S["file"], mount_path="reports/report.pdf")
    assert resource.id == S["resource"] and resource.file_id == S["file"]
    assert resource.mount_path == "reports/report.pdf"

    with facade("list_session_resources") as ext:
        page = ext.sessions.resources.list(S["session"])
    assert len(page.data) == 1 and page.data[0].id == S["resource"]

    with facade("delete_session_resource") as ext:
        deleted = ext.sessions.resources.delete(S["session"], S["resource"])
    assert deleted.type == "session_resource_deleted"
