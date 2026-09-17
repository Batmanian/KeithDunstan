#!/usr/bin/env python3
"""
Create stub .md files in vault/articles/the-age/YEAR/ for each PDF scan
that contains a Keith Dunstan byline.

Usage (run from repo root):
    python3 scripts/create-age-1986-stubs.py [--year YYYY] [--scans-dir PATH] [--dry-run]

Defaults to 1986 with scans in src/articles/the-age/1986/scans/.
The script auto-detects PDFs directly in the year directory too
(i.e. src/articles/the-age/1985/ where PDFs sit at the top level).
"""

import os
import re
import sys
import subprocess
from datetime import datetime
from pathlib import Path

DRY_RUN = "--dry-run" in sys.argv

# Parse --year and --scans-dir arguments
_args = sys.argv[1:]
_year = "1986"
_scans_dir = None
for i, a in enumerate(_args):
    if a == "--year" and i + 1 < len(_args):
        _year = _args[i + 1]
    if a == "--scans-dir" and i + 1 < len(_args):
        _scans_dir = Path(_args[i + 1])

if _scans_dir is None:
    # Auto-detect: prefer year/scans/ subdir (if it has PDFs), fall back to year/ directly
    _candidate_sub = Path(f"src/articles/the-age/{_year}/scans")
    _candidate_top = Path(f"src/articles/the-age/{_year}")
    _has_sub_pdfs = _candidate_sub.exists() and any(_candidate_sub.glob("*.pdf"))
    _scans_dir = _candidate_sub if _has_sub_pdfs else _candidate_top

SCANS_DIR = _scans_dir
VAULT_OUT = Path(f"vault/articles/the-age/{_year}")

# Month name to number
MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
}

# Publication detection patterns
PUB_PATTERNS = [
    (re.compile(r"Sydney Morning Herald", re.I), "The Sydney Morning Herald"),
    (re.compile(r"THE AGE|The Age", re.I),        "The Age"),
    (re.compile(r"The Australian",   re.I),        "The Australian"),
    (re.compile(r"Good Weekend",     re.I),        "The Age — Good Weekend"),
]

def parse_date_from_filename(fname: str):
    """Extract date from filename like 'April_1,_1986_(Page_11_of_68).pdf'."""
    m = re.match(r"([A-Za-z]+)_(\d+),_(\d{4})", fname)
    if not m:
        return None
    month_name, day, year = m.group(1).lower(), int(m.group(2)), int(m.group(3))
    month = MONTHS.get(month_name)
    if not month:
        return None
    return datetime(year, month, day).date()

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text)
    return text.strip("-")

def extract_text(pdf_path: Path) -> str:
    try:
        result = subprocess.run(
            ["pdftotext", str(pdf_path), "-"],
            capture_output=True, text=True, timeout=15
        )
        return result.stdout
    except Exception:
        return ""

def has_kd_byline(text: str) -> bool:
    return bool(re.search(r"KEITH DUNSTAN", text))

def detect_publication(text: str) -> str:
    for pattern, pub in PUB_PATTERNS:
        if pattern.search(text):
            return pub
    return "The Age"  # default

def extract_title_candidate(text: str) -> str:
    """
    Heuristic: look for ALL-CAPS headline lines near the KEITH DUNSTAN byline.
    Newspaper headlines set in bold display type appear in pdftotext as short
    all-caps (or mixed-case) lines of 1–8 words. Only accept lines that pass
    strict quality checks; fall back to "" if nothing clean is found.
    """
    lines = text.split("\n")
    kd_pos = None
    for i, line in enumerate(lines):
        if "KEITH DUNSTAN" in line:
            kd_pos = i
            break
    if kd_pos is None:
        return ""

    # Scan a window before the byline for headline candidates
    window = lines[max(0, kd_pos - 80): kd_pos]

    def is_headline_line(s: str) -> bool:
        """Return True only for lines that look like display headline text."""
        if not s or len(s) < 3:
            return False
        words = s.split()
        if not (1 <= len(words) <= 9):
            return False
        if len(s) > 70:
            return False
        # Must be mostly alphabetic
        alpha_ratio = sum(1 for c in s if c.isalpha()) / len(s)
        if alpha_ratio < 0.55:
            return False
        # No non-ASCII
        if re.search(r"[^\x20-\x7E]", s):
            return False
        # Skip common non-headline patterns
        skip_patterns = [
            r"^By ", r"^\d+$", r"^Page \d", r"^THE AGE,", r"^The Age,",
            r"Sydney Morning Herald", r"^Copyright", r"^Reproduced",
            r"\bsaid\b", r"\bsays\b", r"\bwas\b", r"\bwere\b", r"\bhas\b",
            r"\bhave\b", r"\bwould\b", r"\bcould\b", r"\bwill\b",
        ]
        for pat in skip_patterns:
            if re.search(pat, s):
                return False
        # Strong preference: must be ALL CAPS or start with a capital
        if s[0].islower():
            return False
        return True

    # Collect headline candidates; prefer all-caps runs
    candidates = [l.strip() for l in window if is_headline_line(l.strip())]
    if not candidates:
        return ""

    # Score: all-caps lines score higher
    def score(s):
        words = s.split()
        caps_words = sum(1 for w in words if w.isupper() or (w[0].isupper() and len(w) > 1))
        return caps_words / len(words)

    candidates.sort(key=score, reverse=True)
    best = candidates[0]

    # Only accept if it's clearly a headline (all-caps ratio > 0.6 or very short)
    if score(best) < 0.6 and len(best.split()) > 3:
        return ""

    return best

def create_stub(pdf_path: Path, date, pub: str, slug: str, out_path: Path):
    date_str = date.strftime("%Y-%m-%d")

    title_for_frontmatter = f"[Stub — {date_str}]"
    summary = "[Stub — not yet transcribed]"

    content = f"""---
eleventyExcludeFromCollections: true
title: "{title_for_frontmatter}"
date: {date_str}
summary: "{summary}"
categories:
- {pub}
tags:
source_scan: {pdf_path.name}
---

[Stub — not yet transcribed. Open `{SCANS_DIR}/{pdf_path.name}` to transcribe.]
"""
    if DRY_RUN:
        print(f"  DRY RUN → {out_path}")
        print(f"    title: {title_for_frontmatter}")
        print(f"    pub:   {pub}")
    else:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content, encoding="utf-8")
        print(f"  created → {out_path.name}")

def main():
    if not SCANS_DIR.exists():
        print(f"ERROR: {SCANS_DIR} not found — run from repo root.")
        sys.exit(1)

    pdf_files = sorted(SCANS_DIR.glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDFs in {SCANS_DIR}")
    print()

    # Track slugs used to handle duplicates (same date, multiple files)
    used_slugs = {}
    skipped = []
    created = []
    no_kd = []

    for pdf in pdf_files:
        date = parse_date_from_filename(pdf.name)
        if not date:
            print(f"  WARN: can't parse date from {pdf.name}")
            skipped.append(pdf.name)
            continue

        text = extract_text(pdf)
        if not has_kd_byline(text):
            no_kd.append(pdf.name)
            continue

        pub = detect_publication(text)

        date_str = date.strftime("%Y-%m-%d")
        base_slug = date_str

        # Handle multiple KD articles on same date by appending suffix
        count = used_slugs.get(base_slug, 0)
        used_slugs[base_slug] = count + 1
        slug = base_slug if count == 0 else f"{base_slug}-{count + 1}"

        out_path = VAULT_OUT / f"{slug}.md"

        # Don't overwrite existing vault files
        if out_path.exists():
            print(f"  SKIP (exists): {out_path.name}")
            skipped.append(pdf.name)
            continue

        create_stub(pdf, date, pub, slug, out_path)
        created.append(slug)

    print()
    print("=" * 60)
    print(f"Created:  {len(created)} stubs")
    print(f"No KD:    {len(no_kd)} files (skipped)")
    print(f"Skipped:  {len(skipped)} files (date parse failed or already exist)")
    print()
    if not DRY_RUN:
        print("Next: run `npm run link:vault` to wire symlinks into src/")

if __name__ == "__main__":
    main()
