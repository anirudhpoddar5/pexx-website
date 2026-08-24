#!/bin/bash
set -e
W="$(cd "$(dirname "$0")" && pwd)"
SRC="$W/src.png"          # 2000x2000, auto-oriented

# 1. LAB 'a' channel isolates the green turf (green = low a*)
magick "$SRC" -colorspace LAB -channel G -separate +channel -level 42%,58% -threshold 46% "$W/m_lab.png"

# 2. ROI polygon around the quilt only — keeps the label board and plants out
magick -size 2000x2000 xc:black -fill white \
  -draw "polygon 170,455 1890,448 1915,1045 1295,1595 995,1745 165,1715" \
  "$W/m_roi.png"

# 3. combine, clean, feather
magick "$W/m_lab.png" "$W/m_roi.png" -compose multiply -composite \
  -morphology Close Disk:5 -morphology Open Disk:5 \
  -define connected-components:area-threshold=50000 \
  -define connected-components:mean-color=true -connected-components 8 \
  -threshold 50% -blur 0x1.2 -level 45%,55% "$W/m_final.png"

# 4. cut out, shrink the matte 1px to kill any green fringe
magick "$SRC" \( "$W/m_final.png" -morphology Erode Disk:4 -blur 0x1 -level 45%,55% \) \
  -alpha off -compose CopyOpacity -composite "$W/quilt.png"

# 5. colour: neutralise the green cast, warm it, lift the whites
magick "$W/quilt.png" \
  -channel G -evaluate multiply 0.955 +channel \
  -channel R -evaluate multiply 1.035 +channel \
  -modulate 104,96,100 \
  -brightness-contrast 2x6 \
  "$W/quilt_graded.png"

magick "$W/quilt_graded.png" -background "#EFE9E0" -flatten -resize 760x -quality 78 "$W/quilt-check.jpg"
echo ok
