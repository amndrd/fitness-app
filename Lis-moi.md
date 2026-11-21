# Fitness app : le dossier

Nom provisoire, en attendant le vrai nom de l'application.

GitHub : https://github.com/amndrd/fitness-app (public, depuis le 21/11/2026).
- Le dépôt ne contient ni les images de recherche ni les planches qui les assemblent : ce sont des photos de Basic-Fit, Matrix et Technogym.
- Il ne contient pas non plus les scènes `.blend`, refaites par les scripts.
- Le détail est dans `.gitignore`.

Le plan complet de l'application est dans le Google Doc « fitness app · Plan complet ».

## Où on en est

**Étape 1, la recherche (21/11/2026) : les salles et les pectoraux.**
- `3d/recherche/planche.png` : toute la recherche sur une planche, avec ce qu'on en retient, la liste des machines pectoraux, l'ordre proposé et les questions. On la refait avec `python3 3d/outils/planche_recherche.py`.
- `3d/recherche/0-style-des-salles/` : Basic-Fit, ses machines guidées et ses zones libres.
- `3d/recherche/1-pectoraux/` : un dossier par machine (chest press, butterfly, développé couché…), avec les photos des fabricants.
- `sources.json` : la page d'origine de chaque image.

**Tes réponses (21/11) :** un style noir, sobre et sombre, comme les machines Technogym de Fitness Park ; aucune couleur reprise d'avant, on part de zéro. Des machines universelles, avec plusieurs variantes au choix de l'utilisateur.

**Étape 2 (21/11/2026) : les disques et les haltères.**
- `3d/prototypes/01-poids-et-halteres/planche.jpg` : les quatre disques (A fonte, B caoutchouc à poignées, C uréthane, D bumper) et les trois haltères (A hexagonal, B rond, C douze pans), chacun sous quatre angles, dont un sur fond sombre. On la refait avec `python3 3d/outils/planche_poids.py`.
- Les rendus seuls sont dans `disques/` et `halteres/`, un dossier par piste.
- Les modèles sont faits par `3d/outils/blender/poids.py` (les pièces) et `base.py` (le studio, les matières, la caméra). On refait tous les rendus avec `3d/outils/blender/rendus-poids.sh` (environ 20 min sur le M4), ou un essai rapide avec `rendus-poids.sh test disques C barre`.

**Tes choix (21/11) :** l'haltère rond (B), à retravailler ; des disques épais, ronds et noirs.

**Étape 3 (21/11/2026) : le style des poids, tes références et la recherche.**
- `3d/recherche/3-style-poids/planche.png` : l'analyse de tes trois images (le rendu, le design, la texture, les couleurs, la typo), la recherche sur ce style (Skelcore, American Barbell, Hammer Strength, REP, Eleiko), comment je le traduis pour nous, et les questions. On la refait avec `python3 3d/outils/planche_style_poids.py`.
- Tes images sont rangées dans `3d/references/halteres/` et `3d/references/disques/`.

**Tes réponses (21/11) :** rien en haut et en bas du disque, le chiffre de l'haltère en blanc, avec « KG » et sans marque.

**Étape 4 (21/11/2026) : le disque et l'haltère, version 2.**
- `3d/prototypes/02-disque-et-haltere/planche.jpg` : tes références à côté des rendus. Trois variantes, qui ne changent que la police des chiffres : A Archivo Expanded, B Saira Expanded, C Michroma. Il y a aussi les vues communes (la gamme, la barre, le fond sombre). Cette planche reste sur ton Mac, parce qu'elle montre tes références. On la refait avec `python3 3d/outils/planche_poids2.py`.
- Le disque : noir et épais (58 mm pour le 20 kg), avec un rebord, une bague de caoutchouc, un insert en acier tourné et ses deux rainures polies. Le poids est en blanc et en relief à gauche et à droite, avec « KG » ton sur ton.
- L'haltère : des têtes rondes épaisses, une face en médaillon lisse cerclé d'un liseré, un tour grainé, le chiffre et « KG » en blanc, une poignée satinée et des collerettes.
- Les modèles sont dans `3d/outils/blender/poids2.py`. Tous les rendus se refont avec `rendus-poids2.sh` (environ 15 min) ; `compose.mjs` pose le fond clair des références.
- Les polices sont dans `3d/outils/polices/`, avec leur licence OFL.

**Tes réponses (21/11) :** la police A (Archivo Expanded). Le design est validé, mais tu voulais une texture plus réaliste, des coloris (noir, rose, bleu…) que l'utilisateur pourra personnaliser, et plusieurs plans par rendu.

**Étape 5 (21/11/2026) : textures, coloris et designs.**
- `3d/prototypes/03-textures-coloris/planche.jpg` (on la refait avec `python3 3d/outils/planche_poids3.py`) :
  - le disque en quatre textures (moulé, satiné, moucheté, vécu), chacune de face, en lumière rasante et en pile ;
  - les huit coloris (noir, graphite, blanc, rose, bleu, vert, rouge, sable), alignés, en pile et de face ;
  - quatre designs du disque : insert noir, insert laiton, tranche de couleur, chiffres de couleur ;
  - l'haltère en quatre grains (fin, gros, satiné, moucheté), en paire flottante et en lumière rasante ;
  - les coloris de l'haltère, en rangée et en paires ;
  - quatre designs de l'haltère : face de couleur, liseré en acier, tout noir, poignée laiton.
- La lumière vient maintenant d'un vrai studio photographié (HDRI Poly Haven, CC0, voir `3d/outils/credits.md`). Le fichier se retélécharge, il n'est pas sur GitHub.
- Les modèles sont dans `3d/outils/blender/poids3.py`, qui reprend ceux de `poids2.py` en changeant les matières, la lumière et les plans. Tous les rendus se refont avec `rendus-poids3.sh` (environ 22 min), qui relance tout seul un rendu quand Blender s'arrête sans prévenir.

**Tes choix (21/11) :**
- les disques en texture moulée et les haltères en grain fin, dans les huit coloris ;
- les designs (insert, tranche, face, chiffres de couleur…) sont gardés de côté, au cas où la personnalisation irait plus loin que la couleur.

Tout est rassemblé dans **`3d/charte.md`** : la police, les coloris, les tailles et les règles. Les machines suivront cette charte.

**Tes références :** dépose tes images de machines dans `3d/references/` (elles restent sur ton Mac).

## Structure

```
3d/
  charte.md                les choix validés : police, coloris, tailles, textures, ce qui est gardé de côté
  recherche/
    planche.png            la planche de l'étape 1
    0-style-des-salles/    les salles : Basic-Fit (machines guidées, zones libres et force)
    1-pectoraux/           01-chest-press … 11-dips : les photos de chaque machine
    2-poids-et-halteres/   la petite recherche de l'étape 2 (les liens seulement)
    3-style-poids/         l'étape 3 : halteres/, disques/, planche.png
  prototypes/
    01-poids-et-halteres/  la planche de l'étape 2, puis disques/ et halteres/, un dossier par piste
    02-disque-et-haltere/  l'étape 4 : disque/ et haltere/, un dossier par police, et commun/
    03-textures-coloris/   l'étape 5 : disque/ et haltere/, puis texture/, couleur/, design/
  references/              tes images de référence
  outils/
    planche_recherche.py   refait la planche
    page_images.mjs        récupère les photos d'une page de fabricant (liens ou images)
    contact.py             assemble les images d'un dossier en une seule image, pour les regarder d'un coup
    export.mjs             transforme une page HTML en PNG
    planche_poids.py       refait la planche de l'étape 2
    planche_style_poids.py refait la planche de l'étape 3
    planche_poids2.py      refait la planche de l'étape 4
    planche_poids3.py      refait la planche de l'étape 5
    credits.md             les éléments de tiers (HDRI) et leurs licences
    compose.mjs            pose un rendu transparent sur un fond (couleur ou dégradé)
    blender/
      base.py              le studio, les matières, la caméra, le rendu (commun à tous les modèles)
      poids.py             les disques, la barre et les haltères
      rendus-poids.sh      lance tous les rendus de l'étape 2
      poids2.py            le disque et l'haltère, version 2 (étape 4)
      rendus-poids2.sh     lance tous les rendus de l'étape 4
      poids3.py            textures, coloris, designs et plans (étape 5)
      rendus-poids3.sh     lance tous les rendus de l'étape 5
```

Les outils utilisent Playwright, installé dans `~/Desktop/Portfolio/tools`.
