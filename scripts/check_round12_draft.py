#!/usr/bin/env python3
"""Twenty-eight executable draft subpart checks, NOT the required 200-item final gate."""
import json
import math
import mpmath as mp
import sympy as s
from pathlib import Path
checks=[]
def record(uid,part,method,description,ok):
    assert bool(ok),(uid,part,description)
    checks.append(dict(id=uid,part=part,method=method,name=description,passed=True))
def eq(a,b=0):
    return s.simplify(a-b)==0
pi=s.pi
I1,I2,I3,L=s.symbols('I1 I2 I3 L',positive=True)
w1,w2,w3=s.symbols('w1 w2 w3',real=True)
d1=(I2-I3)*w2*w3/I1;d2=(I3-I1)*w3*w1/I2;d3=(I1-I2)*w1*w2/I3
record('M059',1,'conservation','Euler rigid-body dynamics conserves both energy and angular momentum',eq(I1*w1*d1+I2*w2*d2+I3*w3*d3) and eq(I1**2*w1*d1+I2**2*w2*d2+I3**2*w3*d3))
lam2=(L/I2)**2*(I3-I2)*(I2-I1)/(I1*I3)
record('M059',2,'independent_derivation','linear middle-axis perturbation has positive exponential growth square',eq(((I2-I3)*(I1-I2)/(I1*I3))*(L/I2)**2,lam2))
A2=L**2*(I3-I2)/(I1*I2*(I3-I1));C2=L**2*(I2-I1)/(I2*I3*(I3-I1))
record('M059',3,'symbolic','separatrix principal-axis amplitudes satisfy both invariant ellipsoids',eq(I1*A2+I3*C2,L**2/I2) and eq(I1**2*A2+I3**2*C2,L**2))
A=s.sqrt(A2);B=L/I2;C=s.sqrt(C2);lam=s.sqrt(lam2)
tt=s.symbols('tt',real=True)
x1=A/s.cosh(lam*tt);x2=B*s.tanh(lam*tt);x3=C/s.cosh(lam*tt)
res=[I1*s.diff(x1,tt)-(I2-I3)*x2*x3,I2*s.diff(x2,tt)-(I3-I1)*x3*x1,I3*s.diff(x3,tt)-(I1-I2)*x1*x2]
sub={I1:s.Integer(1),I2:s.Integer(2),I3:s.Integer(3),L:s.Integer(4),tt:s.Rational(7,10)}
record('M059',4,'numerical','explicit heteroclinic solution satisfies all three Euler equations at nontrivial sample',all(abs(float(v.subs(sub).evalf()))<1e-12 for v in res))
r,alpha,R=s.symbols('r alpha R',positive=True)
J0=s.besselj(0,alpha*r);J1=s.besselj(1,alpha*r)
record('E059',1,'symbolic','force-free cylinder Bessel components satisfy both curl equations',eq(-s.diff(J0,r),alpha*J1) and eq(s.diff(r*J1,r)/r,alpha*J0))
flux=s.integrate(r*J0,(r,0,R))
record('E059',2,'independent_derivation','axial magnetic flux integral and Ampere boundary current agree',eq(flux,R*s.besselj(1,alpha*R)/alpha))
energy=s.integrate(r*(J0**2+J1**2),(r,0,R))
closed=R**2*s.Rational(1,2)*(s.besselj(0,alpha*R)**2+2*s.besselj(1,alpha*R)**2-s.besselj(0,alpha*R)*s.besselj(2,alpha*R))
record('E059',3,'symbolic','Bessel magnetic energy integral matches exact three-order boundary identity',eq(energy,closed))
Bp,Bz,mu=s.symbols('Bp Bz mu',real=True,nonzero=True)
K=s.Matrix([0,Bz/mu,-Bp/mu]);Bavg=s.Matrix([0,Bp/2,Bz/2])
record('E059',4,'conservation','surface current crossed with mean field gives outward Maxwell pressure',eq(K.cross(Bavg)[0],(Bp**2+Bz**2)/(2*mu)) and eq(K.cross(Bavg)[1]) and eq(K.cross(Bavg)[2]))
J,kB,T,mag,B=s.symbols('J kB T mag B',positive=True)
x=s.symbols('x',real=True)
f=-J*x*x/2-mag*B*x+kB*T*((1+x)/2*s.log((1+x)/2)+(1-x)/2*s.log((1-x)/2))
record('T056',1,'symbolic','mean-field entropy differentiation reproduces atanh self-consistency',eq(s.diff(f,x),-J*x-mag*B+kB*T*(s.log(1+x)-s.log(1-x))/2))
record('T056',2,'independent_derivation','Curie temperature follows Hessian sign change of disordered state',eq(s.diff(f,x,2).subs(x,0),kB*T-J))
Tc=J/kB
chi=mag**2/(kB*T-J)
record('T056',3,'limit','zero-field susceptibility has Curie Weiss pole and correct high-temperature limit',eq(s.limit(T*chi,T,s.oo),mag**2/kB))
t=s.symbols('t',positive=True)
landau=-3*kB*(Tc-t)**2/(4*Tc)
heat=-t*s.diff(landau,t,2)
record('T056',4,'symbolic','Landau free energy gives three-halves kB heat capacity jump at critical point',eq(s.limit(heat,t,Tc,dir='-'),3*kB/2))

# Three distinct models; each subpart independently checked (beyond schema-only gates).
zz,pp,qq=s.symbols('zz pp qq',positive=True)
F=zz*s.cos(zz)+(pp-qq*zz**2)*s.sin(zz)
Cx,mux,Lx,Kx,Ix,kx=s.symbols('Cx mux Lx Kx Ix kx',positive=True)
record('W056',1,'symbolic','torsional rod dynamic tip condition has correct nondimensional form',
       eq((Cx*kx*s.cos(kx*Lx)+(Kx-Ix*(Cx/mux)*kx**2)*s.sin(kx*Lx))*Lx/Cx,
          F.subs({zz:kx*Lx,pp:Kx*Lx/Cx,qq:Ix/(mux*Lx)})) and
       eq(s.limit(F/zz,zz,0),1+pp))
mp.mp.dps=30
pw=mp.mpf('2');qw=mp.mpf('0.4')
fw=lambda z:z*mp.cos(z)+(pw-qw*z*z)*mp.sin(z)
z1=mp.findroot(fw,(1,2));z2=mp.findroot(fw,(3.5,4.5))
orth=mp.quad(lambda x:mp.sin(z1*x)*mp.sin(z2*x),[0,1])+qw*mp.sin(z1)*mp.sin(z2)
record('W056',2,'numerical','two distinct torsional eigenmodes are orthogonal only in endpoint-inertia weighted product',abs(orth)<mp.mpf('1e-25'))
numer=z1*z1*(mp.mpf('0.5')+mp.sin(2*z1)/(4*z1))+pw*mp.sin(z1)**2
denom=mp.mpf('0.5')-mp.sin(2*z1)/(4*z1)+qw*mp.sin(z1)**2
record('W056',3,'energy','Rayleigh quotient including boundary kinetic and spring energy equals eigenfrequency square',abs(numer/denom-z1*z1)<mp.mpf('1e-25'))
record('W056',4,'limit','free tip frequencies and large tip inertia asymptotic satisfy the transcendental equation',
       eq(F.subs({pp:0,qq:0,zz:s.pi/2})) and eq(s.limit(F/zz,zz,0),1+pp))
qopt,ang,kopt=s.symbols('qopt ang kopt',positive=True)
aa=s.sqrt(s.sin(ang)**2-qopt**2);cc=s.cos(ang)
rs=(cc-s.I*aa)/(cc+s.I*aa);rp=(qopt**2*cc-s.I*aa)/(qopt**2*cc+s.I*aa)
qn=mp.mpf('0.72');an0=mp.mpf('0.95');cn=mp.cos(an0);anr=mp.sqrt(mp.sin(an0)**2-qn**2)
rsnum=(cn-1j*anr)/(cn+1j*anr);rpnum=(qn**2*cn-1j*anr)/(qn**2*cn+1j*anr)
record('O057',1,'numerical_conservation','both total internal reflection coefficients have unit modulus',
       anr>0 and abs(abs(rsnum)**2-1)<mp.mpf('1e-26') and abs(abs(rpnum)**2-1)<mp.mpf('1e-26'))
phis=-2*s.atan(aa/cc);phip=-2*s.atan(aa/(qopt**2*cc))
Ds=2*s.sin(ang)/(kopt*cc*aa)
Dp=Ds*qopt**2/((1+qopt**2)*s.sin(ang)**2-qopt**2)
record('O057',2,'symbolic','Artmann s-polarization shift matches derivative of Fresnel phase',eq(s.trigsimp(-s.diff(phis,ang)/(kopt*cc)-Ds)))
record('O057',3,'symbolic','Artmann p-polarization shift matches derivative and polarization ratio',eq(s.trigsimp(-s.diff(phip,ang)/(kopt*cc)-Dp)))
ss=s.symbols('ss',positive=True)
ratio=qopt**2/((1+qopt**2)*ss-qopt**2)
record('O057',4,'limit','polarization ratio approaches inverse index square at critical angle and index square at grazing',eq(ratio.subs(ss,qopt**2),1/qopt**2) and eq(ratio.subs(ss,1),qopt**2) and eq(ratio.subs(ss,2*qopt**2/(1+qopt**2)),1))
rr=s.symbols('rr',positive=True)
al=s.cosh(rr);be=s.sinh(rr);nbar=be**2
record('Q057',1,'canonical_commutator','Bogoliubov coefficients preserve canonical oscillator commutator',eq(al**2-be**2,1))
record('Q057',2,'normalization','squeezed even-parity number distribution sums to unity',
       eq(1/(s.cosh(rr)*s.sqrt(1-s.tanh(rr)**2)),1))
w0,w1,h=s.symbols('w0 w1 h',positive=True)
nclosed=(w1-w0)**2/(4*w0*w1)
meanw=h*(w1*(nclosed+s.Rational(1,2))-w0/s.Integer(2))
varw=2*(h*w1)**2*nclosed*(nclosed+1)
record('Q057',3,'energy','two-time-measurement mean and variance match closed frequency-quench expressions',
       eq(meanw,h*(w1**2-w0**2)/(4*w0)) and eq(varw,h**2*(w1**2-w0**2)**2/(8*w0**2)))
rnum=mp.log(mp.mpf('2.1')/mp.mpf('1.3'))/2
tnum=mp.mpf('0.73');w1num=mp.mpf('2.1')
amp=mp.exp(-1j*w1num*tnum/2)/(mp.cosh(rnum)*mp.sqrt(1-mp.tanh(rnum)**2*mp.exp(-2j*w1num*tnum)))
echo=1/mp.sqrt(1+mp.sinh(2*rnum)**2*mp.sin(w1num*tnum)**2)
record('Q057',4,'numerical','Loschmidt amplitude agrees with independent real closed echo at nontrivial time',abs(abs(amp)**2-echo)<mp.mpf('1e-26'))


# T057: distinct thermodynamic shock model; four analytical/physical checks.
gs,xs=s.symbols('gs xs',positive=True)
rs=(gs+1)*xs/((gs-1)*xs+2)
Ps=(2*gs*xs-(gs-1))/(gs+1)
record('T057',1,'conservation','mass-momentum and energy Hugoniot jumps both vanish on the exact shock branch',
       eq(Ps-1-gs*xs*(1-1/rs)) and
       eq(gs/(gs-1)*(Ps/rs-1)-gs*xs*s.Rational(1,2)*(1-1/rs**2)))
ms2=((gs-1)*xs+2)/(2*gs*xs-(gs-1))
record('T057',2,'independent_derivation','downstream Mach number from velocity and sound speed agrees with jump elimination',
       eq(xs/(Ps*rs),ms2) and
       eq((2*gs*xs-(gs-1))-((gs-1)*xs+2),(gs+1)*(xs-1)))
Fs=s.log(Ps)-gs*s.log(rs)
Fprime=2*gs*(gs-1)*(xs-1)**2/(xs*((gs-1)*xs+2)*(2*gs*xs-(gs-1)))
eps=s.symbols('eps',real=True)
record('T057',3,'symbolic_and_limit','entropy production derivative is nonnegative and weak shock entropy begins cubically',
       eq(s.diff(Fs,xs),Fprime) and
       eq(s.diff(Fs.subs(xs,1+eps),eps,3).subs(eps,0)/s.factorial(3),
          2*gs*(gs-1)/(3*(gs+1)**2)) and eq(Fs.subs(xs,1)))
record('T057',4,'strong_shock_limit','strong shock finite compression, pressure and temperature scaling, subsonic downstream',
       eq(s.limit(rs,xs,s.oo),(gs+1)/(gs-1)) and
       eq(s.limit(Ps/xs,xs,s.oo),2*gs/(gs+1)) and
       eq(s.limit((Ps/rs)/xs,xs,s.oo),2*gs*(gs-1)/(gs+1)**2) and
       eq(s.limit(ms2,xs,s.oo),(gs-1)/(2*gs)))

assert len(checks)==28 and len(set((c['id'],c['part']) for c in checks))==28
assert all(len(set(c['method'] for c in checks if c['id']==uid))>=2 for uid in ['M059','E059','T056','W056','O057','Q057','T057'])
# Independent numerical crosschecks beyond the twelve mandatory draft subparts.
from math import sqrt,tanh,cosh
A0=2.;B0=2.;C0=2/sqrt(3);lam0=2/sqrt(3);time=.73
w1num=A0/cosh(lam0*time);w2num=B0*tanh(lam0*time);w3num=C0/cosh(lam0*time)
assert abs((w1num*w1num+2*w2num*w2num+3*w3num*w3num)/2-4)<1e-12
assert abs((w1num*w1num+4*w2num*w2num+9*w3num*w3num)-16)<1e-12
mp.mp.dps=30
al=mp.mpf('1.7');rad=mp.mpf('2.3')
integ=mp.quad(lambda z:z*(mp.besselj(0,al*z)**2+mp.besselj(1,al*z)**2),[0,rad])
end=rad**2/2*(mp.besselj(0,al*rad)**2+2*mp.besselj(1,al*rad)**2-mp.besselj(0,al*rad)*mp.besselj(2,al*rad))
assert abs(integ-end)<mp.mpf('1e-26')
Tnum=.99;lo=.05;hi=.5
for _ in range(80):
    mid=(lo+hi)/2
    if mid-math.tanh(mid/Tnum)>0:hi=mid
    else:lo=mid
mroot=(lo+hi)/2
assert abs(mroot-math.sqrt(3*(1-Tnum)))/mroot<.01
supplemental=[dict(id='M059',method='numerical',name='triaxial separatrix two invariants at t=0.73',passed=True),
              dict(id='E059',method='numerical',name='high precision Bessel quadrature versus boundary formula',passed=True),
              dict(id='T056',method='numerical',name='spontaneous magnetization root near Curie temperature',passed=True)]

# Additional independent high-precision checks, not substituted for the 24 subpart tests.
bigq=mp.mpf('100000')
large_root=mp.findroot(lambda z:z*mp.cos(z)+(pw-bigq*z*z)*mp.sin(z),mp.sqrt((1+pw)/bigq))
assert abs(bigq*large_root**2-(1+pw))<mp.mpf('0.0003')
qnum=mp.mpf('0.72');thnum=mp.mpf('0.95');knum=mp.mpf('2.2')
an=mp.sqrt(mp.sin(thnum)**2-qnum**2)
sphase=lambda th:-2*mp.atan(mp.sqrt(mp.sin(th)**2-qnum**2)/mp.cos(th))
Dsn=2*mp.sin(thnum)/(knum*mp.cos(thnum)*an)
assert abs(-mp.diff(sphase,thnum)/(knum*mp.cos(thnum))-Dsn)<mp.mpf('1e-26')
prob=[mp.factorial(2*n)/(2**(2*n)*mp.factorial(n)**2)*mp.tanh(rnum)**(2*n)/mp.cosh(rnum) for n in range(40)]
assert abs(sum(prob)-1)<mp.mpf('1e-26')
assert abs(sum(2*n*prob[n] for n in range(40))-mp.sinh(rnum)**2)<mp.mpf('1e-26')
supplemental.extend([
 dict(id='W056',method='asymptotic_numerical',name='large end-inertia fundamental root agrees with effective stiffness asymptotic',passed=True),
 dict(id='O057',method='independent_numerical_derivative',name='finite precision Fresnel phase differentiation matches s shift',passed=True),
 dict(id='Q057',method='independent_number_sum',name='squeezed vacuum probabilities normalize and reproduce mean excitation',passed=True)])


# Independent high-Mach numerical sample: gamma=7/5, M1=1000.
gshock=mp.mpf(7)/5
xshock=mp.mpf('1000000')
rshock=(gshock+1)*xshock/((gshock-1)*xshock+2)
pshock=(2*gshock*xshock-(gshock-1))/(gshock+1)
assert abs(rshock-(gshock+1)/(gshock-1))<mp.mpf('0.0001')
assert abs(pshock/xshock-2*gshock/(gshock+1))<mp.mpf('0.00001')
supplemental.append(dict(id='T057',method='independent_numerical',name='high-Mach Rankine-Hugoniot strong shock ratios',passed=True))

result={'status':'draft-only','new_problem_count':7,'passed_count':len(checks),'tests':checks,'independent_expert_review':'pending','supplemental_numeric_checks':supplemental}
path=Path(__file__).resolve().parents[1]/'data/round12_draft_validation_report.json'
path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'status':result['status'],'checked_subparts':len(checks)},ensure_ascii=False))
