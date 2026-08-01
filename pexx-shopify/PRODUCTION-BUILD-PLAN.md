# PEXX — Production Build Plan
> Single source of truth for shipping the store. Companion docs: [ECOMMERCE-REQUIREMENTS.md](ECOMMERCE-REQUIREMENTS.md) (strategy), [SHOPIFY-BUILD.md](SHOPIFY-BUILD.md) (wiring log), [LAUNCH-CHECKLIST.md](LAUNCH-CHECKLIST.md) (ops steps).
> A new dev should be able to start from this file + HANDOVER.md.

---

## 1. Product summary

**PEXX** is a D2C Shopify store for hand block-printed **kids merchandise + accessories** from Jaipur (same company as B2B site poddarexp.com, repositioned for consumers). Positioning = **Cluster D**: Indian INR pricing + genuine block-print craft + Indian gifting occasions — a lane no competitor holds (see requirements §2).

**Audience:** Indian parents/gifters (primary), NRIs gifting to India (secondary), bulk/return-gift buyers (tertiary).

**Core flows:**
1. Browse — homepage → category tiles (Little / Carry / Gifting) → collection
2. PDP — benefit accordions, trust band, recommendations → add to cart
3. Cart — drawer, gift-wrap (₹99), gift message note, WELCOME15 from popup
4. Checkout — Shopify checkout; Razorpay + COD (pending activation); free ship ≥₹999, else ₹99
5. Bulk — Return Gifts page → enquiry form with product pre-fill

**Messaging hierarchy (locked, §11):** print/colour → skin-safe → made-to-keep → honest price → craft last. Never discount-first.

**Store facts:** `pexx-7935.myshopify.com` · Basic plan · build theme = **Dwell draft #165377146969** (live theme is untouched Horizon placeholder) · storefront password `rimeup` · push: `shopify theme push --path pexx-shopify/dwell-theme --store pexx-7935.myshopify.com --theme 165377146969`

---

## 2. Current state (what exists today)

### Theme / design system
- Dwell theme, fully customized: palette (cream `#F3EDE3`, ink `#2B241F`, madder `#9E3B2F` accent), Newsreader serif (emotional moments) + Manrope sans (structure)
- Custom snippets: `pexx-blockprint-divider.liquid` (tileable SVG buti border, ×2 on home), `pexx-popup.liquid` (email capture → WELCOME15), `pexx-whatsapp.liquid` (floating button — **dormant**, placeholder number)

### Pages / templates
- **Home** (`index.json`): scrim hero ("Prints worth keeping, on cotton that's safe to chew."), trust bar, pull-quote → Our Story, 3 category tiles, gifting band, Gift-to-India band, block-print dividers
- **PDP** (`product.json`): benefit accordions (Materials+Care, Shipping+Returns), "Buying in bulk?" callout → prefilled enquiry, "real not printed" trust band, recommendations
- **Collection / PLP**: stock Dwell grid + Search & Discovery filters (Availability, Price, Product Type live; Age recreated, activates when real tags land)
- **Cart**: drawer + page, gift-wrap product `43472878370905`, gift-message cart note
- **Content**: Our Story (`page.about`), Return Gifts (bulk form, product pre-fill), Gift to India, Send Rakhi, Contact, FAQ
- **Policies ×4** published (Privacy, Terms, Shipping, Returns) — plain-language, India-compliant drafts in `content-drafts/POLICIES-FINAL.md`
- **Blog**: 2 SEO articles live (plan in `content-drafts/03-seo-aeo-blog-plan.md`)
- **Nav**: main menu (Little · Carry · Gifting▾ · Journal · About), footer = 3 menus (Shop / Customer Care / Information) — fixed, no duplicates

### Commerce / ops (done)
- Collections: Little, Carry, Gifting + occasion smart-collections
- **11 test products** with variant demos (Size / Pack / single)
- Shipping: Standard ₹99 + automatic free-shipping ≥₹999
- WELCOME15 discount (15%, once per customer) — live
- Email auth complete & verified: SPF, Shopify DKIM CNAMEs ×6, DMARC (`p=none`), Google DKIM
- Markets: US + UK active (INR-only — USD/GBP blocked without Shopify Payments)
- Admin API app "Pexx Build" — token in `.shopify-token` (gitignored); scripts in `scripts/`

### Half-done / dead / inconsistent
| Item | State |
|---|---|
| WhatsApp button | Code shipped, hidden behind `910000000000` placeholder guard — needs real number |
| Age/Occasion filters | Recreated with clean values, but empty until real product tags exist |
| 11 test products | Must be deleted before real import |
| Multi-currency | US/UK markets exist but price in INR; true USD/GBP needs PayPal (Phase 2) |
| Blog | 2 of a planned ~12-article calendar |
| Artisan-at-product-level (req diff #1) | **Not built** — no metafields, no artisan content yet |
| "Cost of a Block Print" module (req diff #5) | Not built |
| Certifications (GOTS/OEKO-TEX) | Not secured — no claims on site (correct; don't claim until certified) |
| DMARC | `p=none` — tighten after clean weeks |
| Build token | Rotate/delete "Pexx Build" app after launch |

---

## 3. Gaps & issues

**Launch blockers (revenue = zero until fixed):**
- **No payments** — Razorpay application submitted, not yet approved/connected; COD not enabled. *Impact: can't take money.*
- **No real products** — 11 placeholders. *Impact: nothing to sell.* Template ready at `content-drafts/PRODUCT-IMPORT-TEMPLATE.csv`.
- **GST not configured** — GSTIN + tax-inclusive pricing unset. *Impact: non-compliant invoices.*

**Conversion gaps (fix soon after launch):**
- No reviews/social proof (Judge.me planned post-first-orders)
- WhatsApp dormant — India D2C converts heavily via WhatsApp
- No analytics: GA4 / Meta Pixel not mentioned anywhere in build — flying blind on day 1
- No abandoned-cart or welcome email flows (Shopify Email is free on Basic)
- NRI market pays INR with FX surprise at their bank — PayPal would fix

**Strategy debt (differentiators promised in §2, not yet built):**
- Artisan at product level (name/photo/video per product) — the #1 stated differentiator
- Price-legibility module ("Cost of a Block Print")
- Occasion gift bundles at ₹1,500 / ₹3,500 / ₹7,000 tiers
- Packaging-as-product story (needs physical packaging first)

**Hygiene:**
- Legal sign-off on Privacy/Terms pending (user says easy)
- SEO meta/alt-text pass not yet done on pages/products
- No 404 customization, no search-page tuning (stock Dwell — acceptable)

---

## 4. Recommended target state

**V1 (launch):** A store that takes INR payments + COD, sells the real catalog with clean Age/Occasion filtering, answers trust questions (policies, email deliverability, WhatsApp), and tracks its own traffic. Nothing else gates launch.

**V2 (first 60 days):** Social proof (reviews), retention loops (email flows, WhatsApp), NRI checkout in USD (PayPal), and the two positioning modules that justify the price (artisan-at-product, cost-breakdown). This is where PEXX stops being "a nice Shopify store" and becomes Cluster D.

---

## 5. Phase plan

### Phase 1 — Ship it (blockers + must-haves)
**Goal:** password off, domain live, first real order completed.

| # | Task | Owner |
|---|---|---|
| 1 | Razorpay: approval → API keys → connect in Settings→Payments → activate | 🧑 keys, 🤖 config |
| 2 | Enable COD (manual payment method) | 🧑 |
| 3 | GST: enter GSTIN, set tax-inclusive pricing | 🧑 |
| 4 | Production fills `PRODUCT-IMPORT-TEMPLATE.csv` + photo folder | 🧑 production |
| 5 | Delete 11 test products; bulk-import real catalog via API, attach photos, write descriptions | 🤖 |
| 6 | Wire Age/Occasion filters (tags now real) | 🤖 + 🧑 (S&D UI) |
| 7 | WhatsApp: real number into `pexx-whatsapp.liquid`, push | 🤖 (needs number) |
| 8 | Install GA4 + Meta Pixel (Shopify native integrations) | 🧑 accounts, 🤖 wiring |
| 9 | Lawyer sign-off on Privacy/Terms | 🧑 |
| 10 | Full QA: mobile pass, ₹1 test order (card + COD), filter/nav/form checks | 🤖 + 🧑 |
| 11 | Publish Dwell → remove password → point poddarexp.com DNS to Shopify | 🧑 |
| 12 | Rotate/delete "Pexx Build" API app | 🧑 |

**Acceptance:** a stranger on a phone can find a product by age, pay by UPI/card/COD, get a branded order email that lands in inbox, and reach the brand on WhatsApp. Analytics records the session.

### Phase 2 — Convert & retain (weeks 2–8)
**Goal:** raise conversion and repeat rate; close the NRI gap; build the promised differentiators.

- **Judge.me** reviews after first shipped orders — stars on cards + PDP (🤖 wiring)
- **PayPal** for true USD/GBP NRI checkout (🧑 account, 🤖 config)
- **Email flows** via Shopify Email: abandoned checkout, welcome (popup already captures), post-purchase care-instructions email (🤖)
- **Artisan-at-product**: product metafields (artisan name, photo, 15-sec video) + PDP block. Needs content shoot from production (🧑 assets, 🤖 build)
- **"Cost of a Block Print"** breakdown section — reusable snippet on PDP/About (🤖)
- **Occasion bundles** at ₹1,500/₹3,500/₹7,000 as products or bundle app (🧑 curation, 🤖 build)
- **Blog cadence**: publish remaining articles from the SEO/AEO plan, 1–2/month (🤖 drafts)
- **SEO pass**: meta titles/descriptions, image alt text, collection descriptions (🤖)
- DMARC `p=none` → `quarantine` after clean weeks (🤖 instructions, 🧑 DNS)

**Acceptance:** reviews visible on PDPs; abandoned-cart email firing; an NRI can pay in USD; at least one product page shows its artisan; organic search impressions trending up in Search Console.

### Phase 3 — Nice-to-have / automation
**Goal:** compound what works; expand catalog.

- WhatsApp automation (Interakt/Wati): order notifications, abandoned-cart nudges, catalog
- GOTS + OEKO-TEX certification pursuit → add claims/badges only when secured (§8)
- Personalization (name embroidery — Malabar Baby's proven hook)
- Corporate gifting page/portal for bulk B2B (extends Return Gifts)
- Home & clothing categories (catalog Phase 2 per requirements §1)
- Loyalty/referral (only if repeat-rate data justifies)
- Automated tag-based sub-collections (Sleep / Pack / By Age)

**Acceptance:** each item ships only with a metric behind it (e.g., embroidery only if gifting >30% of orders). No speculative builds.

---

## 6. Open questions (business input needed)

1. **Razorpay** — approval status? Keys when ready.
2. **WhatsApp Business number** — the one item blocking a ready-built feature.
3. **Product data** — when can production deliver the filled CSV + photos? This is the critical path alongside Razorpay.
4. **Artisan content** — can production capture artisan name/photo/video per product batch? Determines Phase 2 scope.
5. **PayPal** — willing to open a business PayPal for NRI USD checkout?
6. **Bundle pricing** — confirm the ₹1,500/₹3,500/₹7,000 tiers and what goes in each.
7. **Certifications** — is GOTS/OEKO-TEX being actively pursued, and on what timeline?
8. **GA4/Meta accounts** — do these exist for the business, or create fresh?

---

## 7. Dev quickstart (new dev, read in order)
1. `HANDOVER.md` — session context + gotchas (Chrome extension unstable; Search & Discovery has no API; theme JSON quirks)
2. This file — plan
3. `SHOPIFY-BUILD.md` — IDs, API app, scripts
4. Theme work: edit `dwell-theme/`, push with the command in §1. API work: token in `.shopify-token`, helpers in `scripts/`, base `/admin/api/2025-01/`.

---

## 8. Improvement Plan (v1.1)
> Added after code-vs-doc audit (2026-07-03). Findings: popup still uses old gold accent `#B48D59` (site moved to madder `#9E3B2F`); popup fires on cart page; no analytics anywhere; SHOPIFY-BUILD.md palette lines stale. Everything else verified matching.

### 8.1 Launch checklist — before payments go live
- [ ] 🤖 Fix `pexx-popup.liquid` accents: `#B48D59` → `#9E3B2F` (eyebrow + code underline)
- [ ] 🤖 Suppress popup on `/cart` + checkout (path guard in the snippet)
- [ ] 🧑🤖 **Analytics (now Phase 1, non-negotiable):**
  - GA4 property → Shopify **Google & YouTube** channel app (native, no theme code)
  - Meta Pixel → Shopify **Facebook & Instagram** channel app
  - Verify 4 events fire: `view_item`, `add_to_cart`, `begin_checkout`, `purchase` (test order)
  - Baseline dashboard: Shopify Analytics + GA4 realtime checked on launch day
- [ ] 🤖 Post-import QA script (`scripts/qa_products.py`): every product has ≥1 image, price > 0, Type set, Age tag on Little items, correct collection. Run before filters wired.
- [ ] 🤖 Sync SHOPIFY-BUILD.md palette lines (gold → madder, scrim `B3`)
- [ ] Existing blockers unchanged: Razorpay connect → COD on → GST in → real catalog imported → filters wired → WhatsApp number in → lawyer sign-off → QA → publish

### 8.2 Top 5 CRO/UX improvements (Phase 2, ordered)
| # | Improvement | Acceptance criteria | Effort |
|---|---|---|---|
| 1 | **Abandoned-checkout + welcome flows** (Shopify Email) | Abandoned email sends ≤4h after abandon; welcome email fires on popup signup; both render on mobile | S |
| 2 | **Judge.me reviews** (post first orders) | Stars on product cards + PDP; review request email 7 days post-delivery | S |
| 3 | **PDP delivery estimate** — "Ships in 3 days from Jaipur · Free over ₹999" near ATC | Line visible above the fold on mobile PDP | S |
| 4 | **WhatsApp per-product prefill** — PDP button includes product title in wa.me text | Enquiry from a PDP names the product without customer typing it | S |
| 5 | **Popup polish** — focus trap, autofocus email, don't fire until 2nd pageview | Keyboard-only user can complete + close; bounce sessions never see it | S |

### 8.3 Artisan content + "Cost of a Block Print" — build without blocking launch
**Principle: metafield-driven, renders nothing when empty.** Ship the code anytime; content lights it up per-product.
- 🤖 Define product metafields: `pexx.artisan_name` (text), `pexx.artisan_photo` (file), `pexx.artisan_video` (file, optional)
- 🤖 PDP block: "Made by {name}" card between accordions and trust band — `{% if metafield %}` guard, zero output otherwise
- 🧑 Production captures artisan name/photo per batch (video optional, later)
- 🤖 "Cost of a Block Print" — one static snippet (carving → dyeing → printing → stitching cost bars), rendered on About + PDP accordion. No metafields needed; copy from requirements §2 diff #5.
- **Sequence:** code ships in Phase 2 week 1 regardless of content; first artisan card goes live whenever the first photo arrives.

### 8.4 Measurement (Phase 1 requirement, restated)
- **Owner setup (🧑):** GA4 property + Meta Business account (or confirm existing — open question #8)
- **Wiring (🤖-guided):** both via native Shopify channel apps — no theme code, survives theme updates
- **Launch-day checks:** purchase event visible in GA4 DebugView on the test order; Meta Pixel Helper green on home/PDP/cart
- **Weekly habit:** Shopify Analytics (conversion funnel) + GA4 acquisition. No custom dashboards until there's traffic to justify them.

### v1.1 scope guard
Everything above is S/M effort for a small team inside 2–3 weeks. Explicitly **not** added: theme rework (done, verified), custom checkout, apps beyond Judge.me + channel apps, loyalty, subscriptions.

---

## 9. High-Performance Organic Growth Plan
> Audit date 2026-07-03. Theme = Dwell (Horizon family). Verified: module/defer JS, woff2 font preloads, Product JSON-LD (`structured_data`), Article schema on blog, per-template assets, meta-tags snippet with og/twitter cards. The gaps are content-layer and migration, not theme architecture.

### A. Performance

**Current problems (concrete, from code):**
- Assets total 1.1MB but load per-template — fine. Largest JS = `qr-code-generator.js` 48KB (gift-card template only — verify it never loads elsewhere).
- `pexx-popup.liquid` inlines ~4KB CSS+JS on every page — negligible, leave it.
- Inline `!important` style block in `theme.liquid` head (collection-card text) — works, leave it.
- **The real risk is unbuilt:** production photos. One 5MB hero JPEG kills mobile LCP regardless of theme quality.
- Fonts preload with `fetchpriority: low` (stock) — hero image will be LCP; confirm Dwell sets `fetchpriority=high`/`loading=eager` on the first hero image (spot-check post-import).

**Targets (mobile, mid-tier Android, PageSpeed Insights):**
- LCP < 2.5s · CLS < 0.1 · INP < 200ms · Lighthouse Perf ≥ 80, SEO ≥ 95

**Implementation steps:**
- [ ] 🤖 **Image discipline in the import script** (S): resize source photos to max 2048px, strip EXIF, target < 400KB before upload. Shopify CDN handles srcset from there. *This one step is worth more than any theme tweak.*
- [ ] 🤖 Post-import PageSpeed run on home + 1 PDP + 1 collection; fix only what scores flag (S)
- [ ] 🤖 Verify hero LCP priority attrs after real hero photo lands (S)
- [ ] 🧑 App restraint rule: every app adds JS. Judge.me + channel apps only; anything else needs a metric justifying it (ongoing)
- Not doing: JS/CSS surgery on stock Dwell (modern loading already; risk > reward), critical-CSS extraction, third-party perf tools.

### B. SEO foundation

**On-site basics:**
- [ ] 🤖 Meta title pattern: `{Product} — Hand Block-Printed {Type} | PEXX` (products), `{Collection} | PEXX` (collections). Set via API at import (S)
- [ ] 🤖 Meta descriptions: unique, benefit-led, ≤155 chars — write during product import; pages/collections in same pass (M)
- [ ] 🤖 One H1 per page audit — verify hero headings render as H1 on home/pages, product title H1 on PDP (S)
- [ ] 🤖 Internal links: each blog article links to ≥1 collection + 1 PDP; each collection description links to sibling collections + relevant pillar page (content rule, ongoing)
- [ ] URL structure: Shopify's `/products/`, `/collections/`, `/pages/` — keep handles short, keyword-first (`/products/indigo-buti-swaddle` not `/products/pexx-product-01`) — enforced in import CSV Handle column

**Content that must exist:**
- Collections: 100–150 word description each (Little / Carry / Gifting + occasion collections) — keyword + internal links (M)
- PDPs: unique descriptions (written at import from photos + specs — never duplicate across colourways) (M, part of import)
- Blog: execute `content-drafts/03-seo-aeo-blog-plan.md` — 2 of ~12 live; 1–2/month cadence (L, ongoing)

**Technical SEO:**
- [ ] 🤖 **Legacy redirect map — CRITICAL, launch day** (S): old poddarexp.com URLs → Shopify URL Redirects via API before DNS switch:
  - `/little.html` → `/collections/little` · `/carry.html` → `/collections/carry` · `/wear.html`, `/interiors.html` → `/` or nearest collection · `/workshops.html` → `/pages/about` · `/contact.html` → `/pages/contact` · `/blog/*`, `/posts/*` → `/blogs/journal` (or per-article where a match exists)
- [ ] Sitemap (`/sitemap.xml`) + canonicals — Shopify native, nothing to do; submit sitemap in **Search Console** on launch day (S 🧑)
- [ ] 🤖 Schema: Product JSON-LD ✅ stock · Article ✅ stock · **FAQPage = missing, we add** (see AEO) · BreadcrumbList — check if Dwell renders breadcrumbs; if not, skip schema, don't build breadcrumbs just for markup (S)
- [ ] 404 page: stock Dwell is fine; add a "Shop Little / Carry / Gifting" link row to the 404 template (S)

**SEO checklist for launch:**
1. Redirect map imported (test 5 old URLs manually post-DNS)
2. Search Console verified + sitemap submitted
3. Meta titles/descriptions on all products, collections, key pages
4. Collection descriptions live
5. Handles keyword-first in import CSV
6. GA4 receiving (already §8.1)

### C. AEO (answer engines)

**Structure rule:** every commercial page answers its top questions in crawlable prose — question-style H2/H3 + a 40–60 word direct answer immediately below, *then* detail. Accordions are fine for UX but the Q&A text must be in the HTML (Dwell accordions are — content is in DOM, just needs question phrasing + schema).

**Where:**
- **PDP accordions** → retitle as questions: "What is it made of?" / "Is it safe for newborns?" / "How do I wash it?" / "When will it arrive?" — first sentence of each = the 40–60 word answer (content-only, no theme change)
- **FAQ page** → already Q&A content; add `FAQPage` JSON-LD via one new snippet rendered on `page.faq` (theme, S)
- **Pillar pages** → add a 3–5 question FAQ block at bottom, same schema snippet

**Pillar pages (improve 3 existing, create 2):**
1. *Gift to India* (exists) — add FAQ block: customs/duties, delivery time to metros, INR payment from abroad, gift note
2. *Return Gifts* (exists) — add: minimum quantity, lead time, bulk pricing, personalisation
3. *Our Story / Why block print* (exists) — add: "What is hand block printing?", "Why does it cost more than screen print?", "Is it colourfast?" (feeds "Cost of a Block Print" later)
4. **NEW:** *Baby gifting guide by occasion* (baby shower / naming ceremony / first birthday) — the highest-intent query cluster in the niche, links every occasion collection
5. **NEW:** *Fabric & safety hub* — azo-free dyes, wash care, newborn skin — one authoritative page every PDP accordion links to

**PDP/category patterns:**
- PDP: question-accordions (above) + first 160 chars of description = standalone answer to "what is this and who is it for"
- Category: description answers "What should I look for in a {swaddle/quilt/tote}?" in 2–3 sentences before the grid

### D. UX & visual improvements (conversion-tied only)

| Change | Why | Type |
|---|---|---|
| Delivery line near ATC: "Ships in 3 days from Jaipur · Free over ₹999" | #1 pre-purchase question, answered at decision point | theme (S) — already §8.2 |
| Age/Occasion filters live at import + linked from collection descriptions | Gifters shop by age/occasion, not product type | config + content (S) |
| Question-style accordion labels (from §C) | Doubles as UX clarity + AEO | content-only |
| 404 page category links | Recovers dead-end sessions post-migration | theme (S) |
| Popup: 2nd-pageview trigger + cart suppression + madder accent | Stop interrupting buyers; brand consistency | theme (S) — already §8 |
| Trust row on PDP under ATC (COD available · 10-day returns · skin-safe dyes) | Compresses the three biggest objections to one glance | theme (S) |
| Mobile nav: verify Little/Carry/Gifting reachable in ≤2 taps from any page | Thumb-distance to revenue | verify only |
| Not doing: breadcrumbs retrofit, mega-menu, PDP redesign, video embeds | Theme is done; no evidence these pay | — |

### E. Phased execution

**Phase 1 — pre-launch (gates payments-on):**
- Image discipline in import script · meta titles/descriptions at import · keyword-first handles · collection descriptions · **legacy redirect map** · Search Console + sitemap · 404 links · PDP trust row + delivery line · question-style accordion labels · FAQPage schema snippet on FAQ page

**Phase 2 — weeks 1–4 post-launch:**
- FAQ blocks + schema on 3 existing pillar pages · *Baby gifting guide* + *Fabric & safety hub* pages · blog cadence resumes (1–2/mo) · PageSpeed audit on real pages, fix flagged items · GA4 landing-page report reviewed weekly → informs next content

**Phase 3 — metric-gated:**
- ≥500 organic sessions/mo → expand blog to full 12-article plan + occasion landing pages per festival
- ≥20 orders/mo → Judge.me review snippets feed star-rich results (Product schema already carries `aggregateRating` once reviews exist)
- Search Console shows question queries → dedicated answer pages for the top 5
- CLS/LCP regress after apps → perf re-audit before adding anything else

> **Open decision (before launch day):** the redirect map above assumes the old poddarexp.com pages retire at launch. If the B2B site should instead live on at a subdomain (e.g. `b2b.poddarexp.com`), the map changes — decide before DNS switch.
