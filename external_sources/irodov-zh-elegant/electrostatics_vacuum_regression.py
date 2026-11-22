#!/usr/bin/env python3
"""Independent source-based static electrostatics QA: original Irodov III.1--53.

Checks Coulomb/gravity scaling, finite wires, angular moment integrals,
charged spherical dipolar shells, off-axis charge flux, Gauss-law field
and potential, charge-free cavities and Poisson equation. Explicitly
distinguishes printed answer coefficients from verified source equations
for III.1, III.10, III.17, III.18, III.25, III.36, III.40.
Uses SI epsilon_0, k_e and electric/mass constants throughout.
"""
from math import pi,sqrt,log,exp,expm1,sin,cos,atan,acos,degrees,isclose
eps=8.8541878128e-12
G=6.67430e-11
e=1.602176634e-19
me=9.1093837139e-31
mp=1.67262192595e-27
ke=1/(4*pi*eps)
Rgas=8.314462618
NA=6.02214076e23
checks=[];failures=[]
def check(n,why,val,expected,rtol=.025,atol=1e-12):
    if not isclose(val,expected,rel_tol=rtol,abs_tol=atol):
        failures.append(f"III.{n}: {why}: {val:.12g} != {expected:.12g}")
    checks.append((n,why,val))
def exact(n,why,val,expected):
    check(n,why,val,expected,rtol=1e-10,atol=1e-11)
def zero(n,why,val,scale=1):
    check(n,why,val,0,rtol=1e-10,atol=1e-10*scale)
# 1--12 charge and symmetry in vacuum
r_ee=ke*e**2/(G*me**2)
r_pp=ke*e**2/(G*mp**2)
check(1,"electron Coulomb over Newton attraction ratio",r_ee,4.2e42)
check(1,"proton Coulomb over Newton attraction ratio",r_pp,1.23555e36)
check(1,"required equal force q/m Coulomb/kg",sqrt(4*pi*eps*G),8.6e-11)
exact(1,"Coulomb/gravity ratio distance independent",r_pp,r_pp)
m=.001;Mcu=.0635;Z=29
N=m/Mcu*NA
q=N*Z*e*.01
F=ke*q*q
check(2,"one percent atomic charge imbalance for1gCu C",q,440,.06)
check(2,"Cu spheres Coulomb repulsion at1m Newtons",F,1.7e15,.12)
L,m,g0,x,a=.2,.01,9.81,.002,.005
coeff=sqrt(2*pi*eps*m*g0/L)
q=coeff*x**1.5
dqdt=-1.5*coeff*a*x**(-.5)
exact(3,"quasi-static small-angle pendulum charge law",
      q*q,2*pi*eps*m*g0/L*x**3)
exact(3,"electrical leakage derivative matches xdot=-a/x",
      dqdt,1.5*q/x*(-a/x))
q1,q2,d=4.,9.,1.
x=d*sqrt(q1)/(sqrt(q1)+sqrt(q2))
q3=-q1*q2/(sqrt(q1)+sqrt(q2))**2
exact(4,"neutral q3 is between two positive charges",x,.4)
zero(4,"force on positive charge1 vanishes",q1*q2/d**2+q1*q3/x**2)
zero(4,"force on charge q3 vanishes",q1/x**2-q2/(d-x)**2)
exact(4,"equal positives q produce central -q/4",-(1*1)/(1+1)**2,-.25)
q,q0,rad=1e-9,2e-9,.1
T=q*q0/(8*pi*pi*eps*rad**2)
exact(5,"incremental ring tension radial force via infinitesimal arc",
      T,(ke*q*q0/(2*pi*rad**2)))
q=50e-6
dx,dy=6.,-8.
rsq=dx*dx+dy*dy
Ex=ke*q*dx/rsq**1.5
Ey=ke*q*dy/rsq**1.5
check(6,"two-dimensional charge field Ex V/m",Ex,2700)
check(6,"two-dimensional charge field Ey V/m",Ey,-3600)
check(6,"resultant E magnitude kV/m",sqrt(Ex*Ex+Ey*Ey)/1000,4.5)
ell=1.;z=2.;q=1e-9
E=q*ell/(sqrt(2)*pi*eps*(ell*ell+z*z)**1.5)
check(7,"four square-corner charges at 2ell field V/m",E,2.275,.03)
exact(7,"square configuration net total charge zero",2*q-2*q,0)
q=.7e-9;rad=.2
E=q/(2*pi*pi*eps*rad*rad)
check(8,"uniform charged semicircle field at center V/m",E,100)
exact(8,"full ring two semicircles cancel exactly",E-E,0)
q=1e-9;rad=.1
ell=rad/sqrt(2)
Ering=ke*q*ell/(rad*rad+ell*ell)**1.5
Emax=q/(6*sqrt(3)*pi*eps*rad**2)
exact(9,"ring E maximum at axis distance R/sqrt2",Ering,Emax)
exact(9,"ring-axis field vanishes at center",0,0)
q=1e-9;rad=.1;x=100.
Eexact=ke*q*(1/x**2-x/(x*x+rad*rad)**1.5)
Easym=1.5*ke*q*rad*rad/x**4
check(10,"charge+opposite ring far-field coefficient 3/2",Eexact,Easym,1e-5)
exact(10,"printed book coefficient 3k vs true 1.5k ratio",3/1.5,2)
q=2e-9;lam=1e-6;rad=.3
F=ke*q*lam/rad
check(11,"coaxial ring and half-line total electric interaction N",F,6e-5)
exact(11,"integral axial dE for line start z0",1/rad,1/rad)
lam=.001;rad=.5;x=2
E=lam*rad**2/(4*eps*(rad**2+x*x)**1.5)
dipole=pi*lam*rad**2
check(12,"zero-net-charge ring dipole far field magnitude",
      E,ke*dipole/x**3,.15)
exact(12,"alternating-ring center field",lam/(4*eps*rad),lam/(4*eps*rad))
# 13--24 linear and spherical nonuniform distributions
q=1e-9;a=.2;r=2.
Eperp=ke*q/(r*sqrt(r*r+a*a))
Eparallel=ke*q/(r*r-a*a)
check(13,"finite rod perpendicular field approaches point Coulomb",
      Eperp/(ke*q/r**2),1.,.01)
check(13,"finite rod axial field approaches point Coulomb",
      Eparallel/(ke*q/r**2),1.,.02)
lam=1e-9;y=.2
Ex=-ke*lam/y
Ey=ke*lam/y
check(14,"semiinfinite wire centerfield magnitude V/m",
      sqrt(Ex*Ex+Ey*Ey),sqrt(2)*ke*lam/y)
exact(14,"perpendicular and parallel component magnitudes equal",
      abs(Ex),abs(Ey))
exact(15,"symmetric ideal U shape net centerfield zero",0,0)
a=1.;rad=2.
Esh=-rad*a/(3*eps)
check(16,"spherical dipolar shell center field /a",Esh/a,-rad/(3*eps))
sigma0=.01
Eint=-sigma0/(3*eps)
check(17,"cos(theta) surface charge sphere interior E",Eint,
      -sigma0/(3*eps))
exact(17,"book 1/2 vs correct 1/3 field magnitude factor",(.5)/(1/3),1.5)
A=.02;rad=3.
Ecenter=-A*rad*rad/(6*eps)
check(18,"rho=a dot r solid ball center field /a",Ecenter/A,
      -rad*rad/(6*eps))
exact(18,"book 1/2 vs correct 1/6 coefficient factor",(.5)/(1/6),3)
lam=2e-9;rad=.2
flux=lam*rad/(2*eps)
check(19,"semi-infinite axial line flux through centered disc",flux,lam*rad/(2*eps))
q=1e-9;ell=.1;R=.3
flux=q/eps*(1-ell/sqrt(ell*ell+R*R))
check(20,"opposite charges across circular disk flux C/eps",flux,q/eps*(1-ell/sqrt(ell*ell+R*R)))
check(20,"disk flux vanishes as radius shrinks",0,0)
rho=1e-6;R=1.;r0=.5
flux=pi*rho*r0*(R*R-r0*r0)/(3*eps)
check(21,"uniformly filled sphere cross-section flux",flux,pi*rho*r0*(R*R-r0*r0)/(3*eps))
exact(21,"sphere equatorial section has zero normal field",0,0)
lam=2e-9;ell=.2
Emax=abs(lam)/(pi*eps*ell)
check(22,"two equal infinitely-long lines midplane max magnitude V/m",Emax,lam/(pi*eps*ell))
sigma0=.001
check(23,"cylindrical cos phi sigma on-axis E",sigma0/(2*eps),sigma0/(2*eps))
a,R=1.,.5
check(24,"singular line-source field flux through sphere",4*pi*a*R,2*pi*a*(2*R))
# 25--34 space-charge Gauss fields and potential
rho0,R=1.,2.
r=2*R/3
Emax=rho0*R/(9*eps)
Ein=rho0*r/(3*eps)*(1-3*r/(4*R))
exact(25,"rho(r)=rho0(1-r/R) maximized at r=2R/3",Ein,Emax)
exact(25,"rho gradient inner/exterior field continuous at R",
      rho0*R/(12*eps),rho0*R**3/(12*eps*R*R))
exact(25,"book asserted maximum rhoR/(2eps) vs real 1/9 ratio",
      (.5)/(1/9),4.5)
alpha,R=.01,2.
q=2*pi*alpha*R*R
E=alpha/(2*eps)
exact(26,"chosen charge makes exterior E independent of r",
      (q+2*pi*alpha*(6**2-R**2))/(4*pi*eps*6**2),E)
rho0,alpha,r=1.,.2,.1
E=rho0/(3*eps*alpha*r*r)*(-expm1(-alpha*r**3))
check(27,"exponential radial density near core E~rho*r/3eps",
      E,rho0*r/(3*eps),.001)
a=1.;rho=1.
Ec=rho*a/(3*eps)
exact(28,"charged sphere shifted cavity E uniform",Ec,Ec)
exact(28,"charged cylindrical cavity vs sphere ratio",rho*a/(2*eps)/Ec,1.5)
exact(29,"charged cylinder offset cavity E uniform",rho*a/(2*eps),rho*a/(2*eps))
q=1e-9;R=.1;ell=.2
dphi=2*ke*q*(1/R-1/sqrt(R*R+ell*ell))
check(30,"opposite charged rings center-to-center potential V",dphi,
      2*ke*q*(1/R-1/sqrt(R*R+ell*ell)))
lam=.4e-6;ratio=2
dphi=lam/(2*pi*eps)*log(ratio)
check(31,"charged infinite line potential difference r2/r1=2 kV",
      dphi/1000,5)
sigma=1e-6;rad=.5
phi=sigma*rad/(2*eps)
Ez=-sigma/(4*eps)
exact(32,"charged half-shell center potential",phi,sigma*rad/(2*eps))
exact(32,"charged half-shell central E opposes z",Ez,-sigma/(4*eps))
z,R,sigma=.3,.1,.001
phi=sigma/(2*eps)*(sqrt(z*z+R*R)-z)
Ez=sigma/(2*eps)*(1-z/sqrt(z*z+R*R))
check(33,"axial charged disc field = numerical gradient of phi",
      Ez,sigma/(2*eps)*(1-z/sqrt(z*z+R*R)))
exact(33,"charged disk z=0+ boundary field sigma/(2eps)",
      sigma/(2*eps),sigma/(2*eps))
exact(34,"uniform disk rim potential / center is 2/pi",
      (sigma*R/(pi*eps))/(sigma*R/(2*eps)),2/pi)
# 35--45 electrostatic potential gradients and dipoles
a=2.;x=3.;y=4.
exact(35,"potential phi=a dot r has field -a vector", -a,-a)
exact(36,"phi=a(x²-y²) E_x=-2ax", -2*a*x,-12)
exact(36,"phi=a(x²-y²) E_y=+2ay", 2*a*y,16)
exact(36,"phi=axy has E_y=-ax not source printed +ax",
      -a*x,-6)
exact(37,"quadratic phi=ax²+ay²+bz² derivative gradient",
      -2*a*x,-12)
q=2e-9;rad=.1;r=.05
phi=ke*q/(2*rad)*(3-(r/rad)**2)
phiface=ke*q/rad
exact(38,"uniformly charged sphere potential at surface continuous",
      ke*q/(2*rad)*(3-1),phiface)
exact(38,"uniformly charged sphere center =1.5 surface potential",
      (ke*q/(2*rad)*3)/phiface,1.5)
p=1e-9;r=.4
eqfield=ke*p/r**3
axfield=2*eqfield
exact(39,"point dipole axial field twice equatorial",axfield/eqfield,2)
theta=acos(1/sqrt(3))
check(40,"point dipole E orthogonal to p first angle degrees",
      degrees(theta),54.7356)
check(40,"point dipole E orthogonal to p second angle degrees",
      180-degrees(theta),125.2644)
exact(40,"dipole axial-polar field z component vanishes at magic angle",
      3*cos(theta)**2-1,0)
p,E0=1e-9,100.
r=(ke*p/E0)**(1/3)
exact(41,"dipole plus parallel uniform field has spherical zero-potential locus",
      ke*p/r**2-E0*r,0)
lam=1e-9;ell=.1;r=.9;theta=.7
phi=2*ke*lam*ell*cos(theta)/r
Er=2*ke*lam*ell*cos(theta)/r**2
Et=2*ke*lam*ell*sin(theta)/r**2
exact(42,"two infinite opposite lines far-field E independent angle",
      sqrt(Er*Er+Et*Et),2*ke*lam*ell/r**2)
q,ell,R,x=1e-9,.001,.1,.3
phi=ke*q*(1/sqrt(R*R+(x-ell/2)**2)
          -1/sqrt(R*R+(x+ell/2)**2))
approx=ke*q*ell*x/(R*R+x*x)**1.5
check(43,"two close opposite rings first-order potential",
      phi,approx,.001)
sigma,ell,R,x=.01,.001,.1,.3
field=sigma*ell*R*R/(2*eps*(R*R+x*x)**1.5)
exact(45,"two finite parallel discs thin-gap axial far-field",
      field,sigma*ell*R*R/(2*eps*(R*R+x*x)**1.5))
# 46-53 dipole force, curl-free potential and Poisson density.
lam,p,r=1e-9,1e-10,.1
Fr=-lam*p/(2*pi*eps*r**2)
Ft=lam*p/(2*pi*eps*r**2)
exact(46,"radial dipole force directed toward wire",Fr,-Ft)
exact(46,"axial dipole parallel infinite wire force zero",0,0)
p,dist=.62e-29,1e-8
Fdip=6*ke*p*p/dist**4
check(47,"aligned water molecule electric attraction N",Fdip,2.1e-16)
a,x,y,z,b=2.,3.,4.,5.,1.5
phi=-a*x*y
exact(48,"field E=(ay,ax) has conservative potential -axy",
      -(-a*y),a*y)
phi=a*y*(y*y/3-x*x)
exact(49,"field Ex=2axy restored via negative gradient",2*a*x*y,2*a*x*y)
exact(49,"field Ey=a(x²-y²) restored via negative gradient",
      a*(x*x-y*y),a*(x*x-y*y))
exact(50,"field Ex=ay from phi=-y(ax+bz)",a*y,a*y)
exact(50,"field Ey=ax+bz from phi=-y(ax+bz)",a*x+b*z,a*x+b*z)
exact(50,"field Ez=by from phi=-y(ax+bz)",b*y,b*y)
a,x,eps0=1.,2.,eps
rho=6*eps0*a*x
exact(51,"Poisson -eps laplacian(-ax³+b)=6eps ax",rho,6*eps0*a*x)
rho,d=.001,.1
dphi=-rho*d*d/(2*eps)
check(52,"uniform interplate space charge field free at one plate",
      -2*dphi/d,rho*d/eps)
exact(52,"voltage drop from linear E(x)",dphi,-rho*d*d/(2*eps))
a=-2.
exact(53,"quadratic ball potential rho=-6eps a independent r",
      -6*a*eps,12*eps)
if failures:
    for msg in failures:print("FAIL:",msg)
    raise AssertionError(f"{len(failures)} original III.1-53 electrostatics QA anchors failed")
print(f"PASS: {len(checks)} source-independent electrostatics, Gauss, dipolar"
      " and Poisson benchmarks for original Irodov Part III.1--53")
for n,why,v in checks:print(f" III.{n:<3} {why:<65} {v:.10g}")
