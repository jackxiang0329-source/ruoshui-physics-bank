#!/usr/bin/env python3
"""Numerical/identity regression samples for previously transcribed chapter 18 candidates.
Does not compare original scans or certify figure-dependent directions.
"""
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHAPTER = 18
CASES = [
    (1, lambda: 5e-4*9.8/(2.5e-8*6e4), lambda: 3.27),
    (2, lambda: 9.1093837e-31*1e7/(1.602176634e-19*.05), lambda: 1.14e-3),
    (3, lambda: 2*math.pi*1.6726219e-27/(1.602176634e-19*.1), lambda: 6.56e-7),
    (4, lambda: math.sqrt(2*1.602176634e-19*20000/9.1093837e-31), lambda: 8.39e7),
    (5, lambda: 2*math.pi*1.49e-18/(1.602176634e-19*240), lambda: 0.243),
    (6, lambda: 1e-16/(1.602176634e-19*1e-8), lambda: 6.24e10),
    (7, lambda: 1.602176634e-19*20*3.5, lambda: 1.12e-17),
    (8, lambda: 9.1093837e-31*.8e8/(1.602176634e-19*4e-7), lambda: 1.14e3),
    (9, lambda: 1.602176634e-19*1.5/(2*math.pi*3.34e-27), lambda: 1.15e7),
    (10, lambda: 16*32.86/29.20, lambda: 18.01),
    (11, lambda: 200*1.5/(8.4e28*1.602176634e-19*.001), lambda: 2.23e-5),
    (12, lambda: .001*.300/(1.602176634e-19*.001*.00655), lambda: 2.86e20),
    (13, lambda: .00105*2e21*1.602176634e-19*.00005/.00125, lambda: 0.01346),
    (14, lambda: 101325/(.02*1.5), lambda: 3.38e6),
    (15, lambda: 1e-4/(.08*.002), lambda: 0.625),
    (16, lambda: .00878*9.8/(2*5*.1*.1), lambda: 0.860),
    (17, lambda: 1000*.100*.020*.010, lambda: 0.0200),
    (18, lambda: (200*8*.15**2)*4, lambda: 144),
    (19, lambda: 10*.2**2/4, lambda: 0.100),
    (20, lambda: 3*9.66e-27/(2*1.602176634e-19*1.2e-15), lambda: 7.54e7),
    (21, lambda: 2*.928e-23/(1.602176634e-19*3e8), lambda: 3.86e-13),
    (22, lambda: (4*math.pi*1e-7)/(2*math.pi)*10*10*.2*(1/.1-1/.2), lambda: 2e-5),
    (23, lambda: (4*math.pi*1e-7)*(100**2)/2, lambda: 6.283e-3),
    (24, lambda: (.2**2-.1**2)/(2*(4*math.pi*1e-7)), lambda: 1.19e4),
    (25, lambda: (4*math.pi*1e-7)*30**2/(2*math.pi*.05), lambda: 3.60e-3),
    (26, lambda: math.pi*.1/2, lambda: 0.15708),
    (27, lambda: 4200**2/(2*5), lambda: 1.764e6),
    (28, lambda: 1.602176634e-19*2/1, lambda: 3.20435e-19),
    (29, lambda: (.1*3e8)*(.1*3e8)/(3e8)**2, lambda: 0.01),
    (30, lambda: -2.39e-23*2*math.cos(math.radians(39.2)), lambda: -3.70e-23),
]

def main():
    q = (ROOT / f"chapters/{CHAPTER:02d}/questions.tex").read_text(encoding="utf-8")
    s = (ROOT / f"chapters/{CHAPTER:02d}/solutions.tex").read_text(encoding="utf-8")
    assert len(CASES) == 30
    assert [n for n, _, _ in CASES] == list(range(1, 31))
    for n, calc, expected in CASES:
        tag = rf"\paragraph{{习题 {CHAPTER}.{n}}}"
        if tag not in q or tag not in s:
            raise AssertionError(f"Missing candidate {CHAPTER}.{n}")
        got, ref = calc(), expected()
        if not (math.isfinite(got) and math.isfinite(ref) and
                math.isclose(got, ref, rel_tol=.025,
                             abs_tol=1e-12 if ref == 0 else 0)):
            raise AssertionError(f"{CHAPTER}.{n} discrepancy: got={got}, expected={ref}")
    print("PASS: chapter 18 30 existing-candidate math/physics checkpoints")
    print("Original PDF figure/source-expert validation NOT performed; new original problems 0.")

if __name__ == "__main__":
    main()
