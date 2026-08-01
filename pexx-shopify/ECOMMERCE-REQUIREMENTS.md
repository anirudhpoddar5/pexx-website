# PEXX Ecommerce Store — Requirements Document
> Working draft. Review, edit, and confirm before development begins.

---

## 1. What We're Building

A Shopify-based ecommerce store for PEXX, a hand block printed textile brand from Jaipur. 

**Launch scope (Phase 1):** Kids merchandise + Accessories (bags, pouches, totes).  
Home and clothing categories are deferred to Phase 2.

**Platform:** Shopify Basic ($29/mo) with a custom theme that mirrors the existing PEXX visual identity.

---

## 2. Strategic Positioning

### The role model: Malabar Baby (malabarbaby.com)
A US brand doing hand block-printed baby textiles — GOTS-certified, artisan-transparent, gifting-first, photography-led. Swaddle gift sets run $50–$418. Free name embroidery, corporate gifting, block-printing process shown on product pages.

**PEXX's opportunity:** Be the Indian-market version of Malabar Baby — INR-priced, optimised for Indian gifting occasions (baby showers, naming ceremonies, Diwali, Rakhi), with the same craft depth. No Indian brand holds this position.

### The gap we're filling
The Indian kids textile market has three clusters — none of which PEXX sits in:
- **Cluster A — Mass functional** (Kassy Pop, SuperBottoms): Discount-heavy, no artisan angle
- **Cluster B — Design-led organic** (Masilo, The Baby Atelier): GOTS-certified, modern aesthetic, but craft process invisible
- **Cluster C — International artisan** (Malabar Baby): Block-printed, GOTS, gifting-first — USD-priced, not built for Indian occasions

**PEXX fills Cluster D:** Domestic INR pricing + block-print craft transparency + Indian gifting occasions. This lane is empty.

### What we will NOT do
- No permanent 50% off sales (kills brand equity — see Aachho, Tjori)
- No discount-first homepage
- No generic "handmade with love" copy — every brand says this
- No age-restrictive swaddle copy ("only for newborns") — show 5+ uses, extend product life

### What makes PEXX different
1. **Artisan at the product level** — name, face, 15-sec video of the artisan who made *this specific product*, on the product page. Not buried in About Us.
2. **Never discount — use scarcity instead** — named seasonal collections, limited print runs, "when it's gone it's gone"
3. **Block print for kids as a focused identity** — not an afterthought to adult wear
4. **Own Indian gifting occasions** — baby shower, naming ceremony, homecoming, birthday, Diwali, Rakhi — curated bundles, price-tiered (₹1,500 / ₹3,500 / ₹7,000)
5. **Make pricing legible** — a "Cost of a Block Print" breakdown pre-empts the Amazon price comparison
6. **Packaging as product** — block-printed gift wrap/box + artisan story card inside every gift order
7. **Certifications stack** — pursue GOTS + OEKO-TEX Standard 100 Class I together; no Indian brand currently holds both (see Section 8)

---

## 3. Product Catalog (Phase 1)

### Category: Little (Kids) — products ready
- Quilts (2 sizes)
- Pouches
- Backpacks
- Laptop / iPad sleeves (also positioned as stationery storage kits)
- Swaddles
- Dohars

### Category: Carry (Accessories)
- Tote bags
- Weekend / carry bags
- Toiletry pouch sets (sets of 3)
- Travel bags

### Per-product data needed before launch
- [ ] Product name
- [ ] Description (we can draft these)
- [ ] Price (INR)
- [ ] Multiple images: flat lay / lifestyle (child using it) / close-up of print detail / scale reference / packaging
- [ ] Variants (size, color, print name)
- [ ] Stock quantity per variant
- [ ] SKU per variant
- [ ] Artisan name + photo who made it
- [ ] Print/block name (e.g. "Bel Boota", "Jaal", "Phool")
- [ ] Material composition
- [ ] Care instructions
- [ ] "Ready to Ship" or "Made to Order (X days)"

---

## 4. Site Architecture & Navigation

### The model: one product, many lenses
A product exists **once** in Shopify (one SKU, one inventory count) but appears in **many collections** at the same time — driven by **tags**. No duplication, no split stock. A kids pouch surfaces under Little, Gifting, and "Under ₹1000" simultaneously. This is how cross-posting works natively.

**Naming principle:** creative label in the nav, searchable term in the page title/H1. Nav says "Little"; the collection page H1 + SEO title is "Kids Swaddles, Quilts & Bedding." Personality + SEO, both.

### Navigation

```
LITTLE                    (kids)
 ├─ Sleep                 → swaddles, dohars, quilts
 ├─ Pack                  → backpacks, pouches, stationery/iPad sleeves
 └─ By Age                → Just Born (0–6m) · Baby (0–2) · Kid (3–6) · Big Kid (6–12)

CARRY                     (accessories — grown-up)
 ├─ Totes
 ├─ Weekenders            → weekend & travel bags
 └─ Trios                 → toiletry pouch sets of 3

GIFTING
 ├─ For the Occasion      → Rakhi · Diwali · Birthday · New Baby · Wedding · Naming
 ├─ Party & Return Gifts  → bulk 10+ inquiry flow
 └─ Gift to India         → NRI / festival landing pages, multi-currency

JOURNAL
ABOUT
```

- Kids "Pack" items and adult "Carry" items stay visually separate in nav (a parent shopping for a kid shouldn't wade through weekenders), but cross-tag so kids bags can also appear in a sitewide "All Bags" or Gift view.
- **Stationery/iPad sleeves:** primary home is Little → Pack, but cross-tagged into Carry too (adults buy laptop sleeves).
- **By Age** shows the real age range under each playful tier label — nobody guesses.

### Tagging schema (the engine)
Tag every product on these axes at upload. Automated collections build themselves from tags; add a new festival next year = one new tag, zero rework.

| Tag axis | Values |
|---|---|
| `category` | kids, accessories |
| `type` | swaddle, dohar, quilt, backpack, pouch, sleeve, tote, weekender, toiletry-set, travel-bag |
| `age` | just-born, baby, kid, big-kid, all-ages |
| `occasion` | rakhi, diwali, birthday, new-baby, wedding, naming |
| `price-band` | under-1000, 1000-1500, 1500-2500, 2500-plus |
| `bulk` | yes *(eligible for Party & Return Gifts)* |
| `colour` / `print` | (for filtering) |

> **Implication for production:** their "category" answer at upload is just these tags. The production checklist (Section 15) is simplified accordingly.

**Collections** = seasonal drops, limited runs, never permanently on sale.

---

## 5. Homepage Structure

### Above the fold
- Full-bleed lifestyle photo: child with block-printed bag or pouch, real environment, warm natural light (not studio white)
- Headline: TBD — NOT "handmade with love", something specific to PEXX's identity
- Two CTAs: "Shop the Collection" + "How It's Made"

### Trust bar (immediately below hero — must be visible on mobile)
Five icons:
- Hand Block Printed
- Artisan Made in Jaipur
- Safe for Kids (no harsh dyes)
- 10-Day Returns
- COD Available

### Collections strip
2–3 named collections with editorial imagery

### Artisan spotlight
- One artisan: name, face, 15-second video clip
- "This bag was block-printed by [Name] in Sanganer. She has been printing for 18 years."

### Gifting occasions strip
Clickable tiles: Birthday / New Baby / Diwali / School → each leads to a curated gift collection

### Social proof
- UGC photo strip from Instagram (real parents, real kids)
- Review count if available at launch

### Newsletter capture
- Not just "10% off" — "Be first to know when new blocks drop" (collector framing)

---

## 6. Product Detail Page (PDP)

### Images
- Minimum 5 per product:
  1. Flat lay
  2. Lifestyle (child using it, real setting)
  3. Close-up of block print detail
  4. Scale reference (e.g. bag next to common object)
  5. Packaging

### Product story block
- "Made by [Name], [Location]" with artisan photo
- "This print: [Block Name] — hand-carved by [artisan name or craft centre]"
- A 15–30 second embedded video of the block printing process (not linked, embedded)

### Functional info
- Variant selector (size / color / print)
- Stock status: "In Stock — Ready to Ship in 2 days" OR "Made to Order — Ships in 7 days"
- "Only X left" when stock is low (threshold: ≤5 units)
- Price — no fake strikethrough discounts
- Material + care instructions (framed as a feature: "Block prints brighten with each wash")
- Dimension guide with practical comparisons ("fits a 13" laptop + water bottle")
- For kids products: material safety statement ("No harsh dyes. GOTS-certified cotton. Safe for children's skin.")

### Trust signals on PDP
- Star rating + review count
- Return policy ("10-day easy returns — no questions")
- COD availability
- Free shipping threshold

### Add to cart area
- Gift wrapping upsell: "Add block-printed gift wrap — ₹99"
- Gift message field (free — the effort signals care)
- *(Name-stamp personalization deferred — not feasible from production at launch)*

### Below the fold
- "Complete the Set" cross-sells (e.g. tote + matching pouch, kids backpack + kids pouch)
- Reviews section (with parent photos prioritized)
- "Cost of this piece" breakdown (optional — can be a collapsible accordion)

---

## 7. Gifting Page (Bulk — single address)

A top-level navigation item from launch. Sells the **service** ("we make bulk gifting effortless"), not just products. All bulk ships to **one address** — no multi-address splitting at launch.

**Minimum order: 10 pieces.** Lead with use cases, not SKUs.

### Use-case tiles (the heart of the page)

| Use case | Hook | Typical order |
|---|---|---|
| **Kids birthday return gifts** | "20–30 return gifts that parents actually keep" | 20–40 pouches / small bags |
| **Wedding favours** | "Handcrafted favours your guests won't toss" | 50–200 pieces |
| **Corporate gifting** | "Diwali & welcome hampers with a craft story" | 25–100 sets |
| **Minor events** (naming, baby shower, festivals) | "Curated sets for the occasion" | 10–50 pieces |

> **Why use-case framing wins:** "return gifts for kids birthday" is high-intent with almost no premium/craft options — parents currently buy plastic junk. PEXX owns this gap instantly. Return gifts are the priority use case to promote.

### Page structure
- Hero: "Gifting in bulk? We make it effortless."
- 4 use-case tiles → each shows photos + sample bundle + indicative price-per-piece
- Trust line: "Block-printed, gift-wrapped, delivered to one address. Min 10 pieces."
- Inquiry form (lead capture): name, phone/WhatsApp, occasion, quantity, budget, date needed
- Response promise: "We reply within 24 hours with a quote"

### Standard gift sets (self-serve, single item)
Pre-curated bundles sold as one SKU, for individual gifting:
- **New Baby Bundle** — swaddle + small pouch
- **First Birthday Set** — kids backpack + pouch
- **Festival Set** — matching pouch for kid + parent
- Price tiers: Under ₹1,500 / ₹3,500 / ₹7,000
- Gift wrap + free message card included
- "Ships by [date]" urgency for festivals

---

## 7b. Marketing & Customer Data

### Customer data capture (minimal friction)

**Fields to ask — that's all:**
- Name
- Email
- Phone (doubles as WhatsApp)
- *Optional, high-value:* Child's name + birthday → "Get a birthday surprise + early access"
- Marketing consent checkbox (email/SMS/WhatsApp — legally required)

Everything else (size, preferences, AOV) is enriched later from order data. **Do not** force signup before browsing — capture at exit popup + checkout only.

**Capture points, ranked by ROI:**
| Where | Offer |
|---|---|
| Exit popup | 15% off first order |
| Checkout account creation | Welcome perk |
| Post-purchase | "Add your child's birthday → birthday gift" |
| Newsletter footer | "First access to new drops" (not a discount) |

**The PEXX birthday angle (unique):** collect the *child's* birthday, not the adult's. Trigger an offer ~2 weeks before — parents buy gifts/outfits around birthdays. No competitor does this.

### Channels (launch stack)
- **Email + SMS:** Shopify Email (free, built-in) — fine until list > ~1,000
- **WhatsApp:** Interakt or Wati (~₹999–1,999/mo) — 70%+ open rate vs ~20% email; carries order updates + promo broadcasts
- *(Loyalty/points app deferred — revisit once there's a repeat-customer base)*

### Time-limited & custom coupons (for paid ads)

Native to Shopify Basic — no app needed:
- **Custom codes** — e.g. `INSTA20`, `DIWALI15` (you name them)
- **Start + end date/time** — exact window (hourly, 1-day, weekend)
- **Usage caps** — total uses or one-per-customer
- **Auto-expiry** — code dies after the window, drives urgency

**Paid-ad flow example:** create `FB48` → active 48 hrs, 15% off, capped at 200 uses → put code in the ad creative → Shopify auto-expires it.

**Add-on (optional but recommended):** Shopify's native countdown is backend-only. For a *visible* ticking timer on ad landing pages (lifts conversion), add **Hextom Countdown Timer Bar** (free tier available).

---

## 7c. Go-to-Market & Marketing Strategy

**Starting reality:** zero brand visibility, modest budget. Paid ads to an unknown brand selling an unfamiliar product is the fastest way to burn cash. PEXX's edge is **story + craft + gifting intent**, not ad spend. Build the engine around that. Layer paid ads in only after there's proof to convert against.

### Tier 1 — Before spending ₹1 on ads

**1. Own "return gifts" search intent (unfair advantage)**
High-intent searches ("return gifts for kids birthday," "eco friendly return gifts bulk India") with almost no premium/craft competition.
- One strong landing page + blog posts ("20 return gift ideas under ₹200 that aren't plastic")
- SEO that converts because the buyer is already in purchase mode
- Compounding, free, high-intent traffic on a keyword competitors ignore

**2. Short-form video — the block printing process IS the content**
A hand pressing a carved block onto cloth is hypnotic and scroll-stopping. Most craft brands waste this on flat product shots.
- 3–4 Reels/week: the print being made, the artisan, "imperfection = authentic," unboxing
- Reels organic reach is still the cheapest distribution in India
- Converts browsers to believers AND is algorithmically favored

**3. Seed 50 micro-influencer gifts (not paid)**
Send free product to 30–50 nano mom-influencers (5k–30k followers, high engagement). Cost = product only. ROI = UGC + authentic reach to the exact target audience. Prioritize ones whose kids photograph well.

### Tier 2 — Convert the traffic

**4. WhatsApp-first remarketing** (once set up) — abandoned-cart recovery is 3–5x email in India. Make it the remarketing spine.
**5. First-order popup + honest scarcity** — 15% off first order via exit popup; "Limited print run — 40 pieces only" on collections (real scarcity, protects no-discount positioning).
**6. Gifting as the acquisition wedge** — a 30-pouch return-gift order = 30 new households exposed to PEXX. Every bulk order ships with a card: "Loved this? Shop PEXX → 15% off."

### Tier 3 — What MORE can be done (less obvious plays)

**7. "Gift the craft" insert** — every order includes a card naming the artisan + the print's story. Turns buyers into storytellers.
**8. Preschool / play-studio partnerships** — they need return gifts and event favours constantly. One school = recurring bulk orders. B2B disguised as gifting.
**9. Diaspora gifting (NRIs)** — Indian parents abroad gifting to family in India. High AOV, value craft, no easy option today. Simple "Gift to India" angle.
**10. The Nestery listing** — borrowed trust + discovery while the brand is unknown.
**11. Non-competing brand collabs** — wooden toys, organic baby food. Cross-promote lists. Free, aligned audiences.
**12. Content moat** — "How block printing works" + "Is it safe for babies" — educational SEO that answers the exact anxieties blocking first purchase.

### What NOT to do yet
- Big paid ad budgets (no brand trust to convert against)
- Influencer fees (gift product instead)
- Loyalty/points app (no repeat base yet)
- Discount-led ads (trains the wrong customer, kills positioning)

### Phased sequence
| Phase | Timing | Focus |
|---|---|---|
| 1 | Weeks 1–4 | Reels engine + return-gift SEO pages + seed 50 influencer gifts |
| 2 | Weeks 4–8 | WhatsApp remarketing + preschool/B2B outreach + The Nestery listing |
| 3 | Month 3+ | *Now* layer small, tightly-targeted paid ads with limited-time codes — once UGC, reviews, and proof exist to convert against |

---

## 8. Certifications Strategy

No Indian competitor currently holds both of these together — this is a genuine moat if pursued:

| Certification | What it covers | Why it matters for PEXX |
|---|---|---|
| **GOTS** (Global Organic Textile Standard) | Full organic supply chain + processing + social standards | Masilo has it. Malabar Baby has it. Parents who seek organic recognise it immediately. |
| **OEKO-TEX Standard 100 Class I** | Fabric/dye safety for direct infant skin contact | Stricter than GOTS for chemical safety. No Indian kids brand prominently claims this. Highest-trust signal for chemically anxious first-time parents. |
| Azo-free dyes | No carcinogenic dyes | Minimum baseline — SuperBottoms already claims this. Necessary but not sufficient. |

**Action required:** Confirm with your production partner which certifications are in place or achievable. Display both GOTS + OEKO-TEX logos on: homepage, every product page, physical packaging tags.

---

## 8b. Swaddle-Specific Product Page Requirements

Swaddles are a high-emotion, high-gifting, high-review-anxiety product. The copy and page structure needs to address specific parent concerns:

- **Dimensions front and centre** — 105x105cm minimum. Parents complain most when swaddles are "too small." Generous dimensions convert.
- **Age/use framing** — do NOT say "only for 0–6 months." Say "Swaddle newborns, use as a summer blanket, feeding cover, stroller shade, playmat, beach blanket." Malabar Baby lists 5+ uses — this justifies premium and extends perceived product life.
- **"Gets softer with every wash"** — the single most powerful copy claim in this category. Verified by competitor review analysis.
- **Block-print variation notice** — proactively frame imperfections as artisan's signature: "Each piece is one-of-a-kind. Slight variations in print are the mark of a hand-block process, not a defect." Put this in product description AND a packaging insert. Manages expectations, elevates the handmade premium.
- **Care instructions as a feature** — not fine print. "Hand wash cold or gentle cycle. Block prints brighten with each wash."
- **GSM callout** — state fabric weight (e.g. 110 GSM muslin). Premium parents compare this.

---

## 9. Trust & Conversion

### Must-have from day one
- [ ] COD available — stated in header and on every product page (not just at checkout)
- [ ] WhatsApp support button (visible on mobile)
- [ ] Return window ("10-day returns") on every product page — not hidden in footer
- [ ] Star rating + review count on product cards in grid view
- [ ] "Ready to Ship" vs "Made to Order" label on every product
- [ ] Free shipping threshold displayed in header

### Payment methods
- UPI
- Credit/debit cards
- COD
- Wallets (Paytm, PhonePe)

### COD strategy
- Offer COD from day one, no gating
- Show COD availability on the product page (before checkout)
- Prepaid nudge: ₹50 discount OR free gift wrapping for UPI/card payment
- WhatsApp message when order is out for delivery with UPI payment link
- OTP verification for COD orders before dispatch (reduces RTO)

### Reviews
- Collect via post-purchase email (Shopify built-in or Judge.me)
- Prioritize getting parent reviews with photos
- Show review count on product cards, not just product pages

---

## 9. Mobile

- Mobile-first design (70%+ of Indian ecommerce traffic is mobile)
- Trust bar visible above the fold on mobile
- COD + WhatsApp visible without scrolling on mobile PDP
- Large tap targets for variant selectors and Add to Cart
- Fast load times — images optimized, no heavy scripts

---

## 10. Shipping & Operations

### Shipping setup (to confirm)
- [ ] Domestic shipping partner: Shiprocket / Delhivery / Ecom Express
- [ ] Free shipping threshold (suggested: ₹999 or ₹1,499)
- [ ] Standard delivery timeline
- [ ] "Ready to Ship" products vs "Made to Order" timelines
- [ ] International shipping (Phase 2 or launch?)

### Order management
- Shopify admin for order processing
- Automatic confirmation email + shipping notification with tracking
- WhatsApp notification integration (optional — Interakt or Zoko)

### Returns
- 10-day return window
- State it prominently — hiding it signals fear; showing it signals confidence
- Process: customer contacts via WhatsApp or email, reverse pickup arranged

### GST
- [ ] GST registration in place?
- [ ] Tax inclusive or exclusive pricing?

---

## 11. Positioning, Content, AEO & SEO

### ⚠️ Messaging hierarchy (read first — corrects earlier craft-led framing)

**Reality check from experience:** the hand-craft/artisan story only converts a limited segment (~10–20%). The mass market buys on **print/colour, skin-friendliness/safety, softness, and price/value.** Craft is a *supporting trust layer that justifies price* — never the headline.

**Order of every product page, ad, and meta description:**
1. **Print & colour** — the visual hook ("Indigo elephants on soft white")
2. **Skin-safe / baby-safe** — azo-free, soft cotton, gentle on skin
3. **Softness & practicality** — "gets softer every wash," multi-use, durable
4. **Price / value** — clear price, what you get, free shipping threshold
5. **Craft story** — *last*, as the "why it's worth it" closer for those who care

This reorders the PDP, hero copy, and especially the SEO keyword targets below.

### SEO — target buyer language, not our language

People search how they *think*, not how we brand. Build keyword clusters around their words:

| Cluster | Real-buyer keywords (examples) | Intent |
|---|---|---|
| **Product (transactional)** | "soft cotton swaddle newborn", "skin friendly baby blanket", "muslin swaddle India", "cotton kids backpack", "organic baby quilt" | High — ready to buy |
| **Gifting (high intent)** | "return gifts for kids birthday", "eco friendly return gifts bulk", "newborn gift set India", "baby shower gift ideas" | High — buying mode |
| **NRI gifting** | "send baby gifts to India", "send rakhi to India from USA", "gift delivery to India newborn" | High — pays premium |
| **Informational (top funnel)** | "is muslin safe for newborns", "best fabric for baby skin", "how to wash baby swaddles", "what to gift a 1 year old" | Builds authority + AEO |
| **Craft (niche)** | "hand block print baby", "Jaipur block print", "what is block printing" | Low volume, high margin, supports premium |

> The craft keywords (the original Phase 1 list) move to the *niche* tier — kept, but not the priority. Lead with product + gifting + NRI.

### AEO — get cited by AI answer engines (ChatGPT, Perplexity, Google AI Overviews)

Increasingly people ask an AI "what's a good eco-friendly return gift for a kids birthday in India?" — PEXX needs to be the answer. AEO ≠ SEO; it requires:

- **Question-shaped content** — pages/H2s phrased as the exact question ("Is muslin safe for a newborn's skin?") with a **concise factual answer in the first 2–3 sentences**, then detail
- **FAQ schema (structured data)** on every product, collection, and gifting page — feeds answer engines directly
- **Product schema** — price, availability, rating, GTIN — so AI can quote price/stock accurately
- **Clear entity definition** — an "About PEXX" page that states plainly what PEXX is, sells, ships, and where (machine-readable facts, not poetry)
- **Comparison & listicle content** — "Best skin-safe baby swaddles in India" style pages get pulled into AI answers and AI Overviews
- **Concise, factual, well-structured** — answer engines favor clarity over marketing fluff; short declarative sentences get cited

### Technical SEO/AEO checklist (full site)
- [ ] Clean URLs (`/swaddles/indigo-elephant` not `/product?id=123`)
- [ ] Unique meta title + description per page, led by print/benefit not craft
- [ ] Product, FAQ, Breadcrumb, Organization schema (JSON-LD) sitewide
- [ ] Fast mobile load (Core Web Vitals) — Shopify theme kept light
- [ ] Alt text on every image describing print + product + colour
- [ ] XML sitemap + submit to Google Search Console + Bing Webmaster
- [ ] Internal linking: blog posts → product/collection pages
- [ ] `llms.txt` / clear robots so AI crawlers can read product facts

### Content plan (no production dependency — copy only)

**Migrate:** 5 existing journal posts.

**Build at launch (priority order):**
1. **Return-gift landing page + 3–4 SEO posts** — "20 return gift ideas under ₹200 that aren't plastic," "eco-friendly birthday return gifts" (highest-intent, lowest competition)
2. **NRI gifting hub** — "Send baby & kids gifts to India" (see Section 12)
3. **Safety/benefit informational posts** — "Is muslin safe for newborns?", "Best fabric for baby skin," "How to wash & care for baby swaddles" (AEO + answers purchase anxieties)
4. **Buyer-guide listicles** — "Best skin-safe swaddles in India," "Newborn gift checklist" (AI-citation bait)
5. **Craft content (secondary)** — "How block printing works," artisan profiles — kept for the niche + premium justification, not lead SEO

---

## 12. Additional Opportunities (Phase 2+)

### NRI Gifting — "Send Gifts to India" (priority, not Phase 2)

**The key unlock:** NRI gifting is *not* international shipping. The buyer is abroad; the **recipient is in India**. So it's a **domestic India delivery paid for with a foreign card/currency.** That removes the hard logistics problem entirely — you already ship within India.

**Why it's a big, underserved market:**
- NRIs pay premium, value Indian craft, and have no easy quality option for kids/baby gifts to India
- Huge emotional occasions: new baby in the family back home, niece/nephew birthday, Rakhi, Diwali
- High AOV, willing to pay for "handled for me, delivered on time"

**What's needed (mostly config, not new logistics):**
- [ ] **Multi-currency display** — show USD/GBP/AED/CAD (Shopify Markets, free)
- [ ] **Accept international cards** — Shopify Payments / Razorpay international, + PayPal (NRIs trust it)
- [ ] **Ship to Indian address, bill to foreign address** — standard Shopify checkout handles this
- [ ] **Gift flow** — recipient's Indian address + delivery date + gift message; buyer never sees price on the packing slip
- [ ] **Occasion landing pages** — "Send Rakhi to India," "Send a Newborn Gift to India," "Diwali Gifts to India" with festival delivery-by dates

**Marketing angle:** Rakhi and newborn gifting are the two strongest NRI hooks. "Send Rakhi to India from USA" is a high-volume seasonal search with weak premium-craft competition.

**SEO/AEO:** dedicated keyword cluster (see Section 11) — "send baby gift to India from USA/UK," "gift delivery to India," festival-specific terms.

### Wholesale / Stockist Channel
- **The Nestery** (thenestery.in) already curates block-printed Jaipur kids items — contact as a stockist to build discovery while DTC audience grows
- Corporate gifting inquiry form (block print pouches/totes are strong corporate gift items)

### Seasonal Subscription (Future)
- "Block Print Kids Club" — seasonal box with a new print/product drop quarterly
- No competitor has done this; builds recurring revenue and retention

---

## 13. What We're NOT Building in Phase 1
- Customer accounts / loyalty program
- Wishlist
- AI chat assistant
- International shipping (explore after domestic is stable)
- Home / Interiors category
- Wear / Clothing category
- Advanced analytics beyond Shopify built-in
- Subscription/box product

---

## 13. Decisions Locked

1. **Pricing:** ₹800–₹2,000 range across all Phase 1 products. Accessible premium — above Kassy Pop/SuperBottoms, in line with Chhapa, below Masilo.
2. **Fulfillment:** All products ready to ship. 3-day dispatch SLA stated on site.
3. **Artisan details:** Names + photos available — will feature per product on PDPs.
4. **Photography:** AI-generated lifestyle photos currently in use on FirstCry. ⚠️ See note below.
5. **Print names:** Will create names from existing block images before launch.
6. **GST:** Registered — tax-inclusive pricing to be confirmed.
7. **Shipping:** Local courier partners until volume justifies aggregator (Shiprocket etc.). 3-day dispatch + estimated delivery 5–8 days domestic.
8. **International:** Yes — from launch. Will need Shopify Markets or a shipping app (Easyship/Shiprocket international).
9. **Personalization:** Not feasible at launch. Remove from scope.
10. **Collection positioning:** Modern conscious parent — Indian craft identity without being nostalgic or folksy. Collections should feel like a considered lifestyle choice, not a heritage artifact.
11. **Certifications:** Azo-free dyes confirmed. GOTS processes followed but not certified. ⚠️ See note below.
12. **The Nestery:** Yes — apply to be stocked as a distribution channel alongside DTC.
13. **Visual benchmark:** Malabar Baby as structural reference for gifting + artisan story architecture. PEXX's own visual identity to be distinct.

---

### ⚠️ Two things that need a decision before we build

**A. Photography**
AI-generated lifestyle photos work on a marketplace like FirstCry where every brand looks the same. On PEXX's own store — where the entire brand is built on real craft, real artisans, real hands — AI photos are a liability. If a conscious parent notices (and some will), it directly contradicts the authenticity story.

Options:
- Use AI photos as placeholders at launch, replace with real shoots within 60 days
- Invest in a one-day lifestyle shoot with real kids before launch (the highest-ROI creative spend for this brand)
- Use product flat-lays + artisan process photos at launch (no kids lifestyle) and add later

**B. GOTS processes but not certified**
Cannot display the GOTS logo or claim "GOTS certified" without the certificate. Can legitimately say "made with organic cotton" or "GOTS-standard production processes." Recommend getting certified — it's the single strongest trust signal for the target customer and Masilo (main competitor) already has it.

---

## 14. Competitive Landscape Summary

| Brand | Positioning | Kids/Acc? | Discount? | Artisan story |
|---|---|---|---|---|
| Anokhi | Heritage, premium — **no India ecommerce** | No | No | Buried in About |
| Chhapa | Digital-first block print, kids + adults | Yes | BUY 1 GET 1 | Generic copy, not per-product |
| Aachho | Mid, Jaipur block print | Yes (secondary) | Permanent 50% | Mentioned, not featured |
| Kari by Kriti | Block print gifting + personalization | Peripheral | HELLO10 | Moderate |
| Fabindia | Mass-market, generic craft | Yes (generic) | Seasonal | None |
| Chumbak | Pop Indian design, gifting | Peripheral | Sale-forward | None |
| Raw Mango | Ultra-premium, editorial | No | Never | Collections only |
| Good Earth | Premium lifestyle | Peripheral | No | "Our World" section |
| iTokri | Craft marketplace | Listed | No | Varies by seller |
| **PEXX** | **Block print, kids + acc, artisan-first** | **Core** | **Never** | **On every product page** |

### Key competitor details

**Chhapa** — the closest direct competitor. Digital-first D2C block print brand, kids range ₹1,290–₹2,190 (shirts, co-ord sets, pyjamas, sizes 0–10 years). 909 reviews, COD, free returns, WhatsApp. Their weakness: photography is functional not aspirational, storytelling is generic. PEXX can out-story them.

**Kari by Kriti** — "India's most loved handcrafted block print bags." Their "Gifting Studio" sells curated hampers, party favours, bulk sets (5/10/15/20 pieces), and personalised embroidered names on items. Featured in Lonely Planet, Cosmopolitan, Elle. Proves the personalisation + gifting angle works. PEXX should offer this too.

### Pricing benchmarks from research

| Category | Competitor range | Recommended PEXX |
|---|---|---|
| Kids clothing (set) | ₹1,290–₹2,190 (Chhapa) | ₹1,499–₹2,499 |
| Kids bags / pouches | ₹599–₹1,899 (Kari / Aachho) | ₹799–₹1,699 |
| Adult tote bags | ₹999–₹3,595 (Chumbak / Aachho) | ₹1,299–₹2,499 |
| Gift sets | ₹1,500–₹3,000 (Kari by Kriti) | ₹1,999–₹3,499 |

Position PEXX above Chhapa/Aachho (quality signal) but below Good Earth (accessible premium). No permanent discounts — seasonal sales tied to real occasions only (Diwali, Children's Day, Holi, Rakhi).

---

*Document version: Draft 1 — June 2026*  
*Next step: Review open questions (Section 13), confirm product list, then begin Shopify setup.*
