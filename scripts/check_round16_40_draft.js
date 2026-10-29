#!/usr/bin/env node
'use strict';
// Draft structural gate: 40 unique TeX source triples, 160 four-part statement/answer pairs.
// Structural checks do not attest scientific correctness or independent peer review.
const fs=require('node:fs'),path=require('node:path');
const groups={M:[95,101],E:[95,101],T:[88,94],W:[88,94],O:[90,95],Q:[90,95]};
const topic={M:"力学",E:"电磁学",T:"热学",W:"振动与波动",O:"光学",Q:"近代物理"};
const ids=Object.entries(groups).flatMap(([p,[a,b]])=>Array.from({length:b-a+1},(_,i)=>p+String(a+i).padStart(3,'0')));
const assert=(condition,message)=>{if(!condition)throw Error(message)};
const splitParts=(source)=>{
  const markers=[...source.matchAll(/^\(([1-4])\)\s/gm)];
  assert(markers.length===4,'Expected exactly four labeled sections');
  return markers.map((m,i)=>({
    number:Number(m[1]),
    content:source.slice(m.index+m[0].length,markers[i+1]?.index??source.length).trim()
  }));
};
const checkMath=(s,id)=>{
 assert((s.match(/\$/g)||[]).length%2===0,id+': Odd number of inline math delimiters');
 let depth=0;for(let i=0;i<s.length;i++){
  if(s[i]==='{'&&s[i-1]!=='\\')depth++;
  if(s[i]==='}'&&s[i-1]!=='\\')depth--;
  assert(depth>=0,id+': Unmatched closing curly brace');
 }
 assert(depth===0,id+': Unmatched opening curly brace');
};
const list=[];
for(const id of ids){
 const dir=path.join('bank',id);
 const meta=JSON.parse(fs.readFileSync(path.join(dir,'meta.json'),'utf8'));
 const q=fs.readFileSync(path.join(dir,'question.tex'),'utf8');
 const s=fs.readFileSync(path.join(dir,'solution.tex'),'utf8');
 assert(meta.id===id,id+' wrong meta id');
 assert(meta.topic===topic[id[0]],id+' wrong topic');
 assert(meta.quality_status==='待独立复核',id+' falsely labelled expert-reviewed');
 assert(meta.tier==='advanced_composite',id+' invalid composite tier');
 assert(Array.isArray(meta.tags)&&meta.tags.length>=3,id+' fewer than three cross-domain tags');
 assert(meta.level>=4&&meta.estimated_minutes>=40,id+' level or duration below admission standard');
 assert(meta.title?.length>=12,id+' missing descriptive title');
 const qs=splitParts(q),ss=splitParts(s);
 for(let i=0;i<4;i++){
  assert(qs[i].number===i+1&&ss[i].number===i+1,id+' wrong part number');
  assert(qs[i].content.length>=18,id+' part '+(i+1)+' statement too short');
  assert(ss[i].content.length>=100,id+' part '+(i+1)+' detailed derivation missing');
 }
 checkMath(q,id+' question');checkMath(s,id+' solution');
 list.push({id,topic:meta.topic,title:meta.title,question_chars:q.length,solution_chars:s.length,subparts:4,review:'待独立复核'});
}
assert(list.length===40&&new Set(ids).size===40,'not exactly 40 unique models');
assert(new Set(list.map(x=>x.title)).size===40,'duplicated new titles');
const report={round:16,branch:'physics-round16-40-draft',draft_problems:40,
 question_subparts:160,answer_subparts:160,per_model_numeric_checks:0,
 independent_expert_review:'待独立复核',global_core_collision_review:'pending',
 mirror_sync:'pending',pdf_questions:'not built',pdf_solutions:'not built',
 status:'STRUCTURAL_ONLY_NOT_MERGEABLE',items:list};
process.stdout.write(JSON.stringify(report,null,2)+'\n');
