// Puts a transparent render on a background (a colour or a CSS gradient) and saves it as JPEG or PNG.
// usage: node compose.mjs <in.png> <out.jpg> "<css background>" [scale 0..1]
import { createRequire } from 'node:module';
import { homedir } from 'node:os';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
const require = createRequire(process.env.PLAYWRIGHT_PKG || `${homedir()}/Desktop/Portfolio/tools/package.json`);
const { chromium } = require('playwright');
const [inp, out, bg, sc] = process.argv.slice(2);
const dims = execFileSync('sips', ['-g', 'pixelWidth', '-g', 'pixelHeight', inp]).toString();
const W = Number(dims.match(/pixelWidth: (\d+)/)[1]), H = Number(dims.match(/pixelHeight: (\d+)/)[1]);
const s = Number(sc || 1);
const w = Math.round(W * s), h = Math.round(H * s);
const b = await chromium.launch({ channel: 'chrome', headless: true });
const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
await p.setContent(`<html><body style="margin:0;width:${w}px;height:${h}px;background:${bg}">
<img src="data:image/png;base64,${fs.readFileSync(inp).toString('base64')}" style="display:block;width:${w}px;height:${h}px"></body></html>`);
await p.waitForLoadState('networkidle');
await p.screenshot({ path: out, type: out.endsWith('.png') ? 'png' : 'jpeg', quality: out.endsWith('.png') ? undefined : 92 });
await b.close();
console.log('saved', out);
