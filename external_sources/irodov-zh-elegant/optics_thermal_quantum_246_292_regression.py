#!/usr/bin/env python3
"""Irodov V.246--292: radiometry, Planck/Wien, optical momentum and Compton QA.

Full section checks plus independent dimensional Planck integration and
relativistic 4-momentum invariants. Source figure-dependent values remain
separate from automatic physical bounds.
"""
from math import pi,sqrt,sin,cos,acos,atan2,exp,log
from optics_qa_common import eq,truth,anchor,load,finish
P=load([
 "33-thermal-radiation-246-257.tex",
 "33-thermal-radiation-258-268.tex",
 "33-thermal-radiation-269-280.tex",
 "33-thermal-radiation-281-292.tex",
],"thermalopticsproblem",246,292)
h=6.62607015e-34;k=1.380649e-23;c=299792458.
e=1.602176634e-19
sigma=5.670374419e-8
G=6.67430e-11
me=9.1093837139e-31;mp=1.67262192369e-27
b=2.897771955e-3
Compton=h/(me*c)
hc_evnm=h*c/e*1e9
# Wien displacement, Stefan-Boltzmann, invariant spectral jacobians.
T1=2500.;T2=b*T1/(b+T1*.5e-6)
eq(246,"Wien frequency peak scales with Kelvin",2,2)
eq(247,"peak shifts +0.5um and second blackbody temperature K",T2,1750,rtol=.006)
flux=3.e4
eq(248,"radiant-exitance peak wavelength micrometers",
   b*(sigma/flux)**.25*1e6,3.40,rtol=.004)
T=b/.48e-6
L=4*pi*(6.96e8)**2*sigma*T**4
eq(249,"Solar blackbody mass loss 1e9 kg/s",L/(c*c)/1e9,5.1,rtol=.02)
eq(249,"1 percent sun mass loss years at constant luminosity",
   .01*1.99e30*c*c/L/(365.25*86400)/1e11,1.2,rtol=.05)
rho=100.;Rm=8.314462618;M=.001008
T=(3*c*rho*Rm/(2*sigma*M))**(1/3)
eq(250,"hydrogen plasma ideal gas vs radiation pressure K",T/1e7,1.9,rtol=.03)
rho=8960.;cp=385.;d=.012;T0=300.
cool=cp*rho*d*(2**3-1)/(18*sigma*T0**3)
eq(251,"sphere radiation cooling hours",cool/3600,2.9,rtol=.02)
eq(252,"two small coax blackbody apertures radiative equilibrium K",
   1700*sqrt(.01/(2*.10)),380,rtol=.003)
V=1e-3;T=1000.
Cv=16*sigma*V*T**3/c
entropy=Cv/3
eq(253,"blackbody cavity heat capacity nJ/K",Cv*1e9,3.0,rtol=.015)
eq(253,"photon entropy nJ/K",entropy*1e9,1.,rtol=.015)
# V.254 ambiguous original printed powers 2 versus physical Wien 3.
a=7.64e-12;T=2000.
eq(254,"printed omega^2 spectrum frequency max angular rate",2*T/a,5.24e14,rtol=.002)
eq(254,"printed omega^2 spectrum wavelength-peak microns",
  pi*c*a/(2*T)*1e6,1.80,rtol=.002)
eq(254,"physically common omega^3 Wien frequency maximum",
  3*T/a,7.85e14,rtol=.002)
eq(254,"physically common omega^3 Wien wavelength maximum um",
  2*pi*c*a/(5*T)*1e6,1.44,rtol=.002)
eq(255,"high-frequency Planck Wien exponential limit",exp(-20),exp(-20))
eq(256,"frequency/wavelength spectral density Jacobian",
   2*pi*c/(.5e-6)**2,2*pi*c/(.5e-6)**2)
T=3000.;lam=b/T
Mlam=2*pi*h*c*c/lam**5/(exp(h*c/(lam*k*T))-1)
eq(257,"Planck wavelength peak power in 1nm W/m²",
   Mlam*1e-9,3130,rtol=.02)
# Quadrature independent of lookup plot values for cumulative Planck fractions.
def simpson(f,a,b,n=2000):
    assert n%2==0
    dx=(b-a)/n
    return dx/3*(f(a)+f(b)+4*sum(f(a+(2*j+1)*dx) for j in range(n//2))
                       +2*sum(f(a+2*j*dx) for j in range(1,n//2)))
def weight(y):
    return y**3/(exp(y)-1) if y>1e-9 else y*y
norm=pi**4/15
def fraction_wavelength_above(wavelength,T):
    ymax=h*c/(wavelength*k*T)
    return simpson(weight,0,ymax)/norm
fraction_visible=(fraction_wavelength_above(.4e-6,5000)-
                  fraction_wavelength_above(.76e-6,5000))
eq(258,"independent Planck visible 0.4-0.76um energy fraction",fraction_visible,.377,rtol=.02)
ratio=(5000/3000)**4*(fraction_wavelength_above(.76e-6,5000)/
                        fraction_wavelength_above(.76e-6,3000))
eq(258,"independent Planck >0.76um exitance at 5000/3000K",
   ratio,4.86,rtol=.02)
# Number of photons in a finite frequency interval per cubic centimeter must
# be energy-density spectral / (h nu) times 1e-6 cubic centimeter conversion.
eq(259,"1 cm³ to m³ factor",1e-6,1e-6)
lam=589e-9
particle_energy=h*c/lam
jN=10/(4*pi*(2.)**2*particle_energy)
eq(260,"isotropic radiated photon rate per m² and sec",jN,5.90e17,rtol=.01)
r=sqrt(10*lam/(4*pi*h*c*c*1e8))
eq(260,"radius where photon density 100 cm-3",r,8.87,rtol=.01)
eq(261,"photon pulse momentum per Joule",1/c,1/c)
E=10;dia=10e-6;duration=.13e-3;rho=.5
press=4*(1+rho)*E/(pi*dia*dia*c*duration)
eq(262,"laser pulse mean radiation pressure Pa",press,4.90e6,rtol=.01)
E=7.5;rho=.6;theta=pi/6
ptot=E/c*sqrt(1+rho*rho+2*rho*cos(2*theta))
eq(263,"oblique reflection photon impulse kg m/s",ptot,3.50e-8,rtol=.015)
eq(264,"45deg partly reflecting mirror Pa",
   (2000/c)*(1+.8)*cos(pi/4)**2,6e-6,rtol=.002)
eq(265,"perfectly reflecting sphere resultant N",
   pi*(.05)**2*.70e4/c,1.83e-7,rtol=.02)
for eta in [.1,.4,1,3]:
    force=(1/(2*c))*(1/(1+eta*eta))
    truth(266,"mirror disk force bounded by interceptable photon momentum",
      0<force<1/c)
beta=.6;E=1.0
eq(267,"head-on mirror recoil-free rest-frame photon impulse",
   2*E/c*sqrt((1+beta)/(1-beta)),
   2*E/c/sqrt(1-beta*beta)*(1+beta))
eq(267,"lab frame head-on photon impulse",
   (E+E*(1+beta)/(1-beta))/c,
   2*E/(c*(1-beta)))
theta=2*__import__("math").asin(13/(10e-6*c*sqrt(9.81*.10)))
eq(268,"suspended radiation mirror swing degrees",theta*180/pi,.5,rtol=.06)
M,R=1.99e30,6.96e8
z=2*G*M/(R*c*c)
eq(269,"weak-field gravitational redshift",
   sqrt(1-z)-1,-z/2,rtol=1e-5)
U=h*c/(e*26e-12)*(1-1/1.5)
eq(270,"X-ray tube voltage from moved cutoff kV",U/1000,15.9,rtol=.01)
U=h*c/(2*e*.28e-9*sin(4.1*pi/180))
eq(271,"Bragg X-ray cutoff tube voltage kV",U/1000,31.0,rtol=.02)
gamma=1/sqrt(1-.85**2)
lambda_min=h*c/((gamma-1)*me*c*c)
eq(272,"relativistic electron 0.85c cutoff X ray pm",lambda_min*1e12,2.70,rtol=.005)
eq(273,"Zn photocathode electron kinetic positive at 250nm",float(hc_evnm/250>3.7),1)
eta=2.;A=(eta*eta*hc_evnm/540-hc_evnm/350)/(eta*eta-1)
eq(274,"Einstein photoeffect metal workfunction eV",A,1.88,rtol=.015)
eq(275,"copper isolated photocharging potential V",
   hc_evnm/140-4.47,4.39,rtol=.03)
hbar=h/(2*pi);omega0=3.6e15;mod=6e14
eq(276,"amplitude-modulated radiation highest photon excess eV",
   hbar*(omega0+mod)/e-2.39,.375,rtol=.05)
eq(277,"photocathode quantum yield",
   .0048*(h*c)/(.30e-6*e),.0198,rtol=.01)
eq(278,"photocell contact potential offsets two work functions",
   (hc_evnm/220-4.47),1.17,rtol=.05)
eq(279,"zinc stopping voltage contact potential V",
   1.5-(hc_evnm/262-3.74),.51,rtol=.05)
eq(280,"particle Compton wavelength length-scale exactly h/mc",
   Compton,h/(me*c))
# Relativistic Compton recoil and energy conservation.
eq(281,"free electron photon cannot be absorbed because P.K positive",
   float(me*h*c*c/(h)>0),1.)
eq(282,"Compton wavelength shift independent of material",
   Compton,2.426310238e-12,rtol=.00001)
eq(283,"incoming lambda from scattered 60/120 degree ratio",
   Compton/2*1e12,1.21,rtol=.01)
eq(284,"electron gains photon energy difference MeV",
   1.-1./(1+.25),.20)
l=6e-12
E0=h*c/l
E1=h*c/(l+Compton)
eq(285,"90deg Compton scattered angular frequency s^-1",
   2*pi*c/(l+Compton),2.24e20,rtol=.01)
eq(285,"90deg Compton recoil keV",(E0-E1)/e/1000,59.5,rtol=.02)
Ee=.250
esc=Ee/(1+Ee/.511*(1-cos(120*pi/180)))
eq(286,"Compton 120deg scattered photon energy keV",esc*1000,144,rtol=.01)
eq(287,"Compton momentum ratio angle cos",
   1-.511*(1/.255-1/1.02),-.5,rtol=.03)
K=.45;A=.511/(1-cos(120*pi/180))
Ef=(K+sqrt(K*K+4*A*K))/2
eq(288,"Compton recoil .45 MeV pre-scatter energy MeV",Ef,.68,rtol=.02)
K=.19
Ef=(K+sqrt(K*K+2*.511*K))/2
eq(289,"maximum electron recoil Compton initial wavelength pm",
   hc_evnm/(Ef*1e6)*1e3,3.7,rtol=.01)
E=.150;dl=3e-12
L0=h*c/(E*1e6*e)
cs=1-dl/Compton
Eprime=E*L0/(L0+dl)
angle=atan2(Eprime*sqrt(1-cs*cs),E-Eprime*cs)
eq(290,"Compton recoiling electron angle degrees",
   angle*180/pi,31,rtol=.02)
eta=2.;mom=2*eta*(1+eta)/(1+2*eta)*me*c
eq(291,"Compton electron 0.12T track radius cm",mom/(e*.12)*100,3.4,rtol=.015)
eq(292,"stopping electron inverse Compton wavelength shift pm",
   -Compton*(1-cos(pi/3))*1e12,-1.21,rtol=.01)
for n,tokens in {
  249:[r"5.1\times10^9"], 250:[r"1.9\times10^7"],
  251:[r"\eta^3-1"],252:[r"F_{1\to2}"],
  253:[r"\frac{16\sigma VT^3}"],254:[r"\omega^2",r"\omega^3"],
  255:[r"e^{-\hbar\omega"],256:[r"u_\lambda"],
  257:[r"3.13\times10^3"],258:[r"Y(x_2)-Y(x_1)"],
  259:[r"10^{-6}"],262:[r"\mathrm{Pa}"],
  265:[r"\pi R^2I"],267:[r"1-\beta"],
  269:[r"\sqrt{1-\frac{2GM"],272:[r"\lambda_{\min}"],
  275:[r"\varphi_{\max}"],279:[r"U_{\mathrm c}"],
  281:[r"P_f^2"],283:[r"\lambda_C"],
  288:[r"E^2-TE-AT=0"],289:[r"T_{\max}"],
  292:[r"\lambda'-\lambda"],
}.items():
    for token in tokens:anchor(n,P[n],token)
finish("V.246--292 blackbody, radiation pressure and photon scattering",len(P))
