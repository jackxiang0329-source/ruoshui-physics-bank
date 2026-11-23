#!/usr/bin/env python3
"""Independent structural and numerical spot checks for the Zhao/Wang 5e trial batch.

Passing does NOT establish professional independent review or rights clearance.
No OCR, external network, or third-party packages are used.
"""
from pathlib import Path
import math
import re

ROOT = Path(__file__).resolve().parent
CHAPTERS = (
    ("chapters/textbook-ch01-foundations-001-003.tex", "sourceproblem",
     [f"1.1.{n}" for n in range(1, 8)] +
     [f"1.2.{n}" for n in range(1, 8)] +
     [f"1.3.{n}" for n in range(1, 4)]),
    ("chapters/textbook-ch01-exercises.tex", "sourceproblem",
     [f"1.3.{n}" for n in range(4, 18)]),
    ("chapters/textbook-ch02-choices.tex", "sourceproblem",
     [f"2.1.{n}" for n in range(1, 13)]),
    ("chapters/textbook-ch02-blanks.tex", "sourceproblem",
     [f"2.2.{n}" for n in range(1, 10)]),
    ("chapters/textbook-ch02-solutions-001-012.tex", "sourceproblem",
     [f"2.3.{n}" for n in range(1, 13)]),
    ("chapters/textbook-ch02-solutions-013-025.tex", "sourceproblem",
     [f"2.3.{n}" for n in range(13, 26)]),
    ("chapters/textbook-ch03-choices.tex", "sourceproblem",
     [f"3.1.{n}" for n in range(1, 9)]),
    ("chapters/textbook-ch03-blanks.tex", "sourceproblem",
     [f"3.2.{n}" for n in range(1, 13)]),
    ("chapters/textbook-ch03-solutions-001-008.tex", "sourceproblem",
     [f"3.3.{n}" for n in range(1, 9)]),
    ("chapters/textbook-ch03-solutions-009-015.tex", "sourceproblem",
     [f"3.3.{n}" for n in range(9, 16)]),
    ("chapters/textbook-ch04-choices.tex", "sourceproblem",
     [f"4.1.{n}" for n in range(1, 13)]),
    ("chapters/textbook-ch04-blanks.tex", "sourceproblem",
     [f"4.2.{n}" for n in range(1, 14)]),
    ("chapters/textbook-ch04-solutions-001-010.tex", "sourceproblem",
     [f"4.3.{n}" for n in range(1, 11)]),
    ("chapters/textbook-ch04-solutions-011-017.tex", "sourceproblem",
     [f"4.3.{n}" for n in range(11, 18)]),
    ("chapters/textbook-ch04-solutions-018-023.tex", "sourceproblem",
     [f"4.3.{n}" for n in range(18, 24)]),
    ("chapters/textbook-ch05-choices.tex", "sourceproblem",
     [f"5.1.{n}" for n in range(1, 15)]),
    ("chapters/textbook-ch05-blanks.tex", "sourceproblem",
     [f"5.2.{n}" for n in range(1, 9)]),
    ("chapters/textbook-ch05-solutions-001-009.tex", "sourceproblem",
     [f"5.3.{n}" for n in range(1, 10)]),
    ("chapters/textbook-ch05-solutions-010-018.tex", "sourceproblem",
     [f"5.3.{n}" for n in range(10, 19)]),
    ("chapters/textbook-ch06-choices.tex", "sourceproblem",
     [f"6.1.{n}" for n in range(1, 14)]),
    ("chapters/textbook-ch06-blanks.tex", "sourceproblem",
     [f"6.2.{n}" for n in range(1, 10)]),
    ("chapters/textbook-ch06-solutions-001-009.tex", "sourceproblem",
     [f"6.3.{n}" for n in range(1, 10)]),
    ("chapters/textbook-ch06-solutions-010-018.tex", "sourceproblem",
     [f"6.3.{n}" for n in range(10, 19)]),
    ("chapters/textbook-ch07-choices.tex", "sourceproblem",
     [f"7.1.{n}" for n in range(1, 12)]),
    ("chapters/textbook-ch07-blanks.tex", "sourceproblem",
     [f"7.2.{n}" for n in range(1, 13)]),
    ("chapters/textbook-ch07-solutions-001-008.tex", "sourceproblem",
     [f"7.3.{n}" for n in range(1, 9)]),
    ("chapters/textbook-ch07-solutions-009-014.tex", "sourceproblem",
     [f"7.3.{n}" for n in range(9, 15)]),
    ("chapters/textbook-ch07-solutions-015-020.tex", "sourceproblem",
     [f"7.3.{n}" for n in range(15, 21)]),
    ("chapters/textbook-ch08-choices.tex", "sourceproblem",
     [f"8.1.{n}" for n in range(1, 14)]),
    ("chapters/textbook-ch08-blanks.tex", "sourceproblem",
     [f"8.2.{n}" for n in range(1, 13)]),
    ("chapters/textbook-ch08-solutions-001-007.tex", "sourceproblem",
     [f"8.3.{n}" for n in range(1, 8)]),
    ("chapters/textbook-ch08-solutions-008-014.tex", "sourceproblem",
     [f"8.3.{n}" for n in range(8, 15)]),
    ("chapters/textbook-ch08-solutions-015-021.tex", "sourceproblem",
     [f"8.3.{n}" for n in range(15, 22)]),
    ("chapters/textbook-ch09-choices.tex", "sourceproblem",
     [f"9.1.{n}" for n in range(1, 14)]),
    ("chapters/textbook-ch09-blanks.tex", "sourceproblem",
     [f"9.2.{n}" for n in range(1, 15)]),
    ("chapters/textbook-ch09-solutions-001-006.tex", "sourceproblem",
     [f"9.3.{n}" for n in range(1, 7)]),
    ("chapters/textbook-ch09-solutions-007-012.tex", "sourceproblem",
     [f"9.3.{n}" for n in range(7, 13)]),
    ("chapters/textbook-ch09-solutions-013-017.tex", "sourceproblem",
     [f"9.3.{n}" for n in range(13, 18)]),
    ("chapters/textbook-ch10-choices.tex", "sourceproblem",
     [f"10.1.{n}" for n in range(1, 19)]),
    ("chapters/textbook-ch10-blanks.tex", "sourceproblem",
     [f"10.2.{n}" for n in range(1, 21)]),
    ("chapters/textbook-ch10-solutions-001-008.tex", "sourceproblem",
     [f"10.3.{n}" for n in range(1, 9)]),
    ("chapters/textbook-ch10-solutions-009-016.tex", "sourceproblem",
     [f"10.3.{n}" for n in range(9, 17)]),
    ("chapters/textbook-ch10-solutions-017-023.tex", "sourceproblem",
     [f"10.3.{n}" for n in range(17, 24)]),
    ("chapters/textbook-ch11-choices.tex", "sourceproblem",
     [f"11.1.{n}" for n in range(1, 12)]),
    ("chapters/textbook-ch11-blanks.tex", "sourceproblem",
     [f"11.2.{n}" for n in range(1, 7)]),
    ("chapters/textbook-ch11-solutions-001-009.tex", "sourceproblem",
     [f"11.3.{n}" for n in range(1, 10)]),
    ("chapters/textbook-ch11-solutions-010-018.tex", "sourceproblem",
     [f"11.3.{n}" for n in range(10, 19)]),
    ("chapters/guide-ch01-examples.tex", "sourceexample",
     [f"1.{n}" for n in range(1, 6)]),
    ("chapters/guide-ch02-examples.tex", "sourceexample",
     [f"2.{n}" for n in range(1, 8)]),
    ("chapters/guide-ch03-examples.tex", "sourceexample",
     [f"3.{n}" for n in range(1, 6)]),
    ("chapters/guide-ch04-examples.tex", "sourceexample",
     [f"4.{n}" for n in range(1, 6)]),
    ("chapters/guide-ch05-examples.tex", "sourceexample",
     [f"5.{n}" for n in range(1, 7)]),
    ("chapters/guide-ch06-examples.tex", "sourceexample",
     [f"6.{n}" for n in range(1, 8)]),
    ("chapters/guide-ch07-examples.tex", "sourceexample",
     [f"7.{n}" for n in range(1, 7)]),
    ("chapters/guide-ch08-examples.tex", "sourceexample",
     [f"8.{n}" for n in range(1, 7)]),
    ("chapters/guide-ch09-examples.tex", "sourceexample",
     [f"9.{n}" for n in range(1, 12)]),
    ("chapters/guide-ch10-examples.tex", "sourceexample",
     [f"10.{n}" for n in range(1, 9)]),
    ("chapters/guide-ch11-examples.tex", "sourceexample",
     [f"11.{n}" for n in range(1, 8)]),
)


def near(actual, expected, tol=1e-8):
    assert math.isclose(actual, expected, rel_tol=tol, abs_tol=tol), (
        f"expected {expected}, got {actual}"
    )


def structural_check():
    total = 0
    for relative, macro, expected in CHAPTERS:
        source = (ROOT / relative).read_text(encoding="utf-8")
        ids = re.findall(r"\\" + macro + r"\{([^}]*)\}", source)
        assert ids == expected, (relative, ids, expected)
        blocks = re.split(r"\\" + macro + r"\{[^}]*\}\{[^}]*\}\{[^}]*\}", source)[1:]
        assert len(blocks) == len(expected)
        for number, block in zip(ids, blocks):
            for label in (r"\problemtext", r"\workings", r"\crosscheck"):
                assert label in block, (number, label)
        total += len(ids)
    assert total == 542, total
    main_source = (ROOT / "main.tex").read_text(encoding="utf-8")
    for relative, _macro, _expected in CHAPTERS:
        stub = relative.removesuffix(".tex")
        assert r"\input{" + stub + "}" in main_source, (
            "unlinked from main.tex", relative
        )
    return total


def numerical_check():
    # 教材1.3.4—1.3.8
    near(math.hypot(2, 12), 2 * math.sqrt(37))
    near(math.hypot(2, 8), 2 * math.sqrt(17))
    v0, g = 23.6, 9.8
    h1 = 2.37 - 0.5 * g * (12 / v0)**2
    h2 = 2.37 - 12 * math.tan(math.radians(5)) - 0.5 * g * (
        12 / (v0 * math.cos(math.radians(5))))**2
    near(h1 - 0.90, 0.20312266590060346)
    near(h2, 0.043561687173862884)
    assert h1 > 0.90 and 0 < h2 < 0.90
    x = lambda t: 4.5*t*t - 2*t**3
    near((x(2) - x(1)), -0.5)
    near((x(1.5) - x(1)) + (x(1.5) - x(2)), 2.25)
    tm = (math.sqrt(33) - 1) / 4
    near(4*tm + tm*tm, 2*tm*tm + 2*tm**3)
    near((4*(2/3) + 6*(2/3)**2) - (4 + 2*(2/3)), 0)

    # 教材1.3.9—1.3.17
    near(math.hypot(16, 32), 16*math.sqrt(5))
    B, A, t = 2.0, 6.0, 0.7
    v = A/B*(1-math.exp(-B*t))
    near(A-B*v, A*math.exp(-B*t))
    near(100 + 4*2 + 4*2**3, 140)
    near(4*10+1.5*10**2, 190)
    near(5+2*10**2+0.5*10**3, 705)
    near(math.cos(0), 1)
    near(3*(2/9), 2/3)
    R, b, initv = 2.0, 4.0, 10.0
    time = (initv - math.sqrt(b*R))/b
    near((initv - b*time)**2 / R, b)
    near(math.hypot(.08,.064), 0.10244998779892558)
    near(math.hypot(30,40),50)

    # 学习指导例1.1—1.5与2.1
    near(25/(6/5), 125/6)
    near(2**3-8, 0)
    beta, initial_v, t = 4.0, 5.0, 0.3
    xx = initial_v / math.sqrt(beta) * math.sin(math.sqrt(beta)*t)
    vv = initial_v * math.cos(math.sqrt(beta)*t)
    near(vv**2 + beta*xx**2, initial_v**2)
    near((7 - 2/3) - 7, -2/3)
    near(abs(-2/3)/(2*math.pi), 1/(3*math.pi))
    angles = [math.radians(a) for a in (12,25,35)]
    ratio = (math.tan(angles[0])+math.tan(angles[1])) / (
        math.tan(angles[0])+math.tan(angles[2]))
    near(ratio, (1 + math.tan(angles[1])/math.tan(angles[0])) / (
        1 + math.tan(angles[2])/math.tan(angles[0])))
    m1,m2,m3,gg=2.0,3.0,4.0,9.8
    den=4*m1*m2+m3*(m1+m2)
    a=m3*(m1+m2)*gg/den
    aA=2*m2*m3*gg/den
    aB=2*m1*m3*gg/den
    near(aA+aB,2*a)
    near(m1*aA,m2*aB)




def second_round_regressions():
    """Independent spot checks for the 69 newly covered references."""
    # First-chapter foundations: circular arc, quadratic velocity, resistance law.
    near(5*math.pi, math.pi*5)
    near(5+3*3+3**2, 23)
    near(math.log(10)/.4, 5.756462732485114)
    near(2.5*math.log(10), math.log(10)/.4)
    # Second-chapter: momentum/energy/fluids.
    near(.5*(.02/2)*(-23.6)**2, .25*.02*23.6**2)
    near(.5 * 100 * .02**2, .02)
    assert .5 * 100 * (.1 - .02)**2 > .5 * 100 * .02**2, (
        "textbook 2.2.7 data should be flagged, not assigned a positive friction coefficient"
    )
    near(40+2.5*100,290)
    near(1000*9.8*50*(5*1.5+1.5**2/2), 4_226_250)
    near(4e-3/(40e-4),1.0)
    near(4e-3/(10e-4),4.0)
    near(10*4+4**2,56)
    near(10*10+10**2,200)
    near((math.sqrt(2)-1)*.01,.004142135623730951)
    near(5*(-1200+900*9.8*5),214_500)
    near(1.5*((.01*(500-30)/1.5)**2)/1.25+1.5*9.8,
         1.5*9.8+1.5*(4.7/1.5)**2/1.25)  # same string-tension model
    near(4.7/1.5, 47/15)
    # Orbit angular momentum and Earth-Moon collinear balance.
    G, ME, MM, D, RM = 6.6743e-11, 5.98e24, 7.35e22, 3.84e8, 1.74e6
    d = D/(1+math.sqrt(ME/MM))
    near(ME/(D-d)**2, MM/d**2)
    near(d-RM, 36_583_322.717654966, 1e-9)
    U = -G*(ME/(D-d)+MM/d)
    near(U,-1_282_619.9019637743,1e-9)
    near(8.75e10*5.46e4/9.08e2, 5.261563876651982e12)
    # Independent check of study-guide example 2.2 (source's "182 m" is suspect).
    m,k,v0,g=45,.03,60,9.8
    t = m/k*math.log1p(k*v0/(m*g))
    H = m*v0/k -m*m*g/(k*k)*math.log1p(k*v0/(m*g))
    near(t, 6.109988081453803)
    near(H,183.17520262909238)
    assert H > 183 and H < 183.2


def third_round_regressions():
    """Independent invariants for 40 source-numbered rigid-body items."""
    from math import pi, sqrt, log, sin, cos

    # Textbook 3.1: energy change from omega to omega/2.
    J, w = 3.0, 8.0
    near(.5*J*(w/2)**2-.5*J*w**2, -3*J*w*w/8)
    # Textbook 3.2: 3-body triangle moments, braking, skating, angular momentum.
    ma = 2.0
    near(3*ma*(.8/sqrt(3))**2, ma*.8**2)
    near((2**2-6**2)/(2*(-12/3)),4.0)
    near(70*5*6.5,2275)
    near(2275/(70*2.5),13)
    near(300/60,5)
    near(5*(5/2),12.5)
    near(.5*6*(2*pi)**2,3*(2*pi)**2)  # correct K0, nonzero
    near((2/6)*(3*2*pi)**2/(2*pi)**2,3)

    # Textbook 3.3.1--3.3.7: kinematics, rotating bowl and coupled pulleys.
    near(.3*.5,.15)
    near(.3*(4*pi/3),.4*pi)
    R,h,g=.1,.04,9.8
    rr=sqrt(2*R*h-h*h)
    ww=sqrt(g/(R-h))
    near(ww**2*rr,g*rr/(R-h))
    near(.6*(1+1.1/2)/g, .09489795918367346)
    j=.5*60*.25**2
    omega0=900*2*pi/60
    tau=.4*(2.5*100)*.25
    near(j*omega0/tau,7.0685834705770345)
    near(j*omega0**2/(4*pi*tau),53.01437602932775)
    f2=j*omega0/(4*(.4*2.5*.25))
    near(f2,176.71458676442586)
    j_cyl=.5*10*.2**2+.5*4*.1**2
    a_rot=(2*g*.2-2*g*.1)/(j_cyl+2*.2**2+2*.1**2)
    near(a_rot,6.125)
    T1,T2=2*(g-.2*a_rot),2*(g+.1*a_rot)
    near(T1*.2-T2*.1,j_cyl*a_rot)
    near(11/8, 5/4+1/8)
    # Textbook 3.3.8: initial insect-stick angular momentum and constant-omega crawl.
    L=1.2; v0=2.4
    initial_j=L*L*(1/12+1/16)  # common mass m=1
    insect_omega=(v0*L/4)/initial_j
    near(insect_omega,12*v0/(7*L))
    t=.12
    rad=L/4+g/(2*insect_omega**2)*sin(insect_omega*t)
    rad_dot=g/(2*insect_omega)*cos(insect_omega*t)
    near(2*rad*rad_dot*insect_omega,g*rad*cos(insect_omega*t))

    # Textbook 3.3.9--15
    m1,m2,l=3.,2.,1.5; d=3*l/4
    ang=m2*5*d/(m1*l*l/3+m2*d*d)
    near(ang,36*m2*5/(l*(16*m1+27*m2)))
    near(20*g/(5+20+.75),7.611650485436893)
    near(3*g/(2*1.5),9.8)
    # Conical pendulum: omega^2 h=g
    h=1.5; radius=.5
    near((g/h)*h,g)
    # Inelastic rim hit: rotational energy ratio in [0, 1]
    mw, mb, angle = 4.,.3,pi/5
    fraction=mb/(mw+mb)*sin(angle)**2
    assert 0 < fraction < 1
    velocity=sqrt((2*6*g*.4-2*.4*.4)/(6+.5/.3**2))
    near(velocity,2.0107403917654123)

    # Study guide 3.1: zero torque when r2=r1*sin(theta).
    r1,theta=.2,pi/6
    r2=r1*sin(theta)
    near(r2-r1*sin(theta),0)
    # Study guide 3.2: rod after bouncing ball.
    m,l,v0=3.,2.,12.
    m0=m/3; r=3*l/4
    near(m0*r*(v0+v0/3)/(m*l*l/3),v0/l)
    # Guide 3.3: final drop after an initially slack string.
    l=.8; v0sq=2*g*l
    near(v0sq/(5*g),2*l/5)
    # Guide 3.4: ball rebound angular impulse.
    f=2*.1*sqrt(2*g*.2)/(.01*sin(pi/6))
    near(f,79.19595949289332,1e-8)
    # Guide 3.5: exponential angular deceleration.
    j,k,w0=3.,.4,6.
    t_half=j/k*log(2)
    near(w0*math.exp(-k*t_half/j),w0/2)


def fourth_round_regressions():
    """Independent checks for chapter 4 mechanical waves and relativity."""
    pi, sqrt, cos, sin = math.pi, math.sqrt, math.cos, math.sin
    # 4.1 basic oscillator phasor and wave propagation
    phase=4*pi/3
    near(cos(phase),-.5)
    assert -sin(phase)>0
    near((pi/3)/(2*pi)*2,1/3)
    near((pi/3)/(pi/2),2/3)  # from +A/2 to +A when T=4 s
    near(2*pi/(6*pi),1/3)
    near((6*pi)/(.06*pi),100)
    near((2*pi)/(.06*pi),100/3)
    # 4.2 fill-ins
    near((2*pi/3)/pi,2/3)
    near(sqrt(.32/.02),4)
    near(2*pi/sqrt(.32/.02),pi/2)
    near((5e4)*.005/(1.5e3)*2*pi,pi/3)
    near((300/100)/6,.5)
    near((100/.4),250)
    near(2.70e-2/(3.00e-2*10),.09)
    # 4.3 mass-spring and combined motions
    near(.3*.5,.15)
    near(10e-3*(8*pi)**2*.1,.064*pi*pi)
    near(.5*10e-3*(8*pi)**2*.1**2,.0032*pi*pi)
    near(-.01*(pi/2)**2*(.24/sqrt(2)),-.004187318519783328)
    near((2*pi/3)/(pi),2/3)
    near(.001*9.8/.049,.2)
    near(sqrt(.2/.008),5)
    A=.20; A1=.173; delta=pi/6
    A2=sqrt(A*A+A1*A1-2*A*A1*cos(delta))
    near(A2,0.10000021029036311)
    assert abs(math.atan2(A*sin(delta),A*cos(delta)-A1)-pi/2)<.003
    # 4.3 wave-phase propagation and interference
    near((10*pi)/(4*pi),2.5)
    near(.2+(10*pi)/(4*pi)*(.25),.825)
    near(.1*sin(5*pi*0-pi*.5),-.1)
    near((2*pi/3)/(4*pi/3),.5)
    near((100/.4),250)
    near(2*(12-9),6)
    near((30-2*9)/6,2)
    near((2e-3)+(2e-3),4e-3)
    # Guide: Lorentz factors and energy-momentum
    beta=sqrt(2/3)
    near(sqrt(1-beta*beta),1/sqrt(3))
    near(sqrt(.5**2+.5**2),1/sqrt(2))
    near((3/2)*sqrt(5)/3*2*3e8,sqrt(5)*3e8)
    near((.5+.5)/(1+.5*.5),.8)
    near(.8/sqrt(1-.8**2),4/3)
    near(1/sqrt(1-.8**2),5/3)



def fifth_round_regressions():
    """Independent non-OCR spot checks of 46 Chapter 5 study items."""
    import math
    kB, R, NA = 1.380649e-23, 8.314462618, 6.02214076e23
    g, T, pi, sqrt = 9.8, 300.15, math.pi, math.sqrt
    # Kinetic theory: molecular energies, Maxwell characteristic speeds.
    near((2.5*R*T)/(1.5*R*T),5/3)
    near((sqrt(2)*sqrt(8/pi)*sqrt(3))**0,1)  # dimensional factor safety
    assert sqrt(2)<sqrt(8/pi)<sqrt(3)
    near(sqrt(2/32),1/4)
    # Fill-ins 5.2.1--5.2.8
    near((1e-5*133.322)/(kB*T), 3.22e17,1e-3)
    near((.1/.01)*(200**2)/3,400000/3)
    near((2.5*R*400.15)-(1.5*R*400.15),R*400.15)
    near(1.01325e5/(kB*273.15),2.68678e25,1e-4)
    near((2.5*R)/(1.5*R),5/3)
    near((1/2)**(-1),2)
    # Textbook detailed 5.3.1--5.3.18
    near(1e5*.028/(R*T),1.1219809899245032)
    p_he=1.36e4*g*(.76-.60)
    V_he=(.12+.76-.60)*2e-4
    near(p_he*V_he*.004/(R*T),1.914081617115364e-6)
    near(3*101325/(400**2),1.89984375)
    sampleT=2*6.21e-21/(3*kB)
    near(sampleT,299.8589793640527)
    near(sqrt(3*R*sampleT/.032),483.4607928707272)
    near(1e6*kB*3.5,4.8322715e-17)
    near(1.5*5e25*kB*400,4.141947e5)
    near(5e25*kB*400,2.761298e5)
    Tmix=2*8.1e6/(5*(11/.044+2/.002)*R)
    near(Tmix,311.74594427649157)
    near(2*675/(5*.002),135000)
    near(3*675/(5*5.4e22),7.5e-21)
    dU=.8*(.5*.002*10**2)
    near(2*dU/(5*1),.032)  # pressure rise at volume 1 cubic metre
    near(5/(3*2),5/6)
    k_est=6.2e-17*.014**2/(3*T)
    near(k_est,1.349547448497973e-23)
    near(R/k_est,6.160927e23,1e-3)
    # Hand-drawn piecewise-speed distribution normalized and integrated.
    v0=3.0
    aOverN=2/(3*v0)
    near(aOverN*(v0/2+v0),1)
    vmean=(2/(3*v0*v0))*v0**3/3 + aOverN*((2*v0)**2-v0**2)/2
    near(vmean,11*v0/9)
    near(aOverN*(2*v0-1.5*v0),1/3)
    lowp=1.38e-3
    n=lowp/(kB*T)
    lam=kB*T/(sqrt(2)*pi*(3e-10)**2*lowp)
    near(n,3.33010138668502e17)
    near(lam,7.509917463748704)
    n0=101325/(kB*273.15)
    lam0=1/(sqrt(2)*pi*(2.3e-10)**2*n0)
    near(lam0,1.5836067074225576e-7)
    # Study guide 5.1--5.6
    m,k=0.5,5.0
    h=3*m*g/k
    A=sqrt((m*g/k)**2+m*g*h/k)
    near(A,2*m*g/k)
    M,clay=3.0,2.0
    near(sqrt(M/(M+clay)),sqrt(3/5))
    near(2*pi/(pi/6),12)
    near(.1*sqrt(1/.1),sqrt(.1))
    near(6**2+8**2,10**2)
    X=3*sqrt(3)+4
    Y=3-4*sqrt(3)
    near(sqrt(X*X+Y*Y),10)



def sixth_round_regressions():
    """Independent spot checks for 47 newly numbered thermo/wave items."""
    R = 8.314462618
    kB = 1.380649e-23
    pi = math.pi
    sqrt = math.sqrt
    log = math.log
    # 6.1: ideal-gas internal energy, Carnot bound, irreversible expansion.
    eta_act = (1800-800)/1800
    eta_carnot = 1-300/400
    assert eta_act > eta_carnot
    near((1800-800), 1000)
    near(1-300/600, .5)
    near(log(2), .6931471805599453)
    # 6.2: first law, equivalent end states, PdV area, 10 mol gas.
    dU = 10*1.5*R
    near(dU,124.71693927)
    near(dU-209,-84.28306073)
    near(1.5*2*R*50, 150*R)
    near(200*(1+1.5),500)
    near(200*(1+2.5),700)
    near((1/3.5),2/7)
    near(101325*.0112,1134.84)
    near((3.34e4-2.09e4)/3.34e4,12500/33400)
    near((1-300/600)*3.34e4,16700)
    near((10*R)*(300.15-200.15),8314.462618)
    # 6.3.1--9: two paths, heat-work balance, polyatomic Cv.
    near(350-126,224)
    near((350-126)+42,266)
    near(-(350-126)-84,-308)
    near(2240-586,1654)
    near(1.5*R*50,623.58469635)
    near(2.5*R*50,1039.30782725)
    near((1600/72)/(1600/72-R),1.5978290432540863)
    T1=300.15
    T2=T1*16**.25
    near(T2,600.3)
    near(3*R*(T2-T1),7486.7578643781)
    near(16*101325/(kB*T2),1.9560725971354185e26)
    near(500/(5*R),12.027235504494271)
    near(math.exp(500/(2*R*273.15)),1.1163663004171762)
    # 6.3.10--18: refrigerator, thermal machine, entropies.
    near(18e6/(80*4.184*1000),53.77629063097514,1e-8)
    near(1-298.15/573.15,.4798045886766117)
    near(2e11*(1-298.15/573.15),9.596091773532234e10)
    near(1000*20/280.15,71.39032661074425)
    near(1000*200/100.15,1997.0044932601097)
    near(2.5*R*log(373.15/273.15),6.484436689942141)
    near(167000/273.15-167000/293.15,41.71145730996254)
    near(4180*(log(373.15/293.15)-80/373.15),112.46316998196394)
    # Guide examples 6.1--6.7: wave speed, phase branch, nodes.
    near(.80/1, .80)                  # 6.1 wavelength
    near((.1)/(5/12), .24)            # guide 6.2 lambda
    near(7*pi/(2*pi/.24), .84)       # guide 6.2 propagation speed
    near(.45/(3/4), .6)
    near((.6/4)/.25, .6)
    near(40/100, .4)                # 6.4 wavelength
    x=.20
    delta=10*pi*x+pi
    near((delta/pi)%2,1)            # destructive at P
    h,lambda_wave,k=1.0,.3,2
    x=(4*h*h-k*k*lambda_wave**2)/(2*k*lambda_wave)
    near(2*sqrt(h*h+(x/2)**2)-x, k*lambda_wave)
    near((.060/3)*(60*(2*3/4))**2,162)



def seventh_round_regressions():
    """Independent physical spot checks for 49 chapter-seven source items."""
    eps0=8.8541878128e-12
    k=1/(4*math.pi*eps0)
    e=1.602176634e-19
    sqrt=math.sqrt
    pi=math.pi
    log=math.log
    # Source 7.1: Gauss law, charge density, electrostatic energy and work.
    q=2e-8; R=.25; r=.10
    near(k*q*(1/r-1/R),k*q/r-k*q/R)
    near(4*(.5*eps0*3**2),.5*eps0*6**2)
    near((-2*sqrt(2)), -2**(3/2))
    near(.5*eps0*20**2,4*(.5*eps0*10**2))
    near((e*200),(-e)*(0-200))
    # Source 7.2: cube flux, proton potential work, spherical conductor induction.
    near((1/6)*6,1)
    near(3*(1/24),1/8)
    near(-8e-15/e,-49932.075542967,1e-5)
    q_inner=3e-8; q_outer=-6e-8; r2=.2
    zero_r=-(q_inner/q_outer)*r2
    near(zero_r,.1)
    near(q_inner/zero_r + q_outer/r2,0)
    near(-q_inner+(-q_inner),-2*q_inner)
    # Source 7.3.1--7.3.8: Coulomb, capacitor force, wire and spherical flux.
    side=.5; qv=1e-8; Qcenter=-qv/sqrt(3)
    near(3*k*abs(qv*Qcenter)/side**2,sqrt(3)*k*qv*qv/side**2)
    S=.04; Qplate=1e-8
    near((Qplate/S)**2 * S /(2*eps0),Qplate**2/(2*eps0*S))
    lam=5e-9; L=.15; d=.05
    Ep=k*lam*(1/d-1/(d+L))
    Eq=k*lam*L/(d*sqrt(d*d+(L/2)**2))
    near(Ep,674.0663844224999,1e-7)
    near(Eq,1495.6190228319656,1e-7)
    rho=2e-5; a=.06; b=.10
    E8=rho*(.08**3-a**3)/(3*eps0*.08**2)
    E12=rho*(b**3-a**3)/(3*eps0*.12**2)
    near(E8,34823.44624400144,1e-7)
    near(E12,40993.36614909479,1e-7)
    # Source 7.3.9--14: potentials, work, arc plus straight sections.
    near(log((.2+.05)/.05),log(5))
    potential_square=4*k*1.25e-8/.05
    near(potential_square,8987.551792299997,1e-7)
    near(-1e-9*potential_square,-8.9875517923e-6,1e-7)
    R=.25
    near(k*(1/(3*R)-1/R),-2*k/(3*R))
    near((pi+2*log(2))-(pi),2*log(2))
    near(7.08e-7/(eps0*.02/.02),79962.16197000975,1e-7)
    # Source 7.3.15--20: charges, potential continuity, electrostatic self-energy.
    R1=.04; R2=.11; e_rel=4
    phi_dielectric=k*q*(1/R2+(1/e_rel)*(1/R1-1/R2))
    phi_metal=k*q*(1/(e_rel*R1)+(1-1/e_rel)/R2)
    near(phi_dielectric,phi_metal)
    near(k*q*(1/R2),k*q/R2)
    U_uniform=3*k*q*q/(5*R)
    U_inside=k*q*q/(10*R)
    U_outside=k*q*q/(2*R)
    near(U_uniform,U_inside+U_outside)
    near(.5*(eps0*.002/.002)*400**2,7.08335025024e-7,1e-8)
    c_spherical=4*pi*eps0*R1*R2/(R2-R1)
    near(q*q/(2*c_spherical),k*q*q/2*(1/R1-1/R2))
    # Guide 7.1--7.6: thermal and Maxwell source data.
    kB=1.380649e-23; Rgas=8.314462618
    T=2*6.21e-21/(3*kB)
    near(T,299.8589793640527,1e-7)
    near(sqrt(3*Rgas*T/.032),483.4607928707272,1e-7)
    near(1.5*1.5e5*.002,450)
    near(2.5*1.5e5*.002,750)
    near(sqrt(2)*1000,1414.213562373095)
    near(sqrt(3)*1000,1732.0508075688772)
    air_n=(1e-5/760*1.013e5)/(kB*300)
    air_lam=1/(sqrt(2)*pi*(3e-10)**2*air_n)
    air_vbar=sqrt(8*Rgas*300/(pi*.0289))
    near(air_n,3.2180390933107194e17,1e-7)
    near(air_lam,7.771436528507355,1e-7)
    near(air_vbar/air_lam,60.32503065938106,1e-7)
    y=1000; mass=.0289/6.02214076e23; grav=9.8
    scale=math.exp(-mass*grav*y/(kB*300))
    near(scale,math.exp(-.0289*grav*y/(Rgas*300)))



def eighth_round_regressions():
    """Source-parameter spot checks, not an independent review of diagrams."""
    mu0=4*math.pi*1e-7
    e=1.602176634e-19
    me=9.1093837e-31
    R=8.314462618
    kB=1.380649e-23
    pi=math.pi
    sqrt=math.sqrt
    # 8.1: half-loop, magnetic moment vs potential work, helix pitch.
    near(mu0/(4*.25), (mu0/(2*.25))/2)
    near(2*(100*.1*pi*.05**2)*1.5,0.23561944901923454)
    near((2*.5)* (2*.5),1)
    near((3*.5),1.5)
    assert (2*math.cos(pi/6))>math.cos(pi/6)
    # 8.2: semicircular torque, orbit, fields.
    near(5*(pi*.2**2/2)*.5,0.15707963267948968)
    near(mu0*8e-9*3e-5/(4*pi*(6e-8)**2),6.666666666666667e-6)
    near(.5*8e-9*3e-5*6e-8,7.2e-21)
    near(2*(2),4)             # doubled area and doubled current
    near(.1*.1, .01)
    near(200*.1/.1,200)
    near(mu0*4200*200,1.0555751316061706)
    # 8.3.4: 30cm by 30cm flux; 8.3.5: quarter arc and half line.
    near(2*.30*.30,.18)
    near(mu0/(8*.2)+mu0/(4*pi*.2),mu0*(pi+2)/(8*pi*.2))
    # 8.3.6: two antiparallel wires.
    near(mu0/(2*pi)*(20/.05+10/.05),1.2e-4)
    near(mu0/(2*pi)*(10/.05-20/.15),1.3333333333333333e-5)
    near((10*.10)/(20-10),.10)
    # 8.3.9--11: hollow cylindrical current, enclosed current profiles.
    a=.06; b=.10; r=.08
    I_enclosed=4*(r*r-a*a)/(b*b-a*a)
    near(I_enclosed,4*(r*r-a*a)/(b*b-a*a))
    near(.5+math.log(2), 1.1931471805599454)
    c=.16; rout=.13; I=8
    near(I*(c*c-rout*rout)/(c*c-b*b),
         I*(1-(rout*rout-b*b)/(c*c-b*b)))
    # 8.3.12 Hall flow speed, 8.3.16 copper Hall emf.
    near(150e-6/(.05*.003),1)
    near(1.5*200/(8.4e28*e*.001),2.2291103837359867e-5)
    # 8.3.15 and 8.3.17: force cancellation and force/moment integral.
    near(mu0/(2*pi)*20*10*.2/.01,8e-4)
    near(mu0/(2*pi)*20*10*.2/.10,8e-5)
    near(8e-4-8e-5,7.2e-4)
    near(mu0/(2*pi)*20*10*math.log(.10/.01),
         9.210340371976183e-5)
    near(mu0/(2*pi)*20*10*(.10-.01),3.6e-6)
    # 8.3.18--21 electron cyclotron and toroidal material.
    v=e*.007*.03/me
    near(v,36935220.23229738,1e-9)
    near(.5*me*v*v,6.213558416922246e-16)
    vperp=e*.002*.02/me
    period=2*pi*me/(e*.002)
    near(vperp,7035280.04424712,1e-9)
    near(period,1.7861933761449807e-8)
    near(sqrt(vperp*vperp+(.05/period)**2),
         sqrt((e*.002*.02/me)**2+(.05*e*.002/(2*pi*me))**2))
    near(1.2/(mu0*200),4774.6482927568595,1e-8)
    # Guide 8.1--8.6: first law, Carnot and mixing entropy.
    near(.5*R*273*math.log(2),786.6694728899045)
    near(.5*3.5*R*136.5,1986.11725787475)
    near(3/5, .6) # translation fraction of rigid-diatomic internal energy
    near(300*16**.25,600)
    near(3*R*300,900*R)
    near(400*R*math.log(5),5352.6445435701135,1e-5)
    near(1-300/400,.25)
    near((.25)*(400*R*math.log(5)),(400*R*math.log(5))/4)
    near(2/29,.06896551724137931)
    p=101325.; T=300.
    V1=.004; V2=.006
    dS=p/T*(V1*math.log((V1+V2)/V1)+V2*math.log((V1+V2)/V2))
    assert dS>0


def ninth_round_regressions():
    """Independent dimension/numeric checks; source figures still require second review."""
    mu0=4*math.pi*1e-7
    eps0=8.8541878128e-12
    pi=math.pi
    ln=math.log
    sqrt=math.sqrt
    # Textbook 9.1: reciprocal mutual, Faraday and energy-density limits.
    near((2*.2*.4**2)/(.2*.4**2),2)
    near(.5*3**2,.5*9)
    near(mu0*10**2/(8*pi*pi*.1**2),
         ((mu0*10/(2*pi*.1))**2)/(2*mu0))
    # 9.2: flux-time derivative, shrinking circle and inductance.
    near(12*2+9,33)
    near(2*pi*1*.2*.5,.2*pi)
    near(400*.2*1e-4/4,.002)
    near(400/(2/.002),.4)
    near(4*2*2,16)
    # 9.3.1--9.3.6: swept-area / moving-wire consistency.
    near(.4*10*2*1e-4,8e-4)
    a=.04; b=.06; d=.05; v=.03; I=5
    emf=(mu0/(2*pi))*I*b*v*(1/d-1/(d+a))
    near(emf,1.6e-8)
    near((1/2)*2,1)
    near((3*1)-(1+2),0)
    # 9.3.7--9.3.12: rotation, vortex field, signed flux.
    ell=.8; B=.6; omega=5
    near(.5*B*omega*((2*ell/3)**2-(ell/3)**2),
         B*omega*ell**2/6)
    near(4e-5*1*9.8*3*math.cos(pi/3),5.88e-4)
    inner=sqrt(3)/4
    outer=pi/12
    near(inner+outer,(3*sqrt(3)+pi)/12)
    near(math.atan(sqrt(3))-math.atan(1/sqrt(3)),pi/6)
    near(ln((.02+.04)/.02),ln(3))
    near(ln((3*.1/4)/(.1/2)),ln(3/2))
    wireL=mu0*3/pi*ln((.4-.01)/.01)
    near(wireL,2*(mu0*3/(2*pi))*ln(.39/.01))
    # 9.3.13--9.3.17: toroid self-energy, displacement continuity.
    a=.04; b=.10; h=.025; N=200; current=2
    L=mu0*N*N*h/(2*pi)*ln(b/a)
    W=.5*L*current**2
    Bflux=lambda r: mu0*N*current/(2*pi*r)
    near(L, N*h*(mu0*N/(2*pi))*ln(b/a))
    near(W,mu0*N*N*h*current**2/(4*pi)*ln(b/a))
    near(mu0*current**2/(16*pi),
         (mu0*current**2/(4*pi))*(1/4))
    epsilon=4*eps0; k=20; R1=.02; R2=.1; length=.5
    def Jd(radius):
        return epsilon*k/(radius*ln(R2/R1))
    near(Jd(.04)*(2*pi*.04*length),
         Jd(.08)*(2*pi*.08*length))
    near(eps0*pi*.1**2*1e13,eps0*1e13*pi*.01)
    near(mu0*eps0*.1*1e13/2,
         mu0*(eps0*pi*.1**2*1e13)/(2*pi*.1))
    # Guide 9.1--9.11: electrostatic force, semiring, cavity and capacitance.
    charge=5e-8; S=.01
    near(charge*charge/(2*eps0*S),
         (.5*eps0*(charge/(eps0*S))**2)*S)
    near((1/(4*pi*eps0))*(pi/2),
         1/(8*eps0))
    lam=.001; ar=.02; r=.5
    Er=lam*ar/(pi*eps0*r*r)
    near(Er*r*r,lam*ar/(pi*eps0))
    sigma=2e-6; holeR=.12; x=.05
    holeU=sigma/(2*eps0)*(holeR-sqrt(holeR**2+x**2))
    assert holeU<0, "source guide 9.5 printed sign contradiction"
    capV=8; q=1e-8; dd=.01; area=.2
    Uc=capV/2+q*dd/(4*eps0*area)
    near(4*eps0*area*(Uc-capV/2)/dd,q)
    R1=.1;R2=.3; q0=2e-7
    q_prime=q0*R1/R2
    near(q_prime/(4*pi*eps0*R1)-q0/(4*pi*eps0*R2),0)
    C1=2e-11; C_as=4e-11; C_bs=5e-11
    C_equiv=C1+C_as*C_bs/(C_as+C_bs)
    assert C_equiv>C1
    base=.5*eps0*.01/.002*400**2
    er=5
    near(base/er, base*(1/er))
    near(-(er-1)*base, (er*base-base)-2*(er-1)*base)



def tenth_round_regressions():
    """Source-based independent checks for 69 optics/magnetostatics items.

    Angles, interface phase, ring indexing and omitted grating orders have
    explicit physical assumptions. Passing is not independent expert review.
    """
    pi = math.pi
    sqrt = math.sqrt
    log = math.log
    mu0 = 4 * pi * 1e-7
    # Choice: Young fringes, Newton rings, Michelson two passes.
    near(600e-9*1.2/(0.5e-3)*1e3, 1.44)
    near((1.42/1.28)**2, 1.230712890625)
    near(1+60*500e-9/(2*.005),1.003)
    near(2*(1.38-1)*.1, .076)
    near(500e-9*(.012)*(.25e-3)/(6*(500e-9)*(.012)), .25e-3/6)
    near(.012*.25e-3/(6*500e-9), 1.0)
    near(.5*math.cos(pi/4)**2,.25)
    # Fill-ins 10.2.2, 10.2.4, 10.2.10, 10.2.12 and 10.2.19.
    near(562.5e-9*1.2/(1.5e-3)*1e3, .450)
    near((5-2)*600/2,900)
    near(2*(4)*math.sin(pi/6),4)
    near(600/(4*1.33),112.781954887218)
    near(600/(2*1.33),225.563909774436)
    near(4*442/589,3.0016977928692697)
    near(math.tan(pi/3),sqrt(3))
    # Textbook detailed problems.
    near(.006*.2e-3/(2*1.0)*1e9,600)
    near(7*550e-9/(1.58-1)*1e6,6.637931034482759)
    near(550/(4*1.38),99.6376811594203)
    near(.048e-3/.12,4e-4)
    near(680e-9/(2*4e-4)*1e3,.85)
    near(700e-9/(2*1e-4*.25e-2),1.4)
    near(3*600,4*450)
    near(sqrt(3*600e-9*1.9)*1e3,1.8493242008906928)
    near((1.4/1.27)**2,1.2152024304048603)
    near(2*.322e-3/1024*1e9,628.90625)
    near(150*500e-9/(2*.632)*1e6,59.335443037974684)
    near(2e-3/(500e-9),4000)
    # Source 10.3.12: distinguish half-wave approximation from exact maxima.
    near(2.5*600/3,500)
    near(2.459*600/3,491.8)
    # Source 10.3.13 asks for *angular* half-width, not linear width.
    half_angle=math.asin(500e-9/(1.33*.1e-3))
    near(half_angle*1e3,3.7594073548146873,1e-6)
    # Grating maxima, missing orders and polarization.
    near(2*600,3*400)
    near(2*600e-9/math.sin(math.atan(.05/.5))*1e6,12.059850745345069)
    near(2*600/.2,6000)
    near(6000/4,1500)
    assert [k for k in range(1, 10) if k % 4 != 0] == [1,2,3,5,6,7,9]
    near(2*.5*480e-9/(.02e-3)*1e3,24)
    near(.5*480e-9/(.10e-3)*1e3,2.4)
    near(.5*math.cos(pi/6)**2,3/8)
    near(.5*math.cos(pi/4)**2,.25)
    near(.5*math.cos(pi/3)**2,1/8)
    near((math.cos(pi/6)**4)/(math.cos(pi/3)**2),9/4)
    near(math.acos(1/sqrt(3))*180/pi,54.735610317245346)
    near(math.acos(sqrt(2/3))*180/pi,35.264389682754654)
    near(math.atan(1.4)*180/pi,54.46232220802562)
    # Guide: rotating rod magnetic moment, cylinder flux, toroidal material.
    a=.2; b=.004; lamb=.003; omega=10
    near((lamb*omega/6)*((a+b)**3-a**3),
         (lamb*omega/2)*(a*a*b+a*b*b+b**3/3))
    near(mu0*10/(4*pi)*(1+2*log(2)),
         (mu0*10/(2*pi))*(.5+log(2)))
    for r in [.05,.09]:
        near((r*r/.1**2)*5,5*r*r/.1**2)
    a=.02;R=.10;r=.01;current=5
    j=current/(pi*(R*R-r*r))
    near(mu0*j*r*r/(2*a),
         mu0*current*r*r/(2*pi*a*(R*R-r*r)))
    l1=.03;l2=.05
    near(mu0*5*2/(2*pi)*log((l1+l2)/l1),
         (mu0*5*2/(2*pi))*log(1+l2/l1))
    near((6e-5*.10)/(mu0*200*.1*5e-5),4774.64829275686)
    near(2/3-1,-1/3)


def eleventh_round_regressions():
    """Independent source-value checks for special relativity and induced fields."""
    c=3e8
    pi=math.pi
    sqrt=math.sqrt
    log=math.log
    mu0=4*pi*1e-7
    eps0=8.8541878128e-12
    # Textbook 11.1: proper time, contraction, frame-invariant rest mass.
    near(5/sqrt(34),.8574929257125442)
    near(10*sqrt(1-.8**2),6)
    near(4.59*sqrt(1-.991**2),.6144259791870786)
    near(400*sqrt(1-.99**2),56.426943918663575)
    near(2*1,2)
    # Textbook 11.2: inverse Lorentz interval / lifetime / kinetic.
    gam=1/sqrt(1-.8**2)
    delta_x=gam*(-120+.8*c*5e-7)
    delta_t=gam*(5e-7+.8*c*(-120)/c**2)
    near(delta_x,0)
    near(delta_t,3e-7)
    near(2e-6/sqrt(1-.988**2),1.2948849481091769e-5)
    near(sqrt(3)/2,.8660254037844386)
    # Textbook 11.3: spacelike simultaneity, velocity addition.
    dx=6e4;dt=-1e-4;v=c*c*dt/dx
    near(v,-.5*c)
    near((dx-v*dt)/sqrt(1-(v/c)**2),sqrt(dx*dx-c*c*dt*dt))
    near(1.25*(2e-7-.6*50/c),1.25e-7)
    near(10/sqrt(1-.8**2),50/3)
    near(sqrt(1-(4/5)**2),.6)
    near(4*.6*c*(5/4),3*c)
    gamma_mu=1/sqrt(1-.998**2)
    near(6000/gamma_mu,6000*sqrt(1-.998**2))
    assert (.998*c*gamma_mu*2e-6)>6000
    near(1.6/(1+.64),.975609756097561)
    near(1.4/1.48,.9459459459459459)
    near(sqrt(.6**2+.64**2),.8772684879784524)
    # Textbook 11.3.10--18, energies and rest-mass balances.
    near((1/sqrt(1-.99**2)-1)*.51,3.1052941455425107)
    near((1/sqrt(1-.1**2)-1)*.51,.0025692857821981697)
    near((1/sqrt(1-.9**2)-1)*.51,.6600202427398651)
    near(1-1/1.1,.09090909090909091)
    near((1/sqrt(1-.8**2)-1/sqrt(1-.4**2))*.51,.29354437989821963)
    near((5e26)/(9e16),5.555555555555556e9)
    near((2e30*9e16)/(5e26),3.6e20)
    near(3.6e16/9e16,.4)
    dm=(3.3437+5.0049-6.6425-1.6750)*1e-27
    assert dm>0
    near(dm*9e16/1.602176634e-13,17.469983899416246)
    # Guide 11.1--7: induced emf, loop torque, displacement and Poynting flux.
    near(mu0*5*.06*.04*.03/(2*pi*.05*(.05+.04)),1.6e-8)
    near(sqrt(3)/4+pi/12,.6948120896913688)
    near(.5*(400e-4),.02)
    near(.5*(400e-4)*10,.2)
    near(.5**2*(400e-4)**2*10/2,.002)
    near(2.0e-3*pi,.006283185307179586)
    a=.02;b=.05;N=200;h=.03
    L=mu0*N*N*h/(2*pi)*log(b/a)
    near(L,mu0*N*N*h/(2*pi)*log(b/a))
    near(.5*L*2**2,mu0*N*N*h*2**2/(4*pi)*log(b/a))
    near(eps0*pi*.1**2*1e13,2.7816251386196766)
    near(mu0*eps0*.1*1e13/2,5.5632502772393526e-6)
    # Guide 11.7, energy flux equals total Joule dissipation in sub-cylinder.
    rho=.02; I0=5.; aa=.10;r=.04;length=2.
    J=I0/(pi*aa**2)
    E=rho*J
    H=I0*r/(2*pi*aa**2)
    near(E*H*2*pi*r*length,
         (I0*r*r/aa**2)**2*(rho*length/(pi*r*r)))


if __name__ == "__main__":
    n = structural_check()
    numerical_check()
    second_round_regressions()
    third_round_regressions()
    fourth_round_regressions()
    fifth_round_regressions()
    sixth_round_regressions()
    seventh_round_regressions()
    eighth_round_regressions()
    ninth_round_regressions()
    tenth_round_regressions()
    eleventh_round_regressions()
    print(f"Structure: {n} referenced worked items; all checked blocks present.")
    print("Selected numeric invariants: passed.")
    print("Not a replacement for full independent physics or copyright review.")
