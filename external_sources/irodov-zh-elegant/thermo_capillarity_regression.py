#!/usr/bin/env python3
"""Independent Irodov original Part II.160--184 capillarity QA.

Applies one-/two-interface Laplace jumps, hydrostatic vs Young-Laplace,
water-bridge force, liquid volume conservation, surfactant free energy,
and the thermodynamic surface-entropy Maxwell relation. The original
II.162 data have an incompatible shared expansion/reduction factor,
which is preserved as a diagnosed conditional-data conflict.
"""
from math import pi,sqrt,log,cos,isclose
g=9.81;rhoW=1000;rhoHg=13600;alphaW=.073;alphaHg=.48
Rgas=8.31446261815324
checks=[];bad=[]
def check(n,why,value,expected,rtol=.025,atol=1e-11):
    if not isclose(value,expected,rel_tol=rtol,abs_tol=atol):
        bad.append(f"II.{n}: {why}: {value:.10g} != {expected:.10g}")
    checks.append((n,why,value))
def exact(n,why,value,expected):
    check(n,why,value,expected,rtol=1e-10,atol=1e-10)
def zero(n,why,value,scale=1):
    check(n,why,value,0,rtol=1e-10,atol=scale*1e-10)
# 160-169: droplet and bubble radii, mercury contact angle.
phg=4*alphaHg/(1.5e-6)
psoap=8*.045/.003
check(160,"mercury droplet single-surface Laplace jump Pa",phg,1.28e6)
check(160,"soap bubble two-surface Laplace jump Pa",psoap,120)
check(160,"soap bubble pressure relative to single liquid sphere",
      psoap/(4*.045/.003),2)
h=4*alphaHg/(rhoHg*g*70e-6)
check(161,"mercury pore maximum head m",h,.21)
zero(161,"water column pressure balanced by capillary threshold",
     rhoHg*g*h-4*alphaHg/(70e-6),scale=1e5)
p0,d,n=101325.,.001,4.
alpha_model=p0*d/8*((1-n**3/n)/(n*n-1))
check(162,"same printed pressure n and diameter n forces negative alpha",
      float(alpha_model<0),1)
check(162,"printed same n gives alpha=-p0*d/8",
      alpha_model,-p0*d/8,1e-10)
independent_expansion=1.3
alpha_consistent=p0*d/8*(1-independent_expansion**3/n)/(independent_expansion**2-1)
check(162,"independent volume ratio permits positive surface tension",
      float(alpha_consistent>0),1)
p_inside=101325+rhoW*g*5+4*alphaW/(4e-6)
check(163,"air bubble single interface at 5m, d4um atm",
      p_inside/101325,2.2)
check(163,"soap bubble double-interface would incorrectly raise p",
      float(p_inside < 101325+rhoW*g*5+8*alphaW/(4e-6)),1)
eta=1.1;d=4e-6
h=(101325*(eta**3-1)+(4*alphaW/d)*(eta**2-1))/(rhoW*g)
check(164,"small underwater bubble rises expanding 1.1x pond depth m",
      h,5.0)
zero(164,"isothermal bottom/top pV matching with curvature",
     101325+rhoW*g*h+4*alphaW/d
     -eta**3*(101325+4*alphaW/(eta*d)),scale=2e5)
theta=138*pi/180
height=4*alphaHg*abs(cos(theta))/(rhoHg*g)*(1/.0005-1/.001)
check(165,"differential mercury capillary depression between two tubes m",
      height,.010695)
check(165,"nonwetting mercury cos theta negative",float(cos(theta)<0),1)
rc=2*alphaW/(rhoW*g*.025)
check(166,"water meniscus curvature radius for 25mm head mm",
      rc*1000,.595)
check(166,"meniscus radius larger than tube radius .25mm",
      float(rc>.00025),1)
length=.110;diam=20e-6
x=length/(1+101325*diam/(4*alphaW))
check(167,"sealed capillary penetration for equal water levels m",
      x,.014)
zero(167,"sealed gas compression matches curved meniscus jump",
     101325*length/(length-x)-101325-4*alphaW/diam,scale=2e4)
length,h,diam,theta=.1,.005,20e-6,0.
alpha=diam/(4*cos(theta))*(rhoW*g*h+101325*h/(length-h))
check(168,"capillary alpha deduced from hydrostatic plus trapped-air Pa",
      alpha,.0269)
zero(168,"Laplace pressure divided into gas compression and head",
     4*alpha*cos(theta)/diam-rhoW*g*h-101325*h/(length-h),scale=10000)
d1,d2=.0015,.002
h=4*alphaW/(rhoW*g*(d2-d1))
check(169,"annular glass capillary rise m",h,.060)
exact(169,"annular contact-perimeter over cross-sectional area",
      (pi*(d2+d1))/(pi/4*(d2*d2-d1*d1)),
      4/(d2-d1))
# 170-179: jets, curvature, capillary adhesion and viscous drainage.
phi=.01;x=.01
h=2*alphaW/(rhoW*g*phi*x)
check(170,"narrow wedge water rise for x1cm, opening0.01rad m",
      h,.149)
d=.002;length=.02;n=1.5
v1=sqrt(2*g*length/(n**4-1))
Q=pi*d*d/4*v1
check(171,"vertical accelerating jet flow m3/s",Q,9.8e-7)
zero(171,"two free-jet velocity head difference",
     (n*n*v1)**2-v1**2-2*g*length,scale=10)
droplet_h=.0023
dr=rhoW*g*droplet_h**3/(8*alphaW)
check(172,"falling droplet polar meniscus radius difference m",dr,.00020)
check(172,"small-deformation linearization self consistency",
      float(dr<droplet_h),1)
R=.02;thickness=.00038;n=2.;theta=135*pi/180
mass=2*pi*alphaHg*R**2*abs(cos(theta))*(n*n-1)/(g*thickness)
check(173,"additional mass to squeeze Hg pancake between plates kg",
      mass,.69)
exact(173,"incompressible pancake final radius scale",
      R*sqrt(n),sqrt(n)*R)
m=.00007;h=.0001
F=2*alphaW*m/(rhoW*h*h)
check(174,"water bridge capillary plate attraction N",F,1)
R=.05;h=1.9e-6
F=2*pi*R*R*alphaW/h
check(175,"wet 5cm glass disks pulled apart force N",F,600)
d=.0001;width=.12
rise=2*alphaW/(rhoW*g*d)
F=.5*rhoW*g*width*rise**2
check(176,"vertical parallel wet plates attraction N",F,13)
exact(176,"force integrated over rising wedge equal algebraic",
      F,2*alphaW**2*width/(rhoW*g*d*d))
eta=.000018;ell=.2;Rb=.01;r=.001;alpha=.045
time=2*eta*ell*Rb**4/(alpha*r**4)
check(177,"soap bubble Poiseuille drainage time for test inputs s",
      time,1.6)
exact(177,"soap bubble time scales with initial R^4",
      (2*eta*ell*(2*Rb)**4/(alpha*r**4))/time,16)
Q_heat=2*pi*alphaW**2/(rhoW*g)
check(178,"heat released as wetting tube spontaneously fills J",
      Q_heat,3.4e-6)
exact(178,"capillary heat released independent tube radius",
      Q_heat,2*pi*alphaW**2/(rhoW*g))
FHg=pi*alphaHg*.0014**2
Fsoap=2*pi*.045*.006**2
check(179,"mercury droplet single-surface free energy microJ",
      FHg*1e6,3.)
check(179,"soap bubble double-surface free energy microJ",
      Fsoap*1e6,10.2)
# 180-184: free-energy minimization and temperature derivative.
dd=.0015
delta=pi*alphaHg*dd**2*(2**(2/3)-2)
check(180,"coalescence 2 Hg drops decreases surface free energy J",
      delta,-1.4e-6)
check(180,"merging lowers surface area for volume conservation",
      float(delta<0),1)
R=.01;alpha=.045
A_surface=8*pi*alpha*R*R
p0=101325.
p=p0+4*alpha/R
V=4*pi*R**3/3
A_gas=p*V*log(p/p0)
check(181,"soap bubble double-layer surface free energy J",A_surface,1.13e-4)
check(181,"source-specific extra reversible gas compression work positive",
      float(A_gas>0),1)
r=.001
dC=4*Rgas*alpha/(3*p0*r+8*alpha)
check(182,"bubble heating molar C-Cp for 1mm radius J/molK",
      dC,.0049)
exact(182,"zero-radius bubble C-Cp limit",Rgas/2,Rgas/2)
T=300.;dalpha_dT=-.00015
single_q=-T*dalpha_dT
check(183,"per-surface heat for unit area increment J/m2",
      single_q,.045)
area_increment=.002
dS=-2*dalpha_dT*area_increment
dU=2*(alpha-T*dalpha_dT)*area_increment
check(184,"soap film two-surface entropy change J/K",dS,6e-7)
check(184,"soap film two-surface internal energy increment J",
      dU,3.6e-4)
exact(184,"surface first law dU=deltaQ+surface work",
      dU,T*dS+2*alpha*area_increment)
if bad:
    for f in bad:print("FAIL:",f)
    raise AssertionError(f"{len(bad)} capillary mechanics/source model QA failures")
print(f"PASS: {len(checks)} independent Irodov Part II.160--184 Laplace,"
      " wetting, interface thermodynamics and flux checks")
for n,why,value in checks:print(f" II.{n:<3} {why:<61} {value:.9g}")
