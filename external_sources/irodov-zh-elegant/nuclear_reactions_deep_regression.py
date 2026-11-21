#!/usr/bin/env python3
"""Second-pass energy/momentum/nuclear-threshold checks, Irodov VI.249--290.

Uses original problem data (including known source misprints) and explicit
units to recompute lab and COM kinematics, material attenuation, fission,
fusion and daughter isotope kinetics. Not a substitute for peer review.
"""
from math import exp,log,sqrt,sin,cos,pi,isclose
E=1.602176634e-19
C=299792458.
NA=6.02214076e23
U=1.66053906660e-27
L2=log(2.)
MEV=1e6*E
YR=365.25*86400
checks=[]
def test(n,description,actual,want,tol=.035):
    if not isclose(actual,want,rel_tol=tol,abs_tol=1e-30):
        raise AssertionError(f"VI.{n} {description} {actual:.9g} != {want:.9g}")
    checks.append((n,description,actual))
def massa(A):return A*U
def qmass(*deltas):return sum(deltas)*931.494
def threshold(delta,projectile,target):
    """Exact endothermic relativistic lab threshold, energies in MeV."""
    return delta*(1+projectile/target)+delta**2/(2*target*931.494)
def nuclear_flux_density(rho_g_cm3,A):return rho_g_cm3/A*NA

# Elastic recoil kinematics and nuclear radii, original 249--259.
m,M=4.,6.
T=7.0
def recoil_angle(gamma):
    return T/(1+(M-m)**2/(4*m*M*cos(gamma*pi/180)**2))
test(249,"Li6 recoil gamma=120 degrees MeV",recoil_angle(120),6.0)
test(249,"elastic daughter energy fraction",recoil_angle(120)/T,6/7,1e-12)
test(250,"n on d head-on neutron energy loss fraction",4*1*2/3**2,8/9,1e-12)
test(250,"n on d 90-degree neutron energy loss fraction",2/3,2/3,1e-12)
test(251,"d on p maximum lab scattering degrees",
     180/pi*__import__("math").asin(1/2),30,1e-10)
def density(r0):
    return 3*U/(4*pi*r0**3)
test(252,"literal 0.13pm nuclear kg per cm3",
     density(.13e-12)/1e6,1.805e5)
test(252,"correct 1.3fm nuclear kg per cm3",
     density(1.3e-15)/1e6,1.805e11)
test(252,"literal nuclear nucleon number per cm3",
     3/(4*pi*(.13e-12)**3)/1e6,1.0868e32)
test(252,"actual nuclear nucleon number per cm3",
     3/(4*pi*(1.3e-15)**3)/1e6,1.0868e38)
# Nuclide completion A,Z conservation, via original figure-independent data.
def balance(ain,zin,aout,zout):
    return ain==aout and zin==zout
test(253,"B10+d -> Be8+alpha mass number",10+2,8+4,1e-12)
test(253,"B10+d -> Be8+alpha charge",5+1,4+2,1e-12)
test(253,"O17+d -> n+F18 mass number",17+2,1+18,1e-12)
test(253,"O17+d -> n+F18 charge",8+1,0+9,1e-12)
test(253,"Na23+p -> Ne20+alpha mass number",23+1,20+4,1e-12)
test(253,"Na23+p -> Ne20+alpha charge",11+1,10+2,1e-12)
test(253,"Cl37+p -> Ar37+n mass number",37+1,37+1,1e-12)
test(253,"Cl37+p -> Ar37+n charge",17+1,18+0,1e-12)
test(255,"radius ratio implies beryllium A",27/1.5**3,8)
test(255,"8Be binding energy MeV",
     qmass(4*.00783,4*.00867,-.00531),56.5)
test(256,"O16 binding per nucleon MeV",
     qmass(8*.00783,8*.00867,-(-.00509))/16,8.0)
test(256,"B11 one-neutron separation MeV",
     qmass(.01294,.00867,-.00930),11.5)
test(256,"B11 alpha separation MeV",
     qmass(.01601,.00260,-.00930),8.7)
test(256,"O16 -> four alpha MeV",
     qmass(4*.00260,+.00509),14.4)
test(257,"B11 neutron/proton separation difference MeV",
     qmass(.01294,.00867,-.01354,-.00783),.22)
test(258,"Ne20 -> C12+2alpha energy MeV",
     20*8.03-12*7.68-8*7.07,11.88)
test(259,"Li8 neutral atom u",
     3*1.00783+5*1.00867-41.3/931.494,8.0225)
test(259,"C10 bare nucleus u",
     6*(1.00783-.0005485799)+4*1.00867-60.4/931.494,10.0135)
test(260,"endothermic binding-energy identity",
     (20+30)-(21+32),-3,1e-12)

# Reaction masses, fuel equivalent, lab neutron- and proton-emission dynamics.
U235_J=(1000/235)*NA*(200*MEV)
test(261,"one kg U235 fission energy J",U235_J,8.21e13)
test(261,"coal kg equivalent to 1kg U235",
     U235_J/30e6,2.74e6)
test(261,"U235 kg equivalent to 30kt TNT",
     (3e7*4.1e6)/U235_J,1.50)
Qfusion=qmass(2*.01410,-.00260)
test(262,"D+D -> alpha energy MeV",Qfusion,23.85)
fusion_J=NA/4*Qfusion*MEV
test(262,"energy from 1g helium J",fusion_J,5.75e11)
test(262,"coal mass from D fusion kg",fusion_J/30e6,1.92e4)
test(263,"Li6+d -> 2alpha total energy MeV",
     qmass(.01513,.01410,-2*.00260),22.38)
test(263,"fusion per participating nucleon MeV",
     qmass(.01513,.01410,-2*.00260)/8,2.80)
test(263,"U235 fission per nucleon MeV",200/235,.851)
test(264,"Li7+p -> 2alpha energy MeV",
     8*7.06-7*5.60,17.28)
pO=(4*4+2.09-2*sqrt(4*4*2.09)*cos(pi/3))/17
test(265,"O17 nuclear recoil energy MeV",pO,.724)
test(265,"N14 alpha-to-proton reaction Q MeV",
     2.09+pO-4,-1.19)
test(266,"Li7(p,n)Be7 reaction Q MeV",
     qmass(.01601,.00783,-.00867,-.01693),-1.64)
test(266,"Be9(n,gamma)Be10 reaction Q MeV",
     qmass(.01219,.00867,-.01354),+6.82)
test(266,"Li7(alpha,n)B10 reaction Q MeV",
     qmass(.01601,.00260,-.00867,-.01294),-2.79)
test(266,"O16(d,alpha)N14 reaction Q MeV",
     qmass(-.00509,.01410,-.00260,-.00307),3.11)
Qbor=2.79
test(267,"B10 thermal neutron alpha kinetic MeV",Qbor*7/11,1.775)
test(267,"B10 thermal neutron Li7 kinetic MeV",Qbor*4/11,1.0145)
test(267,"B10 alpha velocity m/s",
     sqrt(2*Qbor*7/11*MEV/(4*U)),9.2e6)
test(267,"B10 Li recoil velocity m/s",
     sqrt(2*Qbor*4/11*MEV/(7*U)),5.3e6)
test(268,"Li7(p,n)Be7 at neutron-rest proton MeV",
     1.65/(1-1/7),1.925)
test(269,"Be9 alpha->n90 energy MeV",
     (5.7+(1-4/12)*5.3)/(1+1/12),8.52)
Ta=(1+17.28)/2
arg=sqrt(1/(4*4*Ta))
test(270,"two-alpha each kinetic energy MeV",Ta,9.14)
test(270,"symmetrical alpha-alpha opening degrees",
     2*180/pi*__import__("math").acos(arg),170.5)
test(271,"nonrel threshold for delta2.2 and p on d MeV",
     2.2*(1+1/2),3.3)
exact=threshold(2.2,1,2)
test(271,"relativistic threshold correction keV",
     (exact-3.3)*1000,1.299)
test(272,"proton-induced deuteron breakup threshold MeV",exact,3.3)
test(273,"Li7(p,n)Be7 threshold MeV",threshold(1.65,1,7),1.886)
test(273,"Be9(p,n)B9 threshold MeV",threshold(1.85,1,9),2.056)
test(274,"B11 neutron-induced Q MeV",-4.0*11/12,-3.667)
test(275,"Li7(p,n)Be7 threshold MeV",threshold(1.65,1,7),1.886)
test(275,"Li7(p,d)Li6 threshold MeV",threshold(5.03,1,7),5.75)
test(276,"Li7(alpha,n)B10 threshold MeV",
     threshold(2.79,4,7),4.4)
talpha=threshold(2.79,4,7)
test(276,"B10 threshold COM speed m/s",
     sqrt(2*4*U*talpha*MEV)/(11*U),5.3e6)
Q277=-6.17*12/13
test(277,"C12 neutron alpha reaction Q MeV",Q277,-5.70)
test(277,"90deg alpha kinetic MeV",
     ((1-1/9)*10+Q277)/(1+4/9),2.2)
test(278,"deuteron photon threshold excess percent",
     2.2/(2*2*931.494)*100,.059)
test(279,"proton capture He3 compound excitation MeV",
     (7.72-2.22)+(2/3)*1.5,6.50)
test(279,"compound excitation above d+p breakup MeV",
     6.50-(7.72-2.22),1.0)
energies=[16.16+(13/15)*en for en in [.60,.90,1.55,1.80]]
for value,expected in zip(energies,[16.68,16.94,17.50,17.72]):
    test(280,f"N15 compound resonance {expected:g} MeV",value,expected)

# Transport, target activation, reactor generation.
nCd=nuclear_flux_density(8.65,112.4)
sigCd=log(360)/(nCd*.05)/1e-24
test(281,"thermal Cd effective cross section barns",sigCd,2540)
nWater=nuclear_flux_density(1.11,20.)
atten=exp(nWater*(2*7+4.2)*1e-24*5)
test(282,"D2O neutron beam attenuation factor",atten,20.9)
nFe=nuclear_flux_density(7.87,55.85)
frac=(11/13.5)*(1-exp(-nFe*13.5e-24*.5))
test(283,"iron scattering-removal probability",frac,.355)
lambdaBe=log(2)/(53*86400)
w=1.35e8*E/(10e-6*7200*lambdaBe)
test(284,"Be7 accelerator reaction yield",w,.00199)
a=1e10*(98e-24)
lam=log(2)/(2.7*86400)
n0=.01/197*NA
deplete=-log(.99)/a
test(285,"1pct stable gold depletion yr",deplete/YR,325)
test(285,"target-as-reservoir saturation nuclei",
     a*n0/lam,1.01e13)
tstar=log(lam/a)/(lam-a)
test(285,"exact gold product peak days",tstar/86400,58.1)
Nstar=a*n0/(lam-a)*(exp(-a*tstar)-exp(-lam*tstar))
test(285,"exact gold product peak inventory",Nstar,1.008e13)
test(285,"peak daughter activity Bq",lam*Nstar,2.99e7)
# 286 source activation with and without parent depletion.
t=1.0e6
n=1e15
a=.8e-7
lam=2e-6
simple=a*n/lam*(1-exp(-lam*t))
exact_prod=a*n/(lam-a)*(exp(-a*t)-exp(-lam*t))
test(286,"finite target depletion activation state ratio",
     exact_prod/simple,.98,.04)
# 287 delayed activity neutron flux inverse solution.
N0=.2/197*NA
half=2.7*86400
lam=log(2)/half
J=1.9e7*exp(lam*(12*3600))/(96e-24*N0*(1-exp(-lam*6*3600)))
test(287,"delayed Au198 activation flux cm-2s-1",J,5.9e9)
test(288,"generation100 from original gen1",1000*1.05**99,1.25e5)
test(289,"100MW fission-neutron production s-1",
     2.5*100e6/(200*MEV),7.80e18)
test(290,"reactor gain in sixty seconds",
     1.010**(60/1.10),1.72)
test(290,"reactor e-folding seconds",1.10/log(1.010),110.5)
print(f"PASS: {len(checks)} independent nuclear reactions/recoil/threshold/"
      "activation/regeneration calculations on original Part VI.249--290.")
for no,subject,value in checks:
    print(f" VI.{no:<3} {subject:<52} {value:.8g}")
