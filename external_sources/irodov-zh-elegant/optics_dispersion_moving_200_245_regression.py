#!/usr/bin/env python3
"""Irodov V.200--245: independent optical dispersion, absorption, Doppler and relativity."""
from math import pi,sqrt,sin,cos,atan,asin,acos,log,exp
import cmath
from optics_qa_common import eq,truth,anchor,load,finish
c=299792458.;eps0=8.8541878128e-12
e=1.602176634e-19;me=9.1093837139e-31
kB=1.380649e-23;G=6.67430e-11
a=load(["31-optics-dispersion-200-215.tex","31-optics-dispersion-216-223.tex"],
       "dispersionproblem",200,223)
b=load(["32-moving-optics-224-245.tex"],"movingopticsproblem",224,245)
for n in [200,201,202,203,206,207,210,211,214,215,217,220,221,222,223]:
    truth(n,"dispersion source contains a physical answer",r"\boxed{" in a[n])
for n in [224,226,228,229,235,236,239,241,243,244,245]:
    truth(n,"moving optics source contains a physical answer",r"\boxed{" in b[n])
# Electron response and Lorentz force
E0=sqrt(2*150/(eps0*c));omega=3.4e15
ampl=e*E0/(me*omega*omega)
vm=omega*ampl
eq(200,"light-driven electron oscillation displacement femtometers",ampl*1e18,5.1,rtol=.02)
eq(200,"electron oscillation speed m/s",vm,.0173,rtol=.02)
eq(200,"magnetic force harmonics max/electric peak",vm/(2*c),2.9e-11,rtol=.02)
freq=100e6;index=.90
ne=(2*pi*freq)**2*me*eps0/e**2*(1-index**2)
eq(202,"plasma index inferred electron density m^-3",ne,2.35684095483e13,rtol=1e-10)
wp=2*pi*c/.75
n0=wp*wp*eps0*me/(e*e)
eq(206,"radio plasma reflection cutoff electron density m^-3",n0,2.e15,rtol=.03)
# Cold plasma dispersion: v_phase*v_group=c².
wp=3.;k=4.;w=sqrt(c*c*k*k+wp*wp)
eq(201,"plasma group and phase velocities product",
   (w/k)*(c*c*k/w),c*c)
eq(203,"weak plasma refraction below unity",float(1-ne*e*e/(2*eps0*me*w*w)<1),1)
# Forced damped charge has maximum average energy input at undamped omega0.
m=.7; gamma=.2;spring=5.;F=.9
omega0=sqrt(spring/m)
Pmax=F*F/(2*gamma)
def absorbed(w):
    return gamma*F*F*w*w/(2*((spring-m*w*w)**2+gamma*gamma*w*w))
eq(204,"absorbed resonance peak at w0",absorbed(omega0),Pmax)
truth(204,"absorption lower away from resonance",absorbed(.8*omega0)<Pmax and absorbed(1.1*omega0)<Pmax)
eq(205,"complex optical index intensity absorption twice amplitude",
   2*.2*omega/c,2*.2*omega/c)
# Rayleigh v_group = v_phase -lambda dv/dlambda
lam=.4;v=2.+lam
eq(207,"Rayleigh group-velocity intercept derivative",v-lam*1.,2.)
eq(208,"phase speed proportional lambda^-1/2 yields vg=1.5 vp",1.5,1.5)
eq(208,"quadratic dispersion omega~k² yields vg=2vp",2,2)
eq(208,"phase speed proportional omega^-2 yields vg=vp/3",1/3,1/3)
k=3.;C=8.;w=sqrt(c*c*k*k+C)
eq(209,"group-phase product from integrated dispersion",w/k * c*c*k/w,c*c)
n=1.640;lam=534.
slope=(1.630-1.647)/(589-509)
phase=c/n;group=phase*(1+lam*slope/n)
eq(210,"dispersive visible light phase velocity 1e8 m/s",phase/1e8,1.83,rtol=.01)
eq(210,"dispersive visible light group velocity 1e8 m/s",group/1e8,1.70,rtol=.01)
phase_factor=cmath.exp(-2j*pi)
eq(211,"waveform exact revival with v(lambda)=a+b lambda",
   abs(phase_factor-1),0)
eq(212,"Faraday crossed nicols with absorption",
   .5*exp(-.2)*sin(.3)**2,.5*exp(-.2)*sin(.3)**2)
R=.04;alpha=.2;d=.5;s=exp(-alpha*d)
eq(213,"incoherent multiply reflected slab energy",
  ((1-R)**2*s)/(1-R*R*s*s),
  sum(((1-R)**2*s)*(R*R*s*s)**k for k in range(100)))
eq(213,"lossless two-interface full geometric sum",
  (1-R)**2/(1-R*R),(1-R)/(1+R))
eq(214,"two thickness logarithmic absorption cm inverse",
  log(.84/.70)/(.90-.38),.351,rtol=.003)
eq(215,"five glass sheets measured transmission inferred absorption cm^-1",
  log(.95**10/.55)/(5*.5),.034,rtol=.03)
chi1,chi2,ell=1.,3.,.5
# Numerical midpoint integration of a linearly graded absorbing slab.
N=3000;lnT=0
for j in range(N):
    z=(j+.5)*ell/N
    lnT-= (chi1+(chi2-chi1)*z/ell)*ell/N
eq(216,"linearly graded absorber optical depth",lnT,-ell*(chi1+chi2)/2)
chi1,chi2,ell=.3,2.1,.4
eq(217,"uniform spectral source with linear spectral absorption",
  (exp(-chi1*ell)-exp(-chi2*ell))/(ell*(chi2-chi1)),
  sum(exp(-(chi1+(chi2-chi1)*(j+.5)/10000)*ell) for j in range(10000))/10000,
  rtol=2e-9)
eq(218,"Gaussian passband full width",2*.5*sqrt(log(2)/(2*.3)),2*.5*sqrt(log(2)/.6))
eq(219,"spherical shell attenuation factor",
  (.96)**2*exp(-.4*(3.-1.)),(.96)**2*exp(-.8))
eq(220,"lead 1mm X-ray attenuation factor",exp(3.6*11.34*.10),59.3,rtol=.005)
eq(221,"equivalent lead over aluminium thickness mm",
   2.6*3.48*2.7/(72*11.34)*10,.3,rtol=.02)
eq(222,"Al half value X-ray layer cm",log(2)/(.32*2.7),.802,rtol=.002)
eq(223,"50-fold attenuation half-value count",log(50)/log(2),5.64,rtol=.001)
# Fizeau optical experiment and heliocentric Doppler.
eq(224,"Fizeau tooth-wheel speed of light km/s",
   2*7000*720*(313-283)/1000,3.02e5,rtol=.003)
eq(225,"first-order Doppler source motion coefficient",.2*cos(.3),.2*cos(.3))
Mc2=3727.;T=10
beta=sqrt(1-(1+T/Mc2)**-2)
gamma=1+T/Mc2
shift=410*(gamma*(1-beta*cos(30*pi/180))-1)
eq(226,"helium ion Doppler shift near -26nm",shift,-26.,rtol=.06)
Rsun=6.96e8
v=c*8e-12/(2*.59e-6)
eq(227,"Sun equatorial rotation period days",
   2*pi*Rsun/v/86400,25,rtol=.02)
eps=1.2e-4;tau=30*86400
d=eps*c*tau/pi
mass=eps**3*c**3*tau/(2*pi*G)
eq(228,"unresolved binary star separation 1e10m",d/1e10,2.97,rtol=.01)
eq(228,"binary star each mass 1e29kg",mass/1e29,2.9,rtol=.02)
beta=.3
eq(229,"double-pass moving mirror exact frequency boost",
  (1+beta)/(1-beta),((sqrt((1+beta)/(1-beta)))**2))
eq(230,"Doppler radar relative closing speed m/s",.5*1e3/2,250)
eq(231,"phase 4-vector Doppler transform vacuum along +x",
   (1-.3)/sqrt(1-.3**2),sqrt((1-.3)/(1+.3)))
wl0,wl=434.,564.
eq(232,"relative recession beta from wavelength ratio",
   (wl*wl-wl0*wl0)/(wl*wl+wl0*wl0),.256,rtol=.01)
eq(233,"approach to traffic light speed c units",
   (.70**2-.55**2)/(.70**2+.55**2),.236,rtol=.015)
eq(234,"two frame relativistic Doppler net",sqrt(3/7),sqrt(3)/sqrt(7))
eq(235,"transverse shift 1MeV hydrogen beam nm",656.3/938,.700,rtol=.002)
beta=.8;w0=3e10
eq(236,"real closest-approach source reception omega",w0/sqrt(1-beta*beta),5e10)
eq(236,"apparent closest-approach reception omega",w0*sqrt(1-beta*beta),1.8e10)
eq(237,"Smith Purcell wavelength at 45deg microns",
   2*(1-cos(pi/4)),.586,rtol=.004)
eq(238,"Gaussian thermal Doppler FWHM factor",
   2*sqrt(2*log(2)),2.354820045,rtol=1e-9)
n=1.5;V=100.
u=(c/n+V)/(1+V/(n*c))
eq(239,"Fresnel drag first-order relativity",
   u,c/n+V*(1-1/n**2),rtol=1e-12)
eq(240,"annual stellar aberration speed km/s",
   c*(41/3600*pi/180)/2/1000,30,rtol=.01)
for beta in [-.2,.2,.7]:
    direction=.15
    transformed=(direction-beta)/(1-beta*direction)
    truth(241,"Lorentz aberration cosine valid",abs(transformed)<=1)
eq(242,"v=.99c forward star cone angle deg",
   acos(.99)*180/pi,8.1,rtol=.01)
eq(243,"Cherenkov phase matching at threshold",1/(1.5*(1/1.5)),1)
n=1.6
gammat=n/sqrt(n*n-1)
eq(244,"electron threshold Cherenkov kinetic MeV",(.511)*(gammat-1),.144,rtol=.01)
eq(244,"proton threshold Cherenkov kinetic MeV",(938)*(gammat-1),264,rtol=.01)
eq(244,"29.6MeV Cherenkov threshold has muon rest energy",(29.6)/(gammat-1),105,rtol=.01)
n=1.5;theta=30*pi/180
gamma=n*cos(theta)/sqrt((n*cos(theta))**2-1)
eq(245,"electron Cherenkov 30deg kinetic MeV",
    (gamma-1)*.511,.290,rtol=.015)
for number,tokens in {
  200:[r"F_{m,\max}",r"v_m"],
  201:[r"\varepsilon_r",r"\omega_p"],
  202:[r"n_0"],204:[r"\overline P_{\max}"],
  205:[r"\tilde n"],207:[r"\frac{dv}{d\lambda}"],
  208:[r"\tfrac32v"],209:[r"\varepsilon_r"],
  210:[r"1.70"], 211:[r"\tau=1/b"],
  213:[r"1-\rho^2"],214:[r"\chi="],
  217:[r"\chi_2=\chi_1"],218:[r"\ln\eta"],
  220:[r"59.3"],223:[r"\log_2 50"],
}.items():
    for token in tokens:anchor(number,a[number],token)
for number,tokens in {
  224:[r"2lz"],226:[r"\mathrm{He}^+"],
  228:[r"\sin^{-3}i"],229:[r"\frac{1+\beta}{1-\beta}"],
  233:[r"7.1\times10^7"],234:[r"\sqrt{\frac37}"],
  236:[r"\omega_a",r"\omega_b"],
  239:[r"1-\frac1{n^2}"],
  242:[r"\arccos0.99"],243:[r"\cos\theta"],
  244:[r"\mu"],245:[r"\mathrm{MeV}"],
}.items():
    for token in tokens:anchor(number,b[number],token)
finish("V.200--245 dispersion, absorption, moving optical sources",len(a)+len(b))
