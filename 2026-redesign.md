# Keith Dunstan Archive — 2026 Redesign Reference

## Purpose

This document defines the design, information architecture, editorial presentation and authority model for the next major iteration of [keithdunstan.org](https://keithdunstan.org/).

The site has matured beyond the needs of a standard Eleventy theme. It should now present itself as a substantial literary and cultural archive: a primary-source corpus documenting Australian life, especially Melbourne and post-war Australia, through the writing of Keith Dunstan.

The redesign should sit between two complementary models:

- **The Newspaper Archive** — contemporary Australian newspaper modernism, strong typography, publication context, dates, columns, mastheads and editorial structure.
- **The Cultural Atlas** — a networked archive that allows readers to explore people, places, institutions, events, publications, subjects and themes across decades.

The site should remain contemporary rather than nostalgic. Avoid sepia, fake paper textures, typewriter effects or decorative historicism. The historical authority should come from the material itself.

## Core design principles

### 1. The corpus is the primary object

The site is no longer principally a biography with writing attached. The writing itself should be the main object of discovery.

Primary user actions should be:

- Read
- Explore
- Search

Biography, career history and legacy remain important but should support the corpus rather than dominate the homepage or primary navigation.

### 2. Newspaper modernism, not newspaper pastiche

The visual language should draw on Australian print journalism without imitating an old newspaper.

Use:

- strong typographic hierarchy
- prominent dates and publication names
- fine rules and disciplined grids
- editorial serif typography
- compact sans-serif metadata
- archival photography and publication imagery where useful
- restrained use of colour
- generous whitespace
- contemporary responsive layout

Avoid:

- fake ageing
- torn-paper effects
- faux newsprint textures
- typewriter fonts
- ornamental nostalgia

### 3. Readability is a first-order requirement

Keith's writing is the product. Long-form reading should be unusually comfortable.

Target reading-page typography:

- desktop body copy: **19–21px**
- line length: **68–74 characters**
- line height: **1.55–1.7**
- serif typeface for article and book text
- sans-serif for metadata, navigation and interface elements
- dark charcoal text rather than pure black
- slightly warm page background
- strong italics
- proper curly quotation marks, apostrophes and dashes
- visible but controlled paragraph spacing
- no permanent sidebars that compress the reading column

Reading pages should prioritise text over widgets, cards or persistent navigation.

### 4. Authority should be visible

The archive should present itself as an edited literary estate publication.

Use the authority statement:

> **Published by the Keith Dunstan Literary Estate**

This should appear consistently in appropriate site-wide contexts, including About, footer, article metadata or edition apparatus where suitable.

Authority should also be established through transparent editorial practice:

- purpose and scope of the archive
- editorial principles
- transcription policy
- provenance of texts
- corrections policy
- rights and reuse
- citation guidance
- contributors and acknowledgements
- known publication status and corpus coverage

### 5. Findability should work at several levels

Readers should be able to move through the archive in different ways:

- direct search
- publication
- date
- decade
- book
- person
- place
- organisation
- event
- subject
- curated theme
- related article
- chronology

The granular topic system should be preserved because it provides value for search engines, researchers and specialist users. It should no longer carry the burden of being the main public-facing information architecture.

---

# Information architecture

## Entity layer

The 3,000+ granular topics should gain an over-arching entity classification.

Use:

- **People**
- **Places**
- **Organisations**
- **Events**
- **Publications**
- **Subjects**

This can be implemented within the current tag structure if practical, or through a separate index/metadata layer that maps existing topics to entity types.

The goal is to retain all existing granular topic URLs and indexing while providing meaningful higher-level browsing.

### Requirements

- preserve existing topic pages unless there is a compelling reason to change them
- do not remove granular topics from search indexing
- retain topics for SEO, academic research and precise searching
- remove **Topics** as a primary top-level navigation item
- keep **Topics** accessible under **Explore**
- create index pages for each entity class
- support cross-linking between entity pages and article edition pages
- build redirects for any changed URLs

---

# Curated themes

Create a public-facing thematic layer above individual topics.

Initial curated themes:

- **Melbourne**
- **Australian character**
- **Politics & power**
- **Food & drink**
- **Cities & suburbs**
- **Architecture & planning**
- **Media & journalism**
- **Social change**
- **Travel**
- **Wine**
- **Institutions**
- **Technology & progress**

Each theme page should act as an editorial gateway, not merely a tag list.

A theme page may contain:

- short editorial introduction
- selected representative articles
- related books
- important people
- important places
- related publications
- related granular topics
- relevant decades
- latest additions
- eventually, chronological digests where the corpus is deep enough

Themes should remain selective and curated. They are not a replacement for the full topic index.

---

# Article pages as edition pages

Article pages should be redesigned as archival edition pages.

The original article remains the primary content, but should be framed by consistent archival and editorial apparatus.

## Recommended structure

### Header

- article title
- publication
- first publication date
- column or series name, if applicable
- short editorial synopsis or contextual introduction, where available

### Article text

The article should be given a clear, quiet reading environment with minimal visual interference.

### About this item

Use a consistent metadata block such as:

```markdown
### About this item

**Author** Keith Dunstan  
**First published** *The Bulletin*, 13 March 1984  
**Column** Batman's Melbourne  
**Source** Trove / original clipping / estate copy  
**Transcription** Keith Dunstan Archive  
**Last checked** 14 November 2026  
**Permanent URL** …  
**Rights** Literary Estate of Keith Dunstan  
**Cite this item** Copy citation
```

Where the underlying data exists, metadata should be generated automatically from front matter or structured content rather than manually repeated.

### Subjects

Display the relevant topic/entity relationships clearly:

```markdown
### Subjects

Melbourne · Germaine Greer · Sunday trading · Collins Street …
```

Entity types should be available to templates so that subjects can later be grouped intelligently where useful.

### Continue exploring

Provide contextual onward journeys rather than generic "related posts".

Examples:

```markdown
### Continue exploring

**Melbourne in 1974**  
**Melbourne in 1994**  
**More from The Bulletin**  
**Keith on progress**
```

Potential recommendation logic:

- same place in another decade
- same theme in another decade
- same publication
- same column
- same subject
- same person
- related book extract
- previous/next item in a chronology

### Citation

Support a visible **Cite this item** action.

Citation output should include, at minimum:

- Keith Dunstan
- article title
- original publication
- original publication date
- Keith Dunstan Archive
- permanent URL
- access date where appropriate

A plain-text citation is sufficient initially. Additional formats can be added later.

---

# Navigation

Adopt a navigation structure based on reader intent rather than the underlying Eleventy content structure.

## Primary navigation

### **Read**

- Books
- Articles
- Publications
- Latest additions

### **Explore**

- Themes
- People
- Places
- Timeline
- Topics

### **Keith**

- Biography
- Career
- Bibliography
- Legacy

### **About the archive**

- About
- Editorial principles
- Rights & reuse
- Contact

### **Search**

Search should remain prominent and directly accessible from the primary interface.

## Navigation principles

- the archive should feel shallower, not deeper
- primary navigation should describe user goals
- granular topics should remain available without dominating the interface
- breadcrumbing should be used where it improves orientation
- publication, theme, entity and chronology pages should support lateral navigation
- changed navigation URLs should receive permanent redirects

---

# Biography and archive framing

Keith's biography should become a subpage within the **Keith** section.

The homepage should not primarily be a biographical page.

A separate project should explore a broader framing of the archive around **post-war Australia** rather than "Melbourne, observed".

This should not be implemented as part of the first structural redesign because it requires editorial exploration.

Questions for that later project include:

- Is "Post-War Australia" the strongest description of the corpus?
- What date range should define the phrase?
- How should Melbourne remain visible within the national framing?
- How should Keith's roles as journalist, humourist, social observer and cultural commentator be expressed?
- What homepage proposition best serves readers who do not already know Keith Dunstan?
- Should the archive describe itself as a literary archive, journalistic archive, cultural archive, digital edition or a combination of these?
- What claims about Keith's significance can be made confidently and supported by evidence?

The redesign should therefore make room for a future homepage reframing without depending on one now.

---

# Search and discovery

Search should become a first-class archive interface.

Desired capabilities include:

- full-text search
- filter by publication
- filter by date or decade
- filter by content type
- filter by theme
- filter by entity type
- filter by topic
- sort by relevance
- sort chronologically

The implementation should remain compatible with a static Eleventy architecture where practical.

Search results should expose meaningful context rather than only titles and excerpts.

Useful result metadata:

- date
- publication
- column
- content type
- selected subjects
- selected theme
- short excerpt with highlighted match

---

# Index and browse pages

The redesign should create strong index pages that work as destinations in their own right.

Priority indexes:

- Themes
- People
- Places
- Organisations
- Events
- Publications
- Subjects
- Timeline
- Topics
- Books
- Articles
- Latest additions

These pages should avoid giant undifferentiated tag clouds.

Preferred browse patterns include:

- alphabetical index
- grouped index
- most-covered entities
- decade filters
- search-within-index
- editorially featured entries
- article counts
- chronology indicators

---

# Chronological topic digests

This is a later-stage enhancement and should be implemented only after the structural redesign is stable.

Where a topic has sufficient breadth — initially **10 or more articles across a meaningful period** — build a chronological digest that shows how Keith returned to it over time.

Strong initial candidates include:

- Collins Street
- Toorak
- Australian Rules football
- Wine

A digest should be more than a list of articles.

Potential structure:

```markdown
# Collins Street

Keith Dunstan wrote about Collins Street across several decades, using it as a way to observe changes in retail, architecture, class, business and Melbourne identity.

## 1960s
[editorial summary]

- article
- article

## 1970s
[editorial summary]

- article
- article

## 1980s
[editorial summary]

- article
- article

## Related subjects
Melbourne · Retail · Architecture · Whelan the Wrecker · Department stores …
```

The aim is to show change over time and to convert deep topical coverage into narrative cultural history.

These digests may later become one of the archive's strongest distinctive features.

---

# URL and redirect policy

The redesign should preserve durable URLs wherever possible.

Where structure changes require new URLs:

- create permanent redirects
- avoid breaking indexed article URLs
- avoid breaking topic URLs
- preserve external inbound links
- preserve citations already made to the archive
- document redirect mappings in the repository
- test redirects before deployment

Navigation labels may change without changing URLs where that reduces unnecessary migration work.

---

# Visual system

## Character

Target:

> **Contemporary Australian newspaper modernism + cultural atlas**

The visual system should communicate:

- editorial confidence
- archival authority
- readability
- curiosity
- Melbourne/Australian identity without cliché
- modernity rather than nostalgia

## Typography

The typography system should distinguish clearly between:

- reading text
- headlines
- metadata
- interface labels
- archival apparatus
- captions

Suggested pattern:

- serif: article body, book extracts, substantial editorial introductions
- sans serif: navigation, metadata, filters, dates, labels, buttons

## Colour

Use a restrained palette.

Recommended direction:

- warm off-white reading background
- dark charcoal primary text
- muted neutral rules and metadata
- one strong accent colour
- optional secondary archival colour for publication/entity distinctions

Avoid excessive colour coding.

## Layout

- use strong grids
- maintain generous page margins
- allow article pages to become visually quieter than browse pages
- make dates and publication metadata easy to scan
- use cards selectively rather than everywhere
- avoid dashboard-like density on reading pages
- design mobile reading as carefully as desktop

---

# Editorial authority and archive documentation

Create or expand the following pages:

## About

Explain:

- what the archive contains
- why it exists
- who publishes and maintains it
- relationship to Keith Dunstan's literary estate
- current state of digitisation/publication

## Editorial principles

Document:

- transcription approach
- treatment of spelling and punctuation
- treatment of obvious print/OCR errors
- editorial additions
- contextual introductions
- tagging and subject indexing
- dating conventions
- handling of uncertain metadata
- corrections

## Rights & reuse

Clarify:

- copyright status
- estate ownership
- permitted quotation/reuse
- permissions process
- rights in source images where different from literary copyright

## Citation guidance

Provide simple recommended citation formats for:

- article
- book
- topic/entity page
- archive as a whole

---

# Technical principles

The redesign should not require abandoning Eleventy unless a concrete technical limitation is identified.

Prefer:

- structured front matter
- reusable templates
- computed metadata
- generated indexes
- static search-compatible structures
- durable URLs
- accessible semantic HTML
- minimal client-side JavaScript
- good Core Web Vitals
- schema.org metadata where appropriate
- strong Open Graph and social metadata
- sitemap coverage
- canonical URLs

The implementation should favour durability over novelty.

---

# Accessibility

The redesign should meet contemporary accessibility expectations.

Minimum requirements:

- WCAG-conscious contrast
- keyboard-accessible navigation
- visible focus states
- semantic heading hierarchy
- meaningful link text
- scalable typography
- alt text for meaningful images
- decorative images excluded from the accessibility tree
- search and filter controls with clear labels
- no information conveyed through colour alone
- reduced-motion respect if motion is introduced

---

# Success criteria

The redesign is successful if:

1. a first-time visitor can understand what the archive is within seconds
2. a reader can comfortably read a long article on desktop or mobile
3. a researcher can find a specific person, place, publication or subject
4. a general reader can discover writing without already knowing what to search for
5. article pages visibly function as authoritative archival editions
6. the Literary Estate's stewardship is clear
7. the granular topic system remains available without overwhelming the primary interface
8. the site gains a distinctive visual identity independent of its original Eleventy theme
9. old URLs and citations continue to work
10. the architecture can support future chronological cultural digests and a broader "Post-War Australia" framing
