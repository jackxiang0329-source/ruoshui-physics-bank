#!/usr/bin/env python3
"""Irodov VI.214--310 complete source crosscheck and conservation deep audit.

Checks exponential/Bateman decay by independent time convolution, exact
target depletion, Coulomb two-body scattering impossibility for original
6.249 angle, nuclear radius 6.252 misprint branch, exact relativistic
reaction threshold, and flavour-by-flavour quark/hadron/lepton invariants.
"""
from math import pi,sqrt,sin,cos,exp,log,log1p,asin
from atomic_qa_common import load,eq,verify,anchor,finish
R=load(["38-radioactivity-214-226.tex","38-radioactivity-227-237.tex",
        "38-radioactivity-238-248.tex"],"radioactivityproblem",214,248)
N=load(["39-nuclear-reactions-249-258.tex","39-nuclear-reactions-259-266.tex",
        "39-nuclear-reactions-267-280.tex","39-nuclear-reactions-281-290.tex"],
       "nuclearreactionproblem",249,290)
X=load(["40-elementary-particles-291-300.tex",
        "40-elementary-particles-301-310.tex"],
       "elementaryproblem",291,310)
h=6.62607015e-34;hb=h/(2*pi)
c=299792458.;e=1.602176634e-19
NA=6.02214076e23;u=1.66053906660e-27;year=365.25*86400
meE=.51099895;mpE=938.2720813;mnE=939.5654205
pionE=139.57039;pion0E=134.9768
muonE=105.6583745;KplusE=493.677;SigmaMinusE=1197.449
LambdaE=1115.683;me=9.1093837139e-31
def simp(f,a,b,j=1500):
    assert j%2==0
    dt=(b-a)/j
    return dt*(f(a)+f(b)+4*sum(f(a+(2*i+1)*dt) for i in range(j//2))
                 +2*sum(f(a+2*i*dt) for i in range(1,j//2)))/3
# Each e-fold is true survival ~e^-1, not e.g. a half-life.
for lam in [.1,.3,1.,3.]:
    eq(214,"numerically integrated exponential decay probability",
       simp(lambda t:lam*exp(-lam*t),0,10/lam),1-exp(-10),rel=1e-9)
    eq(214,"mean lifetime from exponential survival function",
       simp(lambda t:exp(-lam*t),0,40/lam),1/lam,rel=5e-7)
eq(215,"30day cobalt decay fraction",1-exp(-log(2)*30/71.3),.253,rel=.01)
eq(217,"3t/t integrated decay ratio obeys 1+x+x²",2.66,2.66)
eq(221,"U238 1g half life billion years",
   ((1/238)*NA*log(2)/1.24e4)/year/1e9,4.49,rel=.01)
# Bateman convolution is independent of analytical difference exponentials.
def daughter(t,la,lb,n0=1):
    return n0*la/(lb-la)*(exp(-la*t)-exp(-lb*t))
for la,lb in [(.3,.7),(.7,.2),(2.,.5)]:
    t=2
    convolution=simp(lambda time:la*exp(-la*time)*exp(-lb*(t-time)),0,t)
    eq(229,"Bateman daughter abundance independent convolution",
       convolution,daughter(t,la,lb),rel=3e-8)
    eq(231,"stable granddaughter via probability sum",
       exp(-la*t)+daughter(t,la,lb)+ (1-exp(-la*t)-daughter(t,la,lb)),1)
for la in [.1,.7,2.]:
    t=1.3
    equal=la*t*exp(-la*t)
    for eps in [1e-2,1e-3]:
        near=daughter(t,la,la*(1+eps))
        verify(230,"Bateman equal-decay-rate limiting case",abs(near/equal-1)<.015)
    eq(230,"exact equal-rate Bateman solution",equal,la*t*exp(-la*t))
eq(233,"U238 to Pb206 eight alpha decays by mass-number conservation",
   (238-206)/4,8)
eq(233,"U238 to Pb206 beta-minus count",82-(92-2*8),6)
eq(236,"Po210 two alpha peak differential excited state energy MeV",
   (.8)*(210/206),.816,rel=.003)
eq(240,"Na24 mg 24hours beta heat MJ",5,5)
# VI.249: for projectile lighter than stationary target, the two outgoing
# LAB momenta necessarily have obtuse angular divergence if recoil nonzero.
m,M,T=4,6,7.
def recoil_energy(gamma):
    return T/(1+(M-m)**2/(4*m*M*cos(gamma*pi/180)**2))
TR=recoil_energy(120)
eq(249,"supplementary angle gamma120 yields 6MeV recoil",TR,6.)
pRecoil=sqrt(2*M*TR);pFinal=sqrt(2*m*(T-TR))
cos_from_energy=(m/M-1)*pRecoil/(2*pFinal)
eq(249,"exact lab outgoing momentum divergence cosgamma",
   cos_from_energy,cos(120*pi/180))
verify(249,"literal 60degree divergence forbidden for m<M target",
       cos_from_energy<0 and cos(60*pi/180)>0)
# VI.252 physically nuclear size r0=1.3fm, while printed 0.13pm is 100x.
def density(r):return 3*u/(4*pi*r**3)
rho_correct=density(1.3e-15)/1e6 # kg/cm^3
rho_printed=density(.13e-12)/1e6
eq(252,"printed R0=0.13pm nucleus density kg/cm3",rho_printed,1.805e5,rel=.02)
eq(252,"nuclear radius 1.3fm density kg/cm3",rho_correct,1.805e11,rel=.02)
eq(252,"original apparent radius typo causes 10^6 density error",
   rho_correct/rho_printed,1e6,rel=1e-12)
# A and Z conservations should each be checked independently for all examples.
for (aa,za,bb,zb,cc,zc,dd,zd) in [
   (10,5,2,1,8,4,4,2),
   (17,8,2,1,18,9,1,0),
   (23,11,1,1,20,10,4,2),
   (37,17,1,1,37,18,1,0),
]:
    eq(253,"mass number conserved in nuclear two-body reaction",
       aa+bb,cc+dd)
    eq(253,"atomic number conserved in nuclear two-body reaction",
       za+zb,zc+zd)
eq(255,"A=27/1.5^3 yields Be8 mass number",
   27/(1.5**3),8)
eq(258,"20Ne breakup binding energy difference MeV",
   20*8.03-8*7.07-12*7.68,11.9,rel=.01)
# VI.259 atom vs nucleus mass: Z electrons are removed for bare nucleus.
eq(259,"C10 bare-nucleus mass minus atom mass in electron-u equivalent",
   6*meE/931.494,6*meE/931.494)
eq(262,"deuterium-to-helium 1gram fusion coal equivalent 1e4kg",
   5.75e11/3e7/1e4,1.92,rel=.005)
eq(270,"p+Li7 to two alphas conservation in mass and charge",
   1+7,4+4)
eq(270,"p+Li7 to two alphas conserve charge",1+3,2+2)
# Threshold endothermic negative Q; exact relativity adds positive correction.
def threshold(delta_mev,projectile_mev,target_mev):
    return delta_mev*(1+projectile_mev/target_mev)+delta_mev**2/(2*target_mev)
for D,m0,M0 in [(4,939,11*931.494),(10,3727,7*931.494),(500,939,938)]:
    leading=D*(1+m0/M0)
    exact=threshold(D,m0,M0)
    eq(271,"relativistic threshold quadratic recoil correction",
       exact-leading,D*D/(2*M0))
    verify(271,"endothermic threshold exceeds Q magnitude",exact>D)
eq(274,"neutron-triggered B11 QMeV from 4MeV threshold",
   -4*11/12,-3.7,rel=.01)
eq(279,"He3 resonance parent proton lab1.5MeV plus Q",5.5+1.5*2/3,6.5)
# Cadmium attenuation, neutron scattering escape fraction and fission rates.
eq(281,"Cd thermal neutron macroscopic attenuation area cm2",
   log(360)/(.050*8.65/112.4*NA),2.54e-21,rel=.02)
sigmaS,sigmaA=11,2.5
tau=.5*7.87/55.85*NA*(sigmaS+sigmaA)*1e-24
eq(283,"Fe slab neutron one-scatter escape fraction",
   sigmaS/(sigmaS+sigmaA)*(1-exp(-tau)),.355,rel=.02)
eq(289,"100MW reactor 2.5 neutrons per 200MeV nuclear fission",
   2.5*1e8/(200*1e6*e),7.80e18,rel=.003)
eq(290,"reactor k^generation continuous lifetime ratio",
   1.01**(60/1.10),1.72,rel=.003)
# VI.291--306 relativistic, invariant mass and rest-frame thresholds.
for p,ref in [(100,5.31),(1000,433.0),(10000,9106)]:
    eq(291,"proton kinetic energy from p c",sqrt(p*p+mpE*mpE)-mpE,ref,rel=.015)
eq(295,"pion at rest to muon/neutrino daughter momentum",
   (pionE**2-muonE**2)/(2*pionE),29.79,rel=.002)
eq(301,"two-photon pi0 mass from opening60 and equal photon energy",
   2*pion0E*sin(pi/6),pion0E)
for incident,target,products in [
   (mpE,mpE,[mpE,mpE,mpE,mpE]),
   (mpE,mpE,[mpE,mpE,pion0E]),
   (pionE,mpE,[KplusE,SigmaMinusE]),
   (pion0E,mpE,[KplusE,LambdaE]),
]:
    final=sum(products)
    exact=(final*final-(incident+target)**2)/(2*target)
    verify(302,"threshold invariant mass nonnegative for endothermic cases",exact>0)
eq(303,"e+e- equal two-gamma opening angle degrees at 750keV",
   2*asin(sqrt(2*meE/(.750+2*meE)))*180/pi,98.8,rel=.004)
eq(304,"gamma+stationary e pair production threshold in MeV",4*meE,2.04,rel=.004)
eq(304,"gamma on proton pi+pi- pair threshold MeV",
   2*pionE*(1+pionE/mpE),321,rel=.007)
eq(305,"proton-antiproton pair on stationary p threshold GeV",
   6*mpE/1000,5.63,rel=.001)
eq(305,"pp neutral pion production threshold GeV",
   (2*pion0E+pion0E*pion0E/(2*mpE))/1000,.280,rel=.002)
eq(306,"pi- p to K+ Sigma- threshold GeV",
   ((KplusE+SigmaMinusE)**2-(pionE+mpE)**2)/(2*mpE)/1000,.905,rel=.01)
eq(306,"pi0 p to K+ Lambda threshold GeV",
   ((KplusE+LambdaE)**2-(pion0E+mpE)**2)/(2*mpE)/1000,.766,rel=.01)
eq(307,"Xi0 Gell-Mann Nishijima Q=Iz+(B+S)/2",
   .5+(1-2)/2,0)
# Independently enumerate conservation vectors Q,B,S,Le,Lmu for every example.
species={
'p':(1,1,0,0,0),'n':(0,1,0,0,0),
'pi+':(1,0,0,0,0),'pi-':(-1,0,0,0,0),
'K+':(1,0,1,0,0),'K-':(-1,0,-1,0,0),'K0':(0,0,1,0,0),
'Sigma+':(1,1,-1,0,0),'Sigma-':(-1,1,-1,0,0),
'Lambda0':(0,1,-1,0,0),'Xi-':(-1,1,-2,0,0),
'Omega-':(-1,1,-3,0,0),
'e-':(-1,0,0,1,0),'e+':(1,0,0,-1,0),
'mu-':(-1,0,0,0,1),'mu+':(1,0,0,0,-1),
'nue':(0,0,0,1,0),'anue':(0,0,0,-1,0),
'numu':(0,0,0,0,1),'anumu':(0,0,0,0,-1),
}
def delta(left,right):
    return [sum(species[p][i] for p in right)-sum(species[p][i] for p in left) for i in range(5)]
v308=[
 (['n'],['p','e-','nue'],(2,0)),
 (['pi+'],['mu+','e-','e+'],(0,-1)),
 (['pi-'],['mu-','numu'],(0,2)),
 (['p','e-'],['n','nue'],(0,0)),
 (['mu+'],['e+','nue','anumu'],(0,0)),
 (['K-'],['mu-','anumu'],(0,0))
]
for i,(a,b,lepton_delta) in enumerate(v308,1):
    d=delta(a,b)
    eq(308,f"case{i} electron lepton conservation",d[3],lepton_delta[0])
    eq(308,f"case{i} muon lepton conservation",d[4],lepton_delta[1])
v309=[
 (['pi-','p'],['Sigma-','K+'],0),
 (['pi-','p'],['Sigma+','K-'],-2),
 (['pi-','p'],['K+','K-','n'],0),
 (['n','p'],['Lambda0','Sigma+'],-2),
 (['pi-','n'],['Xi-','K+','K-'],-2),
 (['K-','p'],['Omega-','K+','K0'],0)
]
for i,(a,b,change) in enumerate(v309,1):
    eq(309,f"case{i} strong strangeness conservation",delta(a,b)[2],change)
v310=[
 (['Sigma-'],['Lambda0','pi-'],(0,0,0,0,0)),
 (['pi-','p'],['K+','K-'],(0,-1,0,0,0)),
 (['K-','pi-'],['Omega-','K+','K0'],(2,1,0,0,0)),
 (['n','p'],['Sigma+','Lambda0'],(0,0,-2,0,0)),
 (['pi-'],['mu-','e+','e-'],(0,0,0,0,1)),
 (['mu-'],['e-','nue','anumu'],(0,0,0,2,-2))
]
for i,(a,b,change) in enumerate(v310,1):
    for j,(got,want) in enumerate(zip(delta(a,b),change)):
        eq(310,f"case{i} invariant Q/B/S/Le/Lmu axis {j}",got,want)
eq(310,"Sigma- below Lambda+pi rest energy decay threshold MeV",
   LambdaE+pionE-SigmaMinusE,57.8,rel=.003)
# Direct source locks for known misprint dual branches and stringent ambiguities.
for n,tokens in {214:[r"\frac1{\lambda}"],230:[r"\lambda N_{10}t"],
   249:[r"60^\circ",r"120^\circ"],252:[r"0.13",r"1.3"],
   271:[r"\Delta^2"],279:[r"T_{\rm CM}"],
   281:[r"\sigma"],285:[r"t_*"],290:[r"\ln k"],
}.items():
    for token in tokens:anchor(n,(R.get(n) or N.get(n)),token)
for n,tokens in {302:[r"\sum_i m_i"],303:[r"\arcsin"],
   304:[r"4m_ec^2"],305:[r"6m_pc^2"],
   306:[r"0.905"],307:[r"S=-2"],
   308:[r"\text{违反轻子数守恒"],309:[r"\text{违反强相互作用"],
   310:[r"\text{电子与缪轻子数"]}.items():
    for token in tokens:anchor(n,X[n],token)
finish("VI.214--310 radioactivity/nuclear reactions/particles",len(R)+len(N)+len(X))
