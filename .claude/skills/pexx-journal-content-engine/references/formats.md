# Output formats, field by field

Drafts go to `content-drafts/journal/<YYYY-MM-DD>/`. Publishing is a separate,
approved step.

---

## 1. Bulk post — poddarexp.com

The site is a static GitHub Pages build. A post is **three files that must stay
in sync**, which is why `scripts/new_bulk_post.py` exists — never hand-edit
`data/posts.json`.

- `posts/<slug>.html` — the article body only. No `<html>`, `<head>` or `<body>`;
  the shell is `blog/post.html`, which injects it. Allowed tags: `<p>`, `<h2>`,
  `<h3>`, `<ul>/<li>`, `<ol>/<li>`, `<table>`, `<figure><img><figcaption>`,
  `<em>`, `<strong>`, `<blockquote>`. Images use absolute paths
  (`/assets/blog/<slug>/<file>.jpg`) and `loading="lazy"`.
- `data/posts.json` — newest first. Entry shape, all fields required except
  where noted:

```json
{
  "id": "same-as-slug",
  "slug": "kebab-case-slug",
  "title": "Sentence-case title as displayed",
  "seoTitle": "Title with the query first, ~60 chars | PEXX Journal",
  "date": "2026-08-25",
  "readTime": "7 min read",
  "excerpt": "One or two sentences, italicised at the top of the post.",
  "metaDescription": "Under 160 chars, contains the target query.",
  "image": "/assets/blog/<slug>/hero.jpg",
  "imageAlt": "Literal description of the photograph.",
  "file": "/posts/<slug>.html",
  "category": "Sourcing | Trends | Craft",
  "keywords": "space separated, no commas, real search phrases",
  "faq": [{ "question": "...", "answer": "..." }]
}
```

  `category` also drives the "related posts" strip — posts only relate to
  others in the same category, so don't invent a new one for a single post.
  `faq` is technically optional and must never be omitted: it is what becomes
  FAQPage structured data.

- `blog/<slug>/index.html` — the pretty-URL shell: canonical, og tags, and a
  meta-refresh to `../post.html?slug=<slug>`.

**Known weakness, worth fixing before this scales:** the pretty URL is an empty
page that bounces to a JavaScript-rendered article. Google copes; several AI
crawlers do not run JavaScript and see nothing. The fix is to render the article
body into `blog/<slug>/index.html` itself. Until that happens, expect the AEO
work to underperform on non-Google engines.

Images: `assets/blog/<slug>/`, exported per `references/images.md`.

## 2. Retail post — shop.poddarexp.com

**The store is live and takes SEO/AEO priority over everything else.** The blog
lives at `/blogs/news` (labelled "Journal"). Before writing anything, list what
is already published — five posts exist and a duplicate would compete with our
own URL.

Real collections to link to: `/collections/little`, `/quilts`, `/swaddles`,
`/backpacks`, `/toiletry-pouches`, `/carry`, `/birthday`, `/new-baby`,
`/diwali`, `/wedding-favours`. The bulk path is `/pages/return-gifts` —
from ten pieces, quote within 24 hours. Retail products sit at ₹999–₹1,199;
free shipping over ₹750; free gift pouch over ₹1,999.

Shopify blog article fields:

| Shopify field | What goes in it |
|---|---|
| Title | the displayed title |
| Content | body HTML — `<p>`, `<h2>`, `<h3>`, `<ul>`, `<table>`, `<img>` |
| Excerpt | the answer block, verbatim — it is the strongest 50 words |
| Featured image + alt | hero, 1600×900 |
| Author | the owner |
| Tags | occasion or category tags matching the store's blog tags |
| SEO title | query first, ~60 chars |
| SEO description | under 160 chars |

The theme's product-description stripping (`rte-formatter`) does **not** apply
to blog articles — lists and tables render normally here. Verify once on the
first published article, then stop worrying about it.

FAQ: put the questions at the foot of the article as `<h3>` + `<p>` pairs, and
add FAQPage JSON-LD via the theme or an app. Without the JSON-LD the FAQ still
earns its place for readers.

## 3. LinkedIn

Plain text, ready to paste. Structure:

```
HOOK          one line, survives the "see more" fold
BODY          150–250 words, single-line paragraphs
FREE ADVICE   the thing you'd tell someone who isn't buying from you
SIGN-OFF      one line pointing at the journal post
---
FIRST COMMENT the link, posted by the owner immediately after
IMAGE         path + crop + treatment, 1200×1200
```

Rules that matter: personal profile not company page · link in the first
comment, never the body · at most two hashtags · no emoji in the bulk rail ·
never automate the posting.

## 4. drop-notes.md

Short. What the owner needs, not a diary:

- the sources actually read this session, as links
- any fact added to `references/facts.md`
- anything that needs his decision or a photograph that doesn't exist yet
- the plain-English summary: what this means, what he must do, what it costs,
  what is waiting on him
