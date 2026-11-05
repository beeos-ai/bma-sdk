"""define_tool + agents.tool_calls.runner (ADR 0012 D7); mirrors
typescript/test/tools.test.ts."""

from __future__ import annotations

import json
import re
from typing import Any

import httpx
import pytest
from pydantic import BaseModel

from bma_sdk import AsyncBma, Bma, BmaError, ToolContext, ToolError, define_tool

ORG = "org_aaaaaaaaaaaaaaaaaaaaaaaaaa"
PROJECT = "prj_aaaaaaaaaaaaaaaaaaaaaaaaaa"
AGENT = "agt_aaaaaaaaaaaaaaaaaaaaaaaaaa"
SUB = "agt_bbbbbbbbbbbbbbbbbbbbbbbbbb"
SESSION = "ses_aaaaaaaaaaaaaaaaaaaaaaaaaa"
BASE = f"/v1/orgs/{ORG}/projects/{PROJECT}/agents"


def call(id: str, name: str, input: Any, agent: str = AGENT) -> dict[str, Any]:
    return {
        "id": id, "agent_id": agent, "session_id": SESSION, "turn_id": "turn_1", "provider_call_id": "p",
        "name": name, "input": input, "type": "custom", "state": "ready", "created_at": "2026-11-06T00:00:00Z",
    }


class Weather(BaseModel):
    city: str


def run_weather(input: Weather, ctx: ToolContext) -> str:
    assert ctx.tool_call.name == "get_weather"
    if input.city == "Atlantis":
        raise ToolError("no such city")
    return f"Sunny in {input.city}"


weather = define_tool(name="get_weather", description="Current weather", input_model=Weather, run=run_weather)


def test_define_tool_derives_the_agent_config_entry() -> None:
    assert weather.definition["type"] == "custom"
    assert weather.definition["description"] == "Current weather"
    schema = weather.definition["input_schema"]
    assert schema["type"] == "object" and schema["required"] == ["city"]


class Server:
    def __init__(self) -> None:
        self.submitted: dict[str, Any] = {}

    def __call__(self, request: httpx.Request) -> httpx.Response:
        p = request.url.path
        if p == f"{BASE}/{AGENT}/events/stream":
            assert request.url.params["session_id"] == SESSION
            frames = "".join(
                f"event: tool_call_update\ndata: {json.dumps(d)}\n\n"
                for d in (
                    {"tool_call_id": "tc_2", "agent_id": SUB, "state": "ready"},
                    {"tool_call_id": "tc_3", "state": "ready"},
                    {"tool_call_id": "tc_4", "state": "running"},
                )
            )
            return httpx.Response(200, content=frames.encode(), headers={"content-type": "text/event-stream"})
        if p == f"{BASE}/{AGENT}/tool-calls":
            assert request.url.params["state"] == "ready" and request.url.params["type"] == "custom"
            data = [call("tc_1", "get_weather", {"city": "Paris"}), call("tc_9", "other_tool", {})]
            return httpx.Response(200, json={"data": data, "next_cursor": None})
        if p == f"{BASE}/{SUB}/tool-calls/tc_2":
            return httpx.Response(200, json={"tool_call": call("tc_2", "get_weather", {"city": "Atlantis"}, SUB)})
        if p == f"{BASE}/{AGENT}/tool-calls/tc_3":
            return httpx.Response(200, json={"tool_call": call("tc_3", "get_weather", {"town": 1})})
        m = re.search(r"/agents/(agt_\w+)/tool-calls/(tc_\d)/result$", p)
        if m and request.method == "POST":
            self.submitted[m[2]] = {"agent": m[1], **json.loads(request.read())}
            return httpx.Response(201, json={"tool_call": {}, "tool_result": {}})
        raise AssertionError(f"unexpected {request.method} {p}")

    def check(self) -> None:
        assert self.submitted["tc_1"] == {
            "agent": AGENT, "outcome": "succeeded", "content_blocks": [{"type": "text", "text": "Sunny in Paris"}],
        }
        assert self.submitted["tc_2"] == {
            "agent": SUB, "outcome": "failed", "content_blocks": [{"type": "text", "text": "no such city"}],
        }
        invalid = self.submitted["tc_3"]
        assert invalid["outcome"] == "failed"
        assert re.search(r"invalid input for get_weather: city", invalid["content_blocks"][0]["text"])
        assert len(self.submitted) == 3


def test_sync_runner() -> None:
    server = Server()
    with Bma(
        token="t", base_url="https://bma.test/v1", org_id=ORG, project_id=PROJECT,
        http_client=httpx.Client(transport=httpx.MockTransport(server)),
    ) as bma:
        bma.agents.tool_calls.runner(AGENT, session_id=SESSION, tools=[weather]).until_done()
    server.check()


async def test_async_runner() -> None:
    server = Server()

    async def handler(request: httpx.Request) -> httpx.Response:
        await request.aread()
        return server(request)

    async with AsyncBma(
        token="t", base_url="https://bma.test/v1", org_id=ORG, project_id=PROJECT,
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    ) as bma:
        await bma.agents.tool_calls.runner(AGENT, session_id=SESSION, tools=[weather]).until_done()
    server.check()


def test_runner_rejects_duplicate_tool_names() -> None:
    with Bma(token="t", base_url="https://bma.test/v1", org_id=ORG, project_id=PROJECT) as bma, pytest.raises(BmaError):
        bma.agents.tool_calls.runner(AGENT, tools=[weather, weather])
