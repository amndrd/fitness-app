#!/bin/zsh
# Step 7: the spring clip, the only collar of the library (rebuilt 22/11 after the model chosen by the user).
# One Blender run per colour, run again if Blender dies silently. Raw renders in outils/blender/_bruts/colliers2.
cd "$(dirname "$0")"
B=/Applications/Blender.app/Contents/MacOS/Blender
OUT="$PWD/_bruts/colliers2"; mkdir -p "$OUT"; t0=$(date +%s)
R=${RES:-1400}; S=${SAMPLES:-128}
run() {  # couleur plans
  for essai in 1 2 3; do
    $B -b --factory-startup -P colliers.py -- couleur=$1 plans=$2 res=$R samples=$S out="$OUT" > "$OUT/log-pince-$1.txt" 2>&1
    local missing=0
    for pl in ${(s:,:)2}; do [[ -f "$OUT/pince-$1-$pl.png" ]] || missing=1; done
    [[ $missing == 0 ]] && break
    echo "  relance $1 ($essai)"
  done
  echo "pince $1 : $(( $(date +%s) - t0 )) s"
}
run noir dessus,cote,bout,trois-quarts,arriere,debout,heros,sur-barre,couleurs
for c in rose bleu; do run $c trois-quarts; done
echo "fin : $(( $(date +%s) - t0 )) s"
