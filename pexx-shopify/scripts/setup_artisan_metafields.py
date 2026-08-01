#!/usr/bin/env python3
"""Create the product metafield definitions for artisan-at-product content
(see PRODUCTION-BUILD-PLAN.md §8.3). Definitions only — no values, no theme
block. Renders nothing until production fills in a name/photo per product.
Idempotent: skips any definition that already exists.

Run: python3 scripts/setup_artisan_metafields.py
"""
import os, json, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = open(os.path.join(ROOT, ".shopify-token")).read().strip()
SHOP = "pexx-7935.myshopify.com"
API = f"https://{SHOP}/admin/api/2025-01/graphql.json"

DEFINITIONS = [
    {"name": "Artisan name", "key": "artisan_name", "type": "single_line_text_field",
     "description": "Name of the artisan who made/printed this piece. Shown on PDP if set."},
    {"name": "Artisan photo", "key": "artisan_photo", "type": "file_reference",
     "description": "Photo of the artisan. Shown on PDP if set."},
    {"name": "Artisan video", "key": "artisan_video", "type": "file_reference",
     "description": "Optional short video of the artisan at work."},
]


def gql(query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(API, data=body,
        headers={"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


EXISTING_QUERY = """
{ metafieldDefinitions(first: 20, ownerType: PRODUCT, namespace: "pexx") { nodes { key name } } }
"""

CREATE_MUTATION = """
mutation($definition: MetafieldDefinitionInput!) {
  metafieldDefinitionCreate(definition: $definition) {
    createdDefinition { id name key }
    userErrors { field message }
  }
}
"""


def main():
    existing = gql(EXISTING_QUERY)
    existing_keys = {n["key"] for n in existing["data"]["metafieldDefinitions"]["nodes"]}

    print(f"{'key':20} {'status':10}")
    print("-" * 35)

    for d in DEFINITIONS:
        if d["key"] in existing_keys:
            print(f"{d['key']:20} {'VERIFIED':10} (already exists)")
            continue

        variables = {"definition": {
            "name": d["name"],
            "namespace": "pexx",
            "key": d["key"],
            "type": d["type"],
            "description": d["description"],
            "ownerType": "PRODUCT",
            "pin": True,
        }}
        r = gql(CREATE_MUTATION, variables)
        errors = r["data"]["metafieldDefinitionCreate"]["userErrors"]
        if errors:
            print(f"{d['key']:20} {'FAILED':10} {errors}")
            continue
        created = r["data"]["metafieldDefinitionCreate"]["createdDefinition"]
        print(f"{d['key']:20} {'CREATED':10} (id {created['id']})")


if __name__ == "__main__":
    main()
