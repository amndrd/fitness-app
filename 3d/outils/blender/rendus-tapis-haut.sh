#!/bin/zsh
# Treadmill, correction 2 (23/11): the top (the portal's corners, the shell, the handrails, the heart-rate grips).
# A: straight grips like the original; B: moulded bent grips with two steel pads.
# Raw renders in outils/blender/_bruts/tapis; outils/planche_tapis_haut.py makes the board.
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
run tapis-arriere-gauche-noir.png plans=haut-ref,haut-arriere,haut-poignee,haut-cardio,console,reference,arriere-gauche res=$R samples=$S
run tapis-console-noir-galbees.png plans=haut-cardio,console poignees=galbees suffixe=-galbees res=$R samples=$S
echo "fin : $(( $(date +%s) - t0 )) s"
