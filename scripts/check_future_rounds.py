#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gate for complete 100-item rounds from round 11 onward.

Automated checks never represent independent human expert review.
"""
import collections
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUND_DIR = ROOT / "data" / "rounds"
POLICY = json.loads((ROUND_DIR / "quality_policy.json").read_text(encoding="utf8"))
FILENAMES = re.compile(r"^\d{4}-\d{2}-\d{2}-(\d{2,3})\.json$")
SECTIONS = re.compile(r"(?m)^\(([1-4])\)\s*")
FORBIDDEN = (r"\write18", r"\input", r"\include", r"\documentclass", r"\openout", r"\catcode")
TOPIC_PREFIXES = POLICY["topic_prefixes"]

def load(path):
    return json.loads(path.read_text(encoding="utf8"))

def reject(message):
    raise ValueError(message)

def parts(text):
    marks = list(SECTIONS.finditer(text))
    if len(marks) != 4 or [m.group(1) for m in marks] != ["1","2","3","4"]:
        return None
    return [text[marks[i].end():(marks[i+1].start() if i<3 else len(text))].strip()
            for i in range(4)]

def check():
    baseline=set(POLICY["baseline_ids"])
    if len(baseline)!=252 or POLICY["exact_new_items_per_round"]!=100:
        reject("policy baseline or quota damaged")
    all_items=load(ROOT/"data/problems.json")
    by_id={p["id"]:p for p in all_items}
    current=set(by_id)
    if len(current)!=len(all_items) or not baseline.issubset(current):
        reject("duplicate source ID or baseline ID removed")
    manifests=[]
    for path in ROUND_DIR.glob("*.json"):
        hit=FILENAMES.fullmatch(path.name)
        if hit and int(hit.group(1))>=POLICY["first_enforced_round"]:
            manifests.append((int(hit.group(1)),path))
    manifests.sort()
    if len(current)==252 and not manifests:
        print("100-item round gate armed; baseline=252; next round=11")
        return 0
    if len(current)!=252+100*len(manifests):
        reject("incomplete new round or 100-item manifest missing")
    known=set(baseline)
    for index,(round_no,path) in enumerate(manifests):
        if round_no!=11+index:
            reject("future round numbers must be consecutive starting at 11")
        entry=load(path)
        ids=entry.get("ids")
        if not isinstance(ids,list) or len(ids)!=100 or len(set(ids))!=100:
            reject(f"round {round_no}: exactly 100 distinct IDs required")
        for k,v in (("base_count",252+100*index),("active_total",352+100*index),
                    ("target_new_items",100),("actual_new_items",100)):
            if entry.get(k)!=v:
                reject(f"round {round_no}: wrong {k}")
        if str(entry.get("round","")).lstrip("0")!=str(round_no):
            reject(f"round {round_no}: manifest round mismatch")
        new=set(ids)
        if new&known or not new.issubset(current):
            reject(f"round {round_no}: ID reused or missing")
        counts=collections.Counter(by_id[i]["topic"] for i in ids)
        if set(counts)!=set(TOPIC_PREFIXES) or sorted(counts.values())!=POLICY["per_topic_counts"]:
            reject(f"round {round_no}: six-topic 16/17 balance violated")
        if entry.get("topic_counts")!=dict(counts):
            reject(f"round {round_no}: manifest counts mismatch")
        for uid in ids:
            p=by_id[uid]
            if not re.fullmatch(r"[METWOQ]\d{3,5}",uid) or uid[0]!=TOPIC_PREFIXES[p["topic"]]:
                reject(f"{uid}: ID/topic mismatch")
            if p.get("tier")!="advanced_composite" or p.get("level") not in (4,5):
                reject(f"{uid}: basic problem excluded")
            if p.get("estimated_minutes",0)<40 or len(set(p.get("tags",[])))<3:
                reject(f"{uid}: inadequate cross-topic complexity")
            if p.get("quality_status")!="待独立复核":
                reject(f"{uid}: independent review attestation not substantiated")
            if p.get("kind") in ("选择题","填空题","简单计算题"):
                reject(f"{uid}: low-level format")
            for name in ("question","solution"):
                body=p.get(name)
                source=ROOT/"bank"/uid/(name+".tex")
                if not isinstance(body,str) or not source.exists() or source.read_text(encoding="utf8")!=body:
                    reject(f"{uid}: {name} missing or not synchronized")
                if any(x in body for x in FORBIDDEN) or any(ord(ch)<32 and ch not in "\r\n\t" for ch in body):
                    reject(f"{uid}: unsafe TeX fragment")
            qs=parts(p["question"])
            ss=parts(p["solution"])
            if not qs or not ss or min(map(len,qs))<25:
                reject(f"{uid}: exactly four substantive question subparts required")
            if min(map(len,ss))<POLICY["minimum_solution_part_chars"]:
                reject(f"{uid}: each of four subparts needs a rigorous derivation")
            if not str(p.get("answer","")).strip():
                reject(f"{uid}: final formula missing")
        script=ROOT/"scripts"/f"check_round{round_no:02d}_physics.py"
        if not script.exists():
            reject(f"round {round_no}: no independent executable verification program")
        subprocess.run([sys.executable,str(script)],cwd=ROOT,check=True)
        report_path=ROOT/"data"/f"round{round_no:02d}_validation_report.json"
        if not report_path.exists():
            reject(f"round {round_no}: missing executed QA report")
        report=load(report_path)
        tests=report.get("tests",[])
        if report.get("new_problem_count")!=100 or report.get("passed_count")!=400 or len(tests)!=400:
            reject(f"round {round_no}: must execute 400 successful subpart checks")
        checked=set()
        methods=collections.defaultdict(set)
        for t in tests:
            uid,part,method=t.get("id"),t.get("part"),t.get("method")
            if uid not in new or type(part)!=int or part not in (1,2,3,4):
                reject("test ID or subpart is invalid")
            if (uid,part) in checked or t.get("passed") is not True:
                reject(f"{uid}: duplicate or failed subpart test")
            if method not in POLICY["allowed_evidence_methods"]:
                reject(f"{uid}: invalid check method")
            if not isinstance(t.get("name"),str) or len(t["name"].strip())<15:
                reject(f"{uid}: insufficient explanation of check")
            checked.add((uid,part))
            methods[uid].add(method)
        if checked!={(uid,part) for uid in ids for part in range(1,5)}:
            reject("not all 400 individual subparts have runnable checks")
        if any(len(methods[uid])<2 for uid in ids):
            reject("each problem needs at least two different verification methods")
        known.update(new)
    if current!=known:
        reject("found unmanifested problems outside accepted 100-item rounds")
    print(json.dumps({"status":"passed","problem_count":len(current),
        "new_rounds":len(manifests),"technical_subpart_checks":400*len(manifests),
        "expert_signoff":"not established by automated verification"},ensure_ascii=False))
    return 0

if __name__=="__main__":
    try:
        sys.exit(check())
    except (ValueError,KeyError,TypeError,AssertionError,subprocess.CalledProcessError) as exc:
        print("FUTURE ROUND REJECTED:",exc,file=sys.stderr)
        sys.exit(1)
