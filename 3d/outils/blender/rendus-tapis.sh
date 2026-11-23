#!/bin/zsh
# Cardio 1: the treadmill, after the user's reference (Landice L8, black). One Blender run per set of settings,
# run again if Blender dies silently. Raw renders in outils/blender/_bruts/tapis; outils/planche_tapis.py makes the board.
cd "$(dirname "$0")"
B=/Applications/Blender.app/Contents/MacOS/Blender
OUT="$PWD/_bruts/tapis"; mkdir -p "$OUT"; t0=$(date +%s)
R=${RES:-1400}; S=${SAMPLES:-128}
run() {  # <expected file> <settings...>
  local want=$1; shift
  for essai in 1 2 3; do
    $B -b --factory-startup -P tapis.py -- "$@" out="$OUT" > "$OUT/log-${want%.png}.txt" 2>&1
    [[ -f "$OUT/$want" ]] && break
    echo "  relance $want ($essai)"
  done
  echo "$want : $(( $(date +%s) - t0 )) s"
}
# black like the reference: the two angles of the manufacturer's pictures, the views, the details
run tapis-bout-noir.png plans=reference,arriere-gauche,profil,face,arriere,console,capot,bout res=$R samples=$S
# the other finishes of the portal, at the angle of the user's picture
for c in graphite argent; do run tapis-reference-$c.png plans=reference couleur=$c res=$R samples=$S; done
echo "fin : $(( $(date +%s) - t0 )) s"
