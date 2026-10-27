#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Conservative text-only SeePhys/SeePhys acquisition for manual review.

Images, external illustrations, copyrighted exam sources, and any uncertain
rights-chain remain excluded or unapproved. This never updates bank/.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parent.parent / "external_sources"
DATASET = "SeePhys/SeePhys"
ROOT = BASE / "hf_seephys"
URL = "https://huggingface.co/datasets/" + DATASET
ALLOWED = "apache-2.0"
TOPICS = [
    ("力学", ("mechanic", "dynamics", "kinemat", "fluid", "classical", "gravity")),
    ("热学", ("thermal", "thermo", "statistical", "heat")),
    ("电磁学", ("electric", "magnetic", "electromagnet", "circuit")),
    ("光学", ("optics", "optical", "light", "photonic")),
    ("振动与波动", ("wave", "acoustic", "oscill", "vibrat")),
    ("近代物理", ("quantum", "atomic", "nuclear", "relativ", "particle", "condensed", "modern")),
]
IMAGE_REFS = re.compile(
    r"(?i)<img\b|!\[[^]]*\]\(|\{numref\}|\{ref\}|"
    r"(?:figure|fig\.|diagram|image|plot|picture|graph)\s*[\d:(]|"
    r"(?:shown|depicted|illustrated)\s+in\s+(?:the|a|this)\s+"
    r"(?:figure|image|diagram|plot|picture|graph)|"
    r"see\s+(?:the|figure|fig\.|image|diagram|plot|picture|graph)"
)
def compact(text):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text).casefold()).strip()
def sha(text):
    return hashlib.sha256(compact(text).encode("utf-8")).hexdigest()
def topic(name):
    label = str(name or "").casefold()
    for subject, keys in TOPICS:
        if any(k in label for k in keys):
            return subject
    return "待分类"
def json_api(url, timeout=20):
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "RuoshuiPhysicsOER/2.3"})
    with urlopen(request, timeout=timeout) as response:
        raw = response.read(9000001)
    if len(raw) > 9000000:
        raise ValueError("hf_payload_exceeds_safe_limit")
    return json.loads(raw.decode("utf-8"))
def revision(timeout=20):
    m = json_api("https://huggingface.co/api/datasets/" + DATASET, timeout)
    labels = (m.get("cardData") or {}).get("license")
    if labels != ALLOWED and "license:" + ALLOWED not in m.get("tags", []):
        raise ValueError("seephys_license_not_explicit_apache2")
    if m.get("private") or m.get("gated") not in (False, None):
        raise ValueError("seephys_dataset_private_or_gated")
    rev = m.get("sha")
    if not re.fullmatch(r"[a-f0-9]{40}", str(rev)):
        raise ValueError("seephys_revision_unverifiable")
    return rev
def valid(row):
    if not isinstance(row, dict):
        return None
    if row.get("images") not in (None, []):
        return None
    statement = row.get("question")
    if not isinstance(statement, str):
        return None
    statement = statement.strip()
    if not 35 <= len(statement) <= 4000:
        return None
    if IMAGE_REFS.search(statement):
        return None
    # Keep records as references to their original dataset, not verified exam questions.
    return statement
def read(path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else default
def write(path, doc):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
def run(limit=100, scan_limit=250, timeout=20, version_getter=None, page_getter=None, base=BASE):
    d = base / "hf_seephys"
    manifest_path = d / "manifest.json"
    index_path = d / "index.json"
    m = read(manifest_path, {"dataset": DATASET, "config": "default", "split": "train",
                             "revision": None, "next_offset": 0, "total_rows": None})
    idx = read(index_path, {"records": [], "count": 0, "exam_eligible_count": 0})
    if (m.get("dataset"), m.get("config"), m.get("split")) != (DATASET, "default", "train"):
        raise ValueError("manifest_identity_mismatch")
    get_ver = version_getter or (lambda: revision(timeout))
    current = get_ver()
    if m.get("revision") and m["revision"] != current:
        raise ValueError("dataset_revision_changed_requires_review")
    m["revision"] = current
    def page(offset, amount):
        params = urlencode({"dataset": DATASET, "config": "default", "split": "train",
                            "offset": offset, "length": amount})
        return json_api("https://datasets-server.huggingface.co/rows?" + params, timeout)
    get_page = page_getter or page
    old_offset = int(m.get("next_offset", 0))
    offset = old_offset
    total = m.get("total_rows")
    prior = {x["question_sha256"] for x in idx["records"]}
    cross_path = base / "hf_physics_dpo" / "index.json"
    if cross_path.is_file():
        prior.update(x["question_sha256"] for x in read(cross_path, {"records": []})["records"])
    ident = max((int(x["id"].split("-")[-1]) for x in idx["records"]), default=0)
    pending = []
    reasons = {}
    failures = []
    scanned = 0
    def skip(reason):
        reasons[reason] = reasons.get(reason, 0) + 1
    try:
        while scanned < scan_limit and len(pending) < limit:
            if isinstance(total, int) and offset >= total:
                break
            requested = min(25, scan_limit - scanned)
            payload = get_page(offset, requested)
            if payload.get("partial"):
                raise ValueError("partial_dataset_viewer_response")
            fields = {x.get("name") for x in payload.get("features", [])}
            if not {"question", "images", "subject"}.issubset(fields):
                raise ValueError("unexpected_dataset_schema")
            total = payload.get("num_rows_total")
            if not isinstance(total, int):
                raise ValueError("missing_total_row_count")
            rows = payload.get("rows", [])
            if not rows:
                break
            for item in rows:
                if item.get("row_idx") != offset:
                    raise ValueError("dataset_row_order_changed")
                row = item.get("row") or {}
                number = offset
                offset += 1
                scanned += 1
                question = valid(row)
                if not question:
                    skip("multimodal_or_incomplete_question")
                    continue
                if row.get("level") is not None and not isinstance(row["level"], int):
                    skip("unverifiable_academic_level")
                    continue
                if not isinstance(row.get("subject"), str) or not row["subject"].strip():
                    skip("missing_physics_subject")
                    continue
                digest = sha(question)
                if digest in prior:
                    skip("normalized_duplicate")
                    continue
                ident += 1
                problem_id = "SEEP-" + str(ident).zfill(5)
                pending.append((problem_id, number, question, digest,
                                str(row["subject"]), row.get("level")))
                prior.add(digest)
                if len(pending) >= limit:
                    break
            if len(rows) < requested:
                break
    except Exception as exc:
        failures.append({"at_row": offset, "reason": str(exc)[:220]})
    # Transactional: create files only after checking the source did not change.
    if get_ver() != current:
        raise ValueError("dataset_changed_during_collection_no_files_committed")
    for pid, row_no, statement, digest, subject, level in pending:
        target = d / "raw" / (pid + ".md")
        if target.exists():
            raise ValueError("duplicate_id_file_present")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            "# " + pid + "\n\n" + statement + "\n\n---\n"
            "Dataset: " + URL + "\nDataset row: " + str(row_no)
            + "\nDataset revision observed: " + current
            + "\nLicense metadata: Apache-2.0 (underlying question rights need review)."
            + "\nAnswers, completeness and originality have NOT been verified."
            + "\nExam-ready: no.\n", encoding="utf-8"
        )
        idx["records"].append({
            "id": pid, "source": DATASET, "source_url": URL,
            "row_idx": row_no, "dataset_revision_observed": current,
            "source_subject": subject, "module": topic(subject),
            "level_signal": level, "question_sha256": digest,
            "license": "Apache-2.0 (dataset label; per-item rights review pending)",
            "author": "SeePhys dataset contributors",
            "license_review": "pending", "answer_verified": False,
            "semantic_dedup": "pending", "exam_ready": False,
            "status": "unverified_text_only_question",
        })
    m["next_offset"] = offset
    m["total_rows"] = total
    idx["count"] = len(idx["records"])
    write(manifest_path, m)
    write(index_path, idx)
    report = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "run_id": os.environ.get("GITHUB_RUN_ID", "local"),
        "source": DATASET, "revision_observed": current,
        "added_count": len(pending), "added_ids": [x[0] for x in pending],
        "scanned": scanned, "offset_before": old_offset, "offset_after": offset,
        "total_rows": total, "skipped": reasons, "failures": failures,
        "exam_ready_added": 0,
        "note": "Only self-contained text; multimedia skipped; not university exam-verified.",
    }
    write(base / "logs" / "seephys_import_latest.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--scan-limit", type=int, default=250)
    parser.add_argument("--timeout", type=int, default=20)
    opts = parser.parse_args()
    if not (1 <= opts.limit <= 100 and 1 <= opts.scan_limit <= 500):
        parser.error("Limits exceeded")
    try:
        run(opts.limit, opts.scan_limit, opts.timeout)
    except Exception as exc:
        report = {"timestamp_utc": datetime.now(timezone.utc).isoformat(),
                  "source": DATASET, "added_count": 0,
                  "failures": [{"reason": str(exc)[:300]}],
                  "exam_ready_added": 0}
        write(BASE / "logs" / "seephys_import_latest.json", report)
        print(json.dumps(report, ensure_ascii=False))
        return 1
    return 0
if __name__ == "__main__":
    sys.exit(main())
