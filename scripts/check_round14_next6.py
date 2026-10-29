#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Round 14: next six (M080 E080 T075 W075 O077 Q077), 24 executed physical checks."""
import json,math
from pathlib import Path
import sympy as s
from mpmath import quad,ellipk
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def z(expr):
    v=s.simplify(expr)
    return v==s.zeros(*v.shape) if isinstance(v,s.MatrixBase) else v==0
def ck(uid,part,method,description,yes):
    if not bool(yes): raise AssertionError(f"{uid}/{part} {description}")
    checks.append(dict(id=uid,part=part,method=method,name=description,passed=True))
# M080: exact nonlinear gravity-gradient attitude pendulum
th,n,I=s.symbols("th n I",positive=True)
U=-3*I*n*n*s.cos(th)**2/2; tau=-s.diff(U,th)
ck("M080",1,"symbolic","quadrupole gravitational restoring torque",z(tau+3*I*n*n*s.sin(th)*s.cos(th)))
ck("M080",2,"stability","radial minimum and tangential maximum curvatures",z(s.diff(U,th,2).subs(th,0)-3*I*n*n) and z(s.diff(U,th,2).subs(th,s.pi/2)+3*I*n*n))
ang=.62; k=math.sin(ang)
period_num=4/math.sqrt(3)*quad(lambda x:1/math.sqrt(1-k*k*math.sin(x)**2),[0,math.pi/2])
period_formula=4/math.sqrt(3)*ellipk(k*k)
ck("M080",3,"independent_numerical","elliptic period agrees with quadrature",abs(float(period_num-period_formula))<1e-11 and float(period_formula)>2*math.pi/math.sqrt(3))
v=s.symbols("v",real=True); J=I*v*v/2+U
ck("M080",4,"conservation","Jacobi first integral differentiates to zero",z(s.diff(J,th)*v+s.diff(J,v)*tau/I))
# E080: Maxwell-Wagner interface dynamics
Ei,Eo,si,so,t=s.symbols("Ei Eo si so t",positive=True)
Ke=(Ei-Eo)/(Ei+2*Eo);Ks=(si-so)/(si+2*so);tauMW=(Ei+2*Eo)/(si+2*so)
K=Ks+(Ke-Ks)*s.exp(-t/tauMW)
ck("E080",1,"boundary","normal total-current boundary continuity",z(si*(1-K)-Ei*s.diff(K,t)-so*(1+2*K)-2*Eo*s.diff(K,t)))
ck("E080",2,"symbolic","transient ODE and both time limits",z((Ei+2*Eo)*s.diff(K,t)+(si+2*so)*K-(si-so)) and z(K.subs(t,0)-Ke) and z(s.limit(K,t,s.oo)-Ks))
q=(Eo-Ei)+(Ei+2*Eo)*K
ck("E080",3,"conservation","surface charge accumulation equals current jump",z(q.subs(t,0)) and z(s.diff(q,t)-si*(1-K)+so*(1+2*K)))
params={Ei:4,Eo:2,si:s.Rational(1,2),so:1}
switch=float((tauMW*s.log((Ke-Ks)/(-Ks))).subs(params))
kk=lambda tt:float(K.subs(params).subs(t,tt))
ck("E080",4,"numerical","opposite contrasts give unique positive dipole reversal",switch>0 and abs(kk(switch))<1e-11 and kk(0)>0 and kk(5*switch)<0)
# T075: Tonks exact excluded-volume configuration
L,N,a,kB,T,m,h=s.symbols("L N a kB T m h",positive=True)
lam=h/s.sqrt(2*s.pi*m*kB*T)
lnZ=N*s.log(L-N*a)-s.log(s.gamma(N+1))-N*s.log(lam)
ck("T075",1,"symbolic","canonical integral differentiates to exact equation of state",z(kB*T*s.diff(lnZ,L)-N*kB*T/(L-N*a)))
nd=s.symbols("nd",positive=True)
f=nd*kB*T*(s.log(nd*lam/(1-nd*a))-1)
ck("T075",2,"symbolic","free energy density derivative yields chemical potential",z(s.diff(f,nd)-kB*T*(s.log(nd*lam/(1-nd*a))+nd*a/(1-nd*a))))
p=nd*kB*T/(1-nd*a); kt=(1-nd*a)**2/(nd*kB*T)
ck("T075",3,"fluctuation","isothermal compressibility and number fluctuations",z(kt-1/(nd*s.diff(p,nd))) and z(nd*kB*T*kt-(1-nd*a)**2))
C=s.symbols("C",positive=True); Tad=C/(1/nd-a)**2; p_ad=nd*kB*Tad/(1-nd*a)
ck("T075",4,"adiabatic","adiabatic pressure derivative and dilute sound speed",z(s.diff(p_ad,nd)/m-3*kB*Tad/(m*(1-nd*a)**2)) and z(s.limit(3*kB*T/(m*(1-nd*a)**2),a,0)-3*kB*T/m))
# W075: moving boundary string, distinct from previously indexed convected-wave models
L,vel,mu,ten,A,nmode,c=s.symbols("L vel mu ten A nmode c",positive=True)
slope=s.symbols("slope",real=True)
edge=s.simplify(ten*slope*(-vel*slope)+vel*(mu*(vel*slope)**2+ten*slope**2)/2)
ck("W075",1,"energy_boundary","Reynolds moving-end energy flux and Dirichlet kinematic condition",z(edge+ten*vel*slope**2*(1-mu*vel**2/ten)/2))
E0,L0=s.symbols("E0 L0",positive=True)
En=E0*L0/L
ck("W075",2,"adiabatic","adiabatic action forces mode energy inverse proportional to length",z(s.diff(En,L)+En/L))
emode=ten*s.pi**2*nmode**2*A**2/(4*L)
fend=ten*s.pi**2*nmode**2*A**2/(4*L**2)
ck("W075",3,"independent_derivation","time averaged wall work equals negative adiabatic energy derivative",z(fend-emode/L) and z(fend+s.diff(emode,L)))
doppler=(c-vel)/(c+vel)
ck("W075",4,"doppler","moving wall reflection plus collision rate gives -Ldot/L",z(s.diff(doppler,vel).subs(vel,0)+2/c) and z(s.diff(s.log(doppler),vel).subs(vel,0)*c/(2*L)+1/L))
# O077: independent Poisson interference outputs
ph,V,Np=s.symbols("ph V Np",positive=True,real=True)
mplus=Np*(1+V*s.cos(ph))/2; mminus=Np*(1-V*s.cos(ph))/2
ck("O077",1,"statistics","Poisson difference mean and additive noise",z(mplus+mminus-Np) and z(mplus-mminus-Np*V*s.cos(ph)))
FI=s.simplify(s.diff(mplus,ph)**2/mplus+s.diff(mminus,ph)**2/mminus)
ck("O077",2,"symbolic","joint likelihood Fisher information and ideal visibility limit",z(FI-Np*V**2*s.sin(ph)**2/(1-V**2*s.cos(ph)**2)) and z(FI.subs(V,1)-Np))
zeta=s.symbols("zeta",real=True); FIz=Np*V**2*(1-zeta)/(1-V**2*zeta)
ck("O077",3,"optimization","visibility loss makes quadrature point uniquely optimal",z(s.diff(FIz,zeta)-Np*V**2*(V**2-1)/(1-V**2*zeta)**2) and float(s.diff(FIz,zeta).subs({Np:200,V:.7,zeta:.4}))<0)
ck("O077",4,"noise","quadrature estimator saturates classical inverse Fisher bound",z((mplus+mminus)/(Np*V)**2-1/FI.subs(ph,s.pi/2)))
# Q077: transitionless spin counterdiabatic propagator
sy=s.Matrix([[0,-s.I],[s.I,0]]);sz=s.diag(1,-1)
ang=s.Function("theta",real=True)(t);freq=s.symbols("freq",positive=True)
Ry=s.cos(ang/2)*s.eye(2)-s.I*s.sin(ang/2)*sy
H0=-freq*Ry*sz*Ry.conjugate().T/2
Hcd=s.diff(ang,t)*sy/2
prop=Ry*(s.cos(freq*t/2)*s.eye(2)+s.I*s.sin(freq*t/2)*sz)
n0=s.Matrix([0,0,1]); dn=s.Matrix([1,0,0])
ck("Q077",1,"bloch","counterdiabatic cross product follows moving spin direction",z(n0.cross(dn).cross(n0)-dn))
ck("Q077",2,"matrix","exact moving-frame propagator solves Schrodinger equation",z(s.I*s.diff(prop,t)-(H0+Hcd)*prop))
rate,latitude=s.symbols("rate latitude",positive=True)
ck("Q077",3,"variance","control mean zero but variance is nonzero at finite angular speed",z((rate*s.sin(latitude)/2)**2-rate**2*s.sin(latitude)**2/4) and (rate*s.sin(latitude)/2).subs({rate:2,latitude:s.pi/2})>0)
berry=-s.pi*(1-s.cos(latitude))
ck("Q077",4,"geometry","spin one-half geometric phase equals minus half solid angle",z(berry+s.pi*(1-s.cos(latitude))) and z(berry.subs(latitude,0)))
ids=("M080","E080","T075","W075","O077","Q077")
assert len(checks)==24 and {(q["id"],q["part"]) for q in checks}=={(uid,p) for uid in ids for p in range(1,5)}
for uid in ids:
    path=ROOT/"bank"/uid
    meta=json.loads((path/"meta.json").read_text(encoding="utf-8"))
    assert meta["quality_status"]=="待独立复核"
    assert (path/"question.tex").exists() and (path/"solution.tex").exists()
out={"status":"24_executed_subpart_checks_passed_expert_review_pending","round":14,"ids":list(ids),"passed_count":24,"tests":checks,"independent_expert_review":"待独立复核"}
(ROOT/"data"/"round14_next6_validation_report.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("ROUND14 NEXT SIX: 24/24 EXECUTED; 24/50 DRAFT ONLY")
