#!/usr/bin/env python3
"""705-entry source/figure queue and seven high-risk blockers; metadata gating only."""
import json
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parent
S=ROOT/"source_register.json"
D=json.loads(S.read_text(encoding="utf-8"))
assert len(D["entries"])==705
entries=D["entries"]
ids=[e["source_problem_number"] for e in entries]
assert len(ids)==len(set(ids))
figs=[e for e in entries if e["requires_original_figure"]]
assert len(figs)==159, f"Figure queue changed: {len(figs)}. Regenerate source_figure_recheck_queue.md."
assert all(e.get("textbook_pdf_pages") for e in figs)
expected={
 "15.3": "conditional_internal_physics_only",
 "17.11": "blocked_original_figure_domain_recheck",
 "18.27": "blocked_geometrically_impossible_under_axis_spacing_interpretation",
 "19.11": "conditional_internal_physics_only",
 "21.7": "blocked_unphysical_coherent_steady_current_assumption",
 "25.21": "blocked_original_figure_and_source_answer_recheck",
 "30.17": "conditional_internal_physics_only"
}
byid={e["source_problem_number"]:e for e in entries}
for name,status in expected.items():
 e=byid[name]
 audit=e.get("feasibility_deep_review",{})
 assert audit.get("status")==status,name
 assert audit.get("original_scan_reopened") is False,name
 assert audit.get("expert_review_completed") is False,name
 assert audit.get("review_type")=="independent_candidate_model_only",name
 assert audit.get("report")=="candidate_audit_feasibility_7.md",name
 assert len(e.get("risk_flags",[]))>0,name
for e in entries:
 assert e["exam_ready"] is False,e["source_problem_number"]
 assert e["academic_review"]=="pending_independent_verification",e["source_problem_number"]
assert byid["18.27"]["requires_original_figure"] is True
assert byid["17.11"]["requires_original_figure"] is True
assert byid["25.21"]["requires_original_figure"] is True
chapter_count=Counter(int(e["source_problem_number"].split(".")[0]) for e in figs)
doc=(ROOT/"source_figure_recheck_queue.md").read_text(encoding="utf-8")
for ch,count in chapter_count.items():
 assert f"| {ch} | {count} |" in doc
for e in figs:
 assert f"| {e['source_problem_number']} | {e['volume']} |" in doc,e["source_problem_number"]
assert "159/705" in doc
print("PASS 159 mandatory figure tasks mapped to 705 existing original end-chapter candidates.")
print("PASS 7 audited high-risk records remain unapproved with explicit physical/domain flags.")
print("PASS all 705 end-chapter records remain exam_ready=false and expert_review_pending.")
