#!/usr/bin/env node
'use strict';
const fs=require('fs');const path=require('path');
const ranges={M:[109,115],E:[109,115],T:[102,108],W:[102,108],O:[102,107],Q:[102,107]};
const subjects={M:"力学",E:"电磁学",T:"热学",W:"振动与波动",O:"光学",Q:"近代物理"};
const ids=Object.entries(ranges).flatMap(([p,[a,b]])=>Array.from({length:b-a+1},(_,i)=>p+String(a+i).padStart(3,'0')));
function must(x,msg){if(!x)throw Error(msg)}
function parts(s,id){
 const ms=[...s.matchAll(/^\(([1-4])\)\s/gm)];
 must(ms.length===4,id+' has '+ms.length+' parts, not 4');
 return ms.map((m,i)=>({number:Number(m[1]),body:s.slice(m.index+m[0].length,ms[i+1]?.index??s.length).trim()}));
}
function math(s,id){
 must((s.match(/\$/g)||[]).length%2===0,id+' unpaired inline math $');
 let nesting=0;
 for(let i=0;i<s.length;i++){
  if(s[i]==='{'&&s[i-1]!=='\\')nesting++;
  else if(s[i]==='}'&&s[i-1]!=='\\')nesting--;
  must(nesting>=0,id+' unmatched closing brace');
 }
 must(nesting===0,id+' unmatched opening brace');
}
const items=[];
for(const id of ids){
 const dir=path.join('bank',id);
 const meta=JSON.parse(fs.readFileSync(path.join(dir,'meta.json'),'utf8'));
 const q=fs.readFileSync(path.join(dir,'question.tex'),'utf8');
 const s=fs.readFileSync(path.join(dir,'solution.tex'),'utf8');
 must(meta.id===id,id+' ID mismatch');
 must(meta.topic===subjects[id[0]],id+' wrong physics subject');
 must(meta.quality_status==='待独立复核',id+' review label must stay pending');
 must(meta.level>=4&&meta.estimated_minutes>=40,id+' violates difficulty gate');
 must(meta.tier==='advanced_composite',id+' not composite');
 must(Array.isArray(meta.tags)&&meta.tags.length>=3,id+' insufficient cross-concept tags');
 const qparts=parts(q,id+' question'),sparts=parts(s,id+' solution');
 for(let i=0;i<4;i++){
  must(qparts[i].number===i+1&&sparts[i].number===i+1,id+' disordered four parts');
  must(qparts[i].body.length>=20,id+' question '+(i+1)+' too short');
  must(sparts[i].body.length>=95,id+' solution '+(i+1)+' insufficient derivation');
 }
 math(q,id+' question');math(s,id+' solution');
 items.push({id,title:meta.title,topic:meta.topic,question_parts:4,solution_parts:4,question_chars:q.length,solution_chars:s.length,quality_status:meta.quality_status});
}
must(items.length===40&&new Set(ids).size===40,'Expected 40 distinct IDs');
must(new Set(items.map(x=>x.title)).size===40,'Duplicate titles in round18');
const result={round:18,draft_entries:40,question_subparts:160,solution_subparts:160,completed_independent_subpart_checks:0,global_historical_core_review:'pending',compiled_pdfs:0,expert_review:'待独立复核',merge_allowed:false,items};
process.stdout.write(JSON.stringify(result,null,2)+'\n');
