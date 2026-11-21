#!/bin/zsh
# Step 4: the plate E and the round dumbbell B2, three variants (the font of the numbers).
# Raw renders in outils/blender/_bruts/poids2, finished by outils/planche_poids2.py.
# usage: ./rendus-poids2.sh test [disque|haltere] [A|B|C] [vues]  |  ./rendus-poids2.sh   (everything)
cd "$(dirname "$0")"
B=/Applications/Blender.app/Contents/MacOS/Blender
OUT="$PWD/_bruts/poids2"; mkdir -p "$OUT"; t0=$(date +%s)
if [[ "$1" == test ]]; then
  $B -b --factory-startup -P poids2.py -- piece=${2:-disque} variante=${3:-A} vues=${4:-face20} res=${RES:-720} samples=24 out="$OUT/test" > "$OUT/log-test.txt" 2>&1
  grep -h "Traceback\|Error\|rendu " "$OUT/log-test.txt" | head -20; echo "$(( $(date +%s) - t0 )) s"; exit
fi
for v in A B C; do
  $B -b --factory-startup -P poids2.py -- piece=disque variante=$v vues=face20,face25,tq res=1600 samples=128 out="$OUT" > "$OUT/log-disque-$v.txt" 2>&1
  $B -b --factory-startup -P poids2.py -- piece=haltere variante=$v vues=flottant,face res=1600 samples=128 out="$OUT" > "$OUT/log-haltere-$v.txt" 2>&1
  echo "$v : $(( $(date +%s) - t0 )) s"
done
$B -b --factory-startup -P poids2.py -- piece=disque variante=A vues=gamme,barre,sombre res=1600 samples=96 out="$OUT" > "$OUT/log-disque-commun.txt" 2>&1
$B -b --factory-startup -P poids2.py -- piece=haltere variante=A vues=heros,gamme,sombre res=1600 samples=96 out="$OUT" > "$OUT/log-haltere-commun.txt" 2>&1
echo "fin : $(( $(date +%s) - t0 )) s"
