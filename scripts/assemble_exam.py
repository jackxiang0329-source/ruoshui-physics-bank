#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deterministic constrained exam assembly using independent TeX input fragments.

Examples:
  python scripts/assemble_exam.py --count 10 --seed 20261026 --allow-pending
  python scripts/assemble_exam.py --count 12 --topic-quota 力学=3 \
    --topic-quota 电磁学=3 --max-minutes 180 --total-points 100 --allow-pending
"""
import argparse
import collections
import json
import random
from pathlib import Path

from build import ROOT, TOPICS, check, load_bank, render
from check_review import validate as validate_reviews


def assemble(items, count, seed, topics, min_level, max_level, allow_pending,
             kinds=None, quotas=None, max_minutes=None):
    """Select reproducibly. Any named quota is exact, not a soft preference.

    A duration bound uses up to 128 seeded candidate arrangements. If it fails
    the solver reports search failure, not mathematical infeasibility.
    """
    kinds = set(kinds or [])
    quotas = dict(quotas or {})
    if count < 1 or not 1 <= min_level <= max_level <= 5:
        raise ValueError('题数和难度范围不合法')
    if max_minutes is not None and max_minutes < 1:
        raise ValueError('最大时长必须为正整数')
    if any(t not in TOPICS or type(n) is not int or n < 0
           for t, n in quotas.items()):
        raise ValueError('配额包含未知模块或无效题数')
    if sum(quotas.values()) > count:
        raise ValueError('模块配额总和大于试卷总题数')

    # A forged quality_status without signed-off evidence must not enter a
    # production paper, even when this CLI is run outside CI.
    if not allow_pending:
        approval_errors, _, _ = validate_reviews(ROOT)
        if approval_errors:
            raise ValueError('六轮审核凭证无效，不得正式组卷：' + '; '.join(approval_errors[:3]))

    pool = [p for p in items if
            (not topics or p['topic'] in topics)
            and (not kinds or p['kind'] in kinds)
            and min_level <= p['level'] <= max_level
            and (allow_pending or p['quality_status'] == '质检通过')]
    if len(pool) < count:
        raise ValueError(f'只有 {len(pool)} 道符合约束的题，不能组 {count} 道')

    counts = collections.Counter(p['topic'] for p in pool)
    for topic, quantity in quotas.items():
        if counts[topic] < quantity:
            raise ValueError(f'{topic} 配额要求 {quantity} 道，但题池只有 {counts[topic]} 道')
    if quotas:
        possible_after_quota = sum(counts[t] for t in TOPICS if t not in quotas)
        if possible_after_quota < count - sum(quotas.values()):
            raise ValueError('指定为精确配额的模块不参与余量填充，剩余题池不足')

    for attempt in range(128 if max_minutes is not None else 1):
        rng = random.Random(seed + attempt)
        by_topic = {topic:[p for p in pool if p['topic']==topic]
                    for topic in TOPICS}
        for group in by_topic.values():
            rng.shuffle(group)
        chosen = []
        for topic in TOPICS:
            if topic in quotas:
                for _ in range(quotas[topic]):
                    chosen.append(by_topic[topic].pop())
        fill_topics = [t for t in TOPICS if t not in quotas]
        while len(chosen) < count:
            changed = False
            for topic in fill_topics:
                if by_topic[topic] and len(chosen) < count:
                    chosen.append(by_topic[topic].pop())
                    changed = True
            if not changed:
                break
        if len(chosen) != count:
            raise ValueError('满足模块精确配额的题目不足')
        duration = sum(p['estimated_minutes'] for p in chosen)
        if max_minutes is None or duration <= max_minutes:
            return sorted(chosen, key=lambda x:(TOPICS.index(x['topic']), x['id']))
    raise ValueError('在128组可复现采样中未找到满足考试时间上限的组卷；'
                     '请放宽时长或调整筛选条件')


def assign_points(items, total_points):
    """Deterministic integer allocation; sum exactly equals target, minimum 1."""
    if total_points < len(items):
        raise ValueError('总分至少等于题数，以确保每题不低于1分')
    weights=[max(1,p['level'])*p['estimated_minutes'] for p in items]
    remainder=total_points-len(items)
    total_weight=sum(weights)
    raw=[remainder*w/total_weight for w in weights]
    integer=[int(x) for x in raw]
    left=remainder-sum(integer)
    order=sorted(range(len(items)), key=lambda i:(-(raw[i]-integer[i]),items[i]['id']))
    for i in order[:left]:
        integer[i]+=1
    return [x+1 for x in integer]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--count',type=int,default=10)
    ap.add_argument('--seed',type=int,default=20261026)
    ap.add_argument('--topic',action='append',choices=TOPICS,default=[])
    ap.add_argument('--kind',action='append',default=[],help='精确匹配题型，可重复')
    ap.add_argument('--topic-quota',action='append',default=[],metavar='模块=题数',
                    help='指定模块的精确题数，可重复')
    ap.add_argument('--min-level',type=int,default=1)
    ap.add_argument('--max-level',type=int,default=5)
    ap.add_argument('--max-minutes',type=int,default=None,help='总预计用时上限')
    ap.add_argument('--total-points',type=int,default=None,help='总分，分值自动分配为整数')
    ap.add_argument('--allow-pending',action='store_true',help='仅内部草稿组卷')
    ap.add_argument('--output-dir',type=Path,default=ROOT/'generated')
    args=ap.parse_args()
    quotas={}
    for spec in args.topic_quota:
        if '=' not in spec:
            ap.error('--topic-quota 需要 模块=题数，例如 力学=2')
        topic,raw=spec.rsplit('=',1)
        if topic not in TOPICS or not raw.isdigit() or topic in quotas:
            ap.error('模块配额必须是已知模块=非负整数，且不能重复')
        quotas[topic]=int(raw)

    items=load_bank(ROOT)
    errors,_=check(items,ROOT)
    if errors:
        ap.error('题库结构校验未通过：'+'; '.join(errors[:3]))
    try:
        chosen=assemble(items,args.count,args.seed,args.topic,args.min_level,
                        args.max_level,args.allow_pending,args.kind,
                        quotas,args.max_minutes)
    except ValueError as exc:
        ap.error(str(exc))

    points=None
    if args.total_points is not None:
        try:
            points=assign_points(chosen,args.total_points)
        except ValueError as exc:
            ap.error(str(exc))
    selected=[dict(p) for p in chosen]
    if points is not None:
        for item,score in zip(selected,points):
            item['exam_points']=score
    output=args.output_dir.resolve()
    output.mkdir(parents=True,exist_ok=True)
    for answers,name in ((False,'exam_questions.tex'),(True,'exam_solutions.tex')):
        (output/name).write_text(render(selected,answers,output,ROOT),encoding='utf-8')

    manifest={
        'schema_version':1,
        'status':'draft_only' if args.allow_pending else 'approved',
        'seed':args.seed,
        'question_ids':[p['id'] for p in chosen],
        'question_count':len(chosen),
        'estimated_minutes':sum(p['estimated_minutes'] for p in chosen),
        'total_points':sum(points) if points is not None else None,
        'topic_counts':{t:sum(p['topic']==t for p in chosen) for t in TOPICS},
        'kind_counts':dict(sorted(collections.Counter(p['kind'] for p in chosen).items())),
        'selection_constraints':{
            'topic_filter':args.topic,'kind_filter':args.kind,
            'topic_quota':quotas,'min_level':args.min_level,
            'max_level':args.max_level,'max_minutes':args.max_minutes},
        'questions':[
            {'id':p['id'],'topic':p['topic'],'kind':p['kind'],
             'level':p['level'],'estimated_minutes':p['estimated_minutes'],
             'points':points[i] if points is not None else None}
            for i,p in enumerate(chosen)
        ],
        'sources':'bank/{ID}/{question,solution}.tex',
    }
    (output/'exam_manifest.json').write_text(
        json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
