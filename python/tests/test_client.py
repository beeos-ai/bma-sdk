from __future__ import annotations

import json

import pytest

import bma_sdk
from bma_sdk import AsyncBma, Bma, NotFoundError, error_code


def test_reads_the_bma_environment_only(serve, monkeypatch):
    s = serve(lambda r, req, n: r.json(200, {"data": [], "next_page": None}))
    monkeypatch.setenv("ANTHROPIC_API_KEY", "anthropic-key")
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "http://127.0.0.1:1")
    monkeypatch.setenv("BMA_API_KEY", "bma-key")
    monkeypatch.setenv("BMA_BASE_URL", s.url)
    monkeypatch.setenv("BMA_PROJECT_ID", "proj_1")
    client = Bma()
    client.beta.machines.list()
    client.beta.agents.list()
    assert [r.path for r in s.seen] == ["/v1/machines", "/v1/agents"]
    for r in s.seen:
        assert r.headers["authorization"] == "Bearer bma-key"
        assert r.headers["bma-workspace-id"] == "proj_1"
        assert r.headers["x-bma-sdk"].startswith("bma-sdk-py/")


def test_default_origin_requires_key_and_copy_keeps_settings(serve, monkeypatch):
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://example.invalid")
    assert str(Bma(api_key="k").base_url).rstrip("/") == bma_sdk.DEFAULT_BASE_URL
    monkeypatch.setenv("ANTHROPIC_API_KEY", "anthropic-key")
    with pytest.raises(TypeError, match="BMA_API_KEY"):
        Bma()
    s = serve(lambda r, req, n: r.json(200, {"data": [], "next_page": None}))
    base = Bma(api_key="bma-key", base_url=s.url, project="proj_a")
    clone = base.with_options(max_retries=0, project="proj_b")
    assert isinstance(clone, Bma)
    base.beta.machines.list()
    clone.beta.machines.list()
    assert [r.headers["bma-workspace-id"] for r in s.seen] == ["proj_a", "proj_b"]
    assert s.seen[1].headers["authorization"] == "Bearer bma-key"


def test_extension_create_retries_with_one_idempotency_key(serve):
    def handler(r, req, n):
        if n == 1:
            r.json(500, {"type": "error", "error": {"type": "api_error", "message": "boom"}})
        else:
            r.json(200, {"type": "terminal_session", "id": "tsn_1", "machine_id": "mch_1", "state": "starting"})

    s = serve(handler)
    client = Bma(api_key="k", base_url=s.url, max_retries=2)
    term = client.beta.terminal_sessions.create(machine_id="mch_1", cols=80)
    assert term.id == "tsn_1"
    assert len(s.seen) == 2
    k1, k2 = (r.headers.get("idempotency-key") for r in s.seen)
    assert k1 and k1 == k2
    assert s.seen[0].method == "POST" and s.seen[0].path == "/v1/terminal_sessions"
    assert json.loads(s.seen[0].body) == {"machine_id": "mch_1", "cols": 80}
    client.beta.terminal_sessions.create(machine_id="mch_1", idempotency_key="mine")
    assert s.seen[2].headers["idempotency-key"] == "mine"


def test_paths_queries_paging_and_error_codes(serve):
    def handler(r, req, n):
        if req.path == "/v1/machine_pools/mpo_1/grants" and "page=" not in req.query:
            r.json(200, {"data": [{"id": "g1"}, {"id": "g2"}], "next_page": "p2"})
        elif req.path == "/v1/machine_pools/mpo_1/grants":
            r.json(200, {"data": [{"id": "g3"}], "next_page": None})
        elif req.path == "/v1/desktop_sessions/dsk_1/pending_actions/pa%2F1/confirm":
            r.json(200, {"type": "desktop_action_result"})
        else:
            r.json(404, {"type": "error", "error": {"type": "not_found_error", "message": "nope", "code": "machine_not_found"}})

    s = serve(handler)
    client = Bma(api_key="k", base_url=s.url)
    ids = [g.id for g in client.beta.machine_pools.grants.list("mpo_1", limit=2, sort="created_at")]
    assert ids == ["g1", "g2", "g3"]
    assert s.seen[0].query == "limit=2&sort=created_at"
    assert s.seen[1].query == "limit=2&sort=created_at&page=p2"
    client.beta.desktop_sessions.confirm_action("dsk_1", "pa/1", generation=1)
    with pytest.raises(NotFoundError) as info:
        client.beta.machines.retrieve("mch_x")
    assert info.value.status_code == 404 and error_code(info.value) == "machine_not_found"
    with pytest.raises(ValueError, match="machine_id"):
        client.beta.machines.retrieve("")
    assert error_code(ValueError("plain")) is None


def test_bma_fields_of_shared_objects(serve):
    session = {
        "id": "ses_1",
        "type": "session",
        "status": "idle",
        "bma_harness": {"kind": "acp", "agent": "claude-code", "placement": "sandbox"},
        "bma_model_override": {"agent_id": "agt_1", "api_format": "openai", "model": "m1", "provider_id": "p", "expires_with_session": True},
    }
    env = {"id": "env_1", "bma_desktop": {"wallpaper": {"file_id": "file_1"}}, "bma_machine": {"machine_id": "mch_1", "source_kind": "machine", "lease": {"session_id": None, "queued_sessions": 0}}}

    def handler(r, req, n):
        r.json(200, env if req.path.startswith("/v1/environments") else {"id": "agt_1", "bma_harness": {"kind": "dsh"}} if req.path.startswith("/v1/agents") else session)

    s = serve(handler)
    client = Bma(api_key="k", base_url=s.url)
    created = client.beta.sessions.create(
        agent="aprf_1",
        environment_id="env_1",
        **bma_sdk.session_options(model_override={"model": "m1", "api_key": "secret"}, harness={"kind": "acp"}),
    )
    body = json.loads(s.seen[0].body)
    assert body["bma_harness"] == {"kind": "acp"} and body["bma_model_override"]["model"] == "m1" and body["environment_id"] == "env_1"
    ext = bma_sdk.session_extensions(created)
    assert ext.harness and ext.harness.placement == "sandbox" and ext.model_override and ext.model_override.model == "m1"

    client.beta.sessions.update("ses_1", **bma_sdk.session_options(model_override=None))
    assert json.loads(s.seen[1].body)["bma_model_override"] is None

    agent = client.beta.agents.update("agt_1", version=1, **bma_sdk.agent_options(harness={"kind": "dsh"}))
    assert bma_sdk.agent_extensions(agent).harness.kind == "dsh"  # type: ignore[union-attr]
    assert json.loads(s.seen[2].body)["bma_harness"] == {"kind": "dsh"}

    environment = client.beta.environments.update("env_1", **bma_sdk.environment_options(desktop={"wallpaper": {"file_id": "file_1"}}))
    e = bma_sdk.environment_extensions(environment)
    assert e.desktop and e.desktop.wallpaper and e.desktop.wallpaper.file_id == "file_1"
    assert e.machine and e.machine.machine_id == "mch_1"
    empty = bma_sdk.session_extensions(client.beta.sessions.update("ses_1"))
    assert empty.harness is not None  # the fake server answers the same session


async def test_async_client_uses_extensions_and_idempotency(serve):
    s = serve(lambda r, req, n: r.json(200, {"type": "machine", "id": "mch_1"}) if req.method != "GET" else r.json(200, {"data": [{"id": "mch_1"}], "next_page": None}))
    client = AsyncBma(api_key="k", base_url=s.url)
    machine = await client.beta.machines.create(machine_pool_id="mpo_1")
    assert machine.id == "mch_1" and s.seen[0].headers["idempotency-key"]
    ids = [m.id async for m in client.beta.machines.list()]
    assert ids == ["mch_1"]
    await client.close()
