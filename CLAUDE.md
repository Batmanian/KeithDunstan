# Keith Dunstan — Project Instructions for Claude

This file provides context for Claude (via Claude Code or the Claude.ai interface) when working on this repository.

---

## Project Overview

This is the digital archive of **Keith Dunstan** (1925–2013), Australian journalist and author. The site preserves his books and magazine articles for public access. Copyright is held by his literary estate and managed by his family.

The site is built with **Eleventy (11ty)** using the 11straps boilerplate (Eleventy + Bootstrap 5), compiled with Gulp, and deployed via **Netlify** from this GitHub repository.

Live site: https://keithdunstan.org  
Repository: https://github.com/JackDunstan/KeithDunstan

---

## Repository Structure

```
/
├── src/
│   ├── books/                        # All books, one folder per title
│   │   └── [book-slug]/
│   │       ├── 0-introduction.md
│   │       ├── 1-chapter-name.md
│   │       └── ...
│   ├── articles/                     # All magazine/periodical articles
│   │   ├── bulletin/                 # The Bulletin (bulk of articles)
│   │   ├── walkabout-magazine/
│   │   ├── the-australian-gourmet/
│   │   └── [publication-slug]/       # Add new publications as needed
│   ├── _includes/                    # Nunjucks layout templates
│   └── ...
├── dev/                              # Dev build output (do not edit)
├── docs/                             # Production build output (do not edit)
├── ocr/                              # Working directory for OCR source files
├── _redirects                        # Netlify redirect rules (legacy URL support)
├── .eleventy.js
├── gulpfile.js
├── package.json
└── CLAUDE.md                         # This file
```

---

## URL Structure

```
/books/wowsers/1-chapter-title/
/books/no-brains-at-all/0-introduction/
/articles/bulletin/article-title/
/articles/walkabout-magazine/article-title/
/articles/the-australian-gourmet/article-title/
```

Legacy `/posts/` URLs are redirected via `_redirects` — do not use `/posts/` paths for any new content.

---

## Current Book Catalogue

| Folder | Title |
|--------|-------|
| `a-day-in-the-life-of-australia` | A Day in the Life of Australia |
| `my-life-with-the-demon` | My Life with the Demon |
| `no-brains-at-all` | No Brains At All |
| `ratbags` | Ratbags |
| `supporting-a-column` | Supporting a Column |
| `the-australian-uppercrust-book` | The Australian Upper Crust Book |
| `wowsers` | Wowsers |

---

## Current Article Collections

| Folder | Publication |
|--------|-------------|
| `bulletin` | The Bulletin |
| `walkabout-magazine` | Walkabout Magazine |
| `the-australian-gourmet` | The Australian Gourmet |

When adding a new publication, create a new folder under `src/articles/` using kebab-case of the publication name.

---

## Frontmatter Template

Every Markdown file must include this frontmatter block. Do not omit any field.

```yaml
---
title: Chapter or Article Title
date: YYYY-MM-DD
summary: One or two sentence description of this chapter or article.
tags:
  - Tag One
  - Tag Two
---
```

**date:** Use the book's original publication date for all chapters within a book. For articles, use the original issue date.

**summary:** Concise, factual, third person. Should function as a search result snippet.

**tags:** See tagging rules below.

---

## Tagging Rules

Tags are **granular proper nouns** — specific people, places, and organisations mentioned in the content. Not broad thematic categories.

**Use:**
- Full personal names: `Sir Keith Murdoch`, `Sid Caesar`, `Colin Bednall`
- Specific places: `Honolulu`, `New York`, `London`, `Ballarat`
- Organisations: `Australian Journalists Association`, `Herald and Weekly Times`
- Broad thematic terms only when strongly central to the entire piece: `Autobiography`, `Cricket`

**Do not use:**
- Vague descriptors: `History`, `Writing`, `Interesting`
- Partial names where the full name is known
- Duplicates differing only in capitalisation

Aim for 5–15 tags per file. Generate by reading the full text and extracting every significant proper noun.

---

## Navigation Links

Each chapter ends with an HTML navigation link to the next chapter:

```html
<hr>
Continue to [next chapter title]: <a href="{{ '/books/[book-slug]/[next-filename]' | url }}">[Next Chapter Title]</a>
```

For articles, omit the navigation link unless there is a logical next piece.  
The final chapter of a book links back to the book index page if one exists.

---

## Prose Conventions

When transcribing or cleaning OCR text:

- Preserve Keith Dunstan's voice exactly — do not modernise vocabulary, structure, or punctuation
- Australian English throughout: `colour`, `realise`, `honour`, `organise`
- Dialogue uses single quotes: `'like this'`
- Line breaks within dialogue use `<br>` tags
- Em dashes rendered as ` — ` (space, em dash, space)
- Preserve original paragraph breaks
- Do not add subheadings that do not appear in the original printed text
- Rejoin end-of-line hyphenation from print layout (e.g. `fas-\ncinating` → `fascinating`)

---

## OCR and Transcription Workflow

### Books (physical copies)

1. **Scan** using iPhone — Notes app, Files app, or Continuity Camera direct to Mac
2. **Upload** the scan (PDF or images) to Claude with the prompt template below
3. **Save output** as a `.md` file in `src/books/[book-slug]/`
4. **Review** lightly in VS Code — check for OCR errors, `[?]` flags, malformed characters
5. **Commit and push** — Netlify builds and deploys automatically

### Magazine Articles

1. **Source** from Trove (NLA), State Library Victoria (ProQuest), or other library databases
2. **Extract text** directly if already digitised; scan physical copies if not
3. **Process** with the Claude prompt template below
4. **File** under `src/articles/[publication-slug]/` with correct publication date
5. **Commit and push**

### Claude Transcription Prompt

Use this prompt when uploading a scanned chapter or article to Claude:

```
Transcribe the text from these scanned pages accurately.

Rules:
- Preserve the author's exact wording, punctuation and paragraph structure
- Australian English spelling throughout
- Dialogue uses single quotes
- Em dashes rendered as ` — ` (space, em dash, space)
- Rejoin any words hyphenated across line breaks in the original print layout
- Flag any characters you are uncertain about with [?]
- Do not add commentary, headings, or formatting not present in the original

Output a complete Markdown file with this frontmatter:

---
title: [Chapter or article title as it appears in the source]
date: [Original publication date YYYY-MM-DD]
summary: [One or two sentence factual description, third person]
tags:
  - [All significant proper nouns from the text]
---

[transcribed text]

<hr>
Continue to [next chapter title]: <a href="{{ '/books/[book-slug]/[NEXT_FILENAME]' | url }}">[Next Chapter Title]</a>
```

Replace `[NEXT_FILENAME]` and the link path before committing. For articles, omit the navigation block.

---

## Build Commands

```bash
npm install          # Install dependencies
npm run watch        # Local development with live reload
npm run build-dev    # Build to /dev (unminified)
npm run build        # Build to /docs (minified, production)
```

Pushes to `master` trigger automatic Netlify build and deploy.

---

## What Claude Should Not Do

- Do not alter Keith Dunstan's prose — transcription is not editing
- Do not change Australian/British spellings to American English
- Do not invent tag values — only tag proper nouns present in the text
- Do not add new frontmatter fields without discussion
- Do not write to `/dev` or `/docs` — these are build output folders
- Do not use `/posts/` paths for any new content — use `/books/` or `/articles/`
