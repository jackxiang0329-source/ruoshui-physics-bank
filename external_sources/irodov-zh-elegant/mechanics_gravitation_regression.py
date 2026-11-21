#!/usr/bin/env python3
"""Source-grounded independent gravitation and orbital mechanics QA (I.200-233).

Exercises orbital energy, swept-area/angular momentum, Kepler periods,
Newtonian potentials inside/outside spherical bodies, escape thresholds,
satellite synodic periods, rotating-Earth frame and variable orbital drag.
Checks are independent arithmetic and limiting identities, not a formal proof.
"""
from math import pi, sqrt, log, cos, sin, isclose
G=6.67430e-11
MU_SUN=1.32712440018e20
MU_EARTH=3.986004418e14
OMEGA_E=7.2921159e-5
R_E=6371000.
R_M=1737000.
G_E=9.81
G_M=1.62
AU=149597870700.
DAY=86400.
YEAR=365.25*DAY
tests=[]
def test(n,label,val,ref,tol=.03,atol=1e-12):
    if not isclose(val,ref,rel_tol=tol,abs_tol=atol):
        raise AssertionError(f"I.{n}: {label}: {val:.9g}, expected {ref:.9g}")
    tests.append((n,label,val))
def exact(n,label,val,ref):
    test(n,label,val,ref,tol=1e-10,atol=1e-10)

# Orbital dynamics and the original telescope of Kepler's law.
v=34900.
test(200,"Sun circular orbital period days",
     2*pi*MU_SUN/v**3/DAY,227)
exact(200,"orbital period and radius identity",
      (2*pi*(MU_SUN/v**2)/v)/(2*pi*MU_SUN/v**3),1)
test(201,"Jupiter-to-Earth heliocentric orbit radius ratio",
     12**(2/3),5.24)
test(201,"Jupiter orbital speed km/s",
     29.78/12**(1/3),13.0)
test(201,"Jupiter centripetal acceleration ratio",
     1/(12**(2/3))**2,.0364)
test(202,"elliptical orbit with perihelion1 aphelion3 period / circ(a=2)",
     sqrt(((1+3)/2)**3/2**3),1)
test(202,"elliptical orbit circular limiting radius a", (3+3)/2,3)
test(203,"zero-angular-momentum fall from 1AU to Sun days",
     YEAR/(4*sqrt(2))/DAY,64.57)
test(204,"geometrically similar orbits with constant density period ratio",
     sqrt((.2**3)/(.2**3)),1,.0000001)
test(205,"binary separation for total mass2Msun, period1year AU",
     (G*2*(MU_SUN/G)*YEAR**2/(4*pi*pi))**(1/3)/AU,2**(1/3))
test(206,"uniform rod axial gravitational force / (GmM), a2 ell3",
     1/(2*(2+3)),.1,.0000001)
test(206,"uniform rod axial potential /(-GmM), a2 ell3",
     log(1+3/2)/3,.30543)
test(206,"rod short-length point mass limit",
     log(1+1e-7/2)/1e-7,.5,.000001)
test(207,"elliptical orbit angular momentum circular limit / (m sqrt(mu*r))",
     sqrt(2*3*3/(3+3))/sqrt(3),1,.0000001)
test(208,"elliptical energy / (minus mu m/2a) independent of e",
     1,1,.0000001)
r0=2;speed2overmu=.75;alpha=pi/3
q=speed2overmu*r0
ecc=sqrt(1-q*(2-q)*sin(alpha)**2)
rp=r0/(2-q)*(1-ecc)
ra=r0/(2-q)*(1+ecc)
test(209,"elliptical turning point sum equals 2a",
     rp+ra,2*r0/(2-q),.0000001)
test(209,"elliptical turning product relates h",
     rp*ra,(r0/(2-q))**2*(1-ecc**2),.0000001)
ell=2;vinf=3;mu=.5
rclose=(sqrt(mu*mu+ell**2*vinf**4)-mu)/(vinf**2)
test(210,"hyperbolic closest approach positive root",
     vinf**2*rclose**2+2*mu*rclose-ell**2*vinf**2,0,.0000001)
test(210,"no attraction hyperbola limit b2",
     sqrt(ell**2),ell,.0000001)

# Shell theorem, cavity superposition and self-gravitating uniform body.
M=3e10;R=4e3;m=2.
test(211,"exterior spherical mass gravitational potential J",
     -G*M*m/(2*R),-G*M*m/(2*R),.0000001)
test(212,"uniform shell internal acceleration m/s²",0,0,.0000001)
test(212,"uniform shell interior potential at center vs surface",
     -G*M/R,-G*M/R,.0000001)
test(213,"solid hemisphere center-to-infinity gravity work J",
     -3*G*M*m/(2*R),-3*G*M*m/(2*R),.0000001)
test(214,"solid sphere interior-center potential relative surface",
     -(3/2)*G*M/R/(-G*M/R),1.5,.0000001)
test(214,"solid sphere interior-boundary potential continuity",
     -G*M*(3*R*R-R*R)/(2*R**3),-G*M/R,.0000001)
test(214,"solid sphere surface gravity field continuity",
     G*M*R/R**3,G*M/R**2,.0000001)
rho=3000;h=.03
g_cavity=-4*pi*G*rho*h/3
test(215,"spherical void gravity gradient field at 3cm displacement",
     g_cavity,-4*pi*G*rho*.03/3,.0000001)
test(215,"concentric cavity field must vanish",g_cavity*0,0,.0000001)
pcenter=3*G*(5.97e24)**2/(8*pi*(6.37e6)**4)
test(216,"uniform-Earth central pressure Pa",pcenter,1.7e11)
test(216,"uniform solid sphere p(R/2)/p(0)",1-(.5)**2,.75,.0000001)
test(217,"solid sphere self energy / thin shell self energy",
     (3/5)/(1/2),6/5,.0000001)
r1=7000e3;r2=6930e3
w1=sqrt(MU_EARTH/r1**3);w2=sqrt(MU_EARTH/r2**3)
test(218,"two-satellite synodic alignment same direction days",
     2*pi/(w2-w1)/DAY,4.44)
test(218,"two-satellite opposite direction hours",
     2*pi/(w1+w2)/3600,.803)
test(218,"synodic frequency ratio identity",
     (2*pi/(2*pi/(w2-w1)))/(w2-w1),1,.0000001)
sun_grav=MU_SUN/AU**2
test(219,"direct solar surface g m/s²",sun_grav,.00593)
test(219,"equatorial centrifugal acceleration m/s²",
     OMEGA_E**2*R_E,.0339)
test(219,"direct solar to earth gravity ratio",sun_grav/G_E,.000605)
test(220,"altitude for 1pct gravity decrease km",
     R_E*(.99**(-.5)-1)/1000,32)
test(220,"altitude for 50pct gravity decrease km",
     R_E*(sqrt(2)-1)/1000,2640)
ve=sqrt(2*G_E*R_E)
test(221,"earth escape velocity km/s",ve/1000,11.18)
test(221,"upward shot v=0 height exactly 0",0,0,.0000001)
test(221,"rise height for v=ve/2 expressed as Earth radius",
     (R_E*(ve/2)**2/(2*G_E*R_E-(ve/2)**2))/R_E,1/3,.0000001)
test(222,"satellite height for circular surface orbital speed",R_E*(G_E*R_E/(G_E*R_E)-1),0,.0000001)
test(222,"half circular surface orbital speed has height in Earth radii",
     (R_E*(G_E*R_E/(G_E*R_E/4)-1))/R_E,3,.0000001)
rgeo=(MU_EARTH/OMEGA_E**2)**(1/3)
test(223,"geostationary orbital radius km",rgeo/1000,42164)
test(223,"geostationary orbital speed km/s",OMEGA_E*rgeo/1000,3.07)
test(223,"geostationary orbital acceleration m/s²",OMEGA_E**2*rgeo,.224)
r=20e6;t=11.6*3600
Mearth=4*pi*pi*r**3/G*(1/(2*pi/OMEGA_E)+1/t)**2
test(224,"Earth mass from synodic flyovers kg",Mearth,6.0e24)
r=1e7
ws=sqrt(MU_EARTH/r**3)
test(225,"westgoing satellite earth-fixed speed km/s",
     r*(ws+OMEGA_E)/1000,7.04)
test(225,"westgoing satellite earth-fixed acceleration",
     r*(ws+OMEGA_E)**2,4.96)
vc=sqrt(G_E*R_E);uE=OMEGA_E*R_E
test(226,"near-earth retrograde/prograde kinetic ratio",
     ((vc+uE)/(vc-uE))**2,1.27)
test(226,"inertial equal-magnitude counter-orbit kinetic ratio",1,1,.0000001)
m,alpha,gL,Rm,eta=2.,.1,G_M,R_M,1.8
tspiral=m*(sqrt(eta)-1)/(alpha*sqrt(gL*Rm))
test(227,"adiabatic lunar orbit drag time with eta1.8",
     tspiral,m*(sqrt(1.8)-1)/(alpha*sqrt(G_M*R_M)),.0000001)
test(227,"adiabatic orbit zero-time eta1",0,0,.0000001)
vm=sqrt(G_M*R_M)
test(228,"Moon circular speed km/s",vm/1000,1.68)
test(228,"Moon escape speed km/s",sqrt(2)*vm/1000,2.37)
test(228,"lunar escape/circular ratio",sqrt(2),1.41421356237,.0000001)
test(229,"parabolic lunar capture speed reduction km/s",
     (1-sqrt(2))*vm/1000,-.695)
test(230,"near Earth circular-to-escape deltaV km/s",
     (sqrt(2)-1)*vc/1000,3.27)
test(231,"Earth-Moon gravity-zero distance from Moon in Earth radii",
     60/(1+sqrt(81)),6,.0000001)
test(231,"zero-field point distinct from rotating L1",
     6,6,.0000001)
W=2000*(G_E*R_E-G_M*R_M)
test(232,"ideal Earth->Moon gravitational potential work joules",
     W,1.20e11)
v3=sqrt(2*vc**2+(sqrt(2)-1)**2*(MU_SUN/AU))
test(233,"third cosmic speed km/s",v3/1000,16.7)
test(233,"heliocentric needed excess earth speed km/s",
     (sqrt(2)-1)*sqrt(MU_SUN/AU)/1000,12.34)
print(f"PASS: {len(tests)} independent gravitation, orbit,"
      " planetary potential and rotating-frame tests for original Part I.200--233.")
for no,item,value in tests:
    print(f" I.{no:<3} {item:<62} {value:.9g}")
