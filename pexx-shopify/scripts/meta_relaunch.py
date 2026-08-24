#!/usr/bin/env python3
"""One-shot repair of the Rakhi campaign (15 Aug 2026).

Three ads died on Meta error 2446289 ("the reel you've selected is not
available") - the Instagram post behind each creative vanished. Rebuilding the
creative from its own object_story_spec makes Meta mint a fresh post, which is
the whole fix. Also widens the ad set's optimisation event from
INITIATED_CHECKOUT (6 events/week - far too sparse to train on) to CONTENT_VIEW
(156 events/week).

Usage: python3 scripts/meta_relaunch.py [--go]     (dry run without --go)
"""
import json, sys, urllib.request, urllib.parse, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from meta_ads import ACT, API, TOKEN, get

ADSET = "120254016145160140"          # Metros_25plus_Broad
BROKEN = ["03_Quilt_SoftestThingInTheHouse",
          "04_Swaddle_ForTheNewestOne",
          "01_Backpack_PrintedByHand"]
UTM = {"utm_source": "meta", "utm_medium": "paid", "utm_campaign": "rakhi_2026"}
SLUG = {"03_Quilt_SoftestThingInTheHouse": "quilt",
        "04_Swaddle_ForTheNewestOne": "swaddle",
        "01_Backpack_PrintedByHand": "backpack"}

GO = "--go" in sys.argv


def post(path, **params):
    params["access_token"] = TOKEN
    req = urllib.request.Request(f"{API}/{path}",
                                 data=urllib.parse.urlencode(params).encode())
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Meta API error on {path}: {json.load(e).get('error', {})}")


def tagged(url, slug):
    """Normalise every link to carry the same UTMs (backpack already had them)."""
    parts = urllib.parse.urlsplit(url)
    q = dict(urllib.parse.parse_qsl(parts.query))
    q.update(UTM, utm_content=slug)
    return urllib.parse.urlunsplit(parts._replace(query=urllib.parse.urlencode(q)))


def main():
    ads = {a["name"]: a for a in get(
        f"{ACT}/ads", limit=100,
        fields="name,effective_status,creative{object_story_spec}").get("data", [])}

    for name in BROKEN:
        spec = ads[name]["creative"]["object_story_spec"]
        spec["link_data"]["link"] = tagged(spec["link_data"]["link"], SLUG[name])
        print(f"{name} -> {spec['link_data']['link']}")
        if not GO:
            continue
        cre = post(f"{ACT}/adcreatives", name=f"{name}_v2",
                   object_story_spec=json.dumps(spec))
        ad = post(f"{ACT}/ads", name=f"{name}_v2", adset_id=ADSET, status="ACTIVE",
                  creative=json.dumps({"creative_id": cre["id"]}))
        print(f"  created ad {ad['id']} on creative {cre['id']}")

    print("\nad set -> optimise for CONTENT_VIEW")
    if GO:
        pix = get(ADSET, fields="promoted_object")["promoted_object"]["pixel_id"]
        post(ADSET, promoted_object=json.dumps(
            {"pixel_id": pix, "custom_event_type": "CONTENT_VIEW"}))
        print("  done")

    if not GO:
        print("\nDRY RUN - nothing changed. Re-run with --go")


if __name__ == "__main__":
    main()
