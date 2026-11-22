#!/usr/bin/env python3
"""Combined external candidate inventory and coverage audit.

python3 scripts/external_audit.py inventory
python3 scripts/external_audit.py coverage
Never marks unreviewed questions eligible for formal exams.
"""

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

# Curation-queue coverage audit
"""Audit the *candidate* physics inventory; never represent it as exam-ready."""
import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
EXT=ROOT/"external_sources"
COLUMNS=("id","source","module","license","license_review","answer_verified",
         "semantic_dedup","exam_ready","raw_path")
def audit(root=ROOT):
    path=root/"external_sources"/"curation_queue.csv"
    with path.open(encoding="utf-8-sig",newline="") as f:
        records=list(csv.DictReader(f))
    if not records:
        raise ValueError("External candidate queue is empty")
    ids=[x["id"] for x in records]
    if len(ids)!=len(set(ids)):
        raise ValueError("External candidate IDs are duplicated")
    source=Counter()
    modules=Counter()
    by_source=defaultdict(Counter)
    rights=Counter()
    missing=[]
    approved=[]
    unclassified=[]
    root_real=root.resolve()
    for record in records:
        if any(col not in record for col in COLUMNS):
            raise ValueError("External queue schema is incomplete")
        pid=record["id"]
        raw=record["raw_path"]
        dest=root/raw
        if (not raw.startswith("external_sources/") or
            not dest.resolve().is_relative_to(root_real/"external_sources")):
            raise ValueError("Escaping raw file path for "+pid)
        if not dest.is_file():
            missing.append({"id":pid,"file":raw})
        name=record["source"];subject=record["module"]
        source[name]+=1
        modules[subject]+=1
        by_source[name][subject]+=1
        rights[record.get("license","unspecified")]+=1
        if subject=="待分类":
            unclassified.append(pid)
        if str(record["exam_ready"]).strip().lower() not in ("no","false","0",""):
            approved.append(pid)
    if missing:
        raise ValueError("Missing external raw files: "+json.dumps(missing[:8],ensure_ascii=False))
    if approved:
        raise ValueError("Unreviewed external source marked exam-ready: "+",".join(approved[:8]))
    # Summarize upstream taxonomy signals to enable auditable, conservative
    # class mappings on future runs without fetching huge indexes in ChatGPT.
    missing_hf_domains=Counter()
    hf_path=root/"external_sources"/"hf_physics_dpo"/"index.json"
    if hf_path.exists():
        hf_idx=json.loads(hf_path.read_text(encoding="utf-8"))
        for rec in hf_idx.get("records",[]):
            if rec.get("module")=="待分类":
                missing_hf_domains[str(rec.get("domain","unknown"))]+=1
    missing_cp_titles=Counter()
    college_path=root/"external_sources"/"college_physics"/"index.json"
    if college_path.exists():
        college_idx=json.loads(college_path.read_text(encoding="utf-8"))
        for rec in college_idx.get("records",[]):
            if rec.get("module")=="待分类":
                missing_cp_titles[str(rec.get("title","unknown"))]+=1
    return {
      "unclassified_hf_domains":dict(missing_hf_domains.most_common(100)),
      "unclassified_college_chapters":dict(missing_cp_titles.most_common(100)),
      "generated_utc":datetime.now(timezone.utc).isoformat(),
      "raw_candidate_count":len(records),
      "exam_ready_external_count":0,
      "by_source":dict(source.most_common()),
      "by_module":dict(modules.most_common()),
      "source_module_matrix":{name:dict(c.most_common()) for name,c in sorted(by_source.items())},
      "license_signals":dict(rights.most_common()),
      "unclassified_count":len(unclassified),
      "unclassified_id_examples":unclassified[:20],
      "missing_raw_files":0,
      "quality_note":"Source-count not verified-unique; semantic dedup, solutions, physics validity and license chains remain pending.",
    }
def main():
    report=audit()
    path=EXT/"catalog"/"coverage_report.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:report[k] for k in ("raw_candidate_count","exam_ready_external_count","by_source","by_module","unclassified_count")},ensure_ascii=False,indent=2))

def cli():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode",choices=("inventory","coverage"))
    args=parser.parse_args()
    if args.mode=="inventory":
        print(json.dumps(inventory(),ensure_ascii=False,indent=2))
    else:
        main()


if __name__=="__main__":
    cli()
