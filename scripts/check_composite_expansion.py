#!/usr/bin/env python3
"""独立于题解文本的二批综合题符号/数值检验；技术检查不是专家审稿。"""
import json
from pathlib import Path
import sympy as s
p=Path(__file__).resolve().parents[1]
data={x["id"]:x for x in json.loads((p/"data/problems.json").read_text(encoding="utf-8"))}
required=("M009","E009","T009","W009","O009","Q009")
assert all(i in data for i in required)
checks=[]
def claim(label, ok):
    assert bool(ok),label
    checks.append(label)
m,L,k,alpha,r=s.symbols("m L k alpha r",positive=True)
A=L**2/m+alpha
U=A/(2*r**2)-k/r
r0=A/k
claim("M009 circular equation",s.simplify(s.diff(U,r).subs(r,r0))==0)
claim("M009 stable curvature",s.simplify(s.diff(U,r,2).subs(r,r0)-k/r0**3)==0)
claim("M009 angular ratio",s.simplify((L/(m*r0**2))**2/(k/(m*r0**3))-L**2/(L**2+m*alpha))==0)
a,w,f,t=s.symbols("a w f t",positive=True,real=True)
lam=a+s.I*w
vel=f*(1-s.exp(-lam*t))/lam
claim("E009 full transient",s.simplify(s.diff(vel,t)+lam*vel-f)==0)
vx=f*a/(a*a+w*w);vy=-f*w/(a*a+w*w)
claim("E009 steady energy",s.simplify(f*vx-a*(vx*vx+vy*vy))==0)
P0,st,V0,Cv,R,n,Ti,x=s.symbols("P0 st V0 Cv R n Ti x",positive=True)
c=Cv/R
a2=st*(c+s.Rational(1,2));a1=P0*(c+1)+c*st*V0;a0=c*P0*V0-n*Cv*Ti
Tf=(P0+st*x)*(V0+x)/(n*R)
equ=s.expand(n*Cv*Tf+P0*x+st*x*x/2-n*Cv*Ti)
claim("T009 equilibrium polynomial",s.simplify(equ-(a2*x*x+a1*x+a0))==0)
Tcurve=Ti-(P0*x+st*x*x/2)/(n*Cv)
S=n*Cv*s.log(Tcurve/Ti)+n*R*s.log((V0+x)/V0)
claim("T009 entropy slope",s.simplify(s.diff(S,x)-((n*R*Tcurve/(V0+x))-(P0+st*x))/Tcurve)==0)
kap=s.symbols("kap",positive=True)
Mat=s.Matrix([[k+kap,-kap,0],[-kap,k+2*kap,-kap],[0,-kap,k+kap]])
modes=[(s.Matrix([1,1,1]),k),(s.Matrix([1,0,-1]),k+kap),(s.Matrix([1,-2,1]),k+3*kap)]
for j,(vec,ev) in enumerate(modes):
    claim(f"W009 mode {j}",Mat*vec==ev*vec)
claim("W009 total modal energy",s.simplify(k/6+(k+kap)/4+(k+3*kap)/12-(k+kap)/2)==0)
rr,delta=s.symbols("rr delta",positive=True,real=True)
airy=(1-rr)**2/((1-rr)**2+4*rr*s.sin(delta/2)**2)
claim("O009 resonance unit transmission",s.simplify(airy.subs(delta,2*s.pi)-1)==0)
claim("O009 half maximum R=.5",s.simplify(airy.subs({rr:s.Rational(1,2),delta:2*s.asin(s.Rational(1,2)/(2*s.sqrt(s.Rational(1,2))))})-s.Rational(1,2))==0)
th,phi=s.symbols("th phi",real=True)
nplus=s.Matrix([s.cos(th/2),s.sin(th/2)])
U=s.diag(s.exp(s.I*phi/2),s.exp(-s.I*phi/2))
xplus=s.Matrix([1,1])/s.sqrt(2)
prob=s.trigsimp(s.expand_complex((xplus.conjugate().T*U*nplus)[0]*s.conjugate((xplus.conjugate().T*U*nplus)[0])))
claim("Q009 selected measurement",s.trigsimp(prob-(1+s.sin(th)*s.cos(phi))/2)==0)
Z=s.diag(1,-1)
In=s.eye(2)
sigx=s.Matrix([[0,1],[1,0]])
N=s.sin(th)*sigx+s.cos(th)*Z
Pp=(In+N)/2;Pm=(In-N)/2
rho=s.diag(1,0)
deph=Pp*rho*Pp+Pm*rho*Pm
claim("Q009 nonselective Bloch vector",all(s.trigsimp(v)==0 for v in (deph-(In+s.cos(th)*N)/2)))
report={"added_ids":list(required),"checks":checks,"passed_count":len(checks),"status":"机器交叉校验通过；独立专家复核未完成"}
(p/"data"/"composite_expansion_validation.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=False,indent=2))
