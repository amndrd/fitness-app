# Step 7 (22/11/2026): the two collars reworked from the user's references, shown side by side with them.
# 22/11, later: the clip rebuilt after the model chosen by the user (3d/recherche/6-pince-fab, its pictures stay local),
# each of its views next to ours.
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


FAB = '../../recherche/6-pince-fab/'
LIGHT = 'linear-gradient(#f6f6f6,#e8e8e8)'
DARK = 'radial-gradient(circle at 50% 45%,#3c3c3c,#1f1f1f 75%)'


def ref_crop(img, left, cap):
    """One view of the model (its pictures hold two views side by side)."""
    pos = '0 0' if left else '-440px 0'
    return (f'<figure class="s ref"><div class="crop" style="background-image:url({e(FAB + img)});background-position:{pos}"></div>'
            f'<div class="cap"><b>Le modèle</b> · {e(cap)}</div></figure>')


def duo_fab(img, left, cap, plan):
    return f'<div class="duo">{ref_crop(img, left, cap)}{fig(finish("pince", "noir", plan, LIGHT), "<b>Notre pince</b> · " + e(cap), "s")}</div>'


pince = ''.join([
    duo_fab('rendu-3.jpg', False, 'de dessus', 'dessus'),
    duo_fab('rendu-2.jpg', True, 'de côté', 'cote'),
    duo_fab('rendu-2.jpg', False, 'par les gaines', 'bout'),
    duo_fab('rendu-3.jpg', True, 'de trois-quarts', 'trois-quarts'),
    duo_fab('rendu-1.jpg', False, 'la spirale devant', 'arriere'),
    duo_fab('rendu-1.jpg', True, 'debout', 'debout'),
])
pince_hero = (f'<div class="duo"><figure class="w ref"><img src="{e(FAB + "img-01.jpg")}" alt=""><div class="cap"><b>Le modèle</b> · l\'image principale</div></figure>'
              + fig(finish('pince', 'noir', 'heros', DARK), '<b>Notre pince</b> · l\'image principale', 'w') + '</div>')
pince_plus = (fig(finish('pince', 'noir', 'sur-barre', '#F2F2F3'), 'Sur la barre, contre un disque', 'p')
              + fig(finish('pince', 'rose', 'trois-quarts', LIGHT), 'Gaines roses', 's') + fig(finish('pince', 'bleu', 'trois-quarts', LIGHT), 'Gaines bleues', 's')
              + fig(finish('pince', 'noir', 'couleurs'), 'Les huit coloris', 'l'))
levier = duo('04-ta-reference-levier.jpeg', 'fermé et ouvert', finish('levier', 'noir', 'paire'), 'fermé et ouvert')
levier_plus = (fig(finish('levier', 'noir', 'sur-barre', '#F2F2F3'), 'Sur la barre, contre un disque', 'p')
               + fig(finish('levier', 'rose', 'paire'), 'Rose', 's') + fig(finish('levier', 'bleu', 'paire'), 'Bleu', 's')
               + fig(finish('levier', 'noir', 'couleurs'), 'Les huit coloris', 'l'))

notes = '''
<div class="colw notes">
<section>
  <div class="stitle">Les deux colliers, d'après tes références</div>
  <div class="snote">22/11/2026 · étape 7 · la pince refaite d'après le modèle que tu as choisi, et le collier à levier</div>
  <div class="txt">Chaque rendu est placé à côté de sa référence, pris sous le même angle.</div>
</section>
<section>
  <div class="stitle">La pince : la logique du modèle</div>
  <ul class="list">
    <li><span class="lbl2">Ce que j'avais faux.</span> Je posais les gaines à plat, dans le plan de l'anneau, et je les tournais au hasard. Sur ce modèle, tout suit une logique : on serre les deux gaines entre les doigts pour ouvrir la spirale.</li>
    <li><span class="lbl2">La spirale est à plat :</span> trois spires serrées d'un fil rond. Elle fait trois épaisseurs de fil de haut, et le fil mesure 1/8 de son diamètre.</li>
    <li><span class="lbl2">Les deux bouts partent du même point de l'anneau</span>, en ligne droite : celui de la spire du haut part d'un côté, celui de la spire du bas de l'autre. Chacun reste à sa hauteur, puis se coude vers l'extérieur. Les deux branches forment un V d'environ 50°.</li>
    <li><span class="lbl2">Les gaines sont posées sur la tranche</span>, dans l'axe de leur branche. Leurs grandes faces sont verticales : c'est là qu'on appuie. Elles posent au sol avec la spirale et la dépassent un peu en hauteur. Le bout est arrondi. L'ouverture a une fente où entre le fil, en haut pour une gaine, en bas pour l'autre.</li>
    <li><span class="lbl2">Les proportions</span> sont mesurées sur ses images : gaines de 1,1 diamètre de long et 0,49 de haut, branches de 0,55.</li>
    <li><span class="lbl2">La taille.</span> Le modèle est une pince pour les barres de 25 à 28 mm. La nôtre garde ses proportions mais s'ouvre sur 51 mm, pour la barre olympique : fil de 7,8 mm, gaines de 73 × 33 × 10,5 mm.</li>
    <li><span class="lbl2">Le rendu :</span> un acier satiné (pas un miroir), un caoutchouc gris anthracite, un studio gris très clair aux ombres douces. L'image principale est sur fond gris foncé, comme celle du modèle.</li>
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
    <li>La pince correspond-elle maintenant au modèle ? Qu'est-ce qui diffère encore ?</li>
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
figure.w img{{width:782px;height:440px;object-fit:cover;display:block}}
.crop{{width:440px;height:440px;background-size:880px 440px;background-repeat:no-repeat}}
.cap{{font-size:12px;color:#6B6B6B}}
.cap b{{color:#111}}
</style></head><body>
{notes}
<div class="board">
<section class="big"><div class="stitle">La pince à ressort</div><div class="snote">à gauche le modèle que tu as choisi, à droite notre pince, sous le même angle</div>
  <div class="row">{pince}</div><div class="row">{pince_hero}</div><div class="row">{pince_plus}</div></section>
<section class="big"><div class="stitle">Le collier à levier</div><div class="snote">à gauche ta photo, à droite notre rendu</div>
  <div class="row">{levier}{fig(finish('levier', 'noir', 'detail'), 'Le levier et sa grille', 's')}</div><div class="row">{levier_plus}</div></section>
</div></body></html>'''
(DOS / 'planche.html').write_text(page)
subprocess.run(['node', str(OUT / 'export.mjs'), str(DOS / 'planche.html'), str(DOS / 'planche.jpg'), '1'], check=True)
print('écrit', DOS / 'planche.html')
