#!/usr/bin/env python3
"""Create a compilable ElegantBook wrapper for a single independent question."""
import argparse
from pathlib import Path
from build import ROOT, check, load_bank, render

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('id')
    ap.add_argument('--solutions',action='store_true')
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    items=load_bank(ROOT)
    errors,_=check(items,ROOT)
    if errors: ap.error('; '.join(errors))
    chosen=[p for p in items if p['id']==args.id]
    if len(chosen)!=1: ap.error('题号不存在')
    dest=(args.output or (ROOT/'generated'/(args.id+'.tex'))).resolve()
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(render(chosen,args.solutions,dest.parent,ROOT),encoding='utf-8')
    print(dest)

if __name__=='__main__': main()
