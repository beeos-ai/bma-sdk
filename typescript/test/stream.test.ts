import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { NotFoundError } from '../src/index.js';
import { streamResume } from '../src/resume.js';
import { frame, json, startServer } from './helpers.js';

streamResume.backoffMs = 1;
streamResume.maxBackoffMs = 1;

function sse(res: import('node:http').ServerResponse, ...frames: string[]) {
  if (!res.headersSent) res.writeHead(200, { 'content-type': 'text/event-stream' });
  for (const f of frames) res.write(f);
}

describe('events.stream', () => {
  it('resumes with Last-Event-ID and returns every event once', async () => {
    const s = await startServer((res, _r, n) => {
      switch (n) {
        case 1: // two events of sequence 1, an announcement, then the connection ends
          sse(res, frame('session.status_running', 'sesst_1_run', 1), frame('user.message', 'evt_1', 1), frame('session.status_idle', 'sesst_x', 0));
          return res.end();
        case 2: // the server resumes after sequence 0: replays sequence 1
          sse(res, frame('session.status_running', 'sesst_1_run', 1), frame('user.message', 'evt_1', 1), frame('session.status_idle', 'sesst_x', 1), frame('agent.message', 'evt_2', 2), 'event: ping\ndata: {}\n\n');
          return res.end();
        case 3:
          sse(res, frame('session.status_idle', 'sesst_2_idle', 2));
          return res.end();
        default:
          return json(res, 404, { type: 'error', error: { type: 'not_found_error', message: 'gone' } });
      }
    });
    try {
      const stream = await s.client({ maxRetries: 0 }).beta.sessions.events.stream('ses_1');
      const got: string[] = [];
      await assert.rejects(
        (async () => {
          for await (const event of stream) got.push((event as { id: string }).id);
        })(),
        (err: unknown) => err instanceof NotFoundError,
      );
      assert.deepEqual(got, ['sesst_1_run', 'evt_1', 'sesst_x', 'evt_2', 'sesst_2_idle']);
      assert.equal(s.seen.length, 4);
      assert.deepEqual(s.seen.slice(0, 3).map((r) => r.headers['last-event-id']), [undefined, '0', '1']);
      assert.equal(s.seen[0]?.headers['anthropic-beta'], 'managed-agents-2026-04-01');
      assert.equal(s.seen[0]?.path, '/v1/sessions/ses_1/events/stream');
    } finally {
      await s.close();
    }
  });

  it('resumes after a connection that dies in the middle of a frame', async () => {
    const s = await startServer((res, _r, n) => {
      if (n === 1) {
        sse(res, frame('user.message', 'evt_1', 1), 'event: agent.message\ndata: {"type":"agent.mess');
        return setTimeout(() => res.destroy(), 20);
      }
      sse(res, frame('user.message', 'evt_1', 1), frame('agent.message', 'evt_2', 2));
      return res.end();
    });
    try {
      streamResume.maxReconnects = 1;
      const stream = await s.client({ maxRetries: 0 }).beta.sessions.events.stream('ses_1');
      const got: string[] = [];
      for await (const event of stream) {
        got.push((event as { id: string }).id);
        if (got.length === 2) break;
      }
      assert.deepEqual(got, ['evt_1', 'evt_2']);
      assert.equal(s.seen[1]?.headers['last-event-id'], '0');
    } finally {
      streamResume.maxReconnects = 5;
      await s.close();
    }
  });

  it('gives up after maxReconnects failed attempts in a row', async () => {
    const s = await startServer((res) => {
      res.writeHead(200, { 'content-type': 'text/event-stream' });
      res.end();
    });
    try {
      const stream = await s.client({ maxRetries: 0 }).beta.sessions.events.stream('ses_1');
      await assert.rejects(
        (async () => {
          for await (const _ of stream) void _;
        })(),
        /not resumed after 5 attempts/,
      );
      assert.equal(s.seen.length, 1 + 5);
    } finally {
      await s.close();
    }
  });

  it('stops when the stream is aborted', async () => {
    streamResume.backoffMs = 60_000;
    streamResume.maxBackoffMs = 60_000;
    const s = await startServer((res) => {
      sse(res, frame('user.message', 'evt_1', 1));
      res.end();
    });
    try {
      const stream = await s.client({ maxRetries: 0 }).beta.sessions.events.stream('ses_1');
      const got: string[] = [];
      setTimeout(() => stream.controller.abort(), 50);
      for await (const event of stream) got.push((event as { id: string }).id);
      assert.deepEqual(got, ['evt_1']);
      assert.equal(s.seen.length, 1);
    } finally {
      streamResume.backoffMs = 1;
      streamResume.maxBackoffMs = 1;
      await s.close();
    }
  });
});
