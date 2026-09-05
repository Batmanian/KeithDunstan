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

**'A Day in the Life of Australia' sidebar context:** Every chapter in this book (except the Introduction) shows a context note at the top of the sidebar: "Commissioned by 'The Age' newspaper to celebrate Australia's bicentennial in 1988, Keith wrote a historical account of Australia's history for each day of the year. This is his column about [title]." This is driven by a `bookContext` field in `src/books/a-day-in-the-life-of-australia/a-day-in-the-life-of-australia.json` and rendered conditionally in `blogsidebar-single.njk`. New chapter files in this directory inherit it automatically; add `excludeBookContext: true` to any front-matter file (like the Introduction) where the phrasing doesn't apply.

**Token budget:** For token-heavy tasks (large subagent fan-outs, bulk transcription/triage runs, big searches), don't spend more than ~75% over a typical session's usage unless the user explicitly directs otherwise. If a task looks like it'll blow past that, pause and check in rather than running it to completion.

**Key constraints:**
- **Check `MISTAKES.md` before starting work in an area** — it's a running log of past failures, their root causes, and the rule that stops each one recurring. If an entry covers the approach being considered, follow its Rule instead of re-deriving it. Log a new entry there (per its own format) whenever something breaks, the user corrects an approach, or a fix takes more than one attempt — entries that recur 4+ times graduate into a rule here in `CLAUDE.md`, per that file's own promotion process.
- Adding, sourcing or crediting any image: see `src/assets/images/CLAUDE.md` first — it governs rights clearance, sidecar records and credit formatting, and this file's rules do not override it. It's a nested `CLAUDE.md`, so it also loads automatically whenever work touches that directory.
- Do not manually edit `dev/` or `docs/` — both are build output
- Link targets are enforced globally, not per-link: `src/_includes/snippets/footer.njk` runs a script on every page that opens any link to a different hostname in a new tab (`target="_blank" rel="noopener"`) and forces same-hostname links to stay in the current tab. Don't hand-add `target="_blank"` to individual `<a>` tags in templates or content — it's redundant and can drift from the rule. This covers hand-written links in `.njk` templates and markdown-rendered links in content files alike (including the Trove source link appended to every transcribed article), so newly added content gets correct behaviour automatically.
- **Bulletin article titles — no "Around Melbourne:" prefix.** The "Around Melbourne" column header from the physical Bulletin adds no value in the archive. Use only the article's own subtitle as the `title:` field (e.g. `"Black Sunday for the Port Girls"`, not `"Around Melbourne: Black Sunday for the Port Girls"`). Apply this to filenames too — the slug must not include `around-melbourne-` (e.g. `1964-05-09-black-sunday-for-the-port-girls.md`, not `1964-05-09-around-melbourne-black-sunday-for-the-port-girls.md`). The "Around Melbourne" column name may still appear verbatim in the Trove source citation line at the end of each article, since that records the title as printed.
- **Trove source citation format** (every transcribed Bulletin/Walkabout/Gourmet article ends with one, after a `<hr>`): the article title is plain text, not a link — the hyperlink wraps "National Library of Australia's Trove database" instead. Exact template:
  ```
  *Source: {Title as originally published}, {Publication}, {date}. Accessible via the [National Library of Australia's Trove database]({Trove nla.gov.au URL}).*
  ```
  Real example: `*Source: Around Melbourne: Goodbye to the Glaci, The Bulletin, 27 April 1963. Accessible via the [National Library of Australia's Trove database](https://nla.gov.au/nla.obj-701264126).*` Use the `nla.obj-` fulltext URL (from the stub's own Source line, or looked up via the Trove v3 API if no stub exists — see `trove/fetch_batman.py`) — never guess or fabricate a Trove URL.
- Preserve Keith Dunstan's voice exactly; Australian English; single-quote dialogue
- Tags are granular proper nouns only (people, places, organisations)
- **Tags must be listed alphabetically** in every file's frontmatter `tags:` block — sort case-insensitively, ignoring leading articles ("The", "A"). Apply this order when writing new files and when editing existing ones.
- Article files should have 5–15 tags; book chapter files may have empty tags
- Tag spelling must match exactly across every file that uses it — `src/tags.njk` builds one page per tag via `permalink: /topic/{{ tag | slug }}/`, so variants like "Foster's Lager" vs "Fosters Lager", "St Kilda" vs "St. Kilda", or "X & Y" vs "X and Y" slugify to the same URL and crash the Eleventy build with `DuplicatePermalinkOutputError`. Check `src/_data/topics.md` for the canonical spelling before adding a new tag, and reuse it verbatim.
- **Tag every proper noun actually named in the body, not just the piece's ostensible subject — including passing references, jokes and comparisons.** A name dropped mid-joke (e.g. Bob Hawke name-checked in a column that isn't "about" politics, Warwick Capper invoked as a simile for a leaping dog, Captain Cook as a stock line about a rapturous homecoming) is exactly as taggable as the main subject — the test is "is this a real, identifiable person/place/organisation," not "is this piece about them." Before considering a file done: reread the finished body, list every capitalised proper noun in it (people, places, organisations, named works/events/products), and resolve each one — already in `src/_data/topics.md` → tag it; genuinely notable and missing → add an entry in the established voice (see the summary voice guide below) and tag it; too minor/generic to ever get its own topic page (a one-off unnamed extra, a generic job title) → leave untagged, but make that a deliberate call, not an oversight. "Book chapter files may have empty tags" describes the outcome for a chapter that truly contains no taggable proper nouns after this scan — it is not a shortcut past doing the scan.
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

**Sub-chapter headings within long chapters:** Use `<h2 id="slug">Heading Text</h2>` HTML inline in the markdown file — never `## markdown headings` or `**bold**` text. The slug is the heading text lowercased with spaces replaced by hyphens and punctuation removed (e.g. `Six O'Clock Closing` → `six-oclock-closing`, `The Evil of Tattersall's` → `the-evil-of-tattersalls`). The jump link TOC is driven by a `sections:` frontmatter field (a YAML list of `{title, anchor}` pairs) which `blogsidebar-single.njk` renders as an "In this chapter" list in the sidebar (desktop and mobile), positioned between the summary and "Related topics". Do not add an inline TOC list to the chapter body. The corresponding book index page (`.njk`) sub-chapter list items should link to these anchors using the pattern `<a href="{{ '/books/[book]/[chapter]/' | url }}#slug">Sub-chapter name</a>`.

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

**OCR tooling:** Two options, in order of preference:

1. **Tesseract (free, no API credits required)** — system binary at `/opt/homebrew/bin/tesseract`. Prefer this unless the Anthropic API key has confirmed credits.
2. **`ocr/transcribe.js`** — sends images to the Claude API (`claude-opus-4-7`). Requires `ANTHROPIC_API_KEY` with remaining credits in `.env`.

**iPhone scan pipeline (HEIC files):** iPhones save scans as HEIC. Both Tesseract and the Claude API need plain PNG. Use `sips` to convert, then rotate if needed (phone shots of open books are typically 90° off):

```bash
# 1. Convert HEIC → PNG
mkdir -p /tmp/converted
for f in scans/*.HEIC; do
  sips -s format png "$f" --out /tmp/converted/"$(basename "${f%.HEIC}").png" -Z 1800
done

# 2. Rotate 90° (open-book phone shots usually need this — verify with one image first)
mkdir -p /tmp/rotated
for f in /tmp/converted/*.png; do
  sips -r 90 "$f" --out /tmp/rotated/"$(basename "$f")"
done

# 3. Delete originals once conversion is confirmed — only delete scans that have been fully transcribed;
#    keep any that cover chapters still pending (e.g. a chapter being rescanned)
rm scans/IMG_NNNN.HEIC  # list individually, don't glob-delete untranscribed chapters
```

**Tesseract dependency fix (one-time, per machine):** Tesseract requires `libtiff.5.dylib` but Homebrew ships `.6`. Fix with a symlink:

```bash
ln -sf /opt/homebrew/opt/libtiff/lib/libtiff.6.dylib /opt/homebrew/opt/libtiff/lib/libtiff.5.dylib
```

**Book scan workflow (Tesseract):**
1. Convert and rotate scans as above → `/tmp/rotated/*.png`
2. Run Tesseract across all pages: `for f in /tmp/rotated/*.png; do echo "=== $(basename $f) ==="; tesseract "$f" stdout -l eng --psm 6; echo; done > /tmp/ocr-raw.txt`
3. Read `/tmp/ocr-raw.txt` — note that phone shots of open books capture two pages at once, so OCR output contains noise from the facing page bleeding into each line. Cross-reference with visual reads of the original images to reconstruct clean text.
4. Write `.md` files following the frontmatter conventions above; add tags, summaries, and inter-chapter navigation links by hand.

**Book scan workflow (Claude API / `ocr/transcribe.js`):**
1. `sips` batch-convert `scans/*.HEIC` or `scans/*.jpeg` → `/tmp/converted/*.png` (and rotate if needed)
2. Run `node ocr/transcribe.js /tmp/converted/*.png` to print transcriptions to stdout
3. Review output, split at chapter headings, and write `.md` files following the frontmatter conventions above
4. Add tags, summaries, and inter-chapter navigation links by hand

See `ocr/transcribe.js` for the Claude API pipeline (requires `ANTHROPIC_API_KEY` in env and `npm install sharp @anthropic-ai/sdk`).

**Trove tooling:** `trove/` contains Python scripts for fetching Keith Dunstan's articles from the National Library of Australia's Trove API v3. Pipeline: `setup.py` (once) → `fetch_batman.py` / `fetch_byline.py` → `deduplicate.py` → `remove_duplicates.py` → `triage.py` (interactive review) → move to `src/articles/[publication-slug]/`. See `trove/README.md` for full context.

**Adding a new book (checklist):** whether it's a fresh title or one being added ahead of scans arriving, every book needs all four of these or the site's three "list every book" surfaces (Books page, timeline, bibliography data) drift out of sync:
1. **Index page** — `src/[book-slug].njk`, following the pattern of existing minimal book pages (e.g. `src/the-perfect-cup.njk`): title/summary frontmatter, a lead paragraph, publisher/ISBN if known, and a placeholder note if chapters haven't been transcribed yet.
2. **`src/books.njk` accordion entry** — linking to the index page. **Keep the whole accordion sorted chronologically (oldest first)** — insert the new entry in its correct year position rather than appending to the end.
3. **`src/_data/books.json` entry** — `{ title, year, url, summary }` — this is what powers `/timeline/` (via the `timeline` collection in `.eleventy.js`), so a book only shows up there once it's added here. Order within the file doesn't matter (the collection sorts by date), but keeping it roughly chronological makes the file easier to scan.
4. **Cover image** — if a real cover exists, save it to `src/img/` and reference it directly. If not yet available, point the `<img>` in both the index page and the `books.njk` accordion entry at `src/img/no-cover.svg` (`alt="Cover not yet available"`) as a fallback rather than referencing a jpg that doesn't exist yet — swap it for the real cover once scanned.

**Foreword/Introduction convention:** surveyed 26 Aug 2026 — every book on the site with front-matter (a Foreword and/or Introduction) gives it its own chapter file linked from the Contents list, the same as any numbered chapter; it is never folded as full prose into the book's index page (the index page's "From the original dust jacket"/"About the book" box is marketing copy or a short pull-quote, not a substitute for the actual text). Follow this for every new book:
- One front-matter item (just a Foreword, or just an Introduction): number it `0-`, e.g. `0-introduction.md`, `0-foreword.md`, with the real Chapter 1 starting at `1-`. This is the dominant existing pattern (Wowsers, My Life with the Demon, No Brains At All, Sports, Supporting a Column, Knockers).
- Both a Foreword and an Introduction: number them `0-foreword` and `1-introduction`, with the real Chapter 1 starting at `2-`. (Ratbags and The Paddock That Grew predate this rule and instead number `1-foreword`/`2-introduction`/`3-`... — left as-is rather than renumbered, since renumbering would change their already-published chapter URLs; this `0-`/`1-`/`2-` scheme is for new books going forward.)
- If the Contents list credits someone else as the Foreword's author, use the `<a>Foreword</a>, by {Author}` phrasing (see `supporting-a-column.njk`, `the-paddock-that-grew.njk`), not a parenthetical.
- Known gap: `no-brains-on-tuesday.njk`'s Foreword (by Michael Smith) only exists as a one-sentence pull-quote inline on the index page — the full text was transcribed from the original scans per this file's own data notes, but no `0-foreword.md` was ever written and the source scans are gone (gitignored, overwritten by a later session), so it can't be completed without a re-scan. Don't treat that file's inline-quote pattern as a model to copy.
