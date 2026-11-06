// Runtime behaviour of the resource client: scope defaults, request shape,
// retries and idempotency keys (ADR 0012 D3), errors, pagination and the
// event stream. Uses an in-process fetch stub; contract.test.ts replays the
// recorded contract fixtures over HTTP.
import assert from "node:assert/strict";
import { test } from "node:test";

import {
  DEFAULT_BASE_URL,
  APIConnectionError,
  APIConnectionTimeoutError,
  APIUserAbortError,
  AuthenticationError,
  BmaApiError,
  BmaClient,
  BmaError,
  ConflictError,
  EventStreamError,
  InternalServerError,
  NotFoundError,
  RateLimitError,
  ServiceUnavailableError,
  type AgentStreamEvent,
} from "../src/index.js";
import { FacadeExtensionsClient } from "../src/facade-extensions.js";

interface Call {
  method: string;
  url: URL;
  headers: Headers;
  body: string | FormData | null;
}

type Reply = Response | Error | ((call: Call) => Response | Error | Promise<Response | Error>);

function stub(replies: Reply[]) {
  const calls: Call[] = [];
  const fetch = async (input: string | URL | Request, init?: RequestInit): Promise<Response> => {
    const raw = init?.body;
    const call: Call = {
      method: init?.method ?? "GET",
      url: new URL(String(input)),
      headers: new Headers(init?.headers),
      body: raw instanceof FormData ? raw : raw == null ? null : new TextDecoder().decode(await new Response(raw).arrayBuffer()),
    };
    calls.push(call);
    let reply = replies.shift();
    if (reply === undefined) throw new Error(`unexpected request ${call.method} ${call.url}`);
    if (typeof reply === "function") reply = await reply(call);
    if (reply instanceof Error) throw reply;
    return reply;
  };
  return { calls, fetch: fetch as typeof globalThis.fetch };
}

const json = (status: number, body: unknown, headers: Record<string, string> = {}) =>
  new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json", ...headers } });
const apiError = (status: number, code: string, headers: Record<string, string> = {}) =>
  json(status, { error: `${code} happened`, code }, headers);
const refused = () => Object.assign(new TypeError("fetch failed"), { cause: Object.assign(new Error("connect"), { code: "ECONNREFUSED" }) });
const reset = () => Object.assign(new TypeError("fetch failed"), { cause: Object.assign(new Error("socket"), { code: "ECONNRESET" }) });

const BASE = "https://bma.test";
const ORG = "org_aaaaaaaaaaaaaaaaaaaaaaaaaa";
const PROJECT = "prj_aaaaaaaaaaaaaaaaaaaaaaaaaa";
const AGENT = "agt_aaaaaaaaaaaaaaaaaaaaaaaaaa";
const SESSION = "ses_aaaaaaaaaaaaaaaaaaaaaaaaaa";

function client(replies: Reply[], extra: Partial<ConstructorParameters<typeof BmaClient>[0]> = {}) {
  const s = stub(replies);
  const bma = new BmaClient({ token: "t", baseUrl: BASE, orgId: ORG, projectId: PROJECT, fetch: s.fetch, ...extra });
  return { bma, calls: s.calls };
}

test("scope defaults fill the path; params override them", async () => {
  const { bma, calls } = client([json(200, { agent: {} }), json(200, { agent: {} })]);
  await bma.agents.retrieve(AGENT);
  await bma.agents.retrieve(AGENT, { project_id: "prj_bbbbbbbbbbbbbbbbbbbbbbbbbb" });
  assert.equal(calls[0]!.url.pathname, `/api/v1/orgs/${ORG}/projects/${PROJECT}/agents/${AGENT}`);
  assert.equal(calls[1]!.url.pathname, `/api/v1/orgs/${ORG}/projects/prj_bbbbbbbbbbbbbbbbbbbbbbbbbb/agents/${AGENT}`);
  assert.equal(calls[0]!.headers.get("authorization"), "Bearer t");
});

test("a missing scope is a client error, not a request", async () => {
  const { bma, calls } = client([], { orgId: undefined, projectId: undefined });
  await assert.rejects(bma.agents.list(), (e: unknown) => e instanceof BmaError && /orgId/.test(String(e)));
  assert.equal(calls.length, 0);
});

test("scope defaults come from BMA_ORG_ID / BMA_PROJECT_ID", async () => {
  process.env.BMA_ORG_ID = ORG;
  process.env.BMA_PROJECT_ID = PROJECT;
  try {
    const s = stub([json(200, { data: [], next_cursor: null })]);
    const bma = new BmaClient({ token: "t", baseUrl: BASE, fetch: s.fetch });
    await bma.agents.list();
    assert.equal(s.calls[0]!.url.pathname, `/api/v1/orgs/${ORG}/projects/${PROJECT}/agents`);
  } finally {
    delete process.env.BMA_ORG_ID;
    delete process.env.BMA_PROJECT_ID;
  }
});

test("params split into query, header and JSON body", async () => {
  const { bma, calls } = client([json(201, { agent_input: {} })]);
  await bma.agents.inputs.create(
    AGENT,
    { session_id: SESSION, content_blocks: [{ type: "text", text: "hi" }], delivery_mode: "queued" },
    { idempotencyKey: "input-1" },
  );
  const c = calls[0]!;
  assert.equal(c.method, "POST");
  assert.equal(c.url.searchParams.get("session_id"), SESSION);
  assert.equal(c.headers.get("idempotency-key"), "input-1");
  assert.equal(c.headers.get("content-type"), "application/json");
  assert.deepEqual(JSON.parse(c.body as string), { content_blocks: [{ type: "text", text: "hi" }], delivery_mode: "queued" });
});

test("array and deepObject query parameters", async () => {
  const { bma, calls } = client([json(200, {}), json(200, { data: [], next_cursor: null })]);
  await bma.orgs.usage({ include_project_ids: [PROJECT, "prj_bbbbbbbbbbbbbbbbbbbbbbbbbb"] });
  await bma.orgs.secrets.list({ metadata: { team: "a", env: "b" } });
  assert.deepEqual(calls[0]!.url.searchParams.getAll("include_project_ids"), [PROJECT, "prj_bbbbbbbbbbbbbbbbbbbbbbbbbb"]);
  assert.equal(calls[1]!.url.searchParams.get("metadata[team]"), "a");
  assert.equal(calls[1]!.url.searchParams.get("metadata[env]"), "b");
});

test("binary upload sends the body as is; binary download returns the Response", async () => {
  const { bma, calls } = client([json(201, { id: "file_1" }), new Response("bytes", { status: 200 })]);
  await bma.files.upload({ filename: "a.txt", body: "hello", file_metadata: '{"k":"v"}' }, { idempotencyKey: "u-1" });
  assert.equal(calls[0]!.headers.get("content-type"), "application/octet-stream");
  assert.equal(calls[0]!.headers.get("x-bma-file-metadata"), '{"k":"v"}');
  assert.equal(calls[0]!.body, "hello");
  const res = await bma.files.download("file_1");
  assert.equal(await res.text(), "bytes");
});

test("multipart bodies: files as parts, JSON-encoded fields as JSON", async () => {
  const { bma, calls } = client([json(201, { id: "skl_1" })]);
  await bma.orgs.skills.create({ owner: { kind: "org" } as never, archive: new File(["zip"], "skill.zip") });
  const form = calls[0]!.body as FormData;
  assert.ok(form instanceof FormData);
  assert.equal(form.get("owner"), JSON.stringify({ kind: "org" }));
  assert.equal((form.get("archive") as File).name, "skill.zip");
});

test("204 resolves to undefined", async () => {
  const { bma } = client([new Response(null, { status: 204 })]);
  assert.equal(await bma.agents.machines.delete(AGENT, "mch_1"), undefined);
});

test("errors map to status subclasses with a typed code", async () => {
  const cases: [number, string, new (...a: never[]) => BmaApiError][] = [
    [401, "unauthorized", AuthenticationError],
    [404, "not_found", NotFoundError],
    [409, "state_transition_conflict", ConflictError],
  ];
  for (const [status, code, cls] of cases) {
    const { bma } = client([apiError(status, code)]);
    await assert.rejects(bma.agents.retrieve(AGENT), (e: unknown) => {
      assert.ok(e instanceof cls, `${status} -> ${cls.name}`);
      assert.ok(e instanceof BmaApiError);
      assert.equal(e.status, status);
      assert.equal(e.code, code);
      return true;
    });
  }
});

test("GET retries 5xx and connection errors, honouring retry-after-ms", async () => {
  const { bma, calls } = client([apiError(500, "internal_error", { "retry-after-ms": "1" }), reset(), json(200, { agent: {} })]);
  await bma.agents.retrieve(AGENT);
  assert.equal(calls.length, 3);
});

test("maxRetries bounds the attempts and the last error surfaces", async () => {
  const { bma, calls } = client(
    [apiError(503, "service_unavailable", { "retry-after-ms": "1" }), apiError(503, "service_unavailable", { "retry-after-ms": "1" })],
    { maxRetries: 1 },
  );
  await assert.rejects(bma.agents.retrieve(AGENT), ServiceUnavailableError);
  assert.equal(calls.length, 2);
});

test("409 is never retried", async () => {
  const { bma, calls } = client([apiError(409, "idempotency_key_conflict")]);
  await assert.rejects(bma.agents.create({ name: "a" } as never), ConflictError);
  assert.equal(calls.length, 1);
});

test("idempotent writes reuse one generated Idempotency-Key across retries", async () => {
  const { bma, calls } = client([apiError(500, "internal_error", { "retry-after-ms": "1" }), reset(), json(201, { agent: {} })]);
  await bma.agents.create({ name: "a" } as never);
  assert.equal(calls.length, 3);
  const keys = calls.map((c) => c.headers.get("idempotency-key"));
  assert.match(keys[0]!, /^bma-sdk-retry-[0-9a-f-]{36}$/);
  assert.deepEqual(keys, [keys[0], keys[0], keys[0]]);
});

test("writes without an idempotency key retry only undelivered, 429 and 503", async () => {
  const { bma: a, calls: ca } = client([apiError(500, "internal_error")]);
  await assert.rejects(a.agents.sessions.create(AGENT), InternalServerError);
  assert.equal(ca.length, 1);

  const { bma: b, calls: cb } = client([reset()]);
  await assert.rejects(b.agents.sessions.create(AGENT), APIConnectionError);
  assert.equal(cb.length, 1);

  const { bma: c, calls: cc } = client([
    refused(),
    apiError(429, "rate_limited", { "retry-after-ms": "1" }),
    json(201, { session: { id: SESSION } }),
  ], { maxRetries: 2 });
  await c.agents.sessions.create(AGENT);
  assert.equal(cc.length, 3);

  const { bma: d, calls: cd } = client([apiError(429, "rate_limited", { "retry-after-ms": "1" })], { maxRetries: 0 });
  await assert.rejects(d.agents.sessions.create(AGENT), RateLimitError);
  assert.equal(cd.length, 1);
});

test("an operation without the header rejects an explicit idempotency key", async () => {
  const { bma, calls } = client([]);
  await assert.rejects(bma.agents.sessions.create(AGENT, {}, { idempotencyKey: "x" }), BmaError);
  assert.equal(calls.length, 0);
});

test("timeout and user abort", async () => {
  const slowFetch = ((_: unknown, init?: RequestInit) =>
    new Promise<Response>((_resolve, reject) => {
      init?.signal?.addEventListener("abort", () => reject(init.signal!.reason));
    })) as typeof globalThis.fetch;
  const bma = new BmaClient({ token: "t", baseUrl: BASE, orgId: ORG, projectId: PROJECT, fetch: slowFetch, maxRetries: 0, timeout: 20 });
  await assert.rejects(bma.agents.retrieve(AGENT), APIConnectionTimeoutError);
  const controller = new AbortController();
  const pending = bma.agents.retrieve(AGENT, {}, { signal: controller.signal, timeout: 10_000 });
  controller.abort();
  await assert.rejects(pending, APIUserAbortError);
});

test("cursor pages: await gives the first page, for await walks every item", async () => {
  const page = (ids: string[], next: string | null) => json(200, { data: ids.map((id) => ({ id })), next_cursor: next });
  const { bma, calls } = client([page(["a", "b"], "c1"), page(["a", "b"], "c1"), page(["c"], null)]);
  const first = await bma.agents.list({ limit: 2 });
  assert.deepEqual(first.data.map((a) => a.id), ["a", "b"]);
  assert.equal(first.hasNextPage(), true);
  const ids: string[] = [];
  for await (const agent of bma.agents.list({ limit: 2 })) ids.push(agent.id);
  assert.deepEqual(ids, ["a", "b", "c"]);
  assert.equal(calls[2]!.url.searchParams.get("cursor"), "c1");
  assert.equal(calls[2]!.url.searchParams.get("limit"), "2");
});

function sse(frames: { event: string; id?: string; data: unknown }[], status = 200) {
  const body = frames
    .map((f) => `: keep-alive\n\nevent: ${f.event}\n${f.id ? `id: ${f.id}\n` : ""}data: ${JSON.stringify(f.data)}\n\n`)
    .join("");
  return new Response(body, { status, headers: { "content-type": "text/event-stream" } });
}

test("event stream: discriminated frames; service_unavailable reconnects with Last-Event-ID", async () => {
  const { bma, calls } = client([
    sse([
      { event: "agent_input", id: "5", data: { sequence: 5 } },
      { event: "tool_call_update", data: { tool_call_id: "tc_1", state: "ready" } },
      { event: "error", data: { error: "restarting", code: "service_unavailable" } },
    ]),
    sse([{ event: "model_output", id: "6", data: { sequence: 6 } }]),
  ]);
  const seen: AgentStreamEvent[] = await take(bma.agents.events.stream(AGENT, { session_id: SESSION, after_sequence: 2 }), 3);
  assert.deepEqual(
    seen.map((e) => [e.event, "sequence" in e ? e.sequence : undefined]),
    [["agent_input", 5], ["tool_call_update", undefined], ["model_output", 6]],
  );
  assert.equal(calls[0]!.headers.get("accept"), "text/event-stream");
  assert.equal(calls[0]!.url.searchParams.get("after_sequence"), "2");
  assert.equal(calls[1]!.headers.get("last-event-id"), "5");
  assert.equal(calls[1]!.url.searchParams.get("session_id"), SESSION);
  assert.equal(calls[1]!.url.searchParams.get("after_sequence"), null);
});

test("event stream: a terminal error frame throws EventStreamError", async () => {
  const { bma, calls } = client([sse([{ event: "error", data: { error: "gone", code: "forbidden" } }])]);
  await assert.rejects(
    (async () => {
      for await (const _ of bma.agents.events.stream(AGENT)) void _;
    })(),
    (e: unknown) => e instanceof EventStreamError && e.code === "forbidden",
  );
  assert.equal(calls.length, 1);
});

// --- Review typed-sdk-review-1.0: EventSource reconnection, timeouts, pages --

function rawSSE(text: string) {
  return new Response(text, { status: 200, headers: { "content-type": "text/event-stream" } });
}

async function take<T>(iterable: AsyncIterable<T>, n: number): Promise<T[]> {
  const out: T[] = [];
  for await (const item of iterable) {
    out.push(item);
    if (out.length === n) break;
  }
  return out;
}

test("event stream: a clean end of the response reconnects with Last-Event-ID (EventSource)", async () => {
  const { bma, calls } = client([
    rawSSE('event: model_output\nid: 5\ndata: {"sequence":5}\n\n'),
    rawSSE('event: model_output\nid: 6\ndata: {"sequence":6}\n\n'),
  ]);
  const seen = await take(bma.agents.events.stream(AGENT, { after_sequence: 1 }), 2);
  assert.deepEqual(seen.map((e) => ("sequence" in e ? e.sequence : undefined)), [5, 6]);
  assert.equal(calls.length, 2);
  assert.equal(calls[1]!.headers.get("last-event-id"), "5");
  assert.equal(calls[1]!.url.searchParams.get("after_sequence"), null);
});

test("event stream: an unterminated frame at the end is discarded and the stream reconnects", async () => {
  const { bma, calls } = client([
    rawSSE('event: model_output\nid: 6\ndata: {"sequence":6}\n\nevent: model_output\nid: 7\ndata: {"seq'),
    rawSSE('event: model_output\nid: 7\ndata: {"sequence":7}\n\n'),
  ]);
  const seen = await take(bma.agents.events.stream(AGENT), 2);
  assert.deepEqual(seen.map((e) => ("sequence" in e ? e.sequence : undefined)), [6, 7]);
  assert.equal(calls[1]!.headers.get("last-event-id"), "6");
});

test("event stream: reconnects without data spend maxRetries, then the stream throws", async () => {
  const { bma, calls } = client([rawSSE(""), apiError(503, "service_unavailable"), refused()], { maxRetries: 2 });
  await assert.rejects(take(bma.agents.events.stream(AGENT), 1), APIConnectionError);
  assert.equal(calls.length, 3);
});

test("event stream: data (a heartbeat) resets the reconnect budget", async () => {
  const { bma, calls } = client(
    [rawSSE(": heartbeat\n\n"), rawSSE(": heartbeat\n\n"), rawSSE('event: model_output\nid: 9\ndata: {"sequence":9}\n\n')],
    { maxRetries: 1 },
  );
  const seen = await take(bma.agents.events.stream(AGENT), 1);
  assert.equal(seen.length, 1);
  assert.equal(calls.length, 3);
});

test("event stream: CRLF split across chunks is one line ending", async () => {
  const enc = new TextEncoder();
  const chunks = ["event: model_output\r", "\nid: 3\r\ndata: {\"sequence\":3}\r", "\n\r", "\n"];
  const body = new ReadableStream<Uint8Array>({
    start(c) {
      for (const chunk of chunks) c.enqueue(enc.encode(chunk));
      c.close();
    },
  });
  const { bma } = client([new Response(body, { status: 200 })]);
  const [ev] = await take(bma.agents.events.stream(AGENT), 1);
  assert.equal(ev!.event, "model_output");
});

test("timeout 0 disables the per-attempt timeout", async () => {
  const slow = ((_: unknown, init?: RequestInit) =>
    new Promise<Response>((resolve, reject) => {
      const t = setTimeout(() => resolve(json(200, { agent: {} })), 30);
      init?.signal?.addEventListener("abort", () => {
        clearTimeout(t);
        reject(init.signal!.reason);
      });
    })) as typeof globalThis.fetch;
  const bma = new BmaClient({ token: "t", baseUrl: BASE, orgId: ORG, projectId: PROJECT, fetch: slow, timeout: 0, maxRetries: 0 });
  await bma.agents.retrieve(AGENT);
  const bounded = new BmaClient({ token: "t", baseUrl: BASE, orgId: ORG, projectId: PROJECT, fetch: slow, timeout: 5, maxRetries: 0 });
  await bounded.agents.retrieve(AGENT, {}, { timeout: 0 });
  await assert.rejects(bounded.agents.retrieve(AGENT), APIConnectionTimeoutError);
});

test("uploads have no default wall-clock timeout; a per-call timeout still applies", async () => {
  const slow = ((_: unknown, init?: RequestInit) =>
    new Promise<Response>((resolve, reject) => {
      const t = setTimeout(() => resolve(json(201, { id: "file_1" })), 40);
      init?.signal?.addEventListener("abort", () => {
        clearTimeout(t);
        reject(init.signal!.reason);
      });
    })) as typeof globalThis.fetch;
  const bma = new BmaClient({ token: "t", baseUrl: BASE, orgId: ORG, projectId: PROJECT, fetch: slow, timeout: 5, maxRetries: 0 });
  await bma.files.upload({ body: "x", filename: "a.txt" });
  await assert.rejects(bma.files.upload({ body: "x", filename: "a.txt" }, { timeout: 5 }), APIConnectionTimeoutError);
});

test("aborting while the body is read rejects with APIUserAbortError", async () => {
  const controller = new AbortController();
  const hanging = ((_: unknown, init?: RequestInit) => {
    const body = new ReadableStream<Uint8Array>({
      start(c) {
        c.enqueue(new TextEncoder().encode('{"agent":'));
        init?.signal?.addEventListener("abort", () => c.error(init.signal!.reason));
      },
    });
    return Promise.resolve(new Response(body, { status: 200, headers: { "content-type": "application/json" } }));
  }) as typeof globalThis.fetch;
  const bma = new BmaClient({ token: "t", baseUrl: BASE, orgId: ORG, projectId: PROJECT, fetch: hanging });
  const pending = bma.agents.retrieve(AGENT, {}, { signal: controller.signal });
  setTimeout(() => controller.abort(), 10);
  await assert.rejects(pending, APIUserAbortError);
});

test("BMA_TOKEN and BMA_BASE_URL are the defaults of token and baseUrl", async () => {
  const s = stub([json(200, { agent: {} })]);
  process.env.BMA_TOKEN = "env-token";
  process.env.BMA_BASE_URL = "https://env.test/";
  try {
    const bma = new BmaClient({ orgId: ORG, projectId: PROJECT, fetch: s.fetch });
    await bma.agents.retrieve(AGENT);
  } finally {
    delete process.env.BMA_TOKEN;
    delete process.env.BMA_BASE_URL;
  }
  assert.equal(s.calls[0]!.headers.get("authorization"), "Bearer env-token");
  assert.equal(s.calls[0]!.url.origin, "https://env.test");
  assert.equal(s.calls[0]!.url.pathname, `/api/v1/orgs/${ORG}/projects/${PROJECT}/agents/${AGENT}`);
  assert.throws(() => new BmaClient({ baseUrl: BASE }), BmaError);
});

test("baseUrl is the origin: /api/v1 is appended once, a trailing /api/v1 is not repeated", async () => {
  assert.equal(DEFAULT_BASE_URL, "https://api.bma.beeos.ai");
  for (const baseUrl of ["https://bma.test", "https://bma.test/", "https://bma.test/api/v1", "https://bma.test/api/v1/"]) {
    const s = stub([json(200, { agent: {} })]);
    await new BmaClient({ token: "t", baseUrl, orgId: ORG, projectId: PROJECT, fetch: s.fetch }).agents.retrieve(AGENT);
    assert.equal(s.calls[0]!.url.href, `https://bma.test/api/v1/orgs/${ORG}/projects/${PROJECT}/agents/${AGENT}`, baseUrl);
  }
  const s = stub([json(200, { agent: {} })]);
  await new BmaClient({ token: "t", baseUrl: "https://gw.test/bma", orgId: ORG, projectId: PROJECT, fetch: s.fetch }).agents.retrieve(AGENT);
  assert.equal(s.calls[0]!.url.pathname, `/bma/api/v1/orgs/${ORG}/projects/${PROJECT}/agents/${AGENT}`);
  assert.equal(new FacadeExtensionsClient({ apiKey: "k", baseUrl: "https://bma.test/api/v1/" }).baseUrl, "https://bma.test");
  assert.throws(() => new FacadeExtensionsClient({ apiKey: "k", baseUrl: "https://bma.test/v1" }), BmaError);
});

test("lists with {data, next_<param>} paginate: events, sessions, files", async () => {
  const { bma, calls } = client([
    json(200, { data: [{ sequence: 1 }, { sequence: 2 }], next_after_sequence: 2, next_before_sequence: null, has_more: true }),
    json(200, { data: [{ sequence: 3 }], next_after_sequence: 3, next_before_sequence: null, has_more: false }),
    json(200, { data: [{ sequence: 9 }], next_after_sequence: 9, next_before_sequence: 8, has_more: true }),
    json(200, { data: [{ sequence: 8 }], next_after_sequence: 8, next_before_sequence: null, has_more: false }),
    json(200, { data: [{ id: "ses_1" }], next_before_id: "ses_1" }),
    json(200, { data: [], next_before_id: null }),
    json(200, { data: [{ id: "file_1" }], next_page: "p2" }),
    json(200, { data: [{ id: "file_2" }], next_page: null }),
  ]);
  const forward: number[] = [];
  for await (const ev of bma.agents.events.list(AGENT, { session_id: SESSION })) forward.push(ev.sequence);
  assert.deepEqual(forward, [1, 2, 3]);
  assert.equal(calls[1]!.url.searchParams.get("after_sequence"), "2");
  const backward: number[] = [];
  for await (const ev of bma.agents.events.list(AGENT, { before_sequence: 0 })) backward.push(ev.sequence);
  assert.deepEqual(backward, [9, 8]);
  assert.equal(calls[3]!.url.searchParams.get("before_sequence"), "8");
  const sessions: string[] = [];
  for await (const s of bma.agents.sessions.list(AGENT)) sessions.push(s.id);
  assert.deepEqual(sessions, ["ses_1"]);
  assert.equal(calls[5]!.url.searchParams.get("before_id"), "ses_1");
  const page = await bma.files.list();
  assert.equal(page.hasNextPage(), true);
  const next = await page.getNextPage();
  assert.equal(next.data[0]!.id, "file_2");
  assert.equal(calls[7]!.url.searchParams.get("page"), "p2");
});

test("binary responses are named download", async () => {
  const { bma, calls } = client([new Response("bytes", { status: 200 })]);
  const res = await bma.files.download("file_1");
  assert.equal(await res.text(), "bytes");
  assert.match(calls[0]!.url.pathname, /\/files\/file_1\/content$/);
});
