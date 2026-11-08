const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const sharp = require('sharp');
const { validate, digest, prepare, promote, checkPublished, hash } = require('./index');
async function fixture(t) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'kd-photos-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  for (const dir of ['vault/books/example', 'src/img', 'research/photos/masters', 'research/photos/evidence']) fs.mkdirSync(path.join(root, dir), { recursive: true });
  fs.writeFileSync(path.join(root, 'vault/books/example/1-chapter.md'), 'The village in 1930.\n');
  const image = await sharp({ create: { width: 200, height: 100, channels: 3, background: '#999999' } }).png().toBuffer();
  fs.writeFileSync(path.join(root, 'research/photos/masters/test.png'), image);
  fs.writeFileSync(path.join(root, 'research/photos/evidence/test.txt'), 'Test rights evidence');
  const r = { schemaVersion: 1, id: 'test-village', status: 'approved', brief: { contentPath: 'vault/books/example/1-chapter.md', title: 'Village', sceneDate: '1930', place: 'Village', subject: 'Street', insertAfter: 'The village in 1930.', searchRationale: 'Period street context' }, searchLog: [], candidate: { title: 'Street <view>', creator: 'Test photographer', holder: 'Test archive', identifier: 'TEST-1', photoDate: '1930', place: 'Village', rightsStatement: 'CC BY 4.0', rightsRationale: 'Fixture only', accessedDate: '2026-11-05', sourceUrl: 'https://example.org/item', downloadUrl: 'https://example.org/photo.png', licence: 'CC-BY-4.0', licenceUrl: 'https://creativecommons.org/licenses/by/4.0/', notices: '', evidencePath: 'research/photos/evidence/test.txt', evidenceSha256: hash('Test rights evidence') }, fit: { classification: 'contextual', limitations: 'Not the exact event', ...Object.fromEntries(['date','place','identity'].map(key => [key, { reason: 'Test evidence', sourceUrl: 'https://example.org/item' }])) }, asset: { masterPath: 'research/photos/masters/test.png', masterSha256: hash(image), processing: 'resize-only', maxWidth: 1200 }, presentation: { caption: 'Village in 1930; contextual view, not the event.', alt: 'A village street', modifications: 'No prior modifications reported.' }, approvals: {} };
  approve(r);
  return { root, r };
}
function approve(r) { for (const kind of ['rights','historical']) r.approvals[kind] = { reviewer: 'Test reviewer', date: '2026-11-05', digest: digest(r) }; }
test('prepares, promotes and verifies a credited publication without enlarging', async t => {
  const { root, r } = await fixture(t);
  const m = await prepare(r, root);
  assert.equal(m.width, 200); assert.equal(m.height, 100);
  const html = fs.readFileSync(path.join(root, 'research/photos/prepared/test-village/figure.html'), 'utf8').trim();
  assert.match(html, /Street &lt;view&gt;/);
  promote(r, root);
  assert.throws(() => promote(r, root));
  const content = path.join(root, r.brief.contentPath);
  fs.appendFileSync(content, '\n' + html + '\n');
  r.status = 'published';
  // Fresh builds do not require ignored working masters or staged images.
  fs.rmSync(path.join(root, r.asset.masterPath));
  fs.rmSync(path.join(root, 'research/photos/prepared/test-village/image.jpg'));
  checkPublished(r, root);
  fs.writeFileSync(content, 'The village in 1930.\n');
  assert.throws(() => checkPublished(r, root), /credited figure/);
});
test('rejects unapproved records and stale approvals', async t => {
  const { root, r } = await fixture(t);
  r.presentation.caption = 'Changed';
  assert.throws(() => validate(r, root), /stale/);
  r.status = 'brief';
  await assert.rejects(prepare(r, root), /requires approved/);
});
test('rejects rights gaps, unsafe URLs, missing fit, and altered evidence', async t => {
  const { root, r } = await fixture(t);
  for (const change of [
    x => x.candidate.licence = 'UNRESOLVED',
    x => x.candidate.licenceUrl = 'https://example.org/wrong',
    x => x.candidate.sourceUrl = 'javascript:alert(1)',
    x => x.candidate.evidenceSha256 = '0'.repeat(64),
    x => x.fit.classification = 'unresolved',
    x => x.asset.masterSha256 = '0'.repeat(64),
    x => x.brief.insertAfter = 'Missing paragraph',
    x => x.asset.masterPath = 'research/photos/masters/../../outside.png',
  ]) { const copy = structuredClone(r); change(copy); approve(copy); assert.throws(() => validate(copy, root)); }
});
test('refuses modified prepared assets and existing destination files', async t => {
  const { root, r } = await fixture(t);
  await prepare(r, root);
  await assert.rejects(prepare(r, root), /already exists/);
  const destination = path.join(root, 'vault/books/example/test-village.jpg');
  fs.writeFileSync(destination, 'Existing file');
  assert.throws(() => promote(r, root), /already exists/);
  assert.equal(fs.readFileSync(destination, 'utf8'), 'Existing file');
  fs.unlinkSync(destination);
  fs.appendFileSync(path.join(root, 'research/photos/prepared/test-village/image.jpg'), 'tamper');
  assert.throws(() => promote(r, root), /modified/);
});
test('rejects master symlinks outside the approved directory', async t => {
  const { root, r } = await fixture(t);
  const master = path.join(root, r.asset.masterPath);
  const outside = path.join(root, 'outside.png');
  fs.renameSync(master, outside); fs.symlinkSync(outside, master);
  assert.throws(() => validate(r, root), /escapes/);
});

test('topic priorities count each tag once per file and expose source concentration', () => {
  const { rank } = require('./priorities');
  const result = rank([
    { path: 'a.md', tags: ['Melbourne', 'Melbourne', 'book', 'Henry Bolte'], kind: 'books', source: 'memoir', publicationDecade: '1990s' },
    { path: 'b.md', tags: ['Melbourne', 'Henry Bolte'], kind: 'articles', source: 'bulletin', publicationDecade: '1960s' },
    { path: 'c.md', tags: [], kind: 'articles', source: 'bulletin', publicationDecade: 'unknown' }
  ]);
  assert.deepEqual(result.corpus, { documents: 3, tagged: 2, untagged: 1 });
  assert.equal(result.topics.length, 2);
  assert.equal(result.topics[0].topic, 'Henry Bolte'); // deterministic alphabetical tie
  const melbourne = result.topics[1];
  assert.equal(melbourne.total, 2);
  assert.equal(melbourne.articles, 1);
  assert.equal(melbourne.chapters, 1);
  assert.equal(melbourne.coveragePercent, 66.7);
  assert.deepEqual(melbourne.sources, { 'books/memoir': 1, 'articles/bulletin': 1 });
});

test('topic collection reads vault files once and excludes book fragments', t => {
  const { collect, rank } = require('./priorities');
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'kd-topics-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  fs.mkdirSync(path.join(root, 'vault/books/memoir'), { recursive: true });
  fs.mkdirSync(path.join(root, 'vault/articles/paper/1968'), { recursive: true });
  const content = '---\ntitle: Example\ndate: 1968-01-01\ntags:\n  - Melbourne\n---\nText';
  for (const file of ['vault/books/memoir/1-chapter.md', 'vault/books/memoir/summary.md', 'vault/articles/paper/1968/article.md']) fs.writeFileSync(path.join(root, file), content);
  fs.symlinkSync(path.join(root, 'vault/books/memoir/1-chapter.md'), path.join(root, 'vault/books/memoir/duplicate.md'));
  const docs = collect(root);
  assert.equal(docs.length, 2);
  assert.equal(rank(docs).topics[0].total, 2);
  assert.equal(docs[0].publicationDecade, '1960s');
});
