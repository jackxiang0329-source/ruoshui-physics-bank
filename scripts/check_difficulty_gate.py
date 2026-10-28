#!/usr/bin/env python3
"""Reject unqualified basic physics questions."""
from pathlib import Path
import json,re,sys
root=Path(__file__).resolve().parents[1];errors=[]; seen=set(); files=sorted((root/'bank').glob('*/meta.json'))
if not files: errors.append('empty active bank')
for f in files:
 p=json.loads(f.read_text(encoding='utf-8'));id=p.get('id','?')
 if id in seen or f.parent.name!=id: errors.append(id+': invalid ID')
 seen.add(id)
 if p.get('tier')!='advanced_composite' or p.get('level') not in (4,5): errors.append(id+': advanced level required')
 if not isinstance(p.get('estimated_minutes'),int) or p['estimated_minutes']<40: errors.append(id+': 40 minutes required')
 if len(p.get('tags',[]))<3: errors.append(id+': 3 topics required')
 if p.get('kind') in ('选择题','填空题'): errors.append(id+': basic format excluded')
 q=f.parent/'question.tex';s=f.parent/'solution.tex'
 if not q.exists() or not s.exists(): errors.append(id+': TeX missing');continue
 if len(re.findall(r'\([1-9]\)',q.read_text(encoding='utf-8')))<4: errors.append(id+': >=4 subproblems required')
 if len(s.read_text(encoding='utf-8'))<400: errors.append(id+': detailed derivation required')
 if p.get('quality_status')=='质检通过': errors.append(id+': independent signoff evidence not established')
master=root/'data/problems.json'
if master.exists() and {v['id'] for v in json.loads(master.read_text(encoding='utf-8'))}!=seen:errors.append('data mirror mismatch')
for e in errors:print('REJECT:',e,file=sys.stderr)
print('advanced:',len(files),'errors:',len(errors))
sys.exit(bool(errors))
