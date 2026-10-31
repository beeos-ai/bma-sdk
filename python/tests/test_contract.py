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

from bma_sdk import BmaApiError, BmaClient, unwrap
from bma_sdk.facade_extensions import FacadeApiError, FacadeExtensionsClient, bma_sequence
from bma_sdk.rest.api.agents import (
    archive_agent_session,
    create_agent_session,
    get_agent,
    get_agent_session,
    list_agent_sessions,
    put_agent_session_model_override,
)
from bma_sdk.rest.api.desktops import create_desktop_session
from bma_sdk.rest.api.terminals import create_terminal_connection_ticket
from bma_sdk.rest.models import (
    AgentModelOverrideInput,
    AgentModelOverrideProvider,
    Artifact,
    CreateAgentInputRequest,
    CreateAgentSessionRequest,
    CreateAgentSessionRequestMetadata,
    CreateConnectionTicketRequest,
    CreateDesktopSessionRequest,
    TextContentBlock,
)

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
        yield f"http://127.0.0.1:{server.server_address[1]}{prefix}"
    finally:
        server.shutdown()
        server.server_close()
    if failures:
        raise failures[0]


@contextmanager
def rest(name: str) -> Iterator[BmaClient]:
    with serve(find("rest", name), "/api/v1") as url, BmaClient("test-token", url) as client:
        yield client


@contextmanager
def facade(name: str) -> Iterator[FacadeExtensionsClient]:
    with serve(find("facade", name), "") as url, FacadeExtensionsClient("test-key", url, project_id=S["project"]) as client:
        yield client


def override() -> AgentModelOverrideInput:
    return AgentModelOverrideInput(
        model="deepseek-flash",
        provider=AgentModelOverrideProvider(
            api_format="openai-chat-completions",
            base_url="https://llm.example.com",
            api_variant="default",
            endpoint_path="/v1/chat/completions",
        ),
        api_key="sk-test-0000000000",
        ttl_seconds=3600,
        expires_with_session=True,
    )


def test_session_lifecycle() -> None:
    metadata = CreateAgentSessionRequestMetadata.from_dict({"title": "Quarterly report"})
    with rest("create_session") as bma:
        created = unwrap(
            create_agent_session.sync_detailed(
                S["org"], S["project"], S["agent"], client=bma.rest,
                body=CreateAgentSessionRequest(
                    agent_config_id=S["config"], idempotency_key="beework-task-1",
                    metadata=metadata, model_override=override(),
                ),
            )
        )
    assert created.session.id == S["session"]

    with rest("get_session") as bma:
        got = unwrap(get_agent_session.sync_detailed(S["org"], S["project"], S["agent"], S["session"], client=bma.rest))
    assert got.session.next_event_sequence == 5

    with rest("list_sessions") as bma:
        listed = unwrap(
            list_agent_sessions.sync_detailed(
                S["org"], S["project"], S["agent"], client=bma.rest, include_archived=True, limit=10
            )
        )
    assert len(listed.data) == 1 and listed.next_before_id is None

    with rest("archive_session") as bma:
        archived = unwrap(
            archive_agent_session.sync_detailed(S["org"], S["project"], S["agent"], S["session"], client=bma.rest)
        )
    assert archived.session.state == "archived"

    with rest("put_session_model_override") as bma:
        mo = unwrap(
            put_agent_session_model_override.sync_detailed(
                S["org"], S["project"], S["agent"], S["session"], client=bma.rest, body=override()
            )
        )
    assert mo.model_override.expires_with_session is True and mo.model_override.expires_at is None


def test_session_input_and_stream() -> None:
    from bma_sdk.rest.api.agents import create_agent_input

    with rest("create_session_input") as bma:
        created = unwrap(
            create_agent_input.sync_detailed(
                S["org"], S["project"], S["agent"], client=bma.rest,
                session_id=S["session"], idempotency_key="turn-1",
                body=CreateAgentInputRequest(
                    content_blocks=[TextContentBlock(type_="text", text="Summarize the report.")],
                    delivery_mode="queued",
                ),
            )
        )
    assert created.agent_input.state == "queued"

    with rest("stream_session_events") as bma:
        frames = list(
            bma.stream_events(
                S["org"], S["project"], S["agent"], session_id=S["session"], stream_deltas=True, last_event_id=4
            )
        )
    assert [(f.event, f.sequence) for f in frames] == [
        ("agent_input", 5),
        ("tool_call_update", None),
        ("error", None),
    ]
    assert frames[0].data["event_kind"] == "agent_input"


def test_artifact_download_verifies_digest() -> None:
    artifact = Artifact.from_dict(find("rest", "get_artifact")["response"]["json"])
    with rest("get_artifact_content") as bma:
        assert bma.download_artifact(artifact, max_bytes=1024) == b"hello world"

    artifact.digest = "sha256:" + "0" * 64
    with rest("get_artifact_content") as bma, pytest.raises(ValueError, match="digest mismatch"):
        bma.download_artifact(artifact, max_bytes=1024)


def test_machine_desktop_terminal_and_errors() -> None:
    with rest("create_desktop_session") as bma:
        desktop = unwrap(
            create_desktop_session.sync_detailed(
                S["org"], S["project"], S["machine"], client=bma.rest,
                body=CreateDesktopSessionRequest(agent_id=S["agent"], read_only=True),
            )
        )
    assert desktop.capabilities.width == 1920

    with rest("create_terminal_ticket") as bma:
        ticket = unwrap(
            create_terminal_connection_ticket.sync_detailed(
                S["org"], S["project"], S["machine"], S["terminal_session"], client=bma.rest,
                body=CreateConnectionTicketRequest(ttl_seconds=60),
            )
        )
    assert ticket.purpose == "terminal_connect"

    with rest("get_agent_not_found") as bma, pytest.raises(BmaApiError) as excinfo:
        unwrap(get_agent.sync_detailed(S["org"], S["project"], "agt_zzzzzzzzzzzzzzzzzzzzzzzzzz", client=bma.rest))
    assert excinfo.value.status == 404 and excinfo.value.code == "not_found"


def test_facade_extensions() -> None:
    with facade("desktop_stream") as ext:
        stream = ext.get_session_desktop_stream(
            S["session"], desktop_session_id=S["desktop_session"], ttl_seconds=60, origin="https://app.example.com"
        )
    assert stream.type_ == "bma.desktop_stream" and stream.ticket == "watch-ticket"

    with facade("upload_session_file") as ext:
        file = ext.upload_session_file(S["session"], "notes.txt", b"meeting notes")
    assert file.size_bytes == 13

    with facade("list_session_files") as ext:
        page = ext.list_session_files(S["session"], limit=1)
    assert page.next_page == "1" and len(page.data) == 1

    with facade("upload_session_file_conflict") as ext, pytest.raises(FacadeApiError) as excinfo:
        ext.upload_session_file(S["session"], "dup.txt", b"again")
    assert excinfo.value.status == 409 and excinfo.value.code == "file_already_exists"

    assert bma_sequence({"type": "agent.message", "bma_sequence": 42}) == 42
    assert bma_sequence({"type": "agent.message"}) is None
    with pytest.raises(ValueError):
        FacadeExtensionsClient("k", "https://x.example/v1")


def test_facade_session_resources() -> None:
    with facade("add_session_resource") as ext:
        resource = ext.add_session_resource(S["session"], S["file"], mount_path="reports/report.pdf")
    assert resource.id == S["resource"] and resource.file_id == S["file"]
    assert resource.mount_path == "reports/report.pdf"

    with facade("list_session_resources") as ext:
        page = ext.list_session_resources(S["session"])
    assert len(page.data) == 1 and page.data[0].id == S["resource"]

    with facade("delete_session_resource") as ext:
        deleted = ext.delete_session_resource(S["session"], S["resource"])
    assert deleted.type_ == "session_resource_deleted"


def test_files_upload_mount_outputs() -> None:
    """The README files example: upload, mount into a session, list outputs."""
    from bma_sdk.rest.api.files import add_session_resource, list_files, upload_file
    from bma_sdk.rest.models import FileResourceParams
    from bma_sdk.rest.types import File as Upload

    content = find("rest", "upload_file")["request"]["text"].encode()
    with rest("upload_file") as bma:
        uploaded = unwrap(
            upload_file.sync_detailed(
                S["org"], S["project"], client=bma.rest,
                body=Upload(payload=content), filename="report.pdf", idempotency_key="upload-report-1",
            )
        )
    assert uploaded.id == S["file"] and uploaded.scope is None

    with rest("add_session_file_resource") as bma:
        mounted = unwrap(
            add_session_resource.sync_detailed(
                S["org"], S["project"], S["agent"], S["session"], client=bma.rest,
                body=FileResourceParams(
                    type_="file", file_id=uploaded.id, mount_path="/mnt/session/uploads/reports/report.pdf"
                ),
            )
        )
    assert mounted.file_id == S["mounted_file"] and mounted.mount_path == "/mnt/session/uploads/reports/report.pdf"

    with rest("list_session_outputs") as bma:
        outputs = unwrap(list_files.sync_detailed(S["org"], S["project"], client=bma.rest, scope_id=S["session"]))
    assert [(f.id, f.scope.id) for f in outputs.data] == [(S["output_file"], S["session"])]
    assert outputs.next_page is None
