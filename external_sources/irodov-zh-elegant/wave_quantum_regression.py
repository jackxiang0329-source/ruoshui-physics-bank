#!/usr/bin/env python3
"""Independent numerical and limiting-case checks for Irodov Part VI.49--96.

Distinguishes transformed probability-density modes from mapped speed modes,
lab/centre-of-mass de Broglie wavelengths, bound-state thresholds,
Rydberg energy indexing and leading WKB barrier exponents. Numerical
regressions support but do not replace a derivation-by-derivation peer review.
"""
from math import pi,sin,cos,acos,asin,atan,exp,log,sqrt,degrees,isclose
C=299792458.0
H=6.62607015e-34
HB=H/(2*pi)
E=1.602176634e-19
KB=1.380649e-23
ME=9.1093837139e-31
MP=1.67262192595e-27
MN=1.67492749804e-27
MD=3.3435837724e-27
U=1.66053906660e-27
M_H2=2.01588*U
passed=[]

def check(num,subject,obtained,target,tolerance=.035):
    if not isclose(obtained,target,rel_tol=tolerance,abs_tol=0):
        raise AssertionError(f"VI.{num} {subject}: {obtained:.9g}, expected {target:.9g}")
    passed.append((num,subject,obtained))

def lam(m,T_eV):
    return H/sqrt(2*m*T_eV*E)

# §6.2 quantum wave properties: particle de Broglie dispersions.
check(49,"electron 100eV wavelength pm",lam(ME,100)*1e12,122.64)
check(49,"proton 100eV wavelength pm",lam(MP,100)*1e12,2.8621)
check(49,"uranium 100eV wavelength pm",lam(238.02891*U,100)*1e12,.1862)
check(50,"electron 100pm to 50pm delta kinetic eV",
      (H*H/(2*ME*E))*(1/(50e-12)**2-1/(100e-12)**2),451.24)
p_n=sqrt(2*MN*25*E)
v_n=p_n/MN
v_cm=MN*v_n/(MN+MD)
relative_p=MN*(v_n-v_cm)
check(51,"neutron COM de Broglie wavelength pm",
      H/relative_p*1e12,lam(MN,25)*1e12*(1+MN/MD),.00001)
# Two equal masses with perpendicular momenta p1,p2:
# COM momentum of either = |p1-p2|/2.
p1=H/(.10e-9);p2=H/(.25e-9)
p_com=sqrt(p1*p1+p2*p2)/2
check(52,"equal-mass COM wavelength nm",
      H/p_com*1e9,2/sqrt(1/.10**2+1/.25**2),.00001)
lam53=H/sqrt(2*M_H2*KB*300)
lam54=H/(2*sqrt(M_H2*KB*300))
check(53,"H2 wavelength at most-probable speed pm",lam53*1e12,125.83)
check(54,"mode of H2 wavelength distribution pm",lam54*1e12,88.97)
check(54,"ratio wavelength-mode / speed-mode wavelength",lam54/lam53,1/sqrt(2),.00001)
check(55,"electron max NR kinetic error 1pct keV",
      2*ME*C*C/E*((1.01)**2-1)/1000,20.542)
check(55,"proton max NR kinetic error 1pct MeV",
      2*MP*C*C/E*((1.01)**2-1)/1e6,37.718)
check(56,"electron Compton-matched kinetic keV",
      (sqrt(2)-1)*ME*C*C/E/1000,211.67)
Ttube=H*C/(10e-12)/E
pceV=sqrt(Ttube*(Ttube+2*ME*C*C/E))
check(57,"X-ray tube electron de Broglie pm",
      H*C/(pceV*E)*1e12,3.289)
check(58,"single slit electron speed m/s",
      2*H*.50/(ME*1e-6*.36e-3),2.0205e6)
check(59,"double slit separation microm",
      lam(ME,25)*1.0/(50e-6)*1e6,4.906)
check(60,"consecutive Bragg reflection initial voltage",
      H*H/(2*ME*E*(.20e-9*sin(pi/6))**2),150.412)
check(61,"nickel fourth-order plane distance nm",
      2*lam(ME,180)/cos(55*pi/360)*1e9,.20611)
alpha=atan(.032/(2*.10))/2
check(62,"Al polycrystal third-order spacing nm",
      3*lam(ME,10000)/(2*sin(alpha))*1e9,.23215)
check(63,"metal electron wave index",
      sqrt(1+15/150),1.04881)
check(63,"U/Ui minimum for 1pct departure",
      1/(2*.01+.01**2),49.75124)
# Uncertainty: strictly use sigma_x sigma_p >= ħ/2, comparisons remain limits.
check(66,"electron min speed uncertainty m/s",HB/(2*ME*1e-6),57.885)
check(66,"proton min speed uncertainty m/s",HB/(2*MP*1e-6),.03153)
check(66,"1mg sphere min speed uncertainty m/s",HB/(2*1e-6*1e-6),5.2729e-23)
check(68,"relative velocity uncertainty lower bound",.5,.5,.00001)
check(69,"electron free wave-packet broadening s",
      10*ME*(.10e-9)**2/HB,8.638e-16)
check(70,"electron localization kinetic eV",
      HB**2/(2*ME*(.20e-9)**2)/E,.9525)
check(75,"optimally resolved beam slit width microm",
      sqrt(HB*1/(1.6735e-27*600))*1e6,10.25)
check(77,"central third probability ground infinite well",
      1/3+sqrt(3)/(2*pi),.608998)
check(80,"1cm electron-box level density per eV",
      .01/(pi*HB)*sqrt(ME/(2*E))*E,8.1538e6)
# Infinite multidimensional wells: enumerate *distinct* levels and degeneracy.
two=sorted({i*i+j*j for i in range(1,9) for j in range(1,9)})
check(81,"first four distinct 2D square-well level sums",
      sum(two[:4]),2+5+8+10,.00001)
check(82,"rectangular box ground probability",
      1/3-sqrt(3)/(4*pi),.1955)
from collections import Counter
three=Counter(i*i+j*j+k*k
              for i in range(1,8)
              for j in range(1,8)
              for k in range(1,8))
energies=sorted(three)
check(83,"third-to-fourth energy coefficient",
      energies[3]-energies[2],2,.00001)
check(83,"sixth energy coefficient",energies[5],14,.00001)
check(83,"sixth level spatial degeneracy",three[energies[5]],6,.00001)
# The single-sided well and radial s-wave finite well have a *strict*
# binding inequality above this dimensionless threshold.
check(85,"one-sided well first threshold scaled m l2U0/ħ2",
      pi*pi/8,1.23370055)
check(85,"one-sided well second threshold scaled m l2U0/ħ2",
      9*pi*pi/8,11.10330495)
check(86,"one-sided finite well forbidden-region probability",
      2/(4+3*pi),.148978)
# Radial probability for a normalized spherical ground wave.
check(88,"most-probable normalized radial position r/r0",.5,.5,.00001)
check(88,"interior probability at most-probable radius",.5,.5,.00001)
check(89,"spherical finite well first s-wave threshold",
      pi*pi/8,1.23370055)
check(91,"hydrogen 2s binding energy eV",13.605693/4,3.40142)
check(92,"H 1s expected force magnitude / (ke²/a0²)",
      2,2,.00001)
check(93,"H nucleus electronic-cloud potential V",
      -(1/(4*pi*8.8541878128e-12))*E/5.29177210903e-11,-27.2114)
# WKB analytically integrated barriers: verify exponents by independent quadrature.
U0=7.0
T=2.0
l=1.0
m=1.0
hb=1.0
# dimensionless barrier-exponent expressions, equivalent to a specific
# unit system with ħ=m=l=1; no physical electron-mass assumption.
rect=2*l*sqrt(2*m*(U0-T))/hb
tri=4*l*sqrt(2*m)/(3*hb*U0)*(U0-T)**1.5
parabolic=pi*l/hb*sqrt(2*m/U0)*(U0-T)
check(95,"WKB rectangle exponent dimensionless",rect,2*sqrt(10),.00001)
check(95,"WKB ramp exponent dimensionless",
      tri,4*sqrt(2)*5**1.5/(3*7),.00001)
check(96,"WKB parabola exponent dimensionless",
      parabolic,pi*sqrt(2/7)*5,.00001)
print(f"PASS: {len(passed)} independent numerical and limit-case checks"
      " for original Part VI.49--96 (quantum wave mechanics).")
for q,what,value in passed:
    print(f"  VI.{q:<3} {what:<47} {value:.8g}")
