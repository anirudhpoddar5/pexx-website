# PEXX — Meta Ads Plan (India)

**Written:** 11 August 2026
**Budget assumed:** ₹10–15k/month (~₹400/day)
**Status:** ⚠️ **STALE as of 15 Aug 2026 — this doc's status lines are no longer true.**
Ads went live 12 Aug and have spent real money. The reasoning below is still
sound; the "nothing launched" framing is not. For current account state and
procedures see **`META-ADS-RUNBOOK.md`** — that file is the source of truth.

Everything in Part 1 and Part 2 was checked directly — the Shopify admin, the
live storefront, and Meta's public Ad Library — not assumed. Where something is
an estimate, it says so.

---

## Part 1 — Where PEXX actually stands

Checked in Shopify admin, 1 July – 10 August 2026 (6 weeks):

| Measure | Reality |
|---|---|
| Orders | 7 total — and most are internal tests (`codtest`, `judgemetest`, staff names) |
| Real customer orders | Essentially **one** (#1014, ₹1,203, Mumbai) |
| Gross sales | ₹5,335, of which ₹2,287 was reversed/voided → **₹3,301 total sales** |
| Sessions | ~800 in 6 weeks (~20/day): 398 Mumbai, 110 Jaipur, 54 unknown, 45 Pune |
| Traffic source | Almost entirely **direct** (₹1.3K attributed) + **224 Instagram** sessions. Facebook: 5 sessions. Google: 0 revenue. |
| Products live | 26 SKUs, 22 of 26 variants in stock |
| Price range | **₹99 – ₹1,299** |
| Best sell-through | Pastel Bear Kids Backpack (62.5%), Blush Unicorns Quilt (20%) |
| Meta Pixel | **Live and correct** — ID `1952609352110587`, installed ~27 July via the Facebook & Instagram app, data sharing "Optimized" (includes server-side Conversions API) |

**What this means in plain terms.** The store works, the pixel works, but
commercially the shop is brand new — one real sale and about twenty visitors a
day, most of whom already knew about PEXX.

**One consequence that shapes the whole plan:** there is no retargeting pool.
Retargeting is normally the cheapest way to start, but Meta needs roughly 1,000
people in an audience before it will deliver, and 6 weeks of traffic has produced
maybe 500–700 unique visitors — many of them the team. So the first spend has to
go to cold prospecting, which is the expensive kind. Retargeting becomes
available around week 4–6 of running ads, and that's when the economics improve.

---

## Part 2 — What the Indian market actually shows

Source: Meta Ad Library, filtered to India, active ads only, checked 11 Aug 2026.
The Ad Library shows *which ads are running and for how long* — it does **not**
show targeting, budget, or results. Nobody can reverse-engineer a competitor's
targeting from it. What a long run time does tell you is that the advertiser
keeps paying for that ad, which is the best public proxy for "this one works."

### The direct comparison: Raamaé

The closest brand to PEXX in the entire category — block-printed quilts, baby and
kids, Indian market, gifting framing.

| Their ad | Running since | Length |
|---|---|---|
| "Block Printed Artisan Quilts — handcrafted… 100% ultra-soft cotton muslin, reversible" | **23 Jul 2025** | 12+ months |
| "Personalised Baby Quilts… Ideal for baby showers, birthdays, and newborn gifting" (8 ads share this creative) | **18 Apr 2025** | 16+ months |
| "Mustard Rai Pillows — Tradition Meets Modern Care" | 19 Mar 2025 | 17+ months |

An ad running 12–16 months is as strong a signal as this category offers. It says
block print + baby + gifting **sells profitably on Meta in India**. That is
genuine validation of PEXX's whole premise.

**Their pricing** (from raamae.com): baby quilts from **₹2,620**, adult quilts
from ₹4,599, muslin swaddles ₹1,199, cushion covers ₹649–839. Free shipping over
₹999 — same threshold as PEXX.

### The rest of the category

| Brand | What they run | Price point | Pattern |
|---|---|---|---|
| MomshomeOrganic | "17 Items Hospital Bag", "23 Items", "30 Items" | **₹5,249 – ₹7,999** | Item count in the headline, "50% OFF" framing |
| Kiddo Hut | "44 Essentials in One Box", customisable | Not shown | CTA goes to **WhatsApp**, not a store |
| Zoey | "Hospital Bag Must Have Combo" — 12 items listed, GOTS muslin | Not shown | Baby-shower gifting framing |
| BownBee | Infant collection | ₹1,208 shown in ad | "**Trusted by 10 Lakh+ Indian moms**" as the hook |
| Nintara Baby | Organic swaddle | — | "**Free gift on orders worth ₹2,499**" |
| SuperBottoms | SuperSoft underwear (running since 31 Mar 2026) | — | Emoji benefit-stack: 3x softer, bamboo, antibacterial, AZO-free |

### The four things the winners have in common

1. **They sell a box, not an item.** Almost every long-running gifting ad is a
   multi-item set at ₹2,500–8,000. Single-product ads in this category are rare
   and short-lived.
2. **The occasion is in the ad, not implied.** "Hospital bag", "baby shower",
   "newborn gifting" — named explicitly. PEXX's positioning already believes
   this; the market confirms it.
3. **A specific number does the persuading.** "44 essentials", "10 Lakh+ moms",
   "3x softer", "98% bamboo". Vague craft language is absent from every
   long-running ad.
4. **Video is the dominant format**, contrary to the usual global advice that
   statics win. Nearly every ad found was 14–50 seconds of video.

### Market benchmarks (India D2C, 2026)

CPM ₹100–200 for new brands · CPC ₹5–15 · CTR 1.5–2.5% · **customer acquisition
cost ₹400–800** · realistic month-1 ROAS 1.5–2.5x. Two warnings from the same
sources: Meta CPMs in India are up **40–70%** year on year, and **sale-season
costs roughly triple**.

---

## Part 3 — The economics, honestly

At ₹400/day with the current catalogue:

| | Current catalogue (AOV ~₹1,200) | If AOV reaches ₹2,000 |
|---|---|---|
| Monthly spend | ₹12,000 | ₹12,000 |
| Impressions (at ₹150 CPM) | ~80,000 | ~80,000 |
| Clicks (at 1.5% CTR) | ~1,200 | ~1,200 |
| Orders (at 1.5% conversion) | ~18 | ~18 |
| Revenue | ~₹21,600 | ~₹36,000 |
| ROAS | 1.8x | 3.0x |
| Gross profit (at ~57% margin) | ~₹12,300 | ~₹20,500 |
| **Left after ad spend** | **~₹300 — break-even** | **~₹8,500/month** |

Then subtract shipping and payment fees, and subtract RTO — in India, cash-on-
delivery parcels get refused on arrival often enough that an account can show
4x ROAS while a fifth of the parcels quietly come back.

**The conclusion, stated plainly:** at a ₹1,299 ceiling, ads at this budget are a
break-even customer-acquisition exercise, not a profit engine. That is not fatal
— buying your first 20 customers at cost is a legitimate thing to do, and the
data they generate is what makes month 3 profitable. But it should be a decision,
not a surprise.

You've said no new bundle products, and this plan respects that. There is a
version of raising order value that creates **no new SKUs, no new photography,
and no discounting** — see 4.1.

---

## Part 4 — The plan

### 4.1 Before launch (no new products required)

1. **Free-gift threshold.** "Free block-printed pouch on orders over ₹1,999."
   This is a Shopify automatic discount plus an existing SKU — no new product, no
   photoshoot. Nintara runs exactly this mechanic at ₹2,499. It raises order
   value without discounting, which keeps PEXX's no-sale principle intact.
2. **A "Gifting" collection page** that merchandises quilt + swaddle + pouch
   together on one page. Again: a collection, not a product. This is what the ads
   point at.
3. **Fix the homepage title tag** — it is currently the single word "PEXX", with
   no description. Free, five minutes, helps everything.
4. **Decide the COD position.** Recommend prepaid-only for ad traffic in month 1,
   or COD restricted to metro pincodes. RTO on cold ad traffic is the most common
   way an Indian D2C brand loses money invisibly.
5. **Get 5 reviews live on Judge.me** (already installed). Every long-running
   competitor ad leans on a proof number; PEXX currently has none.

### 4.2 Campaign structure — deliberately minimal

At ₹400/day the biggest risk is fragmenting the budget. Meta wants ~50 purchases
a week to optimise properly; this budget will produce ~4. Spreading that across
multiple campaigns guarantees nothing learns anything.

**Run one campaign. One ad set. Five or six ads.**

- **Objective:** Sales, optimising for Purchase
- **Campaign type:** Advantage+ Shopping — the catalogue is already synced through the Facebook & Instagram app
- **Geography:** Top metros only (Mumbai, Delhi NCR, Bengaluru, Hyderabad, Pune, Chennai, Kolkata, Ahmedabad). Broad-India is the standard 2026 advice, but at ₹400/day a national audience spreads delivery too thin, and metro pincodes also have materially lower RTO.
- **Audience:** No interest stacking. Age 25–45. Let the creative do the targeting — this is what Meta's current algorithm rewards.
- **Placements:** Automatic. Expect Instagram-heavy — 224 of PEXX's ~800 sessions already come from Instagram versus 5 from Facebook.
- **Expect a slow start.** Two to three weeks before delivery stabilises, because the pixel has almost no purchase history to learn from.

### 4.3 The six ads to launch

Each one is modelled on a pattern that is demonstrably running long in this
market, applied to what PEXX actually has.

| # | Angle | Modelled on | Hook direction |
|---|---|---|---|
| 1 | Occasion-named gifting | Raamaé, Zoey | "The baby shower gift that isn't another rattle" |
| 2 | The print as hero | Raamaé's 12-month block-print ad | The block itself, printing, the finished quilt |
| 3 | Artisan named and shown | **Nobody in the category does this** | Hands, the block, the person's name |
| 4 | What's actually in it | MomshomeOrganic, Kiddo Hut | "What ₹1,299 gets you" laid out flat — quilt, wrap, story card |
| 5 | Skin-safe / fabric spec | SuperBottoms | AZO-free, cotton, washable, no chemicals — specific numbers, not adjectives |
| 6 | NRI send-to-India | **White space — no competitor found running it** | "Sending a gift home for the baby" |

Notes: use **video** — the category runs on it. Vertical, captions burned in,
first 3 seconds decide everything. Angle 3 is PEXX's real differentiator and no
competitor is using it, which makes it the most interesting test and also the
riskiest. Angle 6 targets a completely unserved position.

### 4.4 Calendar

- **Rakhi is 28 August — 17 days away.** With a ~5-day shipping cutoff, the real
  deadline is around 23 August. That is too tight to build a proper program, but
  a small dedicated Rakhi push using the existing Rakhi collection is worth doing
  as a live-fire test.
- **Diwali is 8 November.** This is the real target. Work backwards: creative
  ready by early October, spend ramping from mid-October.
- **Warning:** Q4 costs roughly triple. Money spent learning in
  September is worth far more than the same money spent learning in November.

### 4.5 When to stop, when to continue

Judge at day 14, not before — earlier than that is noise.

- **Cost per purchase under ₹700** → working. Continue, start building retargeting.
- **₹700–1,000** → borderline. Fix the landing page and order value before adding budget.
- **Over ₹1,000, or zero purchases after ₹6,000 spent** → stop. The problem is the offer or the price point, not the ads, and more spend won't find it.
- **Watch RTO separately from ROAS.** They can point in opposite directions.

---

## Open decisions for the owner

1. **Free-gift threshold at ₹1,999** — yes or no? (Biggest single lever, lowest effort.)
2. **COD on ad traffic** — prepaid only, metro-only, or unrestricted?
3. **Rakhi:** small push before 23 August, or skip and aim everything at Diwali?
4. **Accepting break-even month 1** as the price of data — confirmed?

---

## Sources

Ad evidence: [Meta Ad Library](https://www.facebook.com/ads/library/) (India, active ads, 11 Aug 2026).
Competitor pricing: [raamae.com](https://raamae.com/).
Benchmarks: [productgrowth.in](https://productgrowth.in/tools/marketing/meta-ads/) · [aimnlaunch.com](https://aimnlaunch.com/how-to-launch-a-d2c-brand-in-india-in-2026-the-complete-playbook-from-zero-to-rs-10l-month/) · [imarkinfotech.com](https://www.imarkinfotech.com/indian-d2c-brands-are-getting-destroyed-on-meta-ads-in-2026-10-reasons-why-and-how-to-fix-it/) · [theshizz.in](https://theshizz.in/blog/meta-ads-for-d2c-brands-india) · [wittelsbach.ai](https://www.wittelsbach.ai/post/cod-policy-meta-ad-copy-what-indian-d2c-brands-can-promise).
Festival dates: [drikpanchang.com](https://www.drikpanchang.com/calendars/indian/indiancalendar.html?year=2026).
Store data: Shopify admin, 1 Jul – 10 Aug 2026.
