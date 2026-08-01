# Repo map — two projects in here

## Root = the live website (poddarexp.com)
GitHub Pages serves this from the repo root (`CNAME → www.poddarexp.com`).
`index.html`, the category pages (`carry.html`, `wear.html`, `little.html`, `interiors.html`, `workshops.html`, `contact.html`), their root-level `.jpeg/.png` images, plus `assets/`, `blog/`, `data/`, `posts/`.
⚠️ **Don't move or rename these** — pages reference images by bare filename; moving anything breaks the live site.

## `pexx-shopify/` = the PEXX Shopify D2C build
Everything for the pexx-7935.myshopify.com store:
- `dwell-theme/` — the live theme (#165870567513, role `main`). Push from repo root:
  `shopify theme push --path pexx-shopify/dwell-theme --store pexx-7935.myshopify.com --theme 165870567513`
- `scripts/` — API helpers (seed catalog, nav, asset upload, oauth). They read the token relative to `pexx-shopify/`.
- `content-drafts/` — page copy, `PRODUCT-IMPORT-TEMPLATE.csv`, `POLICIES-FINAL.md`
- `.shopify-token` / `.shopify-secrets` — API creds (gitignored)
- Docs: `HANDOVER.md`, `SHOPIFY-BUILD.md`, `LAUNCH-CHECKLIST.md`, `ECOMMERCE-REQUIREMENTS.md`, `DNS-EMAIL-RECORDS.md`

## `mimansa-journeys-build/` — separate, untouched.
