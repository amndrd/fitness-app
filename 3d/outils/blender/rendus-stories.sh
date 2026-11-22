#!/bin/zsh
# The Instagram stories (22/11/2026): S1 the bars and the plates, S2a/S2b the dumbbells, S3a/S3b the 25 mm plates and the clips.
# One Blender run per story, run again if Blender dies silently. Raw renders (transparent, with the shadows) in
# outils/blender/_bruts/stories (the objects, then their shadow); outils/stories.py puts them on white at 1080 x 1920 in 3d/stories/.
cd "$(dirname "$0")"
B=/Applications/Blender.app/Contents/MacOS/Blender
OUT="$PWD/_bruts/stories"; mkdir -p "$OUT"; t0=$(date +%s)
R=${RES:-1440}; S=${SAMPLES:-128}
if (( $# )); then list=("$@"); else list=(S1 S2a S2b S3a S3b); fi   # usage: ./rendus-stories.sh [S1 S2a ...]
for sc in $list; do
  for essai in 1 2 3; do
    $B -b --factory-startup -P stories.py -- scenes=$sc res=$R samples=$S out="$OUT" > "$OUT/log-$sc.txt" 2>&1
    [[ -f "$OUT/story-$sc.png" ]] && break
    echo "  relance $sc ($essai)"
  done
  echo "$sc : $(( $(date +%s) - t0 )) s"
done
echo "fin : $(( $(date +%s) - t0 )) s"
