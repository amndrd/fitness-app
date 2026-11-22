#!/bin/zsh
# Step 7: the spring clip and the lever collar, reworked from the user's references.
# One Blender run per piece and colour, run again if Blender dies silently.
# Raw renders in outils/blender/_bruts/colliers2, finished by outils/planche_colliers.py.
# usage: ./rendus-colliers.sh [pince|levier]   (both pieces by default)
cd "$(dirname "$0")"
B=/Applications/Blender.app/Contents/MacOS/Blender
OUT="$PWD/_bruts/colliers2"; mkdir -p "$OUT"; t0=$(date +%s)
R=${RES:-1400}; S=${SAMPLES:-128}
run() {  # piece couleur plans
  for essai in 1 2 3; do
    $B -b --factory-startup -P colliers.py -- piece=$1 couleur=$2 plans=$3 res=$R samples=$S out="$OUT" > "$OUT/log-$1-$2.txt" 2>&1
    local missing=0
    for pl in ${(s:,:)3}; do [[ -f "$OUT/collier2-$1-$2-$pl.png" ]] || missing=1; done
    [[ $missing == 0 ]] && break
    echo "  relance $1 $2 ($essai)"
  done
  echo "$1 $2 : $(( $(date +%s) - t0 )) s"
}
ONLY=${1:-}
if [[ $ONLY != levier ]]; then
  run pince noir paire,macro,trois-quarts,sur-barre,couleurs
  for c in rose bleu; do run pince $c paire; done
fi
if [[ $ONLY != pince ]]; then
  run levier noir paire,detail,sur-barre,couleurs
  for c in rose bleu; do run levier $c paire; done
fi
echo "fin : $(( $(date +%s) - t0 )) s"
