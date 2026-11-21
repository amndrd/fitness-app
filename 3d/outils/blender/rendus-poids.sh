#!/bin/zsh
# Weight plates and dumbbells (step 2, prototypes). Raw renders in outils/blender/_bruts/poids,
# finished (JPEG) into 3d/prototypes/01-poids-et-halteres/.
# usage: ./rendus-poids.sh test [piece] [piste] [vues]  |  ./rendus-poids.sh   (everything, full quality)
cd "$(dirname "$0")"
B=/Applications/Blender.app/Contents/MacOS/Blender
OUT="$PWD/_bruts/poids"; mkdir -p "$OUT"; t0=$(date +%s)
if [[ "$1" == test ]]; then
  $B -b --factory-startup -P poids.py -- piece=${2:-disques} piste=${3:-A} vues=${4:-heros} res=800 samples=24 out="$OUT/test" > "$OUT/log-test.txt" 2>&1
  grep -h "Traceback\|Error\|rendu " "$OUT/log-test.txt" | head -20; echo "$(( $(date +%s) - t0 )) s"; exit
fi
for p in A B C D; do
  $B -b --factory-startup -P poids.py -- piece=disques piste=$p vues=heros,gamme,barre,sombre res=1600 samples=96 out="$OUT" > "$OUT/log-disques-$p.txt" 2>&1
  echo "disques $p : $(( $(date +%s) - t0 )) s"
done
for p in A B C; do
  $B -b --factory-startup -P poids.py -- piece=halteres piste=$p vues=heros,gamme,detail,sombre res=1600 samples=96 out="$OUT" > "$OUT/log-halteres-$p.txt" 2>&1
  echo "halteres $p : $(( $(date +%s) - t0 )) s"
done
