// defineTool + agents.toolCalls.runner (ADR 0012 D7).
import assert from "node:assert/strict";
import { test } from "node:test";
import { z } from "zod";

import { BmaClient, ToolError, defineTool } from "../src/index.js";

const ORG = "org_aaaaaaaaaaaaaaaaaaaaaaaaaa";
const PROJECT = "prj_aaaaaaaaaaaaaaaaaaaaaaaaaa";
const AGENT = "agt_aaaaaaaaaaaaaaaaaaaaaaaaaa";
const SUB = "agt_bbbbbbbbbbbbbbbbbbbbbbbbbb";
const SESSION = "ses_aaaaaaaaaaaaaaaaaaaaaaaaaa";

const call = (id: string, name: string, input: unknown, agent = AGENT) => ({
  id,
  agent_id: agent,
  session_id: SESSION,
  turn_id: "turn_1",
  provider_call_id: "p",
  name,
  input,
  type: "custom",
  state: "ready",
  created_at: "2026-11-06T00:00:00Z",
});

const weather = defineTool({
  name: "get_weather",
  description: "Current weather",
  inputSchema: z.object({ city: z.string() }),
  run: ({ city }) => {
    if (city === "Atlantis") throw new ToolError("no such city");
    return `Sunny in ${city}`;
  },
});

test("defineTool derives the agent config entry from the schema", () => {
  assert.equal(weather.definition.type, "custom");
  assert.equal(weather.definition.description, "Current weather");
  assert.equal((weather.definition.input_schema as { type: string }).type, "object");
  assert.deepEqual((weather.definition.input_schema as { required: string[] }).required, ["city"]);
});

test("runner: lists ready calls on connect, follows tool_call_update, submits results", async () => {
  const submitted = new Map<string, unknown>();
  let release!: () => void;
  const streamDone = new Promise<void>((r) => (release = r));
  const encoder = new TextEncoder();

  const fetch = (async (input: string | URL | Request, init?: RequestInit) => {
    const url = new URL(String(input));
    const p = url.pathname;
    const base = `/v1/orgs/${ORG}/projects/${PROJECT}/agents`;
    if (p === `${base}/${AGENT}/events/stream`) {
      assert.equal(url.searchParams.get("session_id"), SESSION);
      const body = new ReadableStream<Uint8Array>({
        async start(controller) {
          const frame = (data: unknown) => `event: tool_call_update\ndata: ${JSON.stringify(data)}\n\n`;
          controller.enqueue(encoder.encode(frame({ tool_call_id: "tc_2", agent_id: SUB, state: "ready" })));
          controller.enqueue(encoder.encode(frame({ tool_call_id: "tc_3", state: "ready" })));
          controller.enqueue(encoder.encode(frame({ tool_call_id: "tc_4", state: "running" })));
          await streamDone;
          controller.close();
        },
      });
      init?.signal?.addEventListener("abort", () => release());
      return new Response(body, { headers: { "content-type": "text/event-stream" } });
    }
    if (p === `${base}/${AGENT}/tool-calls`) {
      assert.equal(url.searchParams.get("state"), "ready");
      assert.equal(url.searchParams.get("type"), "custom");
      return Response.json({ data: [call("tc_1", "get_weather", { city: "Paris" }), call("tc_9", "other_tool", {})], next_cursor: null });
    }
    if (p === `${base}/${SUB}/tool-calls/tc_2`) return Response.json({ tool_call: call("tc_2", "get_weather", { city: "Atlantis" }, SUB) });
    if (p === `${base}/${AGENT}/tool-calls/tc_3`) return Response.json({ tool_call: call("tc_3", "get_weather", { town: 1 }) });
    const m = /\/agents\/(agt_\w+)\/tool-calls\/(tc_\d)\/result$/.exec(p);
    if (m && init?.method === "POST") {
      submitted.set(m[2]!, { agent: m[1], ...JSON.parse(String(init.body)) });
      if (submitted.size === 3) release();
      return Response.json({ tool_call: {}, tool_result: {} }, { status: 201 });
    }
    throw new Error(`unexpected ${init?.method ?? "GET"} ${p}`);
  }) as typeof globalThis.fetch;

  const bma = new BmaClient({ token: "t", baseUrl: "https://bma.test/v1", orgId: ORG, projectId: PROJECT, fetch });
  const runner = bma.agents.toolCalls.runner(AGENT, { session_id: SESSION, tools: [weather] });
  await streamDone;
  await runner.stop();

  assert.deepEqual(submitted.get("tc_1"), {
    agent: AGENT,
    outcome: "succeeded",
    content_blocks: [{ type: "text", text: "Sunny in Paris" }],
  });
  assert.deepEqual(submitted.get("tc_2"), {
    agent: SUB,
    outcome: "failed",
    content_blocks: [{ type: "text", text: "no such city" }],
  });
  const invalid = submitted.get("tc_3") as { outcome: string; content_blocks: { text: string }[] };
  assert.equal(invalid.outcome, "failed");
  assert.match(invalid.content_blocks[0]!.text, /invalid input for get_weather: city/);
  assert.equal(submitted.size, 3);
});

test("runner: rides out a clean end of the stream (own reconnect budget) and treats a 409 submit as handled", async () => {
  let connects = 0;
  let submits = 0;
  let finish!: () => void;
  const finished = new Promise<void>((r) => (finish = r));
  const fetch = (async (input: string | URL | Request, init?: RequestInit) => {
    const p = new URL(String(input)).pathname;
    const base = `/v1/orgs/${ORG}/projects/${PROJECT}/agents/${AGENT}`;
    if (p === `${base}/events/stream`) {
      connects++;
      // Every connection ends cleanly, as a server shutting down does.
      const text = connects === 2 ? `event: tool_call_update\ndata: ${JSON.stringify({ tool_call_id: "tc_5", state: "ready" })}\n\n` : "";
      return new Response(text, { headers: { "content-type": "text/event-stream" } });
    }
    if (p === `${base}/tool-calls`) return Response.json({ data: [], next_cursor: null });
    if (p === `${base}/tool-calls/tc_5`) return Response.json({ tool_call: call("tc_5", "get_weather", { city: "Oslo" }) });
    if (p === `${base}/tool-calls/tc_5/result` && init?.method === "POST") {
      submits++;
      finish();
      return Response.json({ error: "already answered", code: "conflict" }, { status: 409 });
    }
    throw new Error(`unexpected ${init?.method ?? "GET"} ${p}`);
  }) as typeof globalThis.fetch;

  const bma = new BmaClient({ token: "t", baseUrl: "https://bma.test/v1", orgId: ORG, projectId: PROJECT, fetch, maxRetries: 0 });
  const runner = bma.agents.toolCalls.runner(AGENT, { tools: [weather] });
  let settled = false;
  void runner.done().then(
    () => (settled = true),
    () => (settled = true),
  );
  await finished;
  await new Promise((r) => setTimeout(r, 20));
  assert.equal(settled, false, "the runner must not stop on a clean end of stream or a 409");
  assert.ok(connects >= 2);
  assert.equal(submits, 1);
  await runner.stop();
});

test("runner: a finite reconnect budget makes done() reject instead of ending silently", async () => {
  const fetch = (async (input: string | URL | Request) => {
    const p = new URL(String(input)).pathname;
    if (p.endsWith("/events/stream")) return new Response("", { headers: { "content-type": "text/event-stream" } });
    return Response.json({ data: [], next_cursor: null });
  }) as typeof globalThis.fetch;
  const bma = new BmaClient({ token: "t", baseUrl: "https://bma.test/v1", orgId: ORG, projectId: PROJECT, fetch });
  const runner = bma.agents.toolCalls.runner(AGENT, { tools: [weather], max_reconnects: 0 });
  await assert.rejects(runner.done(), /event stream ended/);
});
