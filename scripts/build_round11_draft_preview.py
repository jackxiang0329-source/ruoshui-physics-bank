#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create two standalone XeLaTeX previews from canonical round 11 draft JSON.

These preview files are uncommitted CI products, NOT published bank PDFs.
The approved canonical bank remains untouched until full batch admission.
"""
from pathlib import Path
import json
from build import TEMPLATE, TOPICS, escape

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/"data/rounds/2026-10-28-11-draft.json"
OUT=ROOT/"tex"
if not INPUT.exists():
    print("No round 11 draft: no preview generated")
    raise SystemExit(0)
payload=json.loads(INPUT.read_text(encoding="utf8"))
problems=payload["items"]
if not problems or len(problems)!=len({p["id"] for p in problems}):
    raise RuntimeError("empty or duplicate draft preview")
for with_solutions in (False,True):
    title="第十一批待审核试题预览" if not with_solutions else "第十一批待审核参考解析预览"
    body=[]
    for topic in TOPICS:
        group=sorted((p for p in problems if p["topic"]==topic),key=lambda p:p["id"])
        if not group: continue
        body.extend(["\\chapter{"+topic+"}",""])
        for p in group:
            body.append("\\noindent{\\large\\bfseries 【"+p["id"]+"】 "+escape(p["title"])+"}\\par")
            body.append("\\noindent\\textbf{题目：} "+p["question"]+"\n\\par")
            if with_solutions:
                body.append("\\noindent\\textbf{参考解析（独立专家复核前的草稿）：} "+p["solution"]+"\n\\par")
                body.append("\\noindent\\textbf{结论：}\\(\\displaystyle "+p["answer"]+"\\)\\par")
            body.append("\\medskip\\noindent\\hrulefill\\par\\medskip")
    target=OUT/("round11-draft-solutions.tex" if with_solutions else "round11-draft-questions.tex")
    value=TEMPLATE.replace("__SUBTITLE__",title).replace("__BODY__","\n".join(body))
    value=value.replace("\\title{大学物理原创试题库}","\\title{大学物理高难度综合题 · 第十一批草稿}")
    value=value.replace("\\date{2026年10月}","\\date{2026年10月28日 · "+str(len(problems))+"道预览，未入正式主库}")
    target.write_text(value,encoding="utf8")
    print(target, "problems",len(problems),"bytes",len(value.encode("utf8")))
