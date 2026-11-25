#!/usr/bin/env node
// Detects tag slug collisions across all Eleventy source files.
// Two tags that differ only in case or punctuation (e.g. "Gold Rush" and
// "gold rush") produce the same /topic/<slug>/ URL and cause a
// DuplicatePermalinkOutputError at build time.
//
// Usage:  node scripts/check-tag-slugs.js
// Exit 0 = no conflicts.  Exit 1 = conflicts found (message printed to stderr).

const fs = require('fs');
const path = require('path');

// Replicates Eleventy's built-in `slug` filter (sindresorhus/slugify behaviour):
// lowercase, collapse non-alphanumeric runs to a single hyphen, trim hyphens.
function toSlug(tag) {
  return tag
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

// Collect all .md files under a directory, following symlinks.
function collectMdFiles(dir, results = []) {
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch {
    return results;
  }
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isSymbolicLink()) {
      let resolved;
      try { resolved = fs.realpathSync(full); } catch { continue; }
      const stat = fs.statSync(resolved, { throwIfNoEntry: false });
      if (!stat) continue;
      if (stat.isDirectory()) collectMdFiles(resolved, results);
      else if (resolved.endsWith('.md')) results.push(resolved);
    } else if (entry.isDirectory()) {
      collectMdFiles(full, results);
    } else if (entry.name.endsWith('.md')) {
      results.push(full);
    }
  }
  return results;
}

// Extract the tags array from a file's YAML frontmatter.
function extractTags(filePath) {
  let content;
  try { content = fs.readFileSync(filePath, 'utf8'); } catch { return []; }
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return [];
  const frontmatter = match[1];
  // Find the tags block: "tags:\n  - Foo\n  - Bar"
  const tagsMatch = frontmatter.match(/^tags:\s*\n((?:[ \t]+-[^\n]*\n?)*)/m);
  if (!tagsMatch) return [];
  return tagsMatch[1]
    .split('\n')
    .map(l => {
      let t = l.replace(/^\s*-\s*/, '').trim();
      // Strip YAML quoting (e.g. "Foo" or 'Foo' are just the string Foo)
      if ((t.startsWith('"') && t.endsWith('"')) ||
          (t.startsWith("'") && t.endsWith("'"))) {
        t = t.slice(1, -1);
      }
      return t;
    })
    .filter(Boolean);
}

const srcDir = path.join(__dirname, '../src');
const files = collectMdFiles(srcDir);

// Map slug → Set of distinct tag strings that produce it
const slugToTags = new Map();

for (const file of files) {
  const tags = extractTags(file);
  for (const tag of tags) {
    const slug = toSlug(tag);
    if (!slugToTags.has(slug)) slugToTags.set(slug, new Set());
    slugToTags.get(slug).add(tag);
  }
}

const conflicts = [];
for (const [slug, tags] of slugToTags) {
  if (tags.size > 1) {
    conflicts.push({ slug, tags: [...tags].sort() });
  }
}

if (conflicts.length === 0) {
  console.log('check-tag-slugs: no conflicts found.');
  process.exit(0);
}

console.error('check-tag-slugs: tag slug conflicts detected — these will cause a build error:\n');
for (const { slug, tags } of conflicts.sort((a, b) => a.slug.localeCompare(b.slug))) {
  console.error(`  slug "${slug}"  ←  ${tags.map(t => JSON.stringify(t)).join('  vs  ')}`);
}
console.error('\nFix by making all variants use the same string (usually the title-case form).');
process.exit(1);
