#!/usr/bin/env node
'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const ranges={M:[144,150],E:[144,150],T:[137,143],W:[137,143],O:[132,137],Q:[132,137]};
const subjects={M:'力学',E:'电磁学',T:'热学',W:'振动与波动',O:'光学',Q:'近代物理'};
const ids=Object.entries(ranges).flatMap(([p,[a,b]])=>Array.from({length:b-a+1},(_,i)=>p+String(a+i).padStart(3,'0')));
function must(ok,msg){if(!ok)throw Error(msg);}
function parts(s,id,kind){
 const ms=[...s.matchAll(/^\(([1-4])\)\s/gm)];
 must(ms.length===4,id+': '+kind+' must have four parts');
 return ms.map((m,i)=>{must(+m[1]===i+1,id+': order');return s.slice(m.index+m[0].length,ms[i+1]?.index??s.length).trim();});
}
function tex(s,id){
 must(!/\\(?:input|include|write18|openout|documentclass|catcode|begin\{document\})/.test(s),id+': dangerous TeX');
 let braces=0;for(let i=0;i<s.length;i++){if(s[i]==='{'&&s[i-1]!=='\\')braces++;if(s[i]==='}'&&s[i-1]!=='\\')braces--;must(braces>=0,id+': unexpected }');}
 must(braces===0,id+': missing }');
 must((s.match(/(?<!\\)\$/g)||[]).length%2===0,id+': unbalanced math $');
}
function gram(s,n){s=s.replace(/[^\p{L}\p{N}]+/gu,'');const out=new Set();for(let i=0;i+n<=s.length;i++)out.add(s.slice(i,i+n));return out;}
function jac(s,t,n){const a=gram(s,n),b=gram(t,n);let overlap=0;for(const v of a)if(b.has(v))overlap++;return overlap/(a.size+b.size-overlap||1);}
const old=[],seenTitles=new Set(),seenQuestions=new Set(),report=[],counts={};
for(const folder of fs.readdirSync('bank')){
 if(!/^[METWOQ]\d{3}$/.test(folder)||ids.includes(folder))continue;
 const dir=path.join('bank',folder),mp=path.join(dir,'meta.json'),qp=path.join(dir,'question.tex');
 if(fs.existsSync(mp)&&fs.existsSync(qp)){let m=JSON.parse(fs.readFileSync(mp,'utf8'));old.push({id:folder,title:m.title,question:fs.readFileSync(qp,'utf8')});}
}
const targeted={
 M146:/软链|桌缘滑链/,E148:/RC传输线|电压扩散/,
 W137:/弦的行波散射|透射振幅/,W138:/阻尼弦|复本征频率/,
 O133:/迈克耳孙|条纹计数/,O134:/线光源|空间相干度/,
 O135:/高斯光束|瑞利长度/,O137:/Jones相位延迟|四十五度线偏振/,
 Q134:/谐振子相干态|泊松光子数/,Q135:/量子势阶|势阶跃/
};
for(const id of ids){
 const dir=path.join('bank',id),m=JSON.parse(fs.readFileSync(path.join(dir,'meta.json'),'utf8'));
 const q=fs.readFileSync(path.join(dir,'question.tex'),'utf8'),s=fs.readFileSync(path.join(dir,'solution.tex'),'utf8');
 must(m.id===id&&m.topic===subjects[id[0]],id+': topic or id mismatch');
 must(m.quality_status==='待独立复核'&&m.tier==='advanced_composite',id+': review gate');
 must(m.kind==='综合推导题'&&m.format==='latex-fragment-v1',id+': format gate');
 must(m.level===5&&m.estimated_minutes>=40,id+': difficulty gate');
 must(Array.isArray(m.tags)&&m.tags.length>=3,id+': cross-topic tags');
 must(!seenTitles.has(m.title)&&!old.some(h=>h.title===m.title),id+': duplicated exact title');
 must(!seenQuestions.has(q.trim()),id+': duplicated new question');seenTitles.add(m.title);seenQuestions.add(q.trim());
 must(!targeted[id]||!targeted[id].test(m.title),id+': previously identified duplicate model returned');
 tex(q,id+' question');tex(s,id+' solution');
 const qs=parts(q,id,'question'),ss=parts(s,id,'solution');
 for(let j=0;j<4;j++){must(qs[j].length>=12,id+': insufficient task '+(j+1));must(ss[j].length>=95,id+': insufficient derivation '+(j+1));must(/\$/.test(ss[j]),id+': missing formula '+(j+1));}
 const near=old.map(h=>({id:h.id,question_similarity:jac(q,h.question,4),title_similarity:jac(m.title,h.title,2)})).sort((a,b)=>b.question_similarity-a.question_similarity)[0];
 must(!old.some(h=>jac(q,h.question,4)>=.88),id+': near exact prior problem');
 must(!old.some(h=>jac(m.title,h.title,2)>=.92),id+': near exact prior title');
 counts[m.topic]=(counts[m.topic]||0)+1;
 report.push({id,title:m.title,parts:4,solution_chars:s.length,nearest_prior:near,sha256:crypto.createHash('sha256').update(q+'\n'+s).digest('hex')});
}
must(report.length===40,'must have 40 source triples');
for(const [prefix,[a,b]] of Object.entries(ranges))must(counts[subjects[prefix]]===b-a+1,'wrong category '+prefix);
const risky=report.filter(r=>r.nearest_prior?.question_similarity>=.42);
process.stdout.write(JSON.stringify({round:23,status:'STRUCTURE_PASSED_INDEPENDENT_REVIEW_PENDING',count:40,prior_canonical_count:old.length,question_parts:160,solution_parts:160,structural_subpart_checks:160,prior_near_matches_for_manual_review:risky,counts,expert_reviews_completed:0,items:report},null,2)+'\n');
