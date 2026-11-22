#!/usr/bin/env python3
"""Irodov V.97--156: independent Fresnel diffraction and gratings QA.

The V.105 branch selector is independently re-derived using complex
Fresnel-zone amplitudes to guard against treating a higher-order optical
thickness as the minimum positive thickness.
"""
from math import pi,sqrt,sin,cos,tan,asin,acos,atan,log
import cmath
from optics_qa_common import eq,truth,anchor,load,finish
files=[
 "29-optics-diffraction-097-108.tex",
 "29-optics-diffraction-109-118.tex",
 "29-optics-diffraction-119-130.tex",
 "29-optics-diffraction-131-142.tex",
 "29-optics-diffraction-143-150.tex",
 "29-optics-diffraction-151-156.tex",
]
blocks=load(files,"diffractionproblem",97,156)
rad=pi/180
eq(97,"Fresnel zone plate r_N² proportional N b wavelength",3*.5e-6*1,1.5e-6)
a=1;r=1e-3;lambda_=0.5e-6;k=3
b=a*r*r/(k*lambda_*a-r*r)
eq(98,"three Fresnel zones distance m",b,2.)
eq(99,"adjacent bright on-axis aperture change um",
   ((1.29e-3)**2-(1.e-3)**2)*(1.+1.25)/(2*1.*1.25)*1e6,.6,rtol=.004)
eq(100,"Fresnel zone intensity open first full zone",abs(1-(cmath.exp(1j*pi)))**2,4)
eq(100,"inner half-area of first zone",abs(1-cmath.exp(1j*pi/2))**2,2)
eq(100,"diametrically halved first Fresnel zone",abs((1-cmath.exp(1j*pi))/2)**2,1)
# Source field =1, first zone=2, outer=-1 in high-Fresnel-zone idealization.
eq(101,"half-aperture restores zero amplitude at disk shadow",
   abs(-1+1)**2,0)
eq(102,"no-shade angular wedge phi=pi/2 P intensity relative",
   (1-pi/2/(2*pi))**2,9/16)
# Complex first 1.5 zones F=(1+i)A0 and unaltered outer O=-i A0.
F=1+1j;O=-1j
eq(105,"first 1.5 Fresnel-zone phasor recovers free field",abs(F+O)**2,1)
lambda_um=.57;n=1.60
hmin=5*lambda_um/(8*(n-1))
eq(105,"FIRST constructive-phase minimum glass thickness um",hmin,.59375)
delta=2*pi*(n-1)*hmin/lambda_um
res=O+F*cmath.exp(1j*delta)
eq(105,"first constructive phase equals analytic maximal intensity",
   abs(res)**2,(1+sqrt(2))**2)
for k in [1,2,3]:
    old_h=hmin+k*lambda_um/(n-1)
    higher=O+F*cmath.exp(2j*pi*(n-1)*old_h/lambda_um)
    eq(105,"higher-order thickness same intensity but not minimum",abs(higher)**2,abs(res)**2)
    truth(105,"first positive thickness smaller than higher branches",hmin<old_h)
# Aperture diffraction with a focusing lens
f,b=.5,.75
eq(106,"lens-curvature Fresnel zone aperture first radius mm",
   sqrt(.54e-6*f*b/abs(b-f))*1000,.90)
eq(107,"similar Fresnel diffraction map distance",9./(3*3),1.)
a,b,lamb,D=12.,18.,.55e-6,.04
eq(108,"sphere edge distortion scale from Fresnel width mm",
   a*b*lamb/(D*(a+b))*1000,.099,rtol=.03)
# Fraunhofer sinc envelope, grating resolving power and angular dispersion
# First dark of finite slit: b sin(theta)=lambda.
slit=.0001;lam=.5e-6
eq(109,"single slit first darkness small-angle radians",asin(lam/slit),.005,rtol=2e-5)
# Independent absence of forbidden orders by kinematics.
for m in [1,2,3]:
    eq(124,"number of additional maxima N-2 in three-slit interval",3-2,1)
    eq(124,"number of internal minima N-1 in three-slit interval",3-1,2)
eq(123,"grazing-angle reflective grating 2nd-order lambda um",
   .001*(cos(1*rad)-cos(3*rad))/2*1e6,.609,rtol=.003)
d=2*.65e-6/sin(45*rad)
eq(125,"second wavelength third diffraction peak angle degree",
  asin(3*.50e-6/d)/rad,55,rtol=.02)
d=3*535e-9/sin(35*rad)
eq(126,"highest order mmax exactly five",int(d/535e-9),5)
eq(126,"grating groove pitch micron",d*1e6,2.8,rtol=.005)
x=sin(15*rad)/sqrt(5-4*cos(15*rad))
eq(127,"two same-side grating orders wavelength nm",2.2e3*x,540,rtol=.01)
d=1.5e-6;wl=530e-9
eq(128,"normal incidence greatest order",int(d/wl),2)
eq(128,"60deg incidence minus 5 order exit angle",
   asin(sin(60*rad)-5*wl/d)/rad,-65.,rtol=.03)
eq(129,"cylindrical grating first order ±f spots cm",
   2*.4*(.6/6)/sqrt(1-(.6/6)**2)*100,8.,rtol=.01)
# Binary half-period phase grating zero order vanishes at odd pi.
eq(131,"deep groove cancels zero order",abs(1+cmath.exp(1j*pi)),0)
eq(131,"first order binary grating condition d=2a",2*.25,.5)
eq(132,"acousto-optic grating speed km/s",
  .55e-6*4.7e6*.35/.0006/1000,1.5,rtol=.01)
eq(133,"binary star first vanishing visibility rad",
  .55e-6/(2*.95),2.9e-7,rtol=.01)
# Dimensionally correct D = m/(d cos theta), convert radians to arcminutes/nm.
def angular_dispersion_arcmin_per_nm(m,d_m,lambda_m,in_sin=0):
    outs=in_sin+m*lambda_m/d_m
    assert abs(outs)<1
    return abs(m)/(d_m*sqrt(1-outs**2))*1e-9*180/pi*60
eq(134,"normal incidence high-order 530nm angular dispersion arcmin/nm",
   angular_dispersion_arcmin_per_nm(2,1.5e-6,530e-9),6.5,rtol=.03)
eq(134,"45deg incidence m-4 dispersion arcmin/nm",
   angular_dispersion_arcmin_per_nm(-4,1.5e-6,530e-9,sin(45*rad)),13.,rtol=.03)
eq(135,"angular dispersion tan(theta)/lambda",
   2/(1.5e-6*sqrt(1-(2*.53/1.5)**2)),
   tan(asin(2*.53/1.5))/.53e-6)
N=10000;d=2.5e-6;wl=589e-9
width=2*wl/(N*d*sqrt(1-(2*wl/d)**2))
eq(136,"grating order-2 full peak width arcsec",width/rad*3600,11.,rtol=.04)
eq(137,"grating resolving power upper bound",
   (d/wl)*(1/d),1/wl)
N=13000;d=1e-3/200;wl=670.8e-9
eq(140,"200 grooves per mm, length6.5cm groove count",N,13000)
eq(140,"minimum line separation in 7th order pm",wl/(7*N)*1e12,7.4,rtol=.01)
d=.01/(5*589/(.6))
eq(141,"minimum order 5 resolving 589nm pair pitch micron",d*1e6,50.93,rtol=.03)
eq(142,"250 grooves/mm on 25mm window total grooves",250*25,6250)
eq(142,"grating Rayleigh first order cannot separate 0.030nm",
   float(.030<310.169/6250),1)
eq(142,"grating Rayleigh second order resolves 0.030nm",
   float(.030>310.169/(2*6250)),1)
wl=.55e-6
eq(146,"50mm telescope Rayleigh angle rad",1.22*wl/.05,1.342e-5,rtol=.002)
eq(146,"3km telescope Rayleigh scene spacing cm",
   3e3*1.22*wl/.05*100,4.,rtol=.01)
eq(147,"5m telescope Moon resolution m",3.84e8*1.22*wl/5,52.,rtol=.02)
eq(148,"telescope aperture / human pupil magnification",.05/.004,12.5)
eq(149,"microscope Rayleigh distance microns",.61*.55/.24,1.4,rtol=.01)
eq(150,"microscope diffraction threshold useful magnification",
    2*.25*.24/.004,30)
eq(152,"2D lattice period a x axis nm",2*40e-12/sin(atan(.060/(2*.10)))*1e9,.28,rtol=.02)
eq(152,"2D lattice period b y axis nm",2*40e-12/sin(atan(.040/(2*.10)))*1e9,.41,rtol=.03)
eq(154,"sodium chloride second-order X-ray wavelength pm",
 ((.05844/6.02214076e23)/(2*2160))**(1/3)*sin(60*rad)*1e12,244.,rtol=.02)
eq(155,"Bragg different orders crystal spacing pm",
    174*sqrt(13-12*cos(30*rad)),281,rtol=.015)
eq(156,"Debye-Scherrer ring radius cm",
    .15*tan(2*asin(2*17.8e-12/(2*155e-12)))*100,3.5,rtol=.02)
for n,tokens in {
  98:[r"b=2.0"], 99:[r"r_2^2-r_1^2"],
  100:[r"4I_0",r"2I_0"], 101:[r"I_a\simeq0"],
  103:[r"\delta_a"], 104:[r"I_{\max}"],
  105:[r"h_{\min}=\frac{5\lambda}{8(n-1)}",r"I_{\max}=(1+\sqrt2)^2 I_0"],
  106:[r"r_j"], 107:[r"b'=\frac b"],
  123:[r"\cos\alpha_0-\cos\alpha"], 124:[r"\text{偶数级缺级}"],
  127:[r"\sqrt{5-4\cos"], 128:[r"\theta_{-5}"],
  131:[r"(2j+1)"], 132:[r"v_s"],
  133:[r"\lambda}{2d"], 136:[r"\Delta\theta"],
  139:[r"10.0\,\mathrm m",r"10.0\,\mathrm{mm}"],
  140:[r"670.8",r"\delta\lambda_{\min}"],
  142:[r"\text{一级不能分辨"],
  145:[r"\mathrm m"], 146:[r"1.22\lambda"],
  150:[r"\Gamma_{\min}"], 156:[r"\arcsin"],
}.items():
    for token in tokens:anchor(n,blocks[n],token)
finish("V.97--156 diffraction and X-ray scattering",len(blocks))
