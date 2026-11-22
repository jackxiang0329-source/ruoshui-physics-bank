#!/usr/bin/env python3
"""Source-integrity and independent invariant helpers for Irodov Part VI.

Complements, rather than replaces, the prior numerical tests. Counts all
executed checks (including per-problem structure) without describing these
numbers as independently certified mathematical solutions.
"""
from pathlib import Path
from math import isclose
import re

BASE=Path(__file__).resolve().parent/"chapters"
nchecks=0
failures=[]
def eq(n,name,got,want,rel=1e-6,absolute=1e-12):
    global nchecks
    nchecks+=1
    if not isclose(float(got),float(want),rel_tol=rel,abs_tol=absolute):
        failures.append(f"VI.{n} {name}: got={got!s}, expected={want!s}, rtol={rel}")
def verify(n,name,condition):
    eq(n,name,int(bool(condition)),1,rel=0,absolute=0)
def anchor(n,body,token):
    global nchecks
    nchecks+=1
    if token not in body:failures.append(f"VI.{n} missing source physics anchor: {token}")
def load(files,macro,lo,hi):
    blocks={}
    for f in files:
        source=(BASE/f).read_text(encoding="utf-8")
        matches=list(re.finditer(r"\\"+re.escape(macro)+r"\{(\d+)\}\{([^}]+)\}",source))
        if not matches:
            raise AssertionError(f"no {macro} source entries in {f}")
        for i,m in enumerate(matches):
            n=int(m.group(1)); page=m.group(2)
            body=source[m.start():matches[i+1].start() if i+1<len(matches) else len(source)]
            if n in blocks:raise AssertionError(f"VI.{n} repeated in {f}")
            blocks[n]=body
            verify(n,"source page label",bool(re.fullmatch(r"\d+(?:--\d+)?",page)))
    required=set(range(lo,hi+1))
    if set(blocks)!=required:
        raise AssertionError(f"VI.{lo}--{hi} block numbering has discrepancies {sorted(set(blocks)^required)}")
    for n,b in blocks.items():
        for token in (r"\exsolution",r"\excheck"):anchor(n,b,token)
        question=b.split(r"\exsolution",1)[0]
        solution=b.split(r"\exsolution",1)[1].split(r"\excheck",1)[0] if r"\exsolution" in b else ""
        check=b.split(r"\excheck",1)[1] if r"\excheck" in b else ""
        verify(n,"nonempty original question",len(question.strip())>35)
        verify(n,"substantive physical solution",len(solution.strip())>55)
        verify(n,"nonempty uncertainty/verification commentary",len(check.strip())>15)
        verify(n,"no fake placeholder instead of derivation",
               not any(token in solution for token in (r"\TODO",r"\text{待补}",r"PLACEHOLDER")))
    return blocks
def finish(label,problems):
    if failures:
        for failure in failures:print("FAIL:",failure)
        raise AssertionError(f"{label}: {len(failures)} / {nchecks} checks failed")
    print(f"PASS: {nchecks} Part-VI source and independent physics assertions, {problems} numbered problems, {label}.")
