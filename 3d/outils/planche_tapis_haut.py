# Treadmill, correction 2 (23/11/2026): the top (the portal's corners, the shell, the handrails, the heart-rate grips),
# after the user's notes. Puts the renders of outils/blender/rendus-tapis-haut.sh on white into
# 3d/prototypes/tapis-de-course/, then writes planche-haut.html and planche-haut.jpg. The board shows close-ups of the
# manufacturer's pictures: it stays on the Mac (see .gitignore).
# usage: python3 3d/outils/planche_tapis_haut.py
import html, subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
BRUTS = OUT / 'blender/_bruts/tapis'
DOS = OUT.parent / 'prototypes/tapis-de-course'
ZOOM = '../../recherche/9-tapis-de-course/zooms/'
REFS = '../../references/tapis/'


def e(s): return html.escape(s, quote=True)


def finish(plan, suffix=''):
    src = BRUTS / f'tapis-{plan}-noir{suffix}.png'
    dst = DOS / f'{plan}-noir{suffix}.jpg'
    DOS.mkdir(parents=True, exist_ok=True)
    if src.exists():
        subprocess.run(['node', str(OUT / 'compose.mjs'), str(src), str(dst), '#FFFFFF'], check=True, capture_output=True)
    return dst.name


def fig(rel, cap, cls='m'):
    return f'<figure class="{cls}"><img src="{e(rel)}" alt=""><div class="cap">{cap}</div></figure>'


avant_apres = (fig('reference-haut-v1-noir.jpg', '<b>Avant</b> · le premier haut') +
               fig(finish('reference'), '<b>Après</b> · sous l\'angle de ta référence') +
               fig(finish('arriere-gauche'), '<b>Après</b> · côté coureur'))
original = (fig(ZOOM + 'haut-original-avant.png', '<b>L\'original</b> · de l\'avant, à droite') +
            fig(finish('haut-ref'), '<b>Notre tapis</b> · de la même place') +
            fig(ZOOM + 'haut-original-arriere.png', '<b>L\'original</b> · côté coureur') +
            fig(finish('haut-arriere'), '<b>Notre tapis</b> · de la même place') +
            fig(ZOOM + 'haut-original-main-courante.png', '<b>L\'original</b> · la main courante droite et sa poignée') +
            fig(finish('haut-poignee'), '<b>Notre tapis</b> · de la même place'))
poignees = (fig(finish('haut-cardio'), '<b>A · Droites</b> · comme l\'original : une barre, une longue gaine chromée') +
            fig(finish('haut-cardio', '-galbees'), '<b>B · Galbées</b> · moulées, coudées là où va la main, deux plaques d\'acier') +
            fig(finish('console'), '<b>A</b> · ce que voit le coureur') +
            fig(finish('console', '-galbees'), '<b>B</b> · ce que voit le coureur') +
            fig('console-haut-v1-noir.jpg', '<b>Avant</b> · le premier haut, ce que voit le coureur'))

notes = '''
<div class="colw notes">
<section>
  <div class="stitle">Le haut du tapis, correction 2</div>
  <div class="snote">23/11/2026 · le portique, la coque, les mains courantes, les poignées cardio · l'écran ne change pas</div>
  <div class="txt">Le bas validé ce matin ne bouge pas. Pour comparer, nos caméras sont placées au même endroit que celles des photos du fabricant.</div>
</section>
<section>
  <div class="stitle">Ce qui change</div>
  <ul class="list">
    <li><span class="lbl2">Le portique</span> a des angles moins arrondis, comme l'original : l'arrondi passe de 27 à 14 cm.</li>
    <li><span class="lbl2">Les mains courantes</span> sont de grandes palettes debout. Elles font 13 cm de haut à la racine et 9,5 cm au bout, pour 5 cm d'épaisseur. Leur bout est arrondi en D, et une petite lèvre court le long du haut. Elles sont plus basses : leur dessus est à 5 cm sous le portique.</li>
    <li><span class="lbl2">Aux deux coins,</span> un bloc arrondi porte le porte-gobelet et recouvre la racine de la main courante.</li>
    <li><span class="lbl2">Le clavier</span> est plus large : + et − de chaque côté, STOP au milieu, la clé de sécurité dessous.</li>
    <li><span class="lbl2">Les poignées cardio</span> partent des côtés du clavier, vers l'arrière et l'extérieur, et rentrent dans le bas de la racine des mains courantes.</li>
  </ul>
</section>
<section>
  <div class="stitle">Questions</div>
  <ol class="list">
    <li>Le haut te convient-il, ou faut-il encore le retravailler ?</li>
    <li>Les poignées cardio : A, droites, ou B, galbées ?</li>
  </ol>
</section>
</div>'''

page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Le haut du tapis</title>
<link rel="stylesheet" href="../../outils/planche_style.css"><style>
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
<section class="big"><div class="stitle">Avant, après</div><div class="snote">le tapis entier</div>
  <div class="row">{avant_apres}</div></section>
<section class="big"><div class="stitle">À côté de l'original</div><div class="snote">les photos du fabricant de près, puis notre rendu de la même place</div>
  <div class="row">{original}</div></section>
<section class="big"><div class="stitle">Les poignées cardio</div><div class="snote">deux propositions</div>
  <div class="row">{poignees}</div></section>
</div></body></html>'''
(DOS / 'planche-haut.html').write_text(page)
subprocess.run(['node', str(OUT / 'export.mjs'), str(DOS / 'planche-haut.html'), str(DOS / 'planche-haut.jpg'), '1'], check=True)
print('écrit', DOS / 'planche-haut.html')
