# Todo — Keith Dunstan Archive

Tracking outstanding work across all active workstreams.
Last updated: May 2026.

---

## Trove API Pipeline

Scripts live in `trove/`. Run from within that directory with the `.venv` activated.

### Bulletin stubs — triage

1,613 stub `.md` files are in `trove/output/bulletin/stubs/` awaiting review.

- [ ] Run `python triage.py` to work through stubs one at a time
  - `k` — keep as stub (return later)
  - `t` — confirmed Keith article, full text added → moves to `transcribed/`
  - `r` — noise or family mention → moves to `rejected/`
  - `q` — quit and save progress (resumes where you left off)
- [ ] Move confirmed transcribed files from `trove/output/bulletin/transcribed/` to `src/posts/bulletin/`
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

~82 stubs in `trove/output/walkabout/stubs/` — a much more manageable set.

- [ ] Run `python triage.py` — note: currently triages bulletin/ only, needs update for walkabout
- [ ] Cross-reference against the 18 known articles listed on the site (`/articles/walkabout-magazine/`)
- [ ] Transcribe the 15 outstanding Walkabout articles (see section below)
- [ ] Move completed files to `src/posts/walkabout-magazine/`

### Trove scripts — maintenance

- [ ] Update `triage.py` to accept a `--publication` argument (e.g. `--publication walkabout`)
  so it can triage any publication's stubs, not just bulletin
- [ ] Update `trove/README.md` to reflect the publication folder structure

### Publications confirmed NOT in Trove (post-1954)

These require physical copies — see Physical Transcription section below.

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

## Walkabout Magazine — Outstanding Articles

15 of 18 known articles remain untranscribed. Source from Trove
(well digitised for this period), then transcribe via the Claude prompt in `CLAUDE.md`.
Save to `src/posts/walkabout-magazine/`.

- [ ] Paddy's Market to Luxury Hotel — `1962-07-01` — `paddys-market-to-luxury-hotel.md`
- [ ] Epicurean Melbourne — `1962-12-01` — `epicurean-melbourne.md`
- [ ] Freedom of Beach — `1963-01-01` — `freedom-of-beach.md`
- [ ] From Prickly Pear to Petroleum — `1963-07-01` — `from-prickly-pear-to-petroleum.md`
- [ ] Christmas Across the Continent — `1963-12-01` — `christmas-across-the-continent.md`
- [ ] Melbourne's Evergreen Exhibition — `1964-05-01` — `melbournes-evergreen-exhibition.md`
- [ ] Adventures of a Would-be Wine Snob — `1964-12-01` — `adventures-of-a-would-be-wine-snob.md`
- [ ] Battle of the Flowers — `1965-05-01` — `battle-of-the-flowers.md`
- [ ] Melbourne Cup Winners, Horses or Hats? — `1966-10-01` — `melbourne-cup-winners-horses-or-hats.md`
- [ ] 1966 and All That — `1966-12-01` — `1966-and-all-that.md`
- [ ] The Bikini - What's next? — `1968-01-01` — `the-bikini-whats-next.md`
- [ ] A Year of Anti-Football Protest — `1968-04-01` — `a-year-of-anti-football-protest.md`
- [ ] Beef Boom in Tombstone Territory — `1968-10-01` — `beef-boom-in-tombstone-territory.md`
- [ ] Collins Street Charm — `1968-12-01` — `collins-street-charm.md`
- [ ] Walkabout Profile — Dr. Jean Battersby — `1969-05-01` — `walkabout-profile-dr-jean-battersby.md`

**Workflow:**
1. Find issue on Trove: https://trove.nla.gov.au — search Walkabout Magazine by date
2. Copy or scan text
3. Upload to Claude with transcription prompt from `CLAUDE.md`
4. Save to `src/posts/walkabout-magazine/[filename].md`
5. `git add`, `git commit`, `git push`

---

## Books — Outstanding Transcription

Physical copies to scan (iPhone → Notes/Files → upload to Claude).
See `CLAUDE.md` for the full transcription prompt.

Books not yet started or incomplete — confirm against `src/posts/` before starting:

- [ ] Wowsers (1968)
- [ ] Knockers (1972)
- [ ] Sports (1973)
- [ ] Ratbags (1979) — partially done, check `src/posts/ratbags/`
- [ ] Saint Ned (1980)
- [ ] My Life with the Demon — check `src/posts/my-life-with-the-demon/`
- [ ] The Australian Upper Crust Book — check `src/posts/the-australian-uppercrust-book/`
- [ ] The Paddock That Grew (1962) — MCG history
- [ ] The Melbourne I Remember (2004)
- [ ] Moonee Ponds to Broadway (2006) — Barry Humphries study

---

## Physical Transcription — Newspapers and Magazines

For publications not in Trove, physical copies must be sourced and scanned.

**Priority targets:**
- [ ] The Sun News-Pictorial — `A Place in the Sun` column, 1958–1978 (daily column — large body of work, consider sampling key pieces first)
- [ ] The Herald — regular contributions post-1978
- [ ] The Courier-Mail — `Day by Day` column (pre-1958 period)
- [ ] The Age — regular columnist, post-1982
- [ ] Epicurean Magazine — mentioned on homepage, extent unknown
- [ ] Australian Gourmet Traveller — extent unknown

**Sources:**
- State Library Victoria (ProQuest newspaper archive) — best for Herald, Sun, Age
- Your personal collection of clippings
- Family archive

**Workflow:**
1. Scan physical copy using iPhone (Notes app, Files app, or Continuity Camera)
2. Upload scan to Claude with transcription prompt from `CLAUDE.md`
3. Save to `src/posts/[publication-slug]/[filename].md`
4. `git add`, `git commit`, `git push`

---

## Site — Technical

- [ ] **Search** — replace Google Custom Search Engine with Pagefind
  - Diagnostic prompt already prepared (see prior Claude sessions)
  - Pagefind is free, static-site-native, no external dependency
  - Implementation: dedicated search page, navbar trigger, results showing title/excerpt/publication/date
  - Existing tag/keyword cloud to be retained beneath results
- [ ] **Theme** — evaluate migration from 11straps/Bootstrap 5 to Eleventy Excellent
  - Eleventy Excellent: fluid typography, modern CSS, Eleventy v3, built-in tag navigation
  - Decision pending — site functional as-is, migration is cosmetic/structural
- [ ] **Epicurean Magazine** — run Trove diagnostic to check if digitised
  - Script: copy `diagnose_walkabout.py`, update publication name and title variants
- [ ] **`triage.py`** — add `--publication` flag to support walkabout and future publications
- [ ] **Annual Trove review** — per data agreement, review published articles against
  current Trove availability annually (next due: before 31 December 2026)
- [ ] **Data agreement expiry** — Trove API data agreement expires 31 December 2026
  - Raw API results (JSON/CSV in `trove/output/`) must be deleted by then
  - Renew agreement if ongoing access required

---

## Completed ✓

- [x] Trove API key obtained and configured
- [x] `trove/` folder structure created (11 publications × 3 status dirs)
- [x] `fetch_batman.py` — Batman column articles fetched (1,594 stubs)
- [x] `fetch_byline.py` — Keith Dunstan byline articles fetched (100 additional)
- [x] `deduplicate.py` — 81 duplicates identified and removed
- [x] `fetch_walkabout.py` — ~82 Walkabout stubs fetched
- [x] `triage.py` — interactive browser triage tool built
- [x] `remove_duplicates.py` — automated duplicate removal script built
- [x] `setup.py` — folder structure creation script built
- [x] Trove API data agreement submitted to NLA
- [x] Trove publication diagnostics run for all major publications
- [x] Batman's Melbourne (18 March 1967) — manually transcribed, ready to commit
- [x] Bulletin articles — 6 transcribed and live on site
- [x] Walkabout articles — 3 transcribed and live on site (Bird Watching, Rough-Riding, Summer Madness)
- [x] Books live on site: No Brains At All, Supporting a Column, A Day in the Life of Australia,
  Ratbags (partial), Wowsers (partial), The Australian Upper Crust Book (partial), My Life with the Demon (partial)
