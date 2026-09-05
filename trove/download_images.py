#!/usr/bin/env python3
"""Download Bulletin stub article pages, with at least 60s between image requests.

Run: python3 -u trove/download_images.py
Cutoff: trove/image-download-config.json, exclusive publication date in "before".
Stop: create trove/output/image-download/STOP (or send SIGTERM).
Resume: remove STOP and run the same command. Stubs are never changed.
"""
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser

ROOT = Path(__file__).resolve().parents[1]
STUBS = ROOT / "trove/output/bulletin/stubs"
DEST = ROOT / "src/trove-scans/bulletin"
CONTROL = ROOT / "trove/output/image-download"
AGENT = "KeithDunstanArchive/1.0 (+https://keithdunstan.org)"
INTERVAL = 60
stopping = False


class ArticleMappingError(ValueError):
    pass


class DeletedScanError(Exception):
    pass


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def save(path, data, create_parent=True):
    if create_parent:
        path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    temp.replace(path)


def log(message):
    print(f"{now()} {message}", flush=True)


def stop_requested():
    return stopping or (CONTROL / "STOP").exists()


def pause(seconds):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if stop_requested():
            raise InterruptedError("Stop requested")
        time.sleep(min(1, max(0, deadline - time.monotonic())))


def request(url, limit):
    with urlopen(Request(url, headers={"User-Agent": AGENT}), timeout=60) as response:
        data = response.read(limit + 1)
        if len(data) > limit:
            raise ValueError(f"Response exceeds {limit} bytes: {url}")
        return data


def article_pages(html, pid):
    match = re.search(r"var work\s*=\s*JSON.parse\(JSON.stringify\(", html)
    if not match:
        raise ValueError("Trove viewer metadata missing")
    work, _ = json.JSONDecoder().raw_decode(html[match.end():])
    children = work.get("children", {})
    article = next((a for a in children.get("article", []) if a["pid"] == pid), None)
    if article is None:
        raise ArticleMappingError("Link does not identify an article; whole-issue download skipped")
    wanted = {p["page"] for p in article.get("existson", [])}
    pages = [p for p in children.get("page", []) if p["pid"] in wanted]
    if not pages or {p["pid"] for p in pages} != wanted:
        raise ValueError("Article page mapping incomplete")
    return work, article, pages


def select_stubs(before):
    cutoff = datetime.date.fromisoformat(before)
    paths = sorted(STUBS.rglob("*.md"))
    selected = []
    for stub in paths:
        match = re.search(r'^date:\s*["\x27]?(\d{4}-\d{2}-\d{2})', stub.read_text(), re.M)
        if not match:
            raise ValueError(f"Cannot apply date cutoff to undated stub: {stub}")
        if datetime.date.fromisoformat(match.group(1)) < cutoff:
            selected.append(stub)
    return selected, len(paths)


def check_deleted(record, folder):
    """A removed scan is a review decision, never a reason to fetch it again."""
    if record.get("status") == "skipped_deleted":
        raise DeletedScanError("Previously deleted during review")
    if record.get("folder_created") and not folder.exists():
        raise DeletedScanError("Article folder deleted during review")
    missing = [p["file"] for p in record.get("images", []) if not (folder / p["file"]).exists()]
    if missing:
        raise DeletedScanError("Previously downloaded image deleted: " + ", ".join(missing))


def load_history():
    """Recover successful downloads even when their folders were already deleted."""
    path = ROOT / "trove/download-history.json"
    history = json.loads(path.read_text()) if path.exists() else {"version": 1, "stubs": {}}
    entries = history["stubs"]
    log_path = CONTROL / "download.log"
    for line in log_path.read_text().splitlines() if log_path.exists() else []:
        match = re.search(r"^(\S+) Saved (.+\.jpg) \((\d+) bytes\)$", line)
        if not match:
            continue
        target = ROOT / match.group(2)
        try:
            relative = target.relative_to(DEST)
        except ValueError:
            continue
        if len(relative.parts) != 3:
            continue
        year, slug, filename = relative.parts
        stub = STUBS / year / (slug + ".md")
        key = str(stub.relative_to(ROOT))
        record = entries.setdefault(key, {"stub": key, "images": [], "status": "downloading"})
        record.update(folder=str(target.parent.relative_to(ROOT)), folder_created=True)
        if not any(p["file"] == filename for p in record["images"]):
            record["images"].append(dict(file=filename, bytes=int(match.group(3)),
                                         downloaded_at=match.group(1), recovered_from="download.log"))
    for sidecar in DEST.rglob("source.json"):
        try:
            saved = json.loads(sidecar.read_text())
        except FileNotFoundError:
            continue  # The user may be removing rejected folders now.
        key = saved.get("stub")
        if not key:
            continue
        record = entries.setdefault(key, {"stub": key, "images": []})
        deleted = record.get("status") == "skipped_deleted"
        images = {p["file"]: p for p in record.get("images", [])}
        images.update({p["file"]: p for p in saved.get("images", [])})
        record.update(saved, images=list(images.values()), folder=str(sidecar.parent.relative_to(ROOT)),
                      folder_created=True)
        if deleted:
            record["status"] = "skipped_deleted"
    for record in entries.values():
        folder = ROOT / record["folder"]
        try:
            check_deleted(record, folder)
        except DeletedScanError as error:
            record["status"] = "skipped_deleted"
            record.setdefault("reason", str(error))
    save(path, history)
    return path, history


def main():
    before = json.loads((ROOT / "trove/image-download-config.json").read_text())["before"]
    paths, inventory_total = select_stubs(before)
    CONTROL.mkdir(parents=True, exist_ok=True)
    lock = (CONTROL / "worker.lock").open("w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        lock.close()
        raise SystemExit("A downloader is already running")
    history_path, history = load_history()
    (CONTROL / "worker.pid").write_text(str(os.getpid()) + "\n")
    state_path = CONTROL / "progress.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    state.update(status="running", pid=os.getpid(), started_at=now(), before=before)
    state.pop("reason", None)
    save(state_path, state)
    robots = RobotFileParser("https://nla.gov.au/robots.txt")
    robots.parse(request(robots.url, 1024 * 1024).decode().splitlines())
    state.update(total_stubs=len(paths), inventory_total=inventory_total,
                 deferred_stubs=inventory_total - len(paths), complete_articles=0,
                 skipped_deleted_articles=0, failed_articles=0)
    consecutive_errors = 0
    log(f"Starting {len(paths)} stubs dated before {before}; "
        f"{inventory_total - len(paths)} deferred; image request interval {INTERVAL}s; destination {DEST}")
    try:
        for stub in paths:
            if stop_requested():
                raise InterruptedError("Stop requested")
            state["current_stub"] = str(stub.relative_to(ROOT))
            save(state_path, state)
            folder = DEST / stub.parent.name / stub.stem
            sidecar = folder / "source.json"
            key = str(stub.relative_to(ROOT))
            record = history["stubs"].get(key, {})
            try:
                check_deleted(record, folder)
                if record.get("status") == "complete":
                    state["complete_articles"] += 1
                    continue
                source = re.search(r"https://nla.gov.au/(nla\.obj-\d+)", stub.read_text())
                if not source:
                    raise ValueError("No NLA object URL in stub")
                url, pid = source.group(), source.group(1)
                if not robots.can_fetch(AGENT, url):
                    raise ValueError("robots.txt disallows source URL")
                pause(2)
                work, article, pages = article_pages(request(url, 20 * 1024**2).decode(), pid)
                check_deleted(record, folder)
                record.update(title=article["title"], creator=article.get("creator", ""),
                              issue_date=work.get("issueDate"), source_url=url,
                              stub=str(stub.relative_to(ROOT)),
                              rights_statement=work.get("copyrightPolicy", "UNRESOLVED"),
                              status="downloading", expected_pages=len(pages))
                record.setdefault("images", [])
                record.pop("error", None)
                save(sidecar, record, create_parent=not record.get("folder_created"))
                record.update(folder=str(folder.relative_to(ROOT)), folder_created=True)
                history["stubs"][key] = record
                save(history_path, history)
                for number, page in enumerate(pages, 1):
                    check_deleted(record, folder)
                    image_file = f"page-{number:02d}-{page['pid']}.jpg"
                    target = folder / image_file
                    prior = next((p for p in record["images"] if p["file"] == image_file), None)
                    if prior:
                        continue
                    if shutil.disk_usage(ROOT).free < 2 * 1024**3:
                        raise InterruptedError("Paused: less than 2 GiB disk space remaining")
                    copy = next(c for c in page["copies"] if c.get("copyrole") == "access")
                    dimensions = copy["technicalmetadata"]
                    image_url = f"https://nla.gov.au/{page['pid']}/image?WID={int(dimensions['width'])}"
                    if not robots.can_fetch(AGENT, image_url):
                        raise ValueError("robots.txt disallows image URL")
                    pause(max(0, INTERVAL - (time.time() - state.get("last_image_request", 0))))
                    check_deleted(record, folder)
                    state["last_image_request"] = time.time()
                    save(state_path, state)
                    log(f"Request image {image_url}")
                    data = request(image_url, 50 * 1024**2)
                    if not data.startswith(b"\xff\xd8\xff") or not data.endswith(b"\xff\xd9"):
                        raise ValueError("Response is not a complete JPEG")
                    check_deleted(record, folder)
                    part = target.with_suffix(".jpg.part")
                    part.write_bytes(data)
                    part.replace(target)
                    record["images"] = [p for p in record["images"] if p["file"] != image_file]
                    record["images"].append(dict(file=image_file, source_url=image_url,
                        width=dimensions["width"], height=dimensions["height"],
                        bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), downloaded_at=now()))
                    save(history_path, history)
                    save(sidecar, record, create_parent=False)
                    state["images_downloaded"] = state.get("images_downloaded", 0) + 1
                    save(state_path, state)
                    log(f"Saved {target.relative_to(ROOT)} ({len(data)} bytes)")
                record["status"] = "complete"
                save(history_path, history)
                save(sidecar, record, create_parent=False)
                state["complete_articles"] += 1
                consecutive_errors = 0
            except InterruptedError:
                raise
            except (DeletedScanError, FileNotFoundError) as error:
                record.update(status="skipped_deleted", reason=str(error), stub=key,
                              folder=str(folder.relative_to(ROOT)))
                history["stubs"][key] = record
                save(history_path, history)
                state["skipped_deleted_articles"] += 1
                log(f"SKIP DELETED {stub.name}: {error}")
            except ArticleMappingError as error:
                record.update(status="needs_review", error=str(error), stub=str(stub.relative_to(ROOT)))
                history["stubs"][key] = dict(record, folder=str(folder.relative_to(ROOT)))
                save(history_path, history)
                state["failed_articles"] += 1
                log(f"REVIEW {stub.name}: {error}")
            except Exception as error:
                record.update(status="error", error=str(error), stub=str(stub.relative_to(ROOT)))
                history["stubs"][key] = dict(record, folder=str(folder.relative_to(ROOT)))
                save(history_path, history)
                state["failed_articles"] += 1
                consecutive_errors += 1
                log(f"ERROR {stub.name}: {error}")
                if isinstance(error, HTTPError) and error.code in (403, 429):
                    raise InterruptedError(f"Paused after HTTP {error.code}; review before resuming")
                if consecutive_errors >= 5:
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
        log(f"Status: {state['status']}")
        (CONTROL / "worker.pid").unlink(missing_ok=True)
        lock.close()


def on_signal(signum, frame):
    global stopping
    stopping = True


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, on_signal)
    signal.signal(signal.SIGINT, on_signal)
    main()
