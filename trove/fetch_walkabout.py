"""
fetch_walkabout.py
------------------
Fetch Keith Dunstan articles from Walkabout Magazine via the Trove API v3.

Walkabout is indexed in Trove under:
  category:     magazine
  response key: work
  isPartOf:     "Walkabout."
  l-title:      "Walkabout"  (server-side filter — works cleanly)

Keith wrote under his real name. No pen name.
Magazine ran 1934–1974; Keith's contributions suspected from 1960s onwards.

Writes one .md stub per article to trove/output/walkabout/stubs/.
Skips articles already present anywhere in output/walkabout/ (safe to re-run).

Usage:
    python fetch_walkabout.py

Output:
    trove/output/walkabout/stubs/<date>-<slug>.md
    trove/output/fetch_walkabout_results.csv
"""

import os
import re
import csv
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TROVE_API_KEY")
if not API_KEY:
    raise SystemExit("ERROR: TROVE_API_KEY not set. Copy .env.example to .env and add your key.")

BASE_DIR    = os.path.dirname(__file__)
OUTPUT_DIR  = os.path.join(BASE_DIR, "output")
STUBS_DIR   = os.path.join(OUTPUT_DIR, "walkabout", "stubs")
os.makedirs(STUBS_DIR, exist_ok=True)

WALKABOUT_DIRS = [
    os.path.join(OUTPUT_DIR, "walkabout", "stubs"),
    os.path.join(OUTPUT_DIR, "walkabout", "transcribed"),
    os.path.join(OUTPUT_DIR, "walkabout", "rejected"),
]

SEARCH_TERMS = [
    "Keith Dunstan",
]

DATE_FROM = "1960-01-01"
DATE_TO   = "1974-12-31"   # Walkabout ceased publication 1974

BASE_URL = "https://api.trove.nla.gov.au/v3/result"

PARAMS_BASE = {
    "key":      API_KEY,
    "category": "magazine",
    "encoding": "json",
    "l-title":  "Walkabout",   # server-side filter — confirmed working
    "n":        100,
}

MONTHS = {
    "january": "01", "february": "02", "march": "03", "april": "04",
    "may": "05", "june": "06", "july": "07", "august": "08",
    "september": "09", "october": "10", "november": "11", "december": "12",
}


def extract_date_from_title(title):
    """
    Extract ISO date and clean title from a Trove title string.
    e.g. "BEEF BOOM IN TOMBSTONE TERRITORY (1 October 1968)"
      -> ("1968-10-01", "BEEF BOOM IN TOMBSTONE TERRITORY")
    """
    match = re.search(r'\((\d{1,2})\s+([A-Za-z]+)\s+(\d{4})\)\s*$', title.strip())
    if match:
        day, month_str, year = match.groups()
        month = MONTHS.get(month_str.lower())
        if month:
            return f"{year}-{month}-{int(day):02d}", title[:match.start()].strip()
    return "", title.strip()


def is_walkabout(work):
    for part in work.get("isPartOf", []):
        if "walkabout" in part.get("value", "").lower():
            return True
    return False


def file_exists_anywhere(filename):
    return any(os.path.exists(os.path.join(d, filename)) for d in WALKABOUT_DIRS)


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[''']", "", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")[:80]


def get_fulltext_url(work):
    for ident in work.get("identifier", []):
        if ident.get("linktype") == "fulltext":
            return ident.get("value", "")
    return work.get("troveUrl", "")


def build_markdown(work):
    raw_title         = work.get("title", "Untitled").strip()
    date, clean_title = extract_date_from_title(raw_title)

    # Walkabout titles often include "KEITH DUNSTAN describes" as a prefix —
    # strip it for a cleaner display title while preserving the actual article name
    clean_title = re.sub(
        r'^KEITH DUNSTAN\s+(?:describes|writes about|on|reports on|reports)\s+',
        '', clean_title, flags=re.IGNORECASE
    ).strip()

    trove_url    = work.get("troveUrl", "")
    full_url     = get_fulltext_url(work)
    snippets     = work.get("snippet", [])
    snippet_text = " ".join(snippets) if snippets else ""
    snippet_text = re.sub(r"<[^>]+>", " ", snippet_text)
    snippet_text = re.sub(r"\s+", " ", snippet_text).strip()
    issue_date   = date or work.get("issued", "unknown date")

    return f"""---
title: "{clean_title}"
date: {date}
summary: "First published in Walkabout Magazine, {issue_date}. [Stub — not yet transcribed]"
categories:
- Walkabout Magazine
tags:
---

{f'> {snippet_text}' if snippet_text else ''}

[Full article text not yet transcribed. Visit the Trove link below to read and transcribe, then move this file to `src/posts/walkabout-magazine/`.]

<hr>

*Source: [{clean_title}]({full_url or trove_url}), Walkabout Magazine, {issue_date}. Retrieved via the National Library of Australia's Trove database.*
""".strip()


def fetch_works(search_term):
    works  = []
    params = {
        **PARAMS_BASE,
        "q": f'{search_term} date:[{DATE_FROM} TO {DATE_TO}]',
        "s": "*",
    }
    page = 1

    while True:
        print(f"  Fetching page {page} for: {search_term!r}")
        try:
            resp = requests.get(BASE_URL, params=params, timeout=30)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  ERROR: {e}")
            break

        records        = resp.json().get("category", [{}])[0].get("records", {})
        items          = records.get("work", [])
        walkabout_items = [w for w in items if is_walkabout(w)]
        works.extend(walkabout_items)
        print(f"  Page {page}: {len(items)} total, {len(walkabout_items)} from Walkabout (running total: {len(works)})")

        next_start = records.get("nextStart")
        if not next_start or len(items) < params["n"]:
            break
        params["s"] = next_start
        page += 1
        time.sleep(0.5)

    return works


def main():
    all_works = {}
    log_rows  = []

    for term in SEARCH_TERMS:
        print(f"\nSearching for: {term!r}")
        for work in fetch_works(term):
            wid = work.get("id", "")
            if wid and wid not in all_works:
                all_works[wid] = work

    print(f"\nTotal unique Walkabout works found: {len(all_works)}")

    for wid, work in all_works.items():
        raw_title         = work.get("title", "Untitled").strip()
        date, clean_title = extract_date_from_title(raw_title)

        clean_title = re.sub(
            r'^KEITH DUNSTAN\s+(?:describes|writes about|on|reports on|reports)\s+',
            '', clean_title, flags=re.IGNORECASE
        ).strip()

        trove_url = work.get("troveUrl", "")
        full_url  = get_fulltext_url(work)
        slug      = slugify(clean_title) or slugify(wid)
        filename  = f"{date}-{slug}.md" if date else f"{work.get('issued', 'undated')}-{slug}.md"

        if file_exists_anywhere(filename):
            print(f"  SKIP (exists): {filename}")
            log_rows.append([wid, clean_title, date, trove_url, full_url, filename, "skipped"])
            continue

        with open(os.path.join(STUBS_DIR, filename), "w", encoding="utf-8") as f:
            f.write(build_markdown(work))

        print(f"  WRITTEN: walkabout/stubs/{filename}")
        log_rows.append([wid, clean_title, date, trove_url, full_url, filename, "written"])

    csv_path = os.path.join(OUTPUT_DIR, "fetch_walkabout_results.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(
            [["trove_id", "title", "date", "trove_url", "fulltext_url", "filename", "status"]] + log_rows
        )

    print(f"\nDone. Stubs: output/walkabout/stubs/  |  Log: output/fetch_walkabout_results.csv")


if __name__ == "__main__":
    main()
