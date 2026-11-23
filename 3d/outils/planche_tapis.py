# Cardio 1 (22/11/2026): the treadmill, first prototype, after the user's reference (Landice L8, black).
# Puts the renders of outils/blender/rendus-tapis.sh on white into 3d/prototypes/tapis-de-course/, then writes
# planche.html and planche.jpg. The board shows the manufacturer's pictures next to our renders: it stays on the Mac
# (see .gitignore).
# usage: python3 3d/outils/planche_tapis.py
import html, subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
BRUTS = OUT / 'blender/_bruts/tapis'
DOS = OUT.parent / 'prototypes/tapis-de-course'
REF = '../../references/tapis/01-ta-reference-landice-l8.jpeg'
REC = '../../recherche/9-tapis-de-course/'


def e(s): return html.escape(s, quote=True)


def finish(plan, colour='noir'):
    src = BRUTS / f'tapis-{plan}-{colour}.png'
    dst = DOS / f'{plan}-{colour}.jpg'
    DOS.mkdir(parents=True, exist_ok=True)
    if src.exists():
        subprocess.run(['node', str(OUT / 'compose.mjs'), str(src), str(dst), '#FFFFFF'], check=True, capture_output=True)
    return dst.name


def fig(rel, cap, cls):
    return f'<figure class="{cls}"><img src="{e(rel)}" alt=""><div class="cap">{cap}</div></figure>'


duo = (fig(REF, '<b>Ta référence</b> · de l\'avant, à droite', 'm') + fig(finish('reference'), '<b>Notre tapis</b> · le même angle', 'm')
       + fig(REC + 'fitness-outlet/img-01.png', '<b>Le même tapis, côté écran</b> · photo du revendeur', 'm')
       + fig(finish('arriere-gauche'), '<b>Notre tapis</b> · le même angle', 'm'))
vues = (fig(finish('profil'), '<b>De profil</b> · le portique penché de 20° vers l\'utilisateur', 'm')
        + fig(finish('face'), '<b>De face</b> · le capot et ses deux grilles', 'm')
        + fig(finish('arriere'), '<b>De l\'arrière</b> · ce qu\'on voit en montant', 'm'))
details = (fig(finish('console'), '<b>La console</b> · ce que voit le coureur : l\'écran (éteint), les porte-gobelets, le clavier, les poignées cardio', 'm')
           + fig(finish('capot'), '<b>Le capot</b> · le dessus incliné, les grilles d\'aération', 'm')
           + fig(finish('bout'), '<b>L\'arrière</b> · les embouts en biais, le rouleau, les pieds réglables', 'm'))
finitions = (fig(finish('reference'), '<b>Noir satiné</b> · comme ta référence', 's')
             + fig(finish('reference', 'graphite'), '<b>Graphite</b>', 's')
             + fig(finish('reference', 'argent'), '<b>Argent</b> · l\'autre finition du vrai tapis', 's'))

notes = '''
<div class="colw notes">
<section>
  <div class="stitle">Le tapis de course, premier prototype</div>
  <div class="snote">22/11/2026 · cardio 1 · d'après ta référence, le Landice L8 noir</div>
  <div class="txt">La forme et les couleurs sombres de ta référence, sans la marque. Les rendus sont seuls sur le blanc, sans sol ni ombre.</div>
</section>
<section>
  <div class="stitle">Ce qu'on a repris</div>
  <ul class="list">
    <li><span class="lbl2">Les mesures du vrai tapis :</span> 2,11 × 0,89 × 1,56 m, une bande de 56 × 160 cm, une marche de 19 cm.</li>
    <li><span class="lbl2">Le portique :</span> deux montants larges et plats, penchés vers l'utilisateur, réunis en haut par un grand arrondi. Une seule pièce.</li>
    <li><span class="lbl2">Le haut :</span> la coque avec ses deux porte-gobelets, le clavier et son bouton STOP, deux poignées cardio chromées, deux mains courantes plates.</li>
    <li><span class="lbl2">La console :</span> une grande tablette inclinée, avec des aérations au dos.</li>
    <li><span class="lbl2">Le châssis :</span> des rails plats de chaque côté de la bande, des embouts coupés en biais à l'arrière, le capot moteur et ses deux grilles à l'avant.</li>
  </ul>
</section>
<section>
  <div class="stitle">Ce qu'on a changé</div>
  <ul class="list">
    <li>Plus de marque : ni logo, ni « L8 » sur le montant, ni nom sur la bande.</li>
    <li>L'écran reste éteint.</li>
  </ul>
</section>
<section>
  <div class="stitle">Questions</div>
  <ol class="list">
    <li>La forme est-elle assez proche ? Qu'est-ce qui doit changer ?</li>
    <li>La finition du portique : noir, graphite ou argent ?</li>
  </ol>
</section>
</div>'''

page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Le tapis de course</title>
<link rel="stylesheet" href="../../outils/planche_style.css"><style>
.board{{display:flex;flex-direction:column;gap:120px}}
.notes section{{width:680px}}
section.big{{width:2050px}}
.row{{display:flex;gap:28px;flex-wrap:wrap;align-items:flex-start}}
figure{{display:flex;flex-direction:column;gap:8px}}
figure img{{display:block;object-fit:contain;background:#fff}}
figure.m img{{width:470px;height:470px}}
figure.s img{{width:620px;height:620px}}
.cap{{font-size:12px;color:#6B6B6B;max-width:470px}}
figure.s .cap{{max-width:620px}}
.cap b{{color:#111}}
</style></head><body>
{notes}
<div class="board">
<section class="big"><div class="stitle">À côté de ta référence</div><div class="snote">les photos du fabricant, puis notre rendu sous le même angle</div>
  <div class="row">{duo}</div></section>
<section class="big"><div class="stitle">Les vues</div><div class="snote">noir satiné</div>
  <div class="row">{vues}</div></section>
<section class="big"><div class="stitle">Les détails</div><div class="snote">de près</div>
  <div class="row">{details}</div></section>
<section class="big"><div class="stitle">Les finitions du portique</div><div class="snote">les plastiques restent noirs</div>
  <div class="row">{finitions}</div></section>
</div></body></html>'''
(DOS / 'planche.html').write_text(page)
subprocess.run(['node', str(OUT / 'export.mjs'), str(DOS / 'planche.html'), str(DOS / 'planche.jpg'), '1'], check=True)
print('écrit', DOS / 'planche.html')
