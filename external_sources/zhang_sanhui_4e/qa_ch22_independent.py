#!/usr/bin/env python3
"""One numeric/physical-identity checkpoint for each existing chapter-22 candidate.
Not an original PDF figure or source-answer validation.
"""
import math
from pathlib import Path
ROOT = Path(__file__).resolve().parent
CHAPTER = 22
CASES = [
    (1, lambda: 2.998e8*1e-8/(589.3e-9), lambda: 5.09e6),
    (2, lambda: .60e-3*2.27e-3/2.5, lambda: 5.448e-7),
    (3, lambda: 2*.002, lambda: .004),
    (4, lambda: .036/(10-1), lambda: .004),
    (5, lambda: math.degrees(math.asin(.5*1-.125)), lambda: 22.0),
    (6, lambda: 12*4.5/50, lambda: 1.08),
    (7, lambda: .001*(math.sin(.01)-math.sin(.005)), lambda: 5e-6),
    (8, lambda: 2*.1*math.sin(.03), lambda: .0059991),
    (9, lambda: math.cos(math.pi/4)**2, lambda: .5),
    (10, lambda: 632.8e-9/math.cos(math.pi/4), lambda: 8.95e-7),
    (11, lambda: 1/(1.3e9), lambda: 7.69e-10),
    (12, lambda: 550e-9/.01, lambda: 55e-6),
    (13, lambda: 7*550e-9/(1.5-1), lambda: 7.7e-6),
    (14, lambda: 600e-9/(4*1.5), lambda: 1e-7),
    (15, lambda: 4*1.5*.4e-6/5, lambda: 480e-9),
    (16, lambda: 560e-9/(4*1.4), lambda: 1e-7),
    (17, lambda: 485*679/(2*1.32*(679-485)), lambda: 643),
    (18, lambda: 600e-9/(4*1.33*math.sqrt(1-(math.sin(math.pi/4)/1.33)**2)), lambda: 1.3376e-7),
    (19, lambda: 550e-9/(4*1.38), lambda: 9.964e-8),
    (20, lambda: (25**2-15**2)/(20*100), lambda: 0.2),
    (21, lambda: 2*(1.5-1)*.003, lambda: .003),
    (22, lambda: 2*.3220e-3/1204, lambda: 5.349e-7),
    (23, lambda: 1+98*589.3e-9/.2, lambda: 1.000289),
]
def main():
 q = (ROOT / f"chapters/{CHAPTER:02d}/questions.tex").read_text(encoding="utf-8")
 s = (ROOT / f"chapters/{CHAPTER:02d}/solutions.tex").read_text(encoding="utf-8")
 assert len(CASES) == 23
 assert [n for n, _, _ in CASES] == list(range(1, 24))
 for n, calc, expected in CASES:
  tag = rf"\paragraph{{习题 {CHAPTER}.{n}}}"
  if tag not in q or tag not in s:
   raise AssertionError(f"Missing existing candidate {CHAPTER}.{n}")
  result, reference = calc(), expected()
  if not (math.isfinite(result) and math.isfinite(reference) and
          math.isclose(result, reference, rel_tol=.025,
                       abs_tol=1e-12 if reference==0 else 0)):
   raise AssertionError(f"{CHAPTER}.{n}: {result} differs from {reference}")
 print("PASS: 22 23 existing-candidate optics checkpoints; source/figure review unresolved")
if __name__ == "__main__": main()
