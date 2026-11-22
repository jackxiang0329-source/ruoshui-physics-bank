#!/usr/bin/env python3
"""Numerical/identity regression samples for previously transcribed chapter 21 candidates.
Does not compare original scans or certify figure-dependent directions.
"""
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHAPTER = 21
CASES = [
    (1, lambda: 2-2, lambda: 0),
    (2, lambda: 4*math.pi*0, lambda: 0),
    (3, lambda: 1.602176634e-19*2e24*math.sin(math.pi/4)/(4*math.pi*8.8541878128e-12*(2.998e8)**2*.2), lambda: 0.113),
    (4, lambda: 1.602176634e-19*(2e4*1.602176634e-19/(9.1093837e-31*5e-9))/(4*math.pi*8.8541878128e-12*(2.998e8)**2*.3), lambda: 0.0377),
    (5, lambda: 8e-3*6e6, lambda: 4.8e4),
    (6, lambda: 2.49e-12/2.998e8, lambda: 8.30e-21),
    (7, lambda: 1.602176634e-19*.0039/9.1093837e-31, lambda: 6.86e8),
    (8, lambda: math.sqrt(1.38e3/(2.998e8*8.8541878128e-12)), lambda: 721),
    (9, lambda: 3e5/(math.pi*(30e-6)**2), lambda: 1.061e14),
    (10, lambda: 3.82e8*math.tan(.880e-6/2), lambda: 168),
    (11, lambda: (1.69e-8*20**2*10)/(math.pi*.0055**2), lambda: 0.711),
    (12, lambda: 100*2, lambda: 200),
    (13, lambda: 2.998e8/.030, lambda: 9.99e9),
    (14, lambda: (1+.5)*1.1e3/(2.998e8), lambda: 5.50e-6),
    (15, lambda: 2*1.5e9/(2.998e8*1.3e-6), lambda: 7.70e6),
    (16, lambda: math.sqrt(2*10*100*2.998e8/1e4), lambda: 7.74e3),
    (17, lambda: 3*6.9e7*(7e8)**2/(4*6.67430e-11*2e30*1000*2.998e8), lambda: 6.3e-7),
]

def main():
    q = (ROOT / f"chapters/{CHAPTER:02d}/questions.tex").read_text(encoding="utf-8")
    s = (ROOT / f"chapters/{CHAPTER:02d}/solutions.tex").read_text(encoding="utf-8")
    assert len(CASES) == 17
    assert [n for n, _, _ in CASES] == list(range(1, 18))
    for n, calc, expected in CASES:
        tag = rf"\paragraph{{习题 {CHAPTER}.{n}}}"
        if tag not in q or tag not in s:
            raise AssertionError(f"Missing candidate {CHAPTER}.{n}")
        got, ref = calc(), expected()
        if not (math.isfinite(got) and math.isfinite(ref) and
                math.isclose(got, ref, rel_tol=.025,
                             abs_tol=1e-12 if ref == 0 else 0)):
            raise AssertionError(f"{CHAPTER}.{n} discrepancy: got={got}, expected={ref}")
    print("PASS: chapter 21 17 existing-candidate math/physics checkpoints")
    print("Original PDF figure/source-expert validation NOT performed; new original problems 0.")

if __name__ == "__main__":
    main()
