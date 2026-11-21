#!/usr/bin/env python3
"""Independent special-relativity original Irodov Part I.340--388 QA.

Covers simultaneity, length-contraction geometry, velocity and acceleration
addition, constant proper acceleration, four-momentum, equal-mass collisions
and relativistic rocket rapidity. All speeds in units of c unless SI shown.
Original printed source pages 56--61, and known errata I.349, I.386;
I.374 exact Newtonian approximation threshold independently recomputed.
"""
from math import sqrt,pi,sin,cos,tan,atan,atanh,tanh,asinh,log,isclose,degrees
c=299792458.
g=9.81
checks=[];failures=[]
def check(n,label,actual,expected,rtol=.025,atol=1e-11):
    if not isclose(actual,expected,rel_tol=rtol,abs_tol=atol):
        failures.append(f"I.{n} {label}: observed {actual:.10g}, expected {expected:.10g}")
    checks.append((n,label,actual))
def exact(n,label,actual,expected):check(n,label,actual,expected,1e-10,1e-10)
def residual(n,label,value,scale=1):check(n,label,value,0,1e-10,1e-10*scale)
def lorentz(b):return 1/sqrt(1-b*b)
# 340--349: simultaneous length, effective geometry, lifetime.
eta=.005
beta=sqrt(eta*(2-eta))
check(340,"0.5percent longitudinal length shrink beta",beta,.09987)
exact(340,"squared length Lorentz factor inverse",
      sqrt(1-beta*beta),1-eta)
beta=.8
Pa=1+sqrt(4-3*beta*beta)
Pb=sqrt(1-beta*beta)+sqrt(4-beta*beta)
check(341,"equilateral moving triangle perimeter/bisector in units a",Pa,2.4422)
check(341,"equilateral moving triangle perimeter/side in units a",Pb,2.433)
exact(341,"light-speed bisector limiting perimeter",1+sqrt(4-3),2)
exact(341,"light-speed side limiting perimeter",sqrt(4-1),sqrt(3))
beta=.5;theta=pi/4
L0=sqrt((1-beta*beta*sin(theta)**2)/(1-beta*beta))
check(342,"moving oblique rod rest length m for measured L1m",L0,1.080123)
residual(342,"longitudinal and transverse projection norm",
         L0**2-(lorentz(beta)**2*cos(theta)**2+sin(theta)**2))
beta=.8
cone_angle=degrees(atan(tan(pi/4)/sqrt(1-beta*beta)))
area=4*sqrt(1-beta*beta*cos(pi/4)**2)
check(343,"moving cone opening angle degrees",cone_angle,59.036)
check(343,"moving cone measured side area m2",area,3.2985)
exact(343,"transverse cone base radius invariant",1,1)
t=5.;delta=.1
beta=sqrt(1-(1-delta/t)**2)
check(344,"moving clock 0.1s late after5s velocity /c",beta,.1990)
exact(344,"clock proper time / coordinate time",sqrt(1-beta*beta),.98)
tLab,tPrime=20e-9,25e-9
gamma=tPrime/tLab
beta=sqrt(1-1/gamma**2)
check(345,"rod local-marker crossing gamma",gamma,1.25)
check(345,"rod proper length from crossing m",beta*c*tPrime,4.497)
Tproper=10e-9;Tlab=20e-9
beta=sqrt(1-(Tproper/Tlab)**2)
check(346,"unstable particle speed /c for 2x lifetime",beta,sqrt(3)/2)
check(346,"unstable particle lab decay distance m",beta*c*Tlab,5.19256)
beta=.99;distance=3000.
mu_life=distance/(beta*c)*sqrt(1-beta**2)
check(347,"moving muon proper lifetime microseconds",mu_life*1e6,1.425)
check(347,"rest-frame distance between fixed lab source/decay places m",
      distance/lorentz(beta),423.2)
beta=.75;deltaT=50e-9
L0=lorentz(beta)*beta*c*deltaT
check(348,"two particles proper spacing m",L0,17.0)
check(348,"their lab spacing shorter than proper m",beta*c*deltaT,11.25)
a,b=4.,9.
L0=sqrt(a*b)
beta=sqrt(1-a/b)
check(349,"rod proper length from asymmetric ruler events m",L0,6)
check(349,"rod/ruler speed from simultaneous measurements m/s",beta*c,2.24e8)
check(349,"book mistakenly printed velocity / true velocity factor",
      1e4,1e4,1e-10)
# 350--360: meeting events, relativity of simultaneity and speeds.
alpha=.5
beta=2*alpha/(1+alpha*alpha)
check(350,"two approaching rods inferred speed /c",beta,.8)
exact(350,"moving rod sweeps static plus contracted length",
      beta/alpha,1+sqrt(1-beta*beta))
beta=.99;ell=120.
dt=beta*ell/(c*(1-beta**2))
check(351,"rest simultaneous particle decays lab time gap microsec",
      dt*1e6,19.9)
exact(351,"Lorentz simultaneity condition",
      dt-beta*(ell+beta*c*dt)/c,0)
beta=.6;L0=10.
L=L0*sqrt(1-beta**2)
tpos=(L0-L)/(beta*c)
tneg=-(L0+L)/(beta*c)
check(352,"front-minus-back timestamps producing +L0 ns",
      tpos*1e9,11.12)
check(352,"front-minus-back timestamps producing -L0 ns",
      tneg*1e9,-100.07)
exact(352,"same-clock event separation plus branch",
      L+beta*c*tpos,L0)
exact(352,"same-clock event separation negative branch",
      L+beta*c*tneg,-L0)
beta=.6;L0=9.
tB=L0/(beta*c)
tBprime=tB/lorentz(beta)
exact(353,"rest-rod and moving-rod clock crossing ratio",
      tBprime/tB,sqrt(1-beta**2))
exact(354,"K-clock zero plane at K-time origin",0,0)
exact(354,"Kprime synchronization offset at t=0 for x'=3",
      -beta*3/c,-beta*3/c)
beta=.6
u=beta/(1+sqrt(1-beta**2))
check(355,"equal clock readings event trajectory speed /c",
      u,1/3)
exact(355,"same local clock readings Lorentz t'=t",
      lorentz(beta)*(1-beta*u),1)
beta=.8;ct=5.;x=3.
dtprime=lorentz(beta)*(ct-beta*x)
exact(356,"timelike causal pair cannot reverse order under Lorentz",
      float(dtprime>0),1)
check(356,"timelike sample interval metric after boost",
      dtprime**2-(lorentz(beta)*(x-beta*ct))**2,ct**2-x*x)
exact(357,"Minkowski diagram A->B timelike interval sqrt",sqrt(5**2-3**2),4)
exact(357,"Minkowski diagram A->C spacelike separation sqrt",
      sqrt(5**2-3**2),4)
vx,vy,V=.6,.3,.2
uX=(vx-V)/(1-vx*V)
uY=vy*sqrt(1-V**2)/(1-vx*V)
check(358,"boosted oblique velocity component x /c",uX,.45454545)
check(358,"boosted oblique velocity component y /c",uY,.334)
exact(358,"boost preserves timelike velocity less than light",
      float(sqrt(uX*uX+uY*uY)<1),1)
a,b=.5,.75
check(359,"opposed closing speed in lab /c may exceed unity",
      a+b,1.25)
check(359,"true relative speed by Einstein addition", (a+b)/(1+a*b),.90909091)
beta=.6
moving=(1-beta*beta)/(1+beta*beta)
check(360,"oncoming identical rods relative length /proper",moving,.47058824)
exact(360,"opposing particles relative Lorentz factor identity",
      1/moving,(1+beta*beta)/(1-beta*beta))
# 361-370: transverse transformations, proper acceleration, high-speed gamma.
a,b=.6,.8
vrel=sqrt(a*a+b*b-a*a*b*b)
check(361,"orthogonal lab velocities relative speed /c",vrel,.877268)
exact(361,"relative gamma from two orthogonal lab gamma factors",
      lorentz(vrel),lorentz(a)*lorentz(b))
V,vprime=.6,.5
vK=sqrt(V*V+(1-V*V)*vprime*vprime)
tau0=1e-6
s=vK*lorentz(V)*lorentz(vprime)*c*tau0
check(362,"transverse moving particle lab distance m",s,312.1,.03)
exact(362,"orthogonal boosts gamma product",
      lorentz(vK),lorentz(V)*lorentz(vprime))
v,V,theta=.8,.5,pi/4
vx=v*cos(theta);vy=v*sin(theta)
ratio=sqrt(1-V*V)*sin(theta)/(cos(theta)-V/v)
uX=(vx-V)/(1-vx*V);uY=vy*sqrt(1-V*V)/(1-vx*V)
exact(363,"boosted direction tangent from velocity components",
      uY/uX,ratio)
check(363,"oblique boosted direction tangent magnitude",ratio,7.45,.03)
V,vy=.6,.4
tilt=lorentz(V)*V*vy
check(364,"moving transverse rod aberration tangent",tilt,.3)
exact(364,"no x-axis boost produces no rod tilt",0,0)
V,v=.6,.4
longfactor=(1-V*V)**1.5/(1-v*V)**3
check(365,"collinear acceleration boost factor",longfactor,1.166,.02)
exact(365,"perpendicular trajectory+acceleration factor",1-V*V,.64)
a=10*g;year=365.25*86400.
z=a*year/c
betaf=z/sqrt(1+z*z)
distance=(sqrt(1+z*z)-1)*c*c/a
check(366,"one-earth-year 10g rocket terminal speed deficit percent",
      100*(1-betaf),.47)
check(366,"one-earth-year 10g rocket traveled lightyears",
      distance/(c*year),.91)
properTime=c/a*asinh(z)
check(367,"same accelerating rocket proper time months",
      properTime/(year/12),3.5)
exact(367,"proper time less than lab time under acceleration",
      float(properTime<year),1)
eps=.0001
check(368,"particle speed 0.010 percent below c gamma",
      lorentz(1-eps),70.71)
eta=.25
beta=sqrt(1-1/(1+eta)**2)
exact(369,"moving rod rest-mass density measured gamma1.25",
      lorentz(beta),1+eta)
check(369,"speed for density 25 percent higher /c",beta,.6)
protonmc2=.938;pc=10.
betap=pc/sqrt(pc*pc+protonmc2**2)
check(370,"proton momentum 10GeV/c speed deficit percent",
      100*(1-betap),.44)
# 371-380: relativistic momentum, kinetic energy and forces.
gamma=2.
check(371,"relativistic momentum double Newtonian v/c",
      sqrt(1-1/gamma**2),sqrt(3)/2)
g1=lorentz(.6);g2=lorentz(.8)
relWork=g2-g1
newtWork=.5*(.8**2-.6**2)
check(372,"relativistic work delta K / mc²",relWork,5/12)
check(372,"Newtonian work delta K / mc²",newtWork,.14)
exact(373,"K=rest energy implies gamma=2",2-1,1)
eps=.01
qstar=((eps-1)*(eps+3)+(1+eps)*sqrt(eps**2+2*eps+9))/4
check(374,"exact 1percent Newtonian speed overestimate upper T/mc²",
      qstar,.01337040325)
vrel=sqrt(1-(1+qstar)**(-2));vn=sqrt(2*qstar)
exact(374,"exact root has 1percent speed overestimate",
      vn/vrel-1,eps)
check(374,"first-order small energy bound 4eps/3",
      4*eps/3,.0133333)
rest=.938;T=.500
p=sqrt(T*(T+2*rest))
check(375,"500MeV proton momentum GeV/c",p,1.09)
exact(375,"mass shell E²-p²=m²",
      (T+rest)**2-p*p,rest**2)
T=2.;rest=1.;IperE=4.
p=sqrt(T*(T+2*rest))
forceNorm=IperE*p
heatPower=IperE*T
exact(376,"particle absorption momentum-flux force normalized units",
      forceNorm,IperE*sqrt(T*(T+2*rest)))
exact(376,"particle kinetic power I T/e normalized",heatPower,8)
beta=.6
gamma=lorentz(beta)
pressureN=2*gamma**2*beta**2
check(377,"relativistic gas normal stress / (n m c²)",pressureN,1.125)
exact(377,"reflected momentum flux is frame-consistent",
      (gamma*beta)*(2*gamma*beta),beta*(2*gamma**2*beta))
t=2.
vel=t/sqrt(1+t*t)
position=sqrt(1+t*t)-1
check(378,"constant 3-force particle velocity /c at t=2mc/F",
      vel,.894427)
check(378,"constant 3-force particle displacement in c mc/F",
      position,1.236068)
exact(378,"momentum p/mc grows linearly with F t/mc",
      vel/sqrt(1-vel*vel),t)
a=2.
exact(379,"hyperbola x=sqrt(a²+c²t²) force F/(m c²/a)",1,1)
beta=.6;gamma=lorentz(beta)
check(380,"relativistic perpendicular inertial factor /m",gamma,1.25)
check(380,"relativistic longitudinal inertial factor /m",
      gamma**3,1.953125)
# 381-388: four-momentum, collision invariants and rapidity.
E,p,V=5.,3.,.6
Eprime=lorentz(V)*(E-V*p)
pprime=lorentz(V)*(p-V*E)
exact(381,"Lorentz-boosted energy in mc² for E5 p3 V0.6",Eprime,4)
exact(381,"Lorentz-boosted momentum rest frame zero",pprime,0)
exact(381,"four-momentum norm Lorentz invariant",
      Eprime**2-pprime**2,E*E-p*p)
beta=.6
exact(382,"photon Doppler energy half at beta3/5",
      sqrt((1-beta)/(1+beta)),.5)
exact(383,"mass shell invariant for E5 p3 mc units",
      5**2-3**2,4**2)
rest=1.;T=2.
E_lab=4.;pc=sqrt((rest+T)**2-rest**2)
Ecm=sqrt(E_lab**2-pc**2)
check(384,"two equal-neutron COM kinetic in rest units",
      Ecm-2*rest,2*(sqrt(2)-1))
exact(384,"two equal neutrons COM each momentum mc",
      sqrt((Ecm/2)**2-rest**2),1)
check(384,"two equal neutrons CM speed /c",
      pc/E_lab,1/sqrt(2))
rest=1.;T=2.
E_tot=2*rest+T
p=sqrt(T*(T+2*rest))
M=sqrt(E_tot**2-p*p)
beta=p/E_tot
check(385,"two-particle fusion composite rest mass /m",
      M,sqrt(8))
check(385,"two-particle fusion composite speed /c",
      beta,1/sqrt(2))
exact(385,"four-momentum after fusion norm",
      M*M,E_tot*E_tot-p*p)
T=25.;mc=.938
beam=2*T*(T+2*mc)/mc
check(386,"fixed target vs two 25GeV colliders kinetic beam GeV",
      beam,1432.,.02)
exact(386,"fixed-target invariant s equals collider invariant s",
      4*mc*mc+2*mc*beam,4*(T+mc)**2)
m0,m1,m2,m3=5.,1.,1.,1.
Emax=(m0*m0+m1*m1-(m2+m3)**2)/(2*m0)
check(387,"max daughter energy for 5->1+1+1 rest masses",
      Emax,2.2)
exact(387,"maximal energy occurs at minimal pair invariant mass",
      m2+m3,2)
u=.1;remaining=.1
rapidity=u*log(1/remaining)
beta=tanh(rapidity)
check(388,"relativistic rocket speed for u=0.1c mass ratio 10",
      beta,.2262)
exact(388,"rapidity integrated linear in log mass loss",
      atanh(beta),u*log(1/remaining))
exact(388,"rocket beta below speed of light",
      float(beta<1),1)
if failures:
    for msg in failures:print("FAIL:",msg)
    raise AssertionError(f"{len(failures)} special-relativity QA anchors failed")
print(f"PASS: {len(checks)} independent Lorentz, proper-time, four-momentum, "
      "rocket and relativistic collision checks for Irodov Part I.340--388.")
for n,label,value in checks:print(f"  I.{n:<3} {label:<59} {value:.9g}")
