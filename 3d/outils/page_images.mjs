// Opens a web page in headless Chrome (the page needs JavaScript) and either
//   - lists its links whose text or address contains a word:   node page_images.mjs liens <url> <mot>
//   - downloads its large images into a folder:                 node page_images.mjs images <url> <dossier> [largeur min, 500]
// Used for the research: manufacturers' product pages (reference photos, not published, see .gitignore).
import { createRequire } from 'node:module';
import { homedir } from 'node:os';
import fs from 'node:fs';
import path from 'node:path';
const require = createRequire(process.env.PLAYWRIGHT_PKG || `${homedir()}/Desktop/Portfolio/tools/package.json`);
const { chromium } = require('playwright');

const [mode, url, arg, minW] = process.argv.slice(2);
const b = await chromium.launch({ channel: 'chrome', headless: true });
const ctx = await b.newContext({ viewport: { width: 1600, height: 1100 }, locale: 'en-US',
  userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36' });
const p = await ctx.newPage();
// remember every image the page loads (galleries often swap their pictures in with JavaScript)
const seen = new Map();
p.on('response', async r => {
  const ct = r.headers()['content-type'] || '';
  if (ct.startsWith('image/') && !ct.includes('svg')) seen.set(r.url(), ct);
});
await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
await p.waitForTimeout(5000);
for (let i = 0; i < 8; i++) { await p.mouse.wheel(0, 900); await p.waitForTimeout(400); }   // lazy images
await p.waitForTimeout(1500);

if (mode === 'liens') {
  const mot = (arg || '').toLowerCase();
  const links = await p.$$eval('a', as => as.map(a => [a.innerText.trim().replace(/\s+/g, ' '), a.href]));
  const uniq = new Map();
  for (const [t, h] of links) if (h && (t.toLowerCase().includes(mot) || h.toLowerCase().includes(mot))) uniq.set(h, t);
  for (const [h, t] of uniq) console.log(`${t.slice(0, 70).padEnd(70)}  ${h}`);
} else {
  const dir = path.resolve(arg); fs.mkdirSync(dir, { recursive: true });
  const min = Number(minW || 500);
  const imgs = await p.$$eval('img', (els) => els.map(e => [e.currentSrc || e.src, e.naturalWidth, e.naturalHeight, e.alt || '']));
  const keep = new Map();
  for (const [s, w, h, alt] of imgs) if (s && !s.startsWith('data:') && w >= min) keep.set(s, alt);
  for (const s of seen.keys()) if (!keep.has(s)) keep.set(s, '');
  const meta = [];
  let n = 0;
  for (const [s, alt] of keep) {
    try {
      const r = await ctx.request.get(s, { headers: { referer: url } });
      if (!r.ok()) continue;
      const buf = await r.body();
      if (buf.length < 25000) continue;                       // icons, logos, thumbnails
      const ext = (r.headers()['content-type'] || 'image/jpeg').split('/')[1].split(';')[0].replace('jpeg', 'jpg');
      const name = `img-${String(++n).padStart(2, '0')}.${ext}`;
      fs.writeFileSync(path.join(dir, name), buf);
      meta.push({ fichier: name, image: s, alt, trouvee_sur: url });
    } catch { /* skip */ }
  }
  fs.writeFileSync(path.join(dir, '_images.json'), JSON.stringify(meta, null, 1));
  console.log(`${n} images -> ${dir}`);
}
await b.close();
