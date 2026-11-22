#!/bin/zsh
# Step 8: the plate-loaded dumbbell (handle, cement-vinyl plates, our clip), after the user's photo.
# One Blender run per set of settings, run again if Blender dies silently.
# Raw renders in outils/blender/_bruts/halteres, finished by outils/planche_halteres.py.
cd "$(dirname "$0")"
B=/Applications/Blender.app/Contents/MacOS/Blender
OUT="$PWD/_bruts/halteres"; mkdir -p "$OUT"; t0=$(date +%s)
R=${RES:-1400}; S=${SAMPLES:-128}
run() {  # <expected file> <settings...>
  local want=$1; shift
  for essai in 1 2 3; do
    $B -b --factory-startup -P halteres.py -- "$@" res=$R samples=$S out="$OUT" > "$OUT/log-${want%.png}.txt" 2>&1
    [[ -f "$OUT/$want" ]] && break
    echo "  relance $want ($essai)"
  done
  echo "$want : $(( $(date +%s) - t0 )) s"
}
run haltere-haltere-noir-C-gros-relief.png plans=paire,detail,haltere couleur=noir finition=C
run haltere-eclate-noir-B-gros-relief.png plans=haltere,eclate couleur=noir finition=B
run haltere-couleurs-noir-B-gros-relief.png plans=poignees,disques,couleurs couleur=noir finition=B
for t in gros fin moule; do run haltere-gros-plan-noir-B-$t-relief.png plans=gros-plan texture=$t; done
run haltere-gros-plan-noir-B-gros-blanc.png plans=gros-plan marquage=blanc
for c in rose bleu; do run haltere-haltere-$c-B-gros-relief.png plans=haltere couleur=$c finition=B; done
echo "fin : $(( $(date +%s) - t0 )) s"
