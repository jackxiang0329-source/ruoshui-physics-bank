#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build questions/solutions with deterministic order and run structural QA.

Usage: python scripts/build.py [--compile] [--project-root PATH]
Requires: Python >=3.9. Optional PDF compile: latexmk + XeLaTeX + ctex.
"""
import argparse, collections, csv, json, re, shutil, subprocess, sys
from pathlib import Path

TOPICS=['力学','电磁学','热学','振动与波动','光学','近代物理']
TEX_PREAMBLE = r'''\documentclass[UTF8,a4paper,11pt]{ctexart}
\usepackage[a4paper,top=2.35cm,bottom=2.1cm,left=2.3cm,right=2.3cm]{geometry}
\usepackage{amsmath,amssymb,mathtools,booktabs,array,xcolor}
\usepackage{fancyhdr,lastpage,hyperref}
\definecolor{ink}{HTML}{15324B}
\definecolor{accent}{HTML}{167D8D}
\definecolor{dim}{HTML}{506778}
\hypersetup{colorlinks=true,linkcolor=accent,urlcolor=accent,pdfauthor={三千弱水大学物理原创试题库}}
\pagestyle{fancy}\fancyhf{}\fancyhead[L]{\small\color{dim} 三千弱水 · 大学物理原创题库}
\fancyhead[R]{\small\color{dim} 阶段一 · 样板题}\fancyfoot[C]{\small\thepage/\pageref{LastPage}}
\renewcommand{\headrulewidth}{0.3pt}
\setlength{\parindent}{2em}\setlength{\parskip}{.35em}
\allowdisplaybreaks
'''
TEX_END=r'\end{document}'+'\n'


def cover(is_solution,n):
    name='参考解答与推导' if is_solution else '试题册'
    sub='Solutions and Derivations' if is_solution else 'Original Examination Problems'
    return r'''\begin{titlepage}
\thispagestyle{empty}
\vspace*{1.5cm}
{\color{accent}\rule{\linewidth}{2.4pt}}
\vspace{2.1cm}
\begin{center}
{\fontsize{32}{42}\selectfont\bfseries\color{ink} 大学物理原创试题库}\par
\vspace{.55cm}
{\fontsize{21}{30}\selectfont\color{ink} '''+name+r'''}\par
\vspace{.35cm}
{\large\color{dim} '''+sub+r'''}\par
\vspace{2.0cm}
{\Huge\color{accent}\bfseries '''+str(n)+r'''\quad 道}\par
\vspace{.65cm}
{\large 力学 · 电磁学 · 热学 · 振动与波动 · 光学 · 近代物理}\par
\vspace{1.25cm}
{\color{dim}\rule{.55\linewidth}{.6pt}}\par
\vspace{.8cm}
{\large 三千弱水 · Ruoshui Physics Bank}\par
\vspace{.3cm}
{\color{dim}\small 2026 年 10 月 · 第一批样板 · 不代表六轮人工质检已完成}\par
\end{center}
\vfill
{\color{accent}\rule{\linewidth}{2.4pt}}
\end{titlepage}
'''


def check(problems):
    errors=[]
    ids=[p.get('id','') for p in problems]
    counts=collections.Counter(p.get('topic','') for p in problems)
    if len(set(ids))!=len(ids): errors.append('题目ID重复')
    if len(set(p.get('question','').strip() for p in problems))!=len(problems): errors.append('题面完全重复')
    for p in problems:
        uid=p.get('id','?')
        if not re.fullmatch(r'[ME T WOQ]'.replace(' ', '')+r'\d{3}', uid): errors.append(f'{uid}: ID格式')
        if p.get('topic') not in TOPICS: errors.append(f'{uid}: 未知知识模块')
        if not isinstance(p.get('level'),int) or not 1<=p['level']<=5: errors.append(f'{uid}: 难度无效')
        if not isinstance(p.get('estimated_minutes'),int) or not 1<=p['estimated_minutes']<=120: errors.append(f'{uid}: 预计用时无效')
        if not isinstance(p.get('tags'),list) or not p['tags'] or not all(isinstance(x,str) and x.strip() for x in p['tags']): errors.append(f'{uid}: 知识点标签无效')
        for k in ['title','question','solution','answer','quality_status','kind']:
            if not str(p.get(k,'')).strip(): errors.append(f'{uid}: 缺失 {k}')
        for k in ['question','solution','answer']:
            s=p.get(k,'')
            if s.count('$')%2: errors.append(f'{uid}: {k} 行内数学定界符不成对')
            if '\\write18' in s or '\\input{' in s or '\\include{' in s: errors.append(f'{uid}: 不允许外部TeX命令')
    if any(counts.get(x,0)==0 for x in TOPICS): errors.append('六大模块未全部覆盖')
    return errors,counts


def render(problems,has_solution):
    title='大学物理原创试题库 · 参考解答' if has_solution else '大学物理原创试题库 · 试题'
    out=TEX_PREAMBLE+'\\hypersetup{pdftitle={'+title+'}}\n\\begin{document}\n'+cover(has_solution,len(problems))
    out+=r'\tableofcontents\clearpage'+'\n'
    for topic in TOPICS:
        ps=[p for p in problems if p['topic']==topic]
        out+='\\section{'+topic+'}\n'
        if not ps:
            continue
        for p in ps:
            out+=r'\noindent{\large\bfseries\color{ink} '+p['id']+' · '+p['title']+r'}\quad{\small\color{dim}[难度 '+str(p['level'])+' / 5 · '+p['kind']+r']}\par'+'\n'
            out+=r'\noindent\textbf{题目}：'+p['question']+'\n'
            if has_solution:
                out+=r'\par\noindent\textbf{解答}：'+p['solution']+'\n'
                out+=r'\par\noindent\textbf{结论}：\(\displaystyle '+p['answer']+r'\)\par'+'\n'
            out+=r'\vspace{1.0em}\par\noindent{\color{accent}\rule{\linewidth}{.35pt}}\vspace{.8em}'+'\n'
    return out+TEX_END


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--compile',action='store_true',help='Compile pdf with latexmk/xelatex')
    parser.add_argument('--project-root',type=Path,default=Path(__file__).resolve().parent.parent)
    args=parser.parse_args(); root=args.project_root.resolve()
    problems=json.loads((root/'data/problems.json').read_text(encoding='utf-8'))
    errors,counts=check(problems)
    if errors:
        print('\n'.join('ERROR: '+x for x in errors),file=sys.stderr); return 1
    (root/'tex').mkdir(exist_ok=True,parents=True)
    (root/'pdf').mkdir(exist_ok=True,parents=True)
    for flag,name in [(False,'questions'),(True,'solutions')]:
        (root/'tex'/f'{name}.tex').write_text(render(problems,flag),encoding='utf-8')
    with (root/'data/index.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['id','topic','kind','level','estimated_minutes','title','tags','quality_status'])
        w.writerows([p['id'],p['topic'],p['kind'],p['level'],p['estimated_minutes'],p['title'],';'.join(p['tags']),p['quality_status']] for p in problems)
    report={'problem_count':len(problems),'module_counts':dict(counts),'schema_check':'passed','id_uniqueness':'passed','exact_question_dedup':'passed','latex_math_delimiters':'passed','compile_status':'not_requested','independent_solution_review':'pending','textbook_fulltext_comparison':'not_performed','six_round_quality_review':'not_performed'}
    if args.compile:
        if not shutil.which('latexmk'): print('ERROR: latexmk not found',file=sys.stderr); return 2
        for name in ['questions','solutions']:
            cmd=['latexmk','-xelatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','-outdir='+str(root/'pdf'),str(root/'tex'/f'{name}.tex')]
            proc=subprocess.run(cmd,cwd=root/'tex',capture_output=True,text=True)
            if proc.returncode:
                print(proc.stdout[-3500:],file=sys.stderr);print(proc.stderr[-1000:],file=sys.stderr)
                report['compile_status']=f'failed_at_{name}'
                (root/'data/qa_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
                return 3
        report['compile_status']='passed'
    (root/'data/qa_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0

if __name__=='__main__':sys.exit(main())
