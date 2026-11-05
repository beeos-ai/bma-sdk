// Cursor pagination. Mirrors the Stainless PagePromise of @anthropic-ai/sdk
// and openai: `await` resolves to the first page, `for await` walks every
// item across pages. Applies to operations with a `cursor` query parameter
// whose response is `{ data: [...], next_cursor }`.

/** Response body of a cursor-paginated operation. */
export interface CursorPageBody {
  data: unknown[];
  next_cursor?: string | null;
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

type FetchPage<R> = (cursor: string | undefined) => Promise<R>;

function makePage<R extends CursorPageBody>(body: R, fetchPage: FetchPage<R>): Page<R> {
  const methods: PageMethods<R> = {
    hasNextPage: () => typeof body.next_cursor === "string" && body.next_cursor !== "" && body.data.length > 0,
    getNextPage: async () => {
      if (!methods.hasNextPage()) throw new Error("bma: no next page; check hasNextPage() first");
      return makePage(await fetchPage(body.next_cursor as string), fetchPage);
    },
    iterPages: async function* () {
      let page: Page<R> = makePage(body, fetchPage);
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

  /** @internal */
  constructor(fetchPage: FetchPage<R>) {
    this.#fetchPage = fetchPage;
  }

  #page(): Promise<Page<R>> {
    this.#first ??= this.#fetchPage(undefined).then((body) => makePage(body, this.#fetchPage));
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
