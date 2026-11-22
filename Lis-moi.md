# Fitness app : le dossier

Nom provisoire, en attendant le vrai nom de l'application.

GitHub : https://github.com/amndrd/fitness-app (public, depuis le 21/11/2026).
- Le dépôt ne contient ni les images de recherche ni les planches qui les assemblent : ce sont des photos de Basic-Fit, Matrix et Technogym.
- Il ne contient pas non plus les scènes `.blend`, refaites par les scripts.
- Le détail est dans `.gitignore`.

Le plan complet de l'application est dans le Google Doc « fitness app · Plan complet ».

## Ce qu'on a sélectionné

Le dossier ne garde que les modèles validés (ménage du 22/11/2026). Leurs images sont dans `3d/modeles/`, et toutes les règles dans **`3d/charte.md`** (police, coloris, tailles, textures).

| Dossier | Le modèle | Le script |
|---|---|---|
| `3d/modeles/1-disque/` | le disque olympique, texture moulée, dans les huit coloris | `poids3.py` (sur la base de `poids2.py`) |
| `3d/modeles/2-haltere/` | l'haltère rond, grain fin, dans les huit coloris | `poids3.py` |
| `3d/modeles/3-barre/` | la barre olympique : B tout acier (l'originale), A et C en options, la couleur sur la bague et l'embout | `barre.py` |
| `3d/modeles/4-pince/` | la pince à ressort, le seul collier, pour tous les poids | `colliers.py` |
| `3d/modeles/5-haltere-disques/` | l'haltère à disques : poignée tout acier au bout chanfreiné, disques sablés au marquage blanc, une pince à chaque bout | `halteres.py` |

Les scripts sont dans `3d/outils/blender/`. Chaque modèle se refait avec son `rendus-*.sh` (les rendus bruts vont dans `_bruts/`, qui reste sur ton Mac).

**Les huit coloris :** noir (par défaut), graphite, blanc, rose, bleu, vert, rouge, sable.

## Le chemin parcouru

1. **La recherche (21/11) :** les salles et les machines pectoraux. Tu as choisi un style noir et sobre, comme les machines Technogym de Fitness Park, et des machines universelles.
2. **Les premiers disques et haltères (21/11) :** tu as retenu l'haltère rond et les disques épais.
3. **Le style des poids (21/11) :** l'analyse de tes références (Skelcore, Eleiko). Rien en haut et en bas du disque, le chiffre en blanc avec « KG », sans marque.
4. **La police (21/11) :** Archivo Expanded.
5. **Les textures et les coloris (21/11) :** le disque moulé, l'haltère au grain fin, les huit coloris.
6. **La barre olympique (21/11) :** la finition B tout acier, avec A et C en options.
7. **Les colliers (22/11) :** la pince, refaite d'après le modèle que tu as choisi. Le collier en aluminium, puis le levier, sont abandonnés : la pince est le seul collier.
8. **L'haltère à disques (22/11) :** d'après ta photo, avec la poignée tout acier au bout chanfreiné.

Les anciens modèles et leurs planches ont été retirés le 22/11 ; ils restent dans l'historique GitHub. La recherche est gardée dans `3d/recherche/`, et tes images de référence dans `3d/references/` (elles restent sur ton Mac).

## Structure

```
3d/
  charte.md                les choix validés : police, coloris, tailles, textures
  modeles/                 les images des modèles validés, un dossier par pièce
  recherche/               la recherche, étape par étape (les images restent sur ton Mac, sources.json garde les liens)
  references/              tes images de référence (sur ton Mac seulement)
  outils/
    blender/
      base.py              le studio, les matières, la caméra, le rendu (commun à tous les modèles)
      poids2.py            le disque et l'haltère rond (les formes)
      poids3.py            leurs textures et leurs coloris, la lumière du studio
      barre.py             la barre olympique
      colliers.py          la pince à ressort
      halteres.py          l'haltère à disques
      rendus-*.sh          refont les rendus de chaque modèle
    polices/               Archivo Expanded (et les polices essayées à l'étape 3), avec leurs licences OFL
    planche_recherche.py   refait la planche de la recherche (étape 1)
    planche_style_poids.py refait la planche de l'étape 3
    page_images.mjs        récupère les photos d'une page de fabricant
    contact.py             assemble les images d'un dossier en une seule image
    export.mjs             transforme une page HTML en image
    compose.mjs            pose un rendu transparent sur un fond
    credits.md             les éléments de tiers (HDRI) et leurs licences
```

Les outils utilisent Playwright, installé dans `~/Desktop/Portfolio/tools`.
