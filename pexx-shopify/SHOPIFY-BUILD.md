# PEXX Shopify Build — Ops & Connection Log
> Living technical record of the store build. Companion to [ECOMMERCE-REQUIREMENTS.md](ECOMMERCE-REQUIREMENTS.md) (strategy) — this file is the *how it's wired*.

---

## Store
- **Handle:** `pexx-7935.myshopify.com`
- **Admin:** https://admin.shopify.com/store/pexx-7935
- **Plan:** Basic
- **Custom domain (current, not yet switched):** www.poddarexp.com (on GitHub Pages — leave until launch)

## Themes
| Theme | ID | Role |
|---|---|---|
| Horizon | 165376688217 | **Live** — original default, untouched backup |
| Dwell | 165377146969 | **Build theme** — all PEXX work happens here (local: `dwell-theme/`) |

- Preview build: https://pexx-7935.myshopify.com?preview_theme_id=165377146969
- Theme is edited locally and pushed (from repo root): `shopify theme push --path pexx-shopify/dwell-theme --store pexx-7935.myshopify.com --theme 165377146969`
- CLI authenticated via `shopify` login (theme scope).

## Why Dwell
Horizon-family theme built for **baby/kids + lifestyle**. Kept Newsreader serif headings (editorial warmth, Craft-like) + Manrope sans body (scannable prices/benefits). See requirements §2.

## Brand foundation (applied)
- Palette: background `#F3EDE3` warm cream · foreground `#2B241F` brown-ink · accent `#B48D59` gold · soft `#E8DDC9` · border `#D8C7AD`
- Fonts: Newsreader (serif) + Manrope (sans). Cormorant Garamond unavailable in Shopify's hosted fonts → not used.

## Design system (premium pass)
- **Type split:** serif **italic** (Newsreader light, h1 64px) reserved for *emotional moments only* — hero headline, pull-quote. Crisp **sans** (Manrope, uppercase, letter-spaced) for *all structural labels* — nav, category titles (Little/Carry), section titles, eyebrows. Accent font = Manrope so eyebrows render sans.
- **Gold** does real work: eyebrows, section rules, "Shop →" links, trust icons — not just badges.
- **Logo:** header + footer render the serif **PEXX** wordmark (global `logo` unset → shop-name fallback in heading font). Icon `logo-pexx.png` set as **favicon**. (For a visible icon on the dark footer, would need a cream/inverse version — deferred.)
- **Hero:** strengthened warm scrim (`#1C130CC0`, gradient to right) so cream serif reads over the busy photo.
- **Pull-quote ink** warmed to `#5A4C3E` (not stark near-black).
- **Gifting block:** deep-brown band, cream text, gold eyebrow — the luxury-contrast moment.
- Reference mockup approved by client before implementation.

---

## API Connection (Admin API)

**Method: OAuth via Dev Dashboard app + local callback capture.**
The store is migrated to Dev Dashboard-only, so the simple custom-app `shpat_` token flow is disabled. Instead we run a local server as the OAuth backend to capture a real token.

- App: created in Dev Dashboard ("Pexx Build"), legacy install flow = true
- Scopes: `write_products, read_products, write_files, write_themes, write_content, write_online_store_navigation`
- Redirect URL registered on app: `http://localhost:3456/callback`
- Capture script: `scripts/shopify-oauth-capture.py` (run with SHOP/CLIENT_ID/CLIENT_SECRET env)
- Captured token saved to `.shopify-token` (gitignored, never committed)
- Secret handling: Client Secret used only locally for the code→token exchange; rotate/delete the app in Dev Dashboard to revoke at any time.

**Status:** ✅ connected. Token captured in `.shopify-token`, verified against `shop.json` (PEXX / INR / Basic). Client ID `1a88856d…aaa92`. Secret stored in `.shopify-secrets` (gitignored) — **rotate or delete the app after build to revoke.**

**Re-capture if token revoked:** `SHOP=pexx-7935.myshopify.com CLIENT_ID=… CLIENT_SECRET=… python3 scripts/shopify-oauth-capture.py` → open http://localhost:3456

---

## Build progress
- [x] Theme foundation (palette + fonts) on Dwell
- [x] Homepage — hero, brand line, trust bar (announcements), Little/Carry sections, gifting feature. Benefit-led copy.
- [x] API token captured (OAuth capture)
- [x] Brand images uploaded (logo → `shopify://shop_images/logo-pexx.png`, hero → `…/hero-pexx.jpg`) + wired
- [x] Collections: Little (469864218713), Carry (469864251481), Gifting (469864284249) — with category images
- [x] Placeholder products — 10, with real category images + tag schema (category/type/age/price-band/occasion/bulk)
- [x] Navigation menu (main-menu): Little · Carry · Gifting · Journal · About
- [x] Content pages rebuilt premium (custom section templates: hero + alternating image/text + FAQ): **Our Story** (`page.about` — "Why PEXX" argument, brand-level/extensible), **Return Gifts** (`page.return-gifts` — bulk CTA → /pages/contact), **Gift to India** (`page.gift-to-india` — currency/occasion). All use real original-brand imagery + the gold-eyebrow→serif-headline→sans-body system.
- [x] **Brand promise spine** runs across the site: homepage trust bar + pull-quote ("Safe for the littlest skin, genuinely hand block-printed, made to keep — honest price, never a fake sale") + OUR STORY link → Our Story's 5-promise argument → echoed on each content page. Positioning ref: requirements §2 (Cluster D).
- [x] Nav: Gifting is a dropdown (Gift Sets · Party & Return Gifts · Gift to India). Contact page exists for bulk quotes.
- [x] Homepage premium pass: Didot PEXX wordmark, serif/sans type split, hero scrim, warm pull-quote, gold accents, 3 equal category tiles w/ scrim+cream labels, balanced gifting band, OUR STORY → /pages/about. Verified in-browser.
- [x] Product page (PDP, `product.json`): real benefit-led accordions (Materials+Care = azo-free/skin-safe + wash care; Shipping+Returns = ready-to-ship 3 days, COD, 10-day returns), "You might also like" recommendations, and a "Real, not printed → Block-printed by hand" trust band (carved teak blocks) reinforcing the promise spine. Verified.

## Built & verified (storefront)
Homepage · Our Story · Return Gifts · Gift to India · PDP · nav (Gifting dropdown) · homepage entry points for both gifting pages. One coherent brand argument throughout.

## Remaining to go LIVE (operational — not theme build)
- Real products/photos/prices/variants from production (replace 10 placeholders)
- Payments (Razorpay/Shopify Payments + COD), shipping zones, GST/tax config
- Multi-currency for NRI (Shopify Markets) + international cards/PayPal
- WhatsApp (Interakt/Wati), reviews app, customer-capture popups
- Real bulk-inquiry form on Return Gifts (currently CTA → contact page)
- GOTS/OEKO-TEX certification claims when secured
- Switch domain poddarexp.com → Shopify (launch day) + re-enable password until then
- Rotate/delete the "Pexx Build" API app after build to revoke token
- [ ] Automated tag-based sub-collections (Sleep/Pack/By Age, occasion gifting)
- [ ] Marketing: customer-capture popups, time-limited coupon setup

## API scripts (`scripts/`)
- `shopify-oauth-capture.py` — token capture server
- `seed_catalog.py` — collections + placeholder products
- `setup_nav.py` — main-menu nav
- `upload_assets.py` — Files upload (logo/hero) → refs in `.asset-refs.json`
All read token from `.shopify-token`. Admin API base: `/admin/api/2025-01/` (REST) + `/graphql.json`.

## Assets available (in repo root)
`logo-pexx.png`, `hero-pexx.jpeg`, `category-little.jpeg`, `category-carry.jpeg`, plus `*-hero-collage.jpeg`. Content drafts in `content-drafts/`.
