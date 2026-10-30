#!/usr/bin/env python3
"""Round38 stage-2 historical LaTeX modernization.
Only transform complete, lexically unambiguous Unicode mathematical tokens
OUTSIDE existing LaTeX math spans. Retain exact glyph-level source evidence.
No expert or semantic verification is implied. Review branch only.
"""
from __future__ import annotations
import json
import pathlib
import re
from collections import Counter

ROOT=pathlib.Path(__file__).resolve().parents[1]
REPORT=ROOT/"editorial"/"historical-latex-review"
REPORT.mkdir(exist_ok=True,parents=True)
GREEK={
"α":r"\alpha","β":r"\beta","γ":r"\gamma","δ":r"\delta","ε":r"\varepsilon",
"ζ":r"\zeta","η":r"\eta","θ":r"\theta","ι":r"\iota","κ":r"\kappa",
"λ":r"\lambda","μ":r"\mu","ν":r"\nu","ξ":r"\xi","ο":"o","π":r"\pi",
"ρ":r"\rho","σ":r"\sigma","τ":r"\tau","υ":r"\upsilon","φ":r"\varphi",
"χ":r"\chi","ψ":r"\psi","ω":r"\omega",
"Α":"A","Β":"B","Γ":r"\Gamma","Δ":r"\Delta","Ε":"E","Ζ":"Z","Η":"H",
"Θ":r"\Theta","Ι":"I","Κ":"K","Λ":r"\Lambda","Μ":"M","Ν":"N",
"Ξ":r"\Xi","Ο":"O","Π":r"\Pi","Ρ":"P","Σ":r"\Sigma","Τ":"T",
"Υ":r"\Upsilon","Φ":r"\Phi","Χ":"X","Ψ":r"\Psi","Ω":r"\Omega"
}
OPER={
"→":r"\to ","←":r"\leftarrow ","↔":r"\leftrightarrow ",
"⇒":r"\Rightarrow ","⇔":r"\Leftrightarrow ","≈":r"\approx ",
"≠":r"\ne ","≤":r"\le ","≥":r"\ge ","≪":r"\ll ","≫":r"\gg ",
"∝":r"\propto ","∞":r"\infty ","±":r"\pm ","∓":r"\mp ",
"×":r"\times ","·":r"\cdot ","⋅":r"\cdot ","∈":r"\in ","∉":r"\notin ",
"∪":r"\cup ","∩":r"\cap ","⊥":r"\perp ","∥":r"\parallel ",
"∂":r"\partial ","∇":r"\nabla ","Σ":r"\Sigma ","∑":r"\sum ",
"ℏ":r"\hbar ","ℓ":r"\ell ","−":"-","∣":r"\mid ",
"√":None,"∫":None,"°":r"^\circ ","′":r"^{\prime}","″":r"^{\prime\prime}",
}
SUP={**dict(zip("⁰¹²³⁴⁵⁶⁷⁸⁹","0123456789")),"⁺":"+","⁻":"-","⁽":"(","⁾":")"}
SUB={**dict(zip("₀₁₂₃₄₅₆₇₈₉","0123456789")),"₊":"+","₋":"-"}
CONVERSIONS={**GREEK,**OPER}
MARKED=set(GREEK)|set(OPER)|set(SUP)|set(SUB)
# Existing TeX mathematics must stay untouched.
MATH_SPLIT=re.compile(r"(\\\([\s\S]*?\\\)|\\\[[\s\S]*?\\\])")
# Token contains mathematics and adjacent Latin symbols, but not Chinese prose.
TOKEN=re.compile(r"[A-Za-z0-9+\-−*/=<>|.,:()'\[\]_^" + "".join(re.escape(k) for k in MARKED) + r"]+")
UNSUPPORTED={ch for ch,val in OPER.items() if val is None}
ALLOWED_RE=re.compile(r"^[A-Za-z0-9+\-*/=<>|.,:()'\[\]_^]+$")

def translate_token(token):
    """Translate mathematics exactly; reject undefined radical/integral scope."""
    if any(ch in token for ch in UNSUPPORTED):
        return None,"nonlocal_math_scope"
    out=[];i=0
    while i<len(token):
        c=token[i]
        if c in SUP:
            j=i
            while j<len(token) and token[j] in SUP:j+=1
            out.append("^{"+"".join(SUP[x] for x in token[i:j])+"}")
            i=j;continue
        if c in SUB:
            j=i
            while j<len(token) and token[j] in SUB:j+=1
            out.append("_{"+"".join(SUB[x] for x in token[i:j])+"}")
            i=j;continue
        if c in CONVERSIONS:
            out.append(CONVERSIONS[c]);i+=1;continue
        if c in "\\{}$%&#":
            return None,"unsafe_tex_metacharacters"
        if c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-*/=<>|.,:()'[]_^":
            return None,"unsupported_character"
        out.append(c);i+=1
    translated="".join(out)
    if translated.count("(")!=translated.count(")"):
        # Some math tokens appear in textual parentheses across token boundaries:
        # do not automatically insert a malformed math delimiter.
        return None,"unbalanced_math_token_parentheses"
    if translated.count("[")!=translated.count("]"):
        return None,"unbalanced_math_token_brackets"
    return translated,None

def improve_prose(text,kind,path):
    edits=[];unresolved=[]
    def chunk(match):
        token=match.group(0)
        if not any(ch in MARKED for ch in token):return token
        stripped=token.rstrip(".,:")
        suffix=token[len(stripped):]
        if not stripped:return token
        transformed,why=translate_token(stripped)
        if why:
            unresolved.append({"path":path,"context":token[:130],"reason":why,"kind":kind})
            return token
        edits.append({"before":token,"after":transformed})
        return r"\("+transformed+r"\)"+suffix
    splits=MATH_SPLIT.split(text)
    for i in range(0,len(splits),2):
        # Skip TeX macros outside math: they should be reviewed explicitly.
        prose=splits[i]
        if "\\" in prose:
            sub=re.split(r"(\\[a-zA-Z]+(?:\{[^}]*\})?)",prose)
            splits[i]="".join(TOKEN.sub(chunk,x) if j%2==0 else x for j,x in enumerate(sub))
        else:
            splits[i]=TOKEN.sub(chunk,prose)
    result="".join(splits)
    if result.count(r"\(")!=result.count(r"\)") or result.count(r"\[")!=result.count(r"\]"):
        unresolved.append({"path":path,"reason":"math_delimiter_validation","kind":kind})
        return text,[],unresolved
    return result,edits,unresolved

def main():
    modified=[];unresolved=[];n=0;scanned=0
    for p in sorted((ROOT/"bank").glob("*/*.tex")):
        if p.name not in ("question.tex","solution.tex"):continue
        scanned+=1
        path=p.relative_to(ROOT).as_posix()
        old=p.read_text(encoding="utf-8")
        new,changes,risks=improve_prose(old,"bank-tex",path)
        unresolved.extend(risks)
        if old!=new:
            p.write_text(new,encoding="utf-8")
            n+=len(changes);modified.append({"path":path,"math_tokens_converted":len(changes),
                "examples":changes[:5]})
    # Explicitly also treat the two old editorial source rounds. Do not
    # overwrite their generated PDFs because those remain separate drafts.
    jsonupdated=[]
    for rd in (34,35):
        for p in sorted((ROOT/"editorial"/("round"+str(rd))/"source").glob("*.json")):
            path=p.relative_to(ROOT).as_posix()
            rows=json.loads(p.read_text(encoding="utf-8"))
            edits=0
            for item in rows:
                for k in ("setup",):
                    before=item[k];after,c,issues=improve_prose(before,"editorial-json",path+"#"+item["id"]+"/"+k)
                    item[k]=after;edits+=len(c);unresolved.extend(issues)
                for k in ("q","s"):
                    for idx,before in enumerate(item[k]):
                        after,c,issues=improve_prose(before,"editorial-json",path+"#"+item["id"]+"/"+k+str(idx+1))
                        item[k][idx]=after;edits+=len(c);unresolved.extend(issues)
            if edits:
                p.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
                jsonupdated.append({"path":path,"converted_tokens":edits})
    report={"phase":"Round38 historical Unicode math token conversion",
        "review_only":True,"fully_verified_academic_content":False,
        "scanned_bank_tex":scanned,
        "modified_bank_tex":len(modified),"converted_bank_tokens":n,
        "edited_round34_35_json":len(jsonupdated),
        "converted_editorial_json_tokens":sum(x["converted_tokens"] for x in jsonupdated),
        "unresolved_segments":len(unresolved),
        "modified":modified,"edited_json":jsonupdated,
        "requires_human_math_review":unresolved}
    (REPORT/"unicode_pass2_audit.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items()
                      if k not in ("modified","edited_json","requires_human_math_review")},ensure_ascii=False))
if __name__=="__main__":main()
