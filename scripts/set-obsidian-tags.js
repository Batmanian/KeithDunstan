#!/usr/bin/env node
// Adds an `obsidian_tags:` frontmatter field alongside the existing `tags:`
// field on every book chapter and article in the vault.
//
// The site's tags are granular proper nouns that often contain spaces
// ("Beatrice Miles", "St Kilda") — required as-is for the site's own
// /topic/[tag]/ page slugging and exact-spelling matching (see CLAUDE.md).
// Obsidian's Tags pane and graph view only recognise tags made of letters,
// digits, `-`, `_` and `/` — no spaces — so those tags are invisible there,
// even though they still work fine as searchable frontmatter Properties.
//
// obsidian_tags: is a hyphenated, Obsidian-valid mirror of the same list,
// in the same order, generated here — never hand-authored. The original
// tags: field is never touched, so the site is completely unaffected.
//
// Edits are surgical text insertion (a new `obsidian_tags:` block added
// right after the existing `tags:` block), not a full YAML re-parse/
// re-serialise, so every other line is left untouched. Skips any file that
// already has an `obsidian_tags:` key, and skips files with no real tags
// (many book chapters intentionally have none — see CLAUDE.md).
//
// Run with `npm run set:obsidian-tags`.

const fs = require("fs");
const path = require("path");
const matter = require("gray-matter");

const ROOT = path.join(__dirname, "..");
const VAULT = path.join(ROOT, "vault");
const FRAGMENT_FILES = new Set(["summary.md", "acknowledgements.md", "front-matter.md"]);

function sanitizeTag(tag) {
  return tag
    .replace(/&/g, "and")
    .replace(/['’"]/g, "")
    .replace(/[()]/g, "")
    .replace(/[^\p{L}\p{N}\s\-_/]/gu, " ")
    .trim()
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
}

function addObsidianTags(filePath) {
  const original = fs.readFileSync(filePath, "utf8");
  const frontmatterMatch = original.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!frontmatterMatch) return false;
  if (/^obsidian_tags:/m.test(frontmatterMatch[1])) return false; // already set

  const { data } = matter(original);
  if (!Array.isArray(data.tags) || data.tags.length === 0) return false;

  const seen = new Set();
  const obsidianTags = [];
  for (const tag of data.tags) {
    if (typeof tag !== "string") continue;
    const sanitized = sanitizeTag(tag);
    if (sanitized && !seen.has(sanitized)) {
      seen.add(sanitized);
      obsidianTags.push(sanitized);
    }
  }
  if (obsidianTags.length === 0) return false;

  // Most files indent tags list items two spaces ("  - Item"); a handful of
  // older files (e.g. Wowsers' chapters) have them at column 0 ("- Item"),
  // and at least one has a single blank line between "tags:" and its first
  // item. Match all three, so the block boundary is found correctly either
  // way — the blank-line allowance uses a lookahead so it only ever
  // consumes a genuinely empty line, never a line with real content after
  // its leading whitespace (which would otherwise eat a real tag's
  // indentation and truncate the match).
  const tagsBlockMatch = frontmatterMatch[1].match(/^tags:[ \t]*(?:\r?\n[ \t]*(?=\r?\n))?(?:\r?\n[ \t]*-.*)*/m);
  if (!tagsBlockMatch) return false;

  const insertion = `${tagsBlockMatch[0]}\nobsidian_tags:\n${obsidianTags.map(t => `  - ${t}`).join("\n")}`;
  const updatedFrontmatter = frontmatterMatch[1].replace(tagsBlockMatch[0], insertion);
  const updated = original.replace(frontmatterMatch[1], updatedFrontmatter);

  // Belt-and-braces: regex-based block matching above has already broken
  // once on an unusual layout (a blank line before the first tag). Rather
  // than trust the regex alone, re-parse the edited file and confirm the
  // original tags: survived byte-for-byte and obsidian_tags: is exactly
  // what was computed — refuse to write otherwise.
  const verify = matter(updated);
  const tagsUnchanged = JSON.stringify(verify.data.tags) === JSON.stringify(data.tags);
  const obsidianTagsCorrect = JSON.stringify(verify.data.obsidian_tags) === JSON.stringify(obsidianTags);
  if (!tagsUnchanged || !obsidianTagsCorrect) {
    console.error(`SKIPPED (verification failed): ${filePath}`);
    return false;
  }

  fs.writeFileSync(filePath, updated);
  return true;
}

function walk(dir) {
  let count = 0;
  if (!fs.existsSync(dir)) return count;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      count += walk(full);
    } else if (entry.isFile() && path.extname(entry.name) === ".md" && !FRAGMENT_FILES.has(entry.name)) {
      if (addObsidianTags(full)) count++;
    }
  }
  return count;
}

const total = walk(path.join(VAULT, "books")) + walk(path.join(VAULT, "articles"));
console.log(`Added obsidian_tags: to ${total} file(s).`);
