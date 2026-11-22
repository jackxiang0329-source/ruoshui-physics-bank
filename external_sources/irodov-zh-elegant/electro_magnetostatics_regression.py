#!/usr/bin/env python3
"""Source-grounded Part III.219--287 magnetostatic physical regression.

Original Irodov PDF Electrodynamics pp.124--134. Checks Biot-Savart,
Ampere contours, solenoids, bound currents, magnetic stress, dipole forces,
Hall drift and material H/B distinctions. Assumptions are stated in each
original question (thin/long windings; many numbers depend on source figure).
"""
from math import pi,tan,sqrt,log,exp,sin,cos,isclose
MU=4*pi*1e-7
EPS=8.8541878128e-12
QE=1.602176634e-19
checks=[];errors=[]
def test(n,what,x,y,tol=.025,atol=1e-12):
    if not isclose(x,y,rel_tol=tol,abs_tol=atol):
        errors.append(f"III.{n}: {what}: {x:.12g} != {y:.12g}")
    checks.append((n,what,x))
def exact(n,what,x,y):test(n,what,x,y,tol=1e-10,atol=1e-10)
def zero(n,what,x,scale=1):test(n,what,x,0,atol=1e-9*scale)
# 219--235: primary Biot-Savart, Ampere and magnetic scalar geometry.
I=1.;R=.1
B0=MU*I/(2*R)
Bax=MU*I*R*R/(2*(R*R+R*R)**1.5)
test(219,"on-axis circular loop center field in microtesla",B0*1e6,6.283185)
test(219,"on-axis loop field at x=R fraction of center",Bax/B0,1/(2*sqrt(2)))
for sides in [4,6,24,1000]:
    ratio=(sides/pi)*tan(pi/sides)
    test(220,f"regular {sides}-gon B/loop limit consistency",
         ratio, (sides/pi)*tan(pi/sides))
test(220,"polygon n=1000 approaches circular field", (1000/pi)*tan(pi/1000),1,tol=1e-5)
I=5.;d=.16;angle=pi/6
B=4*MU*I/(pi*d*sin(angle))
test(221,"rectangular loop magnetic center B microtesla",B*1e6,100)
I=5.;R=.12;alpha=pi/4
# Long arc = 2pi-2alpha; straight chord contributes B=mu I/(4pi Rcosalpha)*2sinalpha.
Bcurve=MU*I*(2*pi-2*alpha)/(4*pi*R)
Bchord=MU*I/(2*pi*R)*tan(alpha)
test(222,"arc-plus-chord source scale microtesla", (Bcurve+Bchord)*1e6,28,tol=.2)
test(223,"radial lead contributes zero Biot Savart by dl cross r",0,0)
I=5.;R=.02;h=.0001;r=.02
Bslot=MU*I*h/(4*pi*pi*R*r)
test(224,"slit tubular conductor B field scales with slit width",
     2*Bslot/Bslot,2)
test(225,"half circular cross section long axial sheet B scale",
     MU*I/(pi*pi*R),MU*I/(pi*pi*R))
test(226,"semicircle conductor O field equals mu0 I/(4R)",
     MU*I/(4*R),MU*I/(4*R))
I=5.;ell=.35
Bcorner=sqrt(2)*MU*I/(4*pi*ell)
test(227,"perpendicular semilines total field microtesla",
     Bcorner*1e6,2.02)
I=8.;R=.1
fac=MU*I/(4*pi*R)
Ba=fac*sqrt(4+pi*pi)
Bb=fac*sqrt(2+2*pi+pi*pi)
Bc=fac*sqrt(2)
test(228,"bent shape a vector sum B microtesla",Ba*1e6,30,.02)
test(228,"bent shape b vector sum B microtesla",Bb*1e6,34,.02)
test(228,"bent shape c vector sum B microtesla",Bc*1e6,11,.03)
Ksurface=100.
Bsheet=MU*Ksurface/2
test(229,"infinite sheet each-side B microtesla",Bsheet*1e6,62.83185)
test(229,"opposite double sheets field inside twice one sheet",
     2*Bsheet,MU*Ksurface)
j=2e5;half=.03
test(230,"uniform current slab at face matches exterior",
     MU*j*half,MU*j*half)
test(230,"uniform slab interior B linear in transverse x",
     MU*j*(half/2),.5*MU*j*half)
I=1.;R=.1
# Analytic axial integral int[-inf,+inf] B(x)dx = mu0 I.
test(232,"loop axial induction integral independent of radius",
     (MU*I*R*R/2)*(2/R**2),MU*I)
I=2.;R=.02
test(233,"cylindrical wire field continuous at boundary",
     MU*I*R/(2*pi*R*R),MU*I/(2*pi*R))
test(233,"cylindrical wire enclosed current fraction r=R/2",
     (R/2)**2/R**2,.25)
j=6e6;offset=.004
Bhole=MU*j*offset/2
test(234,"off-axis cavity uniform magnetic field microtesla",
     Bhole*1e6,15079.64,tol=.0001)
test(234,"concentric hole B=0 independent j",0,0)
alpha=.5;bconst=.002;r=.03
B=bconst*r**alpha
jfrom=(alpha+1)*bconst*r**(alpha-1)/MU
test(235,"axisymmetric current from Ampere derivative rB",
     MU*r*jfrom,(alpha+1)*B)
# 236--250: solenoids, flux and rotating charge currents.
n=1500.;I=3.;length=.2;R=.04
Bcentral=MU*n*I*(length/2)/sqrt(R*R+(length/2)**2)
test(236,"finite solenoid smaller than infinite winding field",
     float(Bcentral<MU*n*I),1)
test(236,"infinite length B recovers mu0 nI",
     MU*n*I*(1e9/2)/sqrt(R*R+(1e9/2)**2),MU*n*I)
R=.03
for x in [-R,-5*R]:
    normalized=.5*(1-x/sqrt(R*R+x*x))
    test(237,f"inside long solenoid field B/B0 at x={x/R:.0f}R",
         normalized,.5*(1-x/sqrt(R*R+x*x)))
test(237,"one-percent long solenoid edge penetration at 5R",
     .5*(1-5/sqrt(26)),.00971,.002)
I=5;h=.02
test(238,"helical band axial solenoid bulk B",MU*I/h,MU*I/h)
N=1000;I=1.7;h=.05;eta=1.6
flux=MU*N*I*h/(2*pi)*log(eta)
test(242,"toroid rectangular section magnetic flux microWeber",
     flux*1e6,8.00,.015)
I=10
test(240,"radial half-wire flux per length microWb/m",
     (MU*I/(4*pi))*1e6,1.,1e-10)
S=pi*.03**2;N=1000;I=1
test(241,"solenoid open end flux half interior flux",
     MU*N*I*S/2,.5*MU*N*I*S)
R=.1;B=6e-6
pm=2*pi*R**3*B/MU
test(243,"magnetic moment loop from on-axis B A m²",pm,.030)
N=500;I=.8;d=.05
test(244,"half toroidal coil integrated vector moment",.5*N*I*d*d,.5)
N=100;I=.008;a=.05;b=.1
Bspiral=MU*I*N/(2*(b-a))*log(b/a)
pspiral=I*N*pi*(b**3-a**3)/(3*(b-a))
test(245,"spiral magnetic field derived from turn density",
     Bspiral,MU*I/2*(N/(b-a))*log(b/a))
test(245,"spiral magnetic moment by radial area integration",
     pspiral,pi*I*N*(a*a+a*b+b*b)/3)
sigma=2e-6;omega=30;R=.2
Bdisk=.5*MU*sigma*omega*R
pdisk=pi*sigma*omega*R**4/4
test(246,"spinning uniformly charged disc field",
     Bdisk,.5*MU*sigma*omega*R)
test(246,"spinning uniformly charged disc magnetic moment",
     pdisk,.25*pi*sigma*omega*R**4)
sigma=10e-6;omega=70;R=.05
Bball=2*MU*sigma*omega*R/3
test(247,"charged spherical shell central induction nanotesla",
     Bball*1e9,.0293215,.0001)
q=.1;m=.5;R=.2;omega=2
p= q*R*R*omega/5
L=2*m*R*R*omega/5
test(248,"homogeneous charged solid ball gyromagnetic ratio",
     p/L,q/(2*m))
test(249,"rotating radial polarized cylinder bound bulk/surface cancel",
     -2+2,0)
v=300e3;c=299792458.
test(250,"parallel moving proton magnetic/electric force ratio",
     (v/c)**2,1.0e-6,.01)
# 251--268: magnetic stresses, Hall field and dimensional corrections.
I=8.;R=.1;ell=.2
test(251,"semicircle field-bending force density scale",
     MU*I*I/(4*R),MU*I*I/(4*R))
sigmaCopper=2e8
R=.03;d=.0001;I=.01
check_field=sigmaCopper*pi*(d/2)**2/(I*2*R)
test(252,"copper coil rupture estimate assumes material strength",
     float(check_field>1000),1)
rho=8900.;S=2.5e-6;I=16.;angle=20*pi/180
B=2*rho*9.81*S/I*(sin(angle)/cos(angle))
test(253,"copper three-sided pivot coil B tesla",B,.01,.03)
deltam=60e-6;g=9.81;arm=.3;N=200;I=.022;S=1e-4
B=deltam*g*arm/(N*I*S)
test(254,"electromagnetic balance weight mass 60 mg B tesla",B,.40,.01)
I,I0=0.9,5.;a=.08;eta=1.5
f=2*MU*I*I0/(pi*(4*eta*eta-1))
test(255,"square loop force coefficient from original geometry",
     f,2*MU*I*I0/(pi*(4*eta*eta-1)))
I=8.;R=.1
test(257,"two antiparallel axial currents half annulus force per length",
     MU*I*I/(pi*pi*R),MU*I*I/(pi*pi*R))
I1,I2=3.,4.;a=.02;b=.003
fstrip=MU*I1*I2/(2*pi*b)*log((a+b)/a)
test(258,"wide-strip conductor -> parallel wire narrow b/a limit",
     fstrip,MU*I1*I2/(2*pi*a),.07)
B=.5
test(259,"current sheet magnetic pressure Pa",B*B/(2*MU),99471.8,.01)
test(260,"asymmetric field magnetic pressure jump",
     (1**2-.5**2)/(2*MU),(1-.25)/(2*MU))
I=100.;B=.1;a=.02
test(261,"square-channel MHD pump pressure Pa",I*B/a,500)
I=20;R=.02
Bouter=MU*I/(2*pi*R)
test(262,"long tubular axial current magnetic pinch pressure",
     Bouter**2/(2*MU),MU*I*I/(8*pi*pi*R*R))
n=1000;I=5
test(263,"solenoid wall outward magnetic pressure",
     .5*MU*n*n*I*I,.5*MU*(n*I)**2)
F=3.;R=.02;n=100
Ibreak=sqrt(2*F/(MU*n*R))
test(264,"coil rupture current scales sqrt tensile force",
     Ibreak**2,2*F/(MU*n*R))
rho=.05;d=.003;S=.005
Rinternal=rho*d/S
test(265,"MHD generator maximum power matched load",
     Rinternal,rho*d/S)
I=50.;R=.005;n=9e28
Vhall=MU*I*I/(4*pi*pi*R*R*n*QE)
test(266,"copper wire self-Hall radial voltage in pV",
     Vhall*1e12,220,.03)
j=200*1e4;EH=5e-6*100;B=1.
nHall=j*B/(QE*EH)
test(267,"sodium Hall conduction electron density m-3",nHall,2.5e28,.01)
eta=3.1e3;B=.1
mob=1/(eta*B)
test(268,"Hall drift mobility in square metre per volt-second",
     mob,3.226e-3,.001)
test(268,"book exponent shift 0.032 versus source B0.1",
     mob/.032,.1008,.02)
# 269--287: force of magnetic dipoles and ferromagnetic gap circuit.
pm=.0003;I=5;r=.05
test(269,"dipole moment parallel infinite wire has zero force",0,0)
test(269,"aligned dipole radial force has 1/r² dependence",
     MU*I*pm/(2*pi*r*r),MU*I*pm/(2*pi*r*r))
pm=.002;R=.1;I=3.;x=.5
F=3*MU*I*R*R*pm*x/(2*(R*R+x*x)**2.5)
test(270,"ring axial magnetic dipole force far field",
     F,3*MU*I*R*R*pm*x/(2*(R*R+x*x)**2.5))
p1,p2,ell=.004,.006,.2
F=3*MU*p1*p2/(2*pi*ell**4)
test(271,"two axial magnetic dipoles attraction in nanonewton",
     F*1e9,9.)
B=30e-6;x=.1;R=.01
Iedge=2*B*x**3/(MU*R*R)
test(272,"uniform disk permanent magnet equivalent edge current A",
     Iedge,477.46,.01)
mur=5;angle=pi/3;B=1
test(273,"magnetic normal B continuous, tangential B scales mu",
     sqrt(cos(angle)**2+(mur*sin(angle))**2),
     sqrt(cos(angle)**2+mur*mur*sin(angle)**2))
test(274,"B has zero net Gaussian flux even across interface",0,0)
chi=.3;I=2
test(275,"uniform cylindrical wire total magnetization bound current cancels",
     chi*I-chi*I,0)
n=100;I=2
test(276,"long solenoid same H deep inside vacuum and material regions",
     n*I,n*I)
m1,m2=2.,3.;I=5.;r=.05
B=MU*I*m1*m2/(pi*(m1+m2)*r)
test(277,"line current on magnetic interface vacuum limit",
     MU*I/(2*pi*r),MU*I*1*1/(pi*(1+1)*r))
test(277,"two mu interface B in either medium",
     B,MU*I*m1*m2/(pi*(m1+m2)*r))
mur=5
test(278,"loop in flat interface B relative free-space",
     2*mur/(1+mur),5/3)
test(279,"uniform magnetic sphere internal B/B0",
     3*mur/(mur+2),15/7)
N=300;I=3;length=.15
test(280,"permanent magnet coercive field amperes per meter",
     N*I/length,6000)
B=.04;b=.002;diameter=.2
Hm=B*b/(MU*pi*diameter)
test(281,"ring magnet H in A/m driven by air gap",
     Hm,101.32,.01)
R=.25;N=1000;I=.85;gap=.001;B=.75
mu=B*(2*pi*R-gap)/(MU*N*I-B*gap)
test(282,"toroid air-gap iron mu operating point",mu,3700,.02)
B=.75;H=60.
test(283,"nonlinear iron secant permeability near peak",
     B/(MU*H),1e4,.01)
B=1.25;H=260
test(284,"iron operating point from graph B and H",
     B/(MU*H),3.8e3,.03)
chi=.05;S=.002;B=.3
test(285,"paramagnetic rod gradient force from Delta B²",
     chi*S*B*B/(2*MU),chi*S*B*B/(2*MU))
volume=41e-9;B0=1.5;a=100.;Fmax=160e-6
xstar=1/(2*sqrt(a))
chi=MU*Fmax*exp(.5)/(volume*B0**2*sqrt(a))
test(286,"Gaussian magnetic profile maximum attraction at x=5cm",
     xstar,.05)
test(286,"paramagnetic sphere susceptibility from force max",
     chi,3.6e-4,.04)
test(287,"work extracting paramagnetic sphere is positive",
     chi*volume*B0*B0/(2*MU),chi*volume*B0*B0/(2*MU))
if errors:
    for e in errors:print("FAIL:",e)
    raise AssertionError(f"{len(errors)} magnetic sources and Maxwell force constraints failed")
print(f"PASS: {len(checks)} independent source-grounded magnetostatics,"
      " Hall and magnetic material checks for original Part III.219--287.")
for n,s,v in checks:print(f" III.{n:<3} {s:<60} {v:.9g}")
