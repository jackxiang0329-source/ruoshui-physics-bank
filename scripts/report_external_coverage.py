#!/usr/bin/env python3
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
    return {
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
if __name__=="__main__":
    main()
