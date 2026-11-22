#!/usr/bin/env python3
"""Strict structural QC for the Zhang Sanhui textbook candidate intake.

Does NOT certify physics correctness, copyright, original figures, or expert review.
Run from any working directory: python external_sources/zhang_sanhui_4e/qa_check.py
"""
from __future__ import annotations

import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REGISTER = ROOT / "source_register.json"
SECTIONS = re.compile(r"\\paragraph\{习题\s+(\d+\.\d+)\}")
CANDIDATE_STATUS = "pending_independent_verification"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def check_latex_fragment(path: Path, name: str) -> list[str]:
    require(path.is_file(), f"missing {name}: {path}")
    text = path.read_text(encoding="utf-8")
    require(r"\documentclass" not in text, f"must be input fragment: {path}")
    for op, cl in [(r"\(", r"\)"), (r"\[", r"\]"),
                   (r"\begin{enumerate}", r"\end{enumerate}")]:
        require(text.count(op) == text.count(cl),
                f"unbalanced TeX delimiter {op}/{cl} in {path}")
    ids = SECTIONS.findall(text)
    require(ids, f"no problem sections: {path}")
    require(len(ids) == len(set(ids)), f"duplicate IDs in {path}")
    return ids


def check_numeric_spotmodels() -> int:
    """Independent reference computations, NOT a full automated physics proof."""
    g = 9.80
    close = lambda a, b, rel=0.001: math.isclose(a, b, rel_tol=rel)

    # 1.11: ballistic bridge landing height
    v = 150 / 3.6
    t = 57 / (v * math.cos(math.radians(5)))
    require(close(v * math.sin(math.radians(5)) * t - .5 * g*t*t,
                  -4.253313229, rel=.002), "1.11 projectile check")
    # 1.12: collision above lower cannon level
    require(close(.5 * math.sqrt(g*(200**2 + 50**2)/50), 45.63441684),
            "1.12 meeting threshold")
    # 1.18: CD radial scan and spin-down
    N, r, v, r1, r2 = 650000, .05, 1.3, .022, .056
    require(close(math.pi*N*(r2*r2-r1*r1)/v/60, 69.42919764),
            "1.18 timing")
    require(close(-v**3/(2*math.pi*N*r**3), -.00430354966),
            "1.18 angular acceleration")
    # 1.23: EAST by SOUTH, not SOUTH by EAST
    require(close(math.hypot(800*math.cos(math.pi/6),
                             1000-800*math.sin(math.pi/6)),
                  916.51513899), "1.23 relative aircraft speed")
    # 2.2: explicit 30 degree angle must survive scan transcription
    m, a, theta = .50, 2.0, math.pi/6
    require(close(m*(g*math.sin(theta)+a*math.cos(theta)),3.3160254),
            "2.2 tension")
    require(close(m*(g*math.cos(theta)-a*math.sin(theta)),3.74352448),
            "2.2 support force")
    # 2.5: double rope
    m1, m2, m3 = .200, .100, .050
    t2 = 4*g/(4/m1 + 1/m2 + 1/m3)
    require(close(t2,.784), "2.5 pulley tension")
    # 2.6: downward incline 1:10
    mu = (25**2/(2*35))/g
    theta = math.atan(.1)
    decel = g*(mu*math.cos(theta)-math.sin(theta))
    require(close(25**2/(2*decel),39.51132804), "2.6 downhill stop")
    # 2.7: board relative slip threshold
    require(close(2*.25*(1.5+2.45)*g,19.355), "2.7 slip threshold")
    # 2.11: friction on banked road
    a = 25**2/400
    require(close(1200*(a*math.cos(math.radians(6))
                         -g*math.sin(math.radians(6))),
                  635.47382579), "2.11 bank friction")
    # 2.12: radius must be in metres, not km
    M = 4*math.pi**2*(1.07e9)**3/(6.6743e-11*(7.16*86400)**2)
    require(close(M,1.89344117254e27), "2.12 Jupiter mass")

    # Chapter 2 second half: independently reproduce raw model values,
    # testing units, area conversion and asymptotic limits.
    G = 6.6743e-11
    # 2.13 Saturn: orbital radius given from planetary centre
    saturn_mass = 4*math.pi**2*(1.36e8)**3/(G*(14.2*3600)**2)
    require(close(saturn_mass, 5.69362746616e26), "2.13 Saturn mass")
    # 2.14 break-up period and stellar minimum mass
    period = math.sqrt(3*math.pi/(G*3e3))
    require(close(period/3600, 1.90576599623), "2.14 minimum spin period")
    star_min_mass = 4*math.pi**2*(1e4)**3/(G*.0016**2)
    require(close(star_min_mass, 2.31054295982e29), "2.14 neutron star bound")
    # 2.15 pressure should have Pascal dimensions; compare barometric factor
    pressure = (2*math.pi/3)*G*1300**2*(7e7)**2
    require(close(pressure/1.013e5, 1.14271433782e7), "2.15 pressure in atm")
    # 2.19 test angular rotation rate and liquid force independently
    omega = 2*math.pi*(5e4/60)
    bottom_force = .5*.012*omega**2*(.020+.100)
    require(close(bottom_force, 19739.20880218), "2.19 sample end pressure force")
    # 2.20 total wing mass cancels
    omega2 = 2*math.pi*400/60
    require(close(omega2**2*5.97/(2*g), 534.43572131),
            "2.20 blade root load over weight")
    # 2.23 truck frame relative speed
    require(close(math.sqrt(2*(7-.5*g)*2), 2.898275349),
            "2.23 truck-relative collision speed")
    # 2.24 space station artificial gravity
    require(close(math.sqrt(g/1800), .0737864787373),
            "2.24 rotating station angular rate")
    # 2.26 drag and input power
    drag = .5*.016*.062*math.pi*25**2*40**2
    require(close(drag, 1558.22995618), "2.26 airship drag")
    require(close(drag/.010, 155822.995618), "2.26 propulsion power")

    # Zhang Sanhui chapters 3 and 12: independently computed numerical invariants.
    eps = 8.8541878128e-12
    electron_q = 1.602176634e-19
    k = 1/(4*math.pi*eps)
    # 3.3 impact impulse with gravity included
    require(close(150*(g+math.sqrt(2*g*5)/.30), 6419.747468305833),
            "3.3 water impact force")
    # 3.5 full momentum stoppage, no unwarranted factor 1/2
    require(close(1.29*22.5*2.62*38**2, 109809.702),
            "3.5 wind momentum force")
    # 3.9 orthogonal vectors, not arithmetic sum
    require(close(math.hypot(9.22, 5.33)*1e-21,
                  1.0649755865746405e-20), "3.9 nucleus recoil")
    # 3.14 source clearly gives 1.29e3 kg/s (NOT 1.29e4)
    m0, rate, burn, u = 2.72e6, 1.29e3, 155, 5.5e4
    mf = m0-rate*burn
    require(close(mf, 2520050.0), "3.14 source mass-flow verification")
    require(close(m0*g/rate, 20663.56589147287), "3.14 liftoff threshold")
    require(close(u*math.log(m0/mf)-g*burn, 2680.4225741362498),
            "3.14 burnout speed")
    require(close(u*(burn-mf/rate*math.log(m0/mf))-.5*g*burn**2,
                  203591.5636030566), "3.14 burnout height")
    # 3.14: independent midpoint quadrature validates the analytic height,
    # and explicitly differs from the companion book's printed 172 km.
    n_int = 10000
    delta_t = burn/n_int
    h_mid = sum(
        (u*math.log(m0/(m0-rate*(i+0.5)*delta_t))
         -g*(i+0.5)*delta_t)*delta_t
        for i in range(n_int)
    )
    require(close(h_mid,203591.5636030566,rel=.00001),
            "3.14 independent midpoint quadrature")
    require(abs(h_mid-172000)>30000,
            "3.14 must preserve printed 172km vs independent integration discrepancy")
    # 3.15 jet engine mass flow and ram ingestion
    require(close(78*490 - 75*210, 22470), "3.15 air-breathing thrust")
    # 3.18 cube with removed cylindrical tunnel
    require(close((.5-math.pi/64)/(1-math.pi/16),.5610805166019814),
            "3.18 cavity centroid under figure tangency")
    # 3.20 comet aphelion, angular momentum conservation
    require(close(8.75e10*5.46e4/(9.08e2),5261563876651.982),
            "3.20 Halley aphelion")
    # 3.22 transfer ellipse area and peri/apo angular momenta
    rp,ra=(6371+205.5)*1000,(6371+35835.7)*1000
    require(close(rp/ra*10200,1589.328234616779),"3.22 apogee speed")
    require(close(2*math.pi*((rp+ra)/2)*math.sqrt(rp*ra)/(rp*10200),
                  38063.89901380998),"3.22 transfer period")
    # 12.4 quark electric repulsion
    require(close(k*2*electron_q**2/(9*(1e-15)**2),
                  51.26839005203858),"12.4 pion charge force")
    # 12.5 original measurement error is 10^-21 * e, NOT 10^-21 C
    require(close(k*(24e-21*electron_q)**2/
                  (6.6743e-11*(16*1.66054e-27)**2),
                  2.82059222767429e-6),"12.5 electrostatic/gravity bound")
    # 12.11 broken charged circle
    require(close(k*(3.12e-9/(2*math.pi*.5-.02))/.5*
                  2*math.sin(.02/(2*.5)),0.7185893953517627),
            "12.11 gap-center field")
    require(close(eps*120/electron_q,6631619229.668532),
            "12.15 excess electrons per square metre")
    require(close(eps*.25/electron_q,13815873.395142775),
            "12.16 electron deficit per cubic metre")
    # 12.23 hydrogen electron cloud PLUS central proton
    require(close(k*electron_q*5*math.exp(-2)/(.53e-10)**2,
                  346881470154.7788),"12.23 hydrogen field with nucleus")
    # 12.24 exponential proton distribution
    x=1/.23
    require(close(k*electron_q/(1e-15)**2*
                  (1-math.exp(-x)*(1+x+x*x/2)),
                  1.1643097581697867e21),"12.24 proton field")
    # 12.26 uniform positive uranium sphere, radius 7.4 fm
    require(close(math.sqrt(k*92*electron_q**2*(2.9e-15)**2/
                  (3.17e-27*(7.4e-15)**3)),
                  11788153.91384249),"12.26 tau orbit speed")
    # 12.27 polarizability model
    require(close(4*math.pi*eps*(.53e-10)**3*(3e6)/electron_q,
                  3.101680528657228e-16),"12.27 cloud displacement")
    require(close(eps*800*.1**2.5,2.2399520255482056e-11),
            "12.29 cube's enclosed charge")
    require(close(.5*(1.4e-13*1.6e6/(1.5e-10))*(.016/20)**2,
                  .0004778666666666667),"12.34 inkjet deflection")


    # Chapter 4 independently computed mechanical-energy references.
    require(close(((1200-1000)*g+(1200+1000)*1.5)*.75,
                  3945.0), "4.1 motor energy during first 1s")
    require(close(.5*132000*(942/3.6)**2,
                  4518983333.333334), "4.3 aircraft kinetic energy")
    require(close(50*1.5**2, 112.5), "4.4 belt motor power")
    require(close(math.sqrt((1-.2)*g*1), 2.8), "4.5 pulley work balance")
    m,k_s,L=72,60,20
    x=(m*g+math.sqrt((m*g)**2+2*k_s*m*g*L))/k_s
    require(close(x, 36.43179766453997), "4.10 maximum bungee stretch")
    x_crit=m*g/k_s
    require(close(math.sqrt(2*g*(L+x_crit)-(k_s/m)*x_crit**2),
                  22.52216685845303), "4.10 maximum speed")
    require(close(.3*g/math.sqrt(8.9*.5),1.3936936616315332),
            "4.12 released spring mass")
    GM=3.986004e14
    r1,r2=6.37e6+1.4e6,6.37e6+3.6e7
    a_transfer=(r1+r2)/2
    require(close(GM*500*(1/(2*r1)-1/(2*a_transfer)),
                  8850106343.165777), "4.18 Hohmann work first burn")
    require(close(math.sqrt(GM*(2/r1-1/a_transfer))-math.sqrt(GM/r1),
                  2148.905731636786), "4.18 Hohmann first delta-v")
    require(close(math.sqrt(G*1e30*(1/40000-1/1e10)),
                  40848112.878075525),"4.19 neutron star contact speed")
    asteroid_mass=(4/3)*math.pi*(1e4)**3*6000
    require(close(GM*asteroid_mass/6.37e6,
                  1.5726720104966442e24),"4.20 asteroid gravity energy")
    sun_mass=1.989e30
    c_light=299792458.0
    require(close(2*G*sun_mass/c_light**2,
                  2954.126555055405),"4.21 solar black hole radius")
    require(close(2*sun_mass*(2e10/1e67)**(1/3),
                  501196593648.1817),"4.22 micro black hole mass")
    require(close(3600*math.pi*.2**2*math.sqrt(2*g*5),
                  4478.4260016636335),"4.27 ideal siphon volume")
    require(close(60*math.pi*.004**2*
                  math.sqrt(2*20*101325/1000)*1000,
                  192.00361589622767),"4.28 nozzle L per min, absolute pressure")

    # Chapter 13 independent electric-potential and energy references.
    ke=1/(4*math.pi*eps)
    require(close(ke*(1e-8/.2+1.5e-8/.3),
                  898.7551792261171),"13.1 potential at 20 cm")
    require(close(ke*2.5e-8/.5,
                  449.37758961305855),"13.1 potential at 50 cm")
    require(close(ke*2e-7*math.log(4),
                  2491.8784739769253),"13.6 axial rod potential")
    require(close(2*ke*2e-7*math.asinh(1.5),
                  4295.198517942593),"13.6 bisector rod potential")
    require(close(1e3/(6.35e-6*math.log(.01/6.35e-6)),
                  21391301.68446818),"13.8 thin wire field")
    require(close(ke*1.6e-12/.0004,
                  35.95020716904468),"13.12 droplet potential")
    require(close(ke*79*electron_q/7e-15,
                  16251028.46850897),"13.13 Au nucleus surface potential")
    electron_mass=9.1093837e-31
    require(close(math.sqrt(2*electron_q*2.5e4/electron_mass),
                  93776863.112971),"13.19 classical electron beam speed")
    require(close((-1e-5*.05+3e-5*.07)/(2*eps),
                  90352.72538984154),"13.21 infinite planes potential")
    require(close(math.sqrt(5)/3,
                  .7453559924999299),"13.23 relativistic beta")
    require(close(-3.5*ke*electron_q/(.20e-10),
                  -251.99379587244925),"13.24 He electronic energy eV")
    require(close(12*ke*electron_q/(3e-15)/1e6,
                  5.759858191370268),"13.25 alpha cluster MeV")
    require(close(ke*electron_q**2/(2*electron_mass*c_light**2),
                  1.408970163334473e-15),"13.27 shell classical radius")
    initial_U=3*ke*(92*electron_q)**2/(5*7.4e-15)
    require(close(initial_U*(1-2**(-2/3))/(electron_q*1e6),
                  365.674807426954),"13.29 symmetric Pd fission energy")
    require(close(math.sqrt(3*ke*92*electron_q**2/(3.17e-27*7.4e-15)),
                  52100290.74000226),"13.31 tau particle nuclear-center speed")
    require(close(eps*100**2/2*(4*math.pi*(6.37e6)**2*1e4)/3.6e6,
                  62705.40282625374),"13.33 atmospheric field kWh")
    hbar=1.054571817e-34
    require(close(-electron_mass*electron_q**4/
                  (2*(4*math.pi*eps)**2*hbar**2)/electron_q,
                  -13.605693137318392),"13.34 Bohr energy in eV")


    # Chapter 5: independent original-data numerical regression checks.
    require(close(25**2/(2*1.25*2*math.pi),39.78873577),
            "5.1 angular acceleration under start-from-rest model")
    require(close(((200+3000)/2)*7/60, 186.6666667),
            "5.2 revolutions over 7 s")
    JA,JB,mH=1.93e-47,1.14e-47,1.6735575e-27
    require(close(math.sqrt((JA+JB)/(2*mH)),9.57709666e-11),
            "5.5 OH bond distance")
    require(close(2*math.degrees(math.atan(math.sqrt(JA/JB))),
                  104.9116327),
            "5.5 theta is full HOH angle, not half-angle")
    mC=720*1.6605390666e-27
    I_C60=(1/6)*mC*(71e-9)**2
    require(close(I_C60,1.004493292e-39),
            "5.6 preserve 71nm printed diameter, flag anomaly separately")
    require(close(math.sqrt(2*6.21e-21/I_C60)/(2*math.pi),
                  5.59638274759e8),"5.6 frequency using TEXTBOOK 6.21e-21J")
    require(close(.1*g/(1/12+.1**2),10.5),"5.12 pivot acceleration")
    I_rod=1*.4**2/3+.008*.3**2
    require(close(.008*200*.3/I_rod,8.8801184),
            "5.16 bullet-rod angular velocity")
    require(close(480000-0.5*2500*4.8**2,451200),
            "5.18 two-car kinetic energy loss")
    require(close(.033/(2*1.26e-5),1309.5238095),
            "5.21 stopping year with constant energy-loss POWER")
    require(close(7.834069878e19/7.3e18,10.73160257),
            "5.22 annual tide loss / companion stated 2004 joules")
    require(close(2000*(1-.6)/(300+1000),.61538461538),
            "5.25 reel rolling acceleration")
    require(close(5*g,49.0),"5.26 yo-yo hand acceleration at 2mg pull")
    require(close(0.5*1e5*(800*2*math.pi/60)**2/7.46e4,
                  4704.01163),"5.28 gyroscope spin-up time")
    # Chapter 14: independent electrostatics model checks.
    kC=1/(4*math.pi*eps)
    QA,QB=3e-8,2e-8
    R1,R2,R3=.06,.08,.10
    require(close(kC*(QA*(1/R1-1/R2)+(QA+QB)/R3),
                  5617.72099),"14.3 initial metal sphere potential")
    Q_A2=QA/R3/(1/R1-1/R2+1/R3)
    require(close(Q_A2,2.1176470588e-8),
            "14.3 sequential grounding metal sphere final charge")
    require(close(1.3e-5*.03/.08,4.875e-6),
            "14.5 three parallel conductor inner-face sigma")
    require(close(9.15e6/1e8,.0915),
            "14.8 minimum conducting sphere radius")
    sigma_belt=320e-6/(.485*33)
    require(close(sigma_belt/(2*eps),1.129e6),
            "14.8 INSULATING belt field sigma/(2 eps)")
    require(close(math.sqrt(3)*2.5,4.330127019),
            "14.11 horizontal field line terminates at sqrt(3) h")
    require(close(1e-8/(math.pi*eps*5),71.91),
            "14.12 field directly below charged line")
    require(close((10*(.05/18)*6.02214076e23*electron_q)/
                  (4*math.pi*eps*6.37e6),3.781470956e6),
            "14.13 0.05g water-drop model is millions of volts")
    require(close((1/(32*math.pi*eps)),
                  (1/(4*math.pi*eps))/8),
            "14.14 conducting sphere mutual-hemisphere force coefficient")


    # Chapter 6 new independent oscillation spot computations.
    require(close(.05*8*math.pi,1.25663706144),"6.1 v_max")
    require(close(2*math.pi/(5*math.pi/6),2.4),"6.3 diagram-derived period")
    require(close(2*math.pi/1.5,4.18879020479),"6.4 sine oscillator period")
    require(close(math.sqrt(1.6/25),.252982212813),"6.8 total energy and amplitude")
    require(close(math.sqrt(1000/.025)/(2*math.pi),31.8309886184),
            "6.13 two-ball reduced-mass vibration frequency")
    require(close(.5*g/(4*math.pi)**2,.0310296124905),
            "6.15 maximum horizontal table amplitude")
    require(close(math.sqrt(g/.05)/(2*math.pi),2.22816920329),
            "6.15 vertical contact frequency threshold")
    require(close(2*math.pi*math.sqrt(.2/(2*.5*g)),.897597901026),
            "6.16 board on counterrotating rollers")
    require(close(2*math.pi*math.sqrt((.121/(13600*.3e-4))/(2*g)),
                  .772884212718),"6.17 mercury U tube")
    HCL_r0=1.3e-10
    kp=8*k*electron_q**2/HCL_r0**3
    mp=1.67262192369e-27
    omega_HCL=math.sqrt(kp/mp)
    require(close(omega_HCL/(2*math.pi),1.1279303975519956e14),
            "6.21 HCl small-oscillation frequency")
    require(close(math.sqrt(3*1.054571817e-34/(mp*omega_HCL)),
                  1.6336865389623234e-11),
            "6.21 HCl companion n=1 uses 3/2 hν, NOT 1/2 hν")
    beta=math.log(5/4)/100
    require(close(beta,.002231435513142098),
            "6.22 exponential damping coefficient")
    require(close(math.log(2)/beta,310.628371951),
            "6.22 4deg to 2deg damping elapsed time")
    require(close(math.sqrt(g)/(2*beta),701.453201328),
            "6.22 pendulum quality factor")
    require(close(math.sqrt((.07*math.cos(math.pi/6))**2+
                   (.01*math.sin(math.pi/6))**2),
                  .060827625303),"6.24 two-phasor resultant amplitude")
    require(close(5*math.pi/(4*314),.0125063401815),
            "6.25 first POSITIVE displaced crossing")
    require(close(2.70e4*2/3,1.80e4),"6.27 Lissajous 3:2 hypothesis")

    # Chapter 15 new independent dielectric, capacitor and bound-charge checks.
    require(close(electron_q*.128e-9,2.05078609152e-29),
            "15.1 fully ionic HCl moment")
    require(close((.128e-9-3.4e-30/electron_q)/18,
                  5.93215939705e-12),"15.1 centroid of ALL eighteen electrons")
    U152=-6e-8*k*((1/6)*(1/.02-1/.04)+(1/3)*(1/.04-1/.06))
    require(close(U152,-3744.81324677549),
            "15.2 TWO spherical dielectric layers voltage")
    require(close(2*math.pi*eps*.01*3e6,1.66897508317e-6),
            "15.5 maximum air line charge for 1cm radius")
    require(close(.52e-3/(eps*6),9788211.91723),
            "15.6 cell membrane field with eps_r=6")
    require(close(.6e-3-eps*50e-6/(eps*50e-6/.6e-3+.25e-12),
                  .000151845071837),
            "15.8 keyboard capacitor pressed distance")
    require(close(3e-6*5e-5/(eps*2.3),7.36571130895),
            "15.9 polyethylene film area")
    require(close(eps*3e6/5e4,5.31251268768e-10),
            "15.10 max plate capacitance per square metre")
    require(close(4*math.pi*eps*.18,2.00277009981e-11),
            "15.11 Van de Graaff isolated sphere capacitance")
    require(close(2*math.pi*eps*.1/math.log(1000),
                  8.05362965617e-13),"15.12 coaxial counter capacitance")
    require(close(eps*.02*(1/.0005+1/(2*.00025)),
                  7.08335025024e-10),
            "15.14 floating three-conductor metal box capacitance")
    require(close(1.5/.7,2.142857142857143),
            "15.16 dielectric insertion voltage ratio")
    require(close(200+800/12,266.666666667),
            "15.18 series 12uF with parallel pair breakdown limit")
    require(close(100e-12*(100/30-1),
                  2.33333333333e-10),"15.23 second parallel capacitor")
    require(close(math.pi*eps*5000**2/math.log(.07/.05),
                  .0020667568047755),"15.25 coaxial cylinder initial force")
    require(close(3/math.log(4),2.16404256133),
            "15.28 dielectric graded profile effective capacitance coefficient")
    require(close(2e-6/(1+3),5.0e-7),
            "15.29 top half of half-immersed charged metal sphere")
    require(close(-13.6/(15.8**2),-.0544784489665),
            "15.30 hydrogenic dielectric-shielded Bohr binding")


    # Chapter 7: numerical wave, dispersion and signal transport references.
    require(close(740/(300*3600),6.85185185185e-4),"7.1 transoceanic wave frequency")
    require(close(8000/740,10.81081081081),"7.1 8000km propagation hours")
    require(close(4/.8,5.0),"7.2 traveling sine-wave wavenumber")
    require(close(.02*2*math.pi*200/100,.2513274123),
            "7.3 maximum strand speed divided by wave speed")
    require(close(.08/.4,.2),"7.5 illustrated wave frequency")
    require(close(7800*5100**2,2.02878e11),"7.8 steel Young modulus")
    require(close(.5*7900*5100*(2*math.pi*1000)**2*(1e-9)**2,
                  7.95292722640e-4),"7.10 harmonic wave intensity")
    require(close(.5*7900*5100*(2*math.pi*1000)**2*(1e-9)**2*.0015,
                  1.19293908396e-6),"7.10 energy power through track")
    require(close(-15*math.cos(1)*math.sin(1.5),-8.08423262031),
            "7.13 standing wave point velocity")
    require(close(5740/(2*.002),1.435e6),"7.15 quartz thickness resonance")
    require(close(1e-12*10**(115/10),.316227766),"7.16 115 dB intensity")
    require(close(1e-12*10**(141/10),125.8925412),"7.16 141 dB intensity")
    require(close(5.1*60/(1/6-1/8),7344),"7.17 earthquake P/S delay 5.1 minutes (companion p117)")
    require(close(10**((9.2+2.9)/.67),1.14736472208e18),
            "7.18 actual textbook formula M=0.67 lgE-2.9")
    require(close(400*(330-80/3.6)/(330-120/3.6),
                  414.981273408),"7.20 pursuit siren Doppler")
    require(close(1540*220/(2*18000+220),9.353948095),
            "7.22 two-way Doppler dolphin speed")
    require(close(2*.32*4e6/1540,1662.3376623),"7.23 blood cell echo shift")
    require(close(3e8*1.1e4/(2*5e10)*3.6,118.8),"7.24 radar speeding km/h")
    require(close(math.degrees(math.asin(1/2.3)),25.77146174),
            "7.25 sonic boom half angle")
    require(close(5000*math.sqrt(2.3**2-1)/(2.3*330),13.6444764),
            "7.25 supersonic delay")
    require(close((60/3.6)*math.sin(math.radians(5)),
                  1.45259571246),"7.26 source 10deg FULL opening means 5deg half-angle")
    require(close((9.5/4.5),2.111111111),"7.27 carrier phase speed")
    require(close(2*math.pi/(5-4),2*math.pi),
            "7.27 packet lobe width")
    require(close((2.5**2-1)/(2.5**2+1),21/29),
            "7.30 conditional relativistic Doppler speed")
    require(close(math.sqrt(2*g*2)/(2*math.pi),.9965867),
            "7.4 thrown person's 2m HEIGHT not seismic AMPLITUDE")
    require(close(4.2-.4/2,4.0),
            "7.6 NEAREST crest x=-0.4 passed origin at t4.0s")
    require((15-2)%2==1 and (14%2)==0,
            "7.12 anti-phase coherent waves: midpoint cancels, even x enhance")
    require(close(10**((9.2+2.9)/.67)/4.6e15,249.4271135),
            "7.18 TNT 1Mt-equivalent without early one-digit rounding")

    # Chapter 16: independently recomputed current, leakage, cooling and RC quantities.
    require(close(.008*240/(3e8*electron_q),3.9945658e10),
            "16.1 electron storage-ring number")
    require(close(2*eps*1.2e6*.30*.20,1.275003e-6),
            "16.2 insulator belt current")
    require(close(30/((10500/.1079*6.02214076e23)*electron_q*
                    math.pi*(.001/2)**2),.00406819932),
            "16.3 estimated silver drift speed")
    require(close(1.75e-8*2/(.02*.08),2.1875e-5),
            "16.4 bulk copper resistor")
    require(close(.05/(1.75e-8*2/(.02*.08)),2285.7142857),
            "16.4 electric current through copper rod")
    require(close(20*((.020**2)*8.7e-8)/
                 (((.025**2-.020**2)*.01)+((.020**2)*8.7e-8)),
                  3.0932854905e-4),
            "16.5 source IRON PIPE inner diameter2.0 outer2.5cm")
    require(close(5*30/(30+70),1.5),"16.6 uniform wire short circuit")
    require(close(120/(4e-12),3e13),"16.7 fair weather air resistivity")
    require(close(1e12*math.log(.02/.005)/(2*math.pi*1000),
                  2.2063560015e8),"16.8 radial cable insulation leak R")
    require(close(10*200/(2*math.pi)*(1-1/1.3),73.45612758),
            "16.10 earth step potential not safety rating")
    require(close((6-3.96)/.00202,1009.9009901),
            "16.14 transistor emitter bias R_e conditional image")
    require(close(1000e-6*.001,1.0e-6),
            "16.15 elementary RC model units")
    require(close(.001*math.log(1e-4/electron_q),.03406741329),
            "16.15 time until one electron charge in 1uF x 100V")
    require(close(.002*4000,8.0),"16.16 source current bounded charge tau")
    require(close(.002*.5,.001),"16.16 discharge lamp RC time")
    require(close(4000/.5,8000),"16.16 discharge initial current")
    require(close(400*200/(4180*60)*60,19.13875598),
            "16.17 electromagnet minimum cooling liters/min")


    # Chapter 8: source-grounded relativistic physics reference computations.
    cc=299792458.0
    mc=9.1093837139e-31
    mpro=1.67262192369e-27
    require(close(math.sqrt(5)*cc,6.7035631523e8),
            "8.4 proper time 2s vs other-frame3s event distance")
    require(close(math.sqrt(3)/cc,5.77749960e-9),
            "8.5 simultaneity offset for event dx=1m -> dxprime=2m")
    require(close(30*3e8,9.0e9),
            "8.6 spaceship-frame EARTH reflection range, not initial Earth-frame range")
    require(close(90*3e8,2.7e10),
            "8.6 Earth-frame ship range at return signal")
    require(close((5/3)*(-6e8+.8*1.8e17/3e8),-2e8),
            "8.7 supernova event Earth-frame negative time")
    require(close((5/3)*(1.8e17+.8*3e8*(-6e8)),6e16),
            "8.7 supernova x spatial Lorentz event")
    require(close(math.degrees(math.atan2(1.2e17,6e16)),63.43494882),
            "8.7 supernova sky position angle from flight axis")
    require(close(-6e8+math.hypot(1.8e17,1.2e17)/cc,
                  1.21609469e8),"8.8 photon arrives at spaceship after explosion")
    require(close((5/3)*(-6e8+math.hypot(1.8e17,1.2e17)/cc)*1.8,
                  3.64828408e8),"8.8 report back to Earth later than direct light")
    require(close((.6+.8)/(1+.6*.8),35/37),
            "8.9 relativistic approach speed less than light")
    require(close(5*math.sqrt(1-.6**2),4.0),
            "8.9 time until collision measured on ship")
    phi=(1+math.sqrt(5))/2
    require(close(math.sqrt(1-1/phi**2),.7861513778),
            "8.13 kinetic energy doubling differs from momentum doubling")
    gam8=1+2.8e9*electron_q/(mc*cc**2)
    require(close(cc/(gam8**2*(1+math.sqrt(1-1/gam8**2))),
                  4.99063907),"8.14 stable electron c minus v at 2.8GeV")
    pp8=math.sqrt((2.8e9*electron_q)*
                  (2.8e9*electron_q+2*mc*cc**2))/cc
    require(close(pp8/(electron_q*(240/(2*math.pi))),
                  .2445598724),"8.14 storage ring B field")
    gamma_p=1+50/(mpro*cc**2)
    require(close(cc/(gamma_p**2*(1+math.sqrt(1-1/gamma_p**2))),
                  1.35496813e-15),"8.15 ultra-high proton speed deficit")
    require(close((1.67265+1.67495-3.34365)*1e-27*cc**2/
                  (electron_q*1e6),2.21578750),
            "8.16 deuteron binding MeV")
    massdef=(4*1.6726-6.6425-2*.0009)*1e-27
    require(close(massdef*cc**2/electron_q/1e6,25.86020346),
            "8.17 simplified solar reaction release MeV")
    require(close(massdef/(4*1.6726e-27),.00689046993),
            "8.17 simplified fusion energy fraction")
    require(close(3.9e26/((massdef/(4*1.6726e-27))*cc**2),
                  6.29758966e11),"8.17 solar proton consumption kg per second")
    require(close(G*1.989e30/(1e4*cc**2),.1477063278),
            "8.18 neutron star Newtonian potential rest-energy fraction")
    require(close((.5+.5)/(1+.5*.5),.8),
            "8.19 two opposite 0.5c protons relative speed")
    ep=mpro*cc**2/electron_q/1e9
    ee=mc*cc**2/electron_q/1e9
    require(close(math.sqrt(ep**2+ee**2+2*ep*(22+ee)),
                  6.4934802351),"8.20 SOURCE available energy total CM not excess")
    Ec=2*(2.8+ee)
    require(close((Ec**2-2*ee**2)/(2*ee),30696.1950),
            "8.21 fixed electron target needs ~3.07e4 GeV")
    require(close(ep*1e18,9.38272088e17),
            "8.23 BOTH protons boosted energy scale squared mass model")
    # Chapter 17: independent current, field, flux and geometry reference checks.
    mu=4*math.pi*1e-7
    require(close((math.pi+2)/(4*math.pi),.4091549431),
            "17.1(b) semicircle plus two half-infinite leads coefficient")
    require(close(9/(2*math.pi),1.4323944878),
            "17.1(c) three equal triangle side field coefficient")
    require(close(mu*1800/(2*math.pi*25),1.44e-5),
            "17.2 HV overhead line ground magnetic field")
    require(close(math.degrees(math.atan(5/18)),15.524111),
            "17.3 compass perpendicular wire field deflection")
    require(close(math.degrees(math.asin(5/18)),16.127620),
            "17.3 compass maximum freely-oriented horizontal field")
    require(close(mu*20*.25/math.pi*math.log(3),2.197224577e-6),
            "17.5 rectangular flux between antiparallel wires")
    require(close(mu*5000/(2*math.pi*.025),.040),
            "17.7 coax cable B peak at inner rod edge")
    Nt=10000/(2*math.pi*1.0)
    require(close(Nt,1591.54943),"17.12 toroid copper turn MINOR radius")
    require(close(mu*Nt*7.3e4/(2*math.pi*2.0),11.61831085),
            "17.12 tokamak peak B ~11.6T (not ~5.8T)")
    require(close(mu/(4*math.pi),1e-7),
            "17.15 internal radial-axial flux coefficient")
    require(close((4/5)**1.5,.7155417528),
            "17.17 Helmholtz axis centre field coefficient")
    require(close(eps*math.pi*.05**2*1e12,.0695406285),
            "17.19 circular capacitor displacement current")
    require(close(mu*eps*.05*1e12/2,2.78162514e-7),
            "17.19 plate-edge Ampere Maxwell B field")
    require(close(2*math.pi*50*1e-12*1.74e5,5.466371217e-5),
            "17.20 50Hz capacitor displacement current peak")


    # Chapter 9: thermometry, kinetic distribution and gas statistical checks.
    kb=1.380649e-23
    NA=6.02214076e23
    RR=8.314462618
    require(close(6650*373.15/273.16,9084.22719),"9.1 constant volume thermometer")
    require(close(40*math.log(7/5)/math.log(7/6),87.309959),
            "9.2 total time for room to cool to15 Celsius")
    Vr=2*math.pi**2*((.7112-.03)/2)*(.015**2)
    Vp=math.pi*.015**2*.30
    require(close((280.15/270.15)*(1+20*Vp/Vr),3.9444674),
            "9.3 tyre final ABSOLUTE pressure multiplier")
    require(close(.18*.029/(3.2e-6*RR),196.194279),
            "9.4 upper atmosphere temperature from density")
    require(close(.18/(kb*196.194279),6.64512e19),
            "9.4 atmospheric particle count per cubic metre")
    rhoext=101325*.029/(RR*293.15)
    require(close(293.15/(1-4500/(2.1e4*rhoext))-273.15,83.37051),
            "9.5 hot air lift threshold degrees C")
    require(close(101325*1e-18*1e-6/(kb*293.15),25.03476),
            "9.6 extreme vacuum 1cm3 average particles")
    require(close(1e10*kb*1e4,1.380649e-9),
            "9.7 interstellar neutral hydrogen cloud pressure")
    require(close(273-.006*8848,219.912),"9.8 Everest lapse model K")
    require(close(101325*(219.912/273)**(.029*9.8/(.006*RR)),
                  29559.6642),"9.8 variable lapse atmospheric pressure")
    require(close(1/(math.sqrt(2)*math.pi*(3.8e-10)**2*
                     (101325/(kb*273.15))),5.80144e-8),
            "9.11 N2 mean free path at standard condition")
    require(close(1.33e-3/(kb*300.15),3.20944554e17),
            "9.12 molecule density vacuum tube")
    nupper=1.5e-9/.029*NA
    require(close(1/(math.sqrt(2)*math.pi*(3e-10)**2*nupper),
                  80.2875964),"9.13 upper atmosphere molecule free path")
    require(close(2/(3*1),2/3),"9.18 speed distribution normalization coefficient")
    require(close(2*250*310/(250+310),276.785714),
            "9.17 equal-pressure unequal-moles gas mixing")
    require(close(math.sqrt(3*kb*300/1.6e-16),.0088125766),
            "9.21 smoke particle Brownian rms")
    require(close(3*RR*300.15/(6.2e-17*.014**2),
                  6.1609265e23),"9.22 Brownian experimental Avogadro constant")
    require(close((2/3)*(11/6),11/9),
            "9.18 Maxwell-like piecewise mean speed relative v0")
    require(close(RR*293.15*math.log(7160/860)/
                  ((4/3)*math.pi*(.212e-6)**3*206.7*9.8*(90e-6)),
                  7.09934046e23),"9.24 Perrin experiment first-to-fourth layer")
    require(close(NA/3.01e4,2.0007112e19),
            "9.25 saturated vapor molecules per cm3")
    moles=1100/44
    vdw=moles*(RR*1000)*286.15/(20-moles*.0427)-3.64e5*(moles/20)**2
    require(close(vdw,2.57291576e6),
            "9.26 van der Waals 20L CO2 pressure with liter units")
    require(close(moles*(RR*1000)*286.15/20,2.97397935e6),
            "9.26 ideal comparison pressure")
    rhos=101325*.004/(RR*273.15)
    heLam=3*1.89e-5/(rhos*1.2e3)
    require(close(heLam,2.64765015e-7),"9.28 He mean free path viscosity model")
    require(close(math.sqrt(1/(math.sqrt(2)*math.pi*
                   (101325/(kb*273.15))*heLam)),1.77877576e-10),
            "9.28 He effective molecular diameter")
    require(close(kb*300.15/(math.sqrt(2)*math.pi*
                  (3.7e-10)**2*.004),1.70330853),
            "9.29 wall spacing Knudsen gas pressure transition")

    require(close(3*7.23e6*(9.55e-5)**2,.1978123225),
            "9.27 original critical CO2 a from companion scan p153")
    require(close(9.55e-5/3,3.1833333333e-5),
            "9.27 original critical CO2 b from companion scan p153")

    # Chapter 18: magnetic Lorentz forces, Hall effect, field-momentum models.
    echarge=1.602176634e-19
    mel=9.1093837e-31
    mpro=1.6726219e-27
    MU=4*math.pi*1e-7
    cc=299792458
    require(close(.0005*g/(2.5e-8*6e4),3.26666667),
            "18.1 B supports levitating charge against gravity")
    require(close(mel*1e7/(echarge*.05),.001137126),
            "18.2 clockwise electron half circle B")
    require(close(math.pi*.05/1e7,1.5707963e-8),
            "18.2 semicircular flight time")
    vel=math.sqrt(2*(2000*echarge)/mpro)
    require(close(2*math.pi*mpro/(echarge*.1),6.5594474e-7),
            "18.3 proton cyclotron period")
    require(close(mpro*vel*math.sin(math.radians(89))/
                  (echarge*.1),.06461116),"18.3 proton helical radius")
    vTV=math.sqrt(2*echarge*2e4/mel)
    rTV=mel*vTV/(echarge*.5e-4)
    require(close(.2**2/(2*rTV),.00209691),
            "18.4 tube Earth magnetic deflection 2mm")
    require(close(2*math.pi*1.49e-18/(echarge*240),.24346946),
            "18.5 momentum-constrained collider field")
    require(close(1e-16/(echarge*1e8),6.24150907e-6),
            "18.6 magnetar electron micrometre gyroradius")
    mom=echarge*20*3.5
    require(close(math.sqrt((mom*cc)**2+(mpro*cc**2)**2)/
                  echarge/1e9,21.0064369),
            "18.7 relativistic proton TOTAL energy GeV")
    require(close(echarge*1.5/(2*math.pi*3.34e-27),1.14518412e7),
            "18.9 deuteron cyclotron frequency")
    require(close((echarge*1.5*.375)**2/(2*3.34e-27)/
                  echarge/1e6,7.58890270),
            "18.9 maximal extracted deuteron energy MeV")
    require(close(16*32.86/29.20,18.00548),
            "18.10 16O/18O mass spectrometry")
    require(close(200*1.5/(8.4e28*echarge*.001),2.22911e-5),
            "18.11 Hall copper 22.3 microvolts")
    require(close(.001*.3/(echarge*.001*.00655),
                  2.85870645e20),"18.12 Hall carrier density")
    require(close(.00105*2e21*echarge*5e-5/.00125,
                  .01345828),"18.13 N-type silicon Hall B")
    require(close(101325/(1.5*.02),3.3775e6),
            "18.14 conductive liquid pressure gradient J")
    require(close(.0001/(.08*.002),.625),"18.15 blood flow Hall sensor speed")
    require(close(.00878*9.8/(2*5*.1*.1),.86044),
            "18.16 reversed current gives 2 n I l B")
    require(close(200*8*.15**2*4,144),"18.18 square loop maximum torque")
    require(close(3*9.66e-27/(2*echarge*1.2e-15),
                  7.5366222e7),"18.20 neutron quark model speed")
    require(close(2*.928e-23/(echarge*cc),3.8640868e-13),
            "18.21 classical spin loop contradicts small electron size")
    require(close(MU*30**2/(2*math.pi*.05),.0036),
            "18.25 parallel 30A wires force per unit length")
    accel=4200**2/(2*5)
    require(close(accel/9.8,180000),"18.27 rail gun acceleration times g")
    force=.317*accel
    loggeom=math.log((.012+.067)/.067)
    Igun=math.sqrt(2*math.pi*force/(MU*loggeom))
    require(close(Igun,4.1194982e6),"18.27 original rail-gun magnet current ~4.12MA")
    require(close((.5*.317*4200**2)/(.4*(2*5/4200))/1000,
                  2.935737e6),"18.27 railgun average electrical power kW")
    require(close(-2*2.39e-23*math.cos(math.radians(39.2)),
                  -3.7042347e-23),"18.30 sodium excited 39.2° energy")


    # Chapter 10: First Law source numbers, reversible cycles and signed work.
    RG=8.314462618
    muv=4*math.pi*1e-7
    require(close(40*101.325*math.log(2),2809.32552281),
            "10.1 path A->B->C->D signed gas expansion work")
    require(close(560-356+220,424),"10.2 ad-b heat based on state U")
    require(close(-(560-356)-282, -486),
            "10.2 b->a releases 486J using reversed internal energy")
    require(close(2*(5/2)*RG*50,2078.6156545),
            "10.3 oxygen internal energy both paths")
    require(close(2*(7/2)*RG*50,2910.0619163),
            "10.3 oxygen constant-pressure input heat")
    require(close(300+1000/((10/28)*(7/2)*RG),396.2178840),
            "10.4 nitrogen isobaric final temperature")
    require(close(60000*5/7,42857.1428571),
            "10.5 diatomic hydrogen internal energy")
    require(close(300*3**(-.4),193.318204493),
            "10.7 adiabatic oxygen final temperature")
    require(close(2*2**1.4,5.278031643),
            "10.8 maximum pressure atmospheres")
    require(close(2*101325*(20/30)*(.6**1.4),66079.553465),
            "10.9 free expansion 20to30L then adiabatic 30to50L")
    require(close(317.2**2*.032/(RG*273.15),1.417688922),
            "10.10 gamma from O2 standard sound speed")
    Vi=2.0
    Vf=Vi+math.pi*.4**2*4
    P0=2.7*101325
    Pf=P0*(Vi/Vf)**1.4
    gasW=(P0*Vi-Pf*Vf)/.4
    require(close(math.sqrt(2*(.75*gasW-101325*(Vf-Vi))/70),
                  36.06149041),
            "10.12 original p2.7atm m70kg after subtract atmospheric work")
    require(close(math.sqrt(2*.315*101325/75),29.17413238),
            "10.12 companion S p164 approximate p2.6atm m75kg alternate 29m/s")
    require(close(101300*.02/RG*2**.4,321.5268563),
            "10.16 two chamber final compressed A temperature")
    require(close(1-10**(-2/7),.4820525321),
            "10.17 Brayton rp10 gamma1.4 efficiency")
    require(close(1e6/(20/298.15)-1e6,13907500),
            "10.21 ocean thermal reject heat 13.9075MW")
    require(close(1e6/(20/298.15)/(1000*4180*20),
                  .1783193780),"10.21 source ocean water volume rate")
    require(close(263.15/(288.15-263.15)*1000,10526),
            "10.22 refrigerator extracted heat for1000J")
    require(close((3.8e7/3600)*11/294.15,394.7343570),
            "10.23 Carnot least air conditioning power")
    require(close(3.34e7*(1-288.15/483.15)*(333.15/45),
                  9.97990479e7),"10.24 Carnot engine plus heat pump water")
    require(close(626+363*(.4513-.2202),709.8893),
            "10.25 measured refrigerant cold absorption kJ")
    require(close(933.3957-709.8893,223.5064),
            "10.25 compressor cycle work kJ")
    require(close(709.8893/223.5064,3.17614753),
            "10.25 measured refrigerator COP")
    require(close(278.15/(353.15-278.15),3.70866667),
            "10.25 Carnot comparison COP")
    # Chapter 19: Boltzmann magnetization, iron cores, and B-H figures.
    qe=1.602176634e-19
    m_e=9.1093837139e-31
    na=6.02214076e23
    mub=9.274e-24
    require(close(qe/(2*m_e),8.79410004e10),
            "19.2 orbital electron Larmor precession B1T")
    require(close(muv*qe*2.2e6/(4*math.pi*(.53e-10)**2),
                  12.5481972),"19.3 Bohr electron orbit central magnetic field")
    require(close(2*7800*math.pi*.005**2*.12/.05585*na*mub,
                  14.70247814),"19.4 two iron spins per atom needle moment")
    require(close(2*7800*(.085*.01*.0002)/.05585*na*mub,
                  .265196835),"19.5 magnetized compass moment")
    require(close(muv*4200*20*.1/.1,.1055575132),
            "19.6 high permeability toroid B")
    require(close(.02/(muv*32),497.359197),
            "19.7 300-turn iron ring relative permeability")
    require(close(1/(muv*(1000*2/(2*math.pi*.15))),375),
            "19.8 iron toroid relative mu")
    require(close(1.2*6/(muv*220),26043.5361),
            "19.9 companion magnetic curve B1.2T H220 => 26kA")
    require(close(170/800,.2125),
            "19.10 companion curve B1T H170 =>0.21A")
    require(close(2*math.pi*.00025*2,.00314159265),
            "19.11 companion onset magnetic flip INNER radius")
    require(close(2*math.pi*.0004*2,.00502654825),
            "19.11 full cross-section coercive field OUTER radius")
    require(close(.18*.60/(muv*1500-.18*.01),1271.252395),
            "19.12 iron toroid one cm air gap permeability")
    require(close(3/muv*(.5/5000+.02),47985.21534),
            "19.13 strong electromagnet NI air gap")
    require(close(.08/muv*(.144/1600+.002),133.0535324),
            "19.14 electric bell iron gap NI")


    # Chapter 11 Second Law: strict scanned source and companion numerical models.
    rr=8.314462618
    mm=4*math.pi*1e-7
    ep0=8.8541878128e-12
    c0=299792458
    require(close((6+8)/2*100+(8+4)/2*100,1300),
            "11.1 figure ab bc work trapezoids 1300J")
    require(close(2.5*(1200-600),1500),
            "11.1 SOURCE rigid diatomic OXYGEN five degrees not monatomic")
    require(close(1300+1500,2800),
            "11.1 rigid diatomic oxygen absorbs 2800J heat")
    require(close(rr*(2.5*math.log(2)+math.log(3)),23.54223661),
            "11.1 oxygen entropy 23.54J/K not helium 17.8J/K")
    require(close(30*(2.1*40+334+4.2*100+2260),92940),
            "11.2 full ice to 100C vapor four heat stages")
    require(close(30*(2.1*math.log(273.15/233.15)+334/273.15
                 +4.2*math.log(373.15/273.15)+2260/373.15),267.6617544),
            "11.2 entropy of ice to vapor four stages 267.66J/K")
    require(close(8e5/273,2930.40293),
            "11.3 daily environmental entropy")
    require(close(2e8/3600*(1/253.15-1/293.15),29.9446786),
            "11.4 heat leak positive entropy production rate")
    require(close(20000/285.15,70.1385236),
            "11.5 car dissipated power entropy generation")
    require(close(1000*1500*9.8*74/285.15,3.8148343e6),
            "11.6 waterfall flow rate and potential energy entropy")
    require(close(4200*(math.log(373.15/273.15)-100/373.15),
                  184.676706),"11.7 single bath water heating total entropy")
    require(close(4200*(math.log(373.15/273.15)-50/323.15
                  -50/373.15),97.60006),
            "11.7 staged heating entropy lower than single bath")
    require(close(-.9*334000/273.15,-1100.494234),
            "11.8 ice-water final EQUAL masses freeze 0.9 kg")
    require(close(.9*334000*(1/273.15-1/373.15),294.920068),
            "11.8 return from 100C bath, total entropy")
    require(close(300*4**(-.4),172.3047533),
            "11.9 isothermal -> isochoric -> reversible adiabatic final T3")
    require(close(3.039e5*4*math.log(4),1.68501243e6),
            "11.9 reversible isothermal work")
    require(close(3.039e5*4*math.log(4)
                  +(3.039e5*4/(300*.4))*(300*4**(-.4)-300),
                  391626.576),"11.9 3-leg heat engine net work")
    require(close(3.039e5*4/300*math.log(4),5617.26475),
            "11.9 entropy isothermal = -isochoric entropy")
    require(close(math.log((280+300)**2/(4*280*300)),.0011904765,rel=.04),
            "11.10 unequal T equal liquid masses generate entropy")
    require(close(math.log((1+2)**2/(4*1*2)),math.log(9/8)),
            "11.11 equal species unequal pressure positive entropy")

    # Chapter 20 electromagnetic induction and magnetic energy.
    require(close(mm*5*10/(2*math.pi)*math.log(3),1.098612289e-5),
            "20.1 a endpoint higher moving 20cm bar near 5A wire")
    require(close(4000*5e-5*math.pi*.12**2*2*math.pi*30,1.70546764),
            "20.2 source 4000-turns generator in 0.5Gauss")
    require(close(mm*1000*5*.2*2/(2*math.pi)*(1/.1-1/.2),.002),
            "20.3 moving 1000-turn rectangular loop 2mV")
    require(close(mm*1000*.2/(2*math.pi)*math.log(2)*500*math.pi,
                  .0435517218),"20.4 stationary coil AC induction amplitude")
    require(close(.42e-4*12.705*1.7*330,.29935521),
            "20.6 FBC-1 airplane south wing higher with speed sound330")
    require(close(.007/(.70e-4*200),.5),
            "20.7 seawater moving probe flux voltage .5m/s")
    require(close(60*12/(2*math.pi*120*.02*.10*.20),2387.3241464),
            "20.8 120-turn generator at12V 2387rpm")
    require(close(mm*50*100*4e-4/(2*.2),6.283185307e-6),
            "20.14 small big coax mutual inductance 6.28microhenry")
    require(close(mm*50*100*4e-4/(2*.2)*50,3.14159265e-4),
            "20.14 induced emf b 0.314mV")
    require(close(mm*1200**2*math.pi*.02**2/.3,.00757985618),
            "20.15 long coil self-inductance 7.58mH")
    require(close(mm*1200**2*math.pi*.02**2/.3*300,2.273956854),
            "20.15 induced self emf 2.27V")
    require(close(.0032/4,.0008),
            "20.16 L from change current and emf 0.8mH")
    require(close(.0008*10/(20e-6),400),
            "20.16 number turns from per turn flux")
    require(close(mm/math.pi*math.log((.2-.005)/.005),
                  4e-7*math.log(39)),
            "20.18 two anti-parallel wires exact between-boundary L prime")
    require(close(1e16/(2*mm),3.97887358e21),
            "20.21 neutron star magnetic vacuum energy density")
    require(close(1e16/(2*mm*c0**2),44270.9391),
            "20.21 magnetic field equivalent mass density")
    require(close(.5*ep0*1e12,4.42709391),
            "20.22 strong laboratory electric field energy density")
    require(close(4/(2*mm),1.59154943e6),
            "20.22 2Tesla field energy density")
    require(close(2*mm*3.6e6,9.047786842),
            "20.23 magnetic storage 1kWh at 1T requires 9m3")
    require(close(2*3.6e6/500**2,28.8),
            "20.23 superconducting coil 500A requires28.8henry")
    require(close((1.69e-8*20/(math.pi*.0055**2)),.003556652613),
            "20.24 copper wire tangential E at surface")
    require(close((mm*20/(2*math.pi*.0055)),.0007272727273),
            "20.24 copper wire surface B at20A")
    require(close((mm*20/(2*math.pi*.0055))**2/(2*mm),.2104528173),
            "20.24 copper wire magnetic energy density")
    require(close(mm/(8*math.pi),5e-8),
            "20.25 coax internal conductor inductance per metre")
    require(close(mm/(2*math.pi)*math.log(3),2e-7*math.log(3)),
            "20.25 coax gap energy inductance coefficient")
    require(close(mm*(3*5)*(.01)*2,3.7699111843e-7),
            "20.27 nested solenoid force formula dimensional sample")

    # Chapter 21: independently reconstructed SI numerical models.
    charge=1.602176634e-19
    electron_mass=9.1093837139e-31
    light=299792458.0
    vacuum_eps=8.8541878128e-12
    coulomb_k=1/(4*math.pi*vacuum_eps)
    require(close(coulomb_k*charge*2e24*math.sin(math.pi/4)/(light**2*.20),
                  .113290996318), "21.3 angular acceleration radiation E")
    require(close(.20/light,6.67128190396e-10),"21.3 retarded signal time")
    require(close(2e4*charge/(electron_mass*5e-9),7.03528003351e23),
            "21.4 Xray target stopping acceleration")
    require(close(coulomb_k*charge*(2e4*charge/(electron_mass*5e-9))/
                  (light**2*.30),.0375725376316),"21.4 Xray radiation")
    require(close(coulomb_k*charge*(8e-3*6e6)/(light**2*1000),
                  7.69044784739e-25),"21.5 single electron antenna E")
    require(close(coulomb_k*charge*1.1e14*math.sin(math.pi/4)/(light**2*.5),
                  2.49240191899e-12),"21.6 proton radiation E")
    require(close(charge*3.9e-3/electron_mass,685939803.267),
            "21.7 wire electron acceleration")
    e_single=coulomb_k*charge*(charge*3.9e-3/electron_mass)/(light**2*4)
    require(close(e_single,2.74749181431e-18),"21.7 single electron radiation")
    n_electrons=8.5e28*math.pi*(.0026/2)**2*.05
    require(close(n_electrons,2.25644892344e22),"21.7 correct 0.26cm DIAMETER")
    require(close(e_single*n_electrons,61995.7494656),
            "21.7 companion coherent sum decimal order suspect")
    require(close(math.sqrt(1380/(light*vacuum_eps)),721.03247698),
            "21.8 rms sunlight E (not peak)")
    require(close(3e5/(math.pi*(30e-6)**2),1.06103295395e14),
            "21.9 laser beam Poynting intensity")
    require(close(math.sqrt(2*3e5/(math.pi*(30e-6)**2*light*vacuum_eps)),
                  282744859.388),"21.9 amplitude requires factor TWO")
    radius_moon=3.82e8*.880e-6/2
    require(close(radius_moon,168.08),"21.10 full divergence angle halved")
    require(close(3800/(math.pi*radius_moon**2),.0428155616207),
            "21.10 moon beam intensity")
    require(close(vacuum_eps*30**2/2,3.98438451576e-9),
            "21.13 absorbing surface pressure")
    require(close(1.1e3*1.5*.5/light,2.75190378538e-6),
            "21.14 50% reflectance radiation force")
    require(close(2*1.5e9/(light*1.3e-6),7697632.96611),
            "21.15 perfect reflector 7.7MPa peak")
    require(close(math.sqrt(2*10*100*light/10000),7743.28687316),
            "21.16 laser recoil return time")
    require(close(3*6.9e7*(7e8)**2/
                  (4*6.6743e-11*2e30*1000*light),6.33650835592e-7),
            "21.17 gravity radiation balance size")

    # Chapter 22 geometrical interference, thin film, Michelson and source-page regression.
    require(close(c0*1e-8/(589.3e-9),5.08726384e6),"22.1 source sodium wave train")
    require(close(.60e-3*2.27e-3/2.5,5.448e-7),"22.2 mercury filtered green light")
    require(close(.5*7.2e-7/(4*.002),4.5e-5),"22.3 Lloyd mirror first bright half fringe")
    require(close(.15e-3*(.036/9)/1,6e-7),"22.4 fringe order 1 to 10 NINE gaps")
    require(close(math.asin(-.625)*180/math.pi,-38.68218745),
            "22.5 south/north antenna lag azimuth branch 1")
    require(close(math.asin(.875)*180/math.pi,61.04497563),
            "22.5 south/north antenna lag azimuth branch 4")
    require(close(25*50/(12*4.5),23.14814815),"22.6 water waves")
    require(close(.000000550/(.0005),.0011),"22.7 oblique incidence small angle")
    require(close(math.asin(c0/(2*25*6e7))*180/math.pi,5.73518676),
            "22.8 minimal NONZERO grazing angle with reflection phase")
    require(close((.0000006328)/math.cos(math.pi/4),8.94914342e-7),
            "22.10 inclined screen projected fringe spacing")
    require(close(2*2*1/(2**2+1**2),.8),"22.10 amplitude ratio visibility")
    require(close(c0/1.3e9,.230609583),"22.11 finite linewidth coherence")
    require(close(550e-9/.01,5.5e-5),"22.12 solar extended source coherence")
    require(close(7*550e-9/.58,6.63793103e-6),"22.13 glass shift seven orders")
    require(close(13*589.3e-9/(4*1.5),1.27681667e-6),
            "22.14 double pi reflection seventh DARK SiO2 order")
    require(close(2400/5,480),"22.15 white light reflected blue 480nm")
    require(close(1200/2,600),"22.15 white light transmission 600nm")
    require(close(560/(4*2.0),70),"22.16 sapphire SiO quarter wave 70nm")
    require(close(485*679/(2*1.32*(679-485)),642.9924242),
            "22.17 oil film adjacent extinction wavelengths")
    require(close(500/(4*math.sqrt(1.33**2-.5)),110.96763094),
            "22.18 green oblique incidence soap film thickness")
    require(close(550/(4*1.38),99.63768116),
            "22.19 MgF2 quarter-wave coating")
    require(close(((4.60e-3)**2-(3e-3)**2)/(20*1.03),5.902912621e-7),
            "22.20 Newton rings FIVE order diameter square spacing")
    require(close(2*.3220e-3/1204,5.348837209e-7),
            "22.22 Michelson mirror translation double optical path")
    require(close(1+98*589.3e-9/.20,1.000288757),
            "22.23 gas index from SINGLE PASS two-tube setup")

    # V2 chapter 23 diffraction independent numeric/geometry models.
    c23=299792458.0
    require(close(2*.5*546.1e-9/.10e-3,.005461),"23.1 central fringe FULL width")
    require(close(632.8e-9/math.sin(math.radians(5)),7.2605657419e-6),
            "23.2 first single slit minimum")
    require(close(600*5/7,428.57142857),"23.3 unknown lambda ~429nm")
    require(close(2*math.degrees(math.asin(20/50)),47.15635696),
            "23.4 harbor is SINGLE slit not circular aperture")
    airy=2*1.22*550e-9/.007
    require(close(airy,1.91714285714e-4),"23.5 airy full angular width")
    require(close(.023*airy*1000,.0044094285714),
            "23.5 retinal spot DIAMETER mm")
    require(close(math.pi*(.023*airy*1000)**2/4*1.5e5,2.290581581),
            "23.5 retinal cell count not divided by four")
    require(close(1500+2*3.5e7*1.22*.1/1500,7193.333333),
            "23.6 source includes emitter dish diameter")
    require(close(1.2*.005/(1.22*550e-9),8941.87779),
            "23.7 headlight Rayleigh distance")
    require(close(1.22*500e-9/(.05/160000),1.952),
            "23.8 low orbit camera ideal minimum aperture")
    require(close(1.22*.2/300,.0008133333333),
            "23.9 FAST working 300m aperture, NOT500m")
    require(close(.05/1e7,5e-9),
            "23.10 explicit 5cm example with 10e3km baseline")
    require(close(1.22*550e-9/(14*math.pi/(180*3600)),.0098859775),
            "23.11 zeta Ursae double star aperture")
    require(close(.5*480e-9/.1e-3,.0024),
            "23.12 double slit 2.4mm fine fringes")
    require(close(2*.5*480e-9/.02e-3,.024),
            "23.12 diffraction envelope central 24mm")
    require(close(.02/6000,3.33333333e-6),
            "23.13 grating 6000 grooves across 2cm")
    require(close(.01/6000*math.sin(math.radians(20)),5.70033556e-7),
            "23.14 first order 20 degree wavelength")
    require(close(2*656.3e-9/math.sin(math.radians(41)),2.0003e-6,rel=.005),
            "23.15 figure read Halpha second order 41degree")
    require(math.ceil(656.3/.18)==3647,
            "23.16 strict integer ceiling not companion truncation 3646")
    require(close((c23/232e6)/(192*6),.00112170908914),
            "23.17 first antenna array null")
    require(close(math.asin((c23/232e6)/6),.217068806193),
            "23.17 first NONZERO PRINCIPAL max not local sidelobe")
    require(close(.55*math.sin(math.pi/4)/3,.1296362432),
            "23.18 third Bragg order within source band")
    require(close(.55*math.sin(math.pi/4)/4,.0972271824),
            "23.18 fourth Bragg order within source band")
    require(close(.215*math.sin(math.radians(50)),.16469955527),
            "23.19 Davisson-Germer in-plane scattering lambda")

    # Chapter 24 polarization: source-angle and Jones-vector numeric models.
    require(close((math.cos(math.pi/6)**4)/(math.cos(math.pi/3)**2),2.25),
            "24.1 inserted middle polarizer INCREASES transmitted intensity")
    require(close(math.degrees(math.acos(math.sqrt(1/3))),54.735610317),
            "24.2 one third of MAX transmitted intensity")
    require(close(math.degrees(math.acos(math.sqrt(2/3))),35.264389683),
            "24.2 one third of incident intensity")
    require(close(.5*(.25/(.25+.75*.25)),2/7),
            "24.3 transverse projected polarizer axis, theta60 phi60")
    require(close(math.degrees(math.atan(1.5/1.33)),48.43766499),
            "24.5 Brewster water to glass angle")
    require(close(math.degrees(math.atan(1.33/1.5)),41.56233501),
            "24.5 reciprocal Brewster complementary angles")
    require(close(math.degrees(math.atan(math.sin(math.pi/4))),35.264389683),
            "24.6 critical TIR 45deg gives Brewster35.26deg")
    require(close(math.tan(math.radians(58)),1.600334529),
            "24.7 refractive index from Brewster 58degrees")
    require(close(90-math.degrees(math.atan(1.33)),36.93876273),
            "24.8 solar elevation reflected horizontal lake")
    require(close(math.degrees(math.asin(1.4864*.5)),48.004724656),
            "24.9 calcite extraordinary ray along equilateral base")
    require(close(3/16,.1875),"24.11 CROSSED P1/P2 analyzer transmitted3/16")
    require(close(632.8/(4*(1.66-1.49)),930.588235294),
            "24.12 632.8nm quartz quarter-wave plate thickness")
    require(close((2*math.pi*(800/4))/400,math.pi),
            "24.13 800nm QWP becomes 400nm HWP")
    require(close(math.degrees(math.asin(1.55/1.658)),69.205745109),
            "24.14 calcite ordinary crystal glue TIR critical angle")
    require(90-math.degrees(math.asin(math.sin(math.radians(22))/1.658))>69.2,
            "24.14 ordinary light hits glue above critical angle")
    require(close(math.pi*(1.55821-1.55810)/396.8e-9,870.90522151),
            "24.15 quartz optical rotation radians per meter")
    require(close((2*(2*math.pi)*(1/8)),math.pi/2),
            "24.16 counterpropagating waves relative phase pi/2 at lambda/8")

    # V2 chapter 25: geometry, surface refraction, exact imaging and optical-model disputes.
    require(close(8/(8-1.7)*1.5,1.90476190476),"25.1 lamp shadow END speed")
    require(close(1.6+2*math.tan(math.asin(math.sin(math.pi/4)/1.33)),
                  2.85545542923),"25.2 swimming pool refraction")
    require(close(math.sin(math.pi/4)/math.sin(math.radians(17)),
                  2.4185198833),"25.3 refraction into diamond")
    require(close(c0/580e-9,5.16883548276e14),
            "25.3 SOURCE 580nm not companion 589nm")
    require(close(580/(math.sin(math.pi/4)/math.sin(math.radians(17))),
                  239.81609744),"25.3 wavelength in diamond nm")
    require(close(math.degrees(math.asin(1/1.52)),41.1395104149),
            "25.5 total internal reflection to AIR")
    require(close(math.degrees(math.asin(1.33/1.52)),61.0449756281),
            "25.5 total internal reflection to WATER")
    require(close(((1.52-1)/(1.52+1))**2,.04257999496),
            "25.6 normal incidence Fresnel reflectance")
    require(close(15*25/(25-15),37.5),"25.8 mirror REAL image for s25")
    require(close(15*10/(10-15),-30),"25.8 mirror VIRTUAL image for s10")
    require(close(5.0,2.0*(5/2)),"25.9 concave dental mirror R5cm")
    require(close(.4/(1.4/2.6),.742857142857),"25.11 eye distant spherical radius")
    require(close(.4/(1.4/2.6+1/25),.691489361702),
            "25.11 companion typo 0.361 vs independent 0.691")
    require(close(1/(.33/20-1.33/10),-8.58369098712),
            "25.12 fish bowl spherical virtual image")
    require(close(20/(2*.662)-20/(2*.698),.7790926168),
            "25.13 chromatic focus shift")
    require(close(math.degrees(math.acos(math.sqrt((1.333**2-1)/3))),
                  59.4104730269),"25.14 red rainbow critical incidence")
    require(close(math.degrees(math.acos(math.sqrt((1.342**2-1)/3))),
                  58.88825686),"25.14 violet rainbow critical incidence")
    require(close(24/(1.6-1),40),"25.15 plano convex lens 40cm focal")
    require(close(((100**2-60**2)/(4*100)),16),
            "25.16 two positions Bessel lens L100 d60 f16")
    require(close(20*500/(500-20),125/6),
            "25.17 slide original correct object position")
    require(close((500/(125/6))**2,576),
            "25.17 exact projected area ratio 576 not rounded 578")
    require(close(1/(1/8+1/20),40/7),
            "25.18 second convex lens virtual-object s=-20cm")
    require(close(1.22*550e-9/1.02,6.57843137255e-7),
            "25.20 Yerkes diffraction vs companion arithmetic")
    require(close(1.22*550e-9/5.1,1.31568627451e-7),
            "25.20 Palomar diffraction")
    require(close(18/6*20,60),"25.21 Cassegrain secondary angular magnification 3 EFL60m")
    require(close(60/.2,300),"25.21 geometrical Cassegrain actual angular 300")
    require(close(1.22*590e-9/10,7.198e-8),
            "25.21 giant telescope Rayleigh resolution")

    # Ch26 wave-particle original textbook independently computed numerical models.
    hc=6.62607015e-34
    cc=299792458.0
    kb=1.380649e-23
    SB=5.670374419e-8
    qel=1.602176634e-19
    me26=9.1093837e-31
    mn26=1.6749275e-27
    require(close(SB*(273.15-5)**4,293.172305169),
            "26.1 ground -5C blackbody total emission not net")
    peak=2.821439372
    T26=hc*3.4e14/(peak*kb)
    require(close(T26,5783.36951394),"26.2 frequency spectrum Sun blackbody T")
    require(close(SB*T26**4,6.343595787e7),"26.2 Sun blackbody M0")
    require(close((1000/SB)**.25-273.15,91.265688736),
            "26.3 single hot water box blackbody Celsius")
    power_sun=3.9e26
    require(close((power_sun/(16*math.pi*SB*(1.5e11)**2))**.25,279.254464008),
            "26.4 Earth distance equilibrium sphere vs disk")
    require(close((power_sun/(16*math.pi*SB*(5.9e12)**2))**.25,44.526621917),
            "26.4 Pluto equilibrium")
    require(close(11*9.460730472e15*math.sqrt(1.7e-12/(SB*6600**4)),
                  1.30812147816e7),"26.5 Procyon B source 11lightyears radius")
    require(close(peak*kb*3/hc,1.76367772722e11),
            "26.6 3K frequency-spectrum maximum")
    require(close(4*math.pi*(6.371e6)**2*SB*3**4,2.34272779218e9),
            "26.6 isotropic incoming Earth CMB power not net")
    require(close(6.62607015e-34*cc/qel/200e-9-4.2,1.99920992166),
            "26.11 aluminum 4.2eV work function source")
    require(close(hc*cc/qel/4.2*1e9,295.20047246),
            "26.11 photoelectric red-limit wavelength nm")
    require(close(1e-15/(hc*cc/500e-9),2517.05828377),
            "26.12 photon density from radiation energy density")
    require(close(2.25*qel/(1/(4*math.pi)*math.pi*(1.3e-10)**2),
                  85.323016),"26.13 classical light energy accumulation 85s")
    require(close(5*math.sqrt(1-.5**2)/(1+.5),2.88675134595),
            "26.14 photon proton rest-frame Doppler redshift")
    require(close(600-600/1.2,100),"26.15 Compton 20% wavelength boost gives electron100keV")
    require(close(4000*(2*4000/511000)/(1+2*4000/511000),
                  61.6570327553),"26.16 max electron recoil with photon 4keV")
    P26=50-math.sqrt(20*(20+2*511))
    eps26=(581**2-P26**2-511**2)/(2*(581+P26))
    require(close(eps26,69.3902653568),"26.18 moving electron inverse Compton photon keV")
    require(close(581-eps26-511,.60973464323),
            "26.18 electron final kinetic not initial 20keV")
    require(close(hc*cc/(.2e-9)/qel,6199.20992166),
            "26.19 photon energy same wavelength as electron")
    require(close(math.hypot(hc*cc/(.2e-9),me26*cc*cc)/qel -
                  me26*cc*cc/qel,37.601632818),
            "26.19 electron kinetic same p but unequal energy")
    require(close(hc/math.sqrt(3*mn26*kb*300)*1e9,.14524297194),
            "26.20 3/2 kT neutron thermal wavelength nm")
    require(close(hc*cc/math.sqrt(40e3*qel*(40e3*qel+2*me26*cc*cc))*1e9,
                  .00601553854639),"26.21 40kV relativistic electron wavelength nm")

    # Ch27/28 original source scan: independent quantum mechanics and atomic model QC.
    h28=6.62607015e-34
    hb28=h28/(2*math.pi)
    cc28=299792458.0
    e28=1.602176634e-19
    kb28=1.380649e-23
    me28=9.1093837139e-31
    a028=5.29177210903e-11
    muB28=9.2740100783e-24
    E27base=h28*h28/(8*1e-17*(1e-5)**2)
    require(close(E27base*(101**2-100**2),1.10310824152e-38),
            "27.1 cell particle levels 100/101 g->kg")
    mO28=.032/6.02214076e23
    E27oxy=h28*h28/(8*mO28*.1**2)
    n27=math.sqrt(1.5*kb28*300/E27oxy)
    require(close(E27oxy,1.032816092e-40),"27.2 oxygen lowest box E1")
    require(close(n27,7.755975e9),"27.2 classical-energy n~7.76e9")
    require(close(E27oxy*(2*n27+1),1.602099e-30),
            "27.2 adjacent oxygen level spacing 1.6e-30J")
    require(close(.25-1/(2*math.pi),.090845056908),
            "27.4 quantum probability first quarter NOT 25percent")
    require(close(1/3-1/(2*math.pi**2),.2826727415),
            "27.5 n1 squared position expectation fraction")
    require(close(math.pi**2*hb28**2/(1e-30*1e-27),1.097e-9,rel=1),
            "27.7 dimensional wall-force proportional n^2/a^3")
    require(close((2**2+2**2+1**2)/(1**2+1**2+1**2),3),
            "27.9 cubic well excitation degeneracy energy ratio")
    require(close(hb28*math.sqrt(1.13e3/1.67e-27)/e28,.5414355324),
            "27.11 oscillator level spacing eV")
    require(close(h28*cc28/(hb28*math.sqrt(1.13e3/1.67e-27))*1e9,2289.9162),
            "27.11 H2 oscillator photon wavelength nm")
    RH28=1.0967758e7
    require(close(36/(5*RH28)*1e9,656.47,rel=.002),
            "28.1 Balmer longest Halpha")
    require(close(4/RH28*1e9,364.70,rel=.002),
            "28.1 Balmer shortest continuum limit")
    photon28=13.6*(1-1/25)
    l28=h28*cc28/(photon28*e28)
    require(close(l28*1e9,94.96,rel=.002),
            "28.2 n5 to n1 photon wavelength")
    require(close(h28/(1.6735575e-27*l28),4.18,rel=.003),
            "28.2 photon recoil hydrogen atom")
    rinfty28=me28*e28**4/(8*8.8541878128e-12**2*h28**3*cc28)
    require(close(rinfty28,1.0973731534e7,rel=.00001),
            "28.5 infinite-mass Rydberg constant")
    require(close(2*a028*1e9,.10583544218),
            "28.6 positronium reduced-mass radius doubled")
    require(close(5.1*e28/h28,1.23317451346e15),
            "28.6 positronium level2 to level1 frequency")
    nEarth=5.97e24*math.sqrt(6.6743e-11*1.99e30*1.5e11)/hb28
    require(2e74<nEarth<3e74,"28.7 gravitational Bohr Earth's huge quantum number")
    require(1e-64<3e11/nEarth<2e-63,
            "28.7 Earth next permitted Bohr radius imperceptibly small")
    require(close(.5*((411.7/410.2-1)+(435.7/434.0-1))*cc28,1.136e6,rel=.02),
            "28.8 Hdelta and Hgamma redshift averaged")
    require(close(1/(2*math.pi*1e-8),1.59154943e7),
            "28.9 natural linewidth Lorentz FWHM not HWHM")
    sigma28=4.56e14/cc28*math.sqrt(kb28*300/1.6735575e-27)
    require(close(sigma28,2.392908483e9),
            "28.10 Doppler one-dimensional sigma frequency")
    require(close(2*math.sqrt(2*math.log(2))*sigma28,5.63486886e9),
            "28.10 Doppler Gaussian FWHM")
    require(close(4/a028**3*math.factorial(2)/(2/a028)**3,1),
            "28.11 hydrogen 1s radial probability integrates to1")
    require(close(4/a028**3*math.factorial(3)/(2/a028)**4/a028,1.5),
            "28.12 hydrogen mean radius 3a0/2")
    require(close(24/(32*math.pi)*(4*math.pi/3),1),
            "28.14 normalized 2p m0 electron wavefunction")
    require(close(1/32,1/64+1/64),"28.14 2p density spherical sum")
    require(close(math.degrees(math.acos(1/math.sqrt(2))),45),
            "28.15 l1 angle45")
    require(close(4.5e-5*e28/h28,1.08809515894e10),
            "28.16 Lyman fine structure frequency NOT Balmer")
    require(close(4.5e-5*e28/(2*muB28),.388709673),
            "28.16 effective spin orbit B~.39T")
    require(close(math.degrees(math.acos(1/math.sqrt(3))),54.7356),
            "28.17 silver jhalf allowed angle")
    require(close(muB28*1.5e3,1.3911015e-20),
            "28.18 silver Stern Gerlach force")
    require(close(muB28*(.04)**2*1.5e3/(3*kb28*2500),.000214948421),
            "28.18 silver two traces split 0.215mm at magnet exit")
    require(close(2*1.41e-26*1.6/h28,6.80946609e7),
            "28.19 NMR resonance 68.1MHz")
    require(sum(2*(2*l+1) for l in range(4))==2*4**2,
            "28.20 n4 electron shell capacity 32")
    require(close(.041e-9*30000*e28/cc28,6.573471771e-34),
            "28.22 Planck inferred from Xray rounded short edge")
    require(close(h28*cc28/(.1e-9*e28),12398.41984),
            "28.23 Xray minimum 12.4kV")
    require(close(h28*cc28/(20000*e28)*1e9,.0619921,rel=.002),
            "28.24 Xray first of four collisions")
    require(close(h28*cc28/(5000*e28)*1e9,.2479684,rel=.002),
            "28.24 Xray last two equal 5keV")
    require(close(h28*cc28/(3.16e-9*e28),392.3550583),
            "28.25 Xray N element Kalpha")
    require(close(h28*cc28/(8028*e28*2*math.sin(math.radians(74.1)))*1e9,.08029171),
            "28.26 Bragg Kalpha d~0.080nm not NaCl cell parameter")
    require(close(h28*cc28/(10.6e-6*e28),.1169662),
            "28.27 CO2 photon energy eV")
    require(close(math.exp(-h28*cc28/(10.6e-6*kb28*300)),.01084061457),
            "28.27 thermal CO2 high-to-low Boltzmann 1.084percent")
    require(close(-h28*cc28/(10.6e-6*kb28*math.log(1.01)),-136411.2),
            "28.27 negative FORMAL inversion temperature")
    require(close(cc28*10e-15/(500e-9),6),
            "28.28 ten femtosecond laser pulse six carrier cycles")
    require(close(cc28*12e-12,.003597509496),
            "28.29 ruby pulse length 3.6mm not S typo0.36mm")
    require(close(.15/(12e-12),1.25e10),
            "28.29 average ruby pulse power12.5GW")
    require(close(.15*694.4e-9/(h28*cc28),5.24353582e17),
            "28.29 total photons per pulse")
    require(close(.005*.8e-6/(h28*cc28),2.013646627e16),
            "28.30 GaAlAs photons per second")
    Rairy28=1.22*515e-9*.035/.003
    require(close(Rairy28,7.3301667e-6),
            "28.31 Airy first minimum radius7.33um")
    require(close(.84*5/(math.pi*Rairy28**2),2.4881222734e10),
            "28.31 Airy central bright spot mean not peak intensity")
    require(close(math.sqrt(hb28/(math.pi*2.66e-26*8.6e10)),1.21135964e-10),
            "28.32 oxygen rigid rotor molecular bond length")
    require(close(5*hb28**2/(4*me28*a028**2*e28),34.01423276),
            "28.33 H2 electron-cloud rotation about internuclear axis34eV")
    require(close((2*math.pi*6.42e13)**2*((12*16/28)*1.6605390666e-27),1852.77246),
            "28.34 CO molecule oscillator spring constant")

    # Chapter29 solid electron Fermi models and semiconductor source checks.
    h29=6.62607015e-34
    hb29=h29/(2*math.pi)
    cc29=299792458.
    ee29=1.602176634e-19
    mm29=9.1093837139e-31
    kk29=1.380649e-23
    Na29=6.02214076e23
    ng29=19.3e3/.197*Na29
    ef29=hb29*hb29/(2*mm29)*(3*math.pi**2*ng29)**(2/3)
    require(close(ng29,5.899863790e28),"29.1 Gold conduction e density")
    require(close(ef29/ee29,5.52626357),"29.1 Au Fermi energy eV")
    require(close(math.sqrt(2*ef29/mm29),1.394253e6),
            "29.1 Au Fermi velocity")
    require(close(ef29/kk29,64129.6257),"29.1 Au Fermi temperature")
    require(close(h29/math.sqrt(2*mm29*ef29)*1e9,.521706),
            "29.1 Fermi deBroglie wavelength nm")
    require(close((2/5)/(2/3),.60),
            "29.2 T0 free electron mean energy 3Ef/5")
    require(close((1/4)/(1/3),.75),
            "29.3 0K mean velocity 3vF/4")
    require(close(math.sqrt((1/5)/(1/3)),math.sqrt(.6)),
            "29.3 vRMS sqrt3/5 vF")
    nm29=5e16/1.6749275e-27
    En29=hb29**2/(2*1.6749275e-27)*(3*math.pi**2*nm29)**(2/3)
    require(close(En29/ee29/1e6,19.0844),
            "29.4 neutron star nonrel EF about19MeV")
    require(close(math.sqrt(2*En29/1.6749275e-27),6.04243256e7),
            "29.4 neutron vF about.2c")
    require(close(.3*5*ee29/(math.pi**2*kk29),1763.6753),
            "29.5 Sommerfeld heat .1 classical occurs near1764K")
    R29=8.314462618
    require(close(math.pi**2*R29*kk29/(2*.00208)/ee29,1.69986),
            "29.6 potassium EF from electronic gamma")
    require(close(math.sqrt(.00208/.00257),.89963244),
            "29.6 potassium gammaT equals betaT3 at0.9K")
    nAg29=10.5e3/.1078682*Na29
    tau29=mm29/(1.6e-8*nAg29*ee29**2)
    require(close(tau29,3.7835672e-14),"29.7 silver Drude scattering time")
    require(close(math.sqrt(8*kk29*300/(math.pi*mm29))*tau29*1e9,
                  4.0712642),"29.7 silver classical mfp in nm")
    vAg29=hb29/mm29*(3*math.pi**2*nAg29)**(1/3)
    require(close(vAg29*tau29*1e9,52.63943),
            "29.7 silver quantum Fermi mfp~53nm")
    require(close(nAg29**(-1/3)*1e9,.2574252),
            "29.7 Ag lattice spacing ~.26nm")
    f29=1/(math.exp(.1*ee29/(kk29*1000))+1)
    require(close(f29,.238585198),"29.8 FD states above EF")
    require(close(1-f29,.761414802),"29.8 FD states below EF")
    require(close(math.exp(-5.5*ee29/(kk29*300)),4.0185e-93,rel=.01),
            "29.9 diamond empty-gap upper over lower occupancy")
    require(close(h29*cc29/(5.5*ee29)*1e9,225.426),
            "29.9 diamond UV absorption threshold")
    nSi29=2.33e3/.028085*Na29
    fSi29=(1e6-1)*1e16/nSi29
    require(close(fSi29,2.00155e-7),"29.10 silicon P replacement fraction")
    require(close((1/.028085)*.030973762*fSi29*1e6,.2207429),
            "29.10 P mass in micrograms per1g silicon")
    require(close(h29*cc29/(.045*ee29)*1e6,27.552),
            "29.11 silicon DONOR 0.045eV not intrinsic GAP1.2eV")
    require(close(h29*cc29/(2.42*ee29)*1e9,512.3314),
            "29.12 CdS visible photoresponse edge")
    require(close(h29*cc29/(.3*ee29)*1e6,4.1328066),
            "29.12 PbS infrared photoresponse edge")
    require(close(h29*cc29/(1.9*ee29)*1e9,652.5484),
            "29.13 GaAsP LED red photon wavelength")
    require(close(h29*cc29/(140e-9*ee29),8.856014),
            "29.14 KCl 140nm photon energy above7.6eV gap")

    # Chapter30 nuclear reaction source-model, careful isotope mass conventions.
    Na30=6.02214076e23
    unit30=931.494
    er30=1.602176634e-19
    year30=365.25*24*3600
    massH30=1.007825
    massN30=1.008665
    require(close(2*79*1.439965/6*(1+4/197),38.693,rel=.002),
            "30.1 gold alpha close approach WITH target recoil fm")
    require(close(2*7*1.439965/6*(1+4/14),4.32),
            "30.1 nitrogen alpha recoil 28.6percent")
    require(close((7*massH30+9*massN30-16.006099)*unit30,117.984),
            "30.2 16N nuclear binding from NEUTRAL atom mass")
    require(close((8*massH30+8*massN30-15.994915)*unit30,127.619),
            "30.2 16O binding energy atomic mass convention")
    require(close((9*massH30+7*massN30-16.011465)*unit30,111.421),
            "30.2 16F nuclear binding")
    require(close(3*(2*6-1)*1.439965/(5*2.79),3.40637),
            "30.4 mirror 11C/B Coulomb inferred radius")
    require(close(3*(2*8-1)*1.439965/(5*3.48),3.72405),
            "30.4 mirror 15O/N inferred radius")
    require(close(3*(2*11-1)*1.439965/(5*4.30),4.21943),
            "30.4 mirror 21Na/Ne inferred radius")
    require(close(3*28.3+3*2.42,92.16),
            "30.5 carbon12 alpha triangle pair interactions")
    require(close(4*28.3+6*2.42,127.72),
            "30.5 oxygen16 tetrahedron six pair bonds")
    require(close(-17.804*232**(2/3)*(2**(1/3)-1)
                  +.7103*90**2/232**(1/3)*(1-2**(-2/3)),
                  171.7572),"30.6 Th232 equal-half liquid-drop fission model")
    require(close(7.3458*12**(2/3)-.8345*36/12**(1/3),25.3808),
            "30.7 two carbon12 fusion semi empirical Q")
    require(close(math.sqrt(2-1),1),
            "30.8 exponential half lifetime RMS is mean tau not mode")
    NK30=.0037*70/.0391*Na30*1.2e-4
    AK30=math.log(2)/(1.3e9*year30)*NK30
    require(close(AK30,8077.94,rel=.005),
            "30.9 natural potassium40 body activity about8.1kBq")
    N238=1e4/(8*16+3*238)*3*Na30*.9927
    N235=1e4/(8*16+3*238)*3*Na30*.0072
    require(close(N238*1600/4.46e9/Na30*226*1e3,2.87,rel=.005),
            "30.10 U238 to Ra226 secular equilibrium mg")
    require(close(N235*3.27e4/7.04e8/Na30*231*1e3,2.75,rel=.02),
            "30.10 U235 to Pa231 secular equilibrium mg")
    require(close(4/30*2**(24/13.1),.4756,rel=.01),
            "30.11 I123 uptake fraction near48percent")
    require(close(300e3/30*2**(-10/14.97),6290,rel=.005),
            "30.12 Na24 radiotracer blood volume milliliters")
    tau30=8270*year30
    age30=8270*math.log((.3*Na30*1.3e-12)/(.15*tau30))
    require(close(age30,1.50e4,rel=.02),
            "30.13 C14 wood dating count-per-minute converted to per-second")
    require(close(4.46e9/math.log(2)*math.log(1+(.12/206)/(.30/238)),
                  2.45e9,rel=.01),
            "30.14 uranium to lead rock closed-system geological age")
    require(close(4.7825*4/222,.08617117),
            "30.15 Ra alpha decay daughter recoil")
    require(close(4.7825*(1+4/222),4.86867),
            "30.15 Ra total release includes recoil")
    require(close((.66-.57)/unit30,9.661898e-5),
            "30.16 difference of Zn64 vs Ni64 NUCLEAR masses")
    require(close((.66-.57+1.022)/unit30,.0011937,rel=.001),
            "30.16 neutral atom mass differs by 2 electron masses")
    nCo30=8.858/59*Na30
    depthCo30=nCo30*120e-24*2
    require(depthCo30>20,"30.17 thick cobalt cube optical depth about21.7")
    incoming30=2e12*(2*2)
    thin30=nCo30*8*120e-24*2e12
    require(thin30>incoming30*20,
            "30.17 S textbook thin rate exceeds incident neutron number UNPHYSICAL")
    decayCo30=math.log(2)/(5.27*year30)
    require(close(decayCo30*thin30*(6*3600)/3.7e10,.4224),
            "30.17 unphysical companion thin source activity0.42Ci")
    require(close(decayCo30*incoming30*(1-math.exp(-depthCo30))*
                  (6*3600)/3.7e10,.01946),
            "30.17 physical one-sided shielded source limited ~.0195Ci")
    nCd30=8.64/112.4*Na30
    dCd30=-math.log(.05)/(nCd30*4000e-24)
    require(close(dCd30*1e4,161.7874),
            "30.18 exact 95percent Cd neutron attenuation 162micron")
    require(close((1-math.exp(-.95)),.61326),
            "30.18 companion thin .95 optical depth absorbs only61percent")
    qC30=(13.003355+1.007825-4.002603-10.012937)*unit30
    require(close(qC30,-4.06131),"30.19 13C(p,alpha)10B endothermic Q")
    require(close((13.003355+1.007825-2.014102-12)*unit30,-2.72183),
            "30.19 13C(p,d)12C Q negative")
    require(close((13.003355+1.007825-14.003074)*unit30,7.55069),
            "30.19 13C(p,gamma)14N Q positive")
    require(close(-qC30*(1+1/13),4.37372),
            "30.20 Coulomb barrier is not same as Q-only threshold")
    require(close(1.5e30/(4*1.67e-27)*24.67e6*er30/
                  3.9e26/year30,7.2115e10),
            "30.21 Sun all-H ideal lifetime using 24.67 MeV no annihilation")
    atomM30=[1.007825,13.005738,13.003355,14.003074,
             15.003065,15.000109,4.002603]
    mH,mN13,mC13,mN14,mO15,mN15,mHe4=atomM30
    electron_u30=.0005485799
    qs30=[(mH+12-mN13)*unit30,
          (mN13-mC13-2*electron_u30)*unit30,
          (mH+mC13-mN14)*unit30,
          (mH+mN14-mO15)*unit30,
          (mO15-mN15-2*electron_u30)*unit30,
          (mH+mN15-12-mHe4)*unit30]
    require(close(sum(qs30),24.68709),
            "30.22 CNO six nuclear Q sum 24.69MeV")
    require(close(sum(qs30)+4*electron_u30*unit30,26.73108),
            "30.22 positron annihilation adds 2.044MeV to 26.73")

    # Independent conceptual physics spotmodels for thought questions (distinct from705).
    require(close((math.cos(math.pi/4)*math.sin(math.pi/4))**2,.25),
            "thought24.5 inserting 45deg polarizer between crossed P gives Iout/I1=.25")
    require(close(1.75/2,.875),"thought25.3 full-length plane mirror half height")
    require(close(1/((1/1.33-1)*(2/.30)),-.604545454545),
            "thought25.8 convex air blister under water is DIVERGING f~-.605m")
    require(close(2.897771955e-3/310*1e6,9.34765147),
            "thought26.2 warm human blackbody peak midinfrared in micrometers")
    require(close(2*6.62607015e-34/(9.1093837139e-31*299792458)*1e12,
                  4.85262047),
            "thought26.9 visible Compton maximum shift~4.85pm")
    require(close(math.sqrt(1.67262192369e-27/9.1093837139e-31),
                  42.85035205),
            "thought26.11 same kinetic energy electron wavelength 42.85x proton")
    require(5-1==4,"thought27.5 5th one-dimensional bound eigenstate four nodes")
    require(close(math.sqrt(5/3),1.290994449),
            "thought27.6 higher step lower kinetic means longer wavelength")
    require(sum(2*l+1 for l in range(3))==9,
            "thought28.2 hydrogen level n3 orbital degeneracy9 no spin")
    require(sum(2*(2*l+1) for l in range(3))==18,
            "thought28.5 third electron shell Pauli capacity18")
    require((1*2**2-1*2**2)==0,
            "thought29.11 intrinsic electron-hole equal mobilities Hall cancellation")
    require(close((64/8)**(1/3),2),
            "thought30.2 saturated nuclear radius R scales as A^(1/3)")
    require(close((3/5)*1.439965/1.2,.7199825),
            "thought30.5 uniform charged sphere nuclear Coulomb coefficient")
    require((235-207)//4==7,"thought30.7 U235 to Pb207 seven alpha decays")
    require(82-(92-2*7)==4,"thought30.7 four beta minus conversions")
    require(close((14.4e3)**2/(2*57*931.494e6),.001952720435),
            "thought30.8 free Fe nucleus 14.4keV gamma recoil~2meV")

    # Ch22/23 source thought concepts: coherence, phase, Fresnel zones and gratings.
    require(close(1+1+2*math.sqrt(1*1)*math.cos(0),4),
            "thought22.5 equal coherent beams add amplitude and give intensity4")
    require(close(1+1+2*math.cos(math.pi),0,rel=.001),
            "thought22.5 equal coherent beams destructive intensity zero")
    require(close(500e-9*2/.5e-3,.002),
            "thought22.6 double slit pitch 2mm for example geometry")
    require(close((1.5-1)*1e-6*2/.5e-3,.002),
            "thought22.12 mica 1um changes center by 2mm but NOT pitch")
    require(1-1+1-1==0,"thought23.3 four half-wave zones cancel not maximum")
    require(close(2*500e-9/.1e-3,.01),
            "thought23.5 increasing slit width narrows central angular width")
    require(close(math.degrees(math.asin(500e-9/2e-6)),14.477512186),
            "thought23.7 grating maxima positions determined by d not N")

    # Newly scanned conceptual chapters 12--21: independent small physics models.
    eps_th=8.8541878128e-12
    mu_th=4*math.pi*1e-7
    c_th=299792458.
    h_th=6.62607015e-34
    e_th=1.602176634e-19
    mp_th=1.67262192369e-27
    require(close(1e-12/(2*eps_th*.01),5.647045336865),
            "thought12.10 parallel plates other-plate field force")
    require(close((1e-6/(4*math.pi*eps_th))-
                  (1e-6/(4*math.pi*eps_th)),0),
            "thought13.3 dipole equipotential bisector")
    require(close(3e-8+(2e-8),5e-8),
            "thought14.2 Q+q external surface shell charge")
    require(close(.001/(eps_th),1.129409067e8),
            "thought14.6 conductor surface normal E sigma/eps")
    require(close(eps_th*.03/.001,2.65625634e-10),
            "thought15.1 dielectric plate capacity by geometry")
    require(close(2*math.pi*eps_th/math.log(3),5.06388863e-11),
            "thought15.13 coaxial cylinder capacitance per meter")
    require(close(1.7e-8*8960*(10**2),.015232),
            "thought16.2 same-material wire R inversely proportional mass")
    require(close(1e9*1e-9,1),
            "thought16.6 RC gigaohm with nF tau1s")
    require(close(mu_th*1000*2,.00251327412),
            "thought17.11 long solenoid field uses turns per length")
    require(close(.5*mu_th*(1000*2)**2,.5*mu_th*4e6),
            "thought17.5 magnetic energy density scale")
    require(close(200e3/.1,2e6),
            "thought18.8 crossed E/B velocity selector")
    require(close(mp_th*1e6/(e_th*.5),.02087936983),
            "thought18.10 charged proton curvature radius at 0.5T")
    require(close((1e-6)*(1e6),1),
            "thought18.5 constant magnetic force cannot change K")
    require(close(.5*mu_th*(1000**2),.62831853),
            "thought19.8 magnetic circuit energy field scale")
    require(close((.1)*(10**2)/2,5),
            "thought20.8 inductive energy at 10A and .1H")
    require(close(1/(2*math.pi*1e3*1e-6),159.15494),
            "thought20.6 inductive circuit characteristic frequency sanity")
    require(close(1/math.sqrt(mu_th*eps_th),c_th,rel=.001),
            "thought21.1 Maxwell vacuum wave speed")
    require(close(.5*eps_th*c_th*1000**2,1327.20936),
            "thought21.4 plane-wave mean Poynting intensity")
    require(close(eps_th*1000**2/c_th,2.95343915e-14),
            "thought21.7 plane-wave momentum density w/c")
    require(close(h_th*5e14/c_th,1.10510955e-27),
            "thought21.7 individual 500THz photon momentum")

    # Companion S-verified V1 selected thought conceptual numerical testmodels.
    require(close(20**2 / 9.8,40.816326530612244),
            "S thought1.8 parabolic apex curvature radius v²/g")
    require(close(9.8-9.8,0),
            "S thought2.6 free-fall board gravity and pseudo force cancel")
    require(close(.05*1**2*20,1.0),
            "S thought3.9 circular L=m r² omega")
    require(close(20/(10),2),"S thought4.9 two frame velocity translation relation")
    require(close(2/1,2),"S thought5.6 angular frequency doubles when I halves")
    require(close(math.sqrt(1+.6/3),1.095445115),
            "S thought6.8 uniform spring effective mass m_s/3 increases period")
    require(close(1/(2*.5)*math.sqrt(40/.004),100),
            "S thought7.7 monochord fundamental frequency 100 Hz")
    require(close(1.25*.6*300/299792458,7.505192e-7),
            "S thought8.3 relativity of simultaneity 300m train 0.6c")
    require(close(math.exp(4*1.66053906660e-27*9.8*10000/
                           (1.380649e-23*300)),1.1706,rel=.01),
            "S thought9.8 diffusive equilibrium N2/O2 ratio rises with height")
    require(close(1-200/500,.6),"S thought10.8 Carnot efficiency not output work")
    require(200*(1/300-1/400)>0,
            "S thought11.6 environmental entropy gain exceeds hot object loss")
    require(close(1/((2*math.pi)*math.sqrt(1+.6/3)),
                  1/(2*math.pi*math.sqrt(1.2))),
            "S thought6.8 period/frequency reciprocal consistency")

    return 663



def check_thought_intake() -> int:
    """Separate original 思考题 register; never count as 章末习题.
    Validates scan provenance and paired conceptual LaTeX, not physics correctness.
    """
    thought_path = ROOT / "thought_register.json"
    require(thought_path.is_file(), "missing distinct 思考题 register")
    reg = json.loads(thought_path.read_text(encoding="utf-8"))
    require(reg.get("section") is None or reg.get("scope", "").startswith("original separately"),
            "wrong conceptual section")
    require(reg.get("main_chapter_end_count_unchanged") == 705,
            "thought registry changed main705 count")
    rows = reg["entries"]
    expected_counts = {12: 10, 13: 11, 14: 11, 15: 14, 16: 9,
                       17: 12, 18: 11, 19: 11, 20: 10, 21: 7,
                       22: 12, 23: 9, 24: 11, 25: 12, 26: 13, 27: 7,
                       28: 14, 29: 13, 30: 10}
    require(reg["thought_question_count"] ==
            reg["thought_solution_count"] == len(rows) == 207,
            "thought count should be exactly 207, separate from705")
    require(len({e["canonical_id"] for e in rows}) == 207,
            "duplicate thought stable IDs")
    require(len({e["source_thought_number"] for e in rows}) == 207,
            "duplicate original 思考题 numbers")
    require(all(e["academic_review"] == "pending_independent_verification"
                and e["exam_ready"] is False for e in rows),
            "conceptual questions falsely marked expert verified")
    require(sum(bool(e.get("answer_unresolved")) for e in rows) == 1,
            "30.6 source isotope notation ambiguity must remain unresolved")
    bundle = (ROOT / "build_intake.tex").read_text(encoding="utf-8")
    standalone = (ROOT / "build_thought_intake.tex").read_text(encoding="utf-8")
    regex = re.compile(r"\\paragraph\{思考题\s+(\d+\.\d+)\}")
    chapter_entries = Counter(int(x["source_thought_number"].split(".")[0])
                              for x in rows)
    require(chapter_entries == expected_counts,
            f"unexpected chapter thought counts: {chapter_entries}")
    for chapter in expected_counts:
        part = [e for e in rows
                if int(e["source_thought_number"].split(".")[0]) == chapter]
        expected = [f"{chapter}.{i}"
                    for i in range(1, expected_counts[chapter] + 1)]
        qrel = f"thought_questions/{chapter}/questions.tex"
        srel = f"thought_questions/{chapter}/solutions.tex"
        qfile, sfile = ROOT / qrel, ROOT / srel
        require(qfile.is_file() and sfile.is_file(),
                f"thought chapter{chapter}: missing TeX fragments")
        qt, st = qfile.read_text(encoding="utf-8"), sfile.read_text(encoding="utf-8")
        require(regex.findall(qt) == regex.findall(st) == expected,
                f"thought chapter{chapter} source/answer/count mismatch")
        for tex in (qt, st):
            require(tex.count(r"\[") == tex.count(r"\]") and
                    tex.count(r"\(") == tex.count(r"\)"),
                    f"unbalanced LaTeX inline/display math in thought chapter{chapter}")
            require(not any(ord(c)<32 and c not in "\n\r\t" for c in tex),
                    f"control-character TeX escape corruption in thought chapter{chapter}")
        for path in (qrel, srel):
            command = r"\input{" + path + "}"
            require(command in bundle and command in standalone,
                    f"missing thought TeX input in proof: {path}")
        for item in part:
            require(item["canonical_id"] ==
                    f"ZS4-T{chapter}-{int(item['source_thought_number'].split('.')[1]):03d}",
                    "unstable canonical thought ID")
            require(item["source_review"].startswith("paraphrased_from_uploaded_scan"),
                    "no original source scan annotation")
            require(item["textbook_pdf_pages"] and
                    all(type(p) is int and 1 <= p <= 515
                        for p in item["textbook_pdf_pages"]),
                    "invalid original V2 physical scan source page")
            require(item["question_file"] == qrel and
                    item["solution_file"] == srel,
                    "thought source register wrong file paths")
    s22t = (ROOT/"thought_questions/22/solutions.tex").read_text(encoding="utf-8")
    s23t = (ROOT/"thought_questions/23/solutions.tex").read_text(encoding="utf-8")
    require("不相干" in s22t and "I_1+I_2" in s22t,
            "thought22.5 incoherent intensities not simple coherent sum")
    require("云母片" in s22t and "零级" in s22t and "上" in s22t,
            "thought22.12 mica upper slit optical path shifts center upper")
    require("半波带" in s23t and "A-A+A-A" in s23t,
            "thought23.3 four half-wave zones source cancellation lost")
    require("随机" in s23t and "N^2" in s23t,
            "thought23.9 random slit grating lacks nonzero regular orders but center coherent")

    # Extra source-and-model guards for 106 thought Q/A added in chapters 12--21.
    q12=(ROOT/"thought_questions/12/questions.tex").read_text(encoding="utf-8")
    s12=(ROOT/"thought_questions/12/solutions.tex").read_text(encoding="utf-8")
    require("自身电场" in s12 and "另一片" in s12,
            "thought12.10 self-field double-counting in capacitor force")
    s15=(ROOT/"thought_questions/15/solutions.tex").read_text(encoding="utf-8")
    require("电源功" in s15 and "保护环" in s15,
            "thought15.6 insertion forces and15.7 guard-ring source assumptions")
    s17=(ROOT/"thought_questions/17/solutions.tex").read_text(encoding="utf-8")
    require("mu_0" in s17 and "非零" in s17,
            "thought17 Ampere law and magnetic Gauss laws")
    s18=(ROOT/"thought_questions/18/solutions.tex").read_text(encoding="utf-8")
    require("v=E/B" in s18 and "电荷" in s18,
            "thought18.8 particle selector must be charge-sign independent")
    s19=(ROOT/"thought_questions/19/solutions.tex").read_text(encoding="utf-8")
    require("磁化" in s19 and "磁阻" in s19,
            "thought19 magnetic matter H/B and circuit reluctance")
    s20=(ROOT/"thought_questions/20/solutions.tex").read_text(encoding="utf-8")
    require("楞次" in s20 and "涡电流" in s20 and "外部" in s20,
            "thought20 electromagnetic damping, induction heat source")
    s21=(ROOT/"thought_questions/21/solutions.tex").read_text(encoding="utf-8")
    require("坡印亭" in s21 and "动量密度" in s21 and "无磁单极" in s21,
            "thought21 Maxwell energy flux and photon momentum")

    main_count = len(json.loads(REGISTER.read_text(encoding="utf-8"))["entries"])
    require(main_count == 705, "main chapter-end original count changed from705")
    s30 = (ROOT/"thought_questions/30/solutions.tex").read_text(encoding="utf-8")
    q30 = (ROOT/"thought_questions/30/questions.tex").read_text(encoding="utf-8")
    require("unresolved" in s30 and "Cu" in s30 and "Zn" in q30,
            "thought30.6 unresolved Cu-to-Zn isotope source typography lost")
    s25 = (ROOT/"thought_questions/25/solutions.tex").read_text(encoding="utf-8")
    require("-0.605" in s25 and "发散" in s25,
            "thought25.8 AIR lens in water must DIVERGE")
    s26 = (ROOT/"thought_questions/26/solutions.tex").read_text(encoding="utf-8")
    require("量子效率" in s26 and "I/(h\\nu)" in s26,
            "thought26.7 photon flux at FIXED light intensity confused")
    s29 = (ROOT/"thought_questions/29/solutions.tex").read_text(encoding="utf-8")
    require("向西" in s29 and "向东" in s29 and "迁移率" in s29,
            "thought29 Hall sign electron/hole and mobility model missing")
    return len(rows)



def check_companion_selected_thought() -> int:
    """Check S-scan selected V1 thought questions without claiming V1 whole-book coverage."""
    registry = ROOT / "supplement_selected_thought_register.json"
    require(registry.is_file(), "missing S-only selected-thought provenance register")
    source = json.loads(registry.read_text(encoding="utf-8"))
    require(source.get("schema") ==
            "zhang-sanhui-4e-companion-selected-V1-thought/v1",
            "wrong S companion thought registry schema")
    require(source["previous_main_end_chapter_count_unchanged"] == 705
            and source["previous_V2_thought_count_unchanged"] == 207,
            "S selected thoughts must not modify existing 705+207 entries")
    entries = source["entries"]
    counts = {1:3, 2:3, 3:3, 4:3, 5:3, 6:2, 7:4, 8:3, 9:2, 10:2, 11:3}
    expected_numbers = {
        1:[7,8,11], 2:[6,7,11], 3:[3,9,10],
        4:[5,9,12], 5:[3,6,10], 6:[7,8],
        7:[6,7,14,17], 8:[3,5,7],
        9:[6,8], 10:[4,8], 11:[4,6,8]
    }
    require(sum(counts.values()) == 31 and len(entries) == 31,
            "S-sourced first-volume selected thought count31 failed")
    require(source["companion_selected_thought_count"] ==
            source["companion_selected_solution_count"] == 31,
            "S-source selected-thought Q/A count mismatch")
    require(source["do_not_duplicate_with_future_V1_full_intake"] is True,
            "future primary-V1 original duplicate protection removed")
    ids = [e["canonical_id"] for e in entries]
    keys = [e["main_book_source_identity"] for e in entries]
    nums = [e["source_thought_number"] for e in entries]
    require(len(set(ids)) == len(set(keys)) == len(set(nums)) == 31,
            "S selected thought duplicate source numbers or identifiers")
    require(all(e["exam_ready"] is False and
                e["academic_review"] == "pending_independent_verification" and
                e["main_book_original_thought_status"] ==
                    "not_checked_unavailable_V1_scan"
                for e in entries),
            "S-only selected thoughts falsely claimed original V1 verification")
    parent = (ROOT/"build_intake.tex").read_text(encoding="utf-8")
    standalone = (ROOT/"build_supplement_selected_thought.tex").read_text(encoding="utf-8")
    pat = re.compile(r"\\paragraph\{思考题\s+(\d+\.\d+)\}")
    for chapter, count in counts.items():
        nums_expected = [f"{chapter}.{i}" for i in expected_numbers[chapter]]
        pref = f"supplement_selected_thought/{chapter:02d}"
        qfile = f"{pref}/questions.tex"
        sfile = f"{pref}/solutions.tex"
        qs = (ROOT / qfile).read_text(encoding="utf-8")
        ss = (ROOT / sfile).read_text(encoding="utf-8")
        require(pat.findall(qs) == pat.findall(ss) == nums_expected,
                f"S selected V1 ch{chapter} original order not matched")
        for source_text in (qs, ss):
            require("\r" not in source_text and "\x08" not in source_text
                    and "\x0b" not in source_text and "\x0c" not in source_text,
                    f"S-source ch{chapter}: hidden JS TeX control-character corruption")
            require(source_text.count(r"\(") == source_text.count(r"\)")
                    and source_text.count(r"\[") == source_text.count(r"\]"),
                    f"S-source ch{chapter}: unbalanced mathematical TeX delimiters")
        for filename in (qfile, sfile):
            tex_input = r"\input{" + filename + "}"
            require(tex_input in parent and tex_input in standalone,
                    f"S source missing XeLaTeX proof include {filename}")
        chapter_items = [row for row in entries
                         if int(row["source_thought_number"].split(".")[0])
                         == chapter]
        require(len(chapter_items) == count,
                f"S source register ch{chapter} size mismatch")
        for row in chapter_items:
            number = row["source_thought_number"]
            ch, i = map(int, number.split("."))
            require(row["canonical_id"] == f"ZS4-V1-T{ch:02d}-{i:03d}",
                    f"S companion thought wrong stable ID {number}")
            require(row["main_book_source_identity"] == f"V1:thought:{number}",
                    f"S companion thought source identity wrong {number}")
            require(row["question_file"] == qfile
                    and row["solution_file"] == sfile
                    and row["source_volume"] == "S",
                    f"S companion thought path/source mismatch {number}")
            require(row["source_companion_pdf_pages"] and
                    all(type(pg) is int and 1 <= pg <= 402
                        for pg in row["source_companion_pdf_pages"])
                    and row["main_textbook_pdf_pages"] == [],
                    f"S companion thought source page / unavailable V1 violation {number}")
    require(len(json.loads(REGISTER.read_text(encoding="utf-8"))["entries"]) == 705
            and len(json.loads((ROOT/"thought_register.json").read_text(
                encoding="utf-8"))["entries"]) == 207,
            "canonical original 705 + V2 thought207 counts unexpectedly mutated")
    return len(entries)




def check_companion_ch1_crosscheck() -> int:
    """S scanned answer numeric provenance, chapter1 1.1--1.26, not expert certification."""
    p=ROOT/"companion_crosscheck_ch01_01_26.json"
    require(p.is_file(), "missing independently sourced S chapter1 crosscheck audit")
    d=json.loads(p.read_text(encoding="utf-8"))
    require(d["schema"]=="zhang-sanhui-4e-companion-answer-crosscheck/v1",
            "S chapter1 audit schema mutated")
    require(d["source"]["sha256"] ==
            "54126dd75edd65eb9ead0a9d7acb96a37bfb25674cf595c76b94f2fb30bce5a7",
            "S source input PDF fingerprint changed without source review")
    records=d["records"]
    require(len(records)==26 and d["summary"]["reviewed_distinct_existing_pairs"]==26,
            "chapter1 source spotcheck must preserve 26 cases")
    original=json.loads(REGISTER.read_text(encoding="utf-8"))
    main={x["canonical_id"]:x for x in original["entries"]}
    require(len(main)==705, "S chapter1 audit changed original source count")
    g=9.8
    u=25+65/3.6
    dist=80-u*.70
    tc=(u-math.sqrt(u*u-4*7.5*dist))/(2*7.5)
    tm=(15-math.sqrt(15**2-2*g*11))/g
    models={
        "1.1":math.sqrt(2*1.8*200e3),
        "1.2":1600/3.6/1.8,
        "1.3":25-7.5*tc,
        "1.4":(200/3.6)/(g/2)+(1200-(200/3.6)**2/g-50)/(200/3.6)+50/(18/3.6),
        "1.5":280/60*2*26/g,
        "1.6":11/(tm-1)+g*(tm-1)/2,
        "1.7":4*2**2-8,
        "1.8":17.5/math.sqrt(2*3.5/g),
        "1.9":2*(110/3.6)**2/(g*math.cos(math.pi/4)),
        "1.10":25**2/(2*g)-g*50**2/(2*25**2),
        "1.11":(150/3.6)**2/(2*265),
        "1.12":math.sqrt(g*(50**2+200**2)/(4*50)),
        "1.13":(2*math.pi*6e4/60)**2*.1/g,
        "1.14":2*math.pi*6378e3/86400*math.cos(math.radians(39.9)),
        "1.15":2.2e6/(2*math.pi*.53e-10),
        "1.16":(3e8)**2*(2*math.pi/240)/g,
        "1.17":math.hypot(10**2/400,.2),
        "1.18":math.pi*650e3*(.056**2-.022**2)/1.3/60,
        "1.19":-1.2+.9,
        "1.20":math.sqrt(344**2-30**2),
        "1.21":math.sqrt(2*1.5/(g-1.2)),
        "1.22":36.,
        "1.23":math.hypot(800*math.cos(math.pi/6),
                          1000-800*math.sin(math.pi/6)),
        "1.24":4*math.pi*6378e3/86400/1000,
        "1.25":(1-.99975)*2.9979e8,
        "1.26":math.hypot(150-5750*math.cos(math.radians(19.5)),
                          750-5750*math.sin(math.radians(19.5)))
    }
    require(len(models)==26, "not 26 independently computed source spotmodels")
    seen=set()
    for rec in records:
        name=rec["source_problem_number"]
        require(name in models and name not in seen,
                f"bad or duplicate S chapter1 crosscheck number {name}")
        seen.add(name)
        cid=f"ZS4-01-{int(name.split('.')[1]):03d}"
        require(rec["canonical_id"]==cid and cid in main,
                f"S source numeric case not linked to canonical original {name}")
        mark=main[cid].get("companion_numerical_source_audit",{})
        require(mark.get("audit_file")=="companion_crosscheck_ch01_01_26.json" and
                mark.get("status")==
                    "key_answer_value_crosschecked_not_full_proof_verified",
                f"source QA key {name} not traceably indexed")
        require(mark.get("scanned_companion_pdf_pages")==
                rec["companion_pdf_physical_pages"] and
                all(type(pg)==int and 1<=pg<=402
                    for pg in rec["companion_pdf_physical_pages"]),
                f"S companion PDF page provenance mismatch {name}")
        require(math.isclose(models[name],
                             rec["independent_computed_value"],
                             rel_tol=.012,abs_tol=1e-12),
                f"S chapter1 source model inconsistency at {name}")
        require(rec["exam_ready"] is False and
                rec["academic_review"]=="pending_independent_verification",
                f"S source audit falsely promotes original {name}")
    require(set(models)==seen, "S companion ch1 1.1--1.26 missing audit entries")
    flag={x["source_problem_number"]:x["discrepancy_note"] for x in records}
    require("rounding" in flag["1.6"].lower() and
            "misprint" in flag["1.23"].lower(),
            "material S source time-rounding or 1.23 speed-unit issue omitted")
    solution=(ROOT/"chapters/01/solutions.tex").read_text(encoding="utf-8")
    require("1.60907028" in solution and "12.93197289" in solution,
            "ch1.3 exact relative-motion collision solution regressed")
    require("917" in solution and "254.6" in solution,
            "ch1.23 917km/h source-misprint correction lost")
    return len(records)




def check_companion_ch2_crosscheck() -> int:
    """Chapter2 S companion scanned source solutions: 8 value and 3 algebra tests."""
    path=ROOT/"companion_crosscheck_ch02_01_11.json"
    require(path.is_file(), "missing S original2.1-2.11 source audit")
    d=json.loads(path.read_text(encoding="utf-8"))
    rows=d["records"]
    require(len(rows)==11 and d["summary"]["reviewed_distinct_existing_pairs"]==11,
            "S original chapter2 audit entry count changed")
    require(d["summary"]["reviewed_numeric_source_answers"]==8 and
            d["summary"]["reviewed_symbolic_source_formulas"]==3,
            "S original chapter2 value vs symbolic categories changed")
    require(d["source"]["sha256"] ==
            "54126dd75edd65eb9ead0a9d7acb96a37bfb25674cf595c76b94f2fb30bce5a7",
            "S PDF fingerprint provenance changed")
    g=9.8
    th=math.pi/6
    mu_red=2*1/(2+1)
    slope=math.atan(.1)
    models={
        "2.1":.4*10*g/(math.cos(th)-.4*math.sin(th)),
        "2.2":.5*(2*math.cos(th)+g*math.sin(th)),
        "2.3":(5000+1500)*(g+.6),
        "2.4":75*g/2,
        "2.5":1.96,
        "2.6":25**2/(25**2/35*math.cos(slope)-2*g*math.sin(slope)),
        "2.7":2*.25*(1.5+2.45)*g,
        "2.8":(25-mu_red*g)/(10+1+mu_red),
        "2.9":math.sqrt(6.67e-11*7.35e22/(1.94e6)),
        "2.10":100*200/(100+200),
        "2.11":1200*(25**2/400*math.cos(math.radians(6))
                      -g*math.sin(math.radians(6)))
    }
    require(len(models)==11, "chapter2 source models count wrong")
    index={x["canonical_id"]:x for x in json.loads(
        REGISTER.read_text(encoding="utf-8"))["entries"]}
    seen=set()
    for x in rows:
        n=x["source_problem_number"]
        require(n in models and n not in seen,
                f"unknown or duplicated chapter2 original {n}")
        seen.add(n)
        cid=f"ZS4-02-{int(n.split('.')[1]):03d}"
        require(x["canonical_id"]==cid and cid in index,
                f"chapter2 original source link missing {n}")
        a=index[cid].get("companion_numerical_source_audit",{})
        require(a.get("audit_file")=="companion_crosscheck_ch02_01_11.json"
                and a.get("status")=="key_answer_value_crosschecked_not_full_proof_verified",
                f"ch2 source crosscheck index not bidirectional {n}")
        require(a.get("scanned_companion_pdf_pages")==x["companion_pdf_physical_pages"]
                and all(type(pg)==int and 1<=pg<=402
                        for pg in x["companion_pdf_physical_pages"]),
                f"invalid S PDF page or wrong ch2 provenance {n}")
        require(math.isclose(models[n],x["independent_computed_value"],
                             rel_tol=.01,abs_tol=1e-12),
                f"physics S sourced ch2 model incorrectly calculated {n}")
        require(x["exam_ready"] is False and
                x["academic_review"]=="pending_independent_verification",
                f"ch2 S source falsely marked admitted {n}")
        if n in ["2.1","2.8","2.10"]:
            require(x["companion_rounded_value"] is None and
                    x["crosscheck"]==
                        "source_symbolic_formula_checked_with_independent_test_parameters",
                    f"ch2 original {n} reviewer-created numerical sample wrongly claimed as source")
    require(set(models)==seen, "ch2 S source original numbers not exhaustive1-11")
    flags={x["source_problem_number"]:x["discrepancy_note"] for x in rows}
    require("small-angle" in flags["2.6"].lower(),
            "ch2.6 source small-slope approximation not recorded")
    return len(rows)




def check_companion_ch2_remaining_crosscheck() -> int:
    """Chapter2 existing originals2.12--2.28: 10 scanned values,7 formulas."""
    p=ROOT/"companion_crosscheck_ch02_12_28.json"
    require(p.is_file(), "missing S-scan chapter2 second-half source audit")
    d=json.loads(p.read_text(encoding="utf-8"))
    rows=d["records"]
    require(len(rows)==17 and d["summary"]["reviewed_distinct_existing_pairs"]==17,
            "chapter2 second-half source crosscheck must cover17 originals")
    require(d["summary"]["reviewed_numeric_source_answers"]==10 and
            d["summary"]["reviewed_symbolic_source_formulas"]==7,
            "S source original vs reviewer test numbers improperly mixed")
    require(d["source"]["sha256"] ==
            "54126dd75edd65eb9ead0a9d7acb96a37bfb25674cf595c76b94f2fb30bce5a7",
            "S scanned 402-page source fingerprint changed")
    G=6.67e-11
    g=9.8
    models={
      "2.12":4*math.pi**2*(1.07e9)**3/(G*(7.16*86400)**2),
      "2.13":4*math.pi**2*(1.36e8)**3/(G*(14.2*3600)**2),
      "2.14":math.sqrt(3*math.pi/(G*3e3)),
      "2.15":(2/3)*math.pi*G*(1.3e3)**2*(7e7)**2/1.013e5,
      "2.16":2*math.pi*math.sqrt(math.sqrt(3)*(1e9)**3/(G*1e30)),
      "2.17":1.5e11*(5.98e24/(3*1.99e30))**(1/3)/1000,
      "2.18":2/(1+(.1*2/1)*3),
      "2.19":.5*.012*(2*math.pi*5e4/60)**2*(.02+.1),
      "2.20":(2*math.pi*400/60)**2*5.97/(2*g),
      "2.21":1/(2*math.pi)*math.sqrt(
          ((math.sin(math.pi/6)-.2*math.cos(math.pi/6))*g)/
          ((math.cos(math.pi/6)+.2*math.sin(math.pi/6))*1)),
      "2.22":(2*1+1*(1+1))*2**2,
      "2.23":math.sqrt(2*(7-.5*g)*2),
      "2.24":math.sqrt(g/1800),
      "2.25":math.sqrt(g/1),
      "2.26":.5*.016*.062*math.pi*25**2*40**2,
      "2.27":1*g/1,
      "2.28":(.10-.05)/(4*math.pi*.02)
    }
    require(len(models)==17, "chapter2 remaining source model count failure")
    original=json.loads(REGISTER.read_text(encoding="utf-8"))
    by_id={item["canonical_id"]:item for item in original["entries"]}
    require(len(by_id)==705, "original main formal count changed")
    own_params={"2.16","2.18","2.21","2.22","2.25","2.27","2.28"}
    seen=set()
    for item in rows:
        n=item["source_problem_number"]
        require(n in models and n not in seen,
                f"original ch2 second half source missing or duplicated {n}")
        seen.add(n)
        cid=f"ZS4-02-{int(n.split('.')[1]):03d}"
        require(item["canonical_id"]==cid and cid in by_id,
                f"S original source stable canonical ID changed {n}")
        x=by_id[cid]
        a=x.get("companion_numerical_source_audit",{})
        require(a.get("audit_file")=="companion_crosscheck_ch02_12_28.json"
                and a.get("status")=="key_answer_value_crosschecked_not_full_proof_verified"
                and a.get("scanned_companion_pdf_pages")==
                    item["companion_pdf_physical_pages"],
                f"original source S ch2 scan provenance wrong {n}")
        require(item["companion_pdf_physical_pages"] and
                all(type(pg) is int and 1<=pg<=402
                    for pg in item["companion_pdf_physical_pages"]),
                f"ch2 scan physical page invalid {n}")
        require(math.isclose(item["independent_computed_value"],models[n],
                             rel_tol=.005,abs_tol=1e-12),
                f"ch2 S-companion independently checked model value wrong {n}")
        require(item["exam_ready"] is False and
                item["academic_review"]=="pending_independent_verification",
                f"source crosscheck must not certify review or originality {n}")
        if n in own_params:
            require(item["companion_rounded_value"] is None and
                    item["crosscheck"]==
                      "source_symbolic_formula_checked_with_independent_test_parameters",
                    f"ch2 {n}: reviewer samples falsely attributed to scanned source")
        else:
            require(item["companion_rounded_value"] is not None,
                    f"ch2 {n}: source actual numeric no longer checked")
    require(set(models)==seen, "chapter2 2.12--2.28 source crosschecks incomplete")
    sol=(ROOT/"chapters/02/solutions.tex").read_text(encoding="utf-8")
    require("严格局部极小值" in sol and "四阶有效势" in sol
            and "S PDF物理页41--42" in sol,
            "ch2.25 equality critical threshold requires quartic energy stability analysis")
    require(any("SOURCE_STABILITY_CONCLUSION_QUESTIONABLE" in
                x["discrepancy_note"] for x in rows),
            "critical rotating hoop source disagreement not traceable")
    return len(rows)




def check_companion_ch3_crosscheck() -> int:
    """S scan ch3 problems3.1--3.24: 18 numeric values +6 analytical formulas."""
    path=ROOT/"companion_crosscheck_ch03_01_24.json"
    require(path.is_file(), "missing chapter3 S companion source audit")
    d=json.loads(path.read_text(encoding="utf-8"))
    rows=d["records"]
    require(len(rows)==24 and d["summary"]["reviewed_distinct_existing_pairs"]==24,
            "S scanned third chapter not all 24 problems audited")
    require(d["summary"]["reviewed_numeric_source_answers"]==18
            and d["summary"]["reviewed_symbolic_source_formulas"]==6,
            "S ch3 formulas versus printed values mislabeled")
    require(d["source"]["sha256"]==
            "54126dd75edd65eb9ead0a9d7acb96a37bfb25674cf595c76b94f2fb30bce5a7",
            "chapter3 original S scan fingerprint changed")
    g=9.8
    G=6.67e-11
    pi=math.pi
    m0=2.72e6
    md=1290.
    burnout=155.
    mf=m0-md*burnout
    vals={
        "3.1":-2*.1/4,
        "3.2":math.sqrt(2)*.05*20,
        "3.3":150*(g+math.sqrt(2*g*5)/.3),
        "3.4":120/60*.0079*735,
        "3.5":1.29*22.5*2.62*38**2,
        "3.6":3e3*10*math.sqrt(2),
        "3.7":2*3*g+2*2**2,
        "3.8":3*.8*2*g,
        "3.9":math.hypot(9.22,5.33)*1e-21,
        "3.10":7600-150/440*910,
        "3.11":math.sqrt(2*.8*g*25),
        "3.12":105+253*math.log(6090/6010),
        "3.13":1-math.exp(-1),
        "3.14":5.5e4*(burnout-mf/md*math.log(m0/mf))-.5*g*burnout**2,
        "3.15":(75+3)*490-75*210,
        "3.16":2*.0958*math.cos(math.radians(105/2))/18,
        "3.17":4/(3*pi),
        "3.18":pi/(4*(16-pi)),
        "3.19":g*(2-5/7),
        "3.20":8.75e10*5.46e4/908,
        "3.21":2*pi*7.35e22*(3.82e8)**2/(27.3*86400),
        "3.22":pi*(6378+205.5+6378+35835.7)*math.sqrt(
            (6378+35835.7)/(6378+205.5))/10.2,
        "3.23":2.,
        "3.24":.75
    }
    require(len(vals)==24, "third chapter S source spotmodel size error")
    own={"3.1","3.7","3.8","3.17","3.19","3.23"}
    reg={x["canonical_id"]:x for x in json.loads(
         REGISTER.read_text(encoding="utf-8"))["entries"]}
    require(len(reg)==705, "new crosschecks cannot enlarge original formal count")
    seen=set()
    for row in rows:
        n=row["source_problem_number"]
        require(n in vals and n not in seen, f"S scanned ch3 original duplicates {n}")
        seen.add(n)
        cid=f"ZS4-03-{int(n.split('.')[1]):03d}"
        require(row["canonical_id"]==cid and cid in reg,
                f"S scanned ch3 original canonical mapping wrong {n}")
        link=reg[cid].get("companion_numerical_source_audit",{})
        require(link.get("audit_file")=="companion_crosscheck_ch03_01_24.json"
            and link.get("scanned_companion_pdf_pages")==
                 row["companion_pdf_physical_pages"]
            and link.get("status")=="key_answer_value_crosschecked_not_full_proof_verified",
            f"S ch3 source audit link broken {n}")
        require(row["companion_pdf_physical_pages"] and
                all(type(pg) is int and 1<=pg<=402
                    for pg in row["companion_pdf_physical_pages"]),
                f"missing S 402-page PDF original problem location {n}")
        require(math.isclose(row["independent_computed_value"],vals[n],
                             rel_tol=.006,abs_tol=1e-18),
                f"original S ch3 model numeric failed {n}")
        require(row["exam_ready"] is False and
                row["academic_review"]=="pending_independent_verification",
                f"ch3 S source check is not expert academic approval {n}")
        if n in own:
            require(row["companion_rounded_value"] is None and
                row["crosscheck"]==
                  "source_symbolic_formula_checked_with_independent_test_parameters",
                f"S ch3 formula {n} incorrectly attributed reviewer sample to source")
        else:
            require(row["companion_rounded_value"] is not None,
                    f"original S source numeric value absent at {n}")
    require(set(vals)==seen, "S ch3 24 original source numbers not exhaustive")
    flags={x["source_problem_number"]:x["discrepancy_note"] for x in rows}
    require("FINITE_BATCH_VS_CONTINUOUS_EXHAUST" in flags["3.12"]
            and "SOURCE_NUMERIC_DISAGREEMENT" in flags["3.14"]
            and "COORDINATE_REFERENCE" in flags["3.18"],
            "original source-model disagreements ch3 must be flagged")
    sol=(ROOT/"chapters/03/solutions.tex").read_text(encoding="utf-8")
    require("108.3455" in sol and "有限喷出质量" in sol,
            "3.12 continuous-exhaust equation and one-shot distinction missing")
    require("203.59" in sol and "172" in sol,
            "3.14 original source reported172km vs exact-integral203.59km lost")
    return len(rows)


def main() -> None:
    raw = json.loads(REGISTER.read_text(encoding="utf-8"))
    require(raw.get("schema") == "zhang-sanhui-4e-exercise-intake/v1",
            "wrong register schema")
    pages = {x["id"]: x["pdf_page_count"] for x in raw["source_files"]}
    require(all(pages[x] > 0 for x in ("V1", "V2", "S")), "missing PDF inventory")
    entries = raw["entries"]
    ids = [x["source_problem_number"] for x in entries]
    stable = [x["canonical_id"] for x in entries]
    require(len(ids) == len(set(ids)), "duplicate original problem number")
    require(len(stable) == len(set(stable)), "duplicate canonical ID")
    require(raw["progress"]["verified_questions"] == len(entries),
            "progress count differs from register")
    for row in entries:
        num = row["source_problem_number"]
        chapter, item = map(int, num.split("."))
        require(row["canonical_id"] ==
                f"ZS4-{chapter:02d}-{item:03d}", f"unstable ID: {num}")
        require(row["exam_ready"] is False, f"unsafe exam admission: {num}")
        require(row["academic_review"] == CANDIDATE_STATUS,
                f"fake expert clearance: {num}")
        require(row["question_status"] == "transcribed_from_pdf_scan",
                f"not actually transcribed: {num}")
        require(row["solution_status"] == "independent_derivation_written",
                f"missing original solution: {num}")
        v = row["volume"]
        require(v in ("V1", "V2"), f"wrong book: {num}")
        for p in row["textbook_pdf_pages"]:
            require(isinstance(p,int) and 1 <= p <= pages[v],
                    f"invalid textbook page: {num} page {p}")
        for p in row["supplement_pdf_pages"]:
            require(isinstance(p,int) and 1 <= p <= pages["S"],
                    f"invalid supplement page: {num} page {p}")
    reported = []
    for ch in raw["chapters"]:
        qpath, spath = ch.get("question_file"), ch.get("solution_file")
        if qpath is None and spath is None:
            require(ch.get("verified_exercise_count",0) == 0,
                    f"chapter without files claims entries: {ch['number']}")
            continue
        require(qpath and spath, f"half-created chapter: {ch['number']}")
        qs = check_latex_fragment(ROOT / qpath, "questions")
        ss = check_latex_fragment(ROOT / spath, "solutions")
        expected = [num for num in ids if int(num.split(".")[0]) == ch["number"]]
        require(qs == ss == expected,
                f"source/solution/register ordering mismatch in chapter {ch['number']}"
                f": questions={qs}; solutions={ss}; register={expected}")
        require(ch["verified_exercise_count"] == len(qs),
                f"chapter count mismatch: {ch['number']}")
        reported.extend(qs)
    require(Counter(reported) == Counter(ids),
            "unindexed exercises or missing fragment sections")
    # Guard previously discovered source transcription regressions.
    ch4q = (ROOT / "chapters/04/questions.tex").read_text(encoding="utf-8")
    ch13q = (ROOT / "chapters/13/questions.tex").read_text(encoding="utf-8")
    # End-of-chapter exercise 4.8 is NOT the separate thought-question 4.8.
    sec4_8 = ch4q.split(r"\paragraph{习题 4.8}", 1)[1].split(
        r"\paragraph{习题 4.9}", 1)[0]
    require("一竖直悬挂的弹簧" in sec4_8,
            "4.8 chapter exercise confused with thought question")
    require("两个相同的钯核" in ch13q and "两个相同的铯核" not in ch13q,
            "13.29 nuclear species must be Pd Z=46, not Cs Z=55")
    require("单数圆筒和双数圆筒分别" in ch13q,
            "13.22 alternating AC cylinder wiring missing")
    require("1\\,\\mathrm{kg}" not in sec4_8,
            "unexpected spurious content in spring exercise")

    ch5q=(ROOT/"chapters/05/questions.tex").read_text(encoding="utf-8")
    ch5s=(ROOT/"chapters/05/solutions.tex").read_text(encoding="utf-8")
    ch14q=(ROOT/"chapters/14/questions.tex").read_text(encoding="utf-8")
    ch14s=(ROOT/"chapters/14/solutions.tex").read_text(encoding="utf-8")
    require("71\\,\\mathrm{nm}" in ch5q,
            "Source chapter 5.6 diameter must remain as printed (71 nm)")
    require("104.91" in ch5s and "\\boxed{\\theta=2\\arctan" in ch5s,
            "5.5 full HOH bond angle must be recorded")
    require("7.3\\times10^{18}" in ch5s,
            "5.22 textbook companion 2004 energy source omitted")
    require("绝缘传送带" in ch14q,
            "14.8 belt is insulating, not conducting")
    require("E_{\\rm belt}" in ch14s
            and "\\frac{|\\sigma_{\\rm belt}|}{2\\varepsilon_0}" in ch14s,
            "14.8 insulating sheet field factor 1/2 omitted")

    # Newly discovered source-scan transcription regression guards.
    q6=(ROOT/"chapters/06/questions.tex").read_text(encoding="utf-8")
    s6=(ROOT/"chapters/06/solutions.tex").read_text(encoding="utf-8")
    q15=(ROOT/"chapters/15/questions.tex").read_text(encoding="utf-8")
    s15=(ROOT/"chapters/15/solutions.tex").read_text(encoding="utf-8")
    require("零点且上升" in q6 and "两均匀长木板" not in q6,
            "6.3 zero-crossing or 6.16 one-board source wording regressed")
    require("\\frac32 h\\nu" in s6 and "1.63\\times10^{-11}" in s6,
            "6.21 original companion energy 3/2 hnu missing")
    require("310.6" in s6 and "1.80\\times10^4" in s6,
            "6.22 damping and 6.27 Lissajous analyses omitted")
    require("15.30" in q15 and "15.30" in s15,
            "chapter15 missing end exercise")
    require("-3.75\\times10^3" in s15,
            "15.2 layered dielectric voltage source regression")
    require("2.33333333333e-10" not in q15,
            "chapter15 questions accidentally contaminated by QA numerics")

    # Source-number and risk regression checks for the new wave/current chapters.
    q7=(ROOT/"chapters/07/questions.tex").read_text(encoding="utf-8")
    a7=(ROOT/"chapters/07/solutions.tex").read_text(encoding="utf-8")
    q16=(ROOT/"chapters/16/questions.tex").read_text(encoding="utf-8")
    a16=(ROOT/"chapters/16/solutions.tex").read_text(encoding="utf-8")
    require("两个分支都应讨论" in q7 and "y_-(x,t)" in a7,
            "7.2 source did not specify wave propagation direction")
    require("被猛烈地向上抛起" in q7 and "0.997" in a7,
            "7.4 thrown person height, NOT source wave amplitude")
    require("M=0.67" in a7 and "1.15\\times10^{18}" in a7,
            "7.18 source magnitude-energy formula changed")
    require("外直径" in q16 and "2.5" in q16
            and "3.09\\times10^{-4}" in a16,
            "16.5 original pipe diameters or flow split regressed")
    require("7.33" in q7 and "7.33" in a7,
            "7.33 ultrasonic motor end exercise missing")
    require("张角" in q7 and "半顶角" in a7,
            "7.26 printed ship wake opening-angle risk must be disclosed")
    require("16.18" in q16 and "16.18" in a16,
            "16.18 homogeneous conductor end exercise missing")
    require("电源正端" in a16 or "电动势正端" in a16,
            "16.11–16.12 image polarity assumption not documented")

    # New source-text risk regression for the two added chapters.
    q8=(ROOT/"chapters/08/questions.tex").read_text(encoding="utf-8")
    s8=(ROOT/"chapters/08/solutions.tex").read_text(encoding="utf-8")
    q17=(ROOT/"chapters/17/questions.tex").read_text(encoding="utf-8")
    s17=(ROOT/"chapters/17/solutions.tex").read_text(encoding="utf-8")
    require("在飞船系" in q8 and "9.00\\times10^9" in s8,
            "8.6 source first subquestion must use ship-frame reflection range")
    require("两个" in q8 and "10^{18}" in s8 and "8.23" in s8,
            "8.23 two-proton energy squared gravitational scaling missing")
    require("可资利用能" in q8 and "质心" in s8,
            "8.20–8.21 source available-energy COM model absent")
    require("17.20" in q17 and "17.20" in s17,
            "17.20 displacement current last numbered exercise missing")
    require("管截面" in q17 and "11.6" in s17,
            "17.12 windings must use MINOR toroid radius for N")
    require("横向分量" in q17 and "B_\\perp" in s17,
            "17.6 semicircle transverse Biot-Savart component discarded")

    # Chapter 9 and 18 source/model regression guards.
    q9=(ROOT/"chapters/09/questions.tex").read_text(encoding="utf-8")
    s9=(ROOT/"chapters/09/solutions.tex").read_text(encoding="utf-8")
    q18=(ROOT/"chapters/18/questions.tex").read_text(encoding="utf-8")
    s18=(ROOT/"chapters/18/solutions.tex").read_text(encoding="utf-8")
    require("9.29" in q9 and "9.29" in s9,
            "ch9 ending Knudsen wall heat-conduction exercise missing")
    require("佩兰" in q9 and "7.10" in s9,
            "9.24 Perrin experiment source counts/independent result absent")
    require("冷却" in q9 and "87.3" in s9,
            "9.2 Newton cooling correct total elapsed minutes regressed")
    require("9.27" in q9 and "9.55\\times10^{-5}" in s9
            and "7.23\\times10^6" in s9 and "0.198" in s9,
            "9.27 companion S p153 critical values and source calculation regressed")
    require("18.30" in q18 and "18.30" in s18,
            "ch18 sodium atom magnetic energy last exercise missing")
    require("18.27" in q18 and "4.12" in s18,
            "18.27 original railgun 1.2cm spacing 6.7cm radius/current source mismatch")
    require("向心" in s18 or "圆周" in s18,
            "Lorentz force directions and circular motion source formula dropped")
    require("电磁场" in s18 and "动量守恒" in s18,
            "18.29 missing field momentum conservation")

    # New original-source chapter 10/19 candidate safeguards.
    q10=(ROOT/"chapters/10/questions.tex").read_text(encoding="utf-8")
    s10=(ROOT/"chapters/10/solutions.tex").read_text(encoding="utf-8")
    q19=(ROOT/"chapters/19/questions.tex").read_text(encoding="utf-8")
    s19=(ROOT/"chapters/19/solutions.tex").read_text(encoding="utf-8")
    require("10.26" in q10 and "10.26" in s10,
            "ch10 ending reversed Stirling question/solution missing")
    require("10.9" in q10 and "10.9" in s10
            and "10" in q10 and "30" in q10,
            "10.9 cylinder free expansion original 20-to-30L model missing")
    require("理想再生器" in s10 and "no" in s10,
            "10.26 refrigerator regenerative and unregenerated regimes missing")
    require("19.14" in q19 and "19.14" in s19,
            "ch19 final 14 numbered end exercises incomplete")
    require("2.60" in s19 and "220" in s19,
            "19.9 exact companion H220 B-H source check regressed")
    require("0.213" in s19 and "170" in s19,
            "19.10 exact companion H170 source check regressed")
    require("3.14" in s19 and "5.03" in s19,
            "19.11 coercive inner-edge onset vs full cross-section caveat missing")

    # New source-specific regression guards for the final V1 chapter and EM induction.
    q11=(ROOT/"chapters/11/questions.tex").read_text(encoding="utf-8")
    s11=(ROOT/"chapters/11/solutions.tex").read_text(encoding="utf-8")
    q20=(ROOT/"chapters/20/questions.tex").read_text(encoding="utf-8")
    s20=(ROOT/"chapters/20/solutions.tex").read_text(encoding="utf-8")
    require("氧气" in q11 and "刚性双原子" in q11
            and "23.54" in s11,
            "11.1 OXYGEN five degrees i=5 source must not revert to He")
    require("质量变成相等" in q11 and "0.9" in s11,
            "11.8 initial 2.5kg water +0.7kg ice freeze only0.9kg")
    require("节流" in q11 and "等焓" in s11 and "等熵" in s11
            and "95" in s11 and "反向" in s11,
            "11.13 original throttling and reversible adiabatic differ from companion")
    require("20.27" in q20 and "20.27" in s20,
            "ch20 27 exercises must include nested solenoid force")
    require(r"4\times10^3" in q20,
            "20.2 original 4000 turns source regression")
    require("0.9" in s11 and "2.68" in s11,
            "11.2 approximate entropy erroneous exact four steps check")
    require("南翼尖" in s20 and "0.30" in s20,
            "20.6 wing polarity and 0.30V source answer absent")
    require("2A'_m" in s20 or "2A'_m" in s20.replace(" ", ""),
            "20.26 constant current source supplies double mechanical energy")

    # Ch21 risk locks: source values and independently discovered companion issues.
    q21=(ROOT/"chapters/21/questions.tex").read_text(encoding="utf-8")
    s21=(ROOT/"chapters/21/solutions.tex").read_text(encoding="utf-8")
    require("21.17" in q21 and "21.17" in s21,
            "21.17 radiation-gravity end exercise missing")
    require("0.26" in q21 and "6.2\\times10^4" in s21
            and "相干" in s21,
            "21.7 original diameter/coherent radiation source issue missing")
    require("2\\langle S\\rangle" in s21,
            "21.9 amplitude versus averaged intensity missing factor two")
    require("-I^2R" in s21 and "向内" in s21,
            "21.11 negative outward Poynting flux missing")

    q22=(ROOT/"chapters/22/questions.tex").read_text(encoding="utf-8")
    s22=(ROOT/"chapters/22/solutions.tex").read_text(encoding="utf-8")
    require("22.23" in q22 and "22.23" in s22,
            "ch22 gas interferometer last exercise missing")
    require("镜面反射" in s22 and "45" in s22,
            "22.3 Lloyd mirror half-wave first bright missing")
    require("第7条" in q22 and "反射暗纹" in q22 and "1.28" in s22,
            "22.14 SiO2 wedge seventh dark with BOTH phase shifts missing")
    require("再次" in q22 and "643" in s22,
            "22.17 consecutive oil-film destructive orders missing")
    require("单程" in s22 and "1.000289" in s22,
            "22.23 single-pass gas-cell index correction missing")

    q23=(ROOT/"chapters/23/questions.tex").read_text(encoding="utf-8")
    s23=(ROOT/"chapters/23/solutions.tex").read_text(encoding="utf-8")
    require("23.19" in q23 and "23.19" in s23,
            "chapter23 final electron diffraction exercise missing")
    require("第3级" in q23 and "429" in s23,
            "23.3 third vs second bright ~429nm source regression")
    require("47.16" in s23 and "单缝" in s23,
            "23.4 harbor single slit not circular rayleigh factor")
    require("3647" in s23 and "3646" in s23,
            "23.16 mandatory integer ceiling and companion discrepancy")
    require("旁瓣" in s23 and "主极大" in s23,
            "23.17 sidelobe vs grating principal maximum distinction")

    q24=(ROOT/"chapters/24/questions.tex").read_text(encoding="utf-8")
    s24=(ROOT/"chapters/24/solutions.tex").read_text(encoding="utf-8")
    require("24.16" in q24 and "24.16" in s24,
            "ch24 final polarization gradient exercise omitted")
    require("临界角" in q24 and "35.26" in s24,
            "24.6 original TIR CRITICAL 45 not Brewster45")
    require("正交" in q24 and "3}{16}" in s24,
            "24.11 P1/P2 CROSSED, transmitted intensity 3Ii/16")
    require("半波片" in s24 and "800nm" in s24,
            "24.13 800nm quarter wave is 400nm half wave")
    require("尼科耳" in q24 and "69.2" in s24,
            "24.14 Nicol prism o ray total internal reflection")

    q25=(ROOT/"chapters/25/questions.tex").read_text(encoding="utf-8")
    s25=(ROOT/"chapters/25/solutions.tex").read_text(encoding="utf-8")
    require("25.21" in q25 and "25.21" in s25,
            "ch25 last Cassegrain exercise omitted")
    require("580" in q25 and "589" in s25 and "580" in s25,
            "25.3 main textbook 580nm must differ companion 589nm")
    require("0.691" in s25 and "0.361" in s25,
            "25.11 independently corrected eye curvature vs companion")
    require("576" in s25 and "578" in s25,
            "25.17 accurate area ratio not rounded companion result")
    require("f_{\\rm eff}=3f_1=60" in s25 and "角放大率160" in s25,
            "25.21 Cassegrain 60m EFL disagreement must remain marked")

    q26=(ROOT/"chapters/26/questions.tex").read_text(encoding="utf-8")
    s26=(ROOT/"chapters/26/solutions.tex").read_text(encoding="utf-8")
    require("26.22" in q26 and "26.22" in s26,
            "ch26 final deBroglie group velocity proof missing")
    require("频率谱" in q26 and "2.821439" in s26,
            "26.2 Wien frequency peak instead of wavelength peak")
    require("85.3" in s26 and "光电效应" in s26,
            "26.13 classical accumulation vs immediate quantum electron")
    require("69.39" in s26 and "逆康普顿" in s26,
            "26.18 head-on moving electron energy conservation")
    require("0.145" in s26 and "0.178" in s26,
            "26.20 thermal neutron mean energy convention must be disclosed")
    require("v_g=v" in s26 and "c^2/v" in s26,
            "26.22 deBroglie group vs phase velocity distinction")

    # Two more scanned source chapters with exact-number and model-discrepancy guards.
    q27=(ROOT/"chapters/27/questions.tex").read_text(encoding="utf-8")
    s27=(ROOT/"chapters/27/solutions.tex").read_text(encoding="utf-8")
    require("27.11" in q27 and "27.11" in s27,
            "27.11 H2 harmonic oscillator last problem missing")
    require("斜底" in q27 and "图27.14" in s27 and "4个内部节点" in s27,
            "27.3 sloped well figure and node count check")
    require("0.090845" in s27 and "1.60" in s27,
            "27.4 quantum first-quarter probability and27.2 huge n energy")
    q28=(ROOT/"chapters/28/questions.tex").read_text(encoding="utf-8")
    s28=(ROOT/"chapters/28/solutions.tex").read_text(encoding="utf-8")
    require("28.34" in q28 and "28.34" in s28,
            "28.34 CO oscillator original last exercise missing")
    require("Lyman" in q28 and "Lyman" in s28 and "Balmer系" in s28,
            "28.16 source specifies LYMAN, must distinguish Balmer")
    require("3.60" in s28 and "0.36" in s28 and "笔误" in s28,
            "28.29 S382 laser pulse millimeters mismatch not flagged")
    require("两个电子云" in q28 and "34" in s28 and "室温" in s28,
            "28.33 two H electron-cloud spheres internuclear rotation model")
    require("3d^{10}" in s28 and "4s^1" in s28,
            "28.21 Cu ground state configuration closed d orbital")
    require("FWHM" in s28 and "sigma" in s28,
            "28.9 and28.10 spectral linewidth conventions should be explicit")

    q29=(ROOT/"chapters/29/questions.tex").read_text(encoding="utf-8")
    s29=(ROOT/"chapters/29/solutions.tex").read_text(encoding="utf-8")
    require("29.14" in q29 and "29.14" in s29,
            "29.14 KCl final original chapter exercise missing")
    require("0.045" in q29 and "27.6" in s29 and "1.2" in s29,
            "29.11 donor shallow energy not full bandgap source")
    require("4.07" in s29 and "52.6" in s29,
            "29.7 classical vs Fermi free paths contrast")
    require("0.900" in s29 and "1.70" in s29,
            "29.6 potassium electronic heat capacity EF and crossing")

    q30=(ROOT/"chapters/30/questions.tex").read_text(encoding="utf-8")
    s30=(ROOT/"chapters/30/solutions.tex").read_text(encoding="utf-8")
    require("30.22" in q30 and "30.22" in s30,
            "last original nuclear CNO cycle exercise30.22 missing")
    require("0.42" in s30 and "0.0194" in s30 and "自屏蔽" in s30,
            "30.17 companion thin cobalt source rate exceeds neutron supply")
    require("162" in s30 and "51" in s30 and "指数式" in s30,
            "30.18 Cd95percent neutron optical thickness source error guard")
    require("9.66" in s30 and "中性原子" in s30 and "核质量" in s30,
            "30.16 zinc vs nickel nuclear mass and atomic electron conventions")
    require("24.69" in s30 and "26.73" in s30 and "湮灭" in s30,
            "30.22 CNO energy without/with positron annihilation")

    thought_count = check_thought_intake()
    S_selected_count = check_companion_selected_thought()
    checked_source_ch1 = check_companion_ch1_crosscheck()
    checked_source_ch2 = check_companion_ch2_crosscheck()
    checked_source_ch2_rest = check_companion_ch2_remaining_crosscheck()
    checked_source_ch3 = check_companion_ch3_crosscheck()
    computed = check_numeric_spotmodels()
    print(f"PASS: {len(ids)} candidate exercises have unique IDs, "
          "paired TeX sections, source pages and no exam admission.")
    print(f"PASS: {thought_count} separately numbered and unapproved thought Q/A pairs. Original 705 exercises unchanged.")
    print(f"PASS: {S_selected_count} S-source selected V1 thought Q/A pairs, source V1 primary not verified.")
    print(f"PASS: {checked_source_ch1} existing original chapter1 exercises S-companion source-value checked; two documented risks.")
    print(f"PASS: {checked_source_ch2} chapter2 S-companion original model/source spotchecks; 8 printed results and 3 symbolic cases.")
    print(f"PASS: {checked_source_ch2_rest} remaining chapter2 original source checks; all28 now covered.")
    print(f"PASS: {checked_source_ch3} third-chapter original S-source spotchecks; 18 actual numeric+6 symbolic.")
    print(f"PASS: {computed+checked_source_ch1+checked_source_ch2+checked_source_ch2_rest+checked_source_ch3} numerical/source-model checks (663+26+11+17+24).")
    print("NOT VERIFIED: full source transcription accuracy, external expert "
          "review, source permissions and independent physical model sufficiency.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
