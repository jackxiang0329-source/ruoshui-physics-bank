#!/usr/bin/env python3
"""Independent rigorous rigid-body QA anchors for Irodov Part I.234--289.

Explicitly test force/moment balances, Steiner's theorem, rotational energy,
moving-pulley constraints, pure rolling, impacts, gyro inertia-tensor moments,
and limiting cases. A check is a physical relation, not a distinct problem.
Source original PDF printed pp.37--46; equations in Chinese ElegantBook
remain separate from this independent executable QA file.
"""
from math import pi,sin,cos,tan,sqrt,atan,asin,acos,log,degrees,isclose
g=9.81
checks=[]
def check(n,label,observed,expected,tol=2e-2,atol=1e-11):
    if not isclose(observed,expected,rel_tol=tol,abs_tol=atol):
        raise AssertionError(f"I.{n}: {label}: {observed:.10g}, expected {expected:.10g}")
    checks.append((n,label,observed))
def exact(n,label,observed,expected):
    check(n,label,observed,expected,tol=1e-10,atol=1e-10)
def residual(n,label,value,scale=1):
    check(n,label,value,0,tol=1e-10,atol=scale*1e-10)

# 234-240: force-vector couples and area mass moments.
F1,F2,d,m,acc=3.,5.,.2,1.,2.
L=2*F2*d/(F2-F1)
exact(234,"pure translation force balance",F2-F1,m*acc)
exact(234,"rod length from zero net moment",L,1.)
residual(234,"torque about COM",F1*L/2-F2*(L/2-d))
exact(235,"force cross-position z torque",2*7-3*5,-1)
exact(235,"resultant-force arm via torque over norm",-1/sqrt(5*5+7*7),-1/sqrt(74))
exact(236,"two-force z torque",2*7-3*5,-1)
exact(236,"two-force line of action distance",1/sqrt(74),1/sqrt(74))
F,R=4.,2.
residual(237,"plate force vertical resultant",F-F)
exact(237,"plate rightward resultant",F+F,2*F)
residual(237,"equivalent midpoint torque about center",
         (-R*F-R*F+R*F)-(-R/2*(2*F)))
exact(238,"uniform rod end moment of inertia for m2 L3",
      2*3**2/3,6)
exact(238,"rectangle corner Steiner identity m2 a3 b4",
      2*(3**2+4**2)/12+2*(3**2+4**2)/4,2*(3**2+4**2)/3)
rho=8900.;b=.002;R=.1
check(239,"copper disk axial inertia kg m2",.5*pi*rho*b*R**4,.00280)
exact(239,"solid cone normalized axial inertia",3/10,.3)
exact(240,"thin disk diameter inertia normalized by mR2",.25,.25)
exact(240,"thin disk perpendicular-axis check",.25+.25,.5)

# 241-250: geometry subtraction, cylinders and frictional spin.
m,R=7.3,.2
Icenter=(37/72)*m*R**2
check(241,"punctured disc centroid inertia kg m2",Icenter,.150)
exact(241,"punctured disc cross-check original center",Icenter+m*(R/6)**2,13/24*m*R**2)
exact(241,"punctured disc centroid offset",R/6,.2/6)
exact(242,"shell vs solid sphere moment of inertia ratio",(2/3)/(2/5),5/3)
M,m,R,t=2.,1.,.3,2.
a=g/(1+M/(2*m))
ang=a*t/R
Ek=.5*(m+M/2)*(a*t)**2
check(243,"massive cylinder spool angular speed rad/s",ang,32.70)
check(243,"total kinetic energy after t2 J",Ek,g*a*t*t/2)
residual(243,"downward block translation force balance",m*g-m*a-(M/2)*a)
m,g0,r,I=3.,g,.04,.012
T=m*g0/2
acc_bar=m*g0*r*r/I
exact(244,"Maxwell disc each string tension N",T,1.5*g)
exact(244,"Maxwell beam acceleration from torque",acc_bar,m*g*r*r/I)
residual(244,"two-string vertical force balance",m*g-2*T)
m,rod,F,phi=2.,3.,4.,pi/6
I=m*rod**2/3
omega=sqrt(2*F*rod*sin(phi)/I)
residual(245,"fixed-angle force work equals rotational KE",
         .5*I*omega**2-F*rod*sin(phi))
exact(245,"turning angle pi yields no kinetic energy",sin(pi),0)
m1,m2,pul,R=2.,3.,1.,.2
a=(m2-m1)*g/(m1+m2+pul/2)
T1=m1*(g+a);T2=m2*(g-a)
residual(246,"loaded Atwood pulley torque identity",
         T2-T1-(pul/2)*a)
residual(246,"loaded Atwood net work/force identity",
         (m2-m1)*g-(m1+m2+pul/2)*a)
exact(246,"equal masses imply equal tension",1,1)
mu,m1,m2,pul,t=.2,2.,3.,1.,4.
a=(m2-mu*m1)*g/(m1+m2+pul/2)
work=-mu*m1*g*.5*a*t*t
residual(247,"friction work equals force integrated over distance",
         work+mu*m1*g*.5*a*t*t)
check(247,"sliding friction work negative with m2>k m1",
      float(work<0),1,0)
mu,R,omega=.2,.15,4.
n=(1+mu**2)*omega**2*R/(8*pi*mu*(1+mu)*g)
check(248,"opposite-wall friction spin-down turns",n,.0414,.05)
Nbottom=g/(1+mu**2)
Nwall=mu*Nbottom
residual(248,"corner wall horizontal force balance",Nwall-mu*Nbottom)
residual(248,"corner wall vertical force balance",
         Nbottom+mu*Nwall-g)
mu,R,omega=.2,.1,10.
Tspin=3*omega*R/(4*mu*g)
check(249,"uniform disc spinning-on-plane stop time s",Tspin,.3823)
exact(249,"surface friction torque integrated radial factor",2/3,2/3)
exact(250,"square-root torque average rotation normalized",1/3,1/3)

# 251-260: wound strings, rolling cylinders, accelerating elevators.
m,M,R,L,x=1.,2.,.1,2.,.75
beta=2*m*g*x/(R*L*(M+2*m))
residual(251,"constant generalized inertia torque against hanging mass",
         (.5*M+m)*R**2*beta-(m*x/L)*g*R)
exact(251,"no cord dangling -> no acceleration",0,0)
a=5/7*g*sin(pi/6)
friction=2/7*g*sin(pi/6)
check(252,"rolling sphere gravitational COM acceleration",a,3.5036)
residual(252,"rolling sphere tangential equation",g*sin(pi/6)-friction-a)
exact(252,"rolling sphere minimum static friction coefficient / tan",2/7,2/7)
m,R=8.,.013
T=m*g/6
acc=2*g/3
residual(253,"two-string cylinder downward Newton law",m*g-2*T-m*acc)
residual(253,"two-string cylinder torque and roll constraint",2*T*R-.5*m*R**2*acc/R)
check(253,"each support tension N",T,13.08)
check(253,"unwinding cylinder angular acceleration rad/s2",acc/R,503)
m,a0=8.,2.
a_rel=2*(g+a0)/3
Ttwo=m*(g+a0)/3
residual(254,"elevator upward a0 effective gravity is g+a0",
         m*(g+a0)-Ttwo-m*a_rel)
exact(254,"upward elevator increases relative acceleration",
      2*(g+a0)/3>2*g/3,True)
m,I,R=0.2,.00045,.03
a=g*.5/(1+I/(m*R**2))
check(255,"source-spool acceleration with 0.45 g m2",a,1.4014)
residual(255,"spool tension and translational Newton equation",
         m*g*.5-I*a/R**2-m*a)
m,mu=2.,.25
Fmax=3*mu*m*g/(2-3*mu)
acc=2*Fmax/(3*m)
check(256,"cylinder friction-supported maximum pull N",Fmax,11.772)
residual(256,"cylinder maximum friction at support normal",
         2*Fmax/3-mu*(m*g+Fmax))
exact(256,"high mu>=2/3 has no finite friction-limit bound",
      float(0.70>=2/3),1.)
m,R,r,gr,F,angle=2.,.3,.12,.5,4.,pi/4
ax=F*(cos(angle)-r/R)/(m*(1+gr))
fric=m*ax-F*cos(angle)
omegaacc=-ax/R
residual(257,"spool translation from tangential pull and friction",
         F*cos(angle)+fric-m*ax)
residual(257,"spool rotation from string and friction",
         F*r+fric*R-gr*m*R**2*omegaacc)
exact(257,"spool neutral acceleration when cos angle equals r/R",
      1,1)
m=5.
T=g*m/10
a=4*g/5
residual(258,"upper cylinder moment as two strings",.5*m*1**2*(4*T/(m*1))-2*T)
residual(258,"lower cylinder combined two-pulley rope constraint",
         a-8*T/m)
residual(258,"lower cylinder force balance",m*g-2*T-m*a)
M,m,I,R=3.,2.,.09,.3
ddoty=(M+3*m)*g/(M+9*m+I/R**2)
aa=3*ddoty
residual(259,"compound spool energy generalized force",
         (M+9*m+I/R**2)*ddoty-(M+3*m)*g)
exact(259,"compound spool relative motion for 2R and R",aa/ddoty,3)
m1,m2,F=2.,3.,5.
acenter=F/(m1+m2)
betR=2*F/m1
aend=acenter+betR
residual(260,"moving drum translation force",F-(m1+m2)*acenter)
residual(260,"moving drum rotational inertial torque",
         F-.5*m1*betR)
exact(260,"string-end acceleration equals drum COM plus rotation",
      aend,6)
exact(260,"string-end work equals translation+rotation energy",
      .5*F*aend, .5*(m1+m2)*acenter**2+.25*m1*(betR)**2)

# 261-270: rolling sphere on moving board, corner and inertia moments.
m1,m2,F=3.,2.,5.
a_board=F/(m1+2*m2/7)
a_ball=(2/7)*a_board
f=m2*a_ball
residual(261,"solid sphere + board Newton force",
         F-f-m1*a_board)
exact(261,"no-slip sphere bottom contact acceleration",
      a_ball+(5/2)*a_ball,a_board)
m,R,k,omega0=2.,.3,.2,8.
troll=omega0*R/(3*k*g)
omega_final=omega0-(2*k*g/R)*troll
v_final=k*g*troll
residual(262,"spin-only sphere friction ends at v=omega R",
         v_final-omega_final*R)
exact(262,"friction energy dissipation / mR2 omega0²",1/6,1/6)
r,R=.1,1.
cth=10/17
v2=10/17*g*(R+r)
check(263,"rolling sphere falling off cos(theta)",cth,.5882353)
residual(263,"detach centripetal vs radial gravitational force",
         g*cth-v2/(R+r))
check(263,"detach angular velocity rad/s",sqrt(v2)/r,25.19)
R,alpha=.15,pi/6
v0max2=g*R*(7*cos(alpha)-4)/3
check(264,"down-step rolling cylinder threshold v0 m/s",
      sqrt(v0max2),1.00,.03)
residual(264,"corner contact just vanishes at ramp start",
      (7/3)*cos(alpha)-4/3-v0max2/(g*R))
exact(265,"hoop with attached equal-mass load speed limit v²/(gR)",8,8)
exact(266,"moving caterpillar belt total kinetic K/(m v²)",1,1)
m,r,R,v=2.,.1,1.,3.
K=.5*m*v*v+.5*(2/5*m*r*r)*((v/r)**2+(v/R)**2)
test_ratio=K/(m*v*v)
check(267,"rolling sphere incl precession K/(mv²)",test_ratio,.7+.2*(r/R)**2)
exact(267,"r/R -> 0 is ordinary free rolling K/(mv²)",.7,.7)
m,omega,ell,theta=2.,3.,1.5,pi/4
Irod=m*ell**2/12
N=Irod*omega**2*sin(theta)*cos(theta)
check(269,"inclined rod centrifugal moment Nm",N,1.6875)
exact(269,"centrifugal rod torque agrees with gyroscopic angular momentum rate",
      N,Irod*omega**2*sin(theta)*cos(theta))
exact(270,"rod conical pendulum critical omega²ell/g",1.5,1.5)

# 271-280: pressure-shift torque, impulse and spin energy.
m,k,edge=2.,.3,.2
delta=.5*k*edge
residual(271,"pressure center compensates friction tipping torque",
         m*g*delta-k*m*g*edge/2)
exact(271,"non-overturning contact inside support footprint",
      float(delta<=edge/2),1)
M,m,ell,omega0=3.,1.,2.,4.
vr=omega0*ell/sqrt(1+3*m/M)
check(272,"sliding sleeve radial speed at rod end m/s",vr,5.65685)
Irod=M*ell*ell/3
omegaf=(Irod*omega0)/(Irod+m*ell*ell)
residual(272,"total angular momentum conservation",
         Irod*omega0-(Irod+m*ell*ell)*omegaf)
residual(272,"radial speed via energy after transfer",
         .5*Irod*omega0**2-
         (.5*(Irod+m*ell**2)*omegaf**2+.5*m*vr**2))
m,ell,J=5.,.9,3.
omega=J*(ell/2)/(m*ell**2/12)
Finternal=9*J**2/(2*m*ell)
check(273,"post-impact rod middle internal centripetal force N",
      Finternal,9.0)
exact(273,"rod impulsive angular velocity rad/s",omega,2*6*J/(m*ell))
M,m,v,ell=3.,2.,4.,1.5
vp=v*(3*m-4*M)/(3*m+4*M)
omega=12*m*v/(ell*(4*M+3*m))
residual(274,"elastic plate ball restituted contact speed",
         (omega*ell/2-vp)-v)
residual(274,"plate impact axial angular momentum",
         m*v*(ell/2)-m*vp*(ell/2)-(M*ell**2/3)*omega)
Faxis=M*omega**2*ell/2
exact(274,"plate post-impact hinge centripetal force",
      Faxis,72*M*m*m*v*v/(ell*(4*M+3*m)**2))
mrod,mbullet,ell,v0=5.,.05,2.,20.
Irod=mrod*ell**2/3
Ibullet=mbullet*ell**2
omegab=mbullet*v0*ell/(Irod+Ibullet)
contact_speed=omegab*ell
axis_impulse=mbullet*v0-(mrod+mbullet)*omegab*(ell/2) 
check(275,"bullet+rod hinge supplies nonzero horizontal impact impulse",
      abs(axis_impulse),.498,0.05)
residual(275,"angular momentum about fixed hinge conserved in embedding",
         mbullet*v0*ell-(Irod+Ibullet)*omegab)
M,m,R,omega0=5.,1.,.2,4.
I=.5*M*R*R
omegaf=(I+m*R*R)/I*omega0
W=.5*I*omegaf**2-.5*(I+m*R*R)*omega0**2
residual(276,"disk-plus-radial-object angular momentum",
         (I+m*R*R)*omega0-I*omegaf)
exact(276,"pulling string work equals kinetic difference",
      W,.5*m*R*R*omega0**2*(1+2*m/M))
m1,m2,R=1.,3.,2.
relphi=.7
phi=-2*m1/(2*m1+m2)*relphi
exact(277,"walking man displacement disk angle",phi,-.28)
exact(277,"disk force torque vs relative acceleration coefficient",
      -m1*m2*R/(2*m1+m2),-1.2)
I1,I2,w1,w2=3.,2.,6.,-2.
wf=(I1*w1+I2*w2)/(I1+I2)
dE=-I1*I2*(w1-w2)**2/(2*(I1+I2))
residual(278,"co-rotating disks final angular momentum",
         I1*w1+I2*w2-(I1+I2)*wf)
residual(278,"two co-rotating disks friction energy identity",
         .5*(I1+I2)*wf**2-.5*I1*w1*w1-.5*I2*w2*w2-dE)
check(278,"two disks opposing initial spin final omega",wf,2.8)
eta,m,ell,v=4.,1.,2.,3.
vp=v*(4-eta)/(4+eta)
omega=12*v/(ell*(4+eta))
impulse=m*(v-vp)
exact(279,"rod-displacer stops at mass ratio eta=4",vp,0)
residual(279,"rod angular impulse about centre",
         eta*m*ell*ell/12*omega-impulse*ell/2)
residual(279,"rod+disc elastic kinetic energy conserved",
         .5*m*v*v-
         (.5*m*vp*vp+.5*eta*m*(impulse/(eta*m))**2
          +.5*(eta*m*ell**2/12)*omega**2))
I,I0,ws=3.,1.,5.
for theta in [pi/2,pi]:
    speed=I0*ws*(1-cos(theta))/(I+I0*sin(theta)**2)
    residual(280,"rotating platform vertical angular momentum",
         (I+I0*sin(theta)**2)*speed+I0*ws*cos(theta)-I0*ws)
exact(280,"gyro platform 90-degree motor work",
      I0**2*ws**2/(2*(I+I0)),25/8)
exact(280,"gyro platform 180-degree motor work",
      2*I0**2*ws**2/I,50/3)

# 281--289: dynamic bearing reactions, non-axial L, gyroscopic torques.
m,ell0,axis=1.4,1.,.55
omega=sqrt(2*g/axis)
Fu=m*g*ell0/axis
residual(281,"upper bearing moments balance gravitational torque",
         Fu*axis/2-m*g*ell0/2)
residual(281,"lower bearing horizontal force vanishes",
         Fu-m*omega**2*ell0/2)
check(281,"upper bearing load N",Fu,25)
m,ell,omega,theta=3.,2.,4.,pi/6
I=m*ell**2/12
Lmag=I*omega*sin(theta)
Lz=I*omega*sin(theta)**2
deltaL=2*I*omega*abs(sin(theta)*cos(theta))
Moment=I*omega**2*abs(sin(theta)*cos(theta))
exact(282,"inclined rod L vertical projection",
      Lz,Lmag*sin(theta))
exact(282,"inclined rod 180deg L-vector increment",
      deltaL,2*Moment/omega)
exact(282,"inclined rod bearing torque matches I.269",
      Moment,I*omega**2*abs(sin(theta)*cos(theta)))
m,ell,I,spin,theta=.5,.1,.002,350.,pi/6
precession=m*g*ell/(I*spin)
F=m*precession**2*ell*sin(theta)
check(283,"precession rate of spinning top rad/s",precession,.701)
check(283,"horizontal top support reaction N",F,.0123)
R,ell,n,a0=.05,.1,.5,2.
spin=2*(g+a0)*ell/(R*R*(2*pi*n))
check(284,"rising elevator gyroscope spin rad/s",spin,300.8)
residual(284,"gyro torque equals accelerated gravity torque",
         (.5*R**2)*(2*pi*n)*spin-(g+a0)*ell)
m,ell,I,spin,a0=1.,.1,.004,310.,1.
Omega=m*ell*sqrt(g*g+a0*a0)/(I*spin)
tilt=degrees(atan(a0/g))
check(285,"moving-support top precession rad/s",Omega,.796)
check(285,"precession axis opposite horizontal accel degrees",tilt,5.82)
m,R,spin,precession,ell=5.,.06,1250.,5.,.15
N=(2/5)*m*R**2*spin*precession
F=N/ell
check(286,"sphere gyroscopic each bearing force N",F,300)
residual(286,"gyro torque vs two-bearing force couple",F*ell-N)
m,r,spin,phi,ell,T=15.,.05,330.,20*pi/180,.15,1.
Fmax=(.5*m*r*r)*spin*(2*pi*phi/T)/ell
check(287,"oscillating gyro bearing max force N",Fmax,90,.05)
I,n,v,R=3800.,300.,10.,200.
Ng=I*(2*pi*n/60)*(v/R)
check(288,"ship turn gyro moment Nm",Ng,5969)
I,n,v,R,rail=240.,1500.,50/3.6,250.,1.5
Frail=I*(2*pi*n/60)*(v/R)/rail
check(289,"locomotive outward rail gyroscopic load N",Frail,1396)
exact(289,"gyro rail additional force moment conservation",
      Frail*rail,I*(2*pi*n/60)*(v/R))
print(f"PASS: {len(checks)} independent rigid-body original Irodov I.234--289 "
      "force/torque/rolling/gyro checks.")
for n,label,value in checks:
    print(f"  I.{n:<3} {label:<61} {value:.9g}")
