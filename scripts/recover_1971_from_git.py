#!/usr/bin/env python3
"""Recover vault .md files for Bulletin 1971 from built HTML in git commit 6cc61c044."""

import subprocess
import html
from pathlib import Path
from bs4 import BeautifulSoup
import html2text

VAULT_BASE = Path("/Users/jack2026/Documents/repos/Untitled/KeithDunstan/vault/articles/bulletin")
SITE_ROOT = Path("/Users/jack2026/Documents/repos/Untitled/KeithDunstan")
GIT_COMMIT = "6cc61c044"

h = html2text.HTML2Text()
h.body_width = 0
h.protect_links = True
h.wrap_links = False


def git_show(commit, path):
    result = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        capture_output=True, text=True, cwd=str(SITE_ROOT)
    )
    if result.returncode != 0:
        return None
    return result.stdout


def body_html_to_markdown(div):
    inner = div.decode_contents()
    md = h.handle(inner)
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


def recover_article(html_content, slug):
    soup = BeautifulSoup(html_content, "html.parser")

    h1 = soup.find("h1", class_="display-3")
    if not h1:
        print(f"  WARN: no h1 in {slug}")
        return None
    title = html.unescape(h1.get_text())

    time_tag = soup.find("time", attrs={"data-pagefind-meta": "date"})
    if not time_tag:
        print(f"  WARN: no date in {slug}")
        return None
    date = time_tag["datetime"]

    sidebar = soup.find("div", class_=lambda c: c and "bg-light" in c and "d-none" in c and "d-md-block" in c)
    summary = ""
    if sidebar:
        lead_p = sidebar.find("p", class_="lead")
        if lead_p:
            summary = lead_p.get_text().strip()
    if not summary:
        mobile_p = soup.find("p", class_=lambda c: c and "lead" in c and "order-2" in c and "d-md-none" in c)
        if mobile_p:
            summary = mobile_p.get_text().strip()

    tags = []
    if sidebar:
        for li in sidebar.find_all("li", class_="topic-jump-item"):
            a = li.find("a", class_="link-secondary")
            if a:
                tags.append(a.get_text().strip())
    tags.sort(key=lambda t: t.lower())

    body_div = soup.find("div", class_="article-body")
    if not body_div:
        print(f"  WARN: no article-body in {slug}")
        return None
    body_md = body_html_to_markdown(body_div)

    return {"title": title, "date": date, "summary": summary, "tags": tags, "body": body_md}


def write_md(vault_path, data):
    vault_path.parent.mkdir(parents=True, exist_ok=True)
    title = data["title"]
    # Quote titles containing colons to avoid YAML parse errors
    if ":" in title:
        title = f'"{title}"'
    lines = ["---"]
    lines.append(f"title: {title}")
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


# Get list of 1971 article slugs from git
result = subprocess.run(
    ["git", "ls-tree", "-r", GIT_COMMIT, "--name-only"],
    capture_output=True, text=True, cwd=str(SITE_ROOT)
)
all_files = result.stdout.splitlines()
slugs_1971 = []
for f in all_files:
    if f.startswith("docs/articles/bulletin/1971/") and f.endswith("/index.html"):
        slug = f.replace("docs/articles/bulletin/1971/", "").replace("/index.html", "")
        slugs_1971.append(slug)
slugs_1971.sort()

print(f"Found {len(slugs_1971)} articles in 1971")

vault_1971 = VAULT_BASE / "1971"
for slug in slugs_1971:
    git_path = f"docs/articles/bulletin/1971/{slug}/index.html"
    md_filename = slug + ".md"
    vault_path = vault_1971 / md_filename

    if vault_path.exists():
        print(f"  EXISTS: {md_filename}")
        continue

    html_content = git_show(GIT_COMMIT, git_path)
    if html_content is None:
        print(f"  FAILED (git show): {slug}")
        continue

    data = recover_article(html_content, slug)
    if data is None:
        print(f"  FAILED (parse): {slug}")
        continue

    write_md(vault_path, data)
    print(f"  OK: {md_filename}")

print("\nDone.")
