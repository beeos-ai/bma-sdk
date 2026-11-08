import assert from 'node:assert/strict';
import { afterEach, describe, it } from 'node:test';
import {
  BmaClient,
  DEFAULT_BASE_URL,
  NotFoundError,
  SDK_VERSION,
  agentExtensions,
  environmentExtensions,
  errorCode,
  sessionExtensions,
} from '../src/index.js';
import { json, startServer } from './helpers.js';

const saved = { ...process.env };
afterEach(() => {
  for (const k of Object.keys(process.env)) if (!(k in saved)) delete process.env[k];
  Object.assign(process.env, saved);
});

describe('BmaClient', () => {
  it('reads the BMA environment and never the ANTHROPIC one', async () => {
    const s = await startServer((res) => json(res, 200, { data: [], next_page: null }));
    try {
      process.env.ANTHROPIC_API_KEY = 'anthropic-key';
      process.env.ANTHROPIC_BASE_URL = 'http://127.0.0.1:1';
      process.env.BMA_API_KEY = 'bma-key';
      process.env.BMA_BASE_URL = s.url;
      process.env.BMA_PROJECT_ID = 'proj_1';
      const client = new BmaClient();
      await client.beta.machines.list();
      await client.beta.agents.list();
      assert.deepEqual(s.seen.map((r) => r.path), ['/v1/machines', '/v1/agents']);
      for (const r of s.seen) {
        assert.equal(r.headers.authorization, 'Bearer bma-key');
        assert.equal(r.headers['x-bma-project-id'], 'proj_1');
        assert.equal(r.headers['x-bma-sdk'], `bma-sdk-ts/${SDK_VERSION}`);
      }
    } finally {
      await s.close();
    }
  });

  it('defaults to the hosted origin, requires a key, and keeps its settings in withOptions', async () => {
    delete process.env.BMA_BASE_URL;
    process.env.ANTHROPIC_BASE_URL = 'https://example.invalid';
    assert.equal(new BmaClient({ apiKey: 'k' }).baseURL, DEFAULT_BASE_URL);
    delete process.env.BMA_API_KEY;
    process.env.ANTHROPIC_API_KEY = 'anthropic-key';
    assert.throws(() => new BmaClient(), /BMA_API_KEY/);

    const s = await startServer((res) => json(res, 200, { data: [], next_page: null }));
    try {
      const base = s.client({ project: 'proj_a' });
      const clone = base.withOptions({ maxRetries: 0, project: 'proj_b' });
      assert.ok(clone instanceof BmaClient);
      await base.beta.machines.list();
      await clone.beta.machines.list();
      assert.deepEqual(s.seen.map((r) => r.headers['x-bma-project-id']), ['proj_a', 'proj_b']);
      assert.equal(s.seen[1]?.headers.authorization, 'Bearer bma-key');
    } finally {
      await s.close();
    }
  });

  it('retries an extension create with one idempotency key and honors an explicit one', async () => {
    const s = await startServer((res, _req, n) =>
      n === 1 ?
        json(res, 500, { type: 'error', error: { type: 'api_error', message: 'boom' } })
      : json(res, 200, { type: 'terminal_session', id: 'tsn_1', machine_id: 'mch_1', state: 'starting' }),
    );
    try {
      const client = s.client({ maxRetries: 2 });
      const term = await client.beta.terminalSessions.create({ machine_id: 'mch_1', cols: 80 });
      assert.equal(term.id, 'tsn_1');
      assert.equal(s.seen.length, 2);
      const [k1, k2] = s.seen.map((r) => r.headers['idempotency-key']);
      assert.ok(k1 && k1 === k2, `keys ${k1} ${k2}`);
      assert.equal(s.seen[0]?.method, 'POST');
      assert.equal(s.seen[0]?.path, '/v1/terminal_sessions');
      assert.deepEqual(JSON.parse(s.seen[0]!.body), { machine_id: 'mch_1', cols: 80 });

      await client.beta.terminalSessions.create({ machine_id: 'mch_1' }, { headers: { 'Idempotency-Key': 'mine' } });
      assert.equal(s.seen[2]?.headers['idempotency-key'], 'mine');
    } finally {
      await s.close();
    }
  });

  it('builds paths and queries, pages automatically and reports BMA error codes', async () => {
    const s = await startServer((res, r) => {
      if (r.path === '/v1/machine_pools/mpo_1/grants' && !r.query.includes('page=')) {
        json(res, 200, { data: [{ id: 'g1' }, { id: 'g2' }], next_page: 'p2' });
      } else if (r.path === '/v1/machine_pools/mpo_1/grants') {
        json(res, 200, { data: [{ id: 'g3' }], next_page: null });
      } else if (r.path === '/v1/desktop_sessions/dsk_1/pending_actions/pa%2F1/confirm') {
        json(res, 200, { type: 'desktop_action_result' });
      } else {
        json(res, 404, { type: 'error', error: { type: 'not_found_error', message: 'nope', code: 'machine_not_found' } });
      }
    });
    try {
      const client = s.client();
      const ids: string[] = [];
      for await (const grant of client.beta.machinePools.grants.list('mpo_1', { limit: 2, sort: 'created_at' })) {
        ids.push(String((grant as { id: string }).id));
      }
      assert.deepEqual(ids, ['g1', 'g2', 'g3']);
      assert.equal(s.seen[0]?.query, 'limit=2&sort=created_at');
      assert.equal(s.seen[1]?.query, 'limit=2&sort=created_at&page=p2');

      await client.beta.desktopSessions.confirmAction('dsk_1', 'pa/1', { generation: 1 });

      await assert.rejects(client.beta.machines.retrieve('mch_x'), (err: unknown) => {
        assert.ok(err instanceof NotFoundError);
        assert.equal(err.status, 404);
        assert.equal(err.type, 'not_found_error');
        assert.equal(errorCode(err), 'machine_not_found');
        return true;
      });
      assert.throws(() => client.beta.machines.retrieve(''), /path segment/);
      assert.equal(errorCode(new Error('plain')), undefined);
    } finally {
      await s.close();
    }
  });

  it('reads and writes the bma_* fields of the shared objects', async () => {
    const session = {
      id: 'ses_1',
      type: 'session',
      status: 'idle',
      bma_harness: { kind: 'acp', agent: 'claude-code', placement: 'sandbox' },
      bma_model_override: { agent_id: 'agt_1', api_format: 'openai', model: 'm1', provider_id: 'p', expires_with_session: true },
    };
    const s = await startServer((res, r) =>
      json(res, 200, r.path.startsWith('/v1/environments') ? { id: 'env_1', bma_desktop: { wallpaper: { file_id: 'file_1' } }, bma_machine: { machine_id: 'mch_1', source_kind: 'machine', lease: { session_id: null, queued_sessions: 0 } } } : r.path.startsWith('/v1/agents') ? { id: 'agt_1', bma_harness: { kind: 'dsh' } } : session),
    );
    try {
      const client = s.client();
      const created = await client.beta.sessions.create({
        agent: 'aprf_1',
        environment_id: 'env_1',
        bma_model_override: { model: 'm1', api_key: 'secret' } as never,
        bma_harness: { kind: 'acp' },
      });
      const body = JSON.parse(s.seen[0]!.body);
      assert.deepEqual(body.bma_harness, { kind: 'acp' });
      assert.equal(body.bma_model_override.model, 'm1');
      assert.equal(body.environment_id, 'env_1');
      const ext = sessionExtensions(created);
      assert.equal(ext.harness?.placement, 'sandbox');
      assert.equal(ext.modelOverride?.model, 'm1');

      await client.beta.sessions.update('ses_1', { bma_model_override: null });
      assert.equal(JSON.parse(s.seen[1]!.body).bma_model_override, null);

      const agent = await client.beta.agents.update('agt_1', { version: 1, bma_harness: { kind: 'dsh' } } as never);
      assert.equal(agentExtensions(agent).harness?.kind, 'dsh');
      assert.deepEqual(JSON.parse(s.seen[2]!.body).bma_harness, { kind: 'dsh' });

      const env = await client.beta.environments.update('env_1', { bma_desktop: { wallpaper: { file_id: 'file_1' } } });
      assert.equal(environmentExtensions(env).desktop?.wallpaper?.file_id, 'file_1');
      assert.equal(environmentExtensions(env).machine?.machine_id, 'mch_1');
      assert.deepEqual(sessionExtensions({}), { modelOverride: null, harness: null });
    } finally {
      await s.close();
    }
  });
});
