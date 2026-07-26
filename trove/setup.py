"""
setup.py
--------
Creates the trove/output/ folder structure for all known publications.
Run once after cloning the repository, before running any fetch scripts.

Usage:
    python setup.py
"""

import os

PUBLICATIONS = [
    "bulletin",
    "walkabout",
    "the-age",
    "the-herald",
    "the-sun",
    "australian-gourmet-traveller",
    "good-weekend",
    "readers-digest",
    "courier-mail",
    "herald-and-weekly-times",
    "unsorted",
]

STATUS_DIRS = ["stubs", "transcribed", "rejected"]

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


def main():
    print(f"Creating output structure in: {OUTPUT_DIR}\n")
    for pub in PUBLICATIONS:
        for status in STATUS_DIRS:
            path = os.path.join(OUTPUT_DIR, pub, status)
            os.makedirs(path, exist_ok=True)
            print(f"  OK  output/{pub}/{status}/")

    print("""
Setup complete.

Workflow:
  Fetch scripts  →  output/<publication>/stubs/
  After review   →  output/<publication>/transcribed/  (or rejected/)
  Site-ready     →  src/posts/<publication>/
""")


if __name__ == "__main__":
    main()
