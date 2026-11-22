#!/bin/zsh
# Step 8: the plate-loaded dumbbell (handle, cement-vinyl plates, our clip), after the user's photo.
# One Blender run per set of settings, run again if Blender dies silently.
# Raw renders in outils/blender/_bruts/halteres.
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
# Defaults since 22/11: handle B (all steel, bare steel ends), sandy plates, white marking, chamfered end.
D=noir-B-gros-blanc
run haltere-haltere-$D-chanfrein.png plans=paire,detail,haltere
run haltere-disques-$D-chanfrein.png plans=eclate,gros-plan,disques
run haltere-bout-$D-chanfrein.png plans=bout
run haltere-couleurs-$D-chanfrein.png plans=couleurs
for c in rose bleu; do run haltere-haltere-$c-B-gros-blanc-chanfrein.png plans=haltere couleur=$c; done
echo "fin : $(( $(date +%s) - t0 )) s"
