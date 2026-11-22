# Step 8 (22/11/2026): the plate-loaded dumbbell after the user's photo. Finishes the renders of
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


def finish(plan, colour='noir', fin='B', tex='gros', mark='relief', opaque=False):
    src = BRUTS / f'haltere-{plan}-{colour}-{fin}-{tex}-{mark}.png'
    dst = DOS / f'{plan}-{colour}-{fin}-{tex}-{mark}.jpg'
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
         + fig(finish('paire', fin='C'), '<b>Notre rendu</b> · même montage, poignée noire', 's') + '</div>'
         + fig(finish('detail', fin='C'), 'Le bout de l\'haltère : le disque, la pince, l\'embout noir', 's'))
haltere = (fig(finish('haltere', fin='C'), 'Poignée C, tout noir (comme ta photo)', 'w')
           + fig(finish('haltere', fin='B'), 'Poignée B, tout acier', 'w')
           + fig(finish('eclate', fin='B'), 'Éclaté : la poignée, trois disques par côté, une pince à chaque bout', 'x'))
poignee = fig(finish('poignees'), 'De devant à derrière : A (prise noire, acier), B (tout acier), C (tout noir)', 'x')
disques = (fig(finish('disques'), '1,25 kg · 2,5 kg · 5 kg', 'x')
           + fig(finish('gros-plan', tex='gros'), '<b>Sablée</b> (comme ta photo), marquage en relief', 's')
           + fig(finish('gros-plan', tex='fin'), '<b>Grain fin</b> (comme nos haltères ronds)', 's')
           + fig(finish('gros-plan', tex='moule'), '<b>Moulée</b> (comme nos disques)', 's')
           + fig(finish('gros-plan', tex='gros', mark='blanc'), 'Sablée, <b>marquage blanc</b>', 's'))
coloris = (fig(finish('couleurs', opaque=True), 'Les huit coloris (disque de 2,5 kg)', 'x')
           + fig(finish('haltere', colour='rose'), 'Rose : les disques et les gaines de la pince', 'w')
           + fig(finish('haltere', colour='bleu'), 'Bleu', 'w'))

notes = '''
<div class="colw notes">
<section>
  <div class="stitle">L'haltère à disques, d'après ta photo</div>
  <div class="snote">22/11/2026 · étape 8 · une poignée de 25 mm, des disques en ciment-vinyle et notre pince</div>
  <div class="txt">Tous les rendus sont sur le gris clair de ta photo.</div>
</section>
<section>
  <div class="stitle">L'analyse de ta photo</div>
  <ul class="list">
    <li><span class="lbl2">Les disques</span> sont en ciment enrobé de vinyle, au grain sablé et mat.
      <ul class="list">
        <li>Le bord est arrondi en bourrelet, avec la ligne de moulage au milieu.</li>
        <li>La face est plate, un peu en retrait. Le poids y est en relief le long de l'anneau, deux fois, face à face. Huit trous sont répartis en cercle.</li>
        <li>Le centre est lisse et en creux autour de l'alésage.</li>
      </ul></li>
    <li><span class="lbl2">Le montage :</span> trois disques par côté, du plus grand au plus petit vers l'extérieur.</li>
    <li><span class="lbl2">La barre</span> fait 25 mm. Ses bouts noirs dépassent après la pince.</li>
    <li><span class="lbl2">La pince</span> est la nôtre. Le modèle que tu as choisi était justement une pince pour barre de 25 mm : on la reprend à cette taille.</li>
  </ul>
</section>
<section>
  <div class="stitle">Les recherches</div>
  <ul class="list">
    <li><span class="lbl2">Les disques ciment-vinyle</span> du commerce, pour les barres de 25 mm :
      <ul class="list">
        <li>1,25 kg : Ø 185 × 34 mm ;</li>
        <li>2,5 kg : Ø 225 × 42 mm ;</li>
        <li>5 kg : Ø 282 × 50 mm ;</li>
        <li>un trou de 25 à 27 mm.</li>
      </ul></li>
    <li><span class="lbl2">Les poignées</span> mesurent de 35 à 45 cm, avec une prise moletée et deux bagues d'arrêt.</li>
    <li>Sources : MuscleSquad, Decathlon, YPC (FXR Sports). Les images sont dans <i>3d/recherche/7-halteres-disques</i>.</li>
  </ul>
</section>
<section>
  <div class="stitle">Nos choix</div>
  <ul class="list">
    <li><span class="lbl2">La poignée</span> fait 46 cm.
      <ul class="list">
        <li>Une prise moletée de 13 cm, entre deux bagues d'arrêt de 37 mm.</li>
        <li>Des manchons lisses de 15 cm, et des embouts noirs bombés.</li>
        <li>Trois finitions, comme pour la barre : A (prise noire), B (tout acier), C (tout noir).</li>
      </ul></li>
    <li><span class="lbl2">Les disques</span> pèsent 1,25, 2,5 et 5 kg. Le marquage « 2,5 KG » est en Archivo Expanded, courbé le long de l'anneau : lisible en bas, à l'envers en haut, comme sur ta photo.</li>
    <li><span class="lbl2">Le montage de ta photo :</span> 5 + 2,5 + 2,5 kg par côté, soit 20 kg de disques par haltère.</li>
    <li><span class="lbl2">La couleur</span> va sur les disques et sur les gaines de la pince.</li>
  </ul>
</section>
<section>
  <div class="stitle">Questions</div>
  <ol class="list">
    <li>Le style des disques et de l'haltère correspond-il à ce que tu veux ?</li>
    <li>Quelle finition de poignée : A, B ou C ?</li>
    <li>Quelle texture de disque : sablée, grain fin ou moulée ? Et le marquage : en relief ou en blanc ?</li>
    <li>Les disques de 1,25, 2,5 et 5 kg suffisent-ils, ou faut-il en ajouter (0,5 kg, 10 kg) ?</li>
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
<section class="big"><div class="stitle">L'haltère</div><div class="snote">les disques sablés, le marquage en relief, notre pince en 25 mm</div>
  <div class="row">{haltere}</div></section>
<section class="big"><div class="stitle">La poignée</div><div class="snote">trois finitions, comme la barre olympique</div>
  <div class="row">{poignee}</div></section>
<section class="big"><div class="stitle">Les disques</div><div class="snote">les trois poids, puis les textures et le marquage</div>
  <div class="row">{disques}</div></section>
<section class="big"><div class="stitle">Les coloris</div><div class="snote">les huit couleurs de la charte</div>
  <div class="row">{coloris}</div></section>
</div></body></html>'''
(DOS / 'planche.html').write_text(page)
subprocess.run(['node', str(OUT / 'export.mjs'), str(DOS / 'planche.html'), str(DOS / 'planche.jpg'), '1'], check=True)
print('écrit', DOS / 'planche.html')
