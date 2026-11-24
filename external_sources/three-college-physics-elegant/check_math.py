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
assert counts=={'tjut':296,'hust':156,'czu':384},counts
assert math.isclose((0.5*2**2+3*2-4)-(0.5+3-4),4.5)
assert math.isclose(5*2**4/12,5*(1.5*2**2)**2/27)
assert math.isclose(math.hypot(8,2),2*math.sqrt(17))
assert math.isclose(math.hypot(-135/2,135*(1-math.cos(math.pi/6))),270*math.sin(math.pi/12))
assert math.isclose((720/11)*(1/60-1/720),1)
assert abs(1-5)+abs(2-1)==5
assert 15+15*math.pi/2 < 80 < 15+45*math.pi/2
assert math.isclose(50**2/30,250/3)
assert 10*4+2*4**3==168
assert math.isclose(0.5*600*(600/200000),0.9)
assert math.isclose((math.cos(math.pi/3)/math.cos(math.pi/4))**2,0.5)
assert 25*(4-1)+10*(8-1)==145
assert 3*4**2/2==24
assert math.isclose(8.10*6817/8762,6.301951609221638,rel_tol=1e-10)
assert 4*8+3*6==50
assert math.isclose((4*4-3*4**2+4**3-(4*2-3*2**2+2**3))/2,14)
assert math.hypot(40,30)==50
assert math.isclose((3100-10-500)/200+0.1+5,18.05)
assert math.isclose((48.96*0.02-0.00392)*0.02/0.008,2.4382)
assert math.isclose(1+1/4+1/8,11/8)
assert math.isclose(0.5*2*(6*math.pi)**2-0.5*6*(2*math.pi)**2,24*math.pi**2)
assert math.isclose(0.1*(12*2**2)**2,230.4)
assert math.isclose(2**4/16,2/2)
assert 3*2**2+2==14
assert math.isclose((3-1)/(14+1+9),1/12)
assert math.isclose((10*1-6*0.5)/8,0.875)
assert math.isclose(400*math.sqrt(0.2/9.8),57.14285714285714)
assert math.isclose(60*math.sqrt(2*180/10),360)
assert math.isclose(0.55*(1000/1.10),500)
assert math.isclose(4*(7*math.pi/24)-2*math.pi/3,math.pi/2)
assert math.isclose(6*2*math.pi/4,3*math.pi)
eta=math.pi*(5e-4)**4*1900**2*9.8*0.05*60/(8*0.1*6.54e-4)
assert 0.039 < eta < 0.041
assert math.isclose(1050*0.5*0.004/3.00e-3,700)
assert math.isclose(1050*0.5**2/2,131.25)
assert math.isclose(6+6*3**2+4*3,72)
assert -10+6+2+2==0
assert math.isclose((19*math.pi/12)/(math.pi/4),19/3)
assert math.isclose(math.hypot(3,4),5)
assert math.isclose(100*math.sqrt(1-0.8**2),60)
assert math.isclose(1.25*(12.5-0.6*10.25/0.3),-10)
assert math.isclose((3*3+3**2)/10,1.8)
assert math.isclose(3*3+2*3**2,27)
assert math.isclose(10/8,1.25)
assert math.isclose((-1/7)**2+(4*math.sqrt(3)/7)**2,1)
assert math.isclose(math.sqrt(1.511**2-0.511**2),math.sqrt(2.022))
assert 17**2-15**2==8**2
assert math.isclose(3/4+1/6,11/12)
assert math.isclose(math.tanh(math.log(3)/2),0.5)
assert math.isclose(2*(1-2/3),2/3)
assert math.isclose(2*3/math.sqrt(5),6/math.sqrt(5))
assert math.isclose(100/math.sqrt(5)/(2*3e8/math.sqrt(5)),5e-7/3)
assert math.isclose(1-1/math.sqrt(1+3),0.5)
assert math.isclose(2/9-(2/3)**2/4,1/9)
assert math.isclose(1/3-1/4,1/12)
assert math.isclose(2.5*math.log(7),4.864775372638283)
z=0.03*60/(45*9.8)
assert math.isclose(45/0.03*math.log1p(z),6.109988081453729,rel_tol=1e-10)
assert math.isclose(45*60/0.03-45**2*9.8/0.03**2*math.log1p(z),183.17520263018378,rel_tol=1e-9)
assert math.isclose(8e-9/4e-9,2)
assert math.isclose(3.2e-15/1.6e-19,2e4)
assert -50*2-20*2==-140
assert math.isclose(6/0.05-60,60)
assert math.isclose(6/0.20-60,-30)
assert math.isclose((0.05*(-1e-5)+0.07*3e-5)/2,8e-7)
assert math.isclose(5*3/8,3*5/8)
assert math.isclose(0.020*(500-50),9)
assert 5*((16**2+16**2)-(4**2+16**2))==1200
assert math.isclose(200*(6.4e6)**2/9e9,9.102222222222222e5)
assert math.isclose(2*math.pi*8.854e-12*0.01*3e6,1.6689396813775216e-6,rel_tol=1e-4)
R1, r, R2 = 1.0, 1.5, 1.8
assert r/(2*R1)<1
assert math.isclose(r*(math.log(r/R1)/2+math.log(R2/r)),r/2*math.log(R2**2/(r*R1)))
assert math.isclose(0.020*500/50-0.020,0.18)
assert 6*3**2==54
assert 150000*180/(0.5*(20**2-10**2))==180000
assert 3*3+3**2==18
assert math.isclose(math.sqrt(3/4)**2/2,3/8)
assert math.isclose(1/(1/4+1/6)*200,480)
assert math.isclose(2*480/(4+6),96)
assert math.isclose((1.75**2+(1.5*math.sqrt(3)/2)**2+1.5**2)/2,3.5)
assert not math.isclose(3.5,2.5**2/2)
assert math.isclose(2.5*math.cos(math.pi/3),1.25)
assert math.isclose(50000*((30000*2+50000)/80000-1),18750)
assert math.isclose(2.5*2-2**3/3,7/3)
assert math.isclose(10*10-0.2*10**2/2,90)
assert (16-9)-(4+9)==-6
assert 1.5*(19**2-3**2)==528
assert math.isclose(2e-7*5000/25,4e-5)
assert (1/2)*4*2==4
assert math.isclose(2*0.4*0.3,0.24)
assert math.isclose(120*0.0079*735/60,11.613)
assert math.isclose(0.5*(1-0.25),3/(16*math.pi)*2*math.pi)
assert math.isclose(1/(2*(3/(16*math.pi))*2*math.pi),4/3)
assert math.isclose((0.5-0.25)/(0.5+0.25),1/3)
assert math.isclose((3/5)*8.9875517923e9*(1.602176634e-19)**2/1.0e-15,1.3842465e-13,rel_tol=1e-3)
assert math.isclose(4*math.pi*1e-7*10/(4*math.pi),1e-6)
assert math.isclose(2*math.pi*0.04*15.8*0.10*math.cos(math.pi/3),0.198548655706875,rel_tol=1e-8)
assert math.isclose(1/12+2*(1/2)**2,7/12)
assert math.isclose(math.sqrt(3*10/(2*(5/3))),3)
assert math.isclose(0.5*((0.5)**2-1),-3/8)
assert math.log1p(1)>1/2
assert math.isclose((30**2-20**2)*math.pi/(2*120),25*math.pi/12)
assert math.isclose(10*math.pi/(25*math.pi/12),4.8)
assert math.isclose(5*100-0.025*100**2,250)
assert math.isclose(1450*0.1/0.29,500)
assert math.isclose(200*0.1/0.1,200)
assert math.isclose(500*0.6**2*220/30,1320)
assert math.isclose(0.25**2,1/16)
assert math.isclose(10e-6*2e5,2)
assert math.isclose(0.5-4/9*(1/18+1/4),59/162)
assert math.isclose((59/162)/(5/9),59/90)
assert math.isclose(8*10/(8+16/2),5)
aa=(150-3*math.sqrt(3))/25
assert math.isclose(180-18*aa-(6*aa+30+3*math.sqrt(3)),aa)
assert math.isclose(1-3/4,1/4)
assert math.isclose(4000*5e-5*math.pi*.12**2*60*math.pi,1.7054676405082415,rel_tol=1e-3)
assert math.isclose(600e-9/3e-4,0.002)
assert math.isclose((1.33-1)*5.5e-6/600e-9,3.025)
assert math.isclose(math.atan(math.sqrt(3))-math.atan(1/math.sqrt(3)),math.pi/6)
assert math.isclose(0.1*0.2**2,0.004)
assert math.isclose(0.004/2*0.5,0.001)
Ja=5000/((800/60)*((800-250)/60))
assert math.isclose(Ja,450/11)
assert math.isclose(2.2*Ja,90)
assert math.isclose(3*9.8*math.sin(math.pi/6)/0.4,36.75)
for M,m in [(1,1),(6,1),(3,1)]:
    v=(3*m-M)/(3*m+M)
    w=6*m/(3*m+M)
    assert math.isclose(m*v+M*w/3,m)
    assert math.isclose(m*v*v+M*w*w/3,m)
assert math.isclose(2*1.33*380/1.5,673.8666666666667)
assert math.isclose(5.5*550/(2*1.5),1008.3333333333334)
assert math.isclose(4e-3*0.3e-3/(2*600e-9),1)
assert math.isclose(3*400/2,600)
assert math.isclose(2*200*4*math.pi*1e-7*4000*3e-4,0.0006031857894892404)
assert math.isclose(1.84*(0.61/1.22)**2,0.46)
assert math.isclose(2*50*1.5*10/25,60)
assert math.isclose(600*0.25**2/2*30*math.pi/25,22.5*math.pi)
assert math.isclose(30*math.pi*(22.5*math.pi)/(4*math.pi),168.75*math.pi)
assert math.isclose(2*600e-9/0.2e-3,0.006)
assert sum(abs(k)<2.5 for k in range(-10,11))==5
assert math.isclose(3*560/4,420)
assert math.isclose(2e-3*3e-4/(2*600e-9),0.5)
assert math.isclose(math.cos(math.pi/6)**2/math.cos(math.pi/4)**2,1.5)
assert math.isclose((1.30e7-1.0e6)*0.032/(1.01e5*0.4),9.504950495049505)
assert math.isclose(2000/math.sqrt(32/2),500)
assert math.isclose(2*675/(5*2e-3),135000)
assert math.isclose((1.5*5/2-3)/3,0.25)
assert math.isclose(9e9*1e-8/0.3**2,1000)
assert math.isclose(0.5*math.cos(math.pi/4)**2*math.sin(math.pi/4)**2,1/8)
assert math.isclose(math.atan(1.6)+math.atan(1/1.6),math.pi/2)
assert math.isclose(0.1/0.01*200**2/3,400000/3)
assert math.isclose((3/8+1/2)/(1/2+1),7/12)
assert math.isclose((1/4+7/3)/(2*(1/2+1)),31/36)
cycle=[(0,50,50),(-50,50,0),(-100,-50,-150),(150,0,150)]
assert all(u+w==q for u,w,q in cycle)
assert sum(u for u,w,q in cycle)==0
assert sum(w for u,w,q in cycle)==sum(q for u,w,q in cycle)==50
assert math.isclose(sum(w for u,w,q in cycle)/sum(max(q,0) for u,w,q in cycle),0.25)
assert math.isclose(2e-8/5e-9,4)
assert math.isclose(2*1.96e24,3.92e24)
assert math.isclose(5/3*2/3,10/9)
assert math.isclose(0.1*32/2,1.6)
T=6e-21/(1.5*1.38e-23)
m=(4.9e6-2/.028*2.5*8.31*T)/(1.5*8.31*T)*.04
assert math.isclose(m,49.48598934158501)
assert math.isclose(2.76e5*.75/(5e25*1.38e-23),300)
assert math.isclose(1-300/400,0.25)
assert 200*600*9==1080000
assert (300-100)*30==6000
S1=.5*335e3/273.15
S2=.5*4180*math.log(293.15/273.15)
SH=-(.5*335e3+.5*4180*20)/293.15
assert math.isclose(S1+S2+SH,46.93358042197235)
assert (12*2*3-6,6*2**2+14*3)==(66,66)
assert math.isclose(9e9*(1.6e-19)**2/(5.29e-11)**2,8.233246736539676e-8)
assert math.isclose(2/7/(2/5),5/7)
assert 826-500==326
assert math.isclose(1.5*10*8.31-209,-84.35)
assert (40-10)*(4-1)==90
assert (80-30)+10==60
assert -(80-30)-20==-70
assert math.isclose(500*(0.1+math.hypot(.02,.04)),72.3606797749979)
assert math.isclose((math.pi/3)/(math.pi/2),2/3)
assert math.isclose(.0565*math.sqrt(2)*math.cos(9*math.pi/4),.0565)
assert math.isclose(1/(1/(math.sqrt(3)-1))**2,3/(1+1/(math.sqrt(3)-1))**2)
assert math.isclose(4*math.pi*8.8541878128e-12*.2*300,6.675900332687222e-9,rel_tol=1e-6)
assert math.isclose(2*2.5*8.31*50,2077.5)
assert (400-200)==200
cyc=[(300,0,300),(300,200,500),(-450,0,-450),(-150,-100,-250)]
assert all(u+w==q for u,w,q in cyc)
assert sum(u for u,w,q in cyc)==0
assert math.isclose(sum(w for u,w,q in cyc)/sum(max(q,0) for u,w,q in cyc),0.125)
assert math.isclose(100*(1+0.6)/math.sqrt(1-0.6**2),200)
assert math.isclose(0.4*10**2/2,20)
assert math.isclose(math.atan2(10,10*math.sqrt(3)-17.3)*180/math.pi,89.882519180084,rel_tol=1e-5)
assert math.isclose((6e-5-4.5e-5)/(3e-9*0.05),1e5)
assert math.isclose(4/math.hypot(4,3)-1/4,0.55)
print('Structural and selected numerical checks passed:',counts)
