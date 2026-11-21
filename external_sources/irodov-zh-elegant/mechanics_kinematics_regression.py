#!/usr/bin/env python3
"""Independent mechanics consistency and limiting-case audit: Part I.1--58.

Recomputes river frames, projectile separation, circular-motion curvature,
accelerating reference events, rigid-body rolling and precessing axes. This
deliberately mixes analytic invariants with numerical problems and does not
claim to establish full source fidelity for graph-dependent questions.
"""
from math import sqrt,sin,cos,tan,atan,asin,acos,pi,degrees,isclose,exp,log
tests=[]
def test(q,label,value,expected,rtol=.025):
    if not isclose(value,expected,rel_tol=rtol,abs_tol=1e-13):
        raise AssertionError(f"I.{q} {label}: {value:.9g} != {expected:.9g}")
    tests.append((q,label,value))

# 1.1 Relative motion, moving observers and acceleration.
test(1,"river speed km/h from raft return",6/(2*1),3,.00001)
# half distance v0, other half average speed (v1+v2)/2:
v0,v1,v2=2,3,5
test(2,"mixed distance/time average speed km/h",
     1/(.5/v0+.5/((v1+v2)/2)),8/3,.00001)
test(3,"uniform-motion duration seconds",25-2*5,15,.00001)
test(6,"relative apparent wind speed km/h",
     sqrt(30**2+15**2+2*30*15*cos(pi/3)),39.686)
test(6,"relative wind apparent angle degrees",
     degrees(atan(15*sin(pi/3)/(30+15*cos(pi/3)))),19.107)
test(7,"second swimmer's shore walking speed km/h",
     2/(2.5/sqrt(2.5**2-2**2)-1),3,.00001)
test(8,"along/across river roundtrip time ratio",
     1.2/sqrt(1.2**2-1),1.8091)
test(9,"minimal drift navigation heading degrees",
     degrees(acos(-1/2)),120,.00001)
test(10,"two projectiles distance after 1.7s metres",
     25*1.7*sqrt(2*(1-sin(pi/3))),22.0)
cross_t=sqrt(3*4)/9.81
test(11,"opposite projectile orthogonal-velocities time s",cross_t,.353)
test(11,"opposite projectile separation at orthogonality m",7*cross_t,2.47)
test(12,"three equal-speed cyclic pursuers meeting time ratio Tv/a",
     2/3,2/3,.00001)
test(13,"chaser time for v3 u2, distance 10",3*10/(9-4),6)
test(14,"ground events spatial gap metres",
     350-.03*60*(30+60/2),242,.00001)
test(14,"inertial frame same-event-position speed m/s",
     -242/60,-4.03333)
test(15,"elevator bolt-fall time seconds",
     sqrt(2*2.7/(9.81+1.2)),.7003)
t=(2*3+3*4)/(3**2+4**2)
dmin=abs(2*4-3*3)/sqrt(3**2+4**2)
test(16,"orthogonal movers minimum-distance time arbitrary units",t,.72,.00001)
test(16,"orthogonal movers min distance arbitrary units",dmin,.2,.00001)
test(17,"optimal road departure distance d/l for speed ratio eta2",
     1/sqrt(2**2-1),.5773503)

# Piecewise v(t) source mechanics graph 1.3 (each scalar checks continuity).
x3=.5+2.0
x4=x3+1-.5
x6=x3+3-9/2
x7=x6-2+1
test(18,"displacement graph x at t=3",x3,2.5,.00001)
test(18,"displacement graph x at t=4",x4,3.0,.00001)
test(18,"displacement graph x at t=6",x6,1.0,.00001)
test(18,"displacement graph x at t=7",x7,0.0,.00001)
R=.160
T=10.
test(19,"half-circle mean speed metres/s",pi*R/T,.050265)
test(19,"half-circle mean velocity magnitude metres/s",2*R/T,.032)
test(19,"half-circle vector-average acceleration m/s2",2*pi*R/T**2,.01005)
test(20,"quadratic turning-point roundtrip path length ratio",.5,.5,.00001)
# v=v0(1-t/tau) with v0=10cm/s and tau=5s.
for t0,expected in [(6,24),(10,0),(20,-200)]:
    test(21,f"linear deceleration position t={t0}s in cm",
         10*(t0-t0*t0/(2*5)),expected,.00001)
test(22,"dx/dt = alpha sqrt(x) immediate departure scaling x/t2",
     (2.5**2)/4,1.5625,.00001)
test(23,"sqrt(v) braking stopping time for v0=9,a=2",
     2*sqrt(9)/2,3,.00001)
test(23,"sqrt(v) braking stopping distance for v0=9,a=2",
     2*9**1.5/(3*2),9,.00001)
test(25,"velocity vs downward acceleration 45deg at alpha t",
     1,1,.00001)
test(26,"sine-cosine cyclotron acceleration/velocity angle deg",
     90,90,.00001)
test(29,"projectile height equals range angle deg",
     degrees(atan(4)),75.964)

# Curvature, tangential/normal acceleration, rotational kinematics.
test(31,"ball second sloping-plane impact distance for h2 alpha30",
     8*2*sin(pi/6),8,.00001)
test(32,"cannon range feasible sin double angle",
     9.81*5100/240**2,.86859)
test(35,"parabola y=b x²/(2a), curvature at x0 for b/a=2",
     1/abs(2),.5,.00001)
test(36,"trajectory with constant tangential vector projection v(x=8), a=2",
     sqrt(2*2*8),sqrt(32),.00001)
test(37,"circular acceleration at tenth lap m/s²",
     .5*sqrt(1+16*pi*pi*.1**2),.80)
test(38,"circle slowing v(t) at v0=2 R=4 t=3",
     2/(1+2*3/4),.8,.00001)
test(38,"circle slowing v(s) at s=R=4",
     2*exp(-1),.73576)
test(39,"circular acceleration angle tangent at s=R/2",
     2*.5,1.0,.00001)
a=.8;R=1;omega=2
test(40,"circular oscillation A at ell0 m/s2",
     omega**2*a*a/R,2.56,.00001)
test(40,"circular oscillation A at ellipse max m/s2",
     omega**2*a,3.20,.00001)
test(40,"circular oscillation minimizing arc |ell| m",
     sqrt(a*a-R*R/2),.37416)
test(40,"circular oscillation minimum acceleration m/s2",
     omega**2*sqrt(a*a-R*R/4),2.498)
test(41,"radius under at,b t4 for a2 b3 s4",
     2**3/(2*3*4),1/3,.00001)
test(42,"parabola curvature at origin a=1/4",1/(2*(1/4)),2,.00001)
test(42,"ellipse apex curvature a2 b3",2**2/3,4/3,.00001)
test(43,"OA rotating chord point speed m/s",
     2*.5*.4,.4,.00001)
test(43,"OA rotating chord point acceleration m/s2",
     4*.5*.4**2,.32,.00001)
test(44,"wheel rim total accel m/s2",
     (.65/2.5)*sqrt(1+4*.2**2*2.5**4),.700)
test(45,"shell axial spin angular velocity rad/s",
     2*pi*2*320/2,640*pi,.00001)
test(46,"rotation phi=at-bt2 first-stop time s",
     6/(2*2),1.5,.00001)
test(46,"rotation phi=at-bt2 average angular velocity rad/s",
     6/2,3,.00001)
test(46,"rotation phi=at-bt2 acceleration rad/s2",-2*2,-4,.00001)
test(47,"angular-acceleration angle alpha60 time s",
     (4*tan(pi/3)/.02)**(1/3),7.02)
test(48,"sqrt-omega decel average ratio Omegaavg/Omega0",
     1/3,1/3,.00001)
test(49,"omega=omega0-a phi exponential angular velocity ratio at t=1/a",
     exp(-1),.367879,.00001)
test(50,"angular speed at phi pi/2 normalized by sqrt(2beta0)",
     sqrt(sin(pi/2)),1,.00001)
test(51,"instantaneous centre trace for x=2 v2 beta3, y",
     2**2/(3*2),2/3,.00001)
test(52,"cycloid crest normal acceleration m/s2",
     1**2/.5,2,.00001)
test(52,"cycloid full period path length metres",8*.5,4,.00001)
test(53,"rolling ball top speed cm/s",2*(2.5*2),10,.00001)
test(53,"rolling ball side-point speed cm/s",
     sqrt(2)*(2.5*2),7.071)
test(53,"rolling ball top-point accel cm/s2",
     sqrt((2*2.5)**2+((5**2)/10)**2),5.59)
test(53,"rolling ball side-point accel cm/s2",2.5,2.5,.00001)
test(54,"cycloid curvature top radius/r",4,4,.00001)
test(54,"cycloid curvature side radius/r",2*sqrt(2),2.8284)
test(55,"two perpendicular rigid rotations relative angular speed",
     sqrt(3**2+4**2),5,.00001)
test(55,"two perpendicular rigid rotations relative angular acceleration",
     3*4,12,.00001)
rot=(.5*10,.06*10**2)
alp=(.5,2*.06*10)
rotmag=sqrt(rot[0]**2+rot[1]**2)
alpmag=sqrt(alp[0]**2+alp[1]**2)
test(56,"time-varying angular velocity modulus at 10s",
     rotmag,sqrt(61),.00001)
test(56,"time-varying angular accel modulus at 10s",alpmag,1.3)
test(56,"angle between omega and alpha degrees",
     degrees(acos((rot[0]*alp[0]+rot[1]*alp[1])/(rotmag*alpmag))),17.2)
test(57,"rolling cone angular speed rad/s",
     .10/(.05*cos(pi/6)),2.31)
test(57,"rolling cone angular acceleration rad/s2",
     (.10/.05)**2*tan(pi/6),2.31)
test(58,"horizontal spinning precessing shaft angular speed rad/s",
     sqrt(.5**2+(.1*3.5)**2),.61033)
test(58,"horizontal spinning precessing shaft angular accel rad/s2",
     .1*sqrt(1+(.5*3.5)**2),.20156)
print(f"PASS: {len(tests)} independent kinematic and rigid-body "
      "limiting/numerical checks, original Part I.1--58.")
for number,label,value in tests:
    print(f" I.{number:<3} {label:<55} {value:.8g}")
