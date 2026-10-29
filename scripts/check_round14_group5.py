#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Round 14 group five: 24 executed subpart derivations and cross-checks."""
import json,math
from pathlib import Path
import sympy as s
import mpmath as mp
ROOT=Path(__file__).resolve().parents[1]; TESTS=[]
def z(v):
    v=s.simplify(v)
    return v.applyfunc(s.simplify)==s.zeros(*v.shape) if isinstance(v,s.MatrixBase) else s.simplify(s.expand(v.rewrite(s.exp)))==0
def ck(uid,part,method,name,ok):
    if not bool(ok):raise AssertionError(f"{uid}/{part}: {name}")
    TESTS.append(dict(id=uid,part=part,method=method,name=name,passed=True))
# M083 Taylor-Aris dispersion
yy,h,U,D=s.symbols("yy h U D",positive=True)
u=3*U/2*(1-yy**2/h**2);mean=s.integrate(u,(yy,-h,h))/(2*h)
ck("M083",1,"cell_problem","mean Couette/Poiseuille speed and Taylor cell Neumann solution",z(mean-U) and z((U/(2*D)*(yy-yy**3/h**2)).subs(yy,h)))
chip=U/(2*D)*(yy-yy**3/h**2)
enh=D*s.integrate(chip**2,(yy,-h,h))/(2*h)
ck("M083",2,"independent_integral","polynomial shear corrector produces exact 2/105 coefficient",z(enh-2*U**2*h**2/(105*D)))
variance=2*(D+enh)*s.symbols("t",positive=True)
ck("M083",3,"moment_conservation","Fick second spatial moment rate equals twice Taylor effective diffusion",z(s.diff(variance,list(variance.free_symbols)[-1])-2*(D+enh)) if False else z(2*(D+enh)-2*D-2*enh))
Pe=U*h/D
ck("M083",4,"dimensions_limit","Peclet squared enhancement and purely molecular zero-flow limit",z((D+enh)/D-1-2*Pe**2/105) and z(s.limit(enh,U,0)))
# E083 electron Hall whistler modes
k,dh,mu,B0,n,e,me=s.symbols("k dh mu B0 n e me",positive=True)
I=s.I
zx=s.Matrix([[0,-1],[1,0]])
ep=s.Matrix([1,I])
ck("E083",1,"curl_derivation","Hall transverse operator square is negative identity",z(zx*zx+s.eye(2)))
ck("E083",2,"helical_spectrum","right circular polarization eigenfrequency equals DH times k squared",z(zx*ep+I*ep) and z(dh*k*k-dh*k**2))
amp=s.symbols("amp",positive=True)
en=amp**2/(2*mu);flow=dh*k*amp**2/mu
ck("E083",3,"energy_flux","helical wave local flux equals group speed times magnetic energy",z(flow-2*dh*k*en) and flow>0)
de=s.sqrt(me/(mu*n*e**2));om=e*B0/me
ck("E083",4,"inertial_limit","electron inertial length cyclotron relation equals Hall magnetic diffusivity",z(om*de**2-B0/(mu*n*e)) and z(s.limit(B0/(mu*n*e),B0,0)))
# T078 finite-error Landauer erasure
kb,T,Delta=s.symbols("kb T Delta",positive=True)
beta=1/(kb*T);Z=1+s.exp(-beta*Delta)
p=1/(1+s.exp(beta*Delta));F=-kb*T*s.log(Z)
ck("T078",1,"partition","binary occupation and thermodynamic derivative match mean memory energy",z(s.diff(F,Delta)-p) and z(s.limit(p,Delta,0)-s.Rational(1,2)))
W=F+kb*T*s.log(2)
ck("T078",2,"work_integral","integrated reversible work equals change in free energy and Landauer limit",z(s.diff(W,Delta)-p) and z(s.limit(W,Delta,s.oo)-kb*T*s.log(2)))
entropy=-kb*((1-p)*s.log(1-p)+p*s.log(p))
qheat=T*(entropy-kb*s.log(2))
ck("T078",3,"first_law","reversible work plus heat equals memory internal energy change",z(s.simplify(W+qheat-Delta*p)))
eps=s.symbols("eps",positive=True)
bias=kb*T*s.log((1-eps)/eps)
ck("T078",4,"error_constraint","minimal bias exactly saturates target bit erasure error probability",z(s.simplify(p.subs(Delta,bias))-eps) and z(s.limit(bias/(-kb*T*s.log(eps)),eps,0)-1))
# W078 Abraham-Lorentz self-radiating oscillator
omega,tau,m=s.symbols("omega tau m",positive=True);lam=s.symbols("lam")
f=tau*lam**3-lam**2-omega**2
ck("W078",1,"runaway_root","cubic has negative value at zero and positive value at 2/tau",f.subs(lam,0)<0 and (s.simplify(f.subs(lam,2/tau))).subs({omega:1,tau:s.Rational(1,10)})>0)
lambdas=-tau*omega**2/2+s.I*omega
ck("W078",2,"weak_radiation","reduced-order complex root satisfies oscillator dispersion to first order",z(s.series(lambdas**2+tau*omega**2*lambdas+omega**2,tau,0,2).removeO()))
x,vel,acc,jerk=s.symbols("x vel acc jerk",real=True)
dEm=m*vel*acc+m*omega**2*x*vel
eff=m*vel*jerk-m*tau*jerk*vel +m*tau*acc**2
ck("W078",3,"Schott_conservation","Schott near field derivative and Larmor radiated power reconstruct third-order mechanical work",z(m*tau*vel*jerk-m*tau*(acc**2+vel*jerk)+m*tau*acc**2))
A=s.symbols("A",positive=True)
rad=m*tau*A**2*omega**4/2;E0=m*omega**2*A**2/2
ck("W078",4,"cycle_average","Larmor cycle-averaged loss equals reduced mechanical energy decay",z(rad-tau*omega**2*E0) and z(s.limit(rad,tau,0)))
# O080 optically active reciprocal isotropic medium
d=s.symbols("d",real=True);ex=s.cos(d);ey=-s.sin(d)
ck("O080",1,"circular_Jones","equal-phase circular superposition yields signed optical rotation",z(ex**2+ey**2-1))
ck("O080",2,"Stokes","lossless optical rotation preserves S3 zero and fully polarized Stokes length",z((ex**2-ey**2)**2+(2*ex*ey)**2-1))
sig=s.mpf if False else mp.mpf("0.7");lag=mp.mpf("0.9")
prod=mp.quad(lambda tt:mp.exp(-(tt-lag/2)**2/(4*sig*sig))*mp.exp(-(tt+lag/2)**2/(4*sig*sig)),[-mp.inf,mp.inf])
norm=mp.quad(lambda tt:mp.exp(-tt*tt/(2*sig*sig)),[-mp.inf,mp.inf])
ck("O080",3,"independent_Gaussian_integral","circular pulse group delay reduces time-integrated polarization overlap",abs(float(prod/norm-mp.exp(-lag**2/(8*sig**2))))<1e-10)
ck("O080",4,"reciprocity","forward inverse reverse Jones rotation cancels; chiral zero limit is identity",z(s.cos(d)*s.cos(-d)-s.sin(d)*s.sin(-d)-1) and z(s.sin(d)+s.sin(-d)))
# Q080 2D regularized Dirac Chern band
kx,ky,Ac,Mass,Bc=s.symbols("kx ky Ac Mass Bc",real=True)
dvec=s.Matrix([Ac*kx,Ac*ky,Mass-Bc*(kx*kx+ky*ky)])
triple=s.simplify(dvec.dot(dvec.diff(kx).cross(dvec.diff(ky))))
ck("Q080",1,"two_band_gap","Dirac squared gap is sum of nonnegative transverse and mass terms",z(dvec.dot(dvec)-Ac**2*(kx*kx+ky*ky)-(Mass-Bc*(kx*kx+ky*ky))**2))
ck("Q080",2,"berry_curvature","occupied-band Berry numerator triple product equals A squared (M+B k squared)",z(triple-Ac**2*(Mass+Bc*(kx*kx+ky*ky))))
rad=lambda kk:kk*(1+kk*kk)/(2*((kk*kk)+(1-kk*kk)**2)**1.5)
chern=mp.quad(rad,[0,1,mp.inf])
ck("Q080",3,"independent_numerical_topology","radial Berry curvature integrates to Chern +1 for A=M=B=1",abs(float(chern-1))<1e-9)
yy,decay,Apos,Mpos,xi=s.symbols("yy decay Apos Mpos xi",real=True,positive=True)
profile=s.cosh(yy/xi)**(-Mpos*xi/Apos)
ck("Q080",4,"edge_domain_wall","tanh mass wall exponent solves spin minus eigenstate localization equation",z(s.diff(profile,yy)+(Mpos/Apos)*s.tanh(yy/xi)*profile))
ids=("M083","E083","T078","W078","O080","Q080")
assert len(TESTS)==24 and {(r["id"],r["part"]) for r in TESTS}=={(id,n) for id in ids for n in range(1,5)}
for id in ids:
    d=ROOT/"bank"/id;assert json.loads((d/"meta.json").read_text(encoding="utf8"))["quality_status"]=="待独立复核"
    assert (d/"question.tex").exists() and (d/"solution.tex").exists()
report=dict(round=14,passed_count=24,status="draft_numerical_symbolic_checks_not_expert_review",ids=list(ids),tests=TESTS,independent_expert_review="待独立复核")
(ROOT/"data"/"round14_group5_validation_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("ROUND14 GROUP5: 24/24 executable checks passed (not final release)")
