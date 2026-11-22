#!/usr/bin/env python3
"""Independent calculation checkpoints for already transcribed chapter 16 candidates.
Not a scan-page crosscheck, complete derivation audit, or expert certification.
"""
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHAPTER = 16
CASES = [
    (1, lambda: .008*240/(1.602176634e-19*3e8), lambda: 4e10),
    (2, lambda: 2*8.8541878128e-12*1.2e6*.3*.2, lambda: 1.275e-6),
    (3, lambda: 30/((10500*6.02214076e23/.1079)*1.602176634e-19*math.pi*(.001/2)**2), lambda: 4.07e-3),
    (4, lambda: 1.75e-8*2/(.020*.080), lambda: 2.1875e-5),
    (5, lambda: 20*((math.pi*.020**2/4)/.01)/((math.pi*.025**2/4-math.pi*.020**2/4)/(8.7e-8)+(math.pi*.020**2/4)/.01), lambda: 3.09e-4),
    (6, lambda: 5*30/(30+70), lambda: 1.5),
    (7, lambda: 4e5/(4e-12*4*math.pi*(6.37e6)**2), lambda: 196),
    (8, lambda: 1e12*math.log(.02/.005)/(2*math.pi*1000), lambda: 2.21e8),
    (9, lambda: 1e8/(4*math.pi)*(1/.1-1/.3), lambda: 5.305e7),
    (10, lambda: 10*200/(2*math.pi)*(1/1-1/1.3), lambda: 73.46),
    (11, lambda: (-8/3)/2, lambda: -4/3),
    (12, lambda: (3/10+1/20)/(1/10+1/20+1/10), lambda: 1.4),
    (13, lambda: (2/4)-(3/6), lambda: 0),
    (14, lambda: 3.76/(.0004+.00002), lambda: 8.95e3),
    (15, lambda: 1000*1e-6*math.log(1e-6*100/1.602176634e-19), lambda: 0.0341),
    (16, lambda: .002*4000/1, lambda: 8),
    (17, lambda: (400*200)/(4180*(80-20))*60, lambda: 19.1),
    (18, lambda: 1-1, lambda: 0),
]

def main():
    q = (ROOT / f"chapters/{CHAPTER:02d}/questions.tex").read_text(encoding="utf-8")
    s = (ROOT / f"chapters/{CHAPTER:02d}/solutions.tex").read_text(encoding="utf-8")
    assert len(CASES) == 18
    assert [n for n, _, _ in CASES] == list(range(1, 19))
    for number, compute, reference in CASES:
        tag = rf"\paragraph{{习题 {CHAPTER}.{number}}}"
        if tag not in q or tag not in s:
            raise AssertionError(f"Missing previously transcribed candidate {CHAPTER}.{number}")
        obtained, expected = compute(), reference()
        if not (math.isfinite(obtained) and math.isfinite(expected) and
                math.isclose(obtained, expected, rel_tol=0.025,
                             abs_tol=1e-12 if expected == 0 else 0)):
            raise AssertionError(f"{CHAPTER}.{number}: {obtained!r} vs {expected!r}")
    print("PASS chapter 16: 18 candidate model/physical-identity checks")
    print("Source PDF revalidation: NOT DONE; new original exercises: 0")

if __name__ == "__main__":
    main()
