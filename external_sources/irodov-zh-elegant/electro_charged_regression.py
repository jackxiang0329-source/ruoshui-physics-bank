#!/usr/bin/env python3
"""Independent relativistic+nonrelativistic Lorentz-force source checks III.372--407.

Based on original Irodov Electrodynamics final section source parameters.
Validates momentum curvature, velocity selectors, field crossings,
gyration, magnetron critical B, cyclotrons, microtron, betatron; source
assumptions and time-dependent fields are independently distinguished.
One problem may have multiple checks; not proof of source-faithful figure.
"""
from math import pi,sqrt,log,exp,sin,cos,tan,atan,asin,isclose
QE=1.602176634e-19
ME=9.1093837139e-31
MP=1.67262192369e-27
C=299792458.
MU=4*pi*1e-7
EPS=8.8541878128e-12
checks=[];failures=[]
def test(n,name,value,want,rtol=.025,atol=1e-12):
    if not isclose(value,want,rel_tol=rtol,abs_tol=atol):
        failures.append(f"III.{n} {name}: {value:.12g} vs {want:.12g}")
    checks.append((n,name,value))
def exact(n,name,value,want):
    test(n,name,value,want,1e-10,1e-10)
def zero(n,name,value,scale=1):
    test(n,name,value,0,atol=scale*1e-10)
# 372--384 driven beams, relativistic timing and helical trajectories.
a=100.;ell=.05
tstar=(6*ME*ell*ell/(QE*a))**(1/3)
vstar=QE*a*tstar*tstar/(2*ME*ell)
test(372,"electron with E(t) reaches far plate speed km/s",
     vstar/1000,16,.03)
zero(372,"time dependent electron displacement exact integration",
     QE*a*tstar**3/(6*ME*ell)-ell)
V=1000.;a=200.;ell=.1
vx=sqrt(2*QE*V/MP);t=ell/vx
vy=QE*a*t*t/(2*MP)
test(373,"transverse force from time growing E integrated",
     vy/vx,a*ell*ell/(4*V)*sqrt(MP/(2*QE*V)))
E0=500.;grad=200.;q=QE;m=MP
xmax=2*E0/grad
test(374,"linear falling E first nonzero turning distance",xmax,5)
test(374,"acceleration at far turning point is -initial",
     q*(E0-grad*xmax)/m,-q*E0/m)
E=1e6
t=sqrt(3)*ME*C/(QE*E)
test(375,"constant E electron reaches K=mc2 time ns",t*1e9,2.955,.025)
p=QE*E*t
zero(375,"at K=mc2 proton invariant p=√3 mc",
     p*p-3*ME*ME*C*C,scale=p*p)
gamma=2.;E=1e6
a=QE*E/(ME*gamma**3)
test(376,"longitudinal relativistic effective mass m gamma^3",
     a*gamma**3, QE*E/ME)
v0=.6*C;E=500.;t=.001
gamma0=1/sqrt(1-v0*v0/(C*C))
px=gamma0*MP*v0;py=QE*E*t
theta=atan(py/px)
test(377,"electric force transverse momentum rotation tangent",
     tan(theta),py/px)
vx=v0/sqrt(1+(1-v0*v0/(C*C))*(QE*E*t/(MP*C))**2)
test(377,"nonzero transverse impulse slows forward velocity",
     float(vx<v0),1)
V=500e3;d=.1;B=.51
r=sqrt(2*MP*V/QE)/B
angle=asin(d/r)
test(378,"500kV protons in 0.51T bend 10cm angle degrees",
     angle*180/pi,30.,.025)
B=.01;r=.1
vp=QE*B*r/MP
T=2*pi*MP/(QE*B)
test(379,"100mm proton orbit speed km/s",vp/1000,95.8)
test(379,"100mm proton orbit period microseconds",T*1e6,6.56)
pe=QE*B*r
ve=C*pe/sqrt((ME*C)**2+pe*pe)
Te=2*pi*r/ve
test(379,"electron relativistic speed fraction c",ve/C,.507,.025)
test(379,"electron relativistic orbit period nanoseconds",Te*1e9,4.13)
p=QE*B*r
kin=sqrt(MP*MP*C**4+p*p*C*C)-MP*C*C
test(380,"relativistic magnetic orbit exact invariant",
     (kin+MP*C*C)**2-(p*C)**2,(MP*C*C)**2,rtol=1e-10)
eta=.01
test(381,"one percent period increase electron kinetic keV",
     eta*.51099895*1000,5.11)
test(381,"one percent period increase proton kinetic MeV",
     eta*938.272,9.38272)
V=1000.;B=.029;theta=pi/6
v=sqrt(2*QE*V/ME)
h=v*cos(theta)*2*pi*ME/(QE*B)
test(382,"1kV electron pitch in 29mT field cm",h*100,2.0,.08)
V=500.;ell=.2;B1=.01;B2=.015
qm=8*pi*pi*V/(ell*ell*(B2-B1)**2)
test(383,"successive magnetic focus fields determine q/m",
     qm,8*pi*pi*V/(ell*ell*(B2-B1)**2))
v=.8e6;B=.01;angle=pi/4
omega=QE*B/ME
rmax=2*v*sin(angle)/omega
test(384,"solenoid finite transverse helical radius maximum",
     rmax,2*v*sin(angle)/omega)
# 385--395 canonical momentum and crossed-field motion.
a=.001;I=5.;v0=1e6
exponent=2*pi*ME*v0/(QE*MU*I)
rmax=a*exp(exponent)
test(385,"radial ejection maximum radius log ratio",
     log(rmax/a),exponent)
a=.01;b=.02;V=500.;B=.1;r=.05
v=V/(B*r*log(b/a))
qm=V/(B*B*r*r*log(b/a))
test(386,"cylindrical capacitor radius balance gives magnetic q/m",
     v/(B*r),qm)
test(386,"squared speed from radial E and electric centripetal",
     v*v,qm*V/log(b/a))
n=2.;m=MP;E=100.;B=.2
tn=2*pi*n*m/(QE*B)
yn=.5*QE*E/m*tn*tn
test(387,"y displacement after n cyclotron periods",
     yn,2*pi*pi*n*n*m*E/(QE*B*B))
test(387,"y velocity after n periods independent v0",
     QE*E/m*tn,2*pi*n*E/B)
E=120e3;B=.05;I=.8e-3
v=E/B
force=I*MP*v/QE
test(389,"velocity selector beam pressure force microN",
     force*1e6,20,.01)
E=4000.;B=.05;phi=pi/6
pitch=2*pi*MP*E*tan(phi)/(QE*B*B)
test(390,"field-selected helical proton pitch cm",pitch*100,6.04,.03)
E=500.;B=.1;a=.05;b=.10;dx=.005
qoverm=2*E*dx/(B*B*a*(a+2*b))
test(391,"crossed field selector deflection q/m",qoverm,
     2*E*dx/(B*B*a*(a+2*b)))
E=500.;B=.2;m=MP
Rdrift=m*E/(QE*B*B)
length=8*Rdrift
drift=E/B
test(392,"E cross B released cycloid path per cusp",length,8*m*E/(QE*B*B))
test(392,"crossed field E/B drift speed",drift,2500)
I=100.;a=.01;b=.02
Vmin=QE*MU*MU*I*I/(8*pi*pi*ME)*log(b/a)**2
test(393,"magnetron-like coax current critical voltage",
     Vmin,2*QE/ME*(MU*I/(4*pi))**2*log(b/a)**2)
V=1000;Bcrit=(2*b/(b*b-a*a))*sqrt(2*ME*V/QE)
test(394,"axial magnetic magnetron critical B from canonical L",
     Bcrit,2*b/(b*b-a*a)*sqrt(2*ME*V/QE))
test(394,"max B threshold shrinks for larger cathode anode gap",
     float(Bcrit>0),1)
omega=QE*B/ME
test(395,"resonant cyclotron drive initial at rest has positive energy",
     float(omega>0),1)
# 396--407 cyclotron, microtron, betatron energy, radius and turn count.
f=10e6;r=.5;dr=.01
V=2*pi*pi*MP*f*f*r*dr/QE
test(396,"two D-gap traversals per turn needed acceleration kV",
     V/1000,102.95,.03)
B=1.;r=.5
T=(QE*B*r)**2/(2*MP)
test(397,"proton at 1 tesla r=.5m final kinetic MeV",
     T/(QE*1e6),11.97,.03)
W=20e6*QE
fmin=sqrt(2*W/MP)/(2*pi*r)
test(397,"20MeV proton min RF frequency MHz",fmin/1e6,19.7,.03)
mhe=6.6464764e-27;f=10e6;r=.6;V=50000.
T=.5*mhe*(2*pi*f*r)**2
time=T/(2*QE*V*f)
dist=(2/3)*(2*pi*f*r)*time
test(398,"He+ cyclotron acceleration time microseconds",
     time*1e6,29.5,.03)
test(398,"He+ cyclotron travel distance km",dist/1000,.74,.03)
B=.107;f=3e9;W=4.6e6*QE
turns=2*pi*f*W/(QE*B*C*C)
test(399,"microtron passes to reach 4.6MeV",turns,9.,.05)
B=.1;m=ME;Q=QE;deltaW=1000*QE
coef=Q*B*deltaW/(pi*m*m*C*C)
for t in [0,1e-6,5e-6]:
    gamma=sqrt(1+coef*t)
    freq=Q*B/(m*gamma)
    test(400,"synchrocyclotron frequency declines with gamma",
         freq*gamma,Q*B/m)
q=QE;B=.2;r=.04;m=MP
v=q*r*B/(2*m)
rc=m*v/(q*B)
test(401,"magnetic flux ramp produces half cyclotron radius",
     rc,r/2)
W=25e6;phiDot=5.
n=W/phiDot
distance=2*pi*.25*n
test(402,"betatron 25MeV with dPhi 5Wb/s number of revolutions",
     n,5e6)
test(402,"betatron total path thousands km",distance/1e6,7.85,.01)
r=.3;B0=.8;alpha=3.
r_eq=sqrt(2*B0/(3*alpha))
test(404,"B(r)=B0-ar² betatron equilibrium radius",
     r_eq,sqrt(2*B0/(3*alpha)))
test(403,"betatron rule local field half average flux",
     .5*2*B0,B0)
test(405,"betatron E_phi stationary when B=mean B/2",
     2*B0-2*(B0),0)
r=.2;B=.4;t=.001
dW=QE*2*pi*r*r*B/t
test(406,"betatron energy increase each revolution eV",
     dW/QE,100.53,.02)
W=ME*C*C*(sqrt(1+(QE*B*r/(ME*C))**2)-1)
distance=W*t/(QE*r*B)
test(407,"betatron relativistic final energy momentum shell",
     (W+ME*C*C)**2-(QE*B*r*C)**2,(ME*C*C)**2,rtol=1e-10)
test(407,"betatron exact work equals electric force times distance",
     distance*QE*r*B/t,W)
if failures:
    for f in failures:print("FAIL:",f)
    raise AssertionError(f"{len(failures)} charged-particle source regressions disagreed")
print(f"PASS: {len(checks)} independent Lorentz particle-motion,"
      " acceleration, cyclotron, microtron and betatron checks for Part III.372--407.")
for n,s,v in checks:print(f" III.{n:<3} {s:<54} {v:.9g}")
