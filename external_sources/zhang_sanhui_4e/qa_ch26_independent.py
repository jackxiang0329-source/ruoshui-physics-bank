#!/usr/bin/env python3
"""Technical checkpoints for previously transcribed chapter-26 candidate solutions.
These are mathematical-model samples, not source-PDF verification or expert certification.
"""
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CHAPTER=26
CASES=[
    (1, lambda: 5.670374419e-8*(268.15)**4, lambda: 293),
    (2, lambda: 6.62607015e-34*3.4e14/(2.821439*1.380649e-23), lambda: 5780),
    (3, lambda: (1e3/5.670374419e-8)**.25, lambda: 364.42),
    (4, lambda: (3.9e26/(16*math.pi*5.670374419e-8*(1.5e11)**2))**.25, lambda: 279),
    (5, lambda: 11*9.460730472e15*math.sqrt(1.7e-12/(5.670374419e-8*6600**4)), lambda: 1.31e7),
    (6, lambda: 2.821439*1.380649e-23*3/6.62607015e-34, lambda: 1.76e11),
    (7, lambda: 2.99792458e8/(500e-9)**2, lambda: 1.199e21),
    (8, lambda: (2*math.pi*math.sin(math.pi/2)**2)/4/math.pi, lambda: .5),
    (9, lambda: 3*(1-math.exp(-2.821439)), lambda: 2.821439),
    (10, lambda: 2*math.pi**5*1.380649e-23**4/(15*(6.62607015e-34)**3*(2.99792458e8)**2), lambda: 5.670374419e-8),
    (11, lambda: 1239.842/200-4.2, lambda: 2.00),
    (12, lambda: 1e-15*500e-9/(6.62607015e-34*2.99792458e8), lambda: 2.52e3),
    (13, lambda: 4*1.0**2*(2.25*1.602176634e-19)/(1*(1.3e-10)**2), lambda: 85.3),
    (14, lambda: 5*(1-.5)/math.sqrt(1-.5**2), lambda: 2.887),
    (15, lambda: .60-.60/1.2, lambda: .10),
    (16, lambda: 4000-4000/(1+2*4000/511000), lambda: 61.7),
    (17, lambda: 2*511000*1000, lambda: 1.022e9),
    (18, lambda: (581**2-(50-math.sqrt(20*(20+2*511)))**2-511**2)/(2*(581+50-math.sqrt(20*(20+2*511)))), lambda: 69.39),
    (19, lambda: 6.62607015e-34/.20e-9, lambda: 3.31e-24),
    (20, lambda: 6.62607015e-34/math.sqrt(3*1.675e-27*1.380649e-23*300), lambda: 1.45e-10),
    (21, lambda: 1239.842/math.sqrt(40000*(40000+2*511000)), lambda: 0.00602),
    (22, lambda: (2*3**2)/(math.sqrt(3**2+4**2)+5), lambda: 1.8),
]
def main():
 q=(ROOT/f"chapters/{CHAPTER:02d}/questions.tex").read_text(encoding="utf-8")
 s=(ROOT/f"chapters/{CHAPTER:02d}/solutions.tex").read_text(encoding="utf-8")
 assert len(CASES)==22 and [i for i,_,_ in CASES]==list(range(1,23))
 for n,calc,expected in CASES:
  tag=rf"\paragraph{{习题 {CHAPTER}.{n}}}"
  if tag not in q or tag not in s:
   raise AssertionError(f"Missing candidate {CHAPTER}.{n}")
  result,ref=calc(),expected()
  if not math.isfinite(result) or not math.isfinite(ref) or not math.isclose(result,ref,rel_tol=.025,abs_tol=1e-12 if ref==0 else 0):
   raise AssertionError(f"{CHAPTER}.{n}: {result!r}, expected {ref!r}")
 print("PASS: 26, 22 math/physics checkpoints on existing candidate pairs")
 print("Scan-original and independent expert review remain pending; new source questions: zero")
if __name__=="__main__":main()
