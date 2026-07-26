"""
deduplicate.py
--------------
Merge the CSV logs from fetch_batman.py and fetch_byline.py, identify
duplicate articles (same Trove ID written by both passes), and produce
a single master CSV for review.

Does NOT delete any .md files — duplicates are flagged in the CSV only.
Review the master CSV and manually delete duplicate files from
output/bulletin/stubs/.

Usage:
    python deduplicate.py

Output:
    trove/output/master_results.csv
"""

import os
import csv

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

RESULT_FILES = {
    "fetch_batman": os.path.join(OUTPUT_DIR, "fetch_batman_results.csv"),
    "fetch_byline": os.path.join(OUTPUT_DIR, "fetch_byline_results.csv"),
}


def main():
    seen_ids   = {}
    all_rows   = []
    duplicates = []

    for pass_name, path in RESULT_FILES.items():
        if not os.path.exists(path):
            print(f"  MISSING (run the fetch script first): {os.path.basename(path)}")
            continue

        with open(path, newline="", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                tid = row.get("trove_id", "")
                row["source_pass"] = pass_name
                if tid in seen_ids:
                    row["duplicate_of"] = seen_ids[tid]["filename"]
                    duplicates.append(row)
                else:
                    seen_ids[tid] = row
                    row["duplicate_of"] = ""
                all_rows.append(row)

    fieldnames = [
        "trove_id", "title", "date", "trove_url", "fulltext_url",
        "filename", "status", "source_pass", "duplicate_of"
    ]

    master_path = os.path.join(OUTPUT_DIR, "master_results.csv")
    with open(master_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    byline_only = [r for r in all_rows if r["source_pass"] == "fetch_byline" and not r["duplicate_of"]]

    print(f"Batman pass:     {sum(1 for r in all_rows if r['source_pass'] == 'fetch_batman')} articles")
    print(f"Byline pass:     {sum(1 for r in all_rows if r['source_pass'] == 'fetch_byline')} articles")
    print(f"Unique articles: {len(seen_ids)}")
    print(f"Duplicates:      {len(duplicates)}")
    print(f"Byline-only:     {len(byline_only)} articles not in Batman pass")
    print(f"\nMaster CSV: {master_path}")

    if duplicates:
        print(f"\nDuplicate files to remove from output/bulletin/stubs/:")
        for d in duplicates:
            print(f"  {d['filename']}")


if __name__ == "__main__":
    main()
