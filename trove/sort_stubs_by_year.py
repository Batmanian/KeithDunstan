#!/usr/bin/env python3
"""Sort loose publication stubs into year directories.

Only Markdown files directly inside a publication's ``stubs`` directory are
moved. Existing workflow folders such as ``Scans`` and their contents are left
untouched.
"""

from __future__ import annotations

import argparse
import re
import shutil
from collections import Counter
from pathlib import Path


DATE_RE = re.compile(r"^date:\s*['\"]?(\d{4})-\d{2}-\d{2}", re.MULTILINE)
FILENAME_RE = re.compile(r"^(\d{4})-\d{2}-\d{2}-")


def year_for(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    frontmatter_match = DATE_RE.search(text)
    filename_match = FILENAME_RE.match(path.name)

    frontmatter_year = frontmatter_match.group(1) if frontmatter_match else None
    filename_year = filename_match.group(1) if filename_match else None

    if frontmatter_year and filename_year and frontmatter_year != filename_year:
        raise ValueError(
            f"{path.name}: frontmatter year {frontmatter_year} does not match "
            f"filename year {filename_year}"
        )
    if frontmatter_year:
        return frontmatter_year
    if filename_year:
        return filename_year
    raise ValueError(f"{path.name}: cannot determine year")


def sort_stubs(root: Path, dry_run: bool) -> Counter[str]:
    counts: Counter[str] = Counter()
    loose_stubs = sorted(root.glob("*.md"))

    for source in loose_stubs:
        year = year_for(source)
        destination = root / year / source.name

        if destination.exists():
            if source.read_bytes() == destination.read_bytes():
                raise FileExistsError(
                    f"Duplicate already exists at {destination}; source left untouched"
                )
            raise FileExistsError(
                f"Different file already exists at {destination}; source left untouched"
            )

        if not dry_run:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(destination))
        counts[year] += 1

    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "publication",
        nargs="?",
        default="bulletin",
        help="publication directory under trove/output (default: bulletin)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate and report moves without changing files",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent / "output" / args.publication / "stubs"
    if not root.is_dir():
        raise SystemExit(f"Stub directory does not exist: {root}")

    counts = sort_stubs(root, args.dry_run)
    action = "Would move" if args.dry_run else "Moved"
    total = sum(counts.values())
    print(f"{action} {total} stub(s) into {len(counts)} year folder(s).")
    for year, count in sorted(counts.items()):
        print(f"  {year}: {count}")


if __name__ == "__main__":
    main()
