"""Static type assertions, checked by pyright (strict) in CI: every line
marked ``pyright: ignore[...]`` must be an error, because
reportUnnecessaryTypeIgnoreComment fails the build if it is not."""

from __future__ import annotations

from typing_extensions import assert_type

from bma_sdk import Bma, SyncCursorPage
from bma_sdk.types import Agent, AgentSessionEnvelope


def check(bma: Bma) -> None:
    assert_type(bma.agents.sessions.create("agt_x"), AgentSessionEnvelope)
    assert_type(bma.agents.list(), SyncCursorPage[Agent])

    bma.agents.sessions.create("agt_x", no_such_field=1)  # pyright: ignore[reportCallIssue]
    bma.agents.inputs.create("agt_x")  # pyright: ignore[reportCallIssue]
    bma.agents.inputs.create("agt_x", content_blocks=[{"type": "txt", "text": "hi"}])  # pyright: ignore[reportArgumentType]
    bma.agents.sessions.create("agt_x", idempotency_key=1)  # pyright: ignore[reportArgumentType]

    for ev in bma.agents.events.stream("agt_x"):
        if ev.event == "tool_call_update":
            ev.data.tool_call_id
            ev.sequence  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
