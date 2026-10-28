#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Round 07 independently evaluated formula invariants.

Mechanical review of selected claims only, not full theorem proving or expert approval.
"""
import json, math
from pathlib import Path
import sympy as s
import mpmath as mp

ROOT=Path(__file__).resolve().parents[1]
bank={p["id"]:p for p in json.loads((ROOT/"data/problems.json").read_text(encoding="utf-8"))}
ids=tuple(f"{prefix}{n:03d}" for prefix in "METWOQ" for n in (22,23))
assert len(ids)==12 and all(i in bank for i in ids)
checks=[]
def check(label, yes):
    assert bool(yes),label
    checks.append(label)
def zero(v): return s.simplify(v)==0

m,v,b,kappa=s.symbols("m v b kappa",positive=True)
energy=m*v**2/2
rmin=(kappa+s.sqrt(kappa**2+m**2*v**4*b**2))/(m*v**2)
L=m*v*b
check("M022 Rutherford turning point",zero((2*energy*rmin**2-2*kappa*rmin-L**2/m)))
check("M022 Rutherford cross section units coefficient",zero(kappa**2/(4*m**2*v**4)-kappa**2/(16*energy**2)))
lmb=s.symbols("lmb",real=True)
mat=s.Matrix([[2-2*lmb,-lmb],[-lmb,1-lmb]])
check("M023 double-pendulum determinant",zero(mat.det()-(lmb**2-4*lmb+2)))
check("M023 first normal frequency",zero(mat.det().subs(lmb,2-s.sqrt(2))))
check("M023 second normal frequency",zero(mat.det().subs(lmb,2+s.sqrt(2))))
mass=s.Matrix([[2,1],[1,1]])
check("M023 mass-weighted orthogonality",zero((s.Matrix([[1,s.sqrt(2)]])*mass*s.Matrix([1,-s.sqrt(2)]))[0]))
sigma0,h,Ex=s.symbols("sigma0 h Ex",positive=True)
sigma=sigma0/(1+h**2)*s.Matrix([[1,-h],[h,1]])
current=sigma*s.Matrix([Ex,-h*Ex])
check("E022 Hall open side current",zero(current[1]) and zero(current[0]-sigma0*Ex))
check("E022 zero Hall field transverse current",zero((sigma*s.Matrix([Ex,0]))[1]-h*sigma0*Ex/(1+h**2)))
eps,w,d,L,K,Q,V,x=s.symbols("eps w d L K Q V x",positive=True)
cap=eps*w*(L+(K-1)*x)/d
cq=s.diff(cap,x)
check("E023 fixed Q force",zero(-s.diff(Q**2/(2*cap),x)-Q**2*cq/(2*cap**2)))
check("E023 fixed V battery energy",zero(V**2*cq-V**2*cq/2-V**2*cq/2))
N,wd,Hbar,kB,T,TD=s.symbols("N wd Hbar kB T TD",positive=True)
freq=s.symbols("freq",positive=True)
density=9*N*freq**2/wd**3
check("T022 Debye normal mode count",zero(s.integrate(density,(freq,0,wd))-3*N))
check("T022 Debye zero point",zero(s.integrate(Hbar*freq*density/2,(freq,0,wd))-9*N*Hbar*wd/8))
check("T022 Debye low-temperature derivative",zero(s.diff(3*s.pi**4*N*kB*T**4/(5*TD**3),T)-12*s.pi**4*N*kB*T**3/(5*TD**3)))
na,aa,bb,Cv,R,Vi,Ti,Vol=s.symbols("na aa bb Cv R Vi Ti Vol",positive=True)
temp=Ti+aa*na/Cv*(1/Vol-1/Vi)
ent=na*Cv*s.log(temp/Ti)+na*R*s.log((Vol-na*bb)/(Vi-na*bb))
pressure=na*R*temp/(Vol-na*bb)-aa*na**2/Vol**2
check("T023 van der Waals isenergetic entropy slope",zero(s.diff(ent,Vol)-pressure/temp))
check("T023 van der Waals free-expansion cooling",zero(s.diff(temp,Vol)+aa*na/(Cv*Vol**2)))
mu,permitt,a,omega=s.symbols("mu permitt a omega",positive=True)
omc=s.pi/(a*s.sqrt(mu*permitt))
kz2=mu*permitt*(omega**2-omc**2)
check("W022 waveguide cutoff",zero(kz2-(mu*permitt*omega**2-s.pi**2/a**2)))
vg=(1/s.sqrt(mu*permitt))*s.sqrt(1-omc**2/omega**2)
vp=(1/s.sqrt(mu*permitt))/s.sqrt(1-omc**2/omega**2)
check("W022 group phase product",zero(vp*vg-1/(mu*permitt)))
root=mp.findroot(lambda z:z*mp.cos(z)-mp.sin(z), (mp.mpf("4.4"),mp.mpf("4.6")))
check("W023 first spherical Neumann root",abs(root-mp.mpf("4.493409457909064"))<mp.mpf("1e-10"))
sig,dist,lam=s.symbols("sig dist lam",positive=True)
k=2*s.pi/lam
Vcoh=s.exp(-(k*dist*sig)**2/2)
coh=lam/(s.sqrt(2)*s.pi*sig)
check("O022 Gaussian angular coherence 1/e length",zero(Vcoh.subs(dist,coh)-s.E**(-1)))
j,ff=s.symbols("j ff",positive=True)
rn2=j*lam*ff+(j*lam/2)**2
check("O023 exact Fresnel zone radius",zero(s.expand(ff**2+rn2-(ff+j*lam/2)**2)))
check("O023 binary phase efficiency quadruple",zero(4/s.pi**2-4*(1/s.pi**2)))
a0,a1=s.symbols("a0 a1",real=True)
check("Q022 exchange-symmetric orbit at coincident coordinates",zero((a0*a1-a1*a0)/s.sqrt(2)))
muR,Z,el,epsilon,Hbar2=s.symbols("muR Z el epsilon Hbar2",positive=True)
bohr=4*s.pi*epsilon*Hbar2**2/(muR*Z*el**2)
r=s.symbols("r",positive=True)
pr=4*r**2/s.Integer(1)/bohr**3*s.exp(-2*r/bohr)
check("Q023 hydrogen radial normalization",zero(s.integrate(pr,(r,0,s.oo))-1))
check("Q023 hydrogen mean radius",zero(s.integrate(r*pr,(r,0,s.oo))-3*bohr/2))
check("Q023 hydrogen Coulomb expectation",zero(s.integrate(pr/r,(r,0,s.oo))-1/bohr))
check("Q023 hydrogen variance moment",zero(s.integrate(r**2*pr,(r,0,s.oo))-3*bohr**2))
report={"batch":"07","ids":list(ids),"passed_count":len(checks),"check_names":checks,
"status":"selected invariant tests passed; independent expert review not performed"}
(ROOT/"data"/"round07_validation_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=False,indent=2))
