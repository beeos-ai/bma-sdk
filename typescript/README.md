# @beeos-ai/bma-sdk

[![npm](https://img.shields.io/npm/v/@beeos-ai/bma-sdk.svg)](https://www.npmjs.com/package/@beeos-ai/bma-sdk)

TypeScript client for BMA, version 2.0 (ADR 0025): **the official
[`@anthropic-ai/sdk`](https://www.npmjs.com/package/@anthropic-ai/sdk) 1.6.0
plus the BMA extensions**. `BmaClient` extends the official `Anthropic` client,
so every Claude Managed Agents resource under `client.beta` (agents,
environments, sessions, events, files, skills, vaults, memory stores, …) is the
official one with its signatures; the BMA extensions (`machines`,
`machinePools` and `.grants`, `desktopSessions` and `.tickets`,
`terminalSessions` and `.tickets`, `organization.projects`) are generated from
[`contracts/bma/v2/extensions.openapi.yaml`](../contracts/bma/v2/extensions.openapi.yaml)
and use the same client: base URL, authentication, retries, timeouts, `fetch`,
middleware and error classes. Server side only: the API key is a tenant
credential (hand end users a ticket, never the key).

| | |
| --- | --- |
| Version | 2.0.0, see [CHANGELOG](../CHANGELOG.md); from 1.x: [MIGRATION](../MIGRATION.md#typescript-1x--20) |
| Official core | `@anthropic-ai/sdk` 1.6.0 (exact pin) |
| Node.js | 20 or newer; ESM |

```ts
import { BmaClient, errorCode, sessionExtensions } from "@beeos-ai/bma-sdk";

// apiKey: BMA_API_KEY, baseURL: BMA_BASE_URL (default https://api.bma.beeos.ai),
// project: BMA_PROJECT_ID. ANTHROPIC_* is never read.
const client = new BmaClient({ apiKey: process.env.BMA_API_KEY, baseURL: process.env.BMA_BASE_URL });

const session = await client.beta.sessions.create({
  agent: agentId,
  environment_id: environmentId,
  bma_model_override: { model: "deepseek-flash" }, // typed BMA field
});
console.log(sessionExtensions(session).modelOverride);

// Open the stream first, then send. A dropped stream resumes with Last-Event-ID
// and returns every event once.
const stream = await client.beta.sessions.events.stream(session.id);
await client.beta.sessions.events.send(session.id, {
  events: [{ type: "user.message", content: [{ type: "text", text: "Start the task." }] }],
});
for await (const event of stream) {
  if (event.type === "session.status_idle") break;
}

// Extensions
for await (const machine of client.beta.machines.list({ limit: 20 })) console.log(machine.id);
const term = await client.beta.terminalSessions.create({ machine_id: machineId }); // sends an Idempotency-Key
const ticket = await client.beta.terminalSessions.tickets.create(term.id, {}); // single use; give it to the end user

try {
  await client.beta.machines.retrieve("mch_x");
} catch (err) {
  console.log(errorCode(err)); // BMA's error.code, e.g. "machine_not_found"
}
```

- **Extension fields.** `sessionExtensions`, `agentExtensions`,
  `environmentExtensions` and `eventExtensions` read `bma_*` response fields as
  typed values; `sessions.create/update`, `agents.create/update` and
  `environments.create/update` accept `bma_model_override`, `bma_harness` and
  `bma_desktop` as typed params (`bma_model_override: null` revokes).
- **Project.** `new BmaClient({ project })` sets `x-bma-project-id`;
  `client.withOptions({ project })` copies the client into another project.
- **Idempotency.** Extension creates send a random `Idempotency-Key` once per
  call, so automatic retries resend it; pass `{ headers: { "Idempotency-Key": key } }`
  to choose it. CMA creates get none unless you pass one.
- **Types.** The extension request and response types are exported by name
  (`Machine`, `MachineCreateParams`, …); the whole schema set is
  `components["schemas"]`.
- Credential features of the official client (profiles, `authToken`,
  federation) are disabled: authentication is the BMA API key.

## Development

```bash
npm ci
npm run build   # tsc
npm test        # unit tests against a local server; BMA_INTEGRATION=1 adds the staging test
```

`src/generated/` is written by `tools/generate.sh` (openapi-typescript for the
types, `tools/sdkgen/ts2gen.py` for the services); never edit it by hand.
