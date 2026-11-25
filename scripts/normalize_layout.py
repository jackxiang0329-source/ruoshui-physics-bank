#!/usr/bin/env python3
"""One-time normalized layout migration; keep binary and TeX files byte-identical."""
import os, re, subprocess
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlparse
ROOT=Path(__file__).resolve().parents[1]
BOOKS={"external_sources/irodov-zh-elegant":"textbooks/irodov","external_sources/three-college-physics-elegant":"textbooks/three_college","external_sources/zhao-wang-physics-5e-elegant":"textbooks/zhao_wang"}
BANK={"M":"mechanics","E":"electromagnetism","T":"thermodynamics","W":"waves","O":"optics","Q":"modern_physics"}
RENAMES={"quality-check.md":"quality_check.md","qa-eight-rounds-summary.md":"qa_eight_rounds_summary.md","review-round20.md":"review_round20.md","chapters/COMPACTION-MAP.md":"chapters/compaction_map.md"}
def git(*args):
    return subprocess.check_output(["git",*args],cwd=ROOT)
def tracked():
    return git("ls-files","-z").decode().strip("\0").split("\0")
def map_path(path):
    for old,new in BOOKS.items():
        if path==old or path.startswith(old+"/"):
            suffix=path[len(old):].lstrip("/")
            return new+("/"+RENAMES.get(suffix,suffix) if suffix else "")
    for prefix,name in BANK.items():
        if path=="bank/"+prefix+".json":
            return "bank/"+name+".json"
    return path
original=tracked()
moves={p:map_path(p) for p in original if map_path(p)!=p}
assert len(moves)>30
for old,new in sorted(moves.items()):
    dest=ROOT/new
    dest.parent.mkdir(parents=True,exist_ok=True)
    git("mv","--",old,new)
# Verify bytes of every moved file before editing documentation or build entrypoints.
for old,new in moves.items():
    assert git("rev-parse","HEAD:"+old).strip()==git("hash-object",new).strip(), old
print("byte-identical tracked moves:",len(moves))
# Rewrite relative links by resolving them against their original location first.
pattern=re.compile(r"(?<!!)\[([^\]\n]+)\]\(([^)\n]+)\)")
reverse={v:k for k,v in moves.items()}
for rel in tracked():
    if not rel.endswith(".md") or rel in ("README.md","textbooks/README.md","scripts/README.md","docs/policies/repository_naming.md"):
        continue
    path=ROOT/rel
    oldrel='README.md' if rel=='docs/history/compaction_history.md' else reverse.get(rel,rel)
    original_parent=ROOT/Path(oldrel).parent
    text=path.read_text(encoding="utf-8")
    def repl(m):
        target=m.group(2)
        if not target or urlparse(target).scheme or target.startswith(("#","//")):
            return m.group(0)
        raw,sep,frag=target.partition("#")
        if not raw:
            return m.group(0)
        resolved=(original_parent/unquote(raw.strip("<>"))).resolve()
        if not resolved.is_relative_to(ROOT):
            return m.group(0)
        key=resolved.relative_to(ROOT).as_posix()
        mapped=map_path(key)
        if mapped==key and oldrel==rel:
            return m.group(0)
        new=os.path.relpath(ROOT/mapped,path.parent).replace(os.sep,"/")
        return "["+m.group(1)+"]("+new+(sep+frag if sep else "")+")"
    out=pattern.sub(repl,text)
    # Update literal paths outside archive-history documents; the old history remains a record.
    if rel!="docs/history/compaction_history.md":
        for old,new in BOOKS.items(): out=out.replace(old,new)
        for prefix,name in BANK.items(): out=out.replace("bank/"+prefix+".json","bank/"+name+".json")
        for a,b in RENAMES.items():
            if rel.startswith("textbooks/"): out=out.replace(a,b)
    if out!=text:
        path.write_text(out,encoding="utf-8")
# The two shared-class build scripts refer to the former sibling directory name.
for rel in ("textbooks/three_college/build.sh","textbooks/zhao_wang/build.sh"):
    p=ROOT/rel
    text=p.read_text(encoding="utf-8")
    p.write_text(text.replace("../irodov-zh-elegant","../irodov"),encoding="utf-8")
# Keep the original archived material and live IDs unchanged.
assert all((ROOT/"bank"/(n+".json")).is_file() for n in BANK.values())
git("add","-u")
print("normalized directories and relative links")
