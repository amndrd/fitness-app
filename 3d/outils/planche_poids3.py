# The board of step 5: textures, colours and designs of the plate and the round dumbbell (21/11/2026).
# Finishes the renders of outils/blender/rendus-poids3.sh (background added to the transparent ones), saves them as
# JPEG in 3d/prototypes/03-textures-coloris/, then writes planche.html and planche.jpg.
# usage: python3 3d/outils/planche_poids3.py
import html, subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
BRUTS = OUT / 'blender/_bruts/poids3'
DOS = OUT.parent / 'prototypes/03-textures-coloris'
BG_D = '#F5F5F6'
BG_H = 'radial-gradient(ellipse at 50% 35%, #F4F4F4 0%, #E6E6E7 70%, #DDDDDE 100%)'
TRANSPARENT = {'face', 'rasant', '3q', 'flottant', 'macro', 'macro3q'}


def e(s): return html.escape(s, quote=True)


def finish(piece, groupe, var, plan):
    src = BRUTS / f'{piece}-{groupe}-{var}-{plan}.png'
    dst = DOS / piece / groupe / f'{var}-{plan}.jpg'
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.exists():
        if plan in TRANSPARENT:
            bg = BG_D if piece == 'disque' else BG_H
            subprocess.run(['node', str(OUT / 'compose.mjs'), str(src), str(dst), bg], check=True, capture_output=True)
        else:
            subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '90', str(src), '--out', str(dst)], check=True, capture_output=True)
    return str(dst.relative_to(DOS))


def fig(rel, cap, cls):
    return f'<figure class="{cls}"><img src="{e(rel)}" alt=""><div class="cap">{e(cap)}</div></figure>'


def row(letter, titre, txt, figs):
    head = (f'<div class="head"><span class="letter">{e(letter)}</span><div><div class="stitle">{e(titre)}</div>'
            f'<div class="txt">{txt}</div></div></div>') if titre else ''
    return f'<div class="piste">{head}<div class="renders">{"".join(figs)}</div></div>'


CAP_D = {'face': 'De face, façon catalogue', 'rasant': 'En lumière rasante : la texture', 'pile': 'En pile : la tranche et le dessus', '3q': 'De trois quarts'}
CAP_H = {'flottant': 'La paire de 40 kg', 'macro': 'En lumière rasante : le grain', 'macro3q': 'De près', 'entier': 'En entier', 'rangee': 'La rangée'}

TEX_D = [('moule', 'Moulé', "Le caoutchouc mat tel qu'il sort du moule : <b>grain fin</b>, <b>anneaux de moulage</b> à peine visibles, brillance qui varie légèrement."),
         ('satine', 'Satiné', "L'uréthane : <b>surface lisse et satinée</b>, un vernis léger, un très léger « peau d'orange ». Le plus haut de gamme."),
         ('mouchete', 'Moucheté', "Le <b>caoutchouc recyclé</b> des salles : de petites mouchetures grises dans la masse. Très reconnaissable."),
         ('vecu', 'Vécu', "Le moulé après des mois de salle : <b>traces brillantes</b>, <b>bords usés</b>, un peu de <b>craie</b> dans les creux, l'acier marqué de doigts.")]
TEX_H = [('fin', 'Grain fin', "Le grain actuel : fin et régulier, une poudre de reflets."),
         ('gros', 'Grain gros', "Un grain plus marqué, comme les haltères American Barbell : il se voit de loin."),
         ('satine', 'Satiné', "L'uréthane lisse et satiné, sans grain : plus doux, plus « objet »."),
         ('mouchete', 'Moucheté', "Le caoutchouc recyclé, comme le disque moucheté : les deux vont ensemble.")]
COULEURS = ['noir', 'graphite', 'blanc', 'rose', 'bleu', 'vert', 'rouge', 'sable']
DES_D = [('insert-noir', 'Insert noir', "L'acier anodisé noir : un disque entièrement noir, « stealth »."),
         ('insert-laiton', 'Insert laiton', "Un insert couleur laiton : le noir devient premium."),
         ('tranche-rose', 'Tranche de couleur', "Le disque reste noir, seule la tranche prend la couleur : elle se voit quand les disques sont rangés."),
         ('chiffres-bleus', 'Chiffres de couleur', "Le disque noir, les chiffres dans la couleur choisie.")]
DES_H = [('face-rose', 'Face de couleur', "La tête reste noire, seul le médaillon prend la couleur."),
         ('liseré-acier', 'Liseré en acier', "Le liseré autour de la face devient une bague d'acier poli."),
         ('tout-noir', 'Tout noir', "Poignée et collerettes en acier noir : l'haltère entièrement noir."),
         ('poignee-laiton', 'Poignée laiton', "Poignée et collerettes couleur laiton, comme l'insert laiton du disque.")]

# ---- the plate
s_tex_d = ''.join(row(str(i + 1), t, txt, [fig(finish('disque', 'texture', v, p), CAP_D[p], 'p' if p != 'pile' else 'l') for p in ('face', 'rasant', 'pile')])
                  for i, (v, t, txt) in enumerate(TEX_D))
s_col_d = (row('', '', '', [fig(finish('disque', 'couleur', 'tous', 'alignes'), 'Les huit coloris', 'xl'),
                            fig(finish('disque', 'couleur', 'mix', 'pile'), 'Une pile de trois coloris', 'l')])
           + row('', '', '', [fig(finish('disque', 'couleur', c, 'face'), c.capitalize(), 's') for c in COULEURS]))
s_des_d = row('', '', '', [fig(finish('disque', 'design', v, '3q'), t, 'p') for v, t, _ in DES_D])
s_des_d_txt = '<ul class="list">' + ''.join(f'<li><b>{e(t)}.</b> {e(x)}</li>' for _, t, x in DES_D) + '</ul>'
# ---- the dumbbell
s_tex_h = ''.join(row(str(i + 1), t, txt, [fig(finish('haltere', 'texture', v, p), CAP_H[p], 'p') for p in ('flottant', 'macro')])
                  for i, (v, t, txt) in enumerate(TEX_H))
s_col_h = (row('', '', '', [fig(finish('haltere', 'couleur', 'tous', 'rangee'), 'Les huit coloris', 'xl')])
           + row('', '', '', [fig(finish('haltere', 'couleur', c, 'flottant'), c.capitalize(), 'p') for c in ('rose', 'bleu', 'blanc', 'sable')]))
s_des_h = (row('', '', '', [fig(finish('haltere', 'design', v, 'entier'), t, 'p') for v, t, _ in DES_H])
           + row('', '', '', [fig(finish('haltere', 'design', v, 'macro3q'), t + ', de près', 'p') for v, t, _ in DES_H]))
s_des_h_txt = '<ul class="list">' + ''.join(f'<li><b>{e(t)}.</b> {e(x)}</li>' for _, t, x in DES_H) + '</ul>'

notes = '''
<div class="colw notes">
<section>
  <div class="stitle">Textures, coloris et designs</div>
  <div class="snote">21/11/2026 · étape 5 · police A (Archivo Expanded) · Blender et Cycles</div>
  <div class="txt">Le design ne change pas. On travaille ce qui rend un objet vrai (la texture, la lumière), puis ce qui le rend à soi (la couleur, les détails). Chaque piste est montrée sous plusieurs plans.</div>
</section>
<section>
  <div class="stitle">Ce qui rend un rendu réaliste</div>
  <ol class="z">
    <li><b>1</b><span><span class="lbl2">La lumière d'un vrai studio.</span> Une image d'éclairage photographiée dans un studio (Poly Haven, libre de droits) éclaire maintenant les objets. Les reflets de l'acier et du caoutchouc sont ceux d'un vrai lieu, plus seulement ceux de mes lampes.</span></li>
    <li><b>2</b><span><span class="lbl2">Rien n'est parfaitement lisse.</span> Le grain du moule, les anneaux de moulage, une brillance qui varie un peu d'un endroit à l'autre : c'est ce qui manquait au disque.</span></li>
    <li><b>3</b><span><span class="lbl2">La matière.</span> Une légère marbrure de couleur, et pour le moucheté les grains du caoutchouc recyclé.</span></li>
    <li><b>4</b><span><span class="lbl2">La vie.</span> Des traces, des bords usés, de la craie (la texture « vécu »). À doser : trop, et l'objet paraît sale.</span></li>
    <li><b>5</b><span><span class="lbl2">Les plans.</span> La lumière rasante révèle la texture, la pile montre l'épaisseur, la rangée montre la gamme.</span></li>
  </ol>
</section>
<section>
  <div class="stitle">La personnalisation dans l'app</div>
  <ul class="list">
    <li>Pour chaque équipement, l'utilisateur choisirait <b>une couleur</b> (les huit ci-contre, ou plus), <b>une finition</b> du métal (acier, noir, laiton) et <b>un accent</b> (tranche, face ou chiffres de couleur).</li>
    <li>Un <b>thème</b> appliquerait les mêmes choix à tout son matériel en une fois : tout rose, noir et laiton…</li>
    <li>Les modèles sont prêts : la couleur, la texture et les accents sont des <b>réglages</b>, pas des modèles différents. Il n'y a rien à remodéliser.</li>
    <li>Dans l'app, les textures fines (grain, mouchetures) seront « cuites » dans des images de texture. On le vérifiera au test sur l'iPhone.</li>
  </ul>
</section>
<section>
  <div class="stitle">Mon avis</div>
  <ul class="list">
    <li><b>Disque : le moulé</b> par défaut. Il est réaliste sans être sale, et il marche dans toutes les couleurs.</li>
    <li><b>Le satiné et le moucheté</b> en options de style. Le vécu, plutôt pour les images de présentation que dans l'app.</li>
    <li><b>Haltère :</b> le grain gros se lit mieux de loin. À comparer avec le fin sur les gros plans.</li>
    <li><b>Les accents</b> (tranche, face de couleur) gardent le noir sobre que tu aimes, tout en laissant de la place à la couleur.</li>
  </ul>
</section>
<section>
  <div class="stitle">Questions</div>
  <ol class="list">
    <li>Quelle texture pour le disque ? Et pour l'haltère, le grain fin ou le gros ?</li>
    <li>Les coloris : lesquels garder, et lesquels ajouter ?</li>
    <li>Parmi les designs (insert noir ou laiton, tranche, face, chiffres de couleur, tout noir), lesquels deviennent des options ?</li>
    <li>La suite : la barre et les colliers dans le même style, ou les pièces communes des machines ?</li>
  </ol>
</section>
</div>'''

page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Textures, coloris et designs</title>
<link rel="stylesheet" href="../../outils/planche_style.css">
<style>
.board{{display:flex;flex-direction:column;gap:120px}}
.notes section{{width:660px}}
section.big{{width:2260px}}
.piste{{display:flex;flex-direction:column;gap:18px;padding:26px 0;border-top:1px solid #E6E6E6}}
.head{{display:flex;gap:16px;align-items:flex-start;max-width:1600px}}
.letter{{flex:none;width:34px;height:34px;border-radius:17px;background:#111;color:#fff;font-weight:600;font-size:15px;text-align:center;line-height:34px}}
.renders{{display:flex;gap:16px;flex-wrap:wrap}}
figure{{display:flex;flex-direction:column;gap:8px}}
figure.p img{{width:440px;height:550px;object-fit:cover;display:block}}
figure.s img{{width:256px;height:320px;object-fit:cover;display:block}}
figure.l img{{width:780px;height:auto;display:block}}
figure.xl img{{width:1380px;height:auto;display:block}}
.cap{{font-size:12px;color:#6B6B6B}}
</style></head><body>
{notes}
<div class="board">
<section class="big"><div class="stitle">Le disque · les textures</div><div class="snote">noir · de face, en lumière rasante, en pile</div>{s_tex_d}</section>
<section class="big"><div class="stitle">Le disque · les coloris</div><div class="snote">texture moulée · chiffres blancs sur les foncés, anthracite sur les clairs</div>{s_col_d}</section>
<section class="big"><div class="stitle">Le disque · les designs</div><div class="snote">des accents sur le disque noir</div>{s_des_d_txt}{s_des_d}</section>
<section class="big"><div class="stitle">L'haltère · les textures</div><div class="snote">noir · la paire, puis le grain en lumière rasante</div>{s_tex_h}</section>
<section class="big"><div class="stitle">L'haltère · les coloris</div><div class="snote">grain fin · la rangée, puis quatre paires</div>{s_col_h}</section>
<section class="big"><div class="stitle">L'haltère · les designs</div><div class="snote">des accents sur l'haltère noir</div>{s_des_h_txt}{s_des_h}</section>
</div>
</body></html>'''

out = DOS / 'planche.html'
out.write_text(page)
subprocess.run(['node', str(OUT / 'export.mjs'), str(out), str(DOS / 'planche.jpg'), '1'], check=True)
print('écrit', out)
