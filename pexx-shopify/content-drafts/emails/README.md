# PEXX email suite — what to paste where

Drafted 15 Aug 2026. Status updated 17 Aug 2026 — see "Where this stands" below.

Preview of all eight, laid out as they'll look:
https://claude.ai/code/artifact/84a8640a-e69d-42e2-a981-d1ef1f70faa3

## Already done, don't redo

- **Visual branding of transactional emails** — PEXX wordmark (180px) and accent `#9E3B2F` are already set under
  Settings → Notifications → **Customize email templates**. Applies to every notification email. Leave it alone.
- **`custom.print_note`** product field — created, live on all 38 products, 35 values filled.
- **Order confirmation** and **Shipping confirmation** — `transactional-snippets.md` is applied and live.
- **Abandoned-cart email** — subject and preview text already updated and live; recipients already widened to All customers.
- **Google & YouTube sales channel** — the 10 quilts and pouch sets that were on Facebook & Instagram but not
  Google were published on 17 Aug 2026 (Products → select → ··· → Include in sales channels). All 10 now show
  4 channels. The Gift Pouch was deliberately left out.

## Where this stands

| # | File | Where it goes | Status |
|---|---|---|---|
| 1 | `transactional-snippets.md` | Settings → Notifications → Order confirmation / Shipping confirmation → **Edit code** | ✅ live |
| 2 | `marketing-emails.md` § Abandoned cart | Messaging → Automations → Recover abandoned checkout → ··· → Edit | ✅ live 17 Aug 2026 |
| 3 | `marketing-emails.md` § Welcome | Messaging → Automations → Welcome new subscribers | ✅ live 17 Aug 2026 |
| 4 | `print-notes-howto.md` | Products → each product → Print note field | ✅ 35 of 38 |
| 5a | Browse abandonment (§6) | Automations → Create automation → Convert abandoned product browse | ⚠️ created, **Inactive**, copy half-done |
| 5b | Win-back (§5) | Automations → Create automation → Win back customers | ⏳ not started |
| 5c | Care (§3) | Custom automation in Flow — Order fulfilled + 8 days | ⏳ not started |
| 5d | Review (§4) | Custom automation in Flow — Order fulfilled + 22 days | ⏳ not started |

**Browse abandonment, exact state as of 17 Aug 2026:** the automation exists and is **Inactive**, so it is
not sending. Subject was changed to "The one you were looking at" and preview text to "Still here, and
here's how it's made." — both confirmed on screen. The headline was typed as "You were looking at this one"
but the browser connection dropped before that could be verified, so **check the headline first**. Still to
do on it: the Sanganer paragraph, the button label "Have another look", and the trust line. Then **Turn on**.

### What the automation library actually offers

Read off the real template list on 17 Aug 2026:

| Email we want | Template to use | Note |
|---|---|---|
| Browse abandonment (§6) | **Convert abandoned product browse** | exact match |
| Win-back (§5) | **Win back customers** | template sends a **discount** to a 60-day winback segment. Our copy carries no discount — the discount block has to be deleted. |
| Care instructions (§3) | none | no delivery trigger exists |
| Review request (§4) | none | no delivery trigger exists |

**There is no "order delivered" trigger.** Searching Flow's trigger list for "deliver" returns exactly one
result — *Fulfillment order line items prepared for local delivery* — which is local delivery only.
The usable proxy is **Order fulfilled** (fires at dispatch) plus a Wait step.

Delays derived from the published shipping policy ("ship within 3 working days… reach you across India in
**5–8 days**" from dispatch), using the far end so nothing arrives before the parcel:

| Email | Doc says | Flow build |
|---|---|---|
| Care (§3) | on delivery, same day | Order fulfilled → **Wait 8 days** → send |
| Review (§4) | 14 days after delivery | Order fulfilled → **Wait 22 days** → send |

⚠️ Conflict to resolve: the live shipping-confirmation email says "Most arrive within **three to five**
days", while `/pages/shipping-policy` says **5–8 days**. Same journey, two numbers. The 8/22 figures above
follow the policy page. If the real average is 3–5, these should come down to 5 and 19.

## Deviations in what was built, 17 Aug 2026

Recorded so nobody thinks these were accidents:

- **Headline font.** Spec says headlines are serif. In both emails the opening headline shares a text block
  with the paragraph beneath it, and the editor applies font per *block*, so making the headline serif would
  have made the body serif too. Headlines were left in the default bold sans. `WELCOME15` is Georgia serif
  as specified, because it is its own element.
- **Welcome email order.** The trust line sits just above the two closing paragraphs rather than below them.
  Moving it needs a drag-and-drop inside a live email; not worth the risk.
- **`custom.print_note` was not inserted** into the abandoned-cart email. The editor's personalisation
  inserter offers customer/order fields, not product metafields. Per the rule in this file, the line was
  left out entirely rather than replaced with filler.
- **Trust line size** is 13px, not 12.5px — the size field takes whole numbers. 13px also matches the
  13.5px secondary line already live in the transactional emails.

## How to get into these editors — the click path

Walked and verified 17 Aug 2026.

**To edit an existing automation's email**

1. `Messaging` → `Automations` in the left nav. The app takes ~15 seconds to appear — a blank grey
   panel means still loading, not broken.
2. On the automation's row, click `···` at the far right → **Edit automation**.
3. This opens **Shopify Flow**, not an email editor. You'll see the workflow:
   trigger → condition → `Send marketing email`.
4. Click the **Send marketing email** box. A panel opens on the left with a preview of the email.
5. Click **Edit email**. The Shopify Email editor opens full-screen.
6. It opens in **View only**. Click **Edit** (top right), then **Continue** on the warning.
7. The status chip flips to **Draft**. Edit away — it autosaves ("All changes saved").
8. When finished click **Set to active** (top right), then confirm the row reads `Active`
   back on the Automations list.

**Editing text inside the email:** one click selects the *block* and typing does nothing.
**Double-click** to get a cursor, then triple-click to select a line, then type. Font, size and
colour live in the left panel and apply to the whole block — so a headline and a paragraph sharing
one block cannot have different fonts.

**To build a new automation:** `Automations` → **Create automation** → pick a template, or
**Create custom automation** at the bottom, which drops you into Shopify Flow with a blank trigger picker.

**Never touch "Send test"** — that field comes pre-filled with a real customer's address.

## The one dangerous step

Editing the abandoned-cart body flips it back to **Draft**. It has already sent 2 recovery emails.
After editing you must click **Set to active**, or recovery emails silently stop.

## Correction — an earlier claim in this file was wrong

An earlier version said the Shopify Email editor could not be driven by an agent because it sits in a
cross-origin iframe. Wrong diagnosis. The first clicks failed because the browser tab was not frontmost,
so Chrome was not compositing the embedded frame. With the tab in front every click lands, and the
Welcome email was edited and set live that way.

## The one rule

Everything in these files is verifiable against what PEXX actually does — Chhipa printers, women across
printing/design/stitching/finishing, zero discharge, Sanganer, vertical integration, free shipping over ₹750,
10-day returns, COD, azo-free dyes, ships in 3 days.

**No discounts anywhere except the welcome email.** The site sells on "never a fake sale"; a recovery
discount contradicts it and teaches people to abandon carts.

## Claims that needed checking

1. ~~How long one quilt actually takes a printer.~~ **Confirmed by owner, 17 Aug 2026: a day or two.**
   Block printing is slow — one block, one colour, one press at a time, with drying between colours.
   The review email (§4) now says "a day or two at the table". The earlier "a morning" was wrong and understated it.
2. Whether customers have genuinely sent photos of hand-me-downs. Still unverified — I removed this,
   don't reinstate it unless true.
