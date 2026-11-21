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

**Tes références :** dépose tes images de machines dans `3d/references/` (elles restent sur ton Mac).

## Structure

```
3d/
  recherche/
    planche.png            la planche de l'étape 1
    0-style-des-salles/    les salles : Basic-Fit (machines guidées, zones libres et force)
    1-pectoraux/           01-chest-press … 11-dips : les photos de chaque machine
  prototypes/
    01-poids-et-halteres/  la planche de l'étape 2, puis disques/ et halteres/, un dossier par piste
  references/              tes images de référence
  outils/
    planche_recherche.py   refait la planche
    page_images.mjs        récupère les photos d'une page de fabricant (liens ou images)
    contact.py             assemble les images d'un dossier en une seule image, pour les regarder d'un coup
    export.mjs             transforme une page HTML en PNG
    planche_poids.py       refait la planche de l'étape 2
    blender/
      base.py              le studio, les matières, la caméra, le rendu (commun à tous les modèles)
      poids.py             les disques, la barre et les haltères
      rendus-poids.sh      lance tous les rendus de l'étape 2
```

Les outils utilisent Playwright, installé dans `~/Desktop/Portfolio/tools`.
