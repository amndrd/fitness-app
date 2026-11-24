#!/bin/zsh
# Treadmill, the new dashboard (23/11, after the user's reference: the Skillrun's dashboard, without its brand).
# With the two tall upright handles (the user's choice, 23/11). Raw renders in outils/blender/_bruts/tapis;
# outils/planche_tapis_tdb.py puts them on white into 3d/prototypes/tapis-de-course/tableau-de-bord/ with the board.
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
run tapis-profil-noir.png plans=tdb-face,tdb-34,tdb-detail,tdb-stop,tdb-palette,tdb-ecran,tdb-dos,console,reference,arriere-gauche,profil res=$R samples=$S
echo "fin : $(( $(date +%s) - t0 )) s"
