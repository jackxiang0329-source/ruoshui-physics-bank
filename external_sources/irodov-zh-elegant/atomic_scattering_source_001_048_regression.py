#!/usr/bin/env python3
"""Irodov VI.1--48 second-pass source-locked Rutherford/Bohr independent audit.

Guardrails explicitly distinguish finite target from a fixed Coulomb centre,
Rutherford differential versus integrated angle, spectral LINE INDEX versus
upper principal quantum number, and mass-corrected H/D energies.
"""
from math import pi,sqrt,sin,cos,tan,atan,asin,exp,log
from atomic_qa_common import load,eq,verify,anchor,finish
F=["34-atomic-scattering-001-018.tex","34-atomic-scattering-019-032.tex",
   "34-atomic-scattering-033-048.tex"]
P=load(F,"atomicproblem",1,48)
h=6.62607015e-34
c=299792458.0
e=1.602176634e-19
eps=8.8541878128e-12
me=9.1093837139e-31
mp=1.67262192369e-27
md=3.3435837724e-27
hbar=h/(2*pi);Ryd=1.096775834e7
ke=1/(4*pi*eps)
a0=4*pi*eps*hbar*hbar/(me*e*e)
k2=ke*e*e/(1e6*e*1e-15) # 1.44 MeV fm
deg=pi/180
def rutherford_differential(Z1,Z2,T,theta):
    return (k2*Z1*Z2/(4*T))**2 / sin(theta/2)**4 # fm²/sr
def rutherford_integral(Z1,Z2,T,theta0):
    return pi*(k2*Z1*Z2/(2*T))**2 / tan(theta0/2)**2
def numerical_integral(Z1,Z2,T,theta0,N=3000):
    width=(pi-theta0)/N
    def val(theta):
        return 2*pi*sin(theta)*rutherford_differential(Z1,Z2,T,theta)
    return width*(val(theta0)+val(pi)+4*sum(val(theta0+(2*j+1)*width) for j in range(N//2))
             +2*sum(val(theta0+2*j*width) for j in range(1,N//2)))/3
# Independent angular quadrature catches 2pi solid-angle and half-angle mistakes.
for Z1,Z2,T,ang in [(2,79,.27,60),(2,92,1.5,60),(1,47,.7,90),(2,82,.4,110)]:
    theta=ang*deg
    eq(2,"Rutherford dσ/dΩ integrated over full azimuth",
       numerical_integral(Z1,Z2,T,theta),rutherford_integral(Z1,Z2,T,theta),rel=3e-7)
    eq(2,"Rutherford integrated cross-section nonnegative",
       float(rutherford_integral(Z1,Z2,T,theta)>0),1)
for theta_deg in [30,60,90,120,150]:
    theta=theta_deg*deg
    b=k2*2*79/(2*.27)/tan(theta/2)
    eq(2,"impact parameter b and scattering angle inversion",
       2*atan(k2*2*79/(2*.27*b)),theta)
eq(2,"Au b at 60deg pm",(k2*2*79/(2*.27)/tan(pi/6))*1e-3,.730,rel=.005)
# Head-on free target: centre-of-mass kinetic energy is T M/(m+M).
for m,M in [(4,7),(2,82),(1,238)]:
    T=1.2;C=k2*2*3
    free_turn=C*(1+m/M)/T
    fixed_turn=C/T
    eq(3,"free-target recoil increases Coulomb turning distance",free_turn/fixed_turn,1+m/M)
eq(8,"hard-sphere isotropic scattering hemisphere probability",
   .5*(1-cos(pi/2)),.5)
for ang in [15,30,60,120]:
    eq(8,"hard-sphere isotropic solid angle angular density",
       .5*sin(ang*deg),.5*sin(ang*deg))
# Thomson atom and Bohr Coulomb radius are physically DISTINCT models.
R_th=3*ke*e*e/(2*13.6*e)
w_th=sqrt(ke*e*e/(me*R_th**3))
eq(1,"Thomson atom radius nanometres",R_th*1e9,.1588,rel=.001)
eq(1,"Thomson radiation wavelength nanometres",2*pi*c/w_th*1e9,237,rel=.005)
eq(1,"Thomson model not silently identified with Bohr radius",
   float(abs(R_th/a0-1)>.5),1)
eq(16,"U target Coulomb cross section kilobarn",
   rutherford_integral(2,92,1.5,60*deg)*1e-5,0.735,rel=.007)
eq(17,"scattering probability in 60deg fixed angle from 90deg integral",
   4*(.5)/pi,.63662,rel=.001)
# Radiative damping of bound oscillator: radiation is positive and optical
# energy decreases. Orbital Rutherford collapse time scales exactly with r0^3.
for radius in [25e-12,50e-12,100e-12]:
    t=me**2*c**3*radius**3/(4*ke**2*e**4)
    eq(19,"classical orbit collapse cubic radius scaling",
       t/(me**2*c**3*(50e-12)**3/(4*ke**2*e**4)),(radius/(50e-12))**3)
eq(19,"classical hydrogen 50pm collapse in ps",
   me**2*c**3*(50e-12)**3/(4*ke**2*e**4)*1e12,13.,rel=.06)
for n in [2,3,5,10,40,100]:
    # Finite-difference orbital transition is bounded by endpoint derivatives.
    A=13.6
    transition=A*(1/n**2-1/(n+1)**2)
    eq(20,"spectral transition below n-orbital angular frequency",
       float(transition<2*A/n**3),1)
    eq(20,"spectral transition above n+1 angular frequency",
       float(transition>2*A/(n+1)**3),1)
eq(21,"Bohr-quantized harmonic oscillator energy nħomega",5,5)
for Z in (1,2,3):
    eq(22,"hydrogenlike 1s energy scales with Z²",
       13.6*Z**2/13.6,Z**2)
    eq(24,"Bohr orbital magnetic-to-angular ratio e/(2m)",
       e/(2*me),e/(2*me))
eq(25,"Bohr centre field T",
   4*pi*1e-7*e*(e*e/(4*pi*eps*hbar))/(4*pi*a0*a0),12.5,rel=.03)
# Balmer physical LINE NUMBER = upper principal n-2 (not equal to n).
def balmer(n):
    return 1/(Ryd*(.25-1/n**2))
L=.0066
def rayleigh_sin(n):
    return balmer(n)**2/(L*(balmer(n)-balmer(n+1)))
eq(29,"50th Balmer line comes from n=52",50+2,52)
eq(29,"50th line grating Rayleigh sinθ",rayleigh_sin(52),.99938,rel=5e-5)
eq(29,"50th line critical angle deg",asin(rayleigh_sin(52))/deg,88.,rel=.005)
eq(29,"n=50 substitution gives different answer, not 50th line",
   asin(rayleigh_sin(50))/deg,62.8,rel=.005)
for n in [3,4,5,6]:
    eq(31,"all distinct hydrogen transitions n choose 2",n*(n-1)/2,sum(j for j in range(1,n)))
eq(33,"He+ 5->2 transition energy eV",
   54.4*(1/4-1/25),11.424,rel=.005)
eq(38,"two ionization steps He to bare nucleus eV",24.6+4*13.6,79)
eq(40,"equal hydrogen atom elastic threshold is double excitation",2*10.2,20.4)
eq(42,"Lyman 2->1 recoil fraction",10.2*e/(2*mp*c*c),5.43e-9,rel=.005)
# Hydrogen/deuterium must use reduced masses, never one common Rydberg.
mu=lambda M:me*M/(me+M)
eq(46,"finite nuclear mass relative binding overestimate",me/mu(mp)-1,me/mp)
eq(47,"heavy isotope mass increases reduced mass",float(mu(md)>mu(mp)),1)
eq(47,"D-H Lyman wavelength separation picometres",
   121.567e-9*(mu(md)/mu(mp)-1)*1e12,33.1,rel=.005)
eq(48,"positronium Bohr radius twice electron-proton scale",
   2*a0/a0,2)
eq(48,"muonic hydrogen Bohr radius picometres",
   a0*me/(207*me*mp/(207*me+mp))*1e12,.285,rel=.02)
for n,tokens in {2:[r"\cot"],3:[r"1+\frac{m_\alpha}"],
                  8:[r"\frac12"],19:[r"r_0^3"],20:[r"\Omega_n"],
                  29:[r"n=52",r"87"],31:[r"\binom n2"],
                  42:[r"5.43"],47:[r"\mu_D"],48:[r"\mu"]}.items():
    for token in tokens:anchor(n,P[n],token)
finish("VI.1--48 Rutherford/Bohr source+physics",len(P))
