#!/bin/zsh
# Screenshots of the models in Blender's interface (22/11/2026): one Blender window per model, in portrait.
# Blender opens on screen for a few seconds each time. Raw captures in outils/blender/_bruts/captures;
# outils/captures.py puts them in the story format in 3d/stories/blender/.
cd "$(dirname "$0")"
B=/Applications/Blender.app/Contents/MacOS/Blender
OUT="$PWD/_bruts/captures"; mkdir -p "$OUT"
if (( $# )); then list=("$@"); else list=(disque haltere barre pince haltere-disques); fi
for sh in $list; do
  for essai in 1 2 3; do
    $B --factory-startup --window-geometry 0 0 640 831 --python captures.py -- shot=$sh out="$OUT" > "$OUT/log-$sh.txt" 2>&1
    grep -q "^capture" "$OUT/log-$sh.txt" && break
    echo "  relance $sh ($essai)"
  done
  echo "$sh"
done
