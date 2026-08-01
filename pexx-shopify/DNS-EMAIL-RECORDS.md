# PEXX — DNS Email Authentication Records

Domain: **poddarexp.com** · DNS host: **GoDaddy** (`domaincontrol.com` nameservers)
Sender email in Shopify: `info@poddarexp.com`
Captured: 2026-06-28

---

## A. Shopify sender authentication — 6 CNAME records

Add these in GoDaddy → DNS Management for poddarexp.com. **Type = CNAME** for all.

> ⚠️ GoDaddy auto-appends the domain. Enter the **Name** exactly as shown (do NOT add `.poddarexp.com`).
> If GoDaddy rejects a trailing dot on the Value, remove it.

| # | Type  | Name (Host)                  | Value (Points to)                              |
|---|-------|------------------------------|------------------------------------------------|
| 1 | CNAME | `wj5._domainkey`             | `dkim1.d707902fa1d3.p464.email.myshopify.com`  |
| 2 | CNAME | `wj52._domainkey`            | `dkim2.d707902fa1d3.p464.email.myshopify.com`  |
| 3 | CNAME | `pdk1._domainkey.mailerurj`  | `dkim3.93928b837c07.p733.email.myshopify.com`  |
| 4 | CNAME | `pdk2._domainkey.mailerurj`  | `dkim4.93928b837c07.p733.email.myshopify.com`  |
| 5 | CNAME | `mailerwj5`                  | `d707902fa1d3.p464.email.myshopify.com`        |
| 6 | CNAME | `mailerurj`                  | `93928b837c07.p733.email.myshopify.com`        |

After adding, return to Shopify → Settings → Notifications → Email domain authentication → click **"I updated DNS records"**. Propagation can take up to 48h (usually <1h on GoDaddy).

**Faster alternative:** Shopify offers **"Authenticate automatically"** — a one-click GoDaddy OAuth that adds all 6 records for you. You'd log into GoDaddy and approve. (You must do this login yourself — I can't authenticate into your registrar.)

---

## B. DMARC record (recommended — not currently set)

This protects deliverability + prevents spoofing. Add **one TXT record**:

| Type | Name      | Value                                                          |
|------|-----------|----------------------------------------------------------------|
| TXT  | `_dmarc`  | `v=DMARC1; p=none; rua=mailto:info@poddarexp.com; fo=1`         |

Start with `p=none` (monitor only). After a few weeks of clean reports, tighten to `p=quarantine` then `p=reject`.

---

## C. Google Workspace DKIM (for info@ outbound — separate from Shopify)

Mail is on Google Workspace. SPF is already correct:
`v=spf1 include:dc-aa8e722993._spfm.poddarexp.com ~all` → chains to `_spf.google.com` ✅

DKIM is **not yet enabled** for Google. To turn it on:
1. Google Admin (admin.google.com) → Apps → Google Workspace → Gmail → **Authenticate email**
2. Select poddarexp.com → **Generate new record** (2048-bit)
3. Google gives you ONE TXT record (host `google._domainkey`) → add it in GoDaddy
4. Back in Google Admin → **Start authentication**

This is independent of the Shopify records above — both can coexist.

---

## Current state (verified via dig, 2026-06-28) — ALL COMPLETE ✅
- SPF: ✅ present and valid
- Shopify sender CNAMEs: ✅ ALL 6 added via GoDaddy auto-auth + verified resolving.
- DMARC: ✅ live — `v=DMARC1; p=none; rua=mailto:info@poddarexp.com; fo=1` (monitoring mode; tighten to quarantine→reject later)
- Google DKIM: ✅ live + authenticating — selector `google._domainkey`, 2048-bit, verified resolving via dig.

**Email authentication is fully done.** Order/notification emails from info@poddarexp.com are now SPF + DKIM + DMARC aligned.
