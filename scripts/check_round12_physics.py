#!/usr/bin/env python3
"""Round 12 release candidate: execute exactly 200 substantive per-subpart checks.

This automation establishes mathematical/physical test coverage, NOT expert signoff.
"""
import json
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCES=[
    ("scripts/check_round12_draft.py","data/round12_draft_validation_report.json",120),
    ("scripts/check_round12_continuation.py","data/round12_continuation_validation_report.json",16),
    ("scripts/check_round12_next4.py","data/round12_continuation2_validation_report.json",16),
    ("scripts/check_round12_mechanics_electromagnetism.py","data/round12_mechanics_electromagnetism_validation_report.json",16),
    ("scripts/check_round12_last8.py","data/round12_last8_validation_report.json",32),
]
manifest=json.loads((ROOT/"data/rounds/2026-10-28-12.json").read_text(encoding="utf8"))
ids=manifest["ids"]
assert len(ids)==50 and len(set(ids))==50
checks=[]
for script,report,count in SOURCES:
    subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,check=True)
    part=json.loads((ROOT/report).read_text(encoding="utf8"))
    assert len(part["tests"])==count and part["passed_count"]==count,(script,part.get("passed_count"))
    checks.extend(part["tests"])
assert len(checks)==200
expected={(uid,part) for uid in ids for part in (1,2,3,4)}
observed={(x["id"],x["part"]) for x in checks}
assert len(observed)==200 and observed==expected
allowed={"symbolic","numerical","limit","dimensions","conservation","independent_derivation","physical_case"}
for x in checks:
    assert x["passed"] is True and x["method"] in allowed and len(x["name"])>=15
for uid in ids:
    assert len({x["method"] for x in checks if x["id"]==uid})>=2,uid
report={
    "round":"12",
    "status":"technically_verified_by_executable_checks_pending_expert_review",
    "new_problem_count":50,
    "passed_count":200,
    "tests":checks,
    "independent_expert_review":"pending",
}
out=ROOT/"data/round12_validation_report.json"
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print(json.dumps({"round":12,"new_items":50,"passed_subpart_checks":200,
                  "independent_expert_review":"pending"},ensure_ascii=False))
