#!/usr/bin/env python3
"""Prioritize provenance-traceable university physics OER for HUMAN review.

The CSV is a review worklist, NEVER an exam-ready or solution-verified bank.
Index hashes are source-provided and not a substitute for semantic deduplication.
"""
import csv
import json
import re
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "external_sources"
PRIORITIES = (
    ("OpenStax College Physics (historical mirror)", 60, "convert_html_mathml;verify_answer;check_illustrations"),
    ("UBC OPBP", 45, "validate_attribution;verify_answer;check_illustrations"),
    ("Introductory Physics (PHYS 2425)", 15, "verify_excerpt_context;verify_answer;check_illustrations"),
)
DIGEST_INDEXES = (
    ("hf_physics_dpo", "question_sha256"),
    ("hf_seephys", "question_sha256"),
    ("intro_physics", "question_sha256"),
    ("college_physics", "question_sha256"),
)
FIELDNAMES = (
    "review_order", "id", "source", "module", "original_topic", "license",
    "author", "source_url", "raw_path", "pending_checks", "exam_ready",
)

def permissible_signal(license_text):
    """Conservative signal check, not a rights determination."""
    s = str(license_text)
    return bool(re.search(r"\bCC[\s-]?BY\s*[34](?:\.0)?\b", s, re.I)
                and not re.search(r"\bNC\b|non.?commercial|all rights reserved", s, re.I))

def spread(rows, limit):
    """Diversify by chapter subject, rather than picking a first-file-only sample."""
    pools = defaultdict(deque)
    for item in rows:
        pools[item.get("module") or "待分类"].append(item)
    result = []
    labels = sorted(pools)
    while labels and len(result) < limit:
        next_labels = []
        for label in labels:
            if len(result) >= limit:
                break
            if pools[label]:
                result.append(pools[label].popleft())
            if pools[label]:
                next_labels.append(label)
        labels = next_labels
    return result

def digest_overlaps(root):
    positions = defaultdict(list)
    for source, field in DIGEST_INDEXES:
        path = root / source / "index.json"
        if not path.is_file():
            continue
        info = json.loads(path.read_text(encoding="utf-8"))
        for item in info.get("records", []):
            digest = item.get(field)
            if isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest):
                positions[digest].append({"id": item["id"], "source": source})
    groups = [members for members in positions.values() if len(members) > 1]
    cross = [members for members in groups if len({m["source"] for m in members}) > 1]
    return {"same_digest_groups": len(groups), "cross_source_digest_groups": len(cross),
            "cross_source_examples": cross[:20],
            "limitation": "Only source-provided SHA256 question digests. Extraction and normalization differ by format; this is NOT semantic deduplication."}

def generate(root=BASE):
    source_path = root / "curation_queue.csv"
    with source_path.open("r", encoding="utf-8-sig", newline="") as handle:
        originals = list(csv.DictReader(handle))
    all_ids = set()
    by_source = defaultdict(list)
    licensing_excluded = Counter()
    for item in originals:
        problem_id = item.get("id", "")
        if not problem_id or problem_id in all_ids:
            raise ValueError("Missing or duplicated candidate ID: " + problem_id)
        all_ids.add(problem_id)
        if str(item.get("exam_ready", "")).strip().lower() not in ("no", "false", "0", ""):
            raise ValueError("Unreviewed external question has exam-ready flag: " + problem_id)
        src = item.get("source", "")
        if not permissible_signal(item.get("license", "")):
            licensing_excluded[src] += 1
            continue
        relative = item.get("raw_path", "")
        path = root.parent / relative
        if not relative.startswith("external_sources/") or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError("Unsafe source file path: " + problem_id)
        if not path.is_file():
            raise ValueError("Missing raw file for triage: " + problem_id)
        by_source[src].append(item)
    selected = []
    contribution = {}
    for source, quota, checks in PRIORITIES:
        picks = spread(by_source.get(source, []), quota)
        contribution[source] = len(picks)
        for item in picks:
            selected.append({
                "review_order": len(selected) + 1,
                "id": item["id"], "source": source,
                "module": item.get("module", "待分类"),
                "original_topic": item.get("original_topic", ""),
                "license": item["license"], "author": item.get("author", ""),
                "source_url": item["source_url"], "raw_path": item["raw_path"],
                "pending_checks": checks + ";rights_chain;semantic_dedup",
                "exam_ready": "no",
            })
    folder = root / "catalog"
    folder.mkdir(parents=True, exist_ok=True)
    worklist = folder / "review_priority.csv"
    with worklist.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(selected)
    report = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "all_external_candidates": len(originals),
        "priority_review_count": len(selected),
        "priority_sources": contribution,
        "excluded_from_priority_due_to_license_signal": dict(licensing_excluded),
        "content_digest_overlaps": digest_overlaps(root),
        "exam_ready_added": 0,
        "notes": "Priority list is not a license approval, independently solved exam, or full cross-source semantic dedup.",
    }
    (folder / "review_triage_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return report

if __name__ == "__main__":
    generate()
