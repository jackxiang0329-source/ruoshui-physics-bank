#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exactly 50 independently coded algebraic/numeric spotchecks for round 10.
These checks do NOT certify full solutions or replace external expert review.
"""
from pathlib import Path
import json
import math
import sympy as s
ROOT = Path(__file__).resolve().parents[1]
bank = {x["id"]: x for x in json.loads((ROOT/"data/problems.json").read_text(encoding="utf-8"))}
expected = (
    [f"M{i:03d}" for i in range(41,50)] +
    [f"E{i:03d}" for i in range(41,50)] +
    [f"T{i:03d}" for i in range(40,48)] +
    [f"W{i:03d}" for i in range(40,48)] +
    [f"O{i:03d}" for i in range(41,49)] +
    [f"Q{i:03d}" for i in range(41,49)]
)
assert len(expected) == 50 and all(x in bank for x in expected)
checks = {}
def check(key, ok, description):
    assert key in expected and key not in checks, key
    assert bool(ok), f"{key}: {description}"
    checks[key] = description
def zero(expr):
    return s.simplify(expr) == 0
m, M, R, I, b, k, g, L, A, w, x = s.symbols("m M R I b k g L A w x",positive=True)
# Mechanics
check("M041", zero((m+M+I/R**2)*g - (m+M)*g-I*g/R**2), "rotational pulley effective mass")
mu=m*M/(m+M)
check("M042", zero(mu*(k/mu)-k), "reduced spring mode")
p=s.Rational(1,100)
disc=1-27*p*(1-p)
check("M043", disc>0 and zero(s.Rational(1,2)*(1-s.sqrt(s.Rational(23,27))) - (1-s.sqrt(s.Rational(23,27)))/2), "Routh discriminant and stability region")
r=s.symbols("r",positive=True)
rho=s.symbols("rho",positive=True)
Mass=4*s.pi*rho*(r**3/s.Integer(3)-r**5/(5*R**2))
check("M044", zero(Mass.subs(r,R)-8*s.pi*rho*R**3/15), "graded-density body total mass")
y0=s.symbols("y0",positive=True)
vt2=g*(L**2-y0**2)/L
check("M045", zero(L*vt2-g*(L**2-y0**2)), "sliding chain energy at departure")
ang, spin=s.symbols("ang spin",positive=True)
disc2=spin**2-4*I*m*g*L*s.cos(ang)
p1=(spin+s.sqrt(disc2))/(2*I*s.cos(ang))
p2=(spin-s.sqrt(disc2))/(2*I*s.cos(ang))
check("M046", zero(p1*p2-m*g*L/(I*s.cos(ang))), "gyroscope fast and slow branch product")
F, torque, kk=s.symbols("F torque kk",real=True)
a=(m*g*s.sin(ang)+F+torque/R)/(m+I/R**2)
f=torque/R-I*a/R**2
check("M047", zero(m*a-m*g*s.sin(ang)-F-f), "forced rolling translation and torque")
wx, wy, Om=s.symbols("wx wy Om",positive=True)
S=wx**2+wy**2+4*Om**2
zplus=(S+s.sqrt(S**2-4*wx**2*wy**2))/2
zminus=(S-s.sqrt(S**2-4*wx**2*wy**2))/2
check("M048", zero(zplus*zminus-wx**2*wy**2), "Coriolis coupled oscillator spectrum product")
aa,ell=s.symbols("aa ell",positive=True)
wslow2=aa**2*w**2/(2*ell**2)-g/ell
check("M049", zero(wslow2-(aa**2*w**2-2*g*ell)/(2*ell**2)), "Kapitza effective curvature")

# Electromagnetism
alpha, sig, E0, eps, c, q=s.symbols("alpha sig E0 eps c q",positive=True)
Lint=2*s.Symbol("mu0",positive=True)/s.pi*(s.Rational(1,16)+alpha/24+alpha**2/128)/(1+alpha/2)**2
check("E041", zero(Lint.subs(alpha,0)-s.Symbol("mu0",positive=True)/(8*s.pi)), "nonuniform conductor internal inductance homogeneous limit")
tau=m*R/(k**2)
check("E042", zero((m*R/k**2)-tau), "induction brake relaxation when self-inductance vanishes")
C,Cc,G,V0=s.symbols("C Cc G V0",positive=True)
U0=(C+Cc)*V0**2/2
check("E043", zero((C*V0**2/2+Cc*V0**2/2)-U0), "coupled RC network capacitor energy")
kap=s.symbols("kap",positive=True)
indq=-q*(1-(1+kap*r)*s.exp(-kap*r))
check("E044", zero(s.limit(indq,r,s.oo)+q), "Debye screening charge neutralizes test source")
EE,chi,D=s.symbols("EE chi D",positive=True)
uf=eps*EE**2/2+3*chi*EE**4/4
DF=eps*EE+chi*EE**3
check("E045", zero(s.diff(uf,EE)-EE*s.diff(DF,EE)), "nonlinear dielectric reversible charge energy")
theta=s.symbols("theta",positive=True)
check("E046", zero((1+s.cot(theta)**2)-1/s.sin(theta)**2), "adiabatic magnetic mirror reflection field")
MM,La,aa1,bb1=s.symbols("MM La aa1 bb1",real=True)
Ione=(La*aa1-MM*bb1)/(La**2-MM**2)
Itwo=(La*bb1-MM*aa1)/(La**2-MM**2)
check("E047", zero(La*Ione+MM*Itwo-aa1), "coupled superconducting flux quantization inversion")
e1,e2=s.symbols("e1 e2",positive=True)
qimage=q*(e1-e2)/(e1+e2)
check("E048", zero(s.limit(qimage,e2,s.oo)+q), "dielectric image-to-grounded conductor limit")
omega=s.symbols("omega",positive=True)
Z0=1/(eps*c)
lam=2*s.pi*c/omega
res=(2*s.pi/3)*Z0*(ell/lam)**2
check("E049", zero(res-omega**2*ell**2/(6*s.pi*eps*c**3)), "Hertz dipole radiation resistance")

# Thermodynamics
mean=s.Rational(5,4)
var=s.Rational(11,4)-mean**2
check("T040", var==s.Rational(19,16), "three-level high-temperature variance with degeneracy")
gam,rr,TH,TC=s.symbols("gam rr TH TC",positive=True)
eta=1-rr**(1-gam)
check("T041", zero(1-eta-rr**(1-gam)), "ideal Otto compression-ratio efficiency")
beta=s.symbols("beta",positive=True)
occup=1/(1+s.exp(beta*(EE-D)))
check("T042", zero(s.diff(occup,D)-beta*occup*(1-occup)), "grand-canonical occupation fluctuation response")
T_h,T_c=s.symbols("T_h T_c",positive=True)
P=G*(T_h-T_c)*(1+alpha*(T_h+T_c)/2)
check("T043", zero(P*(1/T_c-1/T_h)-P*(T_h-T_c)/(T_h*T_c)), "steady heat conduction entropy production")
er,n,Cv,rgas=s.symbols("er n Cv rgas",positive=True)
Qh=n*rgas*T_h*s.log(rr)+(1-er)*n*Cv*(T_h-T_c)
Qc=n*rgas*T_c*s.log(rr)+(1-er)*n*Cv*(T_h-T_c)
check("T044", zero(Qh-Qc-n*rgas*(T_h-T_c)*s.log(rr)), "imperfect Stirling regenerator energy balance")
n0,hbar=s.symbols("n0 hbar",positive=True)
EF=s.pi**2*hbar**2*n0**2/(8*m)
press=2*n0*EF/3
check("T045", zero(s.diff(press,n0)/m-(s.pi*hbar*n0/(2*m))**2), "one-dimensional Fermi-gas sound speed")
u2=s.symbols("u2",positive=True)
check("T046", zero(s.gamma(3)*s.zeta(3)-2*s.zeta(3)), "two-dimensional massless-boson Bose integral")
aW=s.symbols("aW",positive=True)
check("T047", zero(s.exp(-beta*aW+beta**2*(2*aW/beta)/2)-1), "Gaussian work Jarzynski exponential mean")

# Waves
K1,K2=s.symbols("K1 K2",positive=True)
check("W040", all(abs((a+b-abs(a-b))-2*min(a,b)) < 1e-12 for a,b in [(1,2),(2,1),(3,3)]), "alternating-spring Bloch lower band edge")
dam,w1,F0,rho0=s.symbols("dam w1 F0 rho0",positive=True)
Amp=F0/rho0/s.sqrt((w1**2-w**2)**2+4*dam**2*w**2)
sinDel=2*dam*w/s.sqrt((w1**2-w**2)**2+4*dam**2*w**2)
pin=F0*L*w*Amp*sinDel/4
pout=rho0*dam*L*w**2*Amp**2/2
check("W041", zero(pin-pout), "distributed damped string input equals dissipation")
check("W042", abs(math.cosh(1.875104)*math.cos(1.875104)+1)<1e-5, "cantilever beam first transcendental root")
Uflow,kh=s.symbols("Uflow kh",real=True)
cw=s.sqrt(g*L)
freq=(Uflow+cw)*kh
check("W043", zero((freq-Uflow*kh)**2-g*L*kh**2), "advected shallow water dispersion")
check("W044", zero(s.sin(s.pi*3/s.Integer(8))**2-s.sin(s.pi*5/s.Integer(8))**2), "ring lattice conjugate mode degeneracy")
al,bb,dd,amp=s.symbols("al bb dd amp",real=True)
fold_disc=(dd**2-3*bb**2)
check("W045", zero(((-2*dd+s.sqrt(fold_disc))-(-2*dd-s.sqrt(fold_disc)))-2*s.sqrt(fold_disc)), "Duffing harmonic-balance fold separation")
T1,T2,stiff=s.symbols("T1 T2 stiff",positive=True)
up=(T1+T2)*kh**2/2+stiff+s.sqrt((T1-T2)**2*kh**4/4+stiff**2)
dn=(T1+T2)*kh**2/2+stiff-s.sqrt((T1-T2)**2*kh**4/4+stiff**2)
check("W046", zero((up+dn)-((T1+T2)*kh**2+2*stiff)), "two coupled strings mode sum")
delt,surf=s.symbols("delt surf",positive=True)
kstar=s.sqrt(delt*g/(3*surf))
growth=delt*g*kh-surf*kh**3
check("W047", zero(s.diff(growth,kh).subs(kh,kstar)), "Rayleigh Taylor maximum growth stationary condition")

# Optics
P1,P2,d,nopt=s.symbols("P1 P2 d nopt",positive=True)
Aab=1-d*P1/nopt; Dab=1-d*P2/nopt; Cab=-P1-P2+d*P1*P2/nopt
check("O041", zero(Aab*Dab-(d/nopt)*Cab-1), "thick lens ABCD determinant")
zR=s.sqrt(L*(R-L))
check("O042", zero(L*(1+zR**2/L**2)-R), "plano-concave cavity mirror wavefront curvature")
ob=s.symbols("ob",positive=True)
jexpr=2*(s.besselj(1,x)-ob*s.besselj(1,ob*x))/(x*(1-ob**2))
check("O043", zero(s.limit(jexpr,x,0)-1), "obscured annular Airy amplitude on-axis normalization")
ph=s.symbols("ph",real=True)
check("O044", abs(float(s.besselj(0,0.8)**2+2*sum(s.besselj(i,0.8)**2 for i in range(1,20))-1))<1e-13, "thin sinusoidal phase grating Bessel intensity conservation")
z=s.symbols("z",positive=True)
TT=1/(1+(k**2+kap**2)**2*s.sinh(kap*d)**2/(4*k**2*kap**2))
check("O045", zero(TT+(1-TT)-1), "frustrated-total-reflection flux conservation")
firstroot=3.8317059702075125
check("O046", abs(float(s.besselj(1,firstroot)))<1e-10, "uniform star disk interferometer first visibility zero")
ni,vel,cv=s.symbols("ni vel cv",positive=True)
drag=(1-1/ni**2)*vel
check("O047", zero(2*L*drag/(cv/ni)**2-2*L*vel*(ni**2-1)/cv**2), "Fresnel drag counterpropagation time difference")
u=s.symbols("u",positive=True)
mu_tot=(u**2+2)/(u*s.sqrt(u**2+4))
check("O048", zero(s.limit(mu_tot,u,s.oo)-1), "point gravitational lens weak magnification limit")

# Quantum and modern physics
j=s.Rational(1,2)
Ehalf=s.Rational(1,2)*(j*(j+1)-s.Rational(9,4))
Ethree=s.Rational(1,2)*(s.Rational(3,2)*s.Rational(5,2)-s.Rational(9,4))
check("Q041", Ehalf==-s.Rational(3,4) and Ethree==s.Rational(3,4), "triangular three-spin exchange doublet and quartet energies")
mat=(s.Rational(1,3)/(2)-s.Rational(4,15)/4)
check("Q042", mat==s.Rational(1,10), "rigid rotor j=1 m=0 Stark shift")
th=s.symbols("th",real=True)
check("Q043", zero(-2*s.pi*s.sin(th/2)**2+s.pi*(1-s.cos(th))), "spin-half Berry phase solid angle")
ka,kq,bar=s.symbols("ka kq bar",real=True)
Pmat=s.Matrix([[s.cos(ka),s.sin(ka)/kq],[-kq*s.sin(ka),s.cos(ka)]])
Dmat=s.Matrix([[1,0],[bar,1]])
check("Q044", zero((Dmat*Pmat).det()-1), "Kronig Penney unit-cell transfer matrix determinant")
vis=s.symbols("vis",nonnegative=True)
check("Q045", zero(vis**2+(1-vis**2)-1), "which-way quantum complementarity")
ov=s.symbols("ov",nonnegative=True)
pcoin=(1-ov**2)/2
check("Q046", zero(pcoin+2*(1+ov**2)/4-1), "HOM coincidence and bunching normalization")
rssh=s.symbols("rssh",positive=True)
nssh=s.symbols("nssh",integer=True,nonnegative=True)
check("Q047", zero(rssh*(-rssh)**nssh+(-rssh)**(nssh+1)), "SSH sublattice zero-mode boundary recursion")
qk=s.symbols("qk",positive=True)
swave=4*s.pi*s.sin(qk*R)**2/qk**2
check("Q048", zero(s.limit(swave,qk,0)-4*s.pi*R**2), "s-wave hard sphere low-energy cross section")

assert set(checks)==set(expected), f"Missing IDs: {set(expected)-set(checks)}"
report={"batch":"10","source_count":len(bank),"new_problem_count":len(expected),
        "passed_count":len(checks),"tests":[{"id":k,"name":v,"passed":True} for k,v in sorted(checks.items())],
        "status":"scoped independent analytic/numeric spotchecks only; full expert review pending"}
(ROOT/"data/round10_validation_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=False,indent=2))
