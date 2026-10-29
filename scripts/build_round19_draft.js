#!/usr/bin/env node
'use strict';
const fs=require('fs'),path=require('path');
const ranges={M:[116,122],E:[116,122],T:[109,115],W:[109,115],O:[108,113],Q:[108,113]};
const ids=Object.entries(ranges).flatMap(([p,[a,b]])=>Array.from({length:b-a+1},(_,i)=>p+String(a+i).padStart(3,'0')));
const out='build/round19';fs.mkdirSync(out,{recursive:true});
const pre=String.raw\`\documentclass[11pt,a4paper]{ctexart}
\usepackage{amsmath,amssymb,geometry,hyperref}
\geometry{margin=23mm}
\hypersetup{hidelinks}
\setlength{\parindent}{2em}
\begin{document}
\begin{center}{\LARGE\bfseries 三千弱水·大学物理高阶综合题}\par\medskip{\large 第十九批内部审校草稿}\end{center}
\noindent\textbf{状态：待独立复核。仅供审校，不满足正式每轮50题、200项分问验证的准入条件。}
\par\bigskip
\tableofcontents
\clearpage
\`;
const post=String.raw\`\end{document}
\`;
for(const kind of ['question','solution']){
 let body=pre;
 for(const id of ids){
  const m=JSON.parse(fs.readFileSync(path.join('bank',id,'meta.json'),'utf8'));
  const src=fs.readFileSync(path.join('bank',id,kind+'.tex'),'utf8');
  const parts=src.replace(/^\(([1-4])\)\s*/gm,(_x,n)=>'\n\n\\par\\medskip\\noindent\\textbf{('+n+')}\\enspace ');
  body+='\\section{'+id+'\\quad '+m.title+'}\n'+parts+'\n\\bigskip\n';
 }
 fs.writeFileSync(path.join(out,'round19-'+(kind==='question'?'questions':'solutions')+'.tex'),body+post);
}
process.stdout.write('Generated two draft-only XeLaTeX books for 40 problems.\n');
