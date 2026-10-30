#!/usr/bin/env python3
"""Post-migration typography audit across historical university physics corpus."""
import json,re,pathlib,collections
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/"editorial/historical-latex-review"
OUT.mkdir(parents=True,exist_ok=True)
GLYPHS=set("αβγδεζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ∑∫∂∇√∞≈≠≤≥±×÷→↔⇒⇔∝∈∉∪∩⊂⊆⊥∥⋅·⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾₀₁₂₃₄₅₆₇₈₉₊₋₌")
MATH=re.compile(r"\\\([\s\S]*?\\\)|\\\[[\s\S]*?\\\]")
def suspicious(s):
    return sorted({x for x in MATH.sub(" ",s) if x in GLYPHS})
def main():
    paths=list((ROOT/"bank").glob("*/*.tex"))
    paths+=list((ROOT/"editorial").glob("round*/canonical/*/*.tex"))
    paths=sorted(p for p in paths if p.name in ("question.tex","solution.tex"))
    counts=collections.Counter();flags=[];no_math=[];old_dollar=[]
    for p in paths:
        rel=p.relative_to(ROOT).as_posix()
        text=p.read_text(encoding="utf-8")
        group="bank" if rel.startswith("bank/") else rel.split("/")[1]
        counts[group]+=1
        c=suspicious(text)
        if c:flags.append({"path":rel,"unicode_outside_math":c})
        if r"\(" not in text and r"\[" not in text:no_math.append(rel)
        if re.search(r"(?<!\\)\$",text):old_dollar.append(rel)
    histories=[];bare=0
    for rd in (34,35):
        for p in sorted((ROOT/"editorial"/("round"+str(rd))/"source").glob("*.json")):
            items=json.loads(p.read_text(encoding="utf-8"))
            issues=[]
            for item in items:
                for key,text in [("setup",item["setup"]),*[(f"q{i+1}",s) for i,s in enumerate(item["q"])],
                                 *[(f"s{i+1}",s) for i,s in enumerate(item["s"])]]:
                    c=suspicious(text)
                    if c:issues.append({"id":item["id"],"part":key,"glyphs":c})
            histories.append({"path":p.relative_to(ROOT).as_posix(),"issues":issues[:40],"issue_count":len(issues)})
            bare+=len(issues)
    ledger=json.loads((OUT/"migration_ledger.json").read_text(encoding="utf-8"))
    stage2=json.loads((OUT/"unicode_pass2_audit.json").read_text(encoding="utf-8"))
    report={"status":"REVIEW_NOT_SCIENTIFIC_CERTIFICATION",
        "canonical_source_files_scanned":len(paths),"by_group":dict(counts),
        "remaining_canonical_with_unicode_math_outside_math":len(flags),
        "remaining_canonical_without_tex_math":len(no_math),
        "remaining_legacy_dollar_files":len(old_dollar),
        "round34_35_json_bare_math_segments":bare,
        "stage1_converted_math_environments":ledger.get("total_converted_math_environments"),
        "stage2_converted_bank_unicode_tokens":stage2.get("converted_bank_tokens"),
        "stage2_converted_round34_35_json_tokens":stage2.get("converted_editorial_json_tokens"),
        "flagged_canonical":flags,"canonical_without_math":no_math,
        "remaining_dollar_files":old_dollar,"historical_json":histories,
        "full_history_conversion":False,"math_semantic_review":"NOT_DONE"}
    (OUT/"post_migration_audit_v3.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    md="# 大学物理历史公式第三轮审计（审核稿）\n\n"
    md+="扫描文件："+str(len(paths))+"；仍含数学环境外Unicode："+str(len(flags))+"；尚无LaTeX数学环境："+str(len(no_math))+"。\n\n"
    md+="第34、35批结构化源文件剩余可疑数学片段："+str(bare)+"。详细文件名和题号见post_migration_audit_v3.json。\n\n"
    md+="所有历史改造仍待逐式数学审核；不可凭自动语法转换宣布正式学术验收。\n"
    (OUT/"post_migration_audit_v3.md").write_text(md,encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k not in ("flagged_canonical","canonical_without_math","remaining_dollar_files","historical_json")},ensure_ascii=False))
if __name__=="__main__":main()
