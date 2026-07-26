#!/bin/bash
#
# ocr-cleanup.sh — remove working OCR files for a chapter once its
# scans have been transcribed and reviewed.
#
# Usage:
#   scripts/ocr-cleanup.sh "<chapter-folder-name>"
#
# <chapter-folder-name> must match the folder name used under both
# src/books/[book-slug]/Scans/ and ocr/, e.g.:
#   scripts/ocr-cleanup.sh "Chapter 1 - Beatrice miles"
#
# The derived JPEGs in ocr/<chapter-folder-name>/ are deleted outright —
# they are cheaply regenerable from the HEIC originals via ocr-prep.sh.
# The original HEIC scans are moved to the Trash (not permanently
# deleted) since they cannot be regenerated without re-scanning the
# physical book.

set -euo pipefail

CHAPTER="${1:?Usage: scripts/ocr-cleanup.sh \"<chapter-folder-name>\"}"

SCAN_DIR=$(find src/books -type d -path "*/Scans/${CHAPTER}" -print -quit)
OCR_DIR="ocr/${CHAPTER}"

if [ -z "$SCAN_DIR" ]; then
  echo "No Scans folder found matching: $CHAPTER" >&2
  exit 1
fi

if [ -d "$OCR_DIR" ]; then
  jpg_count=$(find "$OCR_DIR" -maxdepth 1 -iname "*.jpg" | wc -l | tr -d ' ')
  if [ "$jpg_count" -gt 0 ]; then
    rm -f "$OCR_DIR"/*.jpg
    echo "Deleted $jpg_count converted JPEG(s) in $OCR_DIR"
  fi
  rmdir "$OCR_DIR" 2>/dev/null || true
fi

shopt -s nullglob nocaseglob
HEICS=("$SCAN_DIR"/*.heic)
shopt -u nocaseglob nullglob

if [ ${#HEICS[@]} -eq 0 ]; then
  echo "No HEIC files found in $SCAN_DIR"
  exit 0
fi

ABS_HEICS=()
for f in "${HEICS[@]}"; do
  ABS_HEICS+=("$(cd "$(dirname "$f")" && pwd)/$(basename "$f")")
done

APPLESCRIPT_LIST=""
for f in "${ABS_HEICS[@]}"; do
  APPLESCRIPT_LIST+="(POSIX file \"${f}\") as alias, "
done
APPLESCRIPT_LIST="${APPLESCRIPT_LIST%, }"

osascript -e "tell application \"Finder\" to delete {${APPLESCRIPT_LIST}}" >/dev/null

echo "Moved ${#HEICS[@]} HEIC scan(s) from $SCAN_DIR to Trash"
rmdir "$SCAN_DIR" 2>/dev/null || true
