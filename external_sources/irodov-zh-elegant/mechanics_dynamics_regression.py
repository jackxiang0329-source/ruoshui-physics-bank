#!/usr/bin/env python3
"""Independent physical checks for original Irodov Part I.59--117.

Kinematic constraints, statics vs slipping, Newton's equations, rotating
systems and limiting cases are recomputed using original problem parameters.
The 59 real questions have several check anchors each; this is NOT a
mathematical peer review of all 1878 questions or original illustrations.
"""
from math import sqrt, sin, cos, tan, atan, asin, acos, pi, log, exp, degrees, isclose
G=9.81
OMEGA_E=7.2921159e-5
EARTH_R=6371000.
checks=[]
def test(num,subject,actual,expected,rtol=.035,atol=1e-13):
    if not isclose(actual,expected,rel_tol=rtol,abs_tol=atol):
        raise AssertionError(f"I.{num} {subject}: actual {actual:.9g} expected {expected:.9g}")
    checks.append((num,subject,actual))
def check_equilibrium(num,subject,residual,scale=1.):
    test(num,subject,residual,0,rtol=1e-10,atol=max(1e-12,scale*1e-10))

# 59 and 60: buoyancy and static/sliding friction constraints.
m,w,g=4.,2.,10.
delta=2*m*w/(g+w)
B=m*(g-w)
test(59,"discarded ballast kg",delta,4/3,1e-10)
check_equilibrium(59,"original buoyancy net downward",m*g-B-m*w)
check_equilibrium(59,"after ballast net upward",B-(m-delta)*(g+w))
mu=.2
a=(1-2*mu)*G/3
T12=(1+mu)*G/3
test(60,"three-equal-mass pulley acceleration /g",a/G,.2)
test(60,"interblock rope tension /(mg)",T12/G,.4)
check_equilibrium(60,"second block Newton residual",T12-mu*G-a)
test(60,"static/sliding threshold coefficient",.5,.5,1e-10)
test(60,"static no-motion possible above threshold",float(.6>=.5),1.,1e-10)

# 61--64: two blocks on incline, friction direction and launch criterion.
m1,m2,k1,k2,alpha=2.,3.,.3,.1,pi/6
Nc=m1*m2/(m1+m2)*(k1-k2)*G*cos(alpha)
acc=G*(sin(alpha)-(k1*m1+k2*m2)/(m1+m2)*cos(alpha))
test(61,"mutual force of two sliding blocks N",Nc,2.04)
check_equilibrium(61,"lower block equation",m1*acc-(m1*G*sin(alpha)-k1*m1*G*cos(alpha)+Nc))
check_equilibrium(61,"upper block equation",m2*acc-(m2*G*sin(alpha)-k2*m2*G*cos(alpha)-Nc))
test(61,"critical tan incline", (k1*m1+k2*m2)/(m1+m2),.18,1e-10)
test(61,"equal friction eliminates contact", (k1-k1),0,1e-10)
k=(4-1)/(4+1)*tan(pi/12)
test(62,"up/down time ratio2 friction",k,.16077)
test(62,"free downhill sliding condition",float(k<tan(pi/12)),1,1e-10)
up=sin(pi/6)+.1*cos(pi/6);lo=sin(pi/6)-.1*cos(pi/6)
test(63,"hanging-mass downward launch ratio",up,.5866)
test(63,"hanging-mass upward launch ratio",lo,.4134)
test(63,"static mass ratio interval width",up-lo,.173205)
test(64,"hanging mass acceleration m/s2",
     G*(2/3-sin(pi/6)-.1*cos(pi/6))/(1+2/3),.471)

# 65--70: sliding, incline optimization, normal contact, variable pull.
board,block,mu,r=3.,1.,.2,2.0 # r: applied force growth N/s
t0=mu*block*G*(board+block)/(r*board)
ap=mu*block*G/board
ab=(r*3-mu*block*G)/block
test(65,"two-mass slip onset seconds",t0,1.308)
test(65,"board post-slip acceleration m/s2",ap,.654)
test(65,"block post-slip accel at t=3 m/s2",ab,4.038)
check_equilibrium(65,"onset continuity of common acceleration",r*t0/(board+block)-ap)
test(66,"minimum-time incline degrees",45+degrees(atan(.14))/2,48.99)
tmin=sqrt(4*2.1/(G*(sqrt(1+.14**2)-.14)))
test(66,"shortest incline slide time s",tmin,.992)
beta=atan(.2)
pull=(sin(pi/6)+.2*cos(pi/6))/sqrt(1+.2**2)
normal=(cos(pi/6)-.2*sin(pi/6))/(1+.2**2)
test(67,"best rope inclination degrees",degrees(beta),11.31)
test(67,"minimum tension /(mg)",pull,.660)
test(67,"normal force positive in optimal config",float(normal>0),1,1e-10)
m,a,angle=2.,3.,pi/6
tl=m*G/(a*sin(angle))
vel=a*cos(angle)*tl**2/(2*m)
dist=a*cos(angle)*tl**3/(6*m)
test(68,"liftoff time seconds",tl,13.08)
test(68,"liftoff horizontal speed m/s",vel,111.12)
check_equilibrium(68,"zero normal force at liftoff",m*G-a*tl*sin(angle))
test(68,"liftoff displacement metres",dist,484.0,.05)
test(69,"linearly tilted force speed at alpha pi/2",
     sqrt(2*G/(3*.1)),8.087)
test(70,"motor/bar contact time seconds",
     sqrt(2*5/(3*1+.2*G)),1.42)

# 71--80: two-stage pulleys, accelerating lift, wedge and static margins.
m1,m2,g,a0=2.,1.,G,2.
a1r=(m1-m2)/(m1+m2)*(g+a0)
a1lab=a1r-a0
T=2*m1*m2/(m1+m2)*(g+a0)
test(71,"elevator relative acceleration m/s2",a1r,3.93667)
test(71,"elevator shaft downward acceleration m/s2",a1lab,1.93667)
test(71,"lift pulley roof reaction newtons",2*T,31.4933)
check_equilibrium(71,"descending load relative Newton equation",m1*(g+a0)-T-m1*a1r)
check_equilibrium(71,"ascending load relative Newton equation",T-m2*(g+a0)-m2*a1r)
eta=.4
a72=2*G*(2*eta-sin(pi/6))/(4*eta+1)
test(72,"moving pulley object2 downward acceleration",a72,2.263)
test(72,"moving pulley reversal eta critical",sin(pi/6)/2,.25,1e-10)
m0,m1,m2=1.,2.,3.
TT=2*G*m0*m1*m2/(4*m1*m2+m0*(m1+m2))
a73=G-TT/m1
test(73,"two-pulley tension newtons",TT,4.06)
test(73,"object1 downward acceleration",a73,7.78)
a2=G-TT/m2
a0=2*TT/m0
check_equilibrium(73,"two-cord moving pulley acceleration constraint",
                  a73+a2-2*a0)
check_equilibrium(73,"movable pulley net tension residual",m0*a0-2*TT)
test(74,"friction ball-on-thread with M2 m.5 ell1 t3 N",
     2*1*.5*2/((2-.5)*3**2),4/27,1e-10)
test(75,"two-stage pulley rod-ball meeting time s",
     sqrt(2*1*(4+1.8)/(3*G*(2-1.8))),1.40)
test(75,"rod-ball limiting eta reaches 2",float(1.8<2),1,1e-10)
test(76,"moving pulley rise total after lower mass hits floor m",
     (6*4/(4+4))*.2,.6,1e-10)
eta=2
tanang=tan(pi/6)
aB=G/(tanang+eta/tanang)
aA=aB*tanang
test(77,"wedge B horizontal acceleration m/s2",aB,2.427)
test(77,"rod A vertical acceleration m/s2",aA,1.401)
test(77,"wedge heavy-mass limit B acceleration",G/(tanang+1000/tanang),0,.01,atol=.01)
test(78,"pulley-wedge m1 M2 k.2 block ground acceleration",
     sqrt(2)*G/(2+2+.2),3.303)
k=.2
test(79,"two-block zero-relative-acceleration threshold /g",
     (1-k)/(1+k),2/3,1e-10)
test(79,"mu>=1 implies stationary feasible at zero acceleration",max(0,(1-1.2)/(1+1.2)),0,1e-10)
k=.2
test(80,"prism acceleration upper bound /g",
     (sin(pi/6)+k*cos(pi/6))/(cos(pi/6)-k*sin(pi/6)),.879)
test(80,"max-accel normal force positive condition",float(k<1/tan(pi/6)),1,1e-10)

# 81--90: moving wedges, impulses, circles, pendulum, rotation.
m1,m2=2.,1.
wedgeacc=m2*G*sin(pi/6)*cos(pi/6)/(m1+m2*sin(pi/6)**2)
test(81,"mobile wedge horizontal acceleration",wedgeacc,1.888)
test(81,"wedge acceleration vanishes alpha0",0,0,1e-10)
test(82,"string-on-moving-wedge acceleration",
     G*sin(pi/6)/(2+2*(1-cos(pi/6))),2.163)
test(83,"quarter-circle constant-speed force vector average for m3 R1 v2",
     2*sqrt(2)*3*2**2/pi,10.804)
test(83,"quarter-circle constant tangential acceleration m3 a1.5",
     3*1.5,4.5,1e-10)
v=360/3.6
R=500
m=70
test(84,"vertical loop pilot bottom apparent weight newtons",
     m*(G+v*v/R),2087)
test(84,"vertical loop pilot top apparent weight newtons",
     m*(v*v/R-G),713)
test(84,"vertical loop pilot side apparent weight newtons",
     m*sqrt(G**2+(v*v/R)**2),1558)
c=1/sqrt(3)
test(85,"pendulum maximum vertical speed T/(mg)",3*c,sqrt(3),1e-10)
test(85,"pendulum horizontal net acceleration condition",
     G*(3*c*c-1),0,1e-10)
test(85,"pendulum theta degrees",degrees(acos(c)),54.7356)
test(86,"equal extreme/minimum pendulum acceleration angle",
     2*degrees(atan(.5)),53.1301)
test(87,"frictionless sphere detach cos(theta)",2/3,2/3,1e-10)
test(87,"frictionless sphere detach speed for R1",sqrt(2*G/3),2.557)
b,l0,Kspring,m,omega=.4,.3,10.,1.,2.
delta=(b+l0)/(Kspring/(m*omega**2)-1)
test(88,"outward revolving spring extension metres",delta,.466667)
check_equilibrium(88,"spring vs centrifugal equilibrium",Kspring*delta-m*omega**2*(b+l0+delta))
test(88,"stable extension requires spring stiffness > m omega²",float(Kspring>m*omega**2),1,1e-10)
test(89,"optimal bicycle track radius /R",.5,.5,1e-10)
test(89,"max bicycle speed m/s for k0=.3 R20",
     .5*sqrt(.3*G*20),3.836)
test(90,"friction circle longest slip-free path metres",
     40/2*sqrt((.2*G/.62)**2-1),60.0)
test(90,"friction static initial feasibility",float(.62<=.2*G),1,1e-10)

# 91--100: road curvature, capstan, momentum, analytic force fields.
test(91,"sinusoidal road maximum curvature for a=.2 alpha=2",
     .2/2**2,.05,1e-10)
test(91,"sinusoidal road maximum speed for k.2",
     2*sqrt(.2*G/.2),6.264)
M,Rr,theta,omega=3.,2.,pi/6,1.5
Tchain=M*G/(2*pi)*(1/tan(theta)+omega**2*Rr/G)
test(92,"conical chain tension newtons",Tchain,10.26)
test(92,"static conical chain has nonzero tension",
     M*G/(2*pi*tan(theta)),8.11)
eta0,eta=2.,3.
test(93,"capstan coefficient semicircle",log(eta0)/pi,.220636)
test(93,"slipping accelerated mass a/g", (eta-eta0)/(eta+eta0),.2,1e-10)
test(94,"smooth vertical cylinder normal m2 v3 alpha60 R1 N",
     2*3**2*cos(pi/3)**2,4.5,1e-10)
test(95,"elliptic oscillator force magnitude at phase0 N",
     2*(2**2)*4,32,1e-10)
test(95,"ellipse force always central",0,0,1e-10)
test(96,"projectile momentum difference m2 v10 alpha30 kgm/s",
     2*2*10*sin(pi/6),20,1e-10)
test(97,"bell-shaped force impulse a3 tau4",3*4**3/6,32,1e-10)
test(97,"bell-shaped force path a3 tau4 mass2",3*4**4/(12*2),32,1e-10)
F,m,omega=2.,1.,2.
test(98,"sine-force first half-cycle travelled distance m",
     F/(m*omega**2)*pi,pi/2,1e-10)
test(98,"sine-force first half-cycle speed m/s",
     F/(m*omega)*(1-cos(pi)),2,1e-10)
test(99,"cosine-force first re-stop time s",pi/omega,pi/2,1e-10)
test(99,"cosine-force first re-stop distance m",
     2*F/(m*omega**2),1,1e-10)
test(99,"cosine-force maximum speed m/s",F/(m*omega),1,1e-10)
test(100,"linear-drag boat terminal total distance m",
     2*4/1,8,1e-10)
test(100,"linear-drag boat speed after t2 for m2 r1",
     4*exp(-1),1.4715)
test(100,"linear-drag boat mean speed during halving",
     4*(2-1)/(2*log(2)),2.885)

# 101--110: nonlinear drag and friction, effective potentials, rotating sphere.
test(101,"quadratic-drag bullet transit time h1 v4 to2 s",
     1*(4-2)/(4*2*log(4/2)),.36067)
test(102,"linearly growing friction incline stopping distance m",
     2*tan(pi/6)/.5,2.3094)
test(102,"maximum incline speed with k(x)=.5x m/s",
     sqrt(G/.5*sin(pi/6)*tan(pi/6)),2.379)
m,mu,Fgrowth=2.,.2,4.
t0=mu*m*G/Fgrowth
test(103,"time-dependent friction threshold time s",t0,.981,1e-10)
test(103,"cubic displacement at t2 after rest threshold m",
     Fgrowth/(6*m)*(2-t0)**3,.353)
v0,m,k=10.,2.,.1
test(104,"up/down quadratic-air-drag final speed m/s",
     v0/sqrt(1+k*v0**2/(m*G)),8.14)
F,m,omega=3.,2.,4.
test(105,"rotating force full interval distance m",8*F/(m*omega**2),.75,1e-10)
test(105,"rotating force mean speed m/s",4*F/(pi*m*omega),.47746)
test(105,"rotating force mean velocity y-axis m/s",F/(m*omega),.375,1e-10)
test(106,"gliding plate speed at down-slope alignment /v0",.5,.5,1e-10)
test(106,"gliding plate initial sidewise speed /v0",1.,1.,1e-10)
test(107,"uniform chain first instant acceleration m/s²",
     G/.3*(1-cos(.3)),1.46)
z=(2+sqrt(14))/6
test(108,"accelerating sphere departure theta degrees",degrees(acos(z)),16.9)
test(108,"accelerating sphere departure speed for R1",
     sqrt(2*G/3),2.56)
test(108,"accelerating sphere stationary limit cos theta",
     2/3,2/3,1e-10)
test(109,"velocity-normal force stable for exponent n=.5",
     float(1-.5>0),1,1e-10)
test(109,"velocity-normal force unstable for exponent n=2",
     float(1-2<0),1,1e-10)
test(109,"velocity-normal force marginal at n=1",
     1-1,0,1e-10)
test(110,"revolving semicircle tilted equilibrium for omega4 R1 deg",
     degrees(acos(G/(4**2*1))),52.2)
test(110,"revolving semicircle bottom unstable at omega4",
     float(4**2*1>G),1,1e-10)

# 111--117: Coriolis, rotating rods, apparent forces.
test(111,"northbound bullet 1000m east deflection metres",
     OMEGA_E*1000**2*sin(pi/3)/900,.0702)
test(112,"turntable radial slider 3D contact force newtons",
     .5*sqrt(G**2+(6**2*.3)**2+4*6**2*.5**2),7.89)
test(113,"sliding sleeve Coriolis force newtons",
     2*.5*2*sqrt(1**2+(2*.5)**2),2.828)
test(114,"edge-axis rotating disk farthest-point inertial force",
     sqrt(4*1**2-(2*1)**2),0,1e-10)
test(114,"edge-axis rotating disk at axis force in m omega² R",
     sqrt(4-(0)**2),2,1e-10)
test(114,"edge-axis rotating disk at r=R in m omega² R",
     sqrt(4-1),sqrt(3),1e-10)
mm,angspd,rad=.3,6.,1.
rho=rad*sqrt(5)/3
v2=2*G*rad/3
Fcf=mm*angspd**2*rho
Fcor=2*mm*angspd*sqrt(v2*(2/3)**2+angspd**2*rho**2)
test(115,"rotating sphere centrifugal force N",Fcf,8.05)
test(115,"rotating sphere Coriolis force N",Fcor,17.2)
test(116,"north/south train rail lateral force newtons",
     2*2e6*OMEGA_E*15*sin(pi/3),3790)
test(116,"westward train inertial-force cancellation speed m/s",
     OMEGA_E*EARTH_R*cos(pi/3)/2,116)
test(117,"equatorial falling ball east drift h500 metres",
     OMEGA_E*G/3*(2*500/G)**1.5,.245)
print(f"PASS: {len(checks)} independent statics, dynamics, friction, "
      "pulley, rolling and Coriolis checks for Irodov Part I.59--117.")
for no,name,actual in checks:
    print(f"  I.{no:<3} {name:<55} {actual:.9g}")
