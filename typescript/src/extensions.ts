import type { components } from './generated/extensions.js';

// BMA extension fields on the shared (Claude Managed Agents) objects: top-level
// bma_* properties. The official types keep unknown properties on the parsed
// object; the accessors below read them as typed values, and BmaSessions,
// BmaAgents and BmaEnvironments accept them as typed request fields.
//
// bma_model_override is declared by the contract (x-bma-extension-fields) and
// uses its generated types; the other fields follow the facade's current JSON
// until the contract lists them.

type Schemas = components['schemas'];

export type AgentModelOverride = Schemas['AgentModelOverride'];
export type AgentModelOverrideInput = Schemas['AgentModelOverrideInput'];
export type AgentModelOverridePatch = Schemas['AgentModelOverridePatch'];

/** bma_harness: a non-default brain for an agent or a session. */
export interface Harness {
  kind: string;
  agent?: string;
  /** Where the environment runs the brain (sessions only). */
  placement?: string;
}

/** bma_desktop of an environment: the default wallpaper is a file of the Files API. */
export interface EnvironmentDesktop {
  wallpaper: { file_id: string } | null;
}

/** bma_machine: present on the environment BMA projects from a machine. */
export interface EnvironmentMachine {
  machine_id: string;
  source_kind: string;
  /** Who runs on a persistent machine: sessions borrowing it run their turns one at a time. */
  lease: { session_id: string | null; queued_sessions: number };
}

/** The BMA fields of a session. */
export interface SessionExt {
  /** The active model override (no key) or null. */
  modelOverride: AgentModelOverride | null;
  harness: Harness | null;
}

/** The BMA fields of an agent. */
export interface AgentExt {
  harness: Harness | null;
}

/** The BMA fields of an environment. */
export interface EnvironmentExt {
  desktop: EnvironmentDesktop | null;
  machine: EnvironmentMachine | null;
}

/** The BMA fields of a session event, from a list or a stream. */
export interface EventExt {
  /** Orders the events of a session; Last-Event-ID and the history cursor use it (the SSE id stays the opaque event id). */
  sequence: number | null;
  /** The BMA input of a user.message. */
  inputID: string | null;
  /** BMA's reason on a session.error. */
  errorCode: string | null;
}

function field<T>(object: object, name: string): T | null {
  return ((object as Record<string, unknown>)[name] as T | null | undefined) ?? null;
}

/** The BMA fields of a session returned by client.beta.sessions. */
export function sessionExtensions(session: object): SessionExt {
  return { modelOverride: field(session, 'bma_model_override'), harness: field(session, 'bma_harness') };
}

/** The BMA fields of an agent returned by client.beta.agents. */
export function agentExtensions(agent: object): AgentExt {
  return { harness: field(agent, 'bma_harness') };
}

/** The BMA fields of an environment returned by client.beta.environments. */
export function environmentExtensions(environment: object): EnvironmentExt {
  return { desktop: field(environment, 'bma_desktop'), machine: field(environment, 'bma_machine') };
}

/** The BMA fields of a session event: an item of client.beta.sessions.events.list or a frame of stream. */
export function eventExtensions(event: object): EventExt {
  return {
    sequence: field(event, 'bma_sequence'),
    inputID: field(event, 'bma_input_id'),
    errorCode: field(event, 'bma_error_code'),
  };
}

/** Request fields BMA adds to sessions.create. */
export interface SessionCreateExt {
  /** The override lasts for the session. `apiKey` is write-only. */
  bma_model_override?: AgentModelOverrideInput;
  bma_harness?: Harness;
}

/** Request fields BMA adds to sessions.update. */
export interface SessionUpdateExt {
  /** An input replaces the active override, a patch changes fields of it, null revokes it. */
  bma_model_override?: AgentModelOverrideInput | AgentModelOverridePatch | null;
}

/** Request fields BMA adds to agents.create and agents.update. */
export interface AgentExtParams {
  bma_harness?: Harness;
}

/** Request fields BMA adds to environments.create and environments.update. */
export interface EnvironmentExtParams {
  bma_desktop?: EnvironmentDesktop;
}
