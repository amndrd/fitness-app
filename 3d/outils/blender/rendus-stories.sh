#!/bin/zsh
# The Instagram stories (22/11/2026): 1 the bars and the plates, 2 the round dumbbells, 3 the plate-loaded dumbbell, 4 the 25 mm plates and the clips.
# One Blender run per story, run again if Blender dies silently. Raw renders (transparent, with the shadows) in
# outils/blender/_bruts/stories (the objects, then their shadow); outils/stories.py puts them on white at 1080 x 1920 in 3d/stories/.
cd "$(dirname "$0")"
B=/Applications/Blender.app/Contents/MacOS/Blender
OUT="$PWD/_bruts/stories"; mkdir -p "$OUT"; t0=$(date +%s)
R=${RES:-1440}; S=${SAMPLES:-128}
if (( $# )); then list=("$@"); else list=(barres 1d 2a 2b 2c 3a 3b 3c 3d 4 6); fi   # usage: ./rendus-stories.sh [1a 2b ...]
for sc in $list; do
  for essai in 1 2 3; do
    $B -b --factory-startup -P stories.py -- scenes=$sc res=$R samples=$S out="$OUT" > "$OUT/log-$sc.txt" 2>&1
    [[ -f "$OUT/story-$sc.png" ]] && break
    echo "  relance $sc ($essai)"
  done
  echo "$sc : $(( $(date +%s) - t0 )) s"
done
echo "fin : $(( $(date +%s) - t0 )) s"
