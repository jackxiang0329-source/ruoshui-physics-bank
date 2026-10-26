#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Select stable IDs and assemble TeX via \input. Pending questions are excluded by default."""
import argparse
import json
import random
from pathlib import Path
from build import ROOT, TOPICS, load_bank, check, render

def assemble(items, count, seed, topics, min_level, max_level, allow_pending):
    pool=[p for p in items if (not topics or p['topic'] in topics)
          and min_level<=p['level']<=max_level
          and (allow_pending or p['quality_status']=='质检通过')]
    if count>len(pool):
        raise ValueError(f'仅有{len(pool)}道可用题；未通过审核题默认不入正式卷')
    rng=random.Random(seed)
    groups={topic:[p for p in pool if p['topic']==topic] for topic in TOPICS}
    for group in groups.values():
        rng.shuffle(group)
    chosen=[]
    while len(chosen)<count:
        changed=False
        for topic in TOPICS:
            if groups[topic] and len(chosen)<count:
                chosen.append(groups[topic].pop())
                changed=True
        if not changed: break
    return sorted(chosen,key=lambda x:(TOPICS.index(x['topic']),x['id']))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--count',type=int,default=10)
    ap.add_argument('--seed',type=int,default=20261026)
    ap.add_argument('--topic',action='append',choices=TOPICS,default=[])
    ap.add_argument('--min-level',type=int,default=1)
    ap.add_argument('--max-level',type=int,default=5)
    ap.add_argument('--allow-pending',action='store_true')
    ap.add_argument('--output-dir',type=Path,default=ROOT/'generated')
    args=ap.parse_args()
    if args.count<1 or not 1<=args.min_level<=args.max_level<=5:
        ap.error('题目数须为正，难度范围1-5')
    items=load_bank(ROOT)
    errors,_=check(items,ROOT)
    if errors: ap.error('; '.join(errors))
    try:
        chosen=assemble(items,args.count,args.seed,args.topic,
                        args.min_level,args.max_level,args.allow_pending)
    except ValueError as e: ap.error(str(e))
    output=args.output_dir.resolve()
    output.mkdir(parents=True,exist_ok=True)
    for answers,name in ((False,'exam_questions.tex'),(True,'exam_solutions.tex')):
        (output/name).write_text(render(chosen,answers,output,ROOT),encoding='utf-8')
    manifest={
        'status':'draft_only' if args.allow_pending else 'approved',
        'question_ids':[p['id'] for p in chosen],
        'seed':args.seed,
        'estimated_minutes':sum(p['estimated_minutes'] for p in chosen),
        'topic_counts':{topic:sum(p['topic']==topic for p in chosen) for topic in TOPICS}}
    (output/'exam_manifest.json').write_text(
        json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
