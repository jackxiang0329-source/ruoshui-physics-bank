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

    return 136


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
