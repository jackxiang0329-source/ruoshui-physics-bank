#!/usr/bin/env node
'use strict';
const fs=require('fs'),path=require('path');
const ranges={M:[130,136],E:[130,136],T:[123,129],W:[123,129],O:[120,125],Q:[120,125]};
const ids=Object.entries(ranges).flatMap(([p,[a,b]])=>Array.from({length:b-a+1},(_,i)=>p+String(a+i).padStart(3,'0')));
const out='build/round21';fs.mkdirSync(out,{recursive:true});
function esc(s){return s.replace(/[&%$#_{}]/g,x=>'\\'+x);}
const header=[
 '\\documentclass[11pt,a4paper]{ctexart}',
 '\\usepackage{amsmath,amssymb,mathtools,geometry,hyperref}',
 '\\geometry{margin=23mm}',
 '\\hypersetup{hidelinks}',
 '\\setlength{\\parindent}{2em}',
 '\\begin{document}',
 '\\begin{center}{\\LARGE\\bfseries 三千弱水 · 大学物理高阶综合题}\\par\\medskip{\\large 第二十一批内部审校稿}\\end{center}',
 '\\noindent\\textbf{稿件状态：待独立复核。40题、160分问尚未完成独立分问验证，不满足正式每批50题/200分问的主分支合并门槛。}',
 '\\par\\bigskip\\tableofcontents\\clearpage'
].join('\n')+'\n';
for(const kind of ['question','solution']){
 let doc=header;
 for(const id of ids){
  const m=JSON.parse(fs.readFileSync(path.join('bank',id,'meta.json'),'utf8'));
  const src=fs.readFileSync(path.join('bank',id,kind+'.tex'),'utf8');
  const body=src.replace(/^\(([1-4])\)\s*/gm,(_s,num)=>'\n\\par\\medskip\\noindent\\textbf{('+num+')}\\enspace ');
  doc+='\\section{'+id+'\\quad '+esc(m.title)+'}\n'+body+'\n\\par\\bigskip\n';
 }
 const filename=kind==='question'?'round21-questions.tex':'round21-solutions.tex';
 fs.writeFileSync(path.join(out,filename),doc+'\\end{document}\n');
}
process.stdout.write('Generated two XeLaTeX review-draft books for 40 problems.\n');
