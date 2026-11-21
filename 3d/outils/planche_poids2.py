# The board of step 4: the plate and the round dumbbell reworked from the user's references (21/11/2026).
# Puts the transparent renders of outils/blender/rendus-poids2.sh on their background (the light grey of the
# references), saves them as JPEG in 3d/prototypes/02-disque-et-haltere/, then writes planche.html and planche.jpg.
# The board shows the user's references next to the renders: it stays on the Mac (see .gitignore).
# usage: python3 3d/outils/planche_poids2.py
import html, subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
BRUTS = OUT / 'blender/_bruts/poids2'
DOS = OUT.parent / 'prototypes/02-disque-et-haltere'
REF = '../../references/'
BG_DISQUE = '#F5F5F6'
BG_HALTERE = 'radial-gradient(ellipse at 50% 35%, #F4F4F4 0%, #E6E6E7 70%, #DDDDDE 100%)'
VARIANTES = [('A', 'archivo', 'Archivo Expanded', "Large et très grasse : la plus proche des disques Eleiko. Une famille complète, qui pourrait aussi servir à l'interface de l'app."),
             ('B', 'saira', 'Saira Expanded', "Des chiffres aux angles carrés adoucis : la plus proche de l'haltère de ta référence. Plus « sport »."),
             ('C', 'michroma', 'Michroma', "Très large et technique, un seul poids. La plus graphique, la moins classique.")]


def e(s): return html.escape(s, quote=True)


def finish(src_name, dst, bg):
    src = BRUTS / src_name
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not src.exists():
        return
    if bg:
        subprocess.run(['node', str(OUT / 'compose.mjs'), str(src), str(dst), bg], check=True, capture_output=True)
    else:
        subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '90', str(src), '--out', str(dst)], check=True, capture_output=True)


def fig(rel, cap, cls=''):
    return f'<figure class="{cls}"><img src="{e(rel)}" alt=""><div class="cap">{e(cap)}</div></figure>'


rows_d, rows_h = [], []
for lettre, slug, nom, txt in VARIANTES:
    figs_d, figs_h = [], []
    for vue, cap in (('face20', 'Le 20 kg, de face'), ('face25', 'Le 25 kg, de face'), ('tq', "De trois quarts : l'épaisseur")):
        dst = DOS / 'disque' / f'{lettre}-{slug}' / f'{vue}.jpg'
        finish(f'disque-{lettre}-{vue}.png', dst, BG_DISQUE)
        figs_d.append(fig(str(dst.relative_to(DOS)), cap, 'p'))
    for vue, cap in (('flottant', 'La paire de 40 kg, qui flotte'), ('face', 'La face de près')):
        dst = DOS / 'haltere' / f'{lettre}-{slug}' / f'{vue}.jpg'
        finish(f'haltere-{lettre}-{vue}.png', dst, BG_HALTERE)
        figs_h.append(fig(str(dst.relative_to(DOS)), cap, 'p'))
    head = f'<div class="head"><span class="letter">{lettre}</span><div><div class="stitle">{e(nom)}</div><div class="txt">{e(txt)}</div></div></div>'
    rows_d.append(f'<div class="piste">{head}<div class="renders">{"".join(figs_d)}</div></div>')
    rows_h.append(f'<div class="piste">{head}<div class="renders">{"".join(figs_h)}</div></div>')

common_d, common_h = [], []
for vue, cap in (('gamme', 'La gamme, de 25 à 1,25 kg'), ('barre', 'Sur la barre : 25 et 20 kg'), ('sombre', 'Sur fond sombre')):
    dst = DOS / 'disque' / 'commun' / f'{vue}.jpg'
    finish(f'disque-A-{vue}.png', dst, None)
    common_d.append(fig(str(dst.relative_to(DOS)), cap, 'l'))
for vue, cap in (('heros', 'La paire de 15 kg, posée'), ('gamme', '5, 15 et 30 kg'), ('sombre', 'Sur fond sombre')):
    dst = DOS / 'haltere' / 'commun' / f'{vue}.jpg'
    finish(f'haltere-A-{vue}.png', dst, None)
    common_h.append(fig(str(dst.relative_to(DOS)), cap, 'l'))

ref_d = (fig(REF + 'disques/01-ta-reference-bleu-20.jpeg', 'Ta référence : Eleiko 20 kg', 'p')
         + fig(REF + 'disques/02-ta-reference-rouge-25.jpeg', 'Ta référence : Eleiko 25 kg', 'p'))
ref_h = fig(REF + 'halteres/01-ta-reference-rond.jpeg', 'Ta référence : haltère rond', 'p')

notes = '''
<div class="colw notes">
<section>
  <div class="stitle">Le disque et l'haltère : les prototypes, version 2</div>
  <div class="snote">21/11/2026 · étape 4 · Blender et Cycles, d'après tes références</div>
  <div class="txt">Le disque reprend les disques Eleiko de ta référence, en noir. L'haltère, c'est le rond B retravaillé d'après l'haltère de ta référence.
  Les rendus imitent aussi la photo : le disque de face et sans perspective sur fond blanc, les haltères qui flottent sur un gris clair.</div>
</section>
<section>
  <div class="stitle">Ce qui est fait</div>
  <div class="lbl">Le disque</div>
  <ul class="list">
    <li>Noir et épais : 58 mm pour le 20 kg, 66 mm pour le 25 kg ; 45 cm de diamètre de 10 à 25 kg.</li>
    <li>Un rebord en relief sur le pourtour, une fine ligne autour du moyeu, une bague de caoutchouc.</li>
    <li>Un grand insert en acier tourné : reflets brossés en éventail et deux rainures polies.</li>
    <li>Le poids en blanc et en relief à droite et à gauche (retourné), « KG » ton sur ton dessous. Le haut et le bas restent vides.</li>
  </ul>
  <div class="lbl">L'haltère</div>
  <ul class="list">
    <li>Des têtes rondes et épaisses (0,57 fois leur diamètre), avec de grands rayons des deux côtés.</li>
    <li>Une face en médaillon lisse et creusé, cerclé d'un liseré, et un tour en caoutchouc grainé.</li>
    <li>Le chiffre et « KG » imprimés en blanc. Pas de marque.</li>
    <li>Une poignée en acier satiné moletée et des collerettes d'acier.</li>
  </ul>
</section>
<section>
  <div class="stitle">Trois variantes : trois polices</div>
  <div class="txt">La forme est la même partout ; seule la police des chiffres change. Les trois sont libres de droits (licence OFL) : elles peuvent aller dans l'app.
  Les vues communes (la gamme, la barre, le fond sombre) sont montrées avec la variante A.</div>
</section>
<section>
  <div class="stitle">Questions</div>
  <ol class="list">
    <li>Quelle police gardes-tu, A, B ou C ? Une seule pour les disques et les haltères, pour qu'ils forment une famille.</li>
    <li>Le rendu est-il assez proche de tes références ? Qu'est-ce qui manque ?</li>
    <li>La suite : la barre et les colliers, ou directement les pièces communes des machines et la chest press ?</li>
  </ol>
</section>
</div>'''

page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Disque et haltère : prototypes v2</title>
<link rel="stylesheet" href="../../outils/planche_style.css">
<style>
.board{{display:flex;flex-direction:column;gap:120px}}
.notes section{{width:640px}}
section.big{{width:2060px}}
.piste{{display:flex;flex-direction:column;gap:18px;padding:28px 0;border-top:1px solid #E6E6E6}}
.head{{display:flex;gap:16px;align-items:flex-start;max-width:1500px}}
.letter{{flex:none;width:34px;height:34px;border-radius:17px;background:#111;color:#fff;font-weight:600;font-size:15px;text-align:center;line-height:34px}}
.renders{{display:flex;gap:16px;flex-wrap:wrap}}
figure{{display:flex;flex-direction:column;gap:8px}}
figure.p img{{width:480px;height:600px;object-fit:cover;display:block}}
figure.l img{{width:640px;height:auto;display:block}}
.cap{{font-size:12px;color:#6B6B6B}}
.refs .cap{{color:#111;font-weight:600}}
</style></head><body>
{notes}
<div class="board">
<section class="big"><div class="stitle">Le disque</div><div class="snote">noir, épais, insert en acier tourné · trois polices</div>
  <div class="renders refs">{ref_d}</div>
  {"".join(rows_d)}
  <div class="piste"><div class="stitle">Les vues communes</div><div class="renders">{"".join(common_d)}</div></div>
</section>
<section class="big"><div class="stitle">L'haltère rond, version 2</div><div class="snote">médaillon lisse, tour grainé, chiffre et KG en blanc · trois polices</div>
  <div class="renders refs">{ref_h}</div>
  {"".join(rows_h)}
  <div class="piste"><div class="stitle">Les vues communes</div><div class="renders">{"".join(common_h)}</div></div>
</section>
</div>
</body></html>'''

out = DOS / 'planche.html'
out.write_text(page)
subprocess.run(['node', str(OUT / 'export.mjs'), str(out), str(DOS / 'planche.jpg'), '1'], check=True)
print('écrit', out)
