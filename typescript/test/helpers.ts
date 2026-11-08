import { createServer, type IncomingMessage, type ServerResponse } from 'node:http';
import type { AddressInfo } from 'node:net';
import { BmaClient } from '../src/index.js';

export interface Seen {
  method: string;
  path: string;
  query: string;
  headers: IncomingMessage['headers'];
  body: string;
}

export type Handler = (res: ServerResponse, req: Seen, n: number) => void;

/** A test server that records every request and answers with `handler`. */
export async function startServer(handler: Handler) {
  const seen: Seen[] = [];
  const server = createServer((req, res) => {
    const chunks: Buffer[] = [];
    req.on('data', (c: Buffer) => chunks.push(c));
    req.on('end', () => {
      const url = new URL(req.url ?? '/', 'http://x');
      const entry: Seen = {
        method: req.method ?? '',
        path: url.pathname,
        query: url.search.replace(/^\?/, ''),
        headers: req.headers,
        body: Buffer.concat(chunks).toString(),
      };
      seen.push(entry);
      handler(res, entry, seen.length);
    });
  });
  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', resolve));
  const url = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
  return {
    url,
    seen,
    client: (options: ConstructorParameters<typeof BmaClient>[0] = {}) =>
      new BmaClient({ apiKey: 'bma-key', baseURL: url, ...options }),
    close: () => {
      server.closeAllConnections();
      return new Promise<void>((resolve) => server.close(() => resolve()));
    },
  };
}

export function json(res: ServerResponse, status: number, body: unknown) {
  res.writeHead(status, { 'content-type': 'application/json' });
  res.end(JSON.stringify(body));
}

/** One SSE frame; sequence 0 is an ephemeral frame without bma_sequence. */
export function frame(type: string, id: string, sequence: number): string {
  const data = sequence === 0 ? { type, id } : { type, id, bma_sequence: sequence, processed_at: '2026-11-08T00:00:00Z' };
  return `event: ${type}\ndata: ${JSON.stringify(data)}\n\n`;
}
