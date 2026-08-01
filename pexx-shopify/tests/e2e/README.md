# PEXX storefront E2E tests

Runs against the live store (`shop.poddarexp.com`) as a real visitor would use it —
no staging environment exists, so these are the closest thing to a regression suite.

## Setup

```
cd pexx-shopify
npm install
npx playwright install chromium
```

## Run

```
npm test              # headless, both desktop + mobile projects
npm run test:headed   # watch it click through
npm run test:ui       # Playwright's interactive UI mode
```

## Safety boundaries — do not remove

- **Never submits the newsletter form or the Gifting bulk-enquiry form for real.**
  Both write directly to live systems (a real Shopify Customer record with marketing
  consent, and a real merchant lead) — submitting them from a test run pollutes
  production data every time CI runs. Tests verify the form is reachable, fillable,
  and pre-fills correctly, then stop short of clicking Submit.
- **Never proceeds into real Shopify checkout payment.** Cart tests stop once the
  cart page/drawer shows the correct line item — they do not click "Checkout" through
  to a payment step.
- Run at reasonable frequency/concurrency — the store rate-limited (503s) under a burst
  of ~70 rapid requests in one session (2026-07-20). Keep `fullyParallel` workers
  modest if this suite is ever wired into a tight CI loop.

## Known-flaky / expected-fail context

- `nav-and-mega-menu.spec.ts`'s hover-tracking test encodes the fix for a real bug
  (mega-menu closes on a natural diagonal mouse move before reaching a subcategory
  link). As of 2026-07-20 the fix is correctly deployed to the theme's source but
  Shopify's own origin-side page cache (visible in the response ETag as
  `page_cache:...`) is stuck serving the pre-fix version — unrelated to Cloudflare,
  confirmed via GraphQL `themeFilesUpsert` + a full theme re-publish, neither of
  which invalidated it (re-confirmed directly against the CDN, same day: still
  serving the pre-fix bundle). **This test has passed on some runs even against
  the confirmed-unfixed live code** — meaning either the bug itself is
  timing/race-dependent and this specific mouse trajectory doesn't reproduce it
  100% of the time, or the assertion still has a blind spot. Treat a single green
  run as inconclusive; a red run is real signal. Re-run a few times once the cache
  clears (see `project_mega_menu_hover_cache_stuck` memory) before trusting a pass.
- `footer-and-newsletter.spec.ts`'s footer-link tests expect an `<h1>` on every
  page. **Update 2026-07-22:** `/pages/about`, `/pages/return-gifts`, and
  `/pages/gift-to-india` now render a proper `<h1>` — this is fixed. The
  homepage had a separate bug (hidden `<h1>{{ shop.name }}</h1>` from
  `header.liquid` firing only on `request.page_type == 'index'`, while the real
  hero headline was an `<h2>`) — also fixed 2026-07-22 (hero promoted to `<h1>`,
  redundant hidden one removed). `/pages/send-rakhi-to-india` no longer exists
  (page unpublished, Send Rakhi feature dropped as out of scope for our
  products) — remove any spec assertions still targeting that URL.
