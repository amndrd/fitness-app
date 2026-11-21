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

**Étape 2, à venir : le style.** Trois pistes sur la chest press, rendues en studio et dans l'interface de l'app, sur un écran d'iPhone 16.

## Structure

```
3d/
  recherche/
    planche.png            la planche de l'étape 1
    0-style-des-salles/    les salles : Basic-Fit (machines guidées, zones libres et force)
    1-pectoraux/           01-chest-press … 11-dips : les photos de chaque machine
  prototypes/              les rendus des pistes (étape 2)
  outils/
    planche_recherche.py   refait la planche
    page_images.mjs        récupère les photos d'une page de fabricant (liens ou images)
    contact.py             assemble les images d'un dossier en une seule image, pour les regarder d'un coup
    export.mjs             transforme une page HTML en PNG
    blender/               les scripts Blender (étape 2)
```

Les outils utilisent Playwright, installé dans `~/Desktop/Portfolio/tools`.
