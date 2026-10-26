#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Canonical sources: bank/ID/meta.json, bank/ID/question.tex, bank/ID/solution.tex."""
import argparse
import collections
import csv
import io
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOPICS = ['力学','电磁学','热学','振动与波动','光学','近代物理']
TEMPLATE = r"""\documentclass[lang=cn,color=blue,11pt]{elegantbook}
\usepackage{amsmath,amssymb,mathtools,booktabs}
\title{大学物理原创试题库}
\subtitle{__SUBTITLE__}
\author{三千弱水 · Ruoshui Physics Bank}
\date{2026年10月}
\version{0.2}
\hypersetup{pdftitle={大学物理原创试题库 · __SUBTITLE__}}
\begin{document}
\maketitle
\tableofcontents
\mainmatter
__BODY__
\end{document}
"""

def load_bank(root=ROOT):
    items = []
    for path in sorted((root/'bank').glob('*/meta.json')):
        item=json.loads(path.read_text(encoding='utf-8'))
        item['_dir']=path.parent
        items.append(item)
    return items

def check(items,root=ROOT):
    errors=[]
    ids=[p.get('id','') for p in items]
    counts=collections.Counter(p.get('topic','') for p in items)
    if not items: errors.append('题库为空')
    if len(set(ids))!=len(ids): errors.append('ID重复')
    seen=set()
    for p in items:
        uid=p.get('id','?')
        if not re.fullmatch(r'[METWOQ]\d{3,5}',uid):
            errors.append(uid+': ID无效')
        folder=root/'bank'/uid
        if p.get('_dir')!=folder: errors.append(uid+': 目录不一致')
        if p.get('topic') not in TOPICS: errors.append(uid+': 模块无效')
        if type(p.get('level')) is not int or not 1<=p['level']<=5: errors.append(uid+': 难度无效')
        if type(p.get('estimated_minutes')) is not int or not 1<=p['estimated_minutes']<=120: errors.append(uid+': 用时无效')
        if not isinstance(p.get('tags'),list) or not p['tags']: errors.append(uid+': 标签缺失')
        if p.get('format')!='latex-fragment-v1': errors.append(uid+': 片段格式无效')
        for field in ('title','kind','quality_status','answer'):
            if not str(p.get(field,'')).strip(): errors.append(uid+': 缺失 '+field)
        for section in ('question','solution'):
            fragment=folder/(section+'.tex')
            if not fragment.exists():
                errors.append(uid+': 缺少 '+fragment.name)
                continue
            body=fragment.read_text(encoding='utf-8')
            if not body.strip(): errors.append(uid+': 片段为空')
            if body.count('$')%2: errors.append(uid+': 数学定界符可能不平衡')
            forbidden=(r'\write18',r'\input',r'\include',r'\documentclass',r'\openout',r'\catcode',r'\begin{document}')
            if any(f in body for f in forbidden): errors.append(uid+': 片段含不安全或非独立TeX命令')
            if section=='question':
                normalized=re.sub(r'\s+','',re.sub(r'(?m)^%.*$','',body))
                if normalized in seen: errors.append(uid+': 题面完全重复')
                seen.add(normalized)
    return errors,counts

def escape(text):
    special={'&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}'}
    return ''.join(special.get(x,x) for x in str(text))

def render(items,with_solutions=False,output_dir=None,root=ROOT):
    output_dir=(output_dir or root/'tex').resolve()
    subtitle='参考解答与推导' if with_solutions else '题目选编'
    lines=[]
    for topic in TOPICS:
        group=sorted((p for p in items if p['topic']==topic),key=lambda p:p['id'])
        if not group: continue
        lines.extend(['\\chapter{'+topic+'}',''])
        for p in group:
            uid=p['id']
            lines.append('\\noindent{\\large\\bfseries 【'+uid+'】 '+escape(p['title'])+
                         '}\\quad{\\small 难度 '+str(p['level'])+'/5 · '+escape(p['kind'])+
                         (' · '+str(p['exam_points'])+'分' if 'exam_points' in p else '')+'}\\par')
            relative=(root/'bank'/uid/'question.tex')
            lines.append('\\noindent\\textbf{题目：}\\input{'+Path(os.path.relpath(relative,output_dir)).as_posix()+'}')
            if with_solutions:
                relative=(root/'bank'/uid/'solution.tex')
                lines.append('\\par\\noindent\\textbf{解答：}\\input{'+Path(os.path.relpath(relative,output_dir)).as_posix()+'}')
                lines.append('\\par\\noindent\\textbf{答案：}\\(\\displaystyle '+p['answer']+'\\)\\par')
            lines.append('\\par\\smallskip\\noindent\\hrulefill\\par\\medskip')
    return TEMPLATE.replace('__SUBTITLE__',subtitle).replace('__BODY__','\n'.join(lines))

def render_index(items):
    buf=io.StringIO(newline='')
    w=csv.writer(buf)
    w.writerow(['id','topic','kind','level','estimated_minutes','title','tags','quality_status'])
    for p in sorted(items,key=lambda p:(TOPICS.index(p['topic']),p['id'])):
        w.writerow([p['id'],p['topic'],p['kind'],p['level'],p['estimated_minutes'],
                    p['title'],';'.join(p['tags']),p['quality_status']])
    return '\ufeff'+buf.getvalue()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--check',action='store_true',help='check versioned masters match individual items')
    ap.add_argument('--compile',action='store_true',help='compile with XeLaTeX')
    ap.add_argument('--project-root',type=Path,default=ROOT)
    args=ap.parse_args()
    root=args.project_root.resolve()
    items=load_bank(root)
    errors,counts=check(items,root)
    if errors:
        print('\n'.join('ERROR: '+err for err in errors),file=sys.stderr)
        return 1
    outputs={
        root/'tex'/'questions.tex': render(items,False,root/'tex',root),
        root/'tex'/'solutions.tex': render(items,True,root/'tex',root),
        root/'data'/'index.csv': render_index(items)}
    if args.check:
        missing=[str(f.relative_to(root)) for f,content in outputs.items()
                 if not f.exists() or f.read_text(encoding='utf-8')!=content]
        if missing:
            print('STALE generated documents: '+', '.join(missing),file=sys.stderr)
            return 2
    else:
        for f,content in outputs.items():
            f.parent.mkdir(parents=True,exist_ok=True)
            f.write_text(content,encoding='utf-8')
    report={'problem_count':len(items),'module_counts':dict(counts),'schema_check':'passed',
            'template':'ElegantBook v4.7','source':'bank/ID/*.tex',
            'independent_solution_review':'pending','six_round_quality_review':'not_performed',
            'compile_status':'not_requested'}
    if args.compile:
        if args.check: ap.error('--compile cannot be combined with --check')
        if not shutil.which('latexmk'):
            print('latexmk executable missing',file=sys.stderr)
            return 3
        for basename in ('questions','solutions'):
            process=subprocess.run(['latexmk','-xelatex','-interaction=nonstopmode',
                                    '-halt-on-error',basename+'.tex'],
                                   cwd=root/'tex',capture_output=True,text=True)
            if process.returncode:
                print(process.stdout[-5000:]+'\n'+process.stderr[-1000:],file=sys.stderr)
                return 4
        report['compile_status']='passed'
    if not args.check:
        (root/'data'/'qa_report.json').write_text(
            json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0

if __name__=='__main__':
    sys.exit(main())
