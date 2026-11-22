#!/usr/bin/env python3
"""Technical checkpoints for previously transcribed chapter-29 candidate solutions.
These are mathematical-model samples, not source-PDF verification or expert certification.
"""
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CHAPTER=29
CASES=[
    (1, lambda: 19.3e3*6.02214076e23/.197, lambda: 5.90e28),
    (2, lambda: 3*5/5, lambda: 3),
    (3, lambda: 3/4*1e6, lambda: 7.5e5),
    (4, lambda: (1.054571817e-34**2/(2*1.675e-27)*(3*math.pi**2*(5e16/1.675e-27))**(2/3))/1.602176634e-19, lambda: 1.91e7),
    (5, lambda: .3*5/(math.pi**2*8.617333262e-5), lambda: 1.76e3),
    (6, lambda: math.sqrt(2.08e-3/2.57e-3), lambda: .900),
    (7, lambda: 10.5e3*6.02214076e23/.1078682, lambda: 5.86e28),
    (8, lambda: 1/(math.exp(.10/(8.617333262e-5*1000))+1), lambda: .239),
    (9, lambda: 1239.842/5.5, lambda: 225),
    (10, lambda: (1e6-1)*1e16/(2.33e3/28.085e-3*6.02214076e23), lambda: 2e-7),
    (11, lambda: 1239.842/.045, lambda: 27552),
    (12, lambda: 1239.842/2.42, lambda: 512),
    (13, lambda: 1239.842/1.90, lambda: 653),
    (14, lambda: 1239.842/140, lambda: 8.86),
]
def main():
 q=(ROOT/f"chapters/{CHAPTER:02d}/questions.tex").read_text(encoding="utf-8")
 s=(ROOT/f"chapters/{CHAPTER:02d}/solutions.tex").read_text(encoding="utf-8")
 assert len(CASES)==14 and [i for i,_,_ in CASES]==list(range(1,15))
 for n,calc,expected in CASES:
  tag=rf"\paragraph{{习题 {CHAPTER}.{n}}}"
  if tag not in q or tag not in s:
   raise AssertionError(f"Missing candidate {CHAPTER}.{n}")
  result,ref=calc(),expected()
  if not math.isfinite(result) or not math.isfinite(ref) or not math.isclose(result,ref,rel_tol=.025,abs_tol=1e-12 if ref==0 else 0):
   raise AssertionError(f"{CHAPTER}.{n}: {result!r}, expected {ref!r}")
 print("PASS: 29, 14 math/physics checkpoints on existing candidate pairs")
 print("Scan-original and independent expert review remain pending; new source questions: zero")
if __name__=="__main__":main()
