import { test as base, expect } from '@playwright/test';

/**
 * The "Welcome offer" popup (#pexx-pop) checks localStorage key `pexx_pop_seen`
 * before scheduling itself to auto-open ~4.5s after load — set it up front so
 * the popup never appears and its overlay never intercepts clicks mid-test.
 * (Reactive "dismiss if already open" was tried first and proved timing-fragile:
 * on a loaded/parallel run the popup can open between the dismiss check and the
 * next click, still blocking it — confirmed live, not a hypothetical.)
 *
 * Every spec imports `test`/`expect` from here EXCEPT the one test that
 * verifies the popup itself, which uses plain `@playwright/test` directly so
 * the popup is free to open.
 */
export const test = base.extend({
  page: async ({ page }, use) => {
    await page.addInitScript(() => localStorage.setItem('pexx_pop_seen', '1'));
    await use(page);
  },
});

export { expect };
