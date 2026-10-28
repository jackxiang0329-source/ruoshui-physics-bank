#!/usr/bin/env python3
"""Exhaustive static audit of *every* pinned College Physics candidate.

This audits source integrity and editing obstacles, NOT scientific truth,
license chain approval, semantic uniqueness, solution validity or exam readiness.
All output remains under external_sources/catalog, never bank/.
"""
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path

import import_college_physics as college
import college_tex_draft as tex
import review_preflight as preflight

ROOT=Path(__file__).resolve().parent.parent
SOURCE="OpenStax College Physics (historical mirror)"
MODULE_ORDER=("力学","热学","电磁学","振动与波动","光学","近代物理","物理基础")
COLUMNS=("id","module","chapter","question_type","source_url",
         "source_sha","question_sha256","plain_chars","mathml_expressions",
         "risk_flags","format_tier","review_status","exam_ready")
NEXT_COLUMNS=("review_order","id","module","chapter","question_type",
              "source_url","raw_path","reason","exam_ready")
NUMBER=re.compile(r"(?<![a-z])[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")
SPACE=re.compile(r"\s+")
def src_question(raw):
    """Recover source excerpt between archive header and attribution divider."""
    body=preflight.question_part(raw,SOURCE)
    if "\n\n" not in body:
        return ""
    return body.split("\n\n",1)[1].strip()
def number_template(text):
    text=text.lower()
    text=re.sub(r"<[^>]+>"," ",text)
    text=NUMBER.sub("#",text)
    text=SPACE.sub(" ",text).strip()
    return text if len(text)>=75 and len(re.findall(r"[a-z]{2,}",text))>=12 else ""
def audit(root=ROOT,limit=120):
    base=root/"external_sources"
    src=base/"college_physics"
    index_path=src/"index.json"
    info=json.loads(index_path.read_text(encoding="utf-8"))
    records=info["records"]
    if len(records)!=info["count"] or len(records)==0:
        raise ValueError("College Physics index count mismatch")
    if not 1<=limit<=500:raise ValueError("Invalid manual triage limit")
    seen=set();all_rows=[];kinds=Counter();subjects=Counter();risk_count=Counter()
    tiers=Counter();examples=defaultdict(list);hash_groups=defaultdict(list)
    template_groups=defaultdict(list);integrity_violations=[];missing_files=[]
    for item in records:
        pid=item.get("id","")
        if not re.fullmatch(r"CP-\d{5}",pid) or pid in seen:
            raise ValueError("Duplicate or invalid College Physics ID: "+pid)
        seen.add(pid)
        if item.get("exam_ready") is not False or item.get("answer_verified") is not False:
            raise ValueError("Imported question improperly marked verified: "+pid)
        path=(src/"raw"/(pid+".md"))
        if not path.is_file():
            missing_files.append(pid)
            continue
        raw=path.read_text(encoding="utf-8")
        question=src_question(raw)
        details=preflight.inspect(question,SOURCE)
        flags=set(details["risk_flags"])
        md_start="# "+str(item.get("title",""))+" — "+pid
        if not raw.startswith(md_start+"\n"):
            flags.add("source_heading_mismatch")
        source_sha=str(item.get("source_sha",""))
        if (len(source_sha)!=40 or
            "Git source blob SHA: "+source_sha not in raw or
            "Attribution: OpenStax College" not in raw or
            "CC BY 3.0" not in raw):
            flags.add("attribution_or_revision_mismatch")
        if item.get("source_revision")!=college.REV or item.get("license")!="CC BY 3.0 Unported":
            flags.add("index_source_or_license_mismatch")
        normalized=college.norm(question)
        digest=hashlib.sha256(normalized.encode("utf-8")).hexdigest()
        if item.get("question_sha256")!=digest:
            flags.add("source_question_hash_mismatch")
        formulas=tex.FIND_MATH.findall(question)
        for formula in formulas:
            _,warnings=tex.mathml_to_tex(formula)
            for warning in warnings:
                flags.add("mathml_"+warning.replace(":","_"))
        if "<math" in question.lower() and not formulas:
            flags.add("unclosed_mathml")
        if not normalized:
            flags.add("empty_question")
        # Mechanical tier: neither 'simple' nor 'low risk' means answer-verified.
        critical=("source_heading_mismatch","attribution_or_revision_mismatch",
                  "index_source_or_license_mismatch","source_question_hash_mismatch",
                  "unclosed_mathml","empty_question")
        severe=any(flag in flags for flag in critical) or any(
            f.startswith("mathml_unsupported") or f=="mathml_malformed_mathml" for f in flags)
        if severe:
            tier="source_integrity_or_conversion_review"
        elif flags.intersection(("media_or_figure_reference","cross_reference",
                                 "parameter_template","embedded_answer_section","unbalanced_math_markup")):
            tier="context_or_media_review"
        elif "mathml_requires_conversion" in flags:
            tier="math_format_review"
        else:
            tier="manual_physics_and_solution_review"
        if any(f in flags for f in ("source_heading_mismatch",
           "attribution_or_revision_mismatch","index_source_or_license_mismatch",
           "source_question_hash_mismatch")):
            integrity_violations.append(pid)
        topic=item.get("module","待分类")
        kinds[item.get("question_type","unknown")]+=1
        subjects[topic]+=1
        tiers[tier]+=1
        risk_count.update(flags)
        for flag in flags:
            if len(examples[flag])<10:examples[flag].append(pid)
        hash_groups[digest].append(pid)
        tpl=number_template(details["plain_text"])
        if tpl:template_groups[hashlib.sha256(tpl.encode()).hexdigest()].append(pid)
        all_rows.append({
            "id":pid,"module":topic,"chapter":item.get("title",""),
            "question_type":item.get("question_type","unknown"),
            "source_url":item.get("source_url",""),"source_sha":source_sha,
            "question_sha256":item.get("question_sha256",""),
            "plain_chars":details["plain_text_chars"],
            "mathml_expressions":len(formulas),
            "risk_flags":";".join(sorted(flags)),"format_tier":tier,
            "review_status":"pending_human_review","exam_ready":"no",
        })
    all_files={p.stem for p in (src/"raw").glob("CP-*.md")}
    orphans=sorted(all_files-seen)
    if missing_files or orphans or integrity_violations:
        raise ValueError("Source corpus integrity failed: "+
            json.dumps({"missing":missing_files[:12],"unindexed":orphans[:12],
                       "mismatch":integrity_violations[:12]},ensure_ascii=False))
    if len(all_rows)!=len(records):
        raise ValueError("Incomplete corpus audit")
    dup_hash=[g for g in hash_groups.values() if len(g)>1]
    dup_templates=[g for g in template_groups.values() if len(g)>1]
    folder=base/"catalog"
    folder.mkdir(parents=True,exist_ok=True)
    out=folder/"college_corpus_audit.csv"
    with out.open("w",encoding="utf-8-sig",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=COLUMNS,lineterminator="\n")
        writer.writeheader();writer.writerows(all_rows)
    # Diversify editorial backlog by module; exclude the 60 existing preview ids.
    selected_before=set()
    old=folder/"review_priority.csv"
    if old.is_file():
        with old.open("r",encoding="utf-8-sig",newline="") as f:
            selected_before={x["id"] for x in csv.DictReader(f) if x["source"]==SOURCE}
    pools=defaultdict(deque)
    for row in all_rows:
        if (row["id"] in selected_before or row["module"]=="待分类" or
            row["format_tier"]!="manual_physics_and_solution_review" or
            row["plain_chars"]<70 or row["plain_chars"]>1800):
            continue
        pools[row["module"]].append(row)
    for module in pools:
        pools[module]=deque(sorted(pools[module],key=lambda x:(
            0 if x["question_type"]=="calculation" else 1,
            x["chapter"],x["id"])))
    chosen=[]
    labels=[x for x in MODULE_ORDER if pools[x]]
    while labels and len(chosen)<limit:
        carry=[]
        for label in labels:
            if len(chosen)>=limit:break
            if pools[label]:
                row=pools[label].popleft()
                chosen.append({"review_order":len(chosen)+1,"id":row["id"],
                  "module":row["module"],"chapter":row["chapter"],
                  "question_type":row["question_type"],
                  "source_url":row["source_url"],
                  "raw_path":"external_sources/college_physics/raw/"+row["id"]+".md",
                  "reason":"no_detected_markup_blocker;verify_physics_and_solution;rights_chain",
                  "exam_ready":"no"})
            if pools[label]:carry.append(label)
        labels=carry
    with (folder/"college_next_review.csv").open("w",encoding="utf-8-sig",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=NEXT_COLUMNS,lineterminator="\n")
        writer.writeheader();writer.writerows(chosen)
    report={
        "generated_utc":datetime.now(timezone.utc).isoformat(),
        "upstream_repository":college.REPO,"upstream_revision":college.REV,
        "total_corpus_candidates":len(all_rows),
        "total_raw_file_integrity_mismatches":0,
        "exam_ready_added":0,
        "module_counts":dict(subjects.most_common()),
        "source_question_types":dict(kinds.most_common()),
        "format_tiers":dict(tiers.most_common()),
        "risk_flag_counts":dict(risk_count.most_common()),
        "risk_flag_examples":dict(examples),
        "exact_normalized_duplicate_groups":len(dup_hash),
        "exact_duplicate_examples":dup_hash[:25],
        "same_wording_different_number_template_groups":len(dup_templates),
        "template_duplicate_examples":dup_templates[:25],
        "next_manual_review_count":len(chosen),
        "next_manual_review_by_module":dict(Counter(r["module"] for r in chosen)),
        "limitations":"Static structure and normalized text only. Shared templates are NOT necessarily redundant problems. Physics, solutions, rights and semantics remain unreviewed.",
    }
    (folder/"college_corpus_audit_report.json").write_text(
        json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:report[k] for k in ("total_corpus_candidates",
       "format_tiers","risk_flag_counts","exact_normalized_duplicate_groups",
       "same_wording_different_number_template_groups","next_manual_review_count")},ensure_ascii=False,indent=2))
    return report
if __name__=="__main__":audit()
