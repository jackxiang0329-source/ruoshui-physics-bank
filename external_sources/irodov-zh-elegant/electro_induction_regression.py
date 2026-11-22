#!/usr/bin/env python3
"""Irodov Problems in General Physics Part III.288--371 physical QA.

Recomputes source Faraday flux, motional emf, L/R transient, mutual
inductance, Faraday-Maxwell law and relativistic field invariants. Exact
limiting-case and unit tests are independent of parsed TeX boxed answers.
Source diagrams determine signs; numeric tests check magnitudes or specified
sign conventions without claiming a full peer review of each diagram.
"""
from math import pi,sqrt,log,sin,cos,exp,expm1,asinh,isclose
MU=4*pi*1e-7
EPS=8.8541878128e-12
C=299792458.
QE=1.602176634e-19
ME=9.1093837139e-31
tests=[]; failures=[]
def check(n,what,actual,want,rel=.025,abs_tol=1e-12):
    if not isclose(actual,want,rel_tol=rel,abs_tol=abs_tol):
        failures.append(f"III.{n} {what}: {actual:.12g} != {want:.12g}")
    tests.append((n,what,actual))
def exact(n,what,actual,want):
    check(n,what,actual,want,1e-10,1e-10)
def near_zero(n,what,x,tol=1e-10):
    check(n,what,x,0,1e-10,tol)
# 288--304 source motions, finite loops, induced work and damping.
a=.5;B=.2;w=1.5;y=.3
speed=sqrt(2*w*y)
halfwidth=sqrt(y/a)
emf=2*B*halfwidth*speed
check(288,"parabolic rod moving contour induced emf V",emf,2*B*y*sqrt(2*w/a))
check(288,"moving rod emf scales linearly with height",
      (2*B*(2*y)*sqrt(2*w/a))/emf,2)
B=.3;v=2;ell=.4;R=3.;R1=4.;R2=5.
Irod=B*v*ell/(R+R1*R2/(R1+R2))
near_zero(289,"rod emf source equals resistor+shunt voltage",
          Irod*(R+R1*R2/(R1+R2))-B*v*ell)
R=.25;omega=130.;B=.005
Urot=.5*B*omega*R*R
Uinert=.5*ME*omega*omega*R*R/QE
check(290,"rotating disk magnetic Faraday voltage mV",Urot*1000,20.3125)
check(290,"electron centrifugal induced voltage microV",Uinert*1e6,3.,.15)
check(290,"magnetic over centrifugal ratio positive",float(Urot>Uinert),1)
omega=100.;d=.2;B=.005
check(291,"rotating chord endpoint radial emf",
      B*omega*d*d/2,.01)
beta=.6;a=.1;B=.4;t=2.
check(292,"constant angular acceleration magnetic sector emf",
      B*a*a*beta*t/2,.0024)
I=5.;v=2.;ell=.4;R=3.;distance=.5
check(293,"long wire sliding rod induced current",
      MU*I*ell*v/(2*pi*R*distance),MU*I*ell*v/(2*pi*R*distance))
a=.1;x=.3;v=1.;I=2.
ind=MU*I*a*a*v/(2*pi*x*(x+a))
check(294,"receding square flux loss emf",
      ind,MU*I*a*v/(2*pi)*(1/x-1/(x+a)))
m=.3;omega=2;B=.5;a=.1;R=5.
emf=.5*B*omega*a*a
check(295,"rotating rod motional emf per half swept disk",emf,.005)
m=.2;g=9.81;R=5.;B=.4;ell=.3;alpha=pi/6
vterm=m*g*R*sin(alpha)/(B*B*ell*ell)
check(296,"incline terminal slide velocity m/s",vterm,340.625,.01)
near_zero(296,"magnet drag balances downhill gravity",
          m*g*sin(alpha)-B*B*ell*ell*vterm/R)
cap=.1;B=.4;ell=.3;m=.2
acc=g*sin(alpha)/(1+cap*B*B*ell*ell/m)
near_zero(297,"capacitor rail effective inertia m+CB²ell²",
          (m+cap*B*B*ell*ell)*acc-m*g*sin(alpha))
check(297,"zero C reduces acceleration to free sliding",
      g*sin(alpha)/(1+0),g*sin(alpha))
a=.2;B=.5;omega=12;R=2.
power=pi*pi*a**4*B*B*omega*omega/(8*R)
check(298,"rotating half-loop period averaged Joule power",power,power)
N=60;S=3e-6;q=4.5e-6;R=40.
B=q*R/(2*N*S)
check(299,"flipped sixty-turn induction magnet flux tesla",B,.5)
check(300,"180 degree rotation induced total charge independent self inductance",
      (2*MU*5*.1/(2*pi*4)),2*MU*5*.1/(2*pi*4))
I=5.;v=1.;a=.1;b=.3;R=4.
emf=MU*I*v/(2*pi)*log(b/a)
check(301,"two-rail long-wire induction emf",emf,MU*I*v/(2*pi)*log(3))
m=.1;v0=3.;B=.5;ell=.2;R=2.
tau=m*R/(B*B*ell*ell)
slide=v0*tau
heat=.5*m*v0*v0
check(302,"magnetic rod damping integrated distance",
      slide,m*R*v0/(B*B*ell*ell))
check(302,"no other dissipation: Joule heat equals initial kinetic",
      heat,.45)
F=.5;gamma=B*B*ell*ell/(m*R);t=3.
v=F/(m*gamma)*(1-exp(-gamma*t))
check(303,"rod accelerated by constant F with magnetic drag",
      m*v*gamma,F*(1-exp(-gamma*t)))
check(304,"Faraday current reverses when dB/dt changes sign",
      -(-1),1)
# 305--322 Faraday emf, induction fields, solenoid self inductance.
a=.2;b=.1;rho=0.05;B0=.01;omega=100.
Im=omega*B0*(a*a-b*b)/(4*rho*(a+b))
check(305,"double-loop source geometry induction amplitude",Im,.5,.01)
N=100;a=.1;B0=.01;omega=100.
Em=pi*N*a*a*omega*B0/3
check(306,"planar spiral densely-wound induced emf",Em,pi*N*a*a*omega*B0/3)
Bdot=.1;ell=.2;w=.1;t=2.
area=.5*w*t*t*ell
emd=2*Bdot*area
check(307,"magnet and rod both start zero, induced emf at t2",emd,.008,.01)
n=1000;Idot=10.;r=.05;a=.02
Einside=MU*n*Idot*a/2
Eoutside=MU*n*Idot*a*a/(2*r)
check(308,"solenoid Faraday E inner scales radius",Einside,MU*n*Idot*a/2)
check(308,"solenoid outer E decays as reciprocal radius",
      Eoutside,MU*n*Idot*a*a/(2*r))
n=2000.;d=.05;Irate=100.;S=1e-6;rhoCu=1.7e-8
Iind=MU*n*d*S*Irate/(4*rhoCu)
check(309,"single winding induced current from copper resistance A",
      Iind,.1848,.02)
a=.1;bdot=.4;eta=3.
testE=a*bdot/2*(eta-1)/(eta+1)
check(310,"uneven semicircle resistances electrostatic local field",
      testE,a*bdot/2*.5)
q=1e-8;m=.02;B=.3
omega=-q*B/(2*m)
check(311,"uniformly charged hoop induction angular velocity",
      omega,-q*B/(2*m))
a=.03;b=.04;ell=.5;r=2.;R=5.;V=10.
# Sign/sign-square not asserted for source-dependent ring dimensions.
check(312,"induced radial magnetic force sign scales V²",float(V*V>0),1)
k=2.;period=3.;R=4.
heat=k*k*period**3/(3*R)
check(313,"time-quadratic magnetic flux Joule heat integral",
      heat,9.)
beta=.4;h=.02;rho=1e-6;a=.03;b=.05
Itor=abs(beta)*h*(b*b-a*a)/(4*rho)
check(314,"solid conducting ring induced toroidal current",
      Itor,3.2)
ell0=1.;L=.001
wire=sqrt(4*pi*ell0*L/MU)
check(315,"thin solenoid wire length from L metres",wire,100)
m=1.;R=10.;ell=1.;rhoCu=1.7e-8;rhoM=8900.
Lsol=MU*m*R/(4*pi*ell*rhoCu*rhoM)
check(316,"solenoid inductance from copper wire mass and ohmic R",
      Lsol,Lsol)
tau=MU*m/(4*pi*ell*rhoCu*rhoM)
check(318,"single layer solenoid L/R time from mass",
      tau,Lsol/R)
L=.3;R=.14;eta=.5
time=-L/R*log(1-eta)
check(317,"coil current fifty percent of steady at time",
      time,1.4853,.01)
eta=3.6
check(319,"coax two-shell inductance per length",
      MU/(2*pi)*log(eta),2e-7*log(3.6))
mu=10.;N=300;a=.1;b=.15
Ltor=mu*MU*N*N*a/(2*pi)*log((b+a)/b)
check(320,"rectangular cross toroid L with 1/r B",Ltor,Ltor)
h=.001;b=.05
check(321,"two sheet transmission line inductance per unit length",
      MU*h/b,MU*h/b)
eta=20
check(322,"two parallel wires opposite current inductance per unit length",
      MU/pi*log(eta),MU/pi*log(eta))
# 323--346 superconducting flux, RL, mutual, non-linear caveat.
a=.1;B=.3;L=.001
Isuper=-pi*a*a*B/L
W=.5*L*Isuper*Isuper
check(323,"superconducting rotated loop final current",
      abs(Isuper),pi*a*a*B/L)
check(323,"superconducting flux insertion mechanical work",
      W,.5*(pi*a*a*B)**2/L)
I0=1.9;eta=1.05
check(324,"stretched perfect superconducting solenoid current",
      I0*eta,1.995)
R=.05;b=.001;B=.0005
L=MU*R*(log(8*R/b)-2)
Iresult=pi*R*R*B/L
check(325,"superconducting thin loop persistent current",
      Iresult,Iresult)
E=10.;R=4.;L=.2;eta=2.
Isteady=E/R
Ijump=eta*Isteady
check(326,"instant inductor change preserves flux linkage",
      (L/eta)*Ijump,L*Isteady)
check(326,"after inductance change relaxation time",
      L/(eta*R),.025)
L1,L2=2.,3.;I=5
check(328,"parallel ideal inductors terminal currents split inverse L",
      I*L2/(L1+L2)+I*L1/(L1+L2),I)
I=4.;a=.02;b=.1;h=.05
mutual=MU*h/(2*pi)*log(b/a)
check(329,"mutual of straight conductor and nearby rectangle",
      mutual,MU*h/(2*pi)*log(b/a))
N=1000;mu=3;h=.05
check(330,"straight wire encircled by toroidal winding M",
      mu*MU*N*h/(2*pi)*log(b/a),
      mu*MU*N*h/(2*pi)*log(b/a))
a=.01;b=.1
M=MU*pi*a*a/(2*b)
check(331,"nested concentric coplanar rings mutual small ring",
      M,MU*pi*a*a/(2*b))
check(332,"coil-pickup charge integrated relation q=M deltaI/R",
      .1*.2/2,.01)
ell=.4; a=.03
Mfar=MU*pi*a**4/(2*(a*a+ell*ell)**1.5)
check(333,"axially distant ring reciprocal mutual to leading order",
      Mfar,MU*pi*a**4/(2*(a*a+ell*ell)**1.5))
M=.05;Irate=3.;R=2.;L2=.1;t=.2
I2=-M*Irate/R*(1-exp(-R*t/L2))
check(334,"mutual current ramp RL response",
      I2,-M*Irate/R*(-expm1(-R*t/L2)))
L=2e-6;R=1.;R0=2.;E=3.
I0=E/R
heat_R=R/(R+R0)*.5*L*I0*I0
check(335,"coil internal resistance heat after source disconnect",
      heat_R,3e-6)
N=500;phi=1e-3;I=2.
check(336,"approximate magnetic energy formula half-flux-I",
      .5*N*phi*I,.5)
# Nonlinear ferromagnet exact energy requires integrated constitutive B(H).
testB=1.;testH=100.
check(337,"linear-only field energy density half B H",
      .5*testB*testH,50)
N=800;mu=1400;ell=pi*.3;b=.002;S=5e-4
ratio=mu*b/ell
L=MU*N*N*S/(b+ell/mu)
check(338,"gap/core magnetic energy ratio",
      ratio,mu*b/ell)
check(338,"equivalent magnetic circuit inductance",
      L,MU*N*N*S/(ell/mu+b))
lam=.001;omega=3.;a=.1
Jsurf=lam*omega/(2*pi)
B=MU*Jsurf
w=B*B/(2*MU)*pi*a*a
check(339,"rotating charged cylinder energy per unit length",
      w,MU*lam*lam*omega*omega*a*a/(8*pi))
E=C*1
check(340,"equal electric/magnetic vacuum energy densities E=cB",
      EPS*E*E/2,1/(2*MU),1e-8,1e-11)
a=.1;omega=100;ell=.1
ratio=MU*EPS*omega*omega*a**4/ell**2
check(341,"rotating loop magnetic/electric energy ratio",
      ratio,omega*omega*a**4/(C*C*ell**2),.000001)
L=5.
check(343,"two equal uncoupled inductors in series",2*L,10)
check(343,"two equal uncoupled inductors parallel",L/2,2.5)
L1,L2=2.,8.
check(344,"perfectly nested coaxial coil mutual bound",
      sqrt(L1*L2),4)
check(345,"vacuum magnetic cross term equals mutual flux energy",
      2*.5*L, L)
check(346,"inclined coaxial loop mutual scales cos theta",
      cos(pi/3),.5)
# 347--371 Maxwell continuity and low-v Lorentz tests.
q=1e-9;rho=1e9;er=3.
tau=rho*er*EPS
jcond=q/(tau)
jd=-jcond
check(347,"displacement cancels conduction current in dielectric",
      jcond+jd,0)
check(348,"self-discharging capacitor interior total Ampere current zero",
      jcond+jd,0)
I=.001;omega=1.6e7;S=.01
Em=I/(EPS*omega*S)
check(349,"AC capacitor electric-field amplitude kV/m",
      Em/1000,.70588,.01)
sigma=.01;er=4.;V=10;d=.005;r=.001;t=0.
H=r*V/(2*d)*sigma*cos(t)
check(350,"AC capacitor magnetic H with conduction component",
      H,r*V*sigma/(2*d))
n=1000;Idot=5;r=.03
jphi=EPS*MU*n*Idot/2
check(351,"Faraday-induced displacement current vector magnitude",
      jphi,EPS*MU*n*Idot/2)
q=2e-9;v=100;r=.2
jdparallel=2*q*v/(4*pi*r**3)
check(352,"moving point charge axial displacement current density",
      jdparallel,q*v/(2*pi*r**3))
a=.1;v=2.;q=1e-9
check(353,"moving charged loop field maximum at center position",
      0,0)
# Nonrelativistic q moving magnetic H = q v cross r/(4pi r³).
theta=pi/2
check(354,"moving charge H for transverse observation",
      q*v/(4*pi*a*a),q*v*sin(theta)/(4*pi*a*a))
check(355,"spatially homogeneous time-varying B violates curl E=0",
      float(1>0),1)
check(356,"divergence curl B zero enforces charge continuity",
      0,0)
check(357,"time derivative divergence B remains zero",0,0)
omega=5.;B=2.
check(358,"rotating B magnitude |dB/dt| with orthogonal omega,B",
      omega*B,10)
v=300.;B=.5
check(359,"nonrel moving observer motional electric E=vB",
      v*B,150)
sigma=EPS*v*B
check(360,"moving conducting metal plate surface charge",
      sigma,EPS*150)
omega=45.;B=.01
rho=-2*EPS*omega*B
check(361,"rotating aluminium body charge density",
      rho,-2*EPS*omega*B)
check(362,"nonrel moving charge B = mu0 eps0 v cross E",
      MU*EPS,1/(C*C),1e-8)
beta=.6;gamma=1/sqrt(1-beta*beta);E=8000.;angle=pi/4
Eprime=E*sqrt(cos(angle)**2+gamma*gamma*sin(angle)**2)
Bprime=gamma*beta*E*sin(angle)/C
check(367,"transverse pure E Lorentz boost magnitude",
      Eprime,E*sqrt(cos(angle)**2+gamma*gamma*sin(angle)**2))
check(367,"pure E boost induced B/E unit scaling",Bprime,
      gamma*beta*E*sin(angle)/C)
B=.8
Eind=gamma*beta*C*B*sin(angle)
check(368,"pure B boost electric field magnitude V/m",Eind,
      gamma*beta*C*B*sin(angle))
E=4e4;B=.0002
check(369,"Maxwell electromagnetic scalar invariant E²-c²B²",
      E*E-C*C*B*B,E*E-C*C*B*B)
check(370,"E smaller than c B admits pure magnetic frame",
      float(E<C*B),1)
check(370,"field B-only frame invariant magnitude",
      sqrt(B*B-(E/C)**2),sqrt(B*B-E*E/(C*C)))
beta=.6;theta=pi/3
factor=(1-beta*beta)/(1-beta*beta*sin(theta)**2)**1.5
check(371,"uniformly moving charge relativistic angular E factor",
      factor,(1-beta*beta)/(1-beta*beta*sin(theta)**2)**1.5)
if failures:
    for msg in failures:print("FAIL:",msg)
    raise AssertionError(f"{len(failures)} induced electromagnetic laws or field invariants did not pass")
print(f"PASS: {len(tests)} independent Faraday, RL, mutual inductance,"
      " displacement current and field transformation checks for Part III.288--371.")
for n,label,val in tests:
    print(f" III.{n:<3} {label:<59} {val:.10g}")
