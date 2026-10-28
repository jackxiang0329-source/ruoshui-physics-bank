#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Independent algebraic and numerical invariant checks for round 06.

Partial crosschecks, not a formal proof or signed expert peer review.
"""
import json
import math
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
data={p["id"]:p for p in json.loads((ROOT/"data/problems.json").read_text(encoding="utf-8"))}
ids=[f"{x}{n:03d}" for x in "METWOQ" for n in (20,21)]
assert all(i in data for i in ids)
checks=[]
def check(name, statement):
    assert bool(statement),name
    checks.append(name)
def zero(expr):
    return s.simplify(expr)==0
m,om,om0,t=s.symbols("m om om0 t",positive=True)
nu=s.symbols("nu",real=True)
D=-nu**2-2*om*nu+om0**2-om**2
check("M020 clockwise circular mode",zero(D.subs(nu,om0-om)))
check("M020 anticlockwise circular mode",zero(D.subs(nu,-om0-om)))
M,theta,k=s.symbols("M theta k",positive=True)
me=m*(M+m*s.sin(theta)**2)/(M+m)
check("M021 eliminated effective mass",zero(me-m*(1-m*s.cos(theta)**2/(M+m))))
check("M021 horizontal momentum elimination",zero((M+m)*(-m*s.cos(theta)/(M+m))+m*s.cos(theta)))
B,a,R,J,torque,O=s.symbols("B a R J torque O",positive=True)
gamma=B**2*a**4/(4*R)
I=B*a**2*O/(2*R)
check("E020 magnetic power",zero(I**2*R-gamma*O**2))
check("E020 mechanical torque",zero((B*a**2/2)*I-gamma*O))
q,eps,b=s.symbols("q eps b",positive=True)
image=-q*a/b
rimage=a**2/b
UA=q*image/(8*s.pi*eps*(b-rimage))
FA=q*image/(4*s.pi*eps*(b-rimage)**2)
check("E021 grounded sphere energy gradient",zero(-s.diff(UA,b)-FA))
FN=FA+q**2*a/(4*s.pi*eps*b**3)
check("E021 isolated sphere weaker attraction",bool(float(FN.subs({q:1,a:1,b:2,eps:1}))<0) and bool(float(FN.subs({q:1,a:1,b:2,eps:1}))>float(FA.subs({q:1,a:1,b:2,eps:1}))))
T,tc,N,kB=z=s.symbols("T tc N kB",positive=True)
u=s.Rational(3,2)*N*kB*T*(s.zeta(s.Rational(5,2))/s.zeta(s.Rational(3,2)))*(T/tc)**s.Rational(3,2)
Cv=s.Rational(15,4)*N*kB*(s.zeta(s.Rational(5,2))/s.zeta(s.Rational(3,2)))*(T/tc)**s.Rational(3,2)
check("T020 Bose heat capacity",zero(s.diff(u,T)-Cv))
check("T020 condensate critical boundary",zero((1-(T/tc)**s.Rational(3,2)).subs(T,tc)))
tau,N0,T0=s.symbols("tau N0 T0",positive=True)
x=(1+t/(6*tau))**(-6)
tt=T0*(1+t/(6*tau))**(-2)
check("T021 Knudsen rate ODE",zero(s.diff(x,t)+x*s.sqrt(tt/T0)/tau))
check("T021 effusion energy conservation",zero(s.Rational(3,2)*s.diff(N0*x*tt,t)-2*tt*s.diff(N0*x,t)))
mu,beta,omega,Ten=s.symbols("mu beta omega Ten",positive=True)
kr,ki=s.symbols("kr ki",positive=True)
check("W020 wave energy flux cancellation",zero((Ten*omega*kr/2)-(beta*omega**2/(4*ki))).subs({beta:2*Ten*kr*ki/omega}))
L,EI,den,P,n=s.symbols("L EI den P n",positive=True)
kn=n*s.pi/L
freq2=(EI*kn**4-P*kn**2)/den
check("W021 exact critical soft mode",zero(freq2.subs({n:1,P:s.pi**2*EI/L**2})))
check("W021 pressure decreases frequencies",zero(s.diff(freq2,P)+kn**2/den))
w,bb=s.symbols("w bb",positive=True)
slope=1/w**2-s.I*bb
dq2=(1+bb**2*w**4)/(2*w**2)
check("O020 Gaussian complex width",zero(s.re(1/slope)-w**2/(1+bb**2*w**4)))
check("O020 minimum Fourier uncertainty",zero((w**2/2)*dq2-(1+bb**2*w**4)/4))
lensR,C,lam,ninf,obj=s.symbols("lensR C lam ninf obj",positive=True)
index=ninf+C/lam**2
f=lensR/(2*(index-1))
im=obj*f/(obj-f)
check("O021 chromatic image shift derivative",zero(s.diff(im,lam)-obj**2/(obj-f)**2*lensR*C/(lam**3*(index-1)**2)))
hbar=s.symbols("hbar",positive=True)
energy=s.pi**2*hbar**2*n**2/(2*m*L**2)
check("Q020 quantum pressure F=2E/L",zero(-s.diff(energy,L)-2*energy/L))
check("Q020 quantum work from wall",zero(s.integrate(2*energy/L,(L,s.Symbol("L1",positive=True),s.Symbol("L2",positive=True)))-(energy.subs(L,s.Symbol("L1",positive=True))-energy.subs(L,s.Symbol("L2",positive=True)))))
v0,E=s.symbols("v0 E",positive=True)
kap=s.sqrt(2*m*(v0-E))/hbar
bar=s.sinh(kap*a)**2*v0**2/(4*E*(v0-E))
threshold=s.limit(bar,E,v0,dir="-")
check("Q021 barrier threshold",zero(threshold-m*v0*a**2/(2*hbar**2)))
zeta=s.symbols("zeta",real=True)
check("Q021 constructive barrier resonance",zero((1/(1+zeta*s.sin(s.pi)**2))-1))
report={"batch":"06","checked_ids":ids,"passed_count":len(checks),
"checks":[{"name":name,"passed":True} for name in checks],
"status":"machine symbolic/numeric spotchecks only; independent expert validation pending"}
(ROOT/"data"/"round06_validation_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=False,indent=2))
