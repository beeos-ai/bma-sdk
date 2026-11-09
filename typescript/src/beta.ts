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
import { Events, type EventSendParams, type EventStreamParams } from '@anthropic-ai/sdk/resources/beta/sessions/events';
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

/** The result of `sendAndStream`. */
export interface SentStream {
  /** The send response. */
  sent: Awaited<ReturnType<Events['send']>>;
  /** Starts at the cursor read before the send: its first frames are the sent `user.message` and its turn. */
  stream: Stream<StreamEvent>;
  /** True when the server gave no `bma_resume_cursor` for a `user.message`: the stream replays from `Last-Event-ID: 0`. */
  replayed: boolean;
}

function withLastEventID(options: RequestOptions | undefined, lastEventID: string | undefined): RequestOptions | undefined {
  return lastEventID === undefined ? options : (
      { ...options, headers: mergeHeaders([options?.headers, { 'Last-Event-ID': lastEventID }]) }
    );
}

/** The Last-Event-ID for a stream opened after a send: the smallest `bma_resume_cursor` of the response's
 * `user.message` events; 0 and `replayed` when one has none; undefined without a `user.message`. */
function resumeCursor(sent: { data?: unknown[] }): { after: number | undefined; replayed: boolean } {
  let after: number | undefined;
  for (const event of (sent.data ?? []) as { type?: string; bma_resume_cursor?: number }[]) {
    if (event.type !== 'user.message') continue;
    if (typeof event.bma_resume_cursor !== 'number') return { after: 0, replayed: true };
    after = after === undefined ? event.bma_resume_cursor : Math.min(after, event.bma_resume_cursor);
  }
  return { after, replayed: false };
}

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
    return this.openStream(sessionID, params, options);
  }

  /**
   * Send events, then open the resuming stream at the cursor the send
   * returned (`bma_resume_cursor`: the session's last sequence before the
   * send), so a frame an executor wrote before the stream opened is not lost.
   * The official pattern, a stream opened before the send, needs no cursor;
   * this one is for a caller that sends first. Without a cursor for a
   * `user.message` the stream starts at `Last-Event-ID: 0` and `replayed` is
   * true: it replays the session from its first event, so it can carry events
   * that precede the send; pick this one's turn by `bma_input_id`. A send
   * with no `user.message` streams from the server's default position (new
   * events only). A send error rejects with no stream; an error opening the
   * stream rejects too, after the message was accepted.
   */
  async sendAndStream(
    sessionID: string,
    body: EventSendParams,
    params: EventStreamParams | undefined = {},
    options?: RequestOptions,
  ): Promise<SentStream> {
    const sent = await this.send(sessionID, body, options);
    const { after, replayed } = resumeCursor(sent);
    const stream = await this.openStream(sessionID, params, options, after);
    return { sent, stream, replayed };
  }

  private openStream(
    sessionID: string,
    params: EventStreamParams,
    options: RequestOptions | undefined,
    after?: number,
  ): APIPromise<Stream<StreamEvent>> {
    const open = (lastEventID?: string) =>
      super.stream(sessionID, params, withLastEventID(options, lastEventID)) as unknown as Promise<Stream<StreamEvent>>;
    return super
      .stream(sessionID, params, withLastEventID(options, after === undefined ? undefined : String(after)))
      ._thenUnwrap((first) =>
        resumable(first as Stream<StreamEvent & object>, open as never, this._client, options?.signal, after),
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
