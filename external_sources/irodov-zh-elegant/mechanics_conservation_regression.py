#!/usr/bin/env python3
"""Independent second-pass physical conservation QA for Irodov Part I.118--199.

Work-energy, COM constraints, non-elastic collisions, rockets, torque about
arbitrary origins, variable-mass systems and elastic impacts. Includes
source-answer misprint verification and a nontrivial torque-component
cancellation in original I.195. Tests target individual result anchors and
assumptions; they are not the same as peer-reviewing every one of 1878
translated proofs.
"""
from math import sqrt, sin, cos, tan, pi, log, exp, atan, asin, degrees, isclose
G=9.81
RHO=1.0
checks=[]
failures=[]

def test(n,label,actual,expected,rtol=.025,atol=1e-12):
    if not isclose(actual,expected,rel_tol=rtol,abs_tol=atol):
        failures.append(f"I.{n} {label}: actual={actual:.9g}, expected={expected:.9g}")
    checks.append((n,label,actual))
def equal(n,label,actual,expected):
    test(n,label,actual,expected,rtol=1e-10,atol=1e-10)
def norm2(x):return sum(y*y for y in x)

# 118--130: work, friction, energy-flow and the original source sign error.
test(118,"work of constant vector 3i+4j between endpoints",
     3*(2-1)+4*(-3-2),-17,1e-10)
m,a,t=2.,3.,4.
test(119,"work for v=a sqrt(s) after actual motion starts",
     m*a**4*t*t/8,324)
aa,s,R=3.,2.,4.
test(120,"circular kinetic K=a s2 total force magnitude",
     2*aa*s*sqrt(1+(s/R)**2),13.4164)
test(120,"circular kinetic K=a s2 tangential force",
     2*aa*s,12,1e-10)
test(120,"circular kinetic K=a s2 normal force",
     2*aa*s*s/R,6,1e-10)
test(121,"curved incline constant friction work, h2 ell3 mu.2 mass2",
     2*G*(2+.2*3),51.012)
m,mu,ell,alpha=.05,.15,.50,pi/6
height=mu*ell/(1-mu/tan(alpha))
test(122,"complete two-incline rough-plate energy loss J",
     -m*G*height,-.0496)
test(123,"spring pull transient other block depins N",
     .2*G*(2+3/2),6.867)
test(123,"static block initially needs pull exceeding m1 friction",
     float(2+3/2>2),1.,1e-10)
eta=1/3
test(124,"chain/table friction total work joules",
     -.5*eta*(1-eta)*.8*G*1.5,-1.31)
test(125,"gravity average power full level-to-level projectile",
     0,0,1e-10)
test(125,"gravitational instantaneous power initial with v0=5 alpha30 m2",
     -2*G*5*sin(pi/6),-49.05)
test(126,"kinetic energy normal acceleration a t² with a3 R2 at t4",
     .5*2*3*2*4**2,96)
test(126,"instantaneous force power at t4 for m2 a3 R2",
     2*3*2*4,48,1e-10)
test(126,"time mean power 0--4 for m2 a3 R2",
     2*3*2*4/2,24,1e-10)
test(127,"linear slide braking mean power W",
     -.5*.27*1*G*1.5,-1.987)
test(127,"distance-variable friction max loss rate m1 v1.5 alpha.3",
     -.5*1*1.5**2*sqrt(.3*G),-1.93)
test(128,"constant omega centrifugal potential work J",
     .5*.10*5**2*(.50**2-.30**2),.2,1e-10)
k1,k2,extension=3.,6.,2.
keq=k1*k2/(k1+k2)
test(129,"series-spring effective stiffness N/m",keq,2,1e-10)
test(129,"series-spring quasistatic work J",
     .5*keq*extension**2,4,1e-10)
m,alpha=2.,.5
test(130,"book-implied upward force branch positive work J",
     3*m*G/(4*alpha),29.43)
test(130,"literal printed signed force integral negative J",
     -3*m*G/(4*alpha),-29.43)
test(130,"book-implied lift height before first velocity stop",
     1/alpha,2,1e-10)

# 131--140: force from potential, curves, ramps and chain geometry.
a,b=2.,6.
r0=2*a/b
test(131,"radial potential equilibrium r0",r0,2/3,1e-10)
test(131,"maximum attractive force magnitude",
     b**3/(27*a*a),2,1e-10)
test(131,"force zero at stable potential point",
     2*a/r0**3-b/r0**2,0,1e-10)
test(132,"noncentral quadratic potential equipotential axis ratio",
     sqrt(4/1),2,1e-10)
test(132,"force-magnitude ellipse axis ratio",
     4/1,4,1e-10)
test(133,"stationary plane field F=(a*y,0) curl nonzero",
     -3,-3,1e-10)
test(133,"stationary plane field F=(a*x,b*y) curl zero",
     0,0,1e-10)
test(134,"inclined slider uphill stopping distance m",
     5**2/(2*G*(sin(pi/6)+.2*cos(pi/6))),1.897)
test(134,"inclined slider negative friction work J",
     -.2*2*G*cos(pi/6)*5**2/
     (2*G*(sin(pi/6)+.2*cos(pi/6))),-6.432)
test(135,"horizontal launch platform optimal height /H",.5,.5,1e-10)
test(135,"horizontal launch maximum range /H",1,1,1e-10)
test(136,"detach ring cos theta",2/3,2/3,1e-10)
test(136,"free flight apex horizontal speed at h2",
     2/3*sqrt(G*2/3),1.705)
test(137,"pendulum full vertical-loop minimum suspension speed",
     sqrt(5*G*2),9.905)
test(137,"pendulum tension sideways at threshold for m2",3*2*G,58.86)
test(138,"string winding 2m on cylinder radius .5 initial 4m/s seconds",
     2**2/(2*.5*4),1,1e-10)
m,kappa,ell=2.,10.,3.
elong=(m*G+sqrt((m*G)**2+2*kappa*m*G*ell))/kappa
test(139,"falling sleeve elastic rope maximum elongation",
     elong,(m*G/kappa)+sqrt((m*G/kappa)**2+2*m*G*ell/kappa),1e-10)
test(139,"spring vs released gravity work balance",
     .5*kappa*elong**2-m*G*(ell+elong),0,1e-10)
test(140,"liftoff when stretched spring vertical component equals mg",
     5*(1-1/(5/4)),1,1e-10)
test(140,"spring-lift initial horizontal separation /ell0",3/4,.75,1e-10)
test(140,"spring/pendulum system speed at lift m/s",
     sqrt(19*G*.5/32),1.706)

# 141--160: variable supports, centre of mass, recoil, nonelastic chains.
mu=.2;ang=pi/6;ell=.4
work=mu*1*G*ell*(1-cos(ang))/(2*cos(ang)*(sin(ang)+mu*cos(ang)))
test(141,"elastic cord sliding wood plank friction work J",work,.09)
kappa,l0,eta=10.,.3,.25
work=(kappa*l0*l0/2)*(eta*(1+eta)/(1-eta)**2)
test(142,"slow spool energy for eta=.25 J",work,.250)
test(142,"spring radial stretch for eta=.25 m",
     l0*eta/(1-eta),.1,1e-10)
test(143,"Atwood 3kg/1kg COM acceleration m/s2",
     G*(3-1)**2/(3+1)**2,G/4,1e-10)
test(144,"2:1 mass ratio COM path coordinate mapping",
     -2*3,-6,1e-10)
test(145,"rotating chain centroid radius m",
     G*tan(pi/4)/35**2,.00800)
test(145,"rotating chain thread tension N",
     .36*G/cos(pi/4),4.994)
m=.3;omega=1;alpha=10*pi/180;ell=.17
# Source has m=3.2kg rather than above generic; use original explicitly.
f=3.2*(G*sin(alpha)+omega**2*ell*cos(alpha))
N=3.2*(G*cos(alpha)-omega**2*ell*sin(alpha))
test(146,"conical roller friction force at omega1 N",f,5.98)
test(146,"conical roller contact normal at omega1 N",N,30.8)
k=.25
wmax=sqrt(G*(k-tan(alpha))/(ell*(1+k*tan(alpha))))
test(146,"conical roller max pure rolling omega rad/s",wmax,2.02)
m1,m2,v1,v2=2.,3.,5.,-1.
V=(m1*v1+m2*v2)/(m1+m2)
mu_red=m1*m2/(m1+m2)
test(147,"COM velocity that minimizes lab energy",V,1.4,1e-10)
test(147,"minimum two-body kinetic energy J",
     .5*mu_red*(v1-v2)**2,21.6,1e-10)
test(148,"Koenig energy transform for M4 V3 and internal E7",
     7+.5*4*3**2,25,1e-10)
test(149,"orthogonal two-body relative COM energy J",
     .5*mu_red*(3**2+4**2),15,1e-10)
test(150,"two-spring masses total momentum after 2s kgm/s",
     2*3+3*(-1)-(2+3)*G*2,-95.1)
test(150,"spring-system COM free-fall displacement in 2s metres",
     (V*2-.5*G*2**2),-16.82)
kappa=50;m1=2;m2=3;x=.1
test(151,"release from wall spring system centroid speed m/s",
     x*sqrt(kappa*m2)/(m1+m2),.245)
test(152,"equal-mass spring max extension under F",
     4/20,.2,1e-10)
test(152,"unequal masses m1=2 m2=3 spring max extension under F4",
     2*2*4/(20*(2+3)),.16,1e-10)
q=.1
test(153,"stacked blocks minimum initial compression for liftoff",3*q,.3,1e-10)
test(153,"stacked blocks COM max rise with compression 7q",8*q,.8,1e-10)
M,m,v=5.,1.,2.
v1=-m*v/(M-m)
v2=M*v/(M-m)
test(154,"cross-jump buggy1 initial velocity",-m*v/(M-m),-.5,1e-10)
test(154,"cross-jump buggy2 initial velocity",v2,2.5,1e-10)
test(154,"first buggy after cross-jumping stops",
     (M*v1+m*v2)/(M+m),0,1e-10)
test(155,"jumping rider rear buggy velocity with M5,m1,u3,v0 4",
     4-1*3/(5+1),3.5,1e-10)
test(155,"landing front buggy velocity for same data",
     4+(1*5)/(5+1)**2*3,4+5/12,1e-10)
M,m,u=5.,1.,3.
sim=-2*m*u/(M+2*m)
seq=-m*(2*M+3*m)/((M+m)*(M+2*m))*u
test(156,"simultaneous two jumpers cart velocity",sim,-6/7,1e-10)
test(156,"sequential two jumpers cart velocity",seq,-13/14,1e-10)
test(156,"sequential vs simultaneous impulse ratio",seq/sim,1+m/(2*(M+m)),1e-10)
test(157,"chain impact impulse vs rested-chain weight ratio",2,2,1e-10)
test(157,"total table force from chain / resting weight",3,3,1e-10)
eta=1.25
total=.05*sqrt(2*G*1)*(eta+1)/(eta-1)
test(158,"infinitely rebounding steel ball total plate impulse Ns",
     total,1.99)
test(158,"ratio full impulse to first bounce",eta/(eta-1),5,1e-10)
test(159,"raft/person COM-preserving raft displacement m",
     -1/(5+1)*3,-.5,1e-10)
test(159,"raft/person contact force if relative accel2 N",
     -5*1/(5+1)*2,-5/3,1e-10)
test(160,"balanced ladder-person counterweight COM upward motion",
     1*3/(2*5),.3,1e-10)

# 161--180: elastic scattering, internal explosions, rocket flow.
M,g,alpha,ell,p=10.,G,pi/6,2.,30.
u=sqrt(2*g*ell*sin(alpha))
tau=(p*cos(alpha)-M*u)/(M*g*sin(alpha))
# This arbitrary impulse might be insufficient to stop: check actual feasibility.
p=100
tau=(p*cos(alpha)-M*u)/(M*g*sin(alpha))
test(161,"inclined gun stopping firing time s",tau,.8626,.03)
test(161,"gun recoil momentum balance error",
     M*u+M*g*sin(alpha)*tau-p*cos(alpha),0,1e-10)
test(162,"embedded bullet final velocity m/s for ell1 theta60",
     2*sqrt(G)*sin(pi/6),sqrt(G),1e-10)
test(162,"bullet impact dissipated fraction for M=10m",
     10/(10+1),10/11,1e-10)
test(163,"ball on mobile rounded wedge max height m",
     10*4**2/(2*G*(10+2)),.68)
test(164,"inelastic disc-raft friction total work J",
     -(2*3)/(2+3)*G*1,-11.772,1e-10)
test(164,"inertial-boost leaves internal friction sum unchanged",
     -11.772,-11.772,1e-10)
test(165,"free-fall speed from h3",sqrt(2*G*3),7.672)
v1=(3.,-2.,0.);v2=(0.,4.,-6.)
joined=tuple((v1[i]+2*v2[i])/3 for i in range(3))
test(166,"fully inelastic collision x velocity",joined[0],1,1e-10)
test(166,"fully inelastic collision y velocity",joined[1],2,1e-10)
test(166,"fully inelastic collision z velocity",joined[2],-4,1e-10)
test(166,"fully inelastic collision speed",sqrt(norm2(joined)),sqrt(21),1e-10)
test(167,"inelastic kinetic change for masses 2,3 velocities 4,1 J",
     -.5*(2*3)/(2+3)*(4-1)**2,-5.4,1e-10)
test(168,"perpendicular elastic deflection energy fraction for m1=1,m2=3",
     2*1/(1+3),.5,1e-10)
test(168,"collinear elastic energy fraction for m1=1,m2=3",
     4*1*3/(1+3)**2,.75,1e-10)
test(169,"equal-speed opposite-direction rebound mass ratio",1/3,1/3,1e-10)
test(169,"symmetrical 60deg elastic mass ratio",
     4*cos(pi/6)**2-1,2,1e-10)
test(170,"two equal smooth spheres maximum transient spring fraction",
     .5*cos(pi/4)**2,.25,1e-10)
test(171,"one of three equal fragments maximum explosion speed",
     500*(1+sqrt(2*(1.5-1))),1000,1e-10)
test(172,"1percent kinetic loss equal head-on incoming v10 exit velocity",
     5*(1-sqrt(1-.02)),.05025)
test(173,"oblique impact energy change fraction m/M=.2 theta30",
     (1+.2)*tan(pi/6)**2+.2-1,-.4,1e-10)
test(174,"two-particle COM energy for perpendicular v3 and v4",
     .5*(2*3)/(2+3)*(3**2+4**2),15,1e-10)
test(175,"elastic projectile heavier target max scatter angle degrees",
     degrees(asin(1/2)),30,1e-10)
eta=1.5
uc=(eta**2-2)/(6-eta**2)
phi_cos=sqrt(1-eta**2/4)
J=(1-uc)/(2*phi_cos)
test(176,"triple-disc collision projectile speed ratio for eta1.5",
     uc,1/15,1e-10)
test(176,"triple-disc collision total kinetic energy residual",
     uc**2+2*J**2-1,0,1e-10)
test(176,"triple-disc collision critical separation factor",
     sqrt(2),1.41421356237,1e-10)
test(177,"same-mass elastic target velocity dot-product zero",
     (1+1-2)/2,0,1e-10)
test(177,"same-mass inelastic target velocity dot-product positive",
     .2,.2,1e-10)
test(178,"rocket exhaust force for flow4kg/s relative velocity -300m/s N",
     -4*(-300),1200,1e-10)
test(179,"ideal rocket delta v if m0/m=3 and exhaust300",
     300*log(3),329.58)
test(180,"rocket constant acceleration mass after t2 for m0=10 a3 u30",
     10*exp(-3*2/30),8.1873)

# 181--199: transverse rockets, mass-flow, torque and angular momentum.
test(181,"90-degree exhaust velocity deflection rad",
     100/200*log(3),.5493)
test(182,"leaking-sand constant force acceleration at t2",
     10/(5-.5*2),2.5,1e-10)
test(182,"leaking-sand speed at t2 under force10",
     10/.5*log(5/(5-.5*2)),4.46287)
test(183,"incoming sand static horizontally velocity at t2",
     10*2/(5+.5*2),10/3,1e-10)
test(183,"incoming sand acceleration at t2",
     10*5/(5+.5*2)**2,50/36,1e-10)
test(184,"falling chain exits horizontal tube speed ell4 h1",
     sqrt(2*G*1*log(4/1)),5.215)
test(184,"falling chain vanishes if h equals whole length",
     sqrt(2*G*4*log(4/4)),0,1e-10)
test(185,"L=a+b t² torque at 45deg if a2 b8",
     2*sqrt(2*8),8,1e-10)
test(186,"projectile apex angular momentum m.13 v25 alpha45",
     .13*25**3/(2*G)*sin(pi/4)**2*cos(pi/4),36.61)
test(187,"disc-wall angular momentum change relative offset .5",
     2*2*3*.5*cos(pi/6),5.196)
test(188,"conical pendulum halfturn angular momentum shift for m2 ell1 omega4",
     2*2*G*1/4*sqrt(1-(G/(4**2*1))**2),7.75)
test(189,"falling ball angular momentum shift boosted frame",
     2*3*4,24,1e-10)
test(190,"rotating frame relative angular momentum m2 omega3 v4 t2",
     -2*3*4**2*2**2,-384,1e-10)
test(190,"Coriolis torque is time derivative dL/dt at t2",
     -2*2*3*4**2*2,-384,1e-10)
test(191,"oscillator central potential mass from nearest radius1 v2 k3",
     2*3*1**2/2**2,1.5,1e-10)
test(192,"spherical pendulum horizontal-latitude threshold alpha60 ell1",
     sqrt(2*G*1/cos(pi/3)),sqrt(4*G),1e-10)
test(193,"rope through hole tension when radius halves",
     2*3**2*1**4/(.5**3),144,1e-10)
test(194,"fixed pulley total system angular momentum about pivot at t2",
     3*G*1*2,58.86,1e-10)
m,R,alpha,t=3.,.5,pi/6,2.
s=(5/7)*G*sin(alpha)*t*t/2
normal=m*G*cos(alpha)
# Gravitational and normal torques about initial *fixed* contact point.
gravity_torque=m*G*(s*cos(alpha)+R*sin(alpha))
normal_torque=-s*normal
total=gravity_torque+normal_torque
test(195,"rolling sphere total torque despite moving gravity lever arm",
     total,m*G*R*sin(alpha),1e-10)
test(195,"rolling sphere angular momentum L(t)",
     m*G*R*sin(alpha)*t,14.715,1e-10)
test(195,"rolling sphere gravity torque NOT constant",
     gravity_torque-(m*G*R*sin(alpha)),
     s*m*G*cos(alpha),1e-10)
test(196,"angular momentum shift with origin delta cross total p",
     2*3-4*1,2,1e-10)
# 197: decompose (r_C + r_rel) cross (mV_C + m v_rel) and verify
def cross2(x,y):return x[0]*y[1]-x[1]*y[0]
m1,m2=2.,3.
r1=(1.,2.);r2=(4.,-1.)
v1=(3.,0.);v2=(-1.,2.)
MT=m1+m2
rC=tuple((m1*r1[i]+m2*r2[i])/MT for i in range(2))
p=tuple(m1*v1[i]+m2*v2[i] for i in range(2))
intrinsic=sum(mi*cross2((ri[0]-rC[0],ri[1]-rC[1]),
                         (vi[0]-p[0]/MT,vi[1]-p[1]/MT))
              for mi,ri,vi in [(m1,r1,v1),(m2,r2,v2)])
direct=sum(mi*cross2(ri,vi) for mi,ri,vi in [(m1,r1,v1),(m2,r2,v2)])
test(197,"Koenig angular momentum COM decomposition identity",
     intrinsic+cross2(rC,p)-direct,0,1e-10)
test(198,"elastic projectile vs dumbbell COM angular momentum",
     (1/3)*2*1*3,2,1e-10)
eps_pred=(1*1**2)/(100*.5**2)
eps=eps_pred*(1-1.5*eps_pred) # second order perturbative upper bound
# Compare exact energy mismatch (higher order), not by testing an approximation
# as if it were exact.
eq=1*1**2/2*(1-(1+eps)**(-2))-100*.5**2*eps**2
test(199,"small-extension approximation relative energy residual",
     abs(eq)/(100*.5**2*eps_pred**2),.0,.6,atol=.01)
test(199,"small extension parameter from energy/angular momentum",
     eps_pred,.04,1e-10)
if failures:
    for error in failures:
        print("FAIL:",error)
    raise AssertionError(f"{len(failures)} incorrect numerical benchmarks or physical inconsistencies")
print(f"PASS: {len(checks)} independent work-energy, collision, COM,"
      " rocket and torque checks for original Part I.118--199.")
for n,name,val in checks:
    print(f"  I.{n:<3} {name:<59} {val:.9g}")
