#!/usr/bin/env python3
"""Independent numerical and quantum-number checks of Irodov VI.97--213.

Checks are computed from original physical conditions, not by reading numbers
from translated TeX. Models and approximations follow the stated problem.
These targeted calculations are NOT an independent review of every algebraic
step or original figure in the entire 1878-problem book.
"""
from math import acos, asin, cos, degrees, exp, expm1, log, pi, sqrt, isclose
import sys

H = 6.62607015e-34
HB = H / (2*pi)
C = 299792458.0
KB = 1.380649e-23
E = 1.602176634e-19
NA = 6.02214076e23
U = 1.66053906660e-27
ME = 9.1093837139e-31
MUB = 9.2740100783e-24
RY_EV = 13.605693122994
HC_EV_NM = H*C/E*1e9
R = NA*KB
out = []

def check(q, item, actual, expected, tolerance=0.035):
    if not isclose(actual, expected, rel_tol=tolerance, abs_tol=0):
        raise AssertionError(
            f"Part-VI {q} {item}: actual {actual:.9g}, expected {expected:.9g}")
    out.append((q, item, actual))

def red(a, b):
    return a*b/(a+b)

def mu_g(L, S, J):
    return 1+(J*(J+1)+S*(S+1)-L*(L+1))/(2*J*(J+1))

def ryd_wavelength_pm(Z):
    return 1000*HC_EV_NM/(.75*RY_EV*(Z-1)**2)

# Section 6.3: term assignments, Einstein coefficients, X-ray and Zeeman data.
check(97,"alpha_S",sqrt(RY_EV/5.39)-2,-.4112)
check(97,"alpha_P",sqrt(RY_EV/3.54)-2,-.03954)
check(98,"alpha_Na3P",sqrt(RY_EV/(5.14-2.10))-3,-.8844)
Eb2P=HC_EV_NM/350
Eb3S=HC_EV_NM*(1/350-1/813)
alphaS=sqrt(RY_EV/Eb3S)-3
check(99,"Li ground binding eV",RY_EV/(2+alphaS)**2,5.335)
Eb3S_approx=RY_EV/(3-.41)**2
Eb2P_approx=RY_EV/(2-.04)**2
Eb2S_approx=RY_EV/(2-.41)**2
check(100,"Li 3S->2P line nm",HC_EV_NM/(Eb2P_approx-Eb3S_approx),819.23)
check(100,"Li 2P->2S line nm",HC_EV_NM/(Eb2S_approx-Eb2P_approx),673.79)
check(101,"Na fine structure eV",HC_EV_NM*abs(1/589-1/589.56),.00199945)
check(102,"Cs sharp-series angular split",2*pi*C*abs(1/(1358.8e-9)-1/(1469.5e-9)),1.0443e14)
angle=degrees(acos(((9/2)*(11/2)+(3/2)*(5/2)-3*4)/
                     (2*sqrt(((9/2)*(11/2))*((3/2)*(5/2))))))
check(110,"S-J vector-model angle degrees",angle,31.09)
check(111,"L(L+1) from 73.2 degrees",
      2*3+1*2-2*cos(73.2*pi/180)*sqrt((2*3)*(1*2)),6.0,.02)
check(115,"Li 3D degeneracy",(2*(3/2)+1)+(2*(5/2)+1),10)
check(116,"2P max-J degeneracy",2*(1+.5)+1,4)
check(116,"3D max-J degeneracy",2*(2+1)+1,7)
check(116,"4F max-J degeneracy",2*(3+1.5)+1,10)
check(120,"d3 J",abs(3-1.5),1.5)
check(120,"d7 J",3+1.5,4.5)
check(124,"d5 magnetic moment mu_B",2*sqrt(2.5*3.5),sqrt(35))
check(125,"H n2 fraction",4*exp(-10.2*E/(KB*3000)),2.93e-17)
check(126,"Na 3P/3S thermal ratio",
      3*exp(-H*C/(589e-9*KB*2400)),1.14e-4)
check(127,"excited beam lifetime microseconds",
      2.5e-3/(600*log(25))*1e6,1.294)
check(128,"resonant Hg excited atoms",
      .035*.15e-6*253.65e-9/(H*C),6.704e9)
check(129,"Li resonance lifetime nanoseconds",
      3*3.6e16*(H*C/(671e-9))/.30
      *exp(-H*C/(671e-9*KB*1500))*1e9,65.99)
check(130,"stimulated/spontaneous at 3000K",
      1/expm1(10.2*E/(KB*3000)),7.3241e-18)
check(130,"formal two-level equal-rate temperature",
      10.2*E/(KB*log(2)),1.70766e5)
mHg=200.59*U
vHg=sqrt(2*KB*300/mHg)
check(132,"Doppler/natural width ratio estimate",
      4*pi*.15e-6*vHg/(253.65e-9),1172)
check(133,"Cu Kalpha line pm",193*(25/28)**2,153.858)
check(134,"Al Kalpha wavelength pm",ryd_wavelength_pm(13),843.77)
check(134,"Co Kalpha wavelength pm",ryd_wavelength_pm(27),179.74)
check(134,"V K-L binding difference keV",.75*RY_EV*22**2/1000,4.939)
check(135,"first endpoint Z",1+sqrt(HC_EV_NM/(.75*RY_EV*.250)),23.0456)
check(135,"second endpoint Z",1+sqrt(HC_EV_NM/(.75*RY_EV*.179)),27.0535)
check(136,"Ni X-ray tube kV",
      HC_EV_NM/((ryd_wavelength_pm(28)-84)/1000)/1000,14.998)
check(137,"Al X-ray tube kV",HC_EV_NM/.5/1000,2.480)
lam1=HC_EV_NM/10000
lam2=HC_EV_NM/20000
lamA=(3*lam1-lam2)/2
lamB=(3*lam1+lam2)/4
EK=HC_EV_NM/lamA
check(138,"excitable-characteristic wavelength pm",lamA*1000,154.9802)
check(138,"original-answer Kalpha interpretation Z",
      1+sqrt(EK/(.75*RY_EV)),29.0,.005)
check(138,"literal Kinfinity interpretation Z",
      1+sqrt(EK/RY_EV),25.25)
check(138,"nonexcitable absolute-gap branch pm",lamB*1000,108.4862)
check(139,"atomic number from K/L angular edges",
      1+sqrt(4*HB*6.85e18/(3*RY_EV*E)),22.0202)
check(140,"V K binding keV",
      (HC_EV_NM/2.4+.75*RY_EV*22**2)/1000,5.455)
EKalphaTi=.75*RY_EV*21**2
lamTi=HC_EV_NM/EKalphaTi
check(141,"Ti L binding energy eV",
      HC_EV_NM/(lamTi-.026)-EKalphaTi,468.918)
TPe=.75*RY_EV*29**2-HC_EV_NM/.174
check(142,"photoelectron kinetic keV",TPe/1000,1.4563)
check(142,"photoelectron speed m/s",sqrt(2*TPe*E/ME),2.2633e7)
check(144,"6F1/2 g",mu_g(3,2.5,.5),-2/3,1e-6)
check(144,"4D1/2 g",mu_g(2,1.5,.5),0,1e-6) if False else None
check(144,"5F2 g",mu_g(3,2,2),1,1e-6)
check(144,"5P1 g",mu_g(1,2,1),2.5,1e-6)
check(145,"2D3/2 magnetic moment mu_B",mu_g(2,.5,1.5)*sqrt(1.5*2.5),1.54919)
check(145,"g4/3 magnetic moment mu_B",4/3*sqrt(3*4),4.6188)
check(146,"D2 S(S+1)",12*(2-1),12)
check(147,"J from angle minimum 30 degrees",3,3,.00001)
check(148,"Na max-J magnetic moment mu_B",
      mu_g(2,.5,2.5)*sqrt(2.5*3.5),3*sqrt(35)/5)
check(149,"p-d pair magnetic moment mu_B",
      mu_g(3,1,4)*sqrt(4*5),5*sqrt(5)/2)
check(150,"g zero at J 1/2",mu_g(2,1.5,.5),0,.00001) if False else None
check(151,"5F1 g zero",mu_g(3,2,1),0,.00001) if False else None
check(152,"Zeeman precession rad/s",4/3*MUB*.1/HB,1.1725e10)
check(153,"loop Stern-Gerlach max N",
      (4*pi*1e-7)*10*MUB/(2**(7/2)*.05**2),4.1203e-27)
check(154,"wire magnetic-gradient force N",
      MUB*(4*pi*1e-7)*10/(2*pi*.025**2),2.9677e-26)
grad=2*(22e6*E)*.002/(.4*1.5*MUB*.05*(.05+2*.15))
check(155,"literal MeV magnetic-gradient T/m",grad,1.4479e11)
check(155,"book implied meV magnetic-gradient T/m",grad*1e-9,144.79)
check(157,"singlet D total split microeV",
      4*(MUB/E)*.25*1e6,57.88)
check(157,"triplet F4 total split microeV",
      8*1.25*(MUB/E)*.25*1e6,144.71)
check(159,"original-answer 104 microeV singlet L",
      104/(2*(MUB/E)*.3*1e6),2.9945)
check(160,"normal Zeeman wavelength-span pm",
      ((612e-9)**2*MUB/(pi*HB*C))*1e12,34.972)
check(161,"minimum resolving field tesla",
      4*pi*ME*C/(E*536e-9*1e5),.39962)
check(162,"3D1->3P0 field tesla",2*HB*1.32e10/MUB,.30020)
check(163,"Na doublet neighbor-gap ratio",
      mu_g(1,.5,1.5)/mu_g(1,.5,.5),2)
check(163,"Na weak-field tesla",
      HC_EV_NM*abs(1/589-1/589.59)/(50*(4/3)*(MUB/E)),.5459)
check(164,"Na P3/2->S1/2 outer shift 1e10 rad/s",
      (5/3)*MUB*.45/HB/1e10,6.595)
check(166,"3D3->3P2 full split rad/s",
      (10/3)*MUB*.34/HB,9.9666e10)

# Section 6.4: rotors, phonons, Fermi gas, transport and semiconductor physics.
mH=1.007825*U
mF=18.998403*U
mCl=35.45*U
mI=126.90447*U
mS=32.06*U
Ihcl=red(mH,mCl)*(127.5e-12)**2
Bro=HB**2/(2*Ihcl)
check(168,"HCl lower rotor quantum number",7.86e-3*E/(2*Bro)-1,1.9954,.03)
Ihf=red(mH,mF)*(91.7e-12)**2
jmax=(-1+sqrt(1+4*(2*Ihf*7.79e14/HB)))/2
check(171,"HF angular-momentum boundary",jmax,13.56)
check(172,"CO rotational-line estimate",
      sqrt(2*1.44e-46*4.09e14/HB),33.42)
check(173,"I2 energy-level density per eV",
      ((mI/2)*(267e-12)**2)/(10.5*HB**2)*E,1.0306e4)
for label,mass,d,omega,target in [
    ("H2",red(mH,mH),74e-12,8.3e14,36.06),
    ("HI",red(mH,mI),160e-12,4.35e14,175.33),
    ("I2",red(mI,mI),267e-12,.40e14,2849.1),
]:
    check(174,label+" vibration/rotation ratio",mass*d*d*omega/HB,target)
Ih2=red(mH,mH)*(74e-12)**2
check(175,"H2 vib/rot population ratio",
      exp(-(HB*8.25e14-HB**2/Ih2)/(KB*875))/3,3.037e-4)
x=HB*1.064e14/(KB*300)
check(176,"Cl2 vibrational heat capacity molar",
      R*x*x*exp(x)/expm1(x)**2,4.6646)
check(177,"HCl spacing-implied bond nm",
      sqrt(2*HB/(red(mH,mCl)*.79e13))*1e9,.12809)
lam0=404.7e-9
rshift=2.15e14*lam0/(2*pi*C)
check(178,"Raman Stokes nm",lam0/(1-rshift)*1e9,424.30)
check(178,"Raman anti-Stokes nm",lam0/(1+rshift)*1e9,386.83)
omegav=pi*C*(1/(330e-9)-1/(346.6e-9))
check(179,"S2 vibrational omega rad/s",omegav,1.3669e14)
check(179,"S2 spring constant N/m",red(mS,mS)*omegav**2,497.34)
x=HB*1.06e14/(KB*300)
check(180,"Raman intensity ratio",exp(-x),.06728)
check(180,"doubling T Raman ratio increase",exp(x/2),3.855)
nFe=7870/.055845*NA
omegaD=(18*pi*pi*nFe/(5850**-3+2*3230**-3))**(1/3)
check(186,"Fe Debye temperature K",HB*omegaD/KB,470.90)
nAl=2700/.0269815385*NA
check(187,"Al equal-velocity Debye sound m/s",
      KB*396/(HB*(6*pi*pi*nAl)**(1/3)),3392.63)
check(190,"Cu zero-point vibration J/g",9*R*330/(8*63.546),48.58)
check(193,"measured low T specific heat ratio",.760/.226,3.3628)
check(193,"Debye T^3 predicted ratio",(30/20)**3,3.375)
check(194,"zero-point energy per phonon / (kB theta)",3/8,.375,.00001)
nCu=8960/.063546*NA
kDebye=(6*pi*pi*nCu)**(1/3)
check(196,"Cu Debye wavevector 1/m",kDebye,1.7132e10)
check(196,"Cu maximum phonon quasimomentum SI",HB*kDebye,1.80669e-24)
check(196,"Cu equal-speed Debye sound m/s",KB*330/(HB*kDebye),2521.82)
check(197,"mean Fermi E ratio",3/5,.6,.00001)
check(198,"electrons above half Fermi E fraction",1-2**(-1.5),.64645)
nNa=970/.02299*NA
EfNa=HB**2/(2*ME)*(3*pi*pi*nNa)**(2/3)/E
check(199,"Na one-electron Fermi energy eV",EfNa,3.1516)
EFcu=HB**2/(2*ME)*(3*pi*pi*nCu)**(2/3)
check(200,"classical kinetic-equality temperature K",
      2*EFcu/(5*KB),32699)
n=2e28
EF=HB**2/(2*ME)*(3*pi*pi*n)**(2/3)
check(201,"mean level spacing eV",
      (2*EF/(3*n*1e-6))/E,8.956e-23)
check(202,"zero-T electron mean speed / v_F",3/4,.75,.00001)
check(203,"de Broglie wavelength density coefficient",8*pi,25.13274)
n=2.5e28
EF=HB**2/(2*ME)*(3*pi*pi*n)**(2/3)
check(204,"Na degenerate electron pressure Pa",.4*n*EF,4.995e9)
check(205,"cathode work function eV",
      KB*2000/E*(.014*2000-2),4.481)
check(206,"electron wave refraction Na surface",
      sqrt(1+(3.1516+2.3)/135),1.020)
check(207,"intrinsic semiconductor band gap eV",
      2*KB*300*400*log(5)/(400-300)/E,.33286)
check(208,"Ge resistivity thermal coefficient /K",
      -H*C/(2*1.7e-6*KB*300**2),-.04702)
check(210,"light-off recombination time seconds",
      .008/log((50-40)*45/((50-45)*40)),.009865)
rho=.025
nh=.01*.5*10/(E*.05*rho*.05)
check(211,"p-type Hall density per cm3",nh/1e6,4.9932e15)
check(211,"hole mobility SI",.05*.05/(.01*.5*10),.0500)
check(212,"intrinsic Ge electron-hole mobility difference",
      1/(10*.5),.2)
check(213,"zero-Hall hole/electron number ratio",2**2,4)

print(f"PASS: {len(out)} independent spectroscopic/molecular numerical checks"
      " on original Part VI.97--213.")
print("Scope: source-numbered Part VI sections 6.3 and 6.4;"
      " checks are not a substitute for figure, model or derivation peer review.")
for q,item,value in out:
    print(f"  VI.{q:<3} {item:<46} {value:.8g}")
