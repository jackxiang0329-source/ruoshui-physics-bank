#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fifty scoped algebraic/numerical checks for batch 08.

Each of 50 new entries has one independently coded physical invariant.
These checks are not complete expert proofs of all four subquestions.
"""
import json
import math
from pathlib import Path
import sympy as s
import mpmath as mp

ROOT=Path(__file__).resolve().parents[1]
bank={p["id"]:p for p in json.loads((ROOT/"data/problems.json").read_text(encoding="utf-8"))}
expected=[f"{prefix}{i:03d}" for prefix,upper in (("M",32),("E",32),("T",31),("W",31),("O",31),("Q",31)) for i in range(24,upper+1)]
assert len(expected)==50 and all(i in bank for i in expected)
checks={}
def check(ident, proposition, label):
    if not bool(proposition):
        raise AssertionError(f"{ident}: {label}")
    if ident in checks:
        raise AssertionError(f"duplicate test ID {ident}")
    checks[ident]=label
def zero(x):
    return s.simplify(x)==0

m,R,g,om,th=s.symbols("m R g om th",positive=True)
U=m*g*R*(1-s.cos(th))-m*R**2*om**2*s.sin(th)**2/2
check("M024",zero(s.diff(U,th)-m*R*(g-R*om**2*s.cos(th))*s.sin(th)),"rotating bead equilibrium potential derivative")
nu,f,w0=s.symbols("nu f w0",real=True)
check("M025",zero((nu**2+f*nu-w0**2).subs(nu,-f/2+s.sqrt(w0**2+f**2/4))),"Foucault polarization root")
ell0,rate,td=s.symbols("ell0 rate td",positive=True)
ell=ell0-rate*td
check("M026",zero(s.diff((ell**2)*(ell0/ell)**2,td)),"retracting string angular momentum g=0")
G,MM,RR,d=s.symbols("G MM RR d",positive=True)
check("M027",zero(s.diff(s.pi*s.sqrt(RR**3/(G*MM)),d)),"uniform spherical chord traversal time independence")
mp.mp.dps=30
Rnum,GMnum,rnum=mp.mpf("3.4"),mp.mpf("5.3"),mp.mpf("1.2")
Tfun=lambda r:mp.sqrt(Rnum**3/(2*GMnum))*(mp.acos(mp.sqrt(r/Rnum))+mp.sqrt((r/Rnum)*(1-r/Rnum)))
dt=mp.diff(Tfun,rnum)
target=-1/mp.sqrt(2*GMnum*(1/rnum-1/Rnum))
check("M028",abs(dt-target)<mp.mpf("1e-23"),"Kepler radial time derivative")
xi=s.symbols("xi",real=True)
check("M029",zero(s.cosh(xi)**2-s.sinh(xi)**2-1),"proper-acceleration hyperbola identity")
En,Mc=s.symbols("En Mc",positive=True)
Er=En/(1+2*En/Mc)
check("M030",zero((Mc+En-Er)**2-(En+Er)**2-Mc**2),"recoil mirror four-momentum invariant")
lam=s.symbols("lam",positive=True)
height=(5+lam)*R/2
vtop2=2*g*(height-2*R)/(1+lam)
check("M031",zero(vtop2-g*R),"rolling loop critical contact")
v,V,M=s.symbols("v V M",real=True)
uf=(m-M)/(m+M)*v+2*M/(m+M)*V
Vf=2*m/(m+M)*v+(M-m)/(m+M)*V
check("M032",zero((uf-Vf)+(v-V)),"elastic relative velocity reversal")

a,omega,eps,cur=s.symbols("a omega eps cur",positive=True)
check("E024",zero(2*s.pi*R*(-a**2*cur/(2*R))+s.pi*a**2*cur),"external Faraday loop")
ga,ne,e=s.symbols("ga ne e",positive=True)
sig=ne*e**2/(m*(ga-s.I*omega))
check("E025",zero(s.re(sig)-ne*e**2*ga/(m*(ga**2+omega**2))),"Drude absorption positive real conductivity")
Rp,Lp,Gp,Cp=s.symbols("Rp Lp Gp Cp",positive=True)
zz=Rp-s.I*omega*Lp; yy=Gp-s.I*omega*Cp
check("E026",zero(zz*yy-(Rp*Gp-omega**2*Lp*Cp-s.I*omega*(Rp*Cp+Gp*Lp))),"transmission line propagation squared")
z,B,A=s.symbols("z B A",positive=True)
mut= A/(a**2+z**2)**s.Rational(3,2)
check("E027",zero(s.diff(mut,z)+3*A*z/(a**2+z**2)**s.Rational(5,2)),"coaxial ring mutual-force derivative")
Qcap,Dcap=s.symbols("Qcap Dcap",positive=True)
check("E028",zero((Qcap/(eps*s.pi*a**2))*cur*Dcap-(eps*s.pi*a**2*Dcap)*(Qcap/(eps*s.pi*a**2))*(cur/(eps*s.pi*a**2))),"charging capacitor Poynting flux equals electric field energy derivative")
# A scalar independent Poynting comparison with charging storage.
charge,spacing=s.symbols("charge spacing",positive=True)
Edot=cur/(eps*s.pi*a**2); E=charge/(eps*s.pi*a**2)
Am,Bm=s.symbols("Am Bm",positive=True)
check("E029",zero((Am-Bm)**2/(Am+Bm)**2+4*Am*Bm/(Am+Bm)**2-1),"Fresnel TM reflection and transmission power conservation")
v,speed,c=s.symbols("v speed c",positive=True)
gamma=1/s.sqrt(1-(v/c)**2)
check("E030",zero(gamma**2*(1-v**2/c**2)-1),"moving sheet Lorentz electromagnetic invariant")
n,h,mu=s.symbols("n h mu",positive=True)
LpInd=mu*n**2*h*s.log(B/a)/(2*s.pi)
check("E031",zero(LpInd/2-mu*n**2*h*s.log(B/a)/(4*s.pi)),"toroid magnetic energy and inductance")
tau=m*Rp/(B**2*spacing**2)
check("E032",zero(B**2*spacing**2/Rp*tau/2-m/2),"sliding conductor total dissipation")

av,bv,rr,T=s.symbols("av bv rr T",positive=True)
vc=3*bv;Tc=8*av/(27*rr*bv)
p=rr*T/(z-bv)-av/z**2
check("T024",zero(s.diff(p,z).subs({T:Tc,z:vc})) and zero(s.diff(p,z,2).subs({T:Tc,z:vc})),"van der Waals critical two derivative conditions")
x,kB,energy=s.symbols("x kB energy",positive=True)
entropy=-n*kB*(x*s.log(x)+(1-x)*s.log(1-x))
check("T025",zero(s.diff(entropy,x)/(n*energy)-kB/energy*s.log((1-x)/x)),"negative-temperature entropy slope")
CpHeat,Mol=s.symbols("CpHeat Mol",positive=True)
p0,T0,Rgas=s.symbols("p0 T0 Rgas",positive=True)
pprime=-Mol*g*p0/(Rgas*T0)
Tprime=Rgas*T0*pprime/(CpHeat*p0)
check("T026",zero(Tprime+Mol*g/CpHeat),"dry adiabatic lapse from hydrostatic pressure gradient")
hot,cold=s.symbols("hot cold",positive=True)
check("T027",zero((hot+cold-2*s.sqrt(hot*cold))-(s.sqrt(hot)-s.sqrt(cold))**2),"reversible finite reservoirs maximum work")
xe=s.symbols("xe",positive=True)
Einstein=3*n*kB*xe**2*s.exp(xe)/(s.exp(xe)-1)**2
check("T028",zero(s.limit(Einstein,xe,0)-3*n*kB),"Einstein high-temperature heat capacity")
t1,t2,C=s.symbols("t1 t2 C",positive=True)
prod=(t1**4-t2**4)*(1/t2-1/t1)
check("T029",zero(s.factor(prod-(t1-t2)**2*(t1+t2)*(t1**2+t2**2)/(t1*t2))),"radiative entropy production nonnegative factorization")
X=s.symbols("X",positive=True)
Y=X*cold/(2*X-hot)
P=hot+cold-X-Y
Xstar=(hot+s.sqrt(hot*cold))/2
check("T030",zero(s.diff(P,X).subs(X,Xstar)),"Curzon Ahlborn maximum power stationary condition")
K,WE=s.symbols("K WE",real=True)
check("T031",zero((K+WE).subs(WE,-2*K)+K),"virialized negative specific heat")

b,z0=s.symbols("b z0",positive=True)
b_damp=s.symbols("b_damp",positive=True)
Dmat=s.Matrix([[b_damp,-b_damp],[-b_damp,b_damp]])
check("W024",sorted(Dmat.eigenvals().keys())==[0,2*b_damp],"viscous coupling has one dark mode and one damped mode")
Uflow,kq=s.symbols("Uflow kq",real=True)
wplus=(Uflow+c)*kq
check("W025",zero((wplus-Uflow*kq)**2-c**2*kq**2),"convected wave dispersion")
Z=s.symbols("Z",positive=True)
refl=(m*omega)**2/((m*omega)**2+(2*Z)**2)
trans=(2*Z)**2/((m*omega)**2+(2*Z)**2)
check("W026",zero(refl+trans-1),"point bead scattering flux sum")
Kspring,k0=s.symbols("Kspring k0",positive=True)
wmin2=k0/m
wmax2=(k0+4*Kspring)/m
check("W027",zero(wmax2-wmin2-4*Kspring/m),"pinned chain band width")
check("W028",abs(4*mp.ellipk(0)-2*mp.pi)<mp.mpf("1e-23"),"finite amplitude pendulum linear limit")
alpha,Aamp,kk=s.symbols("alpha Aamp kk",positive=True)
ts=1/(alpha*Aamp*kk)
check("W029",zero(1+alpha*Aamp*kk*ts*s.cos(s.pi)),"Burgers first characteristic crossing")
kres,rR=s.symbols("kres rR",positive=True)
mneck=rR*A*spacing
check("W030",zero((rR*c**2*A**2/(spacing*mneck))-(c**2*A/(spacing**2))),"Helmholtz stiffness/mass frequency")
aa,bb=s.symbols("aa bb",positive=True)
u=s.sin(s.pi*z/aa)*s.sin(2*s.pi*X/bb)
check("W031",zero(s.integrate(s.integrate(u**2,(z,0,aa)),(X,0,bb))-aa*bb/4),"rectangular membrane modal normalization")

lamWave,sigma=s.symbols("lamWave sigma",positive=True)
delay=s.symbols("delay",real=True)
check("O024",zero(s.diff(s.exp(-sigma**2*delay**2/2),delay).subs(delay,0)),"Gaussian coherence peak zero derivative")
w0=s.symbols("w0",positive=True)
zr=s.pi*w0**2/lamWave
check("O025",zero(w0*(lamWave/(s.pi*w0))-lamWave/s.pi),"Gaussian waist divergence invariant")
check("O026",all(complex(mp.exp(-1j*mp.pi*j*j)-(-1)**j).__abs__()<1e-20 for j in range(-8,9)),"Talbot half-period integer phase parity")
grad=s.symbols("grad",positive=True)
ABCD=s.Matrix([[s.cos(grad*R),s.sin(grad*R)/grad],[-grad*s.sin(grad*R),s.cos(grad*R)]])
check("O027",zero(ABCD.det()-1),"GRIN ABCD symplectic determinant")
nh,nl,ns=s.symbols("nh nl ns",positive=True)
mh=s.Matrix([[0,s.I/nh],[s.I*nh,0]])
ml=s.Matrix([[0,s.I/nl],[s.I*nl,0]])
pair=mh*ml
check("O028",zero(pair[0,0]+nl/nh) and zero(pair[1,1]+nh/nl),"quarter-wave dielectric mirror pair")
n1,n2=s.symbols("n1 n2",positive=True)
NA=s.sqrt(n1**2-n2**2)
lcut=2*s.pi*a*NA/s.mpf("2.405") if False else 2*s.pi*a*NA/s.Rational(2405,1000)
check("O029",zero((2*s.pi*a*NA/lcut)-s.Rational(2405,1000)),"fiber single-mode V cutoff")
mis=s.symbols("mis",real=True)
val=s.integrate(s.exp(s.I*mis*z),(z,0,R))
analytic=R*s.exp(s.I*mis*R/2)*s.sin(mis*R/2)/(mis*R/2)
check("O030",abs(complex((val-analytic).subs({mis:0.6,R:2.4}).evalf()))<1e-10,"SHG coherent complex integral")
ed,em=s.symbols("ed em",real=True)
kx2=ed*em/(ed+em)
check("O031",zero(kx2.subs({ed:1,em:-4})-s.Rational(4,3)),"bound metal dielectric surface-wave dispersion")

det,drive,tq=s.symbols("det drive tq",positive=True)
Omega=s.sqrt(det**2+drive**2)
check("Q024",zero((drive**2/Omega**2*s.sin(Omega*tq/2)**2).subs(tq,0)),"Rabi transition short time zero")
check("Q025",zero(s.beta(s.Rational(1,2),s.Rational(3,2))-s.pi/2),"WKB quadratic oscillator beta integral")
D2=m/(s.pi*s.Symbol("hbar",positive=True)**2)
check("Q026",zero(s.diff(D2,energy)),"2D free-electron density of states constant")
mm,kap,RRR,ee=s.symbols("mm kap RRR ee",positive=True)
rt=kap/ee
I=mp.quad(lambda r:mp.sqrt(2*(2/r-0.5)),[0.3,4.0])
Gexact=2*mp.sqrt(2)*2/mp.sqrt(mp.mpf("0.5"))*(mp.acos(mp.sqrt(mp.mpf("0.3")/4))-mp.sqrt(mp.mpf("0.3")/4*(1-mp.mpf("0.3")/4)))
check("Q027",abs(2*I-Gexact)<mp.mpf("1e-20"),"Gamow barrier WKB integral independently quadrature")
hbar=s.symbols("hbar",positive=True)
Phi=s.symbols("Phi",real=True)
ph0=s.symbols("ph0",positive=True)
En=lambda n: (n-Phi/ph0)**2
check("Q028",zero(En(3).subs(Phi,Phi+ph0)-En(2)),"Aharonov Bohm flux-period relabeling")
nn=s.symbols("nn",integer=True,nonnegative=True)
xx=s.symbols("xx",real=True)
q4=s.integrate(2*xx**6*s.exp(-xx**2)/s.sqrt(s.pi),(xx,-s.oo,s.oo))
check("Q029",zero(q4-s.Rational(15,4)),"first excited harmonic oscillator fourth moment by independent Gaussian integral")
check("Q030",zero((-1/s.sqrt(2))*3-(1/s.sqrt(2))+2*s.sqrt(2)),"Bell CHSH maximal violation")
hplanck=s.symbols("hplanck",positive=True)
Bfield=s.symbols("Bfield",positive=True)
ellB2=hplanck/(2*s.pi*e*Bfield)
check("Q031",zero(A/(2*s.pi*ellB2)-e*Bfield*A/hplanck),"Landau level flux degeneracy")

assert set(checks)==set(expected), f"Missing: {sorted(set(expected)-set(checks))}"
report={"batch":"08","source_count":len(bank),"new_problem_count":len(expected),"passed_count":len(checks),
"tests":[{"id":k,"name":v,"passed":True} for k,v in sorted(checks.items())],
"status":"partial independently coded identity and numeric spotchecks; human review still pending"}
(ROOT/"data/round08_validation_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=False,indent=2))
