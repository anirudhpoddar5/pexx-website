"""Generate the PEXX referral insert card (PASSITON15) as a print-ready PNG.
ponytail: drawn with PIL primitives, no external art assets — good enough for a gift-box insert.
Run: python3 make_referral_card.py
"""
from PIL import Image, ImageDraw, ImageFont

# 4in x 6in @ 300dpi — standard gift-insert postcard size
W, H = 1200, 1800
CREAM = (243, 237, 227)
TAN = (216, 199, 173)
DARK_TAN = (137, 111, 78)  # ponytail: readable version of TAN for small print text, TAN itself stays for decorative lines/diamonds
INK = (43, 36, 31)
RUST = (158, 59, 47)

FONT_DIR = "/System/Library/Fonts/Supplemental/"
didot = ImageFont.truetype(FONT_DIR + "Didot.ttc", 64)
didot_small = ImageFont.truetype(FONT_DIR + "Didot.ttc", 30)
georgia = ImageFont.truetype(FONT_DIR + "Georgia.ttf", 40)
georgia_italic = ImageFont.truetype(FONT_DIR + "Georgia Italic.ttf", 30)
georgia_small = ImageFont.truetype(FONT_DIR + "Georgia.ttf", 26)
code_font = ImageFont.truetype(FONT_DIR + "Georgia Bold.ttf", 56)

img = Image.new("RGB", (W, H), CREAM)
draw = ImageDraw.Draw(img)


def tracked_text(xy, text, font, fill, tracking=0, anchor="mm"):
    """Center-anchored text with manual letter-spacing (PIL has no native tracking)."""
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x, y = xy
    if anchor[0] == "m":
        x -= total / 2
    cx = x
    for ch, w in zip(text, widths):
        draw.text((cx, y), ch, font=font, fill=fill, anchor="l" + anchor[1])
        cx += w + tracking
    return total


def diamond(cx, cy, r, fill):
    draw.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=fill)


# --- border frame -----------------------------------------------------------
margin = 48
draw.rectangle([margin, margin, W - margin, H - margin], outline=TAN, width=3)
inner = margin + 18
draw.rectangle([inner, inner, W - inner, H - inner], outline=TAN, width=1)

# block-print diamond strip, top and bottom
strip_y_top = margin + 60
strip_y_bottom = H - margin - 60
step = 46
start_x = margin + 90
n = int((W - 2 * margin - 180) / step)
for i in range(n + 1):
    x = start_x + i * step
    diamond(x, strip_y_top, 8, TAN)
    diamond(x, strip_y_bottom, 8, TAN)

# --- wordmark -----------------------------------------------------------
tracked_text((W / 2, 240), "PEXX", didot, INK, tracking=18)
tracked_text((W / 2, 300), "HAND BLOCK-PRINTED IN JAIPUR", georgia_small, DARK_TAN, tracking=4)

# small rule
draw.line([(W / 2 - 70, 340), (W / 2 + 70, 340)], fill=TAN, width=2)

# --- headline -----------------------------------------------------------
draw.text((W / 2, 460), "Loved it?", font=didot, fill=INK, anchor="mm")
draw.text((W / 2, 540), "Pass it on.", font=didot, fill=RUST, anchor="mm")

# --- subhead -----------------------------------------------------------
subhead_lines = [
    "Someone gave you something a little different.",
    "Give a friend the same — 15% off",
    "their first PEXX order, on us.",
]
y = 660
for line in subhead_lines:
    draw.text((W / 2, y), line, font=georgia, fill=INK, anchor="mm")
    y += 50

# --- code box -----------------------------------------------------------
box_w, box_h = 640, 140
box_x0 = (W - box_w) / 2
box_y0 = 940
box_x1 = box_x0 + box_w
box_y1 = box_y0 + box_h
# dashed rounded rect (PIL has no native dashed outline — draw short segments)
def dashed_rounded_rect(x0, y0, x1, y1, radius, dash=14, gap=10, width=4, fill=RUST):
    import math
    # approximate perimeter path as straight edges only for simplicity (radius kept small)
    edges = [
        ((x0 + radius, y0), (x1 - radius, y0)),
        ((x1, y0 + radius), (x1, y1 - radius)),
        ((x1 - radius, y1), (x0 + radius, y1)),
        ((x0, y1 - radius), (x0, y0 + radius)),
    ]
    for (sx, sy), (ex, ey) in edges:
        length = math.hypot(ex - sx, ey - sy)
        steps = max(1, int(length / (dash + gap)))
        for i in range(steps + 1):
            t0 = i * (dash + gap) / length
            t1 = min(1, t0 + dash / length)
            if t0 >= 1:
                break
            p0 = (sx + (ex - sx) * t0, sy + (ey - sy) * t0)
            p1 = (sx + (ex - sx) * t1, sy + (ey - sy) * t1)
            draw.line([p0, p1], fill=fill, width=width)

dashed_rounded_rect(box_x0, box_y0, box_x1, box_y1, radius=20)
tracked_text((W / 2, box_y0 + box_h / 2), "PASSITON15", code_font, RUST, tracking=6)

# --- footer -----------------------------------------------------------
draw.text((W / 2, 1150), "Redeem at checkout — one use per customer", font=georgia_italic, fill=INK, anchor="mm")

# large centerpiece motif to fill the lower panel
diamond(W / 2, 1420, 46, None) if False else None
draw.polygon([(W / 2, 1370), (W / 2 + 46, 1420), (W / 2, 1470), (W / 2 - 46, 1420)], outline=TAN, width=3)
diamond(W / 2, 1420, 12, TAN)
draw.line([(W / 2 - 130, 1420), (W / 2 - 60, 1420)], fill=TAN, width=2)
draw.line([(W / 2 + 60, 1420), (W / 2 + 130, 1420)], fill=TAN, width=2)

tracked_text((W / 2, H - margin - 150), "SHOP.PODDAREXP.COM", georgia_small, RUST, tracking=3)

out_path = "/Users/anirudhpoddar/Downloads/pexx-website/pexx-shopify/referral-card-PASSITON15.png"
img.save(out_path, "PNG")
print("saved", out_path, img.size)
