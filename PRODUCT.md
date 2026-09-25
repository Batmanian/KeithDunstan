# Keith Dunstan Literary Archive

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

General readers, particularly Generation X and younger people who may not know Keith Dunstan's writing. Baby Boomers familiar with his work remain welcome, but prior familiarity must not be assumed.

## Product Purpose

Introduce Keith Dunstan's writing, social commentary and influence to a new readership. Present the breadth of his work as a source for understanding Australian life and social trends, particularly from 1960 to 2000. This is an interpretive focus, not a limit on the dates of material in the archive.

Success means visitors understand who Keith was as a writer, why his work matters, and the role of the publications through which readers encountered him, then explore his writing.

## Positioning

A dedicated archive bringing together Dunstan's books and journalism, with publication, chronology and topic routes into his observations of Australian life.

## Operating Context

The public website is keithdunstan.org. Readers can browse articles by publication, books, a timeline and topics, or search the collection. Content is maintained through an Obsidian-compatible vault and published as a static Eleventy site.

## Capabilities and Constraints

- Existing implementation: Eleventy, Bootstrap 5, Sass, Gulp and Pagefind search; light and dark themes.
- `vault/` is the authority for book chapters and articles. The corresponding files under `src/` are generated symlinks.
- `dev/` and `docs/` are build outputs, never hand-edited.
- Preserve published content, working routes and archive navigation during interface changes.
- The collection is still being transcribed. Do not imply every work is available in full.
- Claims about influence, publication reach and historical significance need evidence; do not invent readership numbers, quotations or endorsements.

## Brand Commitments

Keith Dunstan Literary Archive. Australian English. Preserve Keith's original voice in transcriptions and distinguish editorial introductions from his own writing.

## Evidence on Hand

- Books and journalism in `vault/`, including The Bulletin and Walkabout material.
- Bibliography in `src/_data/books.json` and publication introductions in the root `src/*.njk` templates.
- Existing biographical material and an attributed Michael Smith quotation in `src/index.njk`; verify quotations against their source before altering them.
- Existing portrait at `src/img/keith.jpg` and cover assets in `src/img/`. Existing availability is not a new rights clearance.

## Product Principles

- Keith is the visual anchor; his body of writing is the subject. Establish its breadth, volume and reach across formats, decades and publications. Biography supports the collection rather than leading it.
- Introduce the writer before assuming recognition of his name.
- Show the breadth of his subjects through actual writing.
- Explain the publications and historical context that made his work influential.
- Make the transition from introduction to reading obvious.
- Preserve source fidelity and distinguish interpretation from evidence.

## Open Decisions

Specific accessibility requirements beyond accessible web practice have not been established. New editorial claims and the final home page composition remain subject to review.
