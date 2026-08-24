# WhatsApp abandoned-cart audit — pre-campaign check

Date: 11 August 2026. Scope: `pexx-shopify/whatsapp-worker/`, the Shopify theme opt-in
surfaces, and the live Shopify webhook registry. Investigation only — nothing modified,
nothing deployed, no message sent.

Live checks performed (all read-only): Shopify Admin GraphQL `webhookSubscriptions`
query using the repo's `pexx-shopify/.shopify-token`; unauthenticated HTTP probes of the
deployed Worker's routes (no valid signature, so no code path past validation could run).

---

## 1. Templates — no abandoned-cart template exists

Three template names, all order-lifecycle, all configured as plain vars:

- `pexx-shopify/whatsapp-worker/wrangler.jsonc:8` — `WA_TEMPLATE_ORDER_CONFIRMED = "order_confirmed_v3"`
- `pexx-shopify/whatsapp-worker/wrangler.jsonc:9` — `WA_TEMPLATE_ORDER_DISPATCHED = "order_shipped_v3"`
- `pexx-shopify/whatsapp-worker/wrangler.jsonc:10` — `WA_TEMPLATE_ORDER_DELIVERED = "order_delivered_v3"`

Consumed at `src/index.ts:100` (confirmed), `:116` (dispatched), `:158` (delivered).
There is **no cart, checkout, or recovery template** anywhere — `grep -i "checkout|abandon|cart"`
across `whatsapp-worker/src/` returns exactly one hit, an unrelated comment about phone
formatting at `src/index.ts:294`.

**On the `order_dispatched` typo (stray `)` + "Thanks you"):** the code no longer points at
`order_dispatched`. Committed config used `order_dispatched`; the uncommitted local config
points at `order_shipped_v3` (see `git diff wrangler.jsonc`). So the typo'd template is out
of the send path *if* `order_shipped_v3` is a clean rewrite rather than a renamed copy. I
could not verify that — the template body lives in Meta's WhatsApp Manager, and `META_WA_TOKEN`
is a Wrangler secret not present in the repo. Someone with WhatsApp Manager access should
eyeball `order_shipped_v3`'s body text before the campaign.

## 2. What triggers a send — full path

```
Shopify event → HTTPS POST → Cloudflare Worker route → HMAC verify → handler → Meta Graph API
```

- Entry point: `src/index.ts:27` `fetch()`. Anything that isn't POST 404s at `:37-39`.
- Recognised webhook paths: `src/index.ts:41-45` — `/webhooks/orders-create`,
  `/webhooks/fulfillments-create`, `/webhooks/fulfillments-update`. Any other path 404s at `:66`.
- Signature gate: `src/index.ts:47-50`, verified by `verifyShopifyWebhook()` at `:70-91`
  against `SHOPIFY_WEBHOOK_SECRET`. Confirmed live — unsigned POSTs to both webhook routes
  return `401`.
- Dispatch: `src/index.ts:61-63` → `handleOrderCreated` (`:93`), `handleFulfillmentCreated` (`:110`),
  `handleFulfillmentUpdated` (`:134`).
- Actual send: `sendTemplate()` at `src/index.ts:301-343`, POSTing to
  `graph.facebook.com/v20.0/{WA_PHONE_NUMBER_ID}/messages`.

**Where the subscription is registered:** nowhere in this repo. No script creates webhook
subscriptions — `pexx-shopify/scripts/` has no webhook script, and no `webhookSubscriptionCreate`
call exists in the codebase. They were created by hand in Shopify Admin. Confirmed against
the live store; exactly three exist, all created 25 July 2026:

| Topic | Callback |
|---|---|
| `ORDERS_CREATE` | `…workers.dev/webhooks/orders-create` |
| `FULFILLMENTS_CREATE` | `…workers.dev/webhooks/fulfillments-create` |
| `FULFILLMENTS_UPDATE` | `…workers.dev/webhooks/fulfillments-update` |

Every trigger is **post-purchase**. Nothing in the system fires before an order exists.

## 3. `checkouts/create` / `checkouts/update` — not wired. Plainly: no.

The live webhook list above is complete (queried `first: 50`, three results). There is no
`CHECKOUTS_CREATE`, no `CHECKOUTS_UPDATE`, and no `CARTS_*` subscription. The Worker would
404 them anyway — `src/index.ts:41-45` only matches the three order paths, and unmatched
paths fall through to `:66`.

The only abandoned-checkout recovery that exists at PEXX today is **Shopify's native
abandoned-checkout email**, noted as Active with a 10h delay in `pexx-shopify/AUTOMATION-PLAN.md:8`.
That is email, sent by Shopify, with no WhatsApp involvement whatsoever.

## 4. Phone capture and storage

Two separate things, neither of which feeds the other.

**Capture (marketing):** the popup at `dwell-theme/snippets/pexx-popup.liquid` — rendered
site-wide via `layout/theme.liquid:179`, auto-opens after 4.5s.
- Optional phone field: `pexx-popup.liquid:35`
- Consent checkbox: `pexx-popup.liquid:36-39`, wording *"Yes, message me on WhatsApp with
  order and product updates."* Ticking it does one thing: a JS `onchange` rewrites the hidden
  tags field (`:32`) from `newsletter, popup` to `newsletter, popup, whatsapp-optin`.
- The form is a stock Shopify `{% form 'customer' %}` (`:20`). It creates a Customer record
  with a tag. **That is the entire pipeline.** Nothing reads the `whatsapp-optin` tag —
  `grep -rn "whatsapp-optin"` across the whole repo returns exactly one hit, the checkbox
  that writes it. The Worker never queries customers, never reads tags for consent, and has
  no KV/D1/database binding at all (`wrangler.jsonc` declares only `vars`).
- The **footer** signup (`dwell-theme/blocks/pexx-newsletter-signup.liquid:9-12`) has no
  phone field and no WhatsApp checkbox at all — email only. The earlier note that a "footer
  checkbox" exists is wrong; it's the popup only.

So: **the known context is still true, and slightly worse than described** — the tag is
write-only and one of the two believed surfaces doesn't exist.

**Capture (transactional):** phones are never stored by the Worker. They are pulled per-request
straight off the webhook payload and normalised in memory by `extractPhone()`
(`src/index.ts:288-299`) — from `order.phone` / `customer.phone` / `shipping_address.phone`
(`:94`) or `fulfillment.destination.phone` (`:111`, `:156`). Bare 10-digit numbers get `+91`
prepended (`:295`, India-only assumption). Nothing persists.

I could not count how many customers carry the `whatsapp-optin` tag — the repo's Admin token
lacks `read_customers` scope (`ACCESS_DENIED` on the `customers` field). The owner can check
this in Shopify Admin by filtering customers on that tag.

## 5. Meta/WhatsApp compliance — no opt-in is checked before any send

**There is no consent check anywhere in the send path.** `sendTemplate()` (`src/index.ts:301`)
is called whenever a phone number can be parsed off the webhook — `:99-101`, `:113-122`,
`:157-162`. No tag lookup, no consent record, no suppression list, no opt-out handling.

Today that is *defensible but not clean*: all three templates are order-lifecycle
(confirmed/shipped/delivered), which Meta classifies as **Utility**, and Utility templates
sent after a transaction have a much lower opt-in bar than Marketing. The customer gave a
phone number at checkout for the order. That's the standing practice for Indian D2C.

It **would not pass for abandoned-cart recovery.** An abandoned cart is not a transaction —
there is no order, no completed relationship. Meta categorises cart-recovery templates as
**Marketing**, which requires documented, demonstrable prior opt-in. PEXX's only opt-in
surface is the popup checkbox (§4), and it is:
- optional and unchecked by default,
- attached to an optional phone field,
- worded for *"order and product updates"* — arguably not explicit marketing consent,
- never recorded with a timestamp, wording snapshot, or source, and never read by anything.

`pexx-shopify/WHATSAPP-MARKETING-PLAN.md:8-14` and `:86` already state the correct model and
flag consent logging as an unbuilt "next action". It is still unbuilt.

Also unbuilt: **no opt-out path**. The Worker has no inbound Meta webhook (no `messages`
subscription, no route to receive one — `src/index.ts:41-45`). A customer who replies STOP
is not heard by any system. Under DPDP (rules notified Nov 2025) and Meta policy, honouring
opt-outs is mandatory, and marketing spam reports throttle the *whole* number — including
the order confirmations that currently work.

## 6. Deployed vs local uncommitted

Three files differ from `HEAD` (289 changed lines in `index.ts`, 57 in the test, 5 in config).
The changes add: the `fulfillments/update` delivered handler and `order_delivered_v3` template,
the POST-gated COD confirm/cancel flow (replacing GET-mutating links), PostHog server-side
capture, the THANKYOU15 referral email, and the v3 template renames.

**The uncommitted local code is what is live.** Verified by route probe: the *committed*
version has no `POST /cod/apply` route (it used GET-mutating `/cod/confirm`), so a POST there
would 404. The deployed Worker returns `400 "Invalid link"` for `POST /cod/apply` — the local
version's validation response — and `404` for `POST /cod/confirm`. That behaviour only exists
in the working tree, not in `HEAD`.

Consequence: git is **behind** production, not ahead. Nothing is waiting to be deployed, but
the live Worker's source exists only on this laptop. If the machine dies, the deployed code
is unrecoverable from the repo. Worth committing regardless of the campaign.

`WA_PHONE_NUMBER_ID`, template names, `SHOPIFY_SHOP`, `WORKER_BASE_URL` and the PostHog keys
are plaintext `vars` in `wrangler.jsonc:6-15`; the four secrets (`SHOPIFY_ADMIN_TOKEN`,
`COD_LINK_SECRET`, `RESEND_API_KEY`, `RESEND_FROM`) are Wrangler secrets I cannot read, so I
cannot confirm which are actually set. Code degrades gracefully when they aren't
(`src/index.ts:12-17`, `:170-173`, `:353-356`).

## 7. Test suite — passes

`node src/index.test.mjs` → exit 0, `"ok — signature + phone parsing + COD detection + link
signing + referral-email dedupe checks passed"`.

Honest caveat: it passes because it tests very little. `src/index.test.mjs` is a smoke test
that **re-declares copies** of `extractPhone`, `isCashOnDelivery`, `signCodToken`,
`verifyCodToken` and `shouldSendReferralEmail` inside the test file (`:28`, `:48`, `:74`, `:81`,
`:99`) rather than importing them from `index.ts` — the file's own header calls it "minimal
smoke test, not a full suite" (`:1`). The copies can drift from the real implementations
without any test failing. No routing, no handler, no HMAC-rejection, and no send-path
behaviour is covered. A green run here does not mean the Worker works.

---

## Verdict

**(a) Can abandoned-cart WhatsApp recovery run during the 12–18 August campaign? No.**
Not "half-wired" — not wired at all. No cart/checkout webhook is subscribed, the Worker has
no route that would accept one, no recovery template exists, and no consent record exists to
send against. All four pieces are missing, not just one. Every trigger in the system fires
only *after* an order is placed. The ~70% of carts that abandon during the campaign will be
touched only by Shopify's native abandoned-checkout **email**.

**(b) Smallest change that would make it work:** there isn't a small one, and the binding
constraint is calendar, not code. A new Marketing template must clear **Meta review**
(typically 24h–several days, and cart-recovery templates are rejected more often than
lifecycle ones) — submitting on 11 August to run from the 12th is a gamble on someone else's
queue. Even granting instant approval, the build is: subscribe `CHECKOUTS_CREATE`/`UPDATE` in
Shopify Admin → add a route + handler in `src/index.ts:41-45` → add a delay/scheduler, since a
recovery message must land ~30–60 min after abandonment and the Worker has no scheduler,
no queue and no storage (Shopify Flow could carry the delay instead) → add a suppression
check so someone who completed checkout isn't chased → add consent lookup. That is days of
work plus an external approval gate.
**The honest recommendation: don't try to ship this for 12–18 August.** Run the campaign on
the native abandoned-checkout email, which is already live and needs nothing. Build the
WhatsApp path properly afterwards, with the templates submitted early.

**(c) Compliance risk if switched on anyway:** high, and it endangers the working system.
Cart recovery is a **Marketing** template under Meta policy — it needs documented prior
opt-in, and PEXX has none that would survive scrutiny: the only consent surface is an
optional, default-unchecked popup box worded for "order and product updates", written to a
Shopify tag that nothing ever reads (`pexx-popup.liquid:36-39`). Sending to every abandoning
checkout would mean messaging people who never opted in. There is also **no opt-out path** —
the Worker has no inbound Meta webhook, so STOP replies go unheard, which breaches both Meta
policy and DPDP expectations. The real damage: marketing spam reports throttle quality rating
for the **entire phone number**, so a bad cart-recovery blast can degrade or block the
`order_confirmed_v3` / `order_shipped_v3` / `order_delivered_v3` messages that currently work
fine. Cold Meta traffic makes this worse — those recipients have no relationship with PEXX
and are the most likely to report.

Secondary flag, unrelated to carts: verify the `order_shipped_v3` body in WhatsApp Manager
before the campaign. The code no longer references the typo'd `order_dispatched`, but I could
not read the new template's text from here.
