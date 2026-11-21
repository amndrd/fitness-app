#!/bin/zsh
# Step 6: the Olympic bar and the collars. One Blender run per variant, run again if Blender dies silently.
# Raw renders in outils/blender/_bruts/barre, finished by outils/planche_barre.py.
cd "$(dirname "$0")"
B=/Applications/Blender.app/Contents/MacOS/Blender
OUT="$PWD/_bruts/barre"; mkdir -p "$OUT"; t0=$(date +%s)
R=${RES:-1400}; S=${SAMPLES:-110}
run() {  # piece variante plans prefix
  for essai in 1 2 3; do
    $B -b --factory-startup -P barre.py -- piece=$1 variantes=$2 plans=$3 res=$R samples=$S out="$OUT" > "$OUT/log-$1-$2.txt" 2>&1
    local missing=0
    for pl in ${(s:,:)3}; do [[ -f "$OUT/$4-$pl.png" ]] || missing=1; done
    [[ $missing == 0 ]] && break
    echo "  relance $1 $2 ($essai)"
  done
  echo "$1 $2 : $(( $(date +%s) - t0 )) s"
}
for f in A B C; do run barre $f entiere,manchon,embout,moletage,chargee barre-$f; done
run barre A gamme barre-A
run couleur noir rack barre-couleur-noir
for c in rose bleu vert; do run couleur $c theme barre-couleur-$c; done
for k in pince levier alu; do run collier $k seul,sur-barre,couleurs collier-$k; done
echo "fin : $(( $(date +%s) - t0 )) s"
