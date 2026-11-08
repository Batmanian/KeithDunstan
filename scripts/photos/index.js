#!/usr/bin/env node
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const ROOT = path.resolve(__dirname, '../..');
const hash = value => crypto.createHash('sha256').update(value).digest('hex');
const read = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const fail = message => { throw new Error(message); };
const required = (value, label) => {
  if (typeof value !== 'string' || !value.trim() || /\b(REPLACE|TODO|TBD)\b/.test(value)) fail(`${label} is required (no placeholders)`);
};
const url = (value, label) => {
  required(value, label);
  let parsed;
  try { parsed = new URL(value); } catch { fail(`${label} must be an HTTPS URL`); }
  if (parsed.protocol !== 'https:' || parsed.username || parsed.password) fail(`${label} must be an HTTPS URL without credentials`);
};
function local(root, relative, prefix, exists = true) {
  required(relative, 'Local path');
  if (path.isAbsolute(relative) || relative.split(/[\\/]/).includes('..') || relative.includes('\\')) fail(`Unsafe path: ${relative}`);
  if (!relative.startsWith(prefix)) fail(`Path must start with ${prefix}: ${relative}`);
  const target = path.resolve(root, relative);
  let ancestor = target;
  while (!fs.existsSync(ancestor)) ancestor = path.dirname(ancestor);
  const real = fs.realpathSync(ancestor);
  const allowed = path.resolve(fs.realpathSync(root), prefix);
  if (real !== allowed && !real.startsWith(allowed + path.sep)) fail(`Path escapes ${prefix}: ${relative}`);
  if (exists && !fs.statSync(target).isFile()) fail(`Not a file: ${relative}`);
  return target;
}
function digest(record) {
  const { status, approvals, ...reviewed } = record;
  return hash(JSON.stringify(reviewed));
}
function validate(record, root = ROOT, publish = false, checkMaster = true) {
  if (record.schemaVersion !== 1) fail('schemaVersion must be 1');
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(record.id || '')) fail('id must be a lowercase hyphenated slug');
  const states = ['brief', 'shortlisted', 'verified', 'approved', 'published', 'held', 'rejected', 'no-suitable-image'];
  if (!states.includes(record.status)) fail('Unknown status');
  const b = record.brief || {};
  const content = local(root, b.contentPath, 'vault/');
  if (!/^vault\/(books|articles)\/.+\.md$/.test(b.contentPath)) fail('contentPath must be a vault article or chapter');
  for (const field of ['title', 'sceneDate', 'place', 'subject', 'insertAfter', 'searchRationale']) required(b[field], `brief.${field}`);
  const prose = fs.readFileSync(content, 'utf8');
  if (prose.split(b.insertAfter).length !== 2) fail('insertAfter must match exactly once in the vault content');
  if (!Array.isArray(record.searchLog)) fail('searchLog must be an array');
  const approved = ['approved', 'published'].includes(record.status);
  if (publish && !approved) fail('Publication requires approved or published status');
  if (!approved) return { id: record.id, status: record.status, ready: false };
  const c = record.candidate || {};
  for (const field of ['title', 'creator', 'holder', 'identifier', 'photoDate', 'place', 'rightsStatement', 'rightsRationale', 'accessedDate']) required(c[field], `candidate.${field}`);
  for (const field of ['sourceUrl', 'downloadUrl', 'licenceUrl']) url(c[field], `candidate.${field}`);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(c.accessedDate) || Number.isNaN(Date.parse(c.accessedDate))) fail('accessedDate must be an ISO date');
  const licences = {
    'CC-BY-4.0': 'https://creativecommons.org/licenses/by/4.0/',
    'CC-BY-SA-4.0': 'https://creativecommons.org/licenses/by-sa/4.0/',
    'CC-BY-3.0': 'https://creativecommons.org/licenses/by/3.0/',
    'CC-BY-SA-3.0': 'https://creativecommons.org/licenses/by-sa/3.0/',
    'CC-BY-2.0': 'https://creativecommons.org/licenses/by/2.0/',
    'CC-BY-SA-2.0': 'https://creativecommons.org/licenses/by-sa/2.0/',
    'CC0-1.0': 'https://creativecommons.org/publicdomain/zero/1.0/'
  };
  if (licences[c.licence]) {
    if (c.licenceUrl !== licences[c.licence]) fail('Licence URL does not match exact supported licence');
  } else if (c.licence === 'PUBLIC-DOMAIN') {
    required(c.publicDomainBasis, 'publicDomainBasis');
    required(c.publicDomainJurisdiction, 'publicDomainJurisdiction');
  } else fail('Unsupported or unresolved licence; manual workflow required (NC/ND/ported licences are not automated)');
  if (typeof c.notices !== 'string') fail('candidate.notices must be a string, empty only when none supplied');
  const evidence = local(root, c.evidencePath, 'research/photos/evidence/');
  if (hash(fs.readFileSync(evidence)) !== c.evidenceSha256) fail('Rights evidence checksum mismatch');
  const fit = record.fit || {};
  if (!['direct', 'contextual', 'later-comparison'].includes(fit.classification)) fail('Historical fit must be resolved');
  for (const field of ['date', 'place', 'identity']) {
    required(fit[field]?.reason, `fit.${field}.reason`);
    url(fit[field]?.sourceUrl, `fit.${field}.sourceUrl`);
  }
  required(fit.limitations, 'fit.limitations (write None only if justified)');
  const a = record.asset || {};
  if (!/^[a-f0-9]{64}$/.test(a.masterSha256 || '')) fail('Master SHA-256 required');
  if (checkMaster) {
    const master = local(root, a.masterPath, 'research/photos/masters/');
    if (hash(fs.readFileSync(master)) !== a.masterSha256) fail('Master checksum mismatch');
  }
  if (a.processing !== 'resize-only') fail('Only resize-only processing is supported');
  if (!Number.isInteger(a.maxWidth) || a.maxWidth < 100 || a.maxWidth > 2400) fail('maxWidth must be 100–2400');
  const p = record.presentation || {};
  for (const field of ['caption', 'alt', 'modifications']) required(p[field], `presentation.${field}`);
  for (const kind of ['historical', 'rights']) {
    const approval = record.approvals?.[kind] || {};
    required(approval.reviewer, `${kind} reviewer`);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(approval.date || '')) fail(`${kind} approval date required`);
    if (approval.digest !== digest(record)) fail(`${kind} approval missing or stale; review current record then record its digest`);
  }
  return { id: record.id, status: record.status, ready: true };
}
const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'}[c]));
function figure(r, width, height) {
  const c = r.candidate, p = r.presentation;
  return `<figure class="figure my-4" id="photo-${r.id}">\n  <img src="/img/${r.id}.jpg" class="figure-img img-fluid" width="${width}" height="${height}" loading="lazy" decoding="async" alt="${escape(p.alt)}">\n  <figcaption class="figure-caption">Archive illustration: ${escape(p.caption)} <a href="${escape(c.sourceUrl)}">${escape(c.title)}</a> — ${escape(c.creator)}; ${escape(c.holder)}, ${escape(c.identifier)}. <a href="${escape(c.licenceUrl)}">${escape(c.licence)}</a>. ${escape(p.modifications)} Resized and encoded as JPEG for display. ${escape(c.notices)}</figcaption>\n</figure>`;
}
function destinations(r) {
  const parts = r.brief.contentPath.split('/');
  return { vault: `${parts.slice(0, 3).join('/')}/${r.id}.jpg`, link: `src/img/${r.id}.jpg` };
}
async function prepare(r, root = ROOT) {
  validate(r, root, true);
  const sharp = require('sharp');
  const input = local(root, r.asset.masterPath, 'research/photos/masters/');
  const meta = await sharp(input).metadata();
  if (!['jpeg', 'png', 'tiff', 'webp'].includes(meta.format) || (meta.pages || 1) !== 1) fail('Only single-frame JPEG, PNG, TIFF and WebP masters supported');
  const { data, info } = await sharp(input).rotate().resize({ width: r.asset.maxWidth, withoutEnlargement: true }).flatten({ background: '#ffffff' }).jpeg({ quality: 85 }).toBuffer({ resolveWithObject: true });
  const folder = path.join(root, 'research/photos/prepared', r.id);
  fs.mkdirSync(folder, { recursive: true });
  local(root, `research/photos/prepared/${r.id}`, 'research/photos/prepared/', false);
  const html = figure(r, info.width, info.height);
  const manifest = { id: r.id, recordDigest: digest(r), sha256: hash(data), width: info.width, height: info.height, bytes: data.length, ...destinations(r) };
  // Exclusive writes prevent replacing an existing preparation or following a file symlink.
  for (const name of ['image.jpg', 'figure.html', 'manifest.json']) if (fs.existsSync(path.join(folder, name))) fail(`Preparation already exists: ${folder}; archive/remove it explicitly before preparing again`);
  fs.writeFileSync(path.join(folder, 'image.jpg'), data, { flag: 'wx' });
  fs.writeFileSync(path.join(folder, 'figure.html'), html + '\n', { flag: 'wx' });
  fs.writeFileSync(path.join(folder, 'manifest.json'), JSON.stringify(manifest, null, 2) + '\n', { flag: 'wx' });
  return manifest;
}
function prepared(r, root, published = false) {
  validate(r, root, true, !published);
  const prefix = `research/photos/prepared/${r.id}/`;
  const m = read(local(root, prefix + 'manifest.json', 'research/photos/prepared/'));
  const bytes = fs.readFileSync(published
    ? local(root, destinations(r).vault, 'vault/')
    : local(root, prefix + 'image.jpg', 'research/photos/prepared/'));
  if (m.recordDigest !== digest(r) || m.sha256 !== hash(bytes)) fail('Prepared assets are stale or modified');
  const expected = destinations(r);
  if (m.vault !== expected.vault || m.link !== expected.link) fail('Prepared destination mismatch');
  const html = figure(r, m.width, m.height);
  if (fs.readFileSync(local(root, prefix + 'figure.html', 'research/photos/prepared/'), 'utf8').trim() !== html) fail('Prepared figure differs from approved record');
  return { m, bytes, html };
}
function promote(r, root = ROOT) {
  const { m, bytes } = prepared(r, root);
  const target = local(root, m.vault, 'vault/', false);
  const link = local(root, m.link, 'src/img/', false);
  if (existsEntry(target) || existsEntry(link)) fail('Destination already exists; refusing to overwrite');
  fs.writeFileSync(target, bytes, { flag: 'wx' });
  try { fs.symlinkSync(path.relative(path.dirname(link), target), link); }
  catch (error) { fs.unlinkSync(target); throw error; }
  return m;
}
function existsEntry(file) { try { fs.lstatSync(file); return true; } catch (e) { if (e.code === 'ENOENT') return false; throw e; } }
function checkPublished(r, root = ROOT) {
  const { m, html } = prepared(r, root, true);
  const target = local(root, m.vault, 'vault/');
  const link = path.join(root, m.link);
  if (!fs.lstatSync(link).isSymbolicLink() || fs.realpathSync(link) !== fs.realpathSync(target)) fail('Publication symlink missing or points at wrong asset');
  if (hash(fs.readFileSync(target)) !== m.sha256) fail('Published image checksum mismatch');
  if (!fs.readFileSync(path.join(root, r.brief.contentPath), 'utf8').includes(html)) fail('Published content does not contain the approved credited figure');
}
async function main() {
  const [command, file, ...extra] = process.argv.slice(2);
  if (extra.length || !['validate', 'digest', 'prepare', 'promote'].includes(command)) fail('Usage: node scripts/photos/index.js validate [record.json] | digest|prepare|promote record.json');
  const files = file ? [path.resolve(file)] : fs.readdirSync(path.join(ROOT, 'research/photos/records')).filter(n => n.endsWith('.json')).map(n => path.join(ROOT, 'research/photos/records', n));
  if (command !== 'validate' && !file) fail('A record path is required');
  const ids = new Set();
  for (const filename of files) {
    const r = read(filename);
    if (ids.has(r.id)) fail(`Duplicate id: ${r.id}`);
    ids.add(r.id);
    if (command === 'digest') console.log(digest(r));
    else if (command === 'validate') {
      const result = validate(r, ROOT, false, r.status !== 'published');
      if (r.status === 'published') checkPublished(r);
      console.log(`${r.id}: ${result.status}${result.ready ? ' (approved)' : ' (not publishable)'}`);
    } else if (command === 'prepare') console.log(JSON.stringify(await prepare(r), null, 2));
    else console.log(JSON.stringify(promote(r), null, 2));
  }
}
if (require.main === module) main().catch(error => { console.error(`Photos: ${error.message}`); process.exitCode = 1; });
module.exports = { validate, digest, figure, prepare, promote, checkPublished, hash };
