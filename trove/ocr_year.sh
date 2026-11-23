#!/bin/bash
# Run Tesseract OCR on all article scan directories for a given year.
# Usage: bash trove/ocr_year.sh 1977
# Output: src/trove-scans/bulletin/YEAR-ocr.txt

YEAR="${1:-1977}"
SCANS="src/trove-scans/bulletin/$YEAR"
OUT="src/trove-scans/bulletin/${YEAR}-ocr.txt"

if [ ! -d "$SCANS" ]; then
  echo "No scan directory: $SCANS"
  exit 1
fi

> "$OUT"

for dir in "$SCANS"/*/; do
  [ -d "$dir" ] || continue
  slug=$(basename "$dir")
  echo "====== $slug ======"
  echo "====== $slug ======" >> "$OUT"
  for img in "$dir"page-*.jpg; do
    [ -f "$img" ] || continue
    echo "--- $(basename "$img") ---" >> "$OUT"
    tesseract "$img" stdout -l eng --psm 6 2>/dev/null >> "$OUT"
    echo >> "$OUT"
  done
done

echo "Done. Lines: $(wc -l < "$OUT")"
