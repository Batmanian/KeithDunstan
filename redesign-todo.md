# Keith Dunstan Archive — 2026 Redesign TODO

This implementation checklist should be read alongside [`2026-redesign.md`](./2026-redesign.md), which defines the design, information architecture, editorial and technical principles for the redesign.

Work should proceed in the order below unless a dependency requires otherwise.

---

## 1. Build the new topic hierarchy and curated themes

Reference: [`2026-redesign.md`](./2026-redesign.md) → **Information architecture**, **Curated themes**, **Index and browse pages**

### Entity classification

- [ ] Audit the existing 3,000+ topic/tag records.
- [ ] Define an entity-type field or mapping system for:
  - [ ] People
  - [ ] Places
  - [ ] Organisations
  - [ ] Events
  - [ ] Publications
  - [ ] Subjects
- [ ] Decide whether entity type belongs in existing front matter/tag data or a separate generated index.
- [ ] Preserve all existing granular topic pages wherever practical.
- [ ] Preserve granular topics for SEO, scholarly use and precise search.
- [ ] Create entity index pages for:
  - [ ] People
  - [ ] Places
  - [ ] Organisations
  - [ ] Events
  - [ ] Publications
  - [ ] Subjects
- [ ] Add counts where useful, e.g. number of articles/books associated with each entity.
- [ ] Add alphabetical browse and/or search-within-index where the index is large.
- [ ] Ensure entity pages cross-link back to relevant articles, books and themes.
- [ ] Remove **Topics** as a primary top-level navigation item.
- [ ] Retain **Topics** under **Explore**.
- [ ] Add redirects for any topic/index URLs that change.

### Curated themes

Create the initial thematic layer:

- [ ] Melbourne
- [ ] Australian character
- [ ] Politics & power
- [ ] Food & drink
- [ ] Cities & suburbs
- [ ] Architecture & planning
- [ ] Media & journalism
- [ ] Social change
- [ ] Travel
- [ ] Wine
- [ ] Institutions
- [ ] Technology & progress

For each theme:

- [ ] write a short editorial introduction
- [ ] identify representative articles
- [ ] identify related books
- [ ] identify important people
- [ ] identify important places
- [ ] identify related publications
- [ ] identify relevant granular topics
- [ ] expose relevant decades where useful
- [ ] create a stable theme URL
- [ ] ensure the page can later accommodate a chronological digest

---

## 2. Convert article pages into archival edition pages

Reference: [`2026-redesign.md`](./2026-redesign.md) → **Article pages as edition pages**, **Editorial authority and archive documentation**

- [ ] Redesign the article template around an archival edition model.
- [ ] Keep the article text visually dominant.
- [ ] Add publication context at the top of each article.
- [ ] Display publication date prominently.
- [ ] Display column/series name where known.
- [ ] Display contextual synopsis/introduction where available.

### Add an "About this item" apparatus

Support fields for:

- [ ] **Author** — Keith Dunstan
- [ ] **First published**
- [ ] **Column**
- [ ] **Source**
- [ ] **Transcription** — Keith Dunstan Archive
- [ ] **Last checked**
- [ ] **Permanent URL**
- [ ] **Rights** — Literary Estate of Keith Dunstan
- [ ] **Cite this item**

Implementation:

- [ ] identify which fields already exist in front matter
- [ ] add missing structured fields
- [ ] generate metadata automatically in templates
- [ ] avoid duplicating manually entered metadata
- [ ] define handling for unknown or uncertain metadata

### Subjects

- [ ] Add a **Subjects** section to edition pages.
- [ ] Display linked people, places, organisations, events, publications and subjects.
- [ ] Ensure links resolve to the new entity/index structure.

### Continue exploring

Build contextual onward navigation.

Prioritise:

- [ ] same topic in another decade
- [ ] same place in another decade
- [ ] same theme
- [ ] same publication
- [ ] same column
- [ ] related person
- [ ] related book
- [ ] adjacent item in a chronology

Avoid generic "related posts" where stronger archive relationships exist.

### Citation

- [ ] Add **Cite this item**.
- [ ] Generate a plain-text citation containing:
  - [ ] Keith Dunstan
  - [ ] article title
  - [ ] original publication
  - [ ] original publication date
  - [ ] Keith Dunstan Archive
  - [ ] permanent URL
- [ ] Consider access date as an optional field.
- [ ] Ensure citation data is derived from structured metadata.

### Authority

- [ ] Add the statement **Published by the Keith Dunstan Literary Estate** in appropriate site-wide contexts.
- [ ] Ensure article pages clearly identify the archive as the transcription/editorial source.
- [ ] Review footer/site chrome for consistent Literary Estate attribution.

---

## 3. Improve typography and long-form readability

Reference: [`2026-redesign.md`](./2026-redesign.md) → **Readability**, **Visual system**

Update the typography style guide and site CSS.

### Reading pages

Target:

- [ ] desktop body copy between **19–21px**
- [ ] reading measure around **68–74 characters**
- [ ] line height between **1.55–1.7**
- [ ] serif body typeface
- [ ] sans-serif metadata/navigation/interface typeface
- [ ] dark charcoal text instead of pure black
- [ ] slightly warm background
- [ ] strong italics
- [ ] proper curly quotation marks and apostrophes
- [ ] proper en/em dashes
- [ ] visible but controlled paragraph spacing
- [ ] no permanent sidebar compressing the article column

### Responsive reading

- [ ] test reading width on mobile
- [ ] test line-height on mobile
- [ ] ensure headings wrap cleanly
- [ ] prevent metadata blocks from overwhelming the article header
- [ ] test very long titles
- [ ] test articles with images, blockquotes and lists

### Style guide

- [ ] document headline scale
- [ ] document article body scale
- [ ] document metadata scale
- [ ] document label/button scale
- [ ] document spacing rhythm
- [ ] document link styles
- [ ] document blockquote treatment
- [ ] document publication/date treatment

---

## 4. Update the primary navigation

Reference: [`2026-redesign.md`](./2026-redesign.md) → **Navigation**

Implement:

### Read

- [ ] Books
- [ ] Articles
- [ ] Publications
- [ ] Latest additions

### Explore

- [ ] Themes
- [ ] People
- [ ] Places
- [ ] Timeline
- [ ] Topics

### Keith

- [ ] Biography
- [ ] Career
- [ ] Bibliography
- [ ] Legacy

### About the archive

- [ ] About
- [ ] Editorial principles
- [ ] Rights & reuse
- [ ] Contact

### Search

- [ ] make Search prominent in desktop navigation
- [ ] make Search equally accessible on mobile

### Migration

- [ ] map current navigation items to the new structure
- [ ] retain existing URLs where there is no benefit in changing them
- [ ] create permanent redirects for changed URLs
- [ ] test all redirects
- [ ] verify canonical URLs
- [ ] update sitemap/navigation metadata

---

## 5. Establish the new visual system

Reference: [`2026-redesign.md`](./2026-redesign.md) → **Visual system**

Direction:

> Contemporary Australian newspaper modernism + cultural atlas

- [ ] replace generic Eleventy-theme visual conventions
- [ ] define editorial serif
- [ ] define interface sans serif
- [ ] define headline hierarchy
- [ ] define warm page background
- [ ] define dark charcoal text colour
- [ ] define restrained accent colour
- [ ] define rule/border system
- [ ] define metadata treatment
- [ ] define publication/date treatment
- [ ] define card/list treatment
- [ ] define image/caption treatment
- [ ] define grid and page-width system

Avoid:

- [ ] sepia nostalgia
- [ ] faux paper textures
- [ ] typewriter fonts
- [ ] torn-paper effects
- [ ] decorative newspaper pastiche
- [ ] excessive cards on reading pages

---

## 6. Build stronger browse/index pages

Reference: [`2026-redesign.md`](./2026-redesign.md) → **Index and browse pages**

Create or improve:

- [ ] Themes
- [ ] People
- [ ] Places
- [ ] Organisations
- [ ] Events
- [ ] Publications
- [ ] Subjects
- [ ] Timeline
- [ ] Topics
- [ ] Books
- [ ] Articles
- [ ] Latest additions

For large indexes:

- [ ] alphabetical navigation
- [ ] search within index
- [ ] article/item counts
- [ ] featured or most-covered entries
- [ ] decade filtering where relevant
- [ ] avoid undifferentiated tag clouds

---

## 7. Improve search and discovery

Reference: [`2026-redesign.md`](./2026-redesign.md) → **Search and discovery**

- [ ] review current static search implementation
- [ ] investigate Pagefind or equivalent static-search tooling
- [ ] index article full text
- [ ] index metadata
- [ ] add publication filter
- [ ] add date/decade filter
- [ ] add content-type filter
- [ ] add theme filter
- [ ] add entity-type filter
- [ ] retain granular-topic searching
- [ ] support relevance sort
- [ ] support chronological sort
- [ ] expose useful metadata in search results
- [ ] show matched excerpts
- [ ] test search across spelling variants and historic terms

---

## 8. Build archive authority pages and policies

Reference: [`2026-redesign.md`](./2026-redesign.md) → **Editorial authority and archive documentation**

### About

- [ ] explain purpose and scope
- [ ] explain who maintains/publishes the archive
- [ ] explain relationship to the Keith Dunstan Literary Estate
- [ ] describe current digitisation/publication status

### Editorial principles

- [ ] transcription policy
- [ ] spelling and punctuation policy
- [ ] OCR correction policy
- [ ] treatment of editorial additions
- [ ] contextual-introduction policy
- [ ] tagging/indexing principles
- [ ] dating conventions
- [ ] uncertain metadata conventions
- [ ] corrections policy

### Rights & reuse

- [ ] literary copyright statement
- [ ] estate rights statement
- [ ] quotation/reuse guidance
- [ ] permissions contact/process
- [ ] distinguish literary rights from third-party image rights where necessary

### Citation

- [ ] article citation guidance
- [ ] book citation guidance
- [ ] topic/entity page citation guidance
- [ ] archive-level citation guidance

---

## 9. Technical and accessibility cleanup

Reference: [`2026-redesign.md`](./2026-redesign.md) → **Technical principles**, **Accessibility**

### Technical

- [ ] keep Eleventy unless a specific limitation justifies migration
- [ ] move repeated archival data into structured front matter/data files
- [ ] use reusable templates
- [ ] use computed metadata where possible
- [ ] generate indexes automatically
- [ ] maintain durable URLs
- [ ] add/verify canonical URLs
- [ ] review sitemap coverage
- [ ] review schema.org metadata
- [ ] review Open Graph metadata
- [ ] minimise client-side JavaScript
- [ ] test Core Web Vitals

### Accessibility

- [ ] review contrast
- [ ] review keyboard navigation
- [ ] add visible focus states
- [ ] verify semantic heading hierarchy
- [ ] review link text
- [ ] verify scalable typography
- [ ] review image alt text
- [ ] ensure decorative images are ignored by assistive technology
- [ ] label search/filter controls
- [ ] ensure colour is not the only information carrier
- [ ] respect reduced-motion preferences

---

## 10. Audit and implement redirects

Reference: [`2026-redesign.md`](./2026-redesign.md) → **URL and redirect policy**

- [ ] inventory existing public URLs
- [ ] identify URLs affected by the new IA
- [ ] prefer retaining article URLs
- [ ] prefer retaining topic URLs
- [ ] create redirect map for moved pages
- [ ] use permanent redirects
- [ ] test old inbound links
- [ ] test indexed URLs
- [ ] test existing citation URLs
- [ ] document redirect rules in the repository
- [ ] run a broken-link crawl before launch

---

## 11. Move biography beneath the Keith section and separately explore the "Post-War Australia" framing

Reference: [`2026-redesign.md`](./2026-redesign.md) → **Biography and archive framing**

This is intentionally the **second-last major redesign action**.

### Structural change

- [ ] move Biography to **Keith → Biography**
- [ ] ensure the homepage no longer functions primarily as a biography
- [ ] create redirects if the biography URL changes

### Separate editorial project

Do not settle this framing incidentally during template work.

Explore:

- [ ] whether **Post-War Australia** should become the principal framing of the archive
- [ ] the appropriate historical date range
- [ ] how Melbourne sits within the broader Australian frame
- [ ] how to describe Keith as journalist, humourist and social commentator
- [ ] what the homepage should say to readers who have never heard of Keith
- [ ] whether "literary archive", "journalistic archive", "cultural archive" or "digital edition" is the strongest descriptor
- [ ] what claims about Keith's significance can be made and evidenced

Deliverable:

- [ ] separate homepage/framing brief before changing the archive's principal proposition

---

## 12. Build chronological digests for deep topics

Reference: [`2026-redesign.md`](./2026-redesign.md) → **Chronological topic digests**

This is intentionally the **final action item**, after the structural redesign is stable.

### Selection criteria

- [ ] identify topics with **10+ articles**
- [ ] prioritise topics spanning multiple years or decades
- [ ] prioritise topics where Keith's changing perspective reveals broader cultural change

Initial candidates:

- [ ] Collins Street
- [ ] Toorak
- [ ] Australian Rules football
- [ ] Wine

### Digest design

For each selected topic:

- [ ] create a short editorial introduction
- [ ] organise coverage chronologically
- [ ] group by decade where useful
- [ ] write short decade-level summaries
- [ ] link representative articles
- [ ] expose related people
- [ ] expose related places
- [ ] expose related institutions
- [ ] expose related themes
- [ ] expose related granular topics
- [ ] show the overall date span and item count

### Purpose

The digest should show how Keith returned to a subject over time and convert deep topical coverage into readable cultural history.

It should not be only an automatically generated article list.

---

# Definition of done

The redesign can be considered substantially complete when:

- [ ] the new entity and theme structure is live
- [ ] article pages function as archival edition pages
- [ ] long-form reading is materially improved
- [ ] the new navigation is live
- [ ] visual design no longer resembles the generic Eleventy theme
- [ ] browse/index pages support genuine exploration
- [ ] search supports meaningful filtering
- [ ] archive authority/editorial policy pages are published
- [ ] redirects have been tested
- [ ] biography has moved beneath the Keith section
- [ ] the separate Post-War Australia framing project has been completed or formally deferred
- [ ] the first chronological topic digest has been published
