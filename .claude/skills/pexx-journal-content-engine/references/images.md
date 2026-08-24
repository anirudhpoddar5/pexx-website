# The photo library — what exists, what's usable, what it needs

Library: `~/Desktop/PEXX/photo-library` — 30 folders, ~3,000 stills
(1,961 jpg · 527 png · 434 jpeg · 82 webp), 19 video files, 6.1 GB. Roughly 70% of frames are 2500px or wider. Audited
22 Aug 2026 by opening every folder; re-audit if the folder changes shape.

**Standing owner instruction: nothing is published straight from this folder.
Every frame is edited first.**

---

## Tier A — process photography. Publish anywhere.

`Printing Classes/` — 83 stills, 4 videos.

Hands drawing a repeat. Carved blocks held to camera. Dye buckets in yellow,
blue, magenta. Printers working down the table. Workshop guests with ink on
their hands. Block detail. A printed motif sheet drying.

This is the most valuable imagery in the business: it is what makes a buyer
believe you make things, and it is the hardest kind of photo to fake — which
matters because the site publishes *How to Identify Genuine Hand Block Printed
Fabric*.

- **Use:** every bulk post, every LinkedIn post, the About page, hero images.
- **Catch:** about half are 960×1280 WhatsApp compressions — fine to 1200px
  wide, no further. The 3024×3024 frames are the hero set.

## Tier B — catalogue documentation. Edit hard, then use.

`Home Bed/` (444) · `Home Quilts/` (216) · `Kids Quilts/` (231) ·
`Kids dohar/` (115) · `Home Dohar/` (96) · `Home Cushions/` (64) ·
`Home Dhurries/` (69) · `Home Gudri/` (32) · `Acc Bags Pouches/` (219) ·
`Fair photos/` (32, showroom set shots on an office floor)

~1,500 frames of product laid flat on artificial green turf with a handwritten
label card in shot — *"Dohar Sqe-Single"*, *"Bed Sheet SS"*, *"Cushion Cover
16×16"*. As internal line sheets they are excellent: complete, consistent,
correctly labelled.

- **Use after editing:** buyer range sheets, print-detail crops for both
  journals, shop product cards.
- **Never raw:** the label card and turf read "warehouse", and the turf throws
  a green cast across every white cloth in frame. Uncorrected, the whites look
  sickly.

## Tier C — AI-generated renders. Retail only.

~270 files named `Gemini_Generated_Image_*`, `ChatGPT Image *`, `*vmake*`.
Concentrated in `Kids Laptop Case/` (~44 of 101), `Kids Backpack/` (~45 of 89),
`Kids Quilts/` (~58), `Kids dohar/` (~51), `Home Table/` (6 of 7).
Styled bedrooms, a child on a wooden floor, a woman with a duffle on a beach.

- **Use:** shop-side lifestyle context, ads, seasonal banners.
- **Never:** poddarexp.com, LinkedIn, or any post about process, craft or
  authenticity. A buyer who spots a rendered "workshop" stops believing the
  page — and the downside is asymmetric because we publish authenticity content.

## Tier D — do not touch.

A run of `Apparel Women/` and `PJ Sets/` frames are **AI model photographs
carrying a tiled "BOTIKA" watermark** — Botika is an AI fashion-model generator,
so these are our real garments on a generated model, exported without a paid
plan. Others are named `*-vmake*`, from a second AI photo tool.

Two separate reasons not to publish them: the watermark, and the fact that the
model is generated. If the watermark is only a plan limitation, a paid export
would remove it — but the images stay Tier C at best, and never go near the bulk
site or a craft story.

## Other assets worth knowing about

- `Prints/` (266) — flat swatch shots of the print library, plus one good table
  setting. Weak lighting, strong content. Good for print-story posts and
  colourway comparisons.
- `Collage/` (20) — finished marketing collateral, including an IHGF Delhi Fair
  invitation. **Read it properly: it is the 2024 fair — "16–20 October 2024,
  Stall F 06/18, Hall 4".** It is a good template, not current information. The
  2026 fair runs 13–17 October; our stall, and whether we are exhibiting at all,
  is unconfirmed.
- `Videos/` (18 clips) — printing story, bed making, PJ sets, sale cuts.
  Vertical-cropped and subtitled: Reels for the shop, two strong LinkedIn video
  posts, no production cost.

---

## Restyling a Tier B frame — the turf shots

Cropping is not enough and the owner has said so. A catalogue frame has to come
off the turf entirely and be re-lit, or it still reads as a warehouse photo.

Two scripts in `scripts/` do it, and they are the recipe as much as the tool:

**`photo-1-cutout.sh`** — isolates the product.
1. Convert to LAB and take the `a` channel. Turf is strongly negative a*; cream,
   pink and orange cloth are positive. Threshold that and the grass separates
   cleanly without touching the print.
2. Multiply by a hand-drawn ROI polygon so the label card, plants and props are
   excluded. Adjust the polygon per photo — it is the only per-image step.
3. Close, open, keep the largest blob, feather, then erode the matte a few pixels
   so no green fringe survives.
4. Grade: pull green down ~4%, push red up ~3%, drop saturation slightly, lift
   brightness. That kills the cast the turf throws across every white.

Watch for: dark tassels and trims on the product edge look like fringe and are
not — do not "clean" them away. Always `-auto-orient` first; these files carry
EXIF rotation and crop geometry silently lands on the wrong axis without it.

**`photo-2-restyle.sh`** — puts it in a scene.
A warm two-tone ground (wall above, floor below, blurred seam), a soft light pool
from the upper left, the product placed with a real contact shadow derived from
its own alpha, then a light vignette and a little grain so it doesn't look
vector-flat. Output 1600×900.

The result is a styled flat-lay, not a fake room. That is deliberate: a
synthetic room reads as a render, and this site publishes authenticity content.
If a real room shot is ever needed, it comes from the shoot in the gap section,
not from a compositing trick.

## Pipeline — six steps, every time

1. **Cull.** 8–12 frames per post, not 40. Reject soft focus, stray feet and
   chair legs, anything watermarked.
2. **Straighten and crop.** Cloth edges parallel to the frame. Crop the label
   card out entirely — never clone it out badly.
3. **Neutralise the cast.** White-balance off a known white in the cloth, then
   sanity-check skin tones in any frame with hands.
4. **Match the print to the real cloth.** Phone cameras push pinks and mute
   indigo. Anything that becomes a product image is colour-checked against the
   physical piece, or it buys returns.
5. **Clean the ground.** Turf frames get cropped to cloth-only or the ground
   gets replaced with a flat neutral. One treatment across a whole set, so a
   range sheet looks like a range.
6. **Export to spec, sharpen last** (after resizing).

Two presets — one for turf frames, one for process shots — are a half-day to
build and turn every later post from hours into minutes.

## Export specs

| Destination | Size | Ratio | Treatment |
|---|---|---|---|
| Journal hero, either property | 1600×900 | 16:9 | Tier A, or edited Tier B |
| Journal in-line | 1200×1500 | 4:5 | detail crops beat whole-product shots |
| LinkedIn single image | 1200×1200 | 1:1 | one subject, legible on a phone |
| LinkedIn document post | 1080×1350 | 4:5 | 8–10 slides, one idea per slide |
| Instagram post / Reel cover | 1080×1350 | 4:5 | colour-forward; print detail wins |
| Shop product image | 1600×2000 | 4:5 | colour-accurate, consistent ground |
| Buyer range sheet PDF | 2000px long edge | varies | Tier B, ground replaced, label typed |

## The gap

There is almost no real lifestyle photography: no actual Indian bedroom with a
quilt on the bed, no hands opening a gift, no child under a dohar, no table laid
in a real home. Renders are filling that hole today — survivable on the shop,
not on the bulk site.

One day of shooting closes it. Shot list: a bed being made and slept in, morning
light · a dohar over a sofa arm · a quilt on a child's bed with the child in it ·
a gift being unwrapped, hands only · the workshop at 8am as the printing table
is set · three tables laid for three different meals · a portrait of a printer at
his table, named. That last frame is worth more to a buyer than any certificate.

## Writing the image brief

Per post, output a brief — never a file dump:

```
HERO — 1600×900
  source: Printing Classes/IMG_3743.jpg
  crop:   square-ish to the block in the hand, leave the cloth below
  treat:  warm the shadows slightly, no filter
  alt:    A carved wooden printing block held above a length of printed cotton
  caption: New blocks take a fortnight to carve before a single metre is printed.
```

If nothing in the library fits, say so and name the missing shot. Do not force a
wrong photograph into a good post.
