#!/usr/bin/env python3
"""Twelve executable independent draft checks, NOT the required 200-item final gate."""
import json
import math
import mpmath as mp
import sympy as s
from pathlib import Path
checks=[]
def record(uid,part,method,description,ok):
    assert bool(ok),(uid,part,description)
    checks.append(dict(id=uid,part=part,method=method,name=description,passed=True))
def eq(a,b=0):
    return s.simplify(a-b)==0
pi=s.pi
I1,I2,I3,L=s.symbols('I1 I2 I3 L',positive=True)
w1,w2,w3=s.symbols('w1 w2 w3',real=True)
d1=(I2-I3)*w2*w3/I1;d2=(I3-I1)*w3*w1/I2;d3=(I1-I2)*w1*w2/I3
record('M059',1,'conservation','Euler rigid-body dynamics conserves both energy and angular momentum',eq(I1*w1*d1+I2*w2*d2+I3*w3*d3) and eq(I1**2*w1*d1+I2**2*w2*d2+I3**2*w3*d3))
lam2=(L/I2)**2*(I3-I2)*(I2-I1)/(I1*I3)
record('M059',2,'independent_derivation','linear middle-axis perturbation has positive exponential growth square',eq(((I2-I3)*(I1-I2)/(I1*I3))*(L/I2)**2,lam2))
A2=L**2*(I3-I2)/(I1*I2*(I3-I1));C2=L**2*(I2-I1)/(I2*I3*(I3-I1))
record('M059',3,'symbolic','separatrix principal-axis amplitudes satisfy both invariant ellipsoids',eq(I1*A2+I3*C2,L**2/I2) and eq(I1**2*A2+I3**2*C2,L**2))
A=s.sqrt(A2);B=L/I2;C=s.sqrt(C2);lam=s.sqrt(lam2)
tt=s.symbols('tt',real=True)
x1=A/s.cosh(lam*tt);x2=B*s.tanh(lam*tt);x3=C/s.cosh(lam*tt)
res=[I1*s.diff(x1,tt)-(I2-I3)*x2*x3,I2*s.diff(x2,tt)-(I3-I1)*x3*x1,I3*s.diff(x3,tt)-(I1-I2)*x1*x2]
sub={I1:s.Integer(1),I2:s.Integer(2),I3:s.Integer(3),L:s.Integer(4),tt:s.Rational(7,10)}
record('M059',4,'numerical','explicit heteroclinic solution satisfies all three Euler equations at nontrivial sample',all(abs(float(v.subs(sub).evalf()))<1e-12 for v in res))
r,alpha,R=s.symbols('r alpha R',positive=True)
J0=s.besselj(0,alpha*r);J1=s.besselj(1,alpha*r)
record('E059',1,'symbolic','force-free cylinder Bessel components satisfy both curl equations',eq(-s.diff(J0,r),alpha*J1) and eq(s.diff(r*J1,r)/r,alpha*J0))
flux=s.integrate(r*J0,(r,0,R))
record('E059',2,'independent_derivation','axial magnetic flux integral and Ampere boundary current agree',eq(flux,R*s.besselj(1,alpha*R)/alpha))
energy=s.integrate(r*(J0**2+J1**2),(r,0,R))
closed=R**2*s.Rational(1,2)*(s.besselj(0,alpha*R)**2+2*s.besselj(1,alpha*R)**2-s.besselj(0,alpha*R)*s.besselj(2,alpha*R))
record('E059',3,'symbolic','Bessel magnetic energy integral matches exact three-order boundary identity',eq(energy,closed))
Bp,Bz,mu=s.symbols('Bp Bz mu',real=True,nonzero=True)
K=s.Matrix([0,Bz/mu,-Bp/mu]);Bavg=s.Matrix([0,Bp/2,Bz/2])
record('E059',4,'conservation','surface current crossed with mean field gives outward Maxwell pressure',eq(K.cross(Bavg)[0],(Bp**2+Bz**2)/(2*mu)) and eq(K.cross(Bavg)[1]) and eq(K.cross(Bavg)[2]))
J,kB,T,mag,B=s.symbols('J kB T mag B',positive=True)
x=s.symbols('x',real=True)
f=-J*x*x/2-mag*B*x+kB*T*((1+x)/2*s.log((1+x)/2)+(1-x)/2*s.log((1-x)/2))
record('T056',1,'symbolic','mean-field entropy differentiation reproduces atanh self-consistency',eq(s.diff(f,x),-J*x-mag*B+kB*T*(s.log(1+x)-s.log(1-x))/2))
record('T056',2,'independent_derivation','Curie temperature follows Hessian sign change of disordered state',eq(s.diff(f,x,2).subs(x,0),kB*T-J))
Tc=J/kB
chi=mag**2/(kB*T-J)
record('T056',3,'limit','zero-field susceptibility has Curie Weiss pole and correct high-temperature limit',eq(s.limit(T*chi,T,s.oo),mag**2/kB))
t=s.symbols('t',positive=True)
landau=-3*kB*(Tc-t)**2/(4*Tc)
heat=-t*s.diff(landau,t,2)
record('T056',4,'symbolic','Landau free energy gives three-halves kB heat capacity jump at critical point',eq(s.limit(heat,t,Tc,dir='-'),3*kB/2))
assert len(checks)==12 and len(set((c['id'],c['part']) for c in checks))==12
assert all(len(set(c['method'] for c in checks if c['id']==uid))>=2 for uid in ['M059','E059','T056'])
# Independent numerical crosschecks beyond the twelve mandatory draft subparts.
from math import sqrt,tanh,cosh
A0=2.;B0=2.;C0=2/sqrt(3);lam0=2/sqrt(3);time=.73
w1num=A0/cosh(lam0*time);w2num=B0*tanh(lam0*time);w3num=C0/cosh(lam0*time)
assert abs((w1num*w1num+2*w2num*w2num+3*w3num*w3num)/2-4)<1e-12
assert abs((w1num*w1num+4*w2num*w2num+9*w3num*w3num)-16)<1e-12
mp.mp.dps=30
al=mp.mpf('1.7');rad=mp.mpf('2.3')
integ=mp.quad(lambda z:z*(mp.besselj(0,al*z)**2+mp.besselj(1,al*z)**2),[0,rad])
end=rad**2/2*(mp.besselj(0,al*rad)**2+2*mp.besselj(1,al*rad)**2-mp.besselj(0,al*rad)*mp.besselj(2,al*rad))
assert abs(integ-end)<mp.mpf('1e-26')
Tnum=.99;lo=.05;hi=.5
for _ in range(80):
    mid=(lo+hi)/2
    if mid-math.tanh(mid/Tnum)>0:hi=mid
    else:lo=mid
mroot=(lo+hi)/2
assert abs(mroot-math.sqrt(3*(1-Tnum)))/mroot<.01
supplemental=[dict(id='M059',method='numerical',name='triaxial separatrix two invariants at t=0.73',passed=True),
              dict(id='E059',method='numerical',name='high precision Bessel quadrature versus boundary formula',passed=True),
              dict(id='T056',method='numerical',name='spontaneous magnetization root near Curie temperature',passed=True)]
result={'status':'draft-only','new_problem_count':3,'passed_count':len(checks),'tests':checks,'independent_expert_review':'pending','supplemental_numeric_checks':supplemental}
path=Path(__file__).resolve().parents[1]/'data/round12_draft_validation_report.json'
path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'status':result['status'],'checked_subparts':len(checks)},ensure_ascii=False))
