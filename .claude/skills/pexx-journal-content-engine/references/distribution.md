# Where a post goes after it is published

Publishing is a quarter of the work. Every post gets the same treatment and it
takes about forty minutes. Everything below was verified on 22 August 2026 —
where a widely-repeated tactic is dead, it says so.

---

## The share card

Each post ships with a **PEXX-branded share card** — the same fonts and colours
as the site, so a screenshot is recognisably ours without hunting for a logo.

Template: `assets/share-card.html`. Fill in five fields, open it at the size you
want, screenshot.

| Size | For |
|---|---|
| 1080×1350 | Instagram, LinkedIn document post |
| 1200×1200 | LinkedIn single image |
| 1200×630 | og:image and WhatsApp link previews |
| **1000×1500** | **Pinterest — strict 2:3, see below** |

Rules: the photo is Tier A or edited Tier B, never a render. The headline is the
reader's question, not a slogan. Nothing on the card that isn't in the post.

**Every share image must be under 600 KB.** WhatsApp silently drops anything
heavier, and WhatsApp is where India actually shares. Check before publishing:

```
magick hero.png -resize 1600x1600\> -strip -quality 80 hero.jpg
```

---

## On-site sharing

Both properties now carry a share row on every article — WhatsApp first, then
LinkedIn, Facebook, Pinterest Save, X, and copy-link. Static site: in
`blog/post.html`, tokens resolved per page by `scripts/build_blog.py`. Shopify:
`snippets/pexx-share-row.liquid`, rendered from `sections/main-blog-post.liquid`.

All share links point at the canonical `/blog/<slug>/`, never the dynamic
viewer, so shares consolidate onto one URL.

---

## Telling the search engines

**Dead advice, still everywhere:** `google.com/ping?sitemap=` now returns 404
and the Bing equivalent returns 410. Google's Indexing API covers job postings
and livestreams only. Ignore any guide that says otherwise.

**Google:** the sitemap is the route. Submit it once in Search Console, then
per-article use Request Indexing — capped at roughly 10–12 URLs a day, which is
plenty at our cadence.

**IndexNow** is set up. The key file is `3bbf3e976bd5fbb4058b2e16593213b3.txt`
at the site root. After publishing, one line:

```
curl "https://api.indexnow.org/indexnow?url=<ARTICLE-URL>&key=3bbf3e976bd5fbb4058b2e16593213b3"
```

That reaches Bing, Yandex, Seznam, Naver, Yep, the Internet Archive and Amazon.
**Not Google.**

---

## The forty minutes, per article

**Publish — 10 min**
1. `python3 scripts/build_blog.py`, then `--check` must print "all blog pages up to date".
2. Confirm every image is under 600 KB.
3. Commit and push. Confirm the article returns 200, not 404.
4. Paste the URL into `developers.facebook.com/tools/debug/` and hit **Scrape
   Again**. Title, description and image must all appear.

**Index — 5 min**
5. Search Console → paste URL → Request Indexing.
6. The IndexNow curl above.

**Distribute — 25 min**
7. **LinkedIn**, from the owner's personal profile, link in the first comment.
   Company page reshares later.
8. **WhatsApp** — Status with the share card, and for bulk posts a short personal
   note to buyers. They reply on WhatsApp and ignore newsletters.
9. **Instagram** — retail posts become a carousel: answer block as slide one, one
   idea per slide, CTA last.
10. **Pinterest** — 2–3 pins from the article's 1000×1500 verticals, real
    descriptions written for search rather than style.
11. **Shopify cross-link** — if the article relates to a product, link it from
    that product page, and back.
12. *Only if it genuinely fits a live thread:* one Reddit comment. Answer the
    question properly; the link is a footnote.

---

## Channels, ranked by what they actually return

**Pinterest — the best channel we have for the shop.** It is a visual search
engine for exactly these categories, and pins keep working for years. Rich Pins
no longer need an application: valid og markup is enough and gets picked up
within about a day (the old Rich Pin validator is dead). The catch is the image
spec — **1000×1500, 2:3, strict**. Our landscape heroes crop badly, so each
article needs a purpose-made vertical. Audience skews US/UK women, which suits
the NRI gift buyer, not the wholesale side. Claim both domains; one domain per
account, so apex and subdomain are separate.

**WhatsApp Channels — twenty minutes, then free forever.** Created in the
WhatsApp Business app (Updates → + → Create channel), not Meta Business Suite.
Nobody discovers a channel by browsing, so it grows only from order
confirmations and the site footer. A re-engagement tool, not acquisition.

**LinkedIn — B2B only, and post an excerpt, never the full article.** LinkedIn
articles are indexed by Google and its domain authority dwarfs ours, but it
gives no canonical field — so a full repost can outrank our own page for our own
writing with no way to fix it. First 30–40%, then link home.

**Reddit — four communities, and most of the obvious ones ban this outright.**

| Sub | Size | Rule |
|---|---|---|
| **r/Gifts** | 337k | Links explicitly encouraged. Best fit for the NRI gift buyer |
| **r/DesiWeddings** | 172k | Has a Vendor Post flair, for vendors who actually participate in comments |
| **r/quilting** | 302k | Sales links go in the bi-weekly Steals & Deals thread |
| **r/IndiaBusiness** | 134k | Promotion by mod approval — worth one message |
| r/IndianHomeDecor, r/smallbusinessindia | — | Comment only, no links, instant ban for violations |

Banned or dead for us: r/IndianParents, r/IndianMoms, r/IndianHomes,
r/blockprinting, r/Handicrafts, r/Entrepreneur, r/smallbusiness. r/IndianExporters
looks perfect and is a graveyard of "DM for rates" posts with zero comments.

**Medium — safe, low value.** Import Story does set the canonical back to us
automatically, confirmed in Medium's own docs, so there is no SEO downside. But
Medium blocks GPTBot, ClaudeBot and PerplexityBot, so it contributes nothing to
AI citation, and its readers are not our buyers. Two minutes if you feel like it.

---

## Skip these — checked, not assumed

- **Flipboard.** Every outbound link is `nofollow`, it blocks AI crawlers, and it
  needs constant curation of other people's posts to stay compliant.
- **Quora.** Not spammy, just bad arithmetic — nofollow links, long answers
  needed to rank, thin question volume in our categories. Only paste an answer
  you had already written anyway.
- **Google Business Profile posts.** The map pin is worth claiming if buyers
  visit the Jaipur workshop; the posts feature sends approximately no traffic.
- **Every Indian trade directory.** Nineteen were checked by counting the actual
  links on live pages. EPCH's member directory contains no website links at all
  (and costs ₹8,850 in year one — worth it for IHGF, not for visibility).
  ExportersIndia's free pages link to their own sales arm. TradeIndia's "success
  story" advertorials link to nobody. IndiaMART's free tier exists to sell you
  the paid tier.
- **Paid article-submission and guest-post networks.** Spam neighbourhoods.
- **Mass Facebook group posting.** Indian parenting groups are strictly
  moderated. Answer questions there as a person, or stay out.

**Two warnings.** Do not register on **indiahandmade.com** — its public seller
pages were exposing other sellers' PAN, GSTIN, bank account numbers and personal
mobiles to anyone who looked. And **fieo.org**'s SSL certificate expired on
17 August 2026; leave it alone until that is fixed.

**Three worth a pitch rather than a submission:** The Voice of Fashion
(thevoiceoffashion.com), Gaatha (gaatha.com) for a Bagru or Sanganer story, and
iTokri — which is a wholesale buyer, not a publisher.

---

## What to check monthly

Three numbers, nothing more:

1. Enquiries or orders that mention a journal post.
2. Whether ChatGPT and Perplexity cite us when asked the questions our posts
   answer — ask by hand, write down who gets cited instead.
3. Which posts precede a sale, from Shopify's own analytics.
