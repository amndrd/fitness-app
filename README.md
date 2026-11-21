# fitness-app

Nom provisoire. Une application mobile (iPhone et Android) d'assistant de musculation : créer ses programmes, les suivre en direct pendant la séance avec le minuteur de repos, voir sa progression. Les machines et le matériel de la salle sont affichés en 3D.

Le projet en est au début : la bibliothèque 3D des machines de musculation, modélisée dans Blender.

## Structure

```
3d/
  recherche/   la recherche par étape : les salles de sport, puis un dossier par muscle et par machine
  outils/      les scripts : récupération des références, planches, modèles Blender
```

L'application elle-même arrivera dans `app/` (Expo, React Native, TypeScript).

## Ce que le dépôt ne contient pas

- Les images de recherche (photos de fabricants et de salles) et les planches qui les assemblent : elles appartiennent à leurs auteurs. Les fichiers `sources.json` gardent le lien de chaque image.
- Les scènes Blender (`.blend`) : trop lourdes, et refaites par les scripts.

Le détail est dans `.gitignore`.

## Droits

Tous droits réservés. Le code est visible, mais il n'est pas sous licence libre : il ne peut pas être réutilisé sans autorisation.

La police Inter (`3d/outils/polices/`) est sous licence SIL Open Font License.
