# Image Sourcing — Project Instructions for Claude

Companion to the root `CLAUDE.md`. This file governs **how images are found, verified,
downloaded, stored, credited and published** on keithdunstan.org.

Suggested location: `src/assets/images/CLAUDE.md` — Claude Code reads nested `CLAUDE.md`
files, so instructions apply automatically when working in the image directory. Add a
one-line pointer to it from the root `CLAUDE.md`.

> **Not legal advice.** This file encodes a working practice for a non-commercial archive.
> It is not a legal opinion. Where a decision carries real risk, escalate to the estate's
> solicitor rather than resolving it in a commit.

---

## 1. Purpose and Scope

Keith's writing is dense with specific, locatable subject matter — Melbourne streetscapes,
the MCG, Anti-Football League stunts, Bourke Street trams, Barry Humphries, wowser-era
temperance halls, the Sun News-Pictorial newsroom. Images make that writing legible to
readers who never saw any of it.

The archive adds images to:

- **Situate** — show the place, object or event the prose describes
- **Corroborate** — give the reader independent evidence the piece is about a real moment
- **Navigate** — give each article and chapter a visual identity in listings and search

Images are **evidence, not decoration**. An image that does not depict something Keith
actually wrote about does not belong on the page.

### Absolute exclusions

- **No AI-generated or AI-upscaled images.** Ever. This is an archive of a journalist; a
  synthesised photograph of a 1963 Melbourne street would poison the record and undermine
  every genuine item alongside it.
- **No images sourced from Pinterest, Google Images results, blog reposts, eBay listings,
  Facebook groups, or Grokipedia.** These are pointers at best. Trace back to the holding
  institution or original uploader and cite that, or do not use the image.
- **No press agency photography** (Fairfax/Nine, News Corp, AAP, Getty, Newspix) without a
  written licence. Nearly all Sun News-Pictorial, Herald and Age photography from Keith's
  era falls here.
- **No third-party image is ever re-licensed under the site's CC BY-NC 4.0.** The site
  licence covers Keith's text. Third-party images carry their own licence, stated per image.
- **No "public domain" claim asserted over an image the archive did not clear.** Applying a
  licence to a work you don't hold rights in (copyfraud) is exactly the behaviour this
  archive exists to argue against.

---

## 2. Australian Copyright — Working Rules

The archive is Australian, hosted for an Australian audience, and mostly draws on Australian
collections. Australian duration rules govern the first pass.

### The pre-1955 rule

**Photographs taken before 1 January 1955 are out of copyright in Australia.** This is the
single most useful fact in this document. It puts the entire pre-war and immediate post-war
visual record — the Melbourne of Keith's childhood, the wowser era, the 1930s–40s MCG —
into the public domain domestically.

### Photographs taken 1955 onwards

Assume **in copyright** and verify before use. Duration depends on publication status,
whether the photographer is identified, and which amendments applied when. Do not reason
your way to a duration from first principles in a commit message. Check the Australian
Copyright Council's *Duration of Copyright* information sheet, or the holding institution's
own rights statement, and record which one you relied on.

Practical consequence: **for Keith's working life (1950s–2000s), almost no press photograph
is free to use.** Expect to build those pages from public-domain streetscapes, institutional
open-licence collections, the family archive, and Keith's own book covers and ephemera.

### Other rules worth holding

- **Crown copyright** — Commonwealth and State government works run 50 years from creation
  or publication. Useful for NAA, AWM and state government photographic series.
- **Moral rights are perpetual and non-transferable.** Attribute the photographer by name
  wherever the name is known — including for public domain works, where no law compels it.
  It is the correct practice for an archive whose entire premise is attribution.
- **Separate rights layers.** A photograph *of* a painting, sculpture, poster or book jacket
  may be freely licensed while the depicted work is still in copyright. Check both.
- **Australia has no freedom of panorama exception for 2D works**, though buildings,
  sculptures and craft works in public places may generally be photographed. Murals, posters
  and signage are riskier than they look.

### Wikimedia Commons and the two-country problem

Commons requires a work to be free **in the United States as well as its source country**.
An Australian photograph from 1948 is public domain in Australia but may still carry a US
term via the URAA restoration. Practically:

- If it is **already hosted on Commons**, the community has made that assessment. Use it and
  cite the Commons file page.
- If it is **not on Commons** but is pre-1955 Australian, it is still usable on an
  Australian-hosted, Australian-audience archive. Note the reasoning in the credit record.

---

## 3. Licence Decision — Traffic Lights

Run every candidate image through this before download.

### 🟢 Green — use freely, credit anyway

| Status | Notes |
|---|---|
| **CC0 / Public Domain Mark** | No conditions. Credit regardless. |
| **Australian photograph taken pre-1955** | PD in Australia. Credit photographer and holding institution. |
| **"No known copyright restrictions"** (Flickr Commons, SLV, institutional) | Institutional assertion, not a licence. Reproduce their statement verbatim in the credit. |
| **CC BY 4.0 / 3.0 / 2.0** | Attribution only. Cropping and resizing permitted. |
| **CC BY-NC** | Site is non-commercial and CC BY-NC itself — compatible. |

### 🟡 Amber — usable with a specific constraint

| Status | Constraint |
|---|---|
| **CC BY-SA / BY-NC-SA** | ShareAlike binds **adaptations**. Use **unmodified** — no crops, no colour correction, no compositing. Resizing to a display width is fine. If a crop is genuinely required, either find another image or release that derivative under the same SA licence and say so in the credit. |
| **CC BY-ND / BY-NC-ND** | No derivatives at all. Unmodified only. Rules the image out of any hero slot that requires a crop to fit. |
| **Crown copyright, age uncertain** | Verify the 50-year point against creation *and* publication dates before use. |
| **Family archive, photographer unknown** | Usable — the estate holds or controls the physical item — but record what is known about provenance and mark the photographer as unidentified rather than guessing. |

### 🔴 Red — do not use

- Any rights statement containing "In Copyright", "All Rights Reserved", "Rights Reserved —
  Free Access", or "Copyright status unknown" without a completed assessment
- Press agency and syndication material without a written licence
- Book jackets, album covers, film stills and posters where the underlying design is in
  copyright (Keith's *own* jackets are a separate case — see §4)
- Anything where the rights statement cannot be traced to the holding institution's own page

### Keith's own material

Keith's copyright runs to **31 December 2083** and is estate-controlled. Photographs of his
books, dust jackets, bylines, column mastheads and personal papers can be used freely by the
archive, credited to the Keith Dunstan Estate. Note that the *jacket design and cover
artwork* may be a separate copyright held by the publisher or a commissioned illustrator —
worth a note on the record, not a blocker for a scholarly archive use.

---

## 4. Source Hierarchy

Work down this list. Higher sources give better provenance and cleaner rights statements.

### Tier 1 — Australian collecting institutions

| Source | Strengths | Rights signal |
|---|---|---|
| **Trove (NLA)** | Aggregates most of the below; `category=image` searchable via the same API v3 key already in `trove/.env` | Per-item; always follow through to the holding institution's own record |
| **State Library Victoria** | The single best source for Melbourne. Rose Stereograph, Argus negatives, Melbourne streetscapes. Large volume of high-res downloads with no known copyright restrictions | Explicit per-item statement; credit line specified in their conditions of use |
| **State Library NSW** | Strong for Sydney material, Home & Away collection | Explicit per-item |
| **National Archives of Australia** | Government photographic series, immigration and public works | Crown copyright, mostly open |
| **Australian War Memorial** | Keith's wartime-adjacent material, RAAF service context | Per-item, much of it open |
| **Museums Victoria** | Objects, trams, domestic life, Melbourne social history; substantial CC BY holdings | Mostly CC BY 4.0 |
| **Public Record Office Victoria** | Municipal records, building plans, MCG and civic material | Mostly open |
| **City of Melbourne / Melbourne Library Service** | Streetscapes, civic events | Varies |

### Tier 2 — Aggregated open collections

- **Wikimedia Commons** — first stop for any named person, building or event with a
  Wikipedia article. File pages carry structured licence data.
- **Flickr Commons** — institutional photostreams under "no known copyright restrictions".
- **Flickr CC search** — filter by licence ID (see §9). Good for contemporary photographs of
  places Keith described that still stand.
- **Wikimedia Commons categories** — often more productive than search. Start at a
  broad category and walk down the tree rather than guessing filenames.

### Tier 3 — Estate and self-generated

- **The family archive and physical scrapbooks** — the Epicurean Magazine clippings and
  similar. Scan these; they are unique and rights-clear.
- **Photograph it yourself.** A present-day photograph of a building, plaque, pub or stretch
  of Collins Street that Keith wrote about is rights-clean, honest, and can be released CC BY
  by the estate. This is an underused option and often the right answer for post-1955 subjects.

---

## 5. Manual Workflow

Follow this end to end for every image. It is the same shape as the Trove text pipeline:
**capture broadly, verify individually, stage before publishing.**

### Step 1 — Derive the image brief from the text

Read the article or chapter. Extract the concrete, depictable subjects: named people, named
buildings, named streets, named events, named objects, dates. Do not search on themes
("Melbourne nostalgia") — search on nouns ("Bourke Street cable tram 1935").

Record the brief in `todo.md` or the sidecar file before searching, so the search is
answering a question rather than trawling.

### Step 2 — Search, widest source first

Search each Tier 1 institution directly, not via Trove alone — Trove's coverage of image
collections is real but incomplete, and the institution's own interface exposes better rights
metadata. Use date-bounded searches wherever the article gives you a year.

### Step 3 — Verify rights at the holding record

**Never take a rights statement from a search result card or a third-party page.** Open the
institution's own item record. Capture, verbatim:

- Rights / copyright status statement
- Photographer or creator, if named
- Title as given by the institution
- Date, and whether it is exact, approximate (`c. 1935`) or a range
- Persistent identifier or permalink (accession number, Trove work ID, Commons file page)

Run it through §3. If Amber or Red, stop and record why.

### Step 4 — Download the master

Take the **highest resolution available**. Save to
`src/assets/images/_masters/` — this directory is **gitignored**; it is the working copy, not
the published asset. Name using the pattern in §6.

### Step 5 — Write the sidecar

Every master gets a `.json` sidecar with the same base filename, committed to the repo even
though the master itself is not. The sidecar is the archive's rights record and survives
independently of the image file. Schema in §7.

### Step 6 — Derive published assets

Generate display sizes and formats (§6). Respect ND and SA constraints — no cropping where
the licence forbids derivatives.

### Step 7 — Reference in frontmatter and body

Hero via frontmatter, inline via shortcode. Schema in §8.

### Step 8 — Verify the rendered credit

Build locally and confirm the caption and credit render correctly before pushing. An image
published without its credit is a licence breach even if the sidecar is perfect.

---

## 6. File Naming, Formats and Directories

### Directory structure

```
src/assets/images/
├── CLAUDE.md                       # this file
├── _masters/                       # gitignored — highest-res originals
│   ├── slv-1935-bourke-street-cable-tram.tif
│   └── slv-1935-bourke-street-cable-tram.json    # sidecar IS committed
├── heroes/                         # 1600w and 800w derivatives
├── inline/                         # 1200w and 600w derivatives
└── thumbs/                         # 400w for listings and search results
```

### Naming pattern

```
[source-prefix]-[year]-[kebab-case-subject].[ext]
```

- `slv-1935-bourke-street-cable-tram.jpg`
- `commons-1968-barry-humphries-portrait.jpg`
- `estate-1972-keith-dunstan-desk-sun-newsroom.jpg`
- `own-2026-collins-street-block-arcade.jpg`

Source prefixes: `slv`, `slnsw`, `nla`, `naa`, `awm`, `mv` (Museums Victoria), `prov`,
`commons`, `flickr`, `estate`, `own`.

Use the **subject's date**, not the download date. Approximate dates use the year alone;
record the `c.` qualifier in the sidecar, not the filename.

### Formats and sizes

| Use | Widths | Format |
|---|---|---|
| Hero | 1600, 800 | WebP with JPEG fallback |
| Inline | 1200, 600 | WebP with JPEG fallback |
| Thumbnail | 400 | WebP |

Keep masters lossless where the source provides it. Derivatives at quality 82 WebP / 85 JPEG.
Historical photographs: **do not** sharpen, denoise, colourise or "restore". Straightening a
scan and correcting exposure on the archive's own scans is acceptable and should be noted.

---

## 7. The Sidecar Schema

`src/assets/images/_masters/[basename].json` — committed. This is the authoritative rights
record and the source for rendered credits.

```json
{
  "id": "slv-1935-bourke-street-cable-tram",
  "title": "Bourke Street looking east, showing cable tram",
  "titleSource": "institution",
  "creator": "Rose Stereograph Co.",
  "creatorNote": "Photographer not individually identified",
  "date": "1935",
  "dateQualifier": "circa",
  "holder": "State Library Victoria",
  "collection": "Rose Stereograph Company collection",
  "identifier": "H32492/4521",
  "sourceUrl": "https://viewer.slv.vic.gov.au/?entity=IE1234567",
  "rightsStatement": "No known copyright restrictions",
  "rightsStatementVerbatim": true,
  "licence": "PDM",
  "licenceUrl": "https://creativecommons.org/publicdomain/mark/1.0/",
  "derivativesPermitted": true,
  "assessedBy": "Jack Dunstan",
  "assessedDate": "2026-08-16",
  "assessmentNote": "Pre-1955 Australian photograph; SLV states no known copyright restrictions.",
  "usedIn": [
    "src/articles/bulletin/the-last-cable-tram.md"
  ],
  "altText": "A cable tram travelling east along Bourke Street, flanked by awninged shopfronts and pedestrians in hats and overcoats."
}
```

**`rightsStatementVerbatim: true`** means `rightsStatement` is the institution's exact
wording. If you have paraphrased, set it `false` and explain in `assessmentNote`. Never
paraphrase silently.

**`derivativesPermitted: false`** for ND and for SA-where-you-don't-want-to-relicense. The
build should treat this as a hard block on cropping.

---

## 8. Frontmatter and Template Integration

### Hero image — frontmatter

Extends the existing frontmatter block. Optional field; omit entirely rather than leaving empty.

```yaml
---
title: The Last Cable Tram
date: 1962-07-01
summary: Keith Dunstan rides Melbourne's final cable tram service on its closing run.
hero:
  id: slv-1935-bourke-street-cable-tram
  caption: Bourke Street, looking east, in the cable tram era.
  crop: wide
tags:
  - Bourke Street
  - Melbourne
---
```

`id` resolves against the sidecar via an Eleventy data file. Caption is **editorial** — the
archive's own words describing why the image is here. It is distinct from the credit, which
is generated from the sidecar and must not be hand-written into the Markdown.

`crop` is honoured only where `derivativesPermitted` is true; otherwise the build falls back
to a contained, uncropped display and logs a warning.

### Inline image — shortcode

```njk
{% image "slv-1935-bourke-street-cable-tram",
         "The cable tram Keith describes, photographed some thirty years earlier." %}
```

Renders as:

```html
<figure class="archive-figure">
  <picture>
    <source srcset="/assets/images/inline/slv-1935-bourke-street-cable-tram-1200.webp" type="image/webp">
    <img src="/assets/images/inline/slv-1935-bourke-street-cable-tram-1200.jpg"
         alt="A cable tram travelling east along Bourke Street…"
         width="1200" height="800" loading="lazy" decoding="async">
  </picture>
  <figcaption>
    <span class="figure-caption-text">The cable tram Keith describes, photographed some thirty years earlier.</span>
    <span class="figure-credit">
      <cite>Bourke Street looking east, showing cable tram</cite>, Rose Stereograph Co., c. 1935.
      <a href="https://viewer.slv.vic.gov.au/?entity=IE1234567">State Library Victoria</a>.
      No known copyright restrictions.
    </span>
  </figcaption>
</figure>
```

### Data file

`src/_data/images.js` globs the sidecars at build time and exposes them as a lookup. Build
should **fail loudly** on a missing `id`, a missing `altText`, or a `licence` field that is
not in the permitted set — a silently missing credit is worse than a broken build.

### Credit format — TASL

**T**itle, **A**uthor, **S**ource, **L**icence. Every credit contains all four, or an explicit
note that one is unknown ("Photographer unidentified"). Link the source. Link the licence
where a CC licence applies; state the institutional wording verbatim where it does not.

### Alt text

Alt text is **description for someone who cannot see the image** — not a caption, not a
credit, not keywords. Describe what is visible and materially relevant to why the image is
on the page. Aim for a single clear sentence. Do not open with "Image of" or "Photograph of".

---

## 9. Search Techniques by Source

### Trove (API v3, existing key)

`category=image` returns pictures, photographs and objects. As with the Bulletin work,
expect the response shape to differ from the newspaper category — inspect the raw JSON
before writing a parser rather than assuming it mirrors `category=newspaper`.

Useful parameters: `l-availability=y/f` for freely available online, `l-decade` and `l-year`
for date bounding, `l-artType` for narrowing. Always follow the record through to the
holding institution before trusting a rights field.

> **Data agreement note.** The Trove Data Agreement expires 31 December 2026 and requires raw
> API results in `trove/output/` to be deleted at that point. Image sidecars are the
> archive's own records, not raw API output, and are not affected — but keep any bulk image
> JSON responses inside `trove/output/` so the existing deletion process catches them.

### Wikimedia Commons

Prefer category traversal to search. For a person, start from the Wikipedia article →
Commons category link → walk subcategories.

The API returns structured licence data:

```
https://commons.wikimedia.org/w/api.php
  ?action=query&generator=search&gsrsearch=<query>&gsrnamespace=6
  &prop=imageinfo&iiprop=url|extmetadata&format=json
```

`extmetadata` yields `LicenseShortName`, `Artist`, `Credit`, `LicenseUrl` and
`UsageTerms` — enough to populate most of a sidecar automatically. **The `Artist` field is
raw HTML**; strip tags before storing.

### Flickr

Licence IDs for the API's `license` parameter:

| ID | Licence |
|---|---|
| 1 | CC BY-NC-SA |
| 2 | CC BY-NC |
| 3 | CC BY-NC-ND |
| 4 | CC BY |
| 5 | CC BY-SA |
| 6 | CC BY-ND |
| 7 | No known copyright restrictions (Flickr Commons) |
| 8 | United States Government Work |
| 9 | CC0 |
| 10 | Public Domain Mark |

For the archive, request `license=2,4,7,9,10` to return only Green-tier results directly.

### State Library Victoria

Search the catalogue, then open the digital viewer for the download options and the
conditions-of-use statement. SLV specifies a preferred credit line — use theirs, not a
paraphrase.

---

## 10. Claude Prompt Templates

### Template A — Image research brief from an article

```
Read the attached article from the Keith Dunstan archive.

Produce an image research brief. For each depictable subject in the text, give:
- The subject as a concrete search term (named person, building, street, event, object)
- The date or date range implied by the article
- Which Tier 1 source is most likely to hold it (SLV, SLNSW, NLA, NAA, AWM,
  Museums Victoria, PROV) and why
- Whether the pre-1955 rule is likely to apply
- A suggested search string for that source

Rank subjects by how central they are to the piece. Flag any subject where the only
likely source is press agency photography, so I can rule it out early.

Do not search. Do not suggest images you have not been asked to verify.
Output as a Markdown table.
```

### Template B — Sidecar from an institutional record

```
I am pasting the item record from [institution]. Produce the JSON sidecar per the
schema in src/assets/images/CLAUDE.md.

Rules:
- Copy the rights statement VERBATIM. Set rightsStatementVerbatim accordingly.
- Do not infer a photographer where the record does not name one — use creatorNote.
- Do not infer an exact date from an approximate one. Use dateQualifier.
- If the rights statement does not map cleanly to a licence in the permitted set,
  set licence to "UNRESOLVED" and explain in assessmentNote. Do not guess.
- Leave assessedBy and assessedDate for me to fill.
- Draft altText: one sentence, describing what is visible, no "photograph of".

[paste record]
```

### Template C — Rights triage

```
Assess this image against the traffic-light system in src/assets/images/CLAUDE.md.

Give: the light (green/amber/red), the specific rule that determines it, any
constraint on derivatives, and what the credit line should say.

If you cannot determine the light from the information given, say what is missing
rather than assuming. Assume Australian copyright law and an Australian-hosted,
non-commercial archive.

[paste record or URL]
```

---

## 11. Future Automation — `/images/` Pipeline Spec

Mirror the `/trove/` pattern: a Python toolchain outside `src/`, staging output before
manual promotion. **Do not build this until the manual workflow has run over thirty or forty
images** — the manual passes are what reveal the real edge cases in institutional metadata.

```
/images/
├── .env                      # gitignored — API keys
├── requirements.txt
├── search_commons.py         # Commons API → candidate JSON
├── search_flickr.py          # Flickr API, licences 2,4,7,9,10 only
├── search_trove_images.py    # Trove v3 category=image
├── build_sidecar.py          # candidate JSON → sidecar, flags UNRESOLVED
├── fetch_masters.py          # download highest-res for approved candidates
├── derive.py                 # Pillow: WebP/JPEG derivatives, honours derivativesPermitted
├── audit.py                  # re-checks every sidecar sourceUrl still resolves
└── output/
    ├── candidates/           # search results awaiting human review
    ├── approved/             # human-approved, sidecar written
    └── rejected/             # with rejection reason recorded
```

**Non-negotiable design constraints:**

- **No script ever writes directly to `src/`.** Human promotion only, exactly as with the
  Trove text pipeline.
- **No script assigns a licence.** Scripts extract and normalise; a human sets
  `assessedBy`. Anything ambiguous lands as `UNRESOLVED` and stops.
- **Respect rate limits and robots.txt on every institutional endpoint.** The archive
  publishes a principled crawler policy of its own; it does not get to ignore other people's.
- **No bulk downloading from any source whose terms prohibit it.** The ProQuest lesson
  applies generally: an institutional relationship is worth more than a batch of files.

`audit.py` should run quarterly alongside the existing crawler user-agent review, checking
that every `sourceUrl` still resolves and every `rightsStatement` still matches the live
record. Institutions do revise rights assessments, occasionally in the restrictive direction.

---

## 12. Site-Level Requirements

- **`/credits/` page** — generated from the sidecars. Every image on the site, with title,
  creator, holder, source link and licence. Machine-readable and human-browsable.
- **Licence separation** — the site footer and the CC BY-NC 4.0 statement must say
  explicitly that the licence covers Keith Dunstan's text, and that third-party images are
  licensed as stated on each item.
- **`llms.txt` and TDMRep** — extend the existing files to state the image position: images
  are third-party licensed and are not covered by any permission granted over the site's text.
- **Takedown path** — a clearly signposted contact route for rights holders, with a stated
  commitment to remove on request pending assessment. For an archive working at the edges of
  orphan-work territory, a visible, responsive takedown process is the single most effective
  risk control available.

---

## 13. What Claude Must Not Do

- Do not generate, synthesise, upscale, colourise or "restore" any historical image
- Do not assert a licence, rights status or public-domain claim that is not stated on the
  holding institution's own record
- Do not paraphrase a rights statement while `rightsStatementVerbatim` is `true`
- Do not infer a photographer, an exact date, or a collection where the record does not give one
- Do not crop, composite or colour-correct any image where `derivativesPermitted` is `false`
- Do not write image files or sidecars directly into `src/` — stage them for manual promotion
- Do not add an image to a page without its caption, alt text and credit in the same commit
- Do not source images from Google Images, Pinterest, blog reposts, or AI-generated
  encyclopaedia articles
- Do not apply the site's CC BY-NC 4.0 licence to any third-party image
- Do not treat this file as legal advice, or resolve a genuine legal question inside it
