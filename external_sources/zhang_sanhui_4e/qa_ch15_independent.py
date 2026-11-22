#!/usr/bin/env python3
"""Independent calculation checkpoints for already transcribed chapter 15 candidates.
Not a scan-page crosscheck, complete derivation audit, or expert certification.
"""
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHAPTER = 15
CASES = [
    (1, lambda: 1.602176634e-19*.128e-9, lambda: 2.05e-29),
    (2, lambda: -6e-8*8.9875517923e9*((1/.02-1/.04)/6+(1/.04-1/.06)/3), lambda: -3.75e3),
    (3, lambda: 2*1/1.5, lambda: 1.3333333),
    (4, lambda: (1-1/4)*2e-6, lambda: 1.5e-6),
    (5, lambda: 2*math.pi*8.8541878128e-12*.01*3e6, lambda: 1.67e-6),
    (6, lambda: .52e-3/(8.8541878128e-12*6)*5.2e-9, lambda: 0.0509),
    (7, lambda: 8.8541878128e-12*(1-1/4)*1000*math.sin(math.pi/6), lambda: 3.3203e-9),
    (8, lambda: .0006-8.8541878128e-12*5e-5/(8.8541878128e-12*5e-5/.0006+.25e-12), lambda: .000152),
    (9, lambda: 3e-6*5e-5/(8.8541878128e-12*2.3), lambda: 7.37),
    (10, lambda: 8.8541878128e-12*3e6/5e4, lambda: 5.31e-10),
    (11, lambda: 4*math.pi*8.8541878128e-12*.18, lambda: 2.00e-11),
    (12, lambda: 2*math.pi*8.8541878128e-12*.1/math.log(1000), lambda: 8.05e-13),
    (13, lambda: (8-1)*8.8541878128e-12*.02/.0005, lambda: 2.479e-9),
    (14, lambda: 8.8541878128e-12*.02*(1/.0005+1/(2*.00025)), lambda: 7.083e-10),
    (15, lambda: sum(8.8541878128e-12*.1*(.2/1000)/( .001+.00005*(i+.5)/1000) for i in range(1000)), lambda: 8.8541878128e-12*.2*.1/.00005*math.log(1+.00005/.001)),
    (16, lambda: 1.5/(.60*2.0-(2.0-1.5)), lambda: 15/7),
    (17, lambda: (.101)/(.1), lambda: 1.01),
    (18, lambda: (12*(2+2))/(12+2+2), lambda: 3.0),
    (19, lambda: 2*2*4/(2+4), lambda: 8/3),
    (20, lambda: 1+(33-1)*.25, lambda: 9.0),
    (21, lambda: (1+3)/2, lambda: 2.0),
    (22, lambda: (2*480)/(4+6), lambda: 96),
    (23, lambda: .5*100e-12*100**2-.5*(100e-12*(100/30))*30**2, lambda: 3.5e-7),
    (24, lambda: -(1e-8)**2*.0002/(2*8.8541878128e-12*.01), lambda: -1.1294e-7),
    (25, lambda: .5*5000**2*(2*math.pi*8.8541878128e-12/math.log(.07/.05)), lambda: 2.067e-3),
    (26, lambda: .5*100**2*8.8541878128e-12*.02*(4-1)/.001, lambda: 2.656e-6),
    (27, lambda: 2*.1*.3/(.1+.3), lambda: 0.15),
    (28, lambda: 3/4-3/4, lambda: 0),
    (29, lambda: 2e-6/(1+3), lambda: 5e-7),
    (30, lambda: -13.6/(15.8**2), lambda: -0.05448),
]

def main():
    q = (ROOT / f"chapters/{CHAPTER:02d}/questions.tex").read_text(encoding="utf-8")
    s = (ROOT / f"chapters/{CHAPTER:02d}/solutions.tex").read_text(encoding="utf-8")
    assert len(CASES) == 30
    assert [n for n, _, _ in CASES] == list(range(1, 31))
    for number, compute, reference in CASES:
        tag = rf"\paragraph{{习题 {ch}.{number}}}"
        if tag not in q or tag not in s:
            raise AssertionError(f"Missing previously transcribed candidate {ch}.{number}")
        obtained, expected = compute(), reference()
        if not (math.isfinite(obtained) and math.isfinite(expected) and
                math.isclose(obtained, expected, rel_tol=0.025,
                             abs_tol=1e-12 if expected == 0 else 0)):
            raise AssertionError(f"{ch}.{number}: {obtained!r} vs {expected!r}")
    print("PASS chapter 15: 30 candidate model/physical-identity checks")
    print("Source PDF revalidation: NOT DONE; new original exercises: 0")

if __name__ == "__main__":
    main()
