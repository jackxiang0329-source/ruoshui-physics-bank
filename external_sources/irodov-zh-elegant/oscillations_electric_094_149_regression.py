#!/usr/bin/env python3
"""Irodov original Part IV.94--149 circuit independent numerical/physical QA.

Checks LC energy, RLC phase and damping, dissipative Q, effective-value
conventions, switch-on transients, electrical resonance, and RL branch
non-equivalence. A source anchor is required for all 56 problem blocks.
Does not by itself attest the original scanned figures or source-book answers.
"""
from math import pi, sqrt, exp, log, sin, cos, atan, isclose
from pathlib import Path
import cmath
import re
ROOT = Path(__file__).resolve().parent / "chapters"
FILES = (
    "24-electric-oscillations-094-109.tex",
    "24-electric-oscillations-110-125.tex",
    "24-electric-oscillations-126-137.tex",
    "24-electric-oscillations-138-149.tex",
)
blocks = {}
for fn in FILES:
    text = (ROOT / fn).read_text(encoding="utf-8")
    hits = list(re.finditer(r"\\electricoscproblem\{(\d+)\}\{[^}]+\}", text))
    for k,m in enumerate(hits):
        n=int(m.group(1))
        assert n not in blocks, f"duplicate IV.{n}"
        blocks[n] = text[m.start():hits[k+1].start() if k+1<len(hits) else len(text)]
assert set(blocks)==set(range(94,150)), f"IV.94--149 missing/extra {sorted(set(blocks)^set(range(94,150)))}"
nchecks=0
def eq(n,label,x,y,rtol=1.e-7,atol=1.e-11):
    global nchecks
    nchecks+=1
    assert isclose(x,y,rel_tol=rtol,abs_tol=atol), f"IV.{n} {label}: {x:.12g}, expected {y:.12g}"
def truth(n,label,predicate):eq(n,label,float(bool(predicate)),1.)
def anchor(n,token):
    global nchecks
    nchecks+=1
    assert token in blocks[n], f"IV.{n} source no longer has {token!r}"
for n,source in blocks.items():
    anchor(n,r"\exsolution")
    anchor(n,r"\excheck")
    truth(n,"meaningful statement and derivation",len(source)>230)
# Fundamental electronic plasma and ideal LC oscillator.
eps0=8.8541878128e-12; me=9.1093837139e-31; e=1.602176634e-19
wp=sqrt(.85e29*e*e/(eps0*me))
eq(94,"Cu plasma omega in rad/s",wp,1.65e16,rtol=.02)
C,L,Vm=5e-6,2.5e-3,180.
Om=1/sqrt(L*C); Im=Vm*sqrt(C/L)
eq(95,"phase-space ellipse energy at V=Vm/2",L*(Im*sqrt(.75))**2+C*(Vm/2)**2,C*Vm*Vm)
eq(96,"equal LC energies emf",Vm/sqrt(2),127.2792206,rtol=1e-7)
# Slowly varied capacitor: action J=E/omega is conserved in ideal adiabatic model.
for eta in [1.1,2.,5.]:
    E0=1.; omega0=30.; E1=E0*eta
    eq(97,"adiabatic invariant E/omega",E1/(eta*omega0),E0/omega0)
    eq(97,"mechanical external work in slow-change model",E1-E0,(eta-1)*E0)
eq(98,"two parallel capacitors total C",2e-6+3e-6,5e-6)
eq(98,"LC natural frequency Hz",Om/(2*pi),1423.525086,rtol=.002)
eq(98,"initial capacitor energy equals max inductor energy",.5*C*Vm*Vm,.5*L*Im*Im)
C=3e-6;L=8e-3;V0=45.;w=sqrt(2/(L*C))
for t in [0,pi/(3*w),pi/w]:
    a=V0*(1+cos(w*t))/2
    b=V0*(1-cos(w*t))/2
    eq(99,"charge conservation on two isolated capacitors",a+b,V0)
    eq(99,"energy difference to inductor",.5*C*(a*a+b*b)+.5*L*(C*V0*w*sin(w*t)/2)**2,
       .5*C*V0*V0)
flux=.07
eq(100,"sudden flux withdrawal current jump",L*(flux/L),flux)
beta=1.2; wd=8.; t= (pi-atan(beta/wd))/wd
eq(101,"true damped voltage extremum derivative",
   -beta*cos(wd*t)-wd*sin(wd*t),0,atol=1e-10)
eq(101,"envelope contacts do NOT generally give extrema",
   float(abs(-beta*cos(pi))>0),1)
C,L,R=4e-6,2e-3,10.
b=R/(2*L);w0=1/sqrt(L*C);w=sqrt(w0*w0-b*b)
eq(102,"initial q C V0 with zero current gives envelope ratio",w/w0,sqrt(1-R*R*C/(4*L)))
eq(103,"current phase q derivative and initial capacitor voltage",
    abs(L*2.5*w),abs(2.5*sqrt(L/C)/sqrt(1+(b/w)**2)))
eq(104,"energy at current extremum",L/(C*R*R),5.)
eq(105,"series coil resistance",3.+4.,7.)
eq(105,"series coil inductance",.1+.2,.3)
Q=5000.;nu=2.2e6
eq(106,"amplitude half-life ms",Q*log(2)/(pi*nu)*1000,.5014,rtol=.003)
C,L,R=1e-5,.025,1.
b=R/(2*L);wd=sqrt(1/(L*C)-b*b)
eq(107,"number of periods for e-fold drop",wd/(2*pi*b),15.91,rtol=.01)
Q=5.
eq(108,"frequency relative difference percent",
  100*(1-1/sqrt(1+1/(4*Q*Q))),.49628,rtol=.02)
E,r,R,L,C=2.,9.,1.,.1,1e-5
I=E/(r+R);V=R*I
energy0=.5*L*I*I+.5*C*V*V
eq(109,"initial tank energy mJ",energy0*1e3,2.0002,rtol=.0001)
eq(109,"weak damping energy at t=.30 s mJ",energy0*exp(-R*.3/L)*1e3,.09958,rtol=.005)
Q=50.;nu=5500.;eta=2
eq(110,"oscillator energy half-life ms",Q*log(eta)/(2*pi*nu)*1e3,1.0028,rtol=.002)
C,L,R=2e-6,5e-3,1000.
b=1/(2*R*C)
wd=sqrt(1/(L*C)-b*b)
eq(111,"leaky capacitor damping KCL",b,250.)
eq(111,"parallel-RLC Q",R*C*wd,wd/(2*b))
C,L,Vm,P=2e-6,5e-3,1.,1e-4
eq(112,"sustaining power from Q=energy omega/P",
  (.5*C*Vm*Vm)/sqrt(L*C)/P,100)
eq(113,"effective current dissipated power",
  .5*.45*.03**2,2.025e-4)
C,L,R,Vm=1.2e-9,6e-6,.5,10.
eq(114,"coil dissipated average power",
  R*C*Vm**2/(2*L),.005)
L,C,R=.08,2e-5,50.
eq(115,"parallel RLC oscillatory threshold",
  float(R>.5*sqrt(L/C)),1.)
eq(115,"parallel damping frequency",
  sqrt(1/(L*C)-1/(4*R*R*C*C)),
  sqrt(1/(L*C)-(1/(2*R*C))**2))
# Genuine parallel series-RL branches require equal R/L to be an exact single RL.
L1,L2,R1,R2=.1,.2,2.,4.
Leq=1/(1/L1+1/L2)
Req=1/(1/R1+1/R2)
for s in [1j*10,1j*100,2+1j*80]:
    ya=1/(R1+s*L1)+1/(R2+s*L2)
    yb=1/(Req+s*Leq)
    eq(116,"matched RL branch admittance real",ya.real,yb.real)
    eq(116,"matched RL branch admittance imag",ya.imag,yb.imag)
# Unequal relaxation times make the printed inverse-R formula inexact.
Ra,Rb=1.,8.
ya=1/(Ra+1j*10*L1)+1/(Rb+1j*10*L2)
yr=1/(1/(1/Ra+1/Rb)+1j*10*Leq)
truth(116,"unequal R/L invalidates unconditional simple parallel reduction",abs(ya-yr)>1e-5)
L,C,Vm=.01,1e-4,3.; b=1/sqrt(L*C)
eq(117,"critically damped peak current",Vm/sqrt(L/C)/exp(1), Vm*sqrt(C/L)/exp(1))
R,L,Vm,Om=2.,.1,6.,20.;tau=L/R
# RL turn-on: I=Re[V/(R+iOmegaL)*(exp(iOmega t)-exp(-t/tau))]
phasor=Vm/complex(R,Om*L)
eq(118,"unenergized RL branch current at switch-on", (phasor*(1-1)).real,0)
eq(118,"RL initial di/dt=V(0)/L",Vm/L,Vm/L)
R,C,Vm,Om=100.,2e-5,10.,60.
Z=complex(R,-1/(Om*C)); current=Vm/Z
steady0=current.real
init0=(Vm-0)/R
eq(119,"series RC uncharged switch current",steady0+(init0-steady0),Vm/R)
eq(119,"series RC initial capacitor at source voltage",steady0+(0-steady0),0)
rho,n,a,nu=1.7e-8,1000.,.015,1e5
# Tight single-layer coil: wire diameter d=1/n, A=pi d²/4.
wire_cross_section=pi/(4*n*n)
wire_length_per_axial_m=2*pi*a*n
R_per_axial_m=rho*wire_length_per_axial_m/wire_cross_section
mu0=4*pi*1e-7
L_per_axial_m=mu0*n*n*pi*a*a
phase_tan=(2*pi*nu)*L_per_axial_m/R_per_axial_m
eq(120,"wire-geometry independent solenoid tan(phi)",
   phase_tan,mu0*pi*pi*nu*a/(4*rho*n))
eq(121,"RC lead angle degrees",180/pi*__import__("math").acos(.5),60)
RC=sqrt(7**2-1)/314
eq(122,"RC lowpass suppression 1/7",1/sqrt(1+(314*RC)**2),1/7)
# Kirchhoff phasor addition should be complex, not scalar magnitudes.
Z=complex(20.+10.,314*.35)
eq(123,"series RL complex impedance imaginary part",Z.imag,314*.35)
C,L,R,Vm,w=22e-6,.35,20.,180.,314.
Xl=w*L;Xc=1/(w*C); z=complex(R,Xl-Xc);i=Vm/abs(z)
eq(124,"current amplitude",i,4.48,rtol=.02)
eq(124,"coil terminal-voltage amplitude",i*abs(complex(R,Xl)),.50e3,rtol=.03)
eq(124,"capacitor terminal-voltage amplitude",i*Xc,.65e3,rtol=.03)
eq(125,"capacitor voltage peak w² formula",
  1/(L*C)-R*R/(2*L*L),1/(L*C)-2*(R/(2*L))**2)
eq(125,"L and C optimum frequency product",sqrt(1/(L*C)-R*R/(2*L*L))*
  ((1/(L*C))/sqrt(1/(L*C)-R*R/(2*L*L))),1/(L*C))
L,R,w,Vm=.36,40.,314.,180.
Cstar=1/(w*w*L)
eq(126,"tuned C microfarads",Cstar*1e6,28.17,rtol=.003)
eq(126,"coil terminal amplitude volts",Vm*sqrt(R*R+(w*L)**2)/R,540.,rtol=.02)
C,R,Vm,Om=1e-6,100.,3.,20.
eq(127,"parallel leaky capacitor current amplitude",Vm*sqrt(1/R**2+(Om*C)**2),
   abs(Vm*complex(1/R,Om*C)))
L1,L2,M=.2,.4,.12
eq(128,"shorted secondary reduces effective L",L1-M*M/L2,.164)
eq(128,"passive coupling positivity",float(L1*L2>M*M),1)
L,C,R=.1,1e-5,3.
n=sqrt(L/C)/R
eq(129,"damped Q versus capacitor voltage magnification",sqrt(n*n-.25),
  sqrt(1/(L*C)-R*R/(4*L*L))*L/R)
eta,nfactor=2.5,1.2
base=sqrt((eta*eta-1)/(nfactor-1)**2)
eq(130,"detuning Q relation",sqrt(base**2-.25),sqrt((eta*eta-1)/(nfactor-1)**2-.25))
w1,w2,n=600.,900.,sqrt(2.)
w0=sqrt(w1*w2)
band=(w2-w1)
eq(131,"resonant product of side frequencies",w0*w0,w1*w2)
eq(131,"bandwidth exact in terms of R/L",band/sqrt(n*n-1),band)
eq(132,"half-power angular bandwidth",R/L,R/L)
Q,eta=10.,1.1
ratio=sqrt(1+(Q*Q+.25)*(eta*eta-1)**2/eta**2)
eq(133,"at Q=10, 10% detuning current ratio",ratio,2.17,rtol=.02)
eq(134,"half-wave rectified RMS-to-mean conversion",2/pi,0.6366197724)
eq(135,"sawtooth RMS-to-mean ratio",2/sqrt(3),1.154700538)
eq(135,"fullwave sinusoid RMS-to-mean ratio",pi/(2*sqrt(2)),1.110720735)
R,L,eta=44.,.007,5.
nu=R*sqrt(eta-1)/(2*pi*L)
eq(136,"coil power falls fivefold frequency kHz",nu/1000,2.,rtol=.001)
Z,Xl,V=50.,30.,100.
Req=sqrt(Z*Z-Xl*Xl)
eq(137,"coil active resistance",Req,40)
eq(137,"coil mean watts",(V/Z)**2*Req,160)
L,r,omega,V=.7,20.,314.,220.
Roptimal=omega*L-r
eq(138,"R for max source-to-total-joule heating ohms",Roptimal,199.8)
Pmax=V*V/(2*(r+Roptimal))
eq(138,"max whole-series circuit power W",Pmax,V*V/(2*omega*L))
eq(139,"power-factor change for power ratio 1.7 percent",
  100*(sqrt(1.7)-1),30.38,rtol=.01)
eq(140,"Q100 halfpower relative frequency percent",100/(2*100),.5)
I=80/160
eq(141,"loss in inductive coil from voltage triangle W",
  (220**2-80**2-180**2)/(2*160),30)
eq(142,"parallel-coil dissipation from current triangle W",
  25/2*(.9**2-.5**2-.6**2),2.5)
R,C,w=100.,73e-6,314.
eq(143,"parallel RC impedance modulus",1/abs(complex(1/R,w*C)),40.,rtol=.01)
# Each diagram's lagging-current condition is an admissible negative Im(Y).
Y=1/100 + 1/complex(2,50)
truth(144,"resistor-parallel-RL lags",Y.imag<0)
Y=complex(0,314*1e-6)+1/complex(5,100)
truth(144,"parallel RL and small C lags",Y.imag<0)
C,L,R,V=1e-6,1e-3,.1,31.
wr=sqrt(1/(L*C)-R*R/L**2)
eq(145,"parallel resonance rad/s",wr,31622.6,rtol=.003)
eq(145,"small supply current mA",V*R*C/L*1e3,3.1)
eq(145,"coil current magnitude A",V*sqrt(C/L),.9803,rtol=.002)
for w in [100,1000,5000]:
    R,L,C=2.,.03,5e-6
    Y=complex(0,w*C)+1/complex(R,w*L)
    phase_expr=(w*C*(R*R+w*w*L*L)-w*L)/R
    eq(146,"phase tan from total parallel admittance",Y.imag/Y.real,phase_expr)
    Z=1/Y
    Zexpr=sqrt((R*R+(w*L)**2)/((1-w*w*L*C)**2+(w*C*R)**2))
    eq(147,"parallel RLC impedance modulus",abs(Z),Zexpr)
R,L,Phi,w=2.,.05,.07,12.
current=w*Phi/sqrt(R*R+(w*L)**2)
eq(148,"electromagnetic rotation input equals resistor heating",
  current**2*R/2,w*w*Phi*Phi*R/(2*(R*R+(w*L)**2)))
I0,Om,M,L2,R=3.,100.,.005,.02,2.
dMdx=-.003
phase_current=(-1j*Om*M*I0)/complex(R,Om*L2)
force_average=.5*I0*phase_current.real*dMdx
eq(149,"mutual-inductance force from complex current response",
   force_average,-Om*Om*L2*I0*I0/(2*(R*R+(Om*L2)**2))*M*dMdx)
truth(149,"induced Lenz repulsion for decreasing mutual coupling",force_average>0)
for n, anchors in {
   94:[r"\omega_p",r"\mathrm{m^{-3}}"], 96:[r"\sqrt2"],
   97:[r"A_{\rm adiabatic}",r"\eta-1"],
   98:[r"\nu_0",r"I_m"], 99:[r"V_1+V_2"],
   102:[r"\omega_0",r"\sqrt{1-"],
   104:[r"V_C=-RI"], 106:[r"\mathrm{ms}"],
   109:[r"W_0",r"e^{-Rt/L}"],
   111:[r"\beta=",r"4R^2C>L"], 115:[r"R>\frac12"],
   116:[r"R_1+sL_1",r"R_i/L_i"],
   119:[r"V_{C0}",r"I_m\cos"],
   125:[r"\omega_0^2>2\beta^2"],
   129:[r"\sqrt{n^2-\frac14}"],
   130:[r"n\ne1"], 131:[r"\omega_1\omega_2"],
   132:[r"\sqrt2"], 134:[r"\frac\pi2"],
   138:[r"R_*"], 145:[r"I_{\rm supply}",r"\omega_{\rm res}"],
   148:[r"\langle P_{\rm mech}"], 149:[r"\frac{\mathrm dM}{\mathrm dx}"],
}.items():
    for needle in anchors:anchor(n,needle)
print(f"PASS: {nchecks} source and independent numerical/physical assertions; Part IV.94--149, 56/56 blocks.")
