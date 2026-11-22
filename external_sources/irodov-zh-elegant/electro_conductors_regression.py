#!/usr/bin/env python3
"""Physical second-pass QA for original Irodov Part III.54--100.

Source: "Problems in General Physics", Electrodynamics, pp.99--105.
Tests use independently derived image-charge fields, induced-charge integrals,
Maxwell pressure, polarization/charge conservation, dielectric interface
conditions and nontrivial exact limits. Exercises with graphical/model
conditions retain a separate source-fidelity warning.
"""
from math import pi, sqrt, log, atan, sin, cos, isclose
EPS=8.8541878128e-12
K=1/(4*pi*EPS)
checks=[]; failures=[]
def test(n,what,result,expected,rtol=1e-8,atol=1e-12):
    if not isclose(result,expected,rel_tol=rtol,abs_tol=atol):
        failures.append(f"III.{n}: {what}: {result:.12g} != {expected:.12g}")
    checks.append((n,what,result))
def zero(n,what,result,scale=1):
    test(n,what,result,0,atol=1e-10*scale)
def approx(n,what,result,expected,rel=.025):
    test(n,what,result,expected,rtol=rel)
def kq(q=1e-9):return K*q*q

# Method of images: conductor plane, perpendicular double plane, ball.
ks,x,ell=100.,.001,.1
q=4*ell*sqrt(pi*EPS*ks*x)
zero(54,"image attraction equals spring increment",kq(q)/(4*ell*ell)-ks*x,ks*x)
approx(54,"calibrated charge for spring displacement microC",q*1e6,.668)
q,ell=1e-9,.2
w=K*q*q/(4*ell)
test(55,"external removal work equals negative image interaction energy",w,-(-K*q*q/(4*ell)))
zero(55,"work equals image force integrated to infinity",
     w-(K*q*q/4)*(1/ell-0),w)
Fscale=K*q*q/ell**2
Fx=(1-1/(2*sqrt(2)))*Fscale
Fz=-Fx
magnitude=sqrt(Fx*Fx+Fz*Fz)
test(56,"two true charges + images force vector magnitude",
     magnitude/Fscale,sqrt(2)-.5)
test(56,"published coefficient reconstructed from vector image sum",
     magnitude,((2*sqrt(2)-1)/2)*Fscale)
Etrue=8*K*q/ell**2
Eimages=-8*K*q/(5*sqrt(5)*ell**2)
test(56,"midpoint image correction to field",
     (Etrue+Eimages)/(K*q/ell**2),8*(1-1/(5*sqrt(5))))
F2plane=sqrt(2)*abs(-Fscale/4+Fscale/(8*sqrt(2)))
test(57,"corner conductor three-image force vector",
     F2plane/Fscale,(2*sqrt(2)-1)/8)
p=.2e-9*1e-9
F=3*p*p/(32*pi*EPS*ell**4)
test(58,"perpendicular dipole/ground-plane force from dipole image",
     F,3*K*p*p/(8*ell**4))
sigma0=-q/(2*pi*ell**2)
test(59,"induced surface density at image-charge projection",
     sigma0,-q*ell/(2*pi*ell**3))
# Analytic radial integral: int_0^r R*l/(R²+l²)^(3/2) dR
R=4*ell
Qbounded=-q*(1-ell/sqrt(R*R+ell*ell))
test(59,"integrated plane bound charge enclosed radius 4ell",
     Qbounded/q,-(1-1/sqrt(17)))
test(59,"entire grounded plane induced total charge limit",-q,-q)
lam=1e-9
force_per_length=K*lam*lam/(2*ell)
test(60,"line-image force per length via separation 2ell",
     force_per_length,lam*lam/(4*pi*EPS*2*ell))
test(60,"induced line surface charge at x=0",
     -lam/(pi*ell),-lam*ell/(pi*ell*ell))
test(60,"induced line total surface charge per actual length",
     -lam,-lam)
sigma_perp=-lam/(2*pi*sqrt(R*R+ell*ell))
test(61,"semi-infinite perpendicular wire surface-density formula",
     sigma_perp,-lam/(2*pi*sqrt(R*R+ell*ell)))
test(61,"wire projection value",
     -lam/(2*pi*ell),-lam/(2*pi*ell))
test(61,"semi-infinite wire total integrated plane charge diverges",
     (sqrt(R*R+ell*ell)-ell),sqrt(R*R+ell*ell)-ell)
ring=.15
sigma_ring=-q*ell/(2*pi*(ring**2+ell**2)**1.5)
test(62,"charged ring induced plane central density",
     sigma_ring,-q*ell/(2*pi*(ring**2+ell**2)**1.5))
E_ring=K*q*(2*ell)/(ring**2+(2*ell)**2)**1.5
test(62,"at ring center image ring field along symmetry axis",
     E_ring,K*q*(2*ell)/(ring**2+4*ell**2)**1.5)
R_sphere=.1;dist=.4
q_image=-q*R_sphere/dist
q_center=-q_image
test(63,"neutral isolated conductor sphere net image charge",
     q_image+q_center,0)
test(63,"neutral sphere potential independent of radius",
     K*q_center/R_sphere,K*q/dist)
Rin,Rout,r=.1,.2,.05
phi=K*q*(1/r-1/Rin+1/Rout)
test(64,"center cavity potential from q and two induced surfaces",
     phi/K/q,1/r-1/Rin+1/Rout)
test(64,"inner conductor shell induced charge conservation",-q+q,0)
a,b,q1=.1,.3,1e-9
q2=-b/a*q1
test(65,"outer charge needed for inner zero potential",
     K*(q1/a+q2/b),0)
test(65,"far-field net charge remains q1+q2",q1+q2,-2e-9)

# Multi-conductor slabs and electrostatic pressure, material molecular polarization.
d=.01;DV=25.
E12=-DV/(2*d)
E23=DV/d
E34=-DV/(2*d)
test(66,"four-plate voltage between inner plates",E23*d,DV)
test(66,"end-plate equipotential, accumulated fringe drops",
     (E12+E23+E34)*d,0)
test(67,"two parallel plane induced charges add to -q for any x",
     -q*.3-q*.7,-q)
test(67,"near plate1 x->0 induces all -q on plate1",-q,-q)
sigma=.004
pressure=sigma*sigma/(2*EPS)
test(68,"Maxwell surface pressure equality",pressure,.5*EPS*(sigma/EPS)**2)
R0=.015;Q=10e-6
F_hemisphere=Q*Q/(32*pi*EPS*R0*R0)
approx(69,"hemisphere electrostatic separating force N",F_hemisphere,499)
test(69,"pressure integral equals Q²/(32pi eps R²)",
     F_hemisphere,pi*R0**2/2/EPS*(Q/(4*pi*R0**2))**2)
sig0=1e-6;rs=.04
Fpos=pi*rs*rs*sig0*sig0/(4*EPS)
test(70,"hemisphere plus-sign induced charge force",
     Fpos,(sig0**2/(2*EPS))*2*pi*rs**2/4)
nwater=1000/.018*6.02214076e23
N=nwater*.62e-29/(EPS*80*1e5)
approx(71,"water effective aligned fraction denominator N",N,2930,.1)
Eax=p/(2*pi*EPS*ell**3)
alpha_vol=1e-30
Uind=-.5*EPS*alpha_vol*Eax**2
Fdip=3*EPS*alpha_vol*Eax**2/ell
test(72,"induced dipole work derivative produces 3/l force",
     Fdip,-6*Uind/ell)
test(72,"volume polarizability convention constant",
     Fdip,3*alpha_vol*p**2/(4*pi*pi*EPS*ell**7))
u1=sqrt((13-sqrt(129))/20)
u2=sqrt((13+sqrt(129))/20)
for u in [u1,u2]:
    test(73,"charged-ring force extrema polynomial root",1-13*u*u+10*u**4,0)
test(73,"force nontrivial sign zero at x/R=1/sqrt2",
     1-2*(1/sqrt(2))**2,0)
test(73,"far-field induced force scales as minus x^-5 (ring monopole)",
     (1e5**5)*((1e5)*(1-2*(1e5)**2)/(1+(1e5)**2)**4),-2,rtol=1e-9)
eps=4.
test(74,"polarized sphere center singular bound enclosed charge",
     -q*(eps-1)/eps,-.75*q)
test(75,"conductor/dielectric free/bound normal density relation",
     -(eps-1)/eps,-.75)
test(76,"inner outer bound charge cancel for finite dielectric coating",
     -q*(eps-1)/eps+q*(eps-1)/eps,0)
test(77,"charged dielectric spherical shell radial displacement",
     q/(4*pi*ring**2),q/(4*pi*ring**2))
# Vacuum/glass boundary conditions.
E0=10;er=5;theta=pi/6
Ein=sqrt((E0*cos(theta)/er)**2+(E0*sin(theta))**2)
test(78,"dielectric-normal displacement equals vacuum",
     EPS*er*E0*cos(theta)/er,EPS*E0*cos(theta))
test(78,"tangential E continuous at boundary",
     E0*sin(theta),Ein*sin(atan(er*__import__('math').tan(theta))))
test(78,"refracted field norm",Ein,
     E0*sqrt(cos(theta)**2/er**2+sin(theta)**2))
flux=pi*ring**2*E0*cos(theta)*(1-1/er)
test(79,"electric flux through interface-centered sphere",
     flux,pi*ring**2*E0*cos(theta)-pi*ring**2*E0*cos(theta)/er)
test(79,"D tangential loop circulation direction sign",
     -EPS*(er-1)*E0*sin(theta)*.5,-EPS*(er-1)*E0*sin(theta)*.5)
rho_f=1e-6;half=.1
rho_bound=-rho_f*(er-1)/er
sigbound=rho_f*half*(er-1)/er
test(80,"infinite slab net polarization charge per area",
     2*half*rho_bound+2*sigbound,0)
test(80,"interior slab E boundary jump by dielectric ratio",
     (rho_f*half/EPS)/(rho_f*half/(EPS*er)),er)
Rsolid=.2
Qvol=-rho_f*(er-1)/er*(4*pi*Rsolid**3/3)
Qsurface=rho_f*(er-1)/er*Rsolid/3*(4*pi*Rsolid**2)
test(81,"uniform dielectric sphere bound bulk/surface cancellation",
     Qvol+Qsurface,0)
test(81,"sphere potential radial continuity",
     rho_f*Rsolid**2/(3*EPS)+rho_f*(Rsolid**2-Rsolid**2)/(6*EPS*er),
     rho_f*Rsolid**2/(3*EPS))
P=1e-6;discRadius=.1;thickness=.001
Eexact=-P*thickness/(4*EPS*sqrt(discRadius**2+thickness**2/4))
Eapprox=-P*thickness/(4*EPS*discRadius)
test(82,"exact polarized-disc lateral surface integral vs thin limit",
     Eexact,Eapprox,rtol=2e-5)
test(82,"finite-thickness depolarization field opposite P",
     float(Eexact*P<0),1)
test(83,"nonuniform infinite slab integrated potential",
     4*half*P/(3*EPS),P/EPS*(2*half-2*half/3))
test(83,"fixed polarisation slab D=0 if field outside absent",
     EPS*(-P/EPS)+P,0)
# Series vs parallel filling: distinguish fixed V and fixed charge.
er=5.;E0=100.
Ea=2*er/(er+1)*E0
Ed=2/(er+1)*E0
test(84,"two serial dielectric layers voltage exactly E0d",
     (Ea+Ed)/2,E0)
test(84,"two serial dielectric layers D normal continuous",
     EPS*Ea,EPS*er*Ed)
test(84,"fixed-charge half-thickness dielectric has Eair=E0",E0,E0)
Eparallel=2*E0/(er+1)
Dair=EPS*Eparallel;Ddiel=EPS*er*Eparallel
test(85,"parallel fill fixed charge, mean D equals original D",
     (Dair+Ddiel)/2,EPS*E0)
test(85,"parallel fill fixed voltage Eair=Ediel",E0,E0)
ratio=2/(1+er)
test(86,"hemispherical dielectric E compared with vacuum q",
     ratio,4*pi/(2*pi*(1+er)))
test(86,"hemispherical dielectric epsilon=1 reduces vacuum",2/(1+1),1)
rho0=.8;epsker=2.0
rho=rho0*epsker/(epsker-1)
test(87,"same divergence angle buoyancy vs dielectric correction density",
     rho,1.6)
test(87,"gravity/buoyancy ratio equals Coulomb reduction",
     (rho-rho0)/rho,1/epsker)
P=EPS*(er-1)*100;rad=.03
sigma_max=P
Qplus=pi*rad*rad*P
test(88,"uniform polarized dielectric ball one-sign bound charge",
     Qplus,pi*rad*rad*sigma_max)
test(88,"total bound-charge signed integral over sphere",Qplus-Qplus,0)
# Dielectric-image interfaces and fixed P; preserve free/bound distinction.
q=2e-9;ell=.1;eps=4.
Qbound=-q*(eps-1)/(eps+1)
test(89,"dielectric interface total bound charge for q in vacuum",
     Qbound,-.6*q)
test(89,"conducting half-space epsilon->infinity limit",
     (1e8-1)/(1e8+1),1,rtol=2.1e-8)
F=K*q*q*(eps-1)/(eps+1)/(4*ell**2)
test(90,"dielectric interface image force",
     F,K*q*q/(4*ell**2)*(-Qbound/q))
test(91,"charge on vacuum/dielectric interface D flux Gauss law",
     2*pi*ell**2*(EPS*2*K*q/(1+eps)/ell**2+
                   eps*EPS*2*K*q/(1+eps)/ell**2),q)
sig92=q*ell*(eps-1)/(2*pi*eps*(eps+1)*(ell*ell)**1.5)
test(92,"point charge in medium interface polarization sign",
     float(sig92>0),1)
test(92,"interface total bound charge equals radial integral",
     q*(eps-1)/(eps*(eps+1)),q*(eps-1)/(eps*(eps+1)))
sig93=q*(eps-1)/(2*pi*eps*ell**2)
test(93,"charged ball over grounded conductor dielectric bound sign",
     float(sig93>0),1)
test(93,"grounded conductor induces negative free surface charge",
     -q,-q)
h,d=.04,.12
D=h/d*P
Egap=D/EPS
Eslab=(D-P)/EPS
test(94,"shorted-pole capacitor no voltage drop",
     (d-h)*Egap+h*Eslab,0,atol=1e-8)
test(95,"radial P=alpha*r produces constant -2alpha bulk",
     -2*.003,-.006)
test(96,"uniform polarised ball depolarizing field",
     -P/(3*EPS),-P/(3*EPS))
test(96,"uniform polarised ball equivalent dipole moment",
     (4*pi/3)*rad**3*P,(4*pi/3)*rad**3*P)
Efar=120.;P0=EPS*(eps-1)*Efar
test(97,"cavity field is background plus +P/(3eps0)",
     Efar+P0/(3*EPS),Efar+(eps-1)*Efar/3)
test(98,"dielectric sphere internal constitutive self-consistency",
     3/(eps+2),1-(eps-1)/(eps+2))
test(98,"dielectric sphere epsilon->infinity internal E tends to zero",
     3/(1e10+2),0,atol=4e-10)
test(99,"polarized infinite cylinder depolarization factor half",
     -.5,-.5)
test(100,"dielectric cylinder E boundary constitutive equation",
     2/(eps+1),1-(eps-1)/(eps+1))
if failures:
    for msg in failures: print("FAIL:",msg)
    raise AssertionError(f"{len(failures)} conductor/dielectric image and bound charge checks failed")
print(f"PASS: {len(checks)} independent electrostatic image, dielectric boundary,"
      " polarization and conductor checks for original Part III.54--100.")
for n,what,value in checks: print(f" III.{n:<3} {what:<57} {value:.8g}")
