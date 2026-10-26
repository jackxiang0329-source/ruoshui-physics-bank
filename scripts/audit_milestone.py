#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit the first 100-item manuscript without claiming physics peer review.

Run: python scripts/audit_milestone.py
This script reads data and prints an audit result; it writes no files.
"""
import collections
import csv
import json
import re
import sys
from pathlib import Path

from build import ROOT, TOPICS, load_bank, check, escape


def verify_index_metadata(rows, problems):
    """Compare CSV values against authoritative per-item metadata, not just IDs."""
    errors=[]
    expected_by_id={item['id']: item for item in problems}
    required=['id','topic','kind','level','estimated_minutes','title','tags','quality_status']
    for row in rows:
        pid=row.get('id','')
        if pid not in expected_by_id:
            errors.append(f'CSV含未知题号: {pid}')
            continue
        item=expected_by_id[pid]
        expected={
            'id':pid,'topic':item['topic'],'kind':item['kind'],
            'level':str(item['level']),'estimated_minutes':str(item['estimated_minutes']),
            'title':item['title'],'tags':';'.join(item['tags']),
            'quality_status':item['quality_status'],
        }
        for key in required:
            if row.get(key)!=expected[key]:
                errors.append(f'{pid}: CSV {key} 与独立元数据不一致')
    return errors


def verify_master_metadata(items, question_book, solution_book):
    """Detect metadata edits not reflected in either rendered ElegantBook master."""
    errors=[]
    for item in items:
        uid=item['id']
        header=(r'\noindent{\large\bfseries 【'+uid+'】 '+escape(item['title'])+
                r'}\quad{\small 难度 '+str(item['level'])+'/5 · '+
                escape(item['kind'])+r'}\par')
        for name,body in [('questions.tex',question_book),('solutions.tex',solution_book)]:
            if body.count(header)!=1:
                errors.append(f'{uid}: {name} 题目标题/题型/难度没有按元数据同步')
        answer=(r'\par\noindent\textbf{答案：}\(\displaystyle '+
                item['answer']+r'\)\par')
        # The solutions book should contain exactly one keyed answer per ID.
        marker=r'\input{../bank/'+uid+r'/solution.tex}'
        start=solution_book.find(marker)
        if start<0:
            errors.append(f'{uid}: 解析册缺失独立解答引用')
        else:
            found=solution_book.find(answer,start,start+len(marker)+600)
            if found<0:
                errors.append(f'{uid}: 解析册标准答案与元数据不一致')
    return errors


def audit(root=ROOT, minimum=100):
    problems=load_bank(root)
    errors,counts=check(problems,root)
    ids=[p['id'] for p in problems]
    known=set(ids)
    if len(ids)<minimum:
        errors.append(f'题量不足: {len(ids)} < {minimum}')
    if len(known)!=len(ids):
        errors.append('重复的稳定题号')
    for topic in TOPICS:
        if not counts.get(topic):
            errors.append(f'缺少物理模块: {topic}')

    for filename,fragment in [('questions.tex','question'),('solutions.tex','solution')]:
        path=root/'tex'/filename
        if not path.is_file():
            errors.append('缺失总册: '+filename)
            continue
        text=path.read_text(encoding='utf-8')
        refs=re.findall(
            r'\\input\{\.\./bank/([METWOQ]\d{3,5})/'+fragment+r'\.tex\}',text)
        if len(refs)!=len(known) or set(refs)!=known:
            errors.append(f'{filename} 引用数或题号集不一致')
        if len(refs)!=len(set(refs)):
            errors.append(f'{filename} 存在重复引用')
        if fragment=='question' and '/solution.tex' in text:
            errors.append('试题册意外引用解析')
    with (root/'data'/'index.csv').open('r',encoding='utf-8-sig',newline='') as inp:
        rows=list(csv.DictReader(inp))
    rowids=[r.get('id','') for r in rows]
    if len(rowids)!=len(known) or set(rowids)!=known:
        errors.append('CSV题号集与单题源不一致')
    if len(rowids)!=len(set(rowids)):
        errors.append('CSV索引重复题号')
    errors.extend(verify_index_metadata(rows, problems))

    report_file=root/'data'/'qa_report.json'
    if report_file.exists():
        report=json.loads(report_file.read_text(encoding='utf-8'))
        if report.get('problem_count')!=len(problems):
            errors.append('qa_report.json 的题量与独立题源不一致')
        if report.get('module_counts')!=dict(counts):
            errors.append('qa_report.json 的模块数量与独立题源不一致')

    qbook=root/'tex'/'questions.tex'
    sbook=root/'tex'/'solutions.tex'
    if qbook.exists() and sbook.exists():
        errors.extend(verify_master_metadata(
            problems,qbook.read_text(encoding='utf-8'),sbook.read_text(encoding='utf-8')))

    source=(root/'scripts'/'check_physics.py').read_text(encoding='utf-8')
    checked=re.findall(r"verify\('([METWOQ]\d{3,5})'",source)
    if set(checked)!=known or len(checked)!=len(known):
        errors.append('符号/数值验证定义未覆盖每个题号或出现重复')
    option_count=sum(p['kind']=='选择题' for p in problems)
    pending=sum(p['quality_status']=='待独立复核' for p in problems)
    approved=sum(p['quality_status']=='质检通过' for p in problems)
    if pending+approved!=len(problems):
        errors.append('存在未知审核状态')

    return errors, {
        'written_questions':len(problems),
        'topic_counts':dict(counts),
        'kind_counts':dict(sorted(collections.Counter(p['kind'] for p in problems).items())),
        'level_counts':dict(sorted(collections.Counter(str(p['level']) for p in problems).items())),
        'multiple_choice_items':option_count,
        'independent_question_tex_files':len(problems),
        'independent_solution_tex_files':len(problems),
        'defined_formula_checks':len(checked),
        'qa_pending':pending,
        'qa_approved_declared':approved,
        'limitation':'审计只检查题量、结构和验证定义覆盖，无法证明公式全部成立、解答正确或六轮独立审稿完成',
    }


def main():
    errors,summary=audit()
    summary['result']='passed' if not errors else 'failed'
    summary['errors']=errors
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    return 0 if not errors else 1


if __name__=='__main__':
    sys.exit(main())
