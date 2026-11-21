# Contact sheet of every image in a folder (to look at a research folder in one picture).
# usage: python3 contact.py <folder> <out.png> [image height px] [page width px]
import sys, html, subprocess, tempfile
from pathlib import Path
src = Path(sys.argv[1]).resolve(); out = Path(sys.argv[2]).resolve()
h = int(sys.argv[3]) if len(sys.argv) > 3 else 300
w = int(sys.argv[4]) if len(sys.argv) > 4 else 2000
imgs = sorted(p for p in src.rglob('*') if p.suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp', '.gif'} and p.name != 'planche.png')
figs = ''.join(f'<figure><img src="{p.as_uri()}"><figcaption>{html.escape(str(p.relative_to(src)))}</figcaption></figure>' for p in imgs)
page = f'''<!doctype html><meta charset="utf-8"><style>
body{{margin:16px;background:#fff;font:12px -apple-system,Helvetica;display:flex;flex-wrap:wrap;gap:10px}}
figure{{margin:0;display:flex;flex-direction:column;gap:4px}} img{{height:{h}px;width:auto;display:block;background:#eee}}
figcaption{{width:0;min-width:100%;color:#333;word-break:break-all}}</style>{figs}'''
tmp = Path(tempfile.mkdtemp()) / 'contact.html'; tmp.write_text(page)
subprocess.run(['node', str(Path(__file__).with_name('export.mjs')), str(tmp), str(out), '1', str(w)], check=True)
