# scripts/ — Plan

Per CLAUDE.md, this file tracks planned/completed work for changes to the `scripts/` pipeline tooling.

## OCR prep tooling

- [x] `ocr-prep.sh` — converts HEIC scans (iPhone/Files/Continuity Camera) to JPEG, resized and compressed under Claude's 256KB read limit, output to gitignored `ocr/`
- [x] Used to prep `src/books/ratbags/Scans/frontmatter` and `src/books/ratbags/Scans/Chapter 1 - Beatrice miles` for transcription
- [ ] No other scripts in this folder yet

## Notes for future sessions

- This folder only contains `ocr-prep.sh` so far — no build/deploy scripts here (those live in `gulpfile.js` / `.eleventy.js` at repo root).
- If adding new pipeline scripts (e.g. batch OCR prep across multiple chapters, tag extraction helpers), add a checklist item here before starting and check it off in place.
