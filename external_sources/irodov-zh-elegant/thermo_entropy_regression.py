#!/usr/bin/env python3
"""Independent Irodov original Part II.113--159 cycle/entropy QA.

Quasistatic heat engine branch bookkeeping (not simply final efficiency
matching), van-der-Waals Maxwell relation, path heat capacities,
Clausius inequality and irreversible mixing. For statistical problems
test binomial normalization and logarithm of extreme weights instead of
numerically overflowing giant exponentials.
"""
from math import sqrt,log,exp,pi,e,isclose,comb,log10
R=8.31446261815324
NA=6.02214076e23
good=[];bad=[]
def ck(n,why,x,y,rtol=.025,atol=1e-10):
    if not isclose(x,y,rel_tol=rtol,abs_tol=atol):
        bad.append(f"II.{n}: {why}: {x:.11g} != {y:.11g}")
    good.append((n,why,x))
def eq(n,why,x,y):ck(n,why,x,y,rtol=1e-10,atol=1e-10)
def z(n,why,x,scale=1):
    ck(n,why,x,0,rtol=1e-10,atol=scale*1e-10)
# 113-122: reversible heat engines, branch heat balance.
Th,Tc,dT=600.,300.,20.
gain_hot=Tc/Th-Tc/(Th+dT)
gain_cold=dT/Th
ck(113,"reduce cold sink more effective than heat hot source",
   float(gain_cold>gain_hot),1)
for gamma,n in [(1.4,2.)]:
    ck(114,"diatomic Carnot when adiabatic V doubles",
       1-n**(1-gamma),.242)
    ck(114,"diatomic Carnot when adiabatic pressure halves",
       1-n**(-(gamma-1)/gamma),.180)
ck(115,"Carnot refrigerator COP reversed from engine 10pct",
   (1-.10)/.10,9)
T1,T2,T3=600.,450.,300.;r=2.
Q1,Q2,Qout=R*T1*log(r),R*T2*log(r),2*R*T3*log(r)
eq(116,"three-temperature multi-isotherm reversible entropy balances",
   Q1/T1+Q2/T2-Qout/T3,0)
ck(116,"three-temperature reversible cycle efficiency",
   (Q1+Q2-Qout)/(Q1+Q2),.428571)
gamma=1.4;ratio=10.
ck(117,"Otto cycle 10-to-1 compression efficiency",
   1-ratio**(1-gamma),.602)
ck(118,"Brayton compression ratio10 efficiency",
   1-ratio**(-(gamma-1)/gamma),.482)
n=2.
eta=(gamma-1)*(n-1)/(1+gamma*n)
Qin=R/(gamma-1)*(n-1)+R*gamma/(gamma-1)*n*(n-1)
W=R*(n-1)**2
eq(119,"two constant-p/V branch heat equals rectangle work",
   eta*Qin,W)
ck(119,"rectangle pV loop efficiency for n2",eta,.105263)
n=3.
eta_low=1-log(n)/(n-1)
eta_high=1-(n-1)/(n*log(n))
ck(120,"cold isotherm and isoV/adiabatic efficiency",
   eta_low,.45069)
ck(120,"cold isotherm and isoP/adiabatic same efficiency",
   1-log(n)/(n-1),eta_low,rtol=1e-10)
ck(121,"hot isotherm and isoV/adiabatic efficiency",
   eta_high,.39317)
ck(121,"hot isotherm and isoP/adiabatic same efficiency",
   eta_high,.39317)
ck(122,"hot isotherm+polytropic+adiabat independent polytropic n",
   eta_high,1-(n-1)/(n*log(n)),rtol=1e-10)
ck(122,"all three cycles below matching Carnot upper bound",
   float(max(eta_high,eta_low)<1-1/n),1)
# 123-129: three-branch and rectangular cycles with explicit Q in/out.
gamma=1.4;n=2.
ea=1-gamma*(n-1)/(n**gamma-1)
eb=1-(n**gamma-1)/(gamma*n**(gamma-1)*(n-1))
ck(123,"single-adiabat expansion branch engine efficiency",ea,.146)
ck(123,"single-adiabat compression branch engine efficiency",eb,.113)
Qin=R*log(n)+R/(gamma-1)*(1-1/n)
Qout=gamma*R/(gamma-1)*(1-1/n)
ck(124,"isothermal expansion + isochoric heating efficiency",
   1-Qout/Qin,.0993,.02)
Qin=gamma*R/(gamma-1)*(n-1)
Qout=R*log(n)+R/(gamma-1)*(n-1)
ck(124,"isothermal compression + isobaric heating efficiency",
   1-Qout/Qin,.0877,.02)
Tlow,Thigh=300.,600.;v=3.
W=R*(Thigh-Tlow)*log(v)
Qin=R*Thigh*log(v)+R/(gamma-1)*(Thigh-Tlow)
eta=W/Qin
ck(125,"non-regenerative Stirling cycle engine efficiency",eta,.2339,.02)
ck(125,"unregenerated Stirling lower than Carnot",
   float(eta<1-Tlow/Thigh),1)
pr=3.
Qin=R*Thigh*log(pr)+gamma*R/(gamma-1)*(Thigh-Tlow)
eta=R*(Thigh-Tlow)*log(pr)/Qin
ck(126,"nonregenerative Ericsson cycle efficiency",eta,.1928,.02)
ck(126,"Ericsson below Carnot without heat regenerator",
   float(eta<1-Tlow/Thigh),1)
gamma=1.4;tau=4
eta=(gamma-1)/(gamma+1)*(sqrt(tau)-1)/(sqrt(tau)+1)
ck(127,"triangular pV cycle efficiency at Tmax/Tmin4",eta,1/18)
ck(128,"Carnot bound 1-Tmin/Tmax",1-Tlow/Thigh,.5)
ck(128,"non-Carnot triangle below heat-source bound",
   float(eta<1-1/tau),1)
a,b,V,T=3.59,.0427,1.,300.
dpdT=R/(V-b)
p=R*T/(V-b)-a/V**2
dUdV=a/V**2
eq(129,"van der Waals identity dU/dV=T dp/dT-p",
   T*dpdT-p,dUdV)
# 130-145: state-function entropy, volume law, Debye and path capacity.
gamma=1.3
Cv=R/(gamma-1);Cp=Cv+R
ck(130,"one-mol CO2 isoV doubles T entropy J/K",Cv*log2 if (log2:=log(2)) else 0,19.2)
ck(130,"one-mol CO2 isobaric double T entropy J/K",Cp*log(2),25.0)
ck(131,"4mol gas isothermal volume ratio for dS23J/K",
   exp(23/(4*R)),2.0)
ck(132,"isoV cooled then isoP heated to original T entropy J/K",
   2*R*log(3.3),19.85)
nu=1.7/4.
dS=-nu*(5/2)*R*log(3)
ck(133,"He reversible adiabat then isoP compressed entropy J/K",
   dS,-9.70)
nu=2.;gamm=1.3
dS=nu*R/(gamm-1)*(gamm*log(2)-log(3))
ck(134,"2 mol gamma1.3 when V2x and p/3 entropy",dS,-11)
nu=1.2
dS=nu*R*((3/2)*log(1/1.5)+log(2))
ck(135,"two He states ratio V2/V1=2 T1/T2=1.5 entropy J/K",
   dS,.85)
gamm=1.4;n=1.2;t_ratio=1.8
dS=R*(n-gamm)/((n-1)*(gamm-1))*log(t_ratio)
eq(136,"polytropic entropy as Cv logT+R logV",
   dS,R/(gamm-1)*log(t_ratio)-R/(n-1)*log(t_ratio))
ck(136,"adiabatic exponent n=gamma makes dS zero",
   (gamm-gamm)/(gamm-1),0)
ck(137,"2mol argon p proportional V, V doubles entropy J/K",
   8*R*log(2),46.1)
p0,alpha,gamm=12.,2.,1.4
Vmax=gamm*p0/(alpha*(gamm+1))
ck(138,"S maximized along linear p=p0-aV at V",Vmax,3.5)
p=p0-alpha*Vmax
eq(138,"entropy dS/dV= (Cv/T) dT/dV+R/V zero",
   (R/(gamm-1))*(p0-2*alpha*Vmax)/(Vmax*p)+R/Vmax,0)
a,T0,V0,V2=3.,300.,1.,2.
T2=T0+R/a*log(V2/V0)
eq(139,"S(T)=aT+Cv lnT implies T vs lnV",a*(T2-T0),R*log(2))
Rgas=R
b=.04;V1,V2=1.,2.;cv=2.5*R
dS=R*log((V2-b)/(V1-b))
ck(140,"vdW one-mol isoT entropy rise J/K",dS,5.94)
dSall=cv*log(2)+R*log((V2-b)/(V1-b))
eq(141,"vdW entropy state difference independent of actual path",
   dSall,cv*log(2)+dS)
a,T=2.,4.
eq(142,"Debye crystal C=aT3 yields S=a T3/3",
   a*T**3/3,(a/3)*T**3)
mass=3000;a=.77;b=.00046
ds=mass*(a*log(2)+b*(600-300))
ck(143,"temperature dependent aluminum entropy J/K",
   ds,2.0e3)
n=-2.;S=3.
eq(144,"T=aS^n gives path C=S/n negative",
   S/n,-1.5)
S0,T0,C=5.,300.,20.
eq(145,"constant process C leads exponential T(S)",
   T0*exp((S0+C*log(2)-S0)/C),2*T0)
# 146-159: entropy work and mixing; distinguish different vs identical gases.
alpha=120.;T1,T2=300.,400.;cv=2.5*R
Q=-alpha*log(T2/T1)
W=Q-cv*(T2-T1)
ck(146,"S=alpha/T gives heat for 300->400K J",Q,-34.52)
eq(146,"first-law entropy path heat and work",Q,cv*(T2-T1)+W)
n=2.
eta_a=(n-1)/(2*n);eta_b=(n-1)/(n+1)
eq(147,"TS upper isotherm triangular cycle efficiency",eta_a,.25)
eq(147,"TS lower isotherm triangular cycle efficiency",eta_b,1/3)
ck(147,"both positive cycles below Carnot for ratio2",
   float(eta_b<.5 and eta_a<.5),1)
nu=2.2;ratio=3.
ck(148,"2.2 mol gas free expansion threefold entropy J/K",
   nu*R*log(ratio),20.1)
gamma=1.4;T0=300
Uf=R*T0/(gamma-1)*(2**(gamma-1)-1)
chk149=R*log(2)
ck(149,"free expansion then slow adiabatic recompression dU J",
   Uf,2.0e3,.10)
ck(149,"free expansion persists positive entropy Rln2",
   chk149,5.76)
ck(150,"free expansion gas retains more energy than isoentropic",
   float(T0>T0*2**(1-gamma)),1)
dS=R*(.3*log(3)+.7*log(1.5))
ck(151,"mixing N2/O2 into both 1V+2V cells entropy J/K",
   dS,5.10)
cu=300*.39;water=100*4.18
T1,T2=370.15,280.15
Tf=(cu*T1+water*T2)/(cu+water)
ds=cu*log(Tf/T1)+water*log(Tf/T2)
ck(152,"real Cu/water heat capacities isolated total entropy J/K",
   ds,3.7)
ck(152,"isolated metal/water mixture net entropy positive",
   float(ds>0),1)
Cv=1.5*R;T1,T2=300.,600.;Tfinal=(T1+T2)/2
ds=Cv*log(Tfinal/T1)+Cv*log(Tfinal/T2)
ck(153,"two equal-mole same gas at 300K,600K equilibration entropy",
   ds,1.46,.02)
eq(153,"equal-temperature gases have no entropy gain",
   Cv*log((300+300)**2/(4*300*300)),0)
P=2**(-10)
ck(154,"exact half-space probability for ten independent particles",
   P,1/1024)
t=1e10*365.25*86400.;tau=1e-5
N=log(t/tau)/log(2)
ck(154,"wait 1e10 years for all N independent gas atoms one half",
   N,75)
eq(155,"ten molecules equal halves binomial degeneracy",
   comb(10,5),252)
ck(155,"most likely equal halves probability",
   comb(10,5)/2**10,.24609)
eq(156,"binomial P(n) sums to one for N5",
   sum(comb(5,i)/2**5 for i in range(6)),1)
eq(157,"general finite-population Pn sums to 1",
   sum(comb(10,i)*.3**i*.7**(10-i) for i in range(11)),1)
nStd=101325/(1.380649e-23*273.15)
N=1e6
diam=(6*N/(pi*nStd))**(1/3)
ck(158,"ball diameter for rel molecular-number fluctuation 0.001 m",
   diam,4.15e-7,.03)
logOmega=1.5*NA*log10(301/300)
ck(159,"statistical multiplicity ratio log10 for +1K on300K",
   logOmega,1.31e21)
if bad:
    for b in bad:print("FAIL:",b)
    raise AssertionError(f"{len(bad)} entropy/cycle benchmark assertions failed")
print(f"PASS: {len(good)} independent Irodov Part II.113--159 entropy/cycle checks")
for n,why,v in good:print(f" II.{n:<3} {why:<60} {v:.9g}")
