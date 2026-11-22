# The Instagram stories (22/11/2026): puts the renders of outils/blender/rendus-stories.sh on white at
# 1080 x 1920 (the story format): the white background, the shadow pass made lighter, then the objects.
# Writes 3d/stories/*.jpg and 3d/stories/planche.jpg (the stories side by side, with labels: that board is for
# choosing, it is not posted).
# usage: python3 3d/outils/stories.py
import subprocess, tempfile
from pathlib import Path

OUT = Path(__file__).resolve().parent
BRUTS = OUT / 'blender/_bruts/stories'
DOS = OUT.parent / 'stories'
SHADOW = 0.5                                     # opacity of the shadows: light, like the models' catalogue renders
STORIES = [   # scene, file, label on the board
    ('S1', '1-barre-et-disques', '1 · La barre et ses disques'),
    ('S2a', '2a-halteres-grille', '2 a · Les haltères, en grille'),
    ('S2b', '2b-halteres-cascade', '2 b · Les haltères, en cascade'),
    ('S3a', '3a-vinyle-et-pinces-rangees', '3 a · Disques vinyle et pinces, en rangées'),
    ('S3b', '3b-vinyle-et-pinces-colonne', '3 b · Disques vinyle et pinces, en colonne'),
]

DOS.mkdir(parents=True, exist_ok=True)
for sc, name, _ in STORIES:
    obj, shd = BRUTS / f'story-{sc}.png', BRUTS / f'story-{sc}-ombre.png'
    if not obj.exists():
        continue
    layers = (f'<img src="{shd.as_uri()}" style="opacity:{SHADOW}">' if shd.exists() else '') + f'<img src="{obj.as_uri()}">'
    page = f'''<html><body style="margin:0;width:1080px;height:1920px;background:#FFFFFF;position:relative;overflow:hidden">
<style>img {{ position:absolute; inset:0; width:1080px; height:1920px; }}</style>{layers}</body></html>'''
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as f:
        f.write(page)
    png = DOS / f'{name}.png'
    subprocess.run(['node', str(OUT / 'export.mjs'), f.name, str(png), '1', '1080'], check=True, capture_output=True)
    subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '95', str(png), '--out', str(DOS / f'{name}.jpg')], check=True, capture_output=True)
    png.unlink()
    Path(f.name).unlink()

cards = ''.join(f'<figure><div class="card"><img src="{name}.jpg"><div class="safe top"></div><div class="safe bottom"></div></div>'
                f'<figcaption>{label}</figcaption></figure>' for _, name, label in STORIES)
page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>
@font-face {{ font-family: Inter; src: url("../outils/polices/inter-latin-500-normal.woff2"); font-weight: 500; }}
@font-face {{ font-family: Inter; src: url("../outils/polices/inter-latin-600-normal.woff2"); font-weight: 600; }}
body {{ margin: 0; padding: 72px; background: #EDEDEF; font-family: Inter, sans-serif; }}
h1 {{ font-size: 30px; font-weight: 600; margin: 0 0 6px; }}
.lead {{ font-size: 17px; color: #6B6B6B; margin: 0 0 48px; }}
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
<h1>Les stories : les modèles isolés, sans sol</h1>
<p class="lead">1080 × 1920, fond blanc, sans texte, une ombre légère sous les objets. Une story par groupe : pour 2 et 3, deux mises en page au choix.<br>
Les pointillés montrent les zones que couvre Instagram (profil en haut, réponse en bas) : ils ne sont pas dans les images.</p>
<div class="row">{cards}</div>
</body></html>'''
(DOS / 'planche.html').write_text(page)
subprocess.run(['node', str(OUT / 'export.mjs'), str(DOS / 'planche.html'), str(DOS / 'planche.jpg'), '1', str(72 * 2 + 5 * 420 + 4 * 32)], check=True)
print('écrit', DOS)
