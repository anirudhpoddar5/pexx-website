# Copy Sync — Rakhi Meta Ads vs Live Site

**DRAFT ONLY.** Nothing here has been published. Nothing on the live store or any API was modified.

Audited 2026-08-11 against `products.json`, `collections.json`, and the rendered live pages for all four collections.
Tone target: the Rakhi ad voice (someone is buying this *for* a child they love, not for themselves).
Rules applied from `.agents/product-marketing.md`: no "handmade with love", no age-restrictive swaddle framing, no discount language, promise spine = print/colour → skin-safe → made-to-keep → honest price → craft last.

---

## 1. Audit table

| Category | What the current copy does well | Where it clashes with the ad tone |
|---|---|---|
| **Backpacks** (₹999) | Opening line is already the right register — "the one accessory a kid actually wants to grab on the way out the door." Concrete carry list (snack box, bottle, toy). Dimensions and 2–6 age fit are stated, and the craft line sits last, correctly. | Reads as a spec sheet for a buyer, not a gift for a nephew. Nothing about who it's for or the occasion. Skin-safe is buried in the final craft paragraph instead of second in the spine. |
| **Toiletry Pouch Sets** (₹1,199) | Best "made-to-keep" writing on the site — the reuse list (packing cube → crayon sorter) does real work extending perceived life. Skin-safe and 3-piece both present. | **Says "a genuine four-in-one set" on a product titled 3-Piece / "A set of 3"** — a contradiction on the same page. Also the most functional, least warm of the four; nothing in it would survive next to "For the sister who became a mother this year." |
| **Quilts** (₹1,299) | Strongest imagery ("a quiet pond scene for story time"). The grow-with-them list (quilt → play mat → AC blanket) is exactly the made-to-keep beat the ads use. | The ad's whole hook is **reversible** and **survived** — neither lands here. "Reversible" appears only in the title and the last clause. Azo-free/skin-safe is **absent from the description entirely** (accordion only). No sense of years passing. |
| **Swaddle Sets** (₹999) | Print description is vivid and the "beyond swaddling" line correctly refuses newborn-only framing. | Only **3** alternate uses; the brand rule asks for 5+. Skin-safe **missing from the description** (accordion only). Nothing for the "won't remember their first Rakhi" angle — the emotional centre of the swaddle ad has no echo on the page. |

---

## 2. Revised collection descriptions

All four collections currently render **no description at all** (`body_html: null` — verified on `collections.json` and the live pages). Ad traffic lands on a bare product grid.

### Backpacks (`/collections/backpacks`) — 82 words
Stripes, bunnies, submarines, penguins — prints a child spots across a room and then refuses to swap. Cotton dyed with azo-free, skin-safe colours, because a bag rides against small shoulders all day long. Hand-quilted with a soft cotton fill and sized H30 x W25 x D10cm: a snack box, a water bottle, one favourite toy, room to spare. Ages roughly 2–6, and comfortable on bigger kids too. ₹999, the same price all year. Hand block-printed in Jaipur, one motif pressed at a time.

### Toiletry Pouch Sets (`/collections/toiletry-pouches`) — 88 words
Bunnies, frogs, submarines, penguins — three nested pouches in one print, and the smallest one always gets claimed first. Quilted cotton, azo-free skin-safe colours, and a wipe-clean lining for everything that leaks. The large works as a toiletry kit or a packing cube, the medium holds creams and wipes, the small takes hair clips, coins, or crayons. A set of three that outlives the trip it was bought for. ₹1,199 for all three. Hand block-printed in Jaipur, one motif pressed at a time.

### Quilts (`/collections/quilts`) — 91 words
Tigers, frogs, unicorns and ponies on one side, a coordinating print on the other — reversible, so it changes mood with the room. Cotton voile, hand-quilted cotton fill, azo-free skin-safe colours, no synthetics. Slept under, dragged to the sofa, taken on trains, washed a hundred times, and somehow kept: a full quilt while they're small, then a play mat, a stroller cover, and a light AC blanket as they get taller. ₹1,299, the same price all year. Hand block-printed in Jaipur, one wooden block at a time.

### Swaddle Sets (`/collections/swaddles`) — 89 words
Sunbursts, polka dots, bunnies and bears — two prints to a set, each with its own striped trim. Double-layer cotton muslin dyed with azo-free, skin-safe colours: soft on day-one skin, softer every wash. At 110 x 110cm they keep working long after the wrapping stops — stroller cover, nursing cover, pram shade, floor blanket for tummy time, a light cover on an AC night. Two pieces, ₹999, the same price all year. Hand block-printed in Jaipur, one motif pressed at a time.

---

## 3. Revised product descriptions (drop-in replacements)

Same paragraph count and roughly the same length as the live copy, so each can be pasted straight into the Shopify description field.

### Backpack — `green-stripe-print-kids-backpack`
> Green Stripe Print Hand Block-Printed Kids Backpack

```html
<p>Crisp green stripes, pressed by hand — the kind of bag a child picks out of a row of bags and then won't put down.</p>
<p>Cotton dyed with azo-free, skin-safe colours, because this rides against small shoulders every single day. Hand-quilted with a soft cotton fill, finished with a teal-green tassel zip-pull.</p>
<p>H30 x W25 x D10cm holds a snack box, a water bottle and one favourite toy with room left over; a secure zip and front pocket keep the small things reachable. Sized for roughly ages 2–6, and comfortable on bigger kids too — so it goes to preschool, then playdates, then on a train.</p>
<p>Hand block-printed in Jaipur, one motif pressed at a time — small variations in the print are the mark of genuine handwork, not a flaw.</p>
```

### Toiletry Pouch Set — `bunny-floral-toiletry-pouch-set`
> Bunny Floral Print Hand Block-Printed Toiletry Pouch Set (3-Piece)

```html
<p>Pink bunnies hop through yellow blooms — as good holding soap and a comb as it is holding alphabet blocks, which is usually where it ends up.</p>
<p>Quilted cotton dyed with azo-free, skin-safe colours, with a wipe-clean plastic-lined interior and a matching yellow tasselled zip-pull.</p>
<p>Three nested pouches, and none of them stay in the bathroom for long: the large works as a toiletry kit or a packing cube, the medium as a travel organiser for creams and wipes, the small as a hair-clip pouch or a coin purse — or hand all three to a toddler as a sorting kit for crayons, blocks and cars.</p>
<p>Hand block-printed in Jaipur, one motif pressed at a time — small variations in the print are the mark of genuine handwork, not a flaw. A set of 3, ready to gift.</p>
```

### Quilt — `tiger-jungle-print-reversible-cotton-quilt-razai`
> Tiger Jungle Print Reversible Cotton Quilt (Razai)

```html
<p>Golden tigers prowl through green palms across this ivory quilt, tiny red stars between them — a print that turns nap time into a small adventure. Flip it and it's palms only, in the same warm palette.</p>
<p>Cotton voile with a hand-quilted cotton fill, dyed with azo-free, skin-safe colours. No synthetics: soft from the first touch, and softer with every wash.</p>
<p>Slept under, dragged around the house, washed a hundred times, and somehow kept — a full quilt while they're small, then a stroller blanket, a play mat, and a lightweight travel or AC blanket as they get taller.</p>
<p>Hand block-printed in Jaipur, one wooden block pressed at a time, so no two quilts carry quite the same leaf.</p>
```

### Swaddle Set — `bunny-floral-stripe-swaddle-set`
> Bunny Floral & Stripe Print Cotton Muslin Swaddle Set (2-Pack)

```html
<p>One side blooms with pink bunnies and lavender florals on a pink striped trim; the other keeps it classic, blue stripes on a coral candy-stripe trim. Two prints, so there's always a clean one.</p>
<p>Double-layer cotton muslin dyed with azo-free, skin-safe colours — soft against day-one skin, and softer every wash.</p>
<p>At 110 x 110cm each, they keep earning their place long after the wrapping stops: stroller cover, nursing cover, pram shade, floor blanket for tummy time, a light cover on an AC night.</p>
<p>Hand block-printed in Jaipur, one motif pressed at a time — small variations in the print are the mark of genuine handwork, not a flaw. A set of 2, ready to gift.</p>
```

---

## 4. Flag list — where the site contradicts the ads

Ordered by how much it would cost you if left alone.

1. **Discount messaging is everywhere, and the ads are not discount ads.** "15% off your first order" runs in the announcement bar, as a WELCOME15 badge on every product page, in the footer signup, and in the popup. A visitor who arrives on "For the sister who became a mother this year" lands on a page whose loudest element is a coupon. It also directly breaks the no-discount brand rule. *Decision needed: suppress WELCOME15 for ad traffic, or accept the clash for Rakhi.*

2. **Delivery promise vs the Rakhi date — the single biggest risk.** The product page badge says "Ships in 3 days from Jaipur", while the accordion says "dispatched within 3 working days and delivered across India in 5–8 days" — i.e. up to **11 days**. Rakhi is 28 August; today is 11 August. Any ad implying arrival in time needs a stated order-by date on the page, and the two statements need to agree. Right now a shopper can reasonably read "ships in 3 days" as "arrives in 3 days".

3. **Free shipping threshold sits exactly on the ad price.** The strip says "Free shipping over ₹999". Backpacks and swaddle sets are ₹999 — *at* the threshold, not over it. If the Shopify rule is strictly "over", two of the four advertised categories don't qualify and the shopper finds out at checkout. **I could not verify the actual shipping rate configuration** (that needs admin access) — worth checking before spend starts. Cheapest fix is wording: "₹999 and above".

4. **Skin-safety is stated inconsistently.** Azo-free / skin-safe appears in the description text for backpacks and pouches, but **only in the accordion** for quilts and swaddles. The promise spine puts skin-safe second on every page, and it's the load-bearing claim for a kids-textile ad. Add it to quilt and swaddle descriptions (done in section 3 above).

5. **"Tested safe for everyday use by little ones" is an unbacked claim.** It appears in the "Is it safe for newborns?" accordion on every product. There's no named test, standard, or certificate behind it — GOTS and OEKO-TEX are still only *in progress* per the product-marketing doc. If ads lean on skin-safety, this is the sentence that gets challenged. Safer: state what's true — azo-free dyes on natural cotton — and drop "tested".

6. **"A genuine four-in-one set" on a 3-piece product.** In every toiletry pouch description, contradicting the title and the "A set of 3" line in the same paragraph. Reads as a mistake, or worse, as one pouch missing from the box. Fixed in the draft above.

7. **All four collection pages have no description.** Verified: `body_html` is null for backpacks, toiletry-pouches, quilts and swaddles, and the live pages render nothing but a grid. If any ad points at a collection rather than a product, the emotional line in the ad has nothing to land on. Section 2 fills this.

8. **The newborn accordion appears on backpacks.** A product for ages 2–6 answers "Is it safe for newborns? Yes". It's the same boilerplate block on all 26 products. Harmless individually, but it signals copy that wasn't looked at.

9. **Swaddles list only 3 alternate uses; the brand rule asks for 5+.** Current copy: stroller cover, nursing cover, lightweight blanket. The revision adds pram shade and tummy-time floor blanket. This matters commercially — it's the argument against "she'll outgrow it in a year".

10. **Quilts lead with the print but not with *reversible*.** The ad's opening asset is the flip. On the page, "reversible" is in the title and the last clause of the last paragraph. Moved into paragraph one in the draft.

---

### Grounding note
Every claim used above already appears on the live pages: hand block-printed in Jaipur one motif at a time; small print variations as the mark of handwork; azo-free skin-safe dyes; backpack H30 x W25 x D10cm and ages 2–6; quilts reversible with cotton voile and hand-quilted cotton fill; pouch sets 3-piece with the three stated sizes; swaddles 2-pack at 110 x 110cm double-layer muslin. No review counts, ratings, customer numbers, or certifications have been introduced.
