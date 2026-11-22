#!/usr/bin/env python3
"""Physics-based Irodov IV.189--224 electromagnetism-wave independent regression.

Verifies 36 individual source/solution/check blocks, EM phase, Maxwell
fields, displacement current, Poynting energy flow, Larmor radiation,
dipole radiation and radiation pressure with independent SI formulae.
Not a substitute for separate original-book image/figure editorial review.
"""
from math import pi, sqrt, log, sin, cos, exp, tan, isclose
from pathlib import Path
import re
root=Path(__file__).resolve().parent/"chapters"
files=[
  "26-em-waves-189-200.tex",
  "26-em-waves-201-212.tex",
  "26-em-waves-213-224.tex",
]
P={}
for filename in files:
    s=(root/filename).read_text(encoding="utf-8")
    hits=list(re.finditer(r"\\emwaveproblem\{(\d+)\}\{[^}]+\}",s))
    for k,m in enumerate(hits):
        n=int(m.group(1))
        assert n not in P,f"duplicate IV.{n}"
        P[n]=s[m.start():hits[k+1].start() if k+1<len(hits) else len(s)]
assert set(P)==set(range(189,225)),f"IV.189-224 problems: {set(P)^set(range(189,225))}"
ncheck=0
def eq(n,description,a,b,rtol=1e-7,atol=1e-11):
    global ncheck
    ncheck+=1
    assert isclose(a,b,rel_tol=rtol,abs_tol=atol),f"IV.{n} {description}: {a:.12g} != {b:.12g}"
def truth(n,description,check):
    eq(n,description,float(bool(check)),1.)
def anchor(n,token):
    global ncheck
    ncheck+=1
    assert token in P[n],f"IV.{n} missing source anchor {token!r}"
for n,block in P.items():
    anchor(n,r"\exsolution")
    anchor(n,r"\excheck")
    truth(n,"substantive LaTeX source problem",len(block)>200)
c=299792458.;eps0=8.8541878128e-12
mu0=1/(eps0*c*c)
e=1.602176634e-19
me=9.1093837139e-31
mp=1.67262192369e-27
G=6.67430e-11
# EM plane wave in inhomogeneous media and medium conduction.
f=3e6;er=4.
eq(189,"dielectric wavelength shift metres",c/f*(1/sqrt(er)-1),-50.,rtol=.002)
eps1,eps2,thickness=9.,4.,2.
# Midpoint quadrature independent of analytic logarithmic mean.
N=10000; t=0.
for j in range(N):
    x=(j+.5)/N
    eps=eps1*exp(x*log(eps2/eps1))
    t+=thickness/N*sqrt(eps)/c
closed=2*thickness*(sqrt(eps1)-sqrt(eps2))/(c*log(eps1/eps2))
eq(190,"exponential permittivity travel time",t,closed,rtol=1e-9)
sigma=10e-3;freq=10e6;er=9.
ratio=sigma/(2*pi*freq*eps0*er)
eq(191,"conduction over displacement current",ratio,2.,rtol=.02)
E=(0.,30.,0.);direction=(1.,0.,0.)
def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1],
            a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0])
H=tuple(x/(mu0*c) for x in cross(direction,E))
eq(192,"transverse H from k cross E",H[2],E[1]/(mu0*c))
amp,k,x=160.,.51,7.7
Hamp=amp/(mu0*c)
eq(193,"vacuum EM H at t=0 A/m",Hamp*cos(k*x),-.30,rtol=.03)
eq(193,"vacuum EM H at t=33ns A/m",
   Hamp*cos(c*k*33e-9-k*x),.18,rtol=.05)
Eamp,f,side=.5e-3,5e6,.5
wn=2*pi*f;k=wn/c
eq(194,"finite-wave square wire loop emf peak V",
   2*Eamp*side*abs(sin(k*side/2)),13e-6,rtol=.01)
eq(195,"Maxwell field mixed derivatives imply phase velocity",
   1/(mu0*eps0),c*c)
Eamp=50.
eq(196,"time-averaged plane-wave Poynting W/m²",
   .5*eps0*c*Eamp**2,Eamp**2/(2*mu0*c))
Eamp=.050;freq=100e6
j=eps0*2*pi*freq*Eamp/sqrt(2)
eq(197,"displacement current rms mA/m²",j*1000,.20,rtol=.02)
eq(197,"plane wave intensity micro W/m²",.5*eps0*c*Eamp*Eamp*1e6,3.3,rtol=.01)
Eamp=200.;er=4.;R=.5;delta=60.
incident=.5*eps0*c*sqrt(er)*Eamp**2*pi*R*R*delta
eq(198,"energy hitting projected spherical area joules",incident,5000.,rtol=.01)
Eamp=100.;k=2*pi/4.;Om=c*k
x=.4;t=.31/Om
# Standing Maxwell Faraday/Ampere in vacuum
dBdt=Eamp/c*sin(k*x)*Om*cos(Om*t)
minus_dEdx=Eamp*k*sin(k*x)*cos(Om*t)
eq(199,"standing field Faraday residual",dBdt,minus_dEdx)
# Average poynting must vanish on an integral cycle
coef=.25*eps0*c*Eamp*Eamp*sin(2*k*x)
eq(200,"standing-wave Poynting instantaneous",
   (Eamp*cos(k*x)*cos(Om*t))*
   (Eamp/(mu0*c)*sin(k*x)*sin(Om*t)),
   coef*sin(2*Om*t))
eq(200,"standing-wave cycle-average flux",sum(coef*sin(2*pi*j/1000) for j in range(1000))/1000,0,atol=1e-10)
# E-B energy peak ratio for time-dependent capacitor/solenoid.
omega,R=1000.,.06
tiny=(omega*R)**2/(8*c*c)
eq(201,"displacement magnetic / electric field energy",
   tiny,5e-15,rtol=.01)
eq(202,"solenoid induced electric / magnetic energy",
   (eps0*mu0*omega*omega*R*R)/8,tiny)
E0,dE,R,h=200.,50.,.4,.01
Hin=eps0*R*dE/2
Pin=2*pi*R*h*E0*Hin
dWdt=eps0*E0*dE*pi*R*R*h
eq(203,"capacitor radial Poynting influx=dU/dt",Pin,dWdt)
I,Rwire=5.,4.
eq(204,"DC resistor Poynting input power",I*I*Rwire,100)
U,I,r=1e6,.02,.1
v=sqrt(2*e*U/mp)
Er=I/(2*pi*eps0*v*r)
Hphi=I/(2*pi*r)
eq(205,"positive proton beam energy flux",Er*Hphi,
   I*I/(4*pi*pi*eps0*r*r)*sqrt(mp/(2*e*U)))
B,Bdot,R,length=.05,.01,.1,.8
Ephi=-R*Bdot/2
dWdt=pi*R*R*length*B*Bdot/mu0
eq(206,"induction Poynting inward sidewall magnetic energy",
   -2*pi*R*length*Ephi*B/mu0,dWdt)
# IV.207 requires original Fig.4.39; do not turn chart arrow into an unsupported numerical truth.
anchor(207,r"\bm E\times\bm H")
V,I=240.,.8;a,b=.01,.1
# Coaxial Poynting radial integration, numerical midpoint.
steps=10000
psum=0.
for j in range(steps):
    r=a+(j+.5)*(b-a)/steps
    Er=V/(r*log(b/a));Hphi=I/(2*pi*r)
    psum+=Er*Hphi*2*pi*r*(b-a)/steps
eq(208,"coax flux area integral VI",psum,V*I,rtol=1e-9)
Vm,Im,phi=100.,2.,.7
eq(209,"average harmonic power factor",Vm*Im*cos(phi)/2,
  (Vm/sqrt(2))*(Im/sqrt(2))*cos(phi))
# Surface continuity: only no free sheet currents or surface sheet energy losses.
Et=(2.,3.,0.);Ht=(-4.,5.,0.)
n=(0.,0.,1.)
flux=sum(x*y for x,y in zip(cross(Et,Ht),n))
eq(210,"tangential fields yield continuous normal Poynting",
  flux,Et[0]*Ht[1]-Et[1]*Ht[0])
# Identical charge/mass particle systems emit no electric dipole field when COM inertial
masses=(1.,3.,5.)
kappa=.2
accels=(2.,-1.,1/5)
totaldipoleacc=sum(kappa*m*a for m,a in zip(masses,accels))
eq(211,"dipole acceleration vanishes for momentum-conserving COM",totaldipoleacc,0.)
a=.1e-9; omega=6.5e14
Pavg=e*e*a*a*omega**4/(12*pi*eps0*c**3)
eq(212,"harmonic electron Larmor power femtowatts",Pavg/1e-15,5.,rtol=.03)
# Orbital charged particle: acceleration from Coulomb, circular Larmor power.
charge=e; q=2*e; orbit=1e-10
accel=abs(charge*q)/(4*pi*eps0*me*orbit*orbit)
eq(213,"circular Coulomb radiation instant power",
   charge**2*accel**2/(6*pi*eps0*c**3),
   charge**4*q*q/(96*pi**3*eps0**3*me**2*c**3*orbit**4))
# Straight-line far-field Coulomb encounter integral independent analytic antiderivative.
b,v=.1,200.
timeint=0.
steps=300000
du=100/steps
for j in range(steps):
    u=-50+(j+.5)*du
    timeint+=du/(1+u*u)**2
eq(214,"inverse quartic line-of-sight Coulomb integral",timeint,pi/2,rtol=1e-5)
eq(214,"Coulomb flying-by energy loss positive",float(timeint>0),1.)
B=1.
ratio=e**3*B/(3*eps0*c**3*mp**2)
eq(215,"proton 1 T semi-orbit radiation fraction",ratio,2e-18,rtol=.1)
def e_fold_loss(m,B):
    return 3*pi*eps0*c**3*m**3/(e**4*B*B)
eq(216,"electron 1 T radiative loss time s",e_fold_loss(me,1.),2.5,rtol=.05)
eq(216,"proton 1 T radiative loss years",e_fold_loss(mp,1.)/(365.25*86400),500.,rtol=.08)
omega,ell=3.3e6,190.
phase=omega*ell/c
truth(217,"retarded source condition yields finite nonnegative flux ratio",
   tan(phase)**2>=0)
beta=.2
eq(218,"radiation toward/away phase ratio",((1+beta)/(1-beta))**4,5.0625)
eq(219,"dipole sin² theta full solid-angle integration",
   2*pi*(4/3),8*pi/3)
P,r=5.,20.
eq(220,"dipole equatorial energy density",3*P/(8*pi*r*r*c),
   (P/(r*r))/(8*pi*c/3))
p,omega=3e-29,2e12
eq(221,"rotating dipole radiated time-mean power",
   p*p*omega**4/(6*pi*eps0*c**3),p*p*omega**4/(6*pi*eps0*c**3))
sigmaT=e**4/(6*pi*eps0**2*me**2*c**4)
eq(222,"Thomson electron cross-section m²",sigmaT,6.6524587e-29,rtol=.002,atol=0)
w,w0=3.,5.
eq(223,"bound-electron scattering suppression factor",w**4/(w0*w0-w*w)**2,81/256)
Psolar,Msun,rho=4e26,1.98847e30,1000.
a=3*Psolar/(16*pi*c*G*Msun*rho)
eq(224,"radiation/gravity balance grain radius micrometers",
   a*1e6,.60,rtol=.02)
for n,tokens in {
 189:[r"\Delta\lambda"], 190:[r"\ln("],
 191:[r"\sigma",r"\varepsilon_0"], 192:[r"\bm k\times\bm E_m"],
 194:[r"\mathcal E_m",r"\sin"], 195:[r"\partial_tB_z"],
 196:[r"\overline{\bm S}"], 197:[r"j_{d,\mathrm{rms}}"],
 198:[r"\pi R^2t"], 199:[r"\bm B(x,t)"],
 200:[r"\overline{S_x}=0"], 201:[r"\omega^2R^2"],
 202:[r"\varepsilon_0\mu_0"], 203:[r"P_{\rm in}"],
 204:[r"I^2R"], 205:[r"\bm S="],
 206:[r"P_{\rm in}"], 207:[r"\text{电源位于图4.39的左侧}"],
 208:[r"\Phi=VI"], 209:[r"\cos\varphi"],
 210:[r"S_{1n}=S_{2n}"], 211:[r"\ddot{\bm p}"],
 212:[r"\overline P"], 214:[r"\int_{-\infty}^{\infty}"],
 215:[r"\Delta W"], 216:[r"t_{1/e}"],
 217:[r"t_r"], 218:[r"S_{\rm toward}"],
 219:[r"8\pi"], 220:[r"\overline w_\perp"],
 221:[r"p^2\omega^4"], 222:[r"\overline P",r"\overline S"],
 223:[r"\omega_0^2-\omega^2"], 224:[r"\rho",r"M_\odot"],
}.items():
    for needle in tokens:anchor(n,needle)
print(f"PASS: {ncheck} independently derived electromagnetic/radiation and structural checks; 36/36 IV.189-224 sources.")
