#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate Round 33 review-only physics sources and build two XeLaTeX books.

Run from repository root:
  python3 editorial/round33/build_review.py
  python3 editorial/round33/build_review.py --compile

This tool NEVER imports editorial work into bank/, never marks independent
review complete, and never modifies data/problems.json.
"""
from __future__ import annotations
import argparse
import collections
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BANK = ROOT / "canonical"
OUT = ROOT / "build"
EXPECT = {"M": range(220,229), "E": range(220,229),
          "T": range(218,226), "W": range(226,234),
          "O": range(226,234), "Q": range(226,234)}
TOPIC = {"M":"力学","E":"电磁学","T":"热学","W":"振动与波动",
         "O":"光学","Q":"近代物理"}
HEAD = re.compile(r"\\subsection\*\{([METWOQ]\d{3})\\quad ([^}\n]+)\}")
ANSWER = r"\par\textbf{逐问解析}"
NUM = re.compile(r"(?m)^\(([1-4])\) ")
DANGEROUS = [r"\input",r"\include",r"\write18",r"\openout",
             r"\documentclass",r"\begin{document}",r"\catcode"]

def parts(text, uid, label):
    ms = list(NUM.finditer(text))
    if [m.group(1) for m in ms] != ["1","2","3","4"]:
        raise ValueError(f"{uid}/{label}: four ordered numbered parts expected")
    return [text[m.end():ms[i+1].start() if i+1<len(ms) else len(text)]
            for i,m in enumerate(ms)]

def validate(text, uid, label):
    if text.count("$") % 2 or text.count("{") != text.count("}"):
        raise ValueError(f"{uid}/{label}: math delimiters or braces unbalanced")
    if any(b in text for b in DANGEROUS):
        raise ValueError(f"{uid}/{label}: TeX command excluded")
    ps = parts(text, uid, label)
    if label=="solution" and any(len(re.sub(r"\s+","",p))<100 for p in ps):
        raise ValueError(f"{uid}: solution subpart below 100 non-whitespace chars")
    return ps

def source_check():
    """Check canonical fragments exactly equal to grouped original content."""
    origin = {}
    for p in sorted(ROOT.glob("[METWOQ]*.tex")):
        content=p.read_text(encoding="utf-8")
        headers=list(HEAD.finditer(content))
        for i,h in enumerate(headers):
            uid,title=h.group(1),h.group(2)
            if uid in origin:
                raise ValueError(f"duplicated origin id {uid}")
            body=content[h.end():headers[i+1].start() if i+1<len(headers) else len(content)]
            qsep=body.split(ANSWER)
            if len(qsep)!=2:
                raise ValueError(f"bad solution separator: {uid}")
            origin[uid]=(title,qsep[0].strip(),re.sub(r"\\par\\medskip\s*$","",qsep[1]).strip())
    return origin

def load():
    origin=source_check()
    records=[]
    for prefix,ids in EXPECT.items():
        for n in ids:
            uid=f"{prefix}{n:03}"
            folder=BANK/uid
            meta=json.loads((folder/"meta.json").read_text(encoding="utf-8"))
            q=(folder/"question.tex").read_text(encoding="utf-8").strip()
            s=(folder/"solution.tex").read_text(encoding="utf-8").strip()
            if uid not in origin:
                raise ValueError(f"no grouped original for {uid}")
            title,oq,os=origin[uid]
            if q!=oq or s!=os:
                raise ValueError(f"{uid}: canonical fragment differs from original!")
            if meta.get("id")!=uid or meta.get("title")!=title:
                raise ValueError(f"{uid}: metadata ID/title mismatch")
            if meta.get("topic")!=TOPIC[prefix] or meta.get("tier")!="advanced_composite":
                raise ValueError(f"{uid}: metadata topic/tier mismatch")
            if meta.get("quality_status")!="待独立复核" or meta.get("status")!="review_only":
                raise ValueError(f"{uid}: review quarantine has been bypassed")
            validate(q,uid,"question")
            validate(s,uid,"solution")
            records.append({"id":uid,"title":title,"topic":TOPIC[prefix],"q":q,"s":s})
    if len(records)!=50 or len(origin)!=50:
        raise ValueError(f"Expected 50 canonical and 50 original items, got {len(records)}, {len(origin)}")
    return records

def checks(records):
    files=["QA_48.json","QA_48_second.json","QA_48_third.json",
           "QA_48_fourth.json","QA_8_final.json"]
    tests=[]
    for file in files:
        d=json.loads((ROOT/file).read_text(encoding="utf-8"))
        rows=d.get("tests") or d.get("results")
        if not rows:
            raise ValueError(f"{file}: missing model checks")
        tests.extend(rows)
    expected={(r["id"],p) for r in records for p in (1,2,3,4)}
    actual=[(r["id"],int(r["part"])) for r in tests]
    if len(tests)!=200 or len(set(actual))!=200 or set(actual)!=expected:
        raise ValueError("200 unique, complete ID/part check records not verified")
    failed=[t for t in tests if not t.get("pass")]
    if failed:
        raise ValueError(f"{len(failed)} model tests still failed: {failed[:2]}")
    return len(tests)

FRONT = r"""\documentclass[UTF8,a4paper,11pt]{ctexbook}
\usepackage{amsmath,amssymb,mathtools}
\usepackage{geometry}
\geometry{margin=23mm}
\usepackage[hidelinks]{hyperref}
\allowdisplaybreaks
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.6em}
\begin{document}
\title{大学物理高难综合题（第33批候选）}
\author{Ruoshui Physics Bank}
\date{2026年10月}
\maketitle
\tableofcontents
\chapter*{重要质量说明}
这是一份审核分支候选资料；自动模型检查不等于独立专家逐式复核。
在跨批查重、人工复核及双册编译均完成前，严禁标记为正式主库验收。
"""
def book(records, solved):
    out=[FRONT]
    topic=None
    for r in records:
        if r["topic"]!=topic:
            topic=r["topic"]
            out.append(r"\chapter{"+topic+"}")
        out.extend([r"\section*{"+r["id"]+r"\quad "+r["title"]+"}",
                    r"\textbf{题目}\par",r["q"]])
        if solved:
            out.extend([r"\par\medskip\textbf{逐问解析}\par",r["s"]])
        out.append(r"\par\medskip\hrule\medskip")
    out.append(r"\end{document}")
    return "\n".join(out)+"\n"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--compile",action="store_true")
    args=ap.parse_args()
    records=load()
    count=checks(records)
    OUT.mkdir(exist_ok=True)
    for name,solved in [("questions",False),("solutions",True)]:
        (OUT/(name+".tex")).write_text(book(records,solved),encoding="utf-8")
    result={
      "round":33,"canonical_fragment_count":50,"verified_original_matches":50,
      "machine_model_check_count":count,"source_gate":"PASS",
      "distribution":dict(collections.Counter(r["topic"] for r in records)),
      "xelatex_both_books":"NOT_RUN",
      "independent_expert_approval":"NOT_DONE",
      "formal_import_allowed":False}
    try:
        if args.compile:
            xelatex=shutil.which("xelatex")
            if not xelatex:
                raise RuntimeError("xelatex not installed")
            for name in ("questions","solutions"):
                for _ in range(2):
                    subprocess.run([xelatex,"-interaction=nonstopmode","-halt-on-error",
                                    name+".tex"],cwd=OUT,check=True,
                                   stdout=subprocess.DEVNULL)
                pdf=OUT/(name+".pdf")
                if not pdf.exists() or pdf.stat().st_size < 10000:
                    raise RuntimeError(f"missing/too small compiled PDF: {name}")
            result["xelatex_both_books"]="PASS"
            result["pdf_sizes"]={name:(OUT/(name+".pdf")).stat().st_size
                                 for name in ("questions","solutions")}
    finally:
        (OUT/"verification.json").write_text(json.dumps(result,ensure_ascii=False,
                                            indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False))

if __name__=="__main__":
    main()
