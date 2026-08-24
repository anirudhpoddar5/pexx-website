#!/usr/bin/env python3
"""Per-card on-image copy for the 4 PEXX carousels, in carousel order.

Card 1 carries the hook. Cards 2-5 each name one use.
Rupee symbol only ever appears in `price` (sans line) — Didot has no ₹ glyph.
"""

FREE = "FREE SHIPPING OVER ₹750"
P999, P1299 = f"₹999  ·  COD  ·  {FREE}", f"₹1,299  ·  COD  ·  {FREE}"

CARDS = {
"quilt": [
 ("Hand block-printed", "Softest thing in the house", "Reversible Cotton Quilt", P999),
 ("In the cot",         "Two quilts in one",          "Print one side, check the other", P999),
 ("As a play mat",      "Cot, floor, pram, picnic",   "One quilt, four ways", P999),
 ("Still theirs at five","It grows with them",        "The larger 110 x 150 size", P1299),
 ("The bigger size",    "For the big-kid bed",        "110 x 150 cm", P1299),
],
"swaddle": [
 ("Pure cotton muslin", "Breathes in an Indian summer","Two swaddles per set", f"₹999 FOR TWO  ·  COD  ·  {FREE}"),
 ("Nought to six months","Wrapped, and asleep",       "Hand Block-Printed Muslin", f"₹999 FOR TWO  ·  COD  ·  {FREE}"),
 ("Two prints per set", "One in the wash, one in use","2-Pack Muslin Swaddles", f"₹999 FOR TWO  ·  COD  ·  {FREE}"),
 ("Newborn size",       "Big enough to wrap properly","Hand Block-Printed Muslin", f"₹999 FOR TWO  ·  COD  ·  {FREE}"),
 ("Two in every set",   "Never caught without one",   "2-Pack Muslin Swaddles", f"₹999 FOR TWO  ·  COD  ·  {FREE}"),
],
"pouch": [
 ("Three sizes, one price","They nest, so they pack flat","3-Piece Pouch Set", f"₹1,199 FOR ALL THREE  ·  COD"),
 ("Packed to travel",   "Everything in its own place","Small, medium and large", f"₹1,199 FOR ALL THREE  ·  COD"),
 ("On the bathroom shelf","Toothbrush in the small one","Wipe-clean lining", f"₹1,199 FOR ALL THREE  ·  COD"),
 ("Crayons and colours","Their kit, their colours",   "3-Piece Pouch Set", f"₹1,199 FOR ALL THREE  ·  COD"),
 ("Mum's own, honestly","You'll borrow the big one",  "3-Piece Pouch Set", f"₹1,199 FOR ALL THREE  ·  COD"),
],
"backpack": [
 ("Hand block-printed", "Quilted cotton, not nylon",  "Kids Backpack", P999),
 ("For the day out",    "Light enough to carry themselves","Hand Block-Printed Backpack", P999),
 ("Out for the day",    "Goes where they go",         "Kids Backpack", P999),
 ("Bottle and pencils fit","Holds the whole day",     "Front pocket, secure zip", P999),
 ("Cotton, not nylon",  "Soft on small shoulders",    "Kids Backpack", P999),
],
}
