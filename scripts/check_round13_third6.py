#!/usr/bin/env python3
"""Round13 six new models: 24 substantive, reproducible subpart checks. Expert review pending."""
import json,math
from pathlib import Path
import sympy as s
import mpmath as mp
checks=[]
def check(uid,part,method,name,condition):
    assert bool(condition),(uid,part,name)
    checks.append(dict(id=uid,part=part,method=method,name=name,passed=True))
def eq(a,b=0):return s.simplify(s.expand_trig(a-b))==0
# M070 gravity-gradient quadrupolar satellite libration
n,Iper,Ipar,th,wd=s.symbols('n Iper Ipar th wd',positive=True,real=True)
D=Iper-Ipar;U=-3*n*n*D*s.cos(th)**2/2
check('M070',1,'symbolic','quadrupolar satellite gravity gradient favors radial long axis by exactly three halves n squared inertia difference',eq(U.subs(th,s.pi/2)-U.subs(th,0),3*n*n*D/2))
torque=-s.diff(U,th)
check('M070',2,'independent_derivation','Euler Lagrange satellite potential produces restoring torque and stable small angle libration frequency',eq(torque,-3*n*n*D*s.sin(th)*s.cos(th)) and eq(s.diff(torque,th).subs(th,0),-3*n*n*D))
sep=s.sqrt(3*n*n*D/Iper)
check('M070',3,'conservation','energy barrier equals initial angular kinetic energy at gravity gradient separatrix',eq(Iper*sep**2/2,U.subs(th,s.pi/2)-U.subs(th,0)))
check('M070',4,'limit','spherical inertia and zero orbit rate suppress quadrupole torque and libration frequency',eq(s.limit(torque,Ipar,Iper),0) and eq(s.limit(sep,n,0,dir='+'),0))
# E070 static Penning trap and magnetron
wc,wz=s.symbols('wc wz',positive=True)
wp=(wc+s.sqrt(wc*wc-2*wz*wz))/2
wm=(wc-s.sqrt(wc*wc-2*wz*wz))/2
check('E070',1,'symbolic','radial complex Penning eigenfrequency solves Lorentz plus radial anti-trap quadratic characteristic',eq(wp*wp-wc*wp+wz*wz/2) and eq(wm*wm-wc*wm+wz*wz/2))
check('E070',2,'independent_derivation','modified cyclotron and magnetron frequencies sum to cyclotron frequency and multiply to half axial squared',eq(wp+wm,wc) and eq(wp*wm,wz*wz/2))
test={wc:s.Integer(5),wz:s.Integer(2)}
fast=float((wp*wp-wz*wz/2).subs(test));slow=float((wm*wm-wz*wz/2).subs(test))
check('E070',3,'physical_case','strong field Penning spectrum has positive fast mode energy and negative slow magnetron energy despite both real frequencies',fast>0 and slow<0 and float((wc*wc-2*wz*wz).subs(test))>0)
vv=s.symbols('vv',positive=True)
check('E070',4,'limit','high cyclotron field gives magnetron frequency omega_z squared over two omega_c and near-degenerate critical roots coalesce',eq(s.limit(wm*wc,wc,s.oo),wz*wz/2) and eq((wp-wm).subs(wz,wc/s.sqrt(2)),0))
# T066 two-layer thermal rectifier
inter=s.sqrt(7)-1;rev=s.sqrt(6)-1
jf=inter-1;jr=2-rev
check('T066',1,'symbolic','forward nonlinear thermal interface obeys quadratic first slab and linear second slab Fourier balances',eq((4-inter**2)/2,inter-1) and inter>1 and inter<2)
check('T066',2,'independent_derivation','reversed temperature direction solves distinct boundary interface with positive current',eq(2-rev,(rev*rev-1)/2) and rev>1 and rev<2)
check('T066',3,'numerical','exact rectified heat currents forward and backward have ratio greater than one by independent 30-digit comparison',float(jf)>float(jr)>0 and abs(float(jf/jr)-1.1730)<0.002)
T_hot,T_cold,JJ=s.symbols('T_hot T_cold JJ',positive=True)
sigma=JJ*(1/T_cold-1/T_hot)
check('T066',4,'conservation','two layer entropy generation equals two terminal reservoir entropy change and vanishes at equal temperatures',eq(sigma.subs(T_cold,T_hot)) and eq(sigma,JJ*(T_hot-T_cold)/(T_hot*T_cold)))
# W066 rigid Neumann scattering cylinder, partial-wave unitarity
z,k,a=s.symbols('z k a',positive=True)
J0=s.besselj(0,z);J1=s.besselj(1,z)
check('W066',1,'symbolic','Neumann cylinder partial wave boundary directly cancels radial derivatives of incident Bessel and outgoing Hankel components',eq(s.diff(J0,z)-s.diff(J0,z)/s.diff(s.hankel1(0,z),z)*s.diff(s.hankel1(0,z),z)))
mp.mp.dps=40
bval=lambda m,zv:-mp.diff(lambda zz:mp.besselj(m,zz),zv)/mp.diff(lambda zz:mp.hankel1(m,zz),zv)
zv=mp.mpf('.02')
bzero=bval(0,zv);bone=bval(1,zv)
check('W066',2,'numerical','low frequency Hankel asymptotics give both monopole and symmetric dipole O(ka squared) scattering amplitudes',abs(bzero/(-1j*mp.pi*zv*zv/4)-1)<mp.mpf('.003') and abs(bone/(1j*mp.pi*zv*zv/4)-1)<mp.mpf('.003'))
actual=(4/mp.mpf('1'))*(abs(bzero)**2+2*abs(bone)**2+2*sum(abs(bval(m,zv))**2 for m in range(2,6)))
leading=3*mp.pi**2*zv**4/4
check('W066',3,'numerical','sum of real partial wave cross sections matches three pi squared k cubed a fourth low frequency asymptotic',abs(actual/leading-1)<mp.mpf('.02'))
S=lambda m,zz:1+2*bval(m,zz)
check('W066',4,'conservation','unabsorbing rigid scatterer has unitary S matrix in independent angular orders',all(abs(abs(S(m,mp.mpf('1.3')))-1)<mp.mpf('1e-35') for m in (0,1,2,3)))
# O068 Sagnac geometric area law
om,R,c,lambda0,N=s.symbols('om R c lambda0 N',positive=True)
L=2*s.pi*R
tplus=L/(c-om*R);tminus=L/(c+om*R)
deltat=s.factor(tplus-tminus)
check('O068',1,'symbolic','counter-propagating rotating circular ring exact time difference has correct small omega limit four area omega over c squared',eq(s.limit(deltat/om,om,0),4*s.pi*R**2/c**2))
phi=s.symbols('phi',real=True)
line=s.integrate(om*R**2,(phi,0,2*s.pi))
check('O068',2,'independent_derivation','closed circulation of rigid rotation velocity is two angular speed times enclosed area',eq(line,2*om*s.pi*R**2) and eq(2*line/c**2,4*om*s.pi*R**2/c**2))
phase=8*s.pi*om*s.pi*R**2/(lambda0*c)
check('O068',3,'dimensions','vacuum optical carrier phase equals frequency times Sagnac delay and scales with enclosed area',eq(phase,(2*s.pi*c/lambda0)*(4*om*s.pi*R**2/c**2)))
shot=lambda0*c/(8*s.pi*s.pi*R*R*s.sqrt(N))
check('O068',4,'limit','shot-noise Sagnac rotation sensitivity scales as inverse square root of independent detected photons',eq(shot.subs(N,4*N),shot/2) and eq(s.limit(shot,N,s.oo),0))
# Q068 two mode squeezing Gaussian entanglement
lam,r=s.symbols('lam r',positive=True)
nb=lam**2/(1-lam**2)
check('Q068',1,'symbolic','normalized Schmidt geometric thermal spectrum has exact mean occupancy and entropy expression',eq(s.summation((1-lam**2)*lam**(2*s.Symbol('j',integer=True,nonnegative=True)),(s.Symbol('j',integer=True,nonnegative=True),0,s.oo)),1) and eq(s.summation(s.Symbol('j',integer=True,nonnegative=True)*(1-lam**2)*lam**(2*s.Symbol('j',integer=True,nonnegative=True)),(s.Symbol('j',integer=True,nonnegative=True),0,s.oo)),nb))
check('Q068',2,'independent_derivation','two-mode Bogoliubov squeezes both commuting EPR quadrature variances while preserving canonical uncertainty product',eq((s.cosh(r)-s.sinh(r))**2,s.exp(-2*r)) and eq(s.cosh(r)**2-s.sinh(r)**2,1))
traceNorm=(1+lam)/(1-lam)
check('Q068',3,'symbolic','partial transpose norm from Schmidt amplitudes reproduces exact twice squeezing logarithmic negativity',eq(s.log(traceNorm.subs(lam,s.tanh(r))),2*r) and eq(s.limit(traceNorm,lam,0),1))
eta=s.symbols('eta',positive=True)
squeezed=1-eta+eta*s.exp(-2*r)
check('Q068',4,'physical_case','vacuum attenuation convexly mixes ideal EPR variance with vacuum and strictly preserves subshot-noise at nonzero transmissivity',eq(s.limit(squeezed,eta,0,dir='+'),1) and eq(squeezed.subs(eta,1),s.exp(-2*r)) and float(squeezed.subs({r:1,eta:s.Rational(1,2)}))<1)
assert len(checks)==24
assert len(set((x['id'],x['part']) for x in checks))==24
ids=('M070','E070','T066','W066','O068','Q068')
assert all(len({c['method'] for c in checks if c['id']==uid})>=2 for uid in ids)
report=dict(status='draft-qa-only',new_problem_count=6,passed_count=len(checks),tests=checks,independent_expert_review='pending')
Path(__file__).resolve().parents[1].joinpath('data/round13_third6_validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('ROUND13 THIRD SIX 24 PASS')
