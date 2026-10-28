#!/usr/bin/env python3
"""Import CC BY 4.0 Physics Refresher practice exercises as unapproved candidates.

Pinned upstream bytes, attribution, independent file hashes and explicit review
gates. No scraped text is ever auto-promoted to the original problem bank.
"""
import argparse
import hashlib
import json
import re
import time
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parent.parent / "external_sources"
REPO = "sharafdin/physics-refresher-for-engineering-and-science"
REV = "266c3a35284e47965df9651f682bcb7cd34f60b8"
SOURCE_NAME = "Physics Refresher (CC BY 4.0)"
MODULES = {
    "module-1-": "物理基础",
    "module-2-": "力学",
    "module-3-": "电磁学",
    "module-4-": "振动与波动",
}
KINDS = {"Concept Questions": "conceptual",
         "Numerical Problems": "calculation",
         "Challenge Problems": "challenge"}
MAX_BYTES = 120_000


def git_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def digest(text):
    compact = re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text).casefold()).strip()
    return hashlib.sha256(compact.encode("utf-8")).hexdigest()


def fetch(path, timeout=18):
    url = "https://raw.githubusercontent.com/" + REPO + "/" + REV + "/" + "/".join(
        quote(x, safe="") for x in path.split("/"))
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers={"User-Agent": "Ruoshui-Physics-Curation/1.0"}),
                         timeout=timeout) as response:
                data = response.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                raise ValueError("upstream_file_exceeds_limit")
            return data
        except (HTTPError, URLError, TimeoutError) as error:
            if attempt == 2 or (isinstance(error, HTTPError) and error.code not in (429, 500, 502, 503, 504)):
                raise
            time.sleep(1 + attempt)
    raise RuntimeError("fetch_unreachable")


def extract(text):
    """Only numbered questions from named Practice Problems subsections."""
    match = re.search(r"(?m)^## Practice Problems\s*$", text)
    if not match:
        return []
    tail = re.split(r"(?m)^## (?!#)", text[match.end():], maxsplit=1)[0]
    kind = None
    rows = []
    current = None

    def flush():
        if current is None:
            return
        question = "\n".join(current["lines"]).strip()
        if 12 <= len(question) <= 4000:
            rows.append((current["kind"], current["number"], question))

    for line in tail.splitlines():
        section = re.match(r"^###\s+(.+?)\s*$", line)
        if section:
            flush()
            current = None
            kind = KINDS.get(section.group(1).strip())
            continue
        if line.strip() == "---":
            flush()
            break
        numbered = re.match(r"^\s*(\d{1,3})\.\s+(.+?)\s*$", line)
        if numbered and kind:
            flush()
            current = {"kind": kind, "number": int(numbered.group(1)),
                       "lines": [numbered.group(2)]}
        elif current is not None:
            current["lines"].append(line.rstrip())
    else:
        flush()
    return rows


def run(limit=350, timeout=18, base=BASE, getter=None):
    folder = base / "physics_refresher"
    mp = folder / "source_manifest.json"
    ip = folder / "index.json"
    manifest = json.loads(mp.read_text(encoding="utf-8"))
    if manifest.get("repository") != REPO or manifest.get("revision") != REV:
        raise ValueError("upstream_revision_or_repository_mismatch")
    source = getter or (lambda path: fetch(path, timeout))
    license_bytes = source("LICENSE")
    readme_bytes = source("README.md")
    if (git_sha(license_bytes) != manifest["license_sha"] or
        git_sha(readme_bytes) != manifest["readme_sha"] or
        "Creative Commons Attribution 4.0 International" not in license_bytes.decode("utf-8") or
        "CC BY 4.0" not in readme_bytes.decode("utf-8")):
        raise ValueError("upstream_license_or_readme_evidence_changed")

    index = json.loads(ip.read_text(encoding="utf-8")) if ip.exists() else {"records": [], "count": 0}
    seen = {(r["source_path"], r["section"], r["number"], r["question_sha256"])
            for r in index["records"]}
    hashes = {r["question_sha256"] for r in index["records"]}
    next_id = max((int(r["id"].split("-")[-1]) for r in index["records"]), default=0)
    added = []
    failures = []
    skipped = Counter()
    inspected = 0
    for doc in manifest["documents"]:
        if doc.get("processed"):
            continue
        path = doc["path"]
        try:
            if not any(path.startswith(prefix) for prefix in MODULES):
                raise ValueError("unapproved_module_path")
            raw = source(path)
            if len(raw) > MAX_BYTES or git_sha(raw) != doc["sha"]:
                raise ValueError("source_blob_sha_or_size_mismatch")
            questions = extract(raw.decode("utf-8"))
            inspected += len(questions)
            finished = True
            for kind, number, question in questions:
                fingerprint = digest(question)
                key = (path, kind, number, fingerprint)
                if key in seen or fingerprint in hashes:
                    skipped["exact_question_duplicate"] += 1
                    continue
                if len(added) >= limit:
                    finished = False
                    break
                next_id += 1
                pid = "PREF-" + str(next_id).zfill(5)
                target = folder / "raw" / (pid + ".md")
                if target.exists():
                    raise ValueError("destination_collision:" + pid)
                topic = next(value for prefix, value in MODULES.items() if path.startswith(prefix))
                link = "https://github.com/" + REPO + "/blob/" + REV + "/" + path
                media = bool(re.search(r"!\[[^]]*\]\(|<img|(?:figure|diagram)\s+(?:above|below)", question, re.I))
                context = bool(re.search(
                    r"\b(?:same\s+(?:car|object|skier|particle|problem)|previous|preceding|"
                    r"as\s+in\s+(?:problem|example|lesson)|see\s+(?:figure|lesson)|"
                    r"example\s+\d|problem\s+\d)\b", question, re.I))
                record = {
                    "id": pid, "source": SOURCE_NAME, "module": topic, "section": kind,
                    "number": number, "source_repository": REPO, "source_revision": REV,
                    "source_path": path, "source_sha": doc["sha"], "source_url": link,
                    "question_sha256": fingerprint,
                    "license": "CC BY 4.0 (repository-level; item rights review pending)",
                    "license_review": "pending", "semantic_dedup": "pending",
                    "answer_verified": False, "exam_eligible": False,
                    "requires_media": media, "requires_context": context,
                    "status": "raw_candidate_requires_review",
                }
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(
                    "# " + pid + " · " + kind + "\n\n" + question +
                    "\n\n---\n\nSource: " + link +
                    "\nAttribution: sharafdin, Physics Refresher for Engineering & Science, "
                    "CC BY 4.0 (repository claim). Individual rights pending review.\n"
                    "Original Git blob SHA: " + doc["sha"] +
                    "\nNo verified answer. Not approved for examination.\n",
                    encoding="utf-8")
                index["records"].append(record)
                seen.add(key)
                hashes.add(fingerprint)
                added.append(pid)
            if finished:
                doc["processed"] = True
                doc["extracted_count"] = len(questions)
            else:
                break
        except Exception as error:
            failures.append({"path": path, "reason": str(error)[:200]})
            continue
    index["count"] = len(index["records"])
    manifest["imported"] = len(index["records"])
    for output, payload in ((mp, manifest), (ip, index)):
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")
    report = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "source": REPO, "revision": REV, "added_count": len(added),
        "total": index["count"], "documents_pending": sum(not d.get("processed")
                                                            for d in manifest["documents"]),
        "inspected": inspected, "skipped": dict(skipped), "failures": failures,
        "exam_ready_added": 0,
    }
    logs = base / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    (logs / "refresher_physics_latest.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=350)
    parser.add_argument("--timeout", type=int, default=18)
    args = parser.parse_args()
    if not 1 <= args.limit <= 350:
        parser.error("limit must be in 1..350")
    run(args.limit, args.timeout)
