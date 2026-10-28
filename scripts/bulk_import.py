#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Stage one curated JSON batch (up to 200) into canonical bank/ID/* sources.

Default is dry run. Explicit --apply writes only after full validation.
No generation of questions or answers; the source JSON must contain both.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from quality_gate_bulk import ROOT, parse_bank, validate

FIELDS=("id","topic","title","kind","level","estimated_minutes","tags","answer",
        "quality_status","tier","format","revision","challenge_profile")
def write_utf8(path,text):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text,encoding="utf-8")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--batch",type=Path,required=True,help="JSON list with full question and solution TeX strings")
    parser.add_argument("--apply",action="store_true",help="write after complete dry-run validation")
    args=parser.parse_args()
    candidates=json.loads(args.batch.read_text(encoding="utf-8"))
    if not isinstance(candidates,list):
        raise SystemExit("batch must be an array of problem records")
    old=parse_bank()
    errors=validate(candidates,old=old,batch=True)
    if errors:
        raise SystemExit("refused batch:\n"+"\n".join(errors[:50]))
    if not args.apply:
        print(json.dumps({"dry_run":True,"accepted_for_staging":len(candidates),
            "count_after_import":len(old)+len(candidates),
            "status":"not written; run with --apply after reviewing"},ensure_ascii=False,indent=2))
        return 0
    # Prepare all files in a private temporary directory; never allow partial
    # writes of an item if the batch source is malformed.
    with tempfile.TemporaryDirectory(prefix="physics-bulk-") as tmpdir:
        staged=Path(tmpdir)
        for item in candidates:
            p=staged/"bank"/item["id"]
            meta={k:item[k] for k in FIELDS if k in item}
            meta["format"]="latex-fragment-v1"
            meta["quality_status"]="待独立复核"
            write_utf8(p/"meta.json",json.dumps(meta,ensure_ascii=False,indent=2)+"\n")
            write_utf8(p/"question.tex",item["question"].rstrip()+"\n")
            write_utf8(p/"solution.tex",item["solution"].rstrip()+"\n")
        full_mirror=old+candidates
        full_mirror.sort(key=lambda x:(("力学","电磁学","热学","振动与波动","光学","近代物理").index(x["topic"]),x["id"]))
        write_utf8(staged/"data"/"problems.json",json.dumps(full_mirror,ensure_ascii=False,indent=2)+"\n")
        written=[]
        backup=ROOT/"data"/"problems.json"
        previous=backup.read_bytes()
        try:
            for item in candidates:
                ident=item["id"]
                destination=ROOT/"bank"/ident
                if destination.exists():
                    raise RuntimeError(f"{ident}: destination unexpectedly exists")
                os.replace(staged/"bank"/ident,destination)
                written.append(destination)
            os.replace(staged/"data"/"problems.json",backup)
            build=subprocess.run([sys.executable,str(ROOT/"scripts"/"build.py")],cwd=ROOT,check=True,
                capture_output=True,text=True)
            subprocess.run([sys.executable,str(ROOT/"scripts"/"check_difficulty_gate.py")],cwd=ROOT,check=True)
            subprocess.run([sys.executable,str(ROOT/"scripts"/"build.py"),"--check"],cwd=ROOT,check=True)
        except Exception:
            backup.write_bytes(previous)
            for destination in written:
                shutil.rmtree(destination,ignore_errors=True)
            # Roll the generated tex/ and index/ back to the old canonical bank.
            subprocess.run([sys.executable,str(ROOT/"scripts"/"build.py")],cwd=ROOT,check=False)
            raise
        print(json.dumps({"imported":len(candidates),"count_after_import":len(full_mirror),
                "build_output":build.stdout[-600:],"status":"pending independent expert review"},
                ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    sys.exit(main())
