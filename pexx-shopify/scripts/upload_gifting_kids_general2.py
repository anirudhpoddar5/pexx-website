#!/usr/bin/env python3
"""Upload the Kids gifting photos + remaining General photos (toilet kits, quilted tote)."""
import os, json, time, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = open(os.path.join(ROOT, ".shopify-token")).read().strip()
SHOP = "pexx-7935.myshopify.com"
GQL = f"https://{SHOP}/admin/api/2025-01/graphql.json"
REFS_PATH = os.path.join(ROOT, ".asset-refs.json")

KIDS_DIR = os.path.expanduser("~/Desktop/PEXX/ecom/Gifts_Kids")
GENERAL_DIR = os.path.expanduser("~/Desktop/PEXX/ecom/Gifts_General")

FILES = [
    (KIDS_DIR, "Gift_Kids_Swaddle.png", "kids-swaddle.png", "image/png"),
    (KIDS_DIR, "Gift_Kids_PencilBox.png", "kids-pencil-box.png", "image/png"),
    (KIDS_DIR, "Gifts_Kids_Utility_Pouch.png", "kids-utility-pouch.png", "image/png"),
    (KIDS_DIR, "Gift_Kids_Ipad_Notebook.png", "kids-ipad-notebook.png", "image/png"),
    (KIDS_DIR, "Gift_Kids_Backpack.png", "kids-backpack.png", "image/png"),
    (KIDS_DIR, "Gift_Kids_Quilt.png", "kids-quilt.png", "image/png"),
    (GENERAL_DIR, "Gfiting_Women_ToiletKit.png", "general-women-toiletkit.png", "image/png"),
    (GENERAL_DIR, "Gifting_Men_ToiletKit.png", "general-men-toiletkit.png", "image/png"),
    (GENERAL_DIR, "Gifting_Quilted_Tote.png", "general-quilted-tote.png", "image/png"),
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
      fileCreate(files:$files){ files{ id fileStatus ... on MediaImage { image{ url } } } userErrors{ message } } }"""
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
