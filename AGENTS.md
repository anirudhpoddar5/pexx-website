# PEXX — website and Shopify store

Entry point for this repo. Shared rules live in `.agents/standards/` and are
written by `~/Projects/standards/sync.mjs` — edit the canonical files there,
never the copies here.

- `.agents/standards/SKILL-ROUTING.md` — **which skill to invoke for which
  task. Read it before starting work.**
- `.agents/standards/BASELINE.md` — what "done" means, testing, deployment.
- `.agents/product-marketing.md` — positioning, ICP, voice.

## The five that must never be missed

1. **The owner is not a coder.** End every substantive message with a short
   plain-English summary: what it means, what he must do, what it costs, and
   what is waiting on him. Lead with the consequence, not the mechanism.
2. **Ads have a runbook and it outranks your memory.**
   `pexx-shopify/META-ADS-RUNBOOK.md` is the source of truth. The real account
   is `act_1350379969884972` — **not** the id in the Ads Manager URL. Invoke
   the `ads` skill before touching strategy, budget or targeting.
3. **Storefront filters break silently.** Size is a **variant option**; Colour
   is the **`custom.colour` metafield** on a constrained list. Get either wrong
   and the product vanishes from filtered collection pages with no error.
4. **Ask before anything that touches live customers or costs money** —
   publishing a theme, sending a campaign, raising ad spend, changing prices or
   discounts. Discounts stack: check `combinesWith` on both sides.
5. **Every product image ships at 1600px.** Originals and restore scripts are
   in `~/Desktop/ECOM Final/_image-restore/`. View every image in a set before
   listing it — AI-generated sets have shipped wrong-product and
   self-contradicting images.

## Layout

| Path | What it is |
|---|---|
| `pexx-shopify/dwell-theme/` | The live Shopify theme |
| `pexx-shopify/scripts/` | Python/TS automation against the Shopify Admin API |
| `pexx-shopify/whatsapp-worker/` | Cloudflare Worker — use the `cloudflare` and `wrangler` skills |
| `pexx-shopify/content-drafts/` | Copy awaiting review, not live |
| `.agents/` | Standards, marketing context, plans |

## Credentials

Tokens are read from files, never hardcoded and never pasted into chat — see
`pexx-shopify/.meta-token` for the pattern. The owner creates the file; scripts
read it.

## Known ceilings

- Products are priced under **₹1,299**; free shipping over **₹750**.
- Quilts are **100×100 cm**. Any 110×110 size guide is wrong and quarantined.
- The PDP gallery is locked to **4:5 portrait** — square infographics lose their
  edge text. Fix is the `aspect_ratio` setting, not more pixels.
