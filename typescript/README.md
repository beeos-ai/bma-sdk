# @beeos-ai/bma-sdk

TypeScript client for the BMA REST API, generated from
[`contracts/bma/rest.openapi.yaml`](../contracts/bma/rest.openapi.yaml), plus
the BMA extensions to the Anthropic Managed Agents API.

```ts
import { BmaClient, unwrap } from "@beeos-ai/bma-sdk";

const bma = new BmaClient({ baseUrl: "https://host/api/v1", token: process.env.BMA_TOKEN! });
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
package [`@beeos-ai/bma-executor-sdk`](../executor/typescript).
