#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Content-level 402-history/50-draft near-duplicate screening, not human originality approval.
Checks exact duplicates, medium-granularity character shingle similarity, and model
distinctions documented per draft item. Never marks expert review 'passed'.
"""
from pathlib import Path
import json,re,math,sys
ROOT=Path(__file__).resolve().parents[1]
db=json.loads((ROOT/"data/problems.json").read_text(encoding="utf-8"))
round14=json.loads((ROOT/"data/rounds/2026-10-29-14.json").read_text(encoding="utf-8"))
ids=set(round14["ids"])
assert len(ids)==50 and len(db)==452 and len({p["id"] for p in db})==452
main=[p for p in db if p["id"] not in ids]
draft=[p for p in db if p["id"] in ids]
assert len(main)==402 and len(draft)==50
audit=json.loads((ROOT/"data/round14_core_model_draft_audit.json").read_text(encoding="utf-8"))
audited={r["id"]:r for r in audit["rows"]}
assert set(audited)==ids and all(r.get("core") and r.get("substantive_difference") and
                                    r.get("expert_review")=="待独立复核"
                                    for r in audit["rows"])
def normalize(text):
    text=re.sub(r"\\[A-Za-z]+","",text.lower())
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]","",text)
def content(p):
    return normalize(p["title"]+" ".join(p["tags"])+
        p["question"][:2200]+p["solution"][:1300])
def grams(p):
    txt=content(p)
    return {txt[j:j+4] for j in range(len(txt)-3)}
vectors={p["id"]:grams(p) for p in db}
models={p["id"]:p for p in db}
def sim(a,b):
    aa,bb=vectors[a],vectors[b]
    if not aa or not bb:return 0
    return len(aa&bb)/math.sqrt(len(aa)*len(bb))
def top(uid,refs):
    return [{"id":v,"title":models[v]["title"],"normalized_shingle_similarity":round(score,6)}
            for score,v in sorted(((sim(uid,r),r) for r in refs),reverse=True)[:5]]
failure=[]
rows=[]
for p in draft:
    uid=p["id"]
    old=top(uid,[x["id"] for x in main])
    peer=top(uid,[x["id"] for x in draft if x["id"]!=uid])
    for other in main+draft:
        if other["id"]==uid:continue
        if normalize(other["title"])==normalize(p["title"]):
            failure.append((uid,other["id"],"identical title"))
        if normalize(other["question"])==normalize(p["question"]):
            failure.append((uid,other["id"],"identical question"))
    # Similarity is a warning only, not proof of unique core physics.
    rows.append({"id":uid,"historical_top5":old,"same_round_top5":peer,
                 "candidate_core":audited[uid]["core"],
                 "documented_distinction":audited[uid]["substantive_difference"],
                 "expert_review":"待独立复核"})
assert len(rows)==50
report={"round":14,"main_baseline_sha":round14["base_main_sha"],
        "historical_count":402,"draft_count":50,"cross_round_pairs":50*402,
        "same_round_pairs":50*49//2,"method":"4-character shingles over title/tags/first 2200 question and first 1300 solution chars; title/question exact-match gate",
        "interpretation":"algorithmic near-duplicate screening; not full independent physics-model expert verification",
        "exact_collision_findings":failure,"rows":rows,
        "quality_status":"待独立复核","independent_expert_review":"待独立复核"}
(ROOT/"data/round14_402_content_similarity_screen.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
if failure:
    print("HARD DUPLICATES",failure,file=sys.stderr)
    sys.exit(1)
print("ROUND14 CONTENT SCREEN: 402 historical × 50 new, 1225 within-round pairs; no exact title/question duplicates; human core-model assessment still pending")
