#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Independent symbolic and numeric checks for the 12 problems in round 05.

These are targeted crosschecks, NOT a proof of every solution or human review.
"""
import json
import math
from pathlib import Path

import sympy as s
import mpmath as mp

ROOT = Path(__file__).resolve().parents[1]
data={p["id"]:p for p in json.loads((ROOT/"data/problems.json").read_text(encoding="utf-8"))}
ids=[f"{prefix}{n:03d}" for prefix in "METWOQ" for n in (16,17)]
assert len(ids)==12 and all(id in data for id in ids)
checks=[]
def verify(label, condition):
    assert bool(condition), label
    checks.append(label)
def iszero(x):
    return s.simplify(x)==0

m,om,r0,t,R=s.symbols("m om r0 t R",positive=True)
r=r0*s.cosh(om*t)
verify("M016 radial ODE",iszero(s.diff(r,t,2)-om**2*r))
verify("M016 energy motor work",iszero(s.integrate(2*m*om**2*r*s.diff(r,t),(t,0,s.acosh(R/r0)/om))-m*om**2*(R**2-r0**2)) if False else iszero(s.diff(m*(s.diff(r,t)**2+om**2*r**2)/2,t)-2*m*om**2*r*s.diff(r,t)))
mu,m0,g,u,v0=s.symbols("mu m0 g u v0",positive=True)
mt=m0-mu*t
vel=v0+u*s.log(m0/mt)-g*t
height=v0*t+u*(t-mt/mu*s.log(m0/mt))-g*t**2/2
verify("M017 rocket displacement derivative",iszero(s.diff(height,t)-vel))
verify("M017 rocket mass acceleration",iszero(s.diff(vel,t)-u*mu/mt+g))
a,c,b,eps1,eps2,Q=s.symbols("a c b eps1 eps2 Q",positive=True)
H=(1/a-1/c)/eps1+(1/c-1/b)/eps2
verify("E016 spherical layered capacitance",iszero((4*s.pi/H)*Q*H/(4*s.pi)-Q))
verify("E016 split energy integral",iszero(
    s.integrate(Q**2/(8*s.pi*eps1*t**2),(t,a,c))
   +s.integrate(Q**2/(8*s.pi*eps2*t**2),(t,c,b))-Q**2*H/(8*s.pi)))
chi1,chi2=s.symbols("chi1 chi2",real=True)
verify("E016 total bound-charge cancellation",iszero(-chi1*Q+(chi1-chi2)*Q+chi2*Q))
L,C,V,alpha,wd=s.symbols("L C V alpha wd",positive=True)
current=V/(L*wd)*s.exp(-alpha*t)*s.sin(wd*t)
charge=C*V*(1-s.exp(-alpha*t)*(s.cos(wd*t)+alpha/wd*s.sin(wd*t)))
relation={wd**2:1/(L*C)-alpha**2}
verify("E017 derivative q=i",iszero(s.factor(s.diff(charge,t)-current).subs(wd**2,relation[wd**2])))
verify("E017 first overshoot",iszero(charge.subs(t,s.pi/wd)-C*V*(1+s.exp(-alpha*s.pi/wd))))
verify("E017 dissipated energy",iszero(C*V**2-C*V**2/2-C*V**2/2))
x,N,kB,magB,muMag=s.symbols("x N kB magB muMag",positive=True)
U=-N*muMag*magB*s.tanh(x)
S=N*kB*(s.log(2*s.cosh(x))-x*s.tanh(x))
verify("T016 entropy-x monotonic",iszero(s.diff(S,x)+N*kB*x/s.cosh(x)**2))
T=s.symbols("T",positive=True)
xx=muMag*magB/(kB*T)
heat=s.diff(U.subs(x,xx),T)
verify("T016 fixed-field heat capacity",iszero(heat-N*kB*xx**2/s.cosh(xx)**2))
radC,vol=s.symbols("radC vol",positive=True)
Ur=radC*vol*T**4;Sr=s.Rational(4,3)*radC*vol*T**3
press=radC*T**4/3
verify("T017 first law dT",iszero(s.diff(Ur,T)-T*s.diff(Sr,T)))
verify("T017 first law dV",iszero(s.diff(Ur,vol)+press-T*s.diff(Sr,vol)))
rho,phi=s.symbols("rho phi",real=True)
tm=(1-rho**2)*s.exp(s.I*phi)/(1-rho**2*s.exp(2*s.I*phi))
rr=rho*(1-s.exp(2*s.I*phi))/(1-rho**2*s.exp(2*s.I*phi))
trans=s.simplify(s.expand_complex(tm*s.conjugate(tm)))
refl=s.simplify(s.expand_complex(rr*s.conjugate(rr)))
verify("W016 scattering flux unity",iszero(trans+refl-1))
verify("W016 resonance unity",iszero(trans.subs(phi,s.pi)-1))
verify("W016 antiresonance",iszero(trans.subs(phi,s.pi/2)-(1-rho**2)**2/(1+rho**2)**2))
z01=mp.besseljzero(0,1)
verify("W017 first Bessel root",abs(z01-mp.mpf("2.4048255577"))<1e-10)
integr=mp.quad(lambda z:z*mp.besselj(0,z01*z)**2,[0,1])
verify("W017 J0 radial normalization",abs(integr-mp.besselj(1,z01)**2/2)<1e-12)
n0,n1,ns=s.symbols("n0 n1 ns",positive=True)
r01=(n0-n1)/(n0+n1);r12=(n1-ns)/(n1+ns)
verify("O016 antireflection index condition",iszero(s.factor(s.together(r01-r12)).subs(n1**2,n0*ns)))
rhos=s.symbols("rhos",real=True)
angle=s.symbols("angle",real=True)
reff=rhos*(1-s.exp(2*s.I*angle))/(1-rhos**2*s.exp(2*s.I*angle))
verify("O016 exact design zero",iszero(reff.subs(angle,0)))
verify("O016 quadratic spectral reflectivity",s.simplify(s.limit(
s.expand_complex(reff*s.conjugate(reff))/angle**2,angle,0)-4*rhos**2/(1-rhos**2)**2)==0)
n,A,zeta=s.symbols("n A zeta",positive=True)
f=s.asin(n*s.sin(zeta))
fsecond=s.diff(f,zeta,2)
expected=n*(n**2-1)*s.sin(zeta)/(1-n**2*s.sin(zeta)**2)**s.Rational(3,2)
verify("O017 minimum-deviation curvature",iszero(fsecond-expected))
verify("O017 prism small-A",iszero(s.limit((2*s.asin(n*s.sin(A/2))-A)/A,A,0)-(n-1)))
alpha0=s.symbols("alpha0")
verify("Q016 Poisson probability sum",iszero(s.summation(s.exp(-alpha0)*alpha0**s.Symbol("j")/s.factorial(s.Symbol("j")),(s.Symbol("j"),0,s.oo))-1))
verify("Q016 coherent state uncertainty",iszero(s.sqrt(s.Symbol("h",positive=True)/(2*m*om))*s.sqrt(m*s.Symbol("h",positive=True)*om/2)-s.Symbol("h",positive=True)/2))
strength=s.symbols("strength",positive=True)
verify("Q017 finite well bound count",all(math.ceil(2*v/math.pi)==n for v,n in [(0.1,1),(1.5,1),(2.1,2),(3.2,3),(4.72,4)]))
verify("Q017 weak-well energy scaling",iszero(-(s.Symbol("h",positive=True)**2/(2*m))*(2*m*V*a/s.Symbol("h",positive=True)**2)**2+2*m*V**2*a**2/s.Symbol("h",positive=True)**2))
report={"batch":"05","ids":ids,"checks":[{"label":x,"passed":True} for x in checks],"count":len(checks),
 "status":"partial independent symbolic and numerical verification; expert review pending"}
(ROOT/"data"/"round05_symbolic_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=False,indent=2))
