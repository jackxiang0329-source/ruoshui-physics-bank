#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Conservative, auditable importer for pinned university-physics OER candidates.

Only CC BY 4.0 items with explicit per-file attribution are imported automatically.
Imported items are *raw candidates*, never exam-approved questions.
"""
import argparse
import hashlib
import json
import os
import re
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "external_sources"
MANIFEST = BASE / "catalog" / "upstream_manifest.json"
DECISIONS = BASE / "catalog" / "auto_import_decisions.json"
UA = "RuoshuiPhysicsOER/1.0 (scheduled educational source inventory)"
SOURCE_DIR = "ubc_opbp"
PREFIX = "UBC"
MAX_BYTES = 180_000

TOPICS = {
    "003": "力学", "004": "力学", "005": "力学", "006": "力学",
    "007": "力学", "008": "力学", "009": "力学", "010": "力学",
    "011": "力学", "012": "力学", "013": "力学", "014": "力学",
    "015": "振动与波动", "016": "振动与波动",
    "018": "电磁学", "019": "电磁学", "020": "电磁学",
    "021": "电磁学", "022": "光学",
}
SOURCE_LABELS = {
    "ubc_opbp": "UBC Open Physics Bank",
    "webwork_brockphysics": "WeBWorK BrockPhysics (NC; manual review)",
    "webwork_brock_thermal": "WeBWorK Thermal (NC; manual review)",
}


def git_blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def canonical(text):
    """Whitespace/text dedup only; does NOT establish semantic uniqueness."""
    text = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", text, flags=re.S)
    text = re.sub(r"(?im)^##\s+Attribution\b[\s\S]*\Z", "", text)
    text = unicodedata.normalize("NFKC", text).casefold()
    return re.sub(r"\s+", " ", text).strip()


def category(topic):
    return TOPICS.get(str(topic)[:3])


def author_name(text):
    match = re.search(r"(?m)^author:\s*([^\r\n#]+)", text)
    return match.group(1).strip().strip("'\"") if match else ""


def source_field(text):
    match = re.search(r"(?m)^source:\s*([^\r\n]+)", text)
    return match.group(1).strip() if match else ""


def license_verdict(text):
    match = re.search(r"(?im)^##\s+Attribution\b([\s\S]*)", text)
    if not match:
        return None, "missing_per_file_attribution"
    attribution = match.group(1)
    if re.search(r"(?:CC[- ]?BY[- ]?(?:NC|SA|ND)\b|/licenses/by-(?:nc|sa|nd))", attribution, re.I):
        return None, "restrictive_or_mixed_license"
    clear_by = re.search(r"CC[- ]?BY\s*4\.0\b|creativecommons\.org/licenses/by/4\.0(?:/|[)\s.]|$)", attribution, re.I)
    if not clear_by:
        return None, "no_explicit_cc_by_4_grant"
    if not author_name(text):
        return None, "missing_named_author"
    return "CC BY 4.0", None


def media_required(text):
    question_text = re.split(r"(?im)^##\s+Attribution\b", text, maxsplit=1)[0]
    if re.search(r"(?i)<img\b|!\[[^\]]*\]\([^)]+\)", question_text):
        return True
    match = re.search(r"(?m)^assets:\s*([^\r\n]*)", text)
    if not match:
        return False
    value = match.group(1).strip().lower()
    if value in ("null", "none", "false", "[]", "~"):
        return False
    if value:
        return True
    return bool(re.search(r"(?m)^assets:\s*\r?\n\s*-\s+\S", text))


def fetch_bytes(url, timeout):
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=timeout) as response:
        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > MAX_BYTES:
            raise ValueError("source_file_too_large")
        raw = response.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError("source_file_too_large")
    return raw


def source_url(row, relative_path):
    fullname = row["root"].rstrip("/") + "/" + relative_path
    suffix = "/".join(quote(part, safe="") for part in fullname.split("/"))
    return ("https://raw.githubusercontent.com/" + row["repository"]
            + "/" + row["revision"] + "/" + suffix)


def existing_hashes():
    blobs, canonical_hashes = set(), set()
    for src, suffix in (("ubc_opbp", ".md"), ("webwork_opl", ".pg"),
                        ("webwork_thermal", ".pg")):
        path = BASE / src / "index.json"
        if not path.exists():
            continue
        idx = json.loads(path.read_text(encoding="utf-8"))
        for item in idx["records"]:
            if item.get("source_sha"):
                blobs.add(item["source_sha"])
            name = item.get("id", "")
            if not re.fullmatch(r"(?:UBC|OPL|THM)-\d{3,7}", name):
                continue
            original = BASE / src / "raw" / (name + suffix)
            if original.is_file():
                data = original.read_bytes()
                blobs.add(git_blob_sha(data))
                canon = canonical(data.decode("utf-8", errors="replace"))
                if canon:
                    canonical_hashes.add(hashlib.sha256(canon.encode()).hexdigest())
    return blobs, canonical_hashes


def read_json(path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")


def upstream_revision_checks(manifest, timeout):
    """Observe newer upstream revisions; never silently rewrite pinned manifests."""
    results = []
    repositories = sorted({x["repository"] for x in manifest["sources"]})
    for repo in repositories:
        link = "https://api.github.com/repos/" + repo + "/git/ref/heads/main"
        row = {"repository": repo}
        try:
            raw = fetch_bytes(link, timeout)
            payload = json.loads(raw.decode("utf-8"))
            sha = payload.get("object", {}).get("sha", "")
            row["latest_revision"] = sha
            row["pinned_revisions"] = sorted({
                x["revision"] for x in manifest["sources"]
                if x["repository"] == repo
            })
            row["newer_revision_detected"] = bool(sha and sha not in row["pinned_revisions"])
            if row["newer_revision_detected"]:
                row["note"] = "New revisions require independent manifest and license review."
        except (ValueError, URLError, HTTPError, TimeoutError, OSError) as exc:
            row["check_error"] = str(exc)[:180]
        results.append(row)
    return results


def execute(limit, scan_limit, timeout, dry_run=False, root=BASE):
    # root injection supports safe local tests.
    manifest_path = root / "catalog" / "upstream_manifest.json"
    manifest = read_json(manifest_path, None)
    if manifest is None or not isinstance(manifest.get("sources"), list):
        raise ValueError("Missing or malformed pinned upstream manifest")
    ubc = next(x for x in manifest["sources"] if x["id"] == "ubc_opbp")
    idx_path = root / SOURCE_DIR / "index.json"
    index = read_json(idx_path, None)
    if index is None:
        raise ValueError("Missing UBC index")
    decision_path = root / "catalog" / "auto_import_decisions.json"
    decisions = read_json(decision_path, {"schema": 1, "blocked": {}})
    blocked_cache = decisions.setdefault("blocked", {})
    known_paths = {x["path"] for x in index["records"]}
    # Hash scanning uses the repository's actual external sources, not an arbitrary URL.
    original_base = globals()["BASE"]
    globals()["BASE"] = root
    try:
        known_blobs, known_canonical = existing_hashes()
    finally:
        globals()["BASE"] = original_base

    now = datetime.now(timezone.utc)
    report = {
        "timestamp_utc": now.isoformat(timespec="seconds"),
        "github_run_id": os.getenv("GITHUB_RUN_ID", "local"),
        "mode": "dry-run" if dry_run else "execute",
        "sources": SOURCE_LABELS,
        "added_count": 0,
        "added": [],
        "checked_candidates": 0,
        "skipped_reasons": {},
        "failures": [],
        "pending_rights_and_academic_review": True,
        "exam_ready_added": 0,
    }
    skipped = Counter()
    id_number = max([int(x["id"].split("-")[-1]) for x in index["records"]] or [0])

    for source in manifest["sources"]:
        if source["id"] != "ubc_opbp":
            skipped["upstream_default_noncommercial_manual_review"] += 1
    for item in ubc["files"]:
        if report["added_count"] >= limit or report["checked_candidates"] >= scan_limit:
            break
        if item.get("downloaded"):
            continue
        rel = item["path"]
        key = ubc["revision"] + ":" + rel
        previous = blocked_cache.get(key)
        if previous and previous.get("sha") == item["sha"]:
            continue
        reason = None
        if (not rel.endswith(".md") or rel.startswith("/")
                or ".." in Path(rel).parts):
            reason = "invalid_manifest_path"
        elif not category(rel.split("/")[0]):
            reason = "outside_supported_physics_modules"
        elif item.get("bytes", 0) > MAX_BYTES:
            reason = "source_file_too_large"
        elif ubc["root"] + "/" + rel in known_paths or item["sha"] in known_blobs:
            reason = "duplicate_path_or_git_blob"
        if reason:
            skipped[reason] += 1
            if not dry_run:
                blocked_cache[key] = {"sha": item["sha"], "reason": reason}
            continue
        report["checked_candidates"] += 1
        if dry_run:
            report["added"].append({"path": rel, "state": "eligible_for_fetch_not_checked"})
            continue
        uri = source_url(ubc, rel)
        try:
            raw = fetch_bytes(uri, timeout)
            if git_blob_sha(raw) != item["sha"]:
                raise ValueError("upstream_git_blob_sha_mismatch")
            text = raw.decode("utf-8")
            license_name, reason = license_verdict(text)
            if not reason and media_required(text):
                reason = "missing_media_assets_manual_review"
            if not reason:
                normalized = canonical(text)
                normalized_sha = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
                if not normalized or normalized_sha in known_canonical:
                    reason = "duplicate_normalized_content"
            if reason:
                skipped[reason] += 1
                blocked_cache[key] = {"sha": item["sha"], "reason": reason}
                continue
            id_number += 1
            pid = PREFIX + "-" + f"{id_number:03d}"
            dest = root / SOURCE_DIR / "raw" / (pid + ".md")
            if dest.exists():
                raise ValueError("unexpected_destination_collision")
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(raw)
            fullpath = ubc["root"].rstrip("/") + "/" + rel
            index["records"].append({
                "id": pid,
                "path": fullpath,
                "license": license_name,
                "license_source": "explicit per-file Attribution; rights-chain review pending",
                "license_review": "automated_signal_only",
                "author": author_name(text),
                "source": source_field(text),
                "requires_media": False,
                "source_sha": item["sha"],
                "source_url": uri.replace("raw.githubusercontent.com/", "github.com/").replace(
                    "/" + ubc["revision"] + "/", "/blob/" + ubc["revision"] + "/", 1),
                "topic": rel.split("/")[0],
                "module": category(rel.split("/")[0]),
                "format": "ubc-myst-markdown",
                "review_status": "needs_academic_review",
                "semantic_dedup": "pending",
                "import_status": "raw_imported_not_exam_ready",
                "exam_eligible": False,
                "copyright_notice_preserved": True,
            })
            item["downloaded"] = True
            known_paths.add(fullpath)
            known_blobs.add(item["sha"])
            known_canonical.add(normalized_sha)
            report["added_count"] += 1
            report["added"].append({
                "id": pid, "source": SOURCE_LABELS["ubc_opbp"],
                "path": rel, "git_blob_sha": item["sha"],
                "module": category(rel.split("/")[0]), "license": license_name,
            })
        except (UnicodeDecodeError, ValueError, URLError, HTTPError,
                TimeoutError, OSError) as exc:
            reason = str(exc)[:180] or exc.__class__.__name__
            skipped["fetch_or_integrity_failure"] += 1
            report["failures"].append({"source": "ubc_opbp", "path": rel, "reason": reason})

    report["skipped_reasons"] = dict(skipped)
    report["source_additions"] = dict(Counter(x["source"] for x in report["added"]
                                               if "source" in x))
    report["remaining_not_downloaded"] = sum(
        not y.get("downloaded") for src in manifest["sources"] for y in src["files"]
    )
    if not dry_run:
        index["imported_questions"] = len(index["records"])
        ubc["raw_imported"] = len(index["records"])
        write_json(idx_path, index)
        write_json(manifest_path, manifest)
        write_json(decision_path, decisions)
        report["upstream_checks"] = upstream_revision_checks(manifest, timeout)
        latest = root / "logs" / "latest.json"
        write_json(latest, report)
        daily = root / "logs" / (now.strftime("%Y-%m-%d") + ".jsonl")
        daily.parent.mkdir(parents=True, exist_ok=True)
        with daily.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(report, ensure_ascii=False, separators=(",", ":")) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true",
                        help="Write verified raw candidates, indexes and run logs.")
    parser.add_argument("--limit", type=int, default=12, help="Max new candidates each run")
    parser.add_argument("--scan-limit", type=int, default=60, help="Max fresh candidates checked")
    parser.add_argument("--timeout", type=int, default=15)
    args = parser.parse_args()
    if not 1 <= args.limit <= 100 or not 1 <= args.scan_limit <= 500:
        parser.error("limit must be 1..100; scan-limit must be 1..500")
    report = execute(args.limit, args.scan_limit, args.timeout,
                     dry_run=not args.execute)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    summary = os.getenv("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as out:
            out.write("## University physics OER import\n\n")
            out.write(f"- Imported raw candidates: **{report['added_count']}**\n")
            out.write(f"- Inspected: {report['checked_candidates']}\n")
            out.write(f"- Remaining manifest candidates: {report['remaining_not_downloaded']}\n")
            out.write(f"- Failures: {len(report['failures'])}\n")
            out.write(f"- Skipped reasons: {json.dumps(report['skipped_reasons'], ensure_ascii=False)}\n\n")
            out.write("New records are **not exam-ready**; licensing and academic review remain required.\n")


if __name__ == "__main__":
    main()
