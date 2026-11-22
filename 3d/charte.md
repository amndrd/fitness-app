# La charte du matériel 3D

Les choix validés, à respecter pour toutes les pièces de la bibliothèque : poids, barres, machines. Mise à jour le 22/11/2026.

## L'esprit

- **Noir, sobre, sombre** par défaut, comme les machines des grandes salles européennes (Fitness Park, Basic-Fit).
- **Universel** : sans marque, mais reconnaissable au premier coup d'œil, et propre à aucune salle en particulier.
- **Personnalisable** : l'utilisateur choisit la couleur de son matériel. La couleur est un réglage, jamais un autre modèle.
- **Réaliste** : rien n'est parfaitement lisse. La lumière vient d'un vrai studio (HDRI).

## La police

**Archivo Expanded** (licence SIL OFL), dans `3d/outils/polices/` :
- les chiffres en **ExtraBold** (graisse 800, largeur 125) ;
- les petites mentions (« KG ») en **SemiBold** (graisse 600), avec des lettres espacées.

## Les coloris

Huit couleurs, les mêmes pour toutes les pièces :

| Coloris | Couleur | Chiffres |
|---|---|---|
| Noir (par défaut) | `#1B1B1D` | blanc `#E7E7E8` |
| Graphite | `#3C3E42` | blanc |
| Blanc | `#E4E2DD` | anthracite `#303032` |
| Rose | `#D98A9B` | blanc |
| Bleu | `#1F4B86` | blanc |
| Vert | `#5E7A62` | blanc |
| Rouge | `#8B2D32` | blanc |
| Sable | `#CBB89D` | anthracite |

Les petites mentions (« KG » sur les disques) sont ton sur ton : de la couleur du disque, en relief.

## Les pièces validées

### Le disque

- **Forme :** d'après les disques Eleiko Sport Training, en noir. Un rebord en relief sur le pourtour, une fine ligne autour du moyeu, une bague de caoutchouc, un grand insert en acier tourné avec deux rainures polies.
- **Tailles :**

  | Poids | Diamètre | Épaisseur |
  |---|---|---|
  | 25 kg | 450 mm | 66 mm |
  | 20 kg | 450 mm | 58 mm |
  | 15 kg | 450 mm | 48 mm |
  | 10 kg | 450 mm | 38 mm |
  | 5 kg | 300 mm | 30 mm |
  | 2,5 kg | 240 mm | 24 mm |
  | 1,25 kg | 200 mm | 18 mm |

  L'alésage est olympique (50 mm).
- **Texte :** le poids en blanc et en relief, à droite, et retourné à gauche. « KG » est dessous, ton sur ton. **Le haut et le bas restent vides.**
- **Texture :** **moulée**. Un caoutchouc mat au grain fin, des anneaux de moulage à peine visibles, une brillance qui varie légèrement.

### L'haltère

- **Forme :** l'haltère rond, retravaillé d'après la référence Skelcore. Des têtes rondes et épaisses (environ 0,57 fois leur diamètre), avec de grands rayons des deux côtés. La face est un médaillon lisse et creusé, cerclé d'un liseré en relief. La poignée est en acier satiné moleté (33 mm), avec des collerettes d'acier.
- **Texte :** le chiffre et « KG » imprimés en blanc sur le médaillon. Pas de marque.
- **Texture :** **grain fin** sur le tour de la tête ; le médaillon reste lisse.

### La barre olympique

- **Mesures normées :**
  - barre homme : 2,20 m et 20 kg, prise de 28 mm, 1 310 mm entre les bagues, manchons de 50 × 415 mm ;
  - barre femme : 2,01 m et 15 kg, prise de 25 mm, manchons de 320 mm, sans moletage central.
- **Détails :** un moletage en pointes de diamant, avec des repères à 81 et 91 cm. La bague d'arrêt est chanfreinée, et le manchon a son joint et deux fines rainures.
- **Finition originale : B, tout acier** (arbre en chrome satiné, manchons polis). Deux options : A, noir et acier, et C, tout noir.
- **La couleur** va sur la bague d'identification et sur l'embout, gravé « 20 KG » (ou « 15 KG ») en Archivo Expanded. Un thème applique la même couleur aux disques, aux colliers et à la bague.

### Les colliers

Deux modèles seulement : **la pince à ressort** et **le collier à levier**, d'après les références de l'utilisateur (étape 7, validée le 22/11). **La pince pour les petites charges, le levier pour les grosses.** La couleur va sur les gaines de la pince et sur tout le plastique du levier.
- **La même pince** sert aussi aux barres de 25 mm (haltères à disques) : à cette taille, elle est réduite de moitié.
- **La pince :** d'après le modèle choisi par l'utilisateur (22/11). La spirale est à plat, trois spires serrées d'un fil d'acier satiné (1/8 du diamètre). Les deux bouts partent du même point de l'anneau, chacun à sa hauteur, puis s'écartent en V d'environ 50°. Les gaines en caoutchouc anthracite sont posées sur la tranche, leurs grandes faces verticales, bout arrondi et ouverture à fente. Elles posent au sol avec la spirale. Dimensions pour la barre olympique : 51 mm dedans, fil de 7,8 mm, gaines de 73 × 35 × 10,5 mm. Le fil reste toujours dans la fente de la gaine (paroi de 0,9 mm).

### L'haltère à disques (étape 8, en cours de validation)

- **Poignée de 25 mm et 46 cm :** une prise moletée de 13 cm, deux bagues d'arrêt de 37 mm, des manchons lisses de 15 cm et des embouts noirs bombés. Trois finitions, comme la barre : A (prise noire), B (tout acier), C (tout noir).
- **Disques ciment-vinyle :** 1,25 kg (Ø 185 × 34 mm), 2,5 kg (Ø 225 × 42 mm) et 5 kg (Ø 282 × 50 mm), avec un alésage de 26,6 mm. Le bord est en bourrelet avec la ligne de moulage, la face porte huit trous, le centre est lisse. Le poids est en relief le long de l'anneau, deux fois. La couleur est un réglage.
- **Une pince** à chaque bout.

## Gardé de côté

Les accents de design ne servent que si la personnalisation va un jour plus loin que le simple choix de la couleur. Ils sont prêts dans `3d/outils/blender/poids3.py`.
- **Disque :** insert noir ou laiton, tranche de couleur, chiffres de couleur.
- **Haltère :** face de couleur, liseré en acier, tout noir, poignée laiton.
- **Autres textures :** satiné, moucheté, vécu (disque) ; gros grain, satiné, moucheté (haltère).

Les rendus de ces pistes sont dans `3d/prototypes/03-textures-coloris/`.
