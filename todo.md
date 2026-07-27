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
| Ratbags | 1980 | 26 (foreword + intro + 24 profiles) | 13 | 3 🔤 + 10 📂 | 0 | See §2 for chapter detail |
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
| 14 | Frank Thring | 🔤 | OCR'd to `ocr/Chapter 12 - Frank Thring/` (11 pages) — ready to transcribe |
| 15 | Lillian Frank | 🔤 | OCR'd to `ocr/Chapter 13 - Lillian Frank/` (8 pages) — ready to transcribe |
| 16 | Xavier (Alfred Francis) Herbert | 🔤 | OCR'd to `ocr/Chapter 14 - Xavier Herbert/` (13 pages) — ready to transcribe |
| 17 | Percy Wills Cerutty | 📂 | Empty scan folder created, awaiting physical scan |
| 18 | Arthur Stace | 📂 | Empty scan folder created, awaiting physical scan |
| 19 | Leonard Paul Evans | 📂 | Empty scan folder created, awaiting physical scan |
| 20 | King O'Malley | 📂 | Empty scan folder created, awaiting physical scan |
| 21 | Alexander Tolmer | 📂 | Empty scan folder created, awaiting physical scan |
| 22 | Percy Aldridge Grainger | 📂 | Empty scan folder created, awaiting physical scan |
| 23 | Germaine Greer | 📂 | Empty scan folder created, awaiting physical scan |
| 24 | Justus Jorgenson | 📂 | Empty scan folder created, awaiting physical scan |
| 25 | Clement John De Garis | 📂 | Empty scan folder created, awaiting physical scan |
| 26 | Kevin Charles — Pro Hart | 📂 | Empty scan folder created, awaiting physical scan |

**Immediate next steps:** transcribe the three already-OCR'd chapters (Thring, Frank, Herbert); run `scripts/ocr-cleanup.sh` for chapters 10–13 whose scans are stale; physically scan the remaining 10 chapters.

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
| The Bulletin | 7 | 2 | 1,594 | See §6 for the Trove pipeline and the 2 known-missing titles |
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

- [ ] "Around Melbourne: Those Were the Days" (10 Mar 1962) — linked from `src/bulletin.njk` at `/bulletin/1962-03-10-around-melbourne-those-were-the-days/`, but no file exists at that path; a draft exists at `src/bulletin/1962-03-10-around-melbourne-those-were-the-days.md` (see data issue below) and a stub was pulled from `trove/output/bulletin/stubs/` for it
- [ ] "Batman's Melbourne: This is a fine state to be in" (18 Mar 1967) — linked from both `src/bulletin.njk` and `src/batman-in-the-bulletin.njk`; todo.md's own Completed section previously called this "manually transcribed, ready to commit" — a draft exists at `src/bulletin/batmans-melbourne-this-is-a-fine-state-to-be-in.md`, again in the non-standard location (see below)

**Data/structural issue found:** two Bulletin articles have been drafted into a new `src/bulletin/` folder, and `eleventy.js` was updated with a `bulletinCollection` filter that reads from both `src/bulletin/` and `src/articles/bulletin/`. **This conflicts with `CLAUDE.md`'s explicit URL-structure rule** — all articles must live under `src/articles/[publication-slug]/`, and no other structure should be introduced. Before committing, move these two drafts into `src/articles/bulletin/` and revert the `src/bulletin/`-specific parts of the `eleventyConfig` change, keeping only the standard `src/articles/bulletin/*.md` glob.

---

## 6. Trove API Pipeline

Scripts live in `trove/`. Run from within that directory with the `.venv` activated. `trove/output/` is **not** gitignored — confirm before committing whether the raw stub corpus (~1,675 files) is meant to be tracked, given the Trove data-agreement expiry note below.

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
- [ ] `diagnose_epicurean.py` / `diagnose_readers_digest.py` / `diagnose_the_age.py` exist but haven't been reported as run — confirm results

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
| Epicurean Magazine | Not yet tested — worth a diagnostic |

---

## 7. Physical Transcription — Newspapers and Magazines

For publications not in Trove, physical copies must be sourced and scanned. Follow the OCR workflow in `CLAUDE.md` (`scripts/ocr-prep.sh` → transcribe → `scripts/ocr-cleanup.sh`).

**Priority targets:**
- [ ] The Sun News-Pictorial — `A Place in the Sun` column, 1958–1978 (large body of work; consider sampling key pieces first)
- [ ] The Herald — regular contributions post-1978
- [ ] The Courier-Mail — `Day by Day` column (pre-1958 period)
- [ ] The Age — regular columnist, post-1982
- [ ] Epicurean Magazine — mentioned on homepage, extent unknown
- [ ] Australian Gourmet Traveller — extent unknown

**Sources:** State Library Victoria (ProQuest newspaper archive) for Herald/Sun/Age; personal and family clipping archives.

---

## 8. Site — Technical

- [ ] **Bulletin collection path conflict** — resolve `src/bulletin/` vs `src/articles/bulletin/` per §5 data issue, before it spreads further
- [ ] **Search** — replace Google Custom Search Engine with Pagefind (free, static-site-native, no external dependency). Implementation: dedicated search page, navbar trigger, results showing title/excerpt/publication/date; retain existing tag/keyword cloud beneath results
- [ ] **Theme** — evaluate migration from 11straps/Bootstrap 5 to Eleventy Excellent (fluid typography, modern CSS, Eleventy v3, built-in tag navigation). Decision pending — site is functional as-is; migration is cosmetic/structural
- [ ] **Epicurean Magazine** — run Trove diagnostic to check if digitised (copy `diagnose_walkabout.py`, update publication name/title variants)
- [ ] **`triage.py`** — add `--publication` flag to support Walkabout and future publications
- [ ] **Annual Trove review** — per data agreement, review published articles against current Trove availability annually (next due: before 31 December 2026)
- [ ] **Data agreement expiry** — Trove API data agreement expires 31 December 2026; raw API results (JSON/CSV in `trove/output/`) must be deleted by then unless renewed
- [ ] **Stray files to clean up:** `src/books/my-life-with-the-demon/a-brand-new-commonwealth.ini` (misplaced planning file, see §4); empty `src/books/ratbags/Scans/Chapter 4 - Edward William Cole/` folder (chapter already complete)

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
- [x] Ratbags — chapters 1–13 of 26 live (foreword, introduction, 11 profiles)
- [x] Ratbags — chapters 12–14 (Frank Thring, Lillian Frank, Xavier Herbert) scanned and OCR'd, awaiting transcription
- [x] Ratbags — 10 further chapters have empty scan folders created, awaiting physical scanning
- [x] Books fully live on site: No Brains At All, Supporting a Column, My Life with the Demon, The Australian Upper Crust Book (as scoped)
- [x] Books partially live: A Day in the Life of Australia (8 of 258 known entries + 11 drafted), Wowsers (2 of 10 chapters), Ratbags (13 of 26 chapters)
