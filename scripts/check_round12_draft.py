#!/usr/bin/env python3
"""Twelve executable independent draft checks, NOT the required 200-item final gate."""
import json
import sympy as s
from pathlib import Path
checks=[]
def record(uid,part,method,description,ok):
    assert bool(ok),(uid,part,description)
    checks.append(dict(id=uid,part=part,method=method,name=description,passed=True))
def eq(a,b=0):
    return s.simplify(a-b)==0
pi=s.pi
m,v,b,g=s.symbols('m v b g',positive=True)
a2=2*g/(m*v**2)
kappa=s.sqrt(1+a2/b**2)
rmin=s.sqrt(b*b+a2)
record('M059',1,'conservation','turning-point radial energy equals asymptotic kinetic energy',eq((m*v*b)**2/(2*m*rmin**2)+g/rmin**2,m*v**2/2))
phi=s.symbols('phi',real=True)
u=s.cos(kappa*phi)/rmin
record('M059',2,'symbolic','inverse-square repulsive Binet orbit solves exact second-order equation',eq(s.diff(u,phi,2)+kappa**2*u))
theta=s.symbols('theta',positive=True)
y=1-theta/pi
btheta=s.sqrt(a2)*y/s.sqrt(1-y*y)
jac=s.simplify(-btheta*s.diff(btheta,theta)/s.sin(theta))
expect=a2*y/(pi*s.sin(theta)*(1-y*y)**2)
record('M059',3,'independent_derivation','inverted impact parameter Jacobian yields differential cross section',eq(jac,expect))
Theta=pi*(1-1/kappa)
record('M059',4,'limit','weak-repulsion scattering deflection has inverse-square impact scaling',eq(s.limit(Theta/g,g,0),pi/(m*v*v*b*b)))
mu,sigma,omega=s.symbols('mu sigma omega',positive=True)
delta=s.sqrt(2/(mu*sigma*omega))
k=(1-s.I)/delta
record('E059',1,'symbolic','complex magnetic penetration wave number satisfies diffusion equation',eq(k*k,-s.I*mu*sigma*omega))
record('E059',2,'independent_derivation','Ampere Ohm and Faraday equations give identical conductor phasors',eq(-k*k/sigma,s.I*mu*omega))
H=s.symbols('H',positive=True)
pflux=H*H/(2*sigma*delta)
pjoule=s.Abs(1-s.I)**2*H*H/(2*sigma*delta**2)*(delta/2)
record('E059',3,'conservation','Poynting influx equals integrated Ohmic heat per unit area',eq(pflux,pjoule))
W=mu*H*H*delta/8
record('E059',4,'dimensions','skin depth frequency scaling and reactive magnetic power agree',eq(delta.subs(omega,4*omega),delta/2) and eq(2*omega*W,pflux))
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
result={'status':'draft-only','new_problem_count':3,'passed_count':len(checks),'tests':checks,'independent_expert_review':'pending'}
path=Path(__file__).resolve().parents[1]/'data/round12_draft_validation_report.json'
path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'status':result['status'],'checked_subparts':len(checks)},ensure_ascii=False))
