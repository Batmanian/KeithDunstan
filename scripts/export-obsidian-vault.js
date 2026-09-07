#!/usr/bin/env node
// One-off/rare-use safety net, NOT the normal workflow — see link-vault-content.js
// for that. The vault (vault/) is the authoritative content source; src/books/
// and src/articles/ are symlinks into it (created by link-vault-content.js), so
// under normal operation there's nothing in src/ for this script to find that
// isn't already a symlink back to the vault.
//
// This script exists for the case where a real (non-symlink) .md/.njk file
// ends up directly in src/books/ or src/articles/ anyway — e.g. old habit, a
// script that hasn't been updated, a merge — and needs absorbing into the
// vault. It only ever reads real files (symlinks are skipped, since those are
// already vault content) and only ever writes into the vault, so it's safe to
// re-run at any time — it can't delete or overwrite existing vault notes.
//
// Absorbed files get the same normalization as the original src-to-vault
// migration: Eleventy's `{{ '/path' | url }}` chapter-nav filter (which
// Obsidian can't evaluate) is resolved to a plain path, and Ratbags' *.njk
// chapters (the one book stored that way, same content shape, no real
// templating) are converted to *.md.
//
// Run `npm run link:vault` afterward to symlink src/ to the absorbed file(s).
// Run with `npm run export:vault`.

const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..");
const SOURCES = [
  { src: path.join(ROOT, "src", "books"), dest: path.join(ROOT, "vault", "books") },
  { src: path.join(ROOT, "src", "articles"), dest: path.join(ROOT, "vault", "articles") },
];

// Matches `{{ '/some/path' | url }}` or `{{ "/some/path" | url }}`.
const URL_FILTER = /\{\{\s*(['"])(.*?)\1\s*\|\s*url\s*\}\}/g;

function resolveUrlFilters(content) {
  return content.replace(URL_FILTER, (_match, _quote, urlPath) => urlPath);
}

// A book's own index/landing page — e.g. src/books/ratbags/ratbags.njk or
// a *-index.njk — lives alongside its chapters but isn't chapter content.
function isBookIndexFile(name, bookSlug) {
  return name === `${bookSlug}.njk` || name.endsWith("-index.njk");
}

// Copies only real (non-symlink) *.md/*.njk files — anything already a
// symlink is already vault content and is left alone.
function absorbStrayContent(srcDir, destDir, bookSlug) {
  let copied = 0;
  if (!fs.existsSync(srcDir)) return copied;
  for (const entry of fs.readdirSync(srcDir, { withFileTypes: true })) {
    if (entry.isSymbolicLink()) continue;
    const srcPath = path.join(srcDir, entry.name);
    const ext = path.extname(entry.name);
    if (entry.isDirectory()) {
      copied += absorbStrayContent(srcPath, path.join(destDir, entry.name), entry.name);
      continue;
    }
    if (!entry.isFile()) continue;

    const isMarkdown = ext === ".md";
    const isChapterNjk = ext === ".njk" && bookSlug && !isBookIndexFile(entry.name, bookSlug);
    if (!isMarkdown && !isChapterNjk) continue;

    const destName = isChapterNjk ? entry.name.replace(/\.njk$/, ".md") : entry.name;
    const destPath = path.join(destDir, destName);
    if (fs.existsSync(destPath)) {
      console.warn(`Skipping ${path.relative(ROOT, srcPath)}: ${path.relative(ROOT, destPath)} already exists in the vault.`);
      continue;
    }
    fs.mkdirSync(destDir, { recursive: true });
    const content = fs.readFileSync(srcPath, "utf8");
    fs.writeFileSync(destPath, resolveUrlFilters(content));
    copied += 1;
  }
  return copied;
}

let total = 0;
for (const { src, dest } of SOURCES) {
  total += absorbStrayContent(src, dest, null);
}

if (total > 0) {
  console.log(`Absorbed ${total} file(s) into vault/. Run 'npm run link:vault' to symlink src/ to them.`);
} else {
  console.log("No stray content files found in src/ — vault is already the sole source.");
}
