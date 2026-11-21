#!/bin/zsh
# Step 5: textures, colours and designs of the plate and the dumbbell, several shots each.
# One Blender run per variant; a run that dies silently (it happens at start-up) is run again.
# Raw renders in outils/blender/_bruts/poids3, finished by outils/planche_poids3.py.
cd "$(dirname "$0")"
B=/Applications/Blender.app/Contents/MacOS/Blender
OUT="$PWD/_bruts/poids3"; mkdir -p "$OUT"; t0=$(date +%s)
R=${RES:-1400}; S=${SAMPLES:-110}
run() {  # piece groupe variante plans
  local first=${4%%,*}
  for essai in 1 2 3; do
    $B -b --factory-startup -P poids3.py -- piece=$1 groupe=$2 variantes=$3 plans=$4 res=$R samples=$S out="$OUT" > "$OUT/log-$1-$2-$3.txt" 2>&1
    local missing=0
    for pl in ${(s:,:)4}; do [[ -f "$OUT/$1-$2-$3-$pl.png" ]] || missing=1; done
    [[ $missing == 0 ]] && break
    echo "  relance $1 $2 $3 ($essai)"
  done
  echo "$1 $2 $3 : $(( $(date +%s) - t0 )) s"
}
for v in moule satine mouchete vecu; do run disque texture $v face,rasant,pile; done
for v in noir graphite blanc rose bleu vert rouge sable; do run disque couleur $v face; done
run disque couleur tous alignes
run disque couleur mix pile
for v in insert-noir insert-laiton tranche-rose chiffres-bleus; do run disque design $v 3q; done
for v in fin gros satine mouchete; do run haltere texture $v flottant,macro; done
run haltere couleur tous rangee
for v in rose bleu blanc sable; do run haltere couleur $v flottant; done
for v in face-rose liseré-acier tout-noir poignee-laiton; do run haltere design $v macro3q,entier; done
echo "fin : $(( $(date +%s) - t0 )) s"
