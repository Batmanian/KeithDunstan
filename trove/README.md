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
- **Content target**: `src/posts/[publication-slug]/` (after triage and manual review)
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

# Interactive triage — opens each article in browser, move to transcribed/ or rejected/
python triage.py
```

Then:

1. Open `output/master_results.csv` to review what was found
2. Complete the frontmatter (`summary`, `tags`) on files in `transcribed/` per `../CLAUDE.md`
3. Move approved files from `output/<publication>/transcribed/` to `src/posts/<publication-slug>/`
4. `git add`, `git commit`, `git push` — Netlify builds automatically

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

Before moving to `src/posts/bulletin/`, you must:
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
6. Move approved files to `src/posts/[publication-slug]/`

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
