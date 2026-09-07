# scripts/ — Plan

Per CLAUDE.md, this file tracks planned/completed work for changes to the `scripts/` pipeline tooling.

## OCR prep tooling

- [x] `ocr-prep.sh` — converts HEIC scans (iPhone/Files/Continuity Camera) to JPEG, resized and compressed under Claude's 256KB read limit, output to gitignored `ocr/`
- [x] Used to prep `src/books/ratbags/Scans/frontmatter` and `src/books/ratbags/Scans/Chapter 1 - Beatrice miles` for transcription
- [x] `ocr-cleanup.sh` — companion cleanup script for the above

## Vault pipeline tooling (added when vault/ became the content authority)

- [x] `link-vault-content.js` (`npm run link:vault`) — symlinks every `.md` file in `vault/books/`/`vault/articles/` into `src/books/`/`src/articles/`. The one everyday command: run it after adding, renaming, or removing a note in the vault. Hardcodes Ratbags as the one book whose chapters map to a `.njk` symlink name instead of `.md`.
- [x] `export-obsidian-vault.js` (`npm run export:vault`) — rare-use safety net, not the normal workflow. Absorbs a stray real (non-symlink) `.md`/`.njk` file that ends up directly in `src/books/`/`src/articles/` into the vault instead. Never deletes or overwrites vault content.
- [x] `link-vault-images.js` (`npm run link:vault-images`) — one-time migration script that moved book/publication cover art and embedded content images into `vault/`, symlinked back from `src/img/`. Safe to re-run (no-ops on anything already migrated) if a new image needs the same treatment — extend its `IMAGE_MAP`.
- [x] `set-og-images.js` (`npm run set:og-images`) — sets an `image:` frontmatter field on vault content files belonging to a book/publication with cover art, so Open Graph previews show the right cover. Surgical text insertion, not a YAML re-serialise. Safe to re-run (skips files that already have `image:`).
- [x] `set-obsidian-tags.js` (`npm run set:obsidian-tags`) — adds `obsidian_tags:`, a generated hyphenated mirror of `tags:`, so multi-word proper-noun tags cluster in Obsidian's Tags pane (which rejects tags containing spaces). Never touches `tags:` itself. Re-parses every edited file afterward and refuses to write if the original `tags:` array didn't survive byte-for-byte — see MISTAKES.md for the two edge cases (zero-indent list items, a blank line before the first item) that check caught during rollout.
- [x] `generate-topics.js` / `check-chapter-links.js` — pre-existing scripts, both updated during the vault migration to follow symlinks correctly (see MISTAKES.md — `Dirent.isFile()`/`isDirectory()` from `fs.readdirSync(..., {withFileTypes:true})` report a symlink's own type, not its target's, so they silently skipped every vault-linked file until fixed to use `fs.statSync`).

## Notes for future sessions

- Build/deploy scripts live in `gulpfile.js` / `.eleventy.js` at repo root, not here.
- Any script that walks `src/books/` or `src/articles/` and needs to distinguish files from directories **must** use `fs.statSync` (follows symlinks), never `Dirent.isFile()`/`isDirectory()` from `fs.readdirSync(dir, {withFileTypes: true})` (reflects the symlink itself) — that content is symlinked in from `vault/`. See the `generate-topics.js`/`check-chapter-links.js` fix above for the concrete failure mode.
- If adding new pipeline scripts, add a checklist item here before starting and check it off in place.
