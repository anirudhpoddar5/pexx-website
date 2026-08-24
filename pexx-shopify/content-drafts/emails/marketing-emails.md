# Marketing emails — copy to paste

These go into Shopify Email's visual editor (Messaging → Automations), so they're plain copy, not code.
Paste block by block. The editor's own styling already carries the PEXX wordmark.

Formatting to apply in the editor:
- Headlines: **serif**, ~28px, colour `#2B241F`
- Body: default sans, ~15px, colour `#463E36`
- Button: background `#9E3B2F`, white text, uppercase
- Trust line at the foot: ~12.5px, colour `#6F655B`

---

## 1. Abandoned cart — LIVE, needs body replaced

Subject and preview text are already updated. Replace the body only.

**Headline**
> We've kept it for you

**Body**
> Nothing has been lost — your basket is exactly as you left it, waiting for whenever the moment is right.

*(product block — the editor inserts this automatically)*

> `{{ product.metafields.custom.print_note }}`

> Every colour here is mixed and matched by our own design team, and printed by hand a few metres at a time. It's a slow way to work, and it's the reason the piece looks the way it does.

**Button:** Return to your basket

**Trust line**
> Free shipping over ₹750 · Ships in 3 days from Jaipur
> 10-day returns · Cash on delivery · Skin-safe, azo-free dyes

**Footer**
> Reply to this email and a person here will answer.
> PEXX · Jaipur, India

⚠️ If the editor won't accept the metafield variable, leave that line out entirely. Do **not** substitute
generic filler — an empty space is better than words that don't match the product.

---

## 2. Welcome — LIVE, needs body replaced

**Subject:** Welcome to PEXX
**Preview:** Your 15% is inside — and a word on why our prices look the way they do.

**Headline**
> We're glad you're here

**Body**
> Here is the 15% we promised, for whenever you'd like it:

**WELCOME15** *(serif, 24px, `#9E3B2F`)*

> Applied at checkout, on your first order.

*(divider)*

> You may notice our prices sit below others doing similar work. There's no trick in it, and nothing has been thinned out to get there.

> We do all of it ourselves — the printing, the stitching, the finishing, the packing — under one roof in Jaipur. Nothing is sent out to a middleman and nothing comes back with a margin added. What you save is simply the part of the price that usually goes to everybody in between.

> It also means we never need a sale. The price in January is the price in October.

**Button:** Have a look around

**Trust line**
> Free shipping over ₹750 · 10-day returns · Cash on delivery
> Delivered across India

---

## 3. Care instructions — NEW automation

**Trigger:** Order delivered · **Delay:** same day

**Subject:** Looking after it
**Preview:** One cold wash on its own, and it will last for years.

**Headline**
> It's with you. Here's how to keep it well.

**Body**
> Natural cloth and natural dyes ask for a little more than synthetics, and give a great deal more back. Four things:

1. First wash cold and on its own. A little colour will come away — that's surplus dye leaving, not the print going.
2. Mild detergent. No bleach, no softener.
3. Dry in the shade. Direct sun will flatten the colour over a season.
4. It softens every time you wash it. That's the cotton doing what it should.

*(divider)*

> The dyes we use are azo-free, and our workshop runs on zero discharge — nothing goes into the ground or the water around us. It's slower and it costs us more. It also means the thing in your home is exactly what it appears to be.

> If anything isn't right, reply within 10 days and we'll take it back. No forms, no restocking fee.

**Trust line**
> Made in Jaipur · Natural fabrics · Azo-free, skin-safe dyes

---

## 4. Review request — NEW automation

**Trigger:** 14 days after delivery · Judge.me is installed and unused

**Subject:** Would you tell us how it's held up?
**Preview:** Two lines would help us more than you'd think.

**Headline**
> A fortnight in — how is it?

**Body**
> You'll have washed it by now, which is when you find out whether a thing was made properly.

> When you chose something printed by hand, a printer in Sanganer spent a day or two at the table with it. Block printing is slow — one block, one colour, one press at a time, and the cloth has to dry between colours. That work continues because people keep choosing it — every order is a few more days of it, and a reason for the next generation of a printing family to stay at the table.

> If ours has earned its place, would you write a line or two? It's how the next person decides.

**Button:** Write a review

> And if it hasn't earned its place — reply and tell us why. That's worth more to us than any rating.

---

## 5. Win-back — NEW automation

**Trigger:** 60–90 days, no order

**Subject:** New prints on the table
**Preview:** Fresh off the blocks in Jaipur.

**Headline**
> New prints on the table

**Body**
> It's been a while, so here's what's come off the blocks since you were last here.

> Block-printed cotton is one of the few things that improves with handling. The colour settles, the cloth softens, the print takes on a little history. People keep these, and then pass them on — which is rather the point of making them slowly.

**Button:** See what's new

> Same prices as when you last visited. We don't run sales, so there's nothing to wait for.

**Trust line**
> Free shipping over ₹750 · 10-day returns · Cash on delivery

Note: deliberately says nothing about children — it has to still work when the range widens.
Also deliberately carries no discount code, even though "Return win-back 15%" exists.

---

## 6. Browse abandonment — NEW automation

**Trigger:** viewed a product, didn't add to cart · **Delay:** 24 hours

**Subject:** The one you were looking at
**Preview:** Still here, and here's how it's made.

**Headline**
> You were looking at this one

*(product block)*

> `{{ product.metafields.custom.print_note }}`

> It was printed in Sanganer, just outside Jaipur, where the water and the cloth have suited each other for four hundred years. One block, one colour, one press at a time — each colour laid over the last, the whole length of the fabric, by eye.

**Button:** Have another look

**Trust line**
> Free shipping over ₹750 · Ships in 3 days from Jaipur · 10-day returns
