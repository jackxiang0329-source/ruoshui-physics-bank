#!/usr/bin/env python3
"""STRICT round 13 originality block. Requires actual change of the flagged core models.
Do not delete the guard, rename ID, or change superficial parameters to bypass review.
"""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
audit=json.loads((ROOT/"data/round13_core_model_overlap_audit.json").read_text(encoding="utf8"))
if audit.get("round")!="13":raise SystemExit("Expected round 13 originality audit")
known=["M075","M076","E074","T069","T071","O072","Q071"]
entries={x["id"]:x for x in audit.get("unresolved_core_model_duplicates",[])}
problems=json.loads((ROOT/"data/problems.json").read_text(encoding="utf8"))
indexed={p["id"]:p for p in problems}
repeated=[]
for id_ in known:
    if id_ not in entries:raise SystemExit(f"Missing strict duplicate resolution record: {id_}")
    row=entries[id_]
    if row.get("resolution_status")!="resolved_replaced_with_distinct_physics":
        repeated.append(f"{id_}: {row.get('shared_core')}")
    elif not row.get("replacement_core") or not row.get("new_subpart_QA_path") or id_ not in indexed:
        raise SystemExit(f"Falsely or incompletely resolved duplicate record: {id_}")
if repeated:
    print("ROUND13 HISTORICAL CORE DUPLICATES MUST BE FIXED BEFORE MERGE:",file=sys.stderr)
    for item in repeated:print(" - "+item,file=sys.stderr)
    raise SystemExit(1)
if audit.get("moderate_risk_overlap_review"):
    remaining=[z for z in audit["moderate_risk_overlap_review"] if z.get("resolution_status")!="resolved_with_substantive_difference"]
    if remaining:raise SystemExit("Additional high similarity overlap needs substantiated documented decision: "+",".join(z["id"] for z in remaining))
print("Round13 historical core model review gate PASS")
