#!/usr/bin/env node
// Adds a `status:` frontmatter field to every article in vault/articles/:
//
//   status: stub         hidden placeholder (eleventyExcludeFromCollections: true
//                        or a "[Stub — ...]" title); not yet transcribed
//   status: for review   transcribed, awaiting the archive owner's check of the
//                        text against the scan (see trove/review_articles.py)
//   status: published    reviewed and live
//
// `status` is a workflow marker only. It does not change what the site shows:
// visibility is still controlled by eleventyExcludeFromCollections, so running
// this never unpublishes anything.
//
// Edits are a one-line text insertion (after the `date:` line), not a YAML
// re-serialise. Per CLAUDE.md, every file is re-parsed after the edit and the
// write is refused unless every other frontmatter field and the body are
// byte-for-byte unchanged. Files that already have `status:` are left alone.
//
//   node scripts/set-article-status.js                 # dry run: counts only
//   node scripts/set-article-status.js --write
//   node scripts/set-article-status.js --write --review vault/articles/x/1946/a.md [...]
//       (--review: these files get "for review" instead of "published")

const fs = require("fs");
const path = require("path");
const matter = require("gray-matter");

const ROOT = path.join(__dirname, "..");
const ARTICLES = path.join(ROOT, "vault", "articles");

const args = process.argv.slice(2);
const write = args.includes("--write");
const reviewIdx = args.indexOf("--review");
const review = new Set(
  reviewIdx === -1 ? [] : args.slice(reviewIdx + 1).filter(a => !a.startsWith("--")).map(p => path.resolve(ROOT, p))
);

function walk(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) {
      if (e.name !== "scans") walk(p, out);
    } else if (e.name.endsWith(".md")) out.push(p);
  }
  return out;
}

function parse(text) {
  // Bypass gray-matter's cache so each parse is independent.
  const m = matter(text, { excerpt: false, cache: false });
  return { data: m.data, content: m.content };
}

const counts = { stub: 0, "for review": 0, published: 0, skipped_has_status: 0, skipped_no_frontmatter: 0, refused: 0 };
for (const file of walk(ARTICLES)) {
  const text = fs.readFileSync(file, "utf8");
  const fm = text.match(/^---\r?\n([\s\S]*?)(\r?\n---[ \t]*\r?\n)/);
  if (!fm) { counts.skipped_no_frontmatter++; console.log("NO FRONTMATTER", path.relative(ROOT, file)); continue; }
  const before = parse(text);
  if (Object.prototype.hasOwnProperty.call(before.data, "status")) { counts.skipped_has_status++; continue; }

  const isStub = before.data.eleventyExcludeFromCollections === true || /^\[Stub/.test(String(before.data.title || ""));
  const status = isStub ? "stub" : review.has(file) ? "for review" : "published";
  if (isStub && review.has(file)) console.log("NOTE: --review ignored for stub", path.relative(ROOT, file));

  // Insert after the top-level `date:` line; fall back to just before the closing ---.
  const block = fm[1];
  const nl = text.includes("\r\n") ? "\r\n" : "\n";
  const dateLine = block.match(/^date:.*$/m);
  let newBlock;
  if (dateLine) {
    const at = dateLine.index + dateLine[0].length;
    newBlock = block.slice(0, at) + nl + `status: ${status}` + block.slice(at);
  } else {
    newBlock = block + nl + `status: ${status}`;
  }
  // Keep the original closing delimiter byte-for-byte (some carry trailing spaces).
  const newText = text.slice(0, fm.index) + "---" + nl + newBlock + fm[2] + text.slice(fm.index + fm[0].length);

  const after = parse(newText);
  const { status: got, ...rest } = after.data;
  const same = JSON.stringify(rest) === JSON.stringify(before.data) && after.content === before.content;
  if (!same || got !== status) {
    counts.refused++;
    console.log("REFUSED (verification failed)", path.relative(ROOT, file));
    continue;
  }
  counts[status]++;
  if (write) fs.writeFileSync(file, newText);
}
console.log(write ? "Written:" : "Dry run (use --write):", counts);
