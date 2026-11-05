# @beeos-ai/bma-sdk

[![npm](https://img.shields.io/npm/v/@beeos-ai/bma-sdk.svg)](https://www.npmjs.com/package/@beeos-ai/bma-sdk)

TypeScript client for the BMA REST API, generated from
[`contracts/bma/rest.openapi.yaml`](../contracts/bma/rest.openapi.yaml), plus
the BMA extensions to the Anthropic Managed Agents API.

| | |
| --- | --- |
| Version | 0.4.2 (tag `v0.4.2`), see [CHANGELOG](../CHANGELOG.md) |
| Contract | BMA REST snapshot recorded in [`contracts/bma/lock.json`](../contracts/bma/lock.json) |
| Node.js | 20 or newer; ESM, depends on `openapi-fetch` |

```sh
npm install @beeos-ai/bma-sdk@0.4.2
```

```ts
import { BmaClient, unwrap } from "@beeos-ai/bma-sdk";

const bma = new BmaClient({ baseUrl: process.env.BMA_BASE_URL!, token: process.env.BMA_TOKEN! });
const path = { orgID: "org_...", projectID: "proj_...", agentID: "agt_..." };

const { session } = unwrap(
  await bma.rest.POST("/orgs/{orgID}/projects/{projectID}/agents/{agentID}/sessions", {
    params: { path },
    body: { idempotency_key: "task-1", model_override: { model: "deepseek-flash", expires_with_session: true /* ... */ } },
  }),
);
await bma.rest.POST("/orgs/{orgID}/projects/{projectID}/agents/{agentID}/inputs", {
  params: { path, query: { session_id: session.id } },
  body: { content_blocks: [{ type: "text", text: "Start." }] },
});
for await (const frame of bma.streamEvents({ ...path, sessionId: session.id })) {
  console.log(frame.event, frame.sequence);
}
```

Set `baseUrl` to your BMA deployment: the hosted service is in early access and
the default `DEFAULT_BASE_URL` (`https://api.bma.beeos.ai/v1`) does not resolve
yet. It is the API root including `/v1` (for example `https://bma.example.com/api/v1`
when the API is served under `/api`). The SDK does not read `BMA_BASE_URL` itself.

`bma.rest` is a fully typed [openapi-fetch](https://openapi-ts.dev/openapi-fetch/)
client for every contract operation. `streamEvents` parses the SSE stream and
`downloadArtifact` verifies the artifact size and sha256 digest.

## BMA extensions to the Anthropic facade

Use the official Anthropic SDK for `/v1/agents`, `/v1/environments`,
`/v1/sessions` and events. The routes BMA adds live in a separate entry point:

```ts
import { FacadeExtensionsClient, bmaSequence } from "@beeos-ai/bma-sdk/facade-extensions";

const ext = new FacadeExtensionsClient({ baseUrl: "https://host", apiKey: key, projectId: "proj_..." });
const ticket = await ext.getSessionDesktopStream(sessionId, { desktopSessionId, origin: location.origin });
await ext.uploadSessionFile(sessionId, new Blob([bytes]), "report.pdf");
const page = await ext.listSessionFiles(sessionId, { limit: 100 });
```

It also exports the extension field types `ModelConfigOverride`
(`agent.model.api_url/api_key/api_format`), `MCPServerBMAAuth`
(`mcp_servers[].bma_auth`), `IDEMPOTENCY_KEY_HEADER`, and `bmaSequence(event)`
for `bma_sequence` resume cursors.

The executor protocol (executor, harness and agent ends) is the separate
package [`@beeos-ai/bma-executor-sdk`](https://github.com/beeos-ai/bma-executor-sdk/tree/main/typescript).
