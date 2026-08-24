#!/bin/bash
set -e
W="$(cd "$(dirname "$0")" && pwd)"
Ww=1600; Hh=900
# 1. ground: warm sand, lighter top-left (window light), soft horizon at 34%
magick -size ${Ww}x$((Hh*34/100)) gradient:'#F4EEE4-#E9E1D4' "$W/s_wall.png"
magick -size ${Ww}x$((Hh*66/100)) gradient:'#E4DACA-#D8CCB8' "$W/s_floor.png"
magick -size ${Ww}x${Hh} xc:'#EFE8DD' \
  "$W/s_wall.png" -geometry +0+0 -composite \
  "$W/s_floor.png" -geometry +0+$((Hh*34/100)) -composite \
  -blur 0x6 "$W/s_base.png"
# 2. warm light pool, upper left
magick "$W/s_base.png" \
  \( -size ${Ww}x${Hh} xc:black -fill '#FFF3E2' -draw "circle 380,190 380,760" -blur 0x120 \) \
  -compose screen -define compose:args=45 -composite "$W/s_lit.png"
# 3. quilt, scaled and placed
magick "$W/quilt_final.png" -trim +repage -resize 1150x "$W/q.png"
QW=$(identify -format %w "$W/q.png"); QH=$(identify -format %h "$W/q.png")
X=$(( (Ww-QW)/2 + 20 )); Y=$(( Hh-QH-60 )); [ $Y -lt 70 ] && Y=70
# 4. contact shadow from the quilt's own alpha
magick "$W/q.png" -channel A -separate +channel -negate -threshold 99% -negate \
  -blur 0x26 -level 0%,52% "$W/q_shadow.png"
magick "$W/s_lit.png" \
  \( "$W/q_shadow.png" -alpha off -write mpr:sh +delete \
     -size ${QW}x${QH} xc:'#4A3B2A' mpr:sh -alpha off -compose CopyOpacity -composite \) \
  -geometry +$((X+14))+$((Y+26)) -compose over -composite "$W/s_sh.png"
magick "$W/s_sh.png" "$W/q.png" -geometry +${X}+${Y} -compose over -composite "$W/s_comp.png"
# 5. grade: subtle vignette + grain
magick "$W/s_comp.png" \
  \( -size ${Ww}x${Hh} radial-gradient:'#FFFFFF00'-'#3A2E20' -alpha set -channel A -evaluate multiply 0.30 +channel \) \
  -compose over -composite \
  -attenuate 0.28 +noise Gaussian -brightness-contrast 1x3 -unsharp 0x0.7+0.4+0.02 \
  -quality 90 "$W/scene-final.jpg"
magick "$W/scene-final.jpg" -resize 780x -quality 76 "$W/scene-preview.jpg"
echo ok
