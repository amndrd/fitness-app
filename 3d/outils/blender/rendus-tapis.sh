#!/bin/zsh
# The treadmill as it stands (23/11/2026): black portal, the big round bend with crisp edges, the reworked hood
# (grilles A), the top with the paddle handrails and the straight grips. Ten views, alone on white, into
# 3d/prototypes/tapis-de-course/. One Blender run per group of views, run again if Blender dies silently.
cd "$(dirname "$0")"
B=/Applications/Blender.app/Contents/MacOS/Blender
OUT="$PWD/_bruts/tapis"; mkdir -p "$OUT"; t0=$(date +%s)
DOS="$PWD/../../prototypes/tapis-de-course"; mkdir -p "$DOS"
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
run tapis-arriere-noir.png plans=reference,arriere-gauche,profil,face,plongee,arriere res=$R samples=$S
run tapis-bout-noir.png plans=console,capot-ref,tdb-detail,bout res=$R samples=$S
# the shot in tapis.py -> the picture in the folder
typeset -A NOMS
NOMS=(reference 01-trois-quarts-avant arriere-gauche 02-trois-quarts-arriere profil 03-profil face 04-face
      plongee 05-plongee arriere 06-dos console 07-console capot-ref 08-capot tdb-detail 09-tableau-de-bord bout 10-bout)
for plan nom in ${(kv)NOMS}; do
  [[ -f "$OUT/tapis-$plan-noir.png" ]] && node ../compose.mjs "$OUT/tapis-$plan-noir.png" "$DOS/$nom.jpg" "#FFFFFF" > /dev/null
done
echo "fin : $(( $(date +%s) - t0 )) s"
