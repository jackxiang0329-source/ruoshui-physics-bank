#!/usr/bin/env python3
"""28 independent mathematical regression checkpoints for Zhang Sanhui chapter 5.

This inspects previously transcribed candidate questions and independently recomputes
one physical quantity per numbered problem. It is NOT an original-PDF comparison,
expert certification, or permission to release the source text.
"""
from __future__ import annotations

import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
G = 9.8
PI = math.pi

def check() -> None:
    q = (ROOT / "chapters" / "05" / "questions.tex").read_text(encoding="utf-8")
    s = (ROOT / "chapters" / "05" / "solutions.tex").read_text(encoding="utf-8")

    # Each test uses candidate problem input parameters, an independent numerical
    # evaluation and the separately printed rounded solution checkpoint.
    # It must not be counted as a newly transcribed or PDF-verified source problem.
    checks = [
        (1, 25**2 / (2 * (1.25 * 2 * PI)), 39.79, "uniform angular acceleration"),
        (2, ((3000 - 200) * 2 * PI / 60) / 7, 41.89, "engine angular acceleration"),
        (3, -(2 * PI * (1.14 / 365)) / (86400**2 * (87 * 365.25 * 86400)), -9.58e-22, "mean Earth angular deceleration"),
        (4, 2 * PI / 86400 * 6.37e6 * math.cos(math.radians(40)), 355, "latitude-dependent linear velocity"),
        (5, 2 * math.degrees(math.atan(math.sqrt(1.93 / 1.14))), 104.91, "water molecule complete bond angle"),
        (6, (60 * 12 * 1.66054e-27) * (71e-9)**2 / 6, 1.00e-39, "C60 printed 71 nm shell inertia, without silently fixing source"),
        (7, 2 * PI * math.sqrt((2.66e-26 * (1.21e-10)**2 / 2) / (2 * 2.06e-21)), 1.37e-12, "diatomic oxygen period"),
        (8, 2 * (2 / 5 * 2 * .1**2 + 2 * (.1 + .6 / 2)**2), .656, "dumbbell off-axis inertia with declared sample masses"),
        (9, .5 * (100 * 4.5**2 / 3) * (2 * PI / 3600)**2, 1.03e-3, "minute-hand rotational kinetic energy"),
        (10, (2 / 3) - (1 / 24 + 1 / 12), 13 / 24, "punctured disk parallel-axis subtraction"),
        (11, (3 - .2 * 2) * G / (3 + 2 + 1 / 2), 4.633, "pulley acceleration with explicitly chosen masses"),
        (12, G * .1 / (1 / 12 + .1**2), 10.5, "meter-stick release angular acceleration"),
        (13, .5 * sum(m * r*r for m, r in [(2,1),(3,2),(4,3)]) * 5**2, 625, "rigid body discrete kinetic-energy identity"),
        (14, .25 * 1 * .2**2 * 12**2, 1.44, "record kinetic energy in declared sample"),
        (15, .5 * 2 * (15 * 2 * PI / 60)**2 * (2 / .8 - 1), 3.70, "work required to pull arms inward"),
        (16, math.degrees(math.acos(1 - (.008 * 200 * .3)**2 / (2 * (1*.4**2/3 + .008*.3**2) * G * (1*.4/2+.008*.3)))), 94.3, "embedded bullet and rod maximum angle"),
        (17, (1200 / (1200 + 80*2**2)) * (2 * PI / 10), .496, "turntable final angular speed"),
        (18, 2 * (.5 * 1200 * 20**2) - .5 * 2500 * ((1200*20*.5/2500)**2), 451200, "offset inelastic car collision energy loss"),
        (19, (300000 + 3*70*2.5**2) / (3*70*2.5**2 * 12), 19.1, "crew revolutions relative to spaceship"),
        (20, .4 * 1.989e30 * (6.96e8)**2 * 2*PI/(26*86400), 1.08e42, "homogeneous Sun angular momentum"),
        (21, .033 / (2 * 1.26e-5), 1.31e3, "pulsar lifetime for constant energy-loss rate"),
        (22, (.33*5.972e24*(6.371e6)**2) * (2*PI/86400) * (2*PI/86400**2) * (16/(1e6*365.25*86400)), 2.48e12, "Earth tidal mechanical power"),
        (23, 26*86400 * (6.37e6/6.96e8)**2, 188, "ideal Sun collapse rotation period"),
        (24, math.hypot((1 + 2*.2) - 2*.7, (-2*.3) - (-2*.3)), 0, "rolling disk instantaneous-contact kinematics"),
        (25, 2000*(1-.6)/(300+1000*1**2), .6154, "spool rolling angular acceleration"),
        (26, G + 4*G, 49.0, "yo-yo string-end acceleration for 2mg pull"),
        (27, (2*PI/(26000*365.25*86400)) * (2*PI*8.05e37/86400) * math.sin(math.radians(23.5)), 1.79e22, "Earth axial precession torque including sine factor"),
        (28, (1e5 * (800*2*PI/60)**2) / (2*7.46e4), 4.70e3, "flywheel spin-up at fixed power"),
    ]
    assert len(checks) == 28
    assert sorted(num for num, *_ in checks) == list(range(1, 29))
    for number, calculated, reference, label in checks:
        paragraph = f"\\paragraph{{习题 5.{number}}}"
        if paragraph not in q or paragraph not in s:
            raise AssertionError(f"5.{number}: candidate problem/solution missing")
        if not math.isfinite(calculated):
            raise AssertionError(f"5.{number}: nonfinite {label}")
        if not math.isclose(calculated, reference, rel_tol=0.015, abs_tol=1e-11 if reference == 0 else 0):
            raise AssertionError(f"5.{number}: {label}: independently computed {calculated!r}, expected {reference!r}")
    print("PASS: 28/28 independent candidate numeric/identity checks; 0 new source-transcribed problems.")
    print("NOT PERFORMED: full original PDF page-by-page check, source answer comparison, expert review.")

if __name__ == "__main__":
    check()
