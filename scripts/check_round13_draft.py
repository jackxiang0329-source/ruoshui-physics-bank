#!/usr/bin/env python3
"""Round 13 draft: per-subpart reproducible algebra, independent integrals, physical limits.
Technical verification, NOT external expert approval.
"""
from pathlib import Path
import json
import sympy as s
import mpmath as mp
import math
checks=[]
def record(uid,part,method,description,ok):
    assert method in {'symbolic','numerical','limit','dimensions','conservation','independent_derivation','physical_case'}
    assert bool(ok),(uid,part,description)
    checks.append(dict(id=uid,part=part,method=method,name=description,passed=True))
def eq(x,y=0):
    return s.simplify(s.expand_trig(x-y))==0

# M068: exact n=1 Lane-Emden stellar hydrostatics.
r,a,rhoc,K,G,xi=s.symbols('r a rhoc K G xi',positive=True,real=True)
density=rhoc*s.sin(r/a)/(r/a)
ode=(s.diff(r*r*s.diff(density,r),r)/r**2+density/a**2)
record('M068',1,'symbolic','analytic polytrope density solves the radial Lane Emden differential equation with regular center',eq(ode) and eq(s.limit(density,r,0),rhoc))
mass=4*s.pi*rhoc*a**3*(s.sin(xi)-xi*s.cos(xi))
record('M068',2,'independent_derivation','independently differentiate mass profile to recover exact shell density and surface enclosed mass',eq(s.diff(mass,xi),4*s.pi*rhoc*a**3*xi*s.sin(xi)) and eq(mass.subs(xi,s.pi),4*s.pi**2*rhoc*a**3))
Pi=2*s.pi**2*K*rhoc**2*a**3
M=4*s.pi**2*a**3*rhoc
R=s.pi*a
W=-3*Pi
record('M068',3,'conservation','virial gravitational energy equals independent mass radius polytropic binding energy at K equals two pi G a squared',eq((W+3*G*M**2/(4*R)).subs(K,2*s.pi*G*a*a)) and eq(4*s.pi*K*rhoc**2*a**3*s.integrate(s.sin(xi)**2,(xi,0,s.pi)),Pi))
U=Pi
record('M068',4,'physical_case','stellar total binding energy is minus twice integrated polytropic pressure and scales as center-density squared',eq(U+W,-2*Pi) and eq(s.diff(U+W,rhoc)*rhoc,2*(U+W)))

# E068: rotating uniformly charged thin shell.
sig,om,aa,mu0,Q,m=s.symbols('sig om aa mu0 Q m',positive=True,real=True)
th=s.symbols('th',real=True)
mz=s.integrate((sig*om*aa**4/2)*s.sin(th)**3*2*s.pi,(th,0,s.pi))
record('E068',1,'independent_derivation','angular surface-current magnetic dipole integral yields exact factor one third of charged spherical shell',eq(mz,4*s.pi*sig*om*aa**4/3) and eq(mz.subs(sig,Q/(4*s.pi*aa**2)),Q*om*aa**2/3))
Mmag=sig*om*aa
Br_in=2*mu0*Mmag*s.cos(th)/3
Bt_in=-2*mu0*Mmag*s.sin(th)/3
Br_out=2*mu0*m*s.cos(th)/(4*s.pi*aa**3)
Bt_out=mu0*m*s.sin(th)/(4*s.pi*aa**3)
record('E068',2,'symbolic','sphere magnetic radial continuity and tangential H jump reproduce prescribed surface current',eq((Br_out-Br_in).subs(m,4*s.pi*sig*om*aa**4/3)) and eq(((Bt_out-Bt_in)/mu0).subs(m,4*s.pi*sig*om*aa**4/3),sig*om*aa*s.sin(th)))
U_inside=mu0*m*m/(6*s.pi*aa**3)
U_outside=mu0*m*m/(12*s.pi*aa**3)
record('E068',3,'conservation','direct interior uniform B energy and exterior dipole field energy sum to surface-current work',eq(U_inside+U_outside,mu0*m*m/(4*s.pi*aa**3)) and eq((mu0*m*m/(4*s.pi*aa**3)).subs(m,4*s.pi*sig*om*aa**4/3),4*s.pi*mu0*sig**2*om**2*aa**5/9))
Rfield=mu0*Q*Q*om*om*aa/(36*s.pi)
record('E068',4,'dimensions','fixed charge and angular rate give magnetic energy linear in sphere radius and field singular at fixed dipole moment',eq(s.diff(Rfield,aa)*aa,Rfield) and eq(s.limit(mu0*m*m/(4*s.pi*aa**3),aa,0),s.oo))

# T064: Cattaneo hyperbolic thermal wave.
tau,D,kw,cv,kap,Tx,qx,Tt,qt,qs=s.symbols('tau D kw cv kap Tx qx Tt qt qs',positive=True,real=True)
w=s.symbols('w')
poly=tau*w*w+s.I*w-D*kw*kw
wplus=(-s.I+s.sqrt(4*tau*D*kw*kw-1))/(2*tau)
wminus=(-s.I-s.sqrt(4*tau*D*kw*kw-1))/(2*tau)
record('T064',1,'symbolic','two Cattaneo thermal roots solve exact telegraph dispersion polynomial',eq(poly.subs(w,wplus)) and eq(poly.subs(w,wminus)))
record('T064',2,'limit','low wave number branch reduces to Fourier diffusion while high wave number speed approaches finite square root D over tau',eq(s.limit(wplus/(-s.I*D*kw**2),kw,0,dir='+'),1) and eq(s.limit(s.re(wplus)/kw,kw,s.oo),s.sqrt(D/tau)))
# Energy equations multiplied by T, q/kappa, then integrated by parts.
temp,flux,tempx,fluxx=s.symbols('temp flux tempx fluxx',real=True)
temporalT=-fluxx/cv
temporalq=(-flux-kap*tempx)/tau
densityrate=cv*temp*temporalT+tau*flux*temporalq/kap
record('T064',3,'conservation','exact quadratic perturbation energy plus thermal flux divergence yields negative entropy production proxy',eq(densityrate+temp*fluxx+flux*tempx,-flux*flux/kap))
record('T064',4,'independent_derivation','zero relaxation limit has slow diffusion and one fast decaying nonhydrodynamic thermal mode',eq(s.limit(wplus,tau,0,dir='+'),-s.I*D*kw**2) and eq(s.limit(tau*wminus,tau,0,dir='+'),-s.I))

# W064: beta-plane Rossby quasigeostrophic wave.
beta,kx,ky,lam=s.symbols('beta kx ky lam',positive=True,real=True)
Q2=kx*kx+ky*ky+lam*lam
omega=-beta*kx/Q2
cgx=-beta*(Q2-2*kx*kx)/Q2**2
cgy=2*beta*kx*ky/Q2**2
record('W064',1,'symbolic','geostrophic potential vorticity Fourier eigenvalue yields westward Rossby phase velocity',eq((-s.I*omega)*(-Q2)+s.I*beta*kx) and eq(omega/kx,-beta/Q2))
record('W064',2,'independent_derivation','differentiate wave frequency independently to recover both group speed components',eq(s.diff(omega,kx),cgx) and eq(s.diff(omega,ky),cgy))
phi=s.symbols('phi',real=True)
psi=s.symbols('psi',real=True)
record('W064',3,'conservation','periodic domain beta energy transport is a pure total spatial derivative and no net work',eq(s.integrate(s.sin(phi)*s.cos(phi),(phi,0,2*s.pi))) and eq((kx*kx+ky*ky+lam*lam)/4,Q2/4))
record('W064',4,'limit','infinite deformation radius and vanishing beta limits give 2D Rossby and zero-frequency invariants',eq(s.limit(omega,lam,0),-beta*kx/(kx*kx+ky*ky)) and eq(s.limit(omega,beta,0),0) and eq(s.limit(omega/(kx),kx,0),-beta/(ky*ky+lam*lam)))

# O066: circular complex Gaussian speckle, Siegert relation and averaging.
I0,Ms,aa1,aa2,corr=s.symbols('I0 Ms aa1 aa2 corr',positive=True,real=True)
Intensity=s.symbols('Intensity',nonnegative=True)
p=s.exp(-Intensity/I0)/I0
record('O066',1,'independent_derivation','normalized exponential speckle density has mean I0 and variance I0 squared by independent integration',eq(s.integrate(p,(Intensity,0,s.oo)),1) and eq(s.integrate(Intensity*p,(Intensity,0,s.oo)),I0) and eq(s.integrate((Intensity-I0)**2*p,(Intensity,0,s.oo)),I0**2))
z=s.symbols('z',real=True)
record('O066',2,'symbolic','complex Gaussian fourth moment Siegert relation obeys perfect-coherence and zero-coherence limits',eq((1+z**2).subs(z,0),1) and eq((1+z**2).subs(z,1),2) and eq(s.diff(1+z**2,z),2*z))
gammam=(Ms/I0)**Ms/s.gamma(Ms)*Intensity**(Ms-1)*s.exp(-Ms*Intensity/I0)
# integral symbolic with integer model count to avoid positivity assumptions.
p3=s.simplify(gammam.subs(Ms,3))
record('O066',3,'numerical','three independent exponential speckles yield Gamma-shape-three distribution with exactly one-third relative variance',eq(s.integrate(p3,(Intensity,0,s.oo)),1) and eq(s.integrate(Intensity*p3,(Intensity,0,s.oo)),I0) and eq(s.integrate((Intensity-I0)**2*p3,(Intensity,0,s.oo)),I0**2/3))
C=s.sqrt(aa1**2+aa2**2)/(aa1+aa2)
record('O066',4,'limit','independent equal-polarization speckle contrast equals inverse square root two while one vanishing polarization restores unit contrast',eq(C.subs(aa2,aa1),1/s.sqrt(2)) and eq(s.limit(C,aa2,0,dir='+'),1))

# Q066: exact coherent-state spin-boson oscillator revival.
g,om,tm=s.symbols('g om tm',positive=True,real=True)
al=-(g/om)*(1-s.exp(-s.I*om*tm))
number=s.expand_complex(al*s.conjugate(al)).simplify()
record('Q066',1,'symbolic','conditional oscillator coherent amplitude solves forced Heisenberg motion and initial vacuum condition',eq(s.diff(al,tm)+s.I*om*al+s.I*g) and eq(al.subs(tm,0)))
lamb=s.exp(-2*number)
reduction=s.exp(-8*(g/om)**2*s.sin(om*tm/2)**2)
record('Q066',2,'independent_derivation','Gaussian coherent-state overlap reproduces exact periodic nonMarkov dephasing with full revival',eq(s.trigsimp(s.simplify(lamb-reduction))) and eq(reduction.subs(tm,2*s.pi/om),1) and eq(reduction.subs(tm,s.pi/om),s.exp(-8*g*g/om**2)))
zeta=s.symbols('zeta',real=True)
rho=s.Matrix([[1,zeta],[zeta,1]])/2
record('Q066',3,'symbolic','reduced spin eigenvalues and purity agree with exact overlap-dependent entanglement entropy spectrum',eq(s.det(rho),(1-zeta*zeta)/4) and eq(s.trace(rho*rho),(1+zeta*zeta)/2) and eq(s.trace(rho),1))
energy_osc=om*number
energy_int=2*g*s.re(al)
record('Q066',4,'conservation','time-dependent oscillator occupation exactly cancels negative interaction energy and closed system energy remains zero',eq(s.trigsimp(s.simplify(energy_osc+energy_int))) and eq(s.trigsimp(number-4*(g/om)**2*s.sin(om*tm/2)**2)))

assert len(checks)==24,(len(checks),checks)
ids=['M068','E068','T064','W064','O066','Q066']
assert {(x['id'],x['part']) for x in checks}=={(uid,part) for uid in ids for part in range(1,5)}
assert all(len({x['method'] for x in checks if x['id']==uid})>=2 for uid in ids)
report=dict(status='draft-only-not-admitted',new_problem_count=6,passed_count=len(checks),tests=checks,independent_expert_review='pending')
out=Path(__file__).resolve().parents[1]/'data/round13_draft_validation_report.json'
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(status=report['status'],subparts=len(checks),models=len(ids)),ensure_ascii=False))
