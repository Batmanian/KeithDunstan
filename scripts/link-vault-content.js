#!/usr/bin/env node
// Single-sources book/article content from the vault/ submodule into the
// Eleventy site: every markdown file in vault/books/ and vault/articles/
// gets a symlink under src/books/ and src/articles/ (the path Eleventy
// actually reads). Editing a note in the vault — via Obsidian or otherwise
// — is immediately what the site builds from; there is no copy step and
// nothing to keep in sync by hand.
//
// Ratbags is the one book whose chapters Eleventy reads as *.njk (run
// through the Nunjucks engine, not markdown-it) even though the vault
// stores them as *.md (see export-obsidian-vault.js, which does the
// reverse mapping when populating the vault). The symlink keeps the .njk
// name so Eleventy's template-engine selection is unaffected — only the
// file's content, which comes from the vault, changes.
//
// Non-content files that live alongside chapters in src/ — directory data
// (books.json, articles.json, [book-slug].json), raw scan images/HEICs —
// are never touched; only the *.md/*.njk chapter symlinks are managed
// here, and only within src/books/ and src/articles/.
//
// Run with `npm run link:vault` after adding or removing a note in the
// vault (new note, renamed/deleted file).

const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..");
const NJK_BOOKS = new Set(["ratbags"]);

// Index-page content fragments (see export-obsidian-vault.js / .eleventy.js's
// bookContent filter) are always read as literal filenames by that filter —
// they're not chapters, so the NJK_BOOKS extension mapping below must never
// touch them, even for a book (like Ratbags) whose real chapters map to .njk.
const CONTENT_FRAGMENT_FILES = new Set(["summary.md", "acknowledgements.md", "front-matter.md"]);

const SOURCES = [
  { vault: path.join(ROOT, "vault", "books"), src: path.join(ROOT, "src", "books"), isBooks: true },
  { vault: path.join(ROOT, "vault", "articles"), src: path.join(ROOT, "src", "articles"), isBooks: false },
];

function walkMarkdown(dir, base = dir) {
  let files = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files = files.concat(walkMarkdown(full, base));
    } else if (entry.isFile() && path.extname(entry.name) === ".md") {
      files.push(path.relative(base, full));
    }
  }
  return files;
}

function destRelFor(vaultRelPath, isBooks) {
  const topSlug = vaultRelPath.split(path.sep)[0];
  const basename = path.basename(vaultRelPath);
  if (isBooks && NJK_BOOKS.has(topSlug) && !CONTENT_FRAGMENT_FILES.has(basename)) {
    return vaultRelPath.replace(/\.md$/, ".njk");
  }
  return vaultRelPath;
}

// Creates/repairs a symlink at destAbs pointing at vaultAbs. Returns true if
// it changed anything (already-correct symlinks are left alone).
function ensureSymlink(destAbs, vaultAbs) {
  fs.mkdirSync(path.dirname(destAbs), { recursive: true });
  const relTarget = path.relative(path.dirname(destAbs), vaultAbs);
  const existing = fs.lstatSync(destAbs, { throwIfNoEntry: false });
  if (existing) {
    if (existing.isSymbolicLink() && fs.readlinkSync(destAbs) === relTarget) {
      return false;
    }
    fs.rmSync(destAbs, { force: true, recursive: true });
  }
  fs.symlinkSync(relTarget, destAbs);
  return true;
}

let linked = 0;
let removed = 0;

for (const { vault, src, isBooks } of SOURCES) {
  const wanted = new Map(); // destRelPath -> vault absolute path
  for (const vaultRel of walkMarkdown(vault)) {
    wanted.set(destRelFor(vaultRel, isBooks), path.join(vault, vaultRel));
  }

  for (const [destRel, vaultAbs] of wanted) {
    if (ensureSymlink(path.join(src, destRel), vaultAbs)) linked++;
  }

  // Remove stale symlinks (managed extensions only) whose vault source is gone.
  const managedExt = isBooks ? [".md", ".njk"] : [".md"];
  const sweep = (dir) => {
    if (!fs.existsSync(dir)) return;
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        sweep(full);
        continue;
      }
      if (!managedExt.includes(path.extname(entry.name))) continue;
      if (!fs.lstatSync(full).isSymbolicLink()) continue;
      if (!wanted.has(path.relative(src, full))) {
        fs.rmSync(full);
        removed++;
      }
    }
  };
  sweep(src);
}

console.log(`Linked ${linked} file(s) from vault/ into src/, removed ${removed} stale link(s).`);
