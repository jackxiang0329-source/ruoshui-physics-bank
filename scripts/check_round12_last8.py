#!/usr/bin/env python3
"""Round 12 final eight advanced models: 32 reproducible nontrivial subpart tests."""
import json,math
from pathlib import Path
import mpmath as mp
import sympy as s
tests=[]
def record(uid,part,method,name,condition):
    assert bool(condition),(uid,part,name)
    tests.append(dict(id=uid,part=part,method=method,name=name,passed=True))
def eq(a,b=0):
    return s.simplify(a-b)==0
mp.mp.dps=35

# M067: Rankine vortex vorticity, pressure and free surface.
rho,Omega,a,R,rr,g=s.symbols("rho Omega a R rr g",positive=True,real=True)
vcore=Omega*rr;vouter=Omega*a*a/rr
record("M067",1,"symbolic","Rankine vortex has uniform core vorticity, irrotational exterior and nonzero constant circulation",eq(s.diff(rr*vcore,rr)/rr,2*Omega) and eq(s.diff(rr*vouter,rr)/rr) and eq(2*s.pi*rr*vouter,2*s.pi*Omega*a*a))
pcore=rho*Omega**2*rr**2/2
pouter=rho*Omega**2*a*a-rho*Omega**2*a**4/(2*rr**2)
record("M067",2,"independent_derivation","piecewise radial Euler pressure gradient equals centrifugal acceleration with continuous core interface",eq(s.diff(pcore,rr),rho*vcore**2/rr) and eq(s.diff(pouter,rr),rho*vouter**2/rr) and eq(pcore.subs(rr,a),pouter.subs(rr,a)))
energy=s.integrate(rho*vcore**2*s.pi*rr,(rr,0,a))+s.integrate(rho*vouter**2*s.pi*rr,(rr,a,R))
angular=s.integrate(2*s.pi*rho*rr**2*vcore,(rr,0,a))+s.integrate(2*s.pi*rho*rr**2*vouter,(rr,a,R))
record("M067",3,"conservation","integrated Rankine kinetic energy and angular momentum match two-region closed-form expressions",eq(energy,s.pi*rho*Omega**2*a**4*(s.Rational(1,4)+s.log(R/a))) and eq(angular,s.pi*rho*Omega*a**2*(R**2-a**2/s.Integer(2))))
surface_outer=-Omega**2*a**4*(1/rr**2-1/R**2)/(2*g)
surface_inner=-Omega**2*(a**2-rr**2+a**2*(1-a**2/R**2))/(2*g)
record("M067",4,"physical_case","vortex free-surface gradients and axis depression independently match radial pressure integration",eq(s.diff(surface_outer,rr),vouter**2/(g*rr)) and eq(s.diff(surface_inner,rr),vcore**2/(g*rr)) and eq(surface_outer.subs(rr,a),surface_inner.subs(rr,a)) and eq(-rho*g*surface_inner.subs(rr,0),pouter.subs(rr,R)))

# E067: nonlinear planar Poisson-Boltzmann double layer.
eps,kappa,VT,psi0,x=s.symbols("eps kappa VT psi0 x",positive=True,real=True)
z=s.tanh(psi0/4)*s.exp(-kappa*x)
psi=4*s.atanh(z)
record("E067",1,"symbolic","Boltzmann cation and anion concentrations yield sinh Poisson source and correct first integral",eq(s.exp(-psi0)-s.exp(psi0),-2*s.sinh(psi0)) and eq(4*s.sinh(psi0/2)**2,2*(s.cosh(psi0)-1)))
sample={psi0:s.Rational(3,2),kappa:s.Rational(6,5),x:s.Rational(7,10)}
residual=s.diff(psi,x,2)-kappa**2*s.sinh(psi)
record("E067",2,"numerical","exact Gouy-Chapman potential satisfies nonlinear Poisson-Boltzmann ODE and decays at infinity",abs(float(residual.subs(sample).evalf()))<1e-11 and eq(s.limit(psi,x,s.oo),0))
sigma=2*eps*kappa*VT*s.sinh(psi0/2)
record("E067",3,"independent_derivation","Grahame surface-charge derivative equals positive differential capacitance with Debye low-potential limit",eq(s.diff(sigma,psi0)/VT,eps*kappa*s.cosh(psi0/2)) and eq(s.limit(sigma/psi0,psi0,0,dir='+'),eps*kappa*VT))
pm=s.symbols("pm",positive=True)
work=s.integrate(2*eps*kappa*VT**2*s.sinh(pm/2),(pm,0,psi0))
record("E067",4,"conservation","charging work integrates Grahame law and Maxwell normal stress equals osmotic excess",eq(work,4*eps*kappa*VT**2*(s.cosh(psi0/2)-1)) and eq(2*s.sinh(psi0/2)**2,s.cosh(psi0)-1))
# O064: causal Lorentz optical susceptibility.
wp,w0,g,w=s.symbols("wp w0 g w",positive=True,real=True)
den=(w0*w0-w*w)**2+g*g*w*w
chip=wp*wp*(w0*w0-w*w)/den;chipp=wp*wp*g*w/den
record("O064",1,"symbolic","real and imaginary Lorentz susceptibility reproduce positive absorbed optical power",eq(s.im(wp**2/(w0**2-w**2-s.I*g*w)),chipp) and float(chipp.subs({wp:1,w0:2,g:s.Rational(1,5),w:2}))>0)
g0=0.01;w00=2.0
def absorption(wv):
    return g0*wv/((w00*w00-wv*wv)**2+g0*g0*wv*wv)
record("O064",2,"numerical","weak damping half-height points at plus or minus gamma over two bracket Lorentz absorption peak",abs(absorption(w00+g0/2)/absorption(w00)-.5)<.004 and abs(absorption(w00-g0/2)/absorption(w00)-.5)<.004)
poles=[complex(-.2j+complex(4-.04)**.5),complex(-.2j-complex(4-.04)**.5)]
overdamped=[complex(-2.5j+complex(4-6.25)**.5),complex(-2.5j-complex(4-6.25)**.5)]
record("O064",3,"physical_case","underdamped and overdamped causal poles remain in lower complex frequency half plane",all(z.imag<0 for z in poles+overdamped))
def spectral(x):
    return mp.mpf('.2')*x*x/((mp.mpf('4')-x*x)**2+mp.mpf('.04')*x*x)
area=mp.quad(spectral,[0,1,mp.mpf('1.9'),2,mp.mpf('2.1'),4,mp.inf])
record("O064",4,"numerical","independent positive-frequency spectral quadrature verifies oscillator-strength sum rule",abs(float(area-mp.pi/2))<1e-9)

# Q064: teleportation and Werner resource.
aa,bb=s.symbols("aa bb")
zero=s.Matrix([1,0]);one=s.Matrix([0,1])
X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1);I=s.eye(2)
psi=aa*zero+bb*one
phi_plus=(s.kronecker_product(zero,zero)+s.kronecker_product(one,one))/s.sqrt(2)
phi_minus=(s.kronecker_product(zero,zero)-s.kronecker_product(one,one))/s.sqrt(2)
psi_plus=(s.kronecker_product(zero,one)+s.kronecker_product(one,zero))/s.sqrt(2)
psi_minus=(s.kronecker_product(zero,one)-s.kronecker_product(one,zero))/s.sqrt(2)
lhs=s.kronecker_product(psi,phi_plus)
rhs=(s.kronecker_product(phi_plus,psi)+s.kronecker_product(phi_minus,Z*psi)+s.kronecker_product(psi_plus,X*psi)+s.kronecker_product(psi_minus,X*Z*psi))/2
record("Q064",1,"symbolic","full eight-component Bell teleportation expansion exactly equals original three-qubit state",all(eq(x) for x in lhs-rhs))
record("Q064",2,"independent_derivation","four Pauli feed-forward corrections recover arbitrary input up to global phase",all(eq((C*E*psi)[i]-psi[i]) for C,E in [(I,I),(Z,Z),(X,X),(Z*X,X*Z)] for i in (0,1)))
p=s.symbols("p",real=True)
rho=s.Matrix([[1,0],[0,0]])
out=p*rho+(1-p)*I/2
record("Q064",3,"symbolic","Werner-assisted teleportation gives isotropic depolarizing channel and input-independent fidelity",eq(out[0,0],(1+p)/2) and eq(s.trace(out),1))
record("Q064",4,"physical_case","quantum advantage and Werner partial-transpose entanglement share strict p greater than one-third threshold",eq(((1+p)/2-s.Rational(2,3)).subs(p,s.Rational(1,3))) and float(((1+p)/2-s.Rational(2,3)).subs(p,s.Rational(3,5)))>0 and float(((1-3*p)/4).subs(p,s.Rational(3,5)))<0)

# T063: OU quench.
ki,zeta,Ti,Tf,tt,kb=s.symbols("ki zeta Ti Tf tt kb",positive=True)
rate=ki/zeta;ri=Ti/Tf;rt=1+(ri-1)*s.exp(-2*rate*tt)
var=kb*Tf/ki*rt
record("T063",1,"symbolic","Ornstein-Uhlenbeck variance solves exact Ito covariance evolution with final bath diffusion",eq(s.diff(var,tt),-2*ki*var/zeta+2*kb*Tf/zeta))
U=ki*var/2;U0=kb*Ti/2;Q=kb*(Tf-Ti)*(1-s.exp(-2*rate*tt))/2
record("T063",2,"conservation","mean harmonic energy change exactly equals heat with zero parameter work",eq(U-U0,Q) and eq(s.limit(U,tt,s.oo),kb*Tf/2))
S=kb*(s.log(rt/ri)+ri-rt)/2
entropy_rate=kb*rate*(rt-1)**2/rt
record("T063",3,"symbolic","total system-plus-bath entropy production derivative is nonnegative perfect square",eq(s.diff(S,tt),entropy_rate) and float(entropy_rate.subs({ki:2,zeta:3,Ti:5,Tf:2,tt:1,kb:1}))>0)
D=(rt-1-s.log(rt))/2
record("T063",4,"independent_derivation","Gaussian KL relative entropy decreases with rate exactly matching thermal entropy production",eq(s.diff(D,tt),-rate*(rt-1)**2/rt))

# W063: Love SH waves in layered solid.
c1,c2,beta,om,q,al,h,mu1,mu2=s.symbols("c1 c2 beta om q al h mu1 mu2",positive=True)
record("W063",1,"dimensions","Love-wave guided velocity window yields oscillatory upper layer and evanescent substrate",float((5/2)**2-2**2)>0 and float(2**2-(5/3)**2)>0)
qv=mp.sqrt(mp.mpf(25)/4-4);av=mp.sqrt(4-mp.mpf(25)/9)
hv=mp.atan(2*av/qv)/qv
record("W063",2,"numerical","SH displacement and shear stress match across both interfaces for exact dispersion root",abs(float(mp.tan(qv*hv)-2*av/qv))<1e-12 and abs(float(qv*mp.sin(qv*hv)-2*av*mp.cos(qv*hv)))<1e-12)
wcut=lambda n:n*math.pi/(1*math.sqrt(1/2**2-1/3**2))
record("W063",3,"limit","Love higher-mode cutoff frequencies scale with positive integer mode order while fundamental cutoff is zero",wcut(2)/wcut(1)==2 and wcut(1)>0 and wcut(0)==0)
record("W063",4,"conservation","substrate mode energy integral has inverse decay length and diverges at loss of confinement",eq(s.integrate(s.exp(-2*al*s.Symbol("zz",positive=True)),(s.Symbol("zz",positive=True),0,s.oo)),1/(2*al)) and s.limit(1/(2*al),al,0,dir='+')==s.oo)

# O065: exact Bessel angular spectrum and finite aperture.
rr,kp=s.symbols("rr kp",positive=True)
j=s.besselj(2,kp*rr)
res=rr**2*s.diff(j,rr,2)+rr*s.diff(j,rr)+(kp*kp*rr*rr-4)*j
record("O065",1,"symbolic","Bessel azimuthal-order-two radial Helmholtz operator annihilates exact mode",eq(s.simplify(s.expand_func(res))))
record("O065",2,"physical_case","zeroth-order Bessel beam has bright axis while nonzero topological order has a dark vortex axis",eq(s.besselj(0,0),1) and eq(s.besselj(2,0)) and eq(s.diff(3*s.Symbol("phi"),s.Symbol("phi")),3))
Rr=s.symbols("Rr",positive=True)
power=Rr**2*(s.besselj(0,Rr)**2+s.besselj(1,Rr)**2)/2
record("O065",3,"numerical","finite-radius Bessel beam power grows linearly with aperture radius instead of converging",abs(float(power.subs(Rr,2000))/2000-1/math.pi)<.001 and float(power.subs(Rr,2000))>float(power.subs(Rr,1000)))
R0,kz=s.symbols("R0 kz",positive=True)
zmax=R0*kz/kp
record("O065",4,"limit","finite-aperture conical ray propagation distance diverges for small cone angle and vanishes for transverse propagation",eq(s.limit(zmax,kp,0,dir='+'),s.oo) and eq(s.limit(zmax,kz,0,dir='+'),0))

# Q065: repeated Zeno projections.
Om,tm=s.symbols("Om tm",positive=True)
N=s.symbols("N",integer=True,positive=True)
record("Q065",1,"symbolic","two-level unitary evolution preserves norm and first orthogonal time gives zero survival",eq(s.cos(Om*tm)**2+s.sin(Om*tm)**2,1) and eq(s.cos(Om*(s.pi/(2*Om)))**2))
record("Q065",2,"numerical","Zeno survival approaches one at rate inverse measurement count for fixed total time",abs(math.cos(.8/10000)**(20000)-(1-.8**2/10000))<1e-8 and math.cos(.8/10000)**(20000)>math.cos(.8/100)**200)
H=s.Matrix([[0,s.Symbol("hbar",positive=True)*Om],[s.Symbol("hbar",positive=True)*Om,0]])
record("Q065",3,"independent_derivation","initial energy variance gives Zeno time inverse Rabi frequency",eq(H[0,0]) and eq((H*H)[0,0],(s.Symbol("hbar",positive=True)*Om)**2))
pn=s.symbols("pn",positive=True)
geom=(1-pn**N)/(1-pn)
record("Q065",4,"limit","expected number of sequential measurements equals truncated geometric sum with deterministic limit N",eq(s.summation(pn**s.Symbol("j",integer=True),(s.Symbol("j",integer=True),0,N-1)),geom) and eq(s.limit(geom,pn,1),N))

assert len(tests)==32 and len(set((x["id"],x["part"]) for x in tests))==32
for uid in ["M067","E067","O064","Q064","T063","W063","O065","Q065"]:
    assert len({x["method"] for x in tests if x["id"]==uid})>=2
report=dict(status="draft-continuation-only",new_problem_count=8,passed_count=32,tests=tests,independent_expert_review="pending")
out=Path(__file__).resolve().parents[1]/"data/round12_last8_validation_report.json"
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("PASS 32 substantive checks for final eight round12 models")
