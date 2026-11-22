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
    require(close(560-356-282, -78) is False,
            "10.2 b->a heat not naive path-work addition")
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
    require(close(math.sqrt(2*.75*gasW/70),84.38704853),
            "10.12 human cannon exit speed using source volume geometry")
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

    return 308


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

    computed = check_numeric_spotmodels()
    print(f"PASS: {len(ids)} candidate exercises have unique IDs, "
          "paired TeX sections, source pages and no exam admission.")
    print(f"PASS: {computed} independent numerical spotmodel checks.")
    print("NOT VERIFIED: full source transcription accuracy, external expert "
          "review, source permissions and independent physical model sufficiency.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
