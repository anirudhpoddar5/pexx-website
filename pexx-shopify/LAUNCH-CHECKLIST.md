# PEXX — Launch Checklist
> Everything left to go live, in order. Companion to [SHOPIFY-BUILD.md](SHOPIFY-BUILD.md) (what's built) and [ECOMMERCE-REQUIREMENTS.md](ECOMMERCE-REQUIREMENTS.md) (strategy).
>
> **Legend:** 🧑 = you / production · 🤖 = Claude can do · ⏳ = has a lead time, start early
>
> **Status:** the storefront is fully built on the **Dwell draft theme** (preview: `?preview_theme_id=165377146969`). What remains below is operational (accounts, payments, data) — not theme work.

---

## ✅ Already done (the three quick admin actions)
- [x] **WELCOME15** discount created (15% off, once per customer) — powers the popup
- [x] **Product Type** filter live (Search & Discovery). *Age/Occasion deferred to real-product time — clean metafield + friendly labels, ~5 min then.*
- [x] Leads route to **info@poddarexp.com** (Sender email). 🧑 confirm you monitor that inbox.

---

## 1. Payments — Razorpay + COD ⏳ 🧑 **(start today — KYC takes 1–2 days)**
- [ ] Sign up at **razorpay.com** with business KYC: PAN, bank account, GST
- [ ] Shopify → **Settings → Payments → Add provider → Razorpay** → connect with your API keys
- [ ] Turn on COD: **Settings → Payments → Manual payment methods → Cash on Delivery**
- 🤖 *I'll confirm the config and test a checkout once it's connected.*

## 2. Multi-currency for NRI ⚠️ 🧑
- [x] ✅ **US + UK markets created & active** (Settings → Markets). International shipping wired.
- ⚠️ **USD/GBP pricing is blocked** — needs Shopify Payments (unavailable in India). NRIs currently pay in **INR** (card does the FX). True USD/GBP checkout = add **PayPal** later. Not a launch blocker.

## 3. Shipping ✅
- [x] ✅ Domestic **Standard Shipping ₹99** set.
- [x] ✅ **Free shipping over ₹750** (automatic discount, active; lowered from ₹999 on 14 Aug 2026 and set to combine with the 15% codes). Trust bar + PDP line updated to match.

## 4. Taxes / GST 🧑
- [ ] **Settings → Taxes and duties → India** → enter **GSTIN**
- [ ] Decide **tax-inclusive pricing** (standard in India)

## 5. Real products ⏳ 🧑 production + 🤖
- [ ] Production fills the **product sheet** (text: title, price, type, variants, tags `category`/`type`/`age_`/`price_`/`occasion_`, + an `image filename` column)
- [ ] Production shares the **photo files** as a folder/zip (named to match the filename column)
- 🤖 *I bulk-import the products and attach the photos via the API — replacing the 10 placeholders. Then I add clean Age/Occasion filters.*

## 6. WhatsApp 🧑 + 🤖
- [ ] Install **Interakt or Wati** (needs your WhatsApp Business number)
- 🤖 *I wire the WhatsApp chat button into the theme afterwards.*

## 7. Email domain authentication (DNS) ✅
- [x] ✅ **Fully done & verified** — SPF + Shopify sender CNAMEs (×6) + DMARC + Google DKIM all live and resolving. Order emails from info@poddarexp.com are inbox-safe. Details: `DNS-EMAIL-RECORDS.md`
- [ ] (Later, optional) tighten DMARC `p=none` → `quarantine` → `reject` after a few clean weeks.

## 8. Legal 🧑
- [x] ✅ All 4 policies redrafted (India-compliant: DPDP, children's data, grievance officer, IP, force majeure, consumer carve-outs) + published to pages. Source: `content-drafts/POLICIES-FINAL.md`
- [ ] Have a lawyer do final sign-off on **Privacy** + **Terms**
- [x] Address + phone on policy pages — **owner decided to omit** (accepted risk; technically required under E-Commerce Rules 2020 but widely skipped). GST stays on invoices only (Shopify auto-generates). Email contact `info@poddarexp.com` is published.

## 9. Reviews (post-launch) 🤖
- [ ] After first orders ship, install **Judge.me** (free) → I wire star ratings onto product cards + PDP

---

## 🚀 Launch day (do in this order)
1. [ ] 🤖 Final QA pass on the published-candidate theme
2. [ ] 🧑 **Publish** the Dwell theme (Online Store → Themes → Publish)
3. [ ] 🧑 **Remove password** (Online Store → Preferences → uncheck Password protection)
4. [ ] 🧑 **Connect domain**: Settings → Domains → point **poddarexp.com** to Shopify (A record → `23.227.38.65`, `www` CNAME → `shops.myshopify.com`)
5. [ ] 🧑 Place one real test order (incl. COD) end-to-end
6. [ ] 🧑 Rotate/delete the **"PEXX API" custom app** to revoke the build token

---

## Critical path
**Razorpay KYC (#1)** is the long pole — start it today. Shipping / tax / markets are quick settings. Products (#5) can run in parallel with production. Everything else is fast once accounts exist.

## What I (Claude) can still do right now, no blockers
- Build the product-import sheet template
- Any further design/content tweaks you flag
- Wire shipping-threshold messaging once you decide the number
- Prep the Judge.me + WhatsApp wiring so it's one step at launch
