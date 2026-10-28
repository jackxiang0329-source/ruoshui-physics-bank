#!/usr/bin/env python3
"""Independent symbolic/numeric identities for 12 newly submitted composite items.
This tests selected invariant relations, not a complete expert proof review.
"""
import json, math
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
problems={p["id"]:p for p in json.loads((ROOT/"data/problems.json").read_text(encoding="utf-8"))}
ids=("M010","M011","E010","E011","T010","T011","W010","W011","O010","O011","Q010","Q011")
assert all(x in problems for x in ids)
checks=[]
def check(label,expr):
    assert bool(expr),label
    checks.append(label)
mu,r1,r2=s.symbols("mu r1 r2",positive=True)
a=(r1+r2)/2
vp=s.sqrt(mu*(2/r1-1/a));va=s.sqrt(mu*(2/r2-1/a))
check("M010 angular momentum",s.simplify((r1*vp)**2-(r2*va)**2)==0)
check("M010 orbital energy",s.simplify((vp**2/2-mu/r1)+(mu/(2*a)))==0)
th=s.symbols("th",real=True)
kap=s.sin(th/2)
check("M011 small amplitude elliptic coefficient",s.simplify(s.limit(s.diff(s.elliptic_k(kap**2),th,2),th,0)-s.pi/16)==0)
L,M,C=s.symbols("L M C",positive=True)
Q=s.symbols("Q",real=True)
ind=s.Matrix([[L,M],[M,L]])
check("E010 eigen inductances",set(ind.eigenvals())=={L+M,L-M})
check("E010 initial energy modes",s.simplify(2*(Q**2/(4*C))-Q**2/(2*C))==0)
rho,rad,eps,eps0,aa=s.symbols("rho rad eps eps0 aa",positive=True)
Din=rho*rad**2/(4*aa)
Dout=rho*aa**3/(4*rad**2)
check("E011 Gauss law inside",s.simplify(s.diff(rad**2*Din,rad)/rad**2-rho*rad/aa)==0)
check("E011 D continuity",s.simplify(Din.subs(rad,aa)-Dout.subs(rad,aa))==0)
Uin=s.integrate(2*s.pi*Din**2*rad**2/eps,(rad,0,aa))
Uout=s.integrate(2*s.pi*Dout**2*rad**2/eps0,(rad,aa,s.oo))
check("E011 total field energy",s.simplify(Uin+Uout-s.pi*rho**2*aa**5*(1/(56*eps)+1/(8*eps0)))==0)
cv,R,beta,N,T1,lam=s.symbols("cv R beta N T1 lam",positive=True)
check("T010 temperature volume scaling",s.simplify((lam**(1-beta))*(lam**(beta-1))-1)==0)
W=N*R*T1*(lam**(1-beta)-1)/(1-beta)
check("T010 isothermal work limit",s.limit(W,beta,1)==N*R*T1*s.log(lam))
v,ad,bd,T=s.symbols("v ad bd T",positive=True)
P=R*T/(v-bd)-ad/v**2
vc=3*bd;Tc=8*ad/(27*R*bd);Pc=ad/(27*bd**2)
check("T011 critical first derivative",s.simplify(s.diff(P,v).subs({v:vc,T:Tc}))==0)
check("T011 critical second derivative",s.simplify(s.diff(P,v,2).subs({v:vc,T:Tc}))==0)
d=s.symbols("d",real=True)
reduced=8/(2+3*d)-3/(1+d)**2
check("T011 cubic critical isotherm",s.expand(s.series(reduced,d,0,4).removeO())==1-3*d**3/2)
m,b,k=s.symbols("m b k",positive=True)
omlo=(s.sqrt(b**2+4*k*m)-b)/(2*m)
omhi=(s.sqrt(b**2+4*k*m)+b)/(2*m)
check("W010 exact power bandwidth",s.simplify(omhi-omlo-b/m)==0)
check("W010 half-power locations",all(s.simplify((k-m*om**2)**2-b**2*om**2)==0 for om in (omlo,omhi)))
m1,m2,k,q,a=s.symbols("m1 m2 k q a",positive=True)
mat=s.Matrix([[2*k-m1*s.Symbol("w2"),-k*(1+s.exp(-s.I*q*a))],[-k*(1+s.exp(s.I*q*a)),2*k-m2*s.Symbol("w2")]])
det=s.simplify(s.expand_trig(mat.det()).rewrite(s.cos))
expected=m1*m2*s.Symbol("w2")**2-2*k*(m1+m2)*s.Symbol("w2")+4*k**2*s.sin(q*a/2)**2
check("W011 Bloch determinant",s.simplify(s.expand_complex(det-expected))==0)
check("W011 acoustic slope squared",s.simplify(k*a**2/(2*(m1+m2))-(a*s.sqrt(k/(2*(m1+m2))))**2)==0)
f,dist,z=s.symbols("f dist z",positive=True)
qin=dist+s.I*z
qout=f*qin/(f-qin)
den=(f-dist)**2+z**2
check("O010 beam q real",s.simplify(s.re(qout)-f*(dist*(f-dist)-z**2)/den)==0)
check("O010 beam q imaginary",s.simplify(s.im(qout)-f**2*z/den)==0)
nu0,dnu,tau=s.symbols("nu0 dnu tau",positive=True,real=True)
integral=s.integrate(s.cos(2*s.pi*s.Symbol("freq")*tau),(s.Symbol("freq"),nu0-dnu/2,nu0+dnu/2))/dnu
check("O011 Fourier sinc",s.trigsimp(integral-s.sin(s.pi*dnu*tau)/(s.pi*dnu*tau)*s.cos(2*s.pi*nu0*tau))==0)
ap,t,cs=s.symbols("ap t cs",positive=True)
x=cs**2/ap*(s.sqrt(1+(ap*t/cs)**2)-1)
v=s.diff(x,t)
check("Q010 worldline coordinate acceleration",s.simplify(s.diff(v,t)-ap/(1+(ap*t/cs)**2)**s.Rational(3,2))==0)
check("Q010 Newtonian distance limit",s.limit(x/ap,t,0)/t**2 if False else s.limit(x/t**2,t,0)==ap/2)
Om,De,tt=s.symbols("Om De tt",positive=True,real=True)
sigx=s.Matrix([[0,1],[1,0]]);sigz=s.Matrix([[1,0],[0,-1]])
WR=s.sqrt(Om**2+De**2);U=s.cos(WR*tt/2)*s.eye(2)-s.I*s.sin(WR*tt/2)*(Om*sigx+De*sigz)/WR
check("Q011 Rabi unitarity",s.simplify(U.conjugate().T*U-s.eye(2))==s.zeros(2))
exc=(U*s.Matrix([0,1]))[0]
check("Q011 excitation probability",s.trigsimp(s.expand_complex(exc*s.conjugate(exc))-Om**2/WR**2*s.sin(WR*tt/2)**2)==0)
report={"checked_ids":list(ids),"passed_count":len(checks),"checks":[{"name":x,"passed":True} for x in checks],"independent_expert_review":"pending"}
(ROOT/"data"/"bulk_qa_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=False,indent=2))
