#!/usr/bin/env python3
"""One editor-only LaTeX draft from selected College Physics review candidates.

Supports a deliberately small subset of MathML. Unsupported constructs receive
visible markers; NO output is exam-ready, error-free, or academically validated.
"""
import csv
import html
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from review_preflight import question_part

ROOT=Path(__file__).resolve().parent.parent
FIND_MATH=re.compile(r"<math\b[^>]*>.*?</math\s*>",re.I|re.S)
MARKUP=re.compile(r"</?[\w:-]+(?:\s[^<>]*?)?/?>",re.S)
GREEK={"π":r"\pi","μ":r"\mu","ν":r"\nu","τ":r"\tau","ρ":r"\rho","φ":r"\phi","σ":r"\sigma","α":r"\alpha","β":r"\beta","γ":r"\gamma",
       "Δ":r"\Delta","θ":r"\theta","ω":r"\omega","λ":r"\lambda",
       "Σ":r"\Sigma","Ω":r"\Omega","∞":r"\infty"}
OPERATORS={"×":r"\times","·":r"\cdot","−":"-","≤":r"\le","≥":r"\ge",
           "≠":r"\neq","±":r"\pm","→":r"\to","∼":r"\sim","≈":r"\approx"}
SPECIAL={"\\":r"\textbackslash{}","&":r"\&","%":r"\%","$":r"\$",
         "#":r"\#","_":r"\_","{":r"\{","}":r"\}","~":r"\textasciitilde{}",
         "^":r"\textasciicircum{}"}
def escape_tex(text):
    return "".join(SPECIAL.get(c,c) for c in text)
def tag(node):
    return node.tag.rsplit("}",1)[-1]
def mathml_element(node,issues):
    name=tag(node)
    children=[x for x in node if tag(x)!="annotation"]
    if name in ("math","semantics","mrow","mstyle","mpadded","mphantom"):
        return "".join(mathml_element(x,issues) for x in children) or (node.text or "").strip()
    if name=="annotation":return ""
    if name=="mspace":return r"\,"
    if name in ("mn","mi","mo","mtext"):
        val="".join(node.itertext()).strip()
        if not val:return ""
        if name=="mtext" and len(val)>1 and val.isalpha():
            return r"\mathrm{"+escape_tex(val)+"}"
        if name in ("mn","mtext") and len(val)>1 and val[-1] in ("°","º"):
            return val[:-1]+r"^{\circ}"
        # Guard command boundaries. The Unicode micro in 'μm' must not become
        # the nonexistent TeX command '\\mum'; the same holds for '°C'.
        result=[]
        for char in val:
            if char in ("°","º"):
                result.append(r"^{\circ}")
            elif char in GREEK:
                result.append(GREEK[char]+"{}")
            elif char in OPERATORS:
                op=OPERATORS[char]
                result.append(op+("{}" if op.startswith("\\") else ""))
            else:
                result.append(char)
        return "".join(result)
    if name=="mfrac" and len(children)==2:
        return r"\frac{"+mathml_element(children[0],issues)+"}{"+mathml_element(children[1],issues)+"}"
    if name in ("msup","msub","msubsup") and len(children)>1:
        base=mathml_element(children[0],issues)
        if name=="msubsup" and len(children)==3:
            return "{"+base+"}_{"+mathml_element(children[1],issues)+"}^{"+mathml_element(children[2],issues)+"}"
        if len(children)==2:
            return "{"+base+"}"+("_" if name=="msub" else "^")+"{"+mathml_element(children[1],issues)+"}"
    if name=="msqrt":
        return r"\sqrt{"+ "".join(mathml_element(x,issues) for x in children)+"}"
    if name=="mroot" and len(children)==2:
        return r"\sqrt["+mathml_element(children[1],issues)+"]{"+mathml_element(children[0],issues)+"}"
    if name=="mfenced":
        op=node.get("open","(");cl=node.get("close",")")
        return op+"".join(mathml_element(x,issues) for x in children)+cl
    if name=="mover" and len(children)==2:
        accent="".join(children[1].itertext()).strip()
        base=mathml_element(children[0],issues)
        if accent in ("-","−","¯","‾"):
            return r"\bar{"+base+"}"
        if accent in ("→","⃗"):
            return r"\vec{"+base+"}"
    # Do not infer missing MathML superscripts, subscripts or unknown accents.
    issues.add("unsupported_mathml:"+name)
    return r"\text{[CHECK MATH]}"
def mathml_to_tex(raw):
    issues=set()
    try:
        root=ET.fromstring(raw)
        if tag(root)!="math":raise ValueError("not_math")
        converted=mathml_element(root,issues)
    except (ET.ParseError,ValueError):
        issues.add("malformed_mathml")
        converted=r"\text{[CHECK MATH]}"
    return converted,sorted(issues)

def render_question(source):
    errors=set()
    originals=FIND_MATH.findall(source)
    placeholders=[]
    text=source
    for i,math in enumerate(originals):
        tex,issues=mathml_to_tex(math)
        errors.update(issues)
        mark="MATHBLOCKZZ"+str(i)+"ZZ"
        placeholders.append((mark,"$"+tex+"$"))
        text=text.replace(math,mark,1)
    if re.search(r"<math\b",text,re.I):
        errors.add("unclosed_or_nested_mathml")
    text=MARKUP.sub(" ",text)
    text=html.unescape(text)
    text=re.sub(r"(?m)^#.*$","",text)
    text=re.sub(r"\s+"," ",text).strip()
    if not text:errors.add("empty_plain_question")
    text=escape_tex(text)
    for mark,tex in placeholders:
        text=text.replace(mark,tex)
    if re.search(r"\{\{|\}\}",source):errors.add("parameterized_source")
    if re.search(r"(?i)figure\s+\d|<img\b|!\[[^]]*\]\(",source):errors.add("media_dependency")
    return text,sorted(errors),len(originals)

def build(root=ROOT):
    folder=root/"external_sources"/"catalog"
    with (folder/"review_priority.csv").open(encoding="utf-8-sig",newline="") as f:
        rows=[x for x in csv.DictReader(f) if x.get("source")=="OpenStax College Physics (historical mirror)"]
    lines=[r"% GENERATED REVIEW DRAFT ONLY. NOT FOR EXAM ASSEMBLY.",
           r"% Copyright: OpenStax College Physics (2014), CC BY 3.0; retain per-item attribution.",
           r"% Each item requires solution, rights chain, MathML and academic verification.",
           ""]
    stats=Counter();manual=[]
    for item in rows:
        if item.get("exam_ready")!="no":raise ValueError("Draft source was unexpectedly approved")
        relative=item["raw_path"]
        source=(root/relative).resolve()
        if not relative.startswith("external_sources/") or not source.is_relative_to((root/"external_sources").resolve()):
            raise ValueError("Unexpected source path")
        raw=source.read_text(encoding="utf-8")
        question=question_part(raw,item["source"])
        latex,problems,count=render_question(question)
        stats["questions"]+=1
        if count:stats["with_mathml"]+=1
        if problems:
            stats["with_conversion_warnings"]+=1
            manual.append({"id":item["id"],"issues":problems})
        lines += [r"\par\medskip", "% "+item["id"]+" — "+item["original_topic"],
                  "% Original: "+item["source_url"],
                  r"\noindent\textbf{"+escape_tex(item["id"])+" — "+escape_tex(item["original_topic"])+r"}",
                  r"\par "+latex,r"\par\smallskip",
                  r"\textit{Draft only; answer, license-chain and physics correctness unchecked.}",
                  r"\par{\footnotesize OpenStax College Physics (2014), CC BY 3.0. "
                  +r"\href{"+item["source_url"]+r"}{Original chapter}}\par\normalsize",""]
    (folder/"college_review_tex_draft.tex").write_text("\n".join(lines)+"\n",encoding="utf-8")
    # Keep unverified TeX entirely separate from approved bank and exam assembly.
    wrapper = r"""\documentclass[UTF8,11pt]{ctexart}
\usepackage[a4paper,margin=23mm]{geometry}
\usepackage{amsmath,amssymb,hyperref,fancyhdr}
\hypersetup{hidelinks,breaklinks=true}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small Editorial OER review}
\fancyhead[R]{\small NOT EXAM READY}
\fancyfoot[C]{\thepage}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.45em}
\begin{document}
\begin{center}
{\LARGE College Physics: source-editing draft}\par
{\small Human review required: rights, solutions, figures, mathematics}\par
\end{center}
\hrule\vspace{1em}
\input{college_review_tex_draft.tex}
\end{document}
"""
    (folder/"college_review_preview.tex").write_text(wrapper,encoding="utf-8")
    summary={"generated_utc":datetime.now(timezone.utc).isoformat(),
             "question_count":stats["questions"],"preview_source":"external_sources/catalog/college_review_preview.tex","with_mathml":stats["with_mathml"],
             "with_conversion_warnings":stats["with_conversion_warnings"],
             "manual_conversion_check_examples":manual[:30],
             "exam_ready_added":0,
             "note":"Editor-only TeX fragments; does NOT compile or establish correct MathML, licensing, originality or physics."}
    (folder/"college_review_tex_report.json").write_text(
        json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    return summary
if __name__=="__main__":build()
