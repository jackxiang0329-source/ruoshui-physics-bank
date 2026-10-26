#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fail closed: no question can be approved without six evidence-backed reviews.

This validator checks presence and current-source binding of review records.
It does not assess a reviewer's expertise or independently re-solve a problem.
"""
import hashlib
import json
import re
import sys
from pathlib import Path
from build import ROOT, load_bank

ALLOWED={'待独立复核','质检通过'}
ROUNDS=(
    '题意与条件',
    '独立推导与量纲',
    '答案与极限验证',
    '原创与许可核对',
    '命题难度与表述',
    '排版与出版复校',
)

def digest_for(root,pid):
    h=hashlib.sha256()
    for part in ('question.tex','solution.tex'):
        body=(root/'bank'/pid/part).read_bytes()
        h.update(part.encode('ascii')+b'\x00'+len(body).to_bytes(8,'big')+body)
    return h.hexdigest()

def validate(root=ROOT):
    problems=load_bank(root)
    errors=[]
    approved=0
    for p in problems:
        pid=p['id']
        status=p.get('quality_status')
        if status not in ALLOWED:
            errors.append(f'{pid}: quality_status invalid: {status!r}')
            continue
        review_path=root/'qa'/(pid+'.json')
        if status=='待独立复核':
            # Pending questions are never silently authorized by an old record.
            continue
        approved+=1
        if not review_path.is_file():
            errors.append(f'{pid}: approved without qa/{pid}.json')
            continue
        try:
            review=json.loads(review_path.read_text(encoding='utf-8'))
        except (OSError,ValueError) as e:
            errors.append(f'{pid}: invalid review file: {e}')
            continue
        if review.get('id')!=pid:
            errors.append(f'{pid}: mismatched QA record id')
        if review.get('source_sha256')!=digest_for(root,pid):
            errors.append(f'{pid}: review proof bound to stale TeX contents')
        if review.get('final_decision')!='approved':
            errors.append(f'{pid}: final decision is not approved')
        rounds=review.get('rounds')
        if not isinstance(rounds,list) or len(rounds)!=6:
            errors.append(f'{pid}: exactly six recorded review rounds required')
            continue
        numbers=[r.get('round') if isinstance(r,dict) else None for r in rounds]
        if numbers!=list(range(1,7)):
            errors.append(f'{pid}: round numbers must be 1..6 in order')
        for i,item in enumerate(rounds):
            if not isinstance(item,dict):
                errors.append(f'{pid}: malformed review round {i+1}')
                continue
            if item.get('name')!=ROUNDS[i]:
                errors.append(f'{pid}: wrong review round {i+1} name')
            if item.get('decision')!='approved':
                errors.append(f'{pid}: round {i+1} not approved')
            if not all(isinstance(item.get(k),str) and item[k].strip()
                       for k in ('reviewer','date','evidence')):
                errors.append(f'{pid}: round {i+1} missing reviewer/date/evidence')
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',str(item.get('date',''))):
                errors.append(f'{pid}: round {i+1} date format invalid')
    return errors,len(problems),approved

def main():
    errors,total,approved=validate()
    if errors:
        print('\n'.join('ERROR: '+e for e in errors),file=sys.stderr)
        return 1
    print(f'QA approval gate PASS: {approved} approved / {total} total; '
          f'{total-approved} pending expert review')
    return 0

if __name__=='__main__':
    sys.exit(main())
