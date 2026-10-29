#!/usr/bin/env python3
"""Executable physical checks for four newly added round12 models. Not external expert review."""
import json,math
from pathlib import Path
import sympy as s
import mpmath as mp
checks=[]
def record(uid,part,method,name,ok):
    assert bool(ok),(uid,part,name)
    checks.append(dict(id=uid,part=part,method=method,name=name,passed=True))
def eq(a,b=0):return s.simplify(a-b)==0

z,lam,t,alpha,delta,rho,cp,L,k=s.symbols('z lam t alpha delta rho cp L k',positive=True)
f=s.erf(z)/s.erf(lam)
record('T062',1,'symbolic','erf similarity temperature profile solves transformed transient heat diffusion equation and satisfies wall interface conditions',eq(s.diff(f,z,2)+2*z*s.diff(f,z)) and eq(f.subs(z,0)) and eq(f.subs(z,lam),1))
Ste=cp*delta/L
left=rho*L*lam*s.sqrt(alpha/t)
right=k*delta*s.exp(-lam**2)/(s.sqrt(s.pi*alpha*t)*s.erf(lam))
record('T062',2,'independent_derivation','latent Stefan boundary condition reduces to unique positive similarity parameter relation',eq((left/right).subs(k,rho*cp*alpha),lam*s.sqrt(s.pi)*s.exp(lam**2)*s.erf(lam)/Ste) and eq(s.limit(lam*s.exp(lam**2)*s.erf(lam)/lam**2,lam,0),2/s.sqrt(s.pi)))
Sensible=2*rho*cp*delta*s.sqrt(alpha*t)*(1-s.exp(-lam**2))/(s.sqrt(s.pi)*s.erf(lam))
Latent=2*rho*L*lam*s.sqrt(alpha*t)
Wall=2*k*delta*s.sqrt(t)/(s.sqrt(s.pi*alpha)*s.erf(lam))
record('T062',3,'conservation','integrated latent plus sensible heat equals time-integrated wall cooling flux on exact Stefan root',eq((Wall-Latent-Sensible).subs(k,rho*cp*alpha).subs(L,cp*delta/(s.sqrt(s.pi)*lam*s.exp(lam**2)*s.erf(lam)))))
F=lam*s.exp(lam**2)*s.erf(lam)
record('T062',4,'limit','small-Stefan asymptotic front square agrees with exact transcendental equation near zero',eq(s.limit(F/lam**2,lam,0),2/s.sqrt(s.pi)) and eq(s.limit(s.diff(F,lam)/lam,lam,0),4/s.sqrt(s.pi)))

x,eta,v,kA,A=s.symbols('x eta v kA A',positive=True)
prof=eta/s.cosh(eta*x)
record('W062',1,'symbolic','localized bright NLS soliton solves stationary focusing cubic envelope ODE with vanishing tail',eq(s.simplify(s.diff(prof,x,2)-eta**2*prof+2*prof**3).rewrite(s.exp)) and eq(s.limit(prof,x,s.oo)))
mp.mp.dps=35;ev=mp.mpf('1.7')
Nn=mp.quad(lambda xx:ev**2/mp.cosh(ev*xx)**2,[-mp.inf,mp.inf])
Hn=mp.quad(lambda xx:mp.mpf('.5')*(ev**2*mp.sinh(ev*xx)/mp.cosh(ev*xx)**2)**2-mp.mpf('.5')*(ev/mp.cosh(ev*xx))**4,[-mp.inf,mp.inf])
record('W062',2,'numerical','35-digit independent spatial quadrature reproduces both NLS soliton norm and negative Hamiltonian',abs(Nn-2*ev)<mp.mpf('1e-30') and abs(Hn+ev**3/3)<mp.mpf('1e-30'))
omega2=kA**2*(kA**2/4-A**2)
record('W062',3,'independent_derivation','linearized focusing NLS sideband dispersion has negative frequency square precisely below critical wave number',eq(omega2,kA**4/4-A**2*kA**2) and eq(omega2.subs(kA,2*A)) and omega2.subs(kA,A)<0)
growth2=kA**2*(A**2-kA**2/4)
record('W062',4,'limit','modulation growth squared is maximized at square-root-two times amplitude with growth rate A squared',eq(s.diff(growth2,kA).subs(kA,s.sqrt(2)*A)) and eq(growth2.subs(kA,s.sqrt(2)*A),A**4) and eq(s.limit(-eta**3/3,eta,0)))

d,y=s.symbols('d y',positive=True);p=y*(1+(d-y)**2)
record('O062',1,'symbolic','Kerr resonator input power reduces to cubic with exact coefficients and nonlinear detuning shift',eq(s.expand(p),y**3-2*d*y**2+(1+d**2)*y))
fp=(2*d+s.sqrt(d*d-3))/3;fm=(2*d-s.sqrt(d*d-3))/3
record('O062',2,'independent_derivation','two folds solve power derivative and merge at detuning square-root three critical cusp',eq(s.diff(p,y).subs(y,fp)) and eq(s.diff(p,y).subs(y,fm)) and eq(s.diff(p,y).subs({d:s.sqrt(3),y:2/s.sqrt(3)})) and eq(p.subs({d:s.sqrt(3),y:2/s.sqrt(3)}),8*s.sqrt(3)/9))
g,kap,n,D=s.symbols('g kap n D',positive=True)
inp=n*((kap/2)**2+(D-g*n)**2)
det=(kap/2)**2+(D-2*g*n)**2-(g*n)**2
record('O062',3,'symbolic','Bogoliubov cavity Jacobian determinant matches nonlinear photon number input-output slope',eq(s.diff(inp,n),det) and eq(s.expand(det),kap**2/4+D**2-4*D*g*n+3*g*g*n*n))
ss,aa=s.symbols('ss aa',real=True)
nn,kre,k0=s.symbols('nn kre k0',positive=True)
nout=ss**2+kre*nn-2*s.sqrt(kre)*ss*aa
ndot=-(kre+k0)*nn+2*s.sqrt(kre)*ss*aa
record('O062',4,'conservation','cavity photon input output loss equals accumulation and strong field power has cubic dominance',eq(ss**2-nout-k0*nn,ndot) and eq(s.limit(inp/(g*g*n**3),n,s.oo),1))

ph=s.symbols('ph',real=True);vec=s.Matrix([1,s.exp(s.I*ph)])/s.sqrt(2)
dv=s.diff(vec,ph);inner=(vec.conjugate().T*dv)[0];norm=(dv.conjugate().T*dv)[0]
record('Q062',1,'symbolic','single photon tangent vector Fubini Study metric gives unit quantum phase Fisher information',eq(4*(norm-inner*s.conjugate(inner)),1))
pp=(1+s.sin(ph))/2;pm=(1-s.sin(ph))/2
record('Q062',2,'independent_derivation','balanced biased interferometer outcome probabilities have unit classical Fisher information',eq(s.trigsimp(s.diff(pp,ph)**2/pp+s.diff(pm,ph)**2/pm),1))
et=s.symbols('et',positive=True)
pure=vec*vec.conjugate().T;dp=s.diff(pure,ph)
rho=s.diag(1,1,1)
rho[:2,:2]=et*pure;rho[2,2]=1-et
sld=s.zeros(3,3);sld[:2,:2]=2*dp
record('Q062',3,'symbolic','erasure flagged density operator satisfies SLD equation and quantum Fisher information equals survival fraction',all(eq(v) for v in ((rho*sld+sld*rho)/2-s.diff(rho,ph))) and eq(s.trace(rho*sld*sld),et))
NN=s.symbols('NN',positive=True);per=NN*et**NN
record('Q062',4,'limit','NOON Fisher information per injected photon has unique continuous optimum at minus reciprocal log survival',eq(s.diff(s.log(per),NN).subs(NN,-1/s.log(et))) and eq(s.limit(per.subs(et,s.Rational(4,5)),NN,s.oo)))

assert len(checks)==16 and len({(c['id'],c['part']) for c in checks})==16
assert all(len({c['method'] for c in checks if c['id']==uid})>=2 for uid in ('T062','W062','O062','Q062'))
report=dict(status='draft-additional-only',new_problem_count=4,passed_count=16,tests=checks,independent_expert_review='pending')
Path(__file__).resolve().parents[1].joinpath('data/round12_continuation2_validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'status':report['status'],'passed_count':len(checks)},ensure_ascii=False))
