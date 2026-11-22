#!/usr/bin/env python3
"""Cross-edition independently-derived physics QA, II.162 / V.139-142 / V.254.

Checks invariants and alternative *physically different* textbook versions:
a scanned n/n bubble versus an n/eta model, 10 m versus 10 mm grating,
670.8 mm versus nm spectrum, and omega^2 versus Wien omega^3.

No assumption that a publicly found different edition proves which glyph was
printed in the user's original scan. No outside webpage is used at CI time.
"""
from pathlib import Path
from math import pi, sin, asin, cos, tan, atan, sqrt, exp, log, isclose
import re
base=Path(__file__).resolve().parent/"chapters"
checks=[];failed=[]
def check(n,label,actual,expected,rel=2e-6,absolute=1e-10):
    if not isclose(actual,expected,rel_tol=rel,abs_tol=absolute):
        failed.append(f"{n}: {label}: computed {actual:.12g} vs expected {expected:.12g}")
    checks.append((n,label))
def truth(n,label,condition):
    check(n,label,float(bool(condition)),1,rel=0,absolute=0)
def get(filename,macro,num):
    source=(base/filename).read_text("utf-8")
    start=re.search(r"\\"+macro+r"\{"+str(num)+r"\}\{[^}]+\}",source)
    if start is None:raise AssertionError(f"missing source block {macro}.{num}")
    nextline=re.search(r"\\"+macro+r"\{\d+\}\{[^}]+\}",source[start.end():])
    end=start.end()+nextline.start() if nextline else len(source)
    item=source[start.start():end]
    for required in [r"\exsolution",r"\excheck"]:
        truth(num,"source block contains "+required,required in item)
    return item
II=get("13-capillarity-160-169.tex","thermocapillaryproblem",162)
V139=get("29-optics-diffraction-131-142.tex","diffractionproblem",139)
V140=get("29-optics-diffraction-131-142.tex","diffractionproblem",140)
V142=get("29-optics-diffraction-131-142.tex","diffractionproblem",142)
V254=get("33-thermal-radiation-246-257.tex","thermalopticsproblem",254)
# Unit/physical constraint for II.162:
def alpha_from_data(p0,d,n,eta):
    return p0*d/8*(n-eta**3)/(n*(eta*eta-1))
for n in [2.,4.,8.,16.]:
    for eta in [1.01,1.03,1.15]:
        if eta >= n**(1/3):continue
        alpha=alpha_from_data(101325.,.001,n,eta)
        p_in=101325+8*alpha/.001
        p_out=101325/n+8*alpha/(eta*.001)
        check("II.162","independent bubble before/after pV equality",p_in/p_out,eta**3,rel=2e-13)
        truth("II.162","positive tension for 1<eta<n^(1/3)",alpha>0)
        truth("II.162","soap double interface pressure jump",8*alpha/.001>0)
    eta=n**(1/3)
    check("II.162","zero tension limit when eta cubed equals n",
          alpha_from_data(101325,.001,n,eta),0,absolute=1e-10)
    check("II.162","scanned equal n/n version negative tension independent of n",
          alpha_from_data(101325,.001,n,n),-101325*.001/8,rel=2e-14)
# Dimensionless independent numerical solve for eta given positive tension.
def n_eta_root(n,pd,alpha):
    lo=1.;hi=n**(1/3)
    for _ in range(60):
        mid=(lo+hi)/2
        a=alpha_from_data(pd,1.,n,mid)
        if a>alpha:lo=mid
        else:hi=mid
    return (lo+hi)/2
for n in [2.,5.,12.]:
    for alpha in [0.03,0.3,3.]:
        eta=n_eta_root(n,101.325,alpha)
        check("II.162","invert bubble alpha to eta by independent bisection",
             alpha_from_data(101.325,1,n,eta),alpha,rel=3e-11)
        truth("II.162","bisection physical eta bounded",1<eta<n**(1/3))
for token in [r"\eta<n^{1/3}",r"\alpha=-\frac{p_0d}{8}",r"\frac{n-\eta^3}"]:
    truth("II.162","source locks original-versus-standard distinction "+token,token in II)
# Spectral grating and actual geometric angular condition.
wl=600.0e-9;dwl=.050e-9
def grating_theta(width):
    sin_theta=wl*wl/(width*dwl)
    return asin(sin_theta)
theta_good=grating_theta(.01);theta_literal=grating_theta(10.)
check("V.139","Mir 10mm version sine",sin(theta_good),.72,rel=1e-12)
check("V.139","Mir 10mm version angle degrees",
      theta_good*180/pi,46.0544804378,rel=3e-8)
check("V.139","scanned literal 10m angle degrees",
      theta_literal*180/pi,.041252966,rel=2e-5)
check("V.139","unit error makes sine differ factor1000",
      sin(theta_good)/sin(theta_literal),1000,rel=1e-12)
for L in [.006,.01,.1,10]:
    if wl*wl/(L*dwl)>1:continue
    theta=grating_theta(L)
    resolving_power=L*sin(theta)/wl
    check("V.139","Rayleigh λ/Δλ from grating geometry",
          resolving_power,wl/dwl,rel=1e-12)
for token in [r"10.0\,\mathrm{mm}",r"10.0\,\mathrm m",
              r"\frac{\lambda^2}{\ell\,\delta\lambda}"]:
    truth("V.139","both version branches and correct formula locked",token in V139)
# V.140: independent restriction |m lambda/d|<=1 and Rayleigh mN.
N=65*200;pitch=.001/200
wavelength=670.8e-9;line_separation=.015e-9
valid=[m for m in range(1,50) if m*wavelength<=pitch]
resolved=[m for m in valid if m*N>=wavelength/line_separation]
check("V.140","physically propagating maximum order",max(valid),7)
check("V.140","first Rayleigh resolved order",min(resolved),4)
check("V.140","doublet shortest resolvable wavelengths in pm",
      670/(max(valid)*N)*1000,7.362637362637362,rel=2e-13)
truth("V.140","scanned mm interpretation has no propagating nonzero order",
      not any(m*670.8e-3<=pitch for m in range(1,10)))
for token in ["670.8",r"\mathrm{nm}",r"670.8\,\mathrm{mm}",
              r"\delta\lambda_{\min}"]:
    truth("V.140","source locks wavelength version/propagation",token in V140)
# V.142: plane-focus x=f tanθ differs from paraxial f sinθ.
f=.8;wl1=310.154e-9;wl2=310.184e-9
for m,exp_um in [(1,6.05452480738),(2,12.44631235375)]:
    # Grating 250 lines/mm instead of V140's 200:
    d=.001/250.
    actual=(f*tan(asin(m*wl2/d))-f*tan(asin(m*wl1/d)))*1e6
    check("V.142",f"exact photographic plane separation order{m} um",
          actual,exp_um,rel=1e-9)
    paraxial=f*m*(wl2-wl1)/d*1e6
    truth("V.142","exact result larger than paraxial for finite theta",
          actual>paraxial)
    mid=(wl1+wl2)/2
    linear=f*m*(wl2-wl1)/d/(1-(m*mid/d)**2)**1.5*1e6
    check("V.142","angle derivative sec cubed correct",linear,actual,rel=1e-8)
truth("V.142","physical non-small-angle position uses tangent",r"\tan" in V142)
truth("V.142","source retains explicit near-axis alternative",
      r"近轴" in V142 and "12.446" in V142)
# V.254: numerically maximize two different spectral *densities*.
h=6.62607015e-34
hb=h/(2*pi)
k=1.380649e-23
c=299792458.
a=7.64e-12
T=2000.
check("V.254","Wien exponent coefficient hbar/k matches 7.64psK",
      hb/k/a,1,rel=.0005)
def golden_max(f,left,right,iterations=100):
    gr=(sqrt(5)-1)/2
    a0=right-gr*(right-left);b0=left+gr*(right-left)
    for _ in range(iterations):
        if f(a0)<f(b0):
            left=a0;a0=b0;b0=left+gr*(right-left)
        else:
            right=b0;b0=a0;a0=right-gr*(right-left)
    return (left+right)/2
for power in [2,3]:
    # x=a omega/T, y=2pi ca/(T lambda), u_omega∝x^power e^-x,
    # u_lambda∝y^(power+2) e^-y. Numerical optimization is
    # independent of analytic derivative yielding p and p+2.
    xmax=golden_max(lambda x:x**power*exp(-x),.05,15.)
    ymax=golden_max(lambda y:y**(power+2)*exp(-y),.05,15.)
    check("V.254",f"numerical omega spectrum peak for omega^{power}",
          xmax,power,rel=1e-7)
    check("V.254",f"numerical wavelength spectrum peak for omega^{power}",
          ymax,power+2,rel=1e-7)
    lambda_um=(2*pi*c*a/(T*ymax))*1e6
    check("V.254",f"wavelength peak micron from Jacobian omega^{power}",
          lambda_um,{2:1.799,3:1.439}[power],rel=.004)
    freq=(xmax*T/a)
    check("V.254",f"angular frequency peak from omega^{power}",
          freq,{2:5.235602094e14,3:7.853403142e14}[power],rel=1e-7)
    check("V.254",f"frequency and wavelength maxima product not 2pi c omega^{power}",
          lambda_um*1e-6*freq/(2*pi*c),power/(power+2),rel=1e-7)
# Numerical area conservation with actual Jacobian, no curve-mode matching:
# use a dimensionless x frequency interval [1,8] and y=const/lambda inverse.
for power in [2,3]:
    def simpson(fun,lo,hi,N=2400):
        step=(hi-lo)/N
        return step/3*(fun(lo)+fun(hi)
              +4*sum(fun(lo+(2*j+1)*step) for j in range(N//2))
              +2*sum(fun(lo+2*j*step) for j in range(1,N//2)))
    freq_area=simpson(lambda x:x**power*exp(-x),1.,8.)
    wavelength_area=simpson(
        lambda y:(1/y)**power*exp(-1/y)/(y*y),
        1/8,1.,N=9600)
    check("V.254",f"ω and λ integrated spectral energy invariant power{power}",
          wavelength_area,freq_area,rel=3e-6)
for token in [r"\omega^2",r"\omega^3",r"\frac{3T}{a}",
              r"\lambda^{-5}",r"\frac{\pi ca}{2T}"]:
    truth("V.254","source locks both versions and density Jacobian",token in V254)
if failed:
    for f in failed:print("FAIL:",f)
    raise AssertionError(f"{len(failed)}/{len(checks)} cross-edition checks failed")
print(f"PASS: {len(checks)} independently recomputed cross-edition physics checks"
      " (original II.162 and V.139,V.140,V.142,V.254; no new problem numbers).")
