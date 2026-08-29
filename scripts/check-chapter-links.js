#!/usr/bin/env node
// Verifies every chapter .md file in src/books/[book]/ is linked from src/[book].njk.
// Exits 1 with a clear error message if any chapter is missing from its book index.

const fs = require('fs');
const path = require('path');

const booksDir = path.join(__dirname, '../src/books');
const srcDir = path.join(__dirname, '../src');

let errors = 0;

const books = fs.readdirSync(booksDir).filter(entry => {
  const full = path.join(booksDir, entry);
  return fs.statSync(full).isDirectory();
});

for (const book of books) {
  const bookDir = path.join(booksDir, book);
  const indexFile = path.join(srcDir, `${book}.njk`);

  if (!fs.existsSync(indexFile)) {
    // Some book dirs may not have an index page yet — warn but don't fail.
    console.warn(`Warning: no index page for book '${book}' (expected ${book}.njk)`);
    continue;
  }

  const indexContent = fs.readFileSync(indexFile, 'utf8');

  const chapters = fs.readdirSync(bookDir)
    .filter(f => f.endsWith('.md'))
    .sort();

  for (const chapter of chapters) {
    const slug = chapter.replace(/\.md$/, '');
    const linkPattern = `/books/${book}/${slug}`;
    if (!indexContent.includes(linkPattern)) {
      console.error(`ERROR: '${book}/${slug}' exists but is not linked from ${book}.njk`);
      errors++;
    }
  }
}

if (errors > 0) {
  console.error(`\n${errors} chapter(s) not linked from their book index page.`);
  process.exit(1);
}

console.log('check-chapter-links: all chapters linked. OK');
