#!/usr/bin/env python3
"""Independent source-grounded Irodov original Part II.185--219 phase QA.

Distinguishes saturation condensation from ideal gas isothermal pV,
isothermal vs adiabatic latent heats, Clausius--Clapeyron sign and
exponential pressure law, van-der-Waals critical relations, thermal
calorimetry branches, melting and irreversible total entropy.
The original answer p.292+ has known unit/decimal errors in II.185,
II.189 and original problem 214 misnumbered 224; do not silently copy.
"""
from math import pi,sqrt,log,exp,isclose
R=8.31446261815324
Ratm=.08205736608
g=9.81
patm=101325
Tw=373.15
Tm=273.15
Mw=.018
L=2260e3
Lm=334e3
cw=4180.
checks=[];errors=[]
def check(n,why,x,y,rtol=.025,atol=1e-12):
    if not isclose(x,y,rel_tol=rtol,abs_tol=atol):
        errors.append(f"II.{n}: {why}: {x:.11g} != {y:.11g}")
    checks.append((n,why,x))
def exact(n,why,x,y):
    check(n,why,x,y,rtol=1e-10,atol=1e-10)
def residual(n,why,x,scale=1):
    check(n,why,x,0,rtol=1e-10,atol=1e-10*scale)
# 185--194: saturation, pressure-temperature, vapor-molecule flux.
dm=.0007
Work=dm/Mw*R*Tw
check(185,"0.70g water vapor condensed at100C piston work J",Work,121)
check(185,"book printed 1.2J smaller by factor near 100",
      Work/1.2,100,.03)
V=.006;mass=5.;vv=.05;vl=.001
mv=(V-mass*vl)/(vv-vl)
Vgas=mv*vv
check(186,"liquid-plus-vapor 6L container vapor mass kg",mv,.020)
check(186,"liquid-plus-vapor 6L container vapor volume L",
      Vgas*1000,1.02,.04)
exact(186,"liquid/vapor volumes sum to 6L",
      mv*vv+(mass-mv)*vl,V)
V1,V2=.005,.0016
mcond=(V1-V2)*patm*Mw/(R*Tw)
check(187,"saturated vapor condensed by 5L to1.6L reduction g",
      mcond*1000,2.0)
exact(187,"same saturation pressure before/after condensation",
      patm,patm)
n,N=2.,100.
eta=(n-1)/(N-1)
check(188,"liquid volume fraction after 2x shrink, liquid/vapor 1/100",
      eta,1/99)
check(188,"vapor remains present if N>n",float(eta<1),1)
entropy=L/Tw
dU=L-R*Tw/Mw
check(189,"one kg water vaporization entropy J/K",entropy,6.05e3)
check(189,"one kg water vaporization internal energy MJ",dU/1e6,2.1)
check(189,"printed 2.1 mJ vs correct internal energy 2.1 MJ factor",
      dU/(2.1e-3),1e9,.03)
m=.020;Q=20000.;heatwarm=m*cw*(100)
mevap=(Q-heatwarm)/L
Vvap=mevap/Mw*R*Tw/patm
rise=Vvap/(410e-4)
check(190,"20g liquid heated to boil and partial boil piston rise m",
      rise,.21)
residual(190,"supplied heat split into sensible and vaporization",
      m*cw*100+mevap*L-Q,scale=Q)
m_cold=.001;Tcold=22+273.15
mcond=m_cold*cw*(Tw-Tcold)/L
Vlost=mcond/Mw*R*Tw/patm
W=patm*Vlost
check(191,"cold water dropped into steam piston atmosphere work J",
      W,25)
a=.072;T=300.15
diam=4*a*Mw/(.01*R*T*1000)
check(192,"Kelvin droplet 1pct vapor-pressure increase diameter m",
      diam,2.1e-7)
mflux=.036*patm*sqrt(Mw/(2*pi*R*Tw))
rate=mflux*1e-4
check(193,"water surface outgoing evaporation gross mass kg/s/cm2",
      rate,3.5e-4)
mflux=1.2e-13*1e-3/1e-4
ptung=mflux*sqrt(2*pi*R*2000/.184)
check(194,"tungsten saturated vapor partial pressure Pa",ptung,9e-10)
# 195-204 van der Waals critical and coexistence.
a_water=5.54
vm_water=.018 # liters per mole at rho ~1 g/cm3
deltaP=a_water/vm_water**2
check(195,"water cohesive pressure removed at liquid density atm",
      deltaP,1.7e4)
check(196,"cohesion pressure from water latent heat Pa",
      1000*L,2.3e9)
a,b=3.59,.0427
Vc=3*b;Pc=a/(27*b*b);Tc=8*a/(27*Ratm*b)
check(197,"vdW CO2 model critical molar volume L/mol",Vc,.1281)
check(197,"vdW CO2 model critical pressure atm",Pc,73)
check(197,"vdW CO2 model critical temperature K",Tc,304)
exact(197,"vdW critical compressibility factor Zc",
      Pc*Vc/(Ratm*Tc),3/8)
Tcrit,pcrit=304.,73.
b=Ratm*Tcrit/(8*pcrit)
a=27*Ratm*Ratm*Tcrit*Tcrit/(64*pcrit)
check(198,"CO2 critical fit b L/mol",b,.0427)
check(198,"CO2 critical fit a atm L2/mol2",a,3.59)
v_crit=3*Ratm*562/(8*78*47)
check(199,"benzene critical mass specific volume L/g",v_crit,.0047)
piRed,nuRed=12.,.5
tau=(piRed+3/nuRed**2)*(3*nuRed-1)/8
exact(200,"reduced vdW 12pc and 0.5Vc gives T/Tc",
      tau,1.5)
bWater=.0305
water_moles=1/.018
Vliq_max=water_moles*3*bWater
check(201,"one kg water liquid branch max-at-critical volume L",
      Vliq_max,5.1)
Pc_water=5.54/(27*bWater*bWater)
check(201,"water vdW idealized limiting saturation pressure atm",
      Pc_water,220,.05)
Tcrit=8*3.59/(27*Ratm*.0427)
rhoCrit=.044/(3*.0427e-3)
check(202,"vdW CO2 fitted critical temperature K",Tcrit,303,.03)
check(202,"vdW CO2 critical mass density kg/m3",rhoCrit,343)
Mc=.074;rhoEther=710.;pc=35.5*patm;Tc=467.
fraction=8*Mc*pc/(3*rhoEther*R*Tc)
check(203,"liquid ether vessel fill fraction to critical state",
      fraction,.25,.05)
# Maxwell equal-area requires equality of Gibbs free energy:
# p_sat * (Vg-Vl) = RT ln((Vg-b)/(Vl-b)) + a(1/Vg-1/Vl)
a,b,T=3.59,.0427,280.
Vl,Vg=.07,.5
psat=(Ratm*T*log((Vg-b)/(Vl-b))+a*(1/Vg-1/Vl))/(Vg-Vl)
area_integral=Ratm*T*log((Vg-b)/(Vl-b))+a*(1/Vg-1/Vl)
exact(204,"coexistence Maxwell area horizontal pressure matching",
      area_integral-psat*(Vg-Vl),0)
# 205-214 supercooling, vapor pressure Clapeyron and triple point.
fraction=4.18*20/334
check(205,"supercooled water -20C fraction immediately freezes",fraction,.25)
check(205,"cooling needed to freeze all initially supercooled K",
      334/4.18,80)
dp=patm;dv=-.091e-3
dt=Tm*dv*dp/Lm
check(206,"ice melting point shift per plus1atm K",dt,-.0075)
check(206,"ice has negative Clapeyron dp/dT",float(dt<0),1)
vv=L*.9/(Tw*3200)
check(207,"steam volume per kg from boiling pressure-temperature slope",
      vv,1.7)
p_ratio=exp(L*Mw/R*(1/Tw-1/(Tw+1.1)))
check(208,"water pressure at101.1C relative to at100C",
      p_ratio,1.04)
growth=(L*Mw/(R*Tw**2)-1/Tw)*1.5
check(209,"steam vapor mass fixed V +1.5K percent",
      growth*100,5)
T1,T2=Tw,330.
ratio=exp(L*Mw/R*(1/T1-1/T2))
check(210,"Clausius saturation vapor pressure drops upon cooling",
      float(ratio<1),1)
deltaP=(640-1)*patm
deltaTm=Tm*(-.09e-3)*deltaP/Lm
meltfrac=2100*abs(deltaTm)/Lm
check(211,"pressure-induced ice melting fraction at640atm",
      meltfrac,.03)
aSub,bSub=9.05,1800.
aVap,bVap=6.78,1310.
Ttr=(bSub-bVap)/(aSub-aVap)
Ptr=10**(aSub-bSub/Ttr)
qSub=log(10)*R*bSub/.044
qVap=log(10)*R*bVap/.044
check(212,"CO2 triple point temperature K via intersecting log10p",
      Ttr,216)
check(212,"CO2 triple point pressure atm",Ptr,5.15)
check(212,"CO2 sublimation heat kJ/kg",qSub/1000,783)
check(212,"CO2 vaporization heat kJ/kg",qVap/1000,570)
check(212,"CO2 fusion heat by latent-cycle Hess law kJ/kg",
      (qSub-qVap)/1000,213)
dS=cw*log(Tw/(10+Tm))+L/Tw
check(213,"1kg 10C water heated then completely boiled entropy kJ/K",
      dS/1000,7.2)
ds=Lm/Tm+cw*log(Tw/Tm)+L/Tw
check(214,"melt ice 0C heat water100C then boil entropy J/gK",
      ds/1000,8.6)
# 215-219: distinguish insufficient vs sufficient heat for ice melting.
mCu=.090;ccu=390
Tcu=363.15
released=mCu*ccu*(Tcu-Tm)
needed_ice_warming=.050*2100*3
melt=(released-needed_ice_warming)/Lm
check(215,"hot copper melting fraction 50g ice",melt/.050,.17)
dSCu=mCu*ccu*log(Tm/Tcu)
check(215,"copper alone entropy change in partial-melt setup J/K",
      dSCu,-10)
mi,mw=.1,.1
Ta=Tm+60
heat=mw*cw*(Ta-Tm)
melt_a=heat/Lm
check(216,"60C hot water cannot melt all 100g ice",float(melt_a<mi),1)
dS_a=mw*cw*log(Tm/Ta)+heat/Tm
check(216,"water60C/ice0C isolated entropy gain J/K",
      dS_a,9)
Tb=Tm+94
Tf=(mi*Tm+mw*Tb-mi*Lm/cw)/(mi+mw)
dS_b=mi*Lm/Tm+mi*cw*log(Tf/Tm)+mw*cw*log(Tf/Tb)
check(216,"water94C with ice final temperature K",
      Tf,280.2)
check(216,"water94C with ice total positive entropy J/K",
      dS_b,20)
m=5.;ql=22.5;cl=.125;Tlead=600.15
total=m*ql*(1/Tm-1/Tlead)+m*cl*(Tlead/Tm-1-log(Tlead/Tm))
check(217,"molten Pb dropped into ice bath positive entropy J/K",
      total,.48)
C=35-L*Mw/Tw
check(218,"saturated steam path negative molar heat capacity J/molK",
      C,-74)
Cwater=4.18e3*Mw
T1,T2=300.,Tw
dS=Cwater*log(T2/T1)+Mw*L/T2
check(219,"heat 1mol liquid water300K then vaporize373K entropy J/K",
      dS,125.4)
if errors:
    for e in errors:print("FAIL:",e)
    raise AssertionError(f"{len(errors)} phase transition physical benchmarks failed")
print(f"PASS: {len(checks)} source-grounded phase, critical, latent"
      " heat and entropy checks for Irodov Part II.185--219")
for n,why,x in checks:print(f" II.{n:<3} {why:<64} {x:.9g}")
