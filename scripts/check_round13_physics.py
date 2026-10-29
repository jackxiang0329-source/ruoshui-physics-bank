#!/usr/bin/env python3
"""Round 13 final 50 x 4 machine-check gate. This is not independent expert signoff."""
import json, subprocess, sys
from pathlib import Path
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[1]
GROUPS=[["scripts/check_round13_draft.py","data/round13_draft_validation_report.json"],["scripts/check_round13_next6.py","data/round13_next6_validation_report.json"],["scripts/check_round13_third6.py","data/round13_third6_validation_report.json"],["scripts/check_round13_fourth6.py","data/round13_fourth6_validation_report.json"],["scripts/check_round13_sixth6.py","data/round13_sixth6_validation_report.json"],["scripts/check_round13_fifth6.py","data/round13_fifth6_validation_report.json"],["scripts/check_round13_seventh6.py","data/round13_seventh6_validation_report.json"],["scripts/check_round13_last8.py","data/round13_last8_validation_report.json"]]
manifest=json.loads((ROOT/'data/rounds/2026-10-29-13.json').read_text(encoding='utf8'))
ids=manifest['ids']
assert len(ids)==50 and len(set(ids))==50
checks=[]
for script,report in GROUPS:
    subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,check=True)
    doc=json.loads((ROOT/report).read_text(encoding='utf8'))
    assert len(doc['tests'])==doc['passed_count'] and all(t['passed'] is True for t in doc['tests'])
    checks.extend(doc['tests'])
assert len(checks)==200 and len({(x['id'],x['part']) for x in checks})==200
assert {(uid,part) for uid in ids for part in range(1,5)}=={(x['id'],x['part']) for x in checks}
methods=defaultdict(set)
for c in checks:
    assert c['method'] in {'symbolic','numerical','limit','dimensions','conservation','independent_derivation','physical_case'}
    assert len(c['name'])>=15
    methods[c['id']].add(c['method'])
assert all(len(methods[uid])>=2 for uid in ids)
report=dict(status='technical-qa-passed-expert-review-pending',new_problem_count=50,passed_count=200,tests=checks,independent_expert_review='pending')
(ROOT/'data/round13_validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('ROUND13 50 MODELS 200 DISTINCT PHYSICAL SUBPART CHECKS PASS; EXPERT REVIEW PENDING')
