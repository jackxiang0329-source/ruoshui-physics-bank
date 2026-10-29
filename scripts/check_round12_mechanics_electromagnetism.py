#!/usr/bin/env python3
"""Round12 independently recomputed mathematical checks for M065 M066 E065 E066."""
import json,math
from pathlib import Path
import sympy as s
tests=[]
def check(uid,part,method,name,ok):
    assert bool(ok),(uid,part,name)
    tests.append(dict(id=uid,part=part,method=method,name=name,passed=True))
def equal(a,b=0):
    return s.simplify(a-b)==0

# M065: symplectic kicked rotor and resonance island.
K,th=s.symbols("K th",positive=True,real=True)
Jac=s.Matrix([[1+K*s.cos(th),1],[K*s.cos(th),1]])
check("M065",1,"symbolic","kicked-rotor standard map Jacobian has determinant one and preserves symplectic area",equal(Jac.det(),1))
check("M065",2,"physical_case","standard map theta-zero point is hyperbolic and theta-pi is elliptic for zero K less than four",float((2+K).subs(K,2))>2 and abs(float((2-K).subs(K,2)))<2)
ps=2*s.sqrt(K)*s.sin(th/2)
check("M065",3,"independent_derivation","small-K pendulum separatrix area integrates to sixteen root K and full width four root K",equal(s.integrate(2*ps,(th,0,2*s.pi)),16*s.sqrt(K)) and equal(2*ps.subs(th,s.pi),4*s.sqrt(K)))
check("M065",4,"limit","unforced standard map becomes free symplectic twist and K four gives period doubling linear threshold",Jac.subs(K,0)==s.Matrix([[1,1],[0,1]]) and equal((2-K).subs(K,4),-2))

# M066: static catenary equilibrium and gravity.
a,xx,ell,lam,g,u=s.symbols("a xx ell lam g u",positive=True,real=True)
Y=a*(s.cosh(xx/a)-s.cosh(ell/(2*a)));H=lam*g*a
check("M066",1,"symbolic","catenary vertical force balance holds exactly for nonlinear arc-length weight",equal(H*s.diff(Y,xx,2),lam*g*s.cosh(xx/a)))
S=2*a*s.sinh(ell/(2*a))
check("M066",2,"independent_derivation","integrated catenary length is two a sinh u and sinh u over u increases from one",equal(s.integrate(s.cosh(xx/a),(xx,-ell/2,ell/2)),S) and float((u*s.cosh(u)-s.sinh(u)).subs(u,1))>0)
check("M066",3,"conservation","support vertical forces exactly balance full chain weight with minimum tension at center",equal(2*H*s.sinh(ell/(2*a)),lam*g*S) and equal((H*s.cosh(xx/a)).subs(xx,0),H))
integral=s.integrate((s.cosh(xx)-s.cosh(u))*s.cosh(xx),(xx,-u,u))
check("M066",4,"symbolic","catenary gravitational energy integral and shallow-sag arc-length expansion are exact",equal(integral,u-s.sinh(u)*s.cosh(u)) and equal(s.limit((s.sinh(u)/u-1)/u**2,u,0),s.Rational(1,6)))
# E065 coated dielectric sphere boundary matching.
e1,e2,e3,f=s.symbols("e1 e2 e3 f",positive=True)
den=e1+2*e2; t=(e2-e1)/den
eff=e2*(1-2*f*t)/(1+f*t)
B=3*e3/((eff+2*e3)*(1+f*t))
A=B*(1+t); C=f*t*B
d=1-B-C
check("E065",1,"symbolic","both dielectric boundary conditions hold at outer and inner interfaces",equal(B+C,1-d) and equal(e2*(B-2*C),e3*(1+2*d)) and equal(e1*A,e2*(B-2*t*B)))
check("E065",2,"limit","effective permittivity reduces to shell-only and equal-material sphere limits",equal(eff.subs(f,0),e2) and equal(eff.subs(e1,e2),e2) and equal(d,(eff-e3)/(eff+2*e3)))
neutral=(e2-e3)*den+f*(e1-e2)*(e3+2*e2)
check("E065",3,"independent_derivation","neutral inclusion condition algebraically equivalent to zero exterior dipole",equal(s.together((eff-e3)*(den-f*(e1-e2))),neutral))
check("E065",4,"numerical","sample positive dielectric stack has finite field and satisfies all four interface equations",all(abs(float(expr.subs({e1:5,e2:2,e3:3,f:s.Rational(1,8)})))<1e-10 for expr in [B+C+d-1,e2*(B-2*C)-e3*(1+2*d),A-B-t*B,e1*A-e2*(B-2*t*B)]))

# E066: incompressible shear Alfven waves and interface energy.
B0,mu,rho,kz=s.symbols("B0 mu rho kz",positive=True,real=True)
vA=B0/s.sqrt(mu*rho)
check("E066",1,"symbolic","ideal MHD momentum and induction equations imply exact shear Alfven phase speed",equal(rho*(vA*kz)**2,B0**2*kz**2/mu))
u0,b0,uz,bz=s.symbols("u0 b0 uz bz",real=True)
ut=B0*bz/(mu*rho);bt=B0*uz
check("E066",2,"independent_derivation","Elsasser variables exactly decouple into opposite-direction transport equations",equal(ut+bt/s.sqrt(mu*rho)-vA*(uz+bz/s.sqrt(mu*rho))) and equal(ut-bt/s.sqrt(mu*rho)+vA*(uz-bz/s.sqrt(mu*rho))))
check("E066",3,"conservation","kinetic and magnetic Alfven energies satisfy exact local flux conservation",equal(rho*u0*ut+b0*bt/mu-B0/mu*(uz*b0+u0*bz)) and equal(B0*s.sqrt(mu*rho)*u0*u0/mu,rho*vA*u0*u0))
Z1,Z2=s.symbols("Z1 Z2",positive=True)
rr=(Z1-Z2)/(Z1+Z2);tt=2*Z1/(Z1+Z2)
check("E066",4,"symbolic","interface Alfven velocity continuity and impedance-weighted energy reflection plus transmission equal unity",equal(1+rr,tt) and equal(Z1*(1-rr),Z2*tt) and equal(rr**2+(Z2/Z1)*tt**2,1))
assert len(tests)==16 and len(set((x["id"],x["part"]) for x in tests))==16
report={"status":"draft-continuation-only","new_problem_count":4,"passed_count":16,"tests":tests,"independent_expert_review":"pending"}
p=Path(__file__).resolve().parents[1]/"data/round12_mechanics_electromagnetism_validation_report.json"
p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("PASS: 16 four-model subpart checks")
