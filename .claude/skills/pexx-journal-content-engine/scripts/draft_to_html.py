#!/usr/bin/env python3
"""Turn a drop draft (.md) into the article HTML both properties need.

The drafts are written once and then published twice — as a body fragment for
poddarexp.com and as Shopify article content. Hand-converting them was the
source of two divergences already, so this does it from the single source.

  python3 draft_to_html.py draft.md            # prints the article HTML
  python3 draft_to_html.py draft.md --faq      # prints the FAQ as JSON for posts.json
  python3 draft_to_html.py --self-check

What it handles, because that is all the drafts use: YAML-ish front matter,
## / ### headings, paragraphs, - bullets, 1. numbered lists, pipe tables,
> blockquotes, **bold**, *italic*, [links](url), and the review-only scaffolding
(the "Answer block" label, the FAQ section, the image brief, and any
"Still to confirm" / "Deliberately left out" notes) which never gets published.
"""
import argparse, html, json, pathlib, re, sys

# sections that exist for review and must never reach a published page
DROP_SECTIONS = ("image brief", "still to confirm", "deliberately left out",
                 "series plan", "series note", "internal links to set", "faq",
                 "notes", "note on", "checked against", "why an upgrade")


def split_front_matter(text):
    if not text.startswith("---"):
        return {}, text
    _, fm, body = text.split("---", 2)
    meta = {}
    for line in fm.splitlines():
        if ":" in line and not line.startswith((" ", "\t", "#")):
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, body


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", s)
    return s


def parse_faq(body):
    """FAQ section is **Question?** followed by the answer paragraph."""
    m = re.search(r"^##\s+FAQ\s*$(.*?)(?=^##\s|\Z)", body, re.S | re.M)
    if not m:
        return []
    out, q, buf = [], None, []
    for line in m.group(1).splitlines():
        qm = re.match(r"^\*\*(.+?)\*\*\s*$", line.strip())
        if qm:
            if q:
                out.append({"question": q, "answer": " ".join(buf).strip()})
            q, buf = qm.group(1), []
        elif line.strip():
            buf.append(line.strip())
    if q:
        out.append({"question": q, "answer": " ".join(buf).strip()})
    return out


def to_html(body):
    lines = body.splitlines()
    out, i, skip = [], 0, False
    para, bullets, numbers, table = [], [], [], []

    def flush():
        nonlocal para, bullets, numbers, table
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para = []
        if bullets:
            out.append("<ul>" + "".join(f"<li>{inline(b)}</li>" for b in bullets) + "</ul>")
            bullets = []
        if numbers:
            out.append("<ol>" + "".join(f"<li>{inline(n)}</li>" for n in numbers) + "</ol>")
            numbers = []
        if table:
            head, *rows = [r for r in table if not set(r.replace("|", "").strip()) <= set("-: ")]
            cells = lambda r, t: "".join(f"<{t}>{inline(c.strip())}</{t}>"
                                         for c in r.strip().strip("|").split("|"))
            out.append("<table><thead><tr>" + cells(head, "th") + "</tr></thead><tbody>"
                       + "".join("<tr>" + cells(r, "td") + "</tr>" for r in rows)
                       + "</tbody></table>")
            table = []

    while i < len(lines):
        line = lines[i]
        i += 1
        h = re.match(r"^(#{2,3})\s+(.*)$", line)
        if h:
            flush()
            title = h.group(2).strip()
            # the answer block is lifted out separately by convert(); drop it here
            low = title.lower().rstrip(":")
            # prefix match — a heading like "Still to confirm with the owner"
            # must be dropped just as surely as a bare "Still to confirm"
            skip = low == "answer block" or any(low.startswith(d) for d in DROP_SECTIONS)
            if skip:
                continue
            out.append(f"<h{len(h.group(1))}>{inline(title)}</h{len(h.group(1))}>")
            continue
        if skip:
            continue
        if line.startswith("```"):          # fenced blocks are review notes only
            while i < len(lines) and not lines[i].startswith("```"):
                i += 1
            i += 1
            continue
        if not line.strip():
            flush()
        elif line.strip() in ("---", "***"):
            flush()
        elif line.lstrip().startswith("|"):
            table.append(line)
        elif line.lstrip().startswith("> "):
            flush()
            out.append("<blockquote><p>" + inline(line.lstrip()[2:]) + "</p></blockquote>")
        elif re.match(r"^\s*[-*]\s+", line):
            if para:
                flush()
            bullets.append(re.sub(r"^\s*[-*]\s+", "", line))
        elif re.match(r"^\s*\d+\.\s+", line):
            if para:
                flush()
            numbers.append(re.sub(r"^\s*\d+\.\s+", "", line))
        elif (bullets or numbers) and line.startswith("  "):
            (bullets or numbers)[-1] += " " + line.strip()
        else:
            para.append(line.strip())
    flush()
    return "\n".join(out)


def convert(path):
    meta, body = split_front_matter(pathlib.Path(path).read_text())
    # the answer block is the lead paragraph, styled, before everything else
    am = re.search(r"^##\s+Answer block\s*$(.*?)(?=^##\s|^---\s*$)", body, re.S | re.M)
    lead = ""
    if am:
        text = " ".join(l.strip() for l in am.group(1).strip().splitlines() if l.strip())
        lead = f'<p class="answer-block"><strong>{inline(text)}</strong></p>\n'
    return meta, lead + to_html(body), parse_faq(body)


def self_check():
    src = """---
title: T
slug: s
---

## Answer block

Short answer here.

---

Opening line.

## A heading

Body with **bold** and a [link](/x).

- one
- two

| A | B |
|---|---|
| 1 | 2 |

## FAQ

**Is it fast?**
Yes it is.

**Really?**
Really.

## Image brief

```
HERO — do not publish
```

## Still to confirm with the owner

1. nothing, ask the owner
"""
    p = pathlib.Path("/tmp/_draft_check.md")
    p.write_text(src)
    meta, out, faq = convert(p)
    assert meta["title"] == "T"
    assert 'class="answer-block"' in out
    assert out.count("Short answer here.") == 1, "answer block must appear once"
    assert "<h2>A heading</h2>" in out
    assert "<strong>bold</strong>" in out and '<a href="/x">link</a>' in out
    assert "<ul><li>one</li><li>two</li></ul>" in out
    assert "<table>" in out and "<th>A</th>" in out and "<td>2</td>" in out
    assert "Image brief" not in out and "do not publish" not in out
    assert "Still to confirm" not in out and "nothing" not in out
    assert "owner" not in out.lower(), "review notes must never reach the page"
    assert "<h2>FAQ</h2>" not in out, "FAQ is data, not body copy"
    assert faq == [{"question": "Is it fast?", "answer": "Yes it is."},
                   {"question": "Really?", "answer": "Really."}], faq
    p.unlink()
    print("self-check ok")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("draft", nargs="?")
    ap.add_argument("--faq", action="store_true", help="print the FAQ as JSON")
    ap.add_argument("--self-check", action="store_true")
    a = ap.parse_args()
    if a.self_check:
        self_check(); sys.exit()
    if not a.draft:
        ap.error("give me a draft path")
    meta, body, faq = convert(a.draft)
    print(json.dumps(faq, indent=2, ensure_ascii=False) if a.faq else body)
