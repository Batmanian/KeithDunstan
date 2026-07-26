"""
diagnose_walkabout.py
---------------------
Diagnostic script to establish how Walkabout Magazine is indexed in Trove API v3.

Tests:
  - Which category Walkabout sits in (magazine vs newspaper)
  - The correct response key (work vs article)
  - The exact l-title or isPartOf string Trove uses
  - Whether Keith Dunstan articles are findable

Usage:
    python diagnose_walkabout.py
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

        data = resp.json()

        if show_raw:
            print("RAW RESPONSE (truncated):")
            print(json.dumps(data, indent=2)[:raw_limit])
            return

        category = data.get("category", [{}])[0]
        records  = category.get("records", {})
        total    = records.get("total", 0)
        print(f"Total results: {total}")
        print(f"Records keys: {list(records.keys())}")

        # Print first item from whatever key holds results
        for key, val in records.items():
            if isinstance(val, list) and val:
                first = val[0]
                print(f"First item under '{key}':")
                print(f"  id:       {first.get('id')}")
                print(f"  title:    {first.get('title')}")
                print(f"  issued:   {first.get('issued')}")
                print(f"  isPartOf: {first.get('isPartOf')}")
                print(f"  url:      {first.get('troveUrl')}")
                break

    except Exception as e:
        print(f"ERROR: {e}")


# ── Test 1: magazine category, broad search ──────────────────────────────────
test("Magazine category — 'Walkabout' in query, no title filter", {
    "key":      API_KEY,
    "category": "magazine",
    "q":        "Walkabout Dunstan",
    "encoding": "json",
    "n":        3,
})

# ── Test 2: magazine category, l-title variants ───────────────────────────────
for title in ["Walkabout", "Walkabout (Sydney)", "Walkabout magazine"]:
    test(f"Magazine + l-title='{title}'", {
        "key":      API_KEY,
        "category": "magazine",
        "q":        "Keith Dunstan",
        "l-title":  title,
        "encoding": "json",
        "n":        3,
    })

# ── Test 3: newspaper category ────────────────────────────────────────────────
test("Newspaper category — Keith Dunstan, no title filter", {
    "key":      API_KEY,
    "category": "newspaper",
    "q":        "Keith Dunstan Walkabout",
    "encoding": "json",
    "n":        3,
})

# ── Test 4: magazine raw response to check response key ──────────────────────
test("Magazine raw response — check keys returned", {
    "key":      API_KEY,
    "category": "magazine",
    "q":        "Walkabout",
    "encoding": "json",
    "n":        2,
}, show_raw=True)

# ── Test 5: search for Keith Dunstan across all categories ───────────────────
test("All categories — Keith Dunstan Walkabout", {
    "key":      API_KEY,
    "category": "all",
    "q":        "Keith Dunstan Walkabout",
    "encoding": "json",
    "n":        3,
})

# ── Test 6: magazine, broader date range, just 'Walkabout' ───────────────────
test("Magazine — just 'Walkabout', date 1960-1974", {
    "key":      API_KEY,
    "category": "magazine",
    "q":        "Walkabout",
    "encoding": "json",
    "n":        3,
    "l-decade": "196",
})
