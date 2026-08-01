// Pre-import catalog QA: reads a product CSV (our import template, see
// content-drafts/PRODUCT-IMPORT-TEMPLATE.csv, or a real Shopify product
// export) and flags rows/products missing an image, a price, or the
// age/occasion tags the Little/Occasion filters depend on.
// See PRODUCTION-BUILD-PLAN.md §8.1 ("Post-import QA script") and §9C.
//
// This is a read-only check — it never calls the Shopify API or writes
// anything, so it's safe to run anytime, including before an import.
//
// Run:
//   node scripts/checkCatalog.ts [path/to/products.csv]
// Defaults to content-drafts/PRODUCT-IMPORT-TEMPLATE.csv if no path given.

import { readFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const DEFAULT_CSV = join(ROOT, "content-drafts", "PRODUCT-IMPORT-TEMPLATE.csv");

type Row = Record<string, string>;

// Minimal RFC4180-ish CSV parser: handles quoted fields containing commas,
// newlines, and doubled-quote escapes (""). No dependency needed for this.
function parseCsv(text: string): Row[] {
  const rows: string[][] = [];
  let field = "", row: string[] = [], inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (inQuotes) {
      if (c === '"') {
        if (text[i + 1] === '"') { field += '"'; i++; }
        else inQuotes = false;
      } else field += c;
    } else if (c === '"') {
      inQuotes = true;
    } else if (c === ",") {
      row.push(field); field = "";
    } else if (c === "\n" || c === "\r") {
      if (c === "\r" && text[i + 1] === "\n") i++;
      row.push(field); field = "";
      if (row.some((cell) => cell.length > 0) || row.length > 1) rows.push(row);
      row = [];
    } else {
      field += c;
    }
  }
  if (field.length > 0 || row.length > 0) { row.push(field); rows.push(row); }

  const [header, ...body] = rows;
  return body.map((cells) => {
    const obj: Row = {};
    header.forEach((h, idx) => (obj[h.trim()] = (cells[idx] ?? "").trim()));
    return obj;
  });
}

function firstNonBlank(rows: Row[], key: string): string {
  for (const r of rows) if (r[key]) return r[key];
  return "";
}

// Supports our own template columns (Age/Occasion/Main Image/Price) and, as
// a fallback, a real Shopify export shape (Tags/Image Src/Variant Price).
function pick(row: Row, ...keys: string[]): string {
  for (const k of keys) if (row[k]) return row[k];
  return "";
}

function extractTag(tags: string, prefix: string): string {
  return tags
    .split(",")
    .map((t) => t.trim())
    .find((t) => t.toLowerCase().startsWith(prefix))
    ?.slice(prefix.length) ?? "";
}

function main() {
  const csvPath = process.argv[2] ? join(process.cwd(), process.argv[2]) : DEFAULT_CSV;
  if (!existsSync(csvPath)) {
    console.error(`ERROR: CSV not found at ${csvPath}`);
    process.exit(1);
  }

  const rows = parseCsv(readFileSync(csvPath, "utf8"));
  if (rows.length === 0) {
    console.error(`ERROR: ${csvPath} has no data rows.`);
    process.exit(1);
  }

  const byHandle = new Map<string, Row[]>();
  for (const row of rows) {
    const handle = pick(row, "Handle");
    if (!handle) continue;
    if (!byHandle.has(handle)) byHandle.set(handle, []);
    byHandle.get(handle)!.push(row);
  }

  let errorCount = 0, warnCount = 0;
  let missingImage = 0, missingOrZeroPrice = 0, missingType = 0, missingAgeOnLittle = 0, missingOccasion = 0;

  console.log(`Checking ${byHandle.size} products from ${csvPath}\n`);

  for (const [handle, variantRows] of byHandle) {
    const title = firstNonBlank(variantRows, "Title") || handle;
    const collection = firstNonBlank(variantRows, "Collection");
    const type = pick(variantRows[0], "Type", "Product Type");
    const tags = pick(variantRows[0], "Tags");
    const age = pick(variantRows[0], "Age") || extractTag(tags, "age_");
    const occasion = pick(variantRows[0], "Occasion") || extractTag(tags, "occasion_");

    const hasImage = variantRows.some((r) => pick(r, "Main Image", "Image Src", "Image 2", "Image 3", "Image 4"));
    const badPriceRows = variantRows.filter((r) => {
      const raw = pick(r, "Price", "Variant Price");
      const n = parseFloat(raw);
      return !raw || Number.isNaN(n) || n <= 0;
    });

    const issues: string[] = [];
    if (!hasImage) { issues.push("ERROR: no image on any variant row"); errorCount++; missingImage++; }
    if (badPriceRows.length > 0) { issues.push(`ERROR: missing/zero price on ${badPriceRows.length} variant row(s)`); errorCount++; missingOrZeroPrice++; }
    if (!type) { issues.push("WARN: Type not set"); warnCount++; missingType++; }
    if (collection.toLowerCase().includes("little") && !age) {
      issues.push("WARN: Little-collection item has no Age tag"); warnCount++; missingAgeOnLittle++;
    }
    if (!occasion) missingOccasion++; // informational only, not every product needs one

    if (issues.length > 0) {
      console.log(`- ${title} (${handle})`);
      for (const issue of issues) console.log(`    ${issue}`);
    }
  }

  console.log("\nSummary");
  console.log("-".repeat(40));
  console.log(`Products checked:            ${byHandle.size}`);
  console.log(`Missing image:                ${missingImage}`);
  console.log(`Missing/zero price (rows):    ${missingOrZeroPrice}`);
  console.log(`Missing Type:                 ${missingType}`);
  console.log(`Little items missing Age:     ${missingAgeOnLittle}`);
  console.log(`Products with no Occasion:    ${missingOccasion} (informational — not every product needs one)`);
  console.log(`\n${errorCount} error(s), ${warnCount} warning(s).`);

  if (errorCount > 0) process.exit(1);
}

main();
