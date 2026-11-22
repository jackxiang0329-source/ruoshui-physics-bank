#!/usr/bin/env python3
"""Technical checkpoints for previously transcribed chapter-30 candidate solutions.
These are mathematical-model samples, not source-PDF verification or expert certification.
"""
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CHAPTER=30
CASES=[
    (1, lambda: 2*79*1.439965/6*(1+4/197), lambda: 38.7),
    (2, lambda: (8*1.007825+8*1.008665-15.994915)*931.494, lambda: 127.7),
    (3, lambda: 53*(26/56)**(2/3), lambda: 32),
    (4, lambda: 1.52*11**(1/3), lambda: 3.38),
    (5, lambda: 3*28.3+3*2.42, lambda: 92.16),
    (6, lambda: -17.8*(232**(2/3))*(2**(1/3)-1)+.71*90**2/(232**(1/3))*(1-2**(-2/3)), lambda: 169),
    (7, lambda: 7.3458*12**(2/3)-.8345*6**2/(12**(1/3)), lambda: 25.4),
    (8, lambda: (2*3**2-2**2)**.5, lambda: math.sqrt(14)),
    (9, lambda: (math.log(2)/(1.3e9*365.25*86400))*(.0037*70/.0391*6.02214076e23*1.2e-4), lambda: 8.1e3),
    (10, lambda: 1600/(4.46e9), lambda: 3.587e-7),
    (11, lambda: 4/30*2**(24/13.1), lambda: .475),
    (12, lambda: 300e3/30*2**(-10/14.97), lambda: 6.29e3),
    (13, lambda: 8270*math.log((.3*6.02214076e23*1.3e-12)/((9/60)*(8270*365.25*86400))), lambda: 1.5e4),
    (14, lambda: 4.46e9/math.log(2)*math.log(1+(.12/206)/(.30/238)), lambda: 2.45e9),
    (15, lambda: 4.7825*4/222, lambda: .08617),
    (16, lambda: .09/931.494, lambda: 9.66e-5),
    (17, lambda: (1.74e14)/(2e12*4), lambda: 21.75),
    (18, lambda: -math.log(.05)/(8.64*6.02214076e23/112.4*4e-21), lambda: .0162),
    (19, lambda: (-4.06)+(-2.72)+7.55, lambda: .77),
    (20, lambda: 4.06*(1+1/13), lambda: 4.37),
    (21, lambda: (1.5e30/(4*1.67e-27))*(24.67e6*1.602176634e-19)/(3.9e26)/(365.25*86400), lambda: 7.2e10),
    (22, lambda: 2*.511, lambda: 1.022),
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
 print("PASS: 30, 22 math/physics checkpoints on existing candidate pairs")
 print("Scan-original and independent expert review remain pending; new source questions: zero")
if __name__=="__main__":main()
