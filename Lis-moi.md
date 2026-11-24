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

## Les stories Instagram (22/11/2026)

Des images de présentation des modèles, au format story (1080 × 1920), sur fond blanc et sans texte. Les objets sont seuls sur le blanc, sans sol ni ombre (comme `3d/modeles/2-haltere/flottant.jpg`).

**Tes choix (22/11) :**
- les barres en arc de la story 1 ;
- la colonne de disques vinyle et de pinces (devenue la story 4) ;
- les deux haltères séparés, chacun sur sa story.

**Validées telles quelles (22/11) :** toutes les stories ci-dessous.


| Story | Le contenu | Les prototypes |
|---|---|---|
| 1 | les barres en arc, et les disques alignés au-dessus, tournés de 64° (la face visible), un petit espace entre eux, la rangée qui déborde un peu de l'écran | une (22/11, d'après ta référence) |
| 2 | les haltères ronds, sur tout l'écran | a en colonne, b les faces, c la gamme de 5 à 40 kg |
| 3 | l'haltère à disques | a les disques, b l'éclaté, c la paire, d les huit coloris |
| 4 | les disques vinyle et les pinces, en colonne | ton choix |
| 5 | « coming soon » : le logo, petit, au centre de l'écran blanc, le texte dessous en Outfit | une |
| 6 | trois disques de face, noir, blanc et rose, l'un au-dessus de l'autre sur toute la hauteur de l'écran | une |

Les fichiers et leur planche (`planche.jpg`) sont dans `3d/stories/`. Le logo (`marque/logo.png`), la story 5 et la planche restent sur ton Mac : le logo n'est pas publié sur GitHub avant l'annonce de l'app. Les modèles restent dans la zone centrale : Instagram couvre le haut (le profil) et le bas (la réponse).

Pour refaire les images :
1. `3d/outils/blender/rendus-stories.sh` fait le rendu de chaque story avec le script `stories.py`.
2. `python3 3d/outils/stories.py` pose les objets sur le blanc.

## Les captures de Blender (22/11/2026)

Des captures d'écran de l'interface de Blender, une par modèle validé, au format story, dans `3d/stories/blender/` :
1. le disque, avec son arbre de matière ;
2. l'haltère rond, avec le maillage en fil de fer et la liste des objets ;
3. le bout de la barre, avec le panneau de la matière de l'embout ;
4. la pince, avec la liste des objets ;
5. l'haltère à disques, avec la liste de ses pièces.

Comment elles sont faites :
- Les captures sont prises par Blender lui-même, dans une fenêtre en portrait.
- La fenêtre fait 640 × 831 points : c'est la plus étroite que Blender accepte, à la hauteur de ton écran.
- La capture est posée sur toute la largeur de la story. Au-dessus et au-dessous, des bandes reprennent la couleur des barres de Blender.

Pour les refaire :
1. `3d/outils/blender/rendus-captures.sh`, avec le script `captures.py`. Blender s'ouvre quelques secondes à l'écran pour chaque modèle.
2. `python3 3d/outils/captures.py` pour la mise au format story.

## Le chemin parcouru

1. **La recherche (21/11) :** les salles et les machines pectoraux. Tu as choisi un style noir et sobre, comme les machines Technogym de Fitness Park, et des machines universelles.
2. **Les premiers disques et haltères (21/11) :** tu as retenu l'haltère rond et les disques épais.
3. **Le style des poids (21/11) :** l'analyse de tes références (Skelcore, Eleiko). Rien en haut et en bas du disque, le chiffre en blanc avec « KG », sans marque.
4. **La police (21/11) :** Archivo Expanded.
5. **Les textures et les coloris (21/11) :** le disque moulé, l'haltère au grain fin, les huit coloris.
6. **La barre olympique (21/11) :** la finition B tout acier, avec A et C en options.
7. **Les colliers (22/11) :** la pince, refaite d'après le modèle que tu as choisi. Le collier en aluminium, puis le levier, sont abandonnés : la pince est le seul collier.
8. **L'haltère à disques (22/11) :** d'après ta photo, avec la poignée tout acier au bout chanfreiné.
9. **L'inventaire (22/11) :** tout ce qu'on peut modéliser, dans le document « Fitness app · Tout ce qu'on peut modéliser » (137 objets). Tu as choisi de commencer par le cardio.
10. **Le tapis de course (22-23/11, en cours) :** d'après ta référence, le Landice L8 noir. L'analyse est dans `3d/recherche/9-tapis-de-course/analyse.md`.
    - **Où on en est :** le portique noir, avec sa grande forme arrondie et des arêtes nettes. Le bas est refait : la coque du capot, le socle, les grilles A et les pieds. Le haut aussi : de grandes palettes comme mains courantes, un bloc et son porte-gobelet à chaque coin, le clavier et les poignées cardio droites (A).
    - **Les images :** 10 vues dans `3d/prototypes/tapis-de-course/`. Il y a les trois quarts avant et arrière, le profil, la face, une vue en plongée, le dos, la console, le capot, la main courante et l'arrière de près. `rendus-tapis.sh` les refait.
    - **Le ménage (23/11) :** les anciennes versions, les variantes écartées et les planches de comparaison sont dans la Corbeille, dossier « Fitness app - ménage tapis 23-11 ». Ce qui était sur GitHub reste dans l'historique.
    - **Le tableau de bord (23-24/11) :** refait d'après celui du Technogym Skillrun, sans la marque. On retrouve :
      - l'écran de 22 pouces (éteint) sur une colonne ;
      - le bac d'une seule pièce avec la colonne ;
      - le guidon modelé d'une seule pièce : le renflement et son STOP rouge, les poignées moletées, les palettes + et − ;
      - les deux grandes poignées (ton choix) et les lignes entre les pièces.

      La version 3 est dans `3d/prototypes/tapis-de-course/tableau-de-bord/`. `rendus-tapis-tdb.sh` la refait, et `planche_tapis_tdb.py` fait sa planche, qui reste locale. L'analyse est dans `3d/recherche/10-tableau-de-bord/analyse.md`.
    - **En pause (24/11) :** le tapis attend ta relecture de la version 3. À reprendre ensuite :
      - tes corrections sur le tableau de bord ;
      - le bord arrière du STOP, qui a de petites marches vu de très près ;
      - les repères des palettes, blancs chez nous et jaunes sur le Skillrun : à choisir ;
      - la bande, qui paraît grise quand on la regarde en rasant ;
      - les 10 vues du dossier, à refaire avec `rendus-tapis.sh` : elles montrent encore l'ancien dessus.

Les anciens modèles et leurs planches ont été retirés le 22/11 ; ils restent dans l'historique GitHub. La recherche est gardée dans `3d/recherche/`, et tes images de référence dans `3d/references/` (elles restent sur ton Mac).

## Structure

```
3d/
  charte.md                les choix validés : police, coloris, tailles, textures
  modeles/                 les images des modèles validés, un dossier par pièce
  prototypes/              les modèles en cours (tapis-de-course : les vues de l'état actuel)
  stories/                 les stories Instagram et leur planche
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
      tapis.py             le tapis de course (rendus-tapis.sh refait ses 10 vues, rendus-tapis-tdb.sh le tableau de bord)
      stories.py           les scènes des stories Instagram
      captures.py          les captures de l'interface de Blender, une fenêtre en portrait par modèle
      rendus-*.sh          refont les rendus de chaque modèle
    polices/               Archivo Expanded (et les polices essayées à l'étape 3), avec leurs licences OFL
    planche_recherche.py   refait la planche de la recherche (étape 1)
    planche_style_poids.py refait la planche de l'étape 3
    planche_tapis_tdb.py   pose les rendus du tableau de bord du tapis sur le blanc et fait sa planche
    page_images.mjs        récupère les photos d'une page de fabricant
    contact.py             assemble les images d'un dossier en une seule image
    export.mjs             transforme une page HTML en image
    compose.mjs            pose un rendu transparent sur un fond
    stories.py             pose les stories sur le blanc (1080 × 1920) et fait leur planche
    credits.md             les éléments de tiers (HDRI) et leurs licences
```

Les outils utilisent Playwright, installé dans `~/Desktop/Portfolio/tools`.
