#!/usr/bin/env python3
"""Irodov Part V.64-96 independent optical interference physics/limiting checks."""
from math import pi,sqrt,sin,cos,asin,acos,atan,log,hypot
import cmath
from optics_qa_common import eq, truth, anchor, load, finish
files=[
 "28-optics-interference-064-075.tex",
 "28-optics-interference-076-086.tex",
 "28-optics-interference-087-096.tex",
]
blocks=load(files,"interferenceproblem",64,96)
rad=pi/180
# Mutual incoherence vs phase coherence and complex polarization.
eq(64,"incoherent phase average cos",sum(cos(2*pi*j/10000) for j in range(10000))/10000,0,atol=1e-12)
eq(64,"orthogonal Jones modes have no interference",0,0)
phasor=1-2j+1.5*cmath.exp(1j*pi/3)
eq(65,"sum of three sinusoidal Jones phasors A/a",abs(phasor),1.9,rtol=.03)
for N,phase in [(2,.3),(3,.6),(8,.7),(10,1.4)]:
    lhs=abs(sum(cmath.exp(1j*j*phase) for j in range(N)))
    rhs=abs(sin(N*phase/2)/sin(phase/2))
    eq(66,"N coherent-source Dirichlet intensity",lhs,rhs)
eq(66,"all phases equal N amplitude",10.,10.)
phi=pi/2; dlam=.25
eq(67,"symmetric directions adjacent phase condition",
   (2*pi*dlam+phi)-( -2*pi*dlam+phi),pi)
eq(68,"scanning phased array position inverse sin",sin(pi/6),.5)
dx=.25e-3;dh=.6e-3;L=1.;eta=1.5
wavelength=2*dx*dh/(L*(eta-1))
eq(69,"Lloyd mirror source displacement inferred wavelength um",wavelength*1e6,.6)
eq(70,"small-angle double-plane interference pitch",.6e-6/.002,.0003)
eq(72,"Fresnel double mirror wavelength um",
  2*(2/60*rad)*.55e-3*1e6,.64,rtol=.01)
eq(73,"slit pair spatial coherence width microns",
  (.60e-6)*(.25**2)/(2*.001*.50)*1e6,37.5,rtol=.03)
n=1.5;theta=20/60*rad
eq(74,"biprism slit separation mm",
  2*.25*(n-1)*theta*1000,1.45444,rtol=.003)
eq(75,"weak-index-difference biprism pitch mm",
  .70e-6/(2*.02*5*rad)*1000,.2005,rtol=.005)
eq(76,"glass strip Young fringe displacement mm",
  (1.5-1)*10e-6/2.5e-3*1000,2.)
eq(77,"interferometer gas index variation",1.000277+17*589e-9/.1,1.00037713)
for n1,n2 in [(1,1.5),(1.5,1.),(1.33,1.5)]:
    r=(n1-n2)/(n1+n2)
    t=2*n1/(n1+n2)
    truth(78,"normal Fresnel transmission field coefficient positive",t>0)
    truth(78,"reflection phase changes only crossing into higher n", (r<0)==(n2>n1))
angle=52*rad
d=.6e-6/(4*sqrt(1.33**2-sin(angle)**2))
eq(79,"thin film bright yellow minimum thickness um",d*1e6,.14,rtol=.07)
d=2.5*.64e-6/(2*sqrt(1.33**2-sin(30*rad)**2))
eq(80,"two-color film first physically admissible thickness um",
  d*1e6,.65,rtol=.03)
eq(80,"yellow constructive reflected path order",2*d*sqrt(1.33**2-.25)/.64e-6,2.5)
eq(80,"blue destructive reflected path order",2*d*sqrt(1.33**2-.25)/.4e-6,4.)
eq(81,"quarter-wave coating thickness at n=1.5 and 600nm nm",
  600/(4*sqrt(1.5)),122.474487139,rtol=1e-9)
d=.6e-6*sqrt(1.5**2-sin(45*rad)**2)/(sin(90*rad)*3*rad)
eq(82,"angular equal-inclination fringe film thickness microns",
   d*1e6,15.,rtol=.04)
# IMPORTANT V.83: reflected ring projected geometrical radius is r=2 ell theta.
ell=1.3;film=.00007;n=1.5
ri,rk=.003,.009
lam=film*abs(ri**2-rk**2)/(4*n*ell**2*3)
eq(83,"equal-inclination returned-ray angle factor 2",
  (ri/(2*ell))**2-ri**2/(4*ell**2),0)
eq(83,"two dark-ring interference phase difference",
  film/n*((rk/(2*ell))**2-(ri/(2*ell))**2),3*lam)
eq(84,"glass wedge fringe on screen normal to reflected ray",
  cos(40*rad),cos(40*rad))
eq(85,"interference temporal coherence spectral width approx",
   .21/15,.014)
eq(86,"Newton ring adjacent bright/dark half period",
  .6e-6*.4/(4*.003),2.e-5)
R=.4;r=.0025;dh=5e-6
eq(87,"raised lens same order Newton ring radius mm",
  sqrt(r*r-2*R*dh)*1000,1.5)
eq(88,"flattened circular apex 6th bright ring mm",
  sqrt(.003**2+5.5*655e-9*1.5)*1000,3.8,rtol=.02)
eq(89,"difference in Newton dark ring squares wavelength um",
   ((.0015)**2-(.001)**2)/(4*.125*5)*1e6,.5)
eq(90,"two plano convex Newton rings aggregate lens power D",
   2*(1.5-1)*(2*5-1)*.6e-6/.0015**2,2.4)
lam=.61e-6;ng=1.5;power=.5
r10=sqrt(2*10*lam*(ng-1)/power)
eq(91,"combined glass lens Newton radius mm",r10*1000,3.5,rtol=.01)
eq(91,"index increasing to water reduces ring radius",
   float(r10/sqrt(1.33)<r10),1.)
r=sqrt(11*.5e-6*1. /(2*1.63))
eq(92,"three indices same-sign reflection fifth dark ring mm",
  r*1000,1.3,rtol=.03)
wave1,wave2=576.97,579.03
eq(93,"mercury doublet first visibility loss order",
   ((wave1+wave2)/2)/(2*(wave2-wave1)),140,rtol=.005)
eq(94,"sodium doublet Michelson mirror best-fringe recurrence mm",
   589.*589.6/(2*(589.6-589.))*1e-6,.2894,rtol=.01)
eq(95,"Fabry-Perot neighboring angular max spacings",
   (2*.025*1e-2)**0,1.)
eq(96,"Fabry-Perot highest interference order",
   2*.025/.5e-6,100000)
eq(96,"Fabry-Perot free spectral wavelength range pm",
   (.5e-6)**2/(2*.025)*1e12,5.)
for n,anchors in {
  65:[r"\widetilde A",r"3\sqrt3"],
  66:[r"\sin(N\varphi/2)"],
  69:[r"\Delta h",r"\eta-1"],
  72:[r"\lambda=2\alpha"],
  73:[r"\delta_{\max}"],
  75:[r"n-n'"], 76:[r"\delta x"], 77:[r"n'="],
  78:[r"n_1-n_2"], 79:[r"(2k+1)"],
  80:[r"d_{\min}"],81:[r"\sqrt n"],
  83:[r"r\simeq2\ell\theta",r"4n\ell^2"],
  86:[r"\Delta r"], 87:[r"r'=\sqrt"],
  90:[r"\Phi"], 93:[r"m_{\min}"],
  94:[r"\delta h"], 96:[r"\Delta\lambda"],
}.items():
    for token in anchors:anchor(n,blocks[n],token)
finish("V.64--96 interference",len(blocks))
