#!/usr/bin/env python3
"""Static format/risk checks for external OER human-review candidates.

Never checks physics correctness or grants exam eligibility. A 'simple' flag only
means no *recognized markup obstacle*, not a license or academic approval.
"""
import csv
import html
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
EXT=ROOT/"external_sources"
FIELDS=["id","source","module","original_topic","source_question_type",
        "plain_text_chars","mathml_nodes","math_formula_signal",
        "review_complexity","risk_flags","pending_checks","exam_ready"]
MATH=re.compile(r"<(?:math|mfrac|msup|msub|msqrt|mrow)\b",re.I)
IMAGE=re.compile(r"(?i)<img\b|!\[[^]]*\]\(|\\includegraphics|"
                 r"\b(?:figure|fig\.|diagram|image|graph)\s*(?:[1-9]\d*|below|above)\b|"
                 r"(?:shown|depicted|illustrated)\s+in\s+(?:the|a)\s+(?:figure|diagram|image)")
REFERENCE=re.compile(r"(?i)\[\[link\]\]|\]\(#|(?:see|refer to)\s+(?:the\s+)?(?:section|previous example|chapter|above|below)\b|\b(?:same\s+\w+\s+as\s+problem\s+\d+|(?:problem|example|lesson)\s+\d+(?:\.\d+)?)\b")
PLACEHOLDER=re.compile(r"\{\{[^{}]{1,160}\}\}|\$\{[^{}]{1,160}\}")
ANSWER=re.compile(r"(?im)^#{1,5}\s*Answer Section\b|<div\s+data-type=[\"']solution[\"']")
TAG=re.compile(r"<[^>]*>")
WORD=re.compile(r"[a-zA-Z]{2,}")
def question_part(raw,source):
    """Separate question from source notice without removing original raw material."""
    if source=="UBC OPBP":
        body=raw
        if raw.startswith("---"):
            sep=raw.find("\n---",4)
            if sep!=-1:body=raw[sep+4:]
        body=re.split(r"(?im)^##\s+Attribution\b",body,maxsplit=1)[0]
        return body
    # Historical CP and PHYS2425 use a final Markdown divider before notices.
    return raw.split("\n---\n",1)[0]

def inspect(question,source):
    flags=[]
    def add(name,condition):
        if condition:flags.append(name)
    add("media_or_figure_reference",bool(IMAGE.search(question)))
    add("cross_reference",bool(REFERENCE.search(question)))
    add("parameter_template",bool(PLACEHOLDER.search(question)))
    add("embedded_answer_section",bool(ANSWER.search(question)))
    nodes=len(MATH.findall(question))
    plain=html.unescape(TAG.sub(" ",question))
    plain=re.sub(r"(?m)^#{1,6}\s.*$"," ",plain)
    plain=re.sub(r"\s+"," ",plain).strip()
    add("short_extracted_text",len(plain)<55)
    add("mathml_requires_conversion",nodes>0)
    add("unbalanced_math_markup",question.lower().count("<math")!=question.lower().count("</math>"))
    if any(v in flags for v in ("media_or_figure_reference","cross_reference","parameter_template",
                                "embedded_answer_section","unbalanced_math_markup")):
        complexity="complex_source_review"
    elif flags:
        complexity="format_review"
    else:
        complexity="standard_manual_review"
    return {"plain_text_chars":len(plain),"mathml_nodes":nodes,
            "math_formula_signal":"yes" if nodes else "no",
            "risk_flags":flags,"review_complexity":complexity,"plain_text":plain}

def find_close_text(rows):
    """Only near-textual duplicates among the shortlist, not semantic duplicates."""
    tokens={}
    for row in rows:
        text=row.get("_text","")
        words=[w.lower() for w in WORD.findall(text)]
        tokens[row["id"]]=set(words) if len(words)>=12 else set()
    pairs=[]
    for i,a in enumerate(rows):
        words=tokens[a["id"]]
        if not words:continue
        for b in rows[i+1:]:
            other=tokens[b["id"]]
            if not other or abs(len(words)-len(other))>max(5,len(words)//4):continue
            jaccard=len(words&other)/len(words|other)
            if jaccard>=0.88:
                pairs.append({"ids":[a["id"],b["id"]],"token_set_jaccard":round(jaccard,3)})
    return sorted(pairs,key=lambda x:-x["token_set_jaccard"])[:50]

def run(root=ROOT):
    ext=root/"external_sources"
    target=ext/"catalog"/"review_priority.csv"
    with target.open(encoding="utf-8-sig",newline="") as f:
        source=list(csv.DictReader(f))
    types={}
    for collection in ("college_physics","intro_physics","physics_refresher"):
        ip=ext/collection/"index.json"
        if ip.is_file():
            for item in json.loads(ip.read_text(encoding="utf-8")).get("records",[]):
                types[item["id"]]=item.get("question_type", item.get("section", "concept_or_example"))
    records=[];risks=Counter();modules=Counter();types_seen=Counter();complexity=Counter()
    for item in source:
        if item["exam_ready"].strip().lower() not in ("no","false","0",""):
            raise ValueError("Review worklist contains exam-ready candidate: "+item["id"])
        relative=item["raw_path"]
        file=(root/relative).resolve()
        if not relative.startswith("external_sources/") or not file.is_relative_to(ext.resolve()):
            raise ValueError("Unsafe external source path: "+relative)
        if not file.is_file():raise ValueError("Missing review source: "+relative)
        question=question_part(file.read_text(encoding="utf-8"),item["source"])
        review=inspect(question,item["source"])
        kind=types.get(item["id"],"needs_manual_type_review")
        entry={
            "id":item["id"],"source":item["source"],"module":item["module"],
            "original_topic":item["original_topic"],"source_question_type":kind,
            "plain_text_chars":review["plain_text_chars"],
            "mathml_nodes":review["mathml_nodes"],
            "math_formula_signal":review["math_formula_signal"],
            "review_complexity":review["review_complexity"],
            "risk_flags":";".join(review["risk_flags"]),
            "pending_checks":item["pending_checks"],"exam_ready":"no",
            "_text":review["plain_text"],
        }
        records.append(entry);risks.update(review["risk_flags"])
        modules[item["module"]]+=1;types_seen[kind]+=1;complexity[review["review_complexity"]]+=1
    dest=ext/"catalog"/"review_preflight.csv"
    with dest.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator="\n");w.writeheader()
        for record in records:w.writerow({k:record[k] for k in FIELDS})
    summary={
        "generated_utc":datetime.now(timezone.utc).isoformat(),
        "total_reviewed_by_static_checks":len(records),
        "by_module":dict(modules),
        "by_source_question_type":dict(types_seen),
        "format_review_complexity":dict(complexity),
        "recognized_risk_flags":dict(risks),
        "near_textual_duplicate_pairs":find_close_text(records),
        "exam_ready_added":0,
        "limitations":"Automated format/risk signals only; NOT physics solving, answer verification, rights-chain approval, semantic dedup or exam readiness.",
    }
    (ext/"catalog"/"review_preflight_report.json").write_text(
        json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    return summary
if __name__=="__main__":run()
