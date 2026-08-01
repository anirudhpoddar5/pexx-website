# PEXX — Post-Launch Automation Plan

## Build status (2026-07-22)

**Done, live now:**
- Self-serve returns/cancellations: ON. Rules: 7-day return window from delivery, no restocking fee, customer pays return shipping, 24h cancellation window, Gift Wrap marked final-sale/non-returnable.
- Email branding fixed store-wide: PEXX wordmark logo + terracotta (#9E3B2F) accent color were never set — now uploaded/set in Settings → Notifications → Customize email templates. This is why Order confirmation looked branded and Shipping confirmation didn't; nothing was broken, branding was just never configured.
- Verified (no changes needed): Pending payment success is live (mandatory template); Abandoned checkout recovery is Active in Shopify Flow/Messaging with a 10h delay already matching plan; Customer privacy cookie banner already correctly scoped to UK-only (India, the main market, isn't gated); PostHog's pixel already has full `analytics.subscribe` event bridges + `posthog.identify(email)` on purchase — analytics was already properly wired, contrary to earlier assumption.
- `whatsapp-worker` extended: PostHog server-side capture (`whatsapp_message_sent`, `order_dispatched`, `order_delivered`) wired via a new `fulfillments/update` webhook subscription; COD email confirm/cancel flow built (signed links, Shopify GraphQL tagging) — code is deployed and tested, but **inert until secrets below are provided**.
- Found and fixed a real live bug: the floating WhatsApp button (`snippets/pexx-whatsapp.liquid`) was still on the placeholder number (`910000000000`), so it silently rendered nothing on every page. Fixed to the real number from `WHATSAPP-MARKETING-PLAN.md` and deployed to the live theme.
- Added a WhatsApp "notify me when back in stock" link that appears on genuinely sold-out products (not just unavailable-variant states), reusing the same number.

**Still open (see task lists above for detail):**
1. Return-defect tagging Flow (native Shopify Flow, not yet built).
2. Notification copy batch (shipping confirmation, cancel, refund, return emails) — drafted, needs your sign-off before saving live.
3. COD hold/24h-reminder/48h-auto-cancel Flow (native Shopify Flow, not yet built).
4. Review-request Flow + worker endpoint — blocked on Judge.me being installed first.
5. Linking the return/refund policy page + footer to the customer-accounts returns portal (Shopify's own suggestion when returns was turned on).

**Blocking on you, to make the COD email flow live:**
- Provision a Shopify Admin API token with `write_orders` scope (via the "Pexx Build" custom app, or a new private app) and give it to me to set as the `SHOPIFY_ADMIN_TOKEN` worker secret.
- Sign up for an email API (Resend recommended — free tier) and verify a sending subdomain (e.g. `notify.poddarexp.com`) via DNS, same pattern as the original email-auth setup. Give me the API key to set as `RESEND_API_KEY`, and confirm the from-address as `RESEND_FROM`.



> Companion to [LAUNCH-CHECKLIST.md](LAUNCH-CHECKLIST.md). Covers what happens to an order *after* it's placed: cancellation/returns, the full notification set, analytics, and COD/reviews/back-in-stock. Written 2026-07-22 after verifying live Shopify Admin state and running 4 parallel planning passes (one per workstream, steelmanned — alternatives argued, not just picked by default).
>
> **Legend:** 🧑 = you / owner decision or action · 🤖 = Claude can build/configure directly · ⚠️ = blocks other work until decided

---

## Verified starting state (as of 2026-07-22)

- **Notifications** (Settings → Notifications → Customer notifications): Order confirmation, Shipping confirmation, Out for delivery, Delivered are all **already live** — no toggles needed, just a copy/branding pass. Cancelled/refund/return/abandoned-checkout templates also exist natively, not yet reviewed for copy quality.
- **Self-serve returns and cancellations: OFF**, with **no rules configured** ("No rules set"). This is the real gap — nothing lets a customer request a return or cancel an order themselves today.
- **Store credit**: already toggled ON for customer accounts.
- **Analytics**: PostHog + Google&YouTube pixels are both connected (Settings → Customer events), status Web/active. PostHog shows no recognized data yet — needs verification, not installation.
- **Apps installed**: Messaging (Inbox), Search & Discovery, Flow, and a private "Pexx Build" app. No returns app, no review app, no back-in-stock app, no COD-verification app.
- **Existing infra to build on**: `pexx-shopify/whatsapp-worker/src/index.ts` — a live Cloudflare Worker, HMAC-verifies Shopify webhooks (`orders/create`, `fulfillments/create`), sends WhatsApp Business template messages via Meta Graph API. Currently send-only, no Admin API token, no inbound message handling.
- **Published policy already answers most "what should the rule be" questions**: `content-drafts/POLICIES-FINAL.md` has a complete returns spec (10-day window, unused/tags-on, faulty = we pay return shipping, change-of-mind = customer pays, COD refunds via bank transfer or store credit, made-to-order/personalised excluded).

---

## 1. Returns & Cancellations — the priority workstream

**Recommendation: turn ON Shopify's native self-serve returns/cancellations, configured to match the published policy exactly. Do not install a paid returns app (Return Prime, Loop Returns) yet — revisit at ~8-10 returns/month.**

Native is free and already sitting in the admin. The paid apps' three real advantages (defect photo upload, COD refund automation, guest-order portal) are all low-value right now: the published policy already routes defect photos to WhatsApp, COD refunds at this volume are a 2-minute manual store-credit action, and a chunk of returns will start on WhatsApp anyway regardless of what portal exists.

**Rules to configure** (Settings → Customer accounts → Policies → Return and cancellation rules):
- Return window: **10 days** from delivery (matches the public promise).
- Restocking fee: **none** — a fee contradicts "no questions asked."
- Return shipping: default **customer-paid**, manually waived by staff when the reason is defective/damaged/wrong (matches the policy's split; native can't branch this automatically, so keep approval manual).
- Exclude from returns: **made-to-order / personalised / gift-wrap** items — ⚠️ **needs owner input: which SKUs are actually made-to-order vs. ready-to-ship.**
- Approval: **manual**, not auto-approve (needed to apply the shipping waiver and pick refund method correctly).
- Cancellation window (unfulfilled orders only): recommended **60 minutes** — ⚠️ **owner to confirm**, alternative is same-day.

**Defect/reason capture**: native gives a fixed reason dropdown (defective/wrong/not-as-described/changed-mind/etc.) with **no photo upload**. Handle photos the way the policy already does — ask for them over WhatsApp/email. Add one **Shopify Flow**: return reason ∈ {defective, damaged, wrong item} → auto-tag the order `return-defect`, so staff can filter for QC signal without any new dashboard.

**Reality check on cancellation**: the store uses passwordless "new customer accounts" + guest checkout, so a large share of customers won't have an authenticated session to self-cancel with. Turn the toggle on anyway (helps the logged-in minority, it's free), but treat **WhatsApp/email → staff cancels in admin** as the primary path for most orders.

**Refunds**:
- Prepaid (Razorpay): refund to original payment method via Shopify's Refund action, 5-7 business days.
- COD: no captured instrument. Default to **store credit** (instant, already enabled, drives repeat purchase); offer **bank transfer (UPI/NEFT)** on request, collected over WhatsApp/email, never a public form. ⚠️ **owner to confirm this is the right default stance.**

**Notifications**: use Shopify's native return/cancellation templates for the customer paper trail (review copy, don't rebuild). Extend the WhatsApp worker with a `refunds/create` handler only for the two highest-signal moments ("return approved, pickup arranged" / "refund issued") — needs two new Meta-approved templates first (🧑 owner: submit `return_approved` + `refund_issued` for Meta review) and confirmed `read_returns`/`read_orders` scopes on the Pexx Build app.

### Task list
1. 🧑 Confirm which SKUs are made-to-order/non-returnable (blocks step 3).
2. 🤖 Turn on self-serve returns/cancellations; configure rules above.
3. 🤖 Mark made-to-order/personalised/gift-wrap items return-ineligible (after #1).
4. 🤖 Review/brand native return notification templates.
5. 🤖 Build the `return-defect` tagging Flow.
6. 🤖 Write the staff WhatsApp/Inbox script for returns, cancellations, COD refunds (store-credit-first, photo request for defects).
7. 🧑 Submit `return_approved` + `refund_issued` WhatsApp templates to Meta; confirm Pexx Build app scopes.
8. 🤖 Add `refunds/create` handler to the worker once templates are approved.
9. Set a tripwire (~8-10 returns/month, or COD-transfer/photo-chasing going weekly) to revisit a paid returns app — don't install one now.

---

## 2. Notification email polish

**Framing**: every lifecycle email is already firing. This is a copy/branding pass on native templates plus one channel-routing decision — essentially no new code.

**Diagnostic first**: Order confirmation renders on-brand (PEXX logo, styled buttons); Shipping confirmation previewed plain/unbranded. Since Shopify's branding settings cascade to all templates, this suggests Shipping confirmation may have been edited to custom Liquid at some point and lost the wrapper. Check its code view — if custom, revert to default before applying new copy.

**Priority order for a copy pass** (drafted copy is in the planning transcript, ready for sign-off): Shipping confirmation (P1, highest volume) → Order canceled + Order refund (P2, trust-critical) → Return request received/approved (P3) → Abandoned checkout light polish (P4, keep as fallback channel — WhatsApp is the real recovery channel per the marketing plan; no discount in the email). Payment error/pending-payment templates: leave as Shopify defaults, not worth spending approval cycles on.

**No distinct "payment received" email** — skip it. Order confirmation already only fires post-payment for prepaid orders; a second email is redundant. The one genuinely distinct case (delayed payment methods like UPI collect) is Shopify's native **Pending payment success** template — just verify it's on and give it the same light copy pass. For COD, there's no reliable "payment received" signal to hang an email on; the real COD payment touchpoint is a WhatsApp out-for-delivery UPI link, which belongs to the COD workstream below, not email.

**Channel routing** (WhatsApp is throttleable/costs money per send + annoyance risk; email is free — email is the default, WhatsApp only where instant-read changes the outcome):

| Event | Channel |
|---|---|
| Order confirmed | Both (already both) |
| Dispatched | Both (already both — fix the WA typo once out of Meta review) |
| Out for delivery | Email only (native, automatic); WhatsApp only for COD orders (carries the UPI payment link — COD workstream) |
| Delivered | Email only |
| Cancelled | Email only |
| Refunded | Email only (see returns workstream for the one exception if volume justifies it) |
| Return approved | Email only |

Net new WhatsApp templates from this workstream: **zero**. Resist mirroring every email onto WhatsApp.

### Task list
1. 🤖 Confirm global email branding (logo/accent) is set so it cascades to all templates.
2. 🤖 Diagnose + fix Shipping confirmation (revert to default if custom Liquid).
3. 🤖 Verify Pending payment success is ON; verify Abandoned checkout is ON, set delay ~10h.
4. 🧑 **Sign off on the copy batch** (shipping, cancel, refund, return-received/approved, abandoned-checkout) — presented as one batch before anything is saved live.
5. 🤖 Save approved copy to each template.
6. 🧑 Fix the `order_dispatched` WhatsApp template typo once out of Meta review (WhatsApp Manager edit, not code — already tracked separately).

---

## 3. Analytics completion

**Framing**: infra exists (PostHog + Google&YouTube pixels connected). This is verification + a small worker addition for events client-side pixels can never see, not a new build.

**Real risk to check first**: the PostHog custom pixel is gated on the "Analytics" consent category, and the theme has **no consent/cookie banner** anywhere. Whether PostHog fires for anyone depends on one setting: Settings → Customer privacy → whether any region requires consent. Since PEXX is India-only and DPDP doesn't mandate GDPR-style gating, the fix (if this is blocking data) is to **not** require consent for any region — not to build a banner. (Tension flagged: NRI/diaspora buyers on Send Rakhi/Gift to India pages could be browsing from GDPR territories — worth a conscious decision, not an accident.)

Also unverified: whether the PostHog pixel code actually has `analytics.subscribe(...)` event bridges, or just loads the base script with nothing wired — if the latter, it's collecting ~nothing. 🧑 **Owner needs to check PostHog's own "Live events" view** — Claude has no PostHog login.

**Worth building**: 3 server-side events from the existing worker, since these happen off-site/days later and no client pixel can ever see them — `order_dispatched`, `order_delivered` (needs a new webhook subscription), and `whatsapp_message_sent` (channel attribution for the WhatsApp-first strategy). Use lowercased customer email as the PostHog `distinct_id`, matching a `posthog.identify(email)` call added client-side on `checkout_completed`, so browsing + lifecycle + WhatsApp events land on the same person. Wrap the PostHog call in `ctx.waitUntil()` and fail silently — analytics must never break the WhatsApp send path.

**Meta Pixel**: still correctly deferred. No ad spend is running yet (CTWA hasn't started); installing now seeds no useful audience and adds a third client-side tag to debug. Free prep only: create the dataset/pixel ID in Meta Events Manager now so it exists when needed; don't install until the week spend is actually scheduled.

### Task list
1. 🧑 Check PostHog "Live events" — is data arriving right now?
2. 🧑 Open the PostHog custom pixel's code in Shopify admin — confirm it has `analytics.subscribe` bridges, not just the loader.
3. 🧑 Settings → Customer privacy — confirm no region is blocking the Analytics-gated pixel (or decide consciously that it should for GDPR-territory visitors).
4. 🤖 Fix whichever of #1-3 is broken; define one funnel + WhatsApp-channel breakdown in PostHog.
5. 🤖 Create Meta pixel/dataset ID in Events Manager (dormant, no install).
6. 🤖 Add `POSTHOG_API_KEY` secret + `capturePosthog()` helper to the worker; emit `whatsapp_message_sent` + `order_dispatched`.
7. 🤖 Subscribe `fulfillment_events/create` (or `orders/updated`); add `order_delivered` capture.
8. 🤖 Verify end-to-end with one test order.

---

## 4. COD verification, reviews, back-in-stock

**Constraint that shapes all three**: the whole brand strategy runs one owned WhatsApp number through the existing worker; the marketing plan explicitly says not to install Meta's official WhatsApp Shopify app because a second integration conflicts with the number. This rules out most "dedicated WhatsApp app" options that send from their own number.

### COD verification — extend the worker, skip the app
Send a WhatsApp **Confirm/Cancel button template** on COD orders (not OTP — one-tap confirm converts better with equal fraud protection). Dedicated apps (Verify COD, Level, GoKwik) either send from a different number (trust-damaging) or want to take over the number entirely (conflicts with the worker) — reject for that reason, not cost. Needs genuinely new infra: an **Admin API token** (`write_orders`, via Pexx Build) and an **inbound Meta webhook** (new for this worker, which is currently send-only) to receive the button tap and tag the order `cod-confirmed`/`cod-cancelled`. Shopify Flow owns the 24h-reminder/48h-auto-cancel escalation — don't build a scheduler into the worker.

### Reviews — keep Judge.me, but request over WhatsApp not email
Judge.me (free) is still right for hosting reviews + star ratings on PDP/product cards + SEO rich snippets. Its native review *request* is email-only, though — since WhatsApp reportedly outperforms email 3-5x here, decouple: Judge.me collects/displays, the **worker sends the request over WhatsApp** deep-linking to the review form. Trigger via Shopify Flow: Delivered → wait **7 days** (textiles need a wash cycle before an honest opinion) → HTTP call to the worker. Frame the template as order-specific Utility, not Marketing, to avoid the opt-in/cap rules.

### Back-in-stock — skip the automated build, ship the ₹0 substitute
Limited handmade size-runs often don't restock the identical print, so an automated "it's back!" promise frequently can't be kept, and current WhatsApp-list size is small. **Skip a dedicated app for now.** Instead add a `wa.me` deep-link pre-filled with the product name on sold-out PDPs — zero infra, feeds the WhatsApp list already being built, restock pings become a manual broadcast to whoever asked. Revisit a free-tier app (STOQ/Notify) only once a specific SKU builds a real repeat-restock waitlist.

### Task list

**COD verification** (do first — real RTO cost):
1. 🧑 Provision Admin API token (`write_orders`) from Pexx Build; add as worker secret.
2. 🧑 Create + submit COD Confirm/Cancel button template to Meta.
3. 🤖 Add COD branch to `handleOrderCreated` → send confirm template.
4. 🤖 Add inbound webhook route (Meta challenge + signature verify + button payload → Admin API lookup → tag).
5. 🧑 Point Meta's inbound webhook config at the worker; subscribe `messages`.
6. 🤖 Build Flow: COD hold → 24h reminder → 48h auto-cancel+restock.
7. 🧑 Adopt dispatch SOP: fulfill only `cod-confirmed`/prepaid orders.

**Reviews** (at/after first deliveries):
1. 🧑 Install Judge.me; connect.
2. 🤖 Place rating/review widgets on product card + PDP.
3. 🧑 Submit review-request Utility template to Meta.
4. 🤖 Add worker endpoint to send the template with the Judge.me link.
5. 🤖 Build Flow: Delivered → wait 7 days → HTTP call to worker.

**Back-in-stock** (anytime, low effort):
1. 🤖 Add sold-out `wa.me` deep-link to the PDP.
2. Revisit a real app only once a specific SKU shows repeat-restock demand.

---

## Open decisions blocking execution (⚠️ owner input needed)

1. Which SKUs are made-to-order/non-returnable vs. ready-to-ship.
2. Cancellation self-serve window (60 min vs. same-day).
3. COD refund default (store-credit-first — recommended — vs. something else).
4. Sign-off on the drafted notification copy batch before it's saved live.
5. Whether to build COD WhatsApp-confirm now — it's real new infra (Admin API token + first-ever inbound webhook for this worker), not just config.
6. PostHog data-verification checks (Live events, pixel code, consent-region setting) — needs the owner's PostHog/Shopify login, not something Claude can check alone.
