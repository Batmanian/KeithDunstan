#!/usr/bin/env python3
"""
review_server.py — Side-by-side scan + stub review tool for Bulletin triage.

Opens at http://localhost:5050

Usage:
    cd /path/to/KeithDunstan
    python trove/review_server.py                  # review all years
    python trove/review_server.py --year 1972      # start at 1972

Actions:
    K / "Keith's"    — move stub to output/bulletin/transcribed/
    R / "Reject"     — move stub to output/bulletin/rejected/
    S / "Skip"       — leave in stubs/, come back later

Progress is remembered: stubs in transcribed/ and rejected/ show their status
in the article list so you can see what's done at a glance.
"""

import os
import sys
import json
import subprocess
import shutil
import re
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths — all relative to the repo root (one level up from trove/)
# ---------------------------------------------------------------------------
TROVE_DIR    = Path(__file__).resolve().parent
REPO_ROOT    = TROVE_DIR.parent
SCANS_BASE   = REPO_ROOT / "src" / "trove-scans" / "bulletin"
STUBS_BASE   = TROVE_DIR / "output" / "bulletin" / "stubs"
TRANS_BASE   = TROVE_DIR / "output" / "bulletin" / "transcribed"
REJECT_BASE  = TROVE_DIR / "output" / "bulletin" / "rejected"
PORT         = 5050

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def find_stub(year: str, slug: str):
    """Return (path, status) for a stub regardless of which bucket it's in."""
    for base, status in [
        (STUBS_BASE, "pending"),
        (TRANS_BASE, "approved"),
        (REJECT_BASE, "rejected"),
    ]:
        p = base / year / f"{slug}.md"
        if p.exists():
            return p, status
    return None, None


def list_stubs_for_year(year: str):
    """Return sorted list of {slug, status} dicts for a year."""
    seen = {}
    for base, status in [
        (STUBS_BASE, "pending"),
        (TRANS_BASE, "approved"),
        (REJECT_BASE, "rejected"),
    ]:
        d = base / year
        if d.is_dir():
            for f in sorted(d.iterdir()):
                if f.suffix == ".md":
                    slug = f.stem
                    if slug not in seen:
                        seen[slug] = status
    return [{"slug": s, "status": seen[s]} for s in sorted(seen)]


def list_years():
    """Return all years that have stubs in any bucket."""
    years = set()
    for base in [STUBS_BASE, TRANS_BASE, REJECT_BASE]:
        if base.is_dir():
            for d in base.iterdir():
                if d.is_dir() and d.name.isdigit():
                    years.add(d.name)
    return sorted(years)


def read_stub(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_title_date(text: str):
    title = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', text, re.MULTILINE)
    date  = re.search(r'^date:\s*(\S+)', text, re.MULTILINE)
    return (
        title.group(1).strip().strip("'\"") if title else "",
        date.group(1).strip() if date else "",
    )


def scan_images(year: str, slug: str):
    """Return list of image paths under src/trove-scans/bulletin/YEAR/SLUG/."""
    scan_dir = SCANS_BASE / year / slug
    if not scan_dir.is_dir():
        return []
    return sorted(
        p for p in scan_dir.iterdir()
        if p.suffix.lower() in {".jpg", ".jpeg", ".png"}
    )


def run_ocr(image_path: Path) -> str:
    """Run tesseract on a single image and return the text."""
    try:
        result = subprocess.run(
            ["tesseract", str(image_path), "stdout", "-l", "eng", "--psm", "6"],
            capture_output=True, text=True, timeout=30
        )
        return result.stdout.strip()
    except Exception as e:
        return f"[OCR error: {e}]"


def move_stub(year: str, slug: str, dest: str):
    """Move stub .md file to transcribed/ or rejected/. Returns (ok, message)."""
    src_path, _status = find_stub(year, slug)
    if src_path is None:
        return False, "Stub not found"
    dest_base = TRANS_BASE if dest == "approve" else REJECT_BASE
    dest_dir  = dest_base / year
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / f"{slug}.md"
    # Copy to destination first, then remove from all other buckets
    if src_path != dest_path:
        shutil.copy2(src_path, dest_path)
    for other_base in [STUBS_BASE, TRANS_BASE, REJECT_BASE]:
        other = other_base / year / f"{slug}.md"
        if other.exists() and other != dest_path:
            other.unlink()
    return True, f"Moved to {dest_base.name}/{year}/"


# ---------------------------------------------------------------------------
# HTML template
# ---------------------------------------------------------------------------
HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bulletin Triage Viewer</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: system-ui, sans-serif; background: #1a1a1a; color: #e0e0e0; height: 100vh; display: flex; flex-direction: column; }

  /* Header */
  #header { background: #111; padding: 8px 16px; display: flex; align-items: center; gap: 12px; border-bottom: 1px solid #333; flex-shrink: 0; }
  #header h1 { font-size: 14px; font-weight: 600; color: #aaa; white-space: nowrap; }
  #year-select { background: #2a2a2a; color: #e0e0e0; border: 1px solid #444; padding: 4px 8px; border-radius: 4px; font-size: 13px; }
  #status-bar { font-size: 12px; color: #888; margin-left: auto; }

  /* Main layout */
  #main { display: flex; flex: 1; overflow: hidden; }

  /* Sidebar */
  #sidebar { width: 240px; flex-shrink: 0; background: #111; border-right: 1px solid #333; overflow-y: auto; }
  .stub-item { padding: 7px 12px; cursor: pointer; font-size: 12px; border-bottom: 1px solid #222; line-height: 1.4; }
  .stub-item:hover { background: #2a2a2a; }
  .stub-item.active { background: #1e3a5f; }
  .stub-item .slug { color: #ccc; word-break: break-all; }
  .stub-item .badge { display: inline-block; font-size: 10px; padding: 1px 5px; border-radius: 3px; margin-top: 3px; }
  .badge.pending  { background: #333; color: #aaa; }
  .badge.approved { background: #1a4a1a; color: #6f6; }
  .badge.rejected { background: #4a1a1a; color: #f66; }

  /* Image panel */
  #image-panel { flex: 1; display: flex; flex-direction: column; overflow: hidden; background: #0d0d0d; }
  #image-toolbar { background: #111; padding: 6px 12px; display: flex; align-items: center; gap: 8px; border-bottom: 1px solid #333; flex-shrink: 0; }
  #image-toolbar button { background: #2a2a2a; color: #ccc; border: 1px solid #444; padding: 3px 10px; border-radius: 3px; cursor: pointer; font-size: 12px; }
  #image-toolbar button:hover { background: #3a3a3a; }
  #page-indicator { font-size: 12px; color: #888; }
  #image-container { flex: 1; overflow: auto; display: flex; align-items: flex-start; justify-content: center; padding: 12px; }
  #scan-img { max-width: 100%; transform-origin: top left; cursor: zoom-in; transition: transform 0.1s; }
  #scan-img.zoomed { cursor: zoom-out; }
  #no-scan { color: #555; font-size: 14px; padding: 40px; text-align: center; }

  /* Text panel */
  #text-panel { width: 400px; flex-shrink: 0; display: flex; flex-direction: column; border-left: 1px solid #333; }
  #text-toolbar { background: #111; padding: 6px 12px; display: flex; align-items: center; gap: 8px; border-bottom: 1px solid #333; flex-shrink: 0; }
  #text-toolbar button { background: #2a2a2a; color: #ccc; border: 1px solid #444; padding: 3px 10px; border-radius: 3px; cursor: pointer; font-size: 12px; }
  #text-toolbar button:hover { background: #3a3a3a; }
  #ocr-btn { background: #1a2a3a !important; color: #69f !important; border-color: #369 !important; }
  #text-content { flex: 1; overflow-y: auto; padding: 16px; font-size: 13px; line-height: 1.6; }
  #text-content pre { white-space: pre-wrap; word-break: break-word; color: #bbb; font-family: 'Menlo', monospace; font-size: 11.5px; }
  #text-content .ocr-block { margin-top: 12px; border-top: 1px solid #333; padding-top: 12px; }
  #text-content .label { font-size: 11px; color: #666; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px; }

  /* Action buttons */
  #actions { padding: 12px; background: #111; border-top: 1px solid #333; display: flex; gap: 8px; flex-shrink: 0; }
  #btn-approve { flex: 1; background: #1a4a1a; color: #6f6; border: 1px solid #3a7a3a; padding: 10px; border-radius: 4px; cursor: pointer; font-size: 14px; font-weight: 600; }
  #btn-approve:hover { background: #2a6a2a; }
  #btn-reject  { flex: 1; background: #4a1a1a; color: #f66; border: 1px solid #7a3a3a; padding: 10px; border-radius: 4px; cursor: pointer; font-size: 14px; font-weight: 600; }
  #btn-reject:hover { background: #6a2a2a; }
  #btn-skip    { background: #2a2a2a; color: #888; border: 1px solid #444; padding: 10px 16px; border-radius: 4px; cursor: pointer; font-size: 14px; }
  #btn-skip:hover { background: #3a3a3a; }

  /* Keyboard hint */
  #kbd-hint { font-size: 11px; color: #555; text-align: center; padding: 4px; background: #111; border-top: 1px solid #222; }
</style>
</head>
<body>

<div id="header">
  <h1>Bulletin Triage</h1>
  <select id="year-select"><option value="">— year —</option></select>
  <span id="status-bar"></span>
</div>

<div id="main">
  <div id="sidebar"></div>

  <div id="image-panel">
    <div id="image-toolbar">
      <button id="prev-page">&#8249; Prev page</button>
      <span id="page-indicator"></span>
      <button id="next-page">Next page &#8250;</button>
      <button id="zoom-in">+</button>
      <button id="zoom-out">−</button>
      <button id="zoom-fit">Fit</button>
    </div>
    <div id="image-container">
      <img id="scan-img" src="" alt="" style="display:none">
      <div id="no-scan">No scan available</div>
    </div>
  </div>

  <div id="text-panel">
    <div id="text-toolbar">
      <strong style="font-size:13px;color:#aaa;" id="article-title">Select an article</strong>
      <button id="ocr-btn" style="margin-left:auto">Run OCR</button>
    </div>
    <div id="text-content">
      <div id="stub-text"></div>
      <div id="ocr-block" class="ocr-block" style="display:none">
        <div class="label">Tesseract OCR output</div>
        <pre id="ocr-text"></pre>
      </div>
    </div>
    <div id="actions">
      <button id="btn-approve">&#10003; Keith's</button>
      <button id="btn-skip">Skip</button>
      <button id="btn-reject">&#10007; Reject</button>
    </div>
    <div id="kbd-hint">K = Keith's &nbsp;|&nbsp; R = Reject &nbsp;|&nbsp; S = Skip &nbsp;|&nbsp; ← → = navigate</div>
  </div>
</div>

<script>
let state = {
  year: '',
  stubs: [],
  idx: 0,
  pages: [],
  pageIdx: 0,
  zoom: 1.0,
};

// ---- Init ----
async function init() {
  const res = await fetch('/api/years');
  const years = await res.json();
  const sel = document.getElementById('year-select');
  years.forEach(y => {
    const opt = document.createElement('option');
    opt.value = opt.textContent = y;
    sel.appendChild(opt);
  });
  sel.addEventListener('change', () => loadYear(sel.value));
  // Auto-select first year with pending stubs
  const startYear = new URLSearchParams(location.search).get('year') || years[0];
  if (startYear) { sel.value = startYear; loadYear(startYear); }
}

async function loadYear(year) {
  if (!year) return;
  state.year = year;
  const res = await fetch(`/api/stubs/${year}`);
  state.stubs = await res.json();
  renderSidebar();
  // Jump to first pending
  const firstPending = state.stubs.findIndex(s => s.status === 'pending');
  loadStub(firstPending >= 0 ? firstPending : 0);
  updateStatusBar();
}

function renderSidebar() {
  const sb = document.getElementById('sidebar');
  sb.innerHTML = '';
  state.stubs.forEach((s, i) => {
    const div = document.createElement('div');
    div.className = 'stub-item' + (i === state.idx ? ' active' : '');
    div.innerHTML = `<div class="slug">${s.slug.replace(/^\d{4}-\d{2}-\d{2}-/, '')}</div>
      <span class="badge ${s.status}">${s.status}</span>`;
    div.addEventListener('click', () => loadStub(i));
    sb.appendChild(div);
  });
}

async function loadStub(idx) {
  if (idx < 0 || idx >= state.stubs.length) return;
  state.idx = idx;
  // Update sidebar active
  document.querySelectorAll('.stub-item').forEach((el, i) => {
    el.classList.toggle('active', i === idx);
  });
  // Scroll into view
  document.querySelectorAll('.stub-item')[idx]?.scrollIntoView({ block: 'nearest' });

  const { slug, status } = state.stubs[idx];
  const year = state.year;

  // Load stub text
  const res = await fetch(`/api/stub/${year}/${encodeURIComponent(slug)}`);
  const data = await res.json();
  document.getElementById('article-title').textContent = data.title || slug;
  document.getElementById('stub-text').innerHTML = `<div class="label">Stub (.md)</div><pre>${escHtml(data.content)}</pre>`;
  document.getElementById('ocr-block').style.display = 'none';
  document.getElementById('ocr-text').textContent = '';

  // Load images
  state.pages = data.images || [];
  state.pageIdx = 0;
  state.zoom = 1.0;
  renderImage();
  updateStatusBar();
}

function renderImage() {
  const img = document.getElementById('scan-img');
  const noScan = document.getElementById('no-scan');
  const pi = document.getElementById('page-indicator');
  if (state.pages.length === 0) {
    img.style.display = 'none';
    noScan.style.display = '';
    pi.textContent = '';
    return;
  }
  noScan.style.display = 'none';
  img.style.display = '';
  img.src = `/image/${state.pages[state.pageIdx]}`;
  img.style.transform = `scale(${state.zoom})`;
  pi.textContent = `Page ${state.pageIdx + 1} / ${state.pages.length}`;
}

function updateStatusBar() {
  const pending  = state.stubs.filter(s => s.status === 'pending').length;
  const approved = state.stubs.filter(s => s.status === 'approved').length;
  const rejected = state.stubs.filter(s => s.status === 'rejected').length;
  document.getElementById('status-bar').textContent =
    `${pending} pending · ${approved} approved · ${rejected} rejected`;
}

// ---- Actions ----
async function doAction(action) {
  if (!state.stubs.length) return;
  const { slug } = state.stubs[state.idx];
  if (action !== 'skip') {
    const res = await fetch(`/api/action/${action}/${state.year}/${encodeURIComponent(slug)}`, { method: 'POST' });
    const data = await res.json();
    if (!data.ok) { alert(data.message); return; }
    state.stubs[state.idx].status = action === 'approve' ? 'approved' : 'rejected';
    renderSidebar();
    updateStatusBar();
  }
  // Advance to next pending
  const next = state.stubs.findIndex((s, i) => i > state.idx && s.status === 'pending');
  if (next >= 0) loadStub(next);
}

// ---- OCR ----
document.getElementById('ocr-btn').addEventListener('click', async () => {
  const btn = document.getElementById('ocr-btn');
  btn.textContent = 'Running…';
  btn.disabled = true;
  const { slug } = state.stubs[state.idx];
  const page = state.pages[state.pageIdx] || '';
  const res = await fetch(`/api/ocr/${encodeURIComponent(page)}`);
  const data = await res.json();
  document.getElementById('ocr-text').textContent = data.text;
  document.getElementById('ocr-block').style.display = '';
  btn.textContent = 'Re-run OCR';
  btn.disabled = false;
});

// ---- Image controls ----
document.getElementById('prev-page').addEventListener('click', () => {
  if (state.pageIdx > 0) { state.pageIdx--; renderImage(); }
});
document.getElementById('next-page').addEventListener('click', () => {
  if (state.pageIdx < state.pages.length - 1) { state.pageIdx++; renderImage(); }
});
document.getElementById('zoom-in').addEventListener('click', () => { state.zoom = Math.min(state.zoom * 1.3, 5); renderImage(); });
document.getElementById('zoom-out').addEventListener('click', () => { state.zoom = Math.max(state.zoom / 1.3, 0.3); renderImage(); });
document.getElementById('zoom-fit').addEventListener('click', () => { state.zoom = 1.0; renderImage(); });

document.getElementById('scan-img').addEventListener('click', () => {
  state.zoom = state.zoom > 1.5 ? 1.0 : 2.5;
  renderImage();
});

// ---- Action buttons ----
document.getElementById('btn-approve').addEventListener('click', () => doAction('approve'));
document.getElementById('btn-reject').addEventListener('click', () => doAction('reject'));
document.getElementById('btn-skip').addEventListener('click', () => doAction('skip'));

// ---- Keyboard shortcuts ----
document.addEventListener('keydown', e => {
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
  if (e.key === 'k' || e.key === 'K') doAction('approve');
  else if (e.key === 'r' || e.key === 'R') doAction('reject');
  else if (e.key === 's' || e.key === 'S') doAction('skip');
  else if (e.key === 'ArrowRight') loadStub(state.idx + 1);
  else if (e.key === 'ArrowLeft') loadStub(state.idx - 1);
  else if (e.key === 'ArrowUp') {
    state.zoom = Math.min(state.zoom * 1.3, 5);
    renderImage();
  } else if (e.key === 'ArrowDown') {
    state.zoom = Math.max(state.zoom / 1.3, 0.3);
    renderImage();
  }
});

function escHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

init();
</script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Request handler
# ---------------------------------------------------------------------------
class Handler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        pass  # silence access log

    def send_json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, html):
        body = html.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def serve_file(self, path: Path, mime: str):
        if not path.exists():
            self.send_error(404)
            return
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path   = parsed.path
        qs     = urllib.parse.parse_qs(parsed.query)

        if path == "/":
            self.send_html(HTML)

        elif path == "/api/years":
            self.send_json(list_years())

        elif path.startswith("/api/stubs/"):
            year = path[len("/api/stubs/"):]
            self.send_json(list_stubs_for_year(year))

        elif path.startswith("/api/stub/"):
            # /api/stub/YEAR/SLUG
            parts = path[len("/api/stub/"):].split("/", 1)
            if len(parts) != 2:
                self.send_error(400); return
            year, slug = parts[0], urllib.parse.unquote(parts[1])
            stub_path, status = find_stub(year, slug)
            if stub_path is None:
                self.send_json({"error": "not found"}, 404); return
            content = read_stub(stub_path)
            title, date = parse_title_date(content)
            images = [
                str(img.relative_to(REPO_ROOT))
                for img in scan_images(year, slug)
            ]
            self.send_json({
                "slug": slug, "year": year, "status": status,
                "title": title, "date": date,
                "content": content, "images": images,
            })

        elif path.startswith("/api/ocr/"):
            rel = urllib.parse.unquote(path[len("/api/ocr/"):])
            img_path = REPO_ROOT / rel
            if not img_path.exists():
                self.send_json({"text": "Image not found"}); return
            text = run_ocr(img_path)
            self.send_json({"text": text})

        elif path.startswith("/image/"):
            rel = urllib.parse.unquote(path[len("/image/"):])
            img_path = REPO_ROOT / rel
            ext = img_path.suffix.lower()
            mime = "image/jpeg" if ext in {".jpg", ".jpeg"} else "image/png"
            self.serve_file(img_path, mime)

        else:
            self.send_error(404)

    def do_POST(self):
        path = urllib.parse.unquote(self.path)
        # /api/action/approve|reject/YEAR/SLUG
        m = re.match(r"/api/action/(approve|reject)/([^/]+)/(.+)$", path)
        if not m:
            self.send_json({"ok": False, "message": "Unknown action"}, 400)
            return
        action, year, slug = m.group(1), m.group(2), m.group(3)
        try:
            ok, msg = move_stub(year, slug, action)
            self.send_json({"ok": ok, "message": msg})
        except Exception as e:
            self.send_json({"ok": False, "message": str(e)}, 500)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    year_arg = None
    for i, arg in enumerate(sys.argv):
        if arg == "--year" and i + 1 < len(sys.argv):
            year_arg = sys.argv[i + 1]

    url = f"http://localhost:{PORT}"
    if year_arg:
        url += f"?year={year_arg}"

    print(f"Bulletin Triage Viewer")
    print(f"  {url}")
    print(f"  K = Keith's  |  R = Reject  |  S = Skip  |  ← → = navigate")
    print(f"  Ctrl-C to stop\n")

    try:
        import webbrowser
        webbrowser.open(url)
    except Exception:
        pass

    server = HTTPServer(("localhost", PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
