#!/bin/zsh
# The plate and the round dumbbell as validated (3d/charte.md): moulded plate, fine-grain dumbbell, the 8 colours.
# One Blender run per variant; a run that dies silently (it happens at start-up) is run again.
# Raw renders in outils/blender/_bruts/poids3.
cd "$(dirname "$0")"
B=/Applications/Blender.app/Contents/MacOS/Blender
OUT="$PWD/_bruts/poids3"; mkdir -p "$OUT"; t0=$(date +%s)
R=${RES:-1400}; S=${SAMPLES:-110}
run() {  # piece groupe variante plans
  for essai in 1 2 3; do
    $B -b --factory-startup -P poids3.py -- piece=$1 groupe=$2 variantes=$3 plans=$4 res=$R samples=$S out="$OUT" > "$OUT/log-$1-$2-$3.txt" 2>&1
    local missing=0
    for pl in ${(s:,:)4}; do [[ -f "$OUT/$1-$2-$3-$pl.png" ]] || missing=1; done
    [[ $missing == 0 ]] && break
    echo "  relance $1 $2 $3 ($essai)"
  done
  echo "$1 $2 $3 : $(( $(date +%s) - t0 )) s"
}
run disque texture moule face,rasant,pile
for v in noir graphite blanc rose bleu vert rouge sable; do run disque couleur $v face; done
run disque couleur tous alignes
run disque couleur mix pile
run haltere texture fin flottant,macro
run haltere couleur tous rangee
for v in rose bleu blanc sable; do run haltere couleur $v flottant; done
echo "fin : $(( $(date +%s) - t0 )) s"
