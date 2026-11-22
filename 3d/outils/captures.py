# The Blender screenshots in the Instagram story format (22/11/2026): each capture of outils/blender/rendus-captures.sh
# (1280 x 1662, the narrowest Blender window) across the whole width, centred; above and below, bands of the
# colour of Blender's own top and bottom bars (sampled from the capture), where Instagram shows the profile and
# the reply bar. Writes 3d/stories/blender/*.jpg.
# usage: python3 3d/outils/captures.py
import base64, subprocess, tempfile
from pathlib import Path

OUT = Path(__file__).resolve().parent
BRUTS = OUT / 'blender/_bruts/captures'
DOS = OUT.parent / 'stories/blender'
SHOTS = [('disque', '1-disque'), ('haltere', '2-haltere-rond'), ('barre', '3-barre'), ('pince', '4-pince'), ('haltere-disques', '5-haltere-disques')]

DOS.mkdir(parents=True, exist_ok=True)
for shot, name in SHOTS:
    src = BRUTS / f'blender-{shot}.png'
    if not src.exists():
        continue
    data = 'data:image/png;base64,' + base64.b64encode(src.read_bytes()).decode()
    page = f'''<html><body style="margin:0;width:1080px;height:1920px;overflow:hidden;position:relative">
<div id="top" style="position:absolute;left:0;right:0;top:0;height:960px"></div>
<div id="bot" style="position:absolute;left:0;right:0;bottom:0;height:960px"></div>
<img id="i" src="{data}" style="position:absolute;left:0;top:50%;width:1080px;transform:translateY(-50%)">
<script>
const im = document.getElementById('i');
im.onload = () => {{
  const c = document.createElement('canvas'); c.width = im.naturalWidth; c.height = im.naturalHeight;
  const g = c.getContext('2d'); g.drawImage(im, 0, 0);
  const px = (x, y) => {{ const d = g.getImageData(x, y, 1, 1).data; return `rgb(${{d[0]}},${{d[1]}},${{d[2]}})`; }};
  document.getElementById('top').style.background = px(600, 4);                  // Blender's top bar
  document.getElementById('bot').style.background = px(600, im.naturalHeight - 4); // its status bar
}};
</script></body></html>'''
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as f:
        f.write(page)
    png = DOS / f'{name}.png'
    subprocess.run(['node', str(OUT / 'export.mjs'), f.name, str(png), '1', '1080'], check=True, capture_output=True)
    subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '95', str(png), '--out', str(DOS / f'{name}.jpg')], check=True, capture_output=True)
    png.unlink(); Path(f.name).unlink()
    print('écrit', DOS / f'{name}.jpg')
