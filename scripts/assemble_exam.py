#!/usr/bin/env python3
"""Reproducible draft examination assembly; unreviewed questions are gated off by default.

Usage: python scripts/assemble_exam.py --count 8 --seed 20261026 --allow-pending
"""
import argparse
import json
import random
import sys
from pathlib import Path

from build import TOPICS, check, render

ROOT=Path(__file__).resolve().parent.parent

def assemble(problems,count,seed,topic_filters,min_level,max_level,allow_pending):
    pool=[p for p in problems if
          (not topic_filters or p['topic'] in topic_filters)
          and min_level<=p['level']<=max_level
          and (allow_pending or p['quality_status']=='质检通过')]
    if count>len(pool):
        raise ValueError(f'符合条件的题目只有 {len(pool)} 道，无法组出 {count} 道；默认不使用未审核题。')
    rng=random.Random(seed)
    # Enforce diverse topics through deterministic round-robin, then fill remaining slots.
    by_topic={topic:[p for p in pool if p['topic']==topic] for topic in TOPICS}
    for group in by_topic.values(): rng.shuffle(group)
    chosen=[]
    while len(chosen)<count:
        changed=False
        for topic in TOPICS:
            if by_topic[topic] and len(chosen)<count:
                chosen.append(by_topic[topic].pop()); changed=True
        if not changed:break
    return sorted(chosen,key=lambda p:(TOPICS.index(p['topic']),p['id']))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--count',type=int,default=10)
    ap.add_argument('--seed',type=int,default=20261026)
    ap.add_argument('--topic',action='append',choices=TOPICS,default=[])
    ap.add_argument('--min-level',type=int,default=1)
    ap.add_argument('--max-level',type=int,default=5)
    ap.add_argument('--allow-pending',action='store_true',help='DRAFT ONLY: include questions without quality approval')
    ap.add_argument('--output-dir',type=Path,default=ROOT/'generated')
    args=ap.parse_args()
    if args.count<1 or not (1<=args.min_level<=args.max_level<=5):
        ap.error('题数至少1；难度须为1到5且下限不能大于上限')
    data=json.loads((ROOT/'data/problems.json').read_text(encoding='utf-8'))
    errs,_=check(data)
    if errs: raise ValueError('题库结构校验失败：'+str(errs))
    try: selected=assemble(data,args.count,args.seed,args.topic,args.min_level,args.max_level,args.allow_pending)
    except ValueError as e:ap.error(str(e))
    dest=args.output_dir;dest.mkdir(parents=True,exist_ok=True)
    label='仅供内部测试（未通过独立质检）' if args.allow_pending else '质检通过题目'
    for with_answers,name in [(False,'exam_questions.tex'),(True,'exam_solutions.tex')]:
        (dest/name).write_text('% '+label+'\n'+render(selected,with_answers),encoding='utf-8')
    manifest={'status':label,'seed':args.seed,'total_items':len(selected),
              'estimated_minutes':sum(x['estimated_minutes'] for x in selected),
              'question_ids':[x['id'] for x in selected],
              'topic_counts':{t:sum(x['topic']==t for x in selected) for t in TOPICS}}
    (dest/'exam_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False,indent=2))
    return 0

if __name__=='__main__':sys.exit(main())
