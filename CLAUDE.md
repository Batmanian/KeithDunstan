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

**Token budget:** For token-heavy tasks (large subagent fan-outs, bulk transcription/triage runs, big searches), don't spend more than ~75% over a typical session's usage unless the user explicitly directs otherwise. If a task looks like it'll blow past that, pause and check in rather than running it to completion.

**Key constraints:**
- Do not manually edit `dev/` or `docs/` — both are build output
- Link targets are enforced globally, not per-link: `src/_includes/snippets/footer.njk` runs a script on every page that opens any link to a different hostname in a new tab (`target="_blank" rel="noopener"`) and forces same-hostname links to stay in the current tab. Don't hand-add `target="_blank"` to individual `<a>` tags in templates or content — it's redundant and can drift from the rule. This covers hand-written links in `.njk` templates and markdown-rendered links in content files alike (including the Trove source link appended to every transcribed article), so newly added content gets correct behaviour automatically.
- Preserve Keith Dunstan's voice exactly; Australian English; single-quote dialogue
- Tags are granular proper nouns only (people, places, organisations)
- Article files should have 5–15 tags; book chapter files may have empty tags
- Tag spelling must match exactly across every file that uses it — `src/tags.njk` builds one page per tag via `permalink: /topic/{{ tag | slug }}/`, so variants like "Foster's Lager" vs "Fosters Lager", "St Kilda" vs "St. Kilda", or "X & Y" vs "X and Y" slugify to the same URL and crash the Eleventy build with `DuplicatePermalinkOutputError`. Check `src/_data/topics.md` for the canonical spelling before adding a new tag, and reuse it verbatim.
- Every `.md` file requires `title`, `date`, and `summary` frontmatter
- Article files may also use a `categories` field (e.g. `- The Bulletin`)
- **`summary` must describe what the piece is actually about — never "First published in [Publication], [date]."** That fact already lives in the `date` field and is emitted separately as `article:published_time` in the page's Open Graph metadata (see "Open Graph metadata" below), so repeating it in `summary` wastes the one sentence a reader (or a search result, or a link preview) actually sees. Write one factual, specific sentence naming the actual subject — a person, event, place, or argument — in the same voice as the entries in `src/_data/topics.md`: declarative, concrete, no throat-clearing ("This article discusses...", "A piece about..."). Mention Keith Dunstan's own role only where it's genuinely part of the story (he covered it, he wrote it as a column, he interviewed the subject), not as a reflex closer on every sentence.
  - The voice to match — a genuine entry from `src/_data/topics.md`: `"The six o'clock swill was the mad rush to down as many beers as possible before hotel bars shut at 6pm, a wartime austerity measure that lingered in Victoria until 1966 and which Keith Dunstan remembered as a defining, faintly absurd feature of 1950s Melbourne drinking."` — definitional, specific, a little wry, ties back to Keith only where it's earned.
  - Applied to an article's `summary` (real example, `src/articles/bulletin/batmans-melbourne-this-is-a-fine-state-to-be-in.md`): `A survey of the deteriorating relations between Victoria and New South Wales, arguing Melbourne's case for its rightful place in the international air network via the new Tullamarine airport.`
  - Bad: `First published in the Bulletin Magazine, 1962.` — says nothing about the piece; this exact boilerplate is what `trove/fetch_batman.py`, `fetch_byline.py`, and `fetch_walkabout.py` write into every stub's `summary` field as a placeholder (correctly marked `[Stub — not yet transcribed]`) — **replacing it with a real summary is part of finishing the transcription, not an optional polish pass.** Don't move a file out of `stubs/`/`transcribed/` into `src/articles/` with that placeholder still in place.
  - avoid Em-dashes, use commas. We need this look to read unlike an AI generated summary.

**Frontmatter example — article:**
```yaml
---
title: Alas, poor Tivoli, I knew it well.
date: 1967-04-15
summary: A eulogy for Melbourne's Tivoli Theatre on its closure, tracing the rise and fall of the city's vaudeville and variety houses from Harry Rickards to Chico Marx.
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
summary: Opens 'No Brains At All' by setting up its central joke — that a working-class Melbourne boyhood produced, by his own account, a journalist of no particular intelligence.
tags:
---
```

**Open Graph metadata:** `src/_includes/snippets/opengraph.njk` (included from every layout via `head.njk`) generates `og:description`/`twitter:description` directly from each page's `summary` frontmatter (falling back to `description`, then to `src/_data/metadata.json`'s sitewide default only when a page has neither). A generic or missing `summary` shows up immediately as a generic link preview — this is the main reason the convention above matters.

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
npm run build    # production build (output → docs/, what Netlify deploys)
```

**Deploy:** `git push` to `master` triggers Netlify build automatically (configured in `netlify.toml`, publishes from `docs/`).

**OCR tooling:** `ocr/` contains a Node.js OCR pipeline (`ocr/index.js`) using `node-tesseract-ocr` for processing scanned documents into markdown.

**Trove tooling:** `trove/` contains Python scripts for fetching Keith Dunstan's articles from the National Library of Australia's Trove API v3. Pipeline: `setup.py` (once) → `fetch_batman.py` / `fetch_byline.py` → `deduplicate.py` → `remove_duplicates.py` → `triage.py` (interactive review) → move to `src/articles/[publication-slug]/`. See `trove/README.md` for full context.
