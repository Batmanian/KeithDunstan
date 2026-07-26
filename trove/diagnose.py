"""
diagnose.py
-----------
Diagnostic script to test Trove API connectivity and surface the exact
parameters needed for The Bulletin searches.

Run this before the main fetch scripts to verify everything is working.

Usage:
    python diagnose.py
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


def test(label, params):
    print(f"\n{'='*60}")
    print(f"TEST: {label}")
    print(f"Params: {json.dumps({k:v for k,v in params.items() if k != 'key'}, indent=2)}")
    try:
        resp = requests.get(BASE_URL, params=params, timeout=30)
        print(f"HTTP status: {resp.status_code}")
        if resp.status_code != 200:
            print(f"Response: {resp.text[:500]}")
            return
        data = resp.json()
        category = data.get("category", [{}])[0]
        records = category.get("records", {})
        total = records.get("total", 0)
        items = records.get("article", [])
        print(f"Total results: {total}")
        print(f"Items returned: {len(items)}")
        if items:
            print("First result:")
            first = items[0]
            print(f"  id:    {first.get('id')}")
            print(f"  title: {first.get('title')}")
            print(f"  date:  {first.get('date')}")
            print(f"  url:   {first.get('troveUrl')}")
            # Show available facets to find correct l-title value
        facets = records.get("facets", {})
        if facets:
            print("Facets available:", list(facets.keys())[:5])
    except Exception as e:
        print(f"ERROR: {e}")


# Test 1 — bare search for Batman with no filters, magazine category
test("Bare search: batman, magazine category, no title filter", {
    "key": API_KEY,
    "category": "magazine",
    "q": "batman",
    "encoding": "json",
    "n": 3,
})

# Test 2 — with l-title as we had it
test("With l-title=The Bulletin", {
    "key": API_KEY,
    "category": "magazine",
    "q": "batman",
    "l-title": "The Bulletin",
    "encoding": "json",
    "n": 3,
})

# Test 3 — try the NLA object ID directly as l-title
test("With NLA object ID in query", {
    "key": API_KEY,
    "category": "magazine",
    "q": 'batman "nla.obj-68375465"',
    "encoding": "json",
    "n": 3,
})

# Test 4 — search known Trove article URL to confirm article category works
test("Known article by Trove ID", {
    "key": API_KEY,
    "category": "magazine",
    "q": "id:nla.obj-699528290",
    "encoding": "json",
    "n": 3,
})

# Test 5 — try newspaper category instead (The Bulletin may be indexed there)
test("Batman in newspaper category (no title filter)", {
    "key": API_KEY,
    "category": "newspaper",
    "q": "batman",
    "encoding": "json",
    "n": 3,
})

# Test 6 — all categories, no filter
test("Batman across ALL categories", {
    "key": API_KEY,
    "category": "all",
    "q": "batman bulletin",
    "encoding": "json",
    "n": 3,
})
