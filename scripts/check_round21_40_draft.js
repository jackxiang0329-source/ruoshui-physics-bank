#!/usr/bin/env node
'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const ranges={M:[130,136],E:[130,136],T:[123,129],W:[123,129],O:[120,125],Q:[120,125]};
const topics={M:'力学',E:'电磁学',T:'热学',W:'振动与波动',O:'光学',Q:'近代物理'};
const ids=Object.entries(ranges).flatMap(([p,[lo,hi]])=>Array.from({length:hi-lo+1},(_,i)=>p+String(lo+i).padStart(3,'0')));
function must(ok,msg){if(!ok)throw Error(msg);}
function splitParts(t,id,kind){
 const a=[...t.matchAll(/^\(([1-4])\)\s*/gm)];
 must(a.length===4,id+' '+kind+': four numbered parts required');
 return a.map((m,j)=>{
  must(Number(m[1])===j+1,id+' '+kind+': wrong part order');
  return t.slice(m.index+m[0].length,a[j+1]?.index??t.length).trim();
 });
}
function texCheck(text,id){
 must(!/\\(?:input|include|write18|openout|documentclass|catcode)/.test(text),id+': unsafe TeX input');
 must((text.match(/(?<!\\)\$/g)||[]).length%2===0,id+': unbalanced dollars');
 let n=0;for(let i=0;i<text.length;i++){if(text[i]==='{'&&text[i-1]!=='\\')n++;if(text[i]==='}'&&text[i-1]!=='\\')n--;must(n>=0,id+': unmatched brace');}
 must(n===0,id+': unmatched brace');
}
function grams(s){s=s.replace(/[^\p{L}\p{N}]+/gu,'');let o=new Set();for(let i=0;i<s.length-1;i++)o.add(s.slice(i,i+2));return o;}
function jac(a,b){const A=grams(a),B=grams(b);let n=0;for(const g of A)if(B.has(g))n++;return n/(A.size+B.size-n||1);}
let historical=[];
for(const name of fs.readdirSync('bank')){
 if(!/^[METWOQ]\d{3}$/.test(name)||ids.includes(name))continue;
 const p=path.join('bank',name,'meta.json');
 if(fs.existsSync(p)){const x=JSON.parse(fs.readFileSync(p,'utf8'));historical.push({id:name,title:x.title||''});}
}
let usedTitle=new Set(),usedQuestion=new Set(),items=[];
for(const id of ids){
 const dir=path.join('bank',id),m=JSON.parse(fs.readFileSync(path.join(dir,'meta.json'),'utf8'));
 const q=fs.readFileSync(path.join(dir,'question.tex'),'utf8'),s=fs.readFileSync(path.join(dir,'solution.tex'),'utf8');
 must(m.id===id&&m.topic===topics[id[0]],id+': metadata category mismatch');
 must(m.quality_status==='待独立复核'&&m.tier==='advanced_composite',id+': review flag');
 must(m.level===5&&m.estimated_minutes>=40&&m.tags.length>=3,id+': level/tags');
 must(m.kind==='综合推导题'&&m.format==='latex-fragment-v1',id+': format');
 must(!usedTitle.has(m.title)&&!historical.some(x=>x.title===m.title),id+': duplicate title');
 usedTitle.add(m.title);
 const normalized=q.replace(/\s+/g,'');
 must(!usedQuestion.has(normalized),id+': duplicate exact question');
 usedQuestion.add(normalized);
 texCheck(q,id+' question');texCheck(s,id+' solution');
 const a=splitParts(q,id,'question'),b=splitParts(s,id,'solution');
 for(let j=0;j<4;j++){must(a[j].length>=12,id+': short question part '+(j+1));must(b[j].length>=90,id+': short solution part '+(j+1));}
 const nearest=historical.map(x=>({id:x.id,similarity:jac(m.title,x.title)})).sort((x,y)=>y.similarity-x.similarity)[0];
 items.push({id,topic:m.topic,title:m.title,question_parts:4,solution_parts:4,nearest_title:nearest,sha256:crypto.createHash('sha256').update(q+'\n'+s).digest('hex')});
}
must(ids.length===40&&items.length===40,'expected 40 problems');
let counts={};for(const x of items)counts[x.topic]=(counts[x.topic]||0)+1;
must(Object.entries(topics).every(([p,t])=>counts[t]===ranges[p][1]-ranges[p][0]+1),'distribution mismatch');
process.stdout.write(JSON.stringify({round:21,source_triples:40,question_parts:160,solution_parts:160,history_count:historical.length,automated_subpart_checks_from_numeric_runner:'separate',expert_review:'待独立复核',release_allowed:false,counts,items},null,2)+'\n');
