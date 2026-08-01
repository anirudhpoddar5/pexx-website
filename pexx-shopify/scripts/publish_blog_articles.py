#!/usr/bin/env python3
"""Publish the remaining outlined PEXX journal articles (see
content-drafts/03-seo-aeo-blog-plan.md) and set a meta description on every
article in the blog (new + the 2 already live). Idempotent on handle.

Run: python3 scripts/publish_blog_articles.py
"""
import os, json, time, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = open(os.path.join(ROOT, ".shopify-token")).read().strip()
SHOP = "pexx-7935.myshopify.com"
API = f"https://{SHOP}/admin/api/2025-01"
BLOG_ID = 108844351577  # "news" blog, handle used by the theme is /blogs/news (nav label "Journal")


def call(method, path, payload=None):
    url = f"{API}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method,
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status, json.loads(resp.read() or b"{}")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(2)
                continue
            return e.code, json.loads(e.read() or b"{}")
    return None, None


# New articles to publish (Posts 3-5 from the blog plan; Posts 1-2 already live).
NEW_ARTICLES = [
    {
        "title": "Best Skin-Safe Swaddles & Baby Bedding in India (Buyer's Guide)",
        "handle": "best-skin-safe-swaddles-baby-bedding-india",
        "tags": "safety, swaddles",
        "meta_description": "A buyer's guide to safe baby swaddles and bedding in India: fabric, dye safety, size, and price across budgets.",
        "body_html": """<p>The best baby swaddles and bedding in India are made from soft, breathable cotton or muslin with azo-free dyes, sized generously (105×105 cm or larger for swaddles), and gentle enough for daily newborn use. Look for breathable weave, safe dyes, and prints in calming colours. Here's what to check before you buy, and a few options across budgets.</p>
<h2>Fabric first</h2>
<p>Pure cotton or muslin breathes better than any synthetic blend, which matters most in Indian summers. A tighter weave holds its shape wash after wash; a looser muslin weave is softer and cooler for the height of summer.</p>
<h2>Dye safety</h2>
<p>Azo-free dyes are non-negotiable for anything against a newborn's skin. If a listing doesn't mention dye safety at all, that's worth asking about directly before you buy.</p>
<h2>Size and weight</h2>
<p>Look for at least 105×105 cm for a swaddle, and a fabric weight suited to your climate — lighter muslin for summer, a slightly heavier weave for winter.</p>
<h2>Price, across budgets</h2>
<p>Basic printed cotton swaddles start under ₹500; hand block-printed sets with matching quilts or pouches usually run ₹800–₹2,000; fully coordinated gifting sets go higher. Price tends to track fabric quality and whether the print is hand-done or machine-printed — worth checking either way, whoever you buy from.</p>
<p>See our own <a href="/collections/little">Little collection</a> for hand block-printed, azo-free swaddles and quilts, and the <a href="/pages/fabric-safety">fabric &amp; safety hub</a> for more on what to check before you buy.</p>""",
    },
    {
        "title": "How to Wash & Care for Baby Swaddles and Quilts",
        "handle": "how-to-wash-care-baby-swaddles-quilts",
        "tags": "care, swaddles",
        "meta_description": "How to wash and care for hand block-printed baby swaddles and quilts — first wash, everyday care, and safe drying and storage.",
        "body_html": """<p>Wash baby swaddles in cold or lukewarm water on a gentle cycle, using a mild detergent, and dry in shade. Cotton and muslin actually get softer with each wash. Wash new items before first use, and avoid harsh bleach so prints and fabric stay gentle on baby's skin.</p>
<h2>Before the first wash</h2>
<p>Wash any new swaddle or quilt once before it touches your baby's skin, even if it looks clean. This clears any residue from manufacturing and softens the weave from the very first use.</p>
<h2>The everyday wash</h2>
<p>Cold or lukewarm water, gentle cycle, mild detergent. Skip fabric softener — it coats the fibres and works against the natural softening that comes from washing. Turn printed pieces inside out to protect the print.</p>
<h2>Some colour release is normal</h2>
<p>Hand block-printed cotton can release a little colour in the first few washes, more with darker or richer prints. This settles quickly — wash separately from light fabrics for the first two or three washes, then treat it like any cotton piece.</p>
<h2>Drying and storage</h2>
<p>Dry in shade rather than direct sun, which keeps colour from fading unevenly. Store folded rather than on a hanger to avoid stretching the weave.</p>
<p>PEXX swaddles and quilts are pure cotton, hand block-printed with azo-free dyes — see the <a href="/collections/little">Little collection</a>, or the <a href="/pages/fabric-safety">fabric &amp; safety hub</a> for how we choose dyes and fabric.</p>""",
    },
    {
        "title": "What Is Hand Block Printing, and Is It Safe for Kids?",
        "handle": "what-is-hand-block-printing-safe-for-kids",
        "tags": "craft, safety",
        "meta_description": "What hand block printing is, how it's made, and why it's safe for children's clothing and bedding when azo-free dyes are used.",
        "body_html": """<p>Hand block printing is a traditional technique where carved wooden blocks are dipped in dye and pressed onto fabric by hand. It's safe for children's clothing and bedding when azo-free, non-toxic dyes are used. Small variations between pieces are normal and are a sign of genuine handwork, not a defect.</p>
<h2>How it's made</h2>
<p>A motif is carved into a teak block, then dipped in dye and pressed onto cotton by hand, one impression at a time — one block per colour, pressed in sequence.</p>
<h2>What makes it safe for kids</h2>
<p>The technique itself is just dye and pressure — the safety comes entirely from what dye is used. Azo-free, skin-friendly dyes are what make a block-printed piece safe for daily wear against a child's skin, same as with any printed textile.</p>
<h2>Why pieces vary slightly</h2>
<p>Hand pressure isn't perfectly even, so two pieces from the same block are never identical. That's the tell that it's genuinely handmade — a flawless, identical repeat usually means machine printing instead.</p>
<h2>Why it costs more than screen printing</h2>
<p>Screen printing stamps identical colour in seconds by machine. Block printing is slower and done by a trained artisan, one press at a time, which limits how much one person can produce in a day. The price reflects that labour.</p>
<p>See <a href="/pages/about">Our Story</a> for more on how PEXX prints are made, or the <a href="/collections/little">Little collection</a> to see it on real pieces.</p>""",
    },
]

# Meta descriptions for the 2 already-live articles (currently unset).
EXISTING_META_DESCRIPTIONS = {
    "20-return-gift-ideas-for-kids-birthdays-that-arent-plastic":
        "20 non-plastic return gift ideas for kids' birthdays in India, from under ₹200 — soft cotton pouches and keepsakes kids actually keep.",
    "is-muslin-safe-for-a-newborns-skin":
        "Is muslin safe for a newborn's skin? Yes — here's what to check (azo-free dyes, weave, size) before buying baby muslin in India.",
}


def set_meta_description(article_id, text):
    payload = {"metafield": {"namespace": "global", "key": "description_tag",
                              "type": "single_line_text_field", "value": text}}
    s, r = call("POST", f"/blogs/{BLOG_ID}/articles/{article_id}/metafields.json", payload)
    return s in (200, 201), r


def main():
    s, body = call("GET", f"/blogs/{BLOG_ID}/articles.json?limit=250")
    if s != 200:
        print(f"ERROR: could not list articles (HTTP {s}): {body}")
        raise SystemExit(1)
    existing = {a["handle"]: a for a in body.get("articles", [])}

    print(f"{'handle':50} {'status':10}")
    print("-" * 70)

    for art in NEW_ARTICLES:
        handle = art["handle"]
        if handle in existing:
            print(f"{handle:50} {'VERIFIED':10} (already published)")
            article_id = existing[handle]["id"]
        else:
            payload = {"article": {
                "title": art["title"], "handle": handle, "body_html": art["body_html"],
                "tags": art["tags"], "author": "PEXX", "published": True,
            }}
            s, r = call("POST", f"/blogs/{BLOG_ID}/articles.json", payload)
            if s not in (200, 201):
                print(f"{handle:50} {'FAILED':10} (HTTP {s}): {r}")
                continue
            article_id = r["article"]["id"]
            print(f"{handle:50} {'CREATED':10} (id {article_id})")

        ok, r = set_meta_description(article_id, art["meta_description"])
        print(f"  -> meta description {'set' if ok else 'FAILED'}")
        time.sleep(0.5)

    for handle, desc in EXISTING_META_DESCRIPTIONS.items():
        if handle not in existing:
            print(f"{handle:50} {'MISSING':10} (expected to already exist)")
            continue
        article_id = existing[handle]["id"]
        s, mf = call("GET", f"/blogs/{BLOG_ID}/articles/{article_id}/metafields.json")
        already = any(m["namespace"] == "global" and m["key"] == "description_tag"
                      for m in mf.get("metafields", [])) if s == 200 else False
        if already:
            print(f"{handle:50} {'VERIFIED':10} (meta description already set)")
            continue
        ok, r = set_meta_description(article_id, desc)
        print(f"{handle:50} {'UPDATED':10} meta description {'set' if ok else 'FAILED'}")
        time.sleep(0.5)


if __name__ == "__main__":
    main()
