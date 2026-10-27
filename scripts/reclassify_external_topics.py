#!/usr/bin/env python3
"""Backfill subject labels using upstream taxonomy without rewriting questions.

Conservative: source subject strings and chapter titles remain unchanged; unknown
labels stay unknown, and no item becomes eligible for exam assembly.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

import import_hf_physics
import import_college_physics

BASE = Path(__file__).resolve().parent.parent / "external_sources"
SOURCES = (
    ("hf_physics_dpo", "domain", import_hf_physics.category),
    ("college_physics", "title", import_college_physics.group),
)

def backfill(root=BASE):
    results = {}
    for source, field, classifier in SOURCES:
        path = root / source / "index.json"
        if not path.is_file():
            results[source]={"updated":0,"missing_index":True}
            continue
        index=json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(index.get("records"),list):
            raise ValueError("Malformed candidate index: "+source)
        changed=0
        for record in index["records"]:
            old=record.get("module","待分类")
            new=classifier(record.get(field,""))
            if new!="待分类" and old!=new:
                # These are unverified external items; never silently approve.
                if record.get("exam_ready") or record.get("exam_eligible"):
                    raise ValueError("Cannot change taxonomy for an exam-approved external item")
                record["module"]=new
                changed+=1
        if changed:
            path.write_text(json.dumps(index,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        results[source]={
            "updated":changed,
            "still_unclassified":sum(r.get("module")=="待分类" for r in index["records"]),
            "total":len(index["records"]),
        }
    report={"timestamp_utc":datetime.now(timezone.utc).isoformat(),"sources":results,
            "notes":"Topic normalization only. Answers, copyright and semantic duplicates are unreviewed."}
    log=root/"logs"/"topic_backfill_latest.json"
    log.parent.mkdir(parents=True,exist_ok=True)
    log.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return report

if __name__=="__main__":
    backfill()
