# Step 6 (21/11/2026): the Olympic bar and the collars.
# 1. The research board: 3d/recherche/4-barre-et-colliers/planche.png (third-party photos: stays on the Mac).
# 2. The prototypes board: finishes the renders of outils/blender/rendus-barre.sh into 3d/prototypes/04-barre-et-colliers/
#    and writes planche.html and planche.jpg next to them.
# usage: python3 3d/outils/planche_barre.py
import json, html, subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
BRUTS = OUT / 'blender/_bruts/barre'
REC = OUT.parent / 'recherche/4-barre-et-colliers'
DOS = OUT.parent / 'prototypes/04-barre-et-colliers'
BG = '#F2F2F3'
LIGHT_FLOOR = ('chargee', 'theme', 'couleurs')


def e(s): return html.escape(s, quote=True)


def fig(rel, cap, cls):
    return f'<figure class="{cls}"><img src="{e(rel)}" alt=""><div class="cap">{cap}</div></figure>'


def row(letter, titre, txt, figs):
    head = (f'<div class="head"><span class="letter">{e(letter)}</span><div><div class="stitle">{e(titre)}</div>'
            f'<div class="txt">{txt}</div></div></div>') if titre else ''
    return f'<div class="piste">{head}<div class="renders">{"".join(figs)}</div></div>'


CSS = '''
.board{display:flex;flex-direction:column;gap:120px}
.notes section{width:660px}
section.big{width:2260px}
.piste{display:flex;flex-direction:column;gap:18px;padding:26px 0;border-top:1px solid #E6E6E6}
.head{display:flex;gap:16px;align-items:flex-start;max-width:1600px}
.letter{flex:none;width:34px;height:34px;border-radius:17px;background:#111;color:#fff;font-weight:600;font-size:15px;text-align:center;line-height:34px}
.renders{display:flex;gap:16px;flex-wrap:wrap}
figure{display:flex;flex-direction:column;gap:8px}
figure.p img{width:400px;height:500px;object-fit:cover;display:block}
figure.l img{width:720px;height:auto;display:block}
figure.r img{height:240px;width:auto;display:block}
.cap{font-size:12px;color:#6B6B6B}
.cap b{color:#111}
'''

# ------------------------------------------------------------------ 1. research board
SRC = json.loads((REC / 'sources.json').read_text())
rfig = lambda pre: ''.join(fig(k, f'<b>{k.split("/")[1][:2]}</b> {e(v["titre"])}', 'r') for k, v in sorted(SRC.items()) if k.startswith(pre))
rec_notes = '''
<div class="colw notes">
<section>
  <div class="stitle">La barre et les colliers : la recherche</div>
  <div class="snote">21/11/2026 · étape 6 · sources dans sources.json</div>
  <div class="txt">Ce qui fait reconnaître une barre olympique et ses colliers, pour la modéliser sans marque.</div>
</section>
<section>
  <div class="stitle">Ce qu'il faut retenir</div>
  <ol class="z">
    <li><b>1</b><span><span class="lbl2">Les mesures sont normées.</span> La barre homme fait 2,20 m pour 20 kg, avec une prise de 28 mm, 1 310 mm entre les bagues et des manchons de 50 mm sur 415 mm. La barre femme fait 2,01 m pour 15 kg, avec une prise de 25 mm, des manchons de 320 mm et pas de moletage au centre.</span></li>
    <li><b>2</b><span><span class="lbl2">La silhouette.</span> Un manchon poli, une bague d'arrêt large, une bague d'identification de couleur (dorée en compétition, argentée à l'entraînement chez Eleiko), un embout plat au bout du manchon.</span></li>
    <li><b>3</b><span><span class="lbl2">Le moletage.</span> Des pointes de diamant, coupées par des repères lisses (81 et 91 cm) qui aident à placer les mains.</span></li>
    <li><b>4</b><span><span class="lbl2">Les finitions.</span> Le chrome (classique), le noir (céramique ou oxyde), ou tout noir.</span></li>
    <li><b>5</b><span><span class="lbl2">Trois colliers.</span> La pince à ressort, la moins chère et la plus courante en salle ; le collier à levier en plastique ; le collier en aluminium usiné, le plus haut de gamme. Tous existent en couleurs.</span></li>
  </ol>
</section>
</div>'''
rec_page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Barre et colliers : recherche</title>
<link rel="stylesheet" href="../../outils/planche_style.css"><style>{CSS}</style></head><body>
{rec_notes}
<div class="board">
<section class="big"><div class="stitle">Les barres</div><div class="snote">Eleiko, Matrix</div><div class="renders">{rfig('barres/')}</div></section>
<section class="big"><div class="stitle">Les colliers</div><div class="snote">pinces à ressort, colliers à levier en plastique, colliers en aluminium</div><div class="renders">{rfig('colliers/')}</div></section>
</div></body></html>'''
(REC / 'planche.html').write_text(rec_page)
subprocess.run(['node', str(OUT / 'export.mjs'), str(REC / 'planche.html'), str(REC / 'planche.png'), '1'], check=True)


# ------------------------------------------------------------------ 2. prototypes board
def finish(name):
    src = BRUTS / f'{name}.png'
    dst = DOS / f'{name}.jpg'
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.exists():
        if any(k in name for k in LIGHT_FLOOR):
            subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '90', str(src), '--out', str(dst)], check=True, capture_output=True)
        else:
            subprocess.run(['node', str(OUT / 'compose.mjs'), str(src), str(dst), BG], check=True, capture_output=True)
    return dst.name


FIN = [('A', 'Noir et acier', "L'arbre noir (revêtement céramique satiné), les manchons et la bague d'arrêt en chrome. Le noir sobre, avec l'acier qui accroche la lumière, comme l'insert des disques."),
       ('B', 'Tout acier', "L'arbre en chrome satiné, les manchons polis. La barre classique des salles."),
       ('C', 'Tout noir', "L'arbre noir, les manchons et la bague d'arrêt en métal noir. La plus sobre.")]
PL = [('entiere', 'La barre entière', 'l'), ('manchon', 'Le manchon, la bague, le début du moletage', 'p'), ('embout', "L'embout gravé", 'p'),
      ('moletage', 'Le moletage et un repère, en lumière rasante', 'p'), ('chargee', 'Chargée : 20 et 10 kg, colliers en aluminium', 'l')]
s_barre = ''.join(row(l, t, txt, [fig(finish(f'barre-{l}-{p}'), cap, c) for p, cap, c in PL]) for l, t, txt in FIN)
s_gamme = row('', '', '', [fig(finish('barre-A-gamme'), 'La barre homme (20 kg, 2,20 m) et la barre femme (15 kg, 2,01 m)', 'l')])
s_col = (row('', '', '', [fig(finish('barre-couleur-noir-rack'), 'La couleur sur la bague et sur l\'embout : les huit coloris', 'l')])
         + row('', '', '', [fig(finish(f'barre-couleur-{c}-theme'), f'Le thème {c} : disques, collier et bague', 'l') for c in ('rose', 'bleu', 'vert')]))
COL = [('pince', 'La pince à ressort', "Trois spires de fil d'acier, deux branches en V et leurs gaines. La plus courante en salle."),
       ('levier', 'Le collier à levier', "Un anneau en plastique, un boîtier et un levier plat sur charnière. Notre propre dessin, inspiré des colliers type Lock-Jaw."),
       ('alu', "Le collier en aluminium", "Un bloc usiné aux angles arrondis, fendu sur le dessus, avec un levier noir. Le plus haut de gamme, en aluminium anodisé.")]
s_colliers = ''.join(row(str(i + 1), t, txt, [fig(finish(f'collier-{k}-seul'), 'Seul', 'p'), fig(finish(f'collier-{k}-sur-barre'), 'Contre un disque', 'p'),
                                              fig(finish(f'collier-{k}-couleurs'), 'Les huit coloris', 'l')])
                     for i, (k, t, txt) in enumerate(COL))

notes = '''
<div class="colw notes">
<section>
  <div class="stitle">La barre et les colliers : les prototypes</div>
  <div class="snote">21/11/2026 · étape 6 · d'après la charte (Archivo Expanded, huit coloris, disques moulés)</div>
  <div class="txt">La barre olympique aux mesures normées, trois finitions, et trois colliers. La couleur de l'utilisateur va sur la <b>bague d'identification</b> et l'<b>embout</b> de la barre, et sur les colliers.</div>
</section>
<section>
  <div class="stitle">Ce qui est modélisé</div>
  <ul class="list">
    <li><b>La barre homme :</b> 2,20 m, prise de 28 mm, 1 310 mm entre les bagues, manchons de 50 × 415 mm. <b>La barre femme :</b> 2,01 m, prise de 25 mm, manchons de 320 mm.</li>
    <li>Un moletage en pointes de diamant, avec un moletage central (barre homme) et des repères lisses à 81 et 91 cm.</li>
    <li>Une bague d'identification et une bague d'arrêt chanfreinée. Le manchon a son joint anti-poussière et deux fines rainures.</li>
    <li>Un embout de couleur, gravé « 20 KG » (ou « 15 KG ») en Archivo Expanded.</li>
  </ul>
</section>
<section>
  <div class="stitle">Mon avis</div>
  <ul class="list">
    <li><b>Finition A (noir et acier)</b> par défaut : le noir sobre de la charte, et l'acier qui répond à l'insert des disques.</li>
    <li><b>Collier en aluminium</b> par défaut : le plus beau, et l'aluminium anodisé prend bien les huit couleurs.</li>
    <li><b>La pince à ressort</b> en variante, parce que c'est celle que la plupart des gens ont dans leur salle. C'est le principe des variantes : chacun retrouve son matériel.</li>
  </ul>
</section>
<section>
  <div class="stitle">Questions</div>
  <ol class="list">
    <li>Quelle finition de barre : A, B ou C ?</li>
    <li>Quels colliers garder, et lequel par défaut ?</li>
    <li>La couleur sur la bague et l'embout te convient-elle, ou veux-tu la couleur ailleurs sur la barre ?</li>
    <li>La suite : les autres barres (EZ, barres fixes, trap bar) ou les pièces communes des machines ?</li>
  </ol>
</section>
</div>'''
page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Barre et colliers : prototypes</title>
<link rel="stylesheet" href="../../outils/planche_style.css"><style>{CSS}</style></head><body>
{notes}
<div class="board">
<section class="big"><div class="stitle">La barre · trois finitions</div><div class="snote">chaque finition sous cinq plans</div>{s_barre}{s_gamme}</section>
<section class="big"><div class="stitle">La barre · la couleur</div><div class="snote">la bague d'identification et l'embout prennent la couleur choisie ; un thème colore tout le matériel</div>{s_col}</section>
<section class="big"><div class="stitle">Les colliers</div><div class="snote">seul, contre un disque, et dans les huit coloris</div>{s_colliers}</section>
</div></body></html>'''
(DOS / 'planche.html').write_text(page)
subprocess.run(['node', str(OUT / 'export.mjs'), str(DOS / 'planche.html'), str(DOS / 'planche.jpg'), '1'], check=True)
print('écrit', DOS / 'planche.html')
