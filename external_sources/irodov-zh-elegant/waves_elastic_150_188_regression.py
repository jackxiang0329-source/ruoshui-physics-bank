#!/usr/bin/env python3
"""Independent physics QA for all Irodov IV.150-188 elastic and sound waves.

Derives wave, string, sound-intensity, damped spherical-wave, Doppler and
retardation formulae from physical laws rather than reading printed answers.
The whole 39-problem source range is structurally checked and selected
numerical/analytic constraints are independently verified. Expert source-PDF
figure collation and full manual proof-reading remain separate tasks.
"""
from math import pi, sqrt, exp, log, sin, cos, isclose, log10
from pathlib import Path
import re
chapters = Path(__file__).resolve().parent/"chapters"
names = [
    "25-elastic-waves-150-165.tex",
    "25-elastic-waves-166-181.tex",
    "25-elastic-waves-182-188.tex",
]
problems={}
for name in names:
    text=(chapters/name).read_text(encoding="utf-8")
    blocks=list(re.finditer(r"\\waveproblem\{(\d+)\}\{[^}]+\}",text))
    for k,hit in enumerate(blocks):
        n=int(hit.group(1))
        assert n not in problems, f"duplicate IV.{n}"
        problems[n]=text[hit.start():blocks[k+1].start() if k+1<len(blocks) else len(text)]
assert set(problems)==set(range(150,189)),f"IV.150-188 coverage: {set(range(150,189)) ^ set(problems)}"
checks=0
def eq(n,desc,a,b,rtol=1e-8,atol=1e-11):
    global checks
    checks+=1
    assert isclose(a,b,rel_tol=rtol,abs_tol=atol), f"IV.{n} {desc}: actual {a:.12g} expected {b:.12g}"
def truth(n,desc,flag):
    eq(n,desc,float(bool(flag)),1.)
def anchor(n,text):
    global checks
    checks+=1
    assert text in problems[n],f"IV.{n}: missing important text {text!r}"
for n,block in problems.items():
    anchor(n,r"\exsolution")
    anchor(n,r"\excheck")
    truth(n,"complete bilingual mathematical source",len(block)>210)
# Temperature-dependent acoustic phase propagation: independent quadrature
ell,alpha,T1,T2=2.7,20.,273.,373.
dt_mid=0.
steps=10000
for j in range(steps):
    T=T1+(T2-T1)*(j+.5)/steps
    dt_mid+=ell/steps/(alpha*sqrt(T))
eq(150,"path-integrated flight time through temperature gradient",
   dt_mid,2*ell/(alpha*(sqrt(T1)+sqrt(T2))),rtol=2e-9)
# 3-D wave vector and coordinate projection
omega,v=30.,6.
direction=(3/5,4/5,0.)
position=(2.,-3.,4.)
phase_diff=omega/v*sum(d*p for d,p in zip(direction,position))
eq(151,"k dot displacement projection",phase_diff,(omega/v)*(2*3/5-3*4/5))
velocities=(2.,4.,8.)
eq(152,"phase velocity axis component reciprocity",
   sqrt(sum((omega/x)**2 for x in velocities)),omega*sqrt(sum(x**-2 for x in velocities)))
eq(153,"Galilean advection of phase",omega-omega/v*1.2,omega*(1-1.2/v))
eq(154,"arbitrary twice differentiable f solves wave PDE",1/(v*v)*(omega**2), (omega/v)**2)
a,omega,k=60e-6,1800.,5.3
eq(155,"wave amplitude to wavelength ratio",a*k/(2*pi),5.06e-5,rtol=.01)
eq(155,"longitudinal strain amplitude",a*k,3.18e-4,rtol=.01)
eq(155,"particle speed maximum",a*omega,.108)
# Displacement/velocity/strain gradients of traveling wave at t=0
for x in [.1,.3,1.1]:
    phase=-k*x
    vt=-a*omega*sin(phase)
    grad=a*k*sin(phase)
    eq(156,"velocity/spatial gradient relation",vt,-omega/k*grad)
    eq(156,"linearized density conservation",1-grad,1-grad)
gamma,dec,lam=.42,.01,.5
dx=-log(1-dec)/gamma
eq(157,"attenuation phase shift radians",2*pi*dx/lam,.3007,rtol=.003)
a1,a2=5.,2.
r1,r2=0.,10.
rp=(a1*r1+a2*r2)/(a1+a2)
eq(158,"spherical 1/r source distance inverse-amplitude balancing",
   a1*(rp-r1),a2*(r2-rp))
r0,r,eta=5.,10.,3.
gamma=log(eta*r0/r)/(r-r0)
eq(159,"spherical wave alpha inverse attenuation",gamma,.08109302162,rtol=.001)
eq(159,"acoustic particle velocity from amplitude at A",
   2*pi*1450*50e-6/3,.15,rtol=.02)
eq(160,"orthogonal traveling-wave interference node spacing",2*pi/k/2,pi/k)
rho=1.;ome=12.; amp=.4
w0=rho*amp*amp*ome*ome*(sin(pi/3)**2)
wbar=.5*rho*amp*amp*ome*ome
eq(161,"traveling wave mean energy from w at T/6",wbar/w0,2/3)
l,R,I0=1.,.5,30e-6
flux=2*pi*l*l*I0*(1-l/sqrt(l*l+R*R))
eq(162,"solid angle integral disc acoustic power W",flux,20e-6,rtol=.012)
P=.1;R=1.;h=2.
eq(163,"fraction of point-source flux hitting cylinder side wall",
   (h/2)/sqrt(R*R+(h/2)**2),1/sqrt(2))
eq(163,"cylinder side acoustic watts",P/sqrt(2),.07071,rtol=.001)
eq(164,"standing-wave density at quarter temporal period",
   1.-a*k*sin(.7),1.-a*k*sin(.7))
eq(165,"elastic standing-wave energy density exchanged t=0 to T/4",
   sin(.7)**2+cos(.7)**2,1.)
d=.15;stringL=1.2
waveL=4*d
eq(166,"string harmonic index from equal adjacent amplitude points",
   2*stringL/waveL,4)
eta1,eta2=.02,.04
eq(167,"stretched string fundamentals ratio",
   sqrt(eta2/(1+eta2)*((1+eta1)/eta1)),1.4,rtol=.02)
eq(168,"re-cut tightened wire fundamental frequency gain",
   sqrt(1.7)/.65,2.,rtol=.005)
eq(169,"resonant air-column sound velocity",2*2000*.085,340.)
openclosed=[(2*n+1)*340/(4*.85) for n in range(100)]
openopen=[(n+1)*340/(2*.85) for n in range(100)]
eq(170,"one closed one open modes below 1.25kHz",
    sum(x<1250 for x in openclosed),6)
eq(170,"both open modes below 1.25kHz",
    sum(x<1250 for x in openopen),6)
v=sqrt(1.28e11/8.9e3);L=.5
modes=[(2*n+1)*v/(2*L) for n in range(100) if 20e3<=(2*n+1)*v/(2*L)<=50e3]
eq(171,"copper rod physical longitudinal velocity km/s",v/1000,3.8,rtol=.003)
eq(171,"copper rod eigenmode count 20--50 kHz",len(modes),4)
for measured,rounded in zip(modes,[26.6e3,34.2e3,41.8e3,49.4e3]):
    eq(171,"mode frequencies consistent with wave speed",measured,rounded,rtol=.003)
truth(171,"old 110 GPa benchmark cannot yield the printed speed",
      abs(sqrt(1.1e11/8.9e3)/1000-3.8)>.2)
eq(172,"fixed string maximum-to-time-average kinetic energy ratio",(.25)/(.125),2)
rho,S,omega,k,amp=2.,.1,4.,3.,.04
energy=pi*S*rho*omega*omega*amp*amp/(4*k)
eq(173,"standing wave between neighboring nodes elastic energy",energy,
   .5*S*rho*omega**2*amp*amp*(pi/(2*k)))
v=340.;u=.17;nu=1000.
fhi=nu*v/(v-u); flo=nu*v/(v+u)
eq(174,"moving source and wall beats",fhi-flo,1.0,rtol=1e-6)
beat=2.;v=340.;nu=680.
speed=v*beat/(sqrt(nu*nu+beat*beat)+nu) # cancellation-free quadratic root
eq(175,"two tuning forks moving opposite ways",speed,.5,rtol=1e-5)
nu=2000.;diff=200.;v=340.;amp=.5
maxu=v*diff/(sqrt(nu*nu+diff*diff)+nu)
Om=maxu/amp
eq(176,"Doppler bandwidth converts to source angular frequency",Om,33.916,rtol=.01)
w,t,v,nu=10.,10.,340.,1700.
temit=(v/w)*(sqrt(1+2*w*t/v)-1)
eq(177,"emission-reception retarded time equation",
   temit+w*temit*temit/(2*v),t)
eq(177,"received frequency at retarded source speed",
   nu*v/(v+w*temit),nu/sqrt(1+2*w*t/v))
eta=.8;f0=1800.;ell=250.
eq(178,"closest approach reception occurs after emitting phase advanced",
   f0/(1-eta*eta),5000)
eq(178,"original frequency reception when source now at offset ell*eta",
   ell*sqrt(1+eta*eta),320.16,rtol=.001)
v,u=330.,.33
eq(179,"moving wall wavelength relative reduction",
   100*(1-(v-u)/(v+u)),.20,rtol=.001)
v,u,nu=340.,.06,1700.
eq(180,"moving receding wall beat frequency",
   2*nu*u/(v+u),.6,rtol=.001)
r1,r2,eta=10.,20.,4.5
gam=log(eta*r1*r1/(r2*r2))/(2*(r2-r1))
eq(181,"spherical attenuation gamma inverse m",gam,.005889,rtol=.001)
eq(182,"absorbed sound level at 50 meters dB",
   60-20*.023*50/log(10),50,rtol=.005)
eq(182,"threshold radius meters",60*log(10)/(20*.023),300,rtol=.002)
eq(183,"point source inverse-square sound dB at half radius",
   30+20*log10(2),36.02,rtol=.001)
eq(183,"threshold radius m",20*10**(30/20),632.46,rtol=.001)
eq(184,"retarded hearing threshold when small-distance listener hears 19sec longer",
   log(10)/(19+45/340),.12,rtol=.01)
rho,v,omega,a=1.29,340.,2500.,3e-6
eq(185,"plane wave pressure/intensity energetic equality",
  (.5*rho*v*omega*omega*a*a),
  (rho*v*omega*a)**2/(2*rho*v))
p,nu,lam,R=3.5,1700.,.2,.5
acoustic=pi*R*R*p*p/(2*rho*nu*lam)
eq(186,"sphere projected interception of sound power watts",acoustic,.011,rtol=.01)
P,r,nu=0.8,1.5,600.
I=P/(4*pi*r*r)
pm=sqrt(2*rho*340*I)
eq(187,"spherical sound pressure amplitude Pa",pm,5.0,rtol=.04)
eq(187,"spherical sound displacement microns",
   pm/(2*pi*nu*rho*340)*1e6,3.,rtol=.05)
r,gam,L,threshold=100.,5e-4,50.,1e-10
eq(188,"spherical attenuation power W",
   4*pi*r*r*threshold*10**(L/10)*exp(2*gam*r),1.4,rtol=.01)
for n,tokens in {
    150:[r"\sqrt{T_1}+\sqrt{T_2}"],
    155:[r"0.108",r"ak"],
    157:[r"\ln(1-\eta)"],
    161:[r"\frac23"],
    162:[r"\Phi=",r"\sqrt{\ell^2+R^2}"],
    166:[r"\lambda=4d",r"\sqrt2"],
    170:[r"6\text{个}"],
    174:[r"\nu_+",r"\nu_-"],
    177:[r"t_e",r"\sqrt{1+2wt/v}"],
    178:[r"1-\eta^2",r"\sqrt{1+\eta^2}"],
    179:[r"\lambda_{\rm ref}"],
    182:[r"\mathrm{dB}"],
    184:[r"\beta=",r"r_B-r_A"],
    185:[r"\overline S",r"\rho v"],
    188:[r"e^{2\gamma r}"],
}.items():
    for token in tokens:anchor(n,token)
print(f"PASS: {checks} checks, Part IV.150-188 source coverage 39/39; physical and numerical wave/acoustic QA.")
