## Quick Reference

**Project:** Digital archive of Keith Dunstan (1925–2013), Australian journalist and author.  
**Site:** https://keithdunstan.org — built with Eleventy (11ty) + Bootstrap 5 (11straps boilerplate), Gulp, deployed via Netlify from GitHub.

**Content lives in:**
- `src/books/[book-slug]/` — book chapters
- `src/articles/[publication-slug]/` — magazine/newspaper articles
- Book intro/index pages sit directly in `src/` (e.g. `src/supporting-a-column.njk`, `src/batman-in-the-bulletin.njk`)

**Current collections:**
| Slug | Location | Type | Description |
|------|----------|------|-------------|
| `no-brains-at-all` | `src/books/` | Book | Memoir, 1990 |
| `supporting-a-column` | `src/books/` | Book | Memoir, 1966 |
| `a-day-in-the-life-of-australia` | `src/books/` | Book | Bicentennial history, 1989 |
| `my-life-with-the-demon` | `src/books/` | Book | Memoir, 1994 |
| `ratbags` | `src/books/` | Book | Profiles, 1980 |
| `the-australian-uppercrust-book` | `src/books/` | Book | 1971 (Keith's chapter only) |
| `wowsers` | `src/books/` | Book | 1968 |
| `bulletin` | `src/articles/` | Articles | Written under pseudonym "John Batman" |
| `walkabout-magazine` | `src/articles/` | Articles | Walkabout magazine pieces |
| `the-australian-gourmet` | `src/articles/` | Articles | Gourmet magazine pieces |

**Default layout (`layouts/post.njk`) and collection tag** (`book` or `article`) are set per-collection by `src/books/books.json` and `src/articles/articles.json` — don't repeat them in frontmatter.

**Key constraints:**
- Do not manually edit `dev/`, `public/`, or `docs/` — all are build output
- Preserve Keith Dunstan's voice exactly; Australian English; single-quote dialogue
- Tags are granular proper nouns only (people, places, organisations)
- Article files should have 5–15 tags; book chapter files may have empty tags
- Every `.md` file requires `title`, `date`, and `summary` frontmatter
- Article files may also use a `categories` field (e.g. `- The Bulletin`)

**Frontmatter example — article:**
```yaml
---
title: Alas, poor Tivoli, I knew it well.
date: 1967-04-15
summary: First published in the Bulletin Magazine, 1967.
categories:
- The Bulletin
tags:
  - Tivoli theatre
  - Melbourne
---
```

**Frontmatter example — book chapter:**
```yaml
---
title: Introduction
date: 1990-11-11
summary: The opening for his first book of memoirs, 'No Brains At All'.
tags:
---
```

---

## Trove API Pipeline

Scripts in `trove/` fetch Keith Dunstan's articles from the National Library of Australia's Trove database via API v3. Output: `.md` files for Eleventy.

**Setup:**
- `cd trove`
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`
- Copy `.env.example` to `.env` and add Trove API key

**Scripts:**
- `diagnose_*.py` — Test API for specific publications (e.g., `diagnose_walkabout.py`)
- `fetch_*.py` — Fetch article stubs (e.g., `fetch_batman.py` for Bulletin, `fetch_byline.py` for general)
- `deduplicate.py` — Remove duplicates
- `triage.py` — Interactive review of stubs (keep/transcribe/reject)
- `remove_duplicates.py` — Automated duplicate removal

**Workflow:**
1. Fetch stubs → `trove/output/[publication]/stubs/`
2. Triage with `python triage.py` → move to `transcribed/` or `rejected/`
3. Move transcribed to `src/articles/[publication]/`
4. Commit and push

**Key notes:**
- Preserve Trove source URLs in output
- Tags: granular proper nouns only
- See `trove/README.md` and `todo.md` for details

---

## Outstanding Work

See `todo.md` for full tracking of:
- Bulletin and Walkabout article triage/transcription
- Physical transcription for non-Trove publications
- Book transcription progress
- Site technical improvements (search, theme migration)

**Build:**
```bash
npm run watch    # local dev (output → dev/)
npm run build    # production build (output → public/, what Netlify deploys)
```

**Deploy:** `git push` to `master` triggers Netlify build automatically (configured in `netlify.toml`, publishes from `public/`).

**OCR tooling:** `ocr/` contains a Node.js OCR pipeline (`ocr/index.js`) using `node-tesseract-ocr` for processing scanned documents into markdown.

**Trove tooling:** `trove/` contains Python scripts for fetching Keith Dunstan's articles from the National Library of Australia's Trove API v3. Pipeline: `setup.py` (once) → `fetch_batman.py` / `fetch_byline.py` → `deduplicate.py` → `remove_duplicates.py` → `triage.py` (interactive review) → move to `src/articles/[publication-slug]/`. See `trove/README.md` for full context.
