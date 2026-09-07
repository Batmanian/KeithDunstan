#!/usr/bin/env node
// Regenerates the Obsidian vault (vault/) from the site's content directories.
// Mirrors every book chapter and article file into the same relative folder
// structure, skipping the Eleventy-only config/index files (*.json, the
// per-book *-index.njk / book-slug.njk pages) that aren't chapter content.
//
// Content is copied verbatim except for one mechanical fix: chapter-nav
// lines use Eleventy's `{{ '/books/x/y' | url }}` template filter (e.g.
// `Continue to the next chapter: <a href="{{ '/books/x/y' | url }}">...`),
// which Obsidian can't evaluate and would otherwise show as broken literal
// text. That filter is a no-op on this site (no pathPrefix), so it's
// resolved to the plain path — the link and its text are unchanged, only
// the unrendered template syntax is removed.
//
// Ratbags' chapters are the one book stored as *.njk instead of *.md (same
// frontmatter/content shape, no real templating) — those are included too,
// written out with a .md extension so Obsidian treats them as notes.
//
// The vault is its own git repository (a submodule of this one), so this
// script only ever touches vault/books/ and vault/articles/, never
// vault/.git, vault/.obsidian, or vault/README.md.
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

function copyContent(srcDir, destDir, bookSlug) {
  let copied = 0;
  fs.mkdirSync(destDir, { recursive: true });
  for (const entry of fs.readdirSync(srcDir, { withFileTypes: true })) {
    const srcPath = path.join(srcDir, entry.name);
    const ext = path.extname(entry.name);
    if (entry.isDirectory()) {
      copied += copyContent(srcPath, path.join(destDir, entry.name), entry.name);
      continue;
    }
    if (!entry.isFile()) continue;

    const isMarkdown = ext === ".md";
    const isChapterNjk = ext === ".njk" && bookSlug && !isBookIndexFile(entry.name, bookSlug);
    if (!isMarkdown && !isChapterNjk) continue;

    const destName = isChapterNjk ? entry.name.replace(/\.njk$/, ".md") : entry.name;
    const content = fs.readFileSync(srcPath, "utf8");
    fs.writeFileSync(path.join(destDir, destName), resolveUrlFilters(content));
    copied += 1;
  }
  return copied;
}

let total = 0;
for (const { src, dest } of SOURCES) {
  fs.rmSync(dest, { recursive: true, force: true });
  total += copyContent(src, dest, null);
}

console.log(`Exported ${total} files to vault/`);
