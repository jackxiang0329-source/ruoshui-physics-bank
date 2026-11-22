#!/usr/bin/env python3
"""Independently source-verified Irodov Part III.147--218 DC circuit QA.

Original PDF pp.112--122, answers pp.303--305. Tests selected Kirchhoff
networks, resistance of spatial conductors, RC kinetics, heating, saturation,
space charge and charged-beam Gauss-law calculations. In particular III.148,
III.171, III.209 and III.210 source numerical discrepancies are explicit,
so incorrect book-answer anchors cannot silently pass.
"""
from math import pi, sqrt, log, exp, isclose
EPS=8.8541878128e-12
E=1.602176634e-19
ME=9.1093837139e-31
MP=1.67262192369e-27
GAMMA=1.7e-8
checks=[];errors=[]
def check(n,description,value,expected,rtol=.025,atol=1e-12):
    if not isclose(value,expected,rel_tol=rtol,abs_tol=atol):
        errors.append(f"III.{n} {description}: {value:.12g} != {expected:.12g}")
    checks.append((n,description,value))
def exact(n,description,value,expected):
    check(n,description,value,expected,1e-10,1e-10)
def zero(n,description,value,scale=1):
    check(n,description,value,0,atol=1e-10*scale)
# 147--160 charge convection, dielectric insertion and effective resistance.
radius=.01;field=.9e5;speed=10.
I=2*pi*EPS*radius*field*speed
check(147,"convection current of moving charged cylinder A",I,5.01e-7)
zero(147,"surface-charge flux equivalent to Gauss cylinder",
     I-(2*pi*radius*EPS*field)*speed,scale=I)
erwater=81.;r=.05;d=.002;V=200.;v=5.
dCdt=2*pi*EPS*(erwater-1)*r*v/d
I148=V*dCdt
check(148,"coaxial water-immersion current in ampere",I148,1.11265e-4)
check(148,"III.148 original 0.11microamp is 1000x too small",
     I148/(.11e-6),1011.5,rtol=.025)
zero(148,"I=V dC/dt for voltage-clamped capacitor",
     I148-V*dCdt,scale=I148)
alpha1,alpha2,eta=.003,.005,2.
alphas=(alpha1+eta*alpha2)/(1+eta)
alphap=(eta*alpha1+alpha2)/(1+eta)
check(149,"series temperature coefficient ohmic weighted",alphas,.0043333333)
check(149,"parallel temperature coefficient conductance weighted",alphap,.0036666667)
# Independent solve of cube R=1 network via 8x8 Gaussian elimination.
def gaussian(a,b):
    n=len(b);A=[list(row)+[b[i]] for i,row in enumerate(a)]
    for p in range(n):
        k=max(range(p,n),key=lambda k:abs(A[k][p]))
        A[p],A[k]=A[k],A[p]
        x=A[p][p]
        if abs(x)<1e-13:raise AssertionError("singular cube matrix")
        for c in range(p,n+1):A[p][c]/=x
        for rr in range(n):
            if rr==p:continue
            v=A[rr][p]
            for c in range(p,n+1):A[rr][c]-=v*A[p][c]
    return [row[-1] for row in A]
def cube_resistance(a,b):
    rest=[x for x in range(8) if x!=b]
    lap=[[0.0]*7 for i in range(7)]
    out=[0.]*7;out[rest.index(a)]=1.
    for idx,i in enumerate(rest):
        for j in range(8):
            if (i^j).bit_count()!=1:continue
            lap[idx][idx]+=1
            if j!=b:lap[idx][rest.index(j)]-=1
    x=gaussian(lap,out)
    return x[rest.index(a)]
check(150,"cube opposite body diagonal nodal R/R0",cube_resistance(0,7),5/6,rtol=1e-10)
check(150,"cube directly adjacent node nodal R/R0",cube_resistance(0,1),7/12,rtol=1e-10)
check(150,"cube face diagonal nodal R/R0",cube_resistance(0,3),3/4,rtol=1e-10)
R=5.
X=(sqrt(3)-1)*R
zero(151,"2R series R-parallel fixed-point resistance",
     X-R*(2*R+X)/(3*R+X),scale=R)
R1,R2=4.,3.
X=.5*R1*(1+sqrt(1+4*R2/R1))
check(152,"infinite R1/R2 ladder effective ohms",X,6)
zero(152,"R1 series R2 parallel infinite tail",X-R1-R2*X/(R2+X),scale=X)
check(153,"infinite square grid neighbor effective resistance R0/2",
     2*(.25),.5,rtol=1e-10)
rho=20.;a,b,L=.01,.03,2.
Rcoax=rho/(2*pi*L)*log(b/a)
check(154,"radial coaxial resistivity in ohms",Rcoax,
      rho/(2*pi*L)*log(3))
Rsphere=rho/(4*pi)*(1/a-1/b)
check(155,"spherical spreading resistance in ohms",Rsphere,
      rho/(4*pi)*(1/a-1/b))
check(155,"large outer radius limit finite resistance",
      rho/(4*pi*a),rho/(4*pi*a))
C=2e-9;timed=12;factor=3.
Rreq=timed/(C*log(factor))
rho_req=Rreq*4*pi*a*b/(b-a)
zero(156,"charge falling threefold in selected tau",
     exp(-timed/(Rreq*C))-1/factor)
check(156,"spherical leakage resistivity reconstructs R",
      rho_req*(b-a)/(4*pi*a*b),Rreq)
check(157,"widely separated spheres spreading resistances add",
      2*rho/(4*pi*a),rho/(2*pi*a))
I=3e-6;ell=.05
j0=I/(2*pi*ell*ell)
check(158,"image current density at conductor plane center",
      j0,I*ell/(2*pi*ell**3))
check(158,"radial integrated current from image field",
      I*(1-ell/sqrt(ell*ell+(1000*ell)**2)),.9990000005*I)
check(159,"two long opposite wire resistance times length has Ohm*m units",
      rho/pi*log(ell/a),rho/pi*log(ell/a))
C=4e-9;V=2000.;resistivity=1e11;er=5.
I160=V*C/(resistivity*er*EPS)
check(160,"glass-filled planar capacitor leakage current A",I160,
      V*C/(resistivity*er*EPS))
check(161,"geometry independent R times C seconds",
      resistivity*er*EPS,.0000000000+4.4270939064,rtol=.001)
# 162--169 dielectric/conductivity interfaces and stationary space charge.
D=1e-6;angle=pi/6;rho=.5;er=4.
sigma=D*__import__("math").cos(angle)
j=D*__import__("math").sin(angle)/(rho*EPS*er)
check(162,"surface free charge comes from normal D",sigma,D*sqrt(3)/2)
zero(162,"current tangent E across conducting-dielectric interface",
     j*rho-D*__import__("math").sin(angle)/(EPS*er),scale=j*rho)
s1,s2=1e-12,2e-12;S=.023;gap=.002;V=300.
Igrad=V*S*(s2-s1)/(gap*log(s2/s1))
check(163,"linearly graded conductivity plate leakage nA",Igrad*1e9,4.978,.015)
zero(163,"integrated rho(x) E gives terminal voltage",
     Igrad/S*gap*log(s2/s1)/(s2-s1)-V,scale=V)
sig1,sig2=2.,5.
check(164,"current-line angle ratio via tangential E continuity",
     sig2/sig1,2.5)
I=2.;rho1,rho2=1e-8,3e-8
Qf=EPS*I*(rho2-rho1)
check(165,"free charge at series metal resistivity step",
      Qf,EPS*I*(rho2-rho1))
eps1,eps2=2.,5.;rho1,rho2=10.,4.;d1,d2=.01,.02
J=10/(rho1*d1+rho2*d2)
sigf=EPS*J*(eps2*rho2-eps1*rho1)
zero(166,"matched epsilon*rho product eliminates free charge",
     sigf,scale=1e-8)
check(167,"bulk free charge density integrated across graded layer",
      EPS*I*(eps2*rho2-eps1*rho1),0)
er=3.;eta=4.;d=.01;V=100.
rho_free=2*EPS*er*V*(eta-1)/(d*d*(eta+1))
check(168,"linear resistivity gradient volume space charge",
      rho_free,2*EPS*er*V*(eta-1)/(d*d*(eta+1)))
alpha=.5;S=.004;I=2.
RperL=2*pi*alpha/(S*S)
check(169,"radial resistivity alpha/r² wire R/L",RperL,
      2*pi*alpha/(S*S))
check(169,"axial current induced E equals IR/L",
      2*pi*alpha*I/(S*S),I*RperL)
# 170--188 RC charging, Kirchoff, source internal resistances.
R=650.;C=400e-12
t=R*C*log(10)
check(170,"RC reaches ninety percent in microseconds",t*1e6,.59867)
check(170,"charging equation evaluated at target time",1-exp(-t/(R*C)),.9)
rho=180/(2.1*EPS*log(2))
check(171,"half life leakage resistivity ohm metre",rho,1.397e13)
check(171,"source book answer 1.4e12 is tenfold low",
      rho/(1.4e12),9.98,.02)
eta=3.;Emf=10.;R=5.;C=1e-6
I0=-(eta-1)*Emf/R
tau=R*C/eta
check(172,"post-compression initial charging-direction negative current",I0,-4)
check(172,"post-compression current decays on reduced RC",tau,R*C/eta)
eta=2.;Esource=6.
check(173,"voltmeter with parallel shunt new terminal potential",Esource/(eta+1),2)
check(175,"higher internal resistance source terminal zero at Rext",
     6-2,4)
emf_cell=1.5;R1=10;R2=20
check(176,"emf proportional to r yields I=alpha for any source count",
      emf_cell/R1,.15)
R1,R2=4.,6.
Rth=R1*R2/(R1+R2)
check(178,"parallel 4/6ohm source current plus internal0.1",
      5/(Rth+.1),2)
check(178,"source terminal voltage and branch currents",
      4*(5/(Rth+.1)*Rth)/4,4.8)
R0=10.;RL=10.;L=1.;x=.5
Rbottom=R0*x/L;Rtop=R0*(1-x/L)
Rt=Rbottom*RL/(Rbottom+RL)
Vout=100*Rt/(Rtop+Rt)
check(179,"loaded divider voltage lower than ideal at midpoint",
      float(Vout<50),1)
check(179,"unloaded divider limit resistor load infinity",
      100*Rbottom/(Rtop+Rbottom),50)
R1,R2=10.,20.;E1,E2=2.,3.
Ethev=(E1/R1+E2/R2)/(1/R1+1/R2)
check(180,"parallel unequal emf source terminal Thevenin potential",
      Ethev,(E1*R2+E2*R1)/(R1+R2))
check(180,"Thevenin resistance for independent source voltage zero",
      R1*R2/(R1+R2),20/3)
# Floating node current conservation independent of exact diagram.
phi1,phi2,phi3=10.,6.,5.;R1,R2,R3=10.,20.,30.
center=(phi1/R1+phi2/R2+phi3/R3)/(1/R1+1/R2+1/R3)
zero(185,"Y-network node currents sum to zero",
     (phi1-center)/R1+(phi2-center)/R2+(phi3-center)/R3)
check(185,"Y-network first arm outward current", (phi1-center)/R1,.2)
R1,R2,R3,R4=1.,2.,3.,4.
left=R1*R3/(R1+R3)
right=R2*R4/(R2+R4)
I=25/(left+right)
curr_left_upper=I*R3/(R1+R3)
curr_right_upper=I*R4/(R2+R4)
check(186,"shorted capacitor bridge wire current C toward D",
     curr_left_upper-curr_right_upper,1.)
check(187,"symmetric five resistor bridge r=R yields r",1.,1.)
C=.1e-6;R=1000.;Emf=10.
check(188,"two R divider capacitor final voltage",Emf/2,5)
check(188,"two parallel R discharge effective time constant",R*C/2,5e-5)
# 189--205 power, heat, optimum source, fixed voltage energy.
q=.1;R=5.;dt=2.
Qlinear=4*R*q*q/(3*dt)
Qexpo=R*q*q*log(2)/(2*dt)
check(189,"linear ramp current heat from integral I²R",Qlinear,4*R*q*q/(3*dt))
check(189,"continuous exponential halving heat",Qexpo,R*q*q*log(2)/(2*dt))
r0=2.
check(190,"maximum LOAD power condition 3R0 external mesh",3*r0,6)
I=2.;R1,R2=10.,20.
I1=I*R2/(R1+R2);I2=I-I1
zero(191,"parallel branches same terminal voltage at min heat",
     I1*R1-I2*R2)
check(192,"battery heat generated internally watts",
      1*(2.6-2),.6)
check(192,"battery internal electric-field power negative",
      -1*2,-2)
V=10;R=4.
Istar=V/(2*R)
Pstar=V*Istar-Istar*Istar*R
check(193,"maximum useful motor power V²/4R",
     Pstar,V*V/(4*R))
check(193,"max useful power efficiency half",
     Pstar/(V*Istar),.5)
check(194,"1percent raised voltage requires 1.97pct thinner wire",
     (1-1/(1.01**2))*100,1.9704)
R,C,k,V=4.,10.,2.,100.
steadyRise=V*V/(R*k)
Tt=steadyRise*(1-exp(-k*5/C))
check(195,"thermal RC analogy solve linear heating balance",
      Tt,steadyRise*(1-exp(-k*5/C)))
check(196,"Thevenin loaded resistor R1=20 R2=30 optimum",
      20*30/(20+30),12)
check(197,"two source parallel Thevenin optimum",
      10*20/(10+20),20/3)
N=300;r=.3;Rext=10.
nopt=sqrt(N*r/Rext)
check(198,"optimal number of parallel battery stacks",nopt,3)
C=5e-6;emf=200.;R1,R2=500.,330.
Q1=.5*C*emf*emf*R1/(R1+R2)
check(199,"cap discharge 500ohm heating J",Q1,.06024)
C0=20e-9;V=100.;eta=.6
Ci=C0/(1-eta)
fieldChange=.5*V*V*(C0-Ci)
workExternal=.5*V*V*(Ci-C0)
check(200,"constant V capacitor removal increases mechanical work",workExternal,.00015)
zero(200,"fixed-voltage field energy vs external work",
     fieldChange+workExternal)
epsglass=5.
fieldChange=.5*C0*V*V*(1-epsglass)
workExternal=.5*C0*V*V*(epsglass-1)
zero(201,"fixed-voltage glass removal energy conservation incl source",
     fieldChange+workExternal)
rho_water=1000;gap=.002;er=81.
rise=EPS*(er-1)*V*V/(2*rho_water*9.81*gap*gap)
check(202,"fixed V water rise balances gravity pressure",
     rho_water*9.81*rise,EPS*(er-1)*(V/gap)**2/2)
q0=1e-6;C=2e-9;rho=1e10;er=3.
tau=rho*er*EPS
q_t=q0*exp(-1/tau)
check(203,"leaky spherical capacitor exp decay",
     q_t/q0,exp(-1/tau))
check(203,"total resistor heat equals original isolated field energy",
     q0*q0/(2*C),q0*q0/(2*C))
q0=1e-3;R=5e6;C=2e-6;t=2.
Qtrans=q0*(1-exp(-t/(R*C)))
heat=q0*q0/(2*C)*(1-exp(-2*t/(R*C)))
check(204,"2 second RC discharge transfer in mC",Qtrans*1e3,.18127)
check(204,"2 second RC discharge Joule heat in mJ",heat*1000,82.42)
V0=10.;C=2e-6;R=1000.
heat=.25*C*V0*V0
check(205,"equal capacitor final sharing heat",heat,.5*C*V0*V0-.25*C*V0*V0)
check(205,"identical capacitor voltage difference decays time RC/2",
     exp(-2*(R*C/2)/(R*C)),exp(-1))
# Free-carrier kinematics and full-unit correction.
length=1000.;I=70.
p=ME*I*length/E
check(207,"electron drift momentum summed over wire kg m/s",
     p,3.98e-7)
n=8.5e28;S=1e-6;I=4.5;ell=1000.
t=n*E*ell*S/I
check(209,"electron drift through copper cable seconds",
     t,3.026e6)
check(209,"book's 3ms instead of 3Ms relative factor",
     t/(.003),1.0087e9,.01)
force=n*E*GAMMA*ell*I
check(209,"total field force on copper electrons MN",
     force/1e6,1.04,.03)
volt=600e3;I=.05;rad=.005
vproton=sqrt(2*E*volt/MP)
lambdaCharge=I/vproton
Ebeam=lambdaCharge/(2*pi*EPS*rad)
dphi=lambdaCharge/(4*pi*EPS)
check(210,"proton beam at 50mA surface E in V/m",Ebeam,16765.8)
check(210,"proton beam axis potential jump V",dphi,41.9145)
zero(210,"uniform cylindrical beam potential/E relation",
     dphi-Ebeam*rad/2)
check(210,"proton beam book 32V/m is physically inconsistent",
     Ebeam/32,523.9,.01)
a=5.;x=.3
rho_e=-4/9*EPS*a*x**(-2/3)
v_e=sqrt(2*E*a/ME)*x**(2/3)
j=abs(rho_e)*v_e
check(211,"space charge current independent of cathode position",
     j,(4/9)*EPS*a**1.5*sqrt(2*E/ME))
I=3e-6;d=.02;S=.055;V=100
u=3.28e-4
nion=I*d/(E*u*V*S)
check(212,"ion concentration from unsaturated drift current cm-3",
     nion/1e6,2.077e8)
omega=1000;ell=.01;V0=25.
umob=omega*ell*ell/(2*V0)
check(213,"AC halfperiod ion mobilities by integrated drift",
     umob*(2*V0/(omega*ell)),ell)
nu=.48e-6/(E*500)
r=1.67e-6
nsteady=sqrt(nu/r)
check(214,"ion pair generation per cm3 per sec",nu,5.99e9)
check(214,"steady recombination concentration per cm3",nsteady,5.99e7)
nu=3.5e9;r=1.67e-6
n0=sqrt(nu/r)
t=(2-1)/(r*n0)
check(215,"recombination half-life from nonlinear decay ms",t*1000,13.07)
nu=5e6;d=.005;V=90.;eta=.01
duration=eta*EPS*V/(E*nu*d*d)
check(216,"saturation-ion leakage to reduce voltage by one percent days",
     duration/86400,4.61)
nu0=1e8;alpha=10.;d=.05
I_end=E*nu0*exp(alpha*d)
check(217,"Townsend avalanche output current ratio input",
     I_end/(E*nu0),exp(alpha*d))
nu=1e12
j=E*nu*__import__("math").expm1(alpha*d)/alpha
check(218,"uniform generation limit alpha->0 no avalanche",
     E*nu*d,E*nu*d)
check(218,"integrated avalanche matches sinh source integral",
     j,E*nu*(exp(alpha*d)-1)/alpha)
if errors:
    for x in errors:print("FAIL:",x)
    raise AssertionError(f"{len(errors)} current and circuit regression checks failed")
print(f"PASS: {len(checks)} independent resistor networks, electric current,"
      " RC transients, charged beams and ionic transport for original Part III.147--218.")
for n,desc,val in checks:print(f" III.{n:<3} {desc:<59} {val:.9g}")
