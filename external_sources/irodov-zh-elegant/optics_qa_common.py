#!/usr/bin/env python3
"""Shared deliberately small integrity harness for Irodov Part V audit files.

Every script below checks each numbered original problem's structural markers
and then independently checks mathematical laws, physical limits and selected
numerical answers. These assertions are not complete manual original-image QA.
"""
from pathlib import Path
import re
from math import isclose

ROOT=Path(__file__).resolve().parent/"chapters"
count=0
failures=[]
def eq(number,title,calculated,reference,rtol=1e-6,atol=1e-11):
    global count
    count+=1
    if not isclose(calculated,reference,rel_tol=rtol,abs_tol=atol):
        failures.append(f"V.{number} {title}: value {calculated:.12g}, reference {reference:.12g}, rel_tol={rtol}")
def truth(number,title,predicate):
    eq(number,title,float(bool(predicate)),1.)
def load(files,macro,begin,end):
    blocks={}
    for file in files:
        src=(ROOT/file).read_text(encoding="utf-8")
        matches=list(re.finditer(r"\\"+re.escape(macro)+r"\{(\d+)\}\{[^}]+\}",src))
        assert matches, f"{file}: no {macro} source blocks"
        for j,m in enumerate(matches):
            n=int(m.group(1))
            assert n not in blocks, f"V.{n}: duplicate number"
            blocks[n]=src[m.start():matches[j+1].start() if j+1<len(matches) else len(src)]
    assert set(blocks)==set(range(begin,end+1)), (
        f"V.{begin}--{end} numbering mismatch {sorted(set(blocks)^set(range(begin,end+1)))}")
    for n,body in blocks.items():
        anchor(n,body,r"\exsolution")
        anchor(n,body,r"\excheck")
        truth(n,"substantive statement/derivation/check content",len(body)>190)
        truth(n,"contains an actual problem-specific solution",len(body.split(r"\exsolution",1)[1].split(r"\excheck",1)[0].strip())>70)
    return blocks
def anchor(n,block,token):
    global count
    count+=1
    if token not in block:
        failures.append(f"V.{n} source invariant absent: {token}")
def finish(tag,nblocks):
    if failures:
        for failure in failures:
            print("FAIL:",failure)
        raise AssertionError(f"{len(failures)} of {count} assertions failed in {tag}")
    print(f"PASS: {count} independent optics/source assertions for {tag}, {nblocks} original numbered blocks.")
