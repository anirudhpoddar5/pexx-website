---
name: pexx-listing-generator
description: Generate SEO/AEO-optimized product listing content (title, description, bullets, specs, tags, image plan) for any PEXX product — quilts, swaddles, dohars, backpacks, pouches, totes — for Shopify, FirstCry, and Amazon India. Use whenever building or updating a product import sheet, writing PDP copy, or preparing a marketplace listing for PEXX.
---

# PEXX Listing Generator

Product-agnostic framework for writing PEXX product listings across Shopify (own store), FirstCry (marketplace), and Amazon India. Built from: PEXX's own brand strategy (`pexx-shopify/ECOMMERCE-REQUIREMENTS.md`), its SEO/AEO blog plan (`pexx-shopify/content-drafts/03-seo-aeo-blog-plan.md`), a teardown of Malabar Baby / Masilo / The Baby Atelier / Amazon.in / FirstCry listings, and Amazon India's actual Blanket-category bulk upload template field list.

**Never fabricate a spec.** Pull material, dimensions, age range, filling, and country of origin from a real source (existing marketplace listing, product spec sheet, or the user directly) — never infer from photos alone. If a fact is missing, ask; don't guess and don't leave it silently blank without a note.

**Never fabricate visual detail either — this failed once, don't repeat it.** Writing copy for N print designs requires actually opening images for *all* N, not extrapolating from one. Before writing per-SKU copy: view **at least 2 images per design** — one front/hero shot and one reverse-reveal (folded-corner or flipped) shot — for every single SKU, not just the first one in a folder. Specifically: **the trim/binding colour is not the same thing as the reverse-side fabric print** — a striped binding very often wraps a *different*, non-striped reverse print (dots, chevron, a second motif). Don't default to "coordinating stripe print" as a filler guess; look at the actual fold. If a detail (motif identity, e.g. "unicorn" vs "pony," or reverse pattern) can't be confirmed from an available image, say so explicitly rather than guessing — a wrong animal/pattern claim is a real product misrepresentation, not a style nitpick.

## 1. Brand rules (non-negotiable, from ECOMMERCE-REQUIREMENTS.md)

- No "handmade with love" or other generic filler — every competitor says this.
- No GOTS claim unless a certificate exists. PEXX is organic-cotton-*standard* but not certified — say "organic cotton" / "cotton voile", never "GOTS-certified".
- No fake discounts / strikethrough pricing.
- Frame print variation as a feature: "small variations in the block print are the mark of genuine handwork, not a flaw" — use this line (or a close variant) whenever the product is hand block-printed.
- Craft/artisan story is a *trust layer*, not the headline. Messaging order: **print/colour → multi-use → skin-safe → gifting → craft (last)**.
- **Always highlight multiple uses.** This is a standing instruction, not optional flavor — every quilt/blanket-type listing must name at least 3 uses explicitly (e.g. kids quilt / stroller blanket / play mat / nursery décor), both in the description and as its own bullet.

## 2. AEO copy pattern + emotional hook

The AEO factual formula alone reads flat — it earns citation value but does none of the "make a parent fall in love with this print" work. Fix: **wrap** the factual core in a sensory open and an evocative close, don't replace it.

> **[Hook — 1 vivid sentence: what the print/colour *does*, imaginatively, for the child — not a spec]** + [Colour/print, 1 clause, factual] + [material + construction, factual] + [who/when it's safe for, factual]. [Multi-use sentence]. **[Reversible + craft line — describe the block-printing process itself (a wooden block, ink, a hand press) rather than only the defensive "variations aren't a flaw" framing].**

Worked example (Tiger Jungle design): *"Golden tigers prowl through a jungle of palms across this ivory quilt — the kind of print that turns nap time into a tiny adventure. Hand block-printed in Jaipur with prowling tigers and palm trees on soft cotton voile with a hand-quilted cotton fill... [factual/multi-use/safety as usual]... Hand block-printed in Jaipur, one wooden block pressed at a time, so no two quilts carry quite the same leaf — flip it over for a palm-only reverse in the same warm palette."*

Keep this hook-and-close treatment to the **Description only**. Title, SEO Title, and the 5 bullets (Section 3) stay factual/keyword-first — that's what the competitor teardown shows actually ranks (Section 7); mixing heavy emotion into a scannable bullet list would work against the proven Amazon/FirstCry bullet formula.

**On Shopify specifically, never ship the description as one dense paragraph — it reads as cluttered, not premium.** Break `Body (HTML)` into 3-4 short `<p>` paragraphs, one idea per paragraph. Do **not** put a `<ul><li>` bullet block in body_html — the theme strips it (Section 4c); spec bullets live in the metafield-driven accordion rows instead (Section 2b).

The original factual-only opener (still correct, just no longer the *whole* opening):

Real example that ranks (haus & kinder, muslin guide): opens with a labeled **"Quick Answer:"** box, verbatim: *"Muslin is the safest, most breathable, most versatile fabric for baby bedding. The loose plain weave allows air to flow, regulates temperature naturally, and reduces overheating risk."* — declarative, no hedging, cites a mechanism. The explicit "Quick Answer:" label is itself part of why it gets lifted — use the same labeled-box pattern on PEXX blog/FAQ content, not just an unlabeled opening paragraph.

If writing a supporting blog/FAQ block, use **question-as-heading + 2-sentence declarative answer**, ideally with a number or standard named, plus an India-climate hook (AC rooms, monsoon humidity, mild North-Indian winters) — e.g. "quilted blankets work better for air conditioned and cooler temperatures" (Masilo's quilt-vs-dohar framing). Target questions for quilts: "best fabric for a baby quilt in India", "quilt vs dohar for a baby", "what size quilt for a toddler", "is block print safe for baby skin". Other citable phrasings worth echoing: "Indian paediatricians typically recommend muslin (mulmul) for newborn bedding," "AZO-free, pre-shrunk muslin... OEKO-TEX skin-safety standards."

## 2b. Product page content split: story (Details) vs specs (metafield-driven bullet rows)

The theme's (Dwell) product accordion has rows built two different ways. "Details" pulls `product.description` (body_html) through `rte-formatter`, which strips lists (Section 4c — still true). But "How do I wash it?" / "When will it arrive?" are static richtext blocks (block type `text`, schema setting type `"richtext"`) rendered through a *different* snippet that does **not** strip lists — confirmed live, real bullets render. "What is it made of?" already existed in `templates/product.json` but showed identical hardcoded text on every product.

Fix (decided 2026-07): make "What is it made of?" and a new "What size is it?" row per-product by pointing each row's richtext `text` setting at a product metafield (`product.metafields.custom.made_of`, `product.metafields.custom.size_specs`) via Shopify's **dynamic source** token — the same mechanism the Details row uses for `{{ closest.product.description }}`, aimed at a metafield and rendered through the non-stripping `text` block. Per-product bullets without ever touching body_html. The theme wiring is a **one-time setup per row**; the two metafield values ship in the CSV at import time (extends Section 4g — ships at import, not a follow-up step).

The content split (merchant-specified — follow exactly):

- **Details (body_html, prose, no bullets)** — pure story: hook (1 vivid sentence, imaginative, what the print/colour *does* for the child) + a print/construction sentence in the same descriptive register — merchant's own example of the register: *"Block-printed with green frogs lazing on lily pads among tiny pink blossoms, finished with a teal-and-sage candy-stripe edge."* — this stays in Details, it's part of the story, not a "spec" — + a multi-use sentence + a craft-close sentence (the block-printing process itself). 3-4 short sentences/paragraphs. This is Section 2's hook-and-close pattern unchanged; the only change is raw fabric-composition/fill/dimension/age-as-data facts move OUT to the two spec rows. Descriptive facts about the print/trim (colour, motif, edge style) stay — they're story.
- **"What is it made of?" (`custom.made_of`, bulleted)** — 1 lead-in sentence, then a real `<ul><li>` list of hard material facts (fabric composition, fill, dye type as a fact), then optionally 1 closing prose sentence for a brand-standard line — this exact existing line is merchant-confirmed fine to keep as prose: *"No synthetics — soft from the first touch, and softer with every wash."*
- **"What size is it?" (`custom.size_specs`, bulleted)** — 1 lead-in sentence, then a real `<ul><li>` list with dimensions in cm and age-fit range as data, then optionally 1 closing prose sentence for graduated-use framing (ties to Section 3b).

Worked example, merchant-approved (Frog Pond quilt) — canonical:

- **Details:** *"Green frogs laze on lily pads across this cream quilt, tiny pink blossoms tucked between — a quiet pond scene for story time and lazy afternoons. It works as a full kids quilt for younger children, a stroller blanket, play mat, or nursery décor throw — then a lightweight travel or AC blanket as your child grows. Hand block-printed in Jaipur, one wooden block pressed at a time, so no two quilts carry quite the same frog."*
- **What is it made of?:** *"Soft cotton voile face with a hand-quilted cotton fill, hand block-printed with azo-free, skin-safe dyes."* + bullets: Fabric: 100% cotton voile / Fill: hand-quilted cotton / Dyes: azo-free, skin-safe + closing prose: *"No synthetics — soft from the first touch, and softer with every wash."*
- **What size is it?:** *"Sized to grow with your child, not just their first year."* + bullets: Dimensions: 110 x 150 cm / Age fit: Newborn – 14 years + closing prose: *"Full coverage up to about 9-10 years, then a throw, travel, or AC blanket as they grow taller."*

This does **not** contradict Section 4c — 4c's finding (body_html strips lists) is still fully correct and is *why* the spec rows moved to metafields instead of living in body_html.

## 3. Bullet formula (works for FirstCry "Key Features" and Amazon "Bullet Points" identically)

5 bullets, `Benefit label: explanation` pattern (this is what the top-ranking Amazon.in competitor, MOM'S HOME, uses — don't reinvent it):

1. **Material bullet** — e.g. "Soft & Breathable Cotton Voile: natural cotton voile face with a hand-quilted soft cotton fill, gentle on skin in every season."
2. **Multi-use bullet** (always include, never skip) — e.g. "Multi-Purpose Use: doubles as a kids quilt, stroller blanket, play mat, or nursery décor throw."
3. **Safety bullet** — e.g. "Eco-Friendly & Skin-Safe: dyed with azo-free, non-toxic colours, safe for daily use."
4. **Construction bullet** — reversible + hand block-print variation line.
5. **Gifting bullet** — e.g. "Perfect Gift Choice: a thoughtful pick for [occasion], blending tradition with modern style."

## 3b. Age range — derive from dimensions, don't just copy an existing listing verbatim

A stated age range on a competing/older listing (e.g. your own FirstCry precedent) may be more conservative than the product actually supports — check it against the physical size before reusing it, per PEXX's own "don't age-restrict, extend product life" principle (Section 1/12 of ECOMMERCE-REQUIREMENTS.md).

Rough Indian child height-by-age (for sizing a rectangular quilt's *full-body coverage* limit): newborn ~50cm, 1yr ~75cm, 3yr ~95cm, 6yr ~115cm, 9yr ~130–135cm, 12yr ~145–150cm, 14yr ~155–165cm. A quilt's *length* (with sleeping margin) roughly caps full lie-down coverage — a 150cm-long quilt covers a child lying down up to ~9–10 years comfortably.

Beyond that height, the product doesn't stop being "usable" — it graduates from primary bedding to a throw/AC blanket/travel or picnic companion, which is a real, sellable use, not a stretch. **State the full range (e.g. "Newborn – 14 years") but write the copy to match: full quilt coverage for younger kids, throw/travel/AC-blanket framing for older ones.** Don't claim full-body sleep coverage at the top of the range if the dimensions don't support it — that's the line between "extending product life" (fine) and overclaiming (not fine, and an AEO risk if it reads as inconsistent with the stated cm dimensions).

## 3c. New sizes: always a variant on the existing product, never a new product

Quilts and Swaddles are planned to get additional sizes added later (confirmed with the merchant, 2026-07). When that happens: the new size must be added as a **new variant on the same existing product** (same handle, an additional `Option1 Value` under an `Option1 Name: "Size"`), not published as a separate new product. This is the standard scalable pattern — Shopify's native Size filter facets on variant options far better than any tag/metafield workaround, and a separate product per size would fragment one print design's reviews, SEO, and collection membership across near-duplicates.

Current live products (7 Quilts, 4 Swaddles) were retrofitted this way: `Option1 Name` renamed from `"Title"`/`"Default Title"` to `"Size"` with the current real size as the single value (Quilts: `110 x 150 cm`; Swaddles: `110 x 110 cm (Set of 2)`) — done specifically so the mechanism is ready before a second size actually lands, so this only needs a `productOptionUpdate`/variant-add when the day comes, not a restructure. Backpacks and Toiletry Pouch Sets were deliberately left on `Title`/`Default Title` — their "size" is a fixed multi-piece dimension set, not a size variant in the same sense, don't force this pattern onto them without a real reason.

**Known limitation to flag, not solve preemptively:** Shopify tags can't be scoped per-variant. Age tags are currently set once per *product* (covering every variant/size uniformly). If a second size on the same product genuinely serves a different age range than the first (plausible — a larger quilt size may suit older kids than the smaller one), there is no clean per-variant age-tagging mechanism today. When this actually comes up, it needs a real decision (e.g. keep the broader combined age range on the product, or split into a genuinely separate product line if the age difference is large enough to warrant it) — don't silently apply one variant's age fit to the whole product.

**Standing instruction: whenever the merchant says a new size is being added to Quilts or Swaddles, proactively remind them of this convention before building anything** — add the size as a variant on the existing product, check whether the age-tag limitation above actually applies for that specific addition, and only then build the CSV/data change.

## 4. Occasion tagging — be specific, don't force-fit

PEXX's occasion axis: `rakhi, diwali, birthday, new-baby, wedding, naming`. **Tag format on the live store is `occ-{value}`** (e.g. `occ-birthday`, `occ-new-baby`) — confirmed against `admin/products/new`; `occ-birthday, occ-new-baby, occ-wedding, occ-diwali` already exist as tags, `occ-naming` and `occ-rakhi` don't yet (fine to create, just note it's new). Assign **2–3 per product**, chosen for genuine fit, not maximum coverage:

- `new-baby` / `naming` (naming ceremony, godh bharai, baby shower) — the strongest fit for any kids quilt/blanket. Real search phrases: "godh bharai gift ideas", "naming ceremony gift for baby", "newborn gift box under ₹1500". Regional terms worth using in backend/meta keywords, not visible copy: *seemantham, valaikappu, dohale jevan, shaad*.
- `birthday` — fits playful/animal/character prints.
- `diwali` — fits neutral, warm-toned prints framed as a festive gift.
- `wedding` — rarely fits a kids quilt directly (favors accessories/carry items instead); only use if the product genuinely suits wedding-favor gifting.
- `rakhi` — **weak fit for quilts** (rakhi shoppers skew toys/personalized items). Research confirms this explicitly — don't tag it just to hit a quota. Leave it off unless there's a real angle (e.g. "rakhi return gift for kids").

## 4b. Vernacular search terms — put them in the visible Title/SEO Title, not just backend keywords

Indian buyers frequently search in Hinglish, not pure English. For quilts/blankets specifically, **"razai"** (the common Hindi word for a quilt) and **"jaipuri" / "jaipur quilt"** (the geographic term shoppers already associate with block-print quilts, and one PEXX genuinely qualifies for) are high-volume real search terms — don't bury them only in Amazon's backend Generic Keyword field. Surface them where a human or a search engine's title-matching actually sees them:

- **Shopify visible Title**: add a parenthetical vernacular tag — `{Motif} Print Reversible Cotton Quilt (Razai)` — keeps the main title clean/brandable while still exact-matching the Hindi-term search.
- **SEO Title (meta title tag, ~60 char)**: lead with the vernacular pairing — `{Motif} Print Kids Quilt / Razai | Jaipur Cotton Voile – PEXX`. This is literally what a parent searching "baby razai jaipur" types, and Google's title-tag matching rewards the exact phrase appearing early.
- **SEO Meta Description**: work "razai" in naturally once, don't force it twice.
- **Amazon title / Generic Keyword field**: both — visible title can include "Razai" and "Jaipuri" (accurate, not stuffing), and reserve genuinely-different-product terms (*dohar, godri* — these are lighter, single-layer products, not synonyms for a quilt) for backend-only, so the visible title stays accurate to what's actually being sold.
- Don't do this for terms that aren't accurate synonyms of *this* product — "razai" and "jaipuri quilt" are correct; "dohar" is a different product category and belongs in backend search terms only, never the visible title, or it misrepresents the item.

## 4c. Shopify theme constraint: Details block strips `<ul>`/`<li>` — use `<p>` only

Verified directly (view raw HTML, edit, re-check the live rendered page): this theme's product-description component (`rte-formatter`, class `...product_description...`) silently drops list markup — a `Body (HTML)` with `<ul><li>` saves fine to `product.body_html` (confirmed via `/products/{handle}.json`) but renders as nothing on the storefront; only `<p>` tags survive. **Never use `<ul>/<li>` in a PEXX Shopify product description** — instead break the AEO hook+factual+multi-use+craft content (Section 2) into 3-4 short `<p>` paragraphs, one idea per paragraph. Same words, just no list wrapper. If a real theme fix is wanted later (patching the Liquid/JS to stop stripping lists), that's a separate theme-code task — don't assume it's fixed without re-verifying via the JSON endpoint. Content that genuinely needs bullets goes in the metafield-driven accordion rows instead — Section 2b.

## 4d. Featured (Position 1) image must crop well as a small square — not just look good full-size

The Position 1 / featured image is what every small-thumbnail context pulls from: sticky add-to-cart bar, "You might also like" cards, collection grids, search results — not just the PDP hero. A wide environmental lifestyle shot (e.g. a child photographed head-to-torso with lots of background) can be a great PDP hero but crops badly into a tight square, landing on empty wall/window instead of the product — this reads as "not premium" even though the full-size image is beautiful.

Before finalizing Position 1 for a product: prefer a shot where the product itself fills most of the frame (flat lay, folded stack, or a close, product-forward lifestyle shot) over a wide environmental portrait. If a wide shot must lead (e.g. it's already live and reordering is disruptive), fix it via Shopify Files → open the image → **click the image to set its focal point** onto the product area — this is a per-file setting that all downstream thumbnail crops respect, verified by reloading the file page and confirming the focal-point marker persisted.

## 4e. Collections: always Automated (smart), never manual — hard rule

Verified the hard way (2026-07, cost 1+ hour): after a 6-product CSV bulk import, products were added to the *manual* collection "Little" via Browse/Edit products + Save. Backend was provably correct (admin product list, storefront `/collections/little/products.json`) but the rendered collection page kept showing only 1 product across browsers/incognito/cache-busting for an extended period. *Smart* collections on the same products ("Birthday", "Diwali", "New Baby") updated instantly. Shopify documents no SLA for manual-collection page propagation; community threads report the same lag. Shopify's own guidance: automated collections for anything definable by a rule, manual only for small hand-curated one-offs (a flash sale, a lookbook).

- **Any collection that maps to a tag/type/vendor pattern must be an Automated collection with a rule** (e.g. "Little" = `Product tag is equal to Kids`). "Little" was converted this way as the fix.
- Membership then becomes a side effect of tagging at import time — no post-import collection step at all (see Section 4g).
- Manual collections only for a genuinely arbitrary hand-picked list with no shared attribute. None currently exist on the store.

## 4e-ii. New product/category: always ask which collections to cross-list into

Found the hard way (2026-07): imported a new "Toilet Kits" line (toiletry pouch set); it obviously belonged in "Carry", but Carry's smart rule was narrowly `Product Type = Backpack`, so it silently missed the collection — only got tagged for Little at first, and the gap was caught because the merchant happened to ask, not because the workflow surfaced it. **Whenever a new product or new product category/type is created, the workflow (Section 10) must explicitly ask the merchant which existing collections (Little, Carry, Gifting, and any collection added later) it should cross-list into** — don't assume just the obvious one. Once the collections are decided, cross-listing is just a tag/type match at import time per Sections 4e/4g — no manual per-collection edit ever — but the *decision* isn't derivable from the product data alone, so it has to be asked.

## 4e-iii. New category: add it to the mega-menu, don't just import products

The site nav (main menu, "Little"/"Carry"/"Gifting") uses this theme's native mega-menu, set to `collection_images` mode (`sections/header-group.json`, block `header-menu`, setting `menu_style`) — every top-level item's children render as an image tile if the child is a real Collection link, or a plain text link otherwise. This is a **global** setting (one value for the whole menu, not per-item), so any collection added as a child anywhere in the main menu inherits image-tile treatment automatically — no per-category code changes needed, ever. The same setting drives the mobile hamburger drawer's tap-to-expand grid too (`snippets/header-drawer.liquid` checks the identical `menu_style`).

**Standing instruction: whenever a new product category/type launches, this is a required step, not optional polish:**
1. Create an Automated collection for it (Section 4e — rule: `Product Type = {the new type}`), same as Quilts/Backpacks/Swaddles/Toiletry Pouches were done (2026-07).
2. **Pick one representative product image for that collection** (`collectionUpdate` → `image: {src: ...}`, or Admin UI) — reuse an existing product photo, no new photography needed. This is what shows as the mega-menu tile.
3. Add it as a child link (type `COLLECTION`, `resourceId` = the collection GID) under the right parent(s) in the main menu — Little, Carry, or both, per whatever Section 4e-ii's cross-listing decision was for that product.

⚠️ The main menu's `menuUpdate` mutation **replaces the entire menu structure** — it is not additive. Always fetch the full current menu (all items, all existing children) first and include everything in the update payload, or sibling items' children get silently wiped. (Learned the hard way, 2026-07 — wiped Gifting's 6 occasion sub-links by only including Little/Carry in an update payload; had to reconstruct and re-push immediately.)

A collection with zero products or no image assigned still renders gracefully in this mega-menu (just a plain text link, no broken image) — fine to leave a low-priority/no-stock occasion collection (e.g. Rakhi, while it has no products yet) without an image rather than force one.

## 4f. Tag namespacing — one taxonomy per prefix, because Search & Discovery filters are tag-value soup otherwise

The Tags field currently mixes two taxonomies: age tags as bare capitalized words (`Baby`, `Kids`, `Newborn`, `Toddler`) and occasion tags as `occ-{value}`. Search & Discovery's auto-generated tag filter sources from **all** product tags, so the "Age" filter displayed age values and `occ-*` values mixed together. Custom tag filters in the app are configured by hand-picking specific tag values — there is **no** prefix/pattern sourcing — so a clean prefix per taxonomy is what keeps a filter's value list pickable and single-purpose.

- **Convention: every taxonomy gets a prefix.** Occasions already do (`occ-`). Age tags should migrate to `age-baby`, `age-kids`, `age-newborn`, `age-toddler`.
- **⚠️ Verify before renaming existing product tags — this is a live store.** The bare `Kids` tag is now the rule for the Automated "Little" collection (Section 4e), and other smart collections may rule on bare age tags too. Renaming a tag without first updating every collection rule (and any theme/filter reference) that matches it will silently empty those collections. Migration order: (1) add the new `age-*` tag alongside the old one on all products, (2) repoint collection rules to the new tag, (3) verify collection pages, (4) only then remove the bare tag. Don't do this as a casual side-task.
- Don't invent further taxonomies; if one genuinely emerges, give it its own prefix from day one.

## 4g. CSV import: the collection-rule tag ships in the `Tags` column, not as a follow-up step

Since collections are rule-based (Section 4e), the CSV generator must emit the rule-defining tag (e.g. the age tag that drives "Little") in each product's `Tags` value at import time, alongside `occ-*` tags. Products then land in their collections the moment the import finishes — never plan a "then manually add to collection" step after a bulk import; that's the exact path that hit the manual-collection lag.

## 4h. Search & Discovery filter deleted by accident — recovery runbook

Removing unwanted values from the auto-generated "Age" tag filter via the per-value **Remove** button ended up deleting the entire filter (2026-07). Unverified whether removing values always collapses a filter or this was a mis-click on a filter-level vs value-level control — treat per-value Remove in this app as dangerous until observed otherwise. Recreate path (Shopify's documented flow):

1. Shopify admin → **Apps → Search & Discovery → Filters → Add filter**.
2. **Source: Tag**, set the label (e.g. "Age"), pick only the wanted tag values, choose AND/OR logic, **Save**.
3. Verify on a storefront collection page that the filter shows only the intended values.

**A human must click through this** — browser automation against this embedded app's UI was confirmed unreliable (clicks don't register). Hand the merchant the steps; don't attempt it via automation.

## 5. Image count and order

Use **every well-composed shot available, prefer 6–8 over capping at 4** if the source folder has them. Order for both customer-facing display and internal reference:
1. Hero / folded or flat lay
2. Lifestyle — in use (bed)
3. Lifestyle — a *second* use case if photographed (play mat / stroller / floor) — directly supports the multi-use claim
4. Close-up of print/block detail
5. Reverse side reveal
6. Scale reference (if available)
7–8. Additional lifestyle/detail as available

## 6. Inventory & bulk fields — answered once, reuse the answer

- **Low stock (3–5 units) does not hurt Shopify's own on-site search** — Shopify ranks by relevance/tags, not stock count, and only removes a product from purchase (not necessarily from search) at zero. **It does matter on Amazon and Google Shopping** — both weight availability into ranking/impressions, and repeatedly hitting zero costs momentum. Default to 3–5 for a new SKU, but flag a restock trigger before it hits zero on marketplace channels.
- **`Bulk` tag** = eligible for Party & Return Gifts, which PEXX's own blog plan prices at ₹100–400. Anything priced meaningfully above that band (e.g. a ₹1,299 quilt) is correctly `No` — write the reason inline (`No — above ₹100–400 return-gift band`) instead of leaving the cell silently blank, so it reads as a decision, not an omission.

## 7. Platform field maps

### Shopify (PEXX's own import pipeline — see `pexx-shopify/content-drafts/PRODUCT-IMPORT-TEMPLATE.csv`)
`Handle, Title, Description, Collection, Type, Age, Occasion, Bulk, Option Name, Option Value, Price, SKU, Inventory, Main Image..Image N, SEO Title (70 char hard limit), SEO Meta Description (160 char hard limit), Image Alt Text`. Title = brandable + one clear keyword + vernacular tag (`{Motif} Print Reversible Cotton Quilt (Razai)`), not keyword-stuffed — Shopify's own on-site search and Google both reward a clean, readable title more than a packed one. See Section 4b for where/how to place "Razai"/"Jaipuri".

**Live Shopify admin, verified directly against `admin/products/new` (2026-07):**

- **Page title / SEO Title: 70-char hard limit** (Shopify's own counter, not the ~60 commonly quoted). **Meta description: 160-char hard limit.** Both enforced in the "Search engine listing" panel — write to these limits exactly, don't estimate.
- **Category taxonomy matters — set it, don't skip it.** Shopify's standard taxonomy has `Home & Garden → Linens & Bedding → Bedding → Blankets` (search "blanket," not "quilt" — "quilt" returns no taxonomy match). Selecting a Category auto-generates **Category metafields** specific to that node, which is where structured spec data actually belongs (and what feeds Google Shopping / Merchant Center filters): for Blankets, that's `Color, Age group, Bedding size, Filler material, Season, Care instructions, Fabric, Warmth rating`. Fill these, don't just rely on free-text Description — this is the single highest-leverage thing missing from the plain CSV-style template.
- **Age group is a multi-select controlled list, not free text.** It's a Metaobject(List) field with fixed entries (`0-6 months, 6-12 months, 1-2 years, Adults, All ages, Babies, Kids, Newborn, Teens, Toddlers, ...`) — you check every age stage the product genuinely serves, you don't write a range string into it. For the 110x150cm quilt (Section 3b: full coverage to ~9-10yr, throw/travel use to ~14yr): check **Newborn, Babies, Toddlers, Kids, Teens**. Keep the human-readable "Newborn – 14 years" phrasing in the on-page Description/Title — that's a *separate* free-text surface from this metafield.
- **`Artisan video`, `Artisan photo`, `Artisan name`** already exist as Product metafields on the live store (empty, unfilled) — this confirms the "artisan at the product level" plan from ECOMMERCE-REQUIREMENTS.md Section on PDP is already wired up in Shopify, just waiting on real artisan data. Flag this as an open input needed from the merchant, don't leave it silently blank in a handoff.
- **Confirmed real tag convention already in use on-store** (don't invent a different format): occasion tags are prefixed **`occ-`** — `occ-birthday, occ-new-baby, occ-wedding, occ-diwali` exist already; `occ-naming` and `occ-rakhi` do not yet exist as tags (creating them is fine, Shopify tags are freeform, but note it's a *new* tag the first time it's used). Age tags are bare capitalized words already in use: `Baby, Newborn, Kids, Toddler` — slated to migrate to `age-*` prefixes, see Section 4f caveat before touching them. Existing Collections: `Carry, Gifting, Home page, Little` — "Little" is now Automated (rule: `Product tag is equal to Kids`), per Section 4e all collections must be Automated. Vendor `PEXX` already exists as a selectable option. Product `Type` has no `Quilt` value yet — first quilt SKU will create it.

### Amazon India (from `BLANKET.xlsm` bulk template, ~270 fields — only the ones relevant to a cotton quilt/blanket)
Required: `SKU, Product Type, Item Name, Brand Name, Product Id Type/Value (GTIN or GTIN-exempt), Country of Origin, Product Description`.
High-value optional/recommended for this category: `Bullet Point (x5), Generic Keyword (backend search terms, 249-byte limit, no repeats of visible words — use Hindi/Hinglish synonyms: razai, dohar, godri, jaipuri quilt), Special Features (x5), Age Range Description, Material (x5 slots), Fabric Type ("100% Cotton Voile"), Fill Material, Pattern, Theme (x5), Animal Theme, Blanket Form, Weave Type, Care Instructions (x5), Included Components, Recommended Uses For Product (x5 — this is the literal field for the multi-use claim), Seasons, Item Thickness, Item Length/Width, Item Package L/W/H/Weight, Compliance - Is Handmade (Yes), Compliance - Printing method (e.g. "Hand Printed - Block")`.

Title formula that ranks (MOM'S HOME, verified top result — real title, use as the literal template): `MOM'S HOME Organic Cotton All Season Baby Quilt | Light Weight | Soft | Perfect for Light Winters | 100x120 cm | 0-3 Year | Lemon | Reversible` → `Brand + Material + Use-case + Size(cm) + Age + Colour + Feature`, pipe-separated, front-load the first 80 characters, 200-char hard limit. Their bullets use the same benefit-label-colon pattern Section 3 already specifies, and bake the gifting angle directly into a bullet: *"Perfect Baby Shower Gift: comes in beautiful hand block prints"* — confirms "hand block print" is already a working ranking phrase in this category, not just a PEXX-specific claim.

Amazon India ranking mechanics (A10 algorithm, 2025/26): relevance is checked **title → backend search terms → bullets → description**, in that priority order — front-load real keywords in the title first, backend terms second, don't rely on the description to carry keywords the title is missing. A10 weighs organic sales velocity and external traffic more heavily than the older A9 did.

### FirstCry
No public bulk template; matches marketplace convention from PEXX's own existing listing + top competitors:
Title formula: `[Brand] [Material] Quilt [Print Name] Print – [Colour]`, e.g. "Babyhug 100% Cotton Digital Printed Quilt Unicorn". Spec block always shows: exact `L x B cm`, age band (e.g. "0–3 years"), material, filling, care instructions, "Items included: 1 Quilt", Country of Origin. PEXX's own existing FirstCry listing ("PEXX Premium Cotton Comfort Baby Quilt with Puppy Print, 0–2.5 years, L110 x B110cm") should set the title-formula precedent for new listings on that channel specifically. Ranking factors (per seller-community consensus, no official doc): stock availability (out-of-stock tanks rank), listing completeness against every structured field (age/size are URL-facet filters — filling them *is* the SEO), white-background + scale-reference images (a hand or baby in-frame for scale), low return/cancellation rate.

## 8. Known PEXX reference specs (verified, reuse rather than re-deriving)

- Brand: PEXX, hand block-printed textile brand, Jaipur.
- Existing FirstCry precedent listing: "PEXX Premium Cotton Comfort Baby Quilt with Puppy Print, 0–2.5 years, L110 x B110cm" — a *different* print/size than the 150x100 collection; don't conflate specs across product lines. Its stated "0–2.5 years" is also a conservative age cap for its size — re-derive age from dimensions per Section 3b rather than copying an old listing's number verbatim.
- The 150x100-folder quilt line's real dimension is **110 x 150cm** (confirmed by the merchant over the folder-name's "150x100"), age range **Newborn – 14 years** with graduated use framing (Section 3b).
- Design #4 motif is confirmed **submarine** (merchant-confirmed) — not astronauts/space, despite Shopify's own AI alt-text suggestion reading the same elongated-capsule-with-portholes print as "gray astronauts and green planets." Don't re-flag this as ambiguous; it's settled.
- Country of Origin: India.
- Standard package: "1 Quilt" (or relevant unit) unless the product is sold as a set.

## 9. Sources (competitor teardown, verified)

- [Malabar Baby quilts](https://www.malabarbaby.com/collections/quilts), [Erawan quilt PDP](https://www.malabarbaby.com/products/erawan-natural-cotton-quilt-fw16jali005) — title formula `[Place name] [Colour] Baby Quilt`; specs "100% Indian cotton voile exterior, natural cotton filling," hand-quilted/block-printed with carved wooden stamps, reversible; dye-variance reframed as authenticity ("real turmeric... may release colour on first wash").
- [Masilo Modern Heirloom quilt](https://masilo.in/products/quilted-blanket-modern-heirloom-natural) — title formula `Organic Cotton [Product] – [Collection Name] ([Colour])`; opens with heritage story ("tomorrow's modern heirloom"); GOTS-certified (PEXX is not — don't copy the certification claim, only the structure).
- [MOM'S HOME Amazon.in listing](https://www.amazon.in/Organic-Cotton-Summer-Blanket-Bedspread/dp/B07D1HTRK4) — top-ranking title/bullet formula, quoted in full in Section 7.
- [FirstCry quilts category](https://www.firstcry.com/blankets,-wrappers-and-sleeping-bags/quilts-dohar-and-comforter?cid=8&scid=107&sub-type=t1-289)
- [haus & kinder muslin guide](https://hausandkinder.com/blogs/the-home-expert/muslin-bedding-babies-gold-standard) — "Quick Answer:" AEO pattern, Section 2.
- [Amazon India A9/A10 SEO guide](https://ecomprotips.in/how-to-rank-products-on-amazon-india-in-2025-a9-a10-algorithm-seo-ads-guide/), [A10 playbook](https://www.threecolts.com/blog/amazon-seo-a10-algorithm/)
- [FirstCry seller guide](https://sellerseva.com/how-to-sell-on-firstcry/)
- Gifting-occasion keyword research: [Godh bharai gift guide](https://zizuka.in/blogs/news/godh-bharai-baby-shower-gift-ideas-india), [Smartpuja godh bharai](https://www.smartpuja.com/blog/godh-bharai/) — confirms Section 4's regional-terms list (*seemantham, valaikappu, dohale jevan, shaad*) and that rakhi skews toys/personalized (weak fit for quilts, Section 4).
- Live Shopify admin (`admin/products/new`, verified 2026-07) for Category taxonomy, metafields, character limits, and tag conventions — see Section 7 Shopify subsection.

## 10. Workflow when invoked

1. Confirm the real spec facts (material, dimensions, age range, filling, price, inventory) — ask if not supplied, don't infer from photos.
2. If this is a new product or new category/type: ask which existing collections (Little, Carry, Gifting, and any added later) it should cross-list into (Section 4e-ii) — the answer becomes tags/type values in the CSV (Section 4g), not a manual step.
3. Confirm which platform(s) this listing is for — the field set and title formula differ per platform (Section 7).
4. Write the content once, split per Section 2b: the Details story (Section 2), the two spec metafield values (`custom.made_of`, `custom.size_specs`), and the 5-bullet block (Section 3) — reused verbatim or near-verbatim across platforms.
5. Assign occasion tags per Section 4, image plan per Section 5.
6. Output in whatever format the platform needs (Shopify xlsx/csv matching the existing template, including the two metafield columns per Section 2b; Amazon field list per Section 7; FirstCry spec block).
