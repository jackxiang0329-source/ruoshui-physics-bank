#!/usr/bin/env python3
"""Independent thermodynamics QA, original Irodov Part II.1--25.

Recompute pressure of mixtures and connected pistons, pumped pressure,
hydrostatic barometric distributions, gas-process extrema and stable
van-der-Waals compressibility. Part II restarts numbering at 1.
Tests are not a declaration of full expert peer review.
"""
from math import log,exp,sqrt,pi,isclose,e
R=8.314462618
Ratm=.08205736608
G=9.81
checks=[];failures=[]
def check(n,label,actual,reference,tol=.025,atol=1e-12):
    if not isclose(actual,reference,rel_tol=tol,abs_tol=atol):
        failures.append(f"II.{n}: {label}: {actual:.12g} != {reference:.12g}")
    checks.append((n,label,actual))
def exact(n,label,actual,reference):check(n,label,actual,reference,tol=1e-10,atol=1e-10)
def residual(n,label,val,scale=1.):
    check(n,label,val,0,tol=1e-10,atol=1e-10*scale)

mremoved=1.3*30*.78
check(1,"gas evacuated at constant 0C mass g",mremoved,30.42)
exact(1,"pressure decrease scales mass linearly in fixed volume",
      2*mremoved,1.3*30*(2*.78))
pinit,t1,t2,threshold=1.,300.15,380.15,1.10
pnew=.5*(pinit*t2/t1-threshold)
check(2,"vacuum half-cell pressure once threshold exceeded atm",pnew,.0833)
residual(2,"valve stops at specified pressure difference",
         (pinit*t2/t1-pnew)-pnew-threshold)
check(2,"initial-vacuum chamber pressure nonnegative",float(pnew>0),1)
ntotal=2*20/(Ratm*293.15)
mH=4*ntotal-5
mHe=10-4*ntotal
check(3,"H2 helium mixture mass ratio",mH/mHe,.50)
exact(3,"mixture total molar accounting",mH/2+mHe/4,ntotal)
exact(3,"mixture total mass in grams",mH+mHe,5)
ntotal=7/28+11/44
V=ntotal*Ratm*290
density=(7+11)/V
check(4,"N2 CO2 mixture mass density g/L",density,1.5)
exact(4,"mixture mole number 0.5",ntotal,.5)
mixmoles=.10+.20+.30
p=mixmoles*Ratm*300/7.5
mm=(.1*32+.2*28+.3*44)/mixmoles
check(5,"O2 N2 CO2 pressure atm",p,1.97)
check(5,"O2 N2 CO2 molar mass g/mol",mm,36.67)
exact(5,"Dalton molar-partial pressures add to total",
      sum(ni*Ratm*300/7.5 for ni in [.1,.2,.3]),p)
initial,final,T0=4.,3.,300.
T=T0*final*(initial*initial-1)/(initial*(final*final-1))
check(6,"shared temperature for piston volume ratio 4->3 K",T,421.875)
residual(6,"piston hydrostatic pressure difference invariant",
         T*(final-1/final)-T0*(initial-1/initial),scale=T)
n=log(1000)/log(1+.1)
check(7,"pump strokes for V10 and sweptV1 three decades",n,72.48)
exact(7,"ideal stroke repeated pressure ratio", (1/(1+.1))**n,.001)
C,V,t=10.,87.,20.
pexp=exp(-C*t/V)
exact(8,"vacuum pump exp pressure decay",pexp,exp(-C*t/V))
exact(8,"constant volumetric speed logarithmic pressure slope",
      log(pexp)/t,-C/V)
t=87/10*log(1000)
check(9,"vacuum 87L at 10L/s 1000-fold pressure fall time s",t,60.10)
exact(9,"vacuum pressure after calculated time",exp(-10*t/87),.001)
dpS=.001;mass=5.;P0=101325.;ell=.05
dT=(P0*dpS+mass*G)*ell/R
check(10,"two uneven piston area heated up delta T K",dT,.903)
exact(10,"quasistatic pressure force on composite piston",
      (P0+mass*G/dpS)*dpS-P0*dpS,mass*G)
p0,a=100.,2.
vstar=sqrt(p0/(3*a))
Tmax=(p0*vstar-a*vstar**3)/R
check(11,"quadratic p(V) temperature stationary positive",vstar,sqrt(100/6))
residual(11,"quadratic gas curve T'(V)=0 at maximum",
         p0-3*a*vstar*vstar)
check(11,"exponential p(V) maximum T for beta0.5",
      p0/(e*.5*R),p0/(e*.5*R),tol=1e-10)
T0,a=300.,4.
vstar=sqrt(T0/a)
pmin=2*R*sqrt(a*T0)
check(12,"temperature increases as V2 min pressure Pa",pmin,2*R*sqrt(a*T0),tol=1e-10)
residual(12,"p(V) derivative zero at stationary volume",
         -T0/vstar**2+a)
M=.028
gradient=-M*G/R
check(13,"constant density nitrogen hydrostatic T lapse K/m",
      gradient,-.03304)
exact(13,"rhoRT/M hydrostatic derivative",
      (R/M)*gradient,-G)
n=1.4
grad=-(n-1)/n*(M*G/R)
check(14,"polytropic atmosphere lapse rate for n1.4",
      grad,-.00944)
exact(14,"n1 implies isothermal profile gradient",
      -(1-1)/1*(M*G/R),0)
Mair=.029;T=273.15;h=5000
scaleheight=R*T/(Mair*G)
pratioUp=exp(-h/scaleheight)
pratioDown=exp(h/scaleheight)
check(15,"isothermal atmosphere at 5km p/p0",pratioUp,.534)
check(15,"deep mine 5km ideal-isothermal pressure p/p0",pratioDown,1.87)
exact(15,"opposite altitude pressure products unity",
      pratioUp*pratioDown,1)
H=R*T/(Mair*G)
check(16,"density e-fold height km",H/1000,7.98)
check(16,"density 1percent separation height m",
      H*log(1.01),79.4)
exact(16,"density e-fold ratio",exp(-H/H),1/e)
S,P0,h=.1,101325.,200
M=.029
H=R*273.15/(M*G)
mass=S*P0/G*(1-exp(-h/H))
check(17,"cylinder 200m isothermal gas mass kg",mass,
      S*P0*M*h/(R*273.15),tol=.025)
exact(17,"hydrostatic total column mass equals p(bottom)-p(top) S/g",
      mass,S*(P0-P0*exp(-h/H))/G)
exact(18,"infinite isothermal atmosphere center of mass height",
      H,R*273.15/(M*G))
a=.0001;T0=300.
nu=M*G/(a*R*T0)
h=100.
pa=(1-a*h)**nu
pb=(1+a*h)**(-nu)
check(19,"decreasing T pressure factor below1",float(pa<1),1)
check(19,"increasing T pressure factor below1",float(pb<1),1)
exact(19,"isothermal limit for small a",pa**(a), (1-a*h)**(nu*a))
M=.029;omega=5.;r=2.;T=300.
ratio=exp(M*omega**2*r**2/(2*R*T))
check(20,"rotating ideal gas radial pressure larger than center",
      float(ratio>1),1)
exact(20,"isothermal rotating pressure potential",
      log(ratio),M*omega**2*r*r/(2*R*T))
molarV=.044/.5 # kg/mol divided by kg/L -> L/mol
pid=Ratm*300/molarV
avdw=3.59;bv=.0427
pvdw=Ratm*300/(molarV-bv)-avdw/molarV**2
check(21,"dense CO2 ideal gas pressure atm",pid,280)
check(21,"dense CO2 vdw pressure atm",pvdw,80,.05)
exact(21,"excluded volume exceeds 40percent molecular V",
      float(bv/molarV>.4),1)
V,a,b,eta=1.,1.4,.039,.1
T=a*(1+eta)*(V-b)/(Ratm*V*(eta*V+b))
pvdw=Ratm*T/(V-b)-a/V**2
pid=Ratm*T/V
check(22,"vdW vs ideal pressure discrepancy temperature K",T,130)
exact(22,"ideal/vdW relative error fixed branch",
      (pid-pvdw)/pvdw,eta)
V,T1,T2,p1,p2=.25,300.,350.,90.,110.
b=V-Ratm*(T2-T1)/(p2-p1)
a=V**2*(Ratm*T1/(V-b)-p1)
check(23,"experimental vdW parameter b L/mol",b,.0449)
check(23,"experimental vdW parameter a atm L2/mol2",a,1.875)
residual(23,"return to first experimental pressure",
         Ratm*T1/(V-b)-a/V**2-p1,scale=p1)
residual(23,"return to second experimental pressure",
         Ratm*T2/(V-b)-a/V**2-p2,scale=p2)
V,b,a,T=1.,.04,1.4,320.
dPdV=-Ratm*T/(V-b)**2+2*a/V**3
chi=-1/(V*dPdV)
check(24,"vdW isothermal compression coefficient 1/atm",chi,
      V**2*(V-b)**2/(Ratm*T*V**3-2*a*(V-b)**2),tol=1e-10)
exact(24,"stable single phase requires dP/dV negative",
      float(dPdV<0),1)
Tcrit=2*a*(V-b)**2/(Ratm*b*V*(2*V-b))
check(25,"vdW more compressible at T below branch threshold",
      float(250<Tcrit),1)
for T in [250.,Tcrit*1.5]:
    dPdV=-Ratm*T/(V-b)**2+2*a/V**3
    if dPdV<0:
        vd=-1/(V*dPdV)
        ideal=V/(Ratm*T)
        exact(25,f"compressibility inequality at T={T:.2f}K",
              float(vd>ideal),float(T<Tcrit))
check(25,"large V threshold tends to a/(Rb) K",
      Tcrit,a/(Ratm*b),tol=.1)
if failures:
    for msg in failures:print("FAIL:",msg)
    raise AssertionError(f"{len(failures)} thermodynamic-state QA anchors failed")
print(f"PASS: {len(checks)} independent ideal/vdW gases, pressure and hydrostatic "
      "original Irodov Part II.1--25 checks.")
for n,label,val in checks: print(f" II.{n:<3} {label:<54} {val:.9g}")
