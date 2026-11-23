"""Structural gate and numerical regressions; not independent academic review."""
from pathlib import Path
import re
import math
root=Path(__file__).resolve().parent
main=(root/'main.tex').read_text(encoding='utf-8')
refs=re.findall(r'\\input\{(chapters/[^}]+)\}',main)
assert refs and len(refs)==len(set(refs))
assert {root/(x+'.tex') for x in refs}==set((root/'chapters').glob('*.tex'))
seen=set()
counts={}
for ref in refs:
    source=(root/(ref+'.tex')).read_text(encoding='utf-8')
    book=Path(ref).name.split('-')[0]
    blocks=re.split(r'\\sourceproblem\{([^}]+)\}\{(\d+)\}\{(\d+)\}',source)
    assert len(blocks)>1 and (len(blocks)-1)%4==0,ref
    for i in range(1,len(blocks),4):
        number,printed,pdf,body=blocks[i:i+4]
        key=(ref,number)
        assert key not in seen,key
        seen.add(key)
        assert int(pdf)-int(printed)=={'tjut':6,'hust':4,'czu':6}[book],key
        for macro in ('problemtext','workings','crosscheck'):
            assert body.count('\\'+macro)==1,(key,macro)
        counts[book]=counts.get(book,0)+1
assert all(counts.get(k,0)>=v for k,v in {'tjut':5,'hust':5,'czu':8}.items())
assert math.isclose((0.5*2**2+3*2-4)-(0.5+3-4),4.5)
assert math.isclose(5*2**4/12,5*(1.5*2**2)**2/27)
assert math.isclose(math.hypot(8,2),2*math.sqrt(17))
assert math.isclose(math.hypot(-135/2,135*(1-math.cos(math.pi/6))),270*math.sin(math.pi/12))
assert math.isclose((720/11)*(1/60-1/720),1)
assert abs(1-5)+abs(2-1)==5
print('Structural and selected numerical checks passed:',counts)
