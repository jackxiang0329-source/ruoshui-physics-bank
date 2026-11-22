#!/usr/bin/env python3
"""Technical checkpoints for previously transcribed chapter-27 candidate solutions.
These are mathematical-model samples, not source-PDF verification or expert certification.
"""
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CHAPTER=27
CASES=[
    (1, lambda: 6.62607015e-34**2/(8*1e-17*(1e-5)**2)*(101**2-100**2), lambda: 1.103e-38),
    (2, lambda: 6.62607015e-34**2/(8*((32e-3)/6.02214076e23)*(.10)**2), lambda: 1.033e-40),
    (3, lambda: 5-1, lambda: 4),
    (4, lambda: .25-1/(2*math.pi), lambda: .0908451),
    (5, lambda: 1/12-1/(2*math.pi**2*1**2), lambda: .03267),
    (6, lambda: math.sin(math.pi)*math.sin(2*math.pi), lambda: 0),
    (7, lambda: (5**2)/(4**2), lambda: 25/16),
    (8, lambda: 2*.10/5, lambda: .04),
    (9, lambda: (1**2+1**2+1**2), lambda: 3),
    (10, lambda: .5*1.054571817e-34*1e12, lambda: 5.27286e-23),
    (11, lambda: (1.054571817e-34*math.sqrt(1.13e3/1.67e-27))/1.602176634e-19, lambda: .5414),
]
def main():
 q=(ROOT/f"chapters/{CHAPTER:02d}/questions.tex").read_text(encoding="utf-8")
 s=(ROOT/f"chapters/{CHAPTER:02d}/solutions.tex").read_text(encoding="utf-8")
 assert len(CASES)==11 and [i for i,_,_ in CASES]==list(range(1,12))
 for n,calc,expected in CASES:
  tag=rf"\paragraph{{习题 {CHAPTER}.{n}}}"
  if tag not in q or tag not in s:
   raise AssertionError(f"Missing candidate {CHAPTER}.{n}")
  result,ref=calc(),expected()
  if not math.isfinite(result) or not math.isfinite(ref) or not math.isclose(result,ref,rel_tol=.025,abs_tol=1e-12 if ref==0 else 0):
   raise AssertionError(f"{CHAPTER}.{n}: {result!r}, expected {ref!r}")
 print("PASS: 27, 11 math/physics checkpoints on existing candidate pairs")
 print("Scan-original and independent expert review remain pending; new source questions: zero")
if __name__=="__main__":main()
