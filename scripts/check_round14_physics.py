#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Execute seven round14 QA modules and aggregate exactly 200 unique checked parts.
The machine report is not independent expert approval.
"""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
jobs=[
 ("scripts/check_round14_draft.py","data/round14_draft_validation_report.json"),
 ("scripts/check_round14_extra6.py","data/round14_extra6_validation_report.json"),
 ("scripts/check_round14_next6.py","data/round14_next6_validation_report.json"),
 ("scripts/check_round14_group3.py","data/round14_group3_validation_report.json"),
 ("scripts/check_round14_group4.py","data/round14_group4_validation_report.json"),
 ("scripts/check_round14_group5.py","data/round14_group5_validation_report.json"),
 ("scripts/check_round14_final8.py","data/round14_final8_validation_report.json")
]
alltests=[]
for script,report in jobs:
    subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,check=True)
    j=json.loads((ROOT/report).read_text(encoding="utf8"))
    tests=j["tests"]
    assert j["passed_count"]==len(tests),script
    alltests.extend(tests)
manifest=json.loads((ROOT/"data/rounds/2026-10-29-14.json").read_text(encoding="utf8"))
ids=manifest["ids"]
assert len(ids)==50 and len(set(ids))==50,(len(ids),"duplicate IDs")
actual={(p["id"],p["part"]) for p in alltests}
expected={(uid,part) for uid in ids for part in range(1,5)}
assert len(alltests)==200 and actual==expected,{"total":len(alltests),"missing":sorted(expected-actual),"extras":sorted(actual-expected)}
allowed=set(json.loads((ROOT/"data/rounds/quality_policy.json").read_text(encoding="utf8"))["allowed_evidence_methods"])
for t in alltests:
    assert t["passed"] is True
    assert t["method"] in allowed,(t["id"],t["method"])
    assert len(t["name"])>=15
assert all(len({t["method"] for t in alltests if t["id"]==uid})>=2 for uid in ids)
report={"round":14,"new_problem_count":50,"passed_count":200,
        "independent_expert_review":"待独立复核",
        "status":"all_200_machine_checks_executed; NOT independent expert review",
        "tests":alltests}
(ROOT/"data/round14_validation_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("ROUND14: 200/200 subparts executed; all 50 IDs; independent expert review pending")
