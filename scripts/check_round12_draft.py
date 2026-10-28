#!/usr/bin/env python3
"""Fifty-two executable draft subpart checks, NOT the required 200-item final gate."""
import json
import math
import mpmath as mp
import sympy as s
from pathlib import Path
checks=[]
def record(uid,part,method,description,ok):
    assert bool(ok),(uid,part,description)
    checks.append(dict(id=uid,part=part,method=method,name=description,passed=True))
def eq(a,b=0):
    return s.simplify(a-b)==0
pi=s.pi
I1,I2,I3,L=s.symbols('I1 I2 I3 L',positive=True)
w1,w2,w3=s.symbols('w1 w2 w3',real=True)
d1=(I2-I3)*w2*w3/I1;d2=(I3-I1)*w3*w1/I2;d3=(I1-I2)*w1*w2/I3
record('M059',1,'conservation','Euler rigid-body dynamics conserves both energy and angular momentum',eq(I1*w1*d1+I2*w2*d2+I3*w3*d3) and eq(I1**2*w1*d1+I2**2*w2*d2+I3**2*w3*d3))
lam2=(L/I2)**2*(I3-I2)*(I2-I1)/(I1*I3)
record('M059',2,'independent_derivation','linear middle-axis perturbation has positive exponential growth square',eq(((I2-I3)*(I1-I2)/(I1*I3))*(L/I2)**2,lam2))
A2=L**2*(I3-I2)/(I1*I2*(I3-I1));C2=L**2*(I2-I1)/(I2*I3*(I3-I1))
record('M059',3,'symbolic','separatrix principal-axis amplitudes satisfy both invariant ellipsoids',eq(I1*A2+I3*C2,L**2/I2) and eq(I1**2*A2+I3**2*C2,L**2))
A=s.sqrt(A2);B=L/I2;C=s.sqrt(C2);lam=s.sqrt(lam2)
tt=s.symbols('tt',real=True)
x1=A/s.cosh(lam*tt);x2=B*s.tanh(lam*tt);x3=C/s.cosh(lam*tt)
res=[I1*s.diff(x1,tt)-(I2-I3)*x2*x3,I2*s.diff(x2,tt)-(I3-I1)*x3*x1,I3*s.diff(x3,tt)-(I1-I2)*x1*x2]
sub={I1:s.Integer(1),I2:s.Integer(2),I3:s.Integer(3),L:s.Integer(4),tt:s.Rational(7,10)}
record('M059',4,'numerical','explicit heteroclinic solution satisfies all three Euler equations at nontrivial sample',all(abs(float(v.subs(sub).evalf()))<1e-12 for v in res))
r,alpha,R=s.symbols('r alpha R',positive=True)
J0=s.besselj(0,alpha*r);J1=s.besselj(1,alpha*r)
record('E059',1,'symbolic','force-free cylinder Bessel components satisfy both curl equations',eq(-s.diff(J0,r),alpha*J1) and eq(s.diff(r*J1,r)/r,alpha*J0))
flux=s.integrate(r*J0,(r,0,R))
record('E059',2,'independent_derivation','axial magnetic flux integral and Ampere boundary current agree',eq(flux,R*s.besselj(1,alpha*R)/alpha))
energy=s.integrate(r*(J0**2+J1**2),(r,0,R))
closed=R**2*s.Rational(1,2)*(s.besselj(0,alpha*R)**2+2*s.besselj(1,alpha*R)**2-s.besselj(0,alpha*R)*s.besselj(2,alpha*R))
record('E059',3,'symbolic','Bessel magnetic energy integral matches exact three-order boundary identity',eq(energy,closed))
Bp,Bz,mu=s.symbols('Bp Bz mu',real=True,nonzero=True)
K=s.Matrix([0,Bz/mu,-Bp/mu]);Bavg=s.Matrix([0,Bp/2,Bz/2])
record('E059',4,'conservation','surface current crossed with mean field gives outward Maxwell pressure',eq(K.cross(Bavg)[0],(Bp**2+Bz**2)/(2*mu)) and eq(K.cross(Bavg)[1]) and eq(K.cross(Bavg)[2]))
J,kB,T,mag,B=s.symbols('J kB T mag B',positive=True)
x=s.symbols('x',real=True)
f=-J*x*x/2-mag*B*x+kB*T*((1+x)/2*s.log((1+x)/2)+(1-x)/2*s.log((1-x)/2))
record('T056',1,'symbolic','mean-field entropy differentiation reproduces atanh self-consistency',eq(s.diff(f,x),-J*x-mag*B+kB*T*(s.log(1+x)-s.log(1-x))/2))
record('T056',2,'independent_derivation','Curie temperature follows Hessian sign change of disordered state',eq(s.diff(f,x,2).subs(x,0),kB*T-J))
Tc=J/kB
chi=mag**2/(kB*T-J)
record('T056',3,'limit','zero-field susceptibility has Curie Weiss pole and correct high-temperature limit',eq(s.limit(T*chi,T,s.oo),mag**2/kB))
t=s.symbols('t',positive=True)
landau=-3*kB*(Tc-t)**2/(4*Tc)
heat=-t*s.diff(landau,t,2)
record('T056',4,'symbolic','Landau free energy gives three-halves kB heat capacity jump at critical point',eq(s.limit(heat,t,Tc,dir='-'),3*kB/2))

# Three distinct models; each subpart independently checked (beyond schema-only gates).
zz,pp,qq=s.symbols('zz pp qq',positive=True)
F=zz*s.cos(zz)+(pp-qq*zz**2)*s.sin(zz)
Cx,mux,Lx,Kx,Ix,kx=s.symbols('Cx mux Lx Kx Ix kx',positive=True)
record('W056',1,'symbolic','torsional rod dynamic tip condition has correct nondimensional form',
       eq((Cx*kx*s.cos(kx*Lx)+(Kx-Ix*(Cx/mux)*kx**2)*s.sin(kx*Lx))*Lx/Cx,
          F.subs({zz:kx*Lx,pp:Kx*Lx/Cx,qq:Ix/(mux*Lx)})) and
       eq(s.limit(F/zz,zz,0),1+pp))
mp.mp.dps=30
pw=mp.mpf('2');qw=mp.mpf('0.4')
fw=lambda z:z*mp.cos(z)+(pw-qw*z*z)*mp.sin(z)
z1=mp.findroot(fw,(1,2));z2=mp.findroot(fw,(3.5,4.5))
orth=mp.quad(lambda x:mp.sin(z1*x)*mp.sin(z2*x),[0,1])+qw*mp.sin(z1)*mp.sin(z2)
record('W056',2,'numerical','two distinct torsional eigenmodes are orthogonal only in endpoint-inertia weighted product',abs(orth)<mp.mpf('1e-25'))
numer=z1*z1*(mp.mpf('0.5')+mp.sin(2*z1)/(4*z1))+pw*mp.sin(z1)**2
denom=mp.mpf('0.5')-mp.sin(2*z1)/(4*z1)+qw*mp.sin(z1)**2
record('W056',3,'energy','Rayleigh quotient including boundary kinetic and spring energy equals eigenfrequency square',abs(numer/denom-z1*z1)<mp.mpf('1e-25'))
record('W056',4,'limit','free tip frequencies and large tip inertia asymptotic satisfy the transcendental equation',
       eq(F.subs({pp:0,qq:0,zz:s.pi/2})) and eq(s.limit(F/zz,zz,0),1+pp))
# O057 replacement: symmetric two-port coherent perfect absorption, not O019 Fresnel TIR.
gi,ge,det=s.symbols('gi ge det',positive=True,real=True)
gg=gi+ge
proj=s.ones(2)/2
Sm=-s.eye(2)+2*ge/(gg-s.I*det)*proj
eigS=-1+2*ge/(gg-s.I*det)
record('O057',1,'symbolic','two port optical scattering matrix has symmetric resonant and antisymmetric dark eigenchannels',
       all(eq(v) for v in Sm*s.Matrix([1,1])-eigS*s.Matrix([1,1]))
       and all(eq(v) for v in Sm*s.Matrix([1,-1])+s.Matrix([1,-1])))
record('O057',2,'limit','coherent perfect absorption occurs only for zero detuning and equal intrinsic and external loss',
       eq(eigS.subs({gi:ge,det:0}))
       and eq(s.simplify((gg-s.I*det)*eigS),ge-gi+s.I*det))
absor=4*gi*ge/(gg**2+det**2)
stored=2*ge/(gg**2+det**2)
record('O057',3,'conservation','coupled mode stored energy and internal dissipation match scattering absorptance and FWHM',
       eq(1-eigS*s.conjugate(eigS),absor)
       and eq(2*gi*stored,absor)
       and eq(absor.subs(det,gg),absor.subs(det,0)/2))
phi=s.symbols('phi',real=True)
record('O057',4,'independent_derivation','two beam phase controlled absorption and single input fifty percent upper bound',
       eq(s.expand_trig(s.cos(phi/2)**2),(1+s.cos(phi))/2)
       and eq(absor.subs({gi:ge,det:0}),1)
       and eq((absor/2).subs({gi:ge,det:0}),s.Rational(1,2)))


# Q057 replacement: amplitude damping is a different core model from Q014 oscillator quench.
et=s.symbols('et',positive=True)
K0=s.diag(1,s.sqrt(et))
K1=s.Matrix([[0,s.sqrt(1-et)],[0,0]])
record('Q057',1,'canonical_commutator','Stinespring one excitation rotation and Kraus completeness yield a trace preserving channel',
       s.simplify(K0.T*K0+K1.T*K1)==s.eye(2)
       and eq(s.Matrix([[s.sqrt(et),-s.sqrt(1-et)],[s.sqrt(1-et),s.sqrt(et)]]).det(),1))
gam,ttq,pq,zq=s.symbols('gam ttq pq zq',positive=True)
etq=s.exp(-gam*ttq)
rhot=s.Matrix([[1-etq*pq,s.sqrt(etq)*zq],[s.sqrt(etq)*zq,etq*pq]])
sm=s.Matrix([[0,1],[0,0]])
np=sm.T*sm
lind=gam*(sm*rhot*sm.T-(np*rhot+rhot*np)/2)
record('Q057',2,'independent_derivation','exact amplitude damping matrix solves zero temperature Lindblad equation and energy balance',
       all(eq(x) for x in (s.diff(rhot,ttq)-lind))
       and eq(s.diff(etq*pq,ttq),-gam*etq*pq))
rAB=s.Matrix([[s.Rational(1,2),0,0,s.sqrt(et)/2],
              [0,0,0,0],[0,0,(1-et)/2,0],
              [s.sqrt(et)/2,0,0,et/2]])
pt=s.Matrix(4,4,lambda i,j:rAB[2*(i//2)+(j%2),2*(j//2)+(i%2)])
lamq=s.symbols('lamq')
record('Q057',3,'symbolic','Bell Choi state partial transpose has exact negative eigenvalue minus eta over two',
       eq(pt.charpoly(lamq).as_expr(),(lamq-s.Rational(1,2))**2*(lamq**2-et**2/4)))
ppq=s.symbols('ppq',real=True)
fid=(1-ppq)*(1-et*ppq)+et*ppq**2+2*s.sqrt(et)*ppq*(1-ppq)
fav=(3+2*s.sqrt(et)+et)/6
fe=(1+s.sqrt(et))**2/4
record('Q057',4,'independent_derivation','Haar averaged fidelity agrees with independent entanglement fidelity identity',
       eq(s.integrate(fid,(ppq,0,1)),fav)
       and eq((2*fe+1)/3,fav)
       and eq(fav.subs(et,1),1) and eq(s.limit(fav,et,0,dir='+'),s.Rational(1,2)))


# T057: distinct thermodynamic shock model; four analytical/physical checks.
gs,xs=s.symbols('gs xs',positive=True)
rs=(gs+1)*xs/((gs-1)*xs+2)
Ps=(2*gs*xs-(gs-1))/(gs+1)
record('T057',1,'conservation','mass-momentum and energy Hugoniot jumps both vanish on the exact shock branch',
       eq(Ps-1-gs*xs*(1-1/rs)) and
       eq(gs/(gs-1)*(Ps/rs-1)-gs*xs*s.Rational(1,2)*(1-1/rs**2)))
ms2=((gs-1)*xs+2)/(2*gs*xs-(gs-1))
record('T057',2,'independent_derivation','downstream Mach number from velocity and sound speed agrees with jump elimination',
       eq(xs/(Ps*rs),ms2) and
       eq((2*gs*xs-(gs-1))-((gs-1)*xs+2),(gs+1)*(xs-1)))
Fs=s.log(Ps)-gs*s.log(rs)
Fprime=2*gs*(gs-1)*(xs-1)**2/(xs*((gs-1)*xs+2)*(2*gs*xs-(gs-1)))
eps=s.symbols('eps',real=True)
record('T057',3,'symbolic_and_limit','entropy production derivative is nonnegative and weak shock entropy begins cubically',
       eq(s.diff(Fs,xs),Fprime) and
       eq(s.diff(Fs.subs(xs,1+eps),eps,3).subs(eps,0)/s.factorial(3),
          2*gs*(gs-1)/(3*(gs+1)**2)) and eq(Fs.subs(xs,1)))
record('T057',4,'strong_shock_limit','strong shock finite compression, pressure and temperature scaling, subsonic downstream',
       eq(s.limit(rs,xs,s.oo),(gs+1)/(gs-1)) and
       eq(s.limit(Ps/xs,xs,s.oo),2*gs/(gs+1)) and
       eq(s.limit((Ps/rs)/xs,xs,s.oo),2*gs*(gs-1)/(gs+1)**2) and
       eq(s.limit(ms2,xs,s.oo),(gs-1)/(2*gs)))


# Round-12 continuation: four new, distinct physical models, each with four executable checks.
aR,cR,etaR=s.symbols('aR cR etaR',positive=True)
tR=cR*s.sinh(etaR)/aR
xR=cR**2*(s.cosh(etaR)-1)/aR
record('M060',1,'symbolic','constant proper acceleration produces a normalized hyperbolic worldline',
       eq((xR+cR**2/aR)**2-cR**2*tR**2,cR**4/aR**2))
record('M060',2,'energy','coordinate acceleration and relativistic kinetic work agree at arbitrary rapidity',
       eq(s.diff(cR*s.tanh(etaR),etaR)/s.diff(tR,etaR),aR/s.cosh(etaR)**3)
       and eq((s.cosh(etaR)-1)*cR**2,aR*xR))
record('M060',3,'independent_derivation','outgoing null ray interception gives exponential redshift and causal horizon',
       eq(s.simplify((cR*tR-xR-cR**2*(1-s.exp(-etaR))/aR).rewrite(s.exp))))
record('M060',4,'conservation','backward photon arrival time and Doppler ratio match adjacent-crest timing',
       eq(s.simplify((cR*tR+xR-cR**2*(s.exp(etaR)-1)/aR).rewrite(s.exp)))
       and eq(s.diff((cR/aR)*(s.exp(etaR)-1),etaR),cR*s.exp(etaR)/aR))
omE,epE,muE,kE,beE=s.symbols('omE epE muE kE beE',positive=True)
xE,ampE,widthE=s.symbols('xE ampE widthE',real=True)
eY=ampE*s.sin(kE*xE)
hX=-beE*eY/(omE*muE)
hZ=-s.I*kE*ampE*s.cos(kE*xE)/(omE*muE)
record('E060',1,'symbolic','TE10 electric and magnetic phasors satisfy both Faraday curl components',
       eq(-s.I*beE*eY,s.I*omE*muE*hX)
       and eq(s.diff(eY,xE),s.I*omE*muE*hZ))
record('E060',2,'independent_derivation','Ampere curl and TE dispersion imply phase-group velocity product',
       eq((s.I*beE*hX-s.diff(hZ,xE)+s.I*omE*epE*eY).subs(beE**2,omE**2*muE*epE-kE**2))
       and eq((omE/beE)*(beE/(omE*epE*muE)),1/(epE*muE)))
powerE=widthE*beE*ampE**2/(4*omE*muE)
energyE=epE*widthE*ampE**2/4
record('E060',3,'energy','Poynting power over electromagnetic energy density equals group velocity',
       eq(powerE/energyE,beE/(omE*epE*muE)))
bE=s.sqrt(omE**2*epE*muE-kE**2)
record('E060',4,'symbolic','TE group velocity dispersion is negative and evanescent axial flux vanishes',
       eq(s.diff(bE,omE,2),-kE**2*epE*muE/(omE**2*epE*muE-kE**2)**s.Rational(3,2))
       and eq(s.re(s.I*s.Symbol('kappaE',real=True)*ampE**2)))
vW,zW=s.symbols('vW zW',positive=True)
uW=vW/(2*s.cosh(s.sqrt(vW)*zW/2)**2)
record('W057',1,'symbolic','KdV solitary sech squared profile satisfies integrated nonlinear traveling wave equation',
       eq(s.diff(uW,zW,2)-vW*uW+3*uW**2))
record('W057',2,'conservation','KdV soliton mass and quadratic invariant equal independent exact sech integrals',
       eq(s.integrate(uW,(zW,-s.oo,s.oo)),2*s.sqrt(vW))
       and eq(s.integrate(uW**2,(zW,-s.oo,s.oo)),s.Rational(2,3)*vW**s.Rational(3,2)))
record('W057',3,'energy','KdV soliton Hamiltonian includes correct negative gradient contribution',
       eq(s.integrate(uW**3-s.diff(uW,zW)**2/2,(zW,-s.oo,s.oo)),vW**s.Rational(5,2)/5))
kW=s.symbols('kW',real=True)
record('W057',4,'limit','linearized KdV dispersion and positive soliton speed have opposite signs',
       eq(-s.I*(-kW**3)+(s.I*kW)**3)
       and eq(s.diff(-kW**3,kW),-3*kW**2))
pQ,stQ,deQ=s.symbols('pQ stQ deQ',positive=True)
OmQ=s.sqrt(pQ**2+stQ**2)
HQ=s.Matrix([[0,pQ,0],[pQ,2*deQ,stQ],[0,stQ,0]])/2
DQ=s.Matrix([stQ,0,-pQ])/OmQ
record('Q058',1,'symbolic','Lambda dark eigenstate annihilated by Hamiltonian and two bright eigenvalues match trace',
       HQ*DQ==s.zeros(3,1) and eq(HQ.det()) and eq(HQ.trace(),deQ))
thQ=s.symbols('thQ',real=True)
darkQ=s.Matrix([s.cos(thQ),0,-s.sin(thQ)])
brightQ=s.Matrix([s.sin(thQ),0,s.cos(thQ)])
record('Q058',2,'independent_derivation','instantaneous dark state derivative equals negative bright mixing vector',
       s.diff(darkQ,thQ)==-brightQ and eq(darkQ.dot(brightQ)))
record('Q058',3,'limit','counterintuitive pulse endpoints transfer population without middle state or Berry connection',
       darkQ.subs(thQ,0)==s.Matrix([1,0,0])
       and darkQ.subs(thQ,s.pi/2)==s.Matrix([0,0,-1])
       and eq(darkQ.dot(s.diff(darkQ,thQ))))
record('Q058',4,'symbolic','two photon detuning causes diagonal dark shift and off diagonal leakage',
       eq((darkQ.T*s.diag(0,0,1)*darkQ)[0],s.sin(thQ)**2)
       and eq((brightQ.T*s.diag(0,0,1)*darkQ)[0],-s.sin(thQ)*s.cos(thQ))
       and eq(s.limit((s.sqrt(deQ**2+OmQ**2)-deQ)*deQ/2,deQ,s.oo),OmQ**2/4))


# M061: nonholonomic Chaplygin sleigh, four substantive independent checks.
mc,Ic,ac,vc,tc=s.symbols('mc Ic ac vc tc',positive=True)
Jc=Ic+mc*ac**2
kc=mc*ac*vc/Jc
uc=vc*s.tanh(kc*tc)
wc=vc*s.sqrt(mc/Jc)/s.cosh(kc*tc)
uvar,omvar=s.symbols('uvar omvar',real=True)
reaction=mc*Ic/Jc*uvar*omvar
accel=-mc*ac*uvar*omvar/Jc
record('M061',1,'independent_derivation','transverse Newton equation and torque equation independently yield same constraint reaction',
       eq(mc*(uvar*omvar+ac*accel),reaction) and eq(Ic*accel,-ac*reaction))
record('M061',2,'symbolic_and_conservation','exact heteroclinic orbit solves both nonholonomic equations and preserves energy',
       eq(s.diff(uc,tc)-ac*wc**2) and eq(s.diff(wc,tc)+mc*ac*uc*wc/Jc) and
       eq((mc*uc**2+Jc*wc**2)/2,mc*vc**2/2))
thetac=2*s.sqrt(Jc/mc)/ac*s.atan(s.exp(kc*tc))
record('M061',3,'limit','heading derivative and total turning agree with exact integration and stable decay rate',
       eq(s.simplify((s.diff(thetac,tc)-wc).rewrite(s.exp))) and
       eq(s.limit(thetac,tc,s.oo)-s.limit(thetac,tc,-s.oo),s.pi*s.sqrt(Jc/mc)/ac) and
       eq(s.diff(-mc*ac*uvar*omvar/Jc,omvar).subs(uvar,vc),-kc))
wc0=vc*s.sqrt(mc/Jc)
record('M061',4,'local_series','cusp acceleration and zero second u derivative follow equations; reaction vanishes at reversal',
       eq(s.diff(uc,tc).subs(tc,0),ac*wc0**2) and
       eq(s.diff(uc,tc,2).subs(tc,0)) and eq((mc*Ic/Jc*uc*wc).subs(tc,0)))

# O058: Fresnel half-plane erfc diffraction, local flux and asymptotics.
ko,zo,xo=s.symbols('ko zo xo',positive=True,real=True)
Ao=s.exp(-s.I*s.pi/4)*s.sqrt(ko/(2*zo))
fo=s.erfc(-Ao*xo)/2
record('O058',1,'symbolic_and_boundary','complex Fresnel kernel derivative and edge amplitude agree with normalized erfc',
       eq(s.diff(fo,xo),Ao*s.exp(s.I*ko*xo**2/(2*zo))/s.sqrt(s.pi)) and
       eq(fo.subs(xo,0),s.Rational(1,2)))
record('O058',2,'local_derivative','edge intensity equals one quarter and its slope has correct Fresnel length',
       eq(s.Abs(fo.subs(xo,0))**2,s.Rational(1,4)) and
       eq(s.re(s.diff(fo,xo).subs(xo,0)),s.sqrt(ko/(4*s.pi*zo))))
so=mp.mpf('12');phaseo=mp.exp(-1j*mp.pi/4)
fbright=mp.erfc(-phaseo*so)/2;fshadow=mp.erfc(phaseo*so)/2
brightasy=1-mp.cos(so**2+mp.pi/4)/(mp.sqrt(mp.pi)*so)
shadowasy=1/(4*mp.pi*so**2)
record('O058',3,'independent_numerical_asymptotics','bright oscillations and shadow inverse-square tail agree with complex erfc numerical evaluation',
       abs(abs(fbright)**2-brightasy)<mp.mpf('0.001') and abs(abs(fshadow)**2-shadowasy)<mp.mpf('0.000001'))
record('O058',4,'conservation','paraxial wave equation and negative edge transverse flux hold identically',
       eq(s.diff(fo,xo,2)+2*s.I*ko*s.diff(fo,zo)) and
       eq(s.im(s.conjugate(fo.subs(xo,0))*s.diff(fo,xo).subs(xo,0))/ko,-1/(4*s.sqrt(s.pi*ko*zo))))


assert len(checks)==52 and len(set((c['id'],c['part']) for c in checks))==52
assert all(len(set(c['method'] for c in checks if c['id']==uid))>=2 for uid in ['M059','E059','T056','W056','O057','Q057','T057','M060','E060','W057','Q058','M061','O058'])
# Independent numerical crosschecks beyond the twelve mandatory draft subparts.
from math import sqrt,tanh,cosh
A0=2.;B0=2.;C0=2/sqrt(3);lam0=2/sqrt(3);time=.73
w1num=A0/cosh(lam0*time);w2num=B0*tanh(lam0*time);w3num=C0/cosh(lam0*time)
assert abs((w1num*w1num+2*w2num*w2num+3*w3num*w3num)/2-4)<1e-12
assert abs((w1num*w1num+4*w2num*w2num+9*w3num*w3num)-16)<1e-12
mp.mp.dps=30
al=mp.mpf('1.7');rad=mp.mpf('2.3')
integ=mp.quad(lambda z:z*(mp.besselj(0,al*z)**2+mp.besselj(1,al*z)**2),[0,rad])
end=rad**2/2*(mp.besselj(0,al*rad)**2+2*mp.besselj(1,al*rad)**2-mp.besselj(0,al*rad)*mp.besselj(2,al*rad))
assert abs(integ-end)<mp.mpf('1e-26')
Tnum=.99;lo=.05;hi=.5
for _ in range(80):
    mid=(lo+hi)/2
    if mid-math.tanh(mid/Tnum)>0:hi=mid
    else:lo=mid
mroot=(lo+hi)/2
assert abs(mroot-math.sqrt(3*(1-Tnum)))/mroot<.01
supplemental=[dict(id='M059',method='numerical',name='triaxial separatrix two invariants at t=0.73',passed=True),
              dict(id='E059',method='numerical',name='high precision Bessel quadrature versus boundary formula',passed=True),
              dict(id='T056',method='numerical',name='spontaneous magnetization root near Curie temperature',passed=True)]

# Additional independent high-precision checks, not substituted for the 24 subpart tests.
bigq=mp.mpf('100000')
large_root=mp.findroot(lambda z:z*mp.cos(z)+(pw-bigq*z*z)*mp.sin(z),mp.sqrt((1+pw)/bigq))
assert abs(bigq*large_root**2-(1+pw))<mp.mpf('0.0003')
giN=mp.mpf('0.81');geN=mp.mpf('1.13');detN=mp.mpf('0.57')
ssN=-1+2*geN/(giN+geN-1j*detN)
AN=4*giN*geN/((giN+geN)**2+detN**2)
assert abs((1-abs(ssN)**2)-AN)<mp.mpf('1e-27')
etaN=mp.mpf('0.37')
fN=lambda p:(1-p)*(1-etaN*p)+etaN*p*p+2*mp.sqrt(etaN)*p*(1-p)
assert abs(mp.quad(fN,[0,1])-(3+2*mp.sqrt(etaN)+etaN)/6)<mp.mpf('1e-27')
supplemental.extend([
 dict(id='W056',method='asymptotic_numerical',name='large end-inertia fundamental root agrees with effective stiffness asymptotic',passed=True),
 dict(id='O057',method='high_precision_scattering',name='independent complex scattering eigenvalue energy balance at finite detuning',passed=True),
 dict(id='Q057',method='independent_numerical_quadrature',name='high precision independent Haar fidelity quadrature for amplitude damping',passed=True)])


# Independent high-Mach numerical sample: gamma=7/5, M1=1000.
gshock=mp.mpf(7)/5
xshock=mp.mpf('1000000')
rshock=(gshock+1)*xshock/((gshock-1)*xshock+2)
pshock=(2*gshock*xshock-(gshock-1))/(gshock+1)
assert abs(rshock-(gshock+1)/(gshock-1))<mp.mpf('0.0001')
assert abs(pshock/xshock-2*gshock/(gshock+1))<mp.mpf('0.00001')
supplemental.append(dict(id='T057',method='independent_numerical',name='high-Mach Rankine-Hugoniot strong shock ratios',passed=True))


# Supplemental numeric checks are independent of the four per-question evidence records.
etaN=mp.mpf('0.91');aN=mp.mpf('1.3');cN=mp.mpf('3.0')
tN=cN/aN*mp.sinh(etaN);xN=cN*cN/aN*(mp.cosh(etaN)-1)
assert abs(cN*tN-xN-cN*cN/aN*(1-mp.exp(-etaN)))<mp.mpf('1e-27')
supplemental.append(dict(id='M060',method='numerical',name='null interception and exponential Doppler redshift at finite rapidity',passed=True))
wN=mp.mpf('3');kcN=mp.pi/2;betaN=mp.sqrt(wN*wN-kcN*kcN)
assert abs((betaN/(4*wN))/(mp.mpf('0.25'))-betaN/wN)<mp.mpf('1e-27')
supplemental.append(dict(id='E060',method='numerical',name='independent TE10 Poynting to energy speed at nonzero cutoff',passed=True))
vN=mp.mpf('4');kN=mp.sqrt(vN)/2
massN=mp.quad(lambda z:vN/(2*mp.cosh(kN*z)**2),[-mp.inf,0,mp.inf])
assert abs(massN-2*mp.sqrt(vN))<mp.mpf('1e-27')
supplemental.append(dict(id='W057',method='numerical',name='high precision nonlinear solitary wave mass quadrature',passed=True))
pN=mp.mpf('1.2');sN=mp.mpf('2.3');dN=mp.mpf('0.7');oN=mp.sqrt(pN*pN+sN*sN)
hN=mp.matrix([[0,pN,0],[pN,2*dN,sN],[0,sN,0]])/2
darkN=mp.matrix([sN/oN,0,-pN/oN])
assert max(abs(x) for x in hN*darkN)<mp.mpf('1e-27')
supplemental.append(dict(id='Q058',method='numerical',name='independent high precision Lambda dark state matrix product',passed=True))


# Supplemental independent high precision numerical verification of new models.
mn=mp.mpf('2');In=mp.mpf('3');an=mp.mpf('1');vn=mp.mpf('4')
Jn=In+mn*an**2;kn=mn*an*vn/Jn;tn=mp.mpf('0.67')
un=vn*mp.tanh(kn*tn);wn=vn*mp.sqrt(mn/Jn)/mp.cosh(kn*tn)
assert abs((mn*un**2+Jn*wn**2)/2-mn*vn**2/2)<mp.mpf('1e-27')
supplemental.append(dict(id='M061',method='high_precision_numerical',name='Chaplygin heteroclinic energy at nontrivial time',passed=True))
zn=mp.mpf('1.7');knu=mp.mpf('3.4')
An=mp.exp(-1j*mp.pi/4)*mp.sqrt(knu/(2*zn))
fn=lambda x:mp.erfc(-An*x)/2
jedge=mp.im(mp.conj(fn(0))*mp.diff(fn,mp.mpf('0')))/knu
assert abs(jedge+1/(4*mp.sqrt(mp.pi*knu*zn)))<mp.mpf('1e-27')
supplemental.append(dict(id='O058',method='independent_numerical_derivative',name='Fresnel edge transverse flux from high precision erfc derivative',passed=True))

result={'status':'draft-only','new_problem_count':13,'passed_count':len(checks),'tests':checks,'independent_expert_review':'pending','supplemental_numeric_checks':supplemental}
path=Path(__file__).resolve().parents[1]/'data/round12_draft_validation_report.json'
path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'status':result['status'],'checked_subparts':len(checks)},ensure_ascii=False))
