# PEXX WhatsApp Marketing Opt-In Plan

Status: draft, awaiting `order_confirmed` / `order_dispatched` template approval before any send-side code changes.
Scope: 1-2 week actionable bootstrap, not a long-term roadmap.

## The compliance model

Meta requires prior, demonstrable opt-in before sending Marketing-category templates.
Since Nov 2024, opt-in can be collected on *any* channel, not just WhatsApp itself.
The unlock: **a person messaging your business number first is itself a valid opt-in
moment.** Their message opens a free 24-hour service window; you reply free-form
("Reply YES to get new drops & offers from PEXX"), log the YES. This is why every
tactic below routes back to getting someone to send the *first* message — the
business number never sends anything unsolicited.

Same number carries utility + marketing. Marketing spam reports throttle the whole
number, including order confirmations — keep marketing sends to 2-4/month and don't
put promotional language inside the Utility templates themselves (Meta will
recategorize them).

## Week 1 — personal contacts (the only real asset today)

1. **Build the entry point** (~2 hrs). A `wa.me` link with pre-filled text:
   `https://wa.me/919660333911?text=Hi%20PEXX!%20Send%20me%20updates`
   The recipient's own tap-to-send is the initiating event.
2. **Log consent** in the Worker — phone, timestamp, exact consent wording, source.
   This is the DPDP compliance record. Small addition to existing KV/D1, reuses infra
   already built for the Worker.
3. **Outreach from personal WhatsApp**, not the business number:
   - Individual messages to relatives/friends (not one mass blast), ~20-30/day.
   - WhatsApp Status posts with the link, 2-3x this week.
   - Family/community groups already a genuine member of — one share, not repeated.
   - Personal-to-personal messaging isn't governed by WhatsApp Business Platform
     policy at all, only the business number's sends are.
4. **Expected yield**: personal networks convert 30-60% when asked individually.
   ~150 contacts -> realistically 50-80 opted-in subscribers by end of week 1.

## Parallel — free owned channels that compound

- Floating WhatsApp button + footer link on the Shopify storefront (hand-codable,
  no app needed).
- **Constraint**: custom checkout-step consent checkboxes need Shopify Plus. Not
  assumed available. Workaround: put the opt-in CTA on the order-status/thank-you
  page instead (works on all plans), and ask for marketing consent in-thread when
  customers reply to the order-confirmation Utility message.
- Do not install Meta's official "WhatsApp by Meta" Shopify app — the number is
  already wired into the custom Cloud API Worker; a second integration conflicts.
- QR code insert card in shipped parcels ("Scan for new block-print drops") —
  highest-intent, zero-cost channel for a handmade goods brand.
- `wa.me` link in Instagram bio now, even with zero relevant D2C followers today —
  costs nothing, compounds as the account grows.

## Ads — click-to-WhatsApp, not yet

"Message us on WhatsApp for 15% off" is the standard CTWA hook and one of the
best-converting formats for opt-in specifically, since the ad click opens directly
into a chat and the resulting first message is the opt-in event itself.

Benchmarks (India, 2025/26): ~₹15-60 per started conversation, 4-12% click-to-order
conversion over 30 days.

Skip for the first two weeks — no proven welcome-flow or conversion data yet, and at
under 100 subscribers a test budget teaches less than 150 free personal-network
conversations will. Revisit week 3-4: small test at ₹300-500/day x 7 days (~₹3,000),
targeting parents 25-40 in metros, "Message us for 15% off your first PEXX order".
Judge on cost-per-opt-in: under ₹60 -> scale, over ₹150 -> fix the creative/offer
before spending more.

## India compliance, practically

- TRAI's TCCCPR doesn't currently cover WhatsApp (it governs telecom SMS/voice) —
  SMS is already out of scope for this brand, so no DLT registration needed.
- DPDP Act 2023 rules notified Nov 2025, full enforcement by May 2027. Being ahead of
  it now costs almost nothing: clear consent wording + logged records (step 2 above),
  honor opt-outs immediately and log them, one line in the Shopify privacy policy
  about WhatsApp usage for order updates and, with consent, marketing.

## Explicitly skip for now

Paid BSPs (Interakt/Wati), WhatsApp Flows forms (a "reply YES" beats a form at this
scale), segmentation tooling, CTWA ads (first 2 weeks), any Instagram content grind.
At this scale a phone-number list plus a send script is the whole stack.

## Next actions once templates are approved

1. Add consent logging to the Worker (KV: phone -> {timestamp, consent_text, source}).
2. Build the one-off send script for the Marketing template, reusing `META_WA_TOKEN`
   and the existing `sendTemplate` pattern from `src/index.ts`.
3. Add the `wa.me` footer button + thank-you page CTA to the Shopify theme.
4. Start personal outreach.
