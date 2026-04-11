#!/bin/bash
# migrate-structure.sh
# Moves content from src/posts/ into src/books/ and src/articles/
# Run from the repository root: bash migrate-structure.sh
# Safe to run multiple times — checks for existing destinations before moving

set -e

echo "Keith Dunstan — Content Structure Migration"
echo "==========================================="
echo ""

# Create destination directories
mkdir -p src/books
mkdir -p src/articles

# ── Books ──────────────────────────────────────────────────────────────────

BOOKS=(
  "a-day-in-the-life-of-australia"
  "my-life-with-the-demon"
  "no-brains-at-all"
  "ratbags"
  "supporting-a-column"
  "the-australian-uppercrust-book"
  "wowsers"
)

echo "Moving books..."
for book in "${BOOKS[@]}"; do
  src="src/posts/$book"
  dest="src/books/$book"
  if [ -d "$src" ]; then
    if [ -d "$dest" ]; then
      echo "  SKIP (already exists): $dest"
    else
      mv "$src" "$dest"
      echo "  OK: $src → $dest"
    fi
  else
    echo "  NOT FOUND (skipping): $src"
  fi
done

# ── Articles ───────────────────────────────────────────────────────────────

ARTICLES=(
  "bulletin"
  "walkabout-magazine"
  "the-australian-gourmet"
)

echo ""
echo "Moving articles..."
for pub in "${ARTICLES[@]}"; do
  src="src/posts/$pub"
  dest="src/articles/$pub"
  if [ -d "$src" ]; then
    if [ -d "$dest" ]; then
      echo "  SKIP (already exists): $dest"
    else
      mv "$src" "$dest"
      echo "  OK: $src → $dest"
    fi
  else
    echo "  NOT FOUND (skipping): $src"
  fi
done

# ── posts.json ─────────────────────────────────────────────────────────────

echo ""
if [ -f "src/posts/posts.json" ]; then
  echo "Note: src/posts/posts.json still exists."
  echo "  You will need to review your .eleventy.js collections config"
  echo "  to point to src/books/ and src/articles/ instead of src/posts/"
  echo "  Then you can delete src/posts/posts.json manually."
else
  echo "No posts.json found in src/posts/ — nothing extra to do there."
fi

# ── Check for empty posts dir ──────────────────────────────────────────────

echo ""
remaining=$(ls src/posts/ 2>/dev/null | grep -v "posts.json" | wc -l | tr -d ' ')
if [ "$remaining" -eq "0" ]; then
  echo "src/posts/ is now empty (except possibly posts.json)."
  echo "You can remove it once you've updated .eleventy.js."
else
  echo "Remaining in src/posts/ (not migrated — check these manually):"
  ls src/posts/ | grep -v "posts.json" | sed 's/^/  /'
fi

echo ""
echo "Done. Next steps:"
echo "  1. Update src/books/ and src/articles/ folder-level JSON config files"
echo "     (rename/copy posts.json as needed for each collection)"
echo "  2. Update .eleventy.js collection definitions to use new paths"
echo "  3. Copy _redirects to repository root (if not already there)"
echo "  4. Run: npm run build-dev  — and check for broken internal links"
echo "  5. Commit and push"
