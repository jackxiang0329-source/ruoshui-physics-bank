#!/usr/bin/env python3
"""One numeric/physical-identity checkpoint for each existing chapter-23 candidate.
Not an original PDF figure or source-answer validation.
"""
import math
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CHAPTER = 23
CASES = [
    (1, lambda: 2*.5*550e-9/1e-4, lambda: .0055),
    (2, lambda: 632.8e-9/math.sin(math.radians(5)), lambda: 7.26e-6),
    (3, lambda: 5*600e-9/7, lambda: 4.286e-7),
    (4, lambda: math.degrees(2*math.asin(20/50)), lambda: 47.16),
    (5, lambda: .023*1.917e-4, lambda: 4.41e-6),
    (6, lambda: 2*math.asin(1.22*.1/1500), lambda: 1.627e-4),
    (7, lambda: 1.2*.005/(1.22*550e-9), lambda: 8.94e3),
    (8, lambda: 1.22*500e-9/(.05/160000), lambda: 1.95),
    (9, lambda: 1.22*.20/300, lambda: 8.133e-4),
    (10, lambda: .05/1e7, lambda: 5e-9),
    (11, lambda: 1.22*550e-9/(14*math.pi/(180*3600)), lambda: .00989),
    (12, lambda: .5*480e-9/1e-4, lambda: .0024),
    (13, lambda: .020/6000, lambda: 3.333e-6),
    (14, lambda: .01/6000*math.sin(math.radians(20)), lambda: 570e-9),
    (15, lambda: 2*656.3e-9/math.sin(math.radians(41)), lambda: 2e-6),
    (16, lambda: math.ceil(656.3/.18), lambda: 3647),
    (17, lambda: math.asin(1.292/(192*6)), lambda: 1.122e-3),
    (18, lambda: 2*.275*math.sin(math.pi/4), lambda: .3889),
    (19, lambda: .215*math.sin(math.radians(50)), lambda: .165),
]
def main():
 q = (ROOT / f"chapters/{CHAPTER:02d}/questions.tex").read_text(encoding="utf-8")
 s = (ROOT / f"chapters/{CHAPTER:02d}/solutions.tex").read_text(encoding="utf-8")
 assert len(CASES) == 19
 assert [n for n, _, _ in CASES] == list(range(1, 20))
 for n, calc, expected in CASES:
  tag = rf"\paragraph{{习题 {CHAPTER}.{n}}}"
  if tag not in q or tag not in s:
   raise AssertionError(f"Missing existing candidate {CHAPTER}.{n}")
  result, reference = calc(), expected()
  if not (math.isfinite(result) and math.isfinite(reference) and
          math.isclose(result, reference, rel_tol=.025,
                       abs_tol=1e-12 if reference==0 else 0)):
   raise AssertionError(f"{CHAPTER}.{n}: {result} differs from {reference}")
 print("PASS: 23 19 existing-candidate optics checkpoints; source/figure review unresolved")
if __name__ == "__main__": main()
