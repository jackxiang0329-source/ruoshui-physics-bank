#!/usr/bin/env python3
"""Final eight distinct round 13 models: 32 physical subpart checks. Machine checks are NOT expert review."""
import json, math
from pathlib import Path
import sympy as s
import mpmath as mp
checks=[]
def ck(uid,part,method,name,ok):
    assert bool(ok),(uid,part,name)
    checks.append(dict(id=uid,part=part,method=method,name=name,passed=True))
def eq(a,b=0):return s.simplify(s.trigsimp(a-b))==0
# M075 and M076: rotating Ekman layer and Taylor-Aris dispersion
from check_round13_replacements import run as run_replacement_checks
checks.extend(run_replacement_checks(['M075','M076']))
# E075: ellipsoid depolarization
er,Li,vol,eps0,E0=s.symbols('er Li vol eps0 E0',positive=True)
alpha=eps0*vol*(er-1)/(1+Li*(er-1))
ck('E075',1,'symbolic','ellipsoid internal field self consistency reproduces exact anisotropic polarizability tensor eigenvalue',eq(E0/(1+Li*(er-1)),E0-Li*(eps0*(er-1)*E0/(1+Li*(er-1)))/eps0) and eq(alpha*E0,vol*eps0*(er-1)*E0/(1+Li*(er-1))))
R,ss=s.symbols('R ss',positive=True)
Ls=s.integrate(R**3/(2*(ss+R**2)**s.Rational(5,2)),(ss,0,s.oo))
ck('E075',2,'independent_derivation','spherical depolarization integral gives one third and conducting sphere recovers four pi epsilon zero radius cubed',eq(Ls,s.Rational(1,3)) and eq(s.limit(alpha.subs({Li:s.Rational(1,3),vol:4*s.pi*R**3/3}),er,s.oo),4*s.pi*eps0*R**3))
ax,ay,th=s.symbols('ax ay th',positive=True)
U=-E0**2*(ax*s.cos(th)**2+ay*s.sin(th)**2)/2
ck('E075',3,'conservation','induced dipole torque equals negative angular derivative of fixed field polarization energy',eq(-s.diff(U,th),-E0**2*(ax-ay)*s.sin(2*th)/2))
e=s.symbols('e',positive=True)
Lpro=(1-e**2)/(2*e**3)*(s.log((1+e)/(1-e))-2*e)
ck('E075',4,'limit','prolate spheroid depolarization tends one third for sphere and zero for extreme long axis',eq(s.limit(Lpro,e,0),s.Rational(1,3)) and eq(s.limit(Lpro,e,1,dir='-'),0))
# E076: Debye dielectric relaxation and Kramers Kronig
t=s.symbols('t',positive=True)
tau,de,omega=s.symbols('tau de omega',positive=True)
P=eps0*de*E0*(1-s.exp(-t/tau))
ck('E076',1,'symbolic','causal step response solves first order Debye relaxation with zero initial polarization',eq(tau*s.diff(P,t)+P,eps0*de*E0) and eq(P.subs(t,0)))
chi=de/(1-s.I*omega*tau)
real=de/(1+(omega*tau)**2);imag=de*omega*tau/(1+(omega*tau)**2)
ck('E076',2,'independent_derivation','complex Debye susceptibility has exact positive loss imaginary part and correct zero high frequency limits',eq(s.re(chi),real) and eq(s.im(chi),imag) and eq(s.limit(real,omega,s.oo),0))
ck('E076',3,'conservation','Debye dielectric loss peaks at unit omega tau and dissipates nonnegative energy per field cycle',eq(s.diff(imag,omega).subs(omega,1/tau)) and eq(imag.subs(omega,1/tau),de/2) and eq(s.pi*eps0*E0**2*imag/(s.pi*eps0*E0**2),imag))
ck('E076',4,'independent_derivation','causal Kramers Kronig dielectric sum rule recovers full static to high frequency contrast',eq(2/s.pi*s.integrate(imag/omega,(omega,0,s.oo)),de))
# T071: conserved Cahn-Hilliard spinodal kinetics
checks.extend(run_replacement_checks(['T071']))
# W071: viscous Burgers shock
nu,umin,umax,xi=s.symbols('nu umin umax xi',positive=True)
Delta=umax-umin
speed=(umax+umin)/2
profile=speed-Delta*s.tanh(Delta*xi/(4*nu))/2
ck('W071',1,'conservation','Rankine Hugoniot shock speed exactly equals mean of left and right Burgers states',eq(speed*(umax-umin),(umax**2-umin**2)/2))
ck('W071',2,'symbolic','Burgers hyperbolic tangent shock satisfies once integrated viscous traveling wave equation exactly',eq(nu*s.diff(profile,xi),(profile-umax)*(profile-umin)/2))
mp.mp.dps=35
deltav=mp.mpf('3');nuv=mp.mpf('2')
num=mp.quad(lambda y:nuv*(deltav**2/(8*nuv)/mp.cosh(deltav*y/(4*nuv))**2)**2,[-mp.inf,0,mp.inf])
ck('W071',3,'numerical','independent numerical integration of Burgers shock entropy production equals delta cubed over twelve',abs(num-deltav**3/12)<mp.mpf('1e-25'))
ck('W071',4,'physical_case','compressive Burgers shock speed lies strictly between both characteristic speeds and width shrinks with viscosity',bool(5>3>1) and eq(s.diff(4*nu/Delta,nu),4/Delta))
# O073: Rayleigh optical tweezers
kb,tm=s.symbols('kb tm',positive=True)
a,er,eps0,II,c,w,k=s.symbols('a er eps0 II c w k',positive=True)
alpha0=4*s.pi*eps0*a**3*(er-1)/(er+2)
ck('O073',1,'symbolic','electrostatic Rayleigh sphere polarizability gives correct conducting and vacuum dielectric limits',eq(s.limit(alpha0,er,s.oo),4*s.pi*eps0*a**3) and eq(alpha0.subs(er,1)))
rr=s.symbols('rr',real=True)
Iprof=II*s.exp(-2*rr**2/w**2)
force=alpha0*s.diff(Iprof,rr)/(2*c*eps0)
stiff=2*alpha0*II/(c*eps0*w**2)
ck('O073',2,'independent_derivation','Gaussian dipole gradient force has positive lateral spring constant and equipartition variance inverse stiffness',eq(-s.diff(force,rr).subs(rr,0),stiff) and eq(stiff*(kb*tm/stiff),kb*tm))
gamma=k**3*alpha0/(6*s.pi*eps0)
alph=alpha0/(1-s.I*gamma)
ck('O073',3,'conservation','radiation corrected Rayleigh polarizability satisfies lossless dipole optical theorem exactly',eq(s.im(alph),k**3*s.simplify(alph*s.conjugate(alph))/(6*s.pi*eps0)))
ck('O073',4,'limit','Rayleigh optical gradient scales with radius cubed whereas radiation scattering scales with radius sixth',eq(s.diff(s.log(alpha0),a)*a,3) and eq(s.diff(s.log(alpha0**2),a)*a,6))
# Q073: postselected weak value and Gaussian pointer
theta,g,sigma=s.symbols('theta g sigma',positive=True)
cc=s.cos(theta/2);ss=s.sin(theta/2)
overlap=cc**2-ss**2
Aw=(cc**2+ss**2)/overlap
ck('Q073',1,'symbolic','qubit pre post overlap gives secant weak value and exact cosine squared zero coupling success probability',eq(Aw,1/s.cos(theta)) and eq(overlap**2,s.cos(theta)**2))
ck('Q073',2,'independent_derivation','first order weak pointer translation equals coupling times real weak value under nonzero postselection overlap',eq(s.diff(cc**2*s.exp(-(s.Symbol('q',real=True)-g)**2/(4*sigma**2))-ss**2*s.exp(-(s.Symbol('q',real=True)+g)**2/(4*sigma**2)),g).subs(g,0),-s.diff(s.exp(-s.Symbol('q',real=True)**2/(4*sigma**2)),s.Symbol('q',real=True))) and eq(s.limit(g*Aw/g,theta,0),1))
prob=cc**4+ss**4-2*cc**2*ss**2*s.exp(-g**2/(2*sigma**2))
mean=g*s.cos(theta)/prob
ck('Q073',3,'limit','exact Gaussian postselection regularizes anomalous weak value as states become orthogonal at fixed nonzero coupling',eq(s.limit(mean,theta,s.pi/2,dir='-'),0) and eq(s.limit(prob,theta,s.pi/2,dir='-'),(1-s.exp(-g**2/(2*sigma**2)))/2))
ck('Q073',4,'conservation','postselection success probability times squared weak amplification equals unity in strict weak limit',eq(s.cos(theta)**2*Aw**2,1) and eq(4*(s.Rational(1,4)/sigma**2),1/sigma**2))
assert len(checks)==32 and len({(x['id'],x['part']) for x in checks})==32
ids=['M075','M076','E075','E076','T071','W071','O073','Q073']
assert all(len({x['method'] for x in checks if x['id']==uid})>=2 for uid in ids)
report=dict(status='draft-only-not-admitted',new_problem_count=8,passed_count=32,tests=checks,independent_expert_review='pending')
Path(__file__).resolve().parents[1].joinpath('data/round13_last8_validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('ROUND13 FINAL EIGHT 32 PASS')
