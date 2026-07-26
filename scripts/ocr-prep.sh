#!/bin/bash
#
# ocr-prep.sh — convert scanned HEIC page images into JPEGs sized for
# transcription (Claude cannot read raw iPhone HEIC scans: wrong format
# and typically too large). Output goes to ocr/ (gitignored working dir).
#
# Usage:
#   scripts/ocr-prep.sh <source-dir> [max-dimension]
#
# Example:
#   scripts/ocr-prep.sh "src/books/ratbags/Scans/frontmatter"
#   scripts/ocr-prep.sh "src/books/ratbags/Scans/Chapter 1 - Beatrice miles" 1600
#
# For each <name>.heic|HEIC in <source-dir>, writes ocr/<source-dir-basename>/<name>.jpg
# resized so its longest edge is <= max-dimension (default 1800px) and
# re-compressed until it is comfortably under Claude's 256KB read limit.

set -euo pipefail

SRC_DIR="${1:?Usage: scripts/ocr-prep.sh <source-dir> [max-dimension]}"
MAX_DIM="${2:-1800}"
MAX_BYTES=$((240 * 1024))

if [ ! -d "$SRC_DIR" ]; then
  echo "Source directory not found: $SRC_DIR" >&2
  exit 1
fi

BASENAME="$(basename "$SRC_DIR")"
OUT_DIR="ocr/${BASENAME}"
mkdir -p "$OUT_DIR"

shopt -s nullglob nocaseglob
FILES=("$SRC_DIR"/*.heic)
shopt -u nocaseglob
shopt -u nullglob

if [ ${#FILES[@]} -eq 0 ]; then
  echo "No .heic files found in $SRC_DIR" >&2
  exit 1
fi

for f in "${FILES[@]}"; do
  name="$(basename "${f%.*}")"
  out="${OUT_DIR}/${name}.jpg"

  quality=80
  sips -s format jpeg -Z "$MAX_DIM" -s formatOptions "$quality" "$f" --out "$out" >/dev/null

  size=$(stat -f%z "$out")
  while [ "$size" -gt "$MAX_BYTES" ] && [ "$quality" -gt 30 ]; do
    quality=$((quality - 15))
    sips -s format jpeg -Z "$MAX_DIM" -s formatOptions "$quality" "$f" --out "$out" >/dev/null
    size=$(stat -f%z "$out")
  done

  echo "$f -> $out (${size} bytes, quality ${quality})"
done
