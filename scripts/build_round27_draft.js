#!/usr/bin/env node
'use strict';
const fs=require('fs'),path=require('path');
const ranges={M:[172,178],E:[172,178],T:[165,171],W:[165,171],O:[156,161],Q:[156,161]};
const ids=Object.entries(ranges).flatMap(([p,[a,b]])=>Array.from({length:b-a+1},(_,i)=>p+String(a+i).padStart(3,'0')));
const out='build/round27';fs.mkdirSync(out,{recursive:true});
function esc(s){return s.replace(/[&%$#_{}]/g,c=>'\\'+c);}
const header=[
 '\\documentclass[11pt,a4paper]{ctexart}',
 '\\usepackage{amsmath,amssymb,mathtools,geometry,hyperref}',
 '\\geometry{margin=23mm}',
 '\\hypersetup{hidelinks}',
 '\\setlength{\\parindent}{2em}',
 '\\begin{document}',
 '\\begin{center}{\\LARGE\\bfseries 三千弱水 · 大学物理高难度综合题}\\par\\medskip{\\large 第二十七批 · 四十题内部校对稿}\\end{center}',
 '\\noindent\\textbf{学术审校状态：待独立专家逐题复核。自动检查、公式回归及PDF编译不能替代独立审稿；正式主库实行每批50题门禁。}',
 '\\par\\bigskip\\tableofcontents\\clearpage'
].join('\n')+'\n';
for(const kind of ['question','solution']){
 let tex=header;
 for(const id of ids){
  const m=JSON.parse(fs.readFileSync(path.join('bank',id,'meta.json'),'utf8'));
  let part=fs.readFileSync(path.join('bank',id,kind+'.tex'),'utf8');
  part=part.replace(/^\(([1-4])\)\s*/gm,(_m,n)=>'\n\\par\\medskip\\noindent\\textbf{('+n+')}\\enspace ');
  tex+='\\section{'+id+'\\quad '+esc(m.title)+'}\n'+part+'\n\\par\\bigskip\n';
 }
 const name=kind==='question'?'round27-questions.tex':'round27-solutions.tex';
 fs.writeFileSync(path.join(out,name),tex+'\\end{document}\n');
}
console.log('Generated 40-problem question and solution books for round27.');
