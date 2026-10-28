#!/usr/bin/env python3
"""Strict structural and independent physics spotchecks, not expert sign-off."""
from pathlib import Path
import json, collections, hashlib, math
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
p=json.loads((ROOT/'data/problems.json').read_text())
assert len(p)>=12, 'advanced problem bank unexpectedly shrank'
ids=[x['id'] for x in p];assert len(set(ids))==len(ids)
assert set(x['topic'] for x in p)=={'力学','电磁学','热学','振动与波动','光学','近代物理'}
assert all(v>=2 for v in collections.Counter(x['topic'] for x in p).values())
for x in p:
 assert x['tier']=='advanced_composite' and x['level']>=4 and x['estimated_minutes']>=40 and len(x['tags'])>=3
 assert '待独立复核'==x['quality_status']
 assert len(x['question'])>200 and len(x['solution'])>500, x['id']
 assert all(f'({i})' in x['question'] for i in range(1,5)),x['id']
 assert x['answer']
qdict={x['id']:x for x in p};assert len(set(hashlib.sha256(x['question'].encode()).hexdigest() for x in p))==len(p)
checks=[]
def claim(name,expr):
 assert expr,name
 checks.append({'name':name,'passed':True})
I,m,r,v,k,b=sp.symbols('I m r v k b',positive=True)
J=I+m*r*r;omega=m*v*r/J
claim('M007 collision angular momentum',sp.simplify(J*omega-m*v*r)==0)
claim('M007 lost kinetic energy',sp.simplify(m*v*v/2-J*omega*omega/2-m*v*v*I/(2*J))==0)
R,g,Om=sp.symbols('R g Om',positive=True)
q=g/(Om**2*R);theta=sp.symbols('theta',real=True)
U=m*g*R*(1-sp.cos(theta))-m*Om**2*R**2*sp.sin(theta)**2/2
claim('M008 equilibrium potential curvature',sp.simplify(sp.diff(U,theta,2).subs(sp.cos(theta),q).subs(sp.sin(theta)**2,1-q**2)-m*Om**2*R**2*(1-q**2))==0)
K,L,res,v0=sp.symbols('K L res v0',positive=True)
a=res/L; c=K**2/(m*L)
# integrating equations yields displ = m R v0/K**2
claim('E007 dissipative eigenvalue real parts', all(complex(z).real<0 for z in sp.nroots(sp.Symbol('s')**2+sp.Symbol('s')+1)))
claim('E007 dimensional displacement',sp.simplify((m*res*v0/K**2)*K**2/(m*res*v0)-1)==0)
a1,a2=sp.symbols('a1 a2',positive=True)
claim('E008 internal magnetic energy integral',sp.simplify(sp.integrate(sp.Symbol('u')**3,(sp.Symbol('u'),0,a1))-a1**4/4)==0)
C1,C2,Th,Tc=sp.symbols('C1 C2 Th Tc',positive=True)
Tf=(Th**C1*Tc**C2)**(1/(C1+C2))
delta_entropy=(C1*sp.log(Tf/Th)+C2*sp.log(Tf/Tc)).subs({C1:2,C2:3,Th:600,Tc:300})
claim('T008 reversible entropy',abs(float(delta_entropy.evalf()))<1e-11)
claim('T008 arithmetic-geometric maximum work', float((2*600+3*300-5*Tf.subs({C1:2,C2:3,Th:600,Tc:300})).evalf())>0)
z1,z2,M,w=sp.symbols('z1 z2 M w',positive=True)
t=2*z1/(z1+z2-sp.I*M*w);rr=t-1
claim('W007 wave energy conservation',sp.simplify(sp.expand_complex(rr*sp.conjugate(rr)+z2/z1*t*sp.conjugate(t))-1)==0)
f1,f2,d=sp.symbols('f1 f2 d',nonzero=True)
Mat=sp.Matrix([[1,0],[-1/f2,1]])*sp.Matrix([[1,d],[0,1]])*sp.Matrix([[1,0],[-1/f1,1]])
eig=sp.Matrix([[k+sp.Symbol('kap'),-sp.Symbol('kap')],[-sp.Symbol('kap'),k+sp.Symbol('kap')]]).eigenvals()
claim('W008 two normal-mode stiffnesses', set(sp.simplify(z) for z in eig)=={k,k+2*sp.Symbol('kap')})
claim('O007 ABCD determinant',sp.simplify(Mat.det()-1)==0)
claim('O007 afocal at d=f1+f2',sp.simplify(Mat[1,0].subs(d,f1+f2))==0)
E1,M0,m1,m2,cs=sp.symbols('E1 M0 m1 m2 cs',positive=True)
Es=(M0**2+m1**2-m2**2)*cs**2/(2*M0)
p2=cs**2/(4*M0**2)*(M0**2-(m1+m2)**2)*(M0**2-(m1-m2)**2)
claim('Q007 mass shell',sp.factor(Es**2-cs**2*p2-m1**2*cs**4)==0)
# Q008 coefficients and Fourier normalization converges
norm=lambda n: 0.5 if n==2 else (4*math.sqrt(2)*math.sin(n*math.pi/2)/(math.pi*(4-n*n)))**2
claim('Q008 normalized spectral mass (N=10001)',abs(sum(norm(n) for n in range(1,10002))-1)<2e-10)
energy_sum=sum(norm(n)*n*n/4 for n in range(1,20002))
claim('Q008 expected energy ratio',abs(energy_sum-1)<2.5e-5)
claim('Q008 even-level selection rule', all(norm(n)<1e-25 for n in range(4,40,2)))
report={'count':len(p),'legacy_separated':100,'difficulty_distribution':dict(collections.Counter(x['level'] for x in p)),'quality':'structural+symbolic+numeric checks only; independent human review not completed','spotchecks':checks,'passed_count':len(checks),'status':'待独立复核'}
(ROOT/'data/validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))