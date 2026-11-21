# La planche de la recherche « les machines de musculation », étape 1 : les salles et les pectoraux (21/11/2026).
# Lit les sources.json de 3d/recherche/0-style-des-salles et 3d/recherche/1-pectoraux,
# écrit 3d/recherche/planche.html puis planche.png (export avec outils/export.mjs).
# usage : python3 3d/outils/planche_recherche.py
import json, html, subprocess
from pathlib import Path

OUT = Path(__file__).resolve().parent
REC = OUT.parent / 'recherche'
SRC = {}
for top in ('0-style-des-salles', '1-pectoraux'):
    for k, v in json.loads((REC / top / 'sources.json').read_text()).items():
        SRC[f'{top}/{k}'] = v

def e(s): return html.escape(s, quote=True)

def figs(paths, h=200):
    out = []
    for p in paths:
        v = SRC[p]
        num = p.split('/')[-1][:2]
        out.append(f'<figure><img src="{e(p)}" style="height:{h}px" alt=""><div class="cap"><b>{num}</b> {e(v["titre"])}</div></figure>')
    return ''.join(out)

def section(num, titre, sous, paths, note, h=200):
    grid = f'<div class="grid">{figs(paths, h)}</div>' if paths else ''
    return (f'<section class="theme"><div class="stitle">{num} {e(titre)}</div>'
            f'<div class="snote">{e(sous)}</div>{grid}'
            f'<div class="keep"><span class="lbl">À retenir</span><div class="txt">{note}</div></div></section>')

BF = '0-style-des-salles/01-basic-fit/'
Z = '0-style-des-salles/02-basic-fit-zones/'
F = '0-style-des-salles/03-basic-fit-force/'
P = '1-pectoraux/'
def all_in(prefix): return sorted(k for k in SRC if k.startswith(prefix))

salles = [
    section('0·1', 'Basic-Fit : les machines guidées', 'site de Basic-Fit · ce sont des Matrix Aura, repeintes en orange',
            all_in(BF),
            "Une haute <b>tour arrondie</b> cache la pile de poids, avec un chapeau perforé en haut. Le cadre est en <b>tubes ronds orange</b> ; les bras mobiles et la sellerie sont <b>noirs</b>. "
            "Les réglages ont des <b>boutons jaunes ou orange</b>, le pivot est rouge sur le curl, et chaque machine porte un <b>panneau d'instructions</b> illustré sur la tour."),
    section('0·2', 'Basic-Fit : les zones libres et force', 'site de Basic-Fit · bancs, racks, haltères, machines à disques',
            all_in(Z) + all_in(F),
            "Dans les zones libres, les bancs et les machines à disques sont <b>orange et noirs</b>, comme les machines guidées. Les racks sont noirs, les disques de couleur, "
            "les plateformes en bois. Les photos produits (0·2 04 à 08) sont des Matrix Magnum : la même famille que les photos du fabricant en 1·04 à 1·10."),
]

machines = [
    section('1·01', 'Chest press', 'développé assis guidé · confirmée chez Basic-Fit',
            all_in(P + '01-') + [BF + '02-chest-press-machine.jpg', BF + '01-chest-press-photo.jpg', BF + '03-chest-press-anim.gif'],
            "Assis, dos au dossier, on pousse deux poignées vers l'avant. On la reconnaît à <b>la tour à côté du siège</b>, à <b>l'arche</b> qui passe au-dessus de la tête et "
            "aux <b>deux poignées à hauteur de poitrine</b>. Matrix dessine une arche en tube rond, Technogym un bras anguleux."),
    section('1·02', 'Butterfly (pec deck)', 'écartés assis guidés · confirmé chez Basic-Fit (photo)',
            all_in(P + '02-') + [BF + '04-pec-fly-photo.jpg'],
            "Assis, on ramène devant soi <b>deux grands bras qui pivotent au-dessus des épaules</b>. Le dossier est haut. La version de Basic-Fit sert dans les deux sens : "
            "face à la machine pour les pectoraux, dos à la machine pour l'arrière des épaules."),
    section('1·03', 'Chest press convergente', 'développé assis, bras indépendants · à vérifier dans ta salle',
            all_in(P + '03-'),
            "Comme la chest press, mais <b>les deux bras sont indépendants et se rapprochent</b> en poussant. C'est une variante de la 1·01 : la tour et la sellerie sont les mêmes, seuls les bras changent."),
    section('1·04', 'Développé couché', 'banc olympique, barre et disques · confirmé chez Basic-Fit (photo 0·2)',
            all_in(P + '04-') + [F + '08-banc-developpe-couche.png'],
            "Un banc plat entre <b>deux montants qui tiennent la barre</b>, et des cornes pour ranger les disques. <b>La barre olympique et les disques</b> serviront partout : "
            "incliné, décliné, smith, squat, machines à disques. La photo 02 le montre : <b>la couleur du cadre est une option</b>, le dessin ne change pas."),
    section('1·05', 'Développé incliné', 'banc olympique incliné',
            all_in(P + '05-'),
            "La même famille que le 1·04 : <b>dossier incliné</b> d'environ 30 à 45°, siège et repose-pieds. Une variante rapide une fois le 1·04 modélisé."),
    section('1·06', 'Développé décliné', 'banc olympique décliné',
            all_in(P + '06-'),
            "Le banc descend vers la tête, avec <b>un cale-jambes en mousse</b> au bout. Une variante du 1·04."),
    section('1·07', 'Smith machine', 'barre guidée · à vérifier dans ta salle',
            all_in(P + '07-'),
            "Un grand cadre avec <b>deux rails verticaux chromés</b> : la barre y est fixée et ne peut que monter et descendre. Reconnaissable entre toutes. Sert aussi pour les épaules et les jambes."),
    section('1·08', 'Poulies vis-à-vis', 'crossover et station à poulies · une multi-station chez Basic-Fit (0·2 07)',
            all_in(P + '08-') + [F + '07-multi-station.png'],
            "Deux tours, chacune avec <b>une poulie qui coulisse sur un rail vertical</b>, reliées en haut par une traverse. Les détails à soigner : <b>le câble, les poulies et les poignées</b>. La plus longue à modéliser."),
    section('1·09', 'Banc réglable et haltères', 'poids libres · confirmés chez Basic-Fit (photos 0·2)',
            all_in(P + '09-') + [Z + '04-zone-halteres.jpg', Z + '05-banc-halteres.jpg'],
            "Le banc a <b>un dossier réglable sur une échelle à crans</b>. Les haltères et leur rack à trois niveaux servent à des dizaines d'exercices : une pièce à faire tôt."),
    section('1·10', 'Machines à disques', 'développés et butterfly chargés de disques · présentes chez Basic-Fit (photo 0·2 01)',
            all_in(P + '10-') + [Z + '01-machine-a-disques-orange.jpg'],
            "Pas de tour : <b>des bras avec des tiges pour charger les disques</b>. Plus brutes et plus industrielles que les machines guidées. Le panneau 06 montre "
            "<b>la position et le mouvement en deux images</b> : c'est exactement ce que notre app pourra faire en 3D."),
    section('1·11', 'Dips assistés', 'dips et tractions avec contrepoids · à vérifier dans ta salle',
            all_in(P + '11-'),
            "Une haute tour, <b>deux poignées parallèles</b> pour les dips, une barre en haut pour les tractions et <b>une plateforme pour les genoux</b> qui allège le poids du corps."),
    section('1·12', 'Pompes et exercices sans machine', 'pas de machine à modéliser',
            [],
            "Les pompes, les dips entre deux bancs, les écartés aux haltères : <b>sans machine, il faut un corps</b> pour montrer le mouvement. C'est le <b>personnage</b>, mis de côté pour plus tard "
            "(mascotte ou corps musclé réaliste). En attendant, ces exercices peuvent montrer le matériel seul (haltères, banc)."),
]

TAB = [
    ('1·01', 'Chest press', 'guidée', 'oui', 'Moyenne', 'tour, pile, siège, dossier, poignées, panneau'),
    ('1·02', 'Butterfly', 'guidée', 'oui', 'Moyenne', 'tour, pile, sellerie + deux grands bras'),
    ('1·03', 'Chest press convergente', 'guidée', 'peut', 'Faible', 'variante de la 1·01'),
    ('1·04', 'Développé couché', 'poids libres', 'oui', 'Faible', 'barre, disques, montants, banc'),
    ('1·05', 'Développé incliné', 'poids libres', 'peut', 'Faible', 'variante de la 1·04'),
    ('1·06', 'Développé décliné', 'poids libres', 'peut', 'Faible', 'variante de la 1·04'),
    ('1·07', 'Smith machine', 'barre guidée', 'peut', 'Moyenne', 'barre, disques, rails, cadre'),
    ('1·08', 'Poulies vis-à-vis', 'poulies', 'peut', 'Forte', 'tour, pile, poulies, câble, poignées'),
    ('1·09', 'Banc réglable et haltères', 'poids libres', 'oui', 'Faible', 'banc, haltères, rack'),
    ('1·10', 'Machines à disques', 'à disques', 'oui', 'Moyenne', 'disques, sellerie, bras à charger'),
    ('1·11', 'Dips assistés', 'guidée', 'peut', 'Moyenne', 'tour, pile, poignées, plateforme'),
    ('1·12', 'Pompes', 'sans machine', 'non', '—', 'le personnage, plus tard'),
]
LBL = {'oui': ('oui', 'confirmée'), 'peut': ('peut', 'à vérifier'), 'non': ('non', '—')}
rows = ''.join(f'<tr><td><b>{n}</b></td><td>{e(m)}</td><td>{e(t)}</td><td><span class="tag {LBL[bf][0]}">{LBL[bf][1]}</span></td><td>{d}</td><td>{e(p)}</td></tr>'
               for n, m, t, bf, d, p in TAB)

notes = f'''
<div class="colw notes">
<section>
  <div class="stitle">Les machines de musculation : la recherche</div>
  <div class="snote">21/11/2026 · étape 1 · les salles, puis le premier muscle : les pectoraux · sources dans sources.json</div>
  <div class="txt">Le but : modéliser dans Blender les machines des grandes salles européennes, <b>sans marque</b> mais <b>reconnaissables au premier coup d'œil</b>, toutes dans le même style, pour les montrer en 3D dans l'app.
  On avance muscle par muscle, puis machine par machine. Les images se citent par leur numéro (par exemple 1·02 03).</div>
</section>
<section>
  <div class="stitle">Ce que la recherche fait ressortir</div>
  <ol class="z">
    <li><b>1</b><span><span class="lbl2">Basic-Fit, c'est du Matrix.</span> Basic-Fit dit être équipé en Matrix et Technogym. Ses machines guidées sont des <b>Matrix Aura</b> (mêmes noms, même tour arrondie, mêmes boutons orange), et ses bancs et machines à disques des <b>Matrix Magnum</b>, repeints en orange (0·1, 0·2).</span></li>
    <li><b>2</b><span><span class="lbl2">Fitness Park, c'est du Technogym.</span> Des machines <b>Selection</b> noires aux touches jaunes (1·01 02, 1·02 03). Pour les zones force, Fitness Park utilise du matériel Eleiko et Pallini.</span></li>
    <li><b>3</b><span><span class="lbl2">On reconnaît une machine à sa silhouette, pas à sa marque.</span> D'un fabricant à l'autre, une chest press a la même anatomie : la tour, le siège, l'arche, les poignées. Ce sont <b>la forme et le mouvement</b> qu'il faut rendre justes. Les logos et les détails propres à une marque, on les laisse.</span></li>
    <li><b>4</b><span><span class="lbl2">La couleur du cadre est une option.</span> Matrix vend le même banc en noir ou en jaune (1·04 02), Basic-Fit le fait en orange. <b>Dans nos modèles, la couleur sera un réglage.</b> C'est ce qui permettra plus tard des machines aux couleurs de la salle de l'utilisateur.</span></li>
  </ol>
</section>
<section>
  <div class="stitle">L'anatomie d'une machine guidée</div>
  <div class="snote">les mêmes pièces reviennent sur presque toutes les machines</div>
  <ul class="list">
    <li><span class="lbl2">La tour :</span> la pile de poids, les deux tiges de guidage, la goupille de sélection, le capot et son chapeau.</li>
    <li><span class="lbl2">Le cadre :</span> des tubes ronds ou ovales, des pieds avec patins réglables.</li>
    <li><span class="lbl2">Le bras mobile :</span> son pivot (souvent de couleur), les poignées en caoutchouc.</li>
    <li><span class="lbl2">La sellerie :</span> le siège et le dossier noirs, réglables par une goupille jaune ou orange.</li>
    <li><span class="lbl2">Le câble et les poulies</span>, souvent cachés sous un carter.</li>
    <li><span class="lbl2">Le panneau d'instructions</span> et les petits accessoires : porte-bouteille, porte-téléphone.</li>
  </ul>
  <div class="txt"><b>La méthode qui en découle :</b> on modélise d'abord une <b>bibliothèque de pièces communes</b> (pile, goupille, poignée, coussin, poulie, pied, barre, disque), puis on assemble chaque machine avec ces pièces.
  Toutes les machines auront ainsi exactement le même style, et chaque nouvelle machine ira plus vite.</div>
</section>
<section>
  <div class="stitle">Les machines des pectoraux</div>
  <div class="snote">« chez Basic-Fit » : confirmée par le site ou les photos de Basic-Fit ; « à vérifier » : à confirmer dans ta salle</div>
  <table><tr><th></th><th>Machine</th><th>Type</th><th>Chez Basic-Fit</th><th>Travail</th><th>Pièces</th></tr>{rows}</table>
</section>
<section>
  <div class="stitle">L'ordre proposé</div>
  <ol class="z">
    <li><b>1</b><span><span class="lbl2">La chest press (1·01).</span> La plus emblématique, confirmée chez Basic-Fit, et elle contient presque toutes les pièces communes. Une fois faite, le reste va plus vite.</span></li>
    <li><b>2</b><span><span class="lbl2">Le butterfly (1·02)</span> : il réutilise la tour et la sellerie.</span></li>
    <li><b>3</b><span><span class="lbl2">Le développé couché (1·04)</span> : le banc, la barre et les disques, qui serviront partout.</span></li>
    <li><b>4</b><span><span class="lbl2">Les variantes :</span> incliné, décliné, convergente, banc réglable et haltères.</span></li>
    <li><b>5</b><span><span class="lbl2">Le reste :</span> smith, machines à disques, dips, puis les poulies.</span></li>
  </ol>
</section>
<section>
  <div class="stitle">Tes réponses (21/11)</div>
  <ul class="list">
    <li>Les onze machines pectoraux sont toutes dans ton Basic-Fit.</li>
    <li>Le style : <b>noir, sobre, sombre</b>, comme les machines Technogym de Fitness Park. Pas de couleur d'accent : on part de zéro.</li>
    <li><b>Universel</b> : pas de machine propre à une salle. Pour chaque machine, <b>plusieurs variantes</b> au choix de l'utilisateur, pour qu'il trouve toujours la sienne.</li>
    <li>Tes propres références de design iront dans <code>3d/references/</code>.</li>
  </ul>
</section>
<section>
  <div class="stitle">La suite : étape 2, les poids</div>
  <div class="txt">On commence par les pièces qu'on retrouvera partout : <b>les disques et les haltères</b>, en plusieurs designs sombres. Voir <code>3d/prototypes/01-poids-et-halteres/</code>.</div>
</section>
</div>'''

cols = [salles + machines[:3], machines[3:8], machines[8:]]
colhtml = ''.join('<div class="colw">' + ''.join(c) + '</div>' for c in cols)

page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Machines de musculation : recherche, étape 1</title>
<link rel="stylesheet" href="../outils/planche_style.css">
<style>
section.theme{{width:1240px}}
.grid{{display:flex;flex-wrap:wrap;gap:16px 12px}}
.grid figure{{display:inline-flex;flex-direction:column;gap:6px}}
.grid img{{width:auto;max-width:320px;object-fit:cover;display:block;background:#EEE}}
.grid .cap{{width:0;min-width:100%;font-size:11px;line-height:1.35;color:#6B6B6B}}
.grid .cap b{{color:#111;font-weight:600}}
.keep{{border-top:1px solid #E6E6E6;padding-top:14px;display:flex;flex-direction:column;gap:4px;max-width:1100px}}
.notes section{{width:760px}}
</style></head><body>
{notes}
{colhtml}
</body></html>'''

out = REC / 'planche.html'
out.write_text(page)
print('écrit', out)

if __name__ == '__main__':
    subprocess.run(['node', str(OUT / 'export.mjs'), str(out), str(REC / 'planche.png'), '1'], check=True)
