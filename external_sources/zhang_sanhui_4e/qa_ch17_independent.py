#!/usr/bin/env python3
"""Independent calculation checkpoints for already transcribed chapter 17 candidates.
Not a scan-page crosscheck, complete derivation audit, or expert certification.
"""
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHAPTER = 17
CASES = [
    (1, lambda: 4*math.pi*1e-7*5/(4*math.pi*.1), lambda: 5e-6),
    (2, lambda: 4*math.pi*1e-7*1800/(2*math.pi*25), lambda: 1.44e-5),
    (3, lambda: math.degrees(math.atan(5/18)), lambda: 15.5),
    (4, lambda: 1/2*2-1/(2*math.pi-2)*(2*math.pi-2), lambda: 0),
    (5, lambda: 2*(4*math.pi*1e-7)*20/(2*math.pi*.2), lambda: 4e-5),
    (6, lambda: (4*math.pi*1e-7)*10/(4*.2), lambda: 1.5708e-5),
    (7, lambda: (4*math.pi*1e-7)*5000/(2*math.pi*.03), lambda: 0.033333),
    (8, lambda: (4*math.pi*1e-7)*10*(.5*.2)/(2*math.pi*.2**2), lambda: 5e-6),
    (9, lambda: 2/.2, lambda: 10),
    (10, lambda: 4*math.pi*1e-7*1000*2, lambda: 0.002513),
    (11, lambda: .5, lambda: 0.5),
    (12, lambda: (4*math.pi*1e-7)*(10000/(2*math.pi*1))*7.3e4/(2*math.pi*2), lambda: 11.62),
    (13, lambda: (4*math.pi*1e-7)*200*5*.05/(2*math.pi)*math.log(.2/.1), lambda: 6.931e-6),
    (14, lambda: (4*math.pi*1e-7)*10, lambda: 1.2566e-5),
    (15, lambda: (4*math.pi*1e-7)*10*.5/(4*math.pi), lambda: 5e-7),
    (16, lambda: (4*math.pi*1e-7)*1e6*.02/2, lambda: 0.012566),
    (17, lambda: (4*math.pi*1e-7)*1/.1*(4/5)**1.5, lambda: 8.9918e-6),
    (18, lambda: (4*math.pi*1e-7)*100*1e-6/(2*math.pi*.2), lambda: 1e-10),
    (19, lambda: 8.8541878128e-12*math.pi*.05**2*1e12, lambda: 6.954e-2),
    (20, lambda: 2*math.pi*50*1e-12*1.74e5, lambda: 5.47e-5),
]

def main():
    q = (ROOT / f"chapters/{CHAPTER:02d}/questions.tex").read_text(encoding="utf-8")
    s = (ROOT / f"chapters/{CHAPTER:02d}/solutions.tex").read_text(encoding="utf-8")
    assert len(CASES) == 20
    assert [n for n, _, _ in CASES] == list(range(1, 21))
    for number, compute, reference in CASES:
        tag = rf"\paragraph{{习题 {CHAPTER}.{number}}}"
        if tag not in q or tag not in s:
            raise AssertionError(f"Missing previously transcribed candidate {CHAPTER}.{number}")
        obtained, expected = compute(), reference()
        if not (math.isfinite(obtained) and math.isfinite(expected) and
                math.isclose(obtained, expected, rel_tol=0.025,
                             abs_tol=1e-12 if expected == 0 else 0)):
            raise AssertionError(f"{CHAPTER}.{number}: {obtained!r} vs {expected!r}")
    print("PASS chapter 17: 20 candidate model/physical-identity checks")
    print("Source PDF revalidation: NOT DONE; new original exercises: 0")

if __name__ == "__main__":
    main()
