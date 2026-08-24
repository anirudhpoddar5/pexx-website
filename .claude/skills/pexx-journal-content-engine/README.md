# How to run and change the content engine

Written for the owner, not for a developer.

## Running it

In Claude Code, in the `pexx-website` folder, type:

```
/pexx-journal-content-engine
```

Or just say what you want in plain English — "let's do the next journal drop",
"write this week's LinkedIn post" — and it loads itself.

Every run starts the same way: three bulk topic options and three retail topic
options, ranked, with a recommendation. **You pick. Nothing gets written until
you do.** Then it researches, writes both posts and the LinkedIn post, and
leaves them in `content-drafts/journal/<date>/` for you to read.

Nothing is ever published without you saying so.

## Changing it

Everything lives in `.claude/skills/pexx-journal-content-engine/`. These are
plain text files — you can edit them yourself, or tell Claude "change the
engine so that…" and it will.

| If you want to change… | Say so, or edit |
|---|---|
| The rules, the voice, what it must never do | `SKILL.md` |
| Which topics are in the pool, what has shipped, fixed dates | `references/calendar.md` |
| Which photos may be used where, the editing steps, export sizes | `references/images.md` |
| Numbers it may state without re-checking — lead times, GSM, dates | `references/facts.md` |
| The exact shape of a published post on either site | `references/formats.md` |
| Where posts get shared, and the free republishing list | `references/distribution.md` |
| The branded share-card template (screenshot it to post) | `assets/share-card.html` |
| How the three poddarexp files get written | `scripts/new_bulk_post.py` |

The most common changes, and where they go:

- **"Stop writing about X."** → add a line to §1 of `SKILL.md`. That's where
  the certification and audit instruction went.
- **"Add this topic."** → `references/calendar.md`, into the right pool.
- **"That number is wrong."** → `references/facts.md`. Fix it there once and
  every future post is correct.
- **"Don't use those photos."** → `references/images.md`.
- **"Change the cadence."** → top of `SKILL.md` and `references/calendar.md`.

After any run, the engine is supposed to update the calendar itself — topics
marked shipped, the next drop dated. If it forgets, tell it.

## Publishing, when a draft is approved

- **poddarexp.com** — Claude runs `scripts/new_bulk_post.py`, which writes the
  three files that have to stay in sync, then commits. The images still need
  exporting into `assets/blog/<slug>/` first.
- **shop.poddarexp.com** — the Shopify theme already has the blog templates.
  The article goes in through the admin or the API, after you approve it.
- **LinkedIn** — always posted by you, by hand. Link in the first comment,
  never in the post body.

## One thing worth fixing when there's time

Journal posts on poddarexp.com are assembled by JavaScript, and the tidy URL is
an empty page that redirects. Google manages this; several AI crawlers don't run
JavaScript and see nothing at all. Until that's fixed, the posts will
under-perform in AI answers on those engines — which is half the point of
writing them this way.
