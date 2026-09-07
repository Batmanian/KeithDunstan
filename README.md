# Keith Dunstan Archive

A digital archive of **Keith Dunstan** (1925–2013), Australian journalist and author. The site preserves his books and magazine articles for public access. Copyright is held by his literary estate and managed by his family.

**Live site:** https://keithdunstan.org  
**Repository:** https://github.com/JackDunstan/KeithDunstan

---

## Tech Stack

Built with [Eleventy (11ty)](https://www.11ty.dev/) using the 11straps boilerplate (Eleventy + Bootstrap 5), compiled with Gulp, deployed via [Netlify](https://www.netlify.com/) from this repository.

---

## Local Development

Requires Node.js (v14+).

All book chapters and articles are authored in the `vault/` git submodule
(an Obsidian vault) rather than directly under `src/` — clone with
`--recurse-submodules`, or run `git submodule update --init` after a plain
clone, or `src/books/`/`src/articles/` will be full of broken symlinks and
the build will be missing all content.

```bash
git clone --recurse-submodules https://github.com/JackDunstan/KeithDunstan.git

npm install       # Install dependencies
npm run watch     # Local dev server with live reload at http://localhost:3000
npm run build-dev # Build to /dev (unminified)
npm run build     # Build to /docs (minified, for production)
```

Pushes to `master` trigger automatic Netlify build and deploy.

---

## Project Structure

```
/
├── vault/                         # Git submodule (Obsidian vault) — the content authority
│   ├── books/[book-slug]/*.md     # Book chapters — edit here, not in src/
│   └── articles/[publication-slug]/*.md
├── src/
│   ├── books/                    # Symlinks into vault/books/ (created by `npm run link:vault`)
│   │   └── [book-slug]/
│   │       ├── 0-introduction.md  -> ../../../vault/books/[book-slug]/0-introduction.md
│   │       └── 1-chapter-name.md  -> ...
│   ├── articles/                 # Symlinks into vault/articles/, same pattern
│   │   ├── bulletin/
│   │   ├── walkabout-magazine/
│   │   └── the-australian-gourmet/
│   ├── _includes/                # Nunjucks layout templates and snippets
│   └── *.njk                     # Top-level pages (index pages for books/articles)
├── dev/                          # Dev build output (do not edit)
├── docs/                         # Production build output, deployed by Netlify (do not edit)
├── ocr/                          # Working directory for OCR source files
├── scripts/link-vault-content.js # Symlinks vault/ content into src/ (`npm run link:vault`)
├── _redirects                    # Netlify redirect rules (legacy URL support only)
├── .eleventy.js
├── gulpfile.js
└── CLAUDE.md                     # Instructions for Claude AI assistance
```

---

## URL Structure

```
/books/[book-slug]/[chapter-filename]/
/articles/[publication-slug]/[article-slug]/
```

**Note:** Legacy `/posts/` URLs from earlier versions of this site are handled by `_redirects` on Netlify only — they do not resolve in local development. All source files use the correct `/books/` and `/articles/` paths.

---

## Books

| Folder | Title |
|--------|-------|
| `a-day-in-the-life-of-australia` | A Day in the Life of Australia |
| `my-life-with-the-demon` | My Life with the Demon |
| `no-brains-at-all` | No Brains At All |
| `ratbags` | Ratbags |
| `supporting-a-column` | Supporting a Column |
| `the-australian-uppercrust-book` | The Australian Upper Crust Book |
| `wowsers` | Wowsers |

## Article Collections

| Folder | Publication |
|--------|-------------|
| `bulletin` | The Bulletin |
| `walkabout-magazine` | Walkabout Magazine |
| `the-australian-gourmet` | The Australian Gourmet |

---

## Content Workflow

Content is transcribed from physical books and digitised magazine scans (sourced from Trove, State Library Victoria), and authored directly into the `vault/` submodule — an Obsidian-compatible vault that is the single source of truth for every chapter and article. `src/books/`/`src/articles/` never hold real content files; they're symlinks, kept in sync with `npm run link:vault`. See `CLAUDE.md` for the full transcription workflow and frontmatter requirements.

---

## AI Assistance

This project uses Claude (via Claude Code) for OCR transcription and content management. See `CLAUDE.md` for detailed instructions covering frontmatter, tagging rules, prose conventions, and transcription prompts.
