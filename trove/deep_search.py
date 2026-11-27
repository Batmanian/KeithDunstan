"""
deep_search.py
--------------
Deep, cross-publication search of Trove for writing by Keith Dunstan that the
archive doesn't already hold.

Why this exists
    The original fetch_*.py scripts each target one magazine (The Bulletin,
    Walkabout) and earlier diagnostics probed newspapers only for 1960-2005,
    where Trove has almost nothing digitised. But Trove's newspaper zone runs
    to ~1954 for most mastheads (and to 1995 for The Canberra Times), which
    covers Keith's 1946-1954 Herald & Weekly Times years, including his New
    York (1949-52) and London (1952-54) correspondent copy, syndicated across
    HWT-affiliated papers (Courier-Mail, Advertiser, Newcastle Morning Herald,
    Perth Daily News...). This script searches all of Trove, not one title.

Stages (run in order; each is resumable and safe to re-run)

    survey   Cheap facet-only probes (n=0) for every search lane. Shows how
             many hits each lane has, broken down by title and decade, before
             spending requests on a harvest. ~1 request per lane.

    harvest  Pages through every lane with bulkHarvest, saving raw records to
             output/deep_search/raw/<lane>.jsonl. A cursor file per lane means
             an interrupted run resumes where it stopped.

    score    No API calls. Normalises every harvested record, scores how
             likely it is that Keith *wrote* it (byline in heading/first lines
             vs merely mentioned), drops other Keith Dunstans (pre-1943, born
             1925), removes anything already in vault/ or trove/output/,
             clusters syndicated copies of the same piece across papers, and
             writes output/deep_search/candidates.csv.

    gapfill  Finds recurring columns among high-confidence hits (e.g.
             "Keith Dunstan's Film World", weekly in The Herald), works out
             which expected issues are missing (usually because OCR garbled
             the byline), and runs one targeted query per missing issue.
             Results are appended to raw/gapfill.jsonl; re-run `score` after.

    stubs    Writes review stubs for candidates at or above --min-score into
             output/<publication-slug>/stubs/<year>/, including the raw OCR and
             links to syndicated alternate copies (useful for cross-checking
             bad OCR during transcription). Never touches vault/ or src/.

Rate limiting
    Trove allows 200 requests/minute on this key. A sliding-window limiter
    caps us at --rpm (default 150) to leave headroom, honours Retry-After on
    429, backs off on 5xx, and stops after 5 consecutive failures rather than
    hammering (see MISTAKES.md 2026-09-18). Every request is counted in
    output/deep_search/requests.log.

Usage
    cd trove && source .venv/bin/activate
    python deep_search.py survey
    python deep_search.py harvest            # or: harvest --lane np-name
    python deep_search.py score
    python deep_search.py gapfill --dry-run  # show missing issues first
    python deep_search.py gapfill
    python deep_search.py score
    python deep_search.py stubs --min-score 0.8

Data agreement: raw API results in output/deep_search/ fall under the Trove
data agreement (expires 31 Dec 2026; delete raw results then unless renewed).
"""

import argparse
import collections
import csv
import datetime as dt
import difflib
import json
import os
import re
import sys
import time
import warnings

warnings.filterwarnings("ignore")  # urllib3/LibreSSL noise on macOS system Python

import requests
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(BASE_DIR)
OUT_DIR = os.path.join(BASE_DIR, "output", "deep_search")
RAW_DIR = os.path.join(OUT_DIR, "raw")
STATE_DIR = os.path.join(OUT_DIR, "state")
API = "https://api.trove.nla.gov.au/v3/result"

load_dotenv(os.path.join(BASE_DIR, ".env"))
API_KEY = os.getenv("TROVE_API_KEY")

# Keith Dunstan: born 1925, RAAF 1943-46, joined HWT 1946, died 2013.
# Anything earlier than this is another Keith Dunstan.
EARLIEST = dt.date(1943, 1, 1)


def iso(d):
    return f"{d}T00:00:00Z"


# ---------------------------------------------------------------------------
# Search lanes. Each lane is one Trove query. Add lanes here as new leads
# appear (column names, pen names, publications). `kind` drives scoring.
# ---------------------------------------------------------------------------

NAME = '"Keith Dunstan"'
# OCR misreads seen in real Herald/Trove text, plus common hyphenation splits.
OCR_VARIANTS = [
    '"Keith Duns tan"', '"Keith Dun stan"', '"Keith Dunslan"', '"Keith Dunsten"',
    '"Keith Dunstau"', '"Keith Dimstan"', '"Keith Dunston"', '"Keifh Dunstan"',
    '"Kcith Dunstan"', '"Keith Dunsttm"', '"Keith Dunstan9s"', '"Keith Dunatan"',
]

LANES = [
    # Newspapers: whole of Trove, Keith's lifetime. Pre-1955 is the big win.
    dict(id="np-name", category="newspaper", kind="newspaper",
         q=f"{NAME} date:[{iso('1943-01-01')} TO {iso('2013-12-31')}]"),
    dict(id="np-ocr", category="newspaper", kind="newspaper",
         q=f"({' OR '.join(OCR_VARIANTS)}) date:[{iso('1943-01-01')} TO {iso('2013-12-31')}]"),
    # Correspondent copy where the byline sits outside the OCR'd article body
    # but the surname survives somewhere in the text.
    dict(id="np-correspondent", category="newspaper", kind="newspaper",
         q=(f'Dunstan AND ("New York" OR London OR Hollywood OR Washington) '
            f'AND (Herald OR correspondent OR staff) '
            f'date:[{iso("1949-01-01")} TO {iso("1955-06-30")}]')),
    # Known recurring Herald columns from New York (seen in the survey).
    dict(id="np-columns", category="newspaper", kind="newspaper",
         q=(f'("Film World" OR "Dunstan\'s Hollywood") '
            f'date:[{iso("1949-01-01")} TO {iso("1953-12-31")}]'),
         extra={"l-title": "1190"}),  # The Herald (Melbourne) title id
    # Magazines: all titles (Bulletin/Walkabout overlap is removed in `score`).
    dict(id="mag-name", category="magazine", kind="magazine", q=NAME),
    dict(id="mag-ocr", category="magazine", kind="magazine", q=f"({' OR '.join(OCR_VARIANTS)})"),
    # Catalogue records for articles *indexed* but not digitised (APAIS etc.).
    # Metadata only, but each one is a precise lead for physical sourcing.
    dict(id="index-articles", category="book", kind="index",
         q='creator:"Dunstan, Keith"', extra={"l-format": "Article"}),
]

# When a piece was syndicated, prefer the home paper's copy as canonical.
PAPER_PREFERENCE = [
    "The Herald (Melbourne", "The Sun News-Pictorial", "The Courier-Mail",
    "The Advertiser (Adelaide", "The Daily News (Perth", "Newcastle Morning Herald",
    "The Canberra Times",
]


# ---------------------------------------------------------------------------
# HTTP with a sliding-window rate limiter
# ---------------------------------------------------------------------------

class Trove:
    def __init__(self, rpm=150):
        if not API_KEY:
            raise SystemExit("ERROR: TROVE_API_KEY not set in trove/.env")
        self.rpm = min(rpm, 190)
        self.stamps = collections.deque()
        self.count = 0
        self.fails = 0
        os.makedirs(OUT_DIR, exist_ok=True)
        self.log = open(os.path.join(OUT_DIR, "requests.log"), "a", encoding="utf-8")

    def _wait(self):
        now = time.monotonic()
        while self.stamps and now - self.stamps[0] > 60:
            self.stamps.popleft()
        if len(self.stamps) >= self.rpm:
            time.sleep(60 - (now - self.stamps[0]) + 0.05)
        self.stamps.append(time.monotonic())

    def get(self, params):
        """params: list of (key, value) tuples (Trove repeats `facet`, etc.)."""
        for attempt in range(6):
            self._wait()
            self.count += 1
            try:
                # Pages carrying full article text can take 40-90s server-side.
                r = requests.get(API, params=[("key", API_KEY), ("encoding", "json")] + params, timeout=180)
            except requests.RequestException as e:
                status, err = "EXC", str(e)
            else:
                status, err = r.status_code, ""
            self.log.write(f"{dt.datetime.now().isoformat(timespec='seconds')}\t{status}\t"
                           f"{[p for p in params if p[0] != 'key']}\n")
            self.log.flush()
            if status == 200:
                self.fails = 0
                return r.json()
            self.fails += 1
            if self.fails >= 5:
                raise SystemExit(f"Stopping: 5 consecutive failures (last: {status} {err}). "
                                 "Check the URL independently before restarting.")
            if status == 429:
                delay = int(r.headers.get("Retry-After", "60"))
            elif status == "EXC" or (isinstance(status, int) and status >= 500):
                delay = 5 * (2 ** attempt)
            else:  # 4xx other than 429: query problem, retrying won't help
                raise SystemExit(f"HTTP {status} for {params}: {r.text[:300]}")
            print(f"    HTTP {status}, retrying in {delay}s")
            time.sleep(delay)
        raise SystemExit("Gave up after repeated failures.")


def lane_params(lane, extra=None):
    p = [("category", lane["category"]), ("q", lane["q"])]
    for k, v in (lane.get("extra") or {}).items():
        p.append((k, v))
    return p + (extra or [])


def records_of(data):
    cat = data.get("category", [{}])[0]
    return cat.get("records", {}), cat.get("facets", {})


# ---------------------------------------------------------------------------
# survey
# ---------------------------------------------------------------------------

def cmd_survey(args):
    t = Trove(args.rpm)
    report = {}
    for lane in LANES:
        facets = ["decade", "title"] if lane["category"] in ("newspaper", "magazine") else ["decade", "format"]
        data = t.get(lane_params(lane, [("n", "0")] + [("facet", f) for f in facets]))
        recs, fac = records_of(data)
        fac = fac.get("facet", [])
        fac = [fac] if isinstance(fac, dict) else fac
        entry = {"total": recs.get("total", 0)}
        for f in fac:
            entry[f["name"]] = {(x.get("display") or x.get("search")): x.get("count") for x in f.get("term", [])}
        report[lane["id"]] = entry
        print(f"\n{lane['id']:<18} total {entry['total']}")
        for name in facets:
            top = list(entry.get(name, {}).items())[:12]
            if top:
                print(f"  {name}: " + ", ".join(f"{k} ({v})" for k, v in top))
    with open(os.path.join(OUT_DIR, "survey.json"), "w") as f:
        json.dump(report, f, indent=2)
    est = sum(-(-v["total"] // 100) for v in report.values())
    print(f"\nRequests used: {t.count}. A full harvest needs about {est} requests "
          f"(~{max(1, -(-est // t.rpm))} min at {t.rpm}/min).")


# ---------------------------------------------------------------------------
# harvest
# ---------------------------------------------------------------------------

def cmd_harvest(args):
    t = Trove(args.rpm)
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(STATE_DIR, exist_ok=True)
    lanes = [l for l in LANES if not args.lane or l["id"] in args.lane]
    for lane in lanes:
        state_path = os.path.join(STATE_DIR, f"{lane['id']}.json")
        state = json.load(open(state_path)) if os.path.exists(state_path) else {"cursor": "*", "done": False, "n": 0}
        if state["done"] and not args.refresh:
            print(f"{lane['id']}: already complete ({state['n']} records); --refresh to redo")
            continue
        if args.refresh:
            state = {"cursor": "*", "done": False, "n": 0}
            open(os.path.join(RAW_DIR, f"{lane['id']}.jsonl"), "w").close()
        out = open(os.path.join(RAW_DIR, f"{lane['id']}.jsonl"), "a", encoding="utf-8")
        extra = [("bulkHarvest", "true")]
        if lane["category"] == "newspaper":
            # Smaller pages: 100 full-text articles per page times out server-side.
            extra += [("n", "50"), ("reclevel", "full"), ("include", "articletext")]
        else:
            # reclevel=full on magazine works times out (>180s) even at n=100;
            # brief records still carry title, isPartOf, identifiers and snippet.
            extra.append(("n", "50"))
        while True:
            data = t.get(lane_params(lane, extra + [("s", state["cursor"])]))
            recs, _ = records_of(data)
            items = recs.get("article") or recs.get("work") or []
            for it in items:
                out.write(json.dumps({"lane": lane["id"], "kind": lane["kind"], "rec": it}) + "\n")
            state["n"] += len(items)
            nxt = recs.get("nextStart")
            print(f"{lane['id']}: +{len(items)} (total {state['n']} of {recs.get('total')})")
            if not nxt or not items:
                state["done"] = True
            else:
                state["cursor"] = nxt
            json.dump(state, open(state_path, "w"))
            out.flush()
            if state["done"]:
                break
        out.close()
    print(f"\nRequests used this run: {t.count}")


# ---------------------------------------------------------------------------
# Normalisation + scoring
# ---------------------------------------------------------------------------

def clean(text):
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    return re.sub(r"\s+", " ", text).strip()


MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july", "august",
     "september", "october", "november", "december"], 1)}


def parse_work_title(title):
    """Magazine works carry their date in the title: 'Heading (1 March 1950)'."""
    m = re.search(r"\((\d{1,2})\s+([A-Za-z]+)\s+(\d{4})\)\s*$", title or "")
    if m and m.group(2).lower() in MONTHS:
        d = dt.date(int(m.group(3)), MONTHS[m.group(2).lower()], int(m.group(1)))
        return d, title[:m.start()].strip()
    m = re.search(r"\(([A-Za-z]+)\s+(\d{4})\)\s*$", title or "")
    if m and m.group(1).lower() in MONTHS:
        return dt.date(int(m.group(2)), MONTHS[m.group(1).lower()], 1), title[:m.start()].strip()
    return None, (title or "").strip()


def normalise(row):
    rec, kind = row["rec"], row["kind"]
    n = {"lane": row["lane"], "kind": kind, "id": str(rec.get("id", "")), "text": ""}
    if kind == "newspaper":
        n["heading"] = clean(rec.get("heading"))
        n["publication"] = (rec.get("title") or {}).get("title", "")
        n["title_id"] = str((rec.get("title") or {}).get("id", ""))
        n["date"] = rec.get("date", "")
        n["page"] = rec.get("page", "")
        n["category"] = rec.get("category", "")
        n["text"] = clean(rec.get("articleText"))
        n["words"] = int(rec.get("wordCount") or 0)
        n["url"] = f"https://nla.gov.au/nla.news-article{n['id']}"
        n["key"] = f"news:{n['id']}"
    else:
        d, heading = parse_work_title(rec.get("title", ""))
        n["heading"] = heading
        n["publication"] = "; ".join(p.get("value", "") for p in rec.get("isPartOf", []) if p.get("value"))
        n["title_id"] = ""
        n["date"] = d.isoformat() if d else str(rec.get("issued", ""))
        n["page"] = ""
        n["category"] = ", ".join(rec.get("type", []) or []) if isinstance(rec.get("type"), list) else str(rec.get("type", ""))
        n["text"] = clean(" ".join(rec.get("snippet", []) if isinstance(rec.get("snippet"), list) else [rec.get("snippet") or ""]))
        n["contributor"] = "; ".join(rec.get("contributor", []) or [])
        n["abstract"] = clean(" ".join(rec.get("abstract", []) if isinstance(rec.get("abstract"), list) else [rec.get("abstract") or ""]))
        n["words"] = 0
        full = next((i.get("value") for i in rec.get("identifier", []) if i.get("linktype") == "fulltext"), "")
        n["url"] = full or rec.get("troveUrl", "")
        n["key"] = f"work:{n['id']}"
        n["obj"] = (re.search(r"nla\.obj-\d+", full or "") or [None])[0] if full else None
    return n


# Fuzzy name: tolerates the OCR damage seen in practice (Keifh, Dunslan, DIMSTAN, Duns tan).
# Also KEITIH / Kcilth (OCR inserts a stray letter before the h).
NAME_RE = re.compile(r"\bk\s?[ec]\s?[il1f]\s?[a-z1]?\s?[tf]\s?[il1]?\s?h\W{0,3}d\s?[uli]\s?[nm]\s?[s5]\s?[tl]\s?[ae]\s?[nu]", re.I)
# A *different* Keith Dunstan in a notice ("Mr. Keith Dunstan, who has been managing...").
OTHER_PERSON_RE = re.compile(r"\b(mr|mrs)\.?\s+(\w+\s+)?" + NAME_RE.pattern[2:], re.I)
BYLINE_RE = re.compile(r"\b(by|from)\s+(our\s+)?" + NAME_RE.pattern[2:], re.I)
OWN_COLUMN_RE = re.compile(NAME_RE.pattern + r"\W{0,3}s\b", re.I)  # "Keith Dunstan's Film World"
DATELINE_RE = re.compile(r"\b(new york|london|hollywood|washington|los angeles|san francisco)\b\s*[.,\-—]", re.I)
REVIEW_RE = re.compile(r"\b(reviewed?|new book|publishers?|\$\d|price)\b", re.I)


def score(n):
    """Return (score 0-1, label, reason). Score = confidence Keith wrote it."""
    try:
        d = dt.date.fromisoformat(n["date"][:10])
    except ValueError:
        d = None
    if d and d < EARLIEST:
        return 0.0, "other-keith", f"dated {d}, before Keith's career"
    if n["kind"] == "newspaper" and n["category"] and n["category"] not in ("Article", "Literature"):
        return 0.05, "not-article", f"Trove category {n['category']}"

    head, text = n["heading"], n["text"]
    lead = text[:400]
    if n["lane"] == "gapfill" and not NAME_RE.search(head + " " + lead):
        # Byline lost to OCR by definition; look for the column's own fingerprint.
        if (re.search(r"\bnew\s?york\b", lead[:200], re.I)
                and re.search(r"\b(hollywood|film|movie|screen|star|studio|broadway|picture)s?\b", head + " " + lead, re.I)
                and n.get("words", 0) >= 250):
            return 0.6, "gapfill-column", "missing-week issue: New York dateline + film subject, byline unreadable"
        return 0.1, "weak", "gap-fill issue scan, no column fingerprint"
    if n["kind"] == "index":
        return 0.85, "indexed-ref", "catalogued with Keith Dunstan as creator (not digitised)"
    if OWN_COLUMN_RE.search(head) or BYLINE_RE.search(head):
        return 0.97, "byline-heading", "name/column title in the article heading"
    if n["kind"] == "magazine" and (NAME_RE.search(n.get("contributor", "")) or BYLINE_RE.search(lead)):
        return 0.9, "byline-text", "contributor or 'by/from Keith Dunstan' in magazine text"
    if BYLINE_RE.search(lead) or OWN_COLUMN_RE.search(lead[:150]):
        return 0.92, "byline-text", "'by/from Keith Dunstan' in opening lines"
    if NAME_RE.search(lead[:120]) and not OTHER_PERSON_RE.search(lead[:160]):
        return 0.7, "name-at-top", "name in first ~120 chars (byline, or a piece about him)"
    correspondent_years = d and dt.date(1949, 1, 1) <= d <= dt.date(1955, 6, 30)
    # Full name required: bare 'Dunstan' matches St. Dunstan's (the blinded servicemen's charity).
    if correspondent_years and DATELINE_RE.search(lead) and NAME_RE.search(text):
        return 0.65, "dateline", "overseas dateline during correspondent years + name present"
    if NAME_RE.search(text) or NAME_RE.search(head):
        if REVIEW_RE.search(text):
            return 0.2, "about-keith", "named in body, looks like a review/notice of his work"
        return 0.3, "mention", "named in body only, possibly about him or another Keith Dunstan"
    return 0.1, "weak", "matched query but name not found in available text"


def norm_title(s):
    s = re.sub(r"keith\s+dunstan'?s?\s+(film world|hollywood)", "", s or "", flags=re.I)
    return re.sub(r"[^a-z0-9 ]+", "", s.lower()).strip()


# ---------------------------------------------------------------------------
# What the archive already has
# ---------------------------------------------------------------------------

def existing_corpus():
    ids, titles = set(), []
    pat = re.compile(r"nla\.obj-\d+|nla\.news-article\d+|trove\.nla\.gov\.au/(?:work|newspaper/article)/(\d+)")
    for root in (os.path.join(REPO_DIR, "vault", "articles"), os.path.join(BASE_DIR, "output")):
        for dirpath, dirs, files in os.walk(root):
            if "deep_search" in dirpath:
                continue
            for fn in files:
                if not fn.endswith(".md"):
                    continue
                try:
                    txt = open(os.path.join(dirpath, fn), encoding="utf-8").read()
                except (UnicodeDecodeError, OSError):
                    continue
                for m in pat.finditer(txt):
                    ids.add(m.group(1) if m.group(1) else m.group(0).replace("nla.news-article", "news:"))
                if True:  # vault articles and existing stubs/transcriptions alike
                    t = re.search(r"^title:\s*\"?(.+?)\"?\s*$", txt, re.M)
                    d = re.search(r"^date:\s*(\d{4}-\d{2}-\d{2})", txt, re.M)
                    if t and d:
                        titles.append((norm_title(t.group(1)), d.group(1), os.path.relpath(os.path.join(dirpath, fn), REPO_DIR)))
    # Every earlier fetch log counts as "already seen", including works that
    # were triaged and rejected (their stub files are gone but the decision stands).
    out = os.path.join(BASE_DIR, "output")
    for fn in sorted(os.listdir(out)):
        if not fn.endswith("_results.csv"):
            continue
        for r in csv.DictReader(open(os.path.join(out, fn), encoding="utf-8")):
            ids.add(r.get("trove_id", ""))
            m = re.search(r"nla\.obj-\d+", r.get("fulltext_url", ""))
            if m:
                ids.add(m.group(0))
    return ids, titles


def already_have(n, ids, titles):
    if n["id"] in ids or f"news:{n['id']}" in ids or (n.get("obj") and n["obj"] in ids):
        return "id-match"
    nt = norm_title(n["heading"])
    if len(nt) < 6:
        return ""
    raw = n["date"] or ""
    try:
        d = dt.date.fromisoformat(raw[:10])
    except ValueError:
        d = None
    year = raw[:4] if re.fullmatch(r"\d{4}", raw[:4]) else None
    if not d and not year:
        return ""
    for t, td, path in titles:
        if d:
            close = abs((dt.date.fromisoformat(td) - d).days) <= 10
        else:  # catalogue records often carry only a year
            close = td[:4] == year
        if close and difflib.SequenceMatcher(None, nt, t).ratio() >= 0.85:
            return f"title-match:{path}"
    return ""
    try:
        d = dt.date.fromisoformat(n["date"][:10])
    except ValueError:
        return ""
    for t, td, path in titles:
        if abs((dt.date.fromisoformat(td) - d).days) <= 10 and difflib.SequenceMatcher(None, nt, t).ratio() >= 0.85:
            return f"title-match:{path}"
    return ""


# ---------------------------------------------------------------------------
# score
# ---------------------------------------------------------------------------

def load_raw():
    rows = {}
    if not os.path.isdir(RAW_DIR):
        raise SystemExit("No harvested data yet: run `harvest` first.")
    for fn in sorted(os.listdir(RAW_DIR)):
        if fn.endswith(".jsonl"):
            for line in open(os.path.join(RAW_DIR, fn), encoding="utf-8"):
                try:
                    n = normalise(json.loads(line))
                except json.JSONDecodeError:  # half-written line from an interrupted run
                    continue
                if n["key"] in rows:
                    rows[n["key"]]["lanes"].add(n["lane"])
                else:
                    n["lanes"] = {n["lane"]}
                    rows[n["key"]] = n
    return list(rows.values())


def shingles(text, k=5):
    w = re.findall(r"[a-z]{3,}", text.lower())[:120]
    return {" ".join(w[i:i + k]) for i in range(max(0, len(w) - k + 1))}


def cluster_syndication(rows):
    """Group copies of one piece run in several papers within a fortnight."""
    news = sorted((r for r in rows if r["kind"] == "newspaper" and r["score"] >= 0.6), key=lambda r: r["date"])
    for r in news:
        r["_sh"] = shingles(r["text"])
    parent = {r["key"]: r["key"] for r in news}

    def find(k):
        while parent[k] != k:
            parent[k] = parent[parent[k]]
            k = parent[k]
        return k

    for i, a in enumerate(news):
        da = dt.date.fromisoformat(a["date"])
        for b in news[i + 1:]:
            if (dt.date.fromisoformat(b["date"]) - da).days > 14:
                break
            if a["publication"] == b["publication"]:
                continue
            same_head = len(norm_title(a["heading"])) > 8 and norm_title(a["heading"]) == norm_title(b["heading"])
            sa, sb = a["_sh"], b["_sh"]
            jac = len(sa & sb) / max(1, len(sa | sb))
            if same_head or jac >= 0.35:
                parent[find(b["key"])] = find(a["key"])
    groups = collections.defaultdict(list)
    for r in news:
        groups[find(r["key"])].append(r)

    def rank(r):
        pref = next((i for i, p in enumerate(PAPER_PREFERENCE) if r["publication"].startswith(p)), 99)
        return (pref, -r.get("words", 0))

    for members in groups.values():
        members.sort(key=rank)
        canon = members[0]
        for m in members:
            m["cluster"] = canon["key"]
            m["is_canonical"] = m is canon
        canon["alternates"] = [m["url"] for m in members[1:]]
    for r in news:
        r.pop("_sh", None)


def cmd_score(args):
    rows = load_raw()
    ids, titles = existing_corpus()
    for r in rows:
        r["score"], r["label"], r["reason"] = score(r)
        r["have"] = already_have(r, ids, titles)
        r.setdefault("cluster", "")
        r.setdefault("is_canonical", True)
        r.setdefault("alternates", [])
    cluster_syndication(rows)
    rows.sort(key=lambda r: (-r["score"], r["date"]))
    path = os.path.join(OUT_DIR, "candidates.csv")
    cols = ["score", "label", "have", "is_canonical", "date", "publication", "heading", "page",
            "url", "alternates", "reason", "lanes", "words", "key", "title_id"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in rows:
            w.writerow([r["score"], r["label"], r["have"], r["is_canonical"], r["date"], r["publication"],
                        r["heading"], r["page"], r["url"], " ".join(r["alternates"]), r["reason"],
                        " ".join(sorted(r["lanes"])), r.get("words", 0), r["key"], r.get("title_id", "")])
    json.dump(rows, open(os.path.join(OUT_DIR, "candidates.json"), "w"), default=list)

    new = [r for r in rows if not r["have"] and r["is_canonical"]]
    print(f"{len(rows)} unique records; {sum(1 for r in rows if r['have'])} already in archive.")
    print("\nNew, de-syndicated candidates by confidence label:")
    for label, c in collections.Counter(r["label"] for r in new).most_common():
        print(f"  {label:<15} {c}")
    strong = [r for r in new if r["score"] >= 0.6]
    print(f"\nStrong new candidates (score >= 0.6): {len(strong)}, by publication:")
    for pub, c in collections.Counter(r["publication"][:60] for r in strong).most_common(20):
        print(f"  {c:>4}  {pub}")
    print(f"\nby year: " + ", ".join(f"{y} ({c})" for y, c in sorted(collections.Counter(r['date'][:4] for r in strong).items())))
    print(f"\nWrote {os.path.relpath(path, BASE_DIR)}")


# ---------------------------------------------------------------------------
# gapfill
# ---------------------------------------------------------------------------

COLUMN_RE = re.compile(NAME_RE.pattern + r"\W{0,3}s\s+([a-z][a-z ]{2,24}?)(?=\s+[A-Z\"']|$)", re.I)


def detect_columns(rows):
    """Recurring '<Keith Dunstan's X>' columns in one paper with a weekly-ish cadence."""
    found = collections.defaultdict(list)
    for r in rows:
        if r["kind"] != "newspaper" or r["score"] < 0.9 or not r.get("title_id"):
            continue
        m = COLUMN_RE.search(r["heading"])
        if m:
            name = m.group(1).strip().lower()
            found[(r["title_id"], r["publication"], name)].append(dt.date.fromisoformat(r["date"]))
    # Merge column names that ran in the same paper on the same weekday, since
    # columns get renamed ("Hollywood" became "Film World" in 1951).
    by_slot = collections.defaultdict(list)
    for (tid, pub, name), dates in found.items():
        if len(dates) < 3:
            continue
        wd = collections.Counter(x.weekday() for x in dates).most_common(1)[0][0]
        by_slot[(tid, pub, wd)].append((name, dates))
    columns = []
    for (tid, pub, wd), parts in by_slot.items():
        dates = sorted({d for _, ds in parts for d in ds})
        if len(dates) < 4:
            continue
        columns.append(dict(title_id=tid, publication=pub, weekday=wd,
                            names=[n for n, _ in parts], dates=dates))
    return columns


def cmd_gapfill(args):
    path = os.path.join(OUT_DIR, "candidates.json")
    if not os.path.exists(path):
        raise SystemExit("Run `score` first.")
    rows = json.load(open(path))
    columns = detect_columns(rows)
    if not columns:
        print("No recurring columns detected.")
        return
    todo = []
    for c in columns:
        have = set(c["dates"])
        d, end = c["dates"][0], c["dates"][-1]
        missing = []
        while d <= end:
            if d not in have and not any(abs((d - h).days) <= 2 for h in have):
                missing.append(d)
            d += dt.timedelta(days=7)
        days = "Mon Tue Wed Thu Fri Sat Sun".split()
        print(f"{c['publication']} | {' / '.join(c['names'])} | {days[c['weekday']]}s "
              f"{c['dates'][0]} to {c['dates'][-1]} | found {len(have)}, missing {len(missing)}")
        todo += [(c, m) for m in missing]
    print(f"\n{len(todo)} targeted queries needed.")
    if args.dry_run:
        return
    t = Trove(args.rpm)
    os.makedirs(RAW_DIR, exist_ok=True)
    done_path = os.path.join(STATE_DIR, "gapfill_done.json")
    os.makedirs(STATE_DIR, exist_ok=True)
    done = set(json.load(open(done_path))) if os.path.exists(done_path) else set()
    out = open(os.path.join(RAW_DIR, "gapfill.jsonl"), "a", encoding="utf-8")
    for c, day in todo:
        tag = f"{c['title_id']}:{day}"
        if tag in done:
            continue
        # Everything that issue carried with an overseas dateline or a column-name
        # fragment; the byline itself is often the bit OCR destroyed.
        words = " OR ".join(f'"{n}"' for n in c["names"])
        q = (f'({words} OR Dunstan OR "NEW YORK" OR LONDON OR HOLLYWOOD) '
             # A same-day range is zero-width on Trove; +/-1 day works.
             f'date:[{iso(day - dt.timedelta(days=1))} TO {iso(day + dt.timedelta(days=1))}]')
        data = t.get([("category", "newspaper"), ("q", q), ("l-title", c["title_id"]),
                      ("n", "40"), ("include", "articletext"), ("reclevel", "full")])
        recs, _ = records_of(data)
        hits = recs.get("article", []) or []
        for it in hits:
            out.write(json.dumps({"lane": "gapfill", "kind": "newspaper", "rec": it}) + "\n")
        print(f"  {day}: {len(hits)} articles")
        done.add(tag)
        json.dump(sorted(done), open(done_path, "w"))
        out.flush()
    print(f"\nRequests used: {t.count}. Re-run `score` to rank the gap-fill results.")


# ---------------------------------------------------------------------------
# stubs
# ---------------------------------------------------------------------------

# Folder per publication. Slugs match existing vault/articles/ and trove/output/
# folders where one exists; renamed runs of one title share a folder.
# (prefix of Trove's title string, folder slug, collection name for categories)
PUB_RULES = [
    ("The Herald (Melbourne", "the-herald", "The Herald"),
    ("The Sun News-Pictorial", "the-sun-news-pictorial", "The Sun News-Pictorial"),
    ("The Courier-Mail", "the-courier-mail", "The Courier-Mail"),
    ("Bulletin (Sydney)", "bulletin", "The Bulletin"),
    ("The Bulletin with Newsweek", "bulletin", "The Bulletin"),
    ("The bulletin", "bulletin", "The Bulletin"),
    ("Walkabout", "walkabout", "Walkabout"),
    ("Sydney Morning Herald. Good Weekend", "good-weekend", "Good Weekend"),
    ("Canberra Times. Good Weekend", "good-weekend", "Good Weekend"),
    ("Pedal power", "pedal-power", "Pedal Power"),
    ("Bicycle Victoria", "pedal-power", "Pedal Power"),
    ("The Australian home beautiful", "home-beautiful", "The Australian Home Beautiful"),
    ("The La Trobe Journal", "the-la-trobe-journal", "The La Trobe Journal"),
    ("La Trobe Journal", "the-la-trobe-journal", "The La Trobe Journal"),
]
EXACT_PUBS = {"Age": ("the-age", "The Age")}


def clean_pub_name(pub):
    """'The Canberra Times (ACT : 1926 - 1995)' -> 'The Canberra Times'."""
    name = re.split(r"\s*\(|\s+:\s", pub or "")[0].strip().rstrip(".")
    return name


def pub_folder(pub):
    if pub in EXACT_PUBS:
        return EXACT_PUBS[pub]
    for prefix, slug, name in PUB_RULES:
        if (pub or "").startswith(prefix):
            return slug, name
    name = clean_pub_name(pub)
    if not name:
        return "unsorted", "Unknown publication"
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-"), name


def yaml_str(s):
    return '"' + (s or "").replace("\\", "\\\\").replace('"', "'") + '"'


COLUMN_PREFIX_RE = re.compile(NAME_RE.pattern + r"\W{0,3}s\s+(film world|hollywood)\b|\bthe film world\b", re.I)


def article_title(heading):
    """Drop the running column header so the title is the piece's own headline."""
    t = COLUMN_PREFIX_RE.sub(" ", heading or "")
    t = re.sub(r"\s+", " ", t).strip(" .-—")
    return t or (heading or "Untitled")


def cmd_stubs(args):
    rows = json.load(open(os.path.join(OUT_DIR, "candidates.json")))
    picked = [r for r in rows if r["score"] >= args.min_score and not r["have"] and r.get("is_canonical", True)]
    written, skipped, per_folder = 0, 0, collections.Counter()
    for r in picked:
        slug, collection = pub_folder(r["publication"])
        printed_pub = clean_pub_name(r["publication"]) or collection
        raw = (r["date"] or "").strip()
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw[:10]):
            d, year, year_only = raw[:10], raw[:4], False
        elif re.fullmatch(r"\d{4}", raw[:4]) and int(raw[:4]) >= 1943:
            d, year, year_only = f"{raw[:4]}-01-01", raw[:4], True
        else:
            d, year, year_only = "", "undated", True
        title = article_title(r["heading"])
        title_slug = re.sub(r"[^a-z0-9]+", "-", norm_title(title))[:70].strip("-") or r["id"]
        folder = os.path.join(BASE_DIR, "output", slug, "stubs", year)
        fname = f"{d or 'undated'}-{title_slug}.md"
        fpath = os.path.join(folder, fname)
        if os.path.exists(fpath):
            if r["url"] in open(fpath, encoding="utf-8").read():
                skipped += 1
                continue  # same record, written on an earlier run
            fpath = fpath[:-3] + f"-{r['id']}.md"
            if os.path.exists(fpath):
                skipped += 1
                continue
        os.makedirs(folder, exist_ok=True)
        if year_only:
            long_date = year if year != "undated" else "date unknown"
        else:
            long_date = dt.date.fromisoformat(d).strftime("%-d %B %Y")
        indexed = r["kind"] == "index"
        alts = "\n".join(f"- {u}" for u in r.get("alternates", []))
        if indexed:
            note = ("**Not digitised.** This is a library catalogue record only; Trove has no scan. "
                    "Source the issue physically (State Library Victoria / NLA) before transcribing.")
            extra = f"Catalogue abstract: {r.get('abstract') or r['text'] or '(none)'}"
        else:
            note = ("[Full article text not yet transcribed. Check the byline on the scan before "
                    "transcribing; the confidence score is heuristic, not proof of authorship. "
                    "If the scan is illegible, flag it for visual review.]")
            extra = ""
            if alts:
                extra += "Syndicated copies (alternate scans/OCR for cross-checking):\n" + alts + "\n\n"
            extra += ("<details><summary>Uncorrected Trove OCR</summary>\n\n"
                      + (r["text"] or "(no text in API record)") + "\n\n</details>")
        page = f", page {r['page']}" if r.get("page") else ""
        body = f"""---
eleventyExcludeFromCollections: true
title: {yaml_str(title)}
date: {d}
summary: "First published in {printed_pub}, {long_date}. [Stub — not yet transcribed]"
categories:
- {collection}
tags:
---

<!-- deep_search.py: score {r['score']} ({r['label']}: {r['reason']}); lanes {', '.join(sorted(r['lanes']))}{page}{'; date is year only' if year_only else ''} -->

{note}

{extra}

<hr>

*Source: {r['heading']}, {printed_pub}, {long_date}. Accessible via the [National Library of Australia's Trove database]({r['url']}).*
"""
        open(fpath, "w", encoding="utf-8").write(re.sub(r"\n{3,}", "\n\n", body))
        written += 1
        per_folder[f"{slug}/stubs/{year}"] += 1
    print(f"Wrote {written} stubs ({skipped} already present) from {len(picked)} candidates >= {args.min_score}:")
    by_pub = collections.Counter()
    for k, v in per_folder.items():
        by_pub[k.split("/")[0]] += v
    for k, v in by_pub.most_common():
        print(f"  {v:>4}  trove/output/{k}/stubs/")


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rpm", type=int, default=150, help="max requests per minute (hard cap 190)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("survey")
    h = sub.add_parser("harvest")
    h.add_argument("--lane", action="append", help="only this lane id (repeatable)")
    h.add_argument("--refresh", action="store_true", help="discard saved progress and re-harvest")
    sub.add_parser("score")
    g = sub.add_parser("gapfill")
    g.add_argument("--dry-run", action="store_true")
    s = sub.add_parser("stubs")
    s.add_argument("--min-score", type=float, default=0.8)
    args = ap.parse_args()
    {"survey": cmd_survey, "harvest": cmd_harvest, "score": cmd_score,
     "gapfill": cmd_gapfill, "stubs": cmd_stubs}[args.cmd](args)


if __name__ == "__main__":
    main()
