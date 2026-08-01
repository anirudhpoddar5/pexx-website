#!/usr/bin/env python3
"""Update the store's main-menu with PEXX nav: Little, Carry, Gifting (+ Journal, About)."""
import os, json, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = open(os.path.join(ROOT, ".shopify-token")).read().strip()
SHOP = "pexx-7935.myshopify.com"
GQL = f"https://{SHOP}/admin/api/2025-01/graphql.json"


def gql(query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(GQL, data=body,
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req).read())


# find main-menu
r = gql("{ menus(first:20){ nodes{ id handle title } } }")
menus = r["data"]["menus"]["nodes"]
main = next((m for m in menus if m["handle"] == "main-menu"), None)
print("menus:", [m["handle"] for m in menus])
if not main:
    print("main-menu not found"); raise SystemExit(1)

items = [
    {"title": "Little", "type": "HTTP", "url": "/collections/little"},
    {"title": "Carry", "type": "HTTP", "url": "/collections/carry"},
    {"title": "Gifting", "type": "HTTP", "url": "/collections/gifting"},
    {"title": "Journal", "type": "HTTP", "url": "/blogs/news"},
    {"title": "About", "type": "HTTP", "url": "/pages/about"},
]

m = """
mutation($id:ID!,$title:String!,$handle:String!,$items:[MenuItemUpdateInput!]!){
  menuUpdate(id:$id,title:$title,handle:$handle,items:$items){
    menu{ id items{ title url } } userErrors{ field message }
  }
}"""
res = gql(m, {"id": main["id"], "title": "Main menu", "handle": "main-menu", "items": items})
out = res.get("data", {}).get("menuUpdate", {})
print("errors:", out.get("userErrors"))
print("items:", [i["title"] for i in out.get("menu", {}).get("items", [])] if out.get("menu") else res)
