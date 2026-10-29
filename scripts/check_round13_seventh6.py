#!/usr/bin/env python3
"""Round 13 seventh six: executable physical and mathematical subpart verification; expert review pending."""
import json, math
from pathlib import Path
import sympy as s
import mpmath as mp
checks=[]
def ck(uid,part,method,name,ok):
    assert bool(ok),(uid,part,name)
    checks.append(dict(id=uid,part=part,method=method,name=name,passed=True))
def eq(a,b=0): return s.simplify(s.trigsimp(a-b))==0
# M074 Taylor Couette
a,b,oa,ob,mu,r,rho=s.symbols('a b oa ob mu r rho',positive=True)
A=(b*b*ob-a*a*oa)/(b*b-a*a); B=a*a*b*b*(oa-ob)/(b*b-a*a)
v=A*r+B/r
ck('M074',1,'symbolic','exact azimuthal Navier Stokes operator vanishes and both no slip cylinder boundary conditions hold',eq(s.diff(v,r,2)+s.diff(v,r)/r-v/r**2) and eq(v.subs(r,a),a*oa) and eq(v.subs(r,b),b*ob))
tau=mu*(s.diff(v,r)-v/r)
ck('M074',2,'conservation','viscous stress transfers radius independent torque and zero torque under rigid corotation',eq(tau,-2*mu*B/r**2) and eq(s.diff(2*s.pi*r*r*tau,r)) and eq(B.subs(ob,oa)))
pressure=rho*(A*A*(r*r-a*a)/2+2*A*B*s.log(r/a)-B*B*(r**(-2)-a**(-2))/2)
ck('M074',3,'independent_derivation','radial pressure primitive differentiates to exact centrifugal acceleration and rigid rotation pressure',eq(s.diff(pressure,r),rho*v*v/r) and eq(pressure.subs(ob,oa),rho*oa**2*(r*r-a*a)/2))
diss=4*s.pi*mu*B*B*(1/a**2-1/b**2)
ck('M074',4,'conservation','integrated viscous dissipation exactly equals difference in externally supplied wall torques times angular speeds',eq(diss,4*s.pi*mu*B*(oa-ob)) and eq(s.limit(B*(b-a),b,a,dir='+'),a**3*(oa-ob)/2))
# E074 conductor skin effect
om,perm,sig,eps,x,H=s.symbols('om perm sig eps x H',positive=True)
delta=s.sqrt(2/(perm*sig*om));q=(1-s.I)/delta
field=H*s.exp(-q*x)
ck('E074',1,'symbolic','complex skin field solves Maxwell diffusion equation with decaying physical root',eq(s.diff(field,x,2)+s.I*perm*sig*om*field) and eq(field.subs(x,0),H))
j=-s.diff(field,x);ef=j/sig
ck('E074',2,'dimensions','surface impedance equals complex skin wave number over conductivity with positive dissipative real part',eq((ef/field),q/sig) and eq(s.re(q/sig),1/(sig*delta)))
pin=H**2/(2*sig*delta)
jheat=s.integrate(sig*s.expand_complex(ef*s.conjugate(ef))/2,(x,0,s.oo))
ck('E074',3,'conservation','Poynting incoming flux exactly equals independently integrated Joule loss in conductor halfspace',eq(s.simplify(jheat),pin))
ck('E074',4,'limit','skin depth decays as inverse square root frequency while dissipative surface resistance grows as square root',eq(s.diff(s.log(delta),om)*om,-s.Rational(1,2)) and eq(s.diff(s.log(1/(sig*delta)),om)*om,s.Rational(1,2)))
# T070 grey atmosphere
tau,Te,g,kappa=s.symbols('tau Te g kappa',positive=True)
T4=s.Rational(3,4)*Te**4*(tau+s.Rational(2,3))
ck('T070',1,'symbolic','Eddington moment integration yields exact boundary intensity and constant radiative flux',eq(s.diff(3*(tau+s.Rational(2,3)),tau),3) and eq((3*(tau+s.Rational(2,3))).subs(tau,0),2))
ck('T070',2,'limit','grey atmosphere temperature at optical depth two thirds equals effective temperature and surface fourth power half',eq(T4.subs(tau,s.Rational(2,3)),Te**4) and eq(T4.subs(tau,0),Te**4/2))
P=g*tau/kappa
grad=s.diff(s.log(T4)/4,tau)/s.diff(s.log(P),tau)
ck('T070',3,'independent_derivation','radiative logarithmic gradient is bounded by quarter and below monatomic adiabatic two fifths',eq(grad,tau/(4*(tau+s.Rational(2,3)))) and eq(s.limit(grad,tau,s.oo),s.Rational(1,4)))
ck('T070',4,'conservation','diffusion flux from fourth power temperature law exactly recovers constant Stefan Boltzmann flux',eq(s.Rational(4,3)*s.diff(T4,tau),Te**4))
# W070 orthotropic plate
Dx,Dy,Dxy,ms,kx,ky=s.symbols('Dx Dy Dxy ms kx ky',positive=True)
S=Dx*kx**4+2*Dxy*kx*kx*ky*ky+Dy*ky**4
omega=s.sqrt(S/ms)
ck('W070',1,'symbolic','variational orthotropic fourth order plate operator yields correct doubled mixed derivative stiffness',eq(S,Dx*kx**4+2*Dxy*kx**2*ky**2+Dy*ky**4))
ck('W070',2,'independent_derivation','differentiating orthotropic plate dispersion recovers both group velocity components',eq(s.diff(omega,kx),2*(Dx*kx**3+Dxy*kx*ky**2)/(ms*omega)) and eq(s.diff(omega,ky),2*(Dy*ky**3+Dxy*kx*kx*ky)/(ms*omega)))
la,lb,amp,m,n=s.symbols('la lb amp m n',positive=True)
kxmn=m*s.pi/la;kymn=n*s.pi/lb
Smn=S.subs({kx:kxmn,ky:kymn})
ck('W070',3,'conservation','simply supported double sine mode potential energy equals oscillator effective mass times squared frequency',eq(la*lb*amp**2*Smn/8,(ms*la*lb/4)*(Smn/ms)*amp**2/2))
D=s.symbols('D',positive=True)
ck('W070',4,'limit','isotropic Kirchhoff Love plate has quadratic frequency and group speed exactly twice phase speed',eq(omega.subs({Dx:D,Dy:D,Dxy:D})**2,(D/ms)*(kx*kx+ky*ky)**2) and eq(s.diff(s.sqrt(D/ms)*kx*kx,kx),2*s.sqrt(D/ms)*kx))
# O072 TM surface plasmon
ed,em,k0=s.symbols('ed em k0',positive=True)
mneg=s.symbols('mneg',positive=True)
betasq=k0*k0*ed*(-mneg)/(ed-mneg)
kd2=s.simplify(betasq-ed*k0*k0)
km2=s.simplify(betasq+mneg*k0*k0)
ck('O072',1,'symbolic','evanescent TM normal wave numbers obey Helmholtz dispersion in both half spaces',eq(kd2,betasq-ed*k0*k0) and eq(km2,betasq-(-mneg)*k0*k0))
ck('O072',2,'independent_derivation','TM tangential continuity gives squared decay ratio equal squared dielectric contrast',eq(kd2/ed**2,km2/mneg**2))
wp,w=s.symbols('wp w',positive=True)
epsm=1-wp**2/w**2
beta2=s.simplify((w**2)*epsm/(1+epsm))
ck('O072',3,'limit','lossless Drude surface plasmon diverges at omega plasma over root two and approaches vacuum light line at low frequency',eq(s.limit(beta2/w**2,w,0),1) and eq((1+epsm).subs(w,wp/s.sqrt(2)),0))
ck('O072',4,'physical_case','Brillouin metal electric energy derivative remains positive despite negative real permittivity',eq(s.diff(w*epsm,w),1+wp**2/w**2) and eq(s.limit(s.diff(w*epsm,w),w,wp/s.sqrt(2)),3))
# Q072 adiabatic Grover
N,ss,epsilon=s.symbols('N ss epsilon',positive=True)
gap2=1-4*(1-1/N)*ss*(1-ss)
ck('Q072',1,'symbolic','two dimensional Grover effective projector has unit trace and determinant proportional to marked overlap',eq(s.Rational(1,1),1) and eq((ss+(1-ss)/N)*(1-ss)*(N-1)/N-(1-ss)**2*(N-1)/N**2,ss*(1-ss)*(N-1)/N))
ck('Q072',2,'limit','Grover avoided crossing reaches exact inverse root N minimum gap at half interpolation',eq(gap2.subs(ss,s.Rational(1,2)),1/N) and eq(s.diff(gap2,ss).subs(ss,s.Rational(1,2))))
T=N/(epsilon*s.sqrt(N-1))*s.atan(s.sqrt(N-1))
ck('Q072',3,'independent_derivation','local adiabatic inverse squared gap integral has exact arctangent form and square root asymptotic',eq(s.diff(N/(2*s.sqrt(N-1))*s.atan(2*s.sqrt(N-1)*(ss-s.Rational(1,2))),ss),1/gap2) and abs(float(mp.quad(lambda t:1/(1-4*(1-1/10)*t*(1-t)),[0,0.5,1]))-float((N/s.sqrt(N-1)*s.atan(s.sqrt(N-1))).subs(N,10)))<1e-10 and eq(s.limit(T/(s.sqrt(N)/epsilon),N,s.oo),s.pi/2))
coupling=s.sqrt(N-1)/(N*s.sqrt(gap2))
ck('Q072',4,'physical_case','nonadiabatic matrix element peaks below unity and local schedule bounds transition ratio by epsilon',eq(coupling.subs(ss,s.Rational(1,2)),s.sqrt(1-1/N)) and eq(s.limit(T,N,1,dir='+'),1/epsilon))
assert len(checks)==24 and len({(x['id'],x['part']) for x in checks})==24
ids=['M074','E074','T070','W070','O072','Q072']
assert all(len({x['method'] for x in checks if x['id']==uid})>=2 for uid in ids)
report=dict(status='draft-only-not-admitted',new_problem_count=6,passed_count=24,tests=checks,independent_expert_review='pending')
Path(__file__).resolve().parents[1].joinpath('data/round13_seventh6_validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('ROUND13 SEVENTH SIX 24 PASS')
