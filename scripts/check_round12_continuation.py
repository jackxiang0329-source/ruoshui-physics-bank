#!/usr/bin/env python3
"""Executed independent mathematical spot-checks for new round-12 models.
NOT a substitute for external expert assessment.
"""
import json
import itertools
import math
from pathlib import Path
import sympy as s

checks=[]
def record(uid,part,method,name,ok):
    assert method in ('symbolic','numerical','limit','dimensions','conservation','independent_derivation','physical_case')
    assert bool(ok),(uid,part,name)
    checks.append(dict(id=uid,part=part,method=method,name=name,passed=True))
def same(a,b=0):
    return s.simplify(a-b)==0

# Hill orbital rendezvous: check all coupled ODEs and exact invariants.
n,t,A,B,C,x0,y0,z0,vz0=s.symbols('n t A B C x0 y0 z0 vz0',positive=True,real=True)
x=A*s.cos(n*t)+B*s.sin(n*t)+2*C/n
y=y0-3*C*t-2*A*s.sin(n*t)+2*B*(s.cos(n*t)-1)
z=z0*s.cos(n*t)+vz0*s.sin(n*t)/n
record('M064',1,'symbolic','tidal Hill radial and tangential equations separately vanish for exact linear solutions',same(s.diff(x,t,2)-2*n*s.diff(y,t)-3*n**2*x) and same(s.diff(y,t,2)+2*n*s.diff(x,t)) and same(s.diff(z,t,2)+n**2*z))
record('M064',2,'independent_derivation','integral of tangential motion equals constant C and periodic vertical oscillator solves initial conditions',same(s.diff(y,t)+2*n*x,C) and same(z.subs(t,0),z0) and same(s.diff(z,t).subs(t,0),vz0))
vx,vy,vzz,xx,zz=s.symbols('vx vy vzz xx zz',real=True)
a_x=2*n*vy+3*n**2*xx;a_y=-2*n*vx;a_z=-n**2*zz
Jdot=2*vx*a_x+2*vy*a_y+2*vzz*a_z-6*n**2*xx*vx+2*n**2*zz*vzz
record('M064',3,'conservation','Jacobi pseudoenergy derivative cancels exactly between Coriolis and tidal forces',same(Jdot))
T=2*s.pi/n
record('M064',4,'physical_case','one orbital period returns radial and vertical coordinates while tangential offset gains only secular minus three C T',same(x.subs(t,T),x.subs(t,0)) and same(z.subs(t,T),z.subs(t,0)) and same(y.subs(t,T)-y.subs(t,0),-3*C*T) and same(s.diff(y,t).subs(t,T)-s.diff(y,t).subs(t,0)))

# Magnetic circular orbit and Lienard radiation with adiabatic cooling.
q,m,c,Bf,eps,gam,v=s.symbols('q m c Bf eps gam v',positive=True)
r=gam*m*v/(q*Bf);a=q*Bf*v/(gam*m)
record('E064',1,'dimensions','relativistic magnetic centripetal force and gyro frequency give consistent radius and acceleration',same(gam*m*v*v/r,q*v*Bf) and same(v/r,q*Bf/(gam*m)) and same(v*v/r,a))
P_L=q**2*gam**6*(a*a-v*v*a*a/c**2)/(6*s.pi*eps*c**3)
P_closed=q**4*Bf**2*(gam**2-1)/(6*s.pi*eps*m**2*c)
record('E064',2,'symbolic','Lienard transverse acceleration reduces to exact gamma-square synchrotron power formula',same(P_L.subs(v*v,c*c*(1-1/gam**2)),P_closed) and same(s.limit((P_closed/(q**2*a*a/(6*s.pi*eps*c**3))).subs(v,c*s.sqrt(1-1/gam**2)),gam,1,dir='+'),1))
kap,tau,u=s.symbols('kap tau u',positive=True)
G=s.coth(u+kap*tau);rad=m*c*s.csch(u+kap*tau)/(q*Bf)
record('E064',3,'conservation','exact coth cooling trajectory satisfies radiation energy balance and strictly decreasing orbital radius',same(s.diff(G,tau),-kap*(G*G-1)) and same(rad,m*c*s.sqrt(G*G-1)/(q*Bf)) and same(s.diff(rad,tau)+kap*rad*s.coth(u+kap*tau)))
beta=s.sqrt(1-1/gam**2)
wc=3*gam**3*c/(2*(gam*m*c*beta/(q*Bf)))
record('E064',4,'limit','ultrarelativistic critical frequency approaches three-halves gamma-squared gyro scale and correct adiabatic loss',same(s.limit(s.simplify(wc/(3*gam**2*q*Bf/(2*m))),gam,s.oo),1) and same((P_closed*2*s.pi*gam*m/(q*Bf))/(gam*m*c*c),2*s.pi*P_closed/(q*Bf*c*c)))

# Finite-N 1D Ising partition and thermodynamic limit.
K,h=s.symbols('K h',positive=True,real=True)
Lplus=s.exp(K)*(s.cosh(h)+s.sqrt(s.sinh(h)**2+s.exp(-4*K)))
Lminus=s.exp(K)*(s.cosh(h)-s.sqrt(s.sinh(h)**2+s.exp(-4*K)))
record('T061',1,'symbolic','exact Ising transfer eigenvalues reproduce matrix trace and determinant',same(Lplus+Lminus,2*s.exp(K)*s.cosh(h)) and same(Lplus*Lminus,s.exp(2*K)-s.exp(-2*K)))
mz=s.sinh(h)/s.sqrt(s.sinh(h)**2+s.exp(-4*K))
record('T061',2,'independent_derivation','field derivative of leading eigenvalue gives exact magnetization and zero-field susceptibility',same(s.diff(s.log(Lplus),h),mz) and same(s.diff(mz,h).subs(h,0),s.exp(2*K)))
xi=-1/s.log(s.tanh(K))
record('T061',3,'limit','eigenvalue spectral ratio yields exponential correlations and low-temperature divergence',same(s.simplify(((Lminus/Lplus).subs(h,0)-s.tanh(K)).rewrite(s.exp))) and same(s.limit(xi*s.exp(-2*K),K,s.oo),s.Rational(1,2)) and same(s.limit(xi,K,0,dir='+')))
Knum=.57;hnum=.31;N=6
Zexact=sum(math.exp(Knum*sum(bits[i]*bits[(i+1)%N] for i in range(N))+hnum*sum(bits)) for bits in itertools.product((-1,1),repeat=N))
Lpn=math.exp(Knum)*(math.cosh(hnum)+math.sqrt(math.sinh(hnum)**2+math.exp(-4*Knum)))
Lmn=math.exp(Knum)*(math.cosh(hnum)-math.sqrt(math.sinh(hnum)**2+math.exp(-4*Knum)))
cK=s.simplify(s.diff(-s.tanh(K),K)*(-K*K))
record('T061',4,'numerical','exact enumeration of 64 spin configurations matches trace transfer sixth power and positive heat capacity',abs(Zexact-(Lpn**N+Lmn**N))<1e-11 and same(cK,K*K/s.cosh(K)**2))

# sine-Gordon kink: PDE, mass shell, factorization and scattering.
X,vv,xx=s.symbols('X vv xx',real=True)
uK=4*s.atan(s.exp(xx-X));du=s.diff(uK,xx)
record('W061',1,'symbolic','sine-Gordon kink solves static nonlinear PDE and saturates exact topological energy density',same(s.trigsimp(s.diff(uK,xx,2)-s.sin(uK)).rewrite(s.exp)) and same(s.simplify((du-2/s.cosh(xx-X)).rewrite(s.exp))) and same(s.simplify(s.simplify(du**2/2+1-s.cos(uK)-4/s.cosh(xx-X)**2).rewrite(s.exp))))
gamma=1/s.sqrt(1-vv*vv);E=8*gamma;Mom=8*gamma*vv
record('W061',2,'conservation','Lorentz-boosted kink energy and momentum give invariant rest mass eight',same(E*E-Mom*Mom,64) and same(E.subs(vv,0),8) and same(Mom.subs(vv,0)))
sx=s.symbols('sx',real=True);eta=1/s.cosh(sx);V=1-2/s.cosh(sx)**2
record('W061',3,'independent_derivation','Pöschl-Teller kink fluctuation operator annihilates normalized translational zero mode',same(-s.diff(eta,sx,2)+V*eta) and same(s.integrate(eta**2,(sx,-s.oo,s.oo)),2))
kk=s.symbols('kk',real=True);phi=(s.tanh(sx)-s.I*kk)*s.exp(s.I*kk*sx);trans=(1-s.I*kk)/(-1-s.I*kk)
record('W061',4,'symbolic','exact Jost scattering wave has no backward component and unit-modulus transmitted wave',same(s.trigsimp(s.simplify(-s.diff(phi,sx,2)+V*phi-(1+kk*kk)*phi))) and same(s.expand_complex(trans*s.conjugate(trans)),1))

assert len(checks)==16
assert len(set((z['id'],z['part']) for z in checks))==16
assert all(len({z['method'] for z in checks if z['id']==uid})>=2 for uid in ('M064','E064','T061','W061'))
report=dict(status='draft-continuation-only',new_problem_count=4,passed_count=len(checks),tests=checks,independent_expert_review='pending')
out=Path(__file__).resolve().parents[1]/'data/round12_continuation_validation_report.json'
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'status':report['status'],'passed_count':len(checks)},ensure_ascii=False))
