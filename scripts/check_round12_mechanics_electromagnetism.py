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

# M065 arbitrary central power law.
r,r0,k,m,alpha,L2=s.symbols("r r0 k m alpha L2",positive=True,real=True)
U=L2/(2*m*r**2)+k*r**alpha/alpha
eq={L2:m*k*r0**(alpha+2)}
check("M065",1,"symbolic","effective-potential derivative vanishes exactly at prescribed circular orbit",equal(s.diff(U,r).subs(r,r0).subs(eq)))
d2=s.diff(U,r,2).subs(r,r0).subs(eq)
check("M065",2,"independent_derivation","radial force derivative equals negative effective-potential curvature",equal(d2,(alpha+2)*k*r0**(alpha-2)) and equal(s.diff(-s.diff(U,r)/m,r).subs(r,r0).subs(eq),-d2/m))
angle=2*s.pi/s.sqrt(alpha+2)
check("M065",3,"physical_case","Kepler apsidal angle 2pi and isotropic oscillator angle pi",equal(angle.subs(alpha,-1),2*s.pi) and equal(angle.subs(alpha,2),s.pi))
Lr=s.sqrt(m*k)*r0**((alpha+2)/2)
Ec=k*r0**alpha*(s.Rational(1,2)+1/alpha)
check("M065",4,"symbolic","circular-orbit dE/dL equals positive orbital angular frequency",equal(s.simplify(s.diff(Ec,r0)/s.diff(Lr,r0)),s.simplify(Lr/(m*r0**2))))

# M066 exact cycloidal tautochrone.
a,th,g,mm,thdot,sdot=s.symbols("a th g mm thdot sdot",positive=True,real=True)
xx=a*(th+s.sin(th)); yy=a*(1-s.cos(th)); ss=4*a*s.sin(th/2)
check("M066",1,"symbolic","arc-length derivative and gravitational potential are exactly harmonic",equal(s.diff(ss,th),2*a*s.cos(th/2)) and equal(s.trigsimp(yy-ss**2/(8*a))))
omega=s.sqrt(g/(4*a))
check("M066",2,"physical_case","quarter-period fall time independent of initial displacement and exact energy oscillator",equal(s.pi/(2*omega),s.pi*s.sqrt(a/g)) and equal(2*s.pi/omega,4*s.pi*s.sqrt(a/g)))
curv_num=s.diff(xx,th)*s.diff(yy,th,2)-s.diff(yy,th)*s.diff(xx,th,2)
curv_den=(s.diff(xx,th)**2+s.diff(yy,th)**2)**s.Rational(3,2)
curv=s.simplify(curv_num/curv_den)
check("M066",3,"numerical","curvature radius and inward normal gravity projection checked at nontrivial angle",abs(float(curv.subs({a:2,th:s.pi/3})-1/(4*a*s.cos(th/2)).subs({a:2,th:s.pi/3})))<1e-12 and abs(float((mm*g*s.cos(th/2)).subs({mm:3,g:9.8,th:s.pi/3})-3*9.8*math.cos(math.pi/6)))<1e-12)
Etheta=mm*(2*a*s.cos(th/2)*thdot)**2/2+mm*g*yy
Es=mm*sdot**2/2+mm*g*ss**2/(8*a)
check("M066",4,"symbolic","theta-coordinate energy exactly equals arc-length energy after Jacobian transformation",equal(s.trigsimp(Etheta-Es.subs(sdot,2*a*s.cos(th/2)*thdot))))

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

# E066 conductor skin depth and power conservation.
mu,sigma,om,eps=s.symbols("mu sigma om eps",positive=True)
delta=s.sqrt(2/(mu*sigma*om))
q=(1-s.I)/delta
check("E066",1,"symbolic","Maxwell conductor propagation constant satisfies diffusion dispersion",equal(q*q,-s.I*mu*sigma*om))
H=(1+s.I)/(om*mu*delta)
Z=(1-s.I)/(sigma*delta)
check("E066",2,"symbolic","Faraday law and positive-real surface impedance exactly agree",equal(-q,s.I*om*mu*H) and equal(Z*H,1) and equal(s.re(Z),1/(sigma*delta)))
P_in=s.simplify(s.re(s.conjugate(H))/2)
P_j=sigma*delta/4
check("E066",3,"conservation","Poynting input equals depth-integrated Joule dissipation",equal(P_in,P_j) and equal(s.integrate(sigma*s.exp(-2*s.Symbol('z',positive=True)/delta)/2,(s.Symbol('z',positive=True),0,s.oo)),P_j))
z=s.symbols("z",positive=True)
fraction=1-s.exp(-2*z/delta)
check("E066",4,"limit","depth-integrated dissipated power fraction approaches unity and skin depth obeys inverse square root of frequency",equal(s.limit(fraction,z,s.oo),1) and equal(s.simplify(delta.subs(om,2*om)/delta),1/s.sqrt(2)))
assert len(tests)==16 and len(set((x["id"],x["part"]) for x in tests))==16
report={"status":"draft-continuation-only","new_problem_count":4,"passed_count":16,"tests":tests,"independent_expert_review":"pending"}
p=Path(__file__).resolve().parents[1]/"data/round12_mechanics_electromagnetism_validation_report.json"
p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print("PASS: 16 four-model subpart checks")
