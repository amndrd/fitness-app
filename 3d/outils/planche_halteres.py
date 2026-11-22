# Step 8 (22/11/2026): the plate-loaded dumbbell after the user's photo. Version 2: the user's choices (handle B
# all steel without the black end caps, sandy plates, white marking) and three ways to finish the bare steel end. Finishes the renders of
# outils/blender/rendus-halteres.sh into 3d/prototypes/06-halteres-disques/, then writes planche.html and planche.jpg.
# The board shows the user's photo: it stays on the Mac (see .gitignore).
# usage: python3 3d/outils/planche_halteres.py
import html, subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
BRUTS = OUT / 'blender/_bruts/halteres'
DOS = OUT.parent / 'prototypes/06-halteres-disques'
REF = '../../references/halteres-disques/01-ta-reference-halteres.jpeg'
BG = '#ECECEE'                      # the light grey of the photo


def e(s): return html.escape(s, quote=True)


def finish(plan, colour='noir', end='chanfrein', opaque=False):
    src = BRUTS / f'haltere-{plan}-{colour}-B-gros-blanc-{end}.png'
    dst = DOS / (f'{plan}-{colour}.jpg' if plan in ('bouts', 'poignees') else f'{plan}-{colour}-{end}.jpg')   # those two show all three ends
    DOS.mkdir(parents=True, exist_ok=True)
    if src.exists():
        if opaque:
            subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '90', str(src), '--out', str(dst)], check=True, capture_output=True)
        else:
            subprocess.run(['node', str(OUT / 'compose.mjs'), str(src), str(dst), BG], check=True, capture_output=True)
    return dst.name


def fig(rel, cap, cls, ref=False):
    return f'<figure class="{cls}{" ref" if ref else ""}"><img src="{e(rel)}" alt=""><div class="cap">{cap}</div></figure>'


photo = (f'<div class="duo">{fig(REF, "<b>Ta photo</b>", "s", True)}'
         + fig(finish('paire'), '<b>Notre rendu</b> · même montage, tout acier, marquage blanc', 's') + '</div>'
         + fig(finish('detail'), 'Le bout de l\'haltère : le disque, la pince, l\'acier nu', 's'))
bouts = (fig(finish('bout', end='chanfrein'), '<b>1 · Chanfrein</b> · un biseau de 1,5 mm, bout plat (comme les manchons de la barre)', 's')
         + fig(finish('bout', end='arrondi'), '<b>2 · Arrondi</b> · un arrondi de 5,5 mm, bout légèrement bombé', 's')
         + fig(finish('bout', end='creux'), '<b>3 · Creux</b> · le chanfrein et un creux dans la face (le bout de la barre olympique, sans son embout)', 's')
         + fig(finish('bouts'), 'De devant à derrière : 1 chanfrein, 2 arrondi, 3 creux', 's')
         + fig(finish('poignees'), 'Les trois poignées entières, dans le même ordre', 'x'))
haltere = (fig(finish('haltere'), 'Poignée tout acier, disques sablés, marquage blanc (bout 1, chanfrein)', 'w')
           + fig(finish('eclate'), 'Éclaté : la poignée, trois disques par côté, une pince à chaque bout', 'w'))
disques = (fig(finish('disques'), '1,25 kg · 2,5 kg · 5 kg', 'x')
           + fig(finish('gros-plan'), 'Sablé, marquage blanc', 's'))
coloris = (fig(finish('couleurs', opaque=True), 'Les huit coloris : marquage blanc, ou anthracite sur les teintes claires', 'x')
           + fig(finish('haltere', colour='rose'), 'Rose : les disques et les gaines de la pince', 'w')
           + fig(finish('haltere', colour='bleu'), 'Bleu', 'w'))

notes = '''
<div class="colw notes">
<section>
  <div class="stitle">L'haltère à disques, version 2</div>
  <div class="snote">22/11/2026 · étape 8 · tes choix appliqués, et trois façons de finir le bout en acier</div>
  <div class="txt">Tous les rendus sont sur le gris clair de ta photo.</div>
</section>
<section>
  <div class="stitle">Tes choix</div>
  <ul class="list">
    <li><span class="lbl2">La poignée</span> est tout en acier (B), sans les embouts noirs.</li>
    <li><span class="lbl2">Les disques</span> sont sablés, avec le marquage blanc. Sur les coloris clairs, il passe en anthracite pour rester lisible.</li>
    <li><span class="lbl2">Les poids :</span> 1,25, 2,5 et 5 kg.</li>
    <li><span class="lbl2">La pince</span> ne change pas : ses gaines sont à la bonne taille.</li>
  </ul>
</section>
<section>
  <div class="stitle">Ce qui change</div>
  <ul class="list">
    <li><span class="lbl2">Plus d'embout noir :</span> le manchon finit en acier nu, tourné dans la masse.</li>
    <li><span class="lbl2">Le manchon passe de 15 à 16,5 cm</span> (poignée de 49 cm). Avant, la pince dépassait un peu du bout de l'acier, et l'embout le cachait. Maintenant l'acier dépasse de 11 mm après la pince, comme sur ta photo.</li>
    <li><span class="lbl2">Un essai écarté :</span> deux fines gorges près du bout, comme sur la barre. Collées à la pince, elles se lisaient comme des spires en plus.</li>
  </ul>
</section>
<section>
  <div class="stitle">Rappel de l'analyse</div>
  <ul class="list">
    <li>Disques ciment-vinyle du commerce pour barre de 25 mm : 1,25 kg Ø 185 × 34 mm, 2,5 kg Ø 225 × 42 mm, 5 kg Ø 282 × 50 mm.</li>
    <li>Bord en bourrelet avec la ligne de moulage, huit trous, centre lisse en creux, le poids écrit deux fois le long de l'anneau.</li>
    <li>Trois disques par côté (5 + 2,5 + 2,5 kg), une pince à chaque bout.</li>
  </ul>
</section>
<section>
  <div class="stitle">Question</div>
  <ol class="list">
    <li>Quel bout pour la poignée : 1 chanfrein, 2 arrondi ou 3 creux ? <b>Ton choix : 1, le chanfrein.</b> L'étape 8 est validée.</li>
  </ol>
</section>
</div>'''

page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>L'haltère à disques</title>
<link rel="stylesheet" href="../../outils/planche_style.css"><style>
.board{{display:flex;flex-direction:column;gap:120px}}
.notes section{{width:680px}}
section.big{{width:2160px}}
.row{{display:flex;gap:28px;flex-wrap:wrap;align-items:flex-start}}
.duo{{display:flex;gap:10px;padding:14px;background:#F6F6F6}}
figure{{display:flex;flex-direction:column;gap:8px}}
figure.s img{{width:440px;height:440px;object-fit:cover;display:block}}
figure.w img{{width:700px;height:auto;display:block}}
figure.x img{{width:1060px;height:auto;display:block}}
.cap{{font-size:12px;color:#6B6B6B}}
.cap b{{color:#111}}
</style></head><body>
{notes}
<div class="board">
<section class="big"><div class="stitle">Comme ta photo</div><div class="snote">à gauche ta photo, à droite notre rendu</div>
  <div class="row">{photo}</div></section>
<section class="big"><div class="stitle">Le bout de la poignée</div><div class="snote">plus d'embout noir : l'acier nu, trois façons de le finir</div>
  <div class="row">{bouts}</div></section>
<section class="big"><div class="stitle">L'haltère</div><div class="snote">tout acier, disques sablés, marquage blanc, notre pince en 25 mm</div>
  <div class="row">{haltere}</div></section>
<section class="big"><div class="stitle">Les disques</div><div class="snote">les trois poids et le marquage blanc</div>
  <div class="row">{disques}</div></section>
<section class="big"><div class="stitle">Les coloris</div><div class="snote">les huit couleurs de la charte</div>
  <div class="row">{coloris}</div></section>
</div></body></html>'''
(DOS / 'planche.html').write_text(page)
subprocess.run(['node', str(OUT / 'export.mjs'), str(DOS / 'planche.html'), str(DOS / 'planche.jpg'), '1'], check=True)
print('écrit', DOS / 'planche.html')
