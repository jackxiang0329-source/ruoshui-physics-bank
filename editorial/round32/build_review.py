#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build round-32 review books directly from the quarantined TeX source.

This is an editorial build, not import to the canonical bank, and does not
constitute independent expert approval.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE / "build"
SECTION = re.compile(r"\\subsection\*\{([METWOQ]\d{3})\\quad ([^}\n]+)\}")
SOLUTION_MARK = re.compile(r"\\par\\textbf\{(?:解答|逐问解析)\}")
SUBPART = re.compile(r"(?m)^\(([1-4])\)\s+")
EXPECTED = {
    "M": list(range(211, 220)), "E": list(range(211, 220)),
    "T": list(range(210, 218)), "W": list(range(218, 226)),
    "O": list(range(218, 226)), "Q": list(range(218, 226)),
}
TOPIC = {"M":"力学","E":"电磁学","T":"热学","W":"振动与波动","O":"光学","Q":"近代物理"}
FILES = {
    "E": "E_9_full_solutions.tex",
    "T": "T_8_full_solutions.tex",
    "W": "W_8_full_solutions.tex",
    "O": "O_8_full_solutions.tex",
    "Q": "Q_8_full_solutions.tex",
}
FORBIDDEN = ("\\write18", "\\openout", "\\documentclass", "\\begin{document}",
             "\\catcode", "\\include", "\\input")


def subparts(text: str) -> list[str]:
    marks = list(SUBPART.finditer(text))
    if [m.group(1) for m in marks] != list("1234"):
        raise ValueError("Subparts must be exactly (1)-(4) in order")
    return [text[marks[i].end(): marks[i + 1].start() if i < 3 else len(text)].strip()
            for i in range(4)]


def check_tex(fragment: str, uid: str, kind: str) -> None:
    if any(bad in fragment for bad in FORBIDDEN):
        raise ValueError(f"{uid}/{kind}: forbidden TeX command")
    if fragment.count("$") % 2:
        raise ValueError(f"{uid}/{kind}: unpaired math dollars")
    if fragment.count("{") != fragment.count("}"):
        raise ValueError(f"{uid}/{kind}: unbalanced braces")
    parts = subparts(fragment)
    if kind == "solution":
        for n, part in enumerate(parts, 1):
            if len(re.sub(r"\s+", "", part)) < 100:
                raise ValueError(f"{uid}: solution part {n} under 100 characters")


def read_cases() -> list[dict]:
    cases = []
    for p, seq in EXPECTED.items():
        if p == "M":
            for num in seq:
                uid = f"{p}{num:03d}"
                root = HERE / "M" / uid
                meta = json.loads((root / "meta.json").read_text(encoding="utf8"))
                if meta["id"] != uid or meta.get("tier") != "advanced_composite":
                    raise ValueError(f"{uid}: metadata mismatch")
                q = (root / "question.tex").read_text(encoding="utf8")
                s = (root / "solution.tex").read_text(encoding="utf8")
                check_tex(q, uid, "question")
                check_tex(s, uid, "solution")
                cases.append({"id":uid, "topic":TOPIC[p], "title":meta["title"],"q":q,"s":s})
        else:
            text = (HERE / FILES[p]).read_text(encoding="utf8")
            hits = list(SECTION.finditer(text))
            for index, match in enumerate(hits):
                uid, title = match.group(1), match.group(2)
                body = text[match.end():hits[index + 1].start() if index + 1 < len(hits) else len(text)]
                marker = SOLUTION_MARK.search(body)
                if not marker:
                    raise ValueError(f"{uid}: missing solution marker")
                q, s = body[:marker.start()].strip(), body[marker.end():].strip()
                check_tex(q, uid, "question")
                check_tex(s, uid, "solution")
                cases.append({"id":uid,"topic":TOPIC[p],"title":title,"q":q,"s":s})
            actual = [z["id"] for z in cases if z["id"].startswith(p)]
            expected = [f"{p}{n:03d}" for n in seq]
            if actual != expected:
                raise ValueError(f"{p}: candidate IDs mismatch: {actual}")
    ids = [c["id"] for c in cases]
    if len(ids) != 50 or len(set(ids)) != 50:
        raise ValueError(f"expected 50 unique questions, got {len(ids)}")
    return cases


PREFIX = r"""\documentclass[UTF8,a4paper,11pt]{ctexbook}
\usepackage{amsmath,amssymb,mathtools,geometry}
\usepackage[colorlinks=false,hidelinks]{hyperref}
\geometry{margin=23mm}
\allowdisplaybreaks
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.5em}
\begin{document}
\title{大学物理高难综合题（第32批候选稿）}
\author{三千弱水 · Ruoshui Physics Bank}
\date{2026年10月}
\maketitle
\tableofcontents
"""

def book(cases: list[dict], solutions: bool) -> str:
    out = [PREFIX, "\\chapter*{质量说明}\n本册为审核候选稿。自动检查不等于独立专家质检，不计入正式主库。\n"]
    last = None
    for case in cases:
        if case["topic"] != last:
            last = case["topic"]
            out.append(r"\chapter{" + last + "}")
        out.append(r"\section*{" + case["id"] + r"\quad " + case["title"] + "}")
        out.append(r"\textbf{题目}\par " + case["q"] + "\n")
        if solutions:
            out.append(r"\par\medskip\textbf{逐问解析}\par " + case["s"] + "\n")
        out.append(r"\par\bigskip\hrule\bigskip")
    out.append(r"\end{document}")
    return "\n".join(out) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--compile", action="store_true", help="also compile both XeLaTeX PDFs")
    args = ap.parse_args()
    cases = read_cases()
    BUILD.mkdir(parents=True, exist_ok=True)
    for name, flag in (("questions", False), ("solutions", True)):
        (BUILD / (name + ".tex")).write_text(book(cases, flag), encoding="utf8")
    report = {"candidate_count":len(cases), "subpart_pairs":len(cases)*4,
              "topic_counts":dict(collections.Counter(c["topic"] for c in cases)),
              "structure_gate":"PASS", "expert_review":"PENDING",
              "canonical_bank_import":False}
    if args.compile:
        exe = shutil.which("xelatex")
        if not exe:
            raise RuntimeError("xelatex not installed")
        for name in ("questions", "solutions"):
            for _ in range(2):
                subprocess.run([exe, "-interaction=nonstopmode", "-halt-on-error",
                                name + ".tex"], cwd=BUILD, check=True,
                               stdout=subprocess.DEVNULL)
            pdf = BUILD / (name + ".pdf")
            if not pdf.exists() or pdf.stat().st_size < 10000:
                raise RuntimeError(f"PDF output missing or suspicious: {name}")
        report["both_xelatex_pdfs"] = "PASS"
        report["pdf_bytes"] = {name:(BUILD/(name+".pdf")).stat().st_size
                               for name in ("questions","solutions")}
    else:
        report["both_xelatex_pdfs"] = "NOT RUN"
    (BUILD/"build_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
