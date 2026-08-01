#!/usr/bin/env python3
"""Push specific dwell-theme/ files to a theme via the Admin REST Asset API
and read each one back to confirm it matches — no `shopify theme` CLI.

Usage:
  python3 scripts/deploy_theme_assets.py [--theme-id ID] <path> [<path> ...]

Paths are relative to dwell-theme/, e.g.:
  python3 scripts/deploy_theme_assets.py layout/theme.liquid templates/page.about.json

Defaults --theme-id to the Dwell build theme (165377146969, see
SHOPIFY-BUILD.md). Only text assets (liquid/json/css/js/svg/…) are supported;
binary assets (images) should go through upload_assets.py / Files instead.
"""
import os, sys, json, time, base64, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEME_DIR = os.path.join(ROOT, "dwell-theme")
TOKEN_PATH = os.path.join(ROOT, ".shopify-token")
SHOP = "pexx-7935.myshopify.com"
API = f"https://{SHOP}/admin/api/2025-01"
DEFAULT_THEME_ID = 165377146969  # Dwell, build theme (unpublished)

BINARY_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".woff", ".woff2", ".ttf", ".ico"}


def strip_leading_comment(text):
    """Shopify's own JSON template convention allows a leading /* ... */
    editor note before the object — valid on push, but Shopify's API strips
    it on save and re-serializes the JSON (escaped slashes, expanded arrays).
    Strip it here too so we compare parsed JSON, not raw bytes."""
    stripped = text.lstrip()
    if stripped.startswith("/*"):
        end = stripped.find("*/")
        if end != -1:
            return stripped[end + 2:]
    return text


def fetch_asset(theme_id, key, token):
    return request("GET", f"/themes/{theme_id}/assets.json?asset%5Bkey%5D={_urlenc(key)}", token)


def check_token():
    if not os.path.exists(TOKEN_PATH):
        print(f"ERROR: {TOKEN_PATH} not found. Re-capture per SHOPIFY-BUILD.md (scripts/shopify-oauth-capture.py).")
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
    args = sys.argv[1:]
    theme_id = DEFAULT_THEME_ID
    if args and args[0] == "--theme-id":
        theme_id = int(args[1])
        args = args[2:]

    if not args:
        print(__doc__)
        raise SystemExit(1)

    token = check_token()

    # Confirm the token works and the theme exists before writing anything.
    s, body = request("GET", f"/themes/{theme_id}.json", token)
    if s != 200:
        print(f"ERROR: could not read theme {theme_id} (HTTP {s}): {body}")
        print("Check the token hasn't been revoked, and the theme id is correct.")
        raise SystemExit(1)
    theme_name = body["theme"]["name"]
    print(f"Target theme: {theme_name} (id {theme_id}, role {body['theme']['role']})\n")

    print(f"{'key':50} {'push':8} {'verify'}")
    print("-" * 80)

    failures = 0
    for rel_path in args:
        local_path = os.path.join(THEME_DIR, rel_path)
        key = rel_path.replace(os.sep, "/")
        ext = os.path.splitext(rel_path)[1].lower()

        if not os.path.exists(local_path):
            print(f"{key:50} {'FAIL':8} local file not found: {local_path}")
            failures += 1
            continue

        if ext in BINARY_EXT:
            with open(local_path, "rb") as f:
                content = f.read()
            asset = {"key": key, "attachment": base64.b64encode(content).decode()}
        else:
            with open(local_path, "r", encoding="utf-8") as f:
                content = f.read()
            asset = {"key": key, "value": content}

        s, r = request("PUT", f"/themes/{theme_id}/assets.json", token, {"asset": asset})
        if s not in (200, 201):
            print(f"{key:50} {'FAIL':8} push error (HTTP {s}): {r}")
            failures += 1
            continue
        pushed_size = r.get("asset", {}).get("size")
        print(f"{key:50} {'OK':8} pushed ({pushed_size} bytes) — verifying...", end=" ")

        # One retry: the Asset API has a brief read-after-write lag on plain
        # text assets often enough that a single immediate GET can be stale.
        vs, vr = fetch_asset(theme_id, key, token)
        if (vs != 200 or "asset" not in vr):
            time.sleep(1.5)
            vs, vr = fetch_asset(theme_id, key, token)
        if vs != 200 or "asset" not in vr:
            print(f"VERIFY FAILED (HTTP {vs})")
            failures += 1
            continue

        remote_value = vr["asset"].get("value")

        if ext in BINARY_EXT:
            remote_ok = vr["asset"].get("size") == pushed_size
            note = ""
        elif ext == ".json":
            # Shopify re-serializes JSON assets (strips any leading comment,
            # escapes slashes, reformats arrays) — compare parsed structure,
            # not bytes.
            try:
                remote_ok = json.loads(remote_value) == json.loads(strip_leading_comment(content))
            except json.JSONDecodeError as e:
                remote_ok = False
                note = f" (JSON parse error: {e})"
            else:
                note = " (semantic compare — Shopify reformats JSON on save)"
        else:
            remote_ok = remote_value == content
            if not remote_ok:
                time.sleep(1.5)
                _, vr2 = fetch_asset(theme_id, key, token)
                remote_ok = vr2.get("asset", {}).get("value") == content
            note = ""

        print(("MATCH" if remote_ok else "MISMATCH") + note)
        if not remote_ok:
            failures += 1

    print()
    if failures:
        print(f"{failures} file(s) failed to push/verify.")
        raise SystemExit(1)
    print("All files pushed and verified.")


def _urlenc(s):
    import urllib.parse
    return urllib.parse.quote(s, safe="")


if __name__ == "__main__":
    main()
