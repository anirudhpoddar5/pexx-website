#!/usr/bin/env python3
"""Seed PEXX collections + placeholder products with real category images & tags."""
import os, json, time, base64, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = open(os.path.join(ROOT, ".shopify-token")).read().strip()
SHOP = "pexx-7935.myshopify.com"
API = f"https://{SHOP}/admin/api/2025-01"


def call(method, path, payload=None):
    url = f"{API}{path}"
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(url, data=data, method=method,
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"})
    for attempt in range(5):
        try:
            return json.loads(urllib.request.urlopen(req).read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(2); continue
            print("ERR", method, path, e.code, e.read().decode()[:200]); return None
    return None


def b64(fn):
    p = os.path.join(ROOT, fn)
    if not os.path.exists(p):
        return None
    return base64.b64encode(open(p, "rb").read()).decode()


# ---- collections ----
collections = [
    ("Little", "Hand block-printed for little ones — swaddles, quilts, bags & more.", "category-little.jpeg"),
    ("Carry", "Block-printed totes, weekenders & toiletry sets for everyday carry.", "category-carry.jpeg"),
    ("Gifting", "Soft, skin-safe gifts they'll keep — for new babies, birthdays & festivals.", "carry-toiletry-bag-sets.jpeg"),
]
col_ids = {}
for title, body, img in collections:
    payload = {"custom_collection": {"title": title, "body_html": body}}
    a = b64(img)
    if a:
        payload["custom_collection"]["image"] = {"attachment": a}
    r = call("POST", "/custom_collections.json", payload)
    if r:
        col_ids[title] = r["custom_collection"]["id"]
        print("collection:", title, col_ids[title])
    time.sleep(0.6)

# ---- products ----  (title, type, price, tags, image, [collections])
products = [
    ("Reversible Cotton Quilt", "Quilt", "1899", "kids,quilt,age_baby,price_1500-2500", "little-kids-quilts.jpeg", ["Little"]),
    ("Block Print Swaddle — Set of 2", "Swaddle", "1499", "kids,swaddle,age_just-born,price_1000-1500,occasion_new-baby", "little-swaddles.jpeg", ["Little", "Gifting"]),
    ("Kids Block Print Backpack", "Backpack", "1299", "kids,backpack,age_kid,price_1000-1500", "little-kids-backpacks.jpeg", ["Little"]),
    ("Little Block Print Pouch", "Pouch", "799", "kids,pouch,age_all-ages,price_under-1000,occasion_birthday,bulk", "little-kids-pouches.jpeg", ["Little", "Gifting"]),
    ("Soft Cotton Dohar", "Dohar", "1699", "kids,dohar,age_baby,price_1500-2500", "little-kids-dohar.jpeg", ["Little"]),
    ("Stationery & iPad Sleeve", "Sleeve", "999", "kids,sleeve,age_big-kid,price_under-1000", "little-kids-pouches.jpeg", ["Little", "Carry"]),
    ("Block Print Tote Bag", "Tote", "1199", "accessories,tote,age_all-ages,price_1000-1500", "carry-tote-bag.jpeg", ["Carry"]),
    ("Weekender Travel Bag", "Weekender", "1999", "accessories,weekender,age_all-ages,price_1500-2500", "carry-duffle-bag.jpeg", ["Carry"]),
    ("Toiletry Trio — Set of 3", "Toiletry Set", "1499", "accessories,toiletry-set,age_all-ages,price_1000-1500,occasion_wedding,bulk", "carry-toiletry-bag-sets.jpeg", ["Carry", "Gifting"]),
    ("Block Print Sling Bag", "Sling", "1099", "accessories,sling,age_all-ages,price_1000-1500", "carry-sling-bags.jpeg", ["Carry"]),
]

for title, ptype, price, tags, img, cols in products:
    payload = {"product": {
        "title": title, "vendor": "PEXX", "product_type": ptype, "status": "active",
        "tags": tags,
        "body_html": f"<p>Hand block-printed in soft, skin-safe cotton with azo-free dyes. Placeholder listing — real description, pricing & photos to follow.</p>",
        "variants": [{"price": price}],
    }}
    a = b64(img)
    if a:
        payload["product"]["images"] = [{"attachment": a}]
    r = call("POST", "/products.json", payload)
    if not r:
        continue
    pid = r["product"]["id"]
    print("product:", title, pid)
    time.sleep(0.6)
    for c in cols:
        if c in col_ids:
            call("POST", "/collects.json", {"collect": {"product_id": pid, "collection_id": col_ids[c]}})
            time.sleep(0.4)

print("DONE")
