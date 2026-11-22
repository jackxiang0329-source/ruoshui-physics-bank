#!/usr/bin/env python3
"""Independent calculation checkpoints for already transcribed chapter 14 candidates.
Not a scan-page crosscheck, complete derivation audit, or expert certification.
"""
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHAPTER = 14
CASES = [
    (1, lambda: 1e-6/8.8541878128e-12, lambda: 1.1294e5),
    (2, lambda: (5617.0/8.9875517923e9-2e-8/.1)/(1/.06-1/.08+1/.1), lambda: 3e-8),
    (3, lambda: 8.9875517923e9*(3e-8*(1/.06-1/.08)+5e-8/.10), lambda: 5.62e3),
    (4, lambda: -2e-8*.1/.4, lambda: -5e-9),
    (5, lambda: 1.3e-5*.03/(.05+.03), lambda: 4.875e-6),
    (6, lambda: 8.9875517923e9*(2e-8-1e-8)*1e-9/(10**2), lambda: 8.98755e-10),
    (7, lambda: (1e-6)**2/(2*8.8541878128e-12), lambda: 0.05647),
    (8, lambda: 9.15e6*320e-6, lambda: 2928),
    (9, lambda: 1-1/math.sqrt(1+3**2), lambda: 0.683772),
    (10, lambda: 8.9875517923e9*(1e-9)**2/(4*.1), lambda: 2.2469e-8),
    (11, lambda: (1-1/math.sqrt(1+3)), lambda: 0.5),
    (12, lambda: -1e-8/(math.pi*8.8541878128e-12*5), lambda: -71.90),
    (13, lambda: 10*(.05/18)*6.02214076e23*1.602176634e-19*8.9875517923e9/6.37e6, lambda: 3.78e6),
    (14, lambda: 8.9875517923e9*(1e-6)**2/(8*.2**2), lambda: 0.028086),
]

def main():
    q = (ROOT / f"chapters/{CHAPTER:02d}/questions.tex").read_text(encoding="utf-8")
    s = (ROOT / f"chapters/{CHAPTER:02d}/solutions.tex").read_text(encoding="utf-8")
    assert len(CASES) == 14
    assert [n for n, _, _ in CASES] == list(range(1, 15))
    for number, compute, reference in CASES:
        tag = rf"\paragraph{{习题 {ch}.{number}}}"
        if tag not in q or tag not in s:
            raise AssertionError(f"Missing previously transcribed candidate {ch}.{number}")
        obtained, expected = compute(), reference()
        if not (math.isfinite(obtained) and math.isfinite(expected) and
                math.isclose(obtained, expected, rel_tol=0.025,
                             abs_tol=1e-12 if expected == 0 else 0)):
            raise AssertionError(f"{ch}.{number}: {obtained!r} vs {expected!r}")
    print("PASS chapter 14: 14 candidate model/physical-identity checks")
    print("Source PDF revalidation: NOT DONE; new original exercises: 0")

if __name__ == "__main__":
    main()
