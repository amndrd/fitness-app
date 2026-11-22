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

**Étape 6 (21/11/2026) : la barre et les colliers.**
- La recherche : `3d/recherche/4-barre-et-colliers/` (barres Eleiko et Matrix, trois types de colliers), avec sa planche `planche.png`, qui reste sur ton Mac.
- Les prototypes : `3d/prototypes/04-barre-et-colliers/planche.jpg`. On refait les deux planches avec `python3 3d/outils/planche_barre.py`. On y trouve :
  - la barre olympique homme (2,20 m, 20 kg) et femme (2,01 m, 15 kg), aux mesures normées ;
  - trois finitions : A noir et acier, B tout acier, C tout noir ;
  - la couleur choisie sur la bague d'identification et l'embout gravé « 20 KG », et des thèmes complets (rose, bleu, vert) ;
  - trois colliers : la pince à ressort, le collier à levier et le collier en aluminium, chacun dans les huit coloris.
- Le modèle est dans `3d/outils/blender/barre.py`. Tous les rendus se refont avec `rendus-barre.sh` (environ 12 min).

**Tes choix (21/11) :** pour la barre, l'originale est la **B (tout acier)**, avec A et C en options ; la couleur sur la bague et l'embout est validée. Les colliers de l'étape 6 ne te plaisaient pas : on n'en garde que deux, refaits d'après tes photos. **Le collier en aluminium est abandonné.**

**Étape 7 (21-22/11/2026) : les deux colliers, d'après tes photos.**
- Tes photos sont dans `3d/references/colliers/` : trois de la pince à ressort, une du collier à levier.
- `3d/prototypes/05-colliers/planche.jpg` : chacune de tes photos à côté de notre rendu, pris sous le même angle, puis les plans en plus (sur la barre, les huit coloris, rose et bleu). La planche reste sur ton Mac, puisqu'elle montre tes photos. On la refait avec `python3 3d/outils/planche_colliers.py`.
- La pince : fil chromé de 4,8 mm, deux spires serrées, branches coudées, gaines plates ouvertes en rectangle et arrondies au bout.
- **Tes retours (22/11) :** le sens des gaines n'allait toujours pas. Tu m'as donné le modèle exact (« Spring collar clip » sur Fab). Ses images sont analysées dans `3d/recherche/6-pince-fab/` et restent sur ton Mac. La pince est refaite de zéro selon sa logique : spirale à plat, deux bouts qui partent du même point, gaines sur la tranche. La planche montre chacune de ses vues à côté de la nôtre.
- Le collier à levier : deux mâchoires à six lobes articulées en bas, une garniture en caoutchouc, une charnière à trois segments, un levier avec sa grille, des vis cruciformes, montré fermé et ouvert.
- Le modèle est dans `3d/outils/blender/colliers.py`. Tous les rendus se refont avec `rendus-colliers.sh` (ou `rendus-colliers.sh pince` pour la pince seule).

**Tes choix (22/11) :** la pince est validée. Elle sert aux petites charges, le levier aux grosses, et les couleurs te conviennent.

**Étape 8 (22/11/2026) : l'haltère à disques, d'après ta photo.**
- Ta photo est dans `3d/references/halteres-disques/`. Les recherches (dimensions des disques ciment-vinyle, poignées de 25 mm) sont dans `3d/recherche/7-halteres-disques/`.
- `3d/prototypes/06-halteres-disques/planche.jpg` montre :
  - ta photo à côté de notre rendu, avec le même montage ;
  - les trois façons de finir le bout en acier ;
  - l'haltère et l'éclaté ;
  - les trois disques, le marquage blanc et les coloris.
  La planche reste sur ton Mac, puisqu'elle montre ta photo. On la refait avec `python3 3d/outils/planche_halteres.py`.
- Le modèle est dans `3d/outils/blender/halteres.py` (il réutilise la pince de `colliers.py`). Tous les rendus se refont avec `rendus-halteres.sh`.

**Tes choix (22/11) :**
- la poignée tout en acier (B), sans les embouts noirs ;
- les disques sablés, avec le marquage blanc ;
- les poids de 1,25, 2,5 et 5 kg ;
- les gaines de la pince telles quelles.

La planche montre maintenant cette version 2 :
- l'acier nu au bout de la poignée, avec trois façons de le finir : chanfrein, arrondi, creux ;
- le manchon allongé à 16,5 cm, pour que l'acier dépasse après la pince comme sur ta photo.

Tu as choisi le bout chanfreiné (22/11) : l'étape 8 est validée.

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
    4-barre-et-colliers/   l'étape 6 : barres/, colliers/, planche.png
  prototypes/
    01-poids-et-halteres/  la planche de l'étape 2, puis disques/ et halteres/, un dossier par piste
    02-disque-et-haltere/  l'étape 4 : disque/ et haltere/, un dossier par police, et commun/
    03-textures-coloris/   l'étape 5 : disque/ et haltere/, puis texture/, couleur/, design/
    04-barre-et-colliers/  l'étape 6 : la barre (trois finitions, la couleur) et les trois premiers colliers (remplacés)
    05-colliers/           l'étape 7 : pince/ et levier/, d'après tes photos
    06-halteres-disques/   l'étape 8 : l'haltère à disques
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
    planche_barre.py       refait les deux planches de l'étape 6
    planche_colliers.py    refait la planche de l'étape 7
    planche_halteres.py    refait la planche de l'étape 8
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
      barre.py             la barre olympique et les trois colliers (étape 6)
      rendus-barre.sh      lance tous les rendus de l'étape 6
      colliers.py          la pince à ressort et le collier à levier (étape 7)
      halteres.py          l'haltère à disques : poignée, disques ciment-vinyle (étape 8)
      rendus-colliers.sh   lance tous les rendus de l'étape 7
```

Les outils utilisent Playwright, installé dans `~/Desktop/Portfolio/tools`.
