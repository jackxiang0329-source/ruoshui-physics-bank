#!/usr/bin/env python3
"""One numeric/physical-identity checkpoint for each existing chapter-24 candidate.
Not an original PDF figure or source-answer validation.
"""
import math
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CHAPTER = 24
CASES = [
    (1, lambda: .5*(math.cos(math.pi/6)**4), lambda: .28125),
    (2, lambda: math.degrees(math.acos(math.sqrt(1/3))), lambda: 54.74),
    (3, lambda: (.5*math.cos(.5)**2)/(math.cos(.5)**2+math.sin(.5)**2*math.cos(.3)**2), lambda: .515),
    (4, lambda: 1*math.sin(math.pi/6)/1.5, lambda: 1/3),
    (5, lambda: math.degrees(math.atan(1.5/1.33)), lambda: 48.43),
    (6, lambda: math.sin(math.pi/4), lambda: 1/math.sqrt(2)),
    (7, lambda: math.tan(math.radians(58)), lambda: 1.60),
    (8, lambda: 90-math.degrees(math.atan(1.33)), lambda: 36.94),
    (9, lambda: math.degrees(math.asin(1.4864*.5)), lambda: 48.0),
    (10, lambda: (1*0)+(0*1), lambda: 0),
    (11, lambda: .5*.5*(math.sin(2*math.pi/3)**2), lambda: 3/16),
    (12, lambda: 632.8e-9/(4*(1.66-1.49)), lambda: 9.31e-7),
    (13, lambda: 2*math.pi*200/400, lambda: math.pi),
    (14, lambda: math.degrees(math.asin(1.55/1.658)), lambda: 69.2),
    (15, lambda: math.pi*(1.55821-1.55810)/(396.8e-9), lambda: 871),
    (16, lambda: 4*math.pi*(1/8), lambda: math.pi/2),
]
def main():
 q = (ROOT / f"chapters/{CHAPTER:02d}/questions.tex").read_text(encoding="utf-8")
 s = (ROOT / f"chapters/{CHAPTER:02d}/solutions.tex").read_text(encoding="utf-8")
 assert len(CASES) == 16
 assert [n for n, _, _ in CASES] == list(range(1, 17))
 for n, calc, expected in CASES:
  tag = rf"\paragraph{{习题 {CHAPTER}.{n}}}"
  if tag not in q or tag not in s:
   raise AssertionError(f"Missing existing candidate {CHAPTER}.{n}")
  result, reference = calc(), expected()
  if not (math.isfinite(result) and math.isfinite(reference) and
          math.isclose(result, reference, rel_tol=.025,
                       abs_tol=1e-12 if reference==0 else 0)):
   raise AssertionError(f"{CHAPTER}.{n}: {result} differs from {reference}")
 print("PASS: 24 16 existing-candidate optics checkpoints; source/figure review unresolved")
if __name__ == "__main__": main()
