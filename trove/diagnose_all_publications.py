"""
diagnose_all_publications.py
----------------------------
Bulk diagnostic to test all remaining publications in Trove API v3.

For each publication, tests both magazine and newspaper categories across
multiple l-title variants to find what's actually digitised and searchable
for Keith Dunstan's active period (1960–2005).

Publications tested:
  - The Herald (Melbourne)
  - The Sun (Melbourne)
  - The Courier-Mail
  - Good Weekend
  - Herald & Weekly Times
  - Australian Gourmet Traveller
  - Any others specified in PUBLICATIONS below

Usage:
    python diagnose_all_publications.py
"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TROVE_API_KEY")
if not API_KEY:
    raise SystemExit("ERROR: TROVE_API_KEY not set.")

BASE_URL  = "https://api.trove.nla.gov.au/v3/result"
DATE_FROM = "1960-01-01"
DATE_TO   = "2005-12-31"

# Each entry: (display_name, category, [l-title variants to try])
PUBLICATIONS = [
    ("The Herald (Melbourne)", "newspaper", [
        "The Herald",
        "Herald (Melbourne)",
        "The Herald (Melbourne)",
        "The Herald (Melbourne, Vic. : 1954 - 1988)",
    ]),
    ("The Sun (Melbourne)", "newspaper", [
        "The Sun",
        "Sun (Melbourne)",
        "The Sun News-Pictorial",
        "Sun News-Pictorial",
    ]),
    ("The Courier-Mail", "newspaper", [
        "The Courier-Mail",
        "Courier-Mail",
        "The Courier Mail",
    ]),
    ("Good Weekend", "magazine", [
        "Good Weekend",
        "The Good Weekend",
        "Good Weekend (Sydney)",
    ]),
    ("Good Weekend", "newspaper", [
        "Good Weekend",
        "The Good Weekend",
    ]),
    ("Herald & Weekly Times", "magazine", [
        "Herald and Weekly Times",
        "Herald & Weekly Times",
    ]),
    ("Herald & Weekly Times", "newspaper", [
        "Herald and Weekly Times",
        "Herald & Weekly Times",
    ]),
    ("Australian Gourmet Traveller", "magazine", [
        "Australian Gourmet Traveller",
        "Gourmet Traveller",
        "Australian Gourmet Traveller.",
    ]),
    ("The Australian", "newspaper", [
        "The Australian",
        "Australian (Sydney, NSW)",
    ]),
    ("The Sun-Herald", "newspaper", [
        "The Sun-Herald",
        "Sun-Herald",
    ]),
]


def probe(pub_name, category, title_variant):
    """Test a single publication/category/title combination."""
    params = {
        "key":      API_KEY,
        "category": category,
        "q":        f"Keith Dunstan date:[{DATE_FROM} TO {DATE_TO}]",
        "l-title":  title_variant,
        "encoding": "json",
        "n":        3,
    }
    try:
        resp = requests.get(BASE_URL, params=params, timeout=30)
        if resp.status_code != 200:
            return None, f"HTTP {resp.status_code}"

        data    = resp.json()
        records = data.get("category", [{}])[0].get("records", {})
        total   = records.get("total", 0)

        if total == 0:
            return 0, None

        # Get first result details
        for key in ("article", "work"):
            items = records.get(key, [])
            if items:
                first     = items[0]
                title_val = first.get("title", "")
                if isinstance(title_val, dict):
                    title_val = title_val.get("title", "")
                date_val  = first.get("issued") or first.get("date", "")
                url_val   = first.get("troveUrl") or f"https://nla.gov.au/nla.news-article{first.get('id')}"
                return total, {
                    "key":   key,
                    "title": str(title_val)[:80],
                    "date":  date_val,
                    "url":   url_val,
                }

        return total, None

    except Exception as e:
        return None, str(e)


def main():
    print(f"\nSearching for Keith Dunstan articles, {DATE_FROM} to {DATE_TO}")
    print("=" * 65)

    hits = []   # collect successful results for summary

    for pub_name, category, variants in PUBLICATIONS:
        print(f"\n── {pub_name} ({category}) ──────────────────────────────")
        found = False
        for variant in variants:
            total, detail = probe(pub_name, category, variant)

            if total is None:
                print(f"  [{variant}]  ERROR: {detail}")
            elif total == 0:
                print(f"  [{variant}]  0 results")
            else:
                print(f"  [{variant}]  ✓ {total} results")
                if isinstance(detail, dict):
                    print(f"    response key: '{detail['key']}'")
                    print(f"    first result: {detail['title']}")
                    print(f"    date:         {detail['date']}")
                    print(f"    url:          {detail['url']}")
                hits.append({
                    "publication": pub_name,
                    "category":    category,
                    "l-title":     variant,
                    "total":       total,
                    "response_key": detail.get("key") if isinstance(detail, dict) else "unknown",
                })
                found = True
                break   # stop trying variants once one works

        if not found:
            print(f"  → Not available in Trove for this period.")

    # Summary
    print("\n" + "=" * 65)
    print("SUMMARY — Publications with results:")
    print("=" * 65)
    if hits:
        for h in hits:
            print(f"  {h['publication']}")
            print(f"    category:     {h['category']}")
            print(f"    l-title:      {h['l-title']}")
            print(f"    response key: {h['response_key']}")
            print(f"    results:      {h['total']}")
            print()
    else:
        print("  None found.")

    print("Publications NOT available:")
    tested = {p[0] for p in PUBLICATIONS}
    found_pubs = {h["publication"] for h in hits}
    for p in tested:
        if p not in found_pubs:
            print(f"  {p}")


if __name__ == "__main__":
    main()
