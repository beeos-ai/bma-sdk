// Live test against a BMA deployment. Runs only with BMA_INTEGRATION=1 and
// BMA_API_KEY, BMA_BASE_URL (origin), BMA_PROJECT_ID and BMA_ORG_ID set:
//
//   BMA_INTEGRATION=1 npm test
//
// It creates an environment (deleted at the end), an agent and a session
// (archived at the end), so it runs against staging, never production.
import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { BmaClient, NotFoundError, eventExtensions, errorCode, environmentExtensions, agentExtensions, sessionExtensions } from '../src/index.js';
import { toFile } from '@anthropic-ai/sdk';

const live = process.env.BMA_INTEGRATION === '1';
const MODEL = 'deepseek-flash';

type Frame = { type: string; id?: string; [k: string]: any };

function requireEnv() {
  for (const k of ['BMA_API_KEY', 'BMA_BASE_URL', 'BMA_PROJECT_ID', 'BMA_ORG_ID']) {
    assert.ok(process.env[k], `${k} is not set`);
  }
  assert.ok(!process.env.BMA_BASE_URL!.includes('api.bma.beeos.ai'), 'refusing to run the live test against production');
}

/** A fetch whose first event-stream body fails after `cutAfter` frames; records the Last-Event-ID of later connections. */
function cuttingFetch(cutAfter: number) {
  const state = { conns: 0, resumes: [] as string[] };
  const fetcher = async (input: any, init?: any) => {
    const res = await fetch(input, init);
    const url = String(input?.url ?? input);
    if (!url.endsWith('/events/stream')) return res;
    state.conns++;
    if (state.conns > 1) {
      state.resumes.push(new Headers(init?.headers).get('last-event-id') ?? '');
      return res;
    }
    const reader = res.body!.getReader();
    const decoder = new TextDecoder();
    let frames = 0;
    let pending = '';
    const body = new ReadableStream({
      async pull(controller) {
        if (frames >= cutAfter) return controller.error(new TypeError('terminated'));
        const { done, value } = await reader.read();
        if (done) return controller.close();
        pending += decoder.decode(value, { stream: true });
        let out = '';
        for (let i = pending.indexOf('\n\n'); i >= 0 && frames < cutAfter; i = pending.indexOf('\n\n')) {
          const chunk = pending.slice(0, i + 2);
          pending = pending.slice(i + 2);
          out += chunk;
          if (chunk.includes('data:')) frames++;
        }
        controller.enqueue(new TextEncoder().encode(out));
      },
      cancel: () => reader.cancel(),
    });
    return new Response(body, { status: res.status, headers: res.headers });
  };
  return { state, fetcher: fetcher as typeof fetch };
}

async function waitFor(stream: AsyncIterator<Frame>, type: string, timeoutMs: number, seen?: (f: Frame) => void): Promise<Frame> {
  const deadline = Date.now() + timeoutMs;
  for (;;) {
    const left = deadline - Date.now();
    if (left <= 0) throw new Error(`timed out waiting for ${type}`);
    const next = await Promise.race([
      stream.next(),
      new Promise<never>((_, reject) => setTimeout(() => reject(new Error(`timed out after ${timeoutMs}ms waiting for ${type}`)), left)),
    ]);
    if (next.done) throw new Error(`stream ended while waiting for ${type}`);
    const f = next.value;
    seen?.(f);
    if (f.type === 'session.error') throw new Error(`session.error: ${JSON.stringify(f)} (bma_error_code ${eventExtensions(f).errorCode})`);
    if (f.type === type) return f;
  }
}

const text = (t: string) => [{ type: 'user.message' as const, content: [{ type: 'text' as const, text: t }] }];

describe('staging', { skip: !live, timeout: 15 * 60_000 }, () => {
  it('runs the CMA scenarios and the BMA extensions against a deployment', async (t) => {
    requireEnv();
    const suffix = `sdk-ts2-it-${Math.floor(Date.now() / 1000)}`;
    const cut = cuttingFetch(3);
    const c = new BmaClient({ fetch: cut.fetcher });
    const plain = new BmaClient();

    await t.test('error', async () => {
      await assert.rejects(c.beta.machines.retrieve('mch_doesnotexist0000000000000'), (err: any) => {
        assert.ok(err instanceof NotFoundError);
        assert.equal(err.status, 404);
        assert.equal(err.type, 'not_found_error');
        assert.ok(err.requestID);
        console.log(`404 not_found_error request_id=${err.requestID} code=${errorCode(err)}`);
        return true;
      });
    });

    const env = await c.beta.environments.create({ name: suffix, config: { type: 'cloud' } as never });
    t.after(async () => {
      // Delete, not archive: each environment is a machine pool.
      await c.beta.environments.delete(env.id).catch((e) => console.error(`delete environment ${env.id}: ${e}`));
    });
    environmentExtensions(env);
    console.log(`environment ${env.id}`);

    const agent = await c.beta.agents.create(
      {
        name: suffix,
        model: { id: MODEL },
        system: "You are a test agent. Follow the user's instructions exactly and keep answers to one sentence.",
        tools: [
          { type: 'agent_toolset_20260401' },
          {
            type: 'custom',
            name: 'get_weather',
            description: 'Returns the current weather of a city.',
            input_schema: { type: 'object', properties: { city: { type: 'string' } }, required: ['city'] },
          },
        ],
      } as never,
      { headers: { 'Idempotency-Key': `${suffix}-agent` } },
    );
    t.after(async () => {
      await c.beta.agents.archive(agent.id).catch((e) => console.error(`archive agent ${agent.id}: ${e}`));
    });
    agentExtensions(agent);
    console.log(`agent ${agent.id}`);

    const session = await c.beta.sessions.create(
      { agent: agent.id, environment_id: env.id, title: suffix },
      { headers: { 'Idempotency-Key': `${suffix}-session` } },
    );
    t.after(async () => {
      await c.beta.sessions.archive(session.id).catch((e) => console.error(`archive session ${session.id}: ${e}`));
    });
    console.log(`session ${session.id} status ${session.status} model_override=${sessionExtensions(session).modelOverride != null}`);

    // Message, custom tool round trip and stream resumption: the first
    // connection is cut after a few frames; stream() must reconnect with
    // Last-Event-ID and lose nothing.
    await t.test('custom_tool_and_resume', async () => {
      const stream = await c.beta.sessions.events.stream(session.id);
      const it = stream[Symbol.asyncIterator]() as AsyncIterator<Frame>;
      const got: string[] = [];
      const streamed = new Set<string>();
      let firstSeq = 0;
      let lastSeq = 0;
      const record = (f: Frame) => {
        const seq = eventExtensions(f).sequence ?? 0;
        console.log(`frame ${f.type} bma_sequence=${seq} id=${f.id}`);
        if (seq === 0) {
          if (f.id) {
            assert.ok(!streamed.has(f.id), `event ${f.id} returned twice`);
            streamed.add(f.id);
            got.push(f.id);
          }
          return;
        }
        assert.ok(seq >= lastSeq && !streamed.has(f.id!), `event ${f.id} (sequence ${seq} after ${lastSeq}): duplicate or out of order`);
        if (firstSeq === 0) firstSeq = seq;
        lastSeq = seq;
        streamed.add(f.id!);
        got.push(f.id!);
      };
      try {
        await c.beta.sessions.events.send(session.id, {
          events: text('Call the get_weather tool for the city Paris. After you get the result, reply with one sentence that repeats it.'),
        });
        const use = await waitFor(it, 'agent.custom_tool_use', 4 * 60_000, record);
        assert.equal(use.name, 'get_weather');
        console.log(`agent.custom_tool_use ${use.id} input=${JSON.stringify(use.input)}`);
        await c.beta.sessions.events.send(session.id, {
          events: [{ type: 'user.custom_tool_result', custom_tool_use_id: use.id!, content: [{ type: 'text', text: 'Sunny, 21 degrees Celsius.' }] }],
        });
        await waitFor(it, 'agent.message', 4 * 60_000, record);
        await waitFor(it, 'session.status_idle', 2 * 60_000, record);
      } finally {
        stream.controller.abort();
      }
      assert.ok(cut.state.conns >= 2 && cut.state.resumes.length > 0, `stream was not resumed: connections ${cut.state.conns}, Last-Event-ID ${cut.state.resumes}`);

      // Every persisted event from the first streamed one on must have arrived once.
      const listed: string[] = [];
      for await (const ev of c.beta.sessions.events.list(session.id)) {
        const seq = eventExtensions(ev).sequence ?? 0;
        if (seq >= firstSeq && seq <= lastSeq && (seq > firstSeq || streamed.has(ev.id))) listed.push(ev.id);
      }
      for (const id of got) assert.ok(listed.includes(id), `streamed event ${id} is not in the list`);
      // Known server gap: a resumed stream replays durable events but not the
      // derived session.status_* events (sesst_ ids) of the list.
      const missing = listed.filter((id) => !streamed.has(id));
      for (const id of missing) assert.ok(id.startsWith('sesst_'), `event ${id} was not streamed (streamed ${got}, listed ${listed})`);
      console.log(`resumed after cut: connections=${cut.state.conns} Last-Event-ID=${cut.state.resumes}; ${got.length} durable events (sequences ${firstSeq}..${lastSeq}) streamed once each and found in the list; omitted derived ${missing}`);
    });

    await t.test('interrupt', async () => {
      const stream = await plain.beta.sessions.events.stream(session.id);
      const it = stream[Symbol.asyncIterator]() as AsyncIterator<Frame>;
      try {
        await plain.beta.sessions.events.send(session.id, { events: text('Use the bash tool to run exactly: sleep 120 && echo finished') });
        await waitFor(it, 'agent.tool_use', 4 * 60_000);
        const start = Date.now();
        await plain.beta.sessions.events.send(session.id, { events: [{ type: 'user.interrupt' }] });
        const idle = await waitFor(it, 'session.status_idle', 90_000);
        console.log(`interrupted: session.status_idle after ${Date.now() - start}ms (stop_reason ${idle.stop_reason?.type})`);
      } finally {
        stream.controller.abort();
      }
    });

    await t.test('files', async () => {
      const content = `hello from bma-sdk ts 2.0 ${suffix}`;
      const meta = await c.beta.files.upload({ file: await toFile(Buffer.from(content), `${suffix}.txt`, { type: 'text/plain' }) });
      try {
        const got = await c.beta.files.retrieveMetadata(meta.id);
        assert.equal(got.filename, `${suffix}.txt`);
        const res = await c.beta.files.download(meta.id);
        assert.equal(await res.text(), content);
        const resource = await c.beta.sessions.resources.add(session.id, { type: 'file', file_id: meta.id });
        await c.beta.sessions.resources.delete(resource.id, { session_id: session.id });
        console.log(`file ${meta.id} uploaded, read back, mounted as ${resource.id} and unmounted`);
      } finally {
        await c.beta.files.delete(meta.id);
      }
    });

    await t.test('organization_and_pools', async () => {
      const projects = await c.beta.organization.projects.list(process.env.BMA_ORG_ID!);
      const pools = await c.beta.machinePools.list();
      console.log(`projects page ${projects.data.length}, machine pools page ${pools.data.length}`);
    });

    await t.test('machines_terminal_desktop', async (st) => {
      const online: any[] = [];
      for await (const m of c.beta.machines.list({ limit: 20 })) if ((m as any).connection_state === 'online') online.push(m);
      if (online.length === 0) return st.skip('no online machine in the project');
      const m = await c.beta.machines.retrieve(online[0].id);
      console.log(`machine ${m.id} online (${online.length} online of the listed)`);

      const term = await c.beta.terminalSessions.create({ machine_id: m.id });
      const ticket: any = await c.beta.terminalSessions.tickets.create(term.id, {});
      assert.ok(ticket.ticket && ticket.ws_url && ticket.purpose === 'connect', `terminal ticket purpose ${ticket.purpose} ws_url ${ticket.ws_url}`);
      const closed: any = await c.beta.terminalSessions.close(term.id);
      console.log(`terminal ${term.id}: ticket purpose=${ticket.purpose} ws_url=${ticket.ws_url}; closed state=${closed.state}`);

      let desk: any;
      const refusals: string[] = [];
      for (const cand of online) {
        try {
          desk = await c.beta.desktopSessions.create({ machine_id: cand.id, read_only: true }, { maxRetries: 0 });
          break;
        } catch (err) {
          refusals.push(`${cand.id}: ${errorCode(err)}`);
        }
      }
      if (!desk) return st.skip(`no online machine provides a desktop (${refusals})`);
      const dt: any = await c.beta.desktopSessions.tickets.create(desk.id, {});
      assert.ok(dt.ticket && dt.purpose === 'watch');
      await c.beta.desktopSessions.retrieve(desk.id);
      await c.beta.desktopSessions.close(desk.id);
      console.log(`desktop ${desk.id}: watch ticket ws_url=${dt.ws_url}; closed`);
    });
  });
});
