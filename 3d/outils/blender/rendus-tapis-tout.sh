#!/bin/zsh
# The treadmill, all the views with the current settings (23/11: the big round portal with crisp edges, the reworked
# hood, the top with the paddle handrails and the straight grips). Raw renders in outils/blender/_bruts/tapis.
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
run tapis-bout-noir.png plans=reference,arriere-gauche,profil,face,arriere,console,capot,bout res=$R samples=$S
run tapis-haut-cardio-noir.png plans=capot-ref,capot-arriere,capot-face,haut-ref,haut-arriere,haut-poignee,haut-cardio res=$R samples=$S
echo "fin : $(( $(date +%s) - t0 )) s"
