#!/usr/bin/env python3
"""Publish one poddarexp.com journal post: body fragment + posts.json entry + pretty-URL shell.

The three files must stay in sync; that is the whole reason this exists.
Re-running with the same slug updates in place instead of duplicating.

  python3 new_bulk_post.py --meta meta.json --body body.html [--root /path/to/repo]
  python3 new_bulk_post.py --self-check

meta.json holds the posts.json entry (see references/formats.md). `id`, `file`
and `image` are filled in from the slug if absent.
"""
import argparse, json, pathlib, sys

SITE = "https://www.poddarexp.com"
REQUIRED = ["slug", "title", "seoTitle", "date", "readTime", "excerpt",
            "metaDescription", "imageAlt", "category", "keywords", "faq"]

SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | PEXX</title>
  <meta name="description" content="{desc}" />
  <meta property="og:title" content="{title} | PEXX" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{site}/blog/{slug}/" />
  <meta property="og:image" content="../..{image}" />
  <link rel="canonical" href="{site}/blog/{slug}/" />
  <meta http-equiv="refresh" content="0; url=../post.html?slug={slug}" />
</head>
<body>
  <p>Redirecting to the article... <a href="../post.html?slug={slug}">Open the post</a>.</p>
</body>
</html>
"""


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def publish(root, meta, body):
    root = pathlib.Path(root)
    slug = meta["slug"]
    missing = [k for k in REQUIRED if not meta.get(k)]
    if missing:
        raise SystemExit(f"meta.json is missing: {', '.join(missing)}")
    if not meta["faq"]:
        raise SystemExit("faq must have entries — it is the FAQPage structured data")
    meta.setdefault("id", slug)
    meta.setdefault("file", f"/posts/{slug}.html")
    meta.setdefault("image", f"/assets/blog/{slug}/hero.jpg")

    (root / "posts" / f"{slug}.html").write_text(body.rstrip() + "\n")

    posts_path = root / "data" / "posts.json"
    posts = json.loads(posts_path.read_text())
    posts = [p for p in posts if (p.get("slug") or p.get("id")) != slug]
    posts.append(meta)
    posts.sort(key=lambda p: p.get("date", ""), reverse=True)
    posts_path.write_text(json.dumps(posts, indent=2, ensure_ascii=False) + "\n")

    shell_dir = root / "blog" / slug
    shell_dir.mkdir(parents=True, exist_ok=True)
    (shell_dir / "index.html").write_text(SHELL.format(
        title=esc(meta["title"]), desc=esc(meta["metaDescription"]),
        site=SITE, slug=slug, image=meta["image"]))

    return [f"posts/{slug}.html", "data/posts.json", f"blog/{slug}/index.html"]


def self_check():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = pathlib.Path(d)
        (root / "posts").mkdir()
        (root / "data").mkdir()
        (root / "data" / "posts.json").write_text(
            '[{"id":"old","slug":"old","date":"2026-01-01"}]')
        meta = {k: "x" for k in REQUIRED}
        meta.update(slug="test-post", date="2026-08-25", faq=[{"question": "q", "answer": "a"}])
        publish(root, dict(meta), "<p>Body</p>")
        publish(root, dict(meta), "<p>Body again</p>")  # rerun must not duplicate

        posts = json.loads((root / "data" / "posts.json").read_text())
        assert [p["slug"] for p in posts] == ["test-post", "old"], posts
        assert (root / "posts" / "test-post.html").read_text() == "<p>Body again</p>\n"
        shell = (root / "blog" / "test-post" / "index.html").read_text()
        assert "post.html?slug=test-post" in shell and "canonical" in shell

        bad = dict(meta); bad["faq"] = []
        try:
            publish(root, bad, "<p>x</p>")
        except SystemExit:
            pass
        else:
            raise AssertionError("empty faq must be rejected")
    print("self-check ok")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--meta")
    ap.add_argument("--body")
    ap.add_argument("--root", default=pathlib.Path(__file__).resolve().parents[4])
    ap.add_argument("--self-check", action="store_true")
    a = ap.parse_args()
    if a.self_check:
        self_check()
        sys.exit()
    if not (a.meta and a.body):
        ap.error("--meta and --body are required")
    written = publish(a.root, json.loads(pathlib.Path(a.meta).read_text()),
                      pathlib.Path(a.body).read_text())
    print("wrote:\n  " + "\n  ".join(written))
    print("\nImages still need copying into assets/blog/<slug>/ before this renders.")
