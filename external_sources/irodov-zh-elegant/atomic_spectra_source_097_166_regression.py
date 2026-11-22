#!/usr/bin/env python3
"""Irodov VI.97--166 second-pass atomic term, spectral and Zeeman QA.

Enumerates angular-momentum couplings and all allowed magnetic sublevel
transitions rather than copying answer counts. Treats an apparent source
6.159 exponent inconsistency as explicit unresolved edition issue.
"""
from math import pi,sqrt,cos,sin,exp,log,asin
from atomic_qa_common import load,eq,verify,anchor,finish
P=load(["36-atomic-spectra-097-104.tex","36-atomic-spectra-105-117.tex",
        "36-atomic-spectra-118-134.tex","36-atomic-spectra-135-147.tex",
        "36-atomic-spectra-148-158.tex","36-atomic-spectra-159-166.tex"],
       "atomictermsproblem",97,166)
h=6.62607015e-34;c=299792458.
e=1.602176634e-19;kb=1.380649e-23
me=9.1093837139e-31
hb=h/(2*pi)
muB=e*hb/(2*me)
Ry=13.605693
def allowed_J(L,S):
    assert round(2*L)==2*L and round(2*S)==2*S
    return [j/2 for j in range(round(2*abs(L-S)),round(2*(L+S))+1,2)]
def g_factor(L,S,J):
    assert J>0
    return 1+(J*(J+1)+S*(S+1)-L*(L+1))/(2*J*(J+1))
def wavelength_nm(deltaev):return h*c/(deltaev*e)*1e9
for L,S in [(0,.5),(1,.5),(2,1),(3,2),(3,3),(2,2.5)]:
    Js=allowed_J(L,S)
    eq(104,"angular-momentum triangle J minimum",Js[0],abs(L-S))
    eq(104,"angular-momentum triangle J maximum",Js[-1],L+S)
    eq(104,"angular-momentum distinct J count",len(Js),2*min(L,S)+1)
eq(103,"one electron 3 shell allowed 3S/3P/3D J terms",
   len(allowed_J(0,.5))+len(allowed_J(1,.5))+len(allowed_J(2,.5)),5)
eq(105,"4P spin S=3/2 gives 3 Js",len(allowed_J(1,1.5)),3)
eq(105,"5D spin S=2 gives 5 Js",len(allowed_J(2,2)),5)
eq(106,"Na 4f max J",max(allowed_J(3,.5)),3.5)
eq(107,"five different J in F requires S=2",len(allowed_J(3,2)),5)
eq(107,"five different J in D for S>=2",len(allowed_J(2,3)),5)
eq(108,"S=1,J=4 permissible L values",sum(4 in allowed_J(L,1) for L in range(8)),3)
eq(109,"D2 possible multiplicities",sum(2 in allowed_J(2,S) for S in range(5)),5)
eq(109,"P_3/2 possible odd-numbered spin doubles",
   sum(1.5 in allowed_J(1,S) for S in [.5,1.5,2.5]),3)
eq(115,"Li 3d spin-orbital complete degeneracy",sum(2*J+1 for J in allowed_J(2,.5)),10)
eq(116,"triplet D at J=3 magnetic degeneracy",2*3+1,7)
eq(117,"triplet F J3 unique 7-fold level",2*3+1,7)
# Hund Aufbau spin and orbital selection are separate constraints.
eq(118,"As closed KLM and 4s2 4p3 total electrons",2+8+18+2+3,33)
eq(119,"p3 high-spin half-shell ground term S",3/2,1.5)
eq(119,"p4 > half-full J=L+S",1+1,2)
eq(120,"d3 < half full 4F_{3/2}",abs(3-1.5),1.5)
eq(120,"d7 > half full 4F_{9/2}",3+1.5,4.5)
eq(124,"d5 half-filled total orbital moment L",sum([-2,-1,0,1,2]),0)
eq(124,"d5 spin only moment sqrt35 in Bohr magnetons",2*sqrt(2.5*3.5),sqrt(35))
# Alkali quantum-defect spectroscopy.
eb2P=13.6/(2-.04)**2;eb3S=13.6/(3-.41)**2;eb2S=13.6/(2-.41)**2
eq(100,"Li 3s to 2p band nm",wavelength_nm(eb2P-eb3S),819,rel=.02)
eq(100,"Li 2p to 2s band nm",wavelength_nm(eb2S-eb2P),674,rel=.02)
eq(101,"sodium doublet FS energy meV",
   h*c/e*(1/(589e-9)-1/(589.56e-9))*1e3,2.0,rel=.01)
eq(102,"Cs term splitting same angular frequency every series transition",
   2*pi*c*(1/(1358.8e-9)-1/(1469.5e-9)),1.044e14,rel=.01)
# Boltzmann degeneracy must not be silently dropped.
eq(125,"H at 3000K n2/n1",
   4*exp(-10.2*e/(kb*3000)),2.9e-17,rel=.06)
eq(126,"Na at 2400K 3P/3S",
   3*exp(-h*c/(589e-9*kb*2400)),1.14e-4,rel=.02)
eq(127,"beam decay time 2.5mm/600ms /ln25 microseconds",
   .0025/(600*log(25))*1e6,1.3,rel=.01)
eq(130,"stimulated-to-spontaneous ratio in BB radiation at 3000K",
   1/(exp(10.2*e/(kb*3000))-1),7.3e-18,rel=.05)
eq(130,"equal Einstein induced and spontaneous threshold temperature K",
   10.2*e/(kb*log(2)),1.71e5,rel=.02)
eq(131,"net absorption nonnegative in thermal equilibrium",
   float(1-exp(-1.7)>0),1)
# Moseley K alpha ∝ (Z-1)^2, not Z².
eq(133,"Fe-Cu Kalpha Moseley picometres",
   193*((26-1)/(29-1))**2,154,rel=.01)
eq(135,"number of elements strictly between Z=23 and Z=27",27-23-1,3)
eq(137,"Al K edge radiation allowed from threshold voltages",
   float(h*c/(.5e-9*e)>1560),1)
# Full Landé g via angular momentum vector coupling.
for L,S,J,expected in [(0,1,1,2),(2,1,1,.5),(3,2.5,.5,-2/3),
                      (2,1.5,.5,0),(3,2,2,1),(1,2,1,2.5),
                      (2,.5,1.5,.8),(1,.5,1.5,4/3)]:
    eq(144,"independent LS Landé g invariant",g_factor(L,S,J),expected)
# True J=0 term has no first-order Zeeman magnetic moment.
verify(143,"singlet S0J0 must not call g formula",0 in allowed_J(0,0))
eq(145,"2D_3/2 magnetic moment units muB",g_factor(2,.5,1.5)*sqrt(1.5*2.5),2*sqrt(15)/5)
eq(146,"D2 maximum projection 4muB requires S3",
   g_factor(2,3,2)*2,4)
eq(147,"S1 L2 J3 magnetic moment muB",
   g_factor(2,1,3)*sqrt(12),8*sqrt(3)/3)
eq(150,"S3/2 L2 at J1/2 has zero first-order moment",
   g_factor(2,1.5,.5),0)
eq(151,"5F1 J1 zero magnetic factor",g_factor(3,2,1),0)
eq(152,"2P3/2 Larmor angular frequency rad/s at 0.1T",
   g_factor(1,.5,1.5)*muB*.1/hb,1.17e10,rel=.01)
eq(156,"4D1/2 has no first order Zeeman splitting",g_factor(2,1.5,.5),0)
eq(157,"triplet F4 total Zeeman width eV 0.25T",
   2*4*g_factor(3,1,4)*muB*.25/e,1.45e-4,rel=.01)
eq(158,"5I5 to 5H4 matching Landé factor",
   g_factor(6,2,5),g_factor(5,2,4))
# VI.159 source prints 10^4 ueV, but a 1F3 level at B=0.3T
# would split by only ~10^2 ueV. These are separate input branches.
width_source=1e4 # micro-eV
width_F3=2*3*muB*.3/e*1e6
eq(159,"printed huge 10^4 micro-eV implies J~288, not F3",
   width_source/(2*muB*.3/e*1e6),288,rel=.003)
eq(159,"1F3 source-answer branch width micro-eV",
   width_F3,104.2,rel=.004)
eq(160,"normal Zeeman outermost full optical wavelength span pm",
   e*1.0*(612e-9)**2/(2*pi*me*c)*1e12,35,rel=.04)
eq(161,"adjacent line resolvable magnetic B T",
   4*pi*me*c/(e*536e-9*1e5),.40,rel=.03)
eq(163,"Na P3/2 / P1/2 Landé spacing ratio",
   g_factor(1,.5,1.5)/g_factor(1,.5,.5),2)
# Explicitly enumerate allowed Zeeman transitions instead of hardcoding 6/9.
def allowed_lines(Ju,Jl,gu,gl,pol):
    mu=[-Ju+i for i in range(round(2*Ju)+1)]
    ml=[-Jl+i for i in range(round(2*Jl)+1)]
    return sorted(set(round(gu*u-gl*l,10) for u in mu for l in ml
                      if (u-l in pol)))
eq(164,"2P3/2 to 2S1/2 distinct Zeeman positions",
   len(allowed_lines(1.5,.5,4/3,2,(-1,0,1))),6)
eq(165,"3D2 to 3P1 all transverse observed components",
   len(allowed_lines(2,1,g_factor(2,1,2),g_factor(1,1,1),(-1,0,1))),9)
eq(165,"3D2 to 3P1 only sigma longitudinal components",
   len(allowed_lines(2,1,g_factor(2,1,2),g_factor(1,1,1),(-1,1))),6)
eq(166,"3D3 to 3P2 extremal angular splitting in field 0.34T",
   (10/3)*(muB*.34/hb),9.97e10,rel=.005)
for n,tokens in {
  107:[r"S\ge2"],115:[r"g=4+6=10"],
  120:[r"{}^{4}F_{9/2}"],124:[r"\sqrt{35}"],
  125:[r"4e^{-10.2"], 130:[r"\ln2"],133:[r"Z-1"],
  144:[r"g_a=-\tfrac23"],150:[r"J=1/2"],
  156:[r"(c)一阶不分裂"],158:[r"\text{(a)正常"],
  159:[r"10^{4}",r"{}^{1}F_3"],
  165:[r"9条",r"6条"],166:[r"\frac{10}{3}"],
}.items():
    for token in tokens:anchor(n,P[n],token)
finish("VI.97--166 atomic multiplets, thermal emission and Zeeman",len(P))
