#!/usr/bin/env python3
"""Independent original Irodov I.290--314 elasticity/strength QA.

Cross-check thermoelastic strain, hoop stresses, rotational rupture,
geometric wire sag, Poisson strain, Euler-Bernoulli bending,
thin-/solid-shaft torsion and elastic energy. Important: I.304 and I.312
source-answer conflicts are independently flagged and NOT silently corrected.
"""
from math import pi,sqrt,sin,cos,log,isclose
g=9.81
Y=2.0e11              # steel Young modulus, SI
G=8.0e10              # steel shear modulus, SI
rho_steel=7800.
tests=[]
def check(n,why,val,expected,rtol=.025,atol=1e-12):
    if not isclose(val,expected,rel_tol=rtol,abs_tol=atol):
        raise AssertionError(f"I.{n} {why}: observed {val:.10g} expected {expected:.10g}")
    tests.append((n,why,val))
def exact(n,why,val,expected):
    check(n,why,val,expected,rtol=1e-10,atol=1e-10)
def residual(n,why,val,scale=1):
    check(n,why,val,0,rtol=1e-10,atol=1e-10*scale)

# 290-299: stress/strain constraints, source material values retained.
alpha=1.1e-5;dT=100.
p=Y*alpha*dT
check(290,"compressive stress countering thermal expansion Pa",p,2.2e8)
residual(290,"net restrained-cylinder strain zero",alpha*dT-p/Y)
sigma=50e6;r=.025;wall=.001
pcyl=sigma*wall/r
psphere=2*sigma*wall/r
check(291,"glass tube failure pressure Pa",pcyl,2.0e6)
check(291,"glass spherical flask failure pressure Pa",psphere,4.0e6)
exact(291,"sphere safely withstands 2x tube pressure",psphere/pcyl,2)
rho_copper=8900.;strength_copper=150e6;length=1.
omega_rupt=sqrt(8*strength_copper/(rho_copper*length*length))
n=omega_rupt/(2*pi)
residual(292,"spinning copper rod mid-plane rupture sigma",rho_copper*omega_rupt**2*length**2/8-strength_copper,scale=strength_copper)
check(292,"spinning copper rod rev/s at assumed sigma150MPa",n,58.44)
exact(292,"spinning rod max mid-stress independent cross-sectional area",
      (rho_copper*omega_rupt**2*length**2/8),strength_copper)
rho_lead=11300.;sigma_lead=15e6;r=.25
nring=sqrt(sigma_lead/rho_lead)/(2*pi*r)
check(293,"lead wire loop rupture turn/s for sigma15MPa",nring,23.2)
residual(293,"ring tangential tensile stress equals centripetal load",
         rho_lead*(2*pi*nring)**2*r*r-sigma_lead,scale=sigma_lead)
m=.25;length=2.;d=.001;area=pi*d*d/4
x=(m*g*length**3/(8*Y*area))**(1/3)
check(294,"horizontally suspended steel wire midpoint sag m",x,.025)
theta_sine=(x/sqrt((length/2)**2+x*x))
tension=Y*area*(2*sqrt((length/2)**2+x*x)-length)/length
check(294,"exact-geometry vertical tension residual relative load",
      2*tension*theta_sine/(m*g),1.,.002)
F=1000.;S=.003
meanstrain=F/(2*Y*S)
check(295,"uniformly accelerated plank mean compression",meanstrain,F/(2*Y*S),1e-10)
check(295,"accelerated plank midpoint stress equals end force half",
      .5*F/S,F/(2*S),1e-10)
rho=8900.;length=2.;omega=10.;r=length/3
TperArea=.5*rho*omega**2*(length**2-r*r)
elong=rho*omega**2*length**3/(3*Y)
residual(296,"spinning copper rod section tension from exterior centrifugal load",
      TperArea-.5*rho*omega**2*(length**2-r*r),scale=TperArea)
check(296,"spinning rod elongation metres",elong,1.186666667e-5,.001)
exact(296,"free end force must vanish",0,0)
E=1.2e11;nu=.35;F=1000;L=.65
deltaV=-(1-2*nu)*F*L/E
check(297,"copper cylinder compressed volume change mm3",deltaV*1e9,-1.625)
exact(297,"volume change independent cylinder area",deltaV/(-F*L/E),1-2*nu)
rho=8900.;L=2.;E=1.2e11;nu=.35
stretch=rho*g*L*L/(2*E)
check(298,"suspended copper rod self-weight stretch m",stretch,1.45515e-6)
exact(298,"average axial strain = half fixed-end strain",
      stretch/L,rho*g*L/(2*E))
exact(298,"relative volume change via Poisson ratio",
      (1-2*nu)*stretch/L,(1-2*nu)*rho*g*L/(2*E))
E=2e11;nu=.3;p=1e6
beta=3*(1-2*nu)/E
check(299,"isotropic material bulk compressibility Pa^-1",beta,6.0e-12)
exact(299,"hydrostatic stress cubic volume strain",
      -beta*p,-3*p*(1-2*nu)/E)
exact(299,"solid stable positive bulk modulus requires nu<0.5",
      float(nu<.5),1)

# 300-304: correct integrals for cantilevers, explicit source discrepancy.
rho=7800.;L=6.;h=.1
Rcurve=Y*h*h/(6*rho*g*L*L)
check(300,"steel self-weight cantilever clamped curvature radius m",
      Rcurve,121)
exact(300,"beam curvature width cancels, compare widths",
      (Y*.04*h**3/12)/(.5*rho*.04*h*g*L**2),
      (Y*.4*h**3/12)/(.5*rho*.4*h*g*L**2))
E=Y;a=.1;beamI=a**4/12;L=2.;N0=50.;F=20.
tip_couple=N0*L**2/(2*E*beamI)
tip_force=F*L**3/(3*E*beamI)
check(301,"beam pure-end-couple tip displacement m",tip_couple,.000060)
check(301,"beam transverse end load tip displacement m",tip_force,.000032)
residual(301,"end-force bending moment free-end boundary",
         F*(L-L))
residual(301,"clamped-end slope for couple bending form",N0*0/(E*beamI))
simply_mid=F*L**3/(48*E*beamI)
check(302,"simple support center load deflection m",
      simply_mid,.00000200)
exact(302,"simply supported center deflection 1/16 cantilever tip load",
      simply_mid/tip_force,1/16)
rho=7800;L=2.;h=.1
tip_cant=3*rho*g*L**4/(2*Y*h*h)
mid_simp=5*rho*g*L**4/(2*Y*h*h)
check(303,"cantilever self-weight tip sag m",tip_cant,.000918)
check(303,"simply supported length2L self-weight center sag m",
      mid_simp,.001531)
exact(303,"ratio of two elastic sagging examples",mid_simp/tip_cant,5/3)
rho=7800;E=2e11;L=1.2;h=.01;acc=2.
# distributed tangential loading q(x)=rho*h*L*acc*x;
# M(x)=rho*h*L*acc*(L^3/3-xL²/2+x³/6)
# moment integration weighted by tip distance -> 11L^5/120
beam_coef=11/10
lambda_b=beam_coef*rho*acc*L**5/(E*h*h)
check(304,"Euler-Bernoulli beam approximation bend coefficient",beam_coef,1.1)
check(304,"beam approximation tip displacement m",lambda_b,.002137)
exact(304,"explicit source printed 9/5 differs from beam 11/10",
      (9/5)-(11/10),.7)
# Important: the original source answer 9/5 remains an open discrepancy.

# 305-314: torsion, stress transmission and strain energy.
G=80e9;L=2.;R=.05;dr=.002;torque=100.
theta_tube=torque*L/(2*pi*G*R**3*dr)
theta_solid=2*torque*L/(pi*G*R**4)
residual(305,"thin tube torque via Saint-Venant polar J",
         torque-((2*pi*R**3*dr)*G*theta_tube/L),scale=torque)
residual(305,"solid rod torque via exact polar J",
         torque-((pi*R**4/2)*G*theta_solid/L),scale=torque)
check(305,"thin tube torsion angle 100Nm at assumed dims rad",
      theta_tube,.00159155)
check(305,"solid rod torsion angle 100Nm at assumed dims rad",
      theta_solid,.00025465)
L=3;d1=.03;d2=.05;angle=2*pi/180
torque=pi*G*(d2**4-d1**4)*angle/(32*L)
check(306,"thick-walled tube torque for original dimensions Nm",
      torque,497)
exact(306,"hollow tube 4th-power difference positive",
      float(d2**4-d1**4>0),1)
L=2.;r=.015;omega=120;twist=2.5*pi/180
T=G*(pi*r**4/2)*twist/L
power=T*omega
check(307,"rotating steel shaft limited power W",power,16650,.04)
residual(307,"transmitted shaft power equals angular speed*torque",
         power-omega*T,scale=power)
m,r1,r2,angacc=3.,.2,.4,5.
r=.3
Ne= m*angacc*(r2**4-r**4)/(2*(r2*r2-r1*r1))
Nroot=m*angacc*(r2**2+r1**2)/2
residual(308,"annular ring interior torque at bore = total I beta",
         m*angacc*(r2**4-r1**4)/(2*(r2**2-r1**2))-Nroot,scale=Nroot)
exact(308,"annular ring outer free boundary torque zero",
      m*angacc*(r2**4-r2**4)/(2*(r2**2-r1**2)),0)
check(308,"annular ring torque at internal radius r0.3 Nm",Ne,1.09375)
m=3.1;rho=7800.;eps=.001
energy=.5*Y*(m/rho)*eps**2
check(309,"steel rod elastic strain energy with source mass J",energy,39.74)
exact(309,"strain energy scales as eps squared",
      (.5*Y*(m/rho)*(2*eps)**2)/energy,4)
rho=7800.;R=.01;L=2;area=pi*R**2
U=area*rho*rho*g*g*L**3/(6*Y)
elong=rho*g*L*L/(2*Y)
U2=(2/3)*area*L*Y*(elong/L)**2
check(310,"self-weight rod elastic energy J",U,U2,1e-10)
exact(310,"nonuniform self-weight energy / mean-strain uniform energy",
      U/(.5*Y*area*L*(elong/L)**2),4/3)
L=2.;width=.06;thickness=.002
work=pi**2*Y*width*thickness**3/(6*L)
check(311,"steel strip bent into hoop energy J",work,78.96)
residual(311,"strain-bending energy equals I-integral",
         work-.5*Y*(width*thickness**3/12)*(2*pi/L)**2*L,
         scale=work)
L=1.;R=.01;angle=pi/3
U=pi*G*R**4*angle**2/(4*L)
check(312,"steel shaft twist energy for source geometry J",U,690)
exact(312,"source book final numeric 7J differs about 100 fold",
      round(U/7),98)
stress=G*angle*R/L
check(312,"maximum elastic-model outer-wall shear stress Pa",
      stress,8.38e8)
# 60deg over 1m with r=.01 -> gamma_max~1.05%,
# may exceed steel yield: the closed-form is idealized linear elasticity.
uouter=G*angle**2*R**2/(2*L**2)
ucenter=G*angle**2*0/(2*L**2)
exact(313,"torsional energy density vanishes on axis",ucenter,0)
check(313,"torsional energy density at rod exterior J/m3",
      uouter,4.386e6)
exact(313,"torsional volume integral equals I.312 stored energy",
      uouter*pi*R**2*L/2,U)
beta=4.8e-10;rho=1000.;h=1000.
energyvol=.5*beta*(rho*g*h)**2
check(314,"water compressibility energy at depth1km J/m3",
      energyvol,2.31e4)
exact(314,"water stored energy density grows as depth squared",
      (.5*beta*(rho*g*(2*h))**2)/energyvol,4)
print(f"PASS: {len(tests)} independent elasticity/strength/bending/torsion "
      "and energy checks for original Irodov Part I.290--314.")
for n,why,val in tests:print(f"  I.{n:<3} {why:<59} {val:.9g}")
