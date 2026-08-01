#!/usr/bin/env python3
"""Ensure PEXX pillar Pages exist with the right handle + theme template.

Idempotent: existing pages with the correct template_suffix are left alone
and just reported as verified. Only missing pages are created (with
placeholder body + SEO description); only wrong template_suffix values are
corrected. See PRODUCTION-BUILD-PLAN.md §9C for the page list.

Run: python3 scripts/setup_pages.py
"""
import os, json, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN_PATH = os.path.join(ROOT, ".shopify-token")
SHOP = "pexx-7935.myshopify.com"
API = f"https://{SHOP}/admin/api/2025-01"

# handle -> (title, template_suffix or None, placeholder body_html, meta description, create_if_missing)
PAGES = {
    "faq": ("FAQ", None, None, None, False),
    "gift-to-india": ("Send a Little Something Home", "gift-to-india", None, None, False),
    "return-gifts": ("Return Gifts Kids Actually Keep", "return-gifts", None, None, False),
    "about": ("Our Story", "about", None, None, False),
    "baby-gifting-guide": (
        "Baby Gifting Guide by Occasion",
        "baby-gifting-guide",
        "<p>Gift ideas for baby shower, naming ceremony and first birthday — see the full guide below.</p>",
        "Baby gift ideas by occasion: baby shower, naming ceremony, first birthday. Soft, azo-free, hand block-printed cotton from PEXX.",
        True,
    ),
    "fabric-safety": (
        "Fabric & Safety Hub",
        "fabric-safety",
        "<p>What our cotton is made of, how it's dyed, and how to wash and care for it — the full fabric &amp; safety reference below.</p>",
        "PEXX fabric and safety hub: azo-free dyes, 100% cotton, and how to wash and care for block-printed pieces safely.",
        True,
    ),
}


def check_token():
    if not os.path.exists(TOKEN_PATH):
        print(f"ERROR: {TOKEN_PATH} not found. Re-capture per SHOPIFY-BUILD.md "
              f"(scripts/shopify-oauth-capture.py).")
        raise SystemExit(1)
    token = open(TOKEN_PATH).read().strip()
    if not token:
        print(f"ERROR: {TOKEN_PATH} is empty.")
        raise SystemExit(1)
    return token


def request(method, path, token, body=None):
    url = f"{API}{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")


def main():
    token = check_token()

    status, body = request("GET", "/pages.json?limit=250", token)
    if status != 200:
        print(f"ERROR: could not list pages (HTTP {status}): {body}")
        print("Check token scopes include read_content/write_content, or that the token hasn't been revoked.")
        raise SystemExit(1)

    existing = {p["handle"]: p for p in body.get("pages", [])}

    print(f"{'handle':22} {'status':10} {'template_suffix'}")
    print("-" * 60)

    for handle, (title, template_suffix, placeholder_body, meta_description, create_if_missing) in PAGES.items():
        page = existing.get(handle)

        if page is None:
            if not create_if_missing:
                print(f"{handle:22} {'MISSING':10} (expected to already exist — check manually)")
                continue
            payload = {"page": {"title": title, "handle": handle, "body_html": placeholder_body or ""}}
            if template_suffix:
                payload["page"]["template_suffix"] = template_suffix
            s, r = request("POST", "/pages.json", token, payload)
            if s not in (200, 201):
                print(f"{handle:22} {'FAILED':10} create error (HTTP {s}): {r}")
                continue
            new_page = r["page"]
            print(f"{handle:22} {'CREATED':10} {new_page.get('template_suffix')}")

            if meta_description:
                mf_payload = {"metafield": {
                    "namespace": "global", "key": "description_tag",
                    "type": "single_line_text_field", "value": meta_description,
                }}
                ms, mr = request("POST", f"/pages/{new_page['id']}/metafields.json", token, mf_payload)
                if ms not in (200, 201):
                    print(f"  -> meta description NOT set (HTTP {ms}): {mr}")
                else:
                    print(f"  -> meta description set ({len(meta_description)} chars)")
            continue

        # Page exists — verify (and only correct) template_suffix.
        current = page.get("template_suffix")
        if template_suffix is None:
            print(f"{handle:22} {'VERIFIED':10} {current!r} (no template change expected)")
        elif current == template_suffix:
            print(f"{handle:22} {'VERIFIED':10} {current}")
        else:
            s, r = request("PUT", f"/pages/{page['id']}.json", token,
                            {"page": {"id": page["id"], "template_suffix": template_suffix}})
            if s != 200:
                print(f"{handle:22} {'FAILED':10} could not fix template (HTTP {s}): {r}")
            else:
                print(f"{handle:22} {'CORRECTED':10} {current!r} -> {template_suffix}")

    print("\nNote: template_suffix only renders correctly once the matching")
    print("templates/page.<suffix>.json file has been pushed to the Dwell theme")
    print("(shopify theme push --path dwell-theme --store pexx-7935.myshopify.com --theme 165377146969).")


if __name__ == "__main__":
    main()
