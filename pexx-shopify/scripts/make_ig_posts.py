#!/usr/bin/env python3
"""Rebuild yesterday's ad photos as ORGANIC Instagram carousels.

Same source photos + same composer as the paid carousels, but: no price on the
image, and every set ends on a CTA card. Meta ads can carry a price; an organic
grid post that leads with ₹ reads as an ad and gets scrolled past.
"""
import json, pathlib, sys, urllib.request, subprocess

sys.path.insert(0, "/Users/anirudhpoddar/Downloads/pexx-website/pexx-shopify/scripts")
from make_ad_creative import compose

SHOP  = "pexx-7935.myshopify.com"
TOKEN = pathlib.Path("/Users/anirudhpoddar/Downloads/pexx-website/pexx-shopify/.shopify-token").read_text().strip()
OUT   = pathlib.Path.home() / "Desktop/PEXX/instagram"
SRC   = OUT / "_src"

# handle, image index, eyebrow, headline, subtitle, cta(sub2 line)
SETS = {
"quilt": [
 ("bunny-floral-print-baby-quilt",     4, "Hand block-printed in Jaipur", "Softest thing in the house", "Reversible cotton quilt", None),
 ("orange-dachshund-print-baby-quilt", 1, "One quilt, four ways",         "In the cot",                 "Nap one, floor the next",  None),
 ("bear-print-baby-quilt",             0, "One quilt, four ways",         "On the floor",               "Play mat that survives the wash", None),
 ("frog-pond-print-kids-quilt",        1, "Two quilts in one",            "Flip it over",               "A different print on the back", None),
 ("blush-unicorn-print-kids-quilt",    2, "Skin-safe dyes · COD",         "Pick your print",            "Free shipping · 10-day returns", "SHOP NOW — LINK IN BIO"),
],
"swaddle": [
 ("unicorn-dolphin-swaddle-set",    3, "Pure cotton muslin",       "Breathes like nothing else", "For the 0-6 month stretch", None),
 ("sunburst-polka-dot-swaddle-set", 3, "Two prints per set",       "Swaddled, asleep",           "Big enough to wrap properly", None),
 ("bear-circus-animal-swaddle-set", 0, "Hand block-printed",       "Light for Indian summers",   "Softer with every wash", None),
 ("bunny-floral-stripe-swaddle-set",1, "Newborn size",             "The gift that gets used",    "Every new-mum friend, sorted", None),
 ("unicorn-dolphin-swaddle-set",    0, "Skin-safe dyes · COD",     "Pick your pair",             "Free shipping · 10-day returns", "SHOP NOW — LINK IN BIO"),
],
"pouch": [
 ("rainbow-butterfly-toiletry-pouch-set", 0, "Three sizes that nest", "Everything in its place", "Small, medium, large",       None),
 ("teal-penguin-toiletry-pouch-set",      2, "Packs flat",            "Ready to travel",         "Toothbrush, crayons, the rest", None),
 ("frog-pond-toiletry-pouch-set",         0, "Wipe-clean lining",     "Lives on the shelf",      "Proper zips, no plastic feel", None),
 ("monkey-print-toiletry-pouch-set",      2, "Not just for the bath", "Crayons and colours",     "Whatever they collect this week", None),
 ("pastel-bear-toiletry-pouch-set",       4, "Hand block-printed · COD","Pick your print",       "Free shipping · 10-day returns", "SHOP NOW — LINK IN BIO"),
],
"backpack": [
 ("monkey-print-kids-backpack",       2, "Quilted cotton, not nylon", "Light enough to carry themselves", "Made for small shoulders", None),
 ("pastel-bear-print-kids-backpack",  0, "Worn, age four",            "Their first own bag",      "Carried all the way, no help", None),
 ("bunny-floral-print-kids-backpack", 4, "Out for the day",           "Holds more than it looks", "Zip closure and a front pocket", None),
 ("penguin-print-kids-backpack",      4, "Bottle and pencils",        "Packed by them",           "Sleepover at Nani's, sorted", None),
 ("submarine-print-kids-backpack",    3, "Skin-safe dyes · COD",      "Pick your print",          "Free shipping · 10-day returns", "SHOP NOW — LINK IN BIO"),
],
}


def images(handle):
    req = urllib.request.Request(
        f"https://{SHOP}/admin/api/2024-10/products.json?handle={handle}&fields=id,handle,images",
        headers={"X-Shopify-Access-Token": TOKEN})
    with urllib.request.urlopen(req) as r:
        p = json.load(r)["products"]
    if not p:
        sys.exit(f"no product {handle}")
    return [i["src"] for i in p[0]["images"]]


def fetch(url, dest):
    if dest.exists():
        return dest
    # ask the CDN for the biggest render — the composer crops to 1080x1350
    big = url.split("?")[0]
    big = big.replace(".jpg", "_2048x2048.jpg").replace(".png", "_2048x2048.png")
    for u in (big, url):
        try:
            urllib.request.urlretrieve(u, dest)
            return dest
        except Exception:
            continue
    sys.exit(f"could not fetch {url}")


SRC.mkdir(parents=True, exist_ok=True)
cache = {}
for prod, cards in SETS.items():
    d = OUT / prod
    d.mkdir(parents=True, exist_ok=True)
    for n, (handle, idx, eyebrow, headline, sub, cta) in enumerate(cards, 1):
        if handle not in cache:
            cache[handle] = images(handle)
        if idx >= len(cache[handle]):
            sys.exit(f"{handle} has no image #{idx}")
        src = fetch(cache[handle][idx], SRC / f"{handle}_{idx}.jpg")
        stem = f"{n}_{handle.split('-print')[0][:22]}.jpg"
        compose(str(src), str(d / stem), eyebrow, headline, sub, "PEXX", cta)
        # Story: same copy, 9:16, type lifted clear of Instagram's reply bar.
        (d / "story").mkdir(exist_ok=True)
        compose(str(src), str(d / "story" / stem), eyebrow, headline, sub, "PEXX",
                cta, size=(1080, 1920), lift=330)
        print("ok", stem)
print("\nDONE ->", OUT)
