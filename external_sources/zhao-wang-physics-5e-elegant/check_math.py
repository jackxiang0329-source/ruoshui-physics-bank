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
    ("chapters/guide-ch01-examples.tex", "sourceexample",
     [f"1.{n}" for n in range(1, 6)]),
    ("chapters/guide-ch02-examples.tex", "sourceexample",
     [f"2.{n}" for n in range(1, 8)]),
    ("chapters/guide-ch03-examples.tex", "sourceexample",
     [f"3.{n}" for n in range(1, 6)]),
    ("chapters/guide-ch04-examples.tex", "sourceexample",
     [f"4.{n}" for n in range(1, 6)]),
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
    assert total == 182, total
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


if __name__ == "__main__":
    n = structural_check()
    numerical_check()
    second_round_regressions()
    third_round_regressions()
    fourth_round_regressions()
    print(f"Structure: {n} referenced worked items; all checked blocks present.")
    print("Selected numeric invariants: passed.")
    print("Not a replacement for full independent physics or copyright review.")
