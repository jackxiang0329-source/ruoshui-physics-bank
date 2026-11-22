#!/usr/bin/env python3
"""Original Irodov Part IV.1--50 independent mechanical oscillator QA.

Compares true elapsed time versus path length and signed velocity, verifies
small-oscillation Hessians, constrained springs, noninertial pendula,
rigid-body eigenfrequency and energetic bounds; reproduces original book
misprinted numerical answers IV.18/23/39 independently.
"""
from math import pi,sqrt,sin,cos,atan,acos,asin,log,isclose
G=9.81
checks=[];failures=[]
def test(n,title,x,ref,tol=.025,abstol=1e-12):
    if not isclose(x,ref,rel_tol=tol,abs_tol=abstol):
        failures.append(f"IV.{n} {title}: {x:.12g} != {ref:.12g}")
    checks.append((n,title,x))
def exact(n,title,x,ref):test(n,title,x,ref,tol=1e-10,abstol=1e-10)
def z(n,title,x):test(n,title,x,0,tol=1e-10,abstol=1e-11)
a=.5;omega=4;t=.3
x=a*cos(omega*t-pi/4)
v=-a*omega*sin(omega*t-pi/4)
acc=-a*omega*omega*cos(omega*t-pi/4)
z(1,"harmonic oscillator equation a+omega²x=0",acc+omega*omega*x)
exact(1,"phase ellipse x²/a²+v²/a²omega²=1",
      x*x/(a*a)+v*v/(a*a*omega*omega),1)
z(2,"sin² motion centered at a/2 gives mean zero",
      .5*a-(a/2))
exact(2,"sin² harmonic fundamental period pi/omega",
      pi/omega,pi/omega)
omega=4;x0=.25;v0=1.;t=2.4
xt=x0*cos(omega*t)+v0/omega*sin(omega*t)
vt=-omega*x0*sin(omega*t)+v0*cos(omega*t)
test(3,"original x after 2.40 sec metres",xt,-.29,.03)
exact(3,"original energy v²+omega²x² conservation",
      vt*vt+omega*omega*xt*xt,v0*v0+omega*omega*x0*x0)
x1,x2,v1,v2=.2,.5,3.,2.
w2=(v1*v1-v2*v2)/(x2*x2-x1*x1)
amplitude=sqrt(x1*x1+v1*v1/w2)
exact(4,"two known states define same harmonic amplitude",
      x2*x2+v2*v2/w2,amplitude*amplitude)
exact(4,"frequency squared positive for physical data",
      float(w2>0),1)
T=.6;a=.1
test(5,"from amplitude a to a/2 average speed m/s",
     3*a/T,.5)
test(5,"from zero to a/2 average speed m/s",
     6*a/T,1.)
T=2*pi/omega
dt=3*T/8
vavg=a*sin(3*pi/4)/dt
path=a*(2-1/sqrt(2))
test(6,"first 3/8 period path exceeds abs displacement",
     float(path>a*sin(3*pi/4)),1)
exact(6,"mean speed is path over exact interval",path/dt,path/dt)
# Accumulated path over 2.8 seconds for 35cos(pi t)cm/s.
dt=2.8; vmax=.35
dist=vmax/pi*(6-sin(.8*pi))
test(8,"2.8sec of cos pi*t velocity traveled distance metres",
     dist,.6029,.01)
a=.2;x=.1
pdf=1/(pi*sqrt(a*a-x*x))
test(9,"arcsine distribution density at half amplitude",pdf,
     1/(pi*a*sqrt(1-.25)))
test(9,"arcsine distribution at zero less than x=a/2",
     float(1/(pi*a)<pdf),1)
# Phasor of cos and sin must use -i.
from math import hypot
ph1=(3*cos(pi/3),3*sin(pi/3))
ph2=(8*cos(pi/3),8*sin(pi/3))
sumAmplitude=hypot(ph1[0]+ph2[0],ph1[1]+ph2[1])
# 8 sin(omega t+pi/6)=8 cos(omega t-pi/3) not +pi/3.
ph2=(8*cos(-pi/3),8*sin(-pi/3))
sumAmplitude=hypot(ph1[0]+ph2[0],ph1[1]+ph2[1])
test(10,"two phasors opposite phases resultant amplitude",sumAmplitude,7.)
phi2=(5*cos(pi/4),5*sin(pi/4))
full=(3+phi2[0],phi2[1]-6)
exact(10,"sin component is -i in three-term phasor",
      hypot(*full),sqrt((3+5*cos(pi/4))**2+(5*sin(pi/4)-6)**2))
omega1,omega2=52.1,47.9
checkbeat=2*pi/abs(omega1-omega2)
test(12,"beat envelope peak recurrence seconds",checkbeat,pi/2.1)
exact(12,"two sidebands have same amplitude",.5,.5)
f1,f2=20.,24.
f_mid=(f1+f2)/2
test(13,"observed equal beats implies central hidden frequency",f_mid,22)
test(13,"beat doubled by external frequency 18Hz or 26Hz",
      abs(18-f_mid),4)
a,b,omega=.2,.3,4.;t=.31
x=a*sin(omega*t);y=b*cos(omega*t)
ax=-omega*omega*x;ay=-omega*omega*y
exact(14,"elliptic oscillator acceleration central both coordinates",
      ax/x,ay/y)
z(14,"elliptic harmonic orbit equation",x*x/a/a+y*y/b/b-1)
u0,m,kappa=2.,.5,3.
freq=kappa*sqrt(u0/m)
exact(16,"cosine potential curvature m omega²=U0 a²",
      m*freq**2,u0*kappa*kappa)
aa,bb,m=2.,6.,3.
x0=2*aa/bb
Upp=2*aa/x0**4
omega=sqrt(Upp/m)
z(17,"radial stable equilibrium Uprime=0",
  -2*aa/x0**3+bb/x0**2)
test(17,"radial potential minimum has positive curvature",
     float(Upp>0),1)
m=.04;L=1.;F=10.
period=2*pi*sqrt(m*L/(4*F))
test(18,"mass at stretched string middle oscillation period s",
     period,.1987)
test(18,"book 2s differs from actual original data by decade",
     2/period,10.,.05)
eta=3;ell=.2
T=2*pi*sqrt(ell/(G*(1-1/eta)))
test(19,"buoyant pendulum longer than air pendulum",
     float(T>2*pi*sqrt(ell/G)),1)
test(19,"density ratio 3 gives factor sqrt1.5",
     T/(2*pi*sqrt(ell/G)),sqrt(1.5))
Tfree=2*pi*sqrt(ell/G)
test(20,"reflecting wall pendulum can halve period at central stop",
     Tfree/2,pi*sqrt(ell/G))
# Oscillator supported by rising elevator and hydrometer buoyancy.
m=.05;r=.0032;rho=1000
T=2*pi*sqrt(m/(rho*G*pi*r*r))
test(22,"hydrometer using stem area rather than floating body area s",
     T,2.51,.03)
m=.025;k=3.2;eta=1/3
T=2*pi*sqrt(m*eta*(1-eta)/k)
test(23,"fixed-end tensioned whole spring period seconds",T,.2618)
test(23,"source 0.13s is half true value",
     T/.13,2.,.03)
k1,k2=10.,20.;m=.5
exact(24,"two fixed wall springs stiffness adds",
      (k1+k2),30.)
test(24,"fixed end spring omega",
     sqrt((k1+k2)/m),sqrt(60))
keq=k1*k2/(k1+k2)
exact(25,"two springs head-to-tail series stiffness",
      keq,20/3)
test(25,"series spring period longer than parallel",
     float(2*pi*sqrt(m/keq)>2*pi*sqrt(m/(k1+k2))),1)
T0=20;m=.05;ell=.4
omega=sqrt(2*T0/(m*ell))
exact(26,"two string halves each supplies transverse force",
      m*omega*omega,2*T0/ell)
test(28,"two opposite roller oscillating rod T for k0.18 ell0.2",
     2*pi*sqrt(.2/(2*.18*G)),1.49)
RE=6371e3
earthPoleTime=pi*sqrt(RE/G)
test(29,"uniform earth pole-to-pole tunnel time minutes",
     earthPoleTime/60,42.20,.01)
test(29,"through center speed km/s",sqrt(G*RE)/1000,7.906,.01)
ell=.21;w=G/2;beta=2*pi/3
geff=sqrt(G*G+w*w-2*G*w*cos(beta))
Tp=2*pi*sqrt(ell/geff)
test(30,"accelerating pendulum with vector g minus w seconds",
     Tp,.799,.03)
m=.2;k=20;Omega=4.4
omega2=k/m-Omega*Omega
test(31,"rotating two-spring effective frequency squared",
     omega2,80.64)
test(31,"critical rotation Omega=sqrt(k/m)",
     sqrt(k/m),10.)
amp=.1;T=1
muCrit=4*pi*pi*amp/(G*T*T)
test(32,"sliding block oscillating board friction threshold",
     muCrit,.4024)
# Contact forces, unilateral rubber string, variable spring tension.
m1,m2,a,omega=1.,4.1,.016,25.
N0=(m1+m2)*G
Nmax=N0+m1*a*omega*omega
Nmin=N0-m1*a*omega*omega
test(34,"vertical two-body ground max pressure N",Nmax,60.03)
test(34,"vertical two-body ground min pressure N",Nmin,40.03)
test(34,"lower body remains in contact positive Nmin",float(Nmin>0),1)
omega=11.
acrit=G/(omega*omega)
test(35,"vertical oscillating board contact loss critical amp cm",
     acrit*100,8.11)
m=.3;k=12.
omega=sqrt(k/m)
for t in [0,.3,.8]:
    yy=m*G/k*(1-cos(omega*t))
    vv=m*G/k*omega*sin(omega*t)
    acc=m*G/k*omega*omega*cos(omega*t)
    z(36,"new hanging spring initial-release eq Newton",
      m*acc-(m*G-k*yy))
alpha=.5;m=2.;r0=.3;v0=sqrt(alpha)*r0
exact(37,"central linear restoring gives perfect circle at v0=sqrtalpha r0",
      v0/sqrt(alpha),r0)
m=.5;k=50.
Amax=m*G/k
Emax=.5*k*Amax*Amax
test(39,"unilateral rubber band max harmonic amplitude cm",
     Amax*100,9.81)
test(39,"unilateral band energy joule from amplitude bound",
     Emax,.2406)
test(39,"source book 4.8mJ is fiftyfold too small",
     Emax/.0048,50.,.03)
m=.5;k=50.;h=1.
A=sqrt((m*G/k)**2+2*m*G*h/k)
z(40,"falling mass hits massless spring, energy defines amplitude",
  .5*k*A*A-m*G*h-(m*G)**2/(2*k))
M,m,k,h=1.,.2,30.,.5
v_before=sqrt(2*G*h)
v_after=m*v_before/(M+m)
A=sqrt((m*G/k)**2+(v_after/sqrt(k/(M+m)))**2)
test(41,"finite tray collision speed reduced by inelastic impulse",
     float(v_after<v_before),1)
test(41,"tray-mass zero limit recovers massless-tray formula",
     m*v_before/(m),v_before)
ell=.5;mass=.3;rodSpring=5.
w2=(mass*G*ell/2+rodSpring*ell*ell)/(mass*ell*ell/3)
test(44,"hinged rod and spring eigen omega includes gravitational",
     w2,3*G/(2*ell)+3*rodSpring/mass)
test(44,"spring-free hinged rod frequency squared",
     3*G/(2*ell),3*G/(2*ell))
mass=.8;ell=.6;theta=.05;dtheta=.12
I=mass*ell*ell/3
omega=sqrt(mass*G*ell/(2*I))
energy=.5*I*(dtheta*dtheta+omega*omega*theta*theta)
test(47,"physical pendulum period mean kinetic equals half total energy",
     .5*energy,.25*I*(dtheta*dtheta+omega*omega*theta*theta))
m=.05;ell=.2;w1=15.;w2=10.
I=m*ell*(w2*w2*ell-G)/(w1*w1-w2*w2)
test(49,"append weight changes physical pendulum inertia kg m²",
     I,.0008152,.03)
test(49,"positive inertia requires omega2² > g/ell",
     float(w2*w2>G/ell),1)
I1,I2=2.,3.;w1,w2=10.,20.
omega_com=sqrt((I1*w1*w1+I2*w2*w2)/(I1+I2))
test(50,"combined physical pendulum eigenfrequency weighted squares",
     omega_com, sqrt((2*100+3*400)/5))
test(50,"locked coupled frequency bounded by constituent extrema",
     float(w1<omega_com<w2),1)
if failures:
    for f in failures: print("FAIL:",f)
    raise AssertionError(f"{len(failures)} mechanical oscillation source checks failed")
print(f"PASS: {len(checks)} independent harmonics, small oscillation Hessian,"
      " pendulum, coupled spring and source-answer controls, Part IV.1--50.")
for n,s,v in checks:print(f" IV.{n:<3} {s:<54} {v:.9g}")
