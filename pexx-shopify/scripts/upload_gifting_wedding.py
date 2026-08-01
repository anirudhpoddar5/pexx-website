#!/usr/bin/env python3
"""Upload the Wedding gifting photos (+ needed General-folder photos for the
Return Gifts gallery) to Shopify Files; merge refs into .asset-refs.json.
"""
import os, json, time, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = open(os.path.join(ROOT, ".shopify-token")).read().strip()
SHOP = "pexx-7935.myshopify.com"
GQL = f"https://{SHOP}/admin/api/2025-01/graphql.json"
REFS_PATH = os.path.join(ROOT, ".asset-refs.json")

WEDDING_DIR = os.path.expanduser("~/Desktop/ECOM Final/Gifts_Wedding")
GENERAL_DIR = os.path.expanduser("~/Desktop/ECOM Final/Gifts_General")

# (source dir, source filename, shop_images filename, mime type)
FILES = [
    (WEDDING_DIR, "Wedding_Welcome_Hamper.png", "wedding-welcome-hamper.png", "image/png"),
    (WEDDING_DIR, "Wedding_Haldi_Tote.png", "wedding-haldi-tote.png", "image/png"),
    (WEDDING_DIR, "Wedding_Mehendi_Potli.png", "wedding-mehendi-potli.png", "image/png"),
    (WEDDING_DIR, "Wedding_Baraat_Scarf_PocketSquare.png", "wedding-baraat-scarf-pocketsquare.png", "image/png"),
    (WEDDING_DIR, "Wedding_CoordSet_Close_Circle.png", "wedding-coordset-close-circle.png", "image/png"),
    (WEDDING_DIR, "Wedding_Kids_Goodies.png", "wedding-kids-goodies.png", "image/png"),
    (WEDDING_DIR, "Wedding_Return_Scarf_PocketSquare.png", "wedding-return-scarf-pocketsquare.png", "image/png"),
    (GENERAL_DIR, "Gifting_Table_Mat_Napkin.png", "general-table-mat-napkin.png", "image/png"),
    (GENERAL_DIR, "Giftig_Towel_Napkin_1.png", "general-towel-napkin-1.png", "image/png"),
    (GENERAL_DIR, "Gifting_women_jewellery_Pouch.png", "general-women-jewellery-pouch.png", "image/png"),
    (GENERAL_DIR, "Gifting_Quilts.png", "general-quilts.png", "image/png"),
]


def gql(query, variables=None):
    import urllib.request
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(GQL, data=body,
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req).read())


def staged(fn, mime):
    q = """mutation($input:[StagedUploadInput!]!){
      stagedUploadsCreate(input:$input){ stagedTargets{ url resourceUrl parameters{ name value } } userErrors{ message } } }"""
    r = gql(q, {"input": [{"filename": fn, "mimeType": mime, "resource": "FILE", "httpMethod": "POST"}]})
    errs = r["data"]["stagedUploadsCreate"]["userErrors"]
    if errs:
        raise RuntimeError(f"stagedUploadsCreate errors for {fn}: {errs}")
    return r["data"]["stagedUploadsCreate"]["stagedTargets"][0]


def upload(target, path):
    args = ["curl", "-s", "-X", "POST", target["url"]]
    for p in target["parameters"]:
        args += ["-F", f"{p['name']}={p['value']}"]
    args += ["-F", f"file=@{path}"]
    subprocess.run(args, capture_output=True, check=True)


def file_create(resource_url):
    q = """mutation($files:[FileCreateInput!]!){
      fileCreate(files:$files){ files{ id fileStatus alt
        ... on MediaImage { image{ url } } } userErrors{ message } } }"""
    r = gql(q, {"files": [{"originalSource": resource_url, "contentType": "IMAGE"}]})
    errs = r["data"]["fileCreate"]["userErrors"]
    if errs:
        raise RuntimeError(f"fileCreate errors: {errs}")
    return r["data"]["fileCreate"]["files"][0]


def main():
    created = []
    for src_dir, src_fn, shop_fn, mime in FILES:
        src_path = os.path.join(src_dir, src_fn)
        if not os.path.exists(src_path):
            print(f"SKIP (not found): {src_path}")
            continue
        t = staged(shop_fn, mime)
        upload(t, src_path)
        f = file_create(t["resourceUrl"])
        created.append((shop_fn, f["id"]))
        print("uploaded:", shop_fn, f["id"], f.get("fileStatus"))

    if not created:
        print("Nothing uploaded.")
        return

    time.sleep(4)
    existing = {}
    if os.path.exists(REFS_PATH):
        existing = json.loads(open(REFS_PATH).read())

    for shop_fn, fid in created:
        q = """query($id:ID!){ node(id:$id){ ... on MediaImage { id fileStatus image{ url } } } }"""
        node = {}
        for attempt in range(5):
            r = gql(q, {"id": fid})
            node = r["data"]["node"]
            if node.get("fileStatus") == "READY" and node.get("image"):
                break
            time.sleep(2)
        url = (node.get("image") or {}).get("url", "")
        base = url.split("/files/")[-1].split("?")[0] if "/files/" in url else shop_fn
        ref = f"shopify://shop_images/{base}"
        existing[shop_fn] = ref
        print(f"{shop_fn}: status={node.get('fileStatus')} ref={ref}")

    open(REFS_PATH, "w").write(json.dumps(existing, indent=2, sort_keys=True))
    print("Updated", REFS_PATH)


if __name__ == "__main__":
    main()
