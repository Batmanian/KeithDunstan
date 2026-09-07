#!/usr/bin/env node
// Sets an explicit `image:` frontmatter field on every book chapter and
// article that belongs to a book/publication with cover art in the vault
// (see link-vault-images.js), so a shared link shows that cover in its
// Open Graph/Twitter Card preview instead of the sitewide fallback
// (src/_data/metadata.json's image, Keith's author portrait) — the only
// piece of Open Graph data not already derived from existing frontmatter
// (title, summary, tags, date, categories all feed snippets/opengraph.njk
// directly; see that file's comments).
//
// Edits are surgical text insertion (an `image:` line added right after
// `date:`), not a full YAML re-parse/re-serialise, so every other line —
// tag ordering, quoting style, blank lines — is left untouched. Skips any
// file that already has an `image:` key, and content fragments
// (summary/acknowledgements/front-matter.md, not standalone pages).
//
// Run with `npm run set:og-images`.

const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..");
const VAULT = path.join(ROOT, "vault");
const FRAGMENT_FILES = new Set(["summary.md", "acknowledgements.md", "front-matter.md"]);

// book-slug -> cover image path (as used in frontmatter `image:`)
const BOOK_COVERS = {
  "a-day-in-the-life-of-australia": "/img/adayinthelifeofaustralia.jpg",
  "batman-in-the-bulletin": "/img/batmaninthebulletin.jpg",
  "just-jeans-the-story": "/img/justjeansthestory.jpg",
  "knockers": "/img/knockers.jpg",
  "my-life-with-the-demon": "/img/mylifewiththedemon.jpg",
  "no-brains-at-all": "/img/no-brains-at-all.jpg",
  "no-brains-on-tuesday": "/img/nobrainsontuesday.jpg",
  "ratbags": "/img/ratbags.jpg",
  "saint-ned": "/img/saintned.jpg",
  "sports": "/img/sports.jpg",
  "supporting-a-column": "/img/supporting-a-column.jpg",
  "the-australian-uppercrust-book": "/img/theaustralianuppercrustbook.jpg",
  "the-confessions-of-a-bicycle-nut": "/img/confessionsofabicyclenut.jpg",
  "the-paddock-that-grew": "/img/thepaddockthatgrew.jpg",
  "wowsers": "/img/wowsers.jpg",
};

// publication-slug -> representative cover image
const PUBLICATION_COVERS = {
  "readers-digest": "/img/readers-digest.jpg",
  "walkabout-magazine": "/img/walkabout-1969-12.jpg",
};

function setImage(filePath, imagePath) {
  const original = fs.readFileSync(filePath, "utf8");
  const match = original.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) return false;
  if (/^image:/m.test(match[1])) return false; // already set, never overwrite

  const dateLineMatch = match[1].match(/^date:.*$/m);
  if (!dateLineMatch) return false;

  const insertion = `${dateLineMatch[0]}\nimage: ${imagePath}`;
  const updatedFrontmatter = match[1].replace(dateLineMatch[0], insertion);
  const updated = original.replace(match[1], updatedFrontmatter);
  fs.writeFileSync(filePath, updated);
  return true;
}

function processDir(dir, imagePath) {
  let count = 0;
  if (!fs.existsSync(dir)) return count;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (!entry.isFile() || path.extname(entry.name) !== ".md") continue;
    if (FRAGMENT_FILES.has(entry.name)) continue;
    if (setImage(path.join(dir, entry.name), imagePath)) count++;
  }
  return count;
}

let total = 0;
for (const [slug, imagePath] of Object.entries(BOOK_COVERS)) {
  total += processDir(path.join(VAULT, "books", slug), imagePath);
}
for (const [slug, imagePath] of Object.entries(PUBLICATION_COVERS)) {
  total += processDir(path.join(VAULT, "articles", slug), imagePath);
}

console.log(`Set image: frontmatter on ${total} file(s).`);
