#!/usr/bin/env node
'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const ranges={M:[130,136],E:[130,136],T:[123,129],W:[123,129],O:[120,125],Q:[120,125]};
const subjects={M:'力学',E:'电磁学',T:'热学',W:'振动与波动',O:'光学',Q:'近代物理'};
const ids=Object.entries(ranges).flatMap(([p,[a,b]])=>Array.from({length:b-a+1},(_,i)=>p+String(a+i).padStart(3,'0')));
function must(ok,msg){if(!ok)throw Error(msg);}
function parts(s,id,kind){
 const matches=[...s.matchAll(/^\(([1-4])\)\s/gm)];
 must(matches.length===4,id+': '+kind+' must contain four numbered sections');
 return matches.map((m,i)=>{must(Number(m[1])===i+1,id+': section order');return s.slice(m.index+m[0].length,matches[i+1]?.index??s.length).trim();});
}
function tex(s,id){
 must(!/\\(?:input|include|write18|openout|documentclass|catcode|begin\{document\})/.test(s),id+': unsafe embedded TeX');
 must((s.match(/(?<!\\)\$/g)||[]).length%2===0,id+': unmatched $');
 let depth=0;for(let i=0;i<s.length;i++){if(s[i]==='{'&&s[i-1]!=='\\')depth++;if(s[i]==='}'&&s[i-1]!=='\\')depth--;must(depth>=0,id+': closing brace');}must(depth===0,id+': opening brace');
 must(!/\\(?:begin|end)\{(?!(?:array|align|aligned|gather|gathered|cases|pmatrix|bmatrix|matrix|equation|split)\b)/.test(s),id+': unusual math environment requires manual review');
}
function grams(s){s=s.replace(/[^\p{L}\p{N}]+/gu,'');const v=new Set();for(let i=0;i<s.length-1;i++)v.add(s.slice(i,i+2));return v;}
function jac(a,b){const A=grams(a),B=grams(b);let hit=0;for(const x of A)if(B.has(x))hit++;return hit/(A.size+B.size-hit||1);}
const history=[];
for(const name of fs.readdirSync('bank')){if(!/^[METWOQ]\d{3}$/.test(name)||ids.includes(name))continue;const f=path.join('bank',name,'meta.json');if(fs.existsSync(f)){const m=JSON.parse(fs.readFileSync(f,'utf8'));history.push({id:name,title:m.title||'',tags:m.tags||[]});}}
const newItems=[],usedTitles=new Set(),usedQ=new Set(),allErrors=[];
for(const id of ids){
 const dir=path.join('bank',id),m=JSON.parse(fs.readFileSync(path.join(dir,'meta.json'),'utf8'));
 const q=fs.readFileSync(path.join(dir,'question.tex'),'utf8'),s=fs.readFileSync(path.join(dir,'solution.tex'),'utf8');
 must(m.id===id&&m.topic===subjects[id[0]],id+': wrong id or subject');
 must(m.quality_status==='待独立复核'&&m.tier==='advanced_composite',id+': misleading review label');
 must(m.level===5&&Number.isInteger(m.estimated_minutes)&&m.estimated_minutes>=40,id+': level / time gate');
 must(Array.isArray(m.tags)&&m.tags.length>=3,id+': tags');
 must(m.kind==='综合推导题'&&m.format==='latex-fragment-v1',id+': format');
 must(!usedTitles.has(m.title)&&!history.some(x=>x.title===m.title),id+': historical or new exact title collision');usedTitles.add(m.title);
 const normalized=q.replace(/\s+/g,'');must(!usedQ.has(normalized),id+': repeated exact question');usedQ.add(normalized);
 tex(q,id+' question');tex(s,id+' solution');
 const qs=parts(q,id,'question'),ss=parts(s,id,'solution');
 for(let j=0;j<4;j++){must(qs[j].length>=12,id+': short stem part '+(j+1));must(ss[j].length>=90,id+': short solution part '+(j+1));must(/[\\$]/.test(ss[j]),id+': no mathematical formula in solution part '+(j+1));}
 const nearest=history.map(h=>({id:h.id,title:h.title,similarity:jac(m.title,h.title)})).sort((a,b)=>b.similarity-a.similarity)[0];
 newItems.push({id,title:m.title,topic:m.topic,question_parts:qs.length,solution_parts:ss.length,question_chars:q.length,solution_chars:s.length,historical_nearest_title:nearest,source_sha256:crypto.createHash('sha256').update(q+'\n'+s).digest('hex')});
}
must(newItems.length===40&&new Set(ids).size===40,'expected 40 distinct items');
const counts={};for(const it of newItems)counts[it.topic]=(counts[it.topic]||0)+1;
must(Object.entries(subjects).every(([p,t])=>counts[t]===ranges[p][1]-ranges[p][0]+1),'category coverage');
const near=newItems.filter(x=>x.historical_nearest_title?.similarity>=0.36);
process.stdout.write(JSON.stringify({round:21,status:'DRAFT_PENDING_INDEPENDENT_REVIEW',checked_source_triples:40,question_parts:160,solution_parts:160,historical_titles_screened:history.length,nearest_title_manual_review_candidates:near,review_status:'待独立复核',counts,items:newItems},null,2)+'\n');
