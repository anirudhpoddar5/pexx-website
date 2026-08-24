# Shipping Policy — findings + draft (NOT PUBLISHED)

Investigated 2026-08-11. Nothing was written to the live store. All Admin API calls were GET only.

---

## 1. What is actually broken

`https://shop.poddarexp.com/policies/shipping-policy` → **HTTP 404**.

Root cause, confirmed via Admin API (`GET /admin/api/2025-07/policies.json`): the shop has **only four policy records** — Contact, Privacy policy, Refund policy, Terms of service. There is **no Shipping policy record at all** in Settings > Policies. Shopify only serves `/policies/<handle>` for policies that have a body, so the URL 404s because the record was never created.

**The storefront does not link to the broken URL.** Every shipping link on the site points to `/pages/shipping-policy` — a normal Shopify page that exists and returns **200**. Checked the rendered HTML of the homepage, the product page `/products/blush-unicorn-print-kids-quilt`, the cart, and the footer: all four contain exactly one `href="/pages/shipping-policy"` and zero references to `/policies/shipping-policy`.

So this is not a broken on-page link. It is a **missing policy record**, which still matters because:

- Shopify's checkout, its Shop app / AI surfaces, and its built-in `search_shop_policies_and_faqs` MCP tool (present in the product page HTML) read the **policy record**, not the `/pages/` page. They currently see no shipping policy.
- The theme's `snippets/tax-info.liquid` and `blocks/price.liquid` both branch on `shop.shipping_policy.body == blank` — the shipping-terms line at checkout/price is silently suppressed because the record is empty.
- Ad reviewers and trust crawlers commonly probe the canonical `/policies/shipping-policy` path.
- `pexx-shopify/tests/e2e/footer-and-newsletter.spec.ts:9` asserts the footer link is `/pages/shipping-policy`, so that test will need updating if the footer is repointed.

## 2. Policy page status (live, verified by HTTP status code)

| URL | Status |
|---|---|
| `/policies/shipping-policy` | **404** — record does not exist |
| `/policies/refund-policy` | 200 |
| `/policies/privacy-policy` | 200 |
| `/policies/terms-of-service` | 200 |
| `/policies/contact-information` | 200 |
| `/policies/legal-notice` | 404 (optional in Shopify; not required) |
| `/policies/subscription-policy` | 404 (not applicable — no subscriptions) |
| `/pages/shipping-policy` | 200 — the real, working page |

## 3. Admin API read-only findings

- Policies present: Contact (149 chars), Privacy policy (18,307), Refund policy (2,820), Terms of service (24,452). No shipping policy.
- Shipping zones: **Domestic** (India) and **International** (28 countries: US, UK, UAE, Canada, Australia, Singapore, most of Western Europe, Japan, HK, NZ, Israel, South Korea, Malaysia, Poland, Czechia).
- **Rate amounts could not be read.** The REST zone objects return empty rate arrays (rates live in delivery profiles), and the GraphQL `deliveryProfiles` query returned `ACCESS_DENIED` — the app token lacks the shipping read scope. The ₹999 free-shipping threshold below is taken from the live storefront copy, not from the rate config. See open questions.
- Registered business address on the Contact policy: F 85, Kartarpura Ind Area, 22 Godown, Jaipur - 302006. Email: info@poddarexp.com.

## 4. Two content conflicts to resolve before publishing

1. **Returns window.** Product pages and the announcement bar say **"10-day returns."** `/policies/refund-policy` says **"30-day return policy."** These contradict each other on a live, ad-facing page. Pick one.
2. **Return address is a placeholder.** The live refund policy literally contains the text `[INSERT RETURN ADDRESS]`. This is visible to any Meta reviewer who opens it, and is a bigger ad-approval risk than the 404.

Also note the live refund policy contains an EU 14-day cooling-off clause and a "we'll send you a return shipping label" promise — both look like unedited Shopify boilerplate for an India-first store.

## 5. Existing `/pages/shipping-policy` content (live today)

> Orders ship within 3 working days and usually reach you across India in 5–8 days. You'll get tracking once it's on the way. Pay by Cash on Delivery, card, UPI, net-banking, or wallet — all work across India. Sending a gift to India from abroad? Order from anywhere and ship to any Indian address — billed in INR, your bank handles the conversion. We also ship to the US and UK at a flat rate shown at checkout (any customs duties are the recipient's). Around festivals, order by the date shown on the product or banner to be safe. Timelines are estimates and can shift during peak periods or courier delays.

It omits the ₹999 free-shipping threshold, says nothing about damaged or late parcels, and says US/UK only while the store's International zone is actually configured for 28 countries.

---

## 6. DRAFT — Shipping Policy

Paste into Settings > Policies > Shipping policy. Plain text with headings; Shopify's editor accepts formatting.

---

### Shipping Policy

Everything we make is hand block-printed in Jaipur and ships from our workshop there.

**When does my order ship?**
We dispatch within 3 working days of your order. You'll get a tracking link by email as soon as it's on the way.

**When will it arrive?**
Most orders reach addresses across India in 5–8 days from dispatch. Remote pin codes can take a little longer. These are estimates, not guarantees — festival periods and courier delays can push them out. If you're buying for a specific date, order early and check any cut-off date shown on the product page or the banner.

**What does shipping cost?**
Shipping is free on orders over ₹750 within India (threshold lowered 14 Aug 2026). Below that, the shipping charge is calculated and shown at checkout before you pay.

**Can I pay cash on delivery?**
Yes. Cash on delivery is available across India. You can also pay by UPI, card, net-banking or wallet.

**Sending a gift to India from abroad?**
You can order from anywhere and ship to any Indian address. You'll be billed in INR; your bank handles the currency conversion. Gift wrapping can be added at checkout.

**International orders**
We ship to selected countries outside India. Available destinations and the exact shipping charge are shown at checkout once you enter your address. Any customs duties or import taxes are payable by the recipient.

**What if my order arrives damaged, or doesn't arrive?**
Please check your parcel when it arrives. If anything is damaged, missing or not what you ordered, email us at info@poddarexp.com with your order number and a photo within 48 hours of delivery and we'll sort it out — replacement or refund, your choice.

If tracking hasn't moved for several days, or your order is well past the estimated window, write to us at info@poddarexp.com and we'll chase the courier for you.

**Wrong or incomplete address**
We can only ship to the address you give us at checkout. If a parcel comes back to us because the address was incomplete or nobody was available to receive it, we'll contact you to arrange redelivery.

Questions: info@poddarexp.com
PEXX, F 85, Kartarpura Industrial Area, 22 Godown, Jaipur 302006, India

---

## 7. How to publish (Shopify policy pages are not normal pages)

1. Shopify admin → **Settings** (bottom-left) → **Policies**.
2. Scroll to **Shipping policy** → click **Add shipping policy** (or **Edit** if it shows one).
3. Paste the draft into the rich-text box. Use the toolbar to bold the question headings.
4. Click **Save**. The page goes live immediately at `https://shop.poddarexp.com/policies/shipping-policy` — no theme publish, no deploy needed.
5. Verify: open that URL and confirm it returns the page rather than 404.

**Do not** create this under Online Store → Pages. That is what produced the current `/pages/shipping-policy`, which Shopify's checkout and AI surfaces do not read.

While in Settings > Policies, also fix `[INSERT RETURN ADDRESS]` in the Refund policy — same screen, same Save.

**After publishing, tidy the duplicate:** the site will then have the same content at two URLs. Either (a) repoint the footer/product links to `/policies/shipping-policy` and delete or redirect the `/pages/` version, or (b) leave the page and add a redirect. Whichever you pick, update `pexx-shopify/tests/e2e/footer-and-newsletter.spec.ts:9`, which currently asserts `/pages/shipping-policy`.

---

## 8. Open questions for the owner — do not invent answers

1. **Courier.** Which courier(s) actually deliver? The draft deliberately names none. Delhivery is referenced elsewhere in this repo as a planned integration but is not confirmed as the live carrier.
2. **Tracking.** Is a tracking link genuinely sent on every order today, including COD? The draft promises one; if that's not automated yet, soften it or wire it up first.
3. **Shipping rate config.** Is the ₹999 free-shipping threshold actually configured in Settings > Shipping, or only claimed in the storefront copy? Could not read rates with the current API token. **Verify this before running ads** — an ad-driven customer charged shipping on a ₹1,299 order after seeing "free over ₹999" is a chargeback and a bad review.
4. **Below-threshold shipping charge.** What is the flat rate under ₹999? Draft says "calculated at checkout" as a safe placeholder.
5. **International.** The zone covers 28 countries but the current page says US and UK only. Which is true, and at what rate? The draft says "selected countries, shown at checkout" to avoid over-promising.
6. **Returns window: 10 days or 30?** Must be reconciled with the Refund policy.
7. **Return address** for the Refund policy placeholder.
8. **RTO / refused delivery on COD.** If a COD parcel is refused or returns undelivered, is anything charged, and is the customer blocked from future COD? Not addressed in the draft.
9. **Damage claim window.** The draft proposes 48 hours with a photo. Confirm or change.
10. **Free-shipping threshold on international orders** — presumed India-only; the draft scopes it that way.
