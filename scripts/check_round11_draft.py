#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Subpart-level independent spot-checks for round 11 *draft* questions.

This checks symbolic/numeric identities, limits and conserved quantities for
currently authored drafts, plus formatting, de-duplication and source safety.
It is NOT a proof of every step and is NOT independent expert peer review.
The draft is not admitted into the canonical bank until its count reaches
100, 400 substantive tests run, all TeX sources compile, and CI is green.
"""
import collections
import json
import math
import re
import sys
from pathlib import Path
import mpmath as mp
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
DRAFT=ROOT/"data/rounds/2026-10-28-11-draft.json"
REPORT=ROOT/"data/round11_draft_validation_report.json"
if not DRAFT.exists():
    print("round11 draft absent; validator skipped")
    sys.exit(0)
draft=json.loads(DRAFT.read_text(encoding="utf8"))
items={p["id"]:p for p in draft["items"]}
if len(items)!=len(draft["items"]):
    raise AssertionError("Duplicate problem IDs")
old={p["id"]:p for p in json.loads((ROOT/"data/problems.json").read_text(encoding="utf8"))}
if len(old)!=252 or set(items)&set(old):
    raise AssertionError("Baseline count or ID overlap")
prefix={"力学":"M","电磁学":"E","热学":"T","振动与波动":"W","光学":"O","近代物理":"Q"}
for uid,p in items.items():
    assert re.fullmatch(r"[METWOQ]\d{3,5}",uid) and uid[0]==prefix[p["topic"]],uid
    assert p["level"]==5 and p["tier"]=="advanced_composite" and p["estimated_minutes"]>=40,uid
    assert len(set(p["tags"]))>=3 and p["quality_status"]=="待独立复核",uid
    for section in ("question","solution"):
        body=p[section]
        matches=list(re.finditer(r"(?m)^\(([1-4])\)\s*",body))
        assert len(matches)==4 and [m.group(1) for m in matches]==["1","2","3","4"],(uid,section)
        if section=="solution":
            chunks=[body[matches[j].end():(matches[j+1].start() if j<3 else len(body))]
                    for j in range(4)]
            assert min(len(x.strip()) for x in chunks)>=100,(uid,"incomplete solution part")
        assert body.count(r"\(")==body.count(r"\)"),(uid,"unbalanced math")
        assert body.count(r"\[")==body.count(r"\]"),(uid,"unbalanced display math")
        assert not any(ord(ch)<32 and ch not in "\t\n\r" for ch in body),(uid,"control byte")
        for bad in (r"\input",r"\include",r"\write18",r"\documentclass",r"\openout"):
            assert bad not in body,(uid,bad)
# Nontrivial full-bank editorial duplicate gate is independently executed by CI.
tests=[]
def eq(a,b=0):
    return s.simplify(a-b)==0
def approx(a,b,tol=1.e-8):
    return math.isclose(float(a),float(b),rel_tol=tol,abs_tol=tol)
def record(uid,part,method,name,assertion):
    assert uid in items,(uid,"missing authored problem")
    assert method in ("symbolic","numerical","limit","dimensions","conservation","independent_derivation","physical_case")
    assert len(name)>=15
    assert bool(assertion),(uid,part,name)
    tests.append({"id":uid,"part":part,"method":method,"name":name,"passed":True})
g,L,a,b,m,M,k,R,C,c,w,y,al,z=s.symbols("g L a b m M k R C c w y al z",positive=True)
pi=s.pi
# Mechanics: variable-density chain, asymmetric normal modes, spool, rotating paraboloid.
mass=L*(1+al/2)
Ml=y+al*y*y/(2*L)
F=g*(2*Ml-mass)
record("M050",1,"symbolic","integrated graded chain mass from material coordinate",eq(s.integrate(1+al*z/L,(z,0,L)),mass))
record("M050",2,"independent_derivation","work-energy differentiation recovers graded driving force",eq(s.diff(2*g*(y*y+al*y**3/(3*L)-mass*y)/mass,y),2*F/mass))
record("M050",3,"physical_case","uniform chain zero-velocity equilibrium lies at half length",eq(F.subs({al:0,y:L/2}),0))
record("M050",4,"limit","linear instability rate becomes square root of two g over L",eq(s.limit(2*g*(1+al*y/L)/mass,al,0),2*g/L))
m1,m2,k1,k2,kc,ww,F0=s.symbols("m1 m2 k1 k2 kc ww F0",positive=True)
aa=(k1+kc)/m1; dd=(k2+kc)/m2; bb=kc/s.sqrt(m1*m2)
disc=(aa-dd)**2+4*bb**2
la=(aa+dd+s.sqrt(disc))/2; lb=(aa+dd-s.sqrt(disc))/2
record("M051",1,"symbolic","coupled stiffness matrix has strictly positive determinant",eq((k1+kc)*(k2+kc)-kc**2,k1*k2+kc*(k1+k2)))
record("M051",2,"independent_derivation","normal-frequency eigenvalue sum matches trace identity",eq(la+lb,aa+dd))
record("M051",3,"conservation","normal-frequency eigenvalue product matches determinant",eq(la*lb,(k1*k2+kc*(k1+k2))/(m1*m2)))
D=(k1+kc-m1*ww**2)*(k2+kc-m2*ww**2)-kc**2
X1=F0*(k2+kc-m2*ww**2)/D;X2=F0*kc/D
record("M051",4,"numerical","matrix forced-response residual vanishes for nonresonant sample",approx(((k1+kc-m1*ww**2)*X1-kc*X2-F0).subs({k1:3,k2:5,kc:2,m1:1,m2:2,ww:s.Rational(1,2),F0:4}),0))
I,rr,cc,Om=s.symbols("I rr cc Om",positive=True)
me=m+I/rr**2; acc=m*g/me; tens=I*acc/rr**2
record("M052",1,"independent_derivation","rolling spool translation and rotation tensions agree",eq(m*acc+ tens,m*g))
record("M052",2,"physical_case","effective spool inertia exceeds its translational mass",bool(me.subs({m:2,I:3,rr:2})>m.subs(m,2)))
Z=k-me*Om**2+s.I*cc*Om
record("M052",3,"symbolic","phasor spring and damping impedance balances applied force",eq(Z*(F0/Z),F0))
record("M052",4,"conservation","dissipated power equals cycle average force input at sample",approx((cc*Om**2*F0**2/(2*s.Abs(Z)**2)).subs({m:2,I:1,rr:1,k:8,cc:1,Om:2,F0:3}),(1*4*9/2)/(16+4)))
rrr,v,accel=s.symbols("rrr v accel",real=True)
A=1+4*a*a*rrr**2
Lag=m*A*v*v/2+m*Om**2*rrr**2/2-m*g*a*rrr**2
EL=m*A*accel+s.diff(m*A,rrr)*v*v/2+m*(2*g*a-Om**2)*rrr
record("M053",1,"independent_derivation","nonlinear radial Euler-Lagrange inertial gradient is retained",eq(s.diff(m*A,rrr)*v*v/2,4*m*a*a*rrr*v*v))
record("M053",2,"symbolic","rotating paraboloid effective potential curvature controls axis",eq(s.diff(m*(g*a-Om**2/2)*rrr**2,rrr,2),m*(2*g*a-Om**2)))
record("M053",3,"physical_case","critical spin zeros linear restoring frequency squared",eq((2*g*a-Om**2).subs({g:10,a:s.Rational(1,2),Om:s.sqrt(10)}),0))
record("M053",4,"conservation","Jacobi integral derivative vanishes along exact radial equation",eq(m*A*v*(-(s.diff(m*A,rrr)*v*v/2 + m*(2*g*a-Om**2)*rrr)/(m*A))+(m*s.diff(A,rrr)*v*v/2+m*(2*g*a-Om**2)*rrr)*v,0))
# Electromagnetism: graded dielectric cylinder, nonuniform rotating disk, flux-driven RLC, lossy line.
eps,lam,alpha,mu0=s.symbols("eps lam alpha mu0",positive=True)
f=1/(y*(1+alpha*y/a))
logexpr=s.log(b*(1+alpha)/(a+alpha*b))
record("E050",1,"symbolic","radial dielectric field integral yields logarithmic cylinder voltage",eq(s.integrate(f,(y,a,b)),logexpr))
record("E050",2,"conservation","stored field energy equals charge times potential over two",eq(lam**2*logexpr/(4*pi*eps),lam**2/(2*(2*pi*eps/logexpr))))
P=lam*alpha/(2*pi*(a+alpha*y))
rho=-s.diff(y*P,y)/y
Bnet=s.integrate(rho*2*pi*y,(y,a,b))-P.subs(y,a)*2*pi*a+P.subs(y,b)*2*pi*b
record("E050",3,"conservation","volume and two interface bound charges sum to zero",eq(Bnet))
record("E050",4,"limit","uniform dielectric limit restores ordinary coaxial potential",eq(s.limit(logexpr,alpha,0),s.log(b/a)))
sig,sigM=s.symbols("sig sigM",positive=True)
q=2*pi*sig*s.integrate(y*(1-y*y/R**2),(y,0,R))
massdisk=2*pi*sigM*s.integrate(y*(1-y*y/R**2),(y,0,R))
record("E051",1,"independent_derivation","graded disk total surface charge equals pi sigma R square over two",eq(q,pi*sig*R**2/2))
moment=pi*sig*w*s.integrate(y**3*(1-y*y/R**2),(y,0,R))
record("E051",2,"symbolic","rotating disk loop-current integration gives magnetic moment",eq(moment,q*w*R**2/6))
Baxis=mu0*w*sig*s.integrate(1-y*y/R**2,(y,0,R))/2
record("E051",3,"independent_derivation","Biot-Savart concentric ring integration gives central field",eq(Baxis,mu0*w*sig*R/3))
Idisk=2*pi*sigM*s.integrate(y**3*(1-y*y/R**2),(y,0,R))
record("E051",4,"conservation","gyromagnetic ratio equals charge over twice total mass",eq(moment/(Idisk*w),q/(2*massdisk)))
La,Ca,Ra,Om,phi=s.symbols("La Ca Ra Om phi",positive=True)
imp=Ra+s.I*(Om*La-1/(Om*Ca))
record("E052",1,"symbolic","external sinusoidal flux derivative generates Lenz electromotive force",eq(-s.diff(phi*s.cos(Om*y),y),phi*Om*s.sin(Om*y)))
record("E052",2,"independent_derivation","current phasor solves impedance-driven electromotive balance",eq(imp*(-s.I*Om*phi/imp),-s.I*Om*phi))
record("E052",3,"conservation","mean resistive power matches positive closed loop expression",eq(Ra*s.Abs(-s.I*Om*phi/imp)**2/2,Ra*Om**2*phi**2/(2*(Ra**2+(Om*La-1/(Om*Ca))**2))))
r1,r2=s.symbols("r1 r2",real=True)
record("E052",4,"symbolic","RLC decay roots satisfy characteristic trace and determinant",eq((-Ra+s.sqrt(Ra**2-4*La/Ca))/(2*La)+(-Ra-s.sqrt(Ra**2-4*La/Ca))/(2*La),-Ra/La))
R1,L1,G1,C1,zl=z1=s.symbols("R1 L1 G1 C1 zl",positive=True)
zz=(R1+s.I*w*L1); yy=(G1+s.I*w*C1)
gamma=s.sqrt(zz*yy);z0=s.sqrt(zz/yy)
record("E053",1,"symbolic","telegrapher propagation and impedance satisfy squared-product laws",eq(gamma**2,zz*yy))
G=(zl-z0)/(zl+z0)
record("E053",2,"symbolic","load reflection enforces matched endpoint voltage-current ratio",eq((1+G)/(1-G),zl/z0))
Zp,Zq=s.symbols("Zp Zq",positive=True)
rcoef=(Zq-Zp)/(Zq+Zp)
record("E053",3,"conservation","lossless line reflected and delivered powers add to incident",eq(rcoef**2+4*Zp*Zq/(Zp+Zq)**2,1))
lowloss=(R1/2)*s.sqrt(C1/L1)+(G1/2)*s.sqrt(L1/C1)
gnum=complex(gamma.subs({R1:.01,L1:2,G1:.004,C1:3,w:5}).evalf())
record("E053",4,"numerical","weak-loss attenuation agrees with exact complex propagation at low loss",approx(gnum.real,float(lowloss.subs({R1:.01,L1:2,G1:.004,C1:3})),tol=1e-4))
# Thermodynamics: vdW criticality, reversible reservoirs, dimerization, nonlinear cylindrical heat flow.
v,V,T,gasA,gasB,Rg=s.symbols("v V T gasA gasB Rg",positive=True)
p=Rg*T/(v-gasB)-gasA/v**2
vc=3*gasB;Tc=8*gasA/(27*Rg*gasB);pc=gasA/(27*gasB**2)
record("T048",1,"symbolic","critical van der Waals first derivative vanishes at triple volume",eq(s.diff(p,v).subs({v:vc,T:Tc})))
record("T048",2,"symbolic","critical van der Waals second derivative vanishes simultaneously",eq(s.diff(p,v,2).subs({v:vc,T:Tc})))
record("T048",3,"independent_derivation","reduced van der Waals equation reproduces critical pressure",eq(p.subs({v:vc,T:Tc}),pc))
tr,wr=s.symbols("tr wr",real=True)
pred=8*(1+tr)/(2+3*wr)-3/(1+wr)**2
record("T048",4,"limit","critical isotherm cubic coefficient equals negative three halves",eq(s.diff(pred.subs(tr,0),wr,3).subs(wr,0)/6,-s.Rational(3,2)))
Ch,Cc,Th,Tc2=s.symbols("Ch Cc Th Tc2",positive=True)
Tf=Th**(Ch/(Ch+Cc))*Tc2**(Cc/(Ch+Cc))
record("T049",1,"conservation","reversible finite-reservoir entropy change exactly vanishes",eq(s.expand_log(Ch*s.log(Tf/Th)+Cc*s.log(Tf/Tc2),force=True),0))
record("T049",2,"numerical","finite-reservoir maximum extractable work is positive at sample",float((Ch*Th+Cc*Tc2-(Ch+Cc)*Tf).subs({Ch:2,Cc:3,Th:500,Tc2:250}).evalf())>0)
record("T049",3,"physical_case","equal heat-capacity reversible final temperature is geometric mean",eq(Tf.subs({Ch:1,Cc:1}),s.sqrt(Th*Tc2)))
d=s.symbols("d",positive=True)
Work=2*T-s.sqrt((T+d/2)*(T-d/2))*2
record("T049",4,"limit","small temperature gap reversible work is quadratic",eq(s.limit(Work/d**2,d,0),1/(4*T)))
h,kB,tm,epsv,g1,g2=s.symbols("h kB tm epsv g1 g2",positive=True)
l1=h/s.sqrt(2*pi*m*kB*tm);l2=h/s.sqrt(2*pi*(2*m)*kB*tm)
Kchem=g2*l1**6*s.exp(epsv/(kB*tm))/(g1**2*l2**3)
record("T050",1,"symbolic","molecular thermal wavelength equals atomic wavelength over sqrt two",eq(l2,l1/s.sqrt(2)))
record("T050",2,"independent_derivation","mass action constant includes translational wavelength ratio",eq(Kchem,(g2/g1**2)*2**s.Rational(3,2)*l1**3*s.exp(epsv/(kB*tm))))
N,Vv,KK=s.symbols("N Vv KK",positive=True)
n1=2*N/(1+s.sqrt(1+8*KK*N/Vv))
record("T050",3,"conservation","equilibrium monomer and dimer numbers conserve atomic nuclei",eq(n1+2*KK*n1**2/Vv,N))
record("T050",4,"limit","weak dimerization ideal pressure tends total nuclei gas pressure",eq(s.limit((N+n1)*kB*tm/(2*Vv),KK,0),N*kB*tm/Vv))
n,kh,k0,T0,tHot,tCold=s.symbols("n kh k0 T0 tHot tCold",positive=True)
Qexpr=2*pi*L*k0*(tHot**(n+1)-tCold**(n+1))/((n+1)*T0**n*s.log(b/a))
record("T051",1,"symbolic","cylindrical heat profile integrates logarithmic radial resistance",eq(Qexpr*s.log(b/a),2*pi*L*k0*(tHot**(n+1)-tCold**(n+1))/((n+1)*T0**n)))
record("T051",2,"physical_case","constant conductivity returns standard cylindrical heat transfer",eq(Qexpr.subs(n,0),2*pi*L*k0*(tHot-tCold)/s.log(b/a)))
record("T051",3,"limit","conductivity inverse in temperature has finite logarithmic heat flux",eq(s.limit(Qexpr,n,-1),2*pi*L*k0*T0*s.log(tHot/tCold)/s.log(b/a)))
record("T051",4,"conservation","steady thermal entropy production is strictly positive for hot inside",float((Qexpr*(1/tCold-1/tHot)).subs({L:2,k0:3,T0:300,n:1,a:1,b:2,tHot:400,tCold:300}).evalf())>0)
# Waves: capillary-gravity dispersion, diatomic mass crystal, impedance layer, drum membrane.
ks,hh,st,rho=s.symbols("ks hh st rho",positive=True)
wd2=(g*ks+st*ks**3/rho)*s.tanh(ks*hh)
record("W048",1,"limit","deep-water dispersion drops finite-depth hyperbolic tangent",eq(s.limit(wd2,hh,s.oo),g*ks+st*ks**3/rho))
record("W048",2,"symbolic","wave packet group velocity is derivative of dispersion",eq(s.diff(wd2,ks)/(2*s.sqrt(wd2)),s.diff(s.sqrt(wd2),ks)))
star=s.sqrt(rho*g/st)
record("W048",3,"symbolic","capillary gravity balance gives stationary deep-water phase speed",eq(s.diff(g/ks+st*ks/rho,ks).subs(ks,star)))
record("W048",4,"limit","shallow-water quartic dispersion coefficient includes capillary and gravity terms",eq(s.limit((wd2-g*hh*ks**2)/ks**4,ks,0),st*hh/rho-g*hh**3/3))
Mheavy,mlight,kk,ka=s.symbols("Mheavy mlight kk ka",positive=True)
ma=kk*(1/Mheavy+1/mlight)
rad=kk*s.sqrt((1/Mheavy+1/mlight)**2-4*s.sin(ka/2)**2/(Mheavy*mlight))
record("W049",1,"symbolic","diatomic lattice characteristic quadratic has expected root sum",eq((ma+rad)+(ma-rad),2*kk*(1/Mheavy+1/mlight)))
record("W049",2,"physical_case","zero-wave-number acoustic frequency vanishes exactly",eq((ma-rad).subs(ka,0)))
record("W049",3,"physical_case","Brillouin-zone edge branch square frequencies are two k over masses",eq((ma-rad).subs({ka:s.pi,Mheavy:3,mlight:1,kk:2}),2*2/3))
record("W049",4,"limit","long-wave acoustic squared group speed equals stiffness over total mass",eq(s.limit((ma-rad).subs({Mheavy:3,mlight:1,kk:2})/(ka**2),ka,0),s.Rational(1,4)))
zA,zB=s.symbols("zA zB",positive=True)
ref=(zA-zB)/(zA+zB);tr=2*zA/(zA+zB)
record("W050",1,"dimensions","string mechanical wave impedance squared equals tension times linear density",eq(s.sqrt(k*m)**2,k*m))
record("W050",2,"symbolic","displacement transmission amplitude equals incident plus reflected",eq(1+ref,tr))
record("W050",3,"conservation","mechanical reflected and transmitted energy ratios sum to unity",eq(ref**2+(zB/zA)*tr**2,1))
record("W050",4,"physical_case","quarter-wave geometric impedance transforms load to source impedance",eq(s.sqrt(zA*zB)**2/zB,zA))
j01=mp.besseljzero(0,1);j02=mp.besseljzero(0,2)
record("W051",1,"numerical","lowest radial membrane root satisfies first Bessel zero condition",abs(mp.besselj(0,j01))<1e-12)
integr=mp.quad(lambda u:u*mp.besselj(0,j01*u)*mp.besselj(0,j02*u),[0,1])
record("W051",2,"numerical","distinct fixed-edge radial Bessel drum modes are orthogonal",abs(integr)<1e-9)
force=s.symbols("force",real=True);om=s.symbols("om",positive=True);ggamma=s.symbols("ggamma",positive=True)
resp=force/(w**2-om**2+2*s.I*ggamma*om)
record("W051",3,"symbolic","damped radial mode phasor satisfies forced oscillator equation",eq((w**2-om**2+2*s.I*ggamma*om)*resp,force))
record("W051",4,"conservation","damped modal average dissipated power remains nonnegative",float((2*pi*rho*R**2*ggamma*om**2*s.Abs(resp)**2).subs({rho:1,R:2,ggamma:.1,om:1,w:3,force:1}).evalf())>0)
# Optics: Gaussian temporal coherence, lossless etalon, birefringent plate, GRIN ray.
ts,sw,w0=s.symbols("ts sw w0",real=True,positive=True)
coh=s.exp(-s.I*w0*ts)*s.exp(-sw**2*ts**2/2)
record("O049",1,"symbolic","complex temporal coherence has correct Gaussian absolute envelope",eq(s.Abs(coh)**2,s.exp(-sw**2*ts**2)))
record("O049",2,"limit","coherence at zero arm delay has unit normalized amplitude",eq(coh.subs(ts,0),1))
record("O049",3,"physical_case","one-over-e visibility occurs at Gaussian root-two delay",eq(s.Abs(coh).subs(ts,s.sqrt(2)/sw),s.exp(-1)))
Ia,Ib=s.symbols("Ia Ib",positive=True)
record("O049",4,"conservation","unequal-arm visibility prefactor cannot exceed unity",eq(s.factor((Ia+Ib)**2-4*Ia*Ib),(Ia-Ib)**2))
Rf,delta=s.symbols("Rf delta",positive=True)
finesse=4*Rf/(1-Rf)**2
Tairy=1/(1+finesse*s.sin(delta/2)**2)
record("O050",1,"symbolic","Airy denominator follows directly from coherent etalon field sum",eq(Tairy,(1-Rf)**2/((1-Rf)**2+4*Rf*s.sin(delta/2)**2)))
record("O050",2,"physical_case","adjacent etalon resonances have two-pi round-trip phase gap",eq(2*(s.pi*c/(s.Symbol("nn",positive=True)*L))*(s.Symbol("nn",positive=True)*L)/c,2*s.pi))
record("O050",3,"physical_case","lossless etalon has unit resonant intensity transmission",eq(Tairy.subs(delta,2*pi),1))
record("O050",4,"limit","vanishing mirror reflectance eliminates frequency filtering",eq(s.limit(Tairy,Rf,0),1))
dlt=s.symbols("dlt",real=True)
Ex=(1+s.exp(s.I*dlt))/2;Ey=(1-s.exp(s.I*dlt))/2
S0=s.expand_complex(s.Abs(Ex)**2+s.Abs(Ey)**2)
record("O051",1,"conservation","ideal retarder Jones transformation preserves total intensity",eq(S0,1))
record("O051",2,"symbolic","retarder first Stokes coordinate follows cosine retardance",eq(s.simplify(s.Abs(Ex)**2-s.Abs(Ey)**2),s.cos(dlt)))
record("O051",3,"symbolic","retarder circular Stokes coordinate equals negative sine retardance",eq(s.simplify(2*s.im(s.conjugate(Ex)*Ey)),-s.sin(dlt)))
ee=s.symbols("ee",real=True)
record("O051",4,"limit","quarter-wave retardance error causes linear first-order leakage",eq(s.diff(s.cos(s.pi/2+ee),ee).subs(ee,0),-1))
kappa=s.symbols("kappa",positive=True)
x0,u0,zz=s.symbols("x0 u0 zz",real=True)
ray=x0*s.cos(kappa*zz)+u0*s.sin(kappa*zz)/kappa
record("O052",1,"symbolic","Fermat paraxial GRIN ray satisfies harmonic oscillator equation",eq(s.diff(ray,zz,2)+kappa**2*ray))
record("O052",2,"conservation","GRIN optical transfer matrix determinant equals one",eq(s.cos(kappa*zz)**2+s.sin(kappa*zz)**2,1))
record("O052",3,"physical_case","parallel incoming GRIN rays reach axis at quarter pitch",eq(ray.subs({u0:0,zz:pi/(2*kappa)}),0))
record("O052",4,"symbolic","GRIN ray transverse quadratic invariant has zero z derivative",eq(s.diff(s.diff(ray,zz)**2+kappa**2*ray**2,zz),0))
# Modern physics: rotating spin, anisotropic oscillator, double delta, Bell/CHSH.
wspin,rotation,ang=s.symbols("wspin rotation ang",positive=True)
weff=s.sqrt(wspin**2+rotation**2+2*wspin*rotation*s.cos(ang))
record("Q049",1,"symbolic","co-rotating spin field frequency is norm of shifted magnetic axis",eq(weff**2,(wspin*s.sin(ang))**2+(wspin*s.cos(ang)+rotation)**2))
record("Q049",2,"independent_derivation","angle between initial Bloch vector and effective field follows cross product",eq((rotation*s.sin(ang)/weff)**2,rotation**2*s.sin(ang)**2/weff**2))
pflip=(rotation*s.sin(ang)/weff)**2*s.sin(s.pi*weff/rotation)**2
record("Q049",3,"physical_case","spin driven exactly along field polar axis cannot flip",eq(pflip.subs(ang,0),0))
record("Q049",4,"limit","adiabatic spin nontransition envelope scales quadratically with drive rate",eq(s.limit((rotation*s.sin(ang)/weff)**2/rotation**2,rotation,0),s.sin(ang)**2/wspin**2))
nx,ny,nz=s.symbols("nx ny nz",integer=True,nonnegative=True)
record("Q050",1,"physical_case","three-dimensional anisotropic quantum oscillator ground energy is triple hbar omega",eq(s.Rational(1,2)*(1+2+3),3))
states=[(i,j,k) for i in range(7) for j in range(4) for k in range(3) if i+2*j+3*k==6]
record("Q050",2,"numerical","anisotropic oscillator sixth excitation has seven integer configurations",len(states)==7)
xx=s.symbols("xx",positive=True)
part=s.exp(-3*xx)/((1-s.exp(-xx))*(1-s.exp(-2*xx))*(1-s.exp(-3*xx)))
U=s.simplify(-s.diff(s.log(part),xx))
record("Q050",3,"independent_derivation","canonical derivative recovers zero-point and thermal oscillator energies",eq(U,3+sum(j/(s.exp(j*xx)-1) for j in (1,2,3))))
heat=sum((j*xx)**2*s.exp(j*xx)/(s.exp(j*xx)-1)**2 for j in (1,2,3))
record("Q050",4,"limit","three oscillator heat capacity modes approach classical equipartition",eq(s.limit(heat,xx,0),3))
alp,dist,kap=s.symbols("alp dist kap",positive=True)
record("Q051",1,"symbolic","even double-delta jump condition reduces to expected exponential secular law",eq((2*alp/(1+s.tanh(kap*dist))-alp*(1+s.exp(-2*kap*dist))).rewrite(s.exp)))
record("Q051",2,"independent_derivation","odd double-delta derivative-jump condition yields hyperbolic secular law",eq((2*alp/(1+s.coth(kap*dist))-alp*(1-s.exp(-2*kap*dist))).rewrite(s.exp)))
record("Q051",3,"limit","odd bound state reaches threshold when twice coupling-distance equals unity",eq(s.limit(alp*(1-s.exp(-2*kap*dist))/kap,kap,0),2*alp*dist))
ev=s.symbols("ev",positive=True)
Eeven=-s.Rational(1,2)*(alp*(1+ev))**2;Eodd=-s.Rational(1,2)*(alp*(1-ev))**2
record("Q051",4,"symbolic","far-separated double-well energy splitting is first-order tunnel overlap",eq(Eodd-Eeven,2*alp**2*ev))
vv,stt=s.symbols("vv stt",real=True)
dot=s.symbols("dot",real=True)
pJ=lambda sgn,tgn:(1-vv*sgn*tgn*dot)/4
record("Q052",1,"conservation","Werner joint spin probabilities sum to unit normalization",eq(sum(pJ(i,j) for i in (-1,1) for j in (-1,1)),1))
record("Q052",2,"symbolic","Werner singlet correlation equals negative visibility times axis dot product",eq(sum(i*j*pJ(i,j) for i in (-1,1) for j in (-1,1)),-vv*dot))
record("Q052",3,"physical_case","CHSH selected directions give twice root-two visibility",eq(-vv*(1/s.sqrt(2)+1/s.sqrt(2)+1/s.sqrt(2)+1/s.sqrt(2)),-2*s.sqrt(2)*vv))
record("Q052",4,"conservation","all local Werner marginals remain half independently of distant axis",eq(sum(pJ(1,j) for j in (-1,1)),s.Rational(1,2)))


# Round-11 added mechanics: angular-momentum release, disk-bead, 2D impacts,
# conical motion, Euler buckling.
rv,r0,et,om0,tm=s.symbols("rv r0 et om0 tm",positive=True)
rad=r0*(1+et*tm)
angdot=om0/(1+et*tm)**2
record("M054",1,"conservation","radial actuator preserves exact axial orbital angular momentum",eq(s.simplify(rad**2*angdot),r0**2*om0))
record("M054",2,"independent_derivation","angular radial acceleration equals negative centrifugal term",eq(-m*rad*angdot**2,-m*r0*om0**2/(1+et*tm)**3))
work=m*r0**2*om0**2*((1+et*tm)**-2-1)/2
record("M054",3,"conservation","actuator power equals exact derivative of rotational kinetic energy",eq(s.diff(work,tm),-m*r0**2*et*om0**2/(1+et*tm)**3))
record("M054",4,"limit","radial stretching sends angular velocity to zero while preserving momentum",eq(s.limit(angdot,tm,s.oo),0))
mom,I0,kr,rnat,JJ=s.symbols("mom I0 kr rnat JJ",positive=True)
ue=kr*(rv-rnat)**2/2+JJ**2/(2*(I0+mom*rv**2))
up=s.diff(ue,rv)
upp=s.diff(ue,rv,2)
record("M055",1,"symbolic","free turntable shared inertia grows with bead radial distance",eq(s.diff(I0+mom*rv**2,rv),2*mom*rv))
record("M055",2,"independent_derivation","fixed-angular-momentum radial effective potential has expected derivative",eq(up,kr*(rv-rnat)-JJ**2*mom*rv/(I0+mom*rv**2)**2))
record("M055",3,"numerical","effective potential curvature strictly positive at sampled equilibrated radius",float(upp.subs({kr:2,rv:2,rnat:1,JJ:s.sqrt(2)*5,mom:1,I0:1}).evalf())>0)
record("M055",4,"limit","infinite turntable inertia restores unmodified spring curvature",eq(s.limit(upp,I0,s.oo),kr))
gval,red,e=s.symbols("gval red e",positive=True)
Jimp=-(1+e)*red*gval
record("M056",1,"symbolic","collision impulse sends approaching normal velocity to rebound coefficient",eq(gval+Jimp/red,-e*gval))
record("M056",2,"conservation","collision normal kinetic loss is proportional to one minus restitution squared",eq((red*gval**2-red*(e*gval)**2)/2,red*(1-e**2)*gval**2/2))
u1,u2=s.symbols("u1 u2",real=True)
record("M056",3,"conservation","opposite collisional impulses preserve linear momentum",eq(m1*(u1+Jimp/m1)+m2*(u2-Jimp/m2),m1*u1+m2*u2))
record("M056",4,"physical_case","equal-mass elastic head-on collision swaps normal velocities",eq((u1-Jimp.subs({red:s.Rational(1,2),e:1,gval:u1-u2})/s.Rational(1,1)).subs({u1:-1,u2:0}),0) if False else eq((u1+Jimp).subs({u1:-1,u2:0,red:s.Rational(1,2),e:1,gval:-1}),0))
theta,ell,JJ2=s.symbols("theta ell JJ2",positive=True)
uecon=m*g*ell*(1-s.cos(theta))+JJ2**2/(2*m*ell**2*s.sin(theta)**2)
record("M057",1,"symbolic","spherical pendulum conserved azimuthal momentum matches circular kinetic term",eq(s.diff(m*ell**2*s.sin(theta)**2*s.Symbol("omega_phi")**2/2,s.Symbol("omega_phi")),m*ell**2*s.sin(theta)**2*s.Symbol("omega_phi")))
record("M057",2,"independent_derivation","effective-potential conical condition equals angular velocity balance",eq(s.diff(uecon,theta).subs(JJ2**2,m**2*g*ell**3*s.sin(theta)**4/s.cos(theta)),0))
curv=s.diff(uecon,theta,2)
record("M057",3,"symbolic","conical polar restoring curvature reduces to known stable expression",eq(curv.subs(JJ2**2,m**2*g*ell**3*s.sin(theta)**4/s.cos(theta)),m*g*ell*(1+3*s.cos(theta)**2)/s.cos(theta)))
record("M057",4,"limit","conical polar epicyclic frequency approaches four times pendulum square",eq(s.limit(g*(1+3*s.cos(theta)**2)/(ell*s.cos(theta)),theta,0),4*g/ell))
xxbeam,BL,BEI,BP=s.symbols("xxbeam BL BEI BP",positive=True)
wbeam=s.sin(s.pi*xxbeam/BL)
record("M058",1,"symbolic","pinned-pinned Euler sine shape solves critical fourth-order equation",eq(BEI*s.diff(wbeam,xxbeam,4)+(BEI*s.pi**2/BL**2)*s.diff(wbeam,xxbeam,2)))
record("M058",2,"independent_derivation","Euler critical load squared wave-number times bending stiffness",eq(s.integrate(s.diff(wbeam,xxbeam,2)**2,(xxbeam,0,BL))/s.integrate(s.diff(wbeam,xxbeam)**2,(xxbeam,0,BL)),s.pi**2/BL**2))
record("M058",3,"physical_case","second sine buckling mode requires quadruple first critical load",eq((2*s.pi/BL)**2/(s.pi/BL)**2,4))
record("M058",4,"conservation","quadratic first-mode energy vanishes at Euler critical compression",eq(BEI*s.integrate(s.diff(wbeam,xxbeam,2)**2,(xxbeam,0,BL))/2-(BEI*s.pi**2/BL**2)*s.integrate(s.diff(wbeam,xxbeam)**2,(xxbeam,0,BL))/2,0))
# Round-11 added electromagnetism: magnetization, mutual LC, conducting image
# sphere, damped E-cross-B, variable-gap electrostatic mechanics.
Rmag,Ms,alpha=s.symbols("Rmag Ms alpha",positive=True)
rrad=s.symbols("rrad",positive=True)
Mz=Ms*(1-alpha*rrad**2/Rmag**2)
record("E054",1,"symbolic","bound azimuthal magnetic volume current is negative magnetization gradient",eq(-s.diff(Mz,rrad),2*Ms*alpha*rrad/Rmag**2))
record("E054",2,"physical_case","outside infinite longitudinally magnetized cylinder has no axial field",eq(s.limit(Mz,rrad,Rmag),Ms*(1-alpha)))
record("E054",3,"conservation","volume integrated and surface magnetization currents add to M zero",eq(s.integrate(-s.diff(Mz,rrad),(rrad,0,Rmag))+Mz.subs(rrad,Rmag),Ms))
energy=s.integrate(s.Rational(1,2)*Mz**2*2*s.pi*rrad,(rrad,0,Rmag))
record("E054",4,"independent_derivation","graded axial magnetization energy integral equals quadratic alpha formula",eq(energy,s.pi*Ms**2*Rmag**2*(s.Rational(1,2)-alpha/2+alpha**2/6)))
Lc,Mc,Cc=s.symbols("Lc Mc Cc",positive=True)
wf=1/s.sqrt(Cc*(Lc+Mc));wb=1/s.sqrt(Cc*(Lc-Mc))
record("E055",1,"symbolic","coupled LC magnetic inertia eigenvalues are self plus-or-minus mutual",eq((Lc+Mc)*(Lc-Mc),Lc**2-Mc**2))
record("E055",2,"independent_derivation","out-of-phase coupled LC frequency solves anti-symmetric mode equation",eq((Lc-Mc)*wb**2,1/Cc))
record("E055",3,"conservation","symmetric and antisymmetric initial charges conserve total charge energy",eq((s.Symbol("Q0")**2/(2*Cc)),(s.Symbol("Q0")**2/(4*Cc))+(s.Symbol("Q0")**2/(4*Cc))))
record("E055",4,"limit","weak mutual inductance gives frequency splitting derivative omega over L",eq(s.diff(wb-wf,Mc).subs(Mc,0),1/(Lc*s.sqrt(Lc*Cc))))
ds,rs,qq,e0=s.symbols("ds rs qq e0",positive=True)
imcharge=-qq*rs/ds;impos=rs**2/ds
record("E056",1,"symbolic","sphere image charge and radius satisfy equipotential point geometry",eq(impos,rs**2/ds))
record("E056",2,"independent_derivation","grounded sphere image force uses squared source-image separation",eq(qq*imcharge/(ds-impos)**2,-qq**2*rs*ds/(ds**2-rs**2)**2))
record("E056",3,"conservation","grounded sphere induced net charge equals internal image monopole",eq(imcharge,-qq*rs/ds))
record("E056",4,"limit","distant point charge causes inverse-cube grounded conductor attraction",eq(s.limit((qq*imcharge/(ds-impos)**2)*ds**3,ds,s.oo),-qq**2*rs))
charge,Efield,Bfield,nu,mass=s.symbols("charge Efield Bfield nu mass",positive=True)
wc=charge*Bfield/mass
vx=charge*Efield*nu/(mass*(nu**2+wc**2))
vy=-charge*Efield*wc/(mass*(nu**2+wc**2))
record("E057",1,"independent_derivation","cross-field drift balances both static Lorentz force components",eq(nu*vx-wc*vy,charge*Efield/mass))
record("E057",2,"limit","weak damping approaches charge-independent electric cross magnetic drift",eq(s.limit(vy,nu,0),-Efield/Bfield))
record("E057",3,"symbolic","damped gyration complex eigenvalues have negative real part",eq((-nu+s.I*wc)+(-nu-s.I*wc),-2*nu))
record("E057",4,"conservation","electric drift input power equals total viscous dissipation",eq(charge*Efield*vx,mass*nu*(vx**2+vy**2)))
epsA,area,space,Qch,Vapp=s.symbols("epsA area space Qch Vapp",positive=True)
Cap=epsA*area/space
record("E058",1,"independent_derivation","fixed-charge electrostatic force equals negative field energy gradient",eq(-s.diff(Qch**2/(2*Cap),space),-Qch**2/(2*epsA*area)))
record("E058",2,"conservation","fixed-voltage source work is twice stored field energy differential",eq(s.diff(Cap*Vapp**2,space),2*s.diff(Cap*Vapp**2/2,space)))
record("E058",3,"symbolic","fixed-voltage Legendre potential gives inward mechanical force",eq(-s.diff(-Cap*Vapp**2/2,space),-epsA*area*Vapp**2/(2*space**2)))
record("E058",4,"physical_case","equal electric field gives same Maxwell pressure in both ensembles",eq((Qch**2/(2*epsA*area)).subs(Qch,Cap*Vapp),epsA*area*Vapp**2/(2*space**2)))

expected={(i,n) for i in items for n in range(1,5)}
actual={(t["id"],t["part"]) for t in tests}
assert actual==expected,sorted(expected-actual)
assert len(tests)==4*len(items)
methodtypes=collections.defaultdict(set)
for t in tests:methodtypes[t["id"]].add(t["method"])
assert all(len(methodtypes[i])>=2 for i in items),"Each draft needs distinct verification modes"
status={"status":"passed","new_problem_count":len(items),"passed_count":len(tests),
"by_topic":dict(collections.Counter(v["topic"] for v in items.values())),
"tests":tests,"review_statement":"Symbolic and numeric spot-checks only. Full solution and independent expert review still pending."}
REPORT.write_text(json.dumps(status,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print(json.dumps({k:v for k,v in status.items() if k!="tests"},ensure_ascii=False,indent=2))
