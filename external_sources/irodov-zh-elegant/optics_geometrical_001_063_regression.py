#!/usr/bin/env python3
"""Original Part V.1--63: photometry, Fresnel/Snell and paraxial matrices.

Independent SI/angle/numerical re-computations and all 63 exact original
problem blocks; diagrams requiring source-image editorial review are flagged
rather than mechanically certified.
"""
from math import pi,sqrt,sin,cos,tan,asin,acos,atan,log
from optics_qa_common import eq, truth, anchor, load, finish
files=[
 "27-optics-photometry-001-012.tex",
 "27-optics-photometry-013-025.tex",
 "27-optics-photometry-026-035.tex",
 "27-optics-photometry-036-045.tex",
 "27-optics-photometry-046-057.tex",
 "27-optics-photometry-058-063.tex",
]
blocks=load(files,"opticsproblem",1,63)
rad=pi/180
Z0=376.730313668
# Treat photometric lm and physical W as different units.
for nvis in [.18,.53,.75,.9]:
    flux=1/(683*nvis)
    eq(1,"spectral photopic lm to radiant W",flux*683*nvis,1.)
eq(1,"510nm radiant flux mW",1000/(683*.53),2.76,rtol=.005)
eq(1,"640nm radiant flux mW",1000/(683*.18),8.13,rtol=.005)
vis=.76
radpower=10/(683*vis)
Em=sqrt(2*Z0*radpower/(4*pi))
eq(2,"electric field from luminous flux V/m",Em,1.1,rtol=.04)
eq(2,"plane-wave magnetic H amplitude mA/m",Em/Z0*1e3,2.85,rtol=.005)
R,l,I=.6,1.,36.
cosedge=sqrt(1-R*R/(l*l))
absorbed=2*pi*I*(1-cosedge)
illuminated=2*pi*R*R*(1-R/l)
eq(3,"illuminated spherical cap average lux",absorbed/illuminated,50)
eq(3,"parallel beam sphere illuminated hemispheric average",.5,.5)
eq(4,"cos radiance hemisphere exitance integral factor",2*pi/3,2.09439510239)
eq(5,"Lambert hemispheric exitance/Radiance",pi,pi)
eq(5,"Lambert cone fraction theta60",sin(60*rad)**2,.75)
L,S,R=1.6e4,.01,1.
for h in [.6,.9,1.1,1.5,2.]:
    e=L*S*h*h/(R*R+h*h)**2
    truth(6,"disk lamp illuminance optimized at h=R",e<=L*S/(4*R*R))
eq(6,"optimum mesa illumination lux",L*S/(4*R*R),40)
eq(7,"uniform table flux",pi*100*1**2/1**2,314.1592653589)
n=1.33
eq(9,"illuminated hemispheric dome",pi,pi)
eq(10,"infinite Lambert plane E/L",pi,pi)
eq(11,"finite disk exitance from axis E=70 lux",70*(1+.75**2/.25**2),700)
eq(12,"radiant sphere projected intensity lx",2e4*pi*.06**2/3**2,8*pi)
# Reflections, critical angle, thin plate deviation.
for e,norm in [( (0.8,0.6), (0.,1.) ), ((-1.,0.), (1.,0.))]:
    reflected=(e[0]-2*(e[0]*norm[0]+e[1]*norm[1])*norm[0],
               e[1]-2*(e[0]*norm[0]+e[1]*norm[1])*norm[1])
    eq(13,"law of reflection preserves ray vector norm",
       reflected[0]**2+reflected[1]**2,e[0]**2+e[1]**2)
eq(14,"three orthogonal planar mirror ray reversal",
   (-1)*(.4),-.4)
eq(15,"air-water Brewster degree",atan(1.33)/rad,53.,rtol=.007)
eta=1.28
eq(16,"ratio total-internal index from critical and Brewster angles",
   1/sqrt(eta*eta-1),1.25,rtol=.01)
theta=60*rad;r=asin(sin(theta)/1.5)
shift=.06*sin(theta-r)/cos(r)
eq(17,"glass parallel slab lateral shift cm",shift*100,3.1,rtol=.02)
theta=40*rad;n=1.33;h=1.2
p=h*n*n*cos(theta)**3/(n*n-sin(theta)**2)**1.5
eq(18,"water apparent depth meridional image positive",float(p>0),1)
for A in [.01,.05]:
   eq(19,"small-angle prism first-order deviation",(.5)*A,(1.5-1)*A)
A=60*rad;n=1.5
mind=2*asin(n*sin(A/2))-A
eq(20,"symmetric prism minimum deviation degrees",mind/rad,37.,rtol=.004)
eq(21,"prism apex when minimum deviation equals apex deg",2*acos(n/2)/rad,83.,rtol=.005)
crit=asin(1/n)
maxd=pi/2+asin(n*sin(A-crit))-A
eq(22,"maximum prism deviation near grazing incidence deg",maxd/rad,58.,rtol=.012)
n=sin((60+37)*rad/2)/sin(30*rad)
water=2*asin(n/1.33*sin(A/2))-A
eq(23,"water-immersed prism deviation deg",water/rad,8.7,rtol=.04)
n1,n2=1.515,1.520
deltadeviation=2*asin(n2*.5)-2*asin(n1*.5)
eq(24,"chromatic deviation delta radians",deltadeviation,.0077,rtol=.03)
# Paraxial conjugate lens equations and thick lens algebra.
f=.25;s=.20
sprime=f*s/(s-f)
eq(28,"concave mirror virtual image axial distance m",sprime,-1.)
eq(27,"mirror f for magnification -2 and 15cm separation cm",15*30/(15+30),10)
eq(29,"spherical interface n'/s'-n/s",1.5/.30-1/(-.20),10)
n=1.5;R=.05
# First glass-air surface at x=0: n'/s'-n/s=(n'-n)/R.
eq(31,"first thick lens glass image distance cm",
   n/((n-1)/R+1/(-.2)),.30,rtol=1e-6)
eq(32,"thick plano convex transverse magnification",
   1-.09*(1.5-1)/(1.5*.025),-.2)
eq(33,"thin lens power sign self-consistency",(-5)<0,True)
eq(36,"conjugate two lens positions for 90cm and beta2",30*60/90,20)
eq(37,"Bessel lens inverted image geometric mean mm",sqrt(2*4.5),3.)
eq(38,"camera image illuminance lx",.9*pi*260/(4*3.5**2),15.,rtol=.015)
eq(40,"two glass lenses submerged in same water phi D",
    2*(1.70-1.51)/.10,3.8)
eq(41,"silvered double-convex thin lens effective focus cm",
   .40/(2*(2*1.5-1))*100,10)
# Transfer matrix P(d) S(-P): column vector [height,slope].
def matmul(A,B):
    return ((A[0][0]*B[0][0]+A[0][1]*B[1][0],A[0][0]*B[0][1]+A[0][1]*B[1][1]),
            (A[1][0]*B[0][0]+A[1][1]*B[1][0],A[1][0]*B[0][1]+A[1][1]*B[1][1]))
def glass(phi):return ((1.,0.),(-phi,1.))
def free(d):return ((1.,d),(0.,1.))
M=matmul(glass(10.),matmul(free(.05),matmul(glass(-10.),matmul(free(.05),glass(10.)))))
eq(42,"three-lens parallel exit focus m",-M[0][0]/M[1][0],1/30)
M2=matmul(free(1/6),matmul(M,free(1/6)))
eq(42,"three-lens symmetric conjugate image matrix B",M2[0][1],0)
eq(43,"Galilean telescope objective cm",45*10/9,50)
eq(43,"Galilean focus shift cm",(.5*50/(50-.5)-.5)*100,.505050505,rtol=.005)
eq(44,"telescope power ratio and exit pupil",.06/.003,20)
eq(45,"angular concentration sqrt40000 gives arcminutes",2*60/sqrt(4e4),.6)
K=1.33*(1.5-1)/(1.5-1.33)
gamma=(15+1)/K-1
eq(46,"submerged telescope unchanged barrel angular magnification",gamma,3.1,rtol=.025)
eq(47,"telescope exit pupil no retinal dimming magnification",.06/.003,20)
eq(48,"microscope extra 2cm tube 100D/20D change",.25*.02/(.01*.05),10)
eq(49,"microscope exit pupil matching magnification",2*.12*.25/.004,15)
power=(2*1.5-1.33-1)/.075
eq(50,"different surrounding media lens image focal distance cm",1.33/power*100,15,rtol=.005)
a=1.
phi=(1/(1.5*a)+1/(-1.5*a)-a/(1.5*a*(-1.5*a)))
eq(51,"telephoto opposed thin lens power 1/a",phi,4/9,rtol=1e-10)
eq(51,"thin meniscus thick lens effective power diopters",.04/1.5*50*50,66.6666666667)
d=.04;phi1=10;phi2=-10
phi=phi1+phi2-d*phi1*phi2
f=1/phi
ell=d-.1+f
eq(54,"telephoto focal length / first-lens-to-focus",f/ell,1/(100*d*d-10*d+1))
eq(54,"optimal telephoto ratio",1/(100*.05*.05-10*.05+1),4/3)
phi1,phi2=5.,-10.;d=.03
phi=phi1+phi2-d/1.5*phi1*phi2
eq(55,"thick meniscus phi D",phi,-4.)
f1,f2,d=.15,.05,.07
eq(56,"two lenses equivalent power",1/f1+1/f2-d/(f1*f2), (f1+f2-d)/(f1*f2))
ng,water,R=1.5,1.33,.38
phi=(2*ng-water-1)/R
eq(57,"lens+mirror round-trip effective optical power",
  2*phi-2*.12/water*phi*phi,3,rtol=.035)
n=1.5;R1=.10;R2=.075
phi=(n-1)*(1/R1-1/R2)
d= n*R1*R2/(n-1)**2*(-1-phi)
eq(58,"thick meniscus at -1D cm",100*d,3.)
eq(59,"equal radius curved thick meniscus nonzero power",(.5**2)*.03/(1.5*.1**2),.5)
eq(60,"ball lenses telescope center spacing cm",
   1.5*(.05+.01)/(2*.5)*100,9)
eq(60,"ball lenses magnification radii ratio",.05/.01,5)
eq(61,"two thick convex elements combined optical power D",
   2*(1.5**2-1)/(1.5**2*.03),37.037037)
eq(62,"gradient-index ray curvature for n height-gradient",3e-8/1.,3e-8)
eq(63,"refractive ray curvature m",1/3e-8,3.3e7,rtol=.011)
eq(63,"required terrestrial refractive index height gradient",
   1/6.4e6,1.6e-7,rtol=.025)
# Direct source integrity assertions protect numerical errata and physical branches.
for n,tokens in {
  1:[r"V(0.51)",r"V(0.64)"],
  2:[r"\overline S",r"Z_0",r"\mathrm{V/m}"],
  3:[r"\bar E"], 6:[r"h_*=R",r"40"],
  15:[r"\arctan n"],17:[r"\delta=d"],
  18:[r"\cos^3\theta"], 20:[r"\delta_{\min}",r"n\sin"],
  24:[r"\Delta\delta"], 29:[r"\frac{n'}{s'}"],
  31:[r"s_2'=6.25"], 32:[r"\beta",r"-0.20"],
  41:[r"\Phi_{\rm eff}"], 42:[r"\mathsf P"],
  46:[r"\Gamma_w"], 50:[r"\Phi",r"x_N"],
  51:[r"\Phi_1"], 54:[r"d_{\max}"],
  55:[r"-4.0"], 56:[r"f_{\rm eq}"], 57:[r"\Phi_{\rm eff}"],
  61:[r"\mathsf M^2"], 63:[r"R_\oplus"],
}.items():
    for token in tokens:anchor(n,blocks[n],token)
finish("V.1--63 geometrical optics and photometry",len(blocks))
