#!/usr/bin/env node
'use strict';
const fs=require('fs'),path=require('path');
const ranges={M:[137,143],E:[137,143],T:[130,136],W:[130,136],O:[126,131],Q:[126,131]};
const ids=Object.entries(ranges).flatMap(([p,[lo,hi]])=>Array.from({length:hi-lo+1},(_,i)=>p+String(lo+i).padStart(3,'0')));
const targeted={
 M137:['M134',/傅科摆|科里奥利|地面进动/],
 E137:['E133',/趋肤|皮肤深度|良导体的皮肤/],
 E138:['E131',/介质片.*电容|横向插入.*介质/],
 E143:['E136',/同轴传输线的分布电感|理想同轴传输线/],
 T130:['T127',/德拜固体|低温三次热容/],
 T132:['T125',/混合熵|双组分理想气体|Gibbs悖论/],
 W130:['W125',/两段不同密度弦|波幅反射|透射系数与能流守恒/],
 W134:['W128',/深水重力波|平方根色散/],
 O126:['O124',/布儒斯特角|Fresnel消反射/],
 O128:['O125',/高斯光束的瑞利|束腰远场发散/],
 O129:['O120',/迈克耳孙干涉仪|镜面平移.*条纹/],
 Q128:['Q123',/康普顿散射|反冲电子与经典极限/]
};
function ngram(s,n){s=s.replace(/[^\p{L}\p{N}]+/gu,'');const z=new Set();for(let i=0;i+n<=s.length;i++)z.add(s.slice(i,i+n));return z;}
function jaccard(x,y,n){const A=ngram(x,n),B=ngram(y,n);let hit=0;for(const a of A)if(B.has(a))hit++;return hit/(A.size+B.size-hit||1);}
const bank='bank',history=[],results=[];
for(const f of fs.readdirSync(bank)){
 if(!/^[METWOQ]\d{3}$/.test(f)||ids.includes(f))continue;
 const root=path.join(bank,f),meta=path.join(root,'meta.json'),q=path.join(root,'question.tex');
 if(!fs.existsSync(meta)||!fs.existsSync(q))continue;
 const m=JSON.parse(fs.readFileSync(meta,'utf8'));history.push({id:f,title:m.title||'',question:fs.readFileSync(q,'utf8')});
}
function must(ok,msg){if(!ok)throw Error(msg);}
let confirmed=0;
for(const id of ids){
 const root=path.join(bank,id);
 const m=JSON.parse(fs.readFileSync(path.join(root,'meta.json'),'utf8'));
 const question=fs.readFileSync(path.join(root,'question.tex'),'utf8');
 const prior=history.map(x=>({id:x.id,titleSimilarity:jaccard(m.title,x.title,2),questionSimilarity:jaccard(question,x.question,4)}));
 prior.sort((a,b)=>b.questionSimilarity-a.questionSimilarity);
 must(!prior.some(x=>x.questionSimilarity>=.88),id+': near-exact prior question body repetition');
 must(!prior.some(x=>x.titleSimilarity>=.92),id+': near-exact prior title repetition');
 const targetedInfo=targeted[id];
 if(targetedInfo){
  const [priorId,forbidden]=targetedInfo;
  must(!forbidden.test(m.title),id+': duplicated physics core model reintroduced');
  const old=history.find(x=>x.id===priorId);
  must(old,id+': prior comparison record unavailable');
  const questionSimilarity=jaccard(question,old.question,4);
  must(questionSimilarity<.72,id+' still substantially repeats '+priorId+' problem body');
  confirmed++;
 }
 results.push({id,title:m.title,nearest_prior_by_question:prior[0],curated_replacement_of:targetedInfo?.[0]||null});
}
must(ids.length===40&&confirmed===12,'expected 40 checked and 12 curated semantic repairs');
console.log(JSON.stringify({round:22,items:40,prior_item_count:history.length,curated_cross_round_duplicates_replaced:confirmed,near_exact_question_screen_passed:true,expert_semantic_review_done:false,items_summary:results},null,2));
