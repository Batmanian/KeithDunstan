#!/usr/bin/env python3
"""
review_articles.py: review transcribed articles against their scans before publishing.

    python3 trove/review_articles.py            # then open http://localhost:5051

Left: the article's scans from vault/articles/<pub>/<year>/scans/<article-name>/
(the article crop first, then full pages; click an image to zoom).
Right: the article's markdown, editable.

  Save                 writes your edits back to the vault file (refused if the
                       frontmatter no longer parses as YAML)
  Approve & publish    sets `status: published` and removes
                       `eleventyExcludeFromCollections: true` so the article
                       appears on the site at the next build. Every other
                       frontmatter field and the body are checked to be
                       unchanged before writing (CLAUDE.md rule).
  Previous / Next      step through the queue

The queue lists articles with `status: for review` (use the filter to see stubs or
published articles). Bound to 127.0.0.1 only; reads and writes only inside
vault/articles/. Uses system python3 (needs PyYAML).
"""
import html
import json
import re
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ARTICLES = (ROOT / "vault" / "articles").resolve()
PORT = 5051
FM_RE = re.compile(r"^---\r?\n(.*?)(\r?\n---[ \t]*\r?\n)", re.S)


def articles(status_filter):
    out = []
    for p in sorted(ARTICLES.rglob("*.md")):
        if "scans" in p.relative_to(ARTICLES).parts:
            continue
        text = p.read_text(encoding="utf-8")
        m = FM_RE.match(text)
        status = ""
        title = p.stem
        if m:
            sm = re.search(r"^status:\s*(.+?)\s*$", m.group(1), re.M)
            tm = re.search(r"^title:\s*(.+?)\s*$", m.group(1), re.M)
            status = sm.group(1) if sm else ""
            title = tm.group(1).strip("\"'") if tm else title
        if status_filter in ("all", status):
            out.append(dict(path=str(p.relative_to(ARTICLES)), title=title, status=status))
    return out


def safe_article(rel):
    p = (ARTICLES / rel).resolve()
    if ARTICLES not in p.parents or p.suffix != ".md" or not p.is_file():
        raise ValueError("not an article in vault/articles")
    return p


def scans_for(p):
    folder = p.parent / "scans" / p.stem
    if not folder.is_dir():
        return []
    imgs = sorted(folder.glob("*.jpg"), key=lambda f: (not f.name.startswith("article"), f.name))
    return [str(f.relative_to(ARTICLES)) for f in imgs]


def parse_fm(text):
    m = FM_RE.match(text)
    if not m:
        raise ValueError("no frontmatter block")
    data = yaml.safe_load(m.group(1))
    if not isinstance(data, dict):
        raise ValueError("frontmatter is not a mapping")
    return m, data


def publish(text):
    m, before = parse_fm(text)
    if str(before.get("title", "")).startswith("[Stub") or "[Stub" in str(before.get("summary", "")):
        raise ValueError("still has stub placeholder title/summary; finish the transcription first")
    block = m.group(1)
    block = re.sub(r"^eleventyExcludeFromCollections:\s*true\s*\r?\n", "", block, flags=re.M)
    if re.search(r"^status:.*$", block, re.M):
        block = re.sub(r"^status:.*$", "status: published", block, count=1, flags=re.M)
    else:
        block = re.sub(r"^(date:.*)$", r"\1\nstatus: published", block, count=1, flags=re.M)
    new = text[: m.start()] + "---\n" + block + m.group(2) + text[m.end():]
    m2, after = parse_fm(new)
    b, a = dict(before), dict(after)
    b.pop("status", None)
    b.pop("eleventyExcludeFromCollections", None)
    if a.pop("status", None) != "published" or a != b or text[m.end():] != new[m2.end():]:
        raise ValueError("verification failed: other fields or body would change; nothing written")
    return new


PAGE = """<!doctype html><html><head><meta charset="utf-8"><title>Review: {title}</title>
<style>
 body{{margin:0;font:14px system-ui,sans-serif;display:flex;flex-direction:column;height:100vh}}
 header{{padding:8px 12px;border-bottom:1px solid #ccc;display:flex;gap:10px;align-items:center;flex-wrap:wrap}}
 header .t{{font-weight:600;flex:1}} .st{{padding:2px 8px;border-radius:10px;background:#eee}}
 main{{flex:1;display:flex;min-height:0}}
 #scans{{flex:1;overflow:auto;background:#555;padding:8px}}
 #scans img{{display:block;width:100%;margin:0 auto 10px;cursor:zoom-in;background:#fff}}
 #scans img.zoom{{width:auto;max-width:none;cursor:zoom-out}}
 #scans .cap{{color:#ddd;font-size:12px;margin:2px 0 4px}}
 #edit{{flex:1;display:flex;flex-direction:column;border-left:1px solid #ccc}}
 textarea{{flex:1;font:14px/1.5 ui-monospace,Menlo,monospace;padding:10px;border:0;resize:none}}
 button{{padding:6px 12px;cursor:pointer}} .ok{{background:#2d7a3a;color:#fff;border:0}}
 #msg{{color:#a33}} a{{color:#245}}
</style></head><body>
<header><a href="/">&larr; Queue</a><span class="t">{title}</span><span class="st">{status}</span>
 <a href="{prev}">&lsaquo; Previous</a><a href="{next}">Next &rsaquo;</a>
 <button onclick="save()">Save</button><button class="ok" onclick="pub()">Approve &amp; publish</button><span id="msg"></span></header>
<main><div id="scans">{scans}</div>
<div id="edit"><textarea id="md" spellcheck="true">{md}</textarea></div></main>
<script>
const path={path};
document.querySelectorAll('#scans img').forEach(i=>i.onclick=()=>i.classList.toggle('zoom'));
let dirty=false; md.oninput=()=>{{dirty=true;msg.textContent='unsaved changes'}};
window.onbeforeunload=()=>dirty?true:undefined;
async function post(url){{const r=await fetch(url,{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{path,text:md.value}})}});const j=await r.json();if(!r.ok){{msg.textContent=j.error;return null}}return j}}
async function save(){{const j=await post('/save');if(j){{dirty=false;msg.style.color='#2d7a3a';msg.textContent='saved'}}}}
async function pub(){{if(!confirm('Mark as published? It will appear on the site at the next build.'))return;const j=await post('/publish');if(j){{dirty=false;md.value=j.text;msg.style.color='#2d7a3a';msg.textContent='published';document.querySelector('.st').textContent='published'}}}}
document.addEventListener('keydown',e=>{{if((e.metaKey||e.ctrlKey)&&e.key==='s'){{e.preventDefault();save()}}}});
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, body, ctype="text/html; charset=utf-8", code=200):
        data = body.encode() if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        try:
            if u.path == "/":
                st = q.get("status", ["for review"])[0]
                rows = articles(st)
                opts = "".join(f'<a href="/?status={urllib.parse.quote(s)}">{s}</a> ' for s in ("for review", "stub", "published", "all"))
                items = "".join(
                    f'<li><a href="/article?path={urllib.parse.quote(r["path"])}&status={urllib.parse.quote(st)}">'
                    f'{html.escape(r["title"])}</a> <small>{html.escape(r["path"])} · {html.escape(r["status"])}'
                    f'{" · scans" if scans_for(ARTICLES / r["path"]) else ""}</small></li>' for r in rows)
                self.send(f"<!doctype html><meta charset=utf-8><title>Review queue</title>"
                          f"<body style='font:15px system-ui;margin:20px'><h2>{html.escape(st)} ({len(rows)})</h2>"
                          f"<p>Show: {opts}</p><ol>{items}</ol>")
            elif u.path == "/article":
                st = q.get("status", ["for review"])[0]
                p = safe_article(q["path"][0])
                rel = str(p.relative_to(ARTICLES))
                queue = [r["path"] for r in articles(st)]
                i = queue.index(rel) if rel in queue else -1
                link = lambda j: f"/article?path={urllib.parse.quote(queue[j])}&status={urllib.parse.quote(st)}" if 0 <= j < len(queue) else "#"
                text = p.read_text(encoding="utf-8")
                sm = re.search(r"^status:\s*(.+?)\s*$", text, re.M)
                imgs = scans_for(p)
                scans = "".join(f'<div class="cap">{html.escape(Path(s).name)}</div><img src="/scan?path={urllib.parse.quote(s)}" loading="lazy">' for s in imgs) \
                    or '<p style="color:#eee">No scans found in ' + html.escape(str((p.parent / "scans" / p.stem).relative_to(ROOT))) + "</p>"
                self.send(PAGE.format(title=html.escape(p.stem), status=html.escape(sm.group(1) if sm else "no status"),
                                      prev=link(i - 1), next=link(i + 1), scans=scans, md=html.escape(text),
                                      path=json.dumps(rel)))
            elif u.path == "/scan":
                f = (ARTICLES / q["path"][0]).resolve()
                if ARTICLES not in f.parents or "scans" not in f.relative_to(ARTICLES).parts or f.suffix != ".jpg":
                    raise ValueError("not a scan")
                self.send(f.read_bytes(), "image/jpeg")
            else:
                self.send("not found", "text/plain", 404)
        except (ValueError, KeyError) as e:
            self.send(str(e), "text/plain", 400)

    def do_POST(self):
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            p = safe_article(body["path"])
            text = body["text"].replace("\r\n", "\n")
            if self.path == "/save":
                parse_fm(text)  # refuse to save broken frontmatter
                p.write_text(text, encoding="utf-8")
                self.send(json.dumps({"ok": True}), "application/json")
            elif self.path == "/publish":
                parse_fm(text)
                new = publish(text)
                p.write_text(new, encoding="utf-8")
                self.send(json.dumps({"ok": True, "text": new}), "application/json")
            else:
                self.send(json.dumps({"error": "unknown action"}), "application/json", 404)
        except (ValueError, KeyError, yaml.YAMLError) as e:
            self.send(json.dumps({"error": f"Not written: {e}"}), "application/json", 400)


if __name__ == "__main__":
    print(f"Review articles at http://localhost:{PORT}  (Ctrl-C to stop)")
    HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
