#!/usr/bin/env python3
"""Compose PEXX ad creative — matches the Rakhi ad house style.

NOTE: Didot.ttc has no rupee glyph. Anything containing the rupee symbol must
go in a sans line (Optima/Baskerville render it fine), never the serif ones.

Layout, bottom-anchored over a soft dark gradient (same as _ads-rakhi):
    EYEBROW      small caps, wide letter-spacing
    Headline     large Didot serif
    Subtitle     medium serif
    P E X X      wordmark, wide letter-spacing

Output is 1080x1350 (4:5). Source photos are centre-cropped to fill.
"""
import subprocess, sys, pathlib, shutil

W, H = 1080, 1350


def set_size(w, h):
    """Google PMax needs 1.91:1 and 1:1 as well as 4:5. Compose at the target
    ratio — centre-cropping a 4:5 creative to landscape destroys the text block."""
    global W, H
    W, H = w, h
SERIF = "/System/Library/Fonts/Supplemental/Didot.ttc"
SANS  = "/System/Library/Fonts/Supplemental/Optima.ttc"
if not pathlib.Path(SANS).exists():
    SANS = "/System/Library/Fonts/Supplemental/Baskerville.ttc"


def space(s, px=6):
    """Fake letter-spacing: ImageMagick has no tracking, so pad between glyphs."""
    return (" " * max(1, px // 3)).join(list(s))


def text_width(txt, font, pt):
    r = subprocess.run(["magick", "-font", font, "-pointsize", str(pt),
                        f"label:{txt}", "-format", "%w", "info:"],
                       capture_output=True, text=True, check=True)
    return int(r.stdout.strip())


def fit(txt, font, start_pt, max_w, min_pt=40):
    """Shrink until the line fits the frame. Long headlines were being cropped
    off at both edges at a fixed point size."""
    # A small line (eyebrow at 27pt) starts below the 40pt floor, so the loop
    # never ran and the line got cropped at both edges. Floor must scale.
    min_pt = min(min_pt, max(12, start_pt // 2))
    pt = start_pt
    while pt > min_pt and text_width(txt, font, pt) > max_w:
        pt -= 2
    return pt


def compose(src, out, eyebrow, headline, subtitle, wordmark="PEXX", sub2=None,
            size=(1080, 1350), lift=0):
    """size: (w,h) of the frame — 1080x1350 for feed, 1080x1920 for stories.
    lift: px to raise the whole type block, so Instagram's own bottom UI
    (the reply bar on a Story) doesn't sit on top of the CTA."""
    W, H = size
    # Two scrims. A long soft fade blends into the photo, then a shorter, much
    # stronger one sits directly under the type. One gradient alone is not enough:
    # on pale fabric (white quilts) the white headline disappears into the image.
    fade, base = "/tmp/_fade.png", "/tmp/_base.png"
    # Both scrims grow by `lift`, otherwise raising the type on a 9:16 story
    # walks it up out of the dark part and the headline goes grey-on-pale.
    fade_h, base_h = min(H, int(H*0.60)+lift), min(H, int(H*0.34)+lift)
    subprocess.run(["magick", "-size", f"{W}x{fade_h}",
                    "gradient:none-black", "-alpha", "set",
                    "-channel", "A", "-evaluate", "multiply", "0.85", "+channel",
                    fade], check=True)
    subprocess.run(["magick", "-size", f"{W}x{base_h}",
                    "gradient:none-black", "-alpha", "set",
                    "-channel", "A", "-evaluate", "multiply", "0.92", "+channel",
                    base], check=True)

    cmd = ["magick", src,
           "-resize", f"{W}x{H}^", "-gravity", "center", "-extent", f"{W}x{H}",
           fade, "-gravity", "south", "-composite",
           base, "-gravity", "south", "-composite",
           "-gravity", "south", "-fill", "white"]

    y = (250 if sub2 else 232) + lift
    if eyebrow:
        eb = space(eyebrow.upper(), 12)
        ep = fit(eb, SANS, 27, W - 130)
        cmd += ["-font", SANS, "-pointsize", str(ep), "-fill", "#f0e9df",
                "-annotate", f"+0+{y+118}", eb]
    hp = fit(headline, SERIF, 78, W - 130)
    cmd += ["-font", SERIF, "-pointsize", str(hp), "-fill", "white",
            "-annotate", f"+0+{y}", headline]
    if subtitle:
        cmd += ["-font", SERIF, "-pointsize", "36", "-fill", "#efe7dc",
                "-annotate", f"+0+{y-72}", subtitle]
    if sub2:
        sp = fit(sub2, SANS, 27, W - 130)
        cmd += ["-font", SANS, "-pointsize", str(sp), "-fill", "#e2d8c8",
                "-annotate", f"+0+{y-126}", sub2]
    cmd += ["-font", SANS, "-pointsize", "30", "-fill", "white",
            "-annotate", f"+0+{62 + lift}", space(wordmark, 14), out]
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    compose(*sys.argv[1:])
