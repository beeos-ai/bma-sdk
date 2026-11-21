import type { Anthropic } from '@anthropic-ai/sdk';

/** The per-request options of the official client (its type is not exported). */
export type RequestOptions = NonNullable<Parameters<Anthropic['beta']['sessions']['events']['stream']>[2]>;

type HeadersLike = RequestOptions['headers'];

/** Merges header sets; a later one wins. Explicit nulls (unset a default) are kept. */
export function mergeHeaders(sets: HeadersLike[]): Headers {
  const out = new Headers();
  for (const set of sets) {
    if (!set) continue;
    const entries: Iterable<[string, string | null | undefined]> =
      set instanceof Headers ? set.entries()
      : Array.isArray(set) ? (set as [string, string][])
      : 'values' in set && (set as { values: unknown }).values instanceof Headers ? (set as { values: Headers }).values.entries()
      : Object.entries(set as Record<string, string | null | undefined>);
    for (const [name, value] of entries) {
      if (value === undefined || value === null) out.delete(name);
      else out.set(name, value);
    }
  }
  return out;
}

/** Tagged template for a URL path: every interpolated segment is checked and percent-encoded. */
export function path(strings: TemplateStringsArray, ...segments: string[]): string {
  return strings.reduce((url, text, i) => {
    if (i === 0) return text;
    const segment = segments[i - 1]!;
    if (segment === '' || segment === '.' || segment === '..') {
      throw new TypeError(`Expected a valid path segment but received ${JSON.stringify(segment)}`);
    }
    return url + encodeURIComponent(segment) + text;
  }, '');
}
