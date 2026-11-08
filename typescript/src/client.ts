import { Anthropic, type ClientOptions } from '@anthropic-ai/sdk';
import { BmaBeta } from './beta.js';
import { SDK_VERSION } from './version.js';

/** The hosted BMA origin (the paths carry /v1). */
export const DEFAULT_BASE_URL = 'https://api.bma.beeos.ai';

export interface BmaClientOptions
  extends Omit<ClientOptions, 'apiKey' | 'authToken' | 'credentials' | 'config' | 'profile' | 'baseURL' | 'webhookKey'> {
  /** The BMA API key (a tenant credential, server side only). Defaults to process.env.BMA_API_KEY. */
  apiKey?: string | null | undefined;
  /** The deployment origin, e.g. https://api.staging.bma.beeos.ai. Defaults to process.env.BMA_BASE_URL, else DEFAULT_BASE_URL. */
  baseURL?: string | null | undefined;
  /** The project scope, sent as x-bma-project-id; required when the key can see more than one project. Defaults to process.env.BMA_PROJECT_ID. */
  project?: string | null | undefined;
}

function env(name: string): string | undefined {
  const value = typeof process !== 'undefined' ? process.env?.[name]?.trim() : undefined;
  return value || undefined;
}

/**
 * The BMA client: the official Anthropic client with the BMA defaults, whose
 * `beta` adds the BMA extensions. It never reads the ANTHROPIC_API_KEY,
 * ANTHROPIC_AUTH_TOKEN, ANTHROPIC_BASE_URL or credential-profile configuration
 * of the official client: the key defaults to BMA_API_KEY, the origin to
 * BMA_BASE_URL and the project to BMA_PROJECT_ID.
 *
 * Only use it on a server: the API key is a tenant credential. End-user
 * clients get single-use tickets instead.
 */
export class BmaClient extends Anthropic {
  override beta: BmaBeta = new BmaBeta(this);

  constructor({ apiKey, baseURL, project, defaultHeaders, ...rest }: BmaClientOptions = {}) {
    const key = apiKey || env('BMA_API_KEY');
    if (!key) {
      throw new TypeError('BmaClient: set the apiKey option or the BMA_API_KEY environment variable');
    }
    const scope = project || undefined;
    super({
      ...rest,
      apiKey: key,
      authToken: null,
      baseURL: baseURL || env('BMA_BASE_URL') || DEFAULT_BASE_URL,
      defaultHeaders: {
        'X-BMA-SDK': `bma-sdk-ts/${SDK_VERSION}`,
        ...(env('BMA_PROJECT_ID') ? { 'x-bma-project-id': env('BMA_PROJECT_ID')! } : {}),
        ...defaultHeaders,
        ...(scope ? { 'x-bma-project-id': scope } : {}),
      },
    });
  }

  /** A copy with other options; `project` replaces the project scope. */
  override withOptions(options: Partial<ClientOptions> & { project?: string | null }): this {
    return super.withOptions(options);
  }

  /** Never resolve the official credential chain (profiles, federation, files). */
  protected override _shouldResolveDefaultCredentials(): boolean {
    return false;
  }
}
