#!/usr/bin/env python3
"""Recover vault .md files for Bulletin 1969 and 1970 from built docs HTML."""

import os
import re
import html
from pathlib import Path
from bs4 import BeautifulSoup
import html2text

DOCS_BASE = Path("/Users/jack2026/Documents/repos/Untitled/KeithDunstan/docs/articles/bulletin")
VAULT_BASE = Path("/Users/jack2026/Documents/repos/Untitled/KeithDunstan/vault/articles/bulletin")

h = html2text.HTML2Text()
h.body_width = 0
h.protect_links = True
h.wrap_links = False


def body_html_to_markdown(div):
    # Serialise the inner HTML of the article-body div
    inner = div.decode_contents()
    md = h.handle(inner)
    # html2text uses * for italic/bold; convert **text** and _text_ from source
    # Strip trailing whitespace and normalise blank lines
    lines = md.split("\n")
    result = []
    blank_count = 0
    for line in lines:
        stripped = line.rstrip()
        if stripped == "":
            blank_count += 1
            if blank_count <= 1:
                result.append("")
        else:
            blank_count = 0
            result.append(stripped)
    return "\n".join(result).strip()


def recover_article(html_path: Path, slug: str, year: str):
    text = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")

    # Title
    h1 = soup.find("h1", class_="display-3")
    if not h1:
        print(f"  WARN: no h1 in {html_path}")
        return None
    title = html.unescape(h1.get_text())

    # Date
    time_tag = soup.find("time", attrs={"data-pagefind-meta": "date"})
    if not time_tag:
        print(f"  WARN: no date in {html_path}")
        return None
    date = time_tag["datetime"]

    # Summary — desktop sidebar lead paragraph (not the mobile duplicate in header)
    # The sidebar div has class "bg-light p-4 rounded d-none d-md-block"
    sidebar = soup.find("div", class_=lambda c: c and "bg-light" in c and "d-none" in c and "d-md-block" in c)
    summary = ""
    if sidebar:
        lead_p = sidebar.find("p", class_="lead")
        if lead_p:
            summary = lead_p.get_text().strip()
    if not summary:
        # Fallback: mobile summary in header
        mobile_p = soup.find("p", class_=lambda c: c and "lead" in c and "order-2" in c and "d-md-none" in c)
        if mobile_p:
            summary = mobile_p.get_text().strip()

    # Tags — from sidebar topic jump list
    tags = []
    if sidebar:
        for li in sidebar.find_all("li", class_="topic-jump-item"):
            a = li.find("a", class_="link-secondary")
            if a:
                tags.append(a.get_text().strip())
    tags.sort(key=lambda t: t.lower())

    # Article body
    body_div = soup.find("div", class_="article-body")
    if not body_div:
        print(f"  WARN: no article-body in {html_path}")
        return None
    body_md = body_html_to_markdown(body_div)

    return {
        "title": title,
        "date": date,
        "summary": summary,
        "tags": tags,
        "body": body_md,
    }


def write_md(vault_path: Path, data: dict):
    vault_path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["---"]
    lines.append(f"title: {data['title']}")
    lines.append(f"date: {data['date']}")
    lines.append(f"summary: {data['summary']}")
    lines.append("categories:")
    lines.append("- The Bulletin")
    lines.append("tags:")
    for tag in data["tags"]:
        lines.append(f"  - {tag}")
    lines.append("---")
    lines.append("")
    lines.append(data["body"])
    lines.append("")
    vault_path.write_text("\n".join(lines), encoding="utf-8")


def process_year(year: str):
    docs_year = DOCS_BASE / year
    vault_year = VAULT_BASE / year

    if not docs_year.exists():
        print(f"No docs for {year}")
        return

    articles = sorted(docs_year.iterdir())
    print(f"\nProcessing {year}: {len(articles)} articles")

    for article_dir in articles:
        if not article_dir.is_dir():
            continue
        html_file = article_dir / "index.html"
        if not html_file.exists():
            print(f"  SKIP (no index.html): {article_dir.name}")
            continue

        slug = article_dir.name
        md_filename = slug + ".md"
        vault_path = vault_year / md_filename

        if vault_path.exists():
            print(f"  EXISTS: {md_filename}")
            continue

        data = recover_article(html_file, slug, year)
        if data is None:
            print(f"  FAILED: {slug}")
            continue

        write_md(vault_path, data)
        print(f"  OK: {md_filename}")


if __name__ == "__main__":
    for year in ["1969", "1970"]:
        process_year(year)
    print("\nDone.")
