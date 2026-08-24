# PEXX — Rakhi Meta Campaign

**Rakhi:** Friday 28 August 2026
**Goal:** Purchases
**Ad window:** 12 – 18 August (7 days)
**Last order date:** 18 August — owner is committing to expedited dispatch
**Budget:** ₹6,000 ≈ **₹850/day**
**Status:** ⚠️ **STALE as of 15 Aug 2026 — this campaign is LIVE and has spent.**
Built and launched 12 Aug; rebuilt 15 Aug after a creative failure. The build
spec below is still the reference for *what was intended*. For what is actually
running, and why it broke, see **`META-ADS-RUNBOOK.md`**.

**Ad images:** cropped to Meta 4:5 (1080×1350) at
`~/Desktop/PEXX/ecom/_ads-4x5/` — Backpack, Utility_Pouch, Quilt, Swaddle.
All four from the `Gifts_Kids` set, so the campaign reads as one family.

---

## RESOLVED — the free gift is built and working

Owner confirmed loose single pouches are in stock. Built and **verified in a live
cart** on 11 Aug:

- Product: **"Gift Pouch — Free over ₹1,999"**, ₹399, published, oversell allowed.
- Automatic discount: **"Free Gift Pouch over ₹1,999"**, runs to 30 Sep 2026,
  qualifying spend counted across backpacks / toiletry-pouches / quilts / swaddles.
- Test: quilt ₹1,299 + backpack ₹999 = ₹2,298 → pouch drops **₹399 → ₹0**. ✅

**Two caveats:**
- The customer must **add the pouch to their cart themselves** — Shopify's native
  buy-X-get-Y does not auto-insert it. It needs to be visible on the product page
  and in the cart or nobody will claim it.
- The gift product has **no image** (owner's decision to skip) — it shows a grey
  placeholder in the cart.
- The below-threshold negative case is configured correctly (the gift isn't in any
  qualifying collection, so it can't count toward its own threshold) but was
  **not observed** — the storefront rate-limits repeated cart tests. Worth one
  manual check: backpack alone + pouch should charge ₹399.

---

## The timing problem — read this first

Your own product page promises: *"Ships in 3 days from Jaipur · delivered across
India in 5–8 days."* That's **8–11 days door to door.**

Working backwards from 28 August:

| Order date | Ships (standard, 3 days) | Arrives | Before Rakhi? |
|---|---|---|---|
| 18 Aug | 21 Aug | 26–29 Aug | **Some miss it** |
| **18 Aug** | **19 Aug (expedited)** | **24–27 Aug** | **Yes** |

**Owner has committed to expedited dispatch for Rakhi orders**, which is what
makes the 18 August last-order date work. That commitment is load-bearing: at
standard 3-day dispatch, orders placed on the 18th arrive as late as the 29th.

**Two operational consequences of that commitment:**
- Orders placed 16–18 August must go out **next day, not in three**. That's roughly the peak-volume window, so it's the hardest time to do it.
- If dispatch slips even a day, the ads are still promising "before Rakhi" while the parcels stop making it. If you know by the 17th that you can't keep up, **pull the deadline line out of the ad copy** rather than letting it keep selling a promise you can't keep.

A Rakhi gift arriving on the 30th is a refund request and a ruined first
impression from a customer you paid to acquire.

---

## Campaign setup

| Setting | Value |
|---|---|
| Objective | **Sales** |
| Conversion event | **Purchase** |
| Conversion location | Website |
| Structure | 1 campaign · 1 ad set · 4 ads |
| Budget | ₹850/day, set at campaign level (Advantage campaign budget ON) |
| Schedule | 12 Aug 00:00 → 18 Aug 23:59 |
| Attribution | 7-day click, 1-day view (default — leave it) |

**On optimising for Purchase:** it's the right call now that purchases are the
goal, but know the trade. Meta wants ~50 purchases a week to optimise well; this
will produce a handful. Delivery will be lumpy and cost per purchase will swing
day to day. That's the price of pointing it at the thing you actually want, and
it's the right price to pay — optimising for cheaper events would fill your
retargeting pool with people who were never going to buy.

---

## Targeting — the exact settings

| Field | Set to |
|---|---|
| **Locations** | Mumbai, Delhi, Gurgaon, Noida, Bengaluru, Hyderabad, Pune, Chennai, Kolkata, Ahmedabad |
| Location type | **People living in this location** (not "recently in") |
| **Age** | 25 – 45 |
| **Gender** | All |
| **Detailed targeting** | **Leave empty** |
| Advantage+ audience | **On** |
| Languages | Leave empty |
| **Placements** | Advantage+ placements (automatic) |

### Why empty targeting, when Meta offers thousands of options

This is the part that feels wrong and isn't. Meta's targeting menu is a museum
piece — it was essential in 2018 and it actively hurts now. The algorithm reads
your image and copy, works out who responds, and finds more of them. Interest
filters just shrink the pool it can search.

Two concrete reasons for PEXX specifically:

- **Your budget is small.** ₹1,200/day across 4 ads is about ₹300 per ad. Narrow the audience and Meta shows the same ad to the same small group repeatedly — people get bored, costs rise, and you've learned nothing.
- **Interest data is stale.** "Interested in: Parenting" includes everyone who liked a parenting page in 2019. Your creative saying *"for the newest one in the family"* is a sharper filter than any checkbox.

**Location and age are the exceptions worth keeping.** Metros because delivery is
faster and cash-on-delivery refusals are lower. 25–45 because that's who buys a
gift for a child in the family.

If you want to test narrowing later, the one worth trying is **Behaviours →
Engaged Shoppers** (people who clicked a shop button in the last week). Not now —
at this budget it will strangle delivery. Note it for Diwali.

---

## The four ads — SUPERSEDED, see "v2" at the end of this file

> Owner review 11 Aug: this first set was too transactional and swappable — any
> block-print brand could have run it. "Hand block-printed in Jaipur" sat at the
> bottom as a spec line. Rewritten as v2 at the end of this document. **Use v2.**

## The four ads (v1 — kept for reference only)

One per product. Warm, specific, no invented claims — you have no reviews or
ratings, so nothing in here implies you do.

Format: static, 4:5 vertical, from `~/Desktop/PEXX/ecom`.

---

### Ad 1 — Backpack · ₹999
**Image:** `Gifts_Kids/Gift_Kids_Backpack.png`
**Sends to:** `/collections/backpacks`

> There's a niece or nephew you only see properly at Rakhi. And every year they're taller than you remembered.
>
> A backpack they carry to school all year is a better way to be remembered than something that's finished by evening.
>
> Hand block-printed in Jaipur, one motif at a time. Six prints. ₹999.
> Order by 18 August to reach them before Rakhi.

**Headline:** Something They'll Carry All Year *(32)*
**Description:** Backpacks ₹999 *(14)*

---

### Ad 2 — Toiletry pouch set · ₹1,199
**Image:** `Toilet Kits/` — the three pouches together
**Sends to:** `/collections/toiletry-pouches`

> Rakhi gifts for children have a short life. Sweets go in a day. Toys by October.
>
> A set of three block-printed pouches goes into every school bag, every holiday, every sleepover — small things kept safe, for years.
>
> Three pieces, hand block-printed in Jaipur. ₹1,199.
> Order by 18 August to reach them before Rakhi.

**Headline:** Three Pouches, One Gift *(23)*
**Description:** 3-piece set ₹1,199 *(18)*

---

### Ad 3 — Quilt · ₹1,299
**Image:** `Quilts 150X100/` — styled, not flat
**Sends to:** `/collections/quilts`

> The newest one in the family won't remember their first Rakhi. Everyone else will.
>
> A reversible cotton quilt, hand block-printed in Jaipur — slept under, dragged around, washed a hundred times, and somehow kept.
>
> Azo-free, skin-safe dyes. ₹1,299.
> Order by 18 August to reach them before Rakhi.

**Headline:** For the Newest One in the Family *(32)*
**Description:** Quilts ₹1,299 *(13)*

---

### Ad 4 — Swaddle set · ₹999
**Image:** `Swaddles/`
**Sends to:** `/collections/swaddles`

> For the sister who became a mother this year.
>
> Two cotton muslin swaddles, hand block-printed in Jaipur — used as a wrap, a pram cover, a nursing shade, a floor sheet, and eventually a blanket that gets dragged everywhere.
>
> ₹999 for two. Azo-free, skin-safe dyes.
> Order by 18 August to reach them before Rakhi.

**Headline:** Two Swaddles, Five Uses *(23)*
**Description:** Set of 2 · ₹999 *(15)*

---

## What you're missing — the list

Things that decide whether the ads turn into purchases. Ordered by how much they
matter.

### 1. Delivery timing (above) — biggest one
Either speed up dispatch or move the last order date to 16 August.

### 2. Your shipping policy page is a 404
`/policies/shipping-policy` returns nothing, and it's linked from product pages.
For a first-time buyer sending a gift, "when will it arrive" is *the* question,
and the page answering it is broken. Meta also occasionally rejects ads from
stores with missing policy pages.

### 3. The free gift has to be visible in the cart
An automatic discount that only reveals itself at checkout doesn't change
behaviour. The cart needs to say *"You're ₹800 away from a free block-printed
pouch."* Otherwise the ₹1,999 threshold does nothing.

### 4. Ad account admin — do this before 12 August
- Payment method added and verified
- Business verification started (new accounts get held up)
- **Ads take up to 24 hours to review.** Submit on the 11th to run on the 12th.
- New ad accounts often start with a low daily spend cap — check yours is above ₹1,200

### 5. Retargeting from day 3
People who viewed a product and didn't buy are your cheapest purchases by a wide
margin. From 14 August, run one small ad (₹200/day) to website visitors from the
last 7 days. It'll likely beat all four cold ads on cost per purchase.

### 6. Abandoned cart follow-up
You have a WhatsApp worker built already. Cart abandonment in India runs around
70%, and a WhatsApp nudge recovers a meaningful slice. Worth checking whether
that pipeline is actually wired before you send paid traffic through it.

### 7. Four prints are out of stock
Green Stripe backpack, Terracotta Stripe and Green Stripe pouch sets, Pony Trail
quilt. Make sure no ad image shows them — including the child-in-park backpack
photo, which is the out-of-stock Green Stripe.

### 8. No reviews anywhere on the site
Every long-running competitor ad leans on a proof number. You have none, so the
ads don't claim any. But a first-time buyer spending ₹1,299 with an unknown brand
has nothing to reassure them. Even three real reviews would help. Judge.me is
already installed.

---

## Run schedule

| Date | Action |
|---|---|
| **11 Aug** | Set up free-gift discount. Crop images to 4:5. Submit ads for review. Fix shipping policy page. |
| **12 Aug** | Ads live. All four at once. |
| 13–14 Aug | **Look, don't touch.** Early numbers are noise. |
| **14 Aug** | Add the retargeting ad (₹200/day). |
| **15 Aug** | First real read. Kill only an ad with zero add-to-carts after ~₹900 spent. |
| **16 Aug, 23:59** | Cold ads off. |
| 17–27 Aug | Retargeting only, small budget. |
| 19 Aug | Everything dispatched. |

Never edit a running ad's creative — it resets Meta's learning. Launch a new one
alongside instead.

---

## What to watch

| Metric | Good | Stop and look |
|---|---|---|
| CTR | above 1.5% | below 0.8% |
| CPC | ₹5–15 | above ₹25 |
| Cost per add-to-cart | under ₹150 | above ₹300 |
| Cost per purchase | under ₹700 | above ₹1,000 |
| RTO on COD orders | under 10% | above 20% |

Judge cost per purchase across the whole 5 days, not day by day. At this budget a
single day is luck.

---

## Diwali (8 November) — what to fix in September

- **Shoot video.** The category runs on it; you have none. Biggest gap.
- **Get reviews live.**
- **Put the artisan's name on product pages.** It's your stated differentiator, no competitor does it, and the ads can't use it until it's there.
- **Fix dispatch speed.** 3 days to ship is the constraint behind every deadline in this document.
- Costs roughly triple in festive season — learn in September.

---

# The four ads — v2 (FINAL, use these)

Rewritten 11 Aug after owner review. The brief: less transactional, warmer,
premium, and impossible for a competitor to run unchanged.

**The two differentiators v1 wasted:**

1. **Real hand block-printing produces variation, and variation is proof.**
   Mass-market "block print" kids goods are screen or digitally printed to
   imitate the look — perfect and identical. PEXX's cannot be. Lead with that;
   it's the evidence a person made it.
2. **PEXX does not discount.** Same price in January and October. Half this
   category leads with "50% OFF" — an explicit no-sale stance is a brand claim
   competitors can't copy.

Every factual claim below is already live on the product pages (hand
block-printed in Jaipur one motif at a time; variation is the mark of handwork;
azo-free skin-safe dyes; cotton voile and hand-quilted cotton fill; 3-piece
pouch sets; 2-pack swaddles). No reviews, ratings or certifications are implied.

---

### Ad 1 — Backpack · ₹999 → `/collections/backpacks`
**Image:** `_ads-4x5/Gift_Kids_Backpack.jpg`

> Somewhere in Jaipur, someone pressed a carved wooden block into cotton, by hand, a few hundred times over. That became this bag.
>
> Look closely and you'll find a bunny slightly out of line, a flower a shade deeper than the one beside it. That isn't a flaw we missed. That's how you know a person made it and a machine didn't.
>
> Most children's bags are printed by the thousand in an afternoon. This one took a week and a pair of hands.
>
> Cotton, quilted soft. Azo-free dyes, because a bag rides against small shoulders all day long. ₹999 — the same ₹999 it was in January. We don't run sales and then call it generosity.
>
> A Rakhi gift they'll still be carrying to school long after the thread has come off.

**Headline:** Printed By Hand, Not By The Thousand *(35)*
**Description:** Backpacks ₹999 *(14)*

---

### Ad 2 — Toiletry pouch set · ₹1,199 → `/collections/toiletry-pouches`
**Image:** `_ads-4x5/Gifts_Kids_Utility_Pouch.jpg`

> Three pouches, one print, and not one of them identical to the next.
>
> They're block-printed by hand in Jaipur — a carved block pressed and lifted, pressed and lifted, until the cotton is covered. Which is why the bear on the small pouch sits a little differently to the bear on the large one.
>
> The big one holds a toothbrush and a comb. The middle one, the things a mother wants within reach. The smallest gets claimed by the child within about a day — for hair clips, coins, and one very important stone.
>
> Quilted cotton, azo-free dyes, wipe-clean inside. ₹1,199 for all three.
>
> The kind of Rakhi gift that's still in use next summer.

**Headline:** Three Pouches, No Two Alike *(27)*
**Description:** Set of 3 · ₹1,199 *(17)*

---

### Ad 3 — Quilt · ₹1,299 → `/collections/quilts`
**Image:** `_ads-4x5/Gift_Kids_Quilt.jpg`

> The newest one in the family won't remember their first Rakhi. Which is exactly why you give them something that lasts long enough for them to ask about it later.
>
> This quilt was block-printed by hand in Jaipur — one wooden block, one motif, one press at a time, across the whole length of the cotton. Then hand-quilted with a cotton fill. No polyester anywhere in it.
>
> Turn it over and there's a second print underneath, so it changes its mind with the room.
>
> It will be slept under, dragged to the sofa, taken on trains, and washed a hundred times. It will still be in the house when the child is far too big for it.
>
> Azo-free, skin-safe dyes on natural cotton. ₹1,299.

**Headline:** Made To Be Kept, Not Replaced *(29)*
**Description:** Reversible · ₹1,299 *(19)*

---

### Ad 4 — Swaddle set · ₹999 → `/collections/swaddles`
**Image:** `_ads-4x5/Gift_Kids_Swaddle.jpg`

> For the sister who became a mother this year.
>
> Two lengths of cotton muslin, block-printed by hand in Jaipur, in azo-free dyes — because this is the cloth that sits against a week-old face, and that is not the place for chemistry you can't pronounce.
>
> She'll use them as a wrap. Then a pram shade. Then a nursing cover, a floor blanket for tummy time, something light over the cot on an AC night. Muslin gets softer every single wash, which is the opposite of how most things go.
>
> Two to a set, each with its own striped edge. ₹999.
>
> Not the biggest gift you could send her. Probably the one she'll use most.

**Headline:** Soft Enough For Week-Old Skin *(29)*
**Description:** Two swaddles · ₹999 *(19)*

---

## The line we still cannot write

The most uncopyable asset PEXX has is **the name of the person who printed it**.
`.agents/product-marketing.md` says the artisan should be named and shown at
product level. Verified 11 Aug: **it is not on the live product pages.**

Once it is, these ads can open with "printed by [name], who has been carving
blocks for nineteen years" — and no competitor in the category can follow.
Until then the claim isn't verifiable on the landing page, so it stays out.

**This is the highest-value pre-Diwali task on the whole list.**

---

# BUILD STATUS — 11 Aug 2026

## The ad account was the problem, and it's fixed

Ads were first built in the **personal** ad account (327847014459823), which
cannot see the PEXX pixel. Correct home is the **PEXX business ad account
1350379969884972**, inside business portfolio **PEXX (1752269172473486)** —
same portfolio that owns the pixel. Everything below is built there.

## Housekeeping completed

| Action | Status |
|---|---|
| Discarded 2 stale "Traffic campaign for Instagram advertisers 23/07/2026" drafts | Done |
| Turned OFF live "New Traffic Campaign with recommended settings" (1,922 link clicks @ ₹0.21, ~₹400 spent, was erroring) | Done |
| Turned OFF Advantage+ catalogue ads on our campaign | Done |
| Investigated the `vtg3wc-2k.myshopify.com` catalogue | **Resolved — it IS PEXX** |

**Correction:** I flagged `vtg3wc-2k.myshopify.com` as "a different Shopify
store". It isn't. Commerce Manager shows that catalogue holds **exactly the 26
PEXX products**, correct prices, last synced 11 Aug 13:44. It's the store's
internal Shopify domain. No action needed, and the catalogue is healthy enough
to power retargeting ads after Rakhi.

## Campaign as built (draft, nothing published, nothing spent)

- **PEXX_Sales_Rakhi_Metros_Aug2026** — Sales objective
- Campaign budget **₹850/day**, highest-volume bidding
- Conversion location Website, conversion event **Purchase**
- Advantage+ catalogue ads OFF

## Pixel health (Events Manager, 14 Jul – 10 Aug)

| Event | Status | Match quality |
|---|---|---|
| Page view | Active | 4.4/10 |
| View content | Active | 4.4/10 |
| Initiate checkout | Active | 4.4/10 |
| Add to cart | **No recent activity** | 4.4/10 |
| Purchase | Active | **0.0/10** |

Browser + Server (Conversions API) on all events. Match quality 4.4/10 is
mediocre (6+ is healthy). **Purchase at 0.0/10** most likely reflects too few
purchase events to score rather than broken parameters — the store has had
roughly one real order.

## Still to build

1. Ad set: locations, age, placements, schedule 12–18 Aug
2. Four ads: images from `~/Desktop/PEXX/ecom/_ads-rakhi/`, v2 copy, per-collection links
3. Clear the abandoned draft left in the personal ad account
4. Stop before Publish for owner confirmation
