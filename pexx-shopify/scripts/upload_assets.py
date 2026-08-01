#!/usr/bin/env python3
"""Upload brand images to Shopify Files; print their reference paths for theme settings."""
import os, json, time, subprocess, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = open(os.path.join(ROOT, ".shopify-token")).read().strip()
SHOP = "pexx-7935.myshopify.com"
GQL = f"https://{SHOP}/admin/api/2025-01/graphql.json"

FILES = [
    ("logo-pexx.png", "image/png"),
    ("hero-pexx.jpeg", "image/jpeg"),
]


def gql(query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(GQL, data=body,
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req).read())


def staged(fn, mime):
    q = """mutation($input:[StagedUploadInput!]!){
      stagedUploadsCreate(input:$input){ stagedTargets{ url resourceUrl parameters{ name value } } userErrors{ message } } }"""
    r = gql(q, {"input": [{"filename": fn, "mimeType": mime, "resource": "FILE", "httpMethod": "POST"}]})
    return r["data"]["stagedUploadsCreate"]["stagedTargets"][0]


def upload(target, path):
    args = ["curl", "-s", "-X", "POST", target["url"]]
    for p in target["parameters"]:
        args += ["-F", f"{p['name']}={p['value']}"]
    args += ["-F", f"file=@{path}"]
    subprocess.run(args, capture_output=True)


def file_create(resource_url):
    q = """mutation($files:[FileCreateInput!]!){
      fileCreate(files:$files){ files{ id fileStatus alt
        ... on MediaImage { image{ url } } } userErrors{ message } } }"""
    r = gql(q, {"files": [{"originalSource": resource_url, "contentType": "IMAGE"}]})
    return r["data"]["fileCreate"]["files"][0]


results = {}
created = []
for fn, mime in FILES:
    t = staged(fn, mime)
    upload(t, os.path.join(ROOT, fn))
    f = file_create(t["resourceUrl"])
    created.append((fn, f["id"]))
    print("uploaded:", fn, f["id"], f.get("fileStatus"))

# poll until READY and fetch url
time.sleep(4)
for fn, fid in created:
    q = """query($id:ID!){ node(id:$id){ ... on MediaImage { id fileStatus image{ url } } } }"""
    r = gql(q, {"id": fid})
    node = r["data"]["node"]
    url = (node.get("image") or {}).get("url", "")
    # derive shop_images reference from CDN filename
    base = url.split("/files/")[-1].split("?")[0] if "/files/" in url else fn
    ref = f"shopify://shop_images/{base}"
    results[fn] = ref
    print(f"{fn}: status={node.get('fileStatus')} ref={ref} url={url[:80]}")

open(os.path.join(ROOT, ".asset-refs.json"), "w").write(json.dumps(results, indent=2))
print("REFS", json.dumps(results))
