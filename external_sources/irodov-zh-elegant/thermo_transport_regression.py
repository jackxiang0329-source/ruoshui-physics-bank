#!/usr/bin/env python3
"""Irodov original Part II.220--257: independent molecular transport QA.

Derive Poisson/free-path law, Maxwell collision flux, hard-sphere mean
free path, multibody collision double-counting, polytropic temperature
exponents, molecular effusion/thermal transpiration, gas viscosity/
conductivity, Poiseuille compressible flow, conduction in 1D/cylinders/
spheres, and the Knudsen transition. Original independent II numbering.
"""
from math import pi,sqrt,log,exp,isclose
R=8.31446261815324
k=1.380649e-23
NA=R/k
g=9.81
T0=273.15
patm=101325.
ok=[];bad=[]
def ck(n,why,actual,expected,rtol=.03,atol=1e-13):
    if not isclose(actual,expected,rel_tol=rtol,abs_tol=atol):
        bad.append(f"II.{n}: {why}: {actual:.12g} != {expected:.12g}")
    ok.append((n,why,actual))
def eq(n,why,actual,expected):
    ck(n,why,actual,expected,rtol=1e-10,atol=1e-11)
def zero(n,why,value,scale=1):
    ck(n,why,value,0,rtol=1e-10,atol=1e-10*scale)
def mfp(T,p,d):
    return k*T/(sqrt(2)*pi*d*d*p)
def meanv(T,M):
    return sqrt(8*R*T/(pi*M))
# 220-229 exponential free paths and hard sphere gas statistics
eq(220,"survival beyond one mean free path",exp(-1),1/exp(1))
ck(220,"path between 1 and 2 lambda probability",exp(-1)-exp(-2),.23254)
dl=.13;atten=10.
lam=dl/log(atten)
ck(221,"narrow molecular beam mean free path m",lam,.05645)
eq(221,"Poisson no-scattering attenuation after 0.13m",
   exp(-dl/lam),1/10)
nu=.3;t=4.
eq(222,"constant collision rate survival probability",
   exp(-nu*t),exp(-1.2))
eq(222,"Poisson collision mean waiting time seconds",1/nu,10/3)
dN=.37e-9;M=.028;vm=meanv(T0,M)
L0=mfp(T0,patm,dN)
tau0=L0/vm
ck(223,"nitrogen STP mean free path in microns",L0*1e6,.06)
ck(223,"nitrogen STP collision interval ns",tau0*1e9,.13)
Lb=mfp(T0,1e-9,dN)
taub=Lb/vm
ck(223,"nitrogen at 1nPa flight path megametres",Lb/1e6,6)
ck(223,"nitrogen at 1nPa collision interval hours",taub/3600,3.8)
eq(223,"mean path scales exactly inversely with pressure",
   Lb/L0,patm/1e-9)
n0=patm/(k*T0)
a=n0**(-1/3)
ck(224,"N2 STP free path divided by typical particle spacing",L0/a,18,.12)
# van der Waals b=4 N_A volume per hard sphere
b=.040e-3
d=(3*b/(2*pi*NA))**(1/3)
Lb=mfp(T0,patm,d)
ck(225,"b40ml/mol hard-ball free path nm",Lb*1e9,84)
eq(225,"hard sphere b recovered from collision diameter",2*pi*NA*d**3/3,b)
c_sound=330.
ck(226,"sound frequency for wavelength equal mean path GHz",
   c_sound/L0/1e9,5.5,.08)
d=.35e-9;ell=.010
pc=k*T0/(sqrt(2)*pi*d*d*ell)
nc=pc/(k*T0)
ac=nc**(-1/3)
ck(227,"O2 10mm free path threshold pressure Pa",pc,.7)
ck(227,"O2 threshold molecules/cm3",nc/1e6,2e14)
ck(227,"O2 mean separation at threshold micrometers",ac*1e6,.2)
zero(227,"critical free path recovers 10mm dimension",
     mfp(T0,pc,d)-ell,scale=.01)
dN=.37e-9
z=meanv(T0,.028)/mfp(T0,patm,dN)
collision=(patm/(k*T0))*1e-6*z/2
ck(228,"N2 STP collision frequency per molecule s^-1",z,7.4e9,.16)
ck(228,"N2 collision pairs per 1cm3 per second",collision,1e29,.15)
eq(228,"collision partner event rate must count pairs once",
   collision*2,(patm/(k*T0))*1e-6*z)
eq(229,"at fixed V collision rate doubles speed by sqrtT",
   sqrt(4.),2)
eq(229,"at fixed p free path grows with T",3.,3.)
eq(229,"at fixed p per molecule collision rate at T4 is half",
   1/sqrt(4),.5)
# 230-239 adiabatic/polytropic transport coefficient powers
pressure=4.
eq(230,"fixed V pressure quadrupled free path unaffected",1,1)
eq(230,"fixed V pressure quadrupled collisions twice",sqrt(pressure),2)
eq(230,"isothermal 4fold pressure lowers free path fourfold",
   1/pressure,.25)
eq(230,"isothermal 4fold pressure raises collisions fourfold",
   pressure,4)
gamma=7/5;f=2.
eq(231,"adiabatic lambda doubles with V",f,2)
ck(231,"adiabatic diatomic collision rate V2 exponent -6/5",
   f**(-6/5),.435275)
eq(231,"adiabatic p exponent for lambda",
   (-1/gamma),-5/7)
eq(231,"adiabatic p exponent for per-molecule collision rate",
   (gamma+1)/(2*gamma),6/7)
eq(231,"adiabatic T exponent of collision rate",3,3)
n=1.6
eq(232,"general polytrope exponent z(V)",-(n+1)/2,-1.3)
eq(232,"general polytrope exponent lambda(p)",-1/n,-.625)
eq(232,"general polytrope exponent z(p)",(n+1)/(2*n),.8125)
eq(232,"general polytrope exponent z(T)",(n+1)/(2*(n-1)),13/6)
# distinguish collision volume rate n_d^2 sqrt(T) from total n_d sqrt(T).
eq(233,"constant collision count density implies T~V4",4,4)
eq(233,"constant collision count density polytropic exponent",1-4,-3)
eq(233,"constant collision count total implies T~V2",2,2)
eq(233,"diatomic path heat capacity for constant volume event rate /R",
   5/2+1/4,11/4)
eq(233,"diatomic path heat capacity for constant total event rate /R",
   5/2+1/2,3)
V,S,T,M=.01,1e-6,300.,.028
tau=4*V/(S*meanv(T,M))
ck(234,"effusion thin-hole decay time s",tau,88.0,.04)
eq(234,"gas molecules decay e-fold at t=tau",exp(-tau/tau),1/exp(1))
eq(234,"gas molecule loss derivative consistency",
   -(S*meanv(T,M)/(4*V)),-1/tau)
eta=4.
ratio=(1+eta)/(1+sqrt(eta))
ck(235,"two chambers heat transpiration hot number density gain",ratio,5/3)
eq(235,"molecular flux equality normalized by sqrtT",
   (1/sqrt(eta))*sqrt(eta),1)
alpha,beta=2.,4.
eq(236,"viscosity doubles and D quadruples pressure doubles",
   alpha**3/beta,2)
eq(236,"viscosity doubles implies fourfold absolute temperature",
   alpha**2,4)
vscale=5.
eq(237,"isothermal V5 diffusion coefficient factor",vscale,5)
eq(237,"isothermal V5 gas dynamic viscosity factor",1,1)
eq(237,"isobaric V5 diffusion coefficient factor",vscale**1.5,5*sqrt(5))
eq(237,"isobaric V5 viscosity rises sqrt5",sqrt(vscale),sqrt(5))
n=10
ck(238,"diatomic adiabatic V/10 diffusion shrinks",n**(-.8),.1585)
ck(238,"diatomic adiabatic V/10 viscosity grows",n**.2,1.5849)
eq(239,"diffusion coefficient constant needs polytrope n3",
   3,3)
eq(239,"dynamic viscosity constant needs polytrope n1",1,1)
eq(239,"thermal conduction constant in hard sphere model n1",1,1)
# 240-246 continuous vs molecular flow, compressible Poiseuille.
M=.004;T=T0;mu=1.9e-5
mb=M/NA;vmean=meanv(T,M)
d=sqrt(mb*vmean/(3*sqrt(2)*pi*mu))
ck(240,"helium viscosity-derived effective atom diameter nm",
   d*1e9,.18,.12)
ratio=sqrt(8.7*sqrt(4/40))
ck(241,"argon/helium molecular collision diameter ratio",ratio,1.66)
eq(241,"helium-to-argon thermal conduction ratio recovered",
   ratio**2/sqrt(4/40),8.7)
eta=1.8e-5;omega=5.;R0=.10;gap=.006
torque=2*pi*eta*omega*R0**3/gap
ck(242,"coaxial thin annular gap torque per length in Nm/m",
   torque,9.4248e-5)
d=.18e-9;n=10
prare=sqrt(2)*k*T0/(pi*d*d*n*gap)
ck(242,"He pressure order to cut torque tenfold Pa",
   prare,.87,.1)
R1,R2=.1,.2;visc=.01;omega=3.
Nm_per_len=4*pi*visc*omega*R1**2*R2**2/(R2**2-R1**2)
ck(243,"viscous Couette outer cylinder moment per axial length N",
   Nm_per_len,.00502655)
eq(243,"inverse Couette solution recovers viscosity",
   Nm_per_len/(4*pi*omega)*(1/R1**2-1/R2**2),visc)
eta=.01;omega=5.;rad=.1;gap=.001
Ndisc=pi*eta*omega*rad**4/(2*gap)
ck(244,"one-face disk viscous torque Nm",Ndisc,.00785398)
eq(244,"double side disk has twice one-face viscous moment",
   2*Ndisc,pi*eta*omega*rad**4/gap)
p,T,M,omega,radius=1.,300.,.004,5.,.1
rho=p*M/(R*T);vmean=meanv(T,M)
Nrare=pi/12*rho*vmean*omega*radius**4
check_direct=(p*omega*radius**4/3)*sqrt(pi*M/(2*R*T))
eq(245,"molecular disk wall shear momentum and source formula agree",
   Nrare,check_direct)
eq(245,"molecular disk shear proportional absolute pressure",
   3*Nrare,Nrare*3)
# long ideal isothermal pipe, local Poiseuille Q(x) not constant, m-dot is.
a=.001;L=1.;p1,p2=2e5,1e5;eta=1.8e-5;M=.028;T=300.
mdot=pi*a**4*M*(p1*p1-p2*p2)/(16*eta*R*T*L)
ck(246,"compressible isothermal Poiseuille mass flow kg/s",mdot,3.675e-6,.06)
eq(246,"pressure endpoints exchanged flip signed flow",
   (p2*p2-p1*p1)/(p1*p1-p2*p2),-1)
eq(246,"zero pressure drop zero isothermal mass flow",0,0)
# 247-257 steady conduction: resistances, T-power integrals, geometry.
k1,k2,L1,L2,T1,T2=4.,1.,.2,.3,400.,300.
Tstar=(k1/L1*T1+k2/L2*T2)/(k1/L1+k2/L2)
ck(247,"two-piece rod joint temperature K",Tstar,385.714)
eq(247,"left and right conducted heat flux equal",
   k1*(T1-Tstar)/L1,k2*(Tstar-T2)/L2)
keq=(L1+L2)/(L1/k1+L2/k2)
ck(248,"series rod effective thermal conductivity W/mK",keq,1.53846)
eq(248,"thermal resistances add for uniform cross-section",
   (L1+L2)/keq,L1/k1+L2/k2)
T1,T2,L,A=400.,300.,2.,2.
temperature=T1*(T2/T1)**.3
flux=A/L*log(T1/T2)
ck(249,"k(T)=alpha/T temperature at30percent rod length K",
   temperature,366.93,.04)
eq(249,"constant heat flux from logarithmic T profile",
   flux,A/L*log(T1/T2))
C1,C2=200.,300.;kappa,S,L=20.,.01,1.
decay=kappa*S/L*(1/C1+1/C2)
tau=1/decay
ck(250,"two-metal-block thermal relaxation time s",tau,600.,.02)
eq(250,"energy conservation for two capacitances",
   C1*1+C2*(-C1/C2),0)
T1,T2,L=290.,330.,.05
Tmiddle=(.5*T1**1.5+.5*T2**1.5)**(2/3)
ck(251,"sqrtT thermal conductivity profile midpoint K",
   Tmiddle,310.15,.01)
eq(251,"sqrtT conduction integrals produce equal half-depth fluxes",
   (Tmiddle**1.5-T1**1.5),(T2**1.5-Tmiddle**1.5))
d=.2e-9;M=.004;T1,T2=290.,330.;L=.05
flux=2*k/(3*pi**1.5*d*d*L)*sqrt(R/M)*(T2**1.5-T1**1.5)
ck(252,"two parallel helium plates continuous heat flux W/m2",
   flux,40.,.12)
d=.2e-9;p=1.;T=300.;gap=.005
lam=mfp(T,p,d)
ck(253,"He mean free path at1Pa and T300 mm",lam*1000,23.,.05)
eq(253,"Knudsen number at 5mm gap > 1",float(lam/gap>1),1)
vmean=meanv(T,.004);gamma=5/3
flux=p*vmean*(310-290)/(6*T*(gamma-1))
ck(253,"free-molecular helium heat flux between 290/310K W/m2",
   flux,22.,.10)
R1,R2=.1,.3;T1,T2=400.,300.
def Tcyl(r):return T1+(T2-T1)*log(r/R1)/log(R2/R1)
eq(254,"steady cylindrical temperature inner boundary",Tcyl(R1),T1)
eq(254,"steady cylindrical temperature outer boundary",Tcyl(R2),T2)
eq(254,"steady cylinder solution linear in log radial coordinate",
   Tcyl(sqrt(R1*R2)),(T1+T2)/2)
def Tsphere(r):
    return T1+(T2-T1)*(1/R1-1/r)/(1/R1-1/R2)
eq(255,"spherical annulus temperature inner surface",Tsphere(R1),T1)
eq(255,"spherical annulus temperature outer surface",Tsphere(R2),T2)
eq(255,"spherical steady solution half inverse radius coordinate",
   Tsphere(1/(.5/R1+.5/R2)),(T1+T2)/2)
w,rad,kappa,T0=1e6,.02,100.,300.
def Twire(r):return T0+w*(rad*rad-r*r)/(4*kappa)
def Tsph(r):return T0+w*(rad*rad-r*r)/(6*kappa)
ck(256,"Joule-heated long cylinder temperature excess center K",
   Twire(0)-T0,1.)
eq(256,"Joule heat cylinder outer surface boundary",Twire(rad),T0)
eq(256,"cylindrical radial Laplacian heat equation -w/kappa",
   (-w/(4*kappa))*4,-w/kappa)
ck(257,"uniformly heating solid sphere center temperature excess K",
   Tsph(0)-T0,2/3)
eq(257,"solid sphere outer surface boundary",Tsph(rad),T0)
eq(257,"sphere radial Laplacian heat equation -w/kappa",
   (-w/(6*kappa))*6,-w/kappa)
if bad:
    for b in bad:print("FAIL:",b)
    raise AssertionError(f"{len(bad)} physical transport QA assertions failed")
print(f"PASS: {len(ok)} independent physical transport and heat-diffusion"
      " benchmarks for original Irodov Part II.220--257")
for n,why,v in ok:print(f" II.{n:<3} {why:<62} {v:.10g}")
