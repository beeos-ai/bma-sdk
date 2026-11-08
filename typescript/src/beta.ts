import { APIPromise } from '@anthropic-ai/sdk/core/api-promise';
import { mergeHeaders, type RequestOptions } from './internal.js';
import { Stream } from '@anthropic-ai/sdk/core/streaming';
import { Beta } from '@anthropic-ai/sdk/resources/beta/beta';
import { Agents, type AgentCreateParams, type AgentUpdateParams } from '@anthropic-ai/sdk/resources/beta/agents/agents';
import {
  Environments,
  type EnvironmentCreateParams,
  type EnvironmentUpdateParams,
} from '@anthropic-ai/sdk/resources/beta/environments/environments';
import { Events, type EventStreamParams } from '@anthropic-ai/sdk/resources/beta/sessions/events';
import {
  Sessions,
  type SessionCreateParams,
  type SessionUpdateParams,
} from '@anthropic-ai/sdk/resources/beta/sessions/sessions';
import { Organization } from '@anthropic-ai/sdk/resources/beta/organization/organization';
import type {
  AgentExtParams,
  EnvironmentExtParams,
  SessionCreateExt,
  SessionUpdateExt,
} from './extensions.js';
import { OrganizationProjects, newExtensionServices, type ExtensionServices } from './generated/extensions-resources.js';
import { resumable } from './resume.js';

type StreamEvent = Awaited<ReturnType<Events['stream']>> extends Stream<infer T> ? T : never;

/** client.beta.sessions.events: the official resource whose `stream` resumes a dropped connection. */
export class BmaEvents extends Events {
  /**
   * Stream Events. Same signature and frames as the official method. When the
   * connection drops or the server ends the stream, it reconnects with
   * `Last-Event-ID` set to the `bma_sequence` before the one of the last frame
   * and returns every event once. The official, non-resuming stream is
   * `Events.prototype.stream.call(client.beta.sessions.events, ...)`.
   */
  override stream(
    sessionID: string,
    params: EventStreamParams | undefined = {},
    options?: RequestOptions,
  ): APIPromise<Stream<StreamEvent>> {
    const open = (lastEventID?: string) =>
      super.stream(
        sessionID,
        params,
        lastEventID ?
          { ...options, headers: mergeHeaders([options?.headers, { 'Last-Event-ID': lastEventID }]) }
        : options,
      ) as unknown as Promise<Stream<StreamEvent>>;
    return super.stream(sessionID, params, options)._thenUnwrap((first) =>
      resumable(first as Stream<StreamEvent & object>, open as never, this._client, options?.signal),
    ) as APIPromise<Stream<StreamEvent>>;
  }
}

/** client.beta.sessions: the official resource with the typed bma_* request fields and the resuming events stream. */
export class BmaSessions extends Sessions {
  override events: BmaEvents = new BmaEvents(this._client);

  override create(params: SessionCreateParams & SessionCreateExt, options?: RequestOptions) {
    return super.create(params, options);
  }

  override update(sessionID: string, params: SessionUpdateParams & SessionUpdateExt, options?: RequestOptions) {
    return super.update(sessionID, params, options);
  }
}

/** client.beta.agents: the official resource with the typed bma_harness request field. */
export class BmaAgents extends Agents {
  override create(params: AgentCreateParams & AgentExtParams, options?: RequestOptions) {
    return super.create(params, options);
  }

  override update(agentID: string, params: AgentUpdateParams & AgentExtParams, options?: RequestOptions) {
    return super.update(agentID, params, options);
  }
}

/** client.beta.environments: the official resource with the typed bma_desktop request field. */
export class BmaEnvironments extends Environments {
  override create(params: EnvironmentCreateParams & EnvironmentExtParams, options?: RequestOptions) {
    return super.create(params, options);
  }

  override update(environmentID: string, params: EnvironmentUpdateParams & EnvironmentExtParams, options?: RequestOptions) {
    return super.update(environmentID, params, options);
  }
}

/** client.beta.organization: the official resource plus `projects`. */
export class BmaOrganization extends Organization {
  projects: OrganizationProjects = new OrganizationProjects(this._client);
}

/** client.beta: the official Beta resources plus the BMA extensions. */
export class BmaBeta extends Beta implements ExtensionServices {
  override agents: BmaAgents = new BmaAgents(this._client);
  override environments: BmaEnvironments = new BmaEnvironments(this._client);
  override sessions: BmaSessions = new BmaSessions(this._client);
  override organization: BmaOrganization = new BmaOrganization(this._client);

  machines = newExtensionServices(this._client).machines;
  machinePools = newExtensionServices(this._client).machinePools;
  desktopSessions = newExtensionServices(this._client).desktopSessions;
  terminalSessions = newExtensionServices(this._client).terminalSessions;
}
