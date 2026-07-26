"""
diagnose2.py
------------
Second diagnostic — finds the correct response structure and category
for The Bulletin in Trove API v3.

Usage:
    python diagnose2.py
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


def test(label, params, show_raw=False):
    print(f"\n{'='*60}")
    print(f"TEST: {label}")
    try:
        resp = requests.get(BASE_URL, params=params, timeout=30)
        print(f"HTTP status: {resp.status_code}")
        data = resp.json()

        if show_raw:
            print("RAW RESPONSE (truncated):")
            print(json.dumps(data, indent=2)[:3000])
            return

        category = data.get("category", [{}])[0]
        records = category.get("records", {})
        total = records.get("total", 0)
        print(f"Total results: {total}")
        print(f"Records keys: {list(records.keys())}")

        # Print first item of whatever key exists
        for key, val in records.items():
            if isinstance(val, list) and val:
                print(f"First item under '{key}':")
                first = val[0]
                print(f"  id:    {first.get('id')}")
                print(f"  title: {first.get('title')}")
                print(f"  date:  {first.get('date')}")
                print(f"  url:   {first.get('troveUrl')}")
                break

    except Exception as e:
        print(f"ERROR: {e}")


# Test 1 — magazine category raw response to see actual keys
test("Magazine category raw response structure", {
    "key": API_KEY,
    "category": "magazine",
    "q": "batman",
    "encoding": "json",
    "n": 3,
}, show_raw=True)

# Test 2 — newspaper category with The Bulletin title filter
test("Newspaper category + l-title=The Bulletin", {
    "key": API_KEY,
    "category": "newspaper",
    "q": "batman",
    "l-title": "The Bulletin",
    "encoding": "json",
    "n": 5,
})

# Test 3 — newspaper category + bulletin in query, no title filter
test("Newspaper category, q=batman bulletin (no title filter)", {
    "key": API_KEY,
    "category": "newspaper",
    "q": "batman bulletin",
    "encoding": "json",
    "n": 5,
})

# Test 4 — newspaper category, search for the known article's NLA ID
test("Newspaper category, known article ID", {
    "key": API_KEY,
    "category": "newspaper",
    "q": "id:nla.obj-699528290",
    "encoding": "json",
    "n": 3,
})

# Test 5 — newspaper + l-title variant spellings
for title in ["Bulletin", "The Bulletin (Sydney)", "Bulletin (Sydney, N.S.W.)"]:
    test(f"Newspaper + l-title={title!r}", {
        "key": API_KEY,
        "category": "newspaper",
        "q": "batman",
        "l-title": title,
        "encoding": "json",
        "n": 3,
    })
