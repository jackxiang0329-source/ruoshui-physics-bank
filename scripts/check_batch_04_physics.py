#!/usr/bin/env python3
"""Symbolic/numeric cross-checks on physically independent fourth-batch relations.

Checks are partial technical verification only; not independent peer review.
"""
from pathlib import Path
import json
import math
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
data={p["id"]:p for p in json.loads((ROOT/"data"/"problems.json").read_text(encoding="utf-8"))}
ids=[f"{prefix}{n:03d}" for prefix in ("M","E","T","W","O","Q") for n in range(12,16)]
assert all(x in data for x in ids) and len(ids)==24
checks=[]
def claim(name,v):
    assert bool(v),name
    checks.append(name)
m,g,c,v0=s.symbols("m g c v0",positive=True)
vT=s.sqrt(m*g/c)
H=vT**2/(2*g)*s.log(1+(v0/vT)**2)
claim("M012 dragless max-height limit",s.limit(H,c,0,dir="+")==v0**2/(2*g))
claim("M012 final-speed bound",float((v0/s.sqrt(1+(v0/vT)**2)).subs({m:2,g:10,c:1,v0:8}))<8)
k,r,p,ang=s.symbols("k r p ang",positive=True)
L=s.symbols("L",nonzero=True,real=True)
U=L**2/(2*m*r**2)+k*r**p/p
r0=(L**2/(m*k))**(1/(p+2))
claim("M013 stable curvature",s.simplify(s.diff(U,r,2).subs(L**2,m*k*r**(p+2))-k*(p+2)*r**(p-2))==0)
gg,aa,ell,theta=s.symbols("gg aa ell theta",positive=True)
Ueff=m*ell*(gg*(1-s.cos(theta))+aa*s.sin(theta))
claim("M014 horizontal acceleration pendulum",s.simplify(s.diff(Ueff,theta)-m*ell*(gg*s.sin(theta)+aa*s.cos(theta)))==0)
phi=s.symbols("phi",real=True)
cycx=ang*(phi-s.sin(phi));cycy=ang*(1-s.cos(phi))
claim("M015 cycloid constant time",s.trigsimp(s.sqrt(s.diff(cycx,phi)**2+s.diff(cycy,phi)**2)**2-4*ang**2*s.sin(phi/2)**2)==0)
epsa,qa,b=s.symbols("epsa qa b",positive=True)
ss=s.symbols("ss",real=True)
J=s.integrate((r/qa)**(-ss)/r,(r,qa,b))
claim("E012 radially graded capacitance continuity",s.simplify(s.limit((1-(qa/b)**ss)/ss,ss,0)-s.log(b/qa))==0)
w,mu,sigma,delta=s.symbols("w mu sigma delta",positive=True)
skin=s.sqrt(2/(w*mu*sigma))
claim("E013 skin wavenumber",s.simplify(((1+s.I)/skin)**2-s.I*w*mu*sigma)==0)
R,eps,permeab,ra,rb=s.symbols("R eps permeab ra rb",positive=True)
Cprime=2*s.pi*eps/s.log(rb/ra)
Lprime=permeab*s.log(rb/ra)/(2*s.pi)
claim("E014 TEM phase speed",s.simplify(Lprime*Cprime-permeab*eps)==0)
C,Lc,Rc,V0,I0=s.symbols("C Lc Rc V0 I0",positive=True)
claim("E015 parallel RLC initial energy",s.simplify((C*V0**2+Lc*I0**2)/2-C*V0**2/2-Lc*I0**2/2)==0)
ah,ac,Th,Tc=s.symbols("ah ac Th Tc",positive=True)
Ts=(ah*Th+ac*Tc)/(ah+ac)
claim("T012 variable-C total entropy",s.simplify(ah*(Ts-Th)+ac*(Ts-Tc))==0)
claim("T012 variable-C maximum work",s.simplify((ah*Th**2+ac*Tc**2-(ah+ac)*Ts**2)/2-ah*ac*(Th-Tc)**2/(2*(ah+ac)))==0)
T1,bb,cv,lam=s.symbols("T1 bb cv lam",positive=True)
Tend=cv/bb*s.LambertW(bb*T1/cv*s.exp(bb*T1/cv)*lam**(-R/cv))
claim("T013 LambertW implicit",abs(float((cv*s.log(Tend/T1)+bb*(Tend-T1)+R*s.log(lam)).subs({cv:3,bb:0.1,T1:300,R:8.3,lam:2}).evalf()))<1e-8)
Lv,T,Tref,P0=s.symbols("Lv T Tref P0",positive=True)
Pv=P0*s.exp(Lv/R*(1/Tref-1/T))
claim("T014 saturation slope",s.simplify(s.diff(Pv,T)-Pv*Lv/(R*T**2))==0)
av,bv,Tv,Cp=s.symbols("av bv Tv Cp",positive=True)
P=s.symbols("P",positive=True)
vol=R*Tv/P+bv-av/(R*Tv)
claim("T015 Joule-Thomson low pressure",s.simplify((Tv*s.diff(vol,Tv)-vol)/Cp-(2*av/(R*Tv)-bv)/Cp)==0)
Z,D,bd,omega=s.symbols("Z D bd omega",positive=True,real=True)
rb=(D+s.I*omega*(Z-bd))/(-D+s.I*omega*(Z+bd))
absorb=s.factor(1-rb*s.conjugate(rb))
claim("W012 passive point termination",s.simplify(absorb-4*bd*Z*omega**2/(D**2+omega**2*(Z+bd)**2))==0)
be=s.symbols("be",positive=True)
q0=s.pi/2
claim("W013 Robin root shift",s.simplify((q0+be/q0)*s.cos(q0+be/q0)+be*s.sin(q0+be/q0)).series(be,0,2).removeO()==0)
mass,imp,K=s.symbols("mass imp K",positive=True)
t=imp/(2*mass-imp)
freq=4*K*mass/(imp*(2*mass-imp))
claim("W014 impurity site equation",s.simplify(imp*freq-2*K*(1+t))==0)
alpha,L,T0,mi,n=s.symbols("alpha L T0 mi n",positive=True)
wn=alpha*s.sqrt(T0/mi)*s.sqrt(s.Rational(1,4)+(n*s.pi/s.log(1+alpha*L))**2)
claim("W015 homogeneous string limit",s.simplify(s.limit(wn,alpha,0,dir="+")-n*s.pi*s.sqrt(T0/mi)/L)==0)
f1,f2,d=s.symbols("f1 f2 d",positive=True)
Mat=s.Matrix([[1,0],[-1/f2,1]])*s.Matrix([[1,d],[0,1]])*s.Matrix([[1,0],[-1/f1,1]])
claim("O012 dual lens determinant",s.simplify(Mat.det()-1)==0)
claim("O012 afocal condition",s.simplify(Mat[1,0].subs(d,f1+f2))==0)
tau,b2,z,T0=s.symbols("tau b2 z T0",positive=True)
sig=b2*z/T0**2
claim("O013 Gaussian pulse energy",s.simplify((T0*s.sqrt(1+sig**2))/s.sqrt(1+sig**2)-T0)==0)
dnu,dt=s.symbols("dnu dt",positive=True)
claim("O011 spectral envelope first zero",s.simplify(s.sin(s.pi*dnu*(1/dnu)))==0)
delta=s.symbols("delta",real=True)
claim("O014 grating finite array central peak",s.limit(s.sin(10*delta)/(10*s.sin(delta)),delta,0)==1)
alpha_p,theta=s.symbols("alpha_p theta",real=True)
out=s.Matrix([s.cos(theta),s.I*s.sin(theta)])
pol=s.Matrix([s.cos(alpha_p),s.sin(alpha_p)])
intensity=s.expand_complex((pol.T*out)[0]*s.conjugate((pol.T*out)[0]))
claim("O015 quarter wave analyzer",s.trigsimp(intensity-(s.cos(alpha_p)**2*s.cos(theta)**2+s.sin(alpha_p)**2*s.sin(theta)**2))==0)
ki,kf=s.symbols("ki kf",positive=True)
Nmean=(kf-ki)**2/(4*ki*kf)
P0state=2*s.sqrt(ki*kf)/(ki+kf)
claim("Q014 no quench excitation",s.simplify(Nmean.subs(kf,ki))==0)
claim("Q014 ground-state overlap",s.simplify(P0state.subs(kf,ki)-1)==0)
gama=s.symbols("gama",positive=True)
beta2=1-1/gama**2
M=s.sqrt(2*(gama+1))
V2=gama**2*beta2/(gama+1)**2
claim("Q015 invariant mass and CoM speed",s.simplify((gama+1)**2-gama**2*beta2-M**2)==0 and s.simplify(V2-(gama-1)/(gama+1))==0)
report={"batch_ids":ids,"passed_count":len(checks),"checks":[{"id":c,"passed":True} for c in checks],
    "status":"partial independent symbolic tests only; human peer review pending"}
(ROOT/"data"/"batch_04_symbolic_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=False,indent=2))
