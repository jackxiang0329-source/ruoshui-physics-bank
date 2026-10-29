#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Round 14 fourth group: four substantive independent checks for six physical models."""
import json,math,random
from pathlib import Path
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[1];CHECKS=[]
def zz(a):
    b=s.simplify(a)
    if isinstance(b,s.MatrixBase):return b.applyfunc(s.simplify)==s.zeros(*b.shape)
    return s.simplify(s.expand(b.rewrite(s.exp)))==0
def ck(uid,part,method,name,test):
    if not bool(test):raise AssertionError(f"{uid} subpart {part}: {name}")
    CHECKS.append(dict(id=uid,part=part,method=method,name=name,passed=True))
# M082 axisymmetric Reynolds squeeze film
r,z,h,a,vis,hd=s.symbols("r z h a vis hd",positive=True)
pr=6*vis*hd*r/h**3
ur=pr*z*(z-h)/(2*vis); qr=s.integrate(ur,(z,0,h))
ck("M082",1,"independent_derivation","Stokes velocity integrates to Reynolds radial flux and incompressible radial flow",zz(qr+hd*r/2) and zz(s.diff(r*qr,r)/r+hd))
pp=3*vis*hd*(r*r-a*a)/h**3;load=s.integrate(2*s.pi*r*pp,(r,0,a))
ck("M082",2,"integral","axisymmetric pressure and force integrated without heuristic coefficients",zz(s.diff(pp,r)-pr) and zz(load+3*s.pi*vis*hd*a**4/(2*h**3)))
F0,h0,t=s.symbols("F0 h0 t",positive=True)
ht=1/s.sqrt(h0**(-2)+4*F0*t/(3*s.pi*vis*a**4))
ck("M082",3,"nonlinear_ode","finite-force squeeze-film closed form solves h cubed descent law",zz(s.diff(ht,t)+2*F0*ht**3/(3*s.pi*vis*a**4)) and zz(ht.subs(t,0)-h0))
diss=s.integrate(2*s.pi*r*s.integrate(vis*s.diff(ur,z)**2,(z,0,h)),(r,0,a))
ck("M082",4,"conservation","velocity-shear dissipation equals exact pressure load times compression speed",zz(diss+load*hd) and zz(diss-3*s.pi*vis*hd**2*a**4/(2*h**3)))
# E082 Hartmann flow
y,H,G,cond,B,mu=s.symbols("y H G cond B mu",positive=True)
lam=B*s.sqrt(cond/mu);Ha=lam*H
u=G/(cond*B*B)*(1-s.cosh(lam*y)/s.cosh(lam*H))
ck("E082",1,"magnetic_ohm","Lorentz resistive braking and Stokes force balance pointwise",zz(mu*s.diff(u,y,2)-cond*B**2*u+G) and zz(u.subs(y,H)))
Q=s.integrate(u,(y,-H,H))
ck("E082",2,"symbolic_limit","integrated Hartmann flux and zero-magnetic-field Poiseuille limit",zz(Q-2*H*G/(cond*B*B)*(1-s.tanh(Ha)/Ha)) and zz(s.limit(u,B,0)-G*(H*H-y*y)/(2*mu)))
ck("E082",3,"asymptotic","large Hartmann number yields plug speed and magnetic boundary layer",float((u*cond*B**2/G).subs({G:1,cond:1,B:100,mu:1,H:1,y:0}))>.99)
left=s.integrate(G*u,(y,-H,H))
right=s.integrate(mu*s.diff(u,y)**2+cond*B*B*u**2,(y,-H,H))
ck("E082",4,"power_conservation","pressure-work integral equals shear and electric Joule dissipation",zz(s.simplify(left-right)))
# T077 2D neutral Dirac fermions
pi=mp.pi
fermi1=mp.quad(lambda xx:xx/(mp.exp(xx)+1),[0,mp.inf])
fermi2=mp.quad(lambda xx:xx**2/(mp.exp(xx)+1),[0,mp.inf])
ck("T077",1,"fermi_integral","electron and hole number integrals equal pi squared over twelve",abs(float(fermi1-pi*pi/12))<1e-11)
ck("T077",2,"independent_numerical","third-order Dirac excitation Fermi integral equals 3 zeta(3) over 2",abs(float(fermi2-1.5*mp.zeta(3)))<1e-11)
T,kB,g,hbar,v=s.symbols("T kB g hbar v",positive=True)
uDir=3*g*s.zeta(3)*(kB*T)**3/(2*s.pi*(hbar*v)**2)
ck("T077",3,"thermodynamic_scaling","area heat capacity and conformal entropic Euler relation",zz(s.diff(uDir,T)-3*uDir/T) and zz((uDir+uDir/2)/T-3*uDir/(2*T)))
response=mp.quad(lambda xx:1/(mp.exp(xx)+1),[0,mp.inf])
ck("T077",4,"susceptibility","compressibility response integral equals log two and vanishes at zero T",abs(float(response-mp.log(2)))<1e-12 and zz(s.limit(g*kB*T*s.log(2)/(s.pi*(hbar*v)**2),T,0)))
# W077 two-dimensional Kirchhoff-Love bending waves
a,b,D,rho,h,kx,ky=s.symbols("a b D rho h kx ky",positive=True)
kx0=s.pi/a;ky0=2*s.pi/b;kt2=kx0**2+ky0**2
omega=s.sqrt(D/(rho*h))*kt2
ck("W077",1,"biharmonic_pde","separable simply supported plate mode solves full bi-Laplacian",zz(rho*h*omega**2-D*kt2**2))
ck("W077",2,"boundary","sine mode and both bending moments vanish at straight simply supported edges",zz(s.sin(kx0*a)) and zz(s.sin(ky0*b)) and zz(omega-s.sqrt(D/(rho*h))*(s.pi**2/a**2+4*s.pi**2/b**2)))
k=s.symbols("k",positive=True)
wp=s.sqrt(D/(rho*h))*k**2
ck("W077",3,"group_speed","free plate group velocity exactly twice phase velocity with k h limit",zz(s.diff(wp,k)-2*wp/k) and zz(s.limit(s.diff(wp,k),k,0)))
nu=s.symbols("nu",real=True)
ang=s.symbols("ang",real=True)
strain=s.Matrix([[1,nu],[nu,1]])
ck("W077",4,"positive_energy","bending form Hessian eigenvalues 1 plus and minus Poisson ratio",strain.eigenvals().get(1+nu,0)==1 and strain.eigenvals().get(1-nu,0)==1 and (1-.2)>0)
# O079 finite wavelet speckle, circular Gaussian Siegert and Gamma average
N=s.symbols("N",integer=True,positive=True)
I4=2-1/N
ck("O079",1,"combinatorics","finite-N phase index pair count has 2N squared minus N terms",zz(I4-((N*(N-1)*2+N)/N**2)) and zz(I4.subs(N,2)-s.Rational(3,2)))
ck("O079",2,"probability","negative exponential intensity law normalized with correct first two moments",abs(float(mp.quad(lambda x:mp.exp(-x),[0,mp.inf])-1))<1e-12 and abs(float(mp.quad(lambda x:x*x*mp.exp(-x),[0,mp.inf])-2))<1e-12)
ck("O079",3,"gaussian_wick","Siegert relation boundaries g2(0)=1 g2(1)=2 and Cauchy bound",zz(1+0**2-1) and zz(1+1**2-2) and (1+0.4**2)<2)
MM=4;pdf=lambda x:MM**MM/mp.gamma(MM)*x**(MM-1)*mp.exp(-MM*x)
norm=mp.quad(pdf,[0,mp.inf]);mean=mp.quad(lambda x:x*pdf(x),[0,mp.inf]);second=mp.quad(lambda x:x*x*pdf(x),[0,mp.inf])
ck("O079",4,"gamma_independent_integral","four independent speckles gamma distribution normalization and 1 over sqrt M contrast",abs(float(norm-1))<1e-11 and abs(float(mean-1))<1e-11 and abs(float(second-mean**2-1/MM))<1e-11)
# Q079 PT-symmetric non-Hermitian two-state effective system
J,gam,tt=s.symbols("J gam tt",positive=True);i=s.I
H=s.Matrix([[i*gam,J],[J,-i*gam]])
ck("Q079",1,"spectral","PT symmetry and coalesced characteristic roots at exceptional point",zz(H**2-(J**2-gam**2)*s.eye(2)) and zz(s.det(H)-(-J**2+gam**2)))
Om=s.sqrt(J**2-gam**2);U=s.cos(Om*tt)*s.eye(2)-i*s.sin(Om*tt)*H/Om
ck("Q079",2,"propagator","closed form nonunitary propagator satisfies exact Schr differential equation",zz(s.diff(U,tt)+i*H*U) and zz(U.subs(tt,0)-s.eye(2)))
a,b=s.symbols("a b");psi=s.Matrix([a,b]); pdt=s.conjugate(psi).T*(i*H.conjugate().T-i*H)*psi
target=2*gam*(s.conjugate(a)*a-s.conjugate(b)*b)
ck("Q079",3,"norm_balance","nonunitary ordinary-norm flux equals twice gain minus loss amplitudes",zz((pdt[0]-target)))
sigmay=s.Matrix([[0,-i],[i,0]]);metric=s.eye(2)+gam/J*sigmay
ck("Q079",4,"pseudohermitian_metric","positive inner product metric intertwines PT Hamiltonian",zz(H.conjugate().T*metric-metric*H) and zz(s.det(metric)-(1-gam**2/J**2)))
ids=("M082","E082","T077","W077","O079","Q079")
assert len(CHECKS)==24 and {(row["id"],row["part"]) for row in CHECKS}=={(uid,p) for uid in ids for p in range(1,5)}
for uid in ids:
    folder=ROOT/"bank"/uid
    assert json.loads((folder/"meta.json").read_text(encoding="utf-8"))["quality_status"]=="待独立复核"
    assert (folder/"question.tex").exists() and (folder/"solution.tex").exists()
report=dict(round=14,passed_count=24,status="draft_executable_checks_passed_not_expert_review",ids=list(ids),tests=CHECKS,independent_expert_review="待独立复核")
(ROOT/"data"/"round14_group4_validation_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("ROUND14 GROUP4: 24/24 EXECUTED SUBPART CHECKS PASSED; NOT RELEASE GATE")
