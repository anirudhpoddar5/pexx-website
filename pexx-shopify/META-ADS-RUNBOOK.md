# PEXX — Meta Ads Runbook

**This is the operating manual, not a plan.** It answers "how do I do X" and
"what already went wrong". Strategy documents live elsewhere and go stale:

| Doc | What it is | Trust it? |
|---|---|---|
| `META-ADS-PLAN.md` | Strategy written 11 Aug, pre-launch | Reasoning yes, status no |
| `RAKHI-CAMPAIGN.md` | Build spec for the Aug campaign | Reasoning yes, status no |
| **this file** | How the account actually works | **Yes — keep it current** |

Both plan docs say "nothing is live". That stopped being true on 12 Aug. Never
act on a status line from them.

---

## How the memory system is set up

Three layers, each with exactly one job. Nothing is duplicated between them —
duplication is what causes drift.

1. **Live numbers — automatic.** A SessionStart hook runs
   `scripts/meta_ads.py 7` and prints spend/sales/ROAS per ad at the top of
   every session. Nobody has to ask. Configured in `.claude/settings.json`.
2. **This runbook — the knowledge.** Account IDs, what the API can and can't
   do, standard procedures, and a dated incident log. Lives in the repo so it
   survives sessions and is readable by any agent.
3. **Memory files — the pointers.** `~/.claude/projects/…/memory/` holds
   one-line facts that make a cold session *find* this file. They must stay
   short. If a memory file starts explaining procedure, it belongs here instead.

**The rule:** anything learned the hard way goes in section "Incident log"
below, same day, with the root cause. Anything that is just today's numbers
goes nowhere — the hook re-derives it.

---

## Account facts (never re-derive these)

| Thing | Value |
|---|---|
| Ad account | `act_1350379969884972` |
| Ads Manager URL shows | `act=327847014459823` — **a different, dead account** |
| Pixel | `1952609352110587` (PEXX's pixel, incl. server-side CAPI) |
| Business | `1752269172473486` |
| Facebook Page | `1277364825452418` |
| Instagram user | `17841408830237947` |
| API app | "PEXX Automation" `1030605322786878` — **LIVE since 21 Aug 2026** (creative API unblocked) |
| Token | `pexx-shopify/.meta-token`, gitignored, never expires |
| Scopes | ads_read, ads_management, business_management |

The account-id trap is the expensive one: reading the URL's account shows 76
old/off campaigns and zero live spend, i.e. a completely false "nothing is
running" picture.

---

## What the API can and cannot do

| Action | API? | Notes |
|---|---|---|
| Read insights, targeting, issues | ✅ | `scripts/meta_ads.py` |
| Turn ads/ad sets/campaigns on/off | ✅ | `POST {id}` with `status=` |
| Change budgets | ✅ | |
| Create an ad creative | ✅ | **Unblocked 21 Aug 2026** — app published to Live mode. Was error_subcode 1885183 |
| Upload ad images | ✅ | `POST {ACT}/adimages` with `-F "filename=@path.jpg"` → returns `hash` for use in `image_hash` |
| Change conversion event on a published ad set | ❌ | error_subcode **3260011** — Meta forbids this in the API *and* the UI |
| See billing / payment state | ❌ | **Not exposed anywhere in the Ads API.** `account_status: 1` and `disable_reason: 0` stay clean while unpaid billing silently halts delivery. Must be read in Business Suite → Billing & payments |
| Check an ad's backing post is alive | ❌ | Token is a SYSTEM_USER without `pages_read_engagement`. Reading `effective_object_story_id` returns `(#100) Missing permissions`. **That 400 is a scope limit, not a broken post** — do not diagnose from it |

**Consequence — the two rules that decide your route:**

- Anything that **mints a new Facebook/Instagram post** → must be Ads Manager.
- Anything that **changes an ad set's pixel, conversion event or optimisation**
  → impossible to edit; you must **duplicate the ad set**.

Duplicating conveniently does both at once, which is why it is the answer to
most problems here.

DONE 21 Aug 2026 — "PEXX Automation" is published/Live. Creating ad creatives
and uploading images via the API both work now. The two rules above about
needing Ads Manager no longer apply to creative; they still apply to changing
an ad set's conversion event.

---

## Standard procedures

### A. Read the numbers
```bash
cd ~/Downloads/pexx-website && python3 pexx-shopify/scripts/meta_ads.py 7
```
The trailing number is days. **Always includes today** — the script uses an
explicit `time_range` because Meta's `last_7d` preset excludes today and once
hid the only purchase in the account.

### B. Fix "Delivery error → Ad creative is incomplete" (error 2446289)
Symptom: *"The reel you've selected for your ad is not available."* The
Instagram/Page post behind the creative was deleted or lost.

Fix: **duplicate the ad** (or its whole ad set) in Ads Manager and publish. The
duplicate mints a fresh post, which is the entire repair. Copy, images and
targeting all carry over — nothing needs rewriting.

### C. Change conversion event, targeting, or optimisation
Cannot be edited. Duplicate the ad set, change the setting in the draft, publish,
then pause the original. Learning resets — at this spend level that costs nothing.

### D. After ANY duplicate — check the toggles
Duplicated ads **inherit the on/off state of the original**. If the source ads
were switched off, the copies arrive approved and silently idle. This has
already cost real hours. Verify:
```bash
python3 -c "
import sys; sys.path.insert(0,'pexx-shopify/scripts')
import meta_ads as m
for a in m.get(f'{m.ACT}/ads', fields='name,status,effective_status,adset{name}', limit=100)['data']:
    print(a['adset']['name'][:30], a['name'][:34], a['status'], a['effective_status'])
"
```

### E. Verify targeting — never trust the ad set name
Names on this account have been actively wrong. Always dump the real spec and
check `user_os`, `genders`, `age_max`, `geo_locations`:
```bash
python3 -c "
import sys; sys.path.insert(0,'pexx-shopify/scripts')
import meta_ads as m, json
for s in m.get(f'{m.ACT}/adsets', fields='name,effective_status,promoted_object,targeting', limit=50)['data']:
    t=s['targeting']
    print(s['name'], s['effective_status'], 'os=',t.get('user_os','ALL'), 'gender=',t.get('genders','ALL'), 'age=',t.get('age_min'),'-',t.get('age_max'))
"
```

---

## Pre-publish checklist

Run through this before publishing any ad set. Every item is here because it
has already failed at least once.

- [ ] Real targeting dumped from the API, not read off the name
- [ ] `user_os` is absent (all devices) unless a device test is the deliberate point
- [ ] Conversion event has **≥ ~50 events/week** of real volume, or Meta cannot train
- [ ] Every link carries UTMs (`utm_source=meta&utm_medium=paid&utm_campaign=…&utm_content=<product>`)
- [ ] After publishing: confirm each ad is `ACTIVE`, not inherited-off
- [ ] After publishing: confirm `issues_info` is empty on every ad
- [ ] Old/replaced ad set paused so budget concentrates

---

## Incident log

### 23 Aug 2026 (late) — geo narrowed to 12 cities. THE live test.

**Why.** A region breakdown of the 22-23 Aug campaign showed delivery badly
skewed away from likely buyers: 76% of impressions outside the metros, **Delhi
got 206 of 16,385 impressions (1.3%)**, while Punjab alone took 2,566 (almost
all quilt). Nothing in the setup told Meta to prefer purchasing power, so it
bought the cheapest inventory in India for a Rs999-Rs1,199 premium product.

**Honest limit on the evidence:** CTR in metro states (1.80%) vs rest (1.91%) is
effectively identical, so the click data does NOT prove the cheap traffic was
worse. Meta recorded zero add-to-cart and zero purchase by region at this
volume, so the deciding number does not exist. This change rests on first
principles, not on a proven regional conversion gap. **Judge it on what happens
next, and say so.**

**Applied to all four PT ad sets** (owner approved, women-only confirmed):
Delhi, Gurugram, Noida, Faridabad, Mumbai, Pune, Bangalore, Hyderabad, Kolkata,
Ahmedabad, Chandigarh, Indore. Owner dropped Chennai and Jaipur from the
proposed list and added Indore and Faridabad.

Audience 102M -> **31M**. Budget unchanged at Rs900/day.

**Measured cost of this move, from the account's own 22-23 Aug data** - states
containing these cities vs everywhere else:

| | CPM | CPC | CTR |
|---|---|---|---|
| The 12-city states | Rs111 | Rs5.30 | 2.11% |
| Rest of India | Rs76 | Rs4.40 | 1.72% |

Views cost ~45% more, **clicks only ~20% more**, because those users click a
third more often. That is the trade being made.

**Affluence layer deliberately NOT stacked.** "Mid & high-value goods" on top
would cut 31M -> **1.0M** (high-value alone: 0.43M) - a further 30x, into the
same territory that produced Rs19-21 CPCs in August. One variable at a time: if
this fails with both applied, you cannot tell which one broke it. Add affluence
as a clean second test only if cities alone works.

**Learning resets on all four ad sets.** Accepted; swaddle had 2 days banked.

### 23 Aug 2026 — competitor pricing kills the "too expensive" theory

kapaaskatha.in (note the double 'a' — kapaskatha.com is a parked lander).
Pulled via `/collections/<c>/products.json`. Owner flagged them for the two
categories whose ads underperform.

| | PEXX | Kapaaskatha |
|---|---|---|
| Kids backpacks | **₹999** (6 SKUs) | ₹1,250-1,590 (19 SKUs) |
| Pouches — single | **none** | ₹325-₹550 (dozens) |
| Pouches — set of 3 | **₹1,199** | ₹699-₹1,250 |

**Backpacks: PEXX is 20-37% CHEAPER than the competitor and still not selling.**
That rules out price as the cause and leaves creative — consistent with the
same-audience/3x-CPC comparison above.

**Pouches — the "PEXX is overpriced" reading is WRONG. Owner's correction:**
the 3-piece sets sell on FirstCry and on Kapaaskatha at *higher* prices than
ours, and they are **the same product — PEXX manufactures them for those
sellers.** So ₹1,199 is not the barrier; the identical item moves at more than
that through channels with existing trust and traffic.

What that leaves: the pouch problem is **brand trust and channel, not price.**
A stranger buys the ₹1,199 set on FirstCry and not from a cold Meta ad for a
brand they have never heard of. Do not treat this as a pricing or catalogue
defect.

A single pouch around ₹450-₹550 may still be worth having as an entry SKU, but
it is **no longer justified as a fix for the ads** — see the owner's correction
above.

**It is a decision, not a to-do, and it is the owner's alone.** Against it: a
₹375-₹550 single sits directly under the ₹1,199 set and could cannibalise it,
and PEXX's position is no-discounting and above mass-market. For it: return
gifts for kids' parties are a core use case, start at ten pieces, and a single
pouch is exactly that product. Verified alongside: every buyable PEXX pouch is
a ₹1,199 three-piece set, ten of them, no single. The ₹399 "Gift Pouch — Free
over ₹1,999" is the gift-wrap add-on, not a standalone SKU, so it does not fill
the gap. **Do not create SKUs off a competitor scrape.**

Also noted: the competitor leans on licensed characters (Cocomelon, Peppa Pig,
Chhota Bheem) and heavy strikethrough discounting on pouches. Neither is a route
PEXX should copy — flagged only so their traffic numbers aren't read as
like-for-like.

### 23 Aug 2026 (afternoon) — two sessions were editing the account at once

**Root cause of a confusing hour.** `PT_backpack` flipped to IN_PROCESS minutes
after my own targeting edit. It was not Meta re-review — a peer session was
editing the same ad account concurrently: it had removed `genders` from all
four ad sets, stripped `family_statuses` off backpack/pouch/swaddle, and
reactivated backpack + pouch. My women-only edit landed in the middle of that.

**Owner's ruling:** one session owns the ad account. Kapaskatha research went to
the peer. Ads consolidated here.

**Conflicting instruction, unresolved at time of writing.** The owner told the
peer session *"no dont restrict to woman only i think"*; he later told this
session *"women - agree"*. Women-only is currently APPLIED to swaddle and quilt
and has been flagged back to him. **Do not silently reverse it on a second-hand
relay** — get it from the owner.

**Lesson:** `ListAgents` + `SendMessage` before touching the account. The API
gives no hint that another agent is writing, and `updated_time` on an ad set
is the only tell.

### 23 Aug 2026 — household income targeting does NOT exist for India

Checked directly against this account via `{ACT}/targetingsearch`, not blogs.
Several 2026 posts claim "Meta launches Household Income targeting in India".
**False for this account.** The `income` type returns US ZIP-code brackets only.

Real affluence proxies that DO exist for India:

| Proxy | ID | Reach |
|---|---|---|
| People in India who prefer **high-value goods** | `6028974370383` | 87.6M |
| People in India who prefer mid- and high-value goods | `6028974351183` | 135M |
| Frequent international travellers | `6022788483583` | — |
| Engaged shoppers | `6071631541183` | — |

Plus two that cost nothing: **locale = English** (a sharp income proxy in India)
and **putting the price in the ad copy**, which self-selects harder than any
targeting setting.

### 23 Aug 2026 — backpack/pouch CPC was a CREATIVE fault, not a targeting one

Do not repeat the 23 Aug morning conclusion that these categories "don't convert
on cold Meta". The controlled comparison says otherwise:

`PT_quilt`, `PT_backpack` and `PT_pouch` ran the **same** campaign, age band,
placements and family segments. Quilt clicked at **₹3.30**; backpack **₹11.00**,
pouch **₹10.10**. Same audience, 3x the click price — that is the creative
failing to stop the scroll.

**Caveat, stated so this is not over-claimed:** backpack only ever accumulated
27 clicks and pouch 36. "Creative isn't stopping the scroll" is the better
hypothesis than audience size — it survives the same-audience comparison and the
competitor-price check — but it is not proven at that volume. Treat it as the
working theory to test, not a settled finding.

**RETRACTED — the eyebrow bug does NOT explain the CPC gap.** It was briefly
recorded here that a text-slicing bug in `scripts/make_ad_creative.py` `fit()`
had shipped on the live backpack ad. **That was never true.** Verified against
the delivered files: all four 21 Aug eyebrows render fully (`HAND BLOCK-PRINTED`,
`THREE SIZES, ONE PRICE`, `HAND BLOCK-PRINTED`, `PURE COTTON MUSLIN`), and an
edge-column luminance sample across all 20 delivered JPEGs found no ink touching
a frame edge. Evidence: `~/Desktop/PEXX/ads/_qa/live-21aug-eyebrows-INTACT.png`.
Backpack and pouch are as clean as quilt, so identical creative health with
3x the CPC **rules the hypothesis out rather than supporting it.**

**The bug is real but irrelevant here** — it only bites above ~20 characters, and
every 21 Aug eyebrow was shorter. Keep the `fit()` fix on its own merits
(before/after: `~/Desktop/PEXX/ads/_qa/bug-before-after.png`). Never cite it to
explain performance.

**Where the gap actually sits: CTR, not CPC.** Quilt ~6-7% against backpack
~2.9%; in the PT carousels, quilt 2.04% against backpack 1.23%. That is upstream
of the click, the landing page, and anything in the file's lower half — it is
whether the image earns attention in feed. Category demand on cold traffic is the
more boring explanation and fits the numbers better than any defect.

**Also:** the owner reports these same SKUs sell well to bulk buyers. The
product has demand. Rebuild the creative before writing the category off.

### 23 Aug 2026 — storefront changed mid-flight; a measurement boundary

Peer sessions shipped these to the live store **today**, so any before/after
comparison across 23 Aug is confounded:

- PDP gallery images lazy-loaded — **~447KB less per product view** (592KB → 145KB
  of image bytes). Paid traffic lands on PDPs, so expect bounce/TTI to improve
  for reasons unrelated to the ads.
- **Gift-wrap was broken until today — but not the way first logged.** Two
  render sites, two different faults. On the **full /cart page** ticking worked
  and un-ticking failed, so a shopper really could get stuck with an unwanted
  ₹99. In the **cart drawer** — where most ad traffic lands, since it opens on
  add-to-cart without a page change — there was no listener at all: the checkbox
  did nothing. A dead control, not a surprise charge. Friction and a trust hit
  at the moment of checkout intent, but do not describe it as a stuck-charge
  leak. (Drawer branch is well-reasoned from the code, not observed; the
  pre-fix behaviour is now untestable.) **All abandonment data before 23 Aug
  carries this contaminant**, and the fix landing mid-campaign means
  post-23-Aug add-to-cart-to-checkout measures a different funnel.
- BreadcrumbList JSON-LD on PDPs; Organization schema url fixed.

**Still unfixed:** collection pages load 17-25 eager images. Irrelevant while
ads land on product pages — **but if paid traffic is ever pointed back at a
collection, fix that first.**


### 23 Aug 2026 — FIRST ATTRIBUTED SALE. Product-page landing works.

**Order #1019, ₹999, Unicorn & Dolphin Swaddle Set.** Verified independently in
Shopify — not just Meta's pixel. Landing site:
`/products/unicorn-dolphin-swaddle-set?utm_source=meta&utm_medium=paid&utm_campaign=producttest`,
referrer facebook.com. Meta reports 3.76x ROAS on that ad set.

**This is the first sale ever traceable to a campaign built here, and it
validates the single biggest fix:** every previous campaign dumped paid traffic
on a 15-product collection page. This one lands on the exact product shown in
the card. The buyer landed on the product page and bought that product.

**Two-day per-product read (the point of the 4-way split):**

| Ad set | CPC | Clicks | ATC | Sales |
|---|---|---|---|---|
| **Swaddle** | **₹3.6–4.9** | 73 | 1 | **1 (₹999)** |
| Quilt | ₹3.3–3.8 | 167 | 1 | 0 |
| Pouch | ₹10 → **₹19** | 36 | 0 | 0 |
| Backpack | ₹10.9 → **₹20.7** | 27 | 0 | 0 |

**Action taken 23 Aug:** paused `PT_pouch` and `PT_backpack`; doubled
`PT_swaddle` ₹150 → ₹300. Quilt held at ₹300. New total ₹600/day (was ₹750).

**Why pausing at 2 days did not break the "judge nothing on one day" rule:**
pouch and backpack CPC is 4-5x the winners' and *rising*, they produced 14
clicks for ₹275 on the final day, and this repeats the clean 18 Aug result
where the same two categories got real CTR and zero purchases. Three
independent windows now say the same thing: **these two do not convert on cold
Meta traffic.** That is a finding, not noise. Retarget or Google Shopping for
them — not cold prospecting.

**Note on the budget increase:** ₹150→₹300 is +100% and will reset the
swaddle ad set's learning. Accepted deliberately — it had only ~₹266 lifetime
spend, so almost no learning was banked, and budget on the only converter
matters more than protecting a barely-started learning phase.


### 21 Aug 2026 — the Rakhi campaign never actually stopped, and is still spending on expired copy
**Found while reviewing performance for a new campaign push.** `stop_time` on
`PEXX_Sales_Rakhi_Metros_Aug2026` is `2026-08-19T09:00:00+0530` — two days in the
past — but `effective_status` is still `ACTIVE` and it spent ₹348 in the 3 days
since (280 clicks, 0 purchases). Meta's `stop_time` did not auto-pause it. The
only live ad is `03_Quilt_SoftestThingInTheHouse`; Backpack/Pouch/Swaddle stayed
correctly paused from the 18 Aug decision.

**Consequence:** the ad's own headline/body promise ("Order by 18 August") is
now false to anyone clicking it — money is being spent sending clicks to a
broken promise, not just a stale one.

**Fixed 21 Aug 2026** — campaign paused via direct API call (`status=PAUSED`
on the campaign object; confirmed `effective_status: PAUSED`). Account is now
a clean slate — zero active campaigns. Next: stand up the "Next campaign —
build spec" below, being rebuilt post-Rakhi with real market research (see
same-day session).

**Lesson:** `stop_time` on a campaign is not a safety net. Check
`effective_status` + actual recent spend directly, never assume a past
stop_time means delivery halted.

### 18 Aug 2026 — the site was fighting the ads. Two mobile CTA bugs, plus billing again

**Delivery: ZERO all day** by 12:15 IST on the campaign's *deadline day*, with
**₹220.38 outstanding** and funding back on Mastercard \*7858 (the ₹1,000 prepaid
credit from 15 Aug is drawn down). Same signature as the 15 Aug incident. The API
says `account_status: 1`, `disable_reason: 0` — as always, it cannot see this.

**Two real conversion bugs found on the storefront, both mobile-only, both fixed
and verified in real Chromium at 375×812:**

1. **The WhatsApp FAB covered the Add to cart button.** Measured at the landing
   scroll position of every product page: the inline Add to cart is 211px wide and
   the FAB (`z-index: 9998`) covered **25% of it, with 44px of vertical overlap**.
   The existing `body:has(.sticky-add-to-cart__bar[data-stuck='true'])` lift only
   ever addressed the *sticky* bar, never the inline button.
   *Fix:* `snippets/pexx-whatsapp.liquid` — an IntersectionObserver hides the FAB
   whenever any `.add-to-cart-button` / `.shopify-payment-button__button` is on
   screen. Verified: hidden at top, returns when scrolled past the buy zone.
2. **The 15%-off popup walled the paid landing page.** It opened 4.5s after load
   on *every* page, sitewide — so every Meta visitor hit a full-screen modal on
   the collection page they were paying to reach.
   *Fix:* `snippets/pexx-popup.liquid` — never opens on the first pageview of a
   session, and never on a product page. Verified all three cases: landing
   suppressed, PDP suppressed, still fires on a later non-product page (so email
   capture is intact).

**Note:** Shopify's origin `page_cache` serves stale HTML for a while after a
theme push, and query-string cache-busting does not defeat it. `curl` the
storefront and grep for a token from the new code — that is the reliable check.
This is the same cache behaviour seen on the mega-menu fix.

**Targeting truths from the full 12–18 Aug window** (account-level breakdowns —
these are the most useful numbers the campaign produced):

| Split | Spend | ATC | Purchases |
|---|---|---|---|
| **iPhone** | ₹1,122 | **25** | **2** |
| Android | ₹1,240 | 8 | 0 |
| **25–34 female** | ₹822 | **14** | **2** |
| 35–44 female | ₹373 | 5 | 0 |
| 18–24 female | ₹264 | **0** | 0 |
| 55+ / most male | ~₹460 | 1 | 0 |

**This partly reverses the 15 Aug conclusion.** `user_os: ["iOS"]` was recorded
as a pure bug because it throttled reach. On conversion it was not: iPhone
delivered **3.4× the add-to-carts per rupee** and every purchase. For a ₹1,299
gifting product in India, iOS skew is an income proxy, not a mistake. Reach was
the real cost — so the successor should *bid toward* iOS, not restrict to it.

**The optimisation-event swap was the bigger error.** Old ad set
(INITIATED_CHECKOUT): 188 clicks → 20 ATC = **15%**. New ad set (CONTENT_VIEW):
1,472 clicks → 5 ATC = **1.1%**. Switching to CONTENT_VIEW because it had more
events was textbook-correct and cost the conversions — Meta optimises for exactly
what you ask for, and content-viewers are not buyers. ADD_TO_CART is the middle
ground and was already the deferred right call on 17 Aug.

**Ad-level action taken:** paused `01_Backpack`, `02_PouchSet`, `04_Swaddle` in
the live ad set (₹630 combined, 9 ATC, **0 purchases**). `03_Quilt` left running
alone — it is the only ad with demonstrated purchase intent.

**Not done, deliberately:** no targeting or budget edit to the live ad set. It
auto-ends 19 Aug 09:00; an edit restarts learning for a window too short to
recover it. The creative's headline and body both say *"Order by 18 August"*, so
the campaign also cannot simply be extended — that would sell a dead promise.

### 17 Aug 2026 — delivery fixed, but the traffic was junk. Reels ate half the budget

**Symptom:** owner reported "lots of Instagram followers, no orders". Correct
diagnosis of his own campaign.

**The numbers:** after switching to CONTENT_VIEW + Advantage+ placements,
clicks went up ~9x while add-to-carts went *down*. Add-to-cart among
product-viewers fell from ~15% (12–14 Aug) to 2.6% (16 Aug) to 0% (17 Aug).

**Root cause — placement, not audience.** Advantage+ placements poured 52% of
spend into **Instagram Reels** (₹790, 29,598 impressions, ₹27 CPM, **5**
add-to-carts). Reels is entertainment inventory: cheap clicks, people bounce,
some follow the profile. Instagram Feed converted to add-to-cart at ~2x Reels
on 40% less money.

**Fix:** restricted placements in place to `instagram: stream, story` +
`facebook: feed`. **Placements ARE editable on a live ad set** — unlike the
conversion event. No duplicate needed, no structural reset.

**Deliberately NOT done:** switching CONTENT_VIEW → ADD_TO_CART. It is the right
call, but it needs a new ad set, and this campaign had ~36h left (Rakhi copy
expires 18 Aug, campaign auto-ends 19 Aug 09:00). A third learning reset in the
final 36 hours would guarantee instability. Deferred to the next build.

**Also found, unfixed:** every ad links to a *collection* (quilts has 15
products) while the creative shows one product. ~2/3 of landing-page visitors
never trigger view_content. Likely the single biggest conversion leak — but the
link cannot be changed without a new creative, which the Development-mode app
blocks. **Fix in the next campaign: land on the product page.**

**Attribution reality check:** the 2 purchases Meta claimed across 12–17 Aug
were the *same customer* (an order and her re-order after Shopify Flow
auto-cancelled the first). The campaign acquired **one** buyer for ~₹2,200. The
store's largest order (#1017, ₹2,208) was not Meta-attributed at all.


### 15 Aug 2026 (evening) — zero delivery all day. Cause was billing, not ads

**Symptom:** the freshly rebuilt ad set launched 13:44 and delivered **nothing**
for over four hours. Zero spend, zero impressions. Lifetime spend sat at
₹999.22, unchanged across three separate readings.

**Everything in the Ads API looked perfect** — and that is the trap:

- campaign, ad set and all 4 ads `effective_status: ACTIVE`, `issues_info: none`
- audience 101–119M, no `user_os` flag, no dayparting, no spend cap
- `account_status: 1`, `disable_reason: 0`

**Root cause:** the ₹363.44 charge from 14 Aug was stuck on **Pending**. Meta
had quietly stopped delivery pending payment. The 12 Aug charge (₹230.10)
cleared and ads ran that day — the delivery record maps 1:1 onto the payment
record.

Lifetime spend was only ~₹1,000, so Meta's billing threshold is tiny. The
account bills every couple of days, which is many chances for a charge to stick.

**Fix:** owner settled the outstanding ₹121.10 and added **₹1,000 as prepaid
credit** — it books as status **`Funded`**, not `Paid`. Balance went ₹102.63 →
₹0.00 and the "Pay Now" button disappeared. **Delivery resumed at 19:43**, about
1h28m later, starting with the Quilt ad.

**Lessons:**
1. **Check billing before anything else when spend is zero.** It is invisible to
   the API (see the capability table above). Four separate API checks all said
   "healthy" while the real cause sat in a screen the API cannot reach.
2. **Prepaid `Funded` credit is the durable fix**, not repeated card payments.
   Drawing down a balance removes the per-threshold charge that can fail.
3. **Never re-add or re-verify the card while a payment is processing** — Meta's
   own on-screen warning says it will make that payment fail.
4. A 400 on a creative's post ID means *missing token scope*, not a dead post.
   Nearly misdiagnosed this as a repeat of the morning's vanished-post bug.

**This is the fourth failure in a row that was plumbing, not creative.**

### 15 Aug 2026 — three of four ads dead, account spending 10% of budget
**Symptom:** "Delivery error" on Quilt, Swaddle, Backpack. Spend ₹596 against a
₹5,950 weekly budget. Zero delivery on 11, 13 and 15 Aug.

**Three separate root causes, found in this order:**

1. **Creative posts vanished** (error 2446289) — killed 3 ads including the only
   profitable one. *Fix:* duplicate → fresh posts.
2. **The ad set was iOS-only.** `Metros_25plus_Broad_InitiateCheckout` was not
   Metros (all India), not 25plus (capped 44), and not Broad — women only, 4
   interests, **and `user_os: ["iOS"]`**, almost certainly leaked from the
   sibling ad set named `iOSonly`. In India that is a small minority of phones.
   This, not the creative error, was the real reason budget went unspent. No
   Ads Manager summary screen shows an OS restriction.
3. **Optimising for a 6-event signal.** Ad set targeted `INITIATED_CHECKOUT`:
   6 events/week. `VIEW_CONTENT` had 156 in the same window. Far too sparse to
   train delivery on.

**Fix shipped:** new ad set `AllIndia_25to44_AllDevices_ViewContent` —
CONTENT_VIEW, all devices, Advantage+ audience and placements on, 4 rebuilt ads,
UTMs normalised across all links. Old ad sets paused.

**Then it went wrong again:** the 4 rebuilt ads cleared review but 3 sat
**switched off**, having inherited the OFF toggle from the originals. Reported
as launched when they were idle. → became procedure D above.

**Lessons now encoded:** verify targeting via API (E); check toggles after any
duplicate (D); check the conversion event has volume before optimising for it.

---

## What is actually working — don't re-litigate these

- **The pixel is live and correct**, including server-side CAPI. Grep of the
  theme gives false negatives; it is installed via the Facebook & Instagram app.
  Stop re-checking this.
- **The creative and copy have never been the problem.** Every failure so far
  has been plumbing — accounts, posts, toggles, targeting flags.
- **The Quilt ad works.** ₹407 → ₹1,203, 2.96x ROAS, 12.2% CTR. On a
  ~₹600 total sample, so it is a signal, not a proof.
- **CTRs are strong across the board** (7–19%). People want the product; the
  constraint has been delivery, not appeal.

---

## Decision rules

- **Price ceiling ₹1,299.** Budget ₹10–15k/month.
- **Judge nothing on one day.** At ₹850/day a single day is ~40 clicks.
- **Before blaming creative, check delivery first** — spend actually spent vs
  budget. Three times out of three so far, the problem was plumbing.
- **A campaign that stops spending is a bug, not a market signal.**

---

## Next campaign — build spec (written 18 Aug from real numbers)

The Rakhi campaign ends 19 Aug 09:00 and nothing is queued. Everything below is
decided by the 12–18 Aug data, not by theory. Steps marked **AM** must be done in
Ads Manager because the app is still in Development mode.

**Structure**
- One campaign, OUTCOME_SALES, one ad set. Do not split by product — at
  ₹850/day there is not enough volume to learn on two.
- Optimise for **ADD_TO_CART**, not CONTENT_VIEW and not INITIATED_CHECKOUT.
  Content-viewers converted at 1.1%; checkout-optimised converted at 15% but on
  a 6-event/week signal. ATC is the only event with both volume and intent.
- **AM** — new ad set, since the conversion event cannot be changed in place.

**Targeting**
- Women **25–44**. Cut 18–24 (₹264, 0 ATC) and 55+ outright — Advantage+
  expansion spent there and returned nothing.
- All devices, **no `user_os` restriction**, but expect and accept an iOS skew:
  iPhone delivered 3.4× the ATCs per rupee and every purchase.
- Placements: Instagram feed + stories + reels, Facebook feed. Exclude
  **Audience Network** (₹85 → 2 view-contents, zero everything else).

**Creative — the two changes that matter most**
1. **Land on the product page, not the collection.** Every ad so far pointed at
   a collection of 15 quilts while the image showed one. This has been the
   standing top suspect for the funnel drop and it is still unfixed.
2. **Lead with the Quilt.** It is the only product that has ever sold from an
   ad. Backpack, pouch and swaddle have spent ₹630 lifetime for zero purchases —
   hold them until the quilt is profitable.
3. Every link needs UTMs. Right now **only the Backpack ad has them** — quilt,
   pouch and swaddle links are bare, so GA4/PostHog cannot see paid sessions at
   all. Fix on every new creative.

**Do not repeat**
- No Rakhi/date language unless the campaign is scheduled to end before it.
  Dated copy is why this campaign cannot simply be extended.
- Check Business Suite → Billing before concluding anything from low spend.

---

## Next campaign v2 — evergreen, post-Rakhi (written 21 Aug from Meta Ad
Library research + Shopify analytics, Rakhi campaign now paused)

Rakhi is over. Everything below replaces the 18 Aug spec above — same
structural rules (ADD_TO_CART, women 25–44, no OS lock, exclude Audience
Network) but a different theme and creative, chosen from real market
research, not the Rakhi calendar.

**Theme: newborn / baby-shower gifting on the Quilt — evergreen, not a
festival.** Reasoning: (1) back-to-school is NOT a live buying moment in
India in Aug–Nov — the CBSE year runs Apr–Mar, that spike is long over, so
backpack ads have no seasonal tailwind right now; (2) the only ad in this
exact niche proven to run 12+ months (Raamaé, personalised baby quilts since
Apr 2025) sells this exact framing; (3) an evergreen angle survives a
₹350–850/day budget without the learning-reset cost every dated campaign has
paid so far; (4) festival creative (Diwali ~8 Nov) can swap onto the *same*
ad set later without a new campaign or learning reset.

**Landing page:** the single Quilt PDP the ad's image matches. Never a
collection page — this is the same funnel leak identified 17/18 Aug, still
unfixed, and this week's Shopify analytics confirm it again: 2,285 sessions
→ only 0.17% completed an order.

**Creative angles — none of these are used by the two closest competitors
(Raamaé, Kari by Kriti), both priced 2–3x PEXX:**
1. **Price as the headline claim.** "A real hand block-print quilt for the
   new baby — ₹1,299, not ₹2,600." Neither competitor advertises a number.
2. **Dye/mouth safety, stated explicitly** — "safe to chew" is already the
   brand tagline; no competitor ad makes a dye-safety claim. **Do not ship
   this without confirming the azo-free/dye-safety claim is actually
   substantiable** — owner to confirm before it goes live.
3. **COD as a headline, not fine print.** Kari explicitly excludes COD on
   its personalised gifting line; PEXX offers COD on everything.
4. **Format:** 15–30s vertical video — every sustained competitor ad found
   was video; static-only ads in this space were older/retired catalogue
   units.

**Backpack/pouch category — do not run cold ads for this again, it already
failed once (18 Aug: ₹352, 471 clicks, 0 purchases).** Real FirstCry demand
exists but PEXX's own site sells it as two separate SKUs on two collection
pages, which a cold scroller won't self-assemble. Fix before any spend:
1. Build one new bundle SKU ("The Little Traveller Set" — backpack + matching
   3-piece pouch set, ~₹1,699 vs ₹2,198 apart), 2–3 print options max, only in
   prints where both halves are actually in stock (3 of 16 current SKUs are
   sold out).
2. Land only on that product's own page.
3. Spend only on **warm traffic** for this category — retarget the Rakhi
   campaign's own visitors/ATC-non-purchasers, plus Google Shopping (closer to
   FirstCry's intent-driven traffic than a cold Meta interrupt). Not cold Meta
   prospecting.
4. Watch add-to-cart rate on that PDP alone, target ≥8% (site-wide is
   currently 1%). Under 3% after ~150 sessions → kill it, it's the product/
   price, not the funnel.

**Open items before launch:** confirm real monthly budget (owner's original
decision was ₹10–15k/month; the Rakhi campaign actually ran at ₹850/day ≈
₹25k/month — these don't match, needs a conscious re-decision, not a default);
verify the dye-safety claim; check FirstCry's actual review count/rating
before using any "best-seller" language in the bundle creative.

---

## Open threads

- **App in Development mode** — blocks all creative automation. Flip to Live?
- **Budget** — ₹850/day held as-is on 15 Aug; owner reviewing 16 Aug.
- **New ad set reports age 18–65, name says `25to44`** (checked via API 15 Aug
  15:11). May just be Advantage+ audience expansion rather than a repeat of the
  old targeting bug — **unverified either way**. Worth one look before the next
  duplicate, given lesson (E). Do not edit the live ad set to "fix" it: it was
  born 13:44 on 15 Aug and an edit restarts learning.
- **Campaign auto-stops 19 Aug 09:00.** The 15 Aug decision was to leave the gap
  and rebuild on real numbers. Those numbers now exist — see "Next campaign"
  above. Rakhi itself is **28 Aug**, so a non-dated evergreen campaign still has
  a run-up worth using; a dated one does not, the copy is already spent.
- **Billing keeps halting delivery** (15 Aug, 18 Aug). Prepaid `Funded` credit is
  the durable fix, and it has now been drawn down twice. Worth a standing top-up
  rather than discovering it again on a deadline day.
- **Shipping / free-shipping threshold** — a long separate discussion in the
  "Order shipping charge discrepancy" session (1,400+ messages, still running as
  of 15 Aug). **Not summarised here** — that session owns it and had not
  finished. Shipping charges affect ad conversion directly, so its conclusions
  belong in this repo when it lands.
