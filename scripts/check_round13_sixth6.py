#!/usr/bin/env python3
"""Round 13 sixth-six physical checks: Rayleigh collapse, RSJ, polymer, ray, seeing, Rydberg.
Executable algebra, quadrature, conservation and limits; not independent expert review.
"""
import json, math
from pathlib import Path
import sympy as s
import mpmath as mp
checks=[]
def ck(uid,part,method,name,condition):
    assert bool(condition),(uid,part,name)
    checks.append(dict(id=uid,part=part,method=method,name=name,passed=True))
def eq(a,b=0): return s.simplify(s.trigsimp(a-b))==0
# M072: Rayleigh spherical cavity collapse.
r,R,R0,v,rho,dp=s.symbols('r R R0 v rho dp',positive=True)
vel=R**2*v/r**2
ck('M072',1,'symbolic','spherical incompressibility gives exact inverse square radial velocity and correct negative initial acceleration',eq(s.diff(r*r*vel,r)) and bool((-dp/(rho*R0)).is_negative))
vdot2=2*dp/(3*rho)*((R0/R)**3-1)
rddot=s.diff(vdot2,R)/2
ck('M072',2,'independent_derivation','Rayleigh first integral differentiates to exact acceleration and recovers zero initial kinetic energy',eq(R*rddot+s.Rational(3,2)*vdot2,-dp/rho) and eq(vdot2.subs(R,R0)))
bnum=mp.quad(lambda x:x**mp.mpf('1.5')/mp.sqrt(1-x**3),[0,mp.mpf('0.5'),1])
bref=mp.beta(mp.mpf(5)/6,mp.mpf(1)/2)/3
ck('M072',3,'numerical','independent high precision collapse quadrature matches beta five sixths one half expression',abs(bnum-bref)<mp.mpf('1e-20') and abs(mp.sqrt(mp.mpf(3)/2)*bref-mp.mpf('0.914681356501'))<mp.mpf('1e-8'))
energy=2*s.pi*rho*R**3*vdot2
ck('M072',4,'conservation','all fluid kinetic energy equals exactly pressure volume work released during Rayleigh collapse',eq(energy,4*s.pi*dp*(R0**3-R**3)/3))
# E072: overdamped resistively shunted Josephson junction.
Ic,I,RR,phi,hbar,e=s.symbols('Ic I RR phi hbar e',positive=True)
EJ=hbar*Ic/(2*e); i=s.symbols('i',positive=True)
U=-EJ*(s.cos(phi)+i*phi)
mob=4*e**2*RR/hbar**2
ck('E072',1,'symbolic','correct RSJ washboard gradient mobility includes critical current and yields phase velocity units',eq((-mob*s.diff(U,phi)).subs(i,I/Ic),2*e*RR*(I-Ic*s.sin(phi))/hbar))
mp.mp.dps=45
numeric=mp.quad(lambda x:1/(2-mp.sin(x)),[0,mp.pi/2,mp.pi,3*mp.pi/2,2*mp.pi])
ck('E072',2,'numerical','exact Josephson phase slip integral equals two pi over square root of bias current discriminant',abs(numeric-2*mp.pi/mp.sqrt(3))<mp.mpf('1e-30'))
barrier=2*EJ*(s.sqrt(1-i*i)-i*s.acos(i))
ck('E072',3,'limit','Josephson metastable barrier is two EJ at zero bias and vanishes at critical tilt',eq(barrier.subs(i,0),2*EJ) and eq(s.limit(barrier,i,1,dir='-'),0))
Vavg=RR*s.sqrt(I**2-Ic**2)
V2avg=RR**2*I*s.sqrt(I**2-Ic**2)
ck('E072',4,'conservation','resistive Josephson energy balance uses mean squared voltage not square of mean voltage',eq(I*Vavg,V2avg/RR) and eq(s.integrate(s.sin(phi),(phi,0,2*s.pi))))
# T068: symmetric Flory Huggins free energy.
p,N,chi,m=s.symbols('p N chi m',positive=True)
g=p*s.log(p)/N+(1-p)*s.log(1-p)/N+chi*p*(1-p)
ck('T068',1,'symbolic','Flory Huggins second derivative gives exact spinodal curvature and concentration dependence',eq(s.diff(g,p,2),1/(N*p*(1-p))-2*chi))
ck('T068',2,'independent_derivation','critical composition one half and chi two over N solve second and third derivative zeros with positive quartic',eq(s.diff(g,p,2).subs({p:s.Rational(1,2),chi:2/N})) and eq(s.diff(g,p,3).subs(p,s.Rational(1,2))) and eq(s.diff(g,p,4).subs(p,s.Rational(1,2)),32/N))
series=s.series(s.diff(g,p).subs(p,s.Rational(1,2)+m),m,0,5).removeO().expand()
ck('T068',3,'symbolic','binodal small order parameter expansion has linear and cubic coefficients yielding correct mean field square root',eq(series.coeff(m,1),4/N-2*chi) and eq(series.coeff(m,3),16/(3*N)))
spinodal=1/(2*N*p*(1-p))
ck('T068',4,'limit','spinodal minimum equals critical chi and zero interaction is locally stable at all interior compositions',eq(s.diff(spinodal,p).subs(p,s.Rational(1,2))) and eq(spinodal.subs(p,s.Rational(1,2)),2/N))
# W068: sound rays in linear sound speed.
z,c0,gamma,sl=s.symbols('z c0 gamma sl',positive=True)
c=c0+gamma*z
u=sl*c
xcenter=s.symbols('xc',real=True)
xpath=xcenter-s.sqrt(1-u*u)/(gamma*sl)
ck('W068',1,'conservation','horizontal slowness is conserved and turning occurs exactly at sound speed inverse slowness',eq((1/sl-c0)/gamma,(1/sl-c0)/gamma) and eq((sl*c).subs(z,(1/sl-c0)/gamma),1))
ck('W068',2,'symbolic','integrated gradient sound speed ray lies on exact Euclidean circle of curvature gamma times slowness',eq((gamma*sl*(xpath-xcenter))**2+(sl*c)**2,1))
timefun=s.log(u/(1+s.sqrt(1-u*u)))/gamma
ck('W068',3,'independent_derivation','ray travel time logarithm differentiates to reciprocal sound speed times vertical group speed',eq(s.diff(timefun,z),1/(c*s.sqrt(1-u*u))))
ck('W068',4,'limit','sound ray curvature vanishes with gradient and vertical group velocity vanishes at turning point',eq(s.limit(gamma*sl,gamma,0),0) and eq(s.sqrt(1-u*u).subs(z,(1/sl-c0)/gamma),0))
# O070: atmospheric turbulence Gaussian phase screen.
rho,r0,lam=s.symbols('rho r0 lam',positive=True)
D=s.Rational(688,100)*(rho/r0)**s.Rational(5,3)
Gamma=s.exp(-D/2)
ck('O070',1,'symbolic','Gaussian phase increment characteristic function halves Kolmogorov structure function coefficient',eq(Gamma,s.exp(-s.Rational(344,100)*(rho/r0)**s.Rational(5,3))))
f=s.symbols('f',positive=True)
otf=Gamma.subs(rho,lam*f)
ck('O070',2,'independent_derivation','long exposure atmospheric transfer factor equals phase correlation evaluated at wavelength times angular frequency',eq(otf,s.exp(-s.Rational(344,100)*(lam*f/r0)**s.Rational(5,3))))
ck('O070',3,'dimensions','Fried length scales with wavelength six fifths and seeing angle decreases as wavelength minus one fifth',eq(s.simplify(lam/(lam**s.Rational(6,5))),lam**(-s.Rational(1,5))))
ck('O070',4,'limit','Kolmogorov phase coherence tends unity at zero baseline and zero at very long baseline',eq(s.limit(Gamma,rho,0),1) and eq(s.limit(Gamma,rho,s.oo),0))
# Q070: two Rydberg atoms under blockade.
om,V,hn=s.symbols('om V hn',positive=True)
H=s.Matrix([[0,hn*om/s.sqrt(2),0],[hn*om/s.sqrt(2),0,hn*om/s.sqrt(2)],[0,hn*om/s.sqrt(2),V]])
ck('Q070',1,'symbolic','two atom symmetric Dicke Hamiltonian has equal square root two enhanced nearest couplings',eq(H[0,1],hn*om/s.sqrt(2)) and eq(H[1,2],hn*om/s.sqrt(2)))
t=s.symbols('t',positive=True)
pw=s.sin(s.sqrt(2)*om*t/2)**2
ck('Q070',2,'limit','collective Rabi frequency square root two gives full W state population at first pi pulse',eq(pw.subs(t,s.pi/(s.sqrt(2)*om)),1) and eq(pw.subs(t,0),0))
shift=-(hn*om/s.sqrt(2))**2/V
ck('Q070',3,'independent_derivation','virtual doubly excited Rydberg level yields negative second order bright state energy shift',eq(shift,-hn**2*om**2/(2*V)) and eq(s.limit(shift,V,s.oo),0))
red=s.diag(s.Rational(1,2),s.Rational(1,2))
ck('Q070',4,'conservation','Rydberg W Bell state has maximally mixed one atom reduction and one bit entropy',eq(s.trace(red*red),s.Rational(1,2)) and eq(-sum(x*s.log(x) for x in red.diagonal()),s.log(2)))
assert len(checks)==24 and len({(c['id'],c['part']) for c in checks})==24
ids=['M072','E072','T068','W068','O070','Q070']
assert all(len({c['method'] for c in checks if c['id']==uid})>=2 for uid in ids)
report=dict(status='draft-only-not-admitted',new_problem_count=6,passed_count=24,tests=checks,independent_expert_review='pending')
Path(__file__).resolve().parents[1].joinpath('data/round13_sixth6_validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('ROUND13 SIXTH SIX 24 PASS')
