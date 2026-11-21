# The prototypes board of step 2: weight plates and dumbbells (21/11/2026).
# Takes the raw renders of outils/blender/rendus-poids.sh (_bruts/poids), saves them as JPEG into
# 3d/prototypes/01-poids-et-halteres/<piece>/<piste>/, then writes planche.html and planche.jpg next to them.
# usage: python3 3d/outils/planche_poids.py
import html, subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
BRUTS = OUT / 'blender/_bruts/poids'
DOS = OUT.parent / 'prototypes/01-poids-et-halteres'

DISQUES = [
    ('A', 'fonte', 'Fonte', 'La fonte peinte en noir satiné. Un moyeu et un rebord en relief, une face creusée, les chiffres en relief ton sur ton. Le disque classique, sans poignées.'),
    ('B', 'caoutchouc-poignees', 'Caoutchouc à poignées', "Le caoutchouc noir mat, trois poignées découpées près du bord, une bague chromée au centre. Le disque le plus répandu dans les grandes salles."),
    ('C', 'urethane', 'Uréthane', "L'uréthane noir satiné, deux poignées courbes, un moyeu en acier brossé avec sa collerette, les chiffres gravés en gris. Le plus sobre et le plus « premium »."),
    ('D', 'bumper', 'Bumper', "Le caoutchouc épais et mat, tous les gros disques au même diamètre, une bague chromée large, les chiffres imprimés à gauche et à droite. Le disque des zones force et des plateformes."),
]
HALTERES = [
    ('A', 'hexagonal', 'Hexagonal', "Des têtes à six pans en caoutchouc (elles ne roulent pas), une poignée chromée moletée, le poids en relief sur la face."),
    ('B', 'rond', 'Rond', "Des têtes rondes en caoutchouc aux bords très doux, une poignée chromée moletée. La forme la plus courante en salle."),
    ('C', 'douze-pans', 'Douze pans', "Des têtes à douze pans en uréthane, un embout en acier sombre avec le poids gravé en gris, une poignée en acier noir. Il va avec le disque C."),
]
VUES_D = [('heros', 'Le 20 kg'), ('gamme', 'La gamme, de 25 à 1,25 kg'), ('barre', 'Sur la barre'), ('heros-sombre', 'Sur fond sombre')]
VUES_H = [('heros', 'La paire de 15 kg'), ('gamme', '5, 15 et 30 kg'), ('detail', 'De près'), ('heros-sombre', 'Sur fond sombre')]


def e(s): return html.escape(s, quote=True)


def finish(piece, lettre, slug, vues):
    figs = []
    for vue, cap in vues:
        src = BRUTS / f'{piece}-{lettre}-{vue}.png'
        dst = DOS / piece / f'{lettre}-{slug}' / f'{vue}.jpg'
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.exists():
            subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '90', str(src), '--out', str(dst)],
                           check=True, capture_output=True)
        rel = dst.relative_to(DOS)
        figs.append(f'<figure><img src="{e(str(rel))}" alt=""><div class="cap">{e(cap)}</div></figure>')
    return ''.join(figs)


def rows(piece, items, vues):
    out = []
    for lettre, slug, titre, txt in items:
        out.append(f'<div class="piste"><div class="head"><span class="letter">{lettre}</span><div><div class="stitle">{e(titre)}</div>'
                   f'<div class="txt">{e(txt)}</div></div></div><div class="renders">{finish(piece, lettre, slug, vues)}</div></div>')
    return ''.join(out)


notes = '''
<div class="colw notes">
<section>
  <div class="stitle">Les poids et les haltères : les prototypes</div>
  <div class="snote">21/11/2026 · étape 2 · modélisés dans Blender par script, rendus dans Cycles</div>
  <div class="txt">Les premières pièces de la bibliothèque 3D : les disques, qu'on retrouvera sur les bancs, la smith et les machines à disques, et les haltères.
  Tout est noir et sobre. Les tailles sont les vraies : disques olympiques de 45 cm, alésage de 50 mm, barre de 2,20 m.</div>
</section>
<section>
  <div class="stitle">Comment lire la planche</div>
  <ul class="list">
    <li>Quatre pistes de disques (A à D) et trois d'haltères (A à C). Chaque ligne montre la même pièce sous quatre angles.</li>
    <li>La dernière image de chaque ligne est sur <b>fond sombre</b> : un objet noir sur fond noir ne se lit que par ses reflets. C'est ce qui nous attend si l'app a une interface sombre.</li>
    <li>Les chiffres sont traités différemment d'une piste à l'autre : en relief ton sur ton (A, B), gravés en gris (C), imprimés (D).</li>
  </ul>
</section>
<section>
  <div class="stitle">Mon avis</div>
  <ul class="list">
    <li><b>Disque C (uréthane)</b> pour les bancs et les machines : le plus sobre, les chiffres se lisent même en petit, et son moyeu en acier accroche la lumière sur fond sombre.</li>
    <li><b>Disque D (bumper)</b> en plus, plus tard, pour les racks et les plateformes de la zone force.</li>
    <li><b>Haltère C (douze pans)</b> : il reprend les matières du disque C (uréthane, acier sombre, chiffres gris). Les deux forment une famille.</li>
    <li>Le B (caoutchouc à poignées) est le plus courant en salle. Il pourrait devenir une <b>variante au choix</b> de l'utilisateur, comme pour les machines.</li>
  </ul>
</section>
<section>
  <div class="stitle">Questions</div>
  <ol class="list">
    <li>Quel disque et quel haltère gardes-tu ? Un mélange est possible (par exemple les poignées du B avec la matière du C).</li>
    <li>Les chiffres : gravés en gris, lisibles, ou ton sur ton, plus discrets ?</li>
    <li>Dans l'app, tu imagines plutôt les machines sur un fond sombre ou sur un fond clair ?</li>
  </ol>
</section>
</div>'''

page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Poids et haltères : prototypes</title>
<link rel="stylesheet" href="../../outils/planche_style.css">
<style>
.board{{display:flex;flex-direction:column;gap:120px}}
.notes section{{width:640px}}
section.big{{width:2560px}}
.piste{{display:flex;flex-direction:column;gap:18px;padding:28px 0;border-top:1px solid #E6E6E6}}
.piste:first-of-type{{border-top:none;padding-top:0}}
.head{{display:flex;gap:16px;align-items:flex-start;max-width:1500px}}
.letter{{flex:none;width:34px;height:34px;border-radius:17px;background:#111;color:#fff;font-weight:600;font-size:15px;text-align:center;line-height:34px}}
.renders{{display:flex;gap:16px}}
.renders figure{{display:flex;flex-direction:column;gap:8px}}
.renders img{{width:600px;height:auto;display:block}}
.cap{{font-size:12px;color:#6B6B6B}}
</style></head><body>
{notes}
<div class="board">
<section class="big"><div class="stitle">Les disques</div><div class="snote">A fonte · B caoutchouc à poignées · C uréthane · D bumper</div>{rows('disques', DISQUES, VUES_D)}</section>
<section class="big"><div class="stitle">Les haltères</div><div class="snote">A hexagonal · B rond · C douze pans</div>{rows('halteres', HALTERES, VUES_H)}</section>
</div>
</body></html>'''

out = DOS / 'planche.html'
out.write_text(page)
subprocess.run(['node', str(OUT / 'export.mjs'), str(out), str(DOS / 'planche.jpg'), '1'], check=True)
print('écrit', out)
