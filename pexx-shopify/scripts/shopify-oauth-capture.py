#!/usr/bin/env python3
"""
One-shot OAuth callback server to capture a Shopify Admin API token.

Reads SHOP, CLIENT_ID, CLIENT_SECRET from env.
Serves http://localhost:3456/  -> redirects to Shopify authorize
Serves http://localhost:3456/callback -> exchanges code for token, writes .shopify-token

Run:  SHOP=pexx-7935.myshopify.com CLIENT_ID=xxx CLIENT_SECRET=yyy python3 scripts/shopify-oauth-capture.py
Then open the printed authorize URL in the browser (already logged into admin) and approve.
"""
import os, sys, json, secrets, urllib.parse, urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

SHOP = os.environ["SHOP"]
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
PORT = int(os.environ.get("PORT", "3456"))
SCOPES = "write_products,read_products,write_files,write_themes,write_content,write_online_store_navigation"
REDIRECT = f"http://localhost:{PORT}/callback"
STATE = secrets.token_hex(8)
TOKEN_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".shopify-token")

AUTH_URL = (
    f"https://{SHOP}/admin/oauth/authorize?client_id={CLIENT_ID}"
    f"&scope={urllib.parse.quote(SCOPES)}"
    f"&redirect_uri={urllib.parse.quote(REDIRECT)}&state={STATE}"
)

class H(BaseHTTPRequestHandler):
    def log_message(self, *a):  # quiet
        pass

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        if u.path == "/":
            self.send_response(302)
            self.send_header("Location", AUTH_URL)
            self.end_headers()
            return
        if u.path == "/callback":
            if q.get("state", [""])[0] != STATE:
                self._html("State mismatch — aborted."); return
            code = q.get("code", [""])[0]
            body = json.dumps({
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code,
            }).encode()
            req = urllib.request.Request(
                f"https://{SHOP}/admin/oauth/access_token",
                data=body, headers={"Content-Type": "application/json"})
            try:
                resp = json.loads(urllib.request.urlopen(req).read())
            except Exception as e:
                self._html(f"Token exchange failed: {e}"); return
            token = resp.get("access_token", "")
            with open(TOKEN_PATH, "w") as f:
                f.write(token)
            self._html("✓ PEXX connected. Token captured. You can close this tab.")
            print("TOKEN_CAPTURED")
            sys.exit(0)
        self._html("Not found")

    def _html(self, msg):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(f"<html><body style='font-family:sans-serif;padding:3rem'><h2>{msg}</h2></body></html>".encode())

print("AUTHORIZE_URL:", AUTH_URL)
HTTPServer(("127.0.0.1", PORT), H).serve_forever()
