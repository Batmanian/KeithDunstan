# AI Agent Instructions — Keith Dunstan Archive

This file helps AI coding assistants be immediately productive in the Keith Dunstan digital archive project.

## Project Overview
Digital archive of Australian journalist Keith Dunstan (1925–2013), built with Eleventy (11ty) + Bootstrap 5 + Gulp. Site: https://keithdunstan.org. Content: memoirs, articles from The Bulletin (under pseudonym "Batman"), Walkabout magazine.

## Essential Workflows

### Build & Development
- **Local dev**: `npm run watch` (outputs to `dev/`, browser-sync enabled)
- **Production build**: `npm run build` (outputs to `public/`, minified, optimized)
- **Deploy**: `git push` triggers Netlify build from `public/`
- **Never edit**: `dev/`, `public/`, `docs/` — these are build outputs

### Content Management
- **Articles**: Add to `src/posts/bulletin/` or `src/posts/walkabout-magazine/`
- **Books**: Add chapters to `src/posts/[book-slug]/` (e.g., `no-brains-at-all/`)
- **Trove ingestion**: Use Python scripts in `trove/` → review output → move to `src/posts/`
- **OCR processing**: Use `ocr/index.js` for scanned documents → manual correction required

## Key Conventions
- **Frontmatter**: Every `.md` file needs `title`, `date`, `summary`. Articles add `categories` and `tags` (5–15 granular proper nouns only).
- **Language**: Australian English, single-quote dialogue.
- **Tags**: Proper nouns (people, places, organizations) — no descriptive labels.
- **File naming**: Book chapters prefixed with numbers (e.g., `1-chapter-title.md`).

## Pitfalls to Avoid
- Committing `.env` (Trove API key) — it's gitignored.
- Empty `tags: []` in articles — breaks tag filtering.
- OCR errors in fetched content — always review and correct.
- Changing build output directories — breaks Gulp/Netlify pipeline.

## Documentation Links
- [CLAUDE.md](CLAUDE.md) — Keith-specific content rules, collections, frontmatter details
- [README.md](README.md) — General 11ty + Bootstrap + Gulp setup
- [trove/README.md](trove/README.md) — Trove API scripts, ingestion workflow
- [package.json](package.json) — Dependencies and scripts
- [.eleventy.js](.eleventy.js) — Eleventy configuration, filters

## Validation
After changes: Run `npm run build` to ensure no errors. Check tag pages and collections render correctly.