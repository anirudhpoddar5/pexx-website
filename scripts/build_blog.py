#!/usr/bin/env python3
"""Pre-render the journal so crawlers that don't run JavaScript can read it.

Before: /blog/<slug>/ was an empty page that meta-refreshed to
post.html?slug=…, where the article was assembled client-side. Google copes;
several AI crawlers do not run JS and saw nothing at all.

After: /blog/<slug>/index.html contains the whole article as HTML, with
Article + FAQPage JSON-LD baked in. blog/post.html is left untouched and still
works as the dynamic viewer.

Also writes sitemap.xml, since it already knows every URL.

  python3 scripts/build_blog.py            # build
  python3 scripts/build_blog.py --check    # verify, exit 1 if anything is stale
  python3 scripts/build_blog.py --self-check
"""
import argparse, datetime, html, json, pathlib, re, sys, urllib.parse

SITE = "https://www.poddarexp.com"
ROOT = pathlib.Path(__file__).resolve().parents[1]

# Pages that aren't posts but belong in the sitemap.
STATIC_PAGES = ["index.html", "interiors.html", "little.html", "wear.html",
                "carry.html", "workshops.html", "contact.html", "blog/index.html"]

NAV_SCRIPT = """  <script>
    (function () {
      const toggle = document.querySelector('.nav-toggle');
      const nav = document.querySelector('#primary-nav');
      if (!toggle || !nav) return;
      toggle.addEventListener('click', () => {
        const open = toggle.getAttribute('aria-expanded') === 'true';
        toggle.setAttribute('aria-expanded', String(!open));
        nav.classList.toggle('open', !open);
      });
    }());
  </script>
"""


def deepen_links(markup):
    """post.html sits in /blog/; the built page sits in /blog/<slug>/."""
    # order matters: deepen the existing ../ links first, or the rewritten
    # back-link below gets deepened a second time
    markup = markup.replace('href="../', 'href="../../')
    markup = markup.replace('src="../', 'src="../../')
    markup = markup.replace('href="./index.html"', 'href="../index.html"')
    return markup


def fmt_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f'{d.strftime("%B")} {d.day}, {d.year}'


def structured_data(post, body):
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    blocks = [{
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post["title"],
        "description": post.get("metaDescription") or post.get("excerpt", ""),
        "image": [SITE + urllib.parse.quote(post["image"])],
        "datePublished": post["date"],
        "dateModified": post["date"],
        "wordCount": words,
        "author": {"@type": "Organization", "name": "PEXX"},
        "publisher": {"@type": "Organization", "name": "PEXX"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{SITE}/blog/{post['slug']}/"},
        "keywords": post.get("keywords", ""),
    }]
    if post.get("faq"):
        blocks.append({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [{
                "@type": "Question", "name": q["question"],
                "acceptedAnswer": {"@type": "Answer", "text": q["answer"]},
            } for q in post["faq"]],
        })
    return json.dumps(blocks if len(blocks) > 1 else blocks[0], indent=2)


def render(template, post, body):
    slug = post["slug"]
    url = f"{SITE}/blog/{slug}/"
    title = html.escape(post.get("seoTitle") or f"{post['title']} | PEXX Journal", quote=True)
    desc = html.escape(post.get("metaDescription") or post.get("excerpt", ""), quote=True)
    img = SITE + urllib.parse.quote(post["image"])

    page = template.split("<script>", 1)[0]  # drop the client-side loader
    page = page.replace('  <meta name="robots" content="noindex,follow" />\n', "")
    page = deepen_links(page)

    page = page.replace("<title>Journal | PEXX</title>", f"<title>{title}</title>")
    page = re.sub(r'<meta name="description" content="[^"]*" />',
                  f'<meta name="description" content="{desc}" />', page, count=1)
    page = re.sub(r'<meta property="og:title" content="[^"]*" />',
                  f'<meta property="og:title" content="{title}" />', page, count=1)
    page = re.sub(r'<meta property="og:description" content="[^"]*" />',
                  f'<meta property="og:description" content="{desc}" />', page, count=1)
    page = re.sub(r'<meta property="og:url" content="[^"]*" />',
                  f'<meta property="og:url" content="{url}" />', page, count=1)
    page = re.sub(r'<meta property="og:image" content="[^"]*" />',
                  f'<meta property="og:image" content="{img}" />', page, count=1)
    page = re.sub(r'<link rel="canonical" href="[^"]*" />',
                  f'<link rel="canonical" href="{url}" />', page, count=1)
    page = re.sub(r'<meta name="twitter:title" content="[^"]*" />',
                  f'<meta name="twitter:title" content="{title}" />', page, count=1)
    page = re.sub(r'<meta name="twitter:description" content="[^"]*" />',
                  f'<meta name="twitter:description" content="{desc}" />', page, count=1)
    page = re.sub(r'<meta name="twitter:image" content="[^"]*" />',
                  f'<meta name="twitter:image" content="{img}" />', page, count=1)
    page = re.sub(r'<meta property="article:published_time" content="[^"]*" />',
                  f'<meta property="article:published_time" content="{post["date"]}" />', page, count=1)
    page = page.replace(
        '<script id="article-structured-data" type="application/ld+json">{}</script>',
        f'<script type="application/ld+json">\n{structured_data(post, body)}\n  </script>')

    # fill the shell that the JS used to fill, and unhide it
    page = page.replace('<div id="article-shell" class="article-shell" hidden>',
                        '<div id="article-shell" class="article-shell">')
    # match the JS viewer's format exactly: "June 27, 2026 · 6 min read"
    date = fmt_date(post["date"])
    meta_line = date + (f' &middot; {post["readTime"]}' if post.get("readTime") else "")
    page = page.replace('<span class="eyebrow" id="post-category">Journal</span>',
                        f'<span class="eyebrow" id="post-category">{html.escape(post.get("category", "Journal"))}</span>')
    page = page.replace('<span class="post-date" id="post-date"></span>',
                        f'<span class="post-date" id="post-date">{meta_line}</span>')
    page = page.replace('<h1 id="post-title"></h1>',
                        f'<h1 id="post-title">{html.escape(post["title"])}</h1>')
    page = page.replace('<p id="post-excerpt"></p>',
                        f'<p id="post-excerpt">{html.escape(post.get("excerpt", ""))}</p>')
    page = page.replace('<img id="post-image" src="" alt="" fetchpriority="high">',
                        f'<img id="post-image" src="{post["image"]}" '
                        f'alt="{html.escape(post.get("imageAlt") or post["title"], quote=True)}" fetchpriority="high">')
    page = page.replace('<div id="post-content" class="article-body"></div>',
                        f'<div id="post-content" class="article-body">\n{deepen_links(body)}\n</div>')

    if post.get("faq"):
        faq = ['<section class="article-faq">', "<h2>Questions we are asked</h2>"]
        for q in post["faq"]:
            faq.append(f'<h3>{html.escape(q["question"])}</h3><p>{html.escape(q["answer"])}</p>')
        faq.append("</section>")
        page = page.replace("</article>", "\n".join(faq) + "\n      </article>", 1)

    q = urllib.parse.quote
    page = (page.replace("__RAWURL__", url)
                .replace("__URL__", q(url, safe=""))
                .replace("__TITLE__", q(post["title"], safe=""))
                .replace("__IMAGE__", q(img, safe="")))
    return page + NAV_SCRIPT + "</body>\n</html>\n"


def build_index(root, posts):
    """The journal hub was JS-only, so nothing linked to the articles. Write the
    cards in as real HTML; the existing script hydrates over them for search."""
    path = root / "blog" / "index.html"
    if not path.exists():
        return None
    page = path.read_text()
    live = [p for p in posts if p.get("slug")]
    if not live:
        return page

    def card(p):
        alt = html.escape(p.get("imageAlt") or p["title"], quote=True)
        return (f'<a class="post-card" href="./{p["slug"]}/">'
                f'<img src="..{p["image"]}" alt="{alt}" loading="lazy">'
                f'<div class="post-card-copy">'
                f'<span class="post-date">{fmt_date(p["date"])}</span>'
                f'<h3>{html.escape(p["title"])}</h3>'
                f'<p>{html.escape(p.get("excerpt", ""))}</p>'
                f'<div class="card-tag-row">'
                f'<span class="category-chip">{html.escape(p.get("category", "Journal"))}</span>'
                f'<span class="read-link">Read more <span aria-hidden="true">&rarr;</span></span>'
                f'</div></div></a>')

    top = live[0]
    featured = (f'<img src="..{top["image"]}" '
                f'alt="{html.escape(top.get("imageAlt") or top["title"], quote=True)}" loading="lazy">'
                f'<div class="featured-copy">'
                f'<span class="post-date">{fmt_date(top["date"])}</span>'
                f'<h3>{html.escape(top["title"])}</h3>'
                f'<p>{html.escape(top.get("excerpt", ""))}</p>'
                f'<a class="read-link" href="./{top["slug"]}/">Read the article '
                f'<span aria-hidden="true">&rarr;</span></a></div>')

    page = re.sub(r'(<article id="featured-post"[^>]*>).*?(</article>)',
                  lambda m: m.group(1) + featured + m.group(2), page, count=1, flags=re.S)
    page = re.sub(r'(<div id="posts-grid"[^>]*>).*?(</div>\s*<div id="empty-state")',
                  lambda m: m.group(1) + "".join(card(p) for p in live)
                            + '</div>\n      <div id="empty-state"',
                  page, count=1, flags=re.S)
    page = page.replace('<p id="results-meta" class="results-meta" aria-live="polite">Loading journal entries...</p>',
                        f'<p id="results-meta" class="results-meta" aria-live="polite">'
                        f'Showing {len(live)} journal entries</p>')
    return page


def sitemap(posts):
    urls = [(f"{SITE}/{p}".replace("/index.html", "/"), None) for p in STATIC_PAGES]
    urls += [(f"{SITE}/blog/{p['slug']}/", p["date"]) for p in posts]
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod in urls:
        out.append("  <url>")
        out.append(f"    <loc>{loc}</loc>")
        if lastmod:
            out.append(f"    <lastmod>{lastmod}</lastmod>")
        out.append("  </url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def build(root, check=False):
    root = pathlib.Path(root)
    template = (root / "blog" / "post.html").read_text()
    posts = json.loads((root / "data" / "posts.json").read_text())
    stale, built, skipped = [], [], []

    for post in posts:
        slug = post.get("slug")
        if not slug:
            skipped.append(post.get("id", "?"))
            continue
        body_file = root / post["file"].lstrip("/")
        if not body_file.exists():
            skipped.append(slug)
            continue
        page = render(template, post, body_file.read_text())
        target = root / "blog" / slug / "index.html"
        if check:
            if not target.exists() or target.read_text() != page:
                stale.append(slug)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page)
        built.append(slug)

    index_html = build_index(root, posts)
    index_path = root / "blog" / "index.html"
    if index_html is not None:
        if check:
            if index_path.read_text() != index_html:
                stale.append("blog/index.html")
        else:
            index_path.write_text(index_html)

    sm = sitemap([p for p in posts if p.get("slug")])
    sm_path = root / "sitemap.xml"
    if check:
        if not sm_path.exists() or sm_path.read_text() != sm:
            stale.append("sitemap.xml")
        return stale, skipped
    sm_path.write_text(sm)
    return built, skipped


def self_check():
    import tempfile
    src = ROOT
    with tempfile.TemporaryDirectory() as d:
        root = pathlib.Path(d)
        (root / "blog").mkdir()
        (root / "data").mkdir()
        (root / "posts").mkdir()
        (root / "blog" / "post.html").write_text((src / "blog" / "post.html").read_text())
        (root / "blog" / "index.html").write_text((src / "blog" / "index.html").read_text())
        post = {"id": "t", "slug": "t", "title": "Title & Co", "seoTitle": "SEO T",
                "date": "2026-08-25", "readTime": "5 min read", "excerpt": "Ex.",
                "metaDescription": "Meta.", "image": "/assets/blog/t/hero.jpg",
                "imageAlt": "Alt", "file": "/posts/t.html", "category": "Trends",
                "keywords": "k", "faq": [{"question": "Q?", "answer": "A."}]}
        (root / "data" / "posts.json").write_text(json.dumps([post]))
        (root / "posts" / "t.html").write_text(
            '<p>Real body text here.</p><img src="../workshop.jpeg">')

        built, skipped = build(root)
        assert built == ["t"] and not skipped, (built, skipped)
        page = (root / "blog" / "t" / "index.html").read_text()

        assert "Real body text here." in page, "article body must be in the HTML"
        assert 'class="article-shell">' in page and "article-shell\" hidden" not in page
        assert "fetch(" not in page, "client-side loader must be stripped"
        assert '"@type": "FAQPage"' in page and '"@type": "BlogPosting"' in page
        assert f'<link rel="canonical" href="{SITE}/blog/t/" />' in page
        assert "Title &amp; Co" in page, "titles must be escaped"
        assert "August 25, 2026" in page, "date must be formatted like the JS viewer"
        assert 'href="../../index.html"' in page, "nav links must be re-based one level deeper"
        assert 'href="../index.html"' in page, "back-to-journal link must point at /blog/"
        assert 'src="../../workshop.jpeg"' in page, "body images must be re-based too"
        assert "wa.me/?text=" in page, "share row must survive into the built page"
        assert "__" not in page.split("<body")[1], "every share token must be resolved"
        assert "noindex" not in page, "built pages must stay indexable"
        idx = (root / "blog" / "index.html").read_text()
        assert 'href="./t/"' in idx, "journal index must link articles without JS"
        assert (root / "sitemap.xml").read_text().count("<loc>") == len(STATIC_PAGES) + 1

        stale, _ = build(root, check=True)
        assert stale == [], f"freshly built output should not be stale: {stale}"
    print("self-check ok")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--check", action="store_true", help="fail if any page is out of date")
    ap.add_argument("--self-check", action="store_true")
    a = ap.parse_args()
    if a.self_check:
        self_check(); sys.exit()
    result, skipped = build(a.root, check=a.check)
    if a.check:
        if result:
            print("stale: " + ", ".join(result)); sys.exit(1)
        print("all blog pages up to date")
    else:
        print("built: " + ", ".join(result))
        print("wrote: sitemap.xml")
    if skipped:
        print("skipped (no slug or missing body file): " + ", ".join(skipped))
