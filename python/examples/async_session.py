"""The session example with AsyncBma."""

from __future__ import annotations

import asyncio
import os
import sys

from bma_sdk import AsyncBma


async def main(agent_id: str) -> None:
    async with AsyncBma(token=os.environ["BMA_API_KEY"], base_url=os.environ["BMA_BASE_URL"] + "/api/v1") as bma:
        created = await bma.agents.sessions.create(agent_id)
        await bma.agents.inputs.create(
            agent_id, session_id=created.session.id, content_blocks=[{"type": "text", "text": "Start the task."}]
        )
        async for ev in bma.agents.events.stream(agent_id, session_id=created.session.id):
            if ev.event == "model_output":
                print(ev.sequence, ev.data.content_blocks)
        first = await bma.agents.list(limit=10)
        print([a.id for a in first.data], first.has_next_page())


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))
