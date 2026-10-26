import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
let markdown;
try { markdown = await import('@astrojs/markdown-remark'); }
catch (e) { if(e.code !== 'ERR_MODULE_NOT_FOUND') throw e; markdown = await import('../.local/node_modules/@astrojs/markdown-remark/dist/index.js'); }
const {createMarkdownProcessor, parseFrontmatter} = markdown;

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const modules = JSON.parse(fs.readFileSync(path.join(ROOT, 'modules.json'), 'utf8'));
const SITE = process.env.INTERVIEW_SITE;
const allowStale = process.argv.includes('--allow-stale');
const read = p => fs.readFileSync(p, 'utf8');
const hash = p => crypto.createHash('sha256').update(read(p).replace(/<!-- AUTO:START -->[\s\S]*?<!-- AUTO:END -->/, '<!-- AUTO:START -->\n<!-- AUTO:END -->')).digest('hex');
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const write = (p, s) => { fs.mkdirSync(path.dirname(p), { recursive: true }); if (!fs.existsSync(p) || read(p) !== s) fs.writeFileSync(p, s); };
const walk = dir => fs.readdirSync(dir, { withFileTypes: true }).flatMap(e => e.isDirectory() ? walk(path.join(dir, e.name)) : [path.join(dir, e.name)]);
const sourceFiles = () => modules.flatMap(m => walk(path.join(ROOT, m.id))).filter(p => p.endsWith('.md')).sort();

// Only this explicit block is generated. Preserve all other human-written material.
for (const m of modules) {
  const files = walk(path.join(ROOT, m.id)).filter(p => p.endsWith('.md') && p !== path.join(ROOT, m.id, 'README.md')).sort();
  for (const lang of ['zh', 'en']) {
    const prefix = lang === 'zh' ? ROOT : path.join(ROOT, '.translations/en');
    const index = path.join(prefix, m.id, 'README.md');
    if (!fs.existsSync(index)) continue;
    const links = files.map(p => {
      const rel = path.relative(path.join(ROOT, m.id), p).split(path.sep).join('/');
      const candidate=path.join(prefix,m.id,rel);
      const data = parseFrontmatter(read(fs.existsSync(candidate)?candidate:p)).frontmatter;
      return `- [${data.title || path.basename(rel, ".md")}](${rel})`;
    }).join('\n');
    write(index, read(index).replace(/<!-- AUTO:START -->[\s\S]*?<!-- AUTO:END -->/, `<!-- AUTO:START -->\n${links}\n<!-- AUTO:END -->`));
  }
}

const processor = await createMarkdownProcessor({ syntaxHighlight: false });
const notes = [];
const errors = [];
for (const p of sourceFiles()) {
  const rel = path.relative(ROOT, p).split(path.sep).join('/');
  const {frontmatter: fm} = parseFrontmatter(read(p));
  if (fm.public === false) continue;
  fm.title ||= path.basename(rel,'.md');
  fm.title_en ||= fm.title;
  if (fm.diagram) {
    const labels = fm.diagram;
    const width = labels.length * 280;
    const boxW = 240;
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="192" viewBox="0 0 ${width} 192" role="img" aria-labelledby="title"><title id="title">${esc(fm.title)} / ${esc(fm.title_en)}</title><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8" fill="none" stroke="#b5231a" stroke-width="2"/></marker></defs><rect width="${width}" height="192" fill="#f2efe8"/>${labels.map((label,i) => {
      const x=24+i*280;
      const parts=label.split(' / ');
      return `<rect x="${x}" y="48" width="${boxW}" height="96" rx="8" fill="white" stroke="#202020" stroke-width="2"/><text x="${x+boxW/2}" y="88" text-anchor="middle" fill="#171717" font-size="19" font-family="system-ui,sans-serif">${esc(parts[0])}</text><text x="${x+boxW/2}" y="117" text-anchor="middle" fill="#57534e" font-size="16" font-family="system-ui,sans-serif">${esc(parts[1] || '')}</text>${i<labels.length-1 ? `<path d="M${x+boxW+5} 96 H${x+275}" stroke="#b5231a" stroke-width="2" marker-end="url(#arrow)"/>` : ''}`;
    }).join('')}</svg>\n`;
    write(path.join(ROOT, 'assets', path.basename(rel, '.md')+'.svg'), svg);
  }
  for (const lang of ['zh','en']) {
    const src = lang === 'zh' ? p : path.join(ROOT,'.translations/en',rel);
    if (!fs.existsSync(src) && !allowStale) {errors.push(`Missing English mirror: ${rel}`); continue;}
    let {frontmatter: data, content} = parseFrontmatter(read(fs.existsSync(src)?src:p));
    data.title ||= fm.title;
    data.description ||= data.title;
    if (lang === 'en' && data.source_hash !== hash(p)) {
      if (!allowStale) errors.push(`Stale English mirror: ${rel}`);
      content='> Translation update pending: the Chinese source has changed. The English text below reflects the previous revision.\n\n'+content;
    }
    const id=rel.replace(/\.md$/, '');
    content=content.replace(/\]\(([^)]+)\)/g,(whole,target)=>{
      if (/^(?:https?:|mailto:|#)/.test(target)) return whole;
      let decoded;
      try { decoded=decodeURIComponent(target.split('#')[0]); } catch {errors.push(`Invalid URL in ${rel}: ${target}`);return whole;}
      let resolved=path.posix.normalize(path.posix.join(path.posix.dirname(lang==='zh'||!fs.existsSync(src)?rel:`.translations/en/${rel}`),decoded));
      if (resolved.startsWith('../') || path.isAbsolute(resolved)) {errors.push(`Escaping link ${rel}: ${target}`);return whole;}
      if (resolved.startsWith('.translations/en/')) resolved=resolved.slice('.translations/en/'.length);
      if (!fs.existsSync(path.join(ROOT,resolved))) errors.push(`Broken link ${rel}: ${target}`);
      if (resolved.endsWith('.md')) return `](@@NOTE:${resolved.replace(/\.md$/,'')}@@)`;
      return `](@@ASSET:${resolved}@@)`;
    });
    let html=(await processor.render(content)).code;
    notes.push({id, path:rel, module:rel.split('/')[0], lang, title:data.title, description:data.description || data.title, html, source:data.source || null});
  }
}
if (errors.length) { console.error(errors.join('\n')); process.exit(1); }
const targetLink = (html, lang, offline) => html
 .replace(/@@NOTE:([^@]+)@@/g, (_,id)=>offline ? `#${lang}-${id}` : `${lang==='zh'?'/cn':''}/interview/${id}/`)
 .replace(/@@ASSET:([^@]+)@@/g,(_,asset)=>{
   if (offline && /\.(svg|png|jpe?g|webp|gif)$/i.test(asset)) { const ext=path.extname(asset).slice(1).toLowerCase(); const mime={svg:'image/svg+xml',png:'image/png',jpg:'image/jpeg',jpeg:'image/jpeg',webp:'image/webp',gif:'image/gif'}[ext];return `data:${mime};base64,${fs.readFileSync(path.join(ROOT,asset)).toString('base64')}`; }
   if (offline) return asset==='assets/system-design-map.html'?'system-design-map.html':`../${asset}`;
   return `/interview-notes/${asset}`;
 });
const css=`:root{color-scheme:light;--ink:#171717;--red:#b5231a;--paper:#f2efe8}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.8 system-ui,-apple-system,sans-serif}header{border-bottom:3px solid var(--ink);padding:35px max(24px,calc((100vw - 1240px)/2))}h1{line-height:1.2;font-size:clamp(30px,4vw,52px)}.eyebrow{color:var(--red);letter-spacing:.12em;font-size:12px}main{max-width:1240px;margin:auto;padding:30px 24px;display:grid;grid-template-columns:270px minmax(0,1fr);gap:40px}nav a{display:block;font-size:14px;padding:4px 0}nav{align-self:start;position:sticky;top:15px;max-height:94vh;overflow:auto}a{color:var(--red);overflow-wrap:anywhere}article{background:white;border:2px solid var(--ink);padding:28px;margin-bottom:35px;scroll-margin-top:20px}h2{line-height:1.4}h3{border-bottom:1px solid #ddd}img{max-width:100%;height:auto}table{width:100%;border-collapse:collapse;font-size:14px;display:block;overflow:auto}td,th{border:1px solid #ddd;padding:8px 12px;text-align:left}blockquote{border-left:3px solid var(--red);margin:15px 0;padding:1px 18px;color:#666;font-size:14px}pre{background:#f3f4f6;padding:14px;overflow:auto;font-size:13px}code{font-size:.88em}details{margin:12px 0}summary{cursor:pointer;font-weight:700}button{padding:8px 15px;background:white;border:2px solid #171717;cursor:pointer}section{min-width:0}@media(max-width:780px){main{display:block}nav{position:static;max-height:none;margin-bottom:28px}article{padding:18px}}@media print{nav,button{display:none}main{display:block;padding:0}article{break-before:page;border:0;padding:0}header{border:0}body{background:white}}`;
for (const lang of ['zh','en']) {
 const selected=notes.filter(n=>n.lang===lang);
 const title=lang==='zh'?'面试知识图谱':'Interview Atlas';
 const toc=modules.map(m=>`<details open><summary>${esc(lang==='zh'?m.title:m.title_en)}</summary>${selected.filter(n=>n.module===m.id).map(n=>`<a href="#${lang}-${n.id}">${esc(n.title)}</a>`).join('')}</details>`).join('');
 const articles=selected.map(n=>`<article id="${lang}-${n.id}">${targetLink(n.html,lang,true)}</article>`).join('');
 write(path.join(ROOT,`downloads/interview-atlas-${lang}.html`),`<!doctype html><html lang="${lang==='zh'?'zh-CN':'en'}"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${title}</title><style>${css}</style><header><div class="eyebrow">YIKUN DING / INTERVIEW ATLAS</div><h1>${title}</h1><p>${lang==='zh'?'六个模块 · 中文笔记与英文术语 · 可离线阅读':'Six modules · bilingual notes · available offline'}</p><a href="interview-atlas-${lang==='zh'?'en':'zh'}.html">${lang==='zh'?'English':'中文'}</a> · <a href="system-design-map.html">${lang==='zh'?'交互总览':'Interactive overview (Chinese)'}</a></header><main><nav aria-label="${lang==='zh'?'目录':'Contents'}">${toc}</nav><section>${articles}</section></main></html>`);
}
fs.copyFileSync(path.join(ROOT,'assets/system-design-map.html'),path.join(ROOT,'downloads/system-design-map.html'));
write(path.join(ROOT,'catalog.json'),JSON.stringify({modules,notes:notes.map(n=>({...n,html:targetLink(n.html,n.lang,false)}))},null,2)+'\n');
if (SITE) {
 const pub=path.join(SITE,'public/interview-notes');
 fs.mkdirSync(pub,{recursive:true});
 fs.cpSync(path.join(ROOT,'assets'),path.join(pub,'assets'),{recursive:true});
 fs.cpSync(path.join(ROOT,'downloads'),path.join(pub,'downloads'),{recursive:true});
 fs.copyFileSync(path.join(ROOT,'catalog.json'),path.join(SITE,'src/data/interview-catalog.json'));
 const snapshot=path.join(pub,'source');
 // Recreate only the managed source snapshot so deletions and renames propagate.
 fs.rmSync(snapshot,{recursive:true,force:true});
 for(const n of notes.filter(n=>n.lang==='zh')) {const dest=path.join(snapshot,n.path);fs.mkdirSync(path.dirname(dest),{recursive:true});fs.copyFileSync(path.join(ROOT,n.path),dest);}
}
console.log(`Validated ${notes.length/2} Chinese notes, ${notes.length/2} English mirrors, local links, and source hashes.`);
