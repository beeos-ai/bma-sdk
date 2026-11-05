"""Create a session on an existing agent, send input and stream its events.

    BMA_BASE_URL=... BMA_API_KEY=... BMA_ORG_ID=... BMA_PROJECT_ID=... python examples/session.py agt_...
"""

from __future__ import annotations

import os
import sys

from bma_sdk import Bma, ConflictError, NotFoundError


def main(agent_id: str) -> None:
    with Bma(
        token=os.environ["BMA_API_KEY"],
        base_url=os.environ["BMA_BASE_URL"],
        org_id=os.environ.get("BMA_ORG_ID"),  # default scope of every method
        project_id=os.environ.get("BMA_PROJECT_ID"),
    ) as bma:
        created = bma.agents.sessions.create(agent_id, idempotency_key="task-1")
        session = created.session
        bma.agents.inputs.create(
            agent_id,
            session_id=session.id,
            content_blocks=[{"type": "text", "text": "Start the task."}],
        )
        for ev in bma.agents.events.stream(agent_id, session_id=session.id, stream_deltas=True):
            if ev.event == "model_output":
                print(ev.sequence, ev.data.content_blocks)  # ev.data: ModelOutputEvent
            elif ev.event == "tool_call_update":
                print(ev.data.tool_call_id, ev.data.state)

        for agent in bma.agents.list(limit=50):  # every page
            print(agent.id, agent.name)

        try:
            bma.agents.retrieve("agt_zzzzzzzzzzzzzzzzzzzzzzzzzz")
        except NotFoundError as e:
            print(e.status, e.code)
        except ConflictError:
            raise


if __name__ == "__main__":
    main(sys.argv[1])
