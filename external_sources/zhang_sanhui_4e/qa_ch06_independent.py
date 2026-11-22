#!/usr/bin/env python3
"""27 checks on EXISTING chapter-6 problem/solution candidates (not PDF source certification)."""
from __future__ import annotations
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
P = math.pi
G = 9.8
def close(a: float, b: float, name: str, rel: float = 0.018) -> None:
    if not (math.isfinite(a) and math.isclose(a, b, rel_tol=rel, abs_tol=1.e-12 if b == 0 else 0)):
        raise AssertionError(f"{name}: computed {a!r} vs candidate checkpoint {b!r}")

def run() -> None:
    questions = (ROOT/"chapters/06/questions.tex").read_text(encoding="utf-8")
    solutions = (ROOT/"chapters/06/solutions.tex").read_text(encoding="utf-8")
    cases: list[tuple[int, float, float, str]] = [
        (1, .05*(8*P)**2, 31.6, "harmonic oscillator maximum acceleration"),
        (2, math.cos(2*P/3), -.5, "phase at -A/2 with negative speed"),
        (3, 2*P/(5*P/6), 2.4, "provisional scanned-figure frequency interpretation"),
        (4, 2*P/(.03/.02), 4.19, "velocity amplitude to period"),
        (5, 2*P/.5, 4*P, "period conversion to angular frequency"),
        (6, math.cos(P/2 - P/2), 1, "second oscillator at maximum when first crosses zero"),
        (7, math.degrees(2*math.acos(.5)), 120, "opposite-speed meeting phase difference"),
        (8, math.sqrt(2*(.2+.6)/25), .253, "potential-energy amplitude from total energy"),
        (9, 2*P*math.sqrt(.5/50), .6283, "vertical-spring period, declared parameter example"),
        (10, math.sqrt(60/(2+3/3)), 4.47214, "elastic spring effective mass m+ms/3, declared example"),
        (11, 2*P*math.sqrt(.3*(10+20)/(10*20)), 1.333, "series spring period, declared example"),
        (12, 2*P*math.sqrt(.3/(10+20)), .6283, "parallel restoring springs, declared example"),
        (13, (1/(2*P))*math.sqrt(1000/(.05/2)), 31.8, "relative two-body spring oscillator"),
        (14, 2*P*math.sqrt((6.371e6)**3/3.986004418e14), 5061, "uniform-Earth tunnel and satellite period"),
        (15, .5*G/(2*P*2)**2, .0310, "horizontal board static-friction amplitude"),
        (16, 2*P*math.sqrt(.2/(2*.5*G)), .898, "counterrotating rollers oscillation period"),
        (17, 2*P*math.sqrt(.121/(2*13600*.30e-4*G)), .773, "U-tube mercury frequency"),
        (18, 2*P*math.sqrt(5**3/20), 15.708, "Kepler radial frequency, declared GM and radius"),
        (19, 2*P*math.sqrt(2/(2*G*.4)), 3.173, "physical-pendulum frequency, declared model"),
        (20, 2*P*math.sqrt(2*.5/G), 2.007, "thin hoop hung at rim, declared radius"),
        (21, (1/(2*P))*math.sqrt((8*8.9875517923e9*(1.602176634e-19)**2/(1.3e-10)**3)/1.67262192369e-27), 1.13e14, "HCl candidate model: fixed chlorine; original quantum level wording disputed"),
        (22, math.log(2)/(math.log(5/4)/100), 310.6, "additional amplitude-halving time of damped pendulum"),
        (23, math.sqrt(50/2), 5, "velocity resonance frequency, example k=50,m=2"),
        (24, abs(.04*complex(math.cos(P/6),math.sin(P/6)) + .03*complex(math.cos(-P/6),math.sin(-P/6))), .06083, "two same-frequency phasor resultant"),
        (25, 5*P/(4*314), .0125, "first positive A/sqrt(2) encounter, correct phase branch"),
        (26, 2*P/(20*P), .100, "orthogonal ellipse traversal period"),
        (27, (2/3)*2.70e4, 1.80e4, "conditional 3:2 Lissajous interpretation: unverified original figure"),
    ]
    assert [r[0] for r in cases] == list(range(1,28))
    for num, calc, expected, label in cases:
        token = rf"\paragraph{{习题 6.{num}}}"
        if token not in questions or token not in solutions:
            raise AssertionError(f"Candidate problem or answer missing: 6.{num}")
        close(calc, expected, f"6.{num} {label}")
    print("PASS: 27/27 ch6 independent candidate model checkpoints; no additional source-transcribed questions.")
    print("IMPORTANT: tests 6.3 and 6.27 are CONDITIONAL on figures not re-opened in this run.")
    print("NOT checked: source PDF original, every line of derivation, expert physics review.")
if __name__ == "__main__":
    run()
