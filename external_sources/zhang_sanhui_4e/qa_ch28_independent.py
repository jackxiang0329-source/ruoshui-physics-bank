#!/usr/bin/env python3
"""Technical checkpoints for previously transcribed chapter-28 candidate solutions.
These are mathematical-model samples, not source-PDF verification or expert certification.
"""
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CHAPTER=28
CASES=[
    (1, lambda: 36/(5*1.097e7), lambda: 656e-9),
    (2, lambda: 13.6*(1-1/25), lambda: 13.06),
    (3, lambda: 1.054571817e-34**2/(2*9.1093837e-31*(5.2917721e-11)**2)/1.602176634e-19, lambda: 13.6),
    (4, lambda: -2*13.6, lambda: -27.2),
    (5, lambda: 9.1093837e-31*1.602176634e-19**4/(8*8.8541878128e-12**2*6.62607015e-34**3*2.99792458e8), lambda: 1.0973732e7),
    (6, lambda: 2*5.291772109e-11, lambda: 1.058e-10),
    (7, lambda: (3**2)/(2**2), lambda: 2.25),
    (8, lambda: (440-434)/434, lambda: 0.01382),
    (9, lambda: 1/(2*math.pi*1e-8), lambda: 1.5915e7),
    (10, lambda: math.sqrt(1.380649e-23*300/(1.6735575e-27*(2.99792458e8)**2)), lambda: 5.26e-6),
    (11, lambda: (4*1**2)*math.exp(-2*1), lambda: 4*math.exp(-2)),
    (12, lambda: 3*5.291772109e-11/2, lambda: 7.93766e-11),
    (13, lambda: (1/5.291772109e-11)*5.291772109e-11, lambda: 1),
    (14, lambda: 1/3, lambda: .3333333),
    (15, lambda: 1/math.sqrt(1*(1+1)), lambda: .7071),
    (16, lambda: 4.5e-5*1.602176634e-19/6.62607015e-34, lambda: 1.088e10),
    (17, lambda: .5/math.sqrt(.5*(.5+1)), lambda: 1/math.sqrt(3)),
    (18, lambda: 9.274e-24*1.5e3, lambda: 1.391e-20),
    (19, lambda: 2*1.41e-26*1.6/6.62607015e-34, lambda: 6.81e7),
    (20, lambda: 2*(2*2+1), lambda: 10),
    (21, lambda: 2+2+1, lambda: 5),
    (22, lambda: 1239.842/30000, lambda: 0.04133),
    (23, lambda: 1239.842/.1, lambda: 12398.42),
    (24, lambda: 1.239842/20, lambda: 0.0619921),
    (25, lambda: 1239.842/3.16, lambda: 392.35),
    (26, lambda: 1.239842/(8.979-0.951), lambda: 0.15444),
    (27, lambda: 1239.842/10600, lambda: 0.11697),
    (28, lambda: 2.99792458e8*10e-15/(800e-9), lambda: 3.7474),
    (29, lambda: 2.99792458e8*12e-12, lambda: .0035975),
    (30, lambda: .005*632.8e-9/(6.62607015e-34*2.99792458e8), lambda: 1.59e16),
    (31, lambda: 5/(math.pi*(.0015)**2), lambda: 7.07e5),
    (32, lambda: 6.62607015e-34/(2*math.pi**2*1e-46), lambda: 3.36e11),
    (33, lambda: 2*(2/5)*9.1093837e-31*(1e-10)**2, lambda: 7.2875e-51),
    (34, lambda: (12*16/28)*1.66053906660e-27, lambda: 1.139e-26),
]
def main():
 q=(ROOT/f"chapters/{CHAPTER:02d}/questions.tex").read_text(encoding="utf-8")
 s=(ROOT/f"chapters/{CHAPTER:02d}/solutions.tex").read_text(encoding="utf-8")
 assert len(CASES)==34 and [i for i,_,_ in CASES]==list(range(1,35))
 for n,calc,expected in CASES:
  tag=rf"\paragraph{{习题 {CHAPTER}.{n}}}"
  if tag not in q or tag not in s:
   raise AssertionError(f"Missing candidate {CHAPTER}.{n}")
  result,ref=calc(),expected()
  if not math.isfinite(result) or not math.isfinite(ref) or not math.isclose(result,ref,rel_tol=.025,abs_tol=1e-12 if ref==0 else 0):
   raise AssertionError(f"{CHAPTER}.{n}: {result!r}, expected {ref!r}")
 print("PASS: 28, 34 math/physics checkpoints on existing candidate pairs")
 print("Scan-original and independent expert review remain pending; new source questions: zero")
if __name__=="__main__":main()
