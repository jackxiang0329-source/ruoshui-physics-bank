#!/usr/bin/env node
'use strict';
const fs=require('fs'),path=require('path');
const ranges={M:[116,122],E:[116,122],T:[109,115],W:[109,115],O:[108,113],Q:[108,113]};
const subjects={M:'力学',E:'电磁学',T:'热学',W:'振动与波动',O:'光学',Q:'近代物理'};
const ids=Object.entries(ranges).flatMap(([p,[a,b]])=>Array.from({length:b-a+1},(_,i)=>p+String(a+i).padStart(3,'0')));
function must(ok,msg){if(!ok)throw Error(msg)}
function parts(s,id){
 const m=[...s.matchAll(/^\(([1-4])\)\s/gm)];
 must(m.length===4,id+' expected four parts, got '+m.length);
 return m.map((x,i)=>({number:+x[1],body:s.slice(x.index+x[0].length,m[i+1]?.index??s.length).trim()}));
}
function math(s,id){
 must((s.match(/(?<!\\)\$/g)||[]).length%2===0,id+' odd inline math dollars');
 let n=0;for(let i=0;i<s.length;i++){if(s[i]==='{'&&s[i-1]!=='\\')n++;if(s[i]==='}'&&s[i-1]!=='\\')n--;must(n>=0,id+' closing brace');}
 must(n===0,id+' opening brace');
}
const old=[];
for(const name of fs.readdirSync('bank')){
 if(!/^[METWOQ]\d{3}$/.test(name)||ids.includes(name))continue;
 const p=path.join('bank',name,'meta.json');
 if(fs.existsSync(p)){const x=JSON.parse(fs.readFileSync(p,'utf8'));old.push({id:name,title:x.title||''});}
}
function bigrams(s){s=s.replace(/[^\p{L}\p{N}]+/gu,'');const z=new Set();for(let i=0;i<s.length-1;i++)z.add(s.slice(i,i+2));return z}
function jac(a,b){const A=bigrams(a),B=bigrams(b);let hit=0;for(const x of A)if(B.has(x))hit++;return hit/(A.size+B.size-hit||1)}
const items=[];
for(const id of ids){
 const dir=path.join('bank',id),meta=JSON.parse(fs.readFileSync(path.join(dir,'meta.json'),'utf8'));
 const q=fs.readFileSync(path.join(dir,'question.tex'),'utf8'),s=fs.readFileSync(path.join(dir,'solution.tex'),'utf8');
 must(meta.id===id,id+' wrong id');must(meta.topic===subjects[id[0]],id+' wrong topic');
 must(meta.quality_status==='待独立复核'&&meta.tier==='advanced_composite',id+' invalid review gate');
 must(meta.level>=4&&meta.estimated_minutes>=40,id+' insufficient difficulty metadata');
 must(Array.isArray(meta.tags)&&meta.tags.length>=3,id+' insufficient tags');
 const qparts=parts(q,id+' question'),sparts=parts(s,id+' solution');
 for(let j=0;j<4;j++){
  must(qparts[j].number===j+1&&sparts[j].number===j+1,id+' part order');
  must(qparts[j].body.length>=18,id+' question part '+(j+1)+' too short');
  must(sparts[j].body.length>=95,id+' solution part '+(j+1)+' too short');
 }
 math(q,id+' question');math(s,id+' solution');
 must(!old.some(x=>x.title===meta.title),id+' exact historical title duplication');
 const ranked=old.map(x=>({id:x.id,similarity:jac(meta.title,x.title)})).sort((a,b)=>b.similarity-a.similarity);
 items.push({id,title:meta.title,topic:meta.topic,question_parts:4,solution_parts:4,question_chars:q.length,solution_chars:s.length,closest_historical_title:ranked[0]});
}
must(items.length===40&&new Set(ids).size===40,'expected exactly 40 unique IDs');
must(new Set(items.map(x=>x.title)).size===40,'duplicate round19 titles');
process.stdout.write(JSON.stringify({round:19,source_triples:40,question_parts:160,solution_parts:160,completed_independent_subpart_checks:0,global_semantic_model_review:'pending',model_family_manual_review:'pending',compiled_pdfs:'separate CI job',expert_review:'待独立复核',merge_allowed:false,items},null,2)+'\n');
