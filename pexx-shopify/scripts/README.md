# Scripts

All scripts read the Admin API token from `../.shopify-token` (gitignored — see
`SHOPIFY-BUILD.md` for how it's captured/rotated). Shop: `pexx-7935.myshopify.com`.

Python scripts need no dependencies beyond the standard library. TypeScript
scripts run directly on Node 22.6+/24 (native type stripping) — no build
step, no npm install.

| Script | Language | What it does | Run |
|---|---|---|---|
| `shopify-oauth-capture.py` | Python | Captures/refreshes the Admin API token | `SHOP=… CLIENT_ID=… CLIENT_SECRET=… python3 scripts/shopify-oauth-capture.py` |
| `setup_nav.py` | Python | Writes the main-menu nav items | `python3 scripts/setup_nav.py` |
| `upload_assets.py` | Python | Uploads brand images to Shopify Files | `python3 scripts/upload_assets.py` |
| `seed_catalog.py` | Python | Creates placeholder catalog + collections | `python3 scripts/seed_catalog.py` |
| `setup_pages.py` | Python | Idempotently ensures the pillar Pages exist with the right handle + `template_suffix`; creates missing ones with placeholder body + meta description | `python3 scripts/setup_pages.py` |
| `deploy_theme_assets.py` | Python | Pushes specific `dwell-theme/` files to a theme via the Admin **Asset API** and reads each back to confirm — no `shopify theme` CLI | `python3 scripts/deploy_theme_assets.py [--theme-id ID] <path> [<path> ...]` (paths relative to `dwell-theme/`) |
| `applyRedirects.ts` | TypeScript | Reads `redirects.csv`, creates any legacy→new URL redirects that don't already exist | `node scripts/applyRedirects.ts --dry-run` to preview, `node scripts/applyRedirects.ts` to apply |
| `checkCatalog.ts` | TypeScript | Read-only: flags products missing an image, price, Type, or Age tag (Little items) in a product CSV | `node scripts/checkCatalog.ts [path/to/products.csv]` (defaults to `content-drafts/PRODUCT-IMPORT-TEMPLATE.csv`) |

## redirects.csv

`path,target` pairs applied by `applyRedirects.ts`. Currently covers the
static-page legacy URLs from PRODUCTION-BUILD-PLAN.md §9B. Deliberately
**excludes** `/blog/*` and `/posts/*` → `/blogs/journal` — Shopify's redirect
API matches exact paths, and wildcard support needs confirming (or the real
list of old post URLs needs gathering) before those rows are added here.

## setup_pages.py — page/template map

| Handle | Template (`template_suffix`) | Notes |
|---|---|---|
| `faq` | *(none — default template)* | FAQ schema is gated on handle, not template |
| `gift-to-india` | `gift-to-india` | |
| `return-gifts` | `return-gifts` | |
| `about` | `about` | Our Story / Why block print |
| `baby-gifting-guide` | `baby-gifting-guide` | Created by this script if missing |
| `fabric-safety` | `fabric-safety` | Created by this script if missing |

A `template_suffix` only renders correctly once the matching
`dwell-theme/templates/page.<suffix>.json` file has been pushed to the Dwell
theme on Shopify. Deploys go through the Admin API, not the CLI:

```
python3 scripts/deploy_theme_assets.py templates/page.baby-gifting-guide.json templates/page.fabric-safety.json
```

## deploy_theme_assets.py — notes

- Uses the REST **Asset API** (`PUT /themes/{id}/assets.json`) directly — no
  `shopify theme` CLI call anywhere in this script.
- Verification is semantic for `.json` templates: Shopify's API strips any
  leading `/* comment */` header and re-serializes the JSON (escaped
  slashes, expanded arrays) when you save it, so a byte-for-byte check would
  always report a false mismatch. The script parses both sides and compares
  the resulting structures instead. Plain-text assets (`.liquid`, `.css`,
  `.js`) are compared byte-for-byte, with one short retry in case of a
  read-after-write lag.
- Binary assets (images/fonts) aren't handled here — use `upload_assets.py`
  / Shopify Files for those.
