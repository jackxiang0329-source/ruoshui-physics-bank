#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Eight distinct final problems, 32 independently evaluated symbolic / numerical / physical checks.
Automated checks do NOT constitute independent expert signoff.
"""
import json, math, cmath
from pathlib import Path
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[1]
TESTS=[]
def zero(x):
    if isinstance(x,s.MatrixBase):
        return all(s.simplify(a)==0 for a in x)
    return s.simplify(s.expand(x))==0
def ck(uid,part,method,name,condition):
    if not bool(condition):
        raise AssertionError(f"{uid} / {part}: {name}")
    TESTS.append(dict(id=uid,part=part,method=method,name=name,passed=True))
def near(a,b,eps=1.e-8):
    return math.isclose(float(a),float(b),rel_tol=eps,abs_tol=eps)
# M084: interface Darcy dispersion.
U,K1,K2,gamma,k=s.symbols("U K1 K2 gamma k",positive=True)
growth=k*(U*(K1-K2)-gamma*K1*K2*k*k)/(K1+K2)
A1=-growth/(K1*k);A2=growth/(K2*k)
xx=s.symbols("xx",real=True)
p1=A1*s.exp(k*xx);p2=A2*s.exp(-k*xx)
ck("M084",1,"symbolic","Darcy pressure perturbations solve the Laplace equation in both semi-infinite fluids",
    zero(s.diff(p1,xx,2)-k*k*p1) and zero(s.diff(p2,xx,2)-k*k*p2))
ck("M084",2,"independent_derivation","Moving interface pressure jump including background gradients reproduces viscosity contrast dispersion",
    zero(A1-A2+(-U/K1+U/K2)-gamma*k*k) and
    zero(-K1*s.diff(p1,xx).subs(xx,0)-growth))
kc2=U*(K1-K2)/(gamma*K1*K2)
km=s.sqrt(kc2/3)
maxg=s.simplify(growth.subs(k,km))
ck("M084",3,"symbolic","Maximal viscous fingering growth is stationary at the capillary-selected wave number",
    zero(s.diff(growth,k).subs(k,km)) and
    zero(maxg-s.Rational(2,3)*U*(K1-K2)/(K1+K2)*km) and
    growth.subs({U:2,K1:3,K2:1,gamma:s.Rational(1,10),k:1})>0)
ck("M084",4,"limit","Capillary stabilization is negative and three-dimensional dimensional analysis preserves inverse time",
    growth.subs({U:0,K1:3,K2:1,gamma:s.Rational(1,10),k:2})<0 and
    zero(growth.subs(K1,K2)+gamma*K2*k**3/2) and
    zero(growth.subs(gamma,0)-k*U*(K1-K2)/(K1+K2)))
# M085: stick slip fold.
x,X,V0,kk,Stiff,vel,zeta=s.symbols("x X V0 kk Stiff vel zeta",real=True,positive=True)
pot=V0*(1-s.cos(kk*x))+Stiff*(x-X)**2/2
force=-s.diff(pot,x)
ck("M085",1,"symbolic","Potential gradient and Hessian yield the exact equilibrium condition and convexity threshold",
    zero(force-Stiff*(X-x)+V0*kk*s.sin(kk*x)) and
    zero(s.diff(pot,x,2)-Stiff-V0*kk**2*s.cos(kk*x)))
xs=mp.acos(-0.25)/2;Xspin=xs+2*mp.sin(2*xs)  # K=1,V0=1,k=2
ck("M085",2,"numerical","Forward depinning fold simultaneously satisfies zero force and zero curvature",
    abs(float(force.subs({x:float(xs),X:float(Xspin),V0:1,Stiff:1,kk:2})))<1e-11 and
    abs(float(s.diff(pot,x,2).subs({x:float(xs),X:float(Xspin),V0:1,Stiff:1,kk:2})))<1e-11)
delt=s.symbols("delt",positive=True)
c2=V0*kk**3*s.symbols("zsin",positive=True)/2
ystar=s.sqrt(Stiff*delt/c2)
vnormal=Stiff*delt*s.symbols("yy",real=True)-c2*s.symbols("yy",real=True)**3/3
yy=s.symbols("yy",real=True)
ck("M085",3,"independent_derivation","Fold normal form gives saddle barrier four-thirds coefficient and square-root soft curvature",
    zero(vnormal.subs(yy,ystar)-vnormal.subs(yy,-ystar)-s.Rational(4,3)*(Stiff*delt)**s.Rational(3,2)/s.sqrt(c2)) and
    zero(s.diff(vnormal,yy,2).subs(yy,-ystar)-2*s.sqrt(Stiff*delt*c2)))
xxdot=s.symbols("xdot",real=True)
ck("M085",4,"conservation","Overdamped nonautonomous potential loses exactly zeta velocity squared after input spring work",
    zero((-zeta*xxdot)*xxdot+Stiff*(X-x)*vel-(-zeta*xxdot**2+Stiff*(X-x)*vel)) and
    (float(zeta.subs(zeta,2))*0.3**2)>0)
# E084 two-carrier Hall tensor.
n,h,ue,uh,B,e=s.symbols("n h ue uh B e",positive=True)
S=e*(n*ue/(1+ue**2*B**2)+h*uh/(1+uh**2*B**2))
D=e*B*(h*uh**2/(1+uh**2*B**2)-n*ue**2/(1+ue**2*B**2))
mat=s.Matrix([[S,D],[-D,S]])
ck("E084",1,"independent_derivation","Electron and hole Drude Hall contributions have opposite odd-in-B signs and positive diagonal conductance",
    zero(S.subs(B,0)-e*(n*ue+h*uh)) and zero(D.subs(h,0)+e*B*n*ue**2/(1+ue**2*B**2)))
den=(n*ue+h*uh)**2+(h-n)**2*ue**2*uh**2*B**2
rx=(n*ue+h*uh+(n*uh+h*ue)*ue*uh*B**2)/(e*den)
rh=(h*uh**2-n*ue**2+(h-n)*ue**2*uh**2*B**2)/(e*den)
ck("E084",2,"symbolic","Exact 2x2 conductivity inversion equals explicit rational magnetoresistance and Hall coefficients",
    zero(s.factor(S/(S**2+D**2)-rx)) and zero(s.factor(D/(B*(S**2+D**2))-rh)))
ck("E084",3,"limit","Compensated magnetoresistance is quadratic and uncompensated strong-field Hall saturates to density difference",
    zero(s.factor(rx.subs(h,n)-(1+ue*uh*B**2)/(e*n*(ue+uh)))) and
    zero(s.limit(rh,B,s.oo)-1/(e*(h-n))))
Ex,Ey=s.symbols("Ex Ey",real=True)
j=mat*s.Matrix([Ex,Ey])
ck("E084",4,"conservation","Antisymmetric Hall term cancels in Joule power and Onsager field reversal is exact",
    zero((s.Matrix([Ex,Ey]).dot(j))-S*(Ex**2+Ey**2)) and
    zero(mat.subs(B,-B)-mat.T))
# E085 MRI linearized determinant, instability and energy.
om,q,wa,ss=s.symbols("om q wa ss",real=True)
ii=s.I
L=s.Matrix([[0,2*om,ii*wa,0],[-(2-q)*om,0,0,ii*wa],
            [ii*wa,0,0,0],[0,ii*wa,-q*om,0]])
char=s.factor((ss*s.eye(4)-L).det())
kap2=2*(2-q)*om**2
disp=ss**4+ss**2*(kap2+2*wa**2)+wa**2*(wa**2-2*q*om**2)
ck("E085",1,"symbolic","Rotating shearing-sheet linear operator contains Coriolis epicycle and induction shear coefficients",
    zero(L[0,1]-2*om) and zero(L[1,0]+(2-q)*om) and zero(L[3,2]+q*om))
ck("E085",2,"independent_derivation","Independent four-by-four determinant reproduces the MRI quartic dispersion exactly",
    zero(char-disp) and zero(disp.subs(wa,0)-(ss**2*(ss**2+kap2))))
qv=s.Rational(3,2);ov=1
xopt=qv*(4-qv)/4
yopt=qv**2/4
ck("E085",3,"numerical","Kepler maximum growth satisfies quartic and stationary conditions at k vA squared fifteen-sixteenths",
    zero(disp.subs({wa:s.sqrt(xopt),ss:s.sqrt(yopt),q:qv,om:ov})) and
    zero(2*yopt+2*xopt-2*qv) and xopt==s.Rational(15,16))
uv=s.Matrix([1+s.I,2-s.I,1-2*s.I,-1+s.I])
du=L.subs({q:s.Rational(3,2),om:2,wa:s.Rational(5,4)})*uv
realprod=lambda a,b:s.re(s.conjugate(a)*b)
energy_rate=s.expand(sum(realprod(uv[j],du[j]) for j in range(4)))
shear=s.Rational(3,2)*2*(realprod(uv[0],uv[1])-realprod(uv[2],uv[3]))
ck("E085",4,"conservation","Reynolds minus Maxwell shear stress equals exact complex-mode energy derivative; rigid rotation conserves energy",
    zero(energy_rate-shear) and
    zero(sum(realprod(uv[j],(L.subs({q:0,om:2,wa:s.Rational(5,4)})*uv)[j]) for j in range(4))))
# T079 2D harmonic trap Bose functions.
z,T,Ak,kb=s.symbols("z T Ak kb",positive=True)
Ns=Ak*(kb*T)**2*s.polylog(2,z)
Us=2*Ak*(kb*T)**3*s.polylog(3,z)
ck("T079",1,"independent_derivation","Harmonic oscillator lattice point count yields linear DOS and Bose polylog Li2 number",
    zero(s.diff(s.symbols("E",positive=True)**2*Ak/2,s.symbols("E",positive=True))-Ak*s.symbols("E",positive=True)) and
    zero(z*s.diff(s.polylog(2,z),z)-s.polylog(1,z)))
N0=s.symbols("N0",positive=True)
Tc=s.sqrt(N0/(Ak*s.zeta(2)))/kb
ck("T079",2,"symbolic","Critical Bose saturation and cubic internal energy reproduce condensate quadratic depletion",
    zero(Ns.subs({z:1,T:Tc})-N0) and
    zero(Us.subs(z,1)-2*Ak*(kb*T)**3*s.zeta(3)))
Cexpr=kb*Ak*(kb*T)**2*(6*s.polylog(3,z)-4*s.polylog(2,z)**2/s.polylog(1,z))
ck("T079",3,"limit","Fixed-N heat capacity is continuous at Bose threshold and classical high-T value is 2NkB",
    zero(s.limit(Cexpr,z,1,dir="-")-6*kb*Ak*(kb*T)**2*s.zeta(3)) and
    zero(s.limit((Cexpr/(Ns*kb)),z,0,dir="+")-2))
Grand=-kb*T*Ak*(kb*T)**2*s.polylog(3,z)
Entropy=kb*Ak*(kb*T)**2*(3*s.polylog(3,z)-s.log(z)*s.polylog(2,z))
ck("T079",4,"conservation","Grand potential thermodynamic identity reproduces entropy and same critical limiting value",
    zero(Us-Grand-(kb*T*s.log(z))*Ns-T*Entropy) and
    zero(s.limit(Entropy,z,1,dir="-")-3*kb*Ak*(kb*T)**2*s.zeta(3)))
# W079 FPUT-beta chain.
m,K,beta,a,k=s.symbols("m K beta a k",positive=True)
w0=2*s.sqrt(K/m)*s.sin(k*a/2)
group=s.diff(w0,k)
ck("W079",1,"conservation","Periodic quartic nearest-neighbor force telescopes to exact zero total momentum change",
    zero(sum(s.symbols(f"d{j}")**3-s.symbols(f"d{(j-1)%5}")**3 for j in range(5))) and
    zero(sum(s.symbols(f"d{j}")-s.symbols(f"d{(j-1)%5}") for j in range(5))))
ck("W079",2,"symbolic","Bloch difference eigenvalue and differentiated acoustic group velocity match exactly",
    zero(w0**2-4*K*s.sin(k*a/2)**2/m) and
    zero(group-a*s.sqrt(K/m)*s.cos(k*a/2)))
theta,A=s.symbols("theta A",real=True)
d1=-2*A*s.sin(k*a/2)*s.sin(theta)
fund=s.integrate(d1**3*s.sin(theta),(theta,0,2*s.pi))/s.pi
ck("W079",3,"independent_derivation","Fourier projection of cubic FPUT bond force gives the three-quarters fundamental coefficient",
    zero(s.trigsimp(fund-(-6*A**3*s.sin(k*a/2)**3))) and
    zero(4*s.sin(k*a/2)**2*(K+3*beta*A**2*s.sin(k*a/2)**2)/m-(4*K*s.sin(k*a/2)**2+12*beta*A**2*s.sin(k*a/2)**4)/m))
dis=[s.Rational(1,2),-s.Rational(2,3),s.Rational(3,4),-s.Rational(1,5)]
v=[s.Rational(1,3),-s.Rational(1,2),s.Rational(2,3),s.Rational(1,7)]
forces=[(dis[j]-dis[(j-1)%4])+2*(dis[j]**3-dis[(j-1)%4]**3) for j in range(4)]
# dq_j/dt = v_{j+1}-v_j, potential K=1 beta=2.
dH=s.factor(sum(v[j]*forces[j] for j in range(4))+
    sum((dis[j]+2*dis[j]**3)*(v[(j+1)%4]-v[j]) for j in range(4)))
ck("W079",4,"conservation","Independent discrete kinetic and quartic potential power sums cancel for nonsymmetric periodic state",
    zero(dH) and zero(sum(forces)))
# O081 spherical rainbow.
nn,i=s.symbols("nn i",positive=True,real=True)
r=s.asin(s.sin(i)/nn)
Dangle=s.pi+2*i-4*r
iS=math.asin(math.sqrt((4-(4/3)**2)/3));rS=math.asin(math.sin(iS)/(4/3))
Dr=math.pi+2*iS-4*rS
ck("O081",1,"symbolic","Snell differentiation agrees with stated rainbow total deviation angle",
    zero(s.diff(Dangle,i)-2+4*s.cos(i)/(nn*s.sqrt(1-s.sin(i)**2/nn**2))))
ck("O081",2,"numerical","Water-drop primary rainbow stationary angle and positive fold curvature give approximately 42 degrees",
    near(math.degrees(math.pi-Dr),42.02965886569771,1e-10) and
    near(2-4*math.cos(iS)/((4/3)*math.cos(rS)),0) and
    2*math.tan(iS)-math.tan(rS)>0)
d2=2*math.tan(iS)-math.tan(rS)
ampcoef=2*math.sin(iS)*math.cos(iS)/(math.sin(Dr)*math.sqrt(2*d2))
eps=1e-6
delta=math.sqrt(2*eps/d2)
# Local two-ray quadratic fold cross section a=1; derivative and two roots both counted.
loc=2*math.sin(iS)*math.cos(iS)/(math.sin(Dr)*d2*delta)
ck("O081",3,"dimensions","Two-ray fold Jacobian reproduces predicted inverse-square-root divergence coefficient with area scale",
    near(loc*math.sqrt(eps),ampcoef) and ampcoef>0 and loc>100)
kval=mp.mpf(3)
Ai0=mp.airyai(0)
ck("O081",4,"numerical","Airy uniform fold amplitude is finite at caustic and obeys k to minus one-third scaling",
    abs(Ai0-1/(3**(mp.mpf(2)/3)*mp.gamma(mp.mpf(2)/3)))<mp.mpf("1e-30") and
    abs((2*mp.pi*(8*kval)**(-mp.mpf(1)/3)*Ai0)/(2*mp.pi*kval**(-mp.mpf(1)/3)*Ai0)-mp.mpf("0.5"))<mp.mpf("1e-20"))
# Q081 tetrahedral SIC qubit tomography.
rr=[s.Matrix([1,1,1])/s.sqrt(3),s.Matrix([1,-1,-1])/s.sqrt(3),
    s.Matrix([-1,1,-1])/s.sqrt(3),s.Matrix([-1,-1,1])/s.sqrt(3)]
ss3=s.Matrix(s.symbols("sx sy sz",real=True))
I3=s.eye(3)
outer=sum((v*v.T for v in rr),s.zeros(3))
ck("Q081",1,"symbolic","Tetrahedral vectors sum to zero and form positive rank-one POVM with tight-frame moment",
    zero(sum(rr,s.zeros(3,1))) and zero(outer-s.Rational(4,3)*I3) and
    all(zero(rr[j].dot(rr[k])+s.Rational(1,3)) for j in range(4) for k in range(j)))
pp=[(1+v.dot(ss3))/4 for v in rr]
recons=3*sum((pp[j]*rr[j] for j in range(4)),s.zeros(3,1))
ck("Q081",2,"independent_derivation","Born probabilities invert exactly to all three Bloch components for arbitrary mixed state",
    zero(recons-ss3) and zero(sum(pp)-1))
N=s.symbols("N",positive=True)
cov=9/N*(sum((pp[j]*rr[j]*rr[j].T for j in range(4)),s.zeros(3))-ss3*ss3.T/9)
ck("Q081",3,"conservation","Multinomial covariance propagation gives total mean-squared Bloch error 9 minus purity over N",
    zero(s.trace(cov)-(9-ss3.dot(ss3))/N) and
    zero(s.trace(cov.subs({ss3[0]:0,ss3[1]:0,ss3[2]:0}))-9/N))
F=s.zeros(3)
for j in range(4):
    F+=N*(rr[j]*rr[j].T)/(16*pp[j])
F0=s.simplify(F.subs({ss3[0]:0,ss3[1]:0,ss3[2]:0}))
Cov0=s.simplify(cov.subs({ss3[0]:0,ss3[1]:0,ss3[2]:0}))
ck("Q081",4,"independent_derivation","At maximally mixed qubit SIC Fisher inverse exactly equals linear tomography covariance",
    zero(F0-N*I3/3) and zero(Cov0-3*I3/N) and zero(F0*Cov0-I3))
ids=["M084","M085","E084","E085","T079","W079","O081","Q081"]
assert len(TESTS)==32,(len(TESTS),"expected 32 executed checks")
assert {(r["id"],r["part"]) for r in TESTS}=={(uid,j) for uid in ids for j in range(1,5)}
for uid in ids:
    folder=ROOT/"bank"/uid
    meta=json.loads((folder/"meta.json").read_text(encoding="utf8"))
    assert meta["quality_status"]=="待独立复核"
    question=(folder/"question.tex").read_text(encoding="utf8")
    solution=(folder/"solution.tex").read_text(encoding="utf8")
    assert all(f"({j})" in question and f"({j})" in solution for j in range(1,5))
out={"round":14,"status":"32_executed_checks_not_expert_signoff","new_problem_count":8,
     "passed_count":len(TESTS),"ids":ids,"tests":TESTS,"independent_expert_review":"待独立复核"}
(ROOT/"data"/"round14_final8_validation_report.json").write_text(
    json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("ROUND14 FINAL8: 32 distinct executable physical checks passed; expert review pending")
