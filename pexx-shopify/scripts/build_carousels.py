#!/usr/bin/env python3
"""Build 4 product carousel ads on Meta — one per product line, ALL PAUSED.

Each carousel card = a different in-stock print showing a DIFFERENT USE, and
each card links to its own product page (not a collection). Targeting differs
per product by real Meta parent-segments matched to the child age the product
actually suits.

Nothing here spends money: campaign, ad sets and ads are all created PAUSED.
Run with --delete to tear the whole thing back down.
"""
import json, sys, urllib.parse, urllib.request, pathlib

ACT   = "act_1350379969884972"
API   = "https://graph.facebook.com/v21.0"
PAGE  = "1277364825452418"
IG    = "17841408830237947"
PIXEL = "1952609352110587"
TOKEN = (pathlib.Path(__file__).parent.parent / ".meta-token").read_text().strip()
P     = json.load(open("/tmp/P.json"))

# Meta family_statuses segments, looked up live from the targeting API.
SEG = {
    "all":        "6002714398372",  # Parents (All)
    "0_12m":      "6023005372383",  # up to 12 months
    "toddler":    "6023005458383",  # 1-2
    "preschool":  "6023005529383",  # 3-5
    "primary":    "6023005570783",  # 6-8
}


def call(path, **params):
    params["access_token"] = TOKEN
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(f"{API}/{path}", data=data)
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        err = json.load(e).get("error", {})
        sys.exit(f"FAIL {path}: {err.get('error_user_msg') or err.get('message')}")


CREATIVE_DIR = pathlib.Path(
    "/private/tmp/claude-501/-Users-anirudhpoddar-Downloads-pexx-website/"
    "92833a19-be73-4b84-950b-e5b33b57946d/scratchpad/FINAL")
_hash_cache = {}


def upload(path):
    """Upload a composed 1080x1350 creative and return its image_hash.

    The cards must use the COMPOSED files (headline/price/wordmark burned in),
    not the bare Shopify product photo — a plain catalogue shot is not an ad.
    """
    path = str(path)
    if path in _hash_cache:
        return _hash_cache[path]
    import subprocess
    r = subprocess.run(["curl", "-s", "-X", "POST",
                        f"{API}/{ACT}/adimages",
                        "-F", f"filename=@{path}",
                        "-F", f"access_token={TOKEN}"],
                       capture_output=True, text=True, check=True)
    d = json.loads(r.stdout)
    if "images" not in d:
        sys.exit(f"image upload failed for {path}: {d}")
    h = list(d["images"].values())[0]["hash"]
    _hash_cache[path] = h
    return h


def card(handle, img_idx, label, use, prod=None, pos=None):
    """One carousel card: composed creative, its own product link, UTMs."""
    files = sorted(CREATIVE_DIR.joinpath(prod).glob("*.jpg"))
    return {
        "link": f"https://shop.poddarexp.com/products/{handle}"
                f"?utm_source=meta&utm_medium=paid&utm_campaign=producttest&utm_content={handle}",
        "name": label[:40],
        "description": use[:30],
        "image_hash": upload(files[pos]),
        "call_to_action": {"type": "SHOP_NOW"},
    }


# ---------------------------------------------------------------- the 4 ads
# card order matters: card 1 leads with the PRINT as hero, then one use each.
ADS = {
"quilt": dict(
  budget=30000, age=(24, 42), segs=["0_12m", "toddler", "preschool"],
  headline="Hand block-printed. From ₹999.",
  desc="Reversible · COD",
  # Owner confirmed 21 Aug: skin-safe/azo-free is true across the range, partial
  # test reports held and shared with buyers on request.
  body=("₹999 · COD · free shipping over ₹750. One quilt, four ways — cot, play "
        "mat, pram, picnic floor.\n\n"
        "Hand block-printed in Jaipur on 100% cotton. Reversible, so it's two "
        "quilts in one. Skin-safe dyes. Machine wash — softer every time.\n\n"
        "100x100 ₹999 · 110x150 ₹1,299 · 10-day returns"),
  cards=[
    ("bunny-floral-print-baby-quilt",      4, "Bunny Floral",   "₹999 · 100cm"),
    ("orange-dachshund-print-baby-quilt",  1, "Orange Dachshund","In the cot"),
    ("bear-print-baby-quilt",              0, "Bear Print",    "As a play mat"),
    ("frog-pond-print-kids-quilt",         1, "Frog Pond",      "Wrapped up"),
    ("blush-unicorn-print-kids-quilt",     2, "Blush Unicorn",  "₹1,299 · large"),
  ]),

"swaddle": dict(
  budget=15000, age=(24, 38), segs=[],
  headline="2 muslin swaddles. ₹999.",
  desc="Pure cotton · COD",
  body=("2 swaddles ₹999 · COD · free shipping over ₹750. Muslin that actually "
        "breathes, for the 0–6 month stretch.\n\n"
        "Hand block-printed on pure cotton with skin-safe dyes. Big enough to "
        "wrap properly, light enough for an Indian summer.\n\n"
        "Made in Jaipur · 10-day returns"),
  cards=[
    ("unicorn-dolphin-swaddle-set",   3, "Unicorn & Dolphin", "The print"),
    ("sunburst-polka-dot-swaddle-set",3, "Sunburst & Dot",    "Swaddled, asleep"),
    ("bear-circus-animal-swaddle-set",0, "Bear & Circus",     "2 prints per set"),
    ("bunny-floral-stripe-swaddle-set",1,"Bunny Floral",      "Newborn size"),
    ("unicorn-dolphin-swaddle-set",   0, "Unicorn & Dolphin", "2-pack"),
  ]),

"pouch": dict(
  budget=15000, age=(24, 45), segs=["toddler", "preschool", "primary"],
  headline="Three pouches. ₹1,199.",
  desc="All 3 sizes · COD",
  body=("All three for ₹1,199 · COD · free shipping over ₹750.\n\n"
        "Three sizes that nest, so they pack flat. Toothbrush in the small, "
        "crayons in the medium, everything else in the large.\n\n"
        "Hand block-printed cotton, wipe-clean lining, proper zips. "
        "Made in Jaipur · 10-day returns"),
  cards=[
    ("rainbow-butterfly-toiletry-pouch-set", 0, "Rainbow Butterfly", "All 3 sizes"),
    ("teal-penguin-toiletry-pouch-set",      2, "Teal Penguin",      "Packed to travel"),
    ("frog-pond-toiletry-pouch-set",         0, "Frog Pond",         "Bathroom shelf"),
    ("monkey-print-toiletry-pouch-set",      2, "Monkey",            "Crayons + colours"),
    ("pastel-bear-toiletry-pouch-set",       4, "Pastel Bear",       "Mum's own too"),
  ]),

"backpack": dict(
  budget=15000, age=(24, 45), segs=["preschool", "primary"],
  headline="Light enough to carry themselves.",
  desc="₹999 · COD",
  # Claims kept to what the PDPs actually say: zip closure + front pocket,
  # azo-free/skin-safe dyes. No "padded straps" (on no product) and no side
  # bottle pocket (Penguin only).
  body=("₹999 · COD · free shipping over ₹750. Light enough for a three-year-old "
        "to carry on their own.\n\n"
        "Hand block-printed quilted cotton, not stiff nylon. Secure zip closure "
        "and a front pocket. Skin-safe azo-free dyes.\n\n"
        "For the day out, the sleepover at Nani's · 10-day returns"),
  cards=[
    ("monkey-print-kids-backpack",       2, "Monkey",       "The print"),
    ("pastel-bear-print-kids-backpack",  0, "Pastel Bear",  "Worn, age 4"),
    ("bunny-floral-print-kids-backpack", 4, "Bunny Floral", "Out for the day"),
    ("penguin-print-kids-backpack",      4, "Penguin",      "Bottle + pencils"),
    ("submarine-print-kids-backpack",    3, "Submarine",    "Cotton, not nylon"),
  ]),
}


def main():
    if "--delete" in sys.argv:
        cid = sys.argv[sys.argv.index("--delete") + 1]
        print(call(cid, status="DELETED"))
        return

    # sanity: every card's product must be in stock and have that image
    for k, a in ADS.items():
        for h, i, lbl, use in a["cards"]:
            if h not in P:            sys.exit(f"{k}: unknown handle {h}")
            if P[h]["inv"] <= 0:      sys.exit(f"{k}: {h} is OUT OF STOCK")
            if i >= len(P[h]["imgs"]):sys.exit(f"{k}: {h} has no image #{i}")
    print("stock + image check passed\n")

    camp = call(f"{ACT}/campaigns",
                name="PEXX_Sales_ProductTest_Aug2026",
                objective="OUTCOME_SALES", status="PAUSED",
                special_ad_categories="[]",
                # OFF on purpose: sharing moves 20% between ad sets, which would
                # contaminate the whole point of this build — a clean per-product read.
                is_adset_budget_sharing_enabled="false")
    print("campaign", camp["id"])

    out = {"campaign": camp["id"], "adsets": {}}
    for key, a in ADS.items():
        tgt = {
            "geo_locations": {"countries": ["IN"]},
            "age_min": a["age"][0], "age_max": a["age"][1],
            "publisher_platforms": ["facebook", "instagram"],
            "facebook_positions": ["feed"],
            "instagram_positions": ["stream", "explore"],
            "device_platforms": ["mobile", "desktop"],
            # OFF: expansion would override the per-product age segments that are
            # the entire point here. 18 Aug incident — expansion spent on 18-24
            # and 55+ and returned nothing.
            "targeting_automation": {"advantage_audience": 0},
        }
        if a["segs"]:
            tgt["family_statuses"] = [{"id": SEG[x], "name": x} for x in a["segs"]]
        aset = call(f"{ACT}/adsets",
            name=f"PT_{key}_parents_{a['age'][0]}to{a['age'][1]}",
            campaign_id=camp["id"], status="PAUSED",
            daily_budget=a["budget"], billing_event="IMPRESSIONS",
            optimization_goal="OFFSITE_CONVERSIONS",
            bid_strategy="LOWEST_COST_WITHOUT_CAP",
            promoted_object=json.dumps({"pixel_id": PIXEL,
                                        "custom_event_type": "ADD_TO_CART"}),
            targeting=json.dumps(tgt))

        spec = {"page_id": PAGE, "instagram_user_id": IG, "link_data": {
            "link": "https://shop.poddarexp.com/collections/all",
            "message": a["body"], "name": a["headline"],
            "description": a["desc"], "multi_share_optimized": False,
            "child_attachments": [card(*c, prod=key, pos=i)
                                  for i, c in enumerate(a["cards"])],
            "call_to_action": {"type": "SHOP_NOW"}}}
        cre = call(f"{ACT}/adcreatives",
                   name=f"PT_{key}_carousel", object_story_spec=json.dumps(spec))
        ad = call(f"{ACT}/ads", name=f"PT_{key}_carousel",
                  adset_id=aset["id"], creative=json.dumps({"creative_id": cre["id"]}),
                  status="PAUSED")
        out["adsets"][key] = {"adset": aset["id"], "creative": cre["id"], "ad": ad["id"],
                              "budget": a["budget"] // 100}
        print(f"  {key:9s} adset={aset['id']} ad={ad['id']} Rs{a['budget']//100}/day")

    json.dump(out, open("/tmp/built.json", "w"), indent=2)
    total = sum(v["budget"] for v in out["adsets"].values())
    print(f"\nALL PAUSED. Total if enabled: Rs {total}/day")


if __name__ == "__main__":
    main()
