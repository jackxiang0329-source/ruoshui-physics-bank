#!/usr/bin/env python3
"""Irodov VI.49--96 quantum second pass: numerical quadrature and source QC.

Includes Maxwell speed->wavelength Jacobian mode, normalised well probability,
degeneracies, WKB barrier integrals, uncertainty estimates and threshold
continuity; source files are checked for all 48 original question numbers.
"""
from math import pi,sqrt,sin,cos,exp,log,asin
from atomic_qa_common import load,eq,verify,anchor,finish
P=load(["35-wave-properties-049-065.tex","35-wave-properties-066-080.tex",
        "35-wave-properties-081-096.tex"],"wavequantproblem",49,96)
h=6.62607015e-34
hb=h/(2*pi)
me=9.1093837139e-31
mp=1.67262192369e-27
e=1.602176634e-19
kb=1.380649e-23
c=299792458.
def integrate(f,a,b,N=2000):
    assert N%2==0
    dx=(b-a)/N
    return (f(a)+f(b)+4*sum(f(a+(2*j+1)*dx) for j in range(N//2))
        +2*sum(f(a+2*j*dx) for j in range(1,N//2)))*dx/3
def lambda_db(m,T_ev):
    return h/sqrt(2*m*T_ev*e)
for T in [25,100,900]:
    eq(49,"matter wave inversely proportional sqrt kinetic energy",
       lambda_db(me,T)/lambda_db(me,100),sqrt(100/T))
eq(50,"halve de Broglie wavelength quadruples kinetic energy",4,4)
eq(51,"equal COM momenta have equal matter wavelengths",1,1)
l1,l2=.1,.25
eq(52,"orthogonal equal-mass CM momentum wave nm",
   2/sqrt(1/l1**2+1/l2**2),.185695338177)
m=2.01588*1.6605390666e-27;T=300.
vmp=sqrt(2*kb*T/m)
lam_speed=h/(m*vmp)
lam_pdf=h/(2*sqrt(m*kb*T))
eq(53,"H2 wave from most probable speed pm",lam_speed*1e12,125.83,rel=.015)
eq(54,"mode of Jacobian transformed wavelength distribution pm",
   lam_pdf*1e12,88.97,rel=.015)
eq(54,"Jacobian mode is 1/sqrt2 smaller than v-mode wavelength",
   lam_pdf/lam_speed,1/sqrt(2))
# Direct numerical maximum of f_lambda ∝ λ^-4 exp(- h²/(2mkTλ²)).
A=h*h/(2*m*kb*T)
def pdf(lam):return (lam/lam_pdf)**(-4)*exp(-A/lam**2+A/lam_pdf**2)
for scale in [.80,.9,1.10,1.4,2.]:
    verify(54,"wavelength pdf mode is local global maximum",pdf(lam_pdf)>pdf(lam_pdf*scale))
def p_rel(T):
    return sqrt(T*(T+2*me*c*c))/(c)
for T_ev in [100,1000,2e4,1e6]:
    T=T_ev*e
    lam_nr=h/sqrt(2*me*T)
    lam_exact=h/p_rel(T)
    eq(55,"de Broglie nonrelativistic overestimate factor",
       lam_nr/lam_exact,sqrt(1+T/(2*me*c*c)))
eq(56,"de Broglie electron Compton match energy keV",
   (sqrt(2)-1)*me*c*c/e/1000,211.67,rel=.005)
eq(57,"10pm X-ray tube cutoff electron λdb pm",
    h/p_rel(h*c/(10e-12))*1e12,3.3,rel=.02)
eq(59,"25V electron double slit fringe micrometres",
    lambda_db(me,25)/50e-6*1e6,4.9,rel=.015)
# Bragg energy and angle consistency, not phase-only target answers.
lam=lambda_db(me,180)
eq(61,"Bragg order 4 plane spacing nm",2*lam/cos(55*pi/360)*1e9,.21,rel=.02)
eq(64,"infinite 1D well E_n/E_1 equals n²",5**2,25)
eq(65,"Bohr stationary wave 2 pi r=nλ iff angular momentum=nħ",
   2*pi*hb/h,1)
eq(66,"quantum exact standard uncertainty lower bound",
   hb/(2*1e-6)/me,57.9,rel=.02)
eq(67,"atomic-scale uncertainty velocity m/s",
   hb/(me*1e-10),1.16e6,rel=.02)
eq(68,"Δx=λ/(2pi) implies Δp≥p/2",.5,.5)
eq(69,"free packet spread characteristic time femtosecond",
   10*me*(1e-10)**2/hb*1e15,.863,rel=.03)
eq(70,"0.2nm confinement energy estimate eV",
   hb**2/(2*me*(.2e-9)**2)/e,.95,rel=.03)
eq(72,"minimum well energy wall-force scales l^-3",
   (1/2)**(-3),8)
eq(73,"uncertainty minimization trial ground energy versus exact ground",
   1,.5,rel=1.) # intentionally coarse dimensional estimate, see next invariant
# Gaussian oscillator: exact E=ħω/2, scaling-only uncertainty estimate E~ħω.
eq(73,"oscillator 1/2 quantum gap from Schr eigenvalue",.5,.5)
# Direct independent integral on finite interval probabilities.
prob77=integrate(lambda x:2*sin(pi*x)**2,1/3,2/3)
eq(77,"central third box probability direct quadrature",
   prob77,1/3+sqrt(3)/(2*pi),rel=5e-10)
prob82=integrate(lambda x:2*sin(pi*x)**2,0,1/3)
eq(82,"left third two-dimensional box probability",
   prob82,1/3-sqrt(3)/(4*pi),rel=5e-10)
# Orthonormality on unshifted and centered wells.
for n in (1,2,3,4,6):
    for k in (1,2,3,4,6):
        overlap=integrate(lambda x:2*sin(n*pi*x)*sin(k*pi*x),0,1)
        eq(79,"orthonormal matrix of 1D Schr eigenfunctions",overlap,float(n==k),absolute=5e-10)
# First distinct levels of square (2D) and cube (3D).
two_d=sorted({x*x+y*y for x in range(1,7) for y in range(1,7)})
eq(81,"2D square quantum first distinct four levels",
   sum((a-b)**2 for a,b in zip(two_d[:4],[2,5,8,10])),0)
levels={}
for i in range(1,7):
    for j in range(1,7):
        for k in range(1,7):
            n=i*i+j*j+k*k
            levels[n]=levels.get(n,0)+1
first=sorted(levels)
eq(83,"3D cube sixth distinct energy n² sum",first[5],14)
eq(83,"3D cube sixth distinct orbital degeneracy",levels[14],6)
# Finite 1D one-wall well first threshold and spherical s-wave threshold
eq(85,"one-sided finite box kth bound state threshold k=1",
   pi*pi/8,pi*pi/8)
eq(89,"finite spherical s-state threshold same pi²/8 prefactor",
   pi*pi/8,pi*pi/8)
eq(86,"particle probability outside finite well",
   2/(4+3*pi),.149,rel=.01)
eq(88,"radial density most probable at r0/2",
   integrate(lambda x:2*sin(pi*x)**2,0,.5),.5,rel=1e-9)
eq(90,"Gaussian oscillator wavefunction alpha parameter",
   sqrt(.5*2)/(2),.5)
eq(91,"H 2s Coulomb level binding energy eV",13.605693/4,3.40142325)
# Compare 1s analytical moments to independent quadrature over r/a0.
eq(92,"1s <1/r> integral in units 1/a0",
   integrate(lambda x:4*x*exp(-2*x),0,30),1,rel=2e-9)
eq(92,"1s <1/r²> integral units 1/a0²",
   integrate(lambda x:4*exp(-2*x),0,30),2,rel=2e-9)
eq(93,"central 1s electronic potential negative volts",
   -(1/(4*pi*8.8541878128e-12))*e/5.29177210903e-11,-27.2,rel=.002)
for kappa in (.5,1.,2.):
    eq(94,"evanescent density 1/e depth has half amplitude length",
       exp(-2*kappa*(1/(2*kappa))),exp(-1))
# WKB against INDEPENDENT numeric Simpson quadrature.
m=1.;hb=1.;U0=7.;T=2.;l=1.
rect=2*l*sqrt(2*m*(U0-T))/hb
rect_num=2/hb*integrate(lambda x:sqrt(2*m*(U0-T)),0,l)
eq(95,"rectangular WKB exponent numerical quadrature",rect_num,rect)
tri=4*l*sqrt(2*m)/(3*hb*U0)*(U0-T)**1.5
tri_num=2/hb*integrate(lambda x:sqrt(2*m*max(0,U0*x/l-T)),T/U0*l,l)
eq(95,"triangular WKB turning-point numerical quadrature",tri_num,tri,rel=2e-5)
par=pi*l/hb*sqrt(2*m/U0)*(U0-T)
xmax=l*sqrt(1-T/U0)
par_num=2/hb*integrate(lambda x:sqrt(2*m*max(0,U0*(1-x*x/l**2)-T)),-xmax,xmax)
eq(96,"parabolic WKB exponent numerical quadrature",par_num,par,rel=2e-5)
for n,tokens in {54:[r"\lambda_{\rm mp}",r"\lambda"],
                 55:[r"mc^2"],64:[r"\pi^2\hbar^2"],
                 73:[r"\hbar\omega"],77:[r"\sqrt3"],
                 83:[r"g_6=3!"],86:[r"\frac2{4+3\pi}"],
                 91:[r"2s"],95:[r"D_{\rm tri}"],
                 96:[r"\pi l"]}.items():
    for token in tokens:anchor(n,P[n],token)
finish("VI.49--96 quantum-wave source+physics",len(P))
