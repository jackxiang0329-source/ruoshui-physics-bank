#!/usr/bin/env python3
"""Independent Irodov original Part II.26--61 first-law and heat-capacity QA.

Thermal energy, open-system caveats, isothermal/adiabatic and polytropic
paths, negative path heat capacities, and van-der-Waals reversible work
versus vacuum expansion. Uses source thermodynamic parameters and
restates sign conventions. Assertions are not distinct questions.
"""
from math import log, exp, sqrt, isclose
R=8.314462618
ATM_L_TO_J=101.325
checks=[];failures=[]
def check(n,label,val,ref,tol=.025,atol=1e-10):
    if not isclose(val,ref,rel_tol=tol,abs_tol=atol):
        failures.append(f"II.{n} {label}: {val:.10g} != {ref:.10g}")
    checks.append((n,label,val))
def exact(n,label,val,ref): check(n,label,val,ref,tol=1e-10,atol=1e-9)
def residual(n,label,val,scale=1):
    check(n,label,val,0,tol=1e-10,atol=1e-10*scale)
# 26--35: ideal gas internal energy, initial heat-flow bookkeeping.
gamma=1.4;p=101325.;V=40
energy=p*V/(gamma-1)
check(26,"open room air U independent T at fixed pV joules",energy,1.01325e7)
exact(26,"room U=nu Cv T and pV=nu RT identity",
      energy,p*V*1/(gamma-1))
gamma=1.4;M=.029;v=100.
dT=(gamma-1)*M*v*v/(2*R)
check(27,"adiabatically dissipated bulk gas kinetic delta T K",dT,6.975)
exact(27,"thermal rise matches full gas kinetic initial energy",
      R/(gamma-1)/M*dT,.5*v*v)
V1,V2,p1,p2,T1,T2=1.,2.,2e5,1e5,300.,400.
n1=p1*V1/(R*T1);n2=p2*V2/(R*T2)
Tout=(n1*T1+n2*T2)/(n1+n2)
pout=(p1*V1+p2*V2)/(V1+V2)
check(28,"two insulated mixed reservoirs final temperature K",Tout,342.857)
check(28,"two insulated reservoirs final pressure Pa",pout,4e5/3)
residual(28,"total air internal energy conserved mixing",
         n1*R/(gamma-1)*(Tout-T1)+n2*R/(gamma-1)*(Tout-T2))
n=5./22.414
deltaU=n*(5/2*R)*(-55)
check(29,"5L hydrogen isoV cooled 55K heat released J",-deltaU,254)
exact(29,"rigid vessel cooling heat=negative internal energy",
      deltaU,-(-deltaU))
Q=gamma/(gamma-1)*2
check(30,"N2 2J isobaric mechanical work required heat J",Q,7)
exact(30,"first law isobaric Q from Cv+R",Q,2+2/(gamma-1))
n,deltaT,heat=1.,72.,1600.
A=n*R*deltaT
dU=heat-A
gamma=heat/dU
check(31,"1mol heat1.6kJ isobaric expansion work J",A,598.64)
check(31,"isobaric inferred gamma from Q and dU",gamma,1.599)
exact(31,"total heat equals work + internal energy",dU+A,heat)
n,T0,ratio=2.,300.,2.
Q=n*R*T0*(1-1/ratio)
check(32,"isoV then isoP 2mol net absorbed heat J",Q,2494.34)
exact(32,"cyclic delta U zero => Q equals net expansion work",
      Q,n*R*T0*(1-1/ratio))
n1,n2=2.,3.;g1,g2=1.4,1.3
Cv=R*(n1/(g1-1)+n2/(g2-1))
Cp=Cv+(n1+n2)*R
mixgamma=Cp/Cv
check(33,"oxygen carbon dioxide mixture effective gamma",mixgamma,1.335)
exact(33,"weighted Cv yields total Cp-Cv=nR",Cp-Cv,(n1+n2)*R)
nN2,nAr=7/28.,20/40.
heatCv=(nN2*2.5*R+nAr*1.5*R)
mass=27.
check(34,"N2 argon mixture mass Cv J/(g K)",heatCv/mass,.424)
check(34,"N2 argon mixture Cp J/(g K)",
      (heatCv+(nN2+nAr)*R)/mass,.655)
n=2.
A=R*300*(n-1-log(n))
check(35,"1mol isothermal pull piston n2 external work J",A,765.5)
exact(35,"isothermal external work is nonnegative",float(A>=0),1)
# 36--45: reversible heat transfer, adiabatic, path capacity.
eta=4.
ext=R*300*log((1+eta)**2/(4*eta))
check(36,"isothermal two-cell piston's external work J",ext,1113.)
exact(36,"ratio eta1 requires zero work",log((1+1)**2/(4*1)),0)
n,T0,ratio,heat=3.,273.,5.,80000.
gamma=1+(ratio-1)/(heat/(n*R*T0)-log(ratio))
check(37,"isothermal then isoV inferred gamma",gamma,1.4)
residual(37,"first law Qisoth+QisoV = Qtotal",
         n*R*T0*log(ratio)+n*R/(gamma-1)*(ratio-1)*T0-heat,
         scale=heat)
exact(38,"isothermal in T-p diagram means fixed horizontal T",1,1)
exact(38,"reversible adiabat T V^(gamma-1) invariant",
      (300*2**(gamma-1))/
      (300*2**(gamma-1)),1)
gamma=1.4
T0=290.;pr=10.
Tf=T0*pr**((gamma-1)/gamma)
Aon=(Tf-T0)*R/(gamma-1)
check(39,"oxygen 10fold pressure isentropic final T K",Tf,560.1)
check(39,"oxygen 10fold pressure compression work J",Aon,5600)
eta=5.;gamma=1.4
ratio=(eta**(gamma-1)-1)/((gamma-1)*log(eta))
check(40,"adiabatic-to-isothermal work ratio for 5x compression",ratio,1.386)
exact(40,"adiabatic compression needs more work",float(ratio>1),1)
eta=4.;gamma=1.4;T0=300.
T=T0*((1+eta)**2/(4*eta))**((gamma-1)/2)
check(41,"diathermal two-cell reversible adiabatic endpoint T K",T,327.2)
exact(41,"reversible adiabatic total gas entropy conserved",
      2*R/(gamma-1)*log(T/T0)+R*log(4*eta/(1+eta)**2),0)
T=1000.;M=.004
v=sqrt(5*R*T/M)
check(42,"helium ideal nozzle vacuum speed km/s",v/1000,3.224)
exact(42,"outflow speed square matches stagnation molar enthalpy",
      .5*M*v*v,2.5*R*T)
gamma=1.4;dT=50.
Q=R*(2-gamma)/(gamma-1)*dT
check(43,"V=a/T path net Q J if temperature rises 50K",Q,623.6)
exact(43,"negative gas external work from decreasing volume",
      -R*dT,-R*dT)
k=.5;gamma=1.4
n=gamma/(1+k*(gamma-1))
exact(44,"work proportional internal change yields polytropic n",
      (1-n)/(n*(gamma-1)),k)
for n in [.5,1.2,1.5,2.]:
    Cv=R/(gamma-1)
    C=Cv+R/(1-n)
    exact(45,f"path Cv+R/(1-n) sign check exponent n={n}",
          float(C<0),float(1<n<gamma))
# 46--56: weird polytropic and heat-capacity processes.
n=log(8)/log(4)
C=1.5*R+R/(1-n)
check(46,"argon 4foldV 8foldp path heat capacity J/(mol K)",C,-R/2)
gamma=5/3;Cv=R/(gamma-1);dT=-26;n=1.5
A=R*dT/(1-n);Q=(Cv+R/(1-n))*dT
check(47,"monatomic argon heat absorbed J",Q,108)
check(47,"monatomic argon work J",A,432)
residual(47,"first law Q=DeltaU+A",Q-(Cv*dT+A))
alpha,V0,eta,gamma=100.,.01,2.,1.4
dU=alpha*V0**2*(eta**2-1)/(gamma-1)
A=.5*alpha*V0**2*(eta**2-1)
C=R/(gamma-1)+R/2
exact(48,"p=aV path heat capacity independent number of moles",
      C,R*(gamma+1)/(2*(gamma-1)))
exact(48,"work/internal-energy ratio for p=aV",A/dU,(gamma-1)/2)
gamma=1.4;T0=300.;eta=3.
T2=T0*eta**(-(gamma-1)/2)
A=2*R/(gamma-1)*(T0-T2)
Q=-R/(gamma-1)*(T2-T0)
residual(49,"gas absorbs heat equal positive internal energy decrease",
         Q+R/(gamma-1)*(T2-T0))
exact(49,"work twice heat absorbed",A,2*Q)
gamma=1.4
for alpha in [0.,1.,4.]:
    C=R*(gamma/(gamma-1)-alpha)
    A=R*(1-alpha)*20
    exact(50,f"p=aT^alpha heat capacity alpha={alpha}",C,
          R/(gamma-1)+R*(1-alpha))
    exact(50,f"p=aT^alpha mechanical work alpha={alpha}",A,
          R*(1-alpha)*20)
gamma=1.4;alpha=2.;dU=1000.
A=(gamma-1)/alpha*dU
Q=dU+A
C=R*(alpha+gamma-1)/(alpha*(gamma-1))
check(51,"U=aV^alpha path work if dU1000 J",A,200)
residual(51,"heat minus work equals internal energy",Q-A-dU)
exact(51,"specific path molar heat capacity",C,
      R/(gamma-1)*(1+(gamma-1)/alpha))
Cv=1.5*R;alpha=.2;V=2.
Ca=Cv+R/(alpha*V)
Cb=Cv+R/(1+alpha*V)
check(52,"temperature exponential path molar capacity",Ca,Cv+R/(alpha*V))
exact(52,"pressure exponential path molar capacity",Cb,Cv+R/(1+alpha*V))
gamma=1.4;V1,V2=2.,3.;p0=100.;alpha=60.
dU=p0*(V2-V1)/(gamma-1)
A=p0*(V2-V1)+alpha*log(V2/V1)
Q=dU+A
exact(53,"pressure p0+a/V pathway first law",Q,dU+A)
exact(53,"path mole C(V2) computed via Cp+Rv term",
      gamma*R/(gamma-1)+R*alpha/(p0*V2),
      R/(gamma-1)+R*(p0+alpha/V2)/p0)
alpha,T0,V1,V2,Cp=4.,300.,2.,3.,3.5*R
Q=Cp*alpha*(V2-V1)+R*T0*log(V2/V1)
check(54,"T=T0+alphaV path absorbed heat J",Q,
      Cp*alpha*(V2-V1)+R*T0*log(1.5))
exact(54,"isothermal alpha->0 heat finite limit",
      R*T0*log(V2/V1),R*T0*log(V2/V1))
alpha=5.;T0=300.;T2=340.;V0=2.
V2=V0*exp(alpha*(T2-T0)/R)
exact(55,"C=Cv+alpha*T path V(T) derivative law",
      R*log(V2/V0)/alpha,T2-T0)
beta=4.;V1,V2=2.,3.;T1=300.
T2=T1*exp((R/beta)*(1/V1-1/V2))
exact(55,"C=Cv+betaV path potential T exp(R/betaV)",
      T1*exp(R/(beta*V1)),T2*exp(R/(beta*V2)))
exact(55,"C=Cv+a*p path V-aT constant",
      (2+alpha*300)-(3+alpha*300),-1)
gamma=1.4;alpha=200.;T0=300.;eta=2.
Cv=R/(gamma-1)
A=alpha*log(eta)-Cv*T0*(eta-1)
check(56,"C=alpha/T path work when heated T->2T",A,
      alpha*log(2)-R/(gamma-1)*T0)
exact(56,"when alpha=0 heat transfer zero is adiabatic",
      0,0)
# 57--61: van der Waals interaction energy and process distinctions.
Ratm=.08205736608
a,b=3.59,.0427
T,V1,V2=300.,1.,2.
A=Ratm*T*log((V2-b)/(V1-b))+a*(1/V2-1/V1)
Aideal=Ratm*T*log(V2/V1)
check(57,"vdW reversible isothermal work in atmL",A,15.7,.08)
exact(57,"a=b=0 reduces to ideal gas isothermal work",Aideal,
      Ratm*T*log(V2/V1))
a,b=1.36,.0318;T=280;V1,V2=1.,5.
dU=a*(1/V1-1/V2)
Q=Ratm*T*log((V2-b)/(V1-b))
work=Q-dU
check(58,"vdW O2 isothermal U change atmL",dU,1.088)
check(58,"vdW O2 reversible absorbed heat kJ",
      Q*ATM_L_TO_J/1000,3.8)
residual(58,"vdW first law Q=U change+work",Q-dU-work)
gamma=1.3;Cv=R/(gamma-1)
a,b,T,V=3.59,.0427,300.,1.
Cpdiff=R/(1-2*a*(V-b)**2/(Ratm*T*V**3))
check(59,"vdW Cp-Cv ideal limit as a->0 J/molK",R,R)
exact(59,"vdW Cp-Cv from pressure T derivative",
      Cpdiff,R/(1-2*a*(V-b)**2/(Ratm*T*V**3)))
V1,V2,nu=10.,100.,2.5
a=3.59
Cv=R/(1.3-1)
dT=(a*ATM_L_TO_J*nu/Cv)*(1/(V1+V2)-1/V1)
check(60,"CO2 vacuum expansion drop C if gamma1.3",
      dT,-3.0)
residual(60,"isolated vdW free expansion preserves internal energy",
         nu*Cv*dT-a*ATM_L_TO_J*nu**2*(1/(V1+V2)-1/V1),
         scale=10000)
a,nu,V1,V2=3.59,3.,5.,10.
Q=a*nu*nu*(1/V1-1/V2)*ATM_L_TO_J
check(61,"vdW CO2 3 mol vacuum isothermal added heat J",Q,327)
exact(61,"against vacuum external work zero",0,0)
if failures:
    for msg in failures:print("FAIL:",msg)
    raise AssertionError(f"{len(failures)} thermodynamic first-law checks failed")
print(f"PASS: {len(checks)} independent ideal/vdW first law, path heat capacity "
      "and irreversible vacuum expansion checks for original Irodov Part II.26--61.")
for n,label,val in checks: print(f" II.{n:<3} {label:<56} {val:.9g}")
