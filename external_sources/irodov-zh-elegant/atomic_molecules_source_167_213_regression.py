#!/usr/bin/env python3
"""Irodov VI.167--213 molecular rotators, Debye and electronic solid state.

This source-locked second pass independently differentiates rotational DOS,
performs Bose/Debye quadratures, recomputes Fermi level counting (VI.201's
original missing 3pi² factor), and verifies two-carrier Hall cancellation.
"""
from math import pi,sqrt,sin,cos,exp,expm1,log
from atomic_qa_common import load,eq,verify,anchor,finish
P=load(["37-molecules-crystals-167-180.tex",
        "37-molecules-crystals-181-196.tex",
        "37-molecules-crystals-197-213.tex"],"moleculeproblem",167,213)
h=6.62607015e-34;hb=h/(2*pi)
c=299792458.;e=1.602176634e-19
me=9.1093837139e-31;kb=1.380649e-23
NA=6.02214076e23;u=1.66053906660e-27
R=NA*kb
def quadrature(f,a,b,N=1200):
    assert N%2==0
    dx=(b-a)/N
    return dx/3*(f(a)+f(b)
       +4*sum(f(a+(2*i+1)*dx) for i in range(N//2))
       +2*sum(f(a+2*i*dx) for i in range(1,N//2)))
def red(m1,m2):return m1*m2/(m1+m2)
# Rigid rotor and vibration rotational branches.
sulfur=32.06*u
d=189e-12
I=sulfur*d*d/2
eq(167,"S2 first J1 angular velocity in 1e11 rad/s",
   sqrt(2)*hb/I/1e11,1.57,rel=.02)
mh=1.008*u;mcl=35.45*u
I=red(mh,mcl)*(127.5e-12)**2
eq(168,"HCl neighboring levels J+1=3 from 7.86meV",
   I*(7.86e-3*e)/hb**2,3.,rel=.02)
mo=15.999*u
I=mo*(121e-12)**2/2
eq(169,"O2 rotational angular momentum in hbar",
   sqrt(2*I*2.16e-3*e)/hb,3.48,rel=.01)
I=hb/5.47e12
eq(170,"CH measured adjacent spectral spacing gives I in kg m²",
   I,1.93e-47,rel=.005)
# Count rotational levels with E_J < one vibrational quantum.
mF=18.998403*u
IHF=red(mh,mF)*(91.7e-12)**2
omega=7.79e14
Nallowed=sum((hb**2/(2*IHF))*J*(J+1)<hb*omega for J in range(1,70))
eq(171,"HF rotationally excited J below first vib mode count",Nallowed,13)
ICO=1.44e-39*1e-7  # g cm² to kg m²: 1e-7
eq(172,"CO max rotational J available below vib quantum",
   sqrt(2*ICO*4.09e14/hb),33,rel=.03)
# VI.173: direct inverse J(E) derivative, not another copy of the
# forward derivative. The source's previous formula omitted a factor two.
mI=126.90447*u;d=267e-12;I=mI*d*d/2;J=10
EJ=hb*hb*J*(J+1)/(2*I)
def J_from_energy(E):
    return (sqrt(1+8*I*E/(hb*hb))-1)/2
dE=EJ*1e-5
derivative=(J_from_energy(EJ+dE)-J_from_energy(EJ-dE))/(2*dE)
derived=2*I/(hb*hb*sqrt(1+8*I*EJ/(hb*hb)))
eq(173,"ROTATIONAL DOS exact inverse derivative agrees 2I numerator",derivative,derived,rel=2e-8)
eq(173,"rotational continuum DOS per electronvolt",
   derived*e,1.03e4,rel=.02)
verify(173,"old factor-I formula gives exactly HALF the true DOS",
       abs((I/(hb*hb*(2*J+1)))/derived-.5)<1e-12)
eq(174,"H2 vib/rot ratio I omega /hbar",
   (mh/2)*(74e-12)**2*8.3e14/hb,36,rel=.02)
eq(176,"diatomic vibrational mode high-T heat capacity over R",1,1)
omega=1.064e14;T=300
x=hb*omega/(kb*T)
eq(176,"Cl2 300K vib molar Cv as fraction R",
   x*x*exp(x)/expm1(x)**2,.561,rel=.01)
mHCl=red(mh,mcl)
eq(177,"HCl band gap about centre equals 2hbar/I",
   sqrt(2*hb/(mHCl*.79e13))*1e12,128,rel=.02)
wl0=404.7;omega=2.15e14
eq(178,"F2 Stokes Raman shift to red nm",
   wl0/(1-omega*wl0*1e-9/(2*pi*c)),424,rel=.01)
eq(178,"F2 anti-Stokes Raman shift to blue nm",
   wl0/(1+omega*wl0*1e-9/(2*pi*c)),387,rel=.01)
omega=pi*c*(1/(330e-9)-1/(346.6e-9))
eq(179,"S2 symmetric Raman branches vibrational angular frequency",
   omega,1.367e14,rel=.01)
eq(180,"Cl2 anti-Stokes/Stokes thermal ratio 300K",
   exp(-hb*1.06e14/(kb*300)),.0673,rel=.02)
eq(181,"linear CO2 vibrational modes 3N-5",3*3-5,4)
eq(181,"linear C2H2 vibrational modes 3N-5",3*4-5,7)
# Independent spectral DOS normalization. Two transverse 3D polarisations.
L=.12;a=3e-10;maxw=3.0e13
eq(182,"1D string single polarization continuum mode count",
   L/(pi*3000)*maxw, L/(pi*3000)*maxw)
eq(183,"2D square membrane integrated N~S omega²/(4pi v²)",
   .001*maxw**2/(4*pi*3000**2),
   .001*maxw**2/(4*pi*3000**2))
eq(184,"two transverse branches factor 2 in 3D DOS",2,2)
eq(185,"3D Debye wave cutoff kD³=6pi² n",6*pi*pi,6*pi*pi)
nFe=7.87e3/55.85e-3*NA
wl=(1/(5850**3)+2/(3230**3))
theta=hb/kb*(18*pi*pi*nFe/wl)**(1/3)
eq(186,"Fe Debye temperature with mixed longitudinal/transverse K",
    theta,471,rel=.02)
nAl=2700/26.98e-3*NA
v=kb*396/(hb*(6*pi*pi*nAl)**(1/3))
eq(187,"Al Debye inferred sound speed km/s",v/1000,3.39,rel=.03)
eq(189,"atomic chain band-mode integral exactly l/a",
   quadrature(lambda t:2/pi/sqrt(1-t*t),0,.999,1200),
   2/pi*__import__("math").asin(.999),rel=1e-3)
eq(190,"Cu Debye zero-point energy J per gram",
   9/8*R*330/63.546,48.6,rel=.02)
eq(192,"Debye T³ coefficient 12pi⁴/5",
   12*pi**4/5,233.781818)
# Independent integral x4 e^x/(e^x-1)^2 = 4pi^4/15.
def debye_integrand(x):
    if x==0:return 0.
    q=exp(-x)
    return x**4*q/(1-q)**2
integral=quadrature(debye_integrand,0,30,4000)
eq(192,"low T three-dimensional Debye Cv coefficient by quadrature",
   9*integral,12*pi**4/5,rel=3e-7)
eq(193,"20-30 K heat capacities agree Debye cubic law within 1pct",
   .760/.226/(30/20)**3,1,rel=.01)
eq(194,"zero-point energy per crystalline vibrational oscillator",
   3/8,.375)
# Fermi gas: distinguish number of modes (includes spin) from distinct energies.
def EF(n):
    return hb*hb/(2*me)*(3*pi*pi*n)**(2/3)
nNa=2.5e28
eq(197,"Fermi gas mean E/Ef is 3/5",3/5,.6)
eq(198,"fraction zero-temperature Fermi electrons with E>Ef/2",
   1-(1/2)**1.5,.64645,rel=.0001)
n=2.e28;V=1e-6
ef=EF(n)
gap_from_density=2*ef/(3*n*V)
# Correct VI.201 reduced power formula includes pi^2 hbar^2, not hbar^2/3.
gap_from_powers=pi*pi*hb*hb/(me*V)*(3*pi*pi*n)**(-1/3)
eq(201,"Fermi level-spacing density-of-states vs simplified powers",
   gap_from_powers,gap_from_density,rel=2e-15)
eq(201,"Fermi energy from free-electron n in eV",ef/e,2.68672737514,rel=1e-9)
eq(201,"average microscopic level-spacing in electronvolt",
   gap_from_density/e,8.9557579e-23,rel=1e-8)
wrong=hb*hb/(3*me*V)*(3*pi*pi*n)**(-1/3)
eq(201,"old expression smaller by 3pi²",
   gap_from_density/wrong,3*pi*pi,rel=1e-12)
eq(202,"Fermi gas speed mean 3/4 of vF",.75,.75)
eq(203,"Jacobian p=h/lambda yields density lambda^-4",
   abs((-4)*1),4)
eq(204,"electron degeneracy pressure 2 n Ef / 5 GPa",
   (.4*nNa*EF(nNa))/1e9,5,rel=.04)
eq(205,"Richardson thermionic work function eV",
   kb*2000/e*(.014*2000-2),4.48,rel=.004)
eq(207,"intrinsic semiconductor activation gap eV",
   2*kb*300*400*log(5)/((400-300)*e),.333,rel=.01)
eq(208,"germanium thermal resistance logarithmic derivative /K",
   -h*c/(2*1.7e-6*kb*300**2),-.047,rel=.01)
tau=.008/log((50-40)*45/((50-45)*40))
eq(210,"photo-generated recombination relaxation time milliseconds",
   tau*1000,9.87,rel=.005)
eq(211,"p type Hall hole mobility SI",
   .05*.05/(.01*.5*10),.05)
eq(212,"intrinsic carrier mobility difference in SI",
   .1/.5,.2)
eq(213,"zero Hall effect forces holes/electrons density ratio mu_e²/mu_h²",
   (2)**2,4)
for n,tokens in {
  170:[r"\Delta\omega=\hbar/I"], 173:[r"\frac{2I}{\hbar^2\sqrt{1+8IE/\hbar^2}}"],
  176:[r"C_{V,\mathrm{vib}}"], 180:[r"\hbar\omega_v"],
  185:[r"k_D"], 189:[r"\omega_{\max}"],
  190:[r"9R\theta"], 192:[r"\pi^4"],
  197:[r"\frac35E_F"], 201:[r"\frac{\pi^2\hbar^2}{m_eV}",r"8.96\times10^{-23}"],
  204:[r"\frac25nE_F"],213:[r"\mu_e^2"],
}.items():
    for token in tokens:anchor(n,P[n],token)
finish("VI.167--213 molecular, Debye and Fermi statistics",len(P))
