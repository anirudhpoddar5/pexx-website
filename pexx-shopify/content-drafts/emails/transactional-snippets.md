# Transactional emails — exact find-and-replace

These are **snippets, not whole templates.** Do not paste a full template over Shopify's — theirs contains
split-cart, pending-payment and local-pickup logic that must survive. Change only the lines below.

Both live at: Settings → Notifications → *(template)* → **Edit code** → Email body (HTML).

Before you start: click **Send test** to email yourself the current version, so you have a before-copy.
If anything goes wrong there is also a **Revert to default** option on each template.

---

## 1. Order confirmation

### 1a. The headline

**FIND**

```liquid
{% capture email_title %}
  Thank you for your order!
{% endcapture %}
```

**REPLACE WITH**

```liquid
{% capture email_title %}
  Thank you. It's in good hands.
{% endcapture %}
```

### 1b. Add the PEXX paragraphs

Find `{% capture email_body %}`. Immediately **after** that line, insert this block:

```liquid
  <p style="margin:0 0 16px; font-size:15.5px; line-height:1.72; color:#463E36;">
    Your order will be packed and sent from Jaipur within three working days, and we'll write again
    the moment it leaves us.
  </p>
  <p style="margin:0 0 16px; font-size:15.5px; line-height:1.72; color:#463E36;">
    Before it reaches you, it will have passed through a good many hands. Our printers are Chhipas —
    second and third generation, most of them, working the same blocks their fathers worked. The women
    in our workshop print, design, stitch and finish; a great deal of what you'll hold was decided by them.
  </p>
  <p style="margin:0 0 16px; font-size:15.5px; line-height:1.72; color:#463E36;">
    One thing worth knowing in advance: you'll find small irregularities in the print — a motif
    fractionally off, a colour a shade deeper in places. That's the hand. It's how you'll know.
  </p>
```

> Why this placement: `email_body` is what renders under the headline and above the order summary.
> Inserting at the top of the capture puts your words first and leaves every total, address and line item untouched.

### 1c. Subject line

Field: **Email subject** (the plain box above the code editor).

- Currently: `Order {{name}} confirmed`
- Change to: `Thank you — order {{name}} is with us`

---

## 2. Shipping confirmation

### 2a. The headline

**FIND** the `email_title` capture (wording varies — it will be along the lines of "Your order is on the way").

**REPLACE the inner text with:**

```
It's on its way
```

### 2b. Body paragraphs

Immediately after `{% capture email_body %}`, insert:

```liquid
  <p style="margin:0 0 16px; font-size:15.5px; line-height:1.72; color:#463E36;">
    Your parcel left Jaipur and is with {{ fulfillment.tracking_company }}.
    Most arrive within three to five days.
  </p>
  <p style="margin:0 0 16px; font-size:15.5px; line-height:1.72; color:#463E36;">
    If this is a gift and it needs to arrive by a particular day, reply and tell us the date.
    We'll follow it with the courier ourselves and keep you posted.
  </p>
  <p style="margin:0 0 16px; font-size:13.5px; line-height:1.65; color:#6F655B;">
    Paying cash on delivery? Do keep the exact amount ready — it makes the handover easier for everyone.
  </p>
```

`{{ fulfillment.tracking_company }}` prints whichever courier actually carries it — Delhivery, Ekart, anyone
you add later. Never hard-code a courier name.

### 2c. Subject line

- Change to: `On its way to you`

---

## After pasting, both templates

1. **Save**
2. **Send test** — check it in your own inbox, on a phone
3. Confirm the tracking line reads the courier name and not a blank

If the tracking company renders empty in the test, that's only because test data has no fulfilment attached.
Verify on the next real order rather than assuming it's broken.
