"""Answer an agent's custom tool calls with a typed handler."""

from __future__ import annotations

import os
import sys

from pydantic import BaseModel

from bma_sdk import Bma, ToolContext, ToolError, define_tool


class WeatherInput(BaseModel):
    city: str


def get_weather(input: WeatherInput, ctx: ToolContext) -> str:
    if not input.city:
        raise ToolError("city is required")
    return f"Sunny in {input.city}"


weather = define_tool(name="get_weather", description="Current weather", input_model=WeatherInput, run=get_weather)


def main(agent_id: str, session_id: str) -> None:
    with Bma(token=os.environ["BMA_API_KEY"], base_url=os.environ["BMA_BASE_URL"] + "/api/v1") as bma:
        bma.agents.tool_calls.runner(agent_id, session_id=session_id, tools=[weather]).until_done()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
