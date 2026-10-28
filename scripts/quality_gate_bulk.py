#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bulk editorial QA, independent from TeX compilation or human approval."""
import argparse
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPICS = ("力学", "电磁学", "热学", "振动与波动", "光学", "近代物理")
PREFIX = {"力学":"M","电磁学":"E","热学":"T","振动与波动":"W","光学":"O","近代物理":"Q"}
FORBIDDEN = (r"\write18", r"\documentclass", r"\input", r"\include", r"\openout", r"\catcode")
BASIC = ("填空题", "选择题", "简单计算题")
REPEAT_CUTOFF = 0.84

def normalized(s):
    return re.sub(r"[\W_]+", "", s, flags=re.UNICODE).lower()

def signature(s, gram=7):
    t=normalized(s)
    return {t[i:i+gram] for i in range(max(0,len(t)-gram+1))}

def near_score(a,b):
    """Jaccard 7-gram; 7 rather than 2 avoids punishing shared physical terminology."""
    if not a or not b:
        return 0.0
    return len(a&b)/len(a|b)

def parse_bank(root=ROOT):
    manifest=json.loads((root/"data/problems.json").read_text(encoding="utf-8"))
    source_ids={p.name for p in (root/"bank").iterdir() if p.is_dir() and (p/"meta.json").is_file()}
    assert {p["id"] for p in manifest}==source_ids, "data mirror and source bank ID mismatch"
    return manifest

def validate(items, old=(), *, batch=False):
    errors=[]
    ids=set()
    content_hash={}
    signatures={}
    known=list(old)+list(items)
    for p in known:
        ident=str(p.get("id",""))
        is_new=p in items
        if not re.fullmatch(r"[METWOQ]\d{3,5}", ident):
            errors.append(f"{ident}: invalid ID")
        if p.get("topic") not in TOPICS or ident[:1]!=PREFIX.get(p.get("topic")):
            errors.append(f"{ident}: ID/topic mismatch")
        if p.get("level") not in (4,5) or p.get("tier")!="advanced_composite":
            errors.append(f"{ident}: lower-level problem excluded")
        if p.get("kind") in BASIC or not str(p.get("kind","")).strip():
            errors.append(f"{ident}: wrong kind")
        if not isinstance(p.get("estimated_minutes"),int) or p["estimated_minutes"]<40:
            errors.append(f"{ident}: insufficient design time")
        if not isinstance(p.get("tags"),list) or len(set(p["tags"]))<3:
            errors.append(f"{ident}: at least 3 distinct cross-topic tags needed")
        q=p.get("question","");s=p.get("solution","")
        if len(q)<200 or len(s)<500 or not str(p.get("answer","")).strip():
            errors.append(f"{ident}: incomplete four-part question, derivation, or answer")
        for j in range(1,5):
            if f"({j})" not in q:
                errors.append(f"{ident}: missing part ({j})")
        if any(f in q or f in s for f in FORBIDDEN):
            errors.append(f"{ident}: unsafe TeX command in fragment")
        if "质检通过"==p.get("quality_status") and is_new:
            errors.append(f"{ident}: expert-reviewed status cannot be self-attested by batch")
        if ident in ids:
            errors.append(f"{ident}: duplicate ID")
        ids.add(ident)
        hashval=hashlib.sha256(normalized(q).encode("utf-8")).hexdigest()
        if hashval in content_hash:
            errors.append(f"{ident}: exact duplicate of {content_hash[hashval]}")
        content_hash[hashval]=ident
        signatures[ident]=signature(q)
    # Across the complete bank, detect near-identical prompts. This detects
    # mechanical numeric substitution, not semantic plagiarization.
    for i,p in enumerate(known):
        a=p["id"]
        for q in known[:i]:
            b=q["id"]
            score=near_score(signatures[a],signatures[b])
            if score>=REPEAT_CUTOFF:
                errors.append(f"{a}/{b}: near duplicate 7-gram similarity={score:.3f}")
    if batch:
        for item in items:
            if item.get("complexity_tier") not in ("L4-A","L4-B","L4-C","L5-A","L5-B","L5-C"):
                errors.append(f'{item.get("id","?")}: missing advanced complexity band')
    if batch and len(items)>200:
        errors.append("batch exceeds 200 distinct problems; split into separate rounds")
    return errors

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--batch",type=Path,default=None,help="optional JSON list of candidates")
    ap.add_argument("--report",type=Path,default=ROOT/"data"/"bulk_quality_report.json")
    args=ap.parse_args()
    try:
        original=parse_bank()
        if args.batch:
            payload=json.loads(args.batch.read_text(encoding="utf-8"))
            if not isinstance(payload,list):
                raise ValueError("batch must be a JSON list")
            problems=payload
            errors=validate(problems,old=original,batch=True)
        else:
            problems=original
            errors=validate(problems)
    except (ValueError,KeyError,AssertionError,OSError) as exc:
        print("BULK CHECK ERROR:",exc,file=sys.stderr)
        return 2
    counts=collections.Counter(x["topic"] for x in problems)
    dist=collections.Counter(x["level"] for x in problems)
    report={"status":"passed" if not errors else "failed","source_count":len(original),
            "checked_count":len(problems),"topic_counts":dict(counts),
            "levels":dict(dist),"errors":errors[:100],
            "warning":"Structural and character-gram de-dup; cannot replace semantic, mathematical or expert review"}
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return int(bool(errors))

if __name__=="__main__":
    sys.exit(main())
