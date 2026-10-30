#!/usr/bin/env python3
"""Conservative and idempotent TeX delimiter migration on review branch.
Change only unambiguous dollar math delimiters to LaTeX math environments.
Do not invent, semantically alter, or guess physics and mathematics.
"""
from __future__ import annotations
import json
import pathlib
import re

ROOT=pathlib.Path(__file__).resolve().parents[1]
REPORT=ROOT/"editorial/historical-latex-review"
REPORT.mkdir(parents=True,exist_ok=True)
GREEK="αβγδεζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"
OPERATORS="∑∫∂∇√∞≈≠≤≥±×÷→↔⇒⇔∝∈∉∪∩⊂⊆⊥∥⋅·"
SUPERSUB="⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾₀₁₂₃₄₅₆₇₈₉₊₋₌"
SUSPICIOUS=set(GREEK+OPERATORS+SUPERSUB)

def tex_files():
    for p in sorted((ROOT/"bank").glob("*/*.tex")):
        if p.name in ("question.tex","solution.tex"):yield p
    for p in sorted((ROOT/"editorial").glob("round*/canonical/*/*.tex")):
        if p.name in ("question.tex","solution.tex"):yield p

def swap_delimiters(src):
    out=[];count=0;i=0;opened=None;start=None;problems=[]
    while i<len(src):
        if src[i]=="\\" and i+1<len(src):
            out.append(src[i:i+2]);i+=2;continue
        if src[i]=="$":
            double=i+1<len(src) and src[i+1]=="$"
            token="$$" if double else "$"
            if opened is None:
                opened=token;start=i
                out.append(r"\[" if double else r"\(")
            elif opened==token:
                if not src[start+len(token):i].strip():problems.append("empty_math")
                opened=None;start=None;count+=1
                out.append(r"\]" if double else r"\)")
            else:
                problems.append("mismatched_math_delimiter")
                out.append(token)
            i+=len(token);continue
        out.append(src[i]);i+=1
    if opened is not None:problems.append("unclosed_math_delimiter")
    if problems:return src,0,sorted(set(problems))
    dest="".join(out)
    def actual_delimiters(text, token):
        return len(re.findall(r"(?<!\\)"+re.escape(token),text))
    if actual_delimiters(dest,r"\(")!=actual_delimiters(dest,r"\)") or actual_delimiters(dest,r"\[")!=actual_delimiters(dest,r"\]"):
        return src,0,["unbalanced_math_environment"]
    return dest,count,[]

def outside_math(s):
    return re.sub(r"\\\([\s\S]*?\\\)|\\\[[\s\S]*?\\\]|\$\$[\s\S]*?\$\$|\$[^$]*\$"," ",s)
def unmarked(s):
    return sorted({c for c in outside_math(s) if c in SUSPICIOUS})

def main():
    files=list(tex_files());modified=[];ambiguous=[];outside=[];nmath=0
    for p in files:
        src=p.read_text(encoding="utf-8")
        dest,num,problems=swap_delimiters(src)
        rel=p.relative_to(ROOT).as_posix()
        if problems:ambiguous.append({"path":rel,"problems":problems})
        elif dest!=src:
            p.write_text(dest,encoding="utf-8")
            modified.append({"path":rel,"math_environments":num})
            nmath+=num
        sus=unmarked(dest)
        if sus:outside.append({"path":rel,"glyphs":sus,"status":"needs_contextual_math_review"})
    historical_json=[]
    for p in sorted((ROOT/"editorial").glob("round*/source/*.json")):
        if p.parent.parent.name=="round37":continue
        data=json.loads(p.read_text(encoding="utf-8"))
        marked=0;bare=0;ids=[]
        for item in data:
            for v in [item.get("setup",""),*item.get("s",[])]:
                if r"\(" in v or r"\[" in v:marked+=1
                elif unmarked(v):bare+=1;ids.append(item.get("id"))
        historical_json.append({"path":p.relative_to(ROOT).as_posix(),"segments_with_tex_math":marked,"segments_with_bare_unicode_math":bare,"example_ids":sorted(set(ids))[:12]})
    result={"scope":"bank canonical and historical editorial canonical tex",
        "scanned_tex_files":len(files),"modified_tex_files":len(modified),
        "converted_math_environments":nmath,"ambiguous_tex_files":len(ambiguous),
        "unmarked_unicode_tex_files":len(outside),
        "source_json":historical_json,
        "full_historical_conversion":"INCOMPLETE",
        "academic_semantics_review":"NOT_DONE",
        "publication":"REVIEW_BRANCH_ONLY",
        "modified":modified,"ambiguous":ambiguous,"needs_review":outside}
    (REPORT/"audit.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lines=["# 历史大学物理公式迁移报告",
        "仅自动转换无歧义的旧数学定界符；保留所有公式原文，不自动猜测物理数学表达。",
        "检查题源：{}份。修改：{}份。数学环境：{}处。".format(len(files),len(modified),nmath),
        "歧义TeX：{}份；裸数学Unicode：{}份。".format(len(ambiguous),len(outside)),
        "所有历史编辑JSON题源已纳入统计；无法确定含义的公式保持原样，需人工复核。",
        "完整路径、题号和审计明细参见audit.json。",
        "本结果仅为审核分支的排版迁移，不是独立专家学术审核或正式主库导入。"]
    (REPORT/"README.md").write_text("\n\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k not in ("modified","ambiguous","needs_review","source_json")},ensure_ascii=False))
if __name__=="__main__":main()
