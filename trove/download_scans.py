#!/usr/bin/env python3
"""Download Trove scans for the stubs written by deep_search.py (newspapers and magazines).

Companion to download_images.py (which handles the original Bulletin stubs) and
follows the same rules: at least 60s between image requests, robots.txt checked,
a source.json sidecar per article, permanent history outside the scan folders,
and a deleted scan or folder is a review decision that is never re-downloaded.

Scans go to src/trove-scans/<publication>/<year>/<stub-name>/ (gitignored and
excluded from Eleventy), mirroring trove/output/<publication>/stubs/<year>/.

  Newspaper stubs (nla.news-article links):
    page-NN-nla.news-pageX.jpg   full newspaper page (Trove "level7", ~4800px wide)
    article-NN.jpg               crop of the article's zones on that page (needs Pillow)
  Magazine stubs (nla.obj- links): the article's page images, as download_images.py.
  Catalogue-only stubs ("Not digitised"): skipped, nothing to download.

Run:    python3 -u trove/download_scans.py            (system python3: stdlib + Pillow)
        python3 -u trove/download_scans.py --dry-run  (count work, no requests)
        --only the-herald --only home-beautiful        (restrict publications)
Stop:   create trove/output/image-download-deep/STOP (or Ctrl-C / SIGTERM). Resume: rerun.
"""
import argparse
import datetime
import fcntl
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import signal
import sys
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser

sys.path.insert(0, str(Path(__file__).resolve().parent))
from download_images import ArticleMappingError, article_pages  # noqa: E402  (magazine viewer parsing)

try:
    from PIL import Image
except ImportError:  # crops are a convenience; full pages are always saved
    Image = None

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "trove/output"
DEST = ROOT / "src/trove-scans"
CONTROL = OUTPUT / "image-download-deep"
SHARED_LOCK = OUTPUT / "image-download/worker.lock"  # never run alongside download_images.py
HISTORY = ROOT / "trove/download-history-deep.json"
AGENT = "KeithDunstanArchive/1.0 (+https://keithdunstan.org)"
MARKER = "<!-- deep_search.py:"
PRIORITY = ["the-herald", "home-beautiful", "the-courier-mail", "the-sun-news-pictorial"]
MAX_SOURCE_FAILURES = 3  # same source failing on 3 separate attempts -> skipped_broken_source
stopping = False


class DeletedScanError(Exception):
    pass


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def log(message):
    line = f"{now()} {message}"
    print(line, flush=True)
    with open(CONTROL / "download.log", "a", encoding="utf-8") as f:
        f.write(line + "\n")


def save(path, data, create_parent=True):
    if create_parent:
        path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    temp.replace(path)


def stop_requested():
    return stopping or (CONTROL / "STOP").exists()


def pause(seconds):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if stop_requested():
            raise InterruptedError("Stop requested")
        time.sleep(min(1, max(0, deadline - time.monotonic())))


def fetch(url, limit):
    with urlopen(Request(url, headers={"User-Agent": AGENT}), timeout=90) as response:
        data = response.read(limit + 1)
        if len(data) > limit:
            raise ValueError(f"Response exceeds {limit} bytes: {url}")
        return data


def is_jpeg(data):
    return data.startswith(b"\xff\xd8\xff") and data.rstrip(b"\x00").endswith(b"\xff\xd9")


ZONE_RE = re.compile(r'class="zone[^"]*"\s+data-page-id="(\d+)"\s+data-x="(\d+)"\s+data-y="(\d+)"'
                     r'\s+data-w="(\d+)"\s+data-h="(\d+)"')


def newspaper_zones(html):
    """{page_id: [(x, y, w, h), ...]} in reading order, from the article page's zone markup."""
    pages = {}
    for pid, *box in ZONE_RE.findall(html):
        pages.setdefault(pid, []).append(tuple(int(v) for v in box))
    return pages


def crop_article(jpeg_bytes, boxes, pad=40):
    im = Image.open(io.BytesIO(jpeg_bytes))
    x0 = min(x for x, y, w, h in boxes)
    y0 = min(y for x, y, w, h in boxes)
    x1 = max(x + w for x, y, w, h in boxes)
    y1 = max(y + h for x, y, w, h in boxes)
    box = (max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad))
    out = io.BytesIO()
    im.crop(box).convert("RGB").save(out, "JPEG", quality=90)
    return out.getvalue(), box


def select_stubs(only):
    stubs = []
    for path in sorted(OUTPUT.glob("*/stubs/**/*.md")):
        text = path.read_text(encoding="utf-8")
        if MARKER not in text:
            continue  # original Bulletin/Walkabout stubs belong to download_images.py
        pub = path.relative_to(OUTPUT).parts[0]
        if only and pub not in only:
            continue
        stubs.append((path, pub, text))
    rank = {p: i for i, p in enumerate(PRIORITY)}
    stubs.sort(key=lambda s: (rank.get(s[1], len(rank)), s[1], s[0].parent.name, s[0].name))
    return stubs


def classify(text):
    if "**Not digitised.**" in text:
        return "not_digitised", None
    m = re.search(r"https://nla\.gov\.au/nla\.news-article(\d+)", text.split("<hr>")[-1])
    if m:
        return "newspaper", m.group(1)
    m = re.search(r"https://nla\.gov\.au/(nla\.obj-\d+)", text.split("<hr>")[-1])
    if m:
        return "magazine", m.group(1)
    return "no_source", None


def check_deleted(record, folder):
    if record.get("status") == "skipped_deleted":
        raise DeletedScanError("Previously deleted during review")
    if record.get("folder_created") and not folder.exists():
        raise DeletedScanError("Article folder deleted during review")
    missing = [p["file"] for p in record.get("images", []) if not (folder / p["file"]).exists()]
    if missing:
        raise DeletedScanError("Previously downloaded image deleted: " + ", ".join(missing))


class Worker:
    def __init__(self, interval, state, state_path):
        self.interval = interval
        self.state = state
        self.state_path = state_path

    def image(self, url, robots):
        if not robots.can_fetch(AGENT, url):
            raise ValueError(f"robots.txt disallows {url}")
        pause(max(0, self.interval - (time.time() - self.state.get("last_image_request", 0))))
        self.state["last_image_request"] = time.time()
        save(self.state_path, self.state)
        log(f"Request image {url}")
        data = fetch(url, 60 * 1024**2)
        if not is_jpeg(data):
            raise ValueError("Response is not a complete JPEG")
        return data


def write_image(folder, name, data, record, source_url, extra=None):
    target = folder / name
    part = target.with_suffix(".jpg.part")
    part.write_bytes(data)
    part.replace(target)
    entry = dict(file=name, source_url=source_url, bytes=len(data),
                 sha256=hashlib.sha256(data).hexdigest(), downloaded_at=now())
    entry.update(extra or {})
    record["images"] = [p for p in record["images"] if p["file"] != name] + [entry]
    log(f"Saved {target.relative_to(ROOT)} ({len(data)} bytes)")


def do_newspaper(article_id, folder, record, worker, robots_trove, save_record):
    page_url = f"https://trove.nla.gov.au/newspaper/article/{article_id}"
    if not robots_trove.can_fetch(AGENT, page_url):
        raise ValueError("robots.txt disallows article page")
    pause(2)
    html = fetch(page_url, 5 * 1024**2).decode("utf-8", "replace")
    zones = newspaper_zones(html)
    if not zones:
        raise ArticleMappingError("No article zones on Trove article page")
    record.update(source_url=f"https://nla.gov.au/nla.news-article{article_id}", article_page=page_url,
                  expected_pages=len(zones), status="downloading", rights_statement="UNRESOLVED")
    save_record()
    for number, (page_id, boxes) in enumerate(zones.items(), 1):
        name = f"page-{number:02d}-nla.news-page{page_id}.jpg"
        crop_name = f"article-{number:02d}.jpg"
        have = {p["file"] for p in record["images"]}
        if name in have and (crop_name in have or Image is None):
            continue
        check_deleted(record, folder)
        if shutil.disk_usage(ROOT).free < 2 * 1024**3:
            raise InterruptedError("Paused: less than 2 GiB disk space remaining")
        url = f"https://trove.nla.gov.au/ndp/imageservice/nla.news-page{page_id}/level7"
        if name in have:
            data = (folder / name).read_bytes()
        else:
            data = worker.image(url, robots_trove)
            check_deleted(record, folder)
            write_image(folder, name, data, record, url, {"zones": boxes})
        if Image is not None and crop_name not in have:
            crop, box = crop_article(data, boxes)
            write_image(folder, crop_name, crop, record, url, {"crop_box": box, "derived_from": name})
        save_record()


def do_magazine(pid, folder, record, worker, robots_nla, save_record):
    url = f"https://nla.gov.au/{pid}"
    if not robots_nla.can_fetch(AGENT, url):
        raise ValueError("robots.txt disallows source URL")
    pause(2)
    work, article, pages = article_pages(fetch(url, 20 * 1024**2).decode(), pid)
    record.update(title=article["title"], creator=article.get("creator", ""),
                  issue_date=work.get("issueDate"), source_url=url,
                  rights_statement=work.get("copyrightPolicy", "UNRESOLVED"),
                  status="downloading", expected_pages=len(pages))
    save_record()
    for number, page in enumerate(pages, 1):
        name = f"page-{number:02d}-{page['pid']}.jpg"
        if any(p["file"] == name for p in record["images"]):
            continue
        check_deleted(record, folder)
        if shutil.disk_usage(ROOT).free < 2 * 1024**3:
            raise InterruptedError("Paused: less than 2 GiB disk space remaining")
        copy = next(c for c in page["copies"] if c.get("copyrole") == "access")
        dims = copy["technicalmetadata"]
        image_url = f"https://nla.gov.au/{page['pid']}/image?WID={int(dims['width'])}"
        data = worker.image(image_url, robots_nla)
        check_deleted(record, folder)
        write_image(folder, name, data, record, image_url,
                    {"width": dims["width"], "height": dims["height"]})
        save_record()


def robots_for(url):
    rp = RobotFileParser(url)
    rp.parse(fetch(url, 1024 * 1024).decode().splitlines())
    return rp


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", action="append", help="publication folder slug (repeatable)")
    ap.add_argument("--interval", type=int, default=5, help="seconds between image requests (min 5)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    interval = max(5, args.interval)

    stubs = select_stubs(set(args.only or []))
    history = json.loads(HISTORY.read_text()) if HISTORY.exists() else {"version": 1, "stubs": {}}
    kinds = {}
    for path, pub, text in stubs:
        kind, _ = classify(text)
        kinds[kind] = kinds.get(kind, 0) + 1
    done = sum(1 for p, _, _ in stubs if history["stubs"].get(str(p.relative_to(ROOT)), {}).get("status")
               in ("complete", "skipped_deleted", "skipped_broken_source", "not_digitised"))
    print(f"{len(stubs)} deep-search stubs: {kinds}; already settled: {done}")
    todo_images = kinds.get("newspaper", 0) + 2 * kinds.get("magazine", 0)
    print(f"Roughly {todo_images} image requests at {interval}s spacing "
          f"= about {todo_images * interval / 3600:.1f} hours (crops are made locally, no extra requests)")
    if Image is None:
        print("Pillow not available: full pages only, no article crops")
    if args.dry_run:
        return

    CONTROL.mkdir(parents=True, exist_ok=True)
    SHARED_LOCK.parent.mkdir(parents=True, exist_ok=True)
    lock = SHARED_LOCK.open("a")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit("A Trove downloader (this or download_images.py) is already running")
    state_path = CONTROL / "progress.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    state.update(status="running", pid=os.getpid(), started_at=now(), total_stubs=len(stubs),
                 complete_articles=0, failed_articles=0, skipped_articles=0)
    state.pop("reason", None)
    save(state_path, state)
    worker = Worker(interval, state, state_path)
    robots_nla = robots_for("https://nla.gov.au/robots.txt")
    robots_trove = robots_for("https://trove.nla.gov.au/robots.txt")
    consecutive = 0
    log(f"Starting {len(stubs)} stubs; image interval {interval}s; destination {DEST}")
    try:
        for path, pub, text in stubs:
            if stop_requested():
                raise InterruptedError("Stop requested")
            key = str(path.relative_to(ROOT))
            folder = DEST / pub / path.parent.name / path.stem
            sidecar = folder / "source.json"
            record = history["stubs"].get(key, {"stub": key, "images": []})
            record.setdefault("images", [])
            state["current_stub"] = key
            save(state_path, state)

            def save_record():
                history["stubs"][key] = record
                save(HISTORY, history)
                if record.get("folder_created") or record.get("images"):
                    save(sidecar, record)

            status = record.get("status")
            if status in ("complete", "skipped_broken_source", "not_digitised"):
                state["complete_articles" if status == "complete" else "skipped_articles"] += 1
                continue
            kind, ident = classify(text)
            try:
                check_deleted(record, folder)
                if kind == "not_digitised":
                    record.update(status="not_digitised", reason="catalogue record only; no Trove scan")
                    history["stubs"][key] = record
                    save(HISTORY, history)
                    state["skipped_articles"] += 1
                    continue
                if kind == "no_source":
                    raise ArticleMappingError("No Trove scan link in stub")
                record.update(publication=pub, folder=str(folder.relative_to(ROOT)), kind=kind)
                folder.mkdir(parents=True, exist_ok=True)
                record["folder_created"] = True
                if kind == "newspaper":
                    do_newspaper(ident, folder, record, worker, robots_trove, save_record)
                else:
                    do_magazine(ident, folder, record, worker, robots_nla, save_record)
                record["status"] = "complete"
                record.pop("error", None)
                save_record()
                state["complete_articles"] += 1
                consecutive = 0
            except InterruptedError:
                raise
            except DeletedScanError as error:
                record.update(status="skipped_deleted", reason=str(error))
                history["stubs"][key] = record
                save(HISTORY, history)
                state["skipped_articles"] += 1
                log(f"SKIP DELETED {path.name}: {error}")
            except ArticleMappingError as error:
                record.update(status="needs_review", error=str(error))
                history["stubs"][key] = record
                save(HISTORY, history)
                state["failed_articles"] += 1
                log(f"REVIEW {path.name}: {error}")
            except Exception as error:
                record["failures"] = record.get("failures", 0) + 1
                if isinstance(error, HTTPError) and error.code >= 500 and record["failures"] >= MAX_SOURCE_FAILURES:
                    # See MISTAKES.md 2026-09-18: a source that keeps 5xx-ing must not loop forever.
                    record.update(status="skipped_broken_source",
                                  reason=f"HTTP {error.code} on {record['failures']} separate attempts")
                else:
                    record.update(status="error", error=str(error))
                history["stubs"][key] = record
                save(HISTORY, history)
                state["failed_articles"] += 1
                consecutive += 1
                log(f"ERROR {path.name}: {error}")
                if isinstance(error, HTTPError) and error.code in (403, 429):
                    raise InterruptedError(f"Paused after HTTP {error.code}; review before resuming")
                if consecutive >= 5:
                    raise InterruptedError("Paused after five consecutive errors")
                pause(60)
            save(state_path, state)
        state["status"] = "finished_with_errors" if state["failed_articles"] else "complete"
    except InterruptedError as error:
        state.update(status="paused", reason=str(error))
        log(str(error))
    finally:
        state["updated_at"] = now()
        save(state_path, state)
        log(f"Status: {state['status']} ({state['complete_articles']} complete, "
            f"{state['skipped_articles']} skipped, {state['failed_articles']} failed)")
        lock.close()


def on_signal(signum, frame):
    global stopping
    stopping = True


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, on_signal)
    signal.signal(signal.SIGINT, on_signal)
    main()
