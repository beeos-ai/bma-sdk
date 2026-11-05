"""Custom tools (ADR 0012 D7). A BMA custom tool call stays ``ready`` until a
consumer submits its result (``submitToolCallResult``); this module gives that
consumer a typed shape, after the Anthropic SDKs' pydantic tool helpers and
``sessions.events.tool_runner``.

    class Weather(BaseModel):
        city: str

    weather = define_tool(name="get_weather", description="Current weather",
                          input_model=Weather, run=lambda w, ctx: f"Sunny in {w.city}")
    bma.agents.tool_calls.runner(agent_id, session_id=session_id, tools=[weather]).until_done()
"""

from __future__ import annotations

import asyncio
import inspect
import threading
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict, Generic, List, Optional, Sequence, Set, TypeVar, Union, cast

import pydantic

from .._core import RequestOptions
from .._errors import BmaError
from .._generated.rest import models as _models
from .._generated.rest import operations as _ops
from .._generated.rest.params import AgentConfigDefinitionToolParam, SubmitToolResultContentBlockParam
from .._resource import AsyncAPIResource, SyncAPIResource

__all__ = [
    "AsyncToolCallsBase",
    "AsyncToolRunner",
    "RunnableTool",
    "ToolCallsBase",
    "ToolContext",
    "ToolError",
    "ToolOutput",
    "ToolRunner",
    "define_tool",
]

M = TypeVar("M", bound=pydantic.BaseModel)

ToolOutput = Union[str, List[SubmitToolResultContentBlockParam]]
"""What a tool returns: text, or result content blocks."""


class ToolError(Exception):
    """Raise from ``run`` to report a failed call with this content to the model."""

    def __init__(self, content: ToolOutput) -> None:
        super().__init__(content if isinstance(content, str) else "tool error")
        self.content = content


@dataclass(frozen=True)
class ToolContext:
    tool_call: _models.ToolCall


@dataclass(frozen=True)
class RunnableTool(Generic[M]):
    name: str
    definition: AgentConfigDefinitionToolParam
    """Agent config entry for ``tools.<name>``."""
    input_model: type[M]
    run: Callable[[M, ToolContext], Union[ToolOutput, Awaitable[ToolOutput]]]

    def parse(self, input: object) -> M:
        try:
            return self.input_model.model_validate(input)
        except pydantic.ValidationError as e:
            detail = "; ".join(
                (".".join(str(p) for p in err["loc"]) + ": " if err["loc"] else "") + err["msg"] for err in e.errors()[:5]
            )
            raise ToolError(f"invalid input for {self.name}: {detail}") from e


def define_tool(
    *,
    name: str,
    description: str,
    input_model: type[M],
    run: Callable[[M, ToolContext], Union[ToolOutput, Awaitable[ToolOutput]]],
) -> RunnableTool[M]:
    """Defines a custom tool from a pydantic model. The input is validated
    before ``run`` sees it; the agent config JSON Schema comes from the model."""
    schema = cast(Dict[str, Any], input_model.model_json_schema())
    if schema.get("type") != "object":
        raise BmaError(f"bma: input schema of tool {name} must be an object")
    definition: AgentConfigDefinitionToolParam = {
        "type": "custom",
        "description": description,
        "input_schema": cast(Any, schema),
    }
    return RunnableTool(name, definition, input_model, run)


def _content(output: ToolOutput) -> List[SubmitToolResultContentBlockParam]:
    return [{"type": "text", "text": output}] if isinstance(output, str) else output


def _wanted(call: _models.ToolCall, tools: Dict[str, RunnableTool[Any]], agent_id: str, session_id: Optional[str]) -> bool:
    if call.type != "custom" or call.state != "ready" or call.name not in tools:
        return False
    return not (session_id and call.agent_id == agent_id and call.session_id != session_id)


def _index(tools: Sequence[RunnableTool[Any]]) -> Dict[str, RunnableTool[Any]]:
    index = {t.name: t for t in tools}
    if len(index) != len(tools):
        raise BmaError("bma: tool names must be unique")
    return index


class ToolRunner:
    """Runs custom tools of one agent (and its subagents) until stopped or the
    event stream ends. Tools run one at a time on the calling thread."""

    def __init__(self, resource: "ToolCallsBase", agent_id: str, session_id: Optional[str], tools: Dict[str, RunnableTool[Any]], scope: Dict[str, str]) -> None:
        self._client = resource._client
        self._agent_id = agent_id
        self._session_id = session_id
        self._tools = tools
        self._scope = scope
        self._seen: Set[str] = set()
        self._lock = threading.Lock()
        self._stream: Any = None
        self._stopped = False

    def _handle(self, call: _models.ToolCall) -> None:
        with self._lock:
            if not _wanted(call, self._tools, self._agent_id, self._session_id) or call.id in self._seen:
                return
            self._seen.add(call.id)
        tool = self._tools[call.name]
        outcome = "succeeded"
        try:
            output = tool.run(tool.parse(call.input), ToolContext(call))
            if inspect.isawaitable(output):
                raise BmaError(f"bma: tool {tool.name} is async; use AsyncBma")
        except ToolError as e:
            outcome, output = "failed", e.content
        except BmaError:
            raise
        except Exception as e:  # the tool's own failure is reported to the model
            outcome, output = "failed", str(e)
        self._client._request(
            _ops.submitToolCallResult,
            {"agentID": call.agent_id, "toolCallID": call.id},
            {**self._scope, "outcome": outcome, "content_blocks": _content(cast(ToolOutput, output))},
            RequestOptions(),
            None,
        )

    def _sweep(self) -> None:
        page = self._client._page(
            _ops.listToolCalls, {"agentID": self._agent_id},
            {**self._scope, "state": "ready", "type": "custom", "include_subagents": True},
            RequestOptions(), _models.ToolCall,
        )
        for call in page:
            self._handle(call)

    def until_done(self) -> None:
        """Runs until the event stream ends or ``stop()`` is called. Ready
        calls are listed on every (re)connection, so calls that became ready
        while disconnected are not lost."""
        params: Dict[str, object] = dict(self._scope)
        if self._session_id:
            params["session_id"] = self._session_id
        self._stream = self._client._stream(
            _ops.streamEvents, {"agentID": self._agent_id}, params, RequestOptions(),
            _models.StreamEventsEvent_EVENTS, on_open=self._sweep,
        )
        for event in self._stream:
            if self._stopped:
                break
            if not isinstance(event, _models.StreamEventsEventToolCallUpdate) or event.data.state != "ready":
                continue
            envelope = self._client._request(
                _ops.getToolCall,
                {"agentID": event.data.agent_id or self._agent_id, "toolCallID": event.data.tool_call_id},
                self._scope, RequestOptions(), _models.ToolCallEnvelope,
            )
            self._handle(envelope.tool_call)

    def stop(self) -> None:
        """Stops listening; safe to call from another thread."""
        self._stopped = True
        if self._stream is not None:
            self._stream.close()


class AsyncToolRunner:
    """Runs custom tools concurrently on the event loop."""

    def __init__(self, resource: "AsyncToolCallsBase", agent_id: str, session_id: Optional[str], tools: Dict[str, RunnableTool[Any]], scope: Dict[str, str]) -> None:
        self._client = resource._client
        self._agent_id = agent_id
        self._session_id = session_id
        self._tools = tools
        self._scope = scope
        self._seen: Set[str] = set()
        self._running: Set["asyncio.Task[None]"] = set()
        self._failure: Optional[BaseException] = None
        self._main: Optional["asyncio.Task[None]"] = None

    def _spawn(self, coro: Awaitable[None]) -> None:
        task = asyncio.ensure_future(coro)
        self._running.add(task)

        def done(t: "asyncio.Task[None]") -> None:
            self._running.discard(t)
            if not t.cancelled() and t.exception() is not None and self._failure is None:
                self._failure = t.exception()
                if self._main is not None:
                    self._main.cancel()

        task.add_done_callback(done)

    async def _run(self, call: _models.ToolCall) -> None:
        tool = self._tools[call.name]
        outcome = "succeeded"
        try:
            output = tool.run(tool.parse(call.input), ToolContext(call))
            if inspect.isawaitable(output):
                output = await output
        except ToolError as e:
            outcome, output = "failed", e.content
        except Exception as e:  # the tool's own failure is reported to the model
            outcome, output = "failed", str(e)
        await self._client._request(
            _ops.submitToolCallResult,
            {"agentID": call.agent_id, "toolCallID": call.id},
            {**self._scope, "outcome": outcome, "content_blocks": _content(cast(ToolOutput, output))},
            RequestOptions(),
            None,
        )

    def _handle(self, call: _models.ToolCall) -> None:
        if not _wanted(call, self._tools, self._agent_id, self._session_id) or call.id in self._seen:
            return
        self._seen.add(call.id)
        self._spawn(self._run(call))

    async def _sweep(self) -> None:
        paginator = self._client._page(
            _ops.listToolCalls, {"agentID": self._agent_id},
            {**self._scope, "state": "ready", "type": "custom", "include_subagents": True},
            RequestOptions(), _models.ToolCall,
        )
        async for call in paginator:
            self._handle(call)

    async def _listen(self) -> None:
        params: Dict[str, object] = dict(self._scope)
        if self._session_id:
            params["session_id"] = self._session_id
        stream = self._client._stream(
            _ops.streamEvents, {"agentID": self._agent_id}, params, RequestOptions(),
            _models.StreamEventsEvent_EVENTS, on_open=lambda: self._spawn(self._sweep()),
        )
        async for event in stream:
            if not isinstance(event, _models.StreamEventsEventToolCallUpdate) or event.data.state != "ready":
                continue
            envelope = await self._client._request(
                _ops.getToolCall,
                {"agentID": event.data.agent_id or self._agent_id, "toolCallID": event.data.tool_call_id},
                self._scope, RequestOptions(), _models.ToolCallEnvelope,
            )
            self._handle(envelope.tool_call)

    async def until_done(self) -> None:
        """Runs until the event stream ends or ``stop()`` is called, then waits
        for running tools; raises the error that stopped it."""
        self._main = asyncio.ensure_future(self._listen())
        try:
            await self._main
        except asyncio.CancelledError:
            if self._failure is None and not self._main.cancelled():
                raise
        while self._running:
            await asyncio.gather(*list(self._running), return_exceptions=True)
        if self._failure is not None:
            raise self._failure

    def stop(self) -> None:
        if self._main is not None:
            self._main.cancel()


def _scope(org_id: Optional[str], project_id: Optional[str]) -> Dict[str, str]:
    scope: Dict[str, str] = {}
    if org_id:
        scope["org_id"] = org_id
    if project_id:
        scope["project_id"] = project_id
    return scope


class ToolCallsBase(SyncAPIResource):
    def runner(
        self,
        agent_id: str,
        *,
        tools: Sequence[RunnableTool[Any]],
        session_id: Optional[str] = None,
        org_id: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> ToolRunner:
        """Runs custom tools for an agent: every ``ready`` custom call (of the
        agent and its subagents) whose name matches a tool is parsed, run, and
        its result submitted. ``session_id`` limits the agent's own calls to
        one session; subagent calls are always handled."""
        return ToolRunner(self, agent_id, session_id, _index(tools), _scope(org_id, project_id))


class AsyncToolCallsBase(AsyncAPIResource):
    def runner(
        self,
        agent_id: str,
        *,
        tools: Sequence[RunnableTool[Any]],
        session_id: Optional[str] = None,
        org_id: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> AsyncToolRunner:
        """Async variant of :meth:`ToolCallsBase.runner`; tools may be async."""
        return AsyncToolRunner(self, agent_id, session_id, _index(tools), _scope(org_id, project_id))
