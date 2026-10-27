#!/usr/bin/env python3
"""Fail early on invisible control characters in LaTeX and physics metadata."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
ALLOWED={9,10,13}

def invisible(text):
    return [(i,ord(c)) for i,c in enumerate(text) if ord(c)<32 and ord(c) not in ALLOWED]
def nested_strings(value):
    if isinstance(value,str):
        yield value
    elif isinstance(value,list):
        for x in value:
            yield from nested_strings(x)
    elif isinstance(value,dict):
        for k,v in value.items():
            yield from nested_strings(k)
            yield from nested_strings(v)
def scan(root=ROOT):
    errors=[]
    for p in sorted((root/"bank").glob("*/*.tex")):
        for pos,code in invisible(p.read_text(encoding="utf-8")):
            errors.append(f"{p.relative_to(root)}: U+{code:04X} at offset {pos}")
    for p in sorted((root/"bank").glob("*/meta.json")):
        for value in nested_strings(json.loads(p.read_text(encoding="utf-8"))):
            for pos,code in invisible(value):
                errors.append(f"{p.relative_to(root)}: U+{code:04X} in metadata at offset {pos}")
    return errors
if __name__=="__main__":
    errors=scan()
    if errors:
        for error in errors: print("ERROR:",error)
        raise SystemExit(1)
    print("PASS: no hidden ASCII control characters in bank TeX and metadata.")
