// Apply legacy URL redirects (scripts/redirects.csv) to the PEXX Shopify store
// via the Admin REST API. Idempotent: skips any path that already has a
// redirect. See PRODUCTION-BUILD-PLAN.md §9B ("Legacy redirect map").
//
// Run (preview only, no writes):
//   node scripts/applyRedirects.ts --dry-run
// Run (creates redirects for real):
//   node scripts/applyRedirects.ts
//
// Requires Node 22.6+ (native TS support) or Node 24 (used elsewhere in this
// repo) — no build step, no npm dependencies.

import { readFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const TOKEN_PATH = join(ROOT, ".shopify-token");
const CSV_PATH = join(ROOT, "scripts", "redirects.csv");
const SHOP = "pexx-7935.myshopify.com";
const API = `https://${SHOP}/admin/api/2025-01`;

type Row = { path: string; target: string };

function parseCsv(text: string): Row[] {
  const lines = text.split(/\r?\n/).filter((l) => l.trim().length > 0);
  const [header, ...rows] = lines;
  const cols = header.split(",").map((c) => c.trim().toLowerCase());
  const pathIdx = cols.indexOf("path");
  const targetIdx = cols.indexOf("target");
  if (pathIdx === -1 || targetIdx === -1) {
    throw new Error(`CSV header must have "path" and "target" columns, got: ${header}`);
  }
  return rows.map((line) => {
    const cells = line.split(",");
    return { path: cells[pathIdx].trim(), target: cells[targetIdx].trim() };
  });
}

async function shopifyFetch(token: string, path: string, init: RequestInit = {}) {
  const res = await fetch(`${API}${path}`, {
    ...init,
    headers: {
      "X-Shopify-Access-Token": token,
      "Content-Type": "application/json",
      ...init.headers,
    },
  });
  const body = await res.json().catch(() => ({}));
  return { status: res.status, body };
}

async function main() {
  const dryRun = process.argv.includes("--dry-run");

  if (!existsSync(TOKEN_PATH)) {
    console.error(`ERROR: ${TOKEN_PATH} not found. Re-capture per SHOPIFY-BUILD.md (scripts/shopify-oauth-capture.py).`);
    process.exit(1);
  }
  const token = readFileSync(TOKEN_PATH, "utf8").trim();
  if (!token) {
    console.error(`ERROR: ${TOKEN_PATH} is empty.`);
    process.exit(1);
  }

  if (!existsSync(CSV_PATH)) {
    console.error(`ERROR: ${CSV_PATH} not found.`);
    process.exit(1);
  }
  const rows = parseCsv(readFileSync(CSV_PATH, "utf8"));

  // Confirm the token actually works before doing anything else.
  const shopCheck = await shopifyFetch(token, "/shop.json");
  if (shopCheck.status !== 200) {
    console.error(`ERROR: token check failed (HTTP ${shopCheck.status}). ${JSON.stringify(shopCheck.body)}`);
    console.error("Token may be revoked/expired — re-capture per SHOPIFY-BUILD.md.");
    process.exit(1);
  }

  console.log(`${"path".padEnd(24)} ${"status".padEnd(10)} target`);
  console.log("-".repeat(70));

  for (const { path, target } of rows) {
    if (!path || !target) {
      console.log(`${path.padEnd(24)} ${"SKIPPED".padEnd(10)} (blank path or target)`);
      continue;
    }

    const existing = await shopifyFetch(token, `/redirects.json?path=${encodeURIComponent(path)}`);
    if (existing.status !== 200) {
      console.log(`${path.padEnd(24)} ${"FAILED".padEnd(10)} lookup error (HTTP ${existing.status})`);
      continue;
    }
    const found = (existing.body as any).redirects ?? [];
    if (found.length > 0) {
      console.log(`${path.padEnd(24)} ${"EXISTS".padEnd(10)} -> ${found[0].target}`);
      continue;
    }

    if (dryRun) {
      console.log(`${path.padEnd(24)} ${"WOULD-CREATE".padEnd(10)} -> ${target}`);
      continue;
    }

    const created = await shopifyFetch(token, "/redirects.json", {
      method: "POST",
      body: JSON.stringify({ redirect: { path, target } }),
    });
    if (created.status === 200 || created.status === 201) {
      console.log(`${path.padEnd(24)} ${"CREATED".padEnd(10)} -> ${target}`);
    } else {
      console.log(`${path.padEnd(24)} ${"FAILED".padEnd(10)} (HTTP ${created.status}) ${JSON.stringify(created.body)}`);
    }
  }

  console.log("\nNot included in this CSV (needs a decision first, see PRODUCTION-BUILD-PLAN.md §9B):");
  console.log("  /blog/* and /posts/* -> /blogs/journal — Shopify redirects match exact paths;");
  console.log("  confirm wildcard support for this shop/API version, or list real old post URLs");
  console.log("  for per-article redirects, before adding them here.");
}

main().catch((err) => {
  console.error("ERROR:", err);
  process.exit(1);
});
