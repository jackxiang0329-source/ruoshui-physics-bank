#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inventory imported third-party physics problem sources without promoting to exams.

Run: python scripts/external_inventory.py
No API access or extra dependencies required. Prints JSON. Does not write files.
"""
import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXT = ROOT / "external_sources"


def canonical(text):
    """Conservative exact-content normalizer, not a semantic duplication oracle."""
    text = unicodedata.normalize("NFKC", text).lower()
    text = re.sub(r"## Attribution[\s\S]*$", "", text, flags=re.I)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def inventory(root=EXT):
    results = []
    issues = []
    all_ids = set()
    for source, extension in (("ubc_opbp", ".md"), ("webwork_opl", ".pg"),
                              ("webwork_thermal", ".pg"), ("intro_physics", ".md"),
                              ("hf_physics_dpo", ".md"), ("hf_seephys", ".md"), ("college_physics", ".md")):
        file = root / source / "index.json"
        if not file.exists():
            issues.append(f"缺少外部题源索引: {file.name} / {source}")
            continue
        info = json.loads(file.read_text(encoding="utf-8"))
        for item in info["records"]:
            pid = item["id"]
            if pid in all_ids:
                issues.append(f"外部题目重复ID: {pid}")
                continue
            all_ids.add(pid)
            # Never trust an imported manifest to select arbitrary filesystem paths.
            if not re.fullmatch(r"(?:UBC|OPL|THM|IP|HFDPO|SEEP|CP)-[0-9]{3,7}", pid):
                issues.append(f"不合法外部ID: {pid}")
                continue
            local = root / source / "raw" / (pid + extension)
            if not local.is_file():
                issues.append(f"外部原始题目缺失: {pid}")
                continue
            raw = local.read_text(encoding="utf-8")
            notice = item.get("license", "")
            if "CC" not in notice and "Apache" not in notice and "MIT" not in notice:
                issues.append(f"授权待核验: {pid}")
            if source == "ubc_opbp" and "## Attribution" not in raw:
                issues.append(f"UBC来源题缺少原始署名区: {pid}")
            if not item.get("source_url") and not item.get("upstream_url"):
                issues.append(f"缺少可追溯的原始链接: {pid}")
            blocked = ("needs_html_mathml_conversion" if source == "college_physics" else
                       "unverified_multimodal_source" if source == "hf_seephys" else
                       "unverified_generated_data" if source == "hf_physics_dpo" else
                       "extracted_example_needs_review" if source == "intro_physics" else
                       "WeBWorK" if source.startswith("webwork_") else
                       "external_media" if item.get("requires_media") else
                       "parametric_or_answer_pending")
            results.append({
                "id": pid,
                "source": source,
                "topic": item.get("topic") or item.get("chapter") or item.get("module") or "unknown",
                "license_signal": notice,
                "author": item.get("author", ""),
                "sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
                "normalized_sha256": hashlib.sha256(canonical(raw).encode("utf-8")).hexdigest(),
                "bytes": len(raw.encode("utf-8")),
                "exam_eligible": False,
                "requires_work": blocked,
            })
    duplicates = defaultdict(list)
    for rec in results:
        duplicates[rec["normalized_sha256"]].append(rec["id"])
    duplicate_groups = [v for v in duplicates.values() if len(v) > 1]
    return {
        "imported_raw_files": len(results),
        "sources": dict(Counter(x["source"] for x in results)),
        "subject_distribution": dict(Counter(x["topic"] for x in results)),
        "exam_eligible": 0,
        "duplicate_groups_exact_normalized": duplicate_groups,
        "blocking_issues": issues,
        "limitation": "仅检查源文件与目录、精确归一化重复、署名信号；不证明授权链、公式正确、语义去重或试卷质量。",
    }


if __name__ == "__main__":
    print(json.dumps(inventory(), ensure_ascii=False, indent=2))
