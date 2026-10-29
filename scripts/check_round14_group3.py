#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Six distinct round-14 cores: executable four-part physics checks, not expert review."""
import json,math
from pathlib import Path
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[1]; TESTS=[]
def zero(x):
    y=s.simplify(x)
    if isinstance(y,s.MatrixBase):return y.applyfunc(lambda q:s.simplify(q.rewrite(s.exp)))==s.zeros(*y.shape)
    return s.simplify(s.expand(y.rewrite(s.exp)))==0
def ck(uid,p,method,label,passed):
    if not bool(passed):raise AssertionError(f"{uid}({p}) {label}")
    TESTS.append(dict(id=uid,part=p,method=method,name=label,passed=True))
# M081 relativistic photon sail: intercepting power differs from beam power.
beta,c,P0,m,chi=s.symbols("beta c P0 m chi",positive=True)
Fin=2*P0*(1-beta)/(c*(1+beta))
ck("M081",1,"momentum","intercepted light momentum and moving mirror reflectivity",zero(P0*(1-beta)*(1+(1-beta)/(1+beta))/c-Fin) and zero(Fin.subs(beta,0)-2*P0/c))
tm=m*c*c*((s.exp(3*chi)-1)/3+s.exp(chi)-1)/(4*P0)
xx=m*c**3*((s.exp(3*chi)-1)/3-s.exp(chi)+1)/(4*P0)
ck("M081",2,"symbolic","exact rapidity time and position derivatives obey sail force ODE",zero(s.diff(tm,chi)-m*c*c*s.exp(2*chi)*s.cosh(chi)/(2*P0)) and zero(s.diff(xx,chi)-m*c**3*s.exp(2*chi)*s.sinh(chi)/(2*P0)))
ck("M081",3,"causality_limit","light-cone gap and one-third ultrarelativistic rapidity scaling",zero(c*tm-xx-m*c**3*(s.exp(chi)-1)/(2*P0)) and zero(s.limit(tm/s.exp(3*chi),chi,s.oo)-m*c*c/(12*P0)))
inter=P0*(1-beta);reflect=inter*(1-beta)/(1+beta)
ck("M081",4,"conservation","net photon-energy loss equals sail mechanical work",zero(inter-reflect-Fin*c*beta))
# E081 Sweet-Parker magnetic reconnection.
L,eta,va,B,rho,mu=s.symbols("L eta va B rho mu",positive=True)
lund=L*va/eta; d=s.sqrt(eta*L/va); vin=eta/d
ck("E081",1,"mass_ohm","steady Ohm layer width and incompressible inflow",zero(vin*L-va*d))
ck("E081",2,"symbolic","layer width and inflow ratio are inverse square root Lundquist",zero(d/L-1/s.sqrt(lund)) and zero(vin/va-1/s.sqrt(lund)))
ck("E081",3,"physical_limit","ram pressure scales as 1/S and resistivity-free reconnection vanishes",zero((rho*vin**2/(B**2/mu)).subs(rho,B**2/(mu*va**2))-1/lund) and zero(s.limit(vin,eta,0)))
Poynting=4*L*B**2*vin/mu;Pjet=2*d*rho*va**3
ck("E081",4,"independent_power","Alfven outflow kinetic energy and input Poynting have finite ratio",zero((Pjet/Poynting).subs(rho,B**2/(mu*va**2))-s.Rational(1,2)))
# T076 radiative transfer in grey homogeneous slab.
z,L,kappa,B,u=s.symbols("z L kappa B u",positive=True)
ip=B*(1-s.exp(-kappa*z/u));im=B*(1-s.exp(-kappa*(L-z)/u))
ck("T076",1,"transport","both directional intensities satisfy transport and vacuum boundaries",zero(u*s.diff(ip,z)-kappa*(B-ip)) and zero(-u*s.diff(im,z)-kappa*(B-im)) and zero(ip.subs(z,0)) and zero(im.subs(z,L)))
tau=1.3
integ=2*mp.pi*(mp.mpf("0.5")-mp.quad(lambda a:a*mp.exp(-tau/a),[0,1]))
e3=mp.pi*(1-2*mp.expint(3,tau))
ck("T076",2,"independent_numerical","angular quadrature matches exponential-integral emergent flux",abs(float(integ-e3))<1e-11 and 0<float(e3)<math.pi)
H=.4;dopt=1.7
jn=.5*mp.quad(lambda a:2-mp.exp(-dopt*H/a)-mp.exp(-dopt*(1-H)/a),[0,1])
ja=1-.5*(mp.expint(2,dopt*H)+mp.expint(2,dopt*(1-H)))
ck("T076",3,"independent_numerical","interior mean radiance symmetric and below source",abs(float(jn-ja))<1e-11 and 0<float(ja)<1 and abs(float(ja-(1-.5*(mp.expint(2,dopt*(1-H))+mp.expint(2,dopt*H)))))<1e-11)
cool=4*mp.pi*mp.quad(lambda v:mp.expint(2,v),[0,tau])
ck("T076",4,"conservation","integrated volumetric radiative cooling equals two face fluxes",abs(float(cool-2*e3))<1e-11)
# W076 Kelvin-Voigt frequency-dependent strain-rate loss.
k,et,mm,ten=s.symbols("k et mm ten",positive=True);omega=s.symbols("omega")
disp=mm*omega**2+s.I*et*k*k*omega-ten*k*k
roots=[-s.I*et*k*k/(2*mm)+a*s.sqrt(ten*k*k/mm-(et*k*k/(2*mm))**2) for a in (1,-1)]
ck("W076",1,"symbolic","both Kelvin-Voigt complex roots solve dispersion determinant",all(zero(disp.subs(omega,r)) for r in roots))
kc=2*s.sqrt(mm*ten)/et
ck("W076",2,"threshold","critical damping wavenumber and long-wave phase speed",zero(ten*kc**2/mm-(et*kc**2/(2*mm))**2) and zero(s.limit(roots[0]/k,k,0)-s.sqrt(ten/mm)))
x,t=s.symbols("x t",real=True);f=s.Function("f")(x,t);ft=s.diff(f,t);fx=s.diff(f,x);fxt=s.diff(f,x,t)
ed=s.diff(mm*ft**2/2+ten*fx**2/2,t)
flux=s.diff(ten*ft*fx+et*ft*fxt,x)
eq=mm*s.diff(f,t,2)-ten*s.diff(f,x,2)-et*s.diff(f,x,2,t)
ck("W076",3,"conservation_identity","local PDE energy flux plus strain-rate loss equals velocity times PDE residual",zero(ed-flux+et*fxt**2-ft*eq))
a=et*k*k/(2*mm);slow=-s.I*a+s.I*s.sqrt(a*a-ten*k*k/mm);fast=-s.I*a-s.I*s.sqrt(a*a-ten*k*k/mm)
ck("W076",4,"high_k_limit","slow relaxation tends to T/eta and fast relaxation grows k squared",zero(s.limit(slow,k,s.oo)+s.I*ten/et) and zero(s.limit(fast/k**2,k,s.oo)+s.I*et/mm))
# O078 polarized free electron Thomson scattering.
theta,re=s.symbols("theta re",positive=True)
cross=re**2*(1+s.cos(theta)**2)/2
ck("O078",1,"polarization","transverse projector yields parallel and perpendicular strengths",zero((re**2*s.cos(theta)**2+re**2)/2-cross))
total=s.integrate(2*s.pi*s.sin(theta)*cross,(theta,0,s.pi))
ck("O078",2,"angular_integral","full sphere cross-section integrates to 8 pi re squared over 3",zero(total-8*s.pi*re**2/3))
pol=s.sin(theta)**2/(1+s.cos(theta)**2)
ck("O078",3,"physical_boundary","side scattering fully polarized; forward and backward zero",zero(pol.subs(theta,s.pi/2)-1) and zero(pol.subs(theta,0)) and zero(pol.subs(theta,s.pi)))
ck("O078",4,"momentum","scattered z momentum integral cancels by front-back symmetry",zero(s.integrate(s.cos(theta)*cross*2*s.pi*s.sin(theta),(theta,0,s.pi))))
# Q078 exactly two interacting bosons on two sites.
J,U=s.symbols("J U",positive=True);Z=s.sqrt(2)
H=s.Matrix([[U,-Z*J,0],[-Z*J,0,-Z*J],[0,-Z*J,U]])
lam=s.symbols("lam");Delta=s.sqrt(U**2+16*J**2)
ck("Q078",1,"spectral","antisymmetric eigenstate and full exact Bose-Hubbard characteristic cubic",zero(H*s.Matrix([1,0,-1])-U*s.Matrix([1,0,-1])) and zero(H.charpoly(lam).as_expr()-(lam-U)*(lam**2-U*lam-4*J**2)))
Y=mp.matrix([[3,-mp.sqrt(2),0],[-mp.sqrt(2),0,-mp.sqrt(2)],[0,-mp.sqrt(2),3]]);wave=mp.expm(-1j*mp.mpf('0.7')*Y)*mp.matrix([0,1,0])
observed=abs(wave[0])**2+abs(wave[2])**2
ck("Q078",2,"independent_numerical","3 by 3 matrix exponential agrees with nonlinear double occupancy probability",abs(observed-16/25*math.sin(5*.7/2)**2)<1e-12 and abs(sum(abs(wave[i])**2 for i in range(3))-1)<1e-12)
Eminus=(U-Delta)/2
ck("Q078",3,"perturbation","exact low eigenvalue matches two separate virtual intermediate paths",zero(s.series(Eminus,J,0,4).removeO()+4*J**2/U))
a2=(1+U/Delta)/2;b2=(1-U/Delta)/2
entropy=-a2*s.log(a2)-b2*s.log(b2/2)
ck("Q078",4,"entanglement","site reduced entropy gives 3/2 log 2 and Mott zero limit",zero(entropy.subs(U,0)-s.Rational(3,2)*s.log(2)) and float(entropy.subs({U:100000,J:1}))<1e-6)
IDS=("M081","E081","T076","W076","O078","Q078")
assert len(TESTS)==24 and {(a["id"],a["part"]) for a in TESTS}=={(uid,i) for uid in IDS for i in range(1,5)}
for uid in IDS:
    p=ROOT/"bank"/uid
    meta=json.loads((p/"meta.json").read_text(encoding="utf-8"))
    assert meta["quality_status"]=="待独立复核" and (p/"question.tex").exists() and (p/"solution.tex").exists()
report={"round":14,"status":"draft_technical_24_tests_passed_not_expert_review","passed_count":len(TESTS),"ids":list(IDS),"tests":TESTS,"independent_expert_review":"待独立复核"}
(ROOT/"data"/"round14_group3_validation_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("ROUND14 GROUP3: 24 independent computational subpart checks passed; draft only")
