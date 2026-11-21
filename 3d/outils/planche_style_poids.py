# The board of step 3: the analysis of the user's references (round dumbbell, Eleiko-style plates)
# and the research on that style (21/11/2026). Reads 3d/recherche/3-style-poids/sources.json and the
# user's images in 3d/references/, writes planche.html and planche.png in 3d/recherche/3-style-poids/.
# usage: python3 3d/outils/planche_style_poids.py
import json, html, subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
DOS = OUT.parent / 'recherche/3-style-poids'
SRC = json.loads((DOS / 'sources.json').read_text())
REF = '../../references/'


def e(s): return html.escape(s, quote=True)


def figs(items, h):
    return ''.join(f'<figure><img src="{e(p)}" style="height:{h}px" alt=""><div class="cap"><b>{e(n)}</b> {e(t)}</div></figure>' for p, n, t in items)


def research(prefix):
    return [(k, k.split('/')[1][:2], v['titre']) for k, v in sorted(SRC.items()) if k.startswith(prefix)]


def section(titre, sous, items, note, h=200, cls='theme'):
    return (f'<section class="{cls}"><div class="stitle">{titre}</div><div class="snote">{e(sous)}</div>'
            f'<div class="grid">{figs(items, h)}</div>'
            + (f'<div class="keep"><span class="lbl">À retenir</span><div class="txt">{note}</div></div>' if note else '') + '</section>')


refs = section('Tes références', 'les trois images que tu as choisies · dans 3d/references/', [
    (REF + 'halteres/01-ta-reference-rond.jpeg', 'H', "L'haltère rond : le style à retravailler"),
    (REF + 'disques/01-ta-reference-bleu-20.jpeg', 'D1', 'Le disque Eleiko Sport Training, 20 kg'),
    (REF + 'disques/02-ta-reference-rouge-25.jpeg', 'D2', 'Le même en 25 kg'),
], '', h=430)

halt = section('3·1 Les haltères ronds : la recherche', 'Skelcore, American Barbell, Hammer Strength', research('halteres/'),
               "Toujours le même vocabulaire : <b>têtes rondes épaisses</b> aux bords très arrondis, <b>grain mat</b> sur le tour, "
               "<b>collerette d'acier</b> à l'entrée de la tête, chiffre sur la face (et parfois sur le côté, 02 et 07).")
disq = section('3·2 Les disques noirs à insert : la recherche', 'REP (noir), Eleiko (ta référence, en couleur)', research('disques/'),
               "La version noire de ta référence existe (01 à 06) : <b>texte blanc en relief</b>, <b>grand insert en acier</b>, "
               "<b>rebord sur le pourtour</b>, texte en symétrie. Sur fond sombre (10, 11), c'est l'acier tourné qui fait vivre le disque.")

notes = '''
<div class="colw notes">
<section>
  <div class="stitle">Le style des poids : tes références et la recherche</div>
  <div class="snote">21/11/2026 · étape 3 · sources dans sources.json</div>
  <div class="txt">Tu gardes <b>l'haltère rond (B)</b>, à retravailler, et tu veux des <b>disques épais, ronds et noirs</b>. Voici l'analyse de tes trois images, puis ce que font les marques de ce style, et comment je propose de le traduire pour nous.</div>
</section>
<section>
  <div class="stitle">Ton haltère : l'analyse (H)</div>
  <ul class="list">
    <li><span class="lbl2">Le rendu.</span> Deux haltères qui flottent sur un gris très clair en dégradé, au format vertical 4:5. Lumière douce venue du haut, aucune ombre au sol. C'est le rendu « catalogue » des sites de matériel : propre, sans décor.</li>
    <li><span class="lbl2">Le design.</span> Des têtes rondes et épaisses (leur épaisseur fait environ 0,6 fois leur diamètre), aux bords très arrondis des deux côtés. La face est un <b>médaillon lisse, légèrement creusé, cerclé d'un fin liseré en relief</b>. La poignée est en acier satiné, moletée, avec une <b>collerette d'acier</b> à l'entrée de chaque tête.</li>
    <li><span class="lbl2">La texture.</span> Le tour de la tête est <b>grainé</b> : un aspect sablé, mat, avec de minuscules reflets. La face est plus lisse. Le contraste entre les deux fait tout le style.</li>
    <li><span class="lbl2">Les couleurs.</span> Un noir profond, mais pas un noir pur : un anthracite qui garde ses volumes. L'acier clair, le chiffre blanc.</li>
    <li><span class="lbl2">La typo.</span> Un chiffre très gras et géométrique, aux angles carrés adoucis. Dessous, la marque en petites capitales espacées.</li>
  </ul>
</section>
<section>
  <div class="stitle">Tes disques : l'analyse (D1, D2)</div>
  <ul class="list">
    <li><span class="lbl2">Le rendu.</span> Vue de face, sans perspective, centrée sur fond blanc. Lumière douce venue d'en haut à gauche : les lettres en relief portent une ombre légère.</li>
    <li><span class="lbl2">Le design.</span> Un disque plat et épais, avec un <b>rebord en relief sur tout le pourtour</b>, séparé de la face par une fine marche. Au centre, une <b>bague de caoutchouc en relief</b> autour d'un <b>grand insert en acier tourné</b> : des rainures concentriques polies et des reflets brossés qui tournent avec la lumière.</li>
    <li><span class="lbl2">Le texte, en symétrie.</span> Le nom en haut et en bas (celui du bas à l'envers), le poids à droite et à gauche (celui de gauche à l'envers). Le disque se lit dans les deux sens, qu'il soit à gauche ou à droite de la barre. Deux niveaux : le gros texte en blanc (nom, poids), le petit ton sur ton (SPORT, TRAINING).</li>
    <li><span class="lbl2">La texture.</span> Un caoutchouc mat, très légèrement marbré, comme moulé.</li>
    <li><span class="lbl2">Les couleurs.</span> Chez Eleiko, la couleur indique le poids (bleu 20, rouge 25 : la norme de l'haltérophilie). Chez nous, tout sera noir : ce sont le texte blanc et l'acier qui feront la différence.</li>
    <li><span class="lbl2">La typo.</span> Une linéale grasse et large (étendue).</li>
  </ul>
</section>
<section>
  <div class="stitle">Ce que la recherche montre</div>
  <ol class="z">
    <li><b>1</b><span><span class="lbl2">Ce style d'haltère est un standard « pro ».</span> Skelcore, American Barbell, Hammer Strength et Rogue font tous des têtes rondes noires grainées. Le grain n'est pas décoratif : il cache l'usure.</span></li>
    <li><b>2</b><span><span class="lbl2">Les grands rayons ont une raison.</span> Ils rendent l'haltère confortable quand il touche le corps (développé, curl).</span></li>
    <li><b>3</b><span><span class="lbl2">Le chiffre peut se répéter sur le côté</span> de la tête (3·1 02, 07) : on le lit même quand l'haltère est rangé dans le rack.</span></li>
    <li><b>4</b><span><span class="lbl2">Le disque noir de ta référence existe</span> chez REP, Rogue ou TKO : texte blanc, insert en acier, rebord (3·2 01 à 06). Le rebord protège l'insert : il le garde au-dessus du sol quand le disque est posé à plat.</span></li>
    <li><b>5</b><span><span class="lbl2">Épais et tous au même diamètre :</span> un 25 kg d'entraînement Eleiko fait environ 67 mm d'épaisseur. Tous les gros disques font 45 cm ; seuls les 5 kg et moins sont plus petits.</span></li>
    <li><b>6</b><span><span class="lbl2">Le fond :</span> tes trois références sont sur fond clair. Sur fond sombre (3·2 10, 11), c'est l'acier qui garde le disque lisible.</span></li>
  </ol>
</section>
<section>
  <div class="stitle">Comment je le traduis pour nous</div>
  <div class="lbl">L'haltère rond, version 2</div>
  <ul class="list">
    <li>Des têtes rondes et épaisses, avec de grands rayons à l'intérieur et à l'extérieur.</li>
    <li>La face : un médaillon lisse et creusé, cerclé d'un liseré en relief. Le tour de la tête : un grain mat et sablé.</li>
    <li>Le chiffre en blanc, grand, avec « KG » en petit à la place de la marque.</li>
    <li>Une poignée en acier satiné moletée, avec sa collerette d'acier.</li>
  </ul>
  <div class="lbl">Le disque, nouveau modèle</div>
  <ul class="list">
    <li>Noir, épais (20 kg : environ 65 mm), plat, 45 cm de diamètre, avec un rebord en relief sur le pourtour.</li>
    <li>Une bague de caoutchouc autour d'un grand insert en acier tourné aux rainures polies.</li>
    <li>Le poids en blanc et en relief, à droite et à gauche, en symétrie. « KG » ton sur ton.</li>
    <li>En haut et en bas, là où Eleiko met son nom : voir la question 1.</li>
  </ul>
  <div class="lbl">Le rendu</div>
  <ul class="list">
    <li>En plus de nos vues : l'haltère qui flotte au format 4:5, et le disque de face sans perspective, comme tes références.</li>
    <li>Pour les chiffres, trois polices libres à essayer : Archivo Expanded, Saira Expanded et Michroma. La police des prototypes (DIN, d'Apple) ne peut pas aller dans l'app.</li>
  </ul>
</section>
<section>
  <div class="stitle">Questions</div>
  <ol class="list">
    <li>En haut et en bas du disque, là où Eleiko met son nom : on laisse vide, on répète le poids, ou on garde la place pour le futur logo de l'app ?</li>
    <li>Le chiffre de l'haltère : blanc comme ta référence, ou gris, plus discret ?</li>
    <li>Je lance les prototypes : deux ou trois variantes de l'haltère et du disque, dans ce style ?</li>
  </ol>
</section>
</div>'''

page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Le style des poids : analyse et recherche</title>
<link rel="stylesheet" href="../../outils/planche_style.css">
<style>
section.theme{{width:1500px}}
.grid{{display:flex;flex-wrap:wrap;gap:16px 12px}}
.grid figure{{display:inline-flex;flex-direction:column;gap:6px}}
.grid img{{width:auto;max-width:520px;object-fit:cover;display:block;background:#EEE}}
.grid .cap{{width:0;min-width:100%;font-size:11.5px;line-height:1.35;color:#6B6B6B}}
.grid .cap b{{color:#111;font-weight:600}}
.keep{{border-top:1px solid #E6E6E6;padding-top:14px;display:flex;flex-direction:column;gap:4px;max-width:1200px}}
.notes section{{width:780px}}
code{{font-size:12px}}
</style></head><body>
{notes}
<div class="colw">{refs}{halt}{disq}</div>
</body></html>'''

out = DOS / 'planche.html'
out.write_text(page)
subprocess.run(['node', str(OUT / 'export.mjs'), str(out), str(DOS / 'planche.png'), '1'], check=True)
print('écrit', out)
