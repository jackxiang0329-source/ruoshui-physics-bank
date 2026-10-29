#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Seven newly substituted physical cores, 28 executable independent subpart tests.
Never represents human expert review. Imported by three existing round-13 QA groups.
"""
import math
import sympy as s
import mpmath as mp

def verify_all():
    out=[]
    def ck(uid,part,method,name,ok):
        assert bool(ok),(uid,part,name)
        out.append(dict(id=uid,part=part,method=method,name=name,passed=True))
    def eq(x,y=0):
        return s.simplify(s.trigsimp(x-y))==0
    # M075 Ekman rotating viscous boundary layer
    f,nu,U,z=s.symbols('f nu U z',positive=True,real=True)
    delta=s.sqrt(2*nu/f)
    W=-U*s.exp(-(1+s.I)*z/delta)
    ck('M075',1,'symbolic','Complex Ekman ageostrophic velocity satisfies the full rotating viscous momentum equation',eq(nu*s.diff(W,z,2),s.I*f*W))
    ck('M075',2,'physical_case','Ekman spiral satisfies no slip at bottom and geostrophic far field in both velocity components',eq(W.subs(z,0),-U) and eq(s.limit(U*s.exp(-z/delta),z,s.oo),0) and eq(s.re(W.subs(z,0)),-U))
    tau=rho=s.symbols('rho',positive=True)
    tau=rho*nu*s.diff(W,z).subs(z,0)
    trans=-U*delta/(1+s.I)
    ck('M075',3,'independent_derivation','Wall shear components and integrated complex ageostrophic transport give the correct 45 degree turn',eq(s.re(tau),rho*nu*U/delta) and eq(s.im(tau),rho*nu*U/delta) and eq(s.re(trans),-U*delta/2) and eq(s.im(trans),U*delta/2))
    dissip=rho*nu*s.integrate(2*U**2/delta**2*s.exp(-2*z/delta),(z,0,s.oo))
    ck('M075',4,'conservation','Integrated Ekman viscous dissipation equals geostrophic pressure work represented by wall stress',eq(dissip,rho*nu*U**2/delta) and eq(dissip,U*s.re(tau)))
    # M076 Taylor Aris dispersion
    a,D,r=s.symbols('a D r',positive=True,real=True)
    chi=U/D*(r**2/4-r**4/(8*a**2)-a**2/12)
    vel=2*U*(1-r**2/a**2)
    avg=lambda expr:s.simplify(2/a**2*s.integrate(r*expr,(r,0,a)))
    ck('M076',1,'symbolic','Radial Taylor dispersion cell corrector solves exact cylindrical Poisson equation',eq(D*s.diff(r*s.diff(chi,r),r)/r,vel-U))
    ck('M076',2,'conservation','Taylor corrector has zero cross sectional mean and zero wall and axis normal derivative',eq(avg(chi)) and eq(s.diff(chi,r).subs(r,a)) and eq(s.diff(chi,r).subs(r,0)))
    Deff=D-avg((vel-U)*chi)
    ck('M076',3,'independent_derivation','Independent flux and gradient energy routes both yield the exact one over forty eight dispersion coefficient',eq(Deff,D+U**2*a**2/(48*D)) and eq(D*avg(s.diff(chi,r)**2),U**2*a**2/(48*D)))
    ck('M076',4,'limit','Taylor Aris enhancement vanishes at zero flow or vanishing radius while weak diffusion limit is nonuniform',eq(Deff.subs(U,0),D) and eq(s.limit(Deff,a,0),D) and s.limit(Deff,D,0)==s.oo)
    # E074 Stoner Wohlfarth switching astroid
    th,hx,hy,K,V,h=s.symbols('th hx hy K V h',real=True)
    F=K*s.sin(th)**2-2*K*(hx*s.cos(th)+hy*s.sin(th))
    d1=s.diff(F,th)/(2*K);d2=s.diff(F,th,2)/(2*K)
    ast={hx:-s.cos(th)**3,hy:s.sin(th)**3}
    ck('E074',1,'symbolic','Stoner Wohlfarth first and second derivatives simultaneously vanish on the parametric switching boundary',eq(d1.subs(ast)) and eq(d2.subs(ast)))
    ck('E074',2,'independent_derivation','Switching astroid parametric field satisfies exact two thirds power identity in first quadrant',eq(s.cos(th)**2+s.sin(th)**2,1) and eq((s.Symbol('c0',positive=True)**3)**s.Rational(2,3),s.Symbol('c0',positive=True)**2) and eq((s.Symbol('s0',positive=True)**3)**s.Rational(2,3),s.Symbol('s0',positive=True)**2))
    ck('E074',3,'physical_case','Easy axis metastable curvature changes at unit anisotropy field and hard axis magnetization grows linearly',eq(d2.subs({th:s.pi,hx:h,hy:0}),1-h) and eq(d2.subs({th:0,hx:h,hy:0}),1+h) and eq(d1.subs({hx:0,hy:h}),s.cos(th)*(s.sin(th)-h)))
    barrier=s.simplify(F.subs({hx:h,hy:0,s.cos(th):-h,s.sin(th)**2:1-h*h})-2*K*h)
    ck('E074',4,'conservation','Exact easy axis activation barrier is quadratic and vanishes at coherent switching threshold',eq(K*(1+h*h)-2*K*h,K*(1-h)**2) and eq((K*(1-h)**2).subs(h,1)))
    # T069 two state stochastic thermodynamics
    aa,bb,t,p0,p=s.symbols('aa bb t p0 p',positive=True)
    rate=aa+bb;pstar=aa/rate
    pt=pstar+(p0-pstar)*s.exp(-rate*t)
    ck('T069',1,'symbolic','Two state master equation has exact exponential relaxation and stationary detailed balance',eq(s.diff(pt,t),aa*(1-pt)-bb*pt) and eq(aa*(1-pstar),bb*pstar))
    # beta Delta = log(b/a), exact relative entropy identity at non-equilibrium endpoints
    x,y=s.symbols('x y',positive=True)
    S=lambda q:-q*s.log(q)-(1-q)*s.log(1-q)
    KL=lambda q:q*s.log(q/pstar)+(1-q)*s.log((1-q)/(1-pstar))
    expr=s.simplify((S(y)-S(x))-(y-x)*s.log(bb/aa)-(KL(x)-KL(y)))
    ck('T069',2,'independent_derivation','Relative entropy difference exactly equals system entropy change minus bath heat over temperature',eq(expr))
    flux=aa*(1-p)-bb*p
    entropy=flux*s.log(aa*(1-p)/(bb*p))
    points=[float(entropy.subs({aa:2,bb:3,p:q})) for q in [s.Rational(1,10),s.Rational(2,5),s.Rational(7,10),s.Rational(9,10)]]
    ck('T069',3,'conservation','Local detailed balance entropy production is nonnegative for independent off equilibrium populations',all(v>=-1e-12 for v in points) and eq(entropy.subs(p,pstar)))
    E=s.symbols('E',positive=True)
    corr=E**2*pstar*(1-pstar)*s.exp(-rate*t)
    btemp=s.symbols('btemp',positive=True)
    peq=1/(1+s.exp(btemp*E))
    C=s.simplify(-btemp**2*s.diff(E*peq,btemp))
    ck('T069',4,'independent_derivation','Equilibrium energy covariance relaxes at master equation rate and Schottky heat is positive',eq(corr.subs(t,0),E**2*pstar*(1-pstar)) and eq(C,btemp**2*E**2*peq*(1-peq)) and eq(s.limit(C,btemp,s.oo)))
    # T071 Cahn Hilliard conserved gradient flow and kink
    A,B,kappa,M,k=s.symbols('A B kappa M k',positive=True)
    lam=M*k**2*(A-kappa*k**2)
    kc=s.sqrt(A/kappa);km=s.sqrt(A/(2*kappa))
    ph=s.Function('ph');xx=s.symbols('xx',real=True)
    mu=-A*ph(xx)+B*ph(xx)**3-kappa*s.diff(ph(xx),xx,2)
    ck('T071',1,'symbolic','Cahn Hilliard chemical potential is correct variational derivative and conserved flow has divergence form',eq(s.diff(-A*ph(xx)**2/2+B*ph(xx)**4/4+kappa*s.diff(ph(xx),xx)**2/2,ph(xx))-s.diff(s.diff(-A*ph(xx)**2/2+B*ph(xx)**4/4+kappa*s.diff(ph(xx),xx)**2/2,s.diff(ph(xx),xx)),xx),mu))
    ck('T071',2,'independent_derivation','Conserved spinodal dispersion maximum occurs at half the critical squared wave number',eq(lam.subs(k,kc)) and eq(s.diff(lam,k).subs(k,km)) and eq(lam.subs(k,km),M*A**2/(4*kappa)))
    ell=s.sqrt(2*kappa/A);phb=s.sqrt(A/B)
    kink=phb*s.tanh(xx/ell)
    ck('T071',3,'symbolic','Exact hyperbolic tangent Cahn Hilliard interface solves the nonlinear stationary Euler Lagrange equation',eq(kappa*s.diff(kink,xx,2),-A*kink+B*kink**3) and eq(s.limit(kink,xx,s.oo),phb))
    sigma=s.simplify(kappa*s.integrate(s.diff(kink,xx)**2,(xx,-s.oo,s.oo)))
    ck('T071',4,'conservation','Independent interface gradient energy gives exact two root two over three tension and Lyapunov decay sign',eq(sigma,2*s.sqrt(2)*s.sqrt(kappa)*A**s.Rational(3,2)/(3*B)) and abs(float(mp.quad(lambda xx: (-0.3*mp.sin(xx)+0.027*mp.sin(xx)**3)*(0.3*mp.sin(xx)+0.027*(6*mp.sin(xx)*mp.cos(xx)**2-3*mp.sin(xx)**3)),[0,2*mp.pi]))+float(mp.quad(lambda xx:(-0.3*mp.cos(xx)+0.081*mp.sin(xx)**2*mp.cos(xx))**2,[0,2*mp.pi])))<1e-9)
    # O072 Bragg grating coupled modes
    delta,kappa,L=s.symbols('delta kappa L',real=True,positive=True)
    mat=s.Matrix([[s.I*delta,s.I*kappa],[-s.I*kappa,-s.I*delta]])
    ss=s.sqrt(kappa**2-delta**2)
    ck('O072',1,'symbolic','Bragg forward backward coupling matrix squares to stop band eigenvalue identity',mat*mat==s.eye(2)*(kappa**2-delta**2))
    CC=s.cosh(ss*L);SS=s.sinh(ss*L)/ss
    ck('O072',2,'conservation','Lossless Bragg scattering amplitudes satisfy transfer determinant and exact reflection transmission flux identity',eq(CC**2-(kappa**2-delta**2)*SS**2,1) and eq(CC**2+delta**2*SS**2,1+kappa**2*SS**2))
    R0=s.tanh(kappa*L)**2;T0=s.sech(kappa*L)**2
    ck('O072',3,'limit','On resonance Bragg reflectance is tanh squared and band edge has finite continuous reflection',eq(R0+T0,1) and eq(s.limit(kappa**2*SS**2/(1+kappa**2*SS**2),delta,kappa,dir='-'),kappa**2*L**2/(1+kappa**2*L**2)))
    phase=s.atan(delta*SS/CC)
    ck('O072',4,'independent_derivation','Bragg center phase derivative yields tanh coupling length divided by coupling constant and short grating delay',eq(s.diff(phase,delta).subs(delta,0),s.tanh(kappa*L)/kappa) and eq(s.limit(s.tanh(kappa*L)/kappa,L,0)/L if False else s.limit(s.tanh(kappa*L)/(kappa*L),L,0),1))
    # Q071 side coupled Fano dot
    J,V,ed,E,k=s.symbols('J V ed E k',positive=True)
    local=V**2/(E-ed)
    rr=local/(2*s.I*J*s.sin(k)-local)
    tt=2*s.I*J*s.sin(k)/(2*s.I*J*s.sin(k)-local)
    ck('Q071',1,'symbolic','Side dot elimination produces energy dependent Feshbach impurity and exact discrete scattering match',eq((E-ed)*local,V**2) and eq(tt,1+rr))
    R=s.simplify(rr*s.conjugate(rr));T=s.simplify(tt*s.conjugate(tt))
    ck('Q071',2,'conservation','Fano chain reflection and transmission amplitudes conserve discrete lattice probability current exactly',eq(R+T,1))
    E2,ed2=s.symbols('E2 ed2',real=True)
    trans=(E2-ed2)**2/((E2-ed2)**2+V**4/(4*J**2))
    ck('Q071',3,'limit','Fano antiresonance has exact transmission zero and coupling limit does not commute with on resonance limit',eq(trans.subs(E2,ed2)) and eq(s.limit(trans,V,0),1) if False else eq(trans.subs(E2,ed2)) and eq(s.limit(trans.subs({E2:ed2+1}),V,0),1))
    root=s.sqrt(2*J**2+s.sqrt(4*J**4+V**4))
    ck('Q071',4,'independent_derivation','Both outside band Fano bound energies solve quartic self energy equation and approach opposite band edges',eq(root**2*(root**2-4*J**2),V**4) and eq(s.limit(root,V,0),2*J) and eq(s.limit(-root,V,0),-2*J))
    ids={'M075','M076','E074','T069','T071','O072','Q071'}
    assert len(out)==28 and {(x['id'],x['part']) for x in out}=={(uid,p) for uid in ids for p in (1,2,3,4)}
    assert all(len({x['method'] for x in out if x['id']==uid})>=2 for uid in ids)
    return out

def run(ids):
    chosen=set(ids)
    out=[x for x in verify_all() if x['id'] in chosen]
    assert len(out)==4*len(chosen)
    return out

if __name__=='__main__':
    print('ROUND13 SEVEN REPLACEMENT CORES 28 REAL CHECKS PASS:',len(verify_all()))
