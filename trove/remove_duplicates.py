"""
remove_duplicates.py
--------------------
Reads master_results.csv and deletes any .md files flagged as duplicates
from output/bulletin/stubs/.

Only deletes files that:
  - Are flagged in the duplicate_of column (i.e. caught by a second pass)
  - Still exist in output/bulletin/stubs/ (won't touch transcribed/ or rejected/)

Run after deduplicate.py has generated master_results.csv.

Usage:
    python remove_duplicates.py
    python remove_duplicates.py --dry-run   # preview without deleting
"""

import os
import csv
import sys

DRY_RUN   = "--dry-run" in sys.argv
BASE_DIR  = os.path.dirname(__file__)
CSV_PATH  = os.path.join(BASE_DIR, "output", "master_results.csv")
STUBS_DIR = os.path.join(BASE_DIR, "output", "bulletin", "stubs")


def main():
    if not os.path.exists(CSV_PATH):
        raise SystemExit("ERROR: output/master_results.csv not found. Run deduplicate.py first.")

    duplicates = []
    with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if row.get("duplicate_of"):
                duplicates.append(row["filename"])

    print(f"Duplicates flagged in master_results.csv: {len(duplicates)}")
    if DRY_RUN:
        print("DRY RUN — no files will be deleted.\n")

    deleted = 0
    missing = 0
    for filename in duplicates:
        filepath = os.path.join(STUBS_DIR, filename)
        if os.path.exists(filepath):
            if DRY_RUN:
                print(f"  WOULD DELETE: {filename}")
            else:
                os.remove(filepath)
                print(f"  DELETED: {filename}")
            deleted += 1
        else:
            print(f"  NOT IN STUBS (already moved or deleted): {filename}")
            missing += 1

    print(f"\n{'Would delete' if DRY_RUN else 'Deleted'}: {deleted} files")
    if missing:
        print(f"Not found in stubs/: {missing} files")


if __name__ == "__main__":
    main()
