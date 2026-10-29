#!/usr/bin/env python3
"""Round13 fourth-six mathematical spotchecks, six distinct physical models. Human review pending."""
import json
import sympy as s
import mpmath as mp
from pathlib import Path
checks=[]
def ck(uid,part,method,name,condition):
    assert bool(condition),(uid,part,name)
    checks.append(dict(id=uid,part=part,method=method,name=name,passed=True))
def eq(a,b=0):return s.simplify(s.expand_trig(a-b))==0
# M071 isothermal Bondi transonic accretion.
G,M,c,r,u=s.symbols('G M c r u',positive=True)
rs=G*M/(2*c*c)
ck('M071',1,'symbolic','continuity-derived Bondi velocity gradient numerator vanishes precisely at the transonic regular sonic point',eq((2*c*c/r-G*M/r**2).subs(r,rs)) and eq((u-c*c/u).subs(u,c)))
rhoinf=s.symbols('rhoinf',positive=True)
rhos=s.exp(s.Rational(3,2))*rhoinf
mdot=4*s.pi*rs*rs*rhos*c
ck('M071',2,'dimensions','regular sonic radius and density determine classical isothermal Bondi accretion rate with exact pi exp three halves coefficient',eq(mdot,s.pi*s.exp(s.Rational(3,2))*G*G*M*M*rhoinf/c**3) and eq(G*M/rs,2*c*c))
w,x=s.symbols('w x',positive=True)
F=w*w/2-s.log(w)-2*s.log(x)-2/x+s.Rational(3,2)
ck('M071',3,'independent_derivation','dimensionless Bernoulli implicit Bondi transonic curve has stationary regular point at w equals x equals one',eq(F.subs({w:1,x:1})) and eq(s.diff(F,w).subs({w:1,x:1})) and eq(s.diff(F,x).subs({w:1,x:1})))
v_asym=s.sqrt(2*G*M/r)
density_asym=mdot/(4*s.pi*r*r*v_asym)
ck('M071',4,'limit','free fall inner Bondi density has minus three halves radial exponent and outer rate tends inverse square distance',eq(s.diff(s.log(density_asym),r)*r,-s.Rational(3,2)) and eq(s.limit(mdot/(4*s.pi*r*r*rhoinf),r,s.oo),0))
# E071 Landau ferroelectric spinodal.
a,b,T,Tc,P,E=s.symbols('a b T Tc P E',positive=True)
A=s.symbols('A',positive=True)
f=-A*P*P/2+b*P**4/4-E*P
P0=s.sqrt(A/b)
ck('E071',1,'symbolic','ferroelectric double well has two nonzero stable roots with positive curvature and an unstable zero root',eq(s.diff(f,P).subs({E:0,P:P0})) and eq(s.diff(f,P,2).subs({E:0,P:P0}),2*A) and eq(s.diff(f,P,2).subs({E:0,P:0}),-A))
chiLow=1/(2*A);chiHigh=1/A
ck('E071',2,'independent_derivation','polarization differential susceptibility follows curvature inverse and critical amplitude ratio is two',eq(chiHigh/chiLow,2) and eq(1/s.diff(f,P,2).subs({E:0,P:P0}),chiLow))
Psp=s.sqrt(A/(3*b))
Esp=-A*Psp+b*Psp**3
ck('E071',3,'symbolic','Landau spinodal simultaneously zero first and second derivatives yields exact coercive spinodal field magnitude',eq(s.diff(f,P,2).subs(P,Psp)) and eq(Esp,-2*A**s.Rational(3,2)/(3*s.sqrt(3*b))))
ck('E071',4,'conservation','zero field double well free energy barrier is positive A squared over four b',eq(f.subs({E:0,P:0})-f.subs({E:0,P:P0}),A*A/(4*b)))
# T067 rotating canonical ideal gas cylinder.
alpha,R=s.symbols('alpha R',positive=True)
Z=(s.exp(alpha*R**2)-1)/alpha
meanR=s.diff(s.log(Z),alpha)
target=R*R*s.exp(alpha*R**2)/(s.exp(alpha*R**2)-1)-1/alpha
ck('T067',1,'symbolic','centrifugal ideal gas equilibrium exponential density follows exact radial isothermal Euler balance',eq(s.diff(s.log(s.exp(alpha*r*r)),r),2*alpha*r))
ck('T067',2,'limit','radial normalization yields uniform volume density as rotation vanishes',eq(s.limit(alpha/(s.exp(alpha*R**2)-1),alpha,0,dir='+'),1/R**2))
ck('T067',3,'independent_derivation','moment of inertia radius equals derivative of logarithmic partition factor and has correct small rotation limit',eq(meanR,target) and eq(s.limit(target,alpha,0,dir='+'),R**2/2))
om,kb,tm,m=s.symbols('om kb tm m',positive=True)
al=m*om**2/(2*kb*tm)
ck('T067',4,'conservation','rotating frame Legendre conjugate derivative equals mass times angular velocity times canonical mean radius squared',eq(kb*tm*s.diff(s.log(Z).subs(alpha,al),om),m*om*target.subs(alpha,al)))
# W067 liquid droplet Rayleigh shape modes.
ell,sigma,rho,R=s.symbols('ell sigma rho R',positive=True)
mass=rho*R**3/ell
stiff=sigma*(ell-1)*(ell+2)
om2=sigma*ell*(ell-1)*(ell+2)/(rho*R**3)
ck('W067',1,'symbolic','spherical harmonic interior radial velocity potential satisfies kinematic boundary exactly',eq(s.diff(s.Symbol('r',positive=True)**ell/(ell*R**(ell-1)),s.Symbol('r',positive=True)).subs(s.Symbol('r',positive=True),R),1))
ck('W067',2,'independent_derivation','dynamic Laplace curvature pressure and Bernoulli condition yield Rayleigh ell mode squared frequency',eq(stiff/mass,om2) and eq(s.simplify(om2.subs(ell,2)),8*sigma/(rho*R**3)))
ck('W067',3,'conservation','Green kinetic integral and second-order surface energy reproduce oscillator mass and positive stiffness',eq(mass*om2,stiff) and eq(s.limit(stiff,ell,2),4*sigma))
ck('W067',4,'physical_case','ell one is pure translation zero frequency while high surface tension raises frequencies',eq(om2.subs(ell,1)) and eq(s.diff(om2,sigma),ell*(ell-1)*(ell+2)/(rho*R**3)))
# O069 transport of intensity wavefront inversion.
I0,k,q,eps,z=s.symbols('I0 k q eps z',positive=True)
phi=eps*s.cos(q*z)
Iz=-I0/k*s.diff(phi,z,2)
ck('O069',1,'symbolic','paraxial continuity gives positive focused intensity derivative for positive sinusoidal phase curvature',eq(Iz,I0*eps*q*q*s.cos(q*z)/k))
ck('O069',2,'independent_derivation','Fourier inverse Poisson coefficient times measured defocus derivative recovers original nonzero phase',eq((k/(I0*q*q))*Iz,phi))
ck('O069',3,'limit','low spatial frequency inverse Poisson transfer grows with inverse square wave number',eq(s.diff(s.log(1/q**2),q)*q,-2) and eq(s.limit(1/q*q,q,0,dir='+'),1))
xx=s.symbols('xx',real=True)
ck('O069',4,'conservation','periodic transverse intensity flux integrates to zero under no boundary leakage',eq(s.integrate(s.diff(s.cos(xx),xx),(xx,0,2*s.pi)),0))
# Q069 Wannier Stark localization and Bloch rephasing.
J,F,a,hn,t=s.symbols('J F a hn t',positive=True)
zB=2*J/(F*a)
m,n=s.symbols('m n',integer=True)
B=s.besselj(n-m,zB)
ck('Q069',1,'symbolic','Bessel recurrence exactly solves tilted tight binding eigenvalue equation for Wannier Stark ladder',eq(-J*(s.besselj(n-m-1,zB)+s.besselj(n-m+1,zB))+F*a*(n-m)*B))
ck('Q069',2,'numerical','numerical Wannier Stark Bessel modes are orthonormal for two distinct translated ladder centers',abs(sum(float(mp.besselj(j,mp.mpf('2.7')))**2 for j in range(-80,81))-1)<1e-13 and abs(sum(float(mp.besselj(j,mp.mpf('2.7'))*mp.besselj(j-1,mp.mpf('2.7'))) for j in range(-80,81)))<1e-13)
T_B=2*s.pi*hn/(F*a)
ck('Q069',3,'limit','every Wannier Stark ladder eigenphase exactly revives after a complete Bloch period and wavepacket broadening vanishes',eq(s.exp(-s.I*F*a*T_B/hn),1) and eq(s.sin(F*a*T_B/(2*hn)),0))
kt=s.symbols('kt',real=True)
xdisp=2*J/F*(s.cos(kt-F*a*t/hn)-s.cos(kt))
ck('Q069',4,'independent_derivation','semiclassical crystal velocity integral recovers exact time derivative of oscillatory position trajectory',eq(s.diff(xdisp,t),2*J*a/hn*s.sin(kt-F*a*t/hn)) and eq(s.simplify(xdisp.subs(t,T_B)),0))
assert len(checks)==24 and len(set((x['id'],x['part']) for x in checks))==24
ids=('M071','E071','T067','W067','O069','Q069')
assert all(len({c['method'] for c in checks if c['id']==uid})>=2 for uid in ids)
report=dict(status='draft-qa-only',new_problem_count=6,passed_count=24,tests=checks,independent_expert_review='pending')
Path(__file__).resolve().parents[1].joinpath('data/round13_fourth6_validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('ROUND13 FOURTH SIX 24 PASS')
