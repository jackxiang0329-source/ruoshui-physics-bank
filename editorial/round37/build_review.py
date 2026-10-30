#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Round37 deterministic GitHub-Action review builder.

All output is generated in the GitHub Actions cloud runner. Publication remains
strictly in editorial/round37 on a separate draft-PR branch.
No human expert approval is claimed and bank/ remains unchanged.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import importlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "review-release"
CANONICAL = ROOT / "canonical"
SOURCE = ROOT / "source"
CATEGORIES = ["M","E","T","W","O","Q"]
RANGES = {"M":range(256,265),"E":range(256,265),
          "T":range(250,258),"W":range(258,266),
          "O":range(258,266),"Q":range(258,266)}
TOPIC = {"M":"力学","E":"电磁学","T":"热学与统计物理",
         "W":"振动与波动","O":"光学","Q":"近代物理"}
SPECIALS = {"\\":r"\textbackslash{}", "&":r"\&", "%":r"\%",
            "$":r"\$", "#":r"\#", "_":r"\_", "{":r"\{",
            "}":r"\}", "~":r"\textasciitilde{}", "^":r"\textasciicircum{}"}

def tex_escape(s):
    return "".join(SPECIALS.get(c,c) for c in s)

MATH_RE = re.compile(r"(\\\((?:.|\n)*?\\\)|\\\[(?:.|\n)*?\\\])")
def tex_render(s):
    """Render only explicit \( ... \) or \[ ... \] math verbatim.
    Escape all other prose, preventing malformed raw LaTeX in text.
    """
    if s.count(r"\(")!=s.count(r"\)") or s.count(r"\[")!=s.count(r"\]"):
        raise ValueError("Unbalanced LaTeX math delimiters")
    chunks=MATH_RE.split(s)
    for i,part in enumerate(chunks):
        if i%2==0:
            if "\\" in part:
                raise ValueError("Unmarked LaTeX slash outside math mode")
            chunks[i]=tex_escape(part)
        else:
            body=part[2:-2]
            if len(body)>105 and part.startswith(r"\("):
                chunks[i]=r"\["+body+r"\]"
            else:
                chunks[i]=part
    return "".join(chunks)

def load_sources():
    records=[]
    for category in CATEGORIES:
        data=json.loads((SOURCE/(category+".json")).read_text(encoding="utf-8"))
        wanted=[f"{category}{n:03d}" for n in RANGES[category]]
        observed=[x["id"] for x in data]
        if observed!=wanted:
            raise ValueError(f"{category}: wrong ID order {observed}, expected {wanted}")
        for r in data:
            uid=r["id"]
            for key in ("title","setup","q","s","tags"):
                if not r.get(key):raise ValueError(f"{uid}: missing {key}")
            if (len(r["q"])!=4 or len(r["s"])!=4 or len(r["tags"])<3
                    or r.get("tier")!="advanced_composite"
                    or r.get("level") not in (4,5)
                    or r.get("estimated_minutes",0)<40
                    or r.get("quality_status")!="待独立复核"
                    or r.get("status")!="review_only"):
                raise ValueError(f"{uid}: admissions policy violation")
            for part,item in enumerate(r["s"],1):
                if len(re.sub(r"\s+","",item))<85:
                    raise ValueError(f"{uid}/{part}: explanation too short")
            for field in ("setup",):
                if not MATH_RE.search(r[field]):
                    raise ValueError(f"{uid}: missing genuine LaTeX math in {field}")
                tex_render(r[field])
            for j,part in enumerate(r["s"],1):
                if not MATH_RE.search(part):
                    raise ValueError(f"{uid}/{j}: no genuine LaTeX math environment")
                tex_render(part)
            for part in r["q"]:
                tex_render(part)
            if r.get("latex_mode")!="strict":
                raise ValueError(f"{uid}: not strict LaTeX mode")
            r["topic"]=TOPIC[category]
            records.append(r)
    if len(records)!=50 or len({r["id"] for r in records})!=50:
        raise ValueError("Expected exactly 50 unique advanced problems")
    return records

def render_parts(parts):
    return "\n".join(
        r"\par\noindent\textbf{("+str(i)+r")} "+tex_render(item)
        for i,item in enumerate(parts,1))

def emit_source_triples(records):
    for row in records:
        uid=row["id"]
        dirname=CANONICAL/uid
        dirname.mkdir(parents=True,exist_ok=True)
        meta={
            "id":uid,"title":row["title"],"topic":row["topic"],
            "tier":"advanced_composite","level":row["level"],
            "estimated_minutes":row["estimated_minutes"],
            "tags":row["tags"],"round":37,
            "quality_status":"待独立复核",
            "status":"review_only",
            "independent_expert_approval":False,
            "formally_accepted":False,
            "source_json":f"editorial/round37/source/{uid[0]}.json",
            "latex_mode":"strict"}
        (dirname/"meta.json").write_text(
            json.dumps(meta,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        (dirname/"question.tex").write_text(
            r"\textbf{物理条件}\par "+tex_render(row["setup"])
            +"\n"+render_parts(row["q"])+"\n",encoding="utf-8")
        (dirname/"solution.tex").write_text(
            render_parts(row["s"])+"\n",encoding="utf-8")
    assert len(list(CANONICAL.glob("*/meta.json")))==50
    assert len(list(CANONICAL.glob("*/question.tex")))==50
    assert len(list(CANONICAL.glob("*/solution.tex")))==50

HEADER = r"""\documentclass[UTF8,a4paper,11pt,oneside,openany]{ctexbook}
\usepackage{fontspec}
\usepackage{amsmath,mathtools}
\usepackage{unicode-math}
\IfFontExistsTF{TeX Gyre Pagella}{\setmainfont{TeX Gyre Pagella}}{\setmainfont{FreeSerif}}
\IfFontExistsTF{TeX Gyre Pagella Math}{\setmathfont{TeX Gyre Pagella Math}}{\setmathfont{Latin Modern Math}}
\IfFontExistsTF{Noto Serif CJK SC}{\setCJKmainfont{Noto Serif CJK SC}}{}
\usepackage{xcolor,geometry}
\usepackage{fancyhdr}
\definecolor{accent}{HTML}{17365D}
\geometry{margin=22mm,headheight=15pt}
\usepackage[hidelinks]{hyperref}
\hypersetup{colorlinks=true,linkcolor=accent}
\allowdisplaybreaks
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.6em}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\textcolor{accent}{大学物理高难综合题}}
\fancyhead[R]{\small\textcolor{accent}{第37批\,\textbar\,审核稿}}
\fancyfoot[C]{\thepage}
\setlength{\headheight}{15pt}
\sloppy
\begin{document}
\title{\textcolor{accent}{大学物理高难综合题}\\\Large 第37批（审核稿）}
\author{Ruoshui Physics Bank}
\date{2026年10月}
\maketitle
\tableofcontents
\chapter*{质量与准入声明}
本册包含五十道综合题和各四个分问，所有数学表达式使用真正的 \LaTeX{} 数学模式。
自动技术检查不等于独立学术专家质检。资料仅存 GitHub 审核分支，不纳入正式主库。
"""
def render_book(records,with_solutions):
    out=[HEADER]
    group=None
    for row in records:
        if row["topic"]!=group:
            group=row["topic"]
            out.append(r"\chapter{"+tex_escape(group)+"}")
        out.extend([r"\section*{"+row["id"]+r"\quad "+tex_escape(row["title"])+"}",
                    (CANONICAL/row["id"]/"question.tex").read_text(encoding="utf-8")])
        if with_solutions:
            out.extend([r"\par\medskip\noindent\textbf{逐问解析}",
                        (CANONICAL/row["id"]/"solution.tex").read_text(encoding="utf-8")])
        out.append(r"\par\bigskip\hrule\bigskip")
    out.append(r"\end{document}")
    return "\n".join(out)+"\n"

def model_tests(records):
    import qa_common
    qa_common.tests.clear()
    for cat in CATEGORIES:
        module=importlib.import_module("qa_"+cat)
        module.run()
    items=qa_common.tests
    counts=collections.Counter((x["id"],x["part"]) for x in items)
    expected={(r["id"],i) for r in records for i in range(1,5)}
    failed=[x for x in items if not x["pass"]]
    status={
        "round":37,"type":"executed_model_level_checks",
        "expected_pairs":200,"executed":len(items),
        "unique_pairs":len(counts),"passing":len(items)-len(failed),
        "failing":len(failed),
        "pair_coverage_complete":set(counts)==expected and all(v==1 for v in counts.values()),
        "failed_checks":failed,
        "human_expert_approval":"NOT_DONE",
        "note":"Each numbered subpart has one executed numeric/formula regression. Some checks are narrow; detailed independent academic and historical duplicate review remains pending.",
        "checks":items}
    OUTPUT.mkdir(parents=True,exist_ok=True)
    (OUTPUT/"QA_200.json").write_text(
        json.dumps(status,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if failed:
        print(json.dumps({"failed_checks":failed},ensure_ascii=False),file=sys.stderr)
    if len(items)!=200 or failed or not status["pair_coverage_complete"]:
        raise RuntimeError(f"Physics check gate failed: {len(items)} tests; {len(failed)} failures; full coverage={status['pair_coverage_complete']}")
    return status

def compiled_pdf(name):
    exe=shutil.which("xelatex")
    if not exe:raise RuntimeError("xelatex unavailable")
    for _ in range(2):
        res=subprocess.run([exe,"-interaction=nonstopmode",
                            "-halt-on-error",name+".tex"],
                           cwd=OUTPUT,capture_output=True,text=True)
        if res.returncode!=0:
            print(res.stdout[-6000:],file=sys.stderr)
            print(res.stderr[-1000:],file=sys.stderr)
            raise RuntimeError(f"XeLaTeX failed: {name}")
    compile_log=(OUTPUT/(name+".log")).read_text(encoding="utf-8",errors="replace")
    lost=[line for line in compile_log.splitlines() if line.startswith("Missing character:")]
    if lost:
        print("UNRENDERED MATH/UNICODE CHARACTERS:",lost[:20],file=sys.stderr)
        raise RuntimeError(f"{name}: {len(lost)} missing Unicode glyphs; refuse release")
    result=OUTPUT/(name+".pdf")
    if not result.exists() or result.stat().st_size<10000:
        raise RuntimeError(f"PDF missing or suspicious: {result}")
    if shutil.which("pdfinfo"):
        info=subprocess.check_output(["pdfinfo",str(result)],text=True)
        pages=next((int(line.split(":",1)[1]) for line in info.splitlines()
                    if line.startswith("Pages:")),0)
    else:pages=None
    return {"bytes":result.stat().st_size,"pages":pages}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--compile",action="store_true")
    args=parser.parse_args()
    sys.path.insert(0,str(ROOT))
    rows=load_sources()
    emit_source_triples(rows)
    checks=model_tests(rows)
    OUTPUT.mkdir(parents=True,exist_ok=True)
    for name,solved in (("questions",False),("solutions",True)):
        (OUTPUT/(name+".tex")).write_text(
            render_book(rows,solved),encoding="utf-8")
    report={"round":37,"source_count":len(rows),"subparts":200,
            "source_triples":150,"machine_checks_passed":checks["passing"],
            "distribution":dict(collections.Counter(r["topic"] for r in rows)),
            "independent_expert_review":"NOT_DONE",
            "historical_full_bank_duplicate_review":"INCOMPLETE",
            "formal_main_bank_import":False,
            "review_branch_only":True,"both_pdf_compilation":"NOT_RUN",
            "source_sha256":{
                x.name:hashlib.sha256(x.read_bytes()).hexdigest()
                for x in sorted(SOURCE.glob("*.json"))}}
    (OUTPUT/"verification.json").write_text(
        json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if args.compile:
        report["pdfs"]={
            "questions":compiled_pdf("questions"),
            "solutions":compiled_pdf("solutions")}
        report["both_pdf_compilation"]="PASS"
        (OUTPUT/"verification.json").write_text(
            json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (OUTPUT/"README.md").write_text(
        "# 第37批大学物理综合题审核产物\n\n"
        "所有题源、解析、质检报告和PDF均由 GitHub Actions 提交到此审核分支。\n"
        "两个 PDF 和 TeX 由源数据自动产生；50道题各有四问及四个解析，"
        "每题有独立 meta.json、question.tex、solution.tex。\n"
        "注意：已执行自动模型检查并不意味着完成独立专家质检、历史去重或正式入库。\n",
        encoding="utf-8")
    bundle=OUTPUT/"round37-complete-review-package.zip"
    includes=(
        list(SOURCE.glob("*.json"))+list(ROOT.glob("qa_*.py"))+
        [ROOT/"build_review.py"]+
        [p for p in CANONICAL.rglob("*") if p.is_file()]+
        [p for p in OUTPUT.glob("*") if p.is_file() and p!=bundle])
    with zipfile.ZipFile(bundle,"w",zipfile.ZIP_DEFLATED) as z:
        for path in includes:
            z.write(path,arcname=str(path.relative_to(ROOT)))
    print(json.dumps(report,ensure_ascii=False))

if __name__=="__main__":
    main()
