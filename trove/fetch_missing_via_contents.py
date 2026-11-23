#!/usr/bin/env python3
"""
fetch_missing_via_contents.py
-----------------------------
For a given year, find edition dates where a bulletin-contents stub exists
but no batman article stub does. For each such date, load the Trove viewer
page for that issue, find the Batman's Melbourne article in the issue
metadata, and write a stub.

No Trove API key required — uses the public Trove viewer HTML.

Usage:
    python3 trove/fetch_missing_via_contents.py 1978
"""

import json
import re
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
AGENT = "KeithDunstanArchive/1.0 (+https://keithdunstan.org)"

BULLETIN_DIRS = [
    ROOT / "trove/output/bulletin/stubs",
    ROOT / "trove/output/bulletin/transcribed",
    ROOT / "trove/output/bulletin/rejected",
]

MONTHS = {
    "january": "01", "february": "02", "march": "03", "april": "04",
    "may": "05", "june": "06", "july": "07", "august": "08",
    "september": "09", "october": "10", "november": "11", "december": "12",
}


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[''']", "", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")[:80]


def fetch_html(url):
    req = Request(url, headers={"User-Agent": AGENT})
    with urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def extract_date_from_title(title):
    match = re.search(r'\((\d{1,2})\s+([A-Za-z]+)\s+(\d{4})\)\s*$', title.strip())
    if match:
        day, month_str, year = match.groups()
        month = MONTHS.get(month_str.lower())
        if month:
            return f"{year}-{month}-{int(day):02d}", title[:match.start()].strip()
    return "", title.strip()


def get_batman_articles_in_issue(contents_url):
    """Load the Trove viewer page for a contents article, find all Batman articles in that issue."""
    html = fetch_html(contents_url)
    match = re.search(r"var work\s*=\s*JSON.parse\(JSON.stringify\(", html)
    if not match:
        raise ValueError("Trove viewer metadata not found")
    work, _ = json.JSONDecoder().raw_decode(html[match.end():])
    articles = work.get("children", {}).get("article", [])
    issue_date = work.get("issueDate", "")
    batman_articles = [
        a for a in articles
        if re.search(r"batman", a.get("title", ""), re.IGNORECASE)
    ]
    return issue_date, batman_articles, work


def article_fulltext_url(article):
    for ident in article.get("identifier", []):
        if ident.get("linktype") == "fulltext":
            return ident.get("value", "")
    pid = article.get("pid", "")
    return f"https://nla.gov.au/{pid}" if pid else ""


def file_exists_anywhere(filename, year):
    for base in BULLETIN_DIRS:
        if (base / year / filename).exists():
            return True
    return False


def build_stub(date, clean_title, full_url, trove_url, snippet):
    issue_date = date
    snippet_line = f"> {snippet}" if snippet else ""
    return f"""---
title: "{clean_title}"
date: {date}
summary: "First published in The Bulletin, {issue_date}. [Stub — not yet transcribed]"
categories:
- The Bulletin
tags:
---

{snippet_line}

[Full article text not yet transcribed. Visit the Trove link below to read and transcribe, then move this file to `src/articles/bulletin/`.]

<hr>

*Source: [{clean_title}]({full_url or trove_url}), The Bulletin, {issue_date}. Retrieved via the National Library of Australia's Trove database.*
""".strip()


def find_missing_dates(year):
    contents_dates = {}  # date -> stub path
    batman_dates = set()

    for base in BULLETIN_DIRS:
        d = base / year
        if not d.exists():
            continue
        for f in sorted(d.glob("*.md")):
            m = re.match(r"(\d{4}-\d{2}-\d{2})", f.stem)
            if not m:
                continue
            date = m.group(1)
            if re.search(r"\bcontents\b", f.stem):
                contents_dates[date] = f
            elif "batman" in f.stem:
                batman_dates.add(date)

    missing = {d: p for d, p in contents_dates.items() if d not in batman_dates}
    return missing


def main():
    year = sys.argv[1] if len(sys.argv) > 1 else "1978"
    stubs_dir = ROOT / "trove/output/bulletin/stubs" / year
    stubs_dir.mkdir(parents=True, exist_ok=True)

    missing = find_missing_dates(year)
    print(f"{year}: {len(missing)} editions missing a Batman article")

    for date in sorted(missing):
        contents_path = missing[date]
        url_match = re.search(r"https://nla\.gov\.au/nla\.obj-\d+", contents_path.read_text())
        if not url_match:
            print(f"  SKIP {date}: no URL in contents stub")
            continue

        contents_url = url_match.group()
        print(f"\n  {date}: loading issue from {contents_url}")
        try:
            issue_date, batman_articles, work = get_batman_articles_in_issue(contents_url)
        except Exception as e:
            print(f"  ERROR fetching issue: {e}")
            time.sleep(2)
            continue

        if not batman_articles:
            print(f"  No batman article found in issue metadata")
            time.sleep(2)
            continue

        for article in batman_articles:
            raw_title = article.get("title", "").strip()
            extracted_date, clean_title = extract_date_from_title(raw_title)
            if not extracted_date:
                extracted_date = date
            if not clean_title:
                clean_title = raw_title

            pid = article.get("pid", "")
            full_url = article_fulltext_url(article)
            trove_url = f"https://nla.gov.au/{pid}" if pid else full_url

            snippets = article.get("snippet", [])
            snippet = " ".join(snippets) if snippets else ""
            snippet = re.sub(r"<[^>]+>", " ", snippet)
            snippet = re.sub(r"\s+", " ", snippet).strip()

            slug = slugify(clean_title) or slugify(pid)
            filename = f"{extracted_date}-{slug}.md"

            if file_exists_anywhere(filename, year):
                print(f"  SKIP (exists): {filename}")
                continue

            stub = build_stub(extracted_date, clean_title, full_url, trove_url, snippet)
            out_path = stubs_dir / filename
            out_path.write_text(stub)
            print(f"  WRITTEN: {filename}")
            print(f"    title: {clean_title}")
            print(f"    url:   {trove_url}")

        time.sleep(2)

    print(f"\nDone.")


if __name__ == "__main__":
    main()
