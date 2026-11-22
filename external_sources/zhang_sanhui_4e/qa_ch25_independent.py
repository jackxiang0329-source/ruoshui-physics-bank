#!/usr/bin/env python3
"""One numeric/physical-identity checkpoint for each existing chapter-25 candidate.
Not an original PDF figure or source-answer validation.
"""
import math
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CHAPTER = 25
CASES = [
    (1, lambda: 8/(8-1.7), lambda: 1.26984),
    (2, lambda: 1.6+2*math.tan(math.asin(math.sin(math.pi/4)/1.33)), lambda: 2.85),
    (3, lambda: math.sin(math.pi/4)/math.sin(math.radians(17)), lambda: 2.42),
    (4, lambda: 1*math.sin(math.pi/6), lambda: 1.5*math.sin(math.asin(1/3))),
    (5, lambda: math.degrees(math.asin(1/1.52)), lambda: 41.14),
    (6, lambda: ((1.52-1)/(1.52+1))**2, lambda: .0426),
    (7, lambda: math.sin(math.radians(50))/math.sin(math.pi/6), lambda: 1.532),
    (8, lambda: .15*.30/(.30-.15), lambda: .30),
    (9, lambda: 1/(1/.02+1/(-.10)), lambda: .025),
    (10, lambda: 20*30/(30-20), lambda: 60),
    (11, lambda: .4/(1.4/2.6+1/25), lambda: .691),
    (12, lambda: 1/((1-1.33)/(-20)-1.33/10), lambda: -8.58),
    (13, lambda: 1/((1.5-1)*(1/.20-1/(-.20))), lambda: .20),
    (14, lambda: math.degrees(math.acos(math.sqrt((1.333**2-1)/3))), lambda: 59.4),
    (15, lambda: .24/(1.6-1), lambda: .4),
    (16, lambda: (1**2-.2**2)/(4*1), lambda: .24),
    (17, lambda: .2*5/(5-.2), lambda: .20833),
    (18, lambda: .10*.15/(.15-.10), lambda: .30),
    (19, lambda: 1/(1/.1+1/.2), lambda: .066667),
    (20, lambda: 19.5/.10, lambda: 195),
    (21, lambda: 3*20/.2, lambda: 300),
]
def main():
 q = (ROOT / f"chapters/{CHAPTER:02d}/questions.tex").read_text(encoding="utf-8")
 s = (ROOT / f"chapters/{CHAPTER:02d}/solutions.tex").read_text(encoding="utf-8")
 assert len(CASES) == 21
 assert [n for n, _, _ in CASES] == list(range(1, 22))
 for n, calc, expected in CASES:
  tag = rf"\paragraph{{习题 {CHAPTER}.{n}}}"
  if tag not in q or tag not in s:
   raise AssertionError(f"Missing existing candidate {CHAPTER}.{n}")
  result, reference = calc(), expected()
  if not (math.isfinite(result) and math.isfinite(reference) and
          math.isclose(result, reference, rel_tol=.025,
                       abs_tol=1e-12 if reference==0 else 0)):
   raise AssertionError(f"{CHAPTER}.{n}: {result} differs from {reference}")
 print("PASS: 25 21 existing-candidate optics checkpoints; source/figure review unresolved")
if __name__ == "__main__": main()
