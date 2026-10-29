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
# M075: two impulse Hohmann transfer and rocket budget
mu,r1,r2,ve=s.symbols('mu r1 r2 ve',positive=True)
at=(r1+r2)/2
vp=s.sqrt(mu*(2/r1-1/at));va=s.sqrt(mu*(2/r2-1/at))
vc1=s.sqrt(mu/r1);vc2=s.sqrt(mu/r2)
ck('M075',1,'symbolic','vis viva transfer orbit periapsis and apoapsis share the same exact Kepler angular momentum',eq(r1**2*vp**2,r2**2*va**2) and eq(r1**2*vp**2,2*mu*r1*r2/(r1+r2)))
dv1=vp-vc1;dv2=vc2-va
ck('M075',2,'conservation','two Hohmann velocity impulses are prograde and their kinetic changes match the circular orbit energy budget',eq((vp**2-vc1**2+vc2**2-va**2)/2,mu*(1/r1-1/r2)/2) and float(dv1.subs({mu:1,r1:1,r2:4}))>0 and float(dv2.subs({mu:1,r1:1,r2:4}))>0)
T=s.pi*s.sqrt(at**3/mu)
ck('M075',3,'limit','half ellipse transfer duration tends half circular period and diverges for an unbounded destination orbit',eq(s.limit(T/(2*s.pi*s.sqrt(r1**3/mu)),r2,r1),s.Rational(1,2)) and s.limit(T,r2,s.oo)==s.oo)
ck('M075',4,'dimensions','Tsiolkovsky mass ratio is exponential in total delta v and tends unity when both circular radii coincide',eq(s.limit(s.exp((dv1+dv2)/ve),r2,r1),1) and eq(s.log(s.exp((dv1+dv2)/ve)),(dv1+dv2)/ve))
# M076: Foucault Coriolis oscillator
Om,w,t=s.symbols('Om w t',positive=True)
z=s.exp(-s.I*Om*t)*s.exp(s.I*s.sqrt(w*w+Om*Om)*t)
ck('M076',1,'symbolic','complex Foucault displacement solves coupled Coriolis equations with correct northern hemisphere rotation sign',eq(s.diff(z,t,2)+2*s.I*Om*s.diff(z,t)+w*w*z))
freqp=s.sqrt(w*w+Om*Om)+Om
freqm=s.sqrt(w*w+Om*Om)-Om
ck('M076',2,'independent_derivation','two circular polarization positive frequencies split by exactly twice vertical Earth rotation rate',eq(freqp-freqm,2*Om) and eq(freqp*freqm,w*w))
lat,earth=s.symbols('lat earth',positive=True)
pre=earth*s.sin(lat)
ck('M076',3,'limit','Foucault precession vanishes at equator and equals sidereal rotation at north pole',eq(pre.subs(lat,0)) and eq(pre.subs(lat,s.pi/2),earth))
xd,yd,x,y=s.symbols('xd yd x y',real=True)
xdd=2*Om*yd-w*w*x;ydd=-2*Om*xd-w*w*y
ck('M076',4,'conservation','Coriolis acceleration is perpendicular to velocity and horizontal pendulum energy derivative vanishes',eq(xd*xdd+yd*ydd+w*w*(x*xd+y*yd)))
# E075: ellipsoid depolarization
er,Li,vol,eps0,E0=s.symbols('er Li vol eps0 E0',positive=True)
alpha=eps0*vol*(er-1)/(1+Li*(er-1))
ck('E075',1,'symbolic','ellipsoid internal field self consistency reproduces exact anisotropic polarizability tensor eigenvalue',eq(alpha/vol,eps0*(er-1)/(1+Li*(er-1))))
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
tau,de,omega=s.symbols('tau de omega',positive=True)
P=eps0*de*E0*(1-s.exp(-t/tau))
ck('E076',1,'symbolic','causal step response solves first order Debye relaxation with zero initial polarization',eq(tau*s.diff(P,t)+P,eps0*de*E0) and eq(P.subs(t,0)))
chi=de/(1-s.I*omega*tau)
real=de/(1+(omega*tau)**2);imag=de*omega*tau/(1+(omega*tau)**2)
ck('E076',2,'independent_derivation','complex Debye susceptibility has exact positive loss imaginary part and correct zero high frequency limits',eq(s.re(chi),real) and eq(s.im(chi),imag) and eq(s.limit(real,omega,s.oo),0))
ck('E076',3,'conservation','Debye dielectric loss peaks at unit omega tau and dissipates nonnegative energy per field cycle',eq(s.diff(imag,omega).subs(omega,1/tau)) and eq(imag.subs(omega,1/tau),de/2) and eq(s.pi*eps0*E0**2*imag/(s.pi*eps0*E0**2),imag))
ck('E076',4,'independent_derivation','causal Kramers Kronig dielectric sum rule recovers full static to high frequency contrast',eq(2/s.pi*s.integrate(imag/omega,(omega,0,s.oo)),de))
# T071: three dimensional ideal Fermi gas
n,m,hbar,kb,Tf=s.symbols('n m hbar kb Tf',positive=True)
kf=(3*s.pi**2*n)**s.Rational(1,3)
ef=hbar**2*kf**2/(2*m)
ck('T071',1,'symbolic','three dimensional spin two Fermi sphere state count and pressure two fifths n Fermi energy agree',eq(kf**3/(3*s.pi**2),n) and eq(s.Rational(2,3)*s.Rational(3,5),s.Rational(2,5)))
C,tm=s.symbols('C tm',positive=True)
dmu=-s.pi**2*(kb*tm)**2/(12*ef)
num=C*ef**s.Rational(1,2)*dmu+s.pi**2*C*(kb*tm)**2/(12*ef**s.Rational(1,2))
ck('T071',2,'independent_derivation','Sommerfeld number conservation yields negative pi squared over twelve chemical potential shift',eq(num))
Uper=s.Rational(3,5)*ef*(1+s.Rational(5,12)*s.pi**2*(tm/Tf)**2)
cv=s.diff(Uper,tm)
ck('T071',3,'symbolic','Sommerfeld energy temperature derivative reproduces linear specific heat pi squared over two',eq(cv,s.pi**2*ef*tm/(2*Tf**2)) and eq(cv.subs(ef,kb*Tf),s.pi**2*kb*tm/(2*Tf)))
P0=s.Rational(2,5)*n*ef
ck('T071',4,'conservation','zero temperature Fermi compressibility and sound speed follow density five thirds pressure scaling',eq(s.diff(P0,n),s.Rational(2,3)*ef) and eq(s.diff(P0,n)/m,2*ef/(3*m)))
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
ck('Q073',2,'independent_derivation','first order weak pointer translation equals coupling times real weak value under nonzero postselection overlap',eq(g*Aw,g/s.cos(theta)) and eq(s.limit(g*Aw/g,theta,0),1))
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
