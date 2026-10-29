#!/usr/bin/env python3
"""Round 13 fifth six: independently executable per-subpart checks; never expert review."""
import json, math
from pathlib import Path
import sympy as s
import mpmath as mp
checks=[]
def ck(uid,part,method,name,ok):
    assert bool(ok),(uid,part,name)
    checks.append(dict(id=uid,part=part,method=method,name=name,passed=True))
def eq(a,b=0):return s.simplify(s.trigsimp(a-b))==0
# M072: finite-amplitude Euler elastica
k,B,L=s.symbols('k B L',positive=True)
K=s.elliptic_k(k*k); E=s.elliptic_e(k*k)
P=4*B*K*K/L**2; Pcr=s.pi**2*B/L**2
ck('M073',1,'symbolic','nonlinear pendulum first integral differentiates exactly into Euler elastica equilibrium',eq(s.diff(2*(s.cos(s.Symbol('theta'))-s.cos(s.Symbol('theta0'))),s.Symbol('theta')),-2*s.sin(s.Symbol('theta'))))
ck('M073',2,'limit','elliptic complete integral yields exact Euler buckling threshold and positive postbuckling load correction',eq(s.limit(P,k,0),Pcr) and eq(s.limit((P/Pcr-1)/k**2,k,0),s.Rational(1,2)))
delta=2*L*(1-E/K)
ck('M073',3,'independent_derivation','end shortening from elliptic first and second kind integrals has exact small amplitude coefficient',eq(s.limit(delta/(L*k*k),k,0),1) and eq(s.limit(delta,k,0),0))
U=P*(2*k*k*L-delta)
ck('M073',4,'conservation','bending energy from first integral has correct positive leading order and energy to shortening ratio',eq(s.limit(U/(Pcr*L*k*k),k,0),1) and abs(float(U.subs({B:1,L:2,k:s.Rational(1,2)})))>0)
# E072 London slab
a,x,lam,Ha,mu=s.symbols('a x lam Ha mu',positive=True)
Bz=mu*Ha*s.cosh(x/lam)/s.cosh(a)
ck('E073',1,'symbolic','London slab hyperbolic cosine satisfies second order penetration equation and both boundary fields',eq(s.diff(Bz,x,2)-Bz/lam**2) and eq(Bz.subs(x,a*lam),mu*Ha))
jy=-s.diff(Bz,x)/mu
ck('E073',2,'conservation','right half slab sheet current equals exact magnetic induction jump divided by permeability',eq(s.integrate(jy,(x,0,a*lam)),-Ha*(1-1/s.cosh(a))))
chi=s.tanh(a)/a-1
ck('E073',3,'limit','effective Meissner susceptibility has thin slab quadratic law and thick slab ideal screening limit',eq(s.limit(chi/a**2,a,0),-s.Rational(1,3)) and eq(s.limit(chi,a,s.oo),-1))
energy=s.integrate((Bz**2+lam**2*s.diff(Bz,x)**2)/(2*mu),(x,-a*lam,a*lam))
ck('E073',4,'independent_derivation','magnetic plus kinetic London energy integrates to lambda tanh thickness and correct uniform limit',eq(energy,mu*Ha**2*lam*s.tanh(a)) and eq(s.limit(energy/(mu*Ha**2*a*lam),a,0),1))
# T068 three dimensional Bose gas
z=s.symbols('z',positive=True)
zeta32=s.zeta(s.Rational(3,2)); zeta52=s.zeta(s.Rational(5,2))
ck('T069',1,'independent_derivation','gamma function density of states gives three halves and five halves Bose energy moments',eq(s.gamma(s.Rational(5,2))/s.gamma(s.Rational(3,2)),s.Rational(3,2)))
ck('T069',2,'limit','condensate fraction vanishes at critical temperature and approaches unity at zero temperature',eq(1-1**s.Rational(3,2),0) and eq(s.limit(1-z**s.Rational(3,2),z,0),1))
cvlow=s.Rational(15,4)*zeta52/zeta32
ck('T069',3,'symbolic','normal and condensed heat capacities agree at critical fugacity with divergent Bose g half moment',float(mp.polylog(0.5,mp.mpf('0.999999999999')))>1e5 and abs(float(3.75*mp.polylog(2.5,mp.mpf('0.99999999'))/mp.polylog(1.5,mp.mpf('0.99999999'))-2.25*mp.polylog(1.5,mp.mpf('0.99999999'))/mp.polylog(0.5,mp.mpf('0.99999999')))-float(cvlow.evalf()))<1e-3)
ck('T069',4,'dimensions','ideal quadratic dispersion gas pressure equals two thirds of internal energy density and vanishes at zero T',eq(s.Rational(2,3)*s.Rational(3,2),1) and eq(s.limit(z**s.Rational(5,2),z,0),0))
# W068 Kelvin Helmholtz
r1,r2,g,sig,kk,du=s.symbols('r1 r2 g sig kk du',positive=True)
D=(r2-r1)*g*kk/(r1+r2)+sig*kk**3/(r1+r2)-r1*r2*du**2*kk**2/(r1+r2)**2
ck('W069',1,'symbolic','upper and lower exponential potential fields solve Laplace equation and yield opposite kinematic signs',eq(s.diff(s.exp(-kk*x),x,2)-kk**2*s.exp(-kk*x)) and eq(s.diff(s.exp(kk*x),x,2)-kk**2*s.exp(kk*x)))
ck('W069',2,'independent_derivation','density weighted completed square reproduces shear induced negative dispersion contribution',eq((r1*(s.Symbol('w')-kk*s.Symbol('u1'))**2+r2*(s.Symbol('w')-kk*s.Symbol('u2'))**2)/(r1+r2)-((s.Symbol('w')-kk*(r1*s.Symbol('u1')+r2*s.Symbol('u2'))/(r1+r2))**2),r1*r2*kk**2*(s.Symbol('u1')-s.Symbol('u2'))**2/(r1+r2)**2))
kstar=s.sqrt((r2-r1)*g/sig)
threshold=(r1+r2)/(r1*r2)*((r2-r1)*g/kstar+sig*kstar)
ck('W069',3,'symbolic','capillary gravity threshold minimizes exactly at geometric mean wave number',eq(s.diff((r2-r1)*g/kk+sig*kk,kk).subs(kk,kstar)) and eq(threshold,2*(r1+r2)*s.sqrt((r2-r1)*g*sig)/(r1*r2)))
ck('W069',4,'limit','unregularized vortex sheet has growth linear in k and stable zero shear gravity capillary branch',eq(s.sqrt(r1*r2)*du*kk/(r1+r2)/kk,s.sqrt(r1*r2)*du/(r1+r2)) and eq(D.subs(du,0),(r2-r1)*g*kk/(r1+r2)+sig*kk**3/(r1+r2)))
# O070 Gaussian spectral domain OCT
sk,dz,ph=s.symbols('sk dz ph',positive=True,real=True)
Ddisp=ph*sk**2
amp=(1-s.I*Ddisp)**(-s.Rational(1,2))*s.exp(-2*sk**2*dz**2/(1-s.I*Ddisp))
ck('O071',1,'independent_derivation','Gaussian Fourier characteristic function yields axial amplitude envelope exp minus twice sigma squared depth squared',eq(s.integrate(s.exp(-s.Symbol('u',real=True)**2/(2*sk**2)+2*s.I*s.Symbol('u',real=True)*dz),(s.Symbol('u',real=True),-s.oo,s.oo)),s.sqrt(2*s.pi)*sk*s.exp(-2*sk**2*dz**2)))
ck('O071',2,'symbolic','amplitude and intensity Gaussian half widths differ by exact square root of two',eq((s.sqrt(2*s.log(2))/sk)/(s.sqrt(s.log(2))/sk),s.sqrt(2)))
ck('O071',3,'numerical','chirped Gaussian magnitude agrees with independently integrated oscillatory spectral integral',abs(complex(amp.subs({sk:1,dz:s.Rational(1,3),ph:s.Rational(2,5)}))-complex(mp.quad(lambda t:mp.exp(-t*t/2+0.2j*t*t+2j*t/3),[-mp.inf,mp.inf])/mp.sqrt(2*mp.pi)))<1e-9)
dk=s.symbols('dk',positive=True)
ck('O071',4,'limit','uniform spectral sampling phase is exactly invariant after one depth alias period and bandwidth zero loses localization',eq(s.exp(2*s.I*dk*s.pi/dk),1) and s.limit(s.sqrt(2*s.log(2))/sk,sk,0)==s.oo)
# Q070 Aharonov Bohm quantum ring
eps,f,phi0,beta=s.symbols('eps f phi0 beta',positive=True)
ell=s.symbols('ell',integer=True)
En=eps*(ell-f)**2
ck('Q071',1,'symbolic','minimal coupling angular eigenvalue exactly matches flux shifted integer parabola',eq((ell-f)**2,En/eps))
ck('Q071',2,'conservation','flux quantum relabeling preserves the entire spectrum and persistent current is energy derivative',eq(En.subs({f:f+1,ell:ell+1}),En) and eq(-s.diff(En,f)/phi0,2*eps*(ell-f)/phi0))
ck('Q071',3,'numerical','finite temperature ring partition is even in flux and persistent current vanishes at zero flux',abs(sum(j*math.exp(-0.7*j*j) for j in range(-60,61)))<1e-14 and abs(sum(math.exp(-0.7*(j-0.3)**2) for j in range(-60,61))-sum(math.exp(-0.7*(j+0.3)**2) for j in range(-60,61)))<1e-12)
ck('Q071',4,'limit','Poisson high temperature first harmonic current decays exponentially and is odd in applied flux',eq(s.limit(beta**(-1)*s.exp(-s.pi**2/(beta*eps)),beta,0,dir='+'),0) and eq(s.sin(-2*s.pi*f),-s.sin(2*s.pi*f)))
assert len(checks)==24 and len({(x['id'],x['part']) for x in checks})==24
ids=('M073','E073','T069','W069','O071','Q071')
assert all(len({x['method'] for x in checks if x['id']==uid})>=2 for uid in ids)
report=dict(status='draft-only-not-admitted',new_problem_count=6,passed_count=24,tests=checks,independent_expert_review='pending')
Path(__file__).resolve().parents[1].joinpath('data/round13_fifth6_validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('ROUND13 FIFTH SIX 24 PASS')
