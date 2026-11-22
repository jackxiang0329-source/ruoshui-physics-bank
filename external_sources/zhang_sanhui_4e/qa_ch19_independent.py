#!/usr/bin/env python3
"""Numerical/identity regression samples for previously transcribed chapter 19 candidates.
Does not compare original scans or certify figure-dependent directions.
"""
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHAPTER = 19
CASES = [
    (1, lambda: math.tanh(.1), lambda: 0.099668),
    (2, lambda: 1.602176634e-19*.1/(2*9.1093837e-31), lambda: 8.795e9),
    (3, lambda: (4*math.pi*1e-7)*1.602176634e-19*2.2e6/(4*math.pi*(.53e-10)**2), lambda: 12.55),
    (4, lambda: 2*7800*math.pi*.005**2*.12/.05585*6.02214076e23, lambda: 1.59e24),
    (5, lambda: 2*7800*.085*.01*.0002/.05585*6.02214076e23*9.274e-24, lambda: 0.265),
    (6, lambda: 4*math.pi*1e-7*4200*20, lambda: 0.1056),
    (7, lambda: .02/((4*math.pi*1e-7)*32), lambda: 497),
    (8, lambda: 1000*2/(2*math.pi*.15), lambda: 2.12e3),
    (9, lambda: 1.2*6/((4*math.pi*1e-7)*220), lambda: 2.60e4),
    (10, lambda: 170/800, lambda: 0.213),
    (11, lambda: 2*math.pi*.00025*2, lambda: 0.00314),
    (12, lambda: .18*.6/((4*math.pi*1e-7)*1000*1.5-.18*.01), lambda: 1.27e3),
    (13, lambda: 3/(4*math.pi*1e-7)*(.5/5000+.02), lambda: 4.80e4),
    (14, lambda: (.08/(4*math.pi*1e-7))*(.002+.144/1600)*220/20, lambda: 1.46e3),
]

def main():
    q = (ROOT / f"chapters/{CHAPTER:02d}/questions.tex").read_text(encoding="utf-8")
    s = (ROOT / f"chapters/{CHAPTER:02d}/solutions.tex").read_text(encoding="utf-8")
    assert len(CASES) == 14
    assert [n for n, _, _ in CASES] == list(range(1, 15))
    for n, calc, expected in CASES:
        tag = rf"\paragraph{{习题 {CHAPTER}.{n}}}"
        if tag not in q or tag not in s:
            raise AssertionError(f"Missing candidate {CHAPTER}.{n}")
        got, ref = calc(), expected()
        if not (math.isfinite(got) and math.isfinite(ref) and
                math.isclose(got, ref, rel_tol=.025,
                             abs_tol=1e-12 if ref == 0 else 0)):
            raise AssertionError(f"{CHAPTER}.{n} discrepancy: got={got}, expected={ref}")
    print("PASS: chapter 19 14 existing-candidate math/physics checkpoints")
    print("Original PDF figure/source-expert validation NOT performed; new original problems 0.")

if __name__ == "__main__":
    main()
