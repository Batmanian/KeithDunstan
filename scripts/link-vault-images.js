#!/usr/bin/env node
// Moves the images that are actual book/publication IP — cover art, and
// images embedded directly in article/chapter text — into the vault
// submodule, then symlinks src/img/ back to them. Same single-sourcing
// pattern as link-vault-content.js: every template/content reference stays
// exactly as it is (still `/img/wowsers.jpg` etc.), only the file itself
// becomes a symlink into vault/books/[slug]/ or vault/articles/[slug]/.
//
// Generic site chrome (favicons, UI icons, the sitewide fallback author
// portrait, stub-book covers with no vault directory yet) is deliberately
// left alone — only images tied to a book/publication that already has a
// vault/ directory are in scope. Run once; re-running is a no-op for
// anything already migrated (skips files that are already symlinks).
//
// Run with `npm run link:vault-images`.

const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..");
const IMG_DIR = path.join(ROOT, "src", "img");

// filename in src/img/ -> vault-relative destination
const IMAGE_MAP = {
  // Book covers (co-located with each book's existing vault directory)
  "adayinthelifeofaustralia.jpg": "books/a-day-in-the-life-of-australia/adayinthelifeofaustralia.jpg",
  "batmaninthebulletin.jpg": "books/batman-in-the-bulletin/batmaninthebulletin.jpg",
  "keith-as-batman.jpg": "books/batman-in-the-bulletin/keith-as-batman.jpg",
  "justjeansthestory.jpg": "books/just-jeans-the-story/justjeansthestory.jpg",
  "knockers.jpg": "books/knockers/knockers.jpg",
  "mylifewiththedemon.jpg": "books/my-life-with-the-demon/mylifewiththedemon.jpg",
  "no-brains-at-all.jpg": "books/no-brains-at-all/no-brains-at-all.jpg",
  "nobrainsontuesday.jpg": "books/no-brains-on-tuesday/nobrainsontuesday.jpg",
  "ratbags.jpg": "books/ratbags/ratbags.jpg",
  "saintned.jpg": "books/saint-ned/saintned.jpg",
  "sports.jpg": "books/sports/sports.jpg",
  "supporting-a-column.jpg": "books/supporting-a-column/supporting-a-column.jpg",
  "theaustralianuppercrustbook.jpg": "books/the-australian-uppercrust-book/theaustralianuppercrustbook.jpg",
  "confessionsofabicyclenut.jpg": "books/the-confessions-of-a-bicycle-nut/confessionsofabicyclenut.jpg",
  "thepaddockthatgrew.jpg": "books/the-paddock-that-grew/thepaddockthatgrew.jpg",
  "wowsers.jpg": "books/wowsers/wowsers.jpg",

  // Images embedded directly in chapter/article body text
  "demon-p207-menu.png": "books/my-life-with-the-demon/demon-p207-menu.png",
  "theaustralianuppercrustbookp9.jpg": "books/the-australian-uppercrust-book/theaustralianuppercrustbookp9.jpg",

  // Publication-representative covers
  "readers-digest.jpg": "articles/readers-digest/readers-digest.jpg",
  "walkabout-1969-12.jpg": "articles/walkabout-magazine/walkabout-1969-12.jpg",
};

let moved = 0;
let skipped = 0;

for (const [filename, vaultRel] of Object.entries(IMAGE_MAP)) {
  const srcPath = path.join(IMG_DIR, filename);
  const vaultPath = path.join(ROOT, "vault", vaultRel);

  if (!fs.existsSync(srcPath)) {
    skipped++;
    continue;
  }
  if (fs.lstatSync(srcPath).isSymbolicLink()) {
    continue; // already migrated
  }

  fs.mkdirSync(path.dirname(vaultPath), { recursive: true });
  fs.renameSync(srcPath, vaultPath);
  const relTarget = path.relative(IMG_DIR, vaultPath);
  fs.symlinkSync(relTarget, srcPath);
  moved++;
}

console.log(`Moved ${moved} image(s) into vault/, symlinked from src/img/. (${skipped} not found, already absent.)`);
