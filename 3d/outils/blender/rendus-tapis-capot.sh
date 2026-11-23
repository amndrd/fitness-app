#!/bin/zsh
# Treadmill, correction 1 (23/11): the front base (motor hood, plinth, feet), after the user's notes.
# Raw renders in outils/blender/_bruts/tapis; outils/planche_tapis.py capot makes the board.
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
run tapis-reference-noir.png plans=capot,capot-ref,capot-arriere,capot-face,reference res=$R samples=$S
run tapis-capot-ref-noir-cloisons.png plans=capot-ref grilles=cloisons suffixe=-cloisons res=$R samples=$S
echo "fin : $(( $(date +%s) - t0 )) s"
