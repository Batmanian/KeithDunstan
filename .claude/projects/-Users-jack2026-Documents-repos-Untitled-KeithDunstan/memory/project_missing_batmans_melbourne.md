---
name: Missing Batman's Melbourne articles — bulletin-contents gap check
description: Some Bulletin editions have a bulletin-contents stub but no matching Batman's Melbourne stub, meaning fetch_batman.py missed those articles
type: project
---

For 1977–1984, some weekly Bulletin editions show a `bulletin-contents-*` stub in the review server but have no corresponding `batman-s-melbourne-*` stub for that same date. Those are gaps — Keith Dunstan wrote a column that issue but fetch_batman.py didn't catch it.

**How to apply:** After each year's review/transcription pass, cross-reference the dates of `bulletin-contents` stubs (in stubs/ or rejected/) against the dates of batman's-melbourne stubs. Any edition date that has a contents page but no batman article is a candidate for a missing article. Check Trove manually for that date and fetch if found.

**Why:** The fetch_batman.py search terms may not catch all column title variants or OCR'd titles. The bulletin-contents page for a given edition is a reliable signal that an issue exists; if batman's melbourne isn't there, the article is missing, not absent.
