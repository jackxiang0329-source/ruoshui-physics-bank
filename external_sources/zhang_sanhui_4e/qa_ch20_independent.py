#!/usr/bin/env python3
"""Numerical/identity regression samples for previously transcribed chapter 20 candidates.
Does not compare original scans or certify figure-dependent directions.
"""
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHAPTER = 20
CASES = [
    (1, lambda: (4*math.pi*1e-7)*5*10/(2*math.pi)*math.log((.1+.2)/.1), lambda: 1.099e-5),
    (2, lambda: 4000*5e-5*math.pi*.12**2*(2*math.pi*30), lambda: 1.71),
    (3, lambda: (4*math.pi*1e-7)*1000*5*.2*2/(2*math.pi)*(1/.1-1/.2), lambda: 2.0e-3),
    (4, lambda: (4*math.pi*1e-7)*1000*.2/(2*math.pi)*math.log(2)*(500*math.pi), lambda: 4.36e-2),
    (5, lambda: .2/2*math.sqrt(.2**2-.2**2/4)*10, lambda: 0.1732),
    (6, lambda: .42e-4*12.705*(1.70*330), lambda: 0.30),
    (7, lambda: .007/(.70e-4*200), lambda: 0.50),
    (8, lambda: 12/(120*.02*.02), lambda: 250),
    (9, lambda: .1*10/(100*.2), lambda: 0.05),
    (10, lambda: (.5**2)*(.01**2)*(.2**2)*.001/1e-6*20, lambda: 0.020),
    (11, lambda: .5, lambda: 0.5),
    (12, lambda: 9.1093837e-31*1e5/(1.602176634e-19*.2), lambda: 2.84e-6),
    (13, lambda: (4*math.pi*1e-7)*1000*500*.01/.5, lambda: 0.012566),
    (14, lambda: (4*math.pi*1e-7)*50*100*.0004/(2*.2), lambda: 6.28e-6),
    (15, lambda: (4*math.pi*1e-7)*(1200**2)*math.pi*.020**2/.300, lambda: 7.58e-3),
    (16, lambda: 8e-4*10/(20e-6), lambda: 400),
    (17, lambda: (4*math.pi*1e-7)*200**2*.05/(2*math.pi)*math.log(2), lambda: 2.77e-4),
    (18, lambda: (4*math.pi*1e-7)/math.pi*math.log((.1-.01)/.01), lambda: 8.79e-7),
    (19, lambda: 2*3/(2+3), lambda: 1.2),
    (20, lambda: 2+3-2*1, lambda: 3),
    (21, lambda: 1e16/(2*(4*math.pi*1e-7)), lambda: 3.98e21),
    (22, lambda: 2**2/(2*(4*math.pi*1e-7)), lambda: 1.59e6),
    (23, lambda: 2*(4*math.pi*1e-7)*3.6e6, lambda: 9.05),
    (24, lambda: 1.69e-8*20/(math.pi*.0055**2), lambda: 3.56e-3),
    (25, lambda: (4*math.pi*1e-7)/(8*math.pi)+(4*math.pi*1e-7)/(2*math.pi)*math.log(.03/.01), lambda: 2.70e-7),
    (26, lambda: (4*math.pi*1e-7)*10**2/(2*math.pi)*math.log(2), lambda: 1.386e-5),
    (27, lambda: (4*math.pi*1e-7)*1000*2000*.01*2*3, lambda: 0.1508),
]

def main():
    q = (ROOT / f"chapters/{CHAPTER:02d}/questions.tex").read_text(encoding="utf-8")
    s = (ROOT / f"chapters/{CHAPTER:02d}/solutions.tex").read_text(encoding="utf-8")
    assert len(CASES) == 27
    assert [n for n, _, _ in CASES] == list(range(1, 28))
    for n, calc, expected in CASES:
        tag = rf"\paragraph{{习题 {CHAPTER}.{n}}}"
        if tag not in q or tag not in s:
            raise AssertionError(f"Missing candidate {CHAPTER}.{n}")
        got, ref = calc(), expected()
        if not (math.isfinite(got) and math.isfinite(ref) and
                math.isclose(got, ref, rel_tol=.025,
                             abs_tol=1e-12 if ref == 0 else 0)):
            raise AssertionError(f"{CHAPTER}.{n} discrepancy: got={got}, expected={ref}")
    print("PASS: chapter 20 27 existing-candidate math/physics checkpoints")
    print("Original PDF figure/source-expert validation NOT performed; new original problems 0.")

if __name__ == "__main__":
    main()
