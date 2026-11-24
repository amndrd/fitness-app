# Treadmill, the new dashboard, after the user's reference: the dashboard of the Technogym Skillrun, without its brand.
# v3 (24/11/2026): the user's notes on v2 (screen lower, smaller column, the tray, the one-piece handlebar with its STOP,
# grips and paddles, the parting lines, a real screen). Puts the renders of outils/blender/rendus-tapis-tdb.sh on white
# into 3d/prototypes/tapis-de-course/tableau-de-bord/, then writes planche.html and planche.jpg there. The board shows
# the manufacturer's pictures next to our renders: it stays on the Mac (see .gitignore).
# usage: python3 3d/outils/planche_tapis_tdb.py
import html, subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
BRUTS = OUT / 'blender/_bruts/tapis'
DOS = OUT.parent / 'prototypes/tapis-de-course/tableau-de-bord'
REC = '../../../recherche/10-tableau-de-bord/technogym/'
REF = '../../../references/tapis/skillrun/'


def e(s): return html.escape(s, quote=True)


def finish(plan, suffix=''):
    src = BRUTS / f'tapis-{plan}-noir{suffix}.png'
    dst = DOS / f'{plan}{suffix.lower()}.jpg'
    DOS.mkdir(parents=True, exist_ok=True)
    if src.exists():
        subprocess.run(['node', str(OUT / 'compose.mjs'), str(src), str(dst), '#FFFFFF'], check=True, capture_output=True)
    return dst.name


def fig(rel, cap, cls='m'):
    return f'<figure class="{cls}"><img src="{e(rel)}" alt=""><div class="cap">{cap}</div></figure>'


avant_apres = (fig('tdb-face-v2.jpg', '<b>Avant (v2)</b> · face au coureur') + fig(finish('tdb-face'), '<b>Après (v3)</b> · face au coureur') +
               fig('tdb-detail-v2.jpg', '<b>Avant (v2)</b> · le bac et le guidon') + fig(finish('tdb-detail'), '<b>Après (v3)</b> · le bac et le guidon'))
original = (fig(REF + 'skillrun1.jpg', '<b>Le Skillrun</b> · le bac et la colonne') +
            fig(finish('tdb-detail'), '<b>Notre tapis</b> · le bac et la colonne') +
            fig(REF + '05-poignee-centrale-zoom.png', '<b>Le Skillrun</b> · le STOP et la poignée') +
            fig(finish('tdb-stop'), '<b>Notre tapis</b> · le STOP et la poignée') +
            fig(REF + '06-palette-zoom.png', '<b>Le Skillrun</b> · la palette') +
            fig(finish('tdb-palette'), '<b>Notre tapis</b> · la palette') +
            fig(REC + 'img-06.png', '<b>Le Skillrun</b> · face au coureur') +
            fig(finish('tdb-face'), '<b>Notre tapis</b> · face au coureur') +
            fig(REF + 'skillrun2.jpg', '<b>Le Skillrun</b> · l\'écran') +
            fig(finish('tdb-ecran'), '<b>Notre tapis</b> · l\'écran, éteint'))
tapis = (fig(finish('tdb-34'), '<b>Le tableau de bord</b> · de trois quarts') +
         fig(finish('tdb-dos'), '<b>De l\'avant</b> · le dos de l\'écran et la colonne') +
         fig(finish('reference'), '<b>Le tapis entier</b> · sous l\'angle de ta référence') +
         fig(finish('arriere-gauche'), '<b>Côté coureur</b>') +
         fig(finish('profil'), '<b>De profil</b>') +
         fig(finish('console'), '<b>Ce que voit le coureur</b> · d\'en haut'))

notes = '''
<div class="colw notes">
<section>
  <div class="stitle">Le tableau de bord, version 3</div>
  <div class="snote">24/11/2026 · d'après le Skillrun, sans la marque · avec les grandes poignées (ton choix)</div>
  <div class="txt">Chaque partie a été reprise une à une, à côté des images de Technogym.</div>
</section>
<section>
  <div class="stitle">Ce qui change</div>
  <ul class="list">
    <li><span class="lbl2">L'écran est plus bas</span> et sa colonne plus petite : 24 cm de large (au lieu de 30), 7 cm d'épaisseur, 17 cm de haut.</li>
    <li><span class="lbl2">Un vrai écran (éteint) :</span> un fin cadre anodisé autour d'une vitre bord à bord, posée un peu en retrait. Sous la vitre, la bordure noire et la zone d'affichage, un peu plus claire. Une coque au dos.</li>
    <li><span class="lbl2">Le bac,</span> d'une seule pièce avec la colonne :
      <ul>
        <li>un bloc qui avance vers le coureur, avec un rebord épais ;</li>
        <li>la ligne de séparation sous le rebord ;</li>
        <li>un fond en léger relief entouré d'une gouttière ;</li>
        <li>une cale inclinée pour le téléphone, coupée de deux encoches ;</li>
        <li>la face de la colonne qui s'arrondit jusqu'au fond.</li>
      </ul>
    </li>
    <li><span class="lbl2">Le guidon est une seule pièce modelée</span> : un tube dont l'épaisseur varie. Au sommet, il s'épaissit en un renflement lisse. Le STOP rouge vif en recouvre le dessus, en suit la courbe, et porte « STOP ». Les poignées moletées font corps avec la barre, un peu plus épaisses, avec une ligne à chaque bout.</li>
    <li><span class="lbl2">Les palettes</span> sont de fines lames qui sortent d'une bague moulée sur la barre : + en haut, − en bas, un trait entre les deux.</li>
    <li><span class="lbl2">Les lignes entre les pièces :</span>
      <ul>
        <li>les deux coques du boîtier ;</li>
        <li>les embouts ;</li>
        <li>le rebord et le corps du bac, sa gouttière ;</li>
        <li>les côtés de la colonne ;</li>
        <li>le renflement, les poignées et les bagues du guidon ;</li>
        <li>une petite poche à gauche de la colonne.</li>
      </ul>
    </li>
  </ul>
</section>
<section>
  <div class="stitle">Question</div>
  <ol class="list">
    <li>Le tableau de bord te convient-il ? Qu'est-ce qui doit encore changer ?</li>
  </ol>
</section>
</div>'''

page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Le tableau de bord, v3</title>
<link rel="stylesheet" href="../../../outils/planche_style.css"><style>
.board{{display:flex;flex-direction:column;gap:120px}}
.notes section{{width:680px}}
section.big{{width:2300px}}
.row{{display:flex;gap:28px;flex-wrap:wrap;align-items:flex-start}}
figure{{display:flex;flex-direction:column;gap:8px}}
figure img{{display:block;object-fit:contain;background:#fff}}
figure.m img{{width:530px;height:530px}}
.cap{{font-size:12px;color:#6B6B6B;max-width:530px}}
.cap b{{color:#111}}
</style></head><body>
{notes}
<div class="board">
<section class="big"><div class="stitle">Avant, après</div><div class="snote">la version 2, puis la version 3</div>
  <div class="row">{avant_apres}</div></section>
<section class="big"><div class="stitle">À côté du Skillrun</div><div class="snote">les images de Technogym, puis notre version</div>
  <div class="row">{original}</div></section>
<section class="big"><div class="stitle">Dans le tapis entier</div><div class="snote">avec les grandes poignées</div>
  <div class="row">{tapis}</div></section>
</div></body></html>'''
(DOS / 'planche.html').write_text(page)
subprocess.run(['node', str(OUT / 'export.mjs'), str(DOS / 'planche.html'), str(DOS / 'planche.jpg'), '1'], check=True)
print('écrit', DOS / 'planche.html')
