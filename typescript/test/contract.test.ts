// Replays contracts/bma/fixtures/sdk-contract.json against the SDK through a
// local HTTP server. tools/check_contract.py validates the fixtures against
// the OpenAPI contracts.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createServer, type IncomingMessage, type ServerResponse } from "node:http";
import type { AddressInfo } from "node:net";
import { resolve } from "node:path";
import { test } from "node:test";

import { BmaClient, ConflictError, NotFoundError, type AgentModelOverrideInput, type Artifact } from "../src/index.js";
import { FacadeExtensionsClient, bmaSequence } from "../src/facade-extensions.js";

interface Case {
  name: string;
  request: {
    method: string;
    path: string;
    query?: Record<string, string>;
    headers?: Record<string, string>;
    json?: unknown;
    text?: string;
    multipart?: { field: string; filename: string; text: string };
  };
  response: {
    status: number;
    json?: unknown;
    text?: string;
    content_type?: string;
    sse?: { comment?: string; event?: string; id?: string; data?: unknown }[];
  };
}

const fixtures = JSON.parse(
  readFileSync(resolve(process.cwd(), "../contracts/bma/fixtures/sdk-contract.json"), "utf8"),
) as { scope: Record<string, string>; rest: Case[]; facade: Case[] };
const s = fixtures.scope as Record<string, string>;

function find(cases: Case[], name: string): Case {
  const found = cases.find((c) => c.name === name);
  assert.ok(found, `fixture ${name}`);
  return found;
}

async function readBody(req: IncomingMessage): Promise<Buffer> {
  const chunks: Buffer[] = [];
  for await (const chunk of req) chunks.push(chunk as Buffer);
  return Buffer.concat(chunks);
}

function check(c: Case, prefix: string, req: IncomingMessage, body: Buffer): void {
  const url = new URL(req.url ?? "/", "http://localhost");
  assert.equal(req.method, c.request.method, `${c.name} method`);
  assert.equal(url.pathname, prefix + c.request.path, `${c.name} path`);
  assert.deepEqual(Object.fromEntries(url.searchParams), c.request.query ?? {}, `${c.name} query`);
  for (const [key, value] of Object.entries(c.request.headers ?? {})) {
    assert.equal(req.headers[key.toLowerCase()], value, `${c.name} header ${key}`);
  }
  if (c.request.json !== undefined) {
    assert.deepEqual(JSON.parse(body.toString("utf8")), c.request.json, `${c.name} body`);
  } else if (c.request.text !== undefined) {
    assert.equal(req.headers["content-type"], "application/octet-stream", `${c.name} content type`);
    assert.equal(body.toString("utf8"), c.request.text, `${c.name} body`);
  } else if (c.request.multipart) {
    const { field, filename, text } = c.request.multipart;
    const raw = body.toString("utf8");
    assert.match(String(req.headers["content-type"]), /^multipart\/form-data; boundary=/);
    assert.ok(raw.includes(`name="${field}"; filename="${filename}"`), `${c.name} multipart header`);
    assert.ok(raw.includes(`\r\n\r\n${text}\r\n`), `${c.name} multipart content`);
  } else {
    assert.ok(body.length === 0 || body.toString() === "{}", `${c.name} unexpected body`);
  }
}

function reply(c: Case, res: ServerResponse): void {
  const r = c.response;
  if (r.sse) {
    res.writeHead(r.status, { "Content-Type": "text/event-stream" });
    for (const frame of r.sse) {
      if (frame.comment) {
        res.write(`: ${frame.comment}\n\n`);
        continue;
      }
      if (frame.event) res.write(`event: ${frame.event}\n`);
      if (frame.id) res.write(`id: ${frame.id}\n`);
      res.write(`data: ${JSON.stringify(frame.data)}\n\n`);
    }
    res.end();
  } else if (r.json !== undefined) {
    res.writeHead(r.status, { "Content-Type": "application/json" });
    res.end(JSON.stringify(r.json));
  } else {
    res.writeHead(r.status, { "Content-Type": r.content_type ?? "application/octet-stream" });
    res.end(r.text ?? "");
  }
}

/** Serves exactly one recorded exchange and returns its base URL. */
async function serve(c: Case, prefix: string): Promise<{ url: string; close: () => void; errors: unknown[] }> {
  const errors: unknown[] = [];
  const server = createServer(async (req, res) => {
    const body = await readBody(req);
    try {
      check(c, prefix, req, body);
    } catch (error) {
      errors.push(error);
      res.writeHead(418).end();
      return;
    }
    reply(c, res);
  });
  await new Promise<void>((done) => server.listen(0, "127.0.0.1", done));
  const { port } = server.address() as AddressInfo;
  return { url: `http://127.0.0.1:${port}${prefix}`, close: () => server.close(), errors };
}

async function withRest<T>(name: string, run: (client: BmaClient, c: Case) => Promise<T>): Promise<T> {
  const c = find(fixtures.rest, name);
  const server = await serve(c, "/api/v1");
  try {
    const result = await run(new BmaClient({ baseUrl: server.url, token: "test-token", orgId: s.org!, projectId: s.project!, maxRetries: 0 }), c);
    assert.deepEqual(server.errors, []);
    return result;
  } finally {
    server.close();
  }
}

async function withFacade<T>(name: string, run: (client: FacadeExtensionsClient) => Promise<T>): Promise<T> {
  const c = find(fixtures.facade, name);
  const server = await serve(c, "");
  try {
    const client = new FacadeExtensionsClient({ baseUrl: server.url, apiKey: "test-key", projectId: s.project, maxRetries: 0 });
    const result = await run(client);
    assert.deepEqual(server.errors, []);
    return result;
  } finally {
    server.close();
  }
}

const override = (): AgentModelOverrideInput => ({
  model: "deepseek-flash",
  provider: {
    api_format: "openai-chat-completions",
    base_url: "https://llm.example.com",
    api_variant: "default",
    endpoint_path: "/v1/chat/completions",
  },
  api_key: "sk-test-0000000000",
  ttl_seconds: 3600,
  expires_with_session: true,
});

test("session lifecycle", async () => {
  const created = await withRest("create_session", (bma) =>
    bma.agents.sessions.create(s.agent!, {
      agent_config_id: s.config,
      idempotency_key: "beework-task-1",
      metadata: { title: "Quarterly report" },
      model_override: override(),
    }),
  );
  assert.equal(created.session.id, s.session);
  assert.equal(created.session.status, "idle");

  const got = await withRest("get_session", (bma) => bma.agents.sessions.retrieve(s.agent!, s.session!));
  assert.equal(got.session.next_event_sequence, 5);
  assert.equal(got.session.status, "running");

  const listed = await withRest("list_sessions", (bma) =>
    bma.agents.sessions.list(s.agent!, { include_archived: true, limit: 10 }),
  );
  assert.equal(listed.data.length, 1);

  const archived = await withRest("archive_session", (bma) => bma.agents.sessions.archive(s.agent!, s.session!));
  assert.equal(archived.session.state, "archived");
  assert.equal(archived.session.status, "terminated");

  const mo = await withRest("put_session_model_override", (bma) =>
    bma.agents.sessions.modelOverride.set(s.agent!, s.session!, override()),
  );
  assert.equal(mo.model_override.expires_with_session, true);
  assert.equal(mo.model_override.expires_at, null);
});

test("session input and event stream", async () => {
  const input = await withRest("create_session_input", (bma) =>
    bma.agents.inputs.create(
      s.agent!,
      { session_id: s.session, content_blocks: [{ type: "text", text: "Summarize the report." }], delivery_mode: "queued" },
      { idempotencyKey: "turn-1" },
    ),
  );
  assert.equal(input.agent_input.state, "queued");

  // The recorded stream ends with a terminal (non service_unavailable) error frame.
  const frames: [string, number | undefined][] = [];
  await assert.rejects(
    withRest("stream_session_events", async (bma) => {
      for await (const ev of bma.agents.events.stream(s.agent!, { session_id: s.session, stream_deltas: true, last_event_id: 4 })) {
        frames.push([ev.event, "sequence" in ev ? ev.sequence : undefined]);
      }
    }),
    (e: unknown) => e instanceof Error && e.name === "EventStreamError",
  );
  assert.deepEqual(frames, [
    ["agent_input", 5],
    ["tool_call_update", undefined],
  ]);
});

test("artifact download verifies size and digest", async () => {
  const artifact = find(fixtures.rest, "get_artifact").response.json as Artifact;
  const bytes = await withRest("get_artifact_content", (bma) => bma.agents.artifacts.downloadVerified(artifact, { maxBytes: 1024 }));
  assert.equal(new TextDecoder().decode(bytes), "hello world");

  await assert.rejects(
    withRest("get_artifact_content", (bma) =>
      bma.agents.artifacts.downloadVerified({ ...artifact, digest: `sha256:${"0".repeat(64)}` }, { maxBytes: 1024 }),
    ),
    /digest mismatch/,
  );
});

test("machines: desktop session, terminal ticket, typed errors", async () => {
  const desktop = await withRest("create_desktop_session", (bma) =>
    bma.machines.desktopSessions.create(s.machine!, { agent_id: s.agent, read_only: true }),
  );
  assert.equal(desktop.capabilities.width, 1920);

  const ticket = await withRest("create_terminal_ticket", (bma) =>
    bma.machines.terminalSessions.connectionTicket(s.machine!, s.terminal_session!, { ttl_seconds: 60 }),
  );
  assert.equal(ticket.purpose, "terminal_connect");

  await assert.rejects(
    withRest("get_agent_not_found", (bma) => bma.agents.retrieve("agt_zzzzzzzzzzzzzzzzzzzzzzzzzz")),
    (error: unknown) => error instanceof NotFoundError && error.status === 404 && error.code === "not_found",
  );
});

test("files: upload, mount into a session, list outputs", async () => {
  const file = await withRest("upload_file", (bma, c) =>
    bma.files.upload({ filename: "report.pdf", body: c.request.text! }, { idempotencyKey: "upload-report-1" }),
  );
  assert.equal(file.id, s.file);
  assert.equal(file.scope, null);

  const mounted = await withRest("add_session_file_resource", (bma) =>
    bma.agents.sessions.resources.add(s.agent!, s.session!, {
      type: "file",
      file_id: file.id,
      mount_path: "/mnt/session/uploads/reports/report.pdf",
    }),
  );
  assert.equal(mounted.file_id, s.mounted_file);
  assert.equal(mounted.mount_path, "/mnt/session/uploads/reports/report.pdf");

  const outputs = await withRest("list_session_outputs", (bma) => bma.files.list({ scope_id: s.session }));
  assert.deepEqual(
    outputs.data.map((f) => [f.id, f.scope?.id]),
    [[s.output_file, s.session]],
  );
  assert.equal(outputs.next_page, null);
});

test("agent machines: create, list, delete", async () => {
  const created = await withRest("create_agent_machine", (bma) =>
    bma.agents.machines.create(
      s.agent!,
      { template: "base-2c4g", machine_pool_id: s.pool, display_name: "Ada's workstation" },
      { idempotencyKey: "machine-ada-1" },
    ),
  );
  assert.equal(created.kind, "persistent");
  assert.equal(created.cpu, null);

  const listed = await withRest("list_agent_machines", (bma) => bma.agents.machines.list(s.agent!));
  assert.deepEqual(
    listed.data.map((m) => [m.id, m.connection_state, m.cpu]),
    [[s.machine, "online", 2]],
  );

  const deleted = await withRest("delete_agent_machine", (bma) => bma.agents.machines.delete(s.agent!, s.machine!));
  assert.equal(deleted, undefined);
});

test("facade extensions: desktop stream and session files", async () => {
  const stream = await withFacade("desktop_stream", (ext) =>
    ext.sessions.desktop.stream(s.session!, {
      desktop_session_id: s.desktop_session!,
      ttl_seconds: 60,
      origin: "https://app.example.com",
    }),
  );
  assert.equal(stream.type, "bma.desktop_stream");
  assert.equal(stream.ticket, "watch-ticket");

  const file = await withFacade("upload_session_file", (ext) =>
    ext.sessions.files.upload(s.session!, { file: new File(["meeting notes"], "notes.txt") }),
  );
  assert.equal(file.size_bytes, 13);

  const page = await withFacade("list_session_files", (ext) => ext.sessions.files.list(s.session!, { limit: 1 }));
  assert.equal(page.next_page, "1");

  await assert.rejects(
    withFacade("upload_session_file_conflict", (ext) =>
      ext.sessions.files.upload(s.session!, { file: new File(["again"], "dup.txt") }),
    ),
    (error: unknown) => error instanceof ConflictError && error.status === 409 && error.code === "file_already_exists",
  );

  assert.equal(bmaSequence({ type: "agent.message", bma_sequence: 42 } as { bma_sequence: number }), 42);
  assert.equal(bmaSequence({}), undefined);
  assert.throws(() => new FacadeExtensionsClient({ baseUrl: "https://x.example/v1", apiKey: "k" }));
});

test("facade extensions: session resources", async () => {
  const resource = await withFacade("add_session_resource", (ext) =>
    ext.sessions.resources.add(s.session!, { type: "file", file_id: s.file!, mount_path: "reports/report.pdf" }),
  );
  assert.equal(resource.id, s.resource);
  assert.equal(resource.file_id, s.file);
  assert.equal(resource.mount_path, "reports/report.pdf");

  const page = await withFacade("list_session_resources", (ext) => ext.sessions.resources.list(s.session!));
  assert.equal(page.data.length, 1);
  assert.equal(page.data[0]!.id, s.resource);

  const deleted = await withFacade("delete_session_resource", (ext) => ext.sessions.resources.delete(s.session!, s.resource!));
  assert.equal(deleted.type, "session_resource_deleted");
});
