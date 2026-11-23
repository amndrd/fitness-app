# Treadmill, correction 1 (23/11/2026): the front base (motor hood, plinth, feet), after the user's notes.
# Puts the renders of outils/blender/rendus-tapis-capot.sh on white into 3d/prototypes/tapis-de-course/, then writes
# planche-capot.html and planche-capot.jpg. The board shows close-ups of the manufacturer's pictures: it stays on the
# Mac (see .gitignore).
# usage: python3 3d/outils/planche_tapis_capot.py
import html, subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
BRUTS = OUT / 'blender/_bruts/tapis'
DOS = OUT.parent / 'prototypes/tapis-de-course'
ZOOM = '../../recherche/9-tapis-de-course/zooms/'


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


avant_apres = (fig('capot-v1-noir.jpg', '<b>Avant</b> · le premier prototype : un bloc droit') +
               fig(finish('capot'), '<b>Après</b> · le même angle'))
original = (fig(ZOOM + 'capot-noir-avant.png', '<b>L\'original</b> · de l\'avant, à droite') +
            fig(finish('capot-ref'), '<b>Notre tapis</b> · le même angle') +
            fig(ZOOM + 'capot-noir-arriere.png', '<b>L\'original</b> · côté coureur') +
            fig(finish('capot-arriere'), '<b>Notre tapis</b> · le même angle'))
vues = (fig(finish('capot-face'), '<b>De face</b> · la face bombée, les grilles en haut, le socle en retrait') +
        fig(finish('reference'), '<b>Dans le tapis entier</b> · sous l\'angle de ta référence'))
grilles = (fig('capot-ref-noir.jpg', '<b>A · Lamelles fines</b> · comme l\'original noir (proposé)') +
           fig(finish('capot-ref', '-cloisons'), '<b>B · Avec cloisons</b> · les lamelles coupées en quatre') +
           fig(ZOOM + 'capot-argent-avant.png', '<b>L\'original argent</b> · ses grilles à cloisons'))

notes = '''
<div class="colw notes">
<section>
  <div class="stitle">Le bas du tapis, correction 1</div>
  <div class="snote">23/11/2026 · le capot moteur, le socle et les pieds · le portique reste noir (ton choix)</div>
  <div class="txt">Seule cette partie a changé. Le reste du tapis est celui du premier prototype.</div>
</section>
<section>
  <div class="stitle">Ce qui change</div>
  <ul class="list">
    <li><span class="lbl2">Deux pièces au lieu d'un bloc :</span> une coque moulée en haut, un socle droit en bas, en retrait de 2 cm. La ligne entre les deux fait le tour.</li>
    <li><span class="lbl2">La face avant</span> est inclinée d'environ 23° et bombée au milieu. Ses coins sont très arrondis.</li>
    <li><span class="lbl2">Le dessus</span> est bombé, avec un plateau en léger relief au milieu. Sur l'original, c'est là qu'est le logo : on le laisse lisse.</li>
    <li><span class="lbl2">Côté coureur,</span> la coque se creuse face à la bande. Sur les côtés, elle descend en deux ailes qui recouvrent l'avant des rails et finissent en pointe.</li>
    <li><span class="lbl2">Les grilles</span> sont plus fines, avec 10 lamelles, en haut de la face avant et vers les coins.</li>
    <li><span class="lbl2">Le socle</span> porte la prise et l'interrupteur, à droite. Deux roues de transport sont aux coins avant.</li>
    <li><span class="lbl2">Les pieds :</span> les montants sont coupés à plat au sol, sans semelle, et boulonnés au châssis. Le châssis repose sur des patins en caoutchouc.</li>
  </ul>
</section>
<section>
  <div class="stitle">Questions</div>
  <ol class="list">
    <li>Le bas te convient-il, ou faut-il encore le retravailler ?</li>
    <li>Les grilles : A, lamelles fines, ou B, avec cloisons ?</li>
  </ol>
</section>
</div>'''

page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Le bas du tapis</title>
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
<section class="big"><div class="stitle">Avant, après</div><div class="snote">sous l'angle de ta capture</div>
  <div class="row">{avant_apres}</div></section>
<section class="big"><div class="stitle">À côté de l'original</div><div class="snote">les photos du fabricant de près, puis notre rendu sous le même angle</div>
  <div class="row">{original}</div></section>
<section class="big"><div class="stitle">De face et dans le tapis entier</div><div class="snote">noir</div>
  <div class="row">{vues}</div></section>
<section class="big"><div class="stitle">Les grilles</div><div class="snote">deux versions existent sur le vrai tapis</div>
  <div class="row">{grilles}</div></section>
</div></body></html>'''
(DOS / 'planche-capot.html').write_text(page)
subprocess.run(['node', str(OUT / 'export.mjs'), str(DOS / 'planche-capot.html'), str(DOS / 'planche-capot.jpg'), '1'], check=True)
print('écrit', DOS / 'planche-capot.html')
