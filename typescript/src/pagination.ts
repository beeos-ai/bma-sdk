// Pagination. Mirrors the Stainless PagePromise of @anthropic-ai/sdk and
// openai: `await` resolves to the first page, `for await` walks every item
// across pages. Applies to every list whose response is
// `{ data: [...], next_<param> }` for a query parameter <param>: `cursor`,
// `page`, `before_id`/`after_id`, `before_sequence`/`after_sequence` (as the
// Anthropic Page supports before_id/after_id).
import { BmaError } from "./errors.js";

/** Response body of a paginated operation. */
export interface CursorPageBody {
  data: unknown[];
}

export type PageItem<R extends CursorPageBody> = R["data"][number];

export interface PageMethods<R extends CursorPageBody> {
  hasNextPage(): boolean;
  /** Fetches the next page; throws when there is none. */
  getNextPage(): Promise<Page<R>>;
  /** This page and every following page. */
  iterPages(): AsyncGenerator<Page<R>>;
  /** Every item of this page and every following page. */
  [Symbol.asyncIterator](): AsyncGenerator<PageItem<R>>;
}

/** One page: the response body plus navigation helpers. */
export type Page<R extends CursorPageBody> = R & PageMethods<R>;

type Cursor = string | number;
type FetchPage<R> = (cursor: Cursor | undefined) => Promise<R>;
type NextCursor = (body: CursorPageBody) => Cursor | undefined;

function makePage<R extends CursorPageBody>(body: R, fetchPage: FetchPage<R>, nextCursor: NextCursor): Page<R> {
  const methods: PageMethods<R> = {
    hasNextPage: () => nextCursor(body) !== undefined,
    getNextPage: async () => {
      const next = nextCursor(body);
      if (next === undefined) throw new BmaError("bma: no next page; check hasNextPage() first");
      return makePage(await fetchPage(next), fetchPage, nextCursor);
    },
    iterPages: async function* () {
      let page: Page<R> = makePage(body, fetchPage, nextCursor);
      yield page;
      while (page.hasNextPage()) {
        page = await page.getNextPage();
        yield page;
      }
    },
    [Symbol.asyncIterator]: async function* () {
      for await (const page of methods.iterPages()) yield* page.data as PageItem<R>[];
    },
  };
  // Methods are non-enumerable so JSON.stringify(page) is the wire body.
  const page = Object.create(null) as Page<R>;
  Object.assign(page, body);
  for (const [key, value] of [...Object.entries(methods), [Symbol.asyncIterator, methods[Symbol.asyncIterator]] as const]) {
    Object.defineProperty(page, key, { value, enumerable: false });
  }
  return page;
}

/** `await` for the first page, `for await` for every item. */
export class PagePromise<R extends CursorPageBody> implements Promise<Page<R>>, AsyncIterable<PageItem<R>> {
  readonly [Symbol.toStringTag] = "PagePromise";
  #first: Promise<Page<R>> | undefined;
  readonly #fetchPage: FetchPage<R>;
  readonly #nextCursor: NextCursor;

  /** @internal */
  constructor(fetchPage: FetchPage<R>, nextCursor: NextCursor) {
    this.#fetchPage = fetchPage;
    this.#nextCursor = nextCursor;
  }

  #page(): Promise<Page<R>> {
    this.#first ??= this.#fetchPage(undefined).then((body) => makePage(body, this.#fetchPage, this.#nextCursor));
    return this.#first;
  }

  then<A = Page<R>, B = never>(
    onfulfilled?: ((value: Page<R>) => A | PromiseLike<A>) | null,
    onrejected?: ((reason: unknown) => B | PromiseLike<B>) | null,
  ): Promise<A | B> {
    return this.#page().then(onfulfilled, onrejected);
  }

  catch<B = never>(onrejected?: ((reason: unknown) => B | PromiseLike<B>) | null): Promise<Page<R> | B> {
    return this.#page().catch(onrejected);
  }

  finally(onfinally?: (() => void) | null): Promise<Page<R>> {
    return this.#page().finally(onfinally);
  }

  async *[Symbol.asyncIterator](): AsyncGenerator<PageItem<R>> {
    yield* await this.#page();
  }
}
