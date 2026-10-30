#!/usr/bin/env node
'use strict';
const fs=require('fs'),path=require('path');
const ranges={M:[130,136],E:[130,136],T:[123,129],W:[123,129],O:[120,125],Q:[120,125]};
const ids=Object.entries(ranges).flatMap(([p,[a,b]])=>Array.from({length:b-a+1},(_,i)=>p+String(a+i).padStart(3,'0')));
const out='build/round21';fs.mkdirSync(out,{recursive:true});
function esc(s){return s.replace(/[&%$#_{}]/g,c=>'\\'+c);}
const header=[
 '\\documentclass[11pt,a4paper]{ctexart}',
 '\\usepackage{amsmath,amssymb,mathtools,geometry,hyperref}',
 '\\geometry{margin=23mm}',
 '\\hypersetup{hidelinks}',
 '\\setlength{\\parindent}{2em}',
 '\\begin{document}',
 '\\begin{center}{\\LARGE\\bfseries 三千弱水 · 大学物理高阶综合题}\\par\\medskip{\\large 第二十一批内部审校稿}\\end{center}',
 '\\noindent\\textbf{状态：待独立学术复核。本批40题各有四问与解析，自动技术校验不等于专家逐题审核；正式主库仍按每批50题与200项分问检查的规则管理。}',
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
 const name=kind==='question'?'round21-questions.tex':'round21-solutions.tex';
 fs.writeFileSync(path.join(out,name),tex+'\\end{document}\n');
}
process.stdout.write('Generated two round-21 draft books.\n');
