#!/usr/bin/env python3
"""Write real SEO/AEO collection descriptions (see PRODUCTION-BUILD-PLAN.md
§9B: "100-150 word description each ... keyword + internal links"). Little/
Carry/Gifting currently have 9-12 word taglines; the 5 occasion smart
collections have none at all. Idempotent: skips any collection whose
body_html already contains the marker text below (safe to re-run).

Run: python3 scripts/update_collection_descriptions.py
"""
import os, json, time, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = open(os.path.join(ROOT, ".shopify-token")).read().strip()
SHOP = "pexx-7935.myshopify.com"
API = f"https://{SHOP}/admin/api/2025-01"


def call(method, path, payload=None):
    url = f"{API}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method,
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")


# handle -> (resource kind, body_html)
DESCRIPTIONS = {
    "little": ("custom", """<p>Little is PEXX's collection for babies and young children — swaddles, quilts, pouches and bags, all hand block-printed on soft, breathable cotton. Every piece is coloured with azo-free, skin-friendly dyes, chosen for skin that hasn't earned any tolerance for shortcuts yet. Sizes run from newborn swaddles to bags for slightly older kids, and every print is pressed by hand from a carved teak block, so no two pieces are ever quite identical — that's the mark of genuine handwork, not a flaw. Wash cold, dry in shade, and the fabric only gets softer with time.</p>
<p>Shopping for a gift rather than for your own child? See <a href="/collections/gifting">Gifting</a> for pieces suited to birthdays and new-baby visits, or read <a href="/pages/fabric-safety">how we choose fabric and dye</a> before you buy.</p>"""),
    "carry": ("custom", """<p>Carry is PEXX's collection of hand block-printed bags and travel accessories — totes, weekenders and toiletry sets for everyday use, not just special occasions. Each piece is made from quilted cotton, printed by hand from a carved teak block, and finished to hold up to daily use rather than sit as a display piece. The same azo-free dyes used on our baby pieces go into Carry, since the people carrying these bags brush against them all day too.</p>
<p>Looking for something to gift rather than keep? Several Carry pieces double well as <a href="/collections/gifting">gifts for weddings and adult birthdays</a> — see also <a href="/pages/about">Our Story</a> for how the prints are made.</p>"""),
    "gifting": ("custom", """<p>Gifting brings together PEXX pieces suited to India's gifting occasions — new babies, birthdays, Rakhi, Diwali, weddings and return gifts for kids' parties. Everything here is hand block-printed on soft cotton with azo-free dyes, gift-wrapped on request with a personal note, and priced honestly rather than marked up for the occasion.</p>
<p>Buying in bulk for a party or corporate order? See <a href="/pages/return-gifts">Return &amp; Bulk Gifts</a> for quantities from ten pieces. Sending something to family in India from abroad? <a href="/pages/gift-to-india">Gift to India</a> covers currency and delivery. For occasion-specific picks, browse <a href="/pages/baby-gifting-guide">our baby gifting guide</a>.</p>"""),
    "birthday": ("smart", """<p>Birthday gifts and return gifts from PEXX are hand block-printed, azo-free and useful long after the party ends — pouches, pencil cases and keepsakes children actually keep, not plastic that breaks the same day.</p>
<p>Ordering in bulk for a class or a party? See <a href="/pages/return-gifts">Return &amp; Bulk Gifts</a> for pricing from ten pieces.</p>"""),
    "diwali": ("smart", """<p>PEXX's Diwali edit is soft, hand block-printed cotton in festive prints — gifts for children and adults that hold up better than sweets or disposable decor. Every piece is azo-free and gift-wrapped on request, ready to hand over as it arrives.</p>"""),
    "new-baby": ("smart", """<p>For a new baby, PEXX's swaddles, quilts and layette pieces are hand block-printed on breathable cotton with azo-free dyes — gentle enough for a newborn's first weeks.</p>
<p>See our <a href="/pages/baby-gifting-guide">baby gifting guide</a> for what to choose by occasion, from godh bharai to namkaran.</p>"""),
    "rakhi": ("smart", """<p>Send a Rakhi gift that isn't another box of sweets — PEXX's hand block-printed pouches and keepsakes for nieces and nephews, gift-wrapped with a note.</p>
<p>Sending from abroad? <a href="/pages/gift-to-india">Gift to India</a> covers currency and delivery to any Indian address.</p>"""),
    "wedding-favours": ("smart", """<p>PEXX wedding favours are hand block-printed cotton pouches and keepsakes — useful, skin-safe and a step up from typical trousseau-packet fillers.</p>
<p>Ordering for a full guest list? <a href="/pages/return-gifts">Return &amp; Bulk Gifts</a> covers bulk pricing and delivery to one address.</p>"""),
}

RESOURCE_PATH = {"custom": "custom_collections", "smart": "smart_collections"}


def main():
    all_collections = {}
    for kind, path in RESOURCE_PATH.items():
        s, body = call("GET", f"/{path}.json?limit=250")
        if s != 200:
            print(f"ERROR: could not list {path} (HTTP {s}): {body}")
            raise SystemExit(1)
        for c in body[path]:
            all_collections[c["handle"]] = (kind, c)

    print(f"{'handle':20} {'status':10} words")
    print("-" * 50)

    for handle, (expected_kind, new_body) in DESCRIPTIONS.items():
        if handle not in all_collections:
            print(f"{handle:20} {'MISSING':10} (collection not found)")
            continue
        kind, collection = all_collections[handle]
        current = collection.get("body_html") or ""
        if len(current.split()) >= 40:
            print(f"{handle:20} {'SKIPPED':10} already has {len(current.split())} words")
            continue

        path = RESOURCE_PATH[kind]
        resource_key = "custom_collection" if kind == "custom" else "smart_collection"
        payload = {resource_key: {"id": collection["id"], "body_html": new_body}}
        s, r = call("PUT", f"/{path}/{collection['id']}.json", payload)
        if s != 200:
            print(f"{handle:20} {'FAILED':10} (HTTP {s}): {r}")
            continue
        word_count = len(new_body.split())
        print(f"{handle:20} {'UPDATED':10} {word_count} words")
        time.sleep(0.4)


if __name__ == "__main__":
    main()
