"""
diagnose_the_age.py
-------------------
Diagnostic script to establish how The Age is indexed in Trove API v3.

The Age is a Melbourne broadsheet — likely in the newspaper category.
Keith Dunstan was a Herald journalist primarily but may have contributed
to or been covered by The Age across his career.

Tests:
  - Which category The Age sits in
  - The correct response key and l-title string
  - Whether Keith Dunstan articles are findable by byline

Usage:
    python diagnose_the_age.py
"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TROVE_API_KEY")
if not API_KEY:
    raise SystemExit("ERROR: TROVE_API_KEY not set.")

BASE_URL = "https://api.trove.nla.gov.au/v3/result"


def test(label, params, show_raw=False, raw_limit=3000):
    print(f"\n{'='*65}")
    print(f"TEST: {label}")
    print(f"Params: {json.dumps({k:v for k,v in params.items() if k != 'key'}, indent=2)}")
    try:
        resp = requests.get(BASE_URL, params=params, timeout=30)
        print(f"HTTP status: {resp.status_code}")
        if resp.status_code != 200:
            print(f"Response: {resp.text[:500]}")
            return

        data     = resp.json()

        if show_raw:
            print("RAW RESPONSE (truncated):")
            print(json.dumps(data, indent=2)[:raw_limit])
            return

        category = data.get("category", [{}])[0]
        records  = category.get("records", {})
        total    = records.get("total", 0)
        print(f"Total results: {total}")
        print(f"Records keys: {list(records.keys())}")

        for key, val in records.items():
            if isinstance(val, list) and val:
                first = val[0]
                print(f"First item under '{key}':")
                print(f"  id:       {first.get('id')}")
                print(f"  title:    {first.get('title')}")
                print(f"  issued:   {first.get('issued')}")
                print(f"  isPartOf: {first.get('isPartOf')}")
                print(f"  url:      {first.get('troveUrl') or first.get('url')}")
                break

    except Exception as e:
        print(f"ERROR: {e}")


# ── Test 1: newspaper category, Keith Dunstan, no title filter ───────────────
test("Newspaper — Keith Dunstan, no title filter", {
    "key":      API_KEY,
    "category": "newspaper",
    "q":        "Keith Dunstan",
    "encoding": "json",
    "n":        3,
})

# ── Test 2: newspaper, l-title variants ──────────────────────────────────────
for title in [
    "The Age",
    "Age (Melbourne)",
    "The Age (Melbourne)",
    "The Age (Melbourne, Vic.)",
]:
    test(f"Newspaper + l-title='{title}'", {
        "key":      API_KEY,
        "category": "newspaper",
        "q":        "Keith Dunstan",
        "l-title":  title,
        "encoding": "json",
        "n":        3,
    })

# ── Test 3: newspaper raw response to check structure ────────────────────────
test("Newspaper raw — The Age, check response structure", {
    "key":      API_KEY,
    "category": "newspaper",
    "q":        "Keith Dunstan",
    "l-title":  "The Age",
    "encoding": "json",
    "n":        2,
}, show_raw=True)

# ── Test 4: date range — his likely active period ────────────────────────────
test("Newspaper — Keith Dunstan, The Age, 1960–2005", {
    "key":      API_KEY,
    "category": "newspaper",
    "q":        'Keith Dunstan date:[1960-01-01 TO 2005-12-31]',
    "l-title":  "The Age",
    "encoding": "json",
    "n":        3,
})

# ── Test 5: magazine category — just in case ─────────────────────────────────
test("Magazine — Keith Dunstan, The Age (just in case)", {
    "key":      API_KEY,
    "category": "magazine",
    "q":        "Keith Dunstan",
    "l-title":  "The Age",
    "encoding": "json",
    "n":        3,
})
