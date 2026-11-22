# Step 7 (22/11/2026): the two collars reworked from the user's references, shown side by side with them.
# 22/11, later: the clip's sleeves turned flat, as on the photo of the pair; the profile photo (another model) is no longer compared.
# Finishes the renders of outils/blender/rendus-colliers.sh into 3d/prototypes/05-colliers/, then writes
# planche.html and planche.jpg. The board shows the user's references: it stays on the Mac (see .gitignore).
# usage: python3 3d/outils/planche_colliers.py
import html, subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
BRUTS = OUT / 'blender/_bruts/colliers2'
DOS = OUT.parent / 'prototypes/05-colliers'
REF = '../../references/colliers/'
FLOOR = ('couleurs',)


def e(s): return html.escape(s, quote=True)


def finish(piece, colour, plan, bg='#FFFFFF'):
    src = BRUTS / f'collier2-{piece}-{colour}-{plan}.png'
    dst = DOS / piece / f'{colour}-{plan}.jpg'
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.exists():
        if plan in FLOOR:
            subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '90', str(src), '--out', str(dst)], check=True, capture_output=True)
        else:
            subprocess.run(['node', str(OUT / 'compose.mjs'), str(src), str(dst), bg], check=True, capture_output=True)
    return str(dst.relative_to(DOS))


def fig(rel, cap, cls, ref=False):
    return f'<figure class="{cls}{" ref" if ref else ""}"><img src="{e(rel)}" alt=""><div class="cap">{cap}</div></figure>'


def duo(ref_img, ref_cap, render, cap):
    return f'<div class="duo">{fig(REF + ref_img, "<b>Ta référence</b> · " + e(ref_cap), "s", True)}{fig(render, "<b>Notre rendu</b> · " + e(cap), "s")}</div>'


pince = ''.join([
    duo('02-ta-reference-pince-paire.jpeg', 'la paire', finish('pince', 'noir', 'paire'), 'la paire'),
    duo('01-ta-reference-pince-macro.jpeg', 'de près', finish('pince', 'noir', 'macro'), 'de près'),
])
pince_plus = (fig(finish('pince', 'noir', 'trois-quarts'), 'De trois-quarts : les gaines à plat, celle du bas pliée vers l\'arrière', 's')
              + fig(finish('pince', 'noir', 'sur-barre', '#F2F2F3'), 'Sur la barre, contre un disque', 'p')
              + fig(finish('pince', 'rose', 'paire'), 'Gaines roses', 's') + fig(finish('pince', 'bleu', 'paire'), 'Gaines bleues', 's')
              + fig(finish('pince', 'noir', 'couleurs'), 'Les huit coloris', 'l'))
levier = duo('04-ta-reference-levier.jpeg', 'fermé et ouvert', finish('levier', 'noir', 'paire'), 'fermé et ouvert')
levier_plus = (fig(finish('levier', 'noir', 'sur-barre', '#F2F2F3'), 'Sur la barre, contre un disque', 'p')
               + fig(finish('levier', 'rose', 'paire'), 'Rose', 's') + fig(finish('levier', 'bleu', 'paire'), 'Bleu', 's')
               + fig(finish('levier', 'noir', 'couleurs'), 'Les huit coloris', 'l'))

notes = '''
<div class="colw notes">
<section>
  <div class="stitle">Les deux colliers, d'après tes références</div>
  <div class="snote">22/11/2026 · étape 7 · la pince à ressort (gaines corrigées) et le collier à levier ; plus de collier en aluminium</div>
  <div class="txt">Chaque rendu est placé à côté de ta photo, pris sous le même angle, sur le même fond blanc.</div>
</section>
<section>
  <div class="stitle">La pince : l'analyse</div>
  <ul class="list">
    <li><span class="lbl2">Le fil.</span> Un acier chromé miroir d'environ 4,8 mm, deux spires serrées de 50 mm de diamètre intérieur.</li>
    <li><span class="lbl2">Les branches.</span> Elles sont courtes et coudées. L'une sort du haut de l'anneau et monte, l'autre sort du côté avec un petit S.</li>
    <li><span class="lbl2">Le sens des gaines (corrigé).</span> Les gaines sont à plat, dans le plan de l'anneau : vues de face, on voit leur grande face. Elles forment un V serré d'environ 40° : celle du haut monte en biais à 45°, celle du bas part vers la gauche. Celle du bas est pliée vers l'arrière : sur ta photo, elle paraît plus courte et montre son ouverture.</li>
    <li><span class="lbl2">Les gaines.</span> Plates, noires et satinées (84 × 26 × 10 mm), ouvertes en rectangle côté fil, arrondies au bout, avec des arêtes douces.</li>
    <li><span class="lbl2">Ta photo de profil</span> montre un autre modèle, aux gaines tournées d'un quart de tour. Elle n'est plus comparée : j'ai suivi la paire et le gros plan, qui vont ensemble (le gros plan montre la pince de dos).</li>
    <li><span class="lbl2">Le rendu.</span> Le chrome se photographie dans une pièce blanche avec quelques bandes noires. C'est ce qui donne ces reflets clairs coupés de traits sombres.</li>
  </ul>
</section>
<section>
  <div class="stitle">Le collier à levier : l'analyse</div>
  <ul class="list">
    <li><span class="lbl2">Deux mâchoires en C</span>, articulées en bas sur un axe : le corps, avec ses vis, et la mâchoire mobile. Le collier est massif : 46 mm de large pour environ 100 mm de diamètre.</li>
    <li><span class="lbl2">Un profil en écrou :</span> six lobes arrondis séparés par des creux.</li>
    <li><span class="lbl2">Une garniture en caoutchouc</span> à l'intérieur de l'anneau, qui serre la barre.</li>
    <li><span class="lbl2">En haut, une charnière à trois segments.</span> Le levier y pivote : il est courbé, avec deux bras, une fenêtre sur la came et une palette couverte d'une grille de 6 × 6 petits carrés. Fermé, il se rabat sur le côté ; ouvert, il se dresse et la mâchoire s'écarte.</li>
    <li><span class="lbl2">Des vis cruciformes noires</span> sur les deux faces, en plastique noir mat. Les ombres sont courtes et douces, sous les colliers.</li>
  </ul>
</section>
<section>
  <div class="stitle">Questions</div>
  <ol class="list">
    <li>Le sens des gaines de la pince est-il bon maintenant ? Le collier à levier te va-t-il ?</li>
    <li>Le collier par défaut : la pince ou le levier ?</li>
    <li>La couleur va sur les gaines (pince) et sur tout le plastique (levier). Ça te va ?</li>
  </ol>
</section>
</div>'''

page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Les deux colliers</title>
<link rel="stylesheet" href="../../outils/planche_style.css"><style>
.board{{display:flex;flex-direction:column;gap:120px}}
.notes section{{width:680px}}
section.big{{width:2160px}}
.row{{display:flex;gap:28px;flex-wrap:wrap;align-items:flex-start}}
.duo{{display:flex;gap:10px;padding:14px;background:#F6F6F6}}
figure{{display:flex;flex-direction:column;gap:8px}}
figure.s img{{width:440px;height:440px;object-fit:cover;display:block;background:#fff}}
figure.p img{{width:440px;height:550px;object-fit:cover;display:block}}
figure.l img{{width:900px;height:auto;display:block}}
.cap{{font-size:12px;color:#6B6B6B}}
.cap b{{color:#111}}
</style></head><body>
{notes}
<div class="board">
<section class="big"><div class="stitle">La pince à ressort</div><div class="snote">à gauche ta photo, à droite notre rendu</div>
  <div class="row">{pince}</div><div class="row">{pince_plus}</div></section>
<section class="big"><div class="stitle">Le collier à levier</div><div class="snote">à gauche ta photo, à droite notre rendu</div>
  <div class="row">{levier}{fig(finish('levier', 'noir', 'detail'), 'Le levier et sa grille', 's')}</div><div class="row">{levier_plus}</div></section>
</div></body></html>'''
(DOS / 'planche.html').write_text(page)
subprocess.run(['node', str(OUT / 'export.mjs'), str(DOS / 'planche.html'), str(DOS / 'planche.jpg'), '1'], check=True)
print('écrit', DOS / 'planche.html')
