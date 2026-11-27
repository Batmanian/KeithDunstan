# Trove API Scripts — Keith Dunstan Archive

This folder contains Python scripts for retrieving Keith Dunstan's articles
from the National Library of Australia's Trove database via the Trove API v3.

These scripts are **CMS-agnostic** — they produce `.md` files that can be
used with any static site generator. The current site (keithdunstan.org) uses
Eleventy, but the output format here is not coupled to it.

---

## Context for Claude Code

- **Project**: Digital archive of Keith Dunstan (1925–2013), Australian journalist
- **Live site**: keithdunstan.org
- **Repo**: github.com/JackDunstan/KeithDunstan
- **Content target**: `vault/articles/[publication-slug]/` — the site's `vault/` git submodule (an Obsidian vault), the authoritative content source, **not** `src/articles/` (which now holds only symlinks into `vault/`; see `../CLAUDE.md`'s "Content authority" section). After moving files there, run `npm run link:vault` in the repo root to symlink them into `src/`.
- **Frontmatter rules**: See `../CLAUDE.md` — tags are granular proper nouns only
- **Attribution rule**: Every article must link back to its Trove source URL
- **Keith's pen name in The Bulletin**: 'Batman' — column titled 'Batman's [topic]'
- **The Bulletin Bib ID**: 1085805 | NLA object: nla.obj-68375465 | Run: 1880–1984

When helping with these scripts, always:
- Preserve the Trove source URL in the output markdown
- Keep `.env` out of git (API key must never be committed)
- Write output to `trove/output/` not directly to `src/`
- Follow the prose conventions in `../CLAUDE.md` when editing article text

---

## Setup

### 1. Python environment

```bash
cd trove
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. API key

```bash
cp .env.example .env
```

Open `.env` and replace `your_api_key_here` with your Trove API key.
The `.env` file is gitignored — never commit it.

### 3. Create output folder structure (once)

```bash
python setup.py
```

This creates `output/<publication>/stubs/`, `transcribed/`, and `rejected/`
for all known publications. Safe to re-run.

---

## Workflow

### Download article scans for later transcription

`python3 -u trove/download_images.py` (from the repository root) downloads the
page images linked by Bulletin stubs within the saved scope, keeping the stubs unchanged. At the
archive owner's request, these review copies live in
`src/trove-scans/bulletin/<year>/<stub-name>/`, with a `source.json` recording
the title, byline, source URLs, rights statement and image checksums. This folder
is gitignored and excluded from Eleventy. No site build is needed.

The saved scope in `trove/image-download-config.json` is currently
`"before": null`: download all remaining Bulletin stubs with no date cutoff.
All 1,469 stubs are in scope, including the 280 previously deferred from 1978
onwards. Completed downloads and deleted scans remain skipped.
To impose a cutoff in future, set `before` to an exclusive ISO date such as
`"1978-01-01"` and restart the same command.
The worker reads this configuration at startup, so stop and restart it to apply
a changed cutoff. `progress.json` records the active cutoff and batch counts;
`images_downloaded` is cumulative across runs.

Image requests are spaced at least 60 seconds apart, including failed requests
and restarts. Successful downloads are recorded permanently in
`trove/download-history.json`, outside the scan folders and included in the
project's versionable files. History is saved after every image and records the
stub, downloaded pages and completion status. Existing logs and sidecars are
used to recover earlier downloads, including folders already deleted.

**Deleting scans is a review decision.** If a previously downloaded image or
article folder is removed, that stub becomes `skipped_deleted`; its files will
not be recreated and any remaining pages for it will not be fetched. This check
also happens after the one-minute wait, so folders deleted while the worker is
running stay deleted. Keep the history file when cleaning up scans. Stub files
are never altered or removed by the downloader.

Completed downloads are skipped on resume. Whole-issue links that
do not identify an article are marked `needs_review`; bylines are recorded for
later triage, not treated as proof of authorship. HTTP 403/429, five consecutive
request failures, or less than 2 GiB free disk space pause the run for review.

The background run's log is `trove/output/image-download/download.log`, and its
counts and status are in `progress.json` beside it. Create an empty
`trove/output/image-download/STOP` file to stop gracefully. Remove that file and
run the command again to resume. The computer must remain awake and online for
downloads to progress. A reboot requires restarting the command.

### Fetch and triage stubs

Run the scripts in order:

```bash
# Pass 1 — Batman column articles (primary target)
python fetch_batman.py

# Pass 2 — Keith Dunstan byline articles
python fetch_byline.py

# Merge CSV logs and flag duplicate Trove IDs
python deduplicate.py

# Delete flagged duplicates from stubs/
python remove_duplicates.py

# Sort any legacy loose stubs into publication/year folders for scan sourcing.
# New fetches are written into these year folders automatically.
python sort_stubs_by_year.py bulletin

# Interactive triage — opens each article in browser, move to transcribed/ or rejected/
python triage.py
```

Then:

1. Open `output/master_results.csv` to review what was found
2. Complete the frontmatter (`summary`, `tags`) on files in `transcribed/` per `../CLAUDE.md`
3. Move approved files from `output/<publication>/transcribed/` to `vault/articles/<publication-slug>/` (the vault submodule, not `src/articles/`)
4. Run `npm run link:vault` in the repo root to symlink the new files into `src/`
5. Commit and push in **both** repos: the vault submodule first, then the site repo (which needs its submodule pointer updated) — `git add`, `git commit`, `git push` in each. Netlify builds automatically once the site repo is pushed.

For manually sourced scans, retain the corresponding stub whenever the article
is deferred, incomplete, rejected from the current transcription batch or still
needs attribution/date checking. Remove a stub and its source scan only after a
complete transcription has been visually verified and published in
`vault/articles/<publication-slug>/`. Track deferred and incomplete scans in
`../todo.md` so they remain visible sourcing tasks.

---

## Deep search across all of Trove (`deep_search.py`)

The `fetch_*.py` scripts each target one magazine. `deep_search.py` searches
**every** Trove title for Keith's writing, with a strategy built around where
Trove actually has digitised text:

| Where | Why it matters |
|---|---|
| Newspapers to ~1954 (Herald, Sun News-Pictorial, Courier-Mail, Advertiser, Newcastle Morning Herald...) | Keith's 1946–54 HWT years, incl. New York (1949–52) and London (1952–54) correspondent copy syndicated across HWT-linked papers. Earlier diagnostics only probed 1960–2005 and missed all of this. |
| The Canberra Times (digitised to 1995) | Syndicated later columns (1960s–80s). |
| Magazines (Home Beautiful, Pedal Power / Bicycle Victoria, Hemisphere...) | Titles beyond Bulletin/Walkabout carrying his byline. |
| Catalogue "Article" records (`category=book`, `l-format=Article`) | Indexed but **not digitised** pieces (Good Weekend, Bulletin post-1984...) — exact title/date leads for physical sourcing. |

```bash
python deep_search.py survey             # facet counts per lane (~7 requests)
python deep_search.py harvest            # resumable; raw JSONL in output/deep_search/raw/
python deep_search.py score              # no API: score, dedupe, cluster → candidates.csv
python deep_search.py gapfill --dry-run  # list missing weeks of recurring columns
python deep_search.py gapfill            # one targeted query per missing issue
python deep_search.py score              # re-rank including gap-fill results
python deep_search.py stubs --min-score 0.8
```

- **Lanes** (search queries) live in the `LANES` list: exact name, OCR variants
  (`Dunslan`, `Duns tan`, `Keifh`...), correspondent datelines, known column
  titles, magazines, catalogue records. Add new lanes as leads appear.
- **Scoring** estimates whether Keith *wrote* the piece: column title/byline in
  the heading (0.97) → "By/From Keith Dunstan" in opening lines (0.92) → name at
  top (0.7) → overseas dateline in correspondent years (0.65) → mention only
  (0.3). Pre-1943 hits (another Keith Dunstan; he was born 1925), "Mr Keith
  Dunstan" notices, St. Dunstan's, advertising and gazettes are pushed down.
- **Dedupe** skips anything whose Trove ID or (fuzzy title + date) already
  appears in `vault/articles/`, `trove/output/**` or any `output/*_results.csv`.
- **Syndication clustering** groups the same piece across papers; the Herald copy
  is canonical and the others are listed as alternates, which are useful for
  cross-checking bad OCR while transcribing.
- **Gap-fill** detects recurring columns (e.g. *Keith Dunstan's Film World*,
  Saturdays in The Herald 1950–52) and queries each missing week directly,
  catching issues where OCR destroyed the byline.
- **Rate limit:** sliding window capped at `--rpm` (default 150, hard cap 190 of
  the 200/min allowance); honours `Retry-After`; stops after 5 consecutive
  failures. In practice the limit is never reached. Full-text pages take
  40–90s for Trove to serve, so pages are kept at 50 records and the request
  timeout is 180s. Every request is logged to `output/deep_search/requests.log`.
- **Stubs** land in `output/<publication-slug>/stubs/<year>/` with raw OCR and
  syndicated alternates attached, and nothing goes into `vault/`. Confidence scores
  are heuristic, so check the byline on the scan before transcribing.
- **Scans:** `python3 -u download_scans.py` (system python3, uses Pillow for crops)
  downloads scans for every deep-search stub into
  `src/trove-scans/<publication>/<year>/<stub-name>/`, following the same rules as
  `download_images.py`: 60s between image requests, robots.txt checked (it never
  touches the disallowed `/newspaper/rendition` service), `source.json` sidecars,
  permanent history in `trove/download-history-deep.json`, and deleted scans are
  never re-fetched. Newspaper stubs get the full page (`page-NN-…jpg`, Trove level7,
  ~4800px) plus `article-NN.jpg` cropped from the article's zone coordinates.
  Catalogue-only stubs are skipped. Stop with `output/image-download-deep/STOP`;
  rerun to resume. It shares `download_images.py`'s lock so the two never run at
  once, and `download_images.py` ignores deep-search stubs.
- Raw results in `output/deep_search/` fall under the Trove data agreement
  (delete by 31 Dec 2026 unless renewed).

---

## Output structure

```
output/
  <publication>/
    stubs/        — raw output from fetch scripts; awaiting triage
    transcribed/  — confirmed Keith articles with full text added
    rejected/     — noise, family mentions, not written by Keith
```

---

## Output format

Each `.md` stub is written with minimal frontmatter:

```yaml
---
title: "Batman's Melbourne: This is a fine state to be in"
date: 1967-03-18
summary: "[Review and complete — article retrieved from Trove]"
categories:
  - The Bulletin
tags: []
---
```

Before moving to `vault/articles/bulletin/`, you must:
- Write a proper `summary` (one or two sentences, factual, third person)
- Add `tags` (5–15 granular proper nouns per `../CLAUDE.md`)
- Review the article text for OCR errors

---

## Script reference

| Script | Purpose |
|--------|---------|
| `setup.py` | Creates output folder structure (run once after cloning) |
| `fetch_batman.py` | Pass 1: searches for Batman column variants |
| `fetch_byline.py` | Pass 2: searches for Keith Dunstan byline |
| `deduplicate.py` | Merges CSV logs, flags duplicate Trove IDs |
| `remove_duplicates.py` | Deletes flagged duplicates from stubs/ |
| `triage.py` | Interactive review: keep stub / transcribed / reject |
| `diagnose.py` | Tests Trove API connectivity and surfaces search parameters |
| `diagnose2.py` | Finds correct response structure and category for The Bulletin |
| `deep_search.py` | Cross-publication deep search: survey, harvest, score, gap-fill, stubs (see above) |
| `review_articles.py` | Local review viewer (http://localhost:5051): scan beside editable markdown for `status: for review` articles in the vault; "Approve & publish" makes them live |
| `download_scans.py` | Downloads scans for deep-search stubs (newspaper pages + article crops, magazine pages) into `src/trove-scans/<publication>/<year>/<stub>/` |
| `deep_search.py` | Cross-publication deep search: survey, harvest, score, gap-fill, stubs (see above) |
| `download_scans.py` | Downloads scans for deep-search stubs (newspaper pages + article crops, magazine pages) into `src/trove-scans/<publication>/<year>/<stub>/` |

### triage.py commands

```
k  — keep as stub (leave in stubs/, revisit later)
t  — transcribed (move to transcribed/ — article confirmed, full text added)
r  — reject (move to rejected/ — noise, family mention, not by Keith)
q  — quit and save progress
```

Progress is saved to `output/triage_progress.txt` — safe to quit and resume.

```bash
python triage.py                  # start or resume from last position
python triage.py --from-start     # restart from the beginning
python triage.py --rejected-only  # re-review files already in rejected/
```

### Search terms used

**fetch_batman.py**
- `"Batman's"`
- `"Batman in the Bulletin"`
- `"Batmans Melbourne"`
- `"Batmans Sydney"`
- `"Batmans Australia"`

**fetch_byline.py**
- `"Keith Dunstan"`

Add new terms directly to the `SEARCH_TERMS` list in each script.

---

## Trove API notes

- **API version**: v3 (`https://api.trove.nla.gov.au/v3/result`)
- **Rate limit**: 200 calls/minute (per data agreement)
- **Pagination**: Scripts use `nextStart` cursor — safe to run on large result sets
- **Full text**: Requested via `include=articleText` — OCR quality varies by issue
- **Re-running**: Scripts skip files already present in `output/` — safe to re-run

### Useful Trove API parameters for future queries

```
category=magazine
l-title=The Bulletin
l-artType=article
include=articleText
bulkHarvest=true
n=100
```

For other publications, change `l-title` to the publication name as it appears in Trove.

---

## Adding a new publication

1. Duplicate `fetch_batman.py` or `fetch_byline.py`
2. Update `SEARCH_TERMS`, `DATE_FROM`, `DATE_TO`, and `l-title` parameter
3. Update the CSV log filename
4. Add the new slug to the `PUBLICATIONS` list in `setup.py` and re-run it
5. Run fetch and triage scripts as normal
6. Move approved files to `vault/articles/[publication-slug]/`, then run `npm run link:vault` in the repo root

---

## Troubleshooting

**`TROVE_API_KEY not set`**
→ You haven't created `.env`. Run `cp .env.example .env` and add your key.

**Empty results**
→ Check the search term spelling. Try a broader term first.
→ Verify the publication title matches Trove's exact title string.

**`articleText` missing or garbled**
→ Some issues are not fully OCR'd in Trove. Visit the Trove URL directly to transcribe manually.

**Rate limit errors (HTTP 429)**
→ The `time.sleep(0.5)` between pages should prevent this. If it persists, increase the sleep value.

**`output/` folders don't exist**
→ Run `python setup.py` to create the folder structure.
