# Todo — Keith Dunstan Archive

Tracking outstanding work across all active workstreams.
Last updated: 27 July 2026.

**Status legend used throughout this file:**

| Symbol | Meaning |
|---|---|
| ✅ | Live on site — transcribed, tagged, complete |
| 📝 | Drafted — body text exists but file is incomplete (wrong extension, placeholder frontmatter, or otherwise not build-ready) |
| 🔤 | OCR'd — scan converted to JPEG in `ocr/`, awaiting transcription |
| 📷 | Scanned — HEIC photos exist in `Scans/`, awaiting OCR conversion |
| 📂 | Scan folder created, but empty — awaiting physical scan |
| ⬜ | Known (title/date confirmed from a contents page or Trove) but no file, folder, or scan exists yet |
| ❓ | Existence/extent unknown — no confirmed source |

---

## 1. Books — overview

| Book | Year | Chapters known | ✅ Live | 📝/🔤/📷 In progress | ⬜ Not started | Notes |
|---|---|---|---|---|---|---|
| No Brains At All | 1990 | 15 (intro + 14) | 15 | 0 | 0 | Complete |
| My Life with the Demon | 1994 | 13 | 13 | 0 | 0 | Complete |
| Supporting a Column | 1966 | 9 | 9 | 0 | 0 | Complete |
| The Australian Upper Crust Book | 1971 | 1 (Keith's chapter only) | 1 | 0 | 0 | Complete as scoped — other authors' chapters out of scope |
| Ratbags | 1980 | 26 (foreword + intro + 24 profiles) | 26 | 0 | 0 | Complete — see §2 for chapter detail |
| Wowsers | 1968 | 10 | 2 | 6 📝 (empty stubs) | 2 | See §3 for chapter detail |
| A Day in the Life of Australia | 1989 | 258 known daily entries | 8 | 11 📝 | 239 | See §4 — scale makes full per-entry tracking impractical |
| Batman in the Bulletin | 2004 | Themed excerpt collection, not chapters | — | — | — | Sourced from Bulletin articles directly; see §5 |
| Kiwi | 2017 | ? | 0 | 0 | ❓ | Not started — no scans, no source material logged |
| Moonee Ponds to Broadway | 2005 | ? | 0 | 0 | ❓ | Not started |
| Collins: the story of Australia's premier street | 2005 | ? | 0 | 0 | ❓ | Contributor credit only — scope unclear |
| The Confessions of a Bicycle Nut | 1999 | ? | 0 | 0 | ❓ | Not started |
| No Brains on Tuesday | 1991 | ? | 0 | 0 | ❓ | Not started |
| Saint Ned | 1980 | ? | 0 | 0 | ❓ | Not started |
| The Store on the Hill | 1979 | ? | 0 | 0 | ❓ | Not started |
| Knockers | 1972 | ? | 0 | 0 | ❓ | Not started — no scans |
| Sports | 1970 | ? | 0 | 0 | ❓ | Not started — no scans |
| The Paddock That Grew | 1962 | ? | 0 | 0 | ❓ | Not started — MCG history |

---

## 2. Ratbags (1980) — chapter detail

Contents list sourced from `src/ratbags.njk`, cross-checked against `src/books/ratbags/*.njk`, `src/books/ratbags/Scans/`, and `ocr/`.

| # | Chapter | Status | Notes |
|---|---|---|---|
| 1 | Foreword (Barry Humphries) | ✅ | |
| 2 | Introduction | ✅ | |
| 3 | Beatrice Miles | ✅ | |
| 4 | Stephen Harold Gascoigne | ✅ | |
| 5 | John Barry Humphries | ✅ | |
| 6 | Edward William Cole | ✅ | Stray empty `Scans/Chapter 4 - Edward William Cole/` folder left behind — safe to remove, chapter already complete |
| 7 | Clement Lindley Wragge | ✅ | |
| 8 | James George Beaney | ✅ | |
| 9 | Alfred Edward Lynch | ✅ | |
| 10 | Hugh Donald McIntosh | ✅ | Scans/OCR files for this chapter still present — cleanup script not yet run |
| 11 | William Charles Wentworth IV | ✅ | Scans/OCR files still present — cleanup not yet run |
| 12 | Prince Leonard of Hutt | ✅ | Scans/OCR files still present — cleanup not yet run |
| 13 | George Dick Meudell | ✅ | Transcribed most recently — Scans/OCR files still present, cleanup not yet run |
| 14 | Frank Thring | ✅ | Scans/OCR files still present — cleanup not yet run |
| 15 | Lillian Frank | ✅ | Transcribed most recently — Scans/OCR files still present, cleanup not yet run |
| 16 | Xavier (Alfred Francis) Herbert | ✅ | Scans/OCR files still present — cleanup not yet run |
| 17 | Percy Wills Cerutty | ✅ | Scans/OCR files still present — cleanup not yet run |
| 18 | Arthur Stace | ✅ | Scans/OCR files still present — cleanup not yet run |
| 19 | Leonard Paul Evans | ✅ | Scans/OCR files still present — cleanup not yet run |
| 20 | King O'Malley | ✅ | Scans/OCR files still present — cleanup not yet run |
| 21 | Alexander Tolmer | ✅ | Scans/OCR files still present — cleanup not yet run |
| 22 | Percy Aldridge Grainger | ✅ | Scans/OCR files still present — cleanup not yet run |
| 23 | Germaine Greer | ✅ | Scans/OCR files still present — cleanup not yet run |
| 24 | Justus Jorgensen | ✅ | Scans/OCR files still present — cleanup not yet run; corrected spelling from "Jorgenson" to "Jorgensen" to match the book |
| 25 | Clement John De Garis | ✅ | Scans/OCR files still present — cleanup not yet run |
| 26 | Kevin Charles — Pro Hart | ✅ | Scans/OCR files still present — cleanup not yet run |

**Ratbags is now complete: 26 of 26 chapters live.** Remaining housekeeping: run `scripts/ocr-cleanup.sh` for chapters 10–26 whose Scans/OCR working files are all still present (cheap to regenerate, HEIC originals should be trashed once reviewed).

* Fix opening lines in chapters so that they're in sentence case
* Ensure all pages link to the next chapter except the last.

---

## 3. Wowsers (1968) — chapter detail

Contents list sourced from `src/wowsers.njk`.

| # | Chapter | Status | Notes |
|---|---|---|---|
| 1 | Wowser | ✅ | |
| 2 | The Evil of the Desecration of the Sabbath | ✅ | |
| 3 | The Evil of the Demon Drink | 📝 | `3-the-evil-of-the-demon-drink.mx` — frontmatter only (`title: XX`, `tags: XXX`), no body text. Has 6 sub-sections in the original contents (The Sots, The Glorious Days of Abstinence, The Seductive Lures, Prohibition, Sober by Law, Six O'Clock Closing) not yet reflected in any file |
| 4 | The Evil of Smoking | 📝 | Same empty-stub pattern |
| 5 | The Theatre Evil and the Evil of Dancing | 📝 | Same empty-stub pattern |
| 6 | The Evil of Bathing | 📝 | Same empty-stub pattern |
| 7 | The Evil of Cremation | 📝 | Same empty-stub pattern |
| 8 | The Evil of the Social Evil | 📝 | Same empty-stub pattern |
| 9 | The Evil of the Printed Word | ⬜ | No file exists at all |
| 10 | The Gambling Evil | ⬜ | No file exists; original has 5 sub-sections (The Collingwood Tote, The Worrall Affair, The Triumph of William Henry Judkins, Totes Bookies and S.P. Men, The 'Evil' of Tattersall's) |

**Data issue found:** the Contents list in `src/wowsers.njk` (lines 48–76) has chapters 3–10 all pointing their `href` at `/books/my-life-with-the-demon/1-the-early-demon` — either a copy-paste artefact or a broken placeholder. The attribute is also misspelled `hrex` instead of `href` on every one of these links, so they don't render as links at all currently. Needs fixing once chapters 3–10 are transcribed and can point to their own pages.

---

## 4. A Day in the Life of Australia (1989)

The book's contents page (`src/a-day-in-the-life-of-australia.njk`) lists **258 known daily entries** across January–December. Given the scale, per-entry tracking isn't practical here — instead:

| Status | Count | Detail |
|---|---|---|
| ✅ Live (`.md`) | 8 | a-brand-new-commonwealth, bridge-disaster-divides-hobart, a-body-blow-to-cricket, a-woman-hanged, clipping-coupons, a-hollow-affair-for-burke-and-wills, duke-makes-sport-in-the-colonies, a-pirate-in-melbourne |
| 📝 Drafted, wrong extension (`.mx`) | 11 | eighteen-wickets-to-fall, the-garbage-symphony, mad-jack-berry, the-wonder-of-listening-in, oh-woe-a-cash-amateur, victoria-ablaze, plane-travels-faster-than-a-horse-or-automobile, last-ride-for-captain-moonlight, stuart-corsses-the-continent, first-fleet-anchors-in-sydney-cove, man-disappears-during-drunken-freak |
| ⬜ Known, no file | 239 | Everything else listed in the January–December contents on the book's index page |

**Data issues found:**
- The 11 `.mx` files **do** contain real transcribed body text (18–27 lines each), unlike the Wowsers stubs — they just have placeholder frontmatter (`title: XXXX`, `date: 1988-XX-XX`, `tags: - XXX`) and the wrong file extension, so Eleventy never builds them. These are the fastest wins: fill in real title/date/tags, rename to `.md`, and they're publishable.
- `src/books/my-life-with-the-demon/a-brand-new-commonwealth.ini` is a stray file — it's actually a plain-text checklist of the first 19 January titles for *this* book, misplaced inside the `my-life-with-the-demon` folder. Should be deleted once no longer needed as a reference (its content is now captured in this file).
- `src/_includes/snippets/theage.njk` contains a master link list of ~280 titles for this book, but every link points at `/articles/bulletin/[slug]` instead of `/books/a-day-in-the-life-of-australia/[slug]`, and every link label is a placeholder (`X.`, date `Y`). This file isn't currently included anywhere live (its usage in `articles.njk` is commented out) but should be fixed or removed rather than left as dead, broken scaffolding.
- A handful of filename mismatches between the January contents list and the actual `.mx` files exist (e.g. `plane-travels-faster-than-horse-or-automobile` vs file `plane-travels-faster-than-a-horse-or-automobile.mx`; `last-ride-for-captain-moonlite` — the historically correct spelling — vs file `last-ride-for-captain-moonlight.mx`; `stuart-crosses-the-continent` vs file `stuart-corsses-the-continent.mx`; `mace-disappears-during-drunken-freak` vs file `man-disappears-during-drunken-freak.mx`). Reconcile spelling against the original book when transcribing.
- Source scan images for this book live uncompressed in `src/books/a-day-in-the-life-of-australia/dayinthelifeofaustralia/*.jpg` (committed to the repo, not gitignored like `Scans/`) — worth confirming these are meant to be tracked long-term or should move to the standard `Scans`/`ocr` workflow.

---

## 5. Articles by publication

| Publication | ✅ Live | Known outstanding (titled) | Stubs awaiting triage (Trove) | Notes |
|---|---|---|---|---|
| The Bulletin | 46 | 2 | 1,594 | 34 "Around Melbourne" columns (Mar–Dec 1962) transcribed from manually-scanned photos on 28–29 Jul 2026; separate from the untouched Trove stub pipeline. See §6 for the Trove pipeline and the 2 known-missing titles below |
| Walkabout Magazine | 4 | 15 | 81 | 18 known articles per site total; 15 remain untranscribed even after Trove triage — see list below |
| The Australian Gourmet | 1 | — | Not in Trove | Extent of Keith's total output for this title is unknown; physical copies needed |
| The Age (post-1954) | 0 | 1 known ("On the right side of Tuscany", 2 May 1989) | Not in Trove | Not digitised — physical/microfilm sourcing required |
| Home Beautiful | 0 | 8 known issues (Dec 1949 – Feb 1951, `src/writing.njk`) | Not in Trove | Not yet sourced |

### Walkabout — 15 outstanding, known titles

- [ ] Paddy's Market to Luxury Hotel — `1962-07-01` *(check: a file of this exact name already exists at `src/articles/walkabout-magazine/paddys-market-to-luxury-hotel.md` — confirm this isn't already done before re-transcribing)*
- [ ] Epicurean Melbourne — `1962-12-01`
- [ ] Freedom of Beach — `1963-01-01`
- [ ] From Prickly Pear to Petroleum — `1963-07-01`
- [ ] Christmas Across the Continent — `1963-12-01`
- [ ] Melbourne's Evergreen Exhibition — `1964-05-01`
- [ ] Adventures of a Would-be Wine Snob — `1964-12-01`
- [ ] Battle of the Flowers — `1965-05-01`
- [ ] Melbourne Cup Winners, Horses or Hats? — `1966-10-01`
- [ ] 1966 and All That — `1966-12-01`
- [ ] The Bikini – What's Next? — `1968-01-01`
- [ ] A Year of Anti-Football Protest — `1968-04-01`
- [ ] Beef Boom in Tombstone Territory — `1968-10-01`
- [ ] Collins Street Charm — `1968-12-01`
- [ ] Walkabout Profile — Dr Jean Battersby — `1969-05-01`

### Bulletin — 2 known-missing titles

*(Updated 29 Jul 2026 — the `src/bulletin/` path-conflict described below was already resolved per the Completed section; both drafts now live correctly under `src/articles/bulletin/`. "Batman's Melbourne: This is a fine state to be in" is live at `src/articles/bulletin/batmans-melbourne-this-is-a-fine-state-to-be-in.md`.)*

- [ ] **"Around Melbourne: Those Were the Days" (10 Mar 1962)** — still missing, but the reason has changed: the photo folder `trove/output/bulletin/stubs/Scans/1962-03-10-around-melbourne-those-were-the-days/` does not actually contain scans of this article. Its three page photos are a duplicate re-scan of "The New Image" (already live, now at `src/articles/bulletin/the-new-image.md`, correctly dated 1962-03-03). The correct Trove URL for "Those Were the Days" is `https://nla.gov.au/nla.obj-701126572` — needs a fresh, correctly-labelled photo of the actual article before it can be transcribed.
- [ ] **"Try a Sim-L Car" (21 Jul 1962)** — folder `trove/output/bulletin/stubs/Scans/1962-07-21-around-melbourne-try-a-sim-l-car/` also contains the wrong photos: they're actually a single page of "Out and About Inside Toorak" (1962-07-14), which has been recovered and transcribed as `src/articles/bulletin/inside-toorak.md` — but that transcription itself cuts off mid-sentence partway through the piece, since only one page/two exposures of it exist. Both "Try a Sim-L Car" (Trove URL `https://nla.gov.au/nla.obj-696379653`) and the remainder of "Inside Toorak" still need proper scans.

Note: two of the 34 newly-transcribed columns — "Rediscovering the Yarra" (1 Dec 1962) and "An Albert Tucker for 2s. a Mile" (15 Dec 1962) — are signed "—FAWKNER" rather than "—BATMAN" in the original scan. Confirmed this is just a second pen name of Keith's (after Melbourne's other co-founder, John Fawkner) — both pieces are his and belong in the archive as normal.

---

## 6. Trove API Pipeline

Scripts live in `trove/`. Run from within that directory with the `.venv` activated. `trove/output/` is **not** gitignored — confirm before committing whether the raw stub corpus (~1,675 files) is meant to be tracked, given the Trove data-agreement expiry note below.

**Summary convention (added 29 Jul 2026 — applies to every stub still in this pipeline):** `summary` frontmatter must describe what the piece is actually about, not `"First published in [Publication], [date]."` — full rationale, good/bad examples, and the exact voice to match are now in `CLAUDE.md`. This was previously the norm for nearly every transcribed Bulletin/Walkabout/Gourmet article (45 of 46 Bulletin files, all 4 Walkabout files, the one Gourmet file) — all retrofitted with real summaries in this pass. The stub generators (`fetch_batman.py`, `fetch_byline.py`, `fetch_walkabout.py`) still correctly write the boilerplate as a placeholder marked `[Stub — not yet transcribed]` — that's fine and doesn't need changing — but replacing it with a real summary is now an explicit, required step of finishing a transcription, not optional polish. Also fixed in this pass: all three fetch scripts, `setup.py`, and `README.md` pointed transcribers at the wrong output directory (`src/posts/[publication]/` — a stale path from before the `src/articles/` rename); corrected to `src/articles/[publication]/` everywhere except the ~1,594 already-generated stub files sitting in `trove/output/*/stubs/`, which still have the old path in their body text and weren't worth a bulk find-replace (CLAUDE.md is the authoritative instruction anyway, per `trove/README.md`'s own workflow step).

### Bulletin stubs — triage

**1,594** stub `.md` files are in `trove/output/bulletin/stubs/` awaiting review. No files have moved to `transcribed/` or `rejected/` yet — those subfolders don't exist until `triage.py` creates them.

- [ ] Run `python triage.py` to work through stubs one at a time
  - `k` — keep as stub (return later)
  - `t` — confirmed Keith article, full text added → moves to `transcribed/`
  - `r` — noise or family mention → moves to `rejected/`
  - `q` — quit and save progress (resumes where you left off)
- [ ] Move confirmed transcribed files from `trove/output/bulletin/transcribed/` to `src/articles/bulletin/` *(not `src/posts/bulletin/` — see CLAUDE.md URL structure rule)*
- [ ] Commit and push — Netlify builds automatically

**Known noise to reject quickly during triage:**
- Files titled `CONTENTS`, `Advertising`, `The Bulletin`, `columns`, `no-title`
- Files where snippet mentions `Mr. and Mrs. W. Dunstan` or similar family references
- Files titled `BOOKS`, `LETTERS`, `NATIONAL NOTEBOOK` (section headers, not articles)

**Early column names to look for (pre-Batman, 1962–1966):**
- `Around Melbourne` — Keith's column before the Batman pen name
- `Out and About` — transitional column name used 1972–1973
- `Out and About with Batman` — bridge period

### Walkabout stubs — triage and transcription

**81** stubs in `trove/output/walkabout/stubs/`.

- [ ] Update `triage.py` to accept a `--publication` argument — it currently only triages `bulletin/`
- [ ] Cross-reference triaged stubs against the 18 known Walkabout articles (4 live, 15 outstanding — see §5)
- [ ] Move completed files to `src/articles/walkabout-magazine/` *(not `src/posts/walkabout-magazine/`)*

### Trove scripts — maintenance

- [ ] Update `trove/README.md` to reflect the publication folder structure
- [x] `diagnose_epicurean.py` — run 29 Jul 2026, confirmed not digitised in Trove (see §7 for full result)
- [ ] `diagnose_readers_digest.py` / `diagnose_the_age.py` exist but haven't been reported as run — confirm results

### Publications confirmed NOT in Trove (post-1954)

| Publication | Status |
|---|---|
| The Herald (Melbourne, 1954–1988) | Not digitised in Trove |
| The Sun News-Pictorial | Not digitised in Trove |
| The Courier-Mail | Not digitised in Trove |
| The Age (post-1954) | Not digitised in Trove |
| Good Weekend | Not digitised in Trove |
| Herald & Weekly Times | Not in Trove |
| Australian Gourmet Traveller | Not in Trove |
| The Australian | Not in Trove |
| The Sun-Herald | Not in Trove |
| Reader's Digest | American publication — not in Trove |
| Epicurean Magazine | Confirmed not digitised in Trove (29 Jul 2026) |

---

## 7. Physical Transcription — Newspapers and Magazines

For publications not in Trove, physical copies must be sourced and scanned. Follow the OCR workflow in `CLAUDE.md` (`scripts/ocr-prep.sh` → transcribe → `scripts/ocr-cleanup.sh`).

**Priority targets:**
- [ ] The Sun News-Pictorial — `A Place in the Sun` column, 1958–1978 (large body of work; consider sampling key pieces first)
- [ ] The Herald — regular contributions post-1978
- [ ] The Courier-Mail — `Day by Day` column (pre-1958 period)
- [ ] The Age — regular columnist, post-1982
- [ ] **Epicurean Magazine** — mentioned on homepage (`src/index.njk`) and in `src/books/my-life-with-the-demon/13-demonic-people.md` (edited by Alan Holdsworth, 1970s food/wine magazine, annual wine-industry dinner/award). `diagnose_epicurean.py` run 29 Jul 2026: **not digitised in Trove** — zero results for "Keith Dunstan" under every `l-title` variant tried (`Epicurean`, `The Epicurean`, `Epicurean Magazine`, `Epicurean (Melbourne)`, `Epicurean.`). The only Trove hit combining "Keith Dunstan" + "Epicurean" is an unrelated 1962 piece titled "Epicurean Melbourne" published *inside Walkabout magazine* (already tracked as a separate outstanding Walkabout title, §5) — not a match for the actual Epicurean Magazine. Physical sourcing needed; the homepage's link to `recollection.com.au/collections/epicurean-magazine/` is a plausible lead to check for archived issues/content
- [ ] Australian Gourmet Traveller — extent unknown

**Sources:** State Library Victoria (ProQuest newspaper archive) for Herald/Sun/Age; personal and family clipping archives.

---

## 8. Site — Technical

- [x] **Bulletin collection path conflict** — resolved: both drafts moved into `src/articles/bulletin/`, `src/bulletin/` removed. `/bulletin/` index now auto-populates from an Eleventy `bulletin` collection (globs `src/articles/bulletin/*.md`), grouped into folding accordion-by-decade
- [ ] **Missing favicon asset — `src/img/safari-pinned-tab.svg`** — referenced by `<link rel="mask-icon">` in `src/_includes/snippets/head.njk` on every page but the file was never committed (404 on all ~1127 pages). Needs the original monochrome mask-icon SVG from whichever favicon-generator bundle produced the rest of `src/img/favicon*` — can't be faithfully recreated without the source logo art. `src/img/site.webmanifest` was similarly missing and has been recreated (references the existing `favicon-32x32.png`/`apple-touch-icon.png`); once the SVG is supplied, drop it in `src/img/` and no template change is needed.
- [x] **Search** — replaced Google Custom Search Engine with Pagefind (free, static-site-native, no external dependency). `npx pagefind --site dev` runs after the Eleventy build in both `build` and `build-dev` (package.json); indexing is scoped to real content only via `data-pagefind-body` on `<main>` in `layouts/post.njk` (topic/index/search pages are correctly excluded — confirmed via `pagefind` CLI output: 125 of 1462 pages indexed). `src/search.njk` has a custom results UI (not the packaged PagefindUI widget) built on the raw Pagefind JS API, matching the site's existing card style from `postloop.njk` — shows title, excerpt, publication, and date per result. Publication/date are exposed as `data-pagefind-meta` in `postcontent.njk`: `date` reuses the existing `<time>` element, `publication` reads `categories[0]` when present (articles) or derives a label from the URL's collection slug via the new `humanizeSlug`/`split` Eleventy filters (books, which have no `categories` field). Existing tag/keyword cloud retained beneath results, unchanged. Verified with a full `npm run build` and `npm run build-dev` — Pagefind assets survive `prod-copy`/`purgecss`/`minify-html` into `public/pagefind/` intact. Not verified in an actual browser (no browser available in the environment this was built in) — worth a manual click-through after deploy.
- [ ] **Theme** — evaluate migration from 11straps/Bootstrap 5 to Eleventy Excellent (fluid typography, modern CSS, Eleventy v3, built-in tag navigation). Decision pending — site is functional as-is; migration is cosmetic/structural
- [x] **Epicurean Magazine** — Trove diagnostic run 29 Jul 2026 (`diagnose_epicurean.py` already existed, wasn't previously run). Confirmed not digitised — see §7 for full detail and next steps
- [ ] **`triage.py`** — add `--publication` flag to support Walkabout and future publications
- [ ] **Annual Trove review** — per data agreement, review published articles against current Trove availability annually (next due: before 31 December 2026)
- [ ] **Data agreement expiry** — Trove API data agreement expires 31 December 2026; raw API results (JSON/CSV in `trove/output/`) must be deleted by then unless renewed
- [ ] **Stray files to clean up:** `src/books/my-life-with-the-demon/a-brand-new-commonwealth.ini` (misplaced planning file, see §4); empty `src/books/ratbags/Scans/Chapter 4 - Edward William Cole/` folder (chapter already complete)
- [ ] **Unexplained Eleventy tag-doubling — worked around, not root-caused.** `src/books/my-life-with-the-demon/13-demonic-people.md` renders its "Related topics" list twice on every `/topic/*` page it appears on. Confirmed via direct `gray-matter` parsing that the file's own frontmatter is clean (24 unique tags, listed once each), but Eleventy's data cascade hands templates `item.data.tags` with 49 entries (`"book"` + the 24 tags, twice) — verified with temporary debug logging in `.eleventy.js`'s `tagList` collection builder and the `filterTagList` filter. Checked and ruled out: no `.11tydata.json`/`.11tydata.js` sidecar file, no duplicate `tags:` key in the frontmatter, no stray YAML anchors, no other directory-data file beyond `src/books/books.json` (`tags: ["book"]`, doesn't explain the doubling of the *other* 24). Tested a structurally similar file (`src/books/ratbags/5-john-barry-humphries.njk`, also inherits `book` via directory data, also multi-tagged) and it behaves correctly — so this is isolated to this one file, not a general `setDataDeepMerge(true)` issue, and the actual mechanism inside Eleventy 3.1.5's TemplateData/computed-data cascade was never found. **Current fix:** both `filterTagList` and the `tagList` collection builder in `.eleventy.js` now dedupe with `[...new Set(tags)]` before filtering/counting, which fully resolves the visible symptom (and is good practice regardless — guards against any future accidental duplicate tag). Worth a proper root-cause dig if this resurfaces on another file or if Eleventy is upgraded.
- [ ] **Related, already fixed:** three files had a trailing empty `-` bullet at the end of their `tags:` list (YAML parses it as `null`), which was generating a garbage `/topic/null/` page site-wide — `src/articles/walkabout-magazine/bird-watching.md`, `src/articles/walkabout-magazine/rough-riding-for-five-minutes-a-year.md`, `src/books/no-brains-at-all/10-apits.md`. The stray lines have been removed; worth a quick grep (`grep -rn "^\s*-\s*$" src --include="*.md" --include="*.njk"` after a `tags:` block) next time new content is transcribed, since it's an easy copy-paste slip.
- [ ] **Review how book introductions are handled relative to their contents pages — inconsistent across books.** Each book's index page (`src/[book-slug].njk`) lists a contents/chapter list, and separately each book has some form of introduction/foreword content (e.g. Ratbags has a distinct "Introduction" chapter *and* a Barry Humphries foreword — both listed as chapters in `src/ratbags.njk`; other books may fold intro text into the index page itself, or omit it, or handle it differently again). No single convention currently governs whether an introduction is: its own chapter file linked from the contents list, inline prose on the book's index page, or something else. Needs a survey of all book index pages (`src/*.njk` for each book slug) plus their `src/books/[book-slug]/` folders to catalogue the current pattern per book, then a decision on a consistent approach going forward.
- [ ] **Explore generating books as ePub / PDF downloads** — for the books that are complete or near-complete on-site (Ratbags, No Brains At All, My Life with the Demon, Supporting a Column), investigate assembling a downloadable ePub and/or PDF per book so readers aren't limited to the chapter-by-chapter web view. Needs: (1) a way to resolve chapter order per book — currently only implicit in each book's numeric filename prefix (`0-introduction`, `1-a-nice-suburb`, ...) and in the hand-written contents list on each book's index page (e.g. `src/ratbags.njk`); no single machine-readable ordering exists yet. (2) a build tool — options worth comparing: Pandoc (markdown/HTML → ePub/PDF, mature, scriptable, not Eleventy-specific), `@11ty/eleventy-plugin-...`-style ePub generators (check npm for current maintained options — none confirmed yet), or a Puppeteer/`eleventy-plugin-pdf`-driven print-CSS-to-PDF approach reusing the existing `layouts/post.njk` styling. (3) where output files live/are linked from (per-book download link on `src/[book-slug].njk`, output into `public/downloads/` or similar, excluded from the `dev/`/Pagefind build). Cover images already exist per book (`src/img/[book-slug].jpg`) and could double as the ePub/PDF cover. No implementation started — this is exploration/spike only.
- [x] **`summary` frontmatter rewritten to feed `og:description` properly (29 Jul 2026).** Previously nearly every Bulletin/Walkabout/Gourmet article's `summary` was just `"First published in [Publication], [date]."` — meaningless boilerplate that was also the literal text search engines and link previews (Slack, X, iMessage, etc.) showed for every single page, since `opengraph.njk` (see below) pulls `og:description`/`twitter:description` straight from `summary`. Rewrote all 46 Bulletin, all 4 Walkabout, and the 1 Gourmet article summaries to actually describe what each piece is about, in the same voice as `src/_data/topics.md`'s entries. Convention (with good/bad examples) is now documented in `CLAUDE.md` so it's self-sustaining for the huge remaining Trove-triage backlog — see the note under §6 above.
- [x] **Found and fixed while doing the above: `og:title`/`og:description`/`twitter:*`/`article:tag` etc. broke silently on any page whose title or summary contained a literal `"`** (e.g. `£7000 for "Divinely Dressed Ladies"`, or a summary quoting "beer czar") — 16 files were affected. Root cause: the `{% metagen %}` shortcode (`eleventy-plugin-metagen`) returns raw HTML rather than going through Nunjucks' normal auto-escaping `{{ }}` output, so quote/ampersand characters passed straight through unescaped and truncated the HTML attribute, corrupting everything downstream in `<head>`. Fixed by piping `title`/`summary`/`imageAlt` through Nunjucks' `escape` filter before they reach the shortcode call, in `src/_includes/snippets/opengraph.njk`. Verified with a full rebuild — zero broken meta tags across all 1462 output pages. Worth remembering for any *future* field added to that shortcode call: it needs the same `| escape` treatment, since the shortcode itself won't do it.
- [x] **Found and fixed in the same file: `when-flappers-fluttered-through-the-flames.md` had ~45 lines of unrelated, badly-OCR'd text (about the "Livingston brothers" yacht racing) glued onto the end of the actual article body**, past its real ending ("Could this be a new name for the Cleopatra in, say, 1967?"). Stray content from some earlier copy/paste, unrelated to the Bulletin piece it was appended to. Removed — worth a spot-check of other older, pre-this-session Bulletin files for the same kind of tail contamination, since it clearly wasn't caught before.

---

## Completed ✓

- [x] Trove API key obtained and configured
- [x] `trove/` folder structure created (11 publications × up to 3 status dirs)
- [x] `fetch_batman.py` — Batman column articles fetched (1,594 stubs currently in `bulletin/stubs/`)
- [x] `fetch_byline.py` — Keith Dunstan byline articles fetched (100 additional)
- [x] `deduplicate.py` — duplicates identified and removed
- [x] `fetch_walkabout.py` — 81 Walkabout stubs fetched
- [x] `triage.py` — interactive browser triage tool built
- [x] `remove_duplicates.py` — automated duplicate removal script built
- [x] `setup.py` — folder structure creation script built
- [x] Trove API data agreement submitted to NLA
- [x] Trove publication diagnostics run for all major publications
- [x] Bulletin articles — 7 transcribed and live on site
- [x] Walkabout articles — 4 transcribed and live on site (Bird Watching, Rough-Riding, Summer Madness, Paddy's Market to Luxury Hotel)
- [x] Ratbags — all 26 of 26 chapters live (foreword, introduction, 24 profiles) — book complete
- [x] Books fully live on site: No Brains At All, Supporting a Column, My Life with the Demon, The Australian Upper Crust Book, Ratbags (as scoped)
- [x] Books partially live: A Day in the Life of Australia (8 of 258 known entries + 11 drafted), Wowsers (2 of 10 chapters)
