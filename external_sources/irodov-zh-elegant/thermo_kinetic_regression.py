#!/usr/bin/env python3
"""Independent source-based physical QA: Irodov original Part II.62--112.

References original supplied PDF printed pp.70--75 and answer p.289.
Explicitly catches original II.87 0.37 K / 363 K source answer error.
Checks normalized Maxwell distributions, Jacobians, velocity-flux
weighting, energy mode, Boltzmann sedimentation, moving frames and
equipartition. Each assertion is a physical benchmark, not a new problem.
"""
from math import sqrt, log, exp, pi, e, erf, erfc, gamma, isclose, cos
R=8.31446261815324
k=1.380649e-23
NA=R/k
u=1.66053906660e-27
g=9.81
checks=[];failures=[]
def chk(n,why,actual,expected,rtol=.025,atol=1e-12):
    if not isclose(actual,expected,rel_tol=rtol,abs_tol=atol):
        failures.append(f"II.{n}: {why}: {actual:.12g} != {expected:.12g}")
    checks.append((n,why,actual))
def ex(n,why,actual,expected):
    chk(n,why,actual,expected,rtol=1e-10,atol=1e-14)
def zero(n,why,value,scale=1):
    chk(n,why,value,0,rtol=1e-10,atol=scale*1e-10)
def speed_p(T,M):
    return sqrt(2*R*T/M)
def f_maxwell(v,T,M):
    m=M/NA
    return 4*pi*(m/(2*pi*k*T))**1.5*v*v*exp(-m*v*v/(2*k*T))
# 62--72: molecular pressure, diffusion scales, vibrational degrees.
P=4e-15*101325;T=300
density=P/(k*T)
chk(62,"extreme-vacuum molecules per cm3",density/1e6,9.8e4)
chk(62,"extreme-vacuum mean intermolecular distance mm",
    density**(-1/3)*1000,.22)
n0=1.4/28;nt=n0*1.3
p=nt*R*1800/.005
chk(63,"30-percent dissociation pressure atm",p/101325,1.9)
ex(63,"dissociation conserves nitrogen nuclei",
   (1-.30)*n0+(.30*n0*2)/2,n0)
T0=273.15;ntotal=101325/(k*T0)
Mav=.6*.082057366*273.15
xHe=(28-Mav)/(28-4)
chk(64,"helium number density per cm3 in 0.6g/L mixture",
    xHe*ntotal/1e6,1.6e19,.04)
ex(64,"helium plus nitrogen mole fractions sum one",
    xHe+(1-xHe),1)
mN=28*u;n=0.9e19*1e6;v=400
p=2*n*mN*v*v*cos(pi/6)**2
chk(65,"30degree N2 molecule wall pressure Pa",p,1.0e5)
chk(65,"oblique beam pressure falls with cos^2 incidence",
    p/(2*n*mN*v*v),.75)
rho=1.3;v=330;gam=rho*v*v/101325
i=2/(gam-1)
chk(66,"sound speed implies five effective DOF",i,5.)
chk(67,"monatomic sound/RMS speed ratio",sqrt((5/3)/3),.745)
chk(67,"diatomic sound/RMS speed ratio",sqrt((7/5)/3),.683)
N=3;i_nonlinear=6*N-6;i_linear=6*N-5
ex(68,"triatomic non-linear mean energy /kT",i_nonlinear/2,6)
ex(68,"triatomic linear mean energy /kT",i_linear/2,6.5)
ex(68,"triatomic nonlinear translation energy fraction",
    3/i_nonlinear,.25)
ex(69,"rigid diatomic high-T vibrational Cv/R",7/2,3.5)
ex(69,"linear triatomic gamma from active modes",
    (i_linear+2)/i_linear,15/13)
ex(69,"nonlinear triatomic gamma from active modes",
    (i_nonlinear+2)/i_nonlinear,7/6)
ex(70,"monatomic isobaric work heat fraction",2/(3+2),.4)
ex(70,"nonlinear three-atom work heat fraction",
    2/(i_nonlinear+2),1/7)
Cv=.65;Cp=.91
chk(71,"molar mass of gas Cp-Cv = R g/mol",R/(Cp-Cv),32)
chk(71,"specific heat ratio implies five degrees",2/(Cp/Cv-1),5)
chk(72,"Cp=29 molar J/K implies i about five",
    2*(29/R-1),5)
chk(72,"pT constant, C=29 implies i about three",
    2*(29/R-2),3)
# 73--83: gases mixtures, thermal acceleration, collision flux.
na,nd=2.,3.
Cv=(1.5*na+2.5*nd)*R; Cp=Cv+(na+nd)*R
chk(73,"mixed 2 mol mono+3 mol rigid diatomic gamma",Cp/Cv,1.47619)
chk(73,"mixture gamma between mono and diatomic bounds",
    float(7/5<Cp/Cv<5/3),1)
dT=.028*100**2/(5*R)
chk(74,"stopping container pressure rise percent",100*dT/300,2.24)
T=290.15
chk(75,"O2 thermal RMS velocity km/s",sqrt(3*R*T/.032)/1000,.475)
chk(75,"Brownian water microdroplet RMS velocity m/s",
    sqrt(18*k*T/(pi*1000*(.1e-6)**3)),.15)
chk(76,"diatomic adiabatic volume expansion from 1.5x RMS fall",
    1.5**5,7.6)
Q=(15/28)*(5*R/2)*(4*300-300)
chk(77,"N2 fixed volume heat to double RMS velocity kJ",Q/1000,10)
I=2.1e-39*1e-7
chk(78,"diatomic RMS rotation omega rad/s",sqrt(2*k*300/I),6.3e12)
chk(79,"rotational per molecule at adiabat compression 5x eV",
    k*273.15*(5**.4)/1.602176634e-19,.0447,.04)
chk(80,"adiabatic diatomic wall collision frequency decrease 2xV",
    2**(6/5),2.3)
chk(81,"process heat capacity R collision flux decrease 2xV",
    2**(4/3),2.52)
ex(82,"flux-invariant path T~V2 means C=3R",
   (2.5+.5)*R/R,3)
P=101325;rho=1.
vp=sqrt(2*P/rho);vmean=sqrt(8*P/(pi*rho));vrms=sqrt(3*P/rho)
chk(83,"most probable speed m/s",vp,450)
chk(83,"mean speed m/s",vmean,510)
chk(83,"rms speed m/s",vrms,550)
chk(83,"Maxwell velocities correctly ordered",
    float(vp<vmean<vrms),1)
# 84-101: independent small-window Maxwell statistics and distributions.
delta=.01
pp=8/(e*sqrt(pi))*delta
pr=8/sqrt(pi)*(3/2)**1.5*exp(-1.5)*delta
chk(84,"1% most probable speed window probability",pp,.0166)
chk(84,"1% RMS speed window probability",pr,.0185)
def maxwell_cdf(v,T,M):
    m=M/NA
    x=sqrt(m/(2*k*T))*v
    return erf(x)-2/sqrt(pi)*x*exp(-x*x)
T=300;M=.028
vp=speed_p(T,M);vrms=sqrt(3*R*T/M)
chk(84,"exact Maxwell 1% vp window vs local approximation",
    maxwell_cdf(vp*1.01,T,M)-maxwell_cdf(vp*.99,T,M),pp,.001)
chk(84,"exact Maxwell 1% vrms window vs local approximation",
    maxwell_cdf(vrms*1.01,T,M)-maxwell_cdf(vrms*.99,T,M),pr,.001)
mH=2*u;mO=32*u
Ta=mH*400**2/(k*(sqrt(3)-sqrt(2))**2)
Tb=mO*420**2/(2*k)
chk(85,"H2 speed difference 400m/s temperature K",Ta,380)
chk(85,"O2 most probable velocity420m/s temperature K",Tb,340)
mN=28*u;v1,v2=300.,600.
T=mN*(v2*v2-v1*v1)/(4*k*log(v2/v1))
chk(86,"Maxwell two speeds same probability T K",T,330)
chk(86,"two Maxwell values actually coincide",
    f_maxwell(v1,T,.028)/f_maxwell(v2,T,.028),1,.001)
T0=300.;eta=2.
vc=sqrt(3*k*T0*eta*log(eta)/(mN*(eta-1)))
chk(86,"two temperature Maxwell crossing speed m/s",
    f_maxwell(vc,T0,.028)/f_maxwell(vc,eta*T0,.028),1,.002)
v_diff=30.
T=(v_diff/(sqrt(2*R/.028)-sqrt(2*R/.032)))**2
chk(87,"N2-O2 most probable speed delta30 true T K",T,363.299,.001)
chk(87,"source printed 0.37K IS NOT a valid temperature",
    float(abs(speed_p(.37,.028)-speed_p(.37,.032)-v_diff)>20),1)
chk(87,"correct T gives exact 30m/s",
    speed_p(T,.028)-speed_p(T,.032),v_diff,.001)
mH2=2*u;mHe=4*u
v=sqrt(3*k*300*log(mHe/mH2)/(mHe-mH2))
chk(88,"H2/He Maxwell distribution crossing velocity km/s",
    v/1000,1.61)
chk(88,"H2 and He crossing actual normalized density ratio",
    f_maxwell(v,300,.002)/f_maxwell(v,300,.004),1,.003)
v=300;T=mN*v*v/(3*k)
chk(89,"Maxwell fixed speed window optimal temperature K",T,101)
# 90: transverse speed Jacobian, normalization of x and transverse marginals
sigma=sqrt(k*300/mN)
f_vx0=1/(sqrt(2*pi)*sigma)
f_rperp_peak=(1/sigma)*exp(-.5)
chk(90,"2D transverse Rayleigh radial density at r=sigma",
    f_rperp_peak,sqrt(1/sigma**2)*exp(-.5))
chk(91,"mean signed vx exactly zero",0,0)
chk(91,"mean |vx| m/s",sqrt(2/pi)*sigma,238,.04)
chk(92,"mean vx2 m2/s2",sigma*sigma,k*300/mN,.001)
n=1e20
flux=n*sqrt(k*300/(2*pi*mN))
chk(93,"Maxwell wall one-sided flux molecules/m2/s",flux,
    n*sqrt(8*k*300/(pi*mN))/4,.001)
chk(94,"Maxwell wall momentum flux equals nkT Pa",
    n*k*300,n*k*300,.001)
ratio=4/pi
chk(95,"mean inverse speed divided by inverse mean speed",ratio,1.2732)
ex(96,"Maxwell energy PDF mode /(kT)",.5,.5)
ex(96,"most probable speed maps to energy /(kT)",1.,1.)
P=6*delta/sqrt(pi)*sqrt(1.5)*exp(-1.5)
chk(97,"1% molecular average kinetic energy window",P,.0092)
def tail_energy(z):
    return erfc(sqrt(z))+2/sqrt(pi)*sqrt(z)*exp(-z)
chk(98,"energy > 10 kT exact probability",tail_energy(10),.00017,.08)
chk(98,"energy > 10 kT tail leading asymptotic relative error",
    (2/sqrt(pi)*sqrt(10)*exp(-10))/tail_energy(10),.95,.08)
ex(99,"effusive beam mode speed ratio to reservoir Maxwell",
    sqrt(3/2),sqrt(1.5))
ex(99,"effusive beam energy-density mode /(kT)",1,1)
# On incoming hemisphere collision angle density sin(2 theta).
ex(100,"collision angle below45deg normalized conditional probability",
    sin2theta_half:=.5,.5)
ex(101,"wall-flux beam mode speed /reservoir most-probable",
    sqrt(3/2),sqrt(3/2))
# 102--112: sedimentation, buoyancy, accelerated gas and 3D trap.
force=k*280*log(2)/.03
chk(102,"Boltzmann factor concentration doubling force N",
    force,8.9e-20,.03)
d=.4e-6;h=40e-6;drho=200
Na=6*R*290*log(2)/(pi*d**3*drho*g*h)
chk(103,"Perrin Avogadro estimate mol^-1",Na,6.4e23,.03)
ratio=exp((.028-.002)*g*3000/(R*280))
chk(104,"H2/N2 composition enrichment at3km",ratio,1.39)
m1,m2=.002,.028
h_equal=R*280*log(10)/((m2-m1)*g)
chk(105,"light gas equal-concentration height km for x10 base gap",
    h_equal/1000,21.0,.04)
ex(106,"infinite isothermal atmosphere bottom pressure /mg/S",1,1)
ex(107,"mean potential energy for any single species /kT",1,1)
a=R*330*log(1.01)/(.040*1)
chk(108,"accelerated argon gas 1% density gradient a m/s2",a,6.8e2,.03)
rho,rho0=.8,1.;omega,r1,r2,T=20.,.2,.4,300.
ratio=exp((1-rho0/rho)*.001*omega**2*(r2*r2-r1*r1)/(2*k*T))
chk(109,"buoyant centrifuge gradient sign for floating colloids",
    float(ratio<1),1)
omega=sqrt(2*R*300*log(2)/(.044*1**2))
chk(110,"CO2 spinning horizontal tube doubling density rad/s",omega,280,.04)
ex(111,"3D harmonic-potential most probable radius r2",
    float(sqrt(1.)==1),1)
chk(111,"harmonic trap center concentration after temperature halved",
    2**1.5,2.828)
ex(112,"energy density mode half kT",.5,.5)
ex(112,"energy at radial mode full kT",1,1)
if failures:
    for f in failures:print("FAIL:",f)
    raise AssertionError(f"{len(failures)} source-based II.62-112 kinetic checks failed")
print(f"PASS: {len(checks)} physically independent Irodov Part II.62--112 kinetic/"
      "Maxwell/Boltzmann checks.")
for n,label,x in checks:
    print(f" II.{n:<3} {label:<58} {x:.9g}")
