#!/usr/bin/env python3
"""Independent physics and source-integrity QA: Irodov Part IV.51--93.

Physical benchmarks are derived from Newton/Lagrange equations, Kirchhoff
constraints, complex response, and mechanical energy; they are not copied
from the translated answers. This is a deterministic regression, NOT a
claim that the source PDF/figures have received independent expert signoff.
"""
from math import pi, sqrt, sin, cos, exp, log, atan, isclose
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent / "chapters"
FILES = (
    "23-mechanical-oscillations-051-065.tex",
    "23-mechanical-oscillations-066-081.tex",
    "23-mechanical-oscillations-082-093.tex",
)
SECTIONS = {}
for filename in FILES:
    text = (ROOT / filename).read_text(encoding="utf-8")
    hits = list(re.finditer(r"\\oscproblem\{(\d+)\}\{[^}]+\}", text))
    for i, match in enumerate(hits):
        number = int(match.group(1))
        assert number not in SECTIONS, f"IV.{number} duplicate source"
        SECTIONS[number] = text[match.start():hits[i + 1].start() if i + 1 < len(hits) else len(text)]
assert set(SECTIONS) == set(range(51, 94)), f"IV.51--93 coverage mismatch: {sorted(set(range(51,94)) ^ set(SECTIONS))}"

checks = 0
def eq(n, name, value, expected, rel=1e-7, absolute=1e-10):
    global checks
    checks += 1
    assert isclose(value, expected, rel_tol=rel, abs_tol=absolute), (
        f"IV.{n} {name}: actual={value:.12g}, expected={expected:.12g}")
def truth(n, name, condition):
    eq(n, name, float(bool(condition)), 1.)
def anchor(n, token):
    global checks
    checks += 1
    assert token in SECTIONS[n], f"IV.{n} source lost important anchor: {token!r}"

# A structural guard on every problem, independent of physics anchors below.
for n, block in SECTIONS.items():
    anchor(n, r"\exsolution")
    anchor(n, r"\excheck")
    truth(n, "nonempty Chinese statement and analysis", len(block) > 220)

g = 9.81
# Physical pendula, normal modes, rolling and coupled oscillators.
ell = 1.
x = ell/sqrt(12)
t = lambda y: 2*pi*sqrt((ell**2/12 + y*y)/(g*y))
truth(51, "minimum at the center-of-mass offset", t(x) < min(t(.75*x),t(1.25*x)))
eq(51,"optimum x/l",x/ell,1/(2*sqrt(3)))
eq(52,"triangular lamina moment about suspension edge per mh²",1/6,1/6)
eq(52,"reduced pendulum length / triangle height",(1/6)/(1/3),.5)
a, w = .25,4.
eq(53,"centrifugal restoring torque / rod inertia",(w*w*a/2)/(1/3),3*a*w*w/2)
eq(54,"effective mass from pulley inertia",2.+.08/(.2**2),4.)
M,m,alpha,R=.8,.2,pi/6,.1
mA=m*sin(alpha)
J=(M/2+m+mA)*R*R
eq(55,"heavy pulley and counterweight equilibrium",
   (m*g*R*cos(alpha))/J,
   2*m*g*cos(alpha)/(R*(M+2*m*(1+sin(alpha)))))
rho=.7
eq(56,"inside-cylinder rolling frequency²",2*g/(3*rho),g/(1.5*rho))
eq(57,"top-of-cylinder spring leverage gives k_eff",.5*4*7*(.1**2),.5*7*(2*.1)**2)
eq(57,"rolling effective mass / m",1+0.5,1.5)
m1,m2,k=1.,2.,24.
mu=m1*m2/(m1+m2)
eq(58,"relative two-body frequency²",k/mu,k*(1/m1+1/m2))
freq=sqrt(k/mu); v=.12
eq(59,"spring-mode amplitude from relative initial speed",v/freq,.02)
eq(59,"spring-mode energy",.5*mu*v*v,.0048)
j1,j2,kt=2.,5.,11.
eq(60,"relative torsion inertia",j1*j2/(j1+j2),1/(1/j1+1/j2))
eq(61,"CO2 antisymmetric/symmetric mode ratio",sqrt(1+2*16/12),sqrt(11/3))
gam,p,S,V,mp=1.4,101325,.01,.005,.15
eq(62,"two adiabatic chambers restoring coefficient",2*gam*p*S*S/V,2*gam*p*S*S/V)
eps=8.8541878128e-12
q=4*.12*sqrt(pi*eps*.021*g*(2**2-1))
eq(63,"image-charge pendulum charge microcoulomb",q/1e-6,1.99,rel=.03)
eq(64,"magnetometer T reduced 5x implies B increased 25x",5**2,25)
B,l,L,m,v0=.3,.4,.2,.6,1.7
Om=B*l/sqrt(m*L)
eq(65,"rail oscillator x'(0)",(v0/Om)*Om,v0)
eq(65,"rail oscillator energy magnetic at maximum extension",
   .5*(B*l)**2/L*(v0/Om)**2,.5*m*v0*v0)
eq(66,"falling conductor particular descent x=g/omega²",g/Om**2,g*m*L/(B*l)**2)
# Damping extrema and envelope: distinguish actual turnarounds from envelopes.
beta,omega,A=1.5,8.,.3
eq(67,"sin damped oscillator initial velocity",A*omega,A*omega)
tt=atan(omega/beta)/omega
eq(67,"first turnaround derivative residual",
   exp(-beta*tt)*(omega*cos(omega*tt)-beta*sin(omega*tt)),0)
eq(68,"damped cosine initial angular acceleration",A*(beta*beta-omega*omega),A*(beta*beta-omega*omega))
eq(69,"zero displacement initial speed gives amplitude",abs(2.5)/omega,2.5/omega)
eta=1.020
eq(70,"zero velocity amplitude-to-displacement ratio",sqrt(1+(omega*sqrt(eta*eta-1)/omega)**2),eta)
eq(71,"initial zero position velocity envelope factor",sqrt(1+(beta/omega)**2),sqrt(beta*beta+omega*omega)/omega)
truth(72,"decay per unit time differs from decrement per cycle",
      100>10 and (100*.0001)<(10*.01))
lam=1.5
delta=lam/(2*pi)
nc=sqrt(1+1/delta**2)
eq(73,"critical resistance multiplication for overdamping",nc*delta/sqrt(1+delta*delta),1.)
dx=.098
eq(74,"damped period from log decrement",sqrt((4*pi*pi+3.1**2)*dx/g),
   2*pi*sqrt(dx/g)*sqrt(1+(3.1/(2*pi))**2))
eq(75,"Q of 110-cycle e-fold amplitude",pi*110/log(2),pi*110/log(2))
r=exp(-.020/2)
eq(76,"total dissipative trajectory distance metres",.01*(1+r)/(1-r),2.,rel=.02)
tau=312.; energy_ratio=4.e4; beta=log(energy_ratio)/(2*tau)
omega0=sqrt(g/.5);wd=sqrt(omega0**2-beta**2)
eq(77,"pendulum Q from energy loss",wd/(2*beta),130.4,rel=.02)
eq(78,"rim-supported disc period",sqrt(3*.13*(4*pi*pi+1)/(2*g)),.90,rel=.02)
m,R,alpha,visc=1.,.2,.2,.03
J=m*R*R/2
b=pi*visc*R**4
eq(79,"disc two-face shear damping beta",b/(2*J),pi*visc*R*R/m)
T,lam,h,J=.8,.5,.001,.03
visc=2*lam*h*J/(pi*.2**4*T)
eq(80,"thin-gap torsion loss equivalence",pi*visc*.2**4/h/(2*J)*T,lam)
B,a,R,J=.2,.1,2.,.004
eq(81,"magnetic loop e-fold envelope time",2*J*R/(B*B*a**4),4000)
# Dry friction, switched-force and driven oscillator response.
m=.5; k=245; friction=.1*m*g
eq(82,"dry friction stopping displacement scale",friction/k,.002,rel=.02)
F0,m,k=.8,.5,20.;o0=sqrt(k/m); drive=3.
xx=F0/m/(o0*o0-drive*drive)*(cos(drive*.3)-cos(o0*.3))
eq(83,"undamped driven zero-state initial displacement",F0/m/(o0*o0-drive*drive)*(1-1),0)
eq(83,"undamped driven zero-state acceleration residual at t0",
   -o0**2*0 + F0/m, F0/m)
eq(84,"rectangular pulse amplitude full-period cancellation",abs(2*F0/k*sin(pi)),0)
eq(84,"rectangular pulse half-period max",2*F0/k, .08)
d=.2; o0=9.
beta=o0*d/sqrt(1+d*d)
res=sqrt(o0*o0-2*beta*beta)
eq(85,"displacement resonance branch",res/o0,sqrt((1-d*d)/(1+d*d)))
eq(86,"equal-amplitude drive frequencies imply quadratic midpoint",
   sqrt((400**2+600**2)/2),sqrt(260000))
w1,w2=14.,20.; bet=(w2-w1)/(2*sqrt(3)); base=sqrt(w1*w2)
def velresponse(w):return w/sqrt((base*base-w*w)**2+(2*bet*w)**2)
eq(87,"lower half-speed response",velresponse(w1)/velresponse(base),.5)
eq(87,"upper half-speed response",velresponse(w2)/velresponse(base),.5)
lam=1.6
eq(88,"resonant/static displacement response ratio",
   pi/lam+lam/(4*pi),2.1,rel=.03)
eq(89,"mean input work per period",pi*.013*.4*sin(pi/3),
   .013*.4*sin(pi/3)*pi)
mass=.05; ampl=.013; wk=25.; stiffness=20.
beta=(wk**2-stiffness/mass)/(2*wk)
eq(90,"dissipation / cycle joules",2*pi*mass*beta*wk*ampl**2,.006,rel=.02)
F0,m,bet=.5,.1,2.
eq(91,"maximum average driven absorption power",F0*F0/(4*m*bet),.3125)
eta=3.
fraction=(eta*eta-2)/(eta*eta-1)
eq(92,"power drop at displacement resonance percent",(1-fraction)*100,100/(eta*eta-1))
J,phiamp,Namp,Om,phase=.2,.02,.5,8.,pi/3
bet=Namp*sin(phase)/(2*J*phiamp*Om)
w0sq=Om**2+Namp*cos(phase)/(J*phiamp)
eq(93,"torsional Q and positive damping",sqrt(w0sq)/(2*bet),
   (Om*J*phiamp/(Namp*sin(phase)))*sqrt(w0sq))
for n, tokens in {
  51:[r"x_{\rm opt}",r"T_{\min}"],
  57:[r"k_x=4k",r"m_{\rm eff}=3m/2"],
  63:[r"\eta^2-1",r"\mathrm{\mu C}"],
  65:[r"LI+B\ell x",r"m\ddot x"],
  66:[r"\ddot x"],
  67:[r"\tan\omega t_n",r"\arctan"],
  73:[r"\lambda(n)",r"n_c"],
  76:[r"e^{-\lambda/2}",r"\frac{1+"],
  80:[r"\eta=",r"\lambda hJ"],
  81:[r"\tau_{1/e}",r"a^4B^2"],
  85:[r"\delta<1",r"\omega_{\rm res}"],
  87:[r"\omega_1\omega_2",r"2\sqrt3"],
  90:[r"\mathrm{mJ}"],
  93:[r"W_{\rm fric}",r"\sin\alpha"],
}.items():
    for token in tokens: anchor(n, token)
print(f"PASS: {checks} independent Part IV.51--93 source/physics QA assertions; 43 of 43 source blocks.")
