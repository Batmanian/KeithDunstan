"""
triage.py
---------
Interactive triage tool for bulletin stubs. Opens each article in your
browser, shows the title/date/snippet in the terminal, and moves the file
based on your input.

Commands:
  k  — keep as stub (skip, leave in stubs/)
  t  — transcribed (move to transcribed/ — article is confirmed Keith's, full text added)
  r  — rejected (move to rejected/ — noise, family mention, not by Keith)
  q  — quit and save progress

Progress is saved to output/triage_progress.txt so you can resume at any time.

Usage:
    python triage.py                  # start or resume from last position
    python triage.py --from-start     # restart from the beginning
    python triage.py --rejected-only  # review only files already in rejected/
"""

import os
import re
import sys
import shutil
import webbrowser

BASE_DIR       = os.path.dirname(__file__)
OUTPUT_DIR     = os.path.join(BASE_DIR, "output")
STUBS_DIR      = os.path.join(OUTPUT_DIR, "bulletin", "stubs")
TRANSCRIBED_DIR = os.path.join(OUTPUT_DIR, "bulletin", "transcribed")
REJECTED_DIR   = os.path.join(OUTPUT_DIR, "bulletin", "rejected")
PROGRESS_FILE  = os.path.join(OUTPUT_DIR, "triage_progress.txt")

FROM_START     = "--from-start" in sys.argv
REJECTED_ONLY  = "--rejected-only" in sys.argv


def extract_frontmatter(filepath):
    """Pull title, date, and snippet from a stub .md file."""
    title    = ""
    date     = ""
    snippet  = ""
    trove_url = ""

    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # Title and date from frontmatter
    title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
    date_match  = re.search(r'^date:\s*(\S+)', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip().strip('"\'')
    if date_match:
        date = date_match.group(1).strip()

    # Snippet from blockquote
    snippet_match = re.search(r'^>\s*(.+)$', content, re.MULTILINE)
    if snippet_match:
        snippet = snippet_match.group(1).strip()[:120]

    # Trove URL from source line at bottom
    url_match = re.search(r'\]\((https://(?:nla\.gov\.au|trove\.nla\.gov\.au)/[^\)]+)\)', content)
    if url_match:
        trove_url = url_match.group(1)

    return title, date, snippet, trove_url


def load_progress():
    """Load the last processed filename."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            return f.read().strip()
    return None


def save_progress(filename):
    with open(PROGRESS_FILE, "w") as f:
        f.write(filename)


def clear_progress():
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)


def get_files():
    if REJECTED_ONLY:
        source = REJECTED_DIR
    else:
        source = STUBS_DIR
    files = sorted(f for f in os.listdir(source) if f.endswith(".md"))
    return files, source


def move_file(filename, source_dir, dest_dir):
    src  = os.path.join(source_dir, filename)
    dest = os.path.join(dest_dir, filename)
    if os.path.exists(dest):
        # Avoid overwriting — append _dup suffix
        base, ext = os.path.splitext(filename)
        dest = os.path.join(dest_dir, f"{base}_dup{ext}")
    shutil.move(src, dest)


def print_header(filename, title, date, snippet, index, total):
    print("\n" + "=" * 65)
    print(f"  [{index}/{total}]  {filename}")
    print("=" * 65)
    print(f"  Title:   {title or '(no title)'}")
    print(f"  Date:    {date or '(no date)'}")
    if snippet:
        print(f"  Snippet: {snippet}...")
    print()
    print("  k = keep stub   t = transcribed   r = reject   q = quit")
    print("-" * 65)


def main():
    files, source_dir = get_files()

    if not files:
        print("No files to triage.")
        return

    # Resume from last position
    last = load_progress() if not FROM_START else None
    start_index = 0
    if last and last in files:
        start_index = files.index(last)
        print(f"Resuming from: {last}  ({start_index + 1}/{len(files)})")
    elif FROM_START:
        clear_progress()
        print(f"Starting from the beginning. {len(files)} files to triage.")
    else:
        print(f"Starting triage. {len(files)} files to triage.")

    print("\nPress Enter after each command.\n")

    stats = {"kept": 0, "transcribed": 0, "rejected": 0, "skipped": 0}

    for i, filename in enumerate(files[start_index:], start=start_index + 1):
        filepath = os.path.join(source_dir, filename)
        if not os.path.exists(filepath):
            continue  # already moved in a previous session

        title, date, snippet, trove_url = extract_frontmatter(filepath)
        print_header(filename, title, date, snippet, i, len(files))

        # Open in browser
        if trove_url:
            webbrowser.open(trove_url)
        else:
            print("  (no Trove URL found in file)")

        while True:
            try:
                cmd = input("  > ").strip().lower()
            except (KeyboardInterrupt, EOFError):
                print("\n\nInterrupted. Progress saved.")
                save_progress(filename)
                print_summary(stats, len(files), start_index, i)
                return

            if cmd == "k":
                print(f"  → Kept as stub.")
                stats["kept"] += 1
                break
            elif cmd == "t":
                move_file(filename, source_dir, TRANSCRIBED_DIR)
                print(f"  → Moved to transcribed/")
                stats["transcribed"] += 1
                break
            elif cmd == "r":
                move_file(filename, source_dir, REJECTED_DIR)
                print(f"  → Moved to rejected/")
                stats["rejected"] += 1
                break
            elif cmd == "q":
                save_progress(filename)
                print(f"\nProgress saved at: {filename}")
                print_summary(stats, len(files), start_index, i)
                return
            else:
                print("  Invalid command. Use k, t, r, or q.")

        save_progress(filename)

    clear_progress()
    print("\n✓ All files triaged.")
    print_summary(stats, len(files), start_index, len(files))


def print_summary(stats, total, start_index, current_index):
    reviewed = current_index - start_index
    print(f"\n  Session summary:")
    print(f"    Reviewed:    {reviewed} of {total}")
    print(f"    Kept:        {stats['kept']}")
    print(f"    Transcribed: {stats['transcribed']}")
    print(f"    Rejected:    {stats['rejected']}")
    remaining = total - current_index
    if remaining > 0:
        print(f"    Remaining:   {remaining} (run again to resume)")


if __name__ == "__main__":
    main()
