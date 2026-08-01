# PEXX — Session Handover

Paste the block below into a fresh Claude Code session opened in this folder.

---

You're continuing the build of **PEXX**, a D2C Shopify store for hand block-printed **kids merchandise + accessories** (same brand as the existing B2B site poddarexp.com, repositioned for consumers). Read these repo docs first — they hold the full context:
- `ECOMMERCE-REQUIREMENTS.md` — strategy, positioning, competitor research
- `SHOPIFY-BUILD.md` — technical build log (store handle, theme IDs, API scripts, what's built)
- `LAUNCH-CHECKLIST.md` — operational steps to go live, with owners
- `content-drafts/` — page copy + `PRODUCT-IMPORT-TEMPLATE.csv`

## Key facts
- **Store:** pexx-7935.myshopify.com. Storefront password: `rimeup`. User is logged into admin.
- **Theme:** the real build is **Dwell (draft) #165377146969** — preview at `https://pexx-7935.myshopify.com/?preview_theme_id=165377146969`. Live theme is still placeholder Horizon (publish Dwell only at launch). Local files: `pexx-shopify/dwell-theme/`. Push from repo root with:
  `shopify theme push --path pexx-shopify/dwell-theme --store pexx-7935.myshopify.com --theme 165377146969`
- **Admin API:** token in `.shopify-token` (custom app "PEXX API"). Scopes: write/read products, write files/themes/content, write nav. **No discounts / no app-config / no settings scope.** Helper scripts in `scripts/` (seed catalog, nav, asset upload, oauth capture).
- **Positioning:** benefit-led order — print/colour → skin-safe → made-to-keep → honest price → **craft last**. The "Why PEXX" argument (Cluster D: Indian-priced + real block-print + kids/gifting) runs as a promise spine across homepage → Our Story → every page.

## Built & verified
Homepage (wordmark, scrim hero, pull-quote→Our Story, 3 category tiles, gifting band→Return Gifts, Gift-to-India band, footer) · Our Story · Return Gifts (with bulk enquiry form, product pre-fill) · Gift to India · Send Rakhi · FAQ + Shipping/Returns/Privacy/Terms · Contact · footer menus · PDP (benefit accordions, "Buying in bulk?" callout→prefilled enquiry, "real not printed" band, recommendations) · capture popup (hands out WELCOME15) · gift-wrap (₹99 product `43472878370905`) + gift-message cart note · occasion smart-collections · 2 SEO blog articles · trust bar incl. "Free shipping over ₹999".
**11 test products** exist with variant demos (Quilt=Size, Swaddle=Pack, Trio=single).

## Pending — admin/user (no API; mostly need their accounts)
1. **Delete the broken "Age" filter** in Search & Discovery (it lists all tags). Leave Availability/Price/Product Type.
2. **Finish shipping rate:** edit Domestic "मानक ₹379" → Standard ₹99; + create an **automatic Free-shipping discount, min ₹999** (clean way to do "free over ₹999").
3. **WELCOME15** discount — user creates (token can't). 
4. Razorpay KYC + COD, GST, Shopify Markets multi-currency (NRI; Razorpay is INR-first — may need PayPal), WhatsApp app, DNS email auth (Sender = info@poddarexp.com), legal review of Privacy/Terms.

## Pending — buildable (Claude)
- **Remove the 11 test products** before real import (user reviewing them first).
- **Real products:** production fills `PRODUCT-IMPORT-TEMPLATE.csv` (Option Name/Value supports Size or Pack or single) + sends a photo folder. **You have vision** — you can look at photos and generate titles/descriptions/type/tags; production supplies price/SKU/stock/specs. You import + attach images via API.
- After real products: set up clean **Age/Occasion filters** (metafield, friendly labels), Judge.me reviews wiring, WhatsApp button wiring.

## Gotchas
- **Chrome extension was extremely unstable** (dropped every action). Don't rely on it for multi-step admin; prefer API or hand clear steps to the user.
- **Search & Discovery filters have NO API** — app UI only, and it resists automation.
- **Theme JSON quirk:** product/section blocks need exact `block_order`; some Dwell text had non-breaking spaces — edit JSON via Python and validate.
- Use the API (token) for products/collections/nav/files/pages — reliable. Theme edits via `shopify theme push`.

## Immediate next step
Confirm with the user whether to remove the test products, then either await the filled product sheet + photos, or knock out any remaining design/content tweaks. The build is essentially complete; the gate to launch is real product data + the user's account setups (Razorpay etc.).
