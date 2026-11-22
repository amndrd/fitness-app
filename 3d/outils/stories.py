# The Instagram stories (22/11/2026): puts the renders of outils/blender/rendus-stories.sh on white at
# 1080 x 1920 (the story format): the objects alone on white, no floor and no shadow (the user's choice, 22/11).
# Writes 3d/stories/*.jpg and 3d/stories/planche.jpg (the stories side by side, with labels: that board is for
# choosing, it is not posted).
# usage: python3 3d/outils/stories.py
import subprocess, tempfile
from pathlib import Path

OUT = Path(__file__).resolve().parent
BRUTS = OUT / 'blender/_bruts/stories'
DOS = OUT.parent / 'stories'
GROUPS = [   # story, its prototypes: scene, file, label on the board
    ('1 · La barre et ses disques', 'les barres en arc, les disques alignés au-dessus', [
        ('1', '1-barre-et-disques', 'les disques alignés et tournés')]),
    ('2 · Les haltères ronds', 'tout l\'écran pour eux', [
        ('2a', '2a-halteres-ronds-colonne', 'a · en colonne'),
        ('2b', '2b-halteres-ronds-faces', 'b · les faces'),
        ('2c', '2c-halteres-ronds-gamme', 'c · la gamme, de 5 à 40 kg')]),
    ('3 · L\'haltère à disques', 'quatre points de vue', [
        ('3a', '3a-haltere-disques-disques', 'a · les disques'),
        ('3b', '3b-haltere-disques-eclate', 'b · l\'éclaté'),
        ('3c', '3c-haltere-disques-paire', 'c · la paire'),
        ('3d', '3d-haltere-disques-couleurs', 'd · les huit coloris')]),
    ('4 · Disques vinyle et pinces', 'ton choix', [
        ('4', '4-vinyle-et-pinces', 'la colonne')]),
]
STORIES = [st for _, _, sts in GROUPS for st in sts]

DOS.mkdir(parents=True, exist_ok=True)
LAYERS = {'1': ['barres', '1d']}    # story 1: the bars and the row of plates, each with its own camera

for sc, name, _ in STORIES:
    objs = [BRUTS / f'story-{k}.png' for k in LAYERS.get(sc, [sc])]
    if not all(o.exists() for o in objs):
        continue
    layers = ''.join(f'<img src="{o.as_uri()}">' for o in objs)
    page = f'''<html><body style="margin:0;width:1080px;height:1920px;background:#FFFFFF;position:relative;overflow:hidden">
<style>img {{ position:absolute; inset:0; width:1080px; height:1920px; }}</style>{layers}</body></html>'''
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as f:
        f.write(page)
    png = DOS / f'{name}.png'
    subprocess.run(['node', str(OUT / 'export.mjs'), f.name, str(png), '1', '1080'], check=True, capture_output=True)
    subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '95', str(png), '--out', str(DOS / f'{name}.jpg')], check=True, capture_output=True)
    png.unlink()
    Path(f.name).unlink()

def card(name, label):
    return (f'<figure><div class="card"><img src="{name}.jpg"><div class="safe top"></div><div class="safe bottom"></div></div>'
            f'<figcaption>{label}</figcaption></figure>')


sections = ''.join(f'<section><div class="t"><b>{title}</b><span>{sub}</span></div><div class="row">{"".join(card(n, l) for _, n, l in sts)}</div></section>'
                   for title, sub, sts in GROUPS)
page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>
@font-face {{ font-family: Inter; src: url("../outils/polices/inter-latin-500-normal.woff2"); font-weight: 500; }}
@font-face {{ font-family: Inter; src: url("../outils/polices/inter-latin-600-normal.woff2"); font-weight: 600; }}
body {{ margin: 0; padding: 72px; background: #EDEDEF; font-family: Inter, sans-serif; }}
h1 {{ font-size: 30px; font-weight: 600; margin: 0 0 6px; }}
.lead {{ font-size: 17px; color: #6B6B6B; margin: 0 0 48px; }}
section {{ margin-bottom: 64px; }}
.t {{ display: flex; gap: 14px; align-items: baseline; margin-bottom: 20px; font-size: 22px; }}
.t span {{ color: #6B6B6B; font-size: 17px; }}
.row {{ display: flex; gap: 32px; }}
figure {{ margin: 0; }}
figcaption {{ margin-top: 16px; font-size: 17px; font-weight: 600; }}
.card {{ position: relative; width: 420px; height: 747px; border-radius: 22px; overflow: hidden; background: #fff;
        box-shadow: 0 2px 6px rgba(0,0,0,.06), 0 18px 40px rgba(0,0,0,.08); }}
.card img {{ width: 100%; height: 100%; display: block; }}
.safe {{ position: absolute; left: 0; right: 0; border-color: rgba(0,0,0,.18); border-style: dashed; border-width: 0; }}
.safe.top {{ top: 0; height: 13%; border-bottom-width: 1px; }}
.safe.bottom {{ bottom: 0; height: 13%; border-top-width: 1px; }}
</style></head><body>
<h1>Les stories : les prototypes</h1>
<p class="lead">1080 × 1920, fond blanc, sans texte, sans sol ni ombre.<br>
Les pointillés montrent les zones que couvre Instagram (profil en haut, réponse en bas) : ils ne sont pas dans les images.</p>
{sections}
</body></html>'''
(DOS / 'planche.html').write_text(page)
subprocess.run(['node', str(OUT / 'export.mjs'), str(DOS / 'planche.html'), str(DOS / 'planche.jpg'), '1', str(72 * 2 + 4 * 420 + 3 * 32)], check=True)
print('écrit', DOS)
