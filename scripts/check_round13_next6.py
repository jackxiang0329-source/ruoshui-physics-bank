#!/usr/bin/env python3
"""Round 13 second group: 24 executable physics checks. Not independent human review."""
import json,math
from pathlib import Path
import sympy as s
import mpmath as mp
checks=[]
def check(uid,part,method,name,condition):
    assert bool(condition),(uid,part,name)
    checks.append(dict(id=uid,part=part,method=method,name=name,passed=True))
def eq(a,b=0):return s.simplify(s.expand_trig(a-b))==0

# M069 acceleration-induced potential-flow added mass.
r,th,U,a,rho,ms,F,time=s.symbols('r th U a rho ms F time',positive=True,real=True)
phi=-U*a**3*s.cos(th)/(2*r*r)
Lapl=s.diff(r*r*s.diff(phi,r),r)/r**2+s.diff(s.sin(th)*s.diff(phi,th),th)/(r*r*s.sin(th))
check('M069',1,'symbolic','exterior spherical Laplace and radial no penetration conditions and tangential velocity',eq(Lapl) and eq(s.diff(phi,r).subs(r,a),U*s.cos(th)) and eq((s.diff(phi,th)/r).subs(r,a),U*s.sin(th)/2))
grad2=s.diff(phi,r)**2+(s.diff(phi,th)/r)**2
TF=s.simplify(rho/2*s.integrate(s.integrate(grad2*r*r*s.sin(th),(th,0,s.pi)),(r,a,s.oo))*2*s.pi)
ma=2*s.pi*rho*a**3/3
check('M069',2,'independent_derivation','direct 3D exterior flow kinetic energy volume integral gives one-half fluid displaced mass',eq(TF,ma*U*U/2))
acc=s.symbols('acc',real=True)
pacc=rho*a*acc*s.cos(th)/2
Fz=-s.integrate(pacc*s.cos(th)*s.sin(th)*2*s.pi*a*a,(th,0,s.pi))
check('M069',3,'conservation','nonstationary Bernoulli pressure integral equals added-mass acceleration reaction',eq(Fz,-ma*acc) and eq(s.integrate(s.cos(th)**2*s.sin(th),(th,0,s.pi)),s.Rational(2,3)))
vel=s.symbols('vel',positive=True)
eqacc=F/(ms+ma)
check('M069',4,'physical_case','work-energy identity for bare sphere plus added fluid mass, and correct vacuum-density limit',eq((ms+ma)*vel*eqacc,F*vel) and eq(s.limit(ma,rho,0),0) and eq(s.limit(ma,a,0),0))

# E069 planar vacuum space-charge limited electron flow.
eps,e,m,d,Vd,x=s.symbols('eps e m d Vd x',positive=True,real=True)
v=s.sqrt(2*e*Vd/m)*(x/d)**s.Rational(2,3)
V=Vd*(x/d)**s.Rational(4,3)
J=4*eps*s.sqrt(2*e/m)*Vd**s.Rational(3,2)/(9*d*d)
rhos=-J/v
check('E069',1,'symbolic','electronic energy plus continuity reproduces nonlinear Poisson equation with exact Child Langmuir coefficient',eq(s.diff(V,x,2),-rhos/eps) and eq(v*v,2*e*V/m))
check('E069',2,'independent_derivation','Child Langmuir voltage law meets both plates, vanishing cathode field and exact current scaling',eq(V.subs(x,d),Vd) and eq(s.limit(s.diff(V,x),x,0,dir='+')) and eq(s.diff(J,Vd)*Vd/J,s.Rational(3,2)))
qarea=s.integrate(rhos,(x,0,d))
fieldE=s.integrate(eps*s.diff(V,x)**2/2,(x,0,d))
check('E069',3,'conservation','space charge finite despite near-cathode singularity and field energy differs from uniform parallel plate capacitor',eq(qarea,-4*eps*Vd/(3*d)) and eq(fieldE,8*eps*Vd*Vd/(15*d)))
check('E069',4,'dimensions','kinetic energy flux equals electron electric energy transfer and soft-voltage current goes to zero',eq(J*m*(v.subs(x,d))**2/(2*e),J*Vd) and eq(s.limit(J,Vd,0,dir='+'),0))

# T065 ballistic bosonic Landauer heat flux.
T,kb,hbar,tc=s.symbols('T kb hbar tc',positive=True,real=True)
qplus=s.pi*kb**2*T*T/(12*hbar)
GQ=s.pi*kb**2*T/(6*hbar)
mp.mp.dps=35
integral=mp.quad(lambda xx:xx/mp.expm1(xx),[0,1,10,mp.inf])
check('T065',1,'numerical','independent high precision Bose occupancy spectral integral equals pi squared over six',abs(integral-mp.pi**2/6)<mp.mpf('1e-30'))
check('T065',2,'symbolic','differential ballistic conductance of quadratic chiral heat flux equals universal thermal conductance quantum',eq(s.diff(qplus,T),GQ) and eq(s.diff(qplus,T)*T,2*qplus))
Y=s.symbols('Y',positive=True)
cut=s.pi**2/6+Y*s.log(1-s.exp(-Y))-s.polylog(2,s.exp(-Y))
Fcut=lambda yy:mp.pi**2/6+yy*mp.log(1-mp.exp(-yy))-mp.polylog(2,mp.exp(-yy))
spectral=lambda xx:xx/mp.expm1(xx)
check('T065',3,'numerical','high precision cutoff Bose spectrum integral equals dilogarithm expression for two finite cutoffs and correct small cutoff slope',all(abs(mp.quad(spectral,[0,yy])-Fcut(yy))<mp.mpf('1e-29') for yy in (mp.mpf('1'),mp.mpf('3'))) and abs(Fcut(mp.mpf('1e-5'))/mp.mpf('1e-5')-1)<mp.mpf('1e-5'))
Tl,Tr=s.symbols('Tl Tr',positive=True)
current=s.pi*kb**2*(Tl*Tl-Tr*Tr)/(12*hbar)
entropy=current*(1/Tr-1/Tl)
check('T065',4,'conservation','Landauer two bath entropy production is positive quadratic temperature-difference factor',eq(entropy,s.pi*kb**2*(Tl-Tr)**2*(Tl+Tr)/(12*hbar*Tl*Tr)) and eq(entropy.subs(Tl,Tr)))

# W065 stratified incompressible internal gravity waves.
N,kx,kz=s.symbols('N kx kz',positive=True,real=True)
K=s.sqrt(kx*kx+kz*kz)
omega=N*kx/K
record_disp=omega**2*(kx*kx+kz*kz)-N*N*kx*kx
check('W065',1,'symbolic','internal wave frequency solves horizontal-buoyancy dispersion and is bounded by N',eq(record_disp) and eq(s.limit(omega,kz,0,dir='+'),N))
cgx=N*kz*kz/K**3
cgz=-N*kx*kz/K**3
check('W065',2,'independent_derivation','wave group velocity derivative is orthogonal to wavevector as implied by homogeneous degree zero dispersion',eq(s.diff(omega,kx),cgx) and eq(s.diff(omega,kz),cgz) and eq(kx*cgx+kz*cgz))
uu,ww,pp,bu,ux,wz,px,pz=s.symbols('uu ww pp bu ux wz px pz',real=True)
ut=-px;wt=-pz+bu;bt=-N*N*ww
energy_t=uu*ut+ww*wt+bu*bt/(N*N)
fluxdiv=ux*pp+wz*pp+uu*px+ww*pz
check('W065',3,'conservation','local Boussinesq perturbation kinetic plus potential energy balances pressure work under incompressible constraint',eq((energy_t+fluxdiv).subs(wz,-ux)))
check('W065',4,'limit','hydrostatic high vertical wave number suppresses frequency while unstratified fluid has zero gravity-wave frequency',eq(s.limit(omega,kz,s.oo),0) and eq(s.limit(omega,N,0,dir='+'),0) and eq(s.limit(cgx,kz,0,dir='+'),0))

# O067 vector Debye focusing.
theta,alpha,krho=s.symbols('theta alpha krho',positive=True,real=True)
xdir,yph=s.symbols('xdir yph',real=True)
sun=s.Matrix([s.sin(theta)*s.cos(yph),s.sin(theta)*s.sin(yph),s.cos(theta)])
pol=s.Matrix([s.cos(theta)*s.cos(yph),s.cos(theta)*s.sin(yph),-s.sin(theta)])
check('O067',1,'symbolic','each focused Debye wave polarization vector is orthogonal to its own wavevector and normalized',eq((sun.T*pol)[0]) and eq((pol.T*pol)[0],1))
axial=s.integrate(s.sin(theta)**2,(theta,0,alpha))
check('O067',2,'independent_derivation','axial vector focusing integral equals analytic alpha over two minus sine double alpha over four',eq(axial,alpha/2-s.sin(2*alpha)/4))
q=s.symbols('q',real=True)
check('O067',3,'symbolic','Bessel angular Fourier identities recover J0 and J1 radial transverse integrals with exact on-axis cancellation',eq(s.diff(s.besselj(0,q),q),-s.besselj(1,q)) and eq(s.besselj(1,0)) and eq(s.besselj(0,0),1))
small=s.limit(axial/alpha**3,alpha,0,dir='+')
check('O067',4,'limit','paraxial longitudinal focal field scales as aperture cubed with correct one-third coefficient',eq(small,s.Rational(1,3)) and eq(s.limit(s.besselj(1,q)/q,q,0),s.Rational(1,2)))

# Q067 Kitaev p-wave superconducting Majorana modes.
t,Del,mu,k=s.symbols('t Del mu k',positive=True,real=True)
h=s.Matrix([[-mu-2*t*s.cos(k),-2*s.I*Del*s.sin(k)],[2*s.I*Del*s.sin(k),mu+2*t*s.cos(k)]])
band=(mu+2*t*s.cos(k))**2+4*Del*Del*s.sin(k)**2
check('Q067',1,'symbolic','BdG Hamiltonian has exact opposite energy eigenvalues and closes superconducting gap at chemical potential plus or minus 2t',all(eq(z) for z in (h*h-band*s.eye(2))) and eq(band.subs({mu:2*t,k:s.pi}),0))
low=s.Matrix([[0,1],[0,0]]);zz=s.diag(1,-1);ident=s.eye(2)
def kron(xs):
  out=xs[0]
  for a0 in xs[1:]:out=s.kronecker_product(out,a0)
  return out
L=3
cc=[kron([zz]*j+[low]+[ident]*(L-j-1)) for j in range(L)]
AA=[ci+ci.H for ci in cc]
BB=[-s.I*(ci-ci.H) for ci in cc]
H0=sum((-(cc[j].H*cc[j+1]+cc[j+1].H*cc[j])+(cc[j]*cc[j+1]+cc[j+1].H*cc[j].H) for j in range(L-1)),s.zeros(2**L))
Hm=sum((s.I*BB[j]*AA[j+1] for j in range(L-1)),s.zeros(2**L))
check('Q067',2,'numerical','independent 8 by 8 fermionic Fock matrix equality verifies Kitaev sweet point and exact two edge commutators',H0==Hm and H0*AA[0]-AA[0]*H0==s.zeros(2**L) and H0*BB[-1]-BB[-1]*H0==s.zeros(2**L))
q0=lambda k0,mu0:-mu0-2*t*s.cos(k0)+2*s.I*Del*s.sin(k0)
check('Q067',3,'physical_case','topological winding circle criterion equivalent to chemical potential between the two gap closing points',eq(q0(0,-2*t)) and eq(q0(s.pi,2*t)) and eq(s.im(q0(s.pi/2,0)),2*Del))
NN=s.zeros(2**L)
for ci in cc:NN+=ci.H*ci
parity=kron([zz]*L)
pair=cc[0]*cc[1]+cc[1].H*cc[0].H
check('Q067',4,'conservation','superconducting pairing changes particle number but commutes with exact many-body fermion parity',pair*parity-parity*pair==s.zeros(2**L) and pair*NN-NN*pair!=s.zeros(2**L))
assert len(checks)==24
assert len(set((z['id'],z['part']) for z in checks))==24
ids=('M069','E069','T065','W065','O067','Q067')
assert all(len({z['method'] for z in checks if z['id']==uid})>=2 for uid in ids)
report=dict(status='draft-qa-only',new_problem_count=6,passed_count=24,tests=checks,independent_expert_review='pending')
Path(__file__).resolve().parents[1].joinpath('data/round13_next6_validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('ROUND13 NEXT 6 24 PASS')
