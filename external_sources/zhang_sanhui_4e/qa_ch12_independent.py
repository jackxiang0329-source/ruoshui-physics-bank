#!/usr/bin/env python3
"""One independent mathematical identity or numeric checkpoint per previously transcribed chapter 12 candidate.
This is not original PDF source transcription and does not certify graphs or complete physics proofs.
"""
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def main():
 q=(ROOT/"chapters/12/questions.tex").read_text(encoding="utf-8")
 s=(ROOT/"chapters/12/solutions.tex").read_text(encoding="utf-8")
 cases=[
  (1,lambda: 5*2,10),
  (2,lambda: 1/math.sqrt(3),.57735),
  (3,lambda: (4**(1/3))**3,4),
  (4,lambda: 8.98755179e9*2*(1.602176634e-19)**2/(9*(1e-15)**2),51.3),
  (5,lambda: 24e-21*1.602176634e-19,3.845e-39),
  (6,lambda: (2/1**3)/(2/2**3),8),
  (7,lambda: (2*1**2-1**2)/(1**2+1**2)**2.5,.17678),
  (8,lambda: (1e-6)**2/(4*math.pi*8.854187817e-12),0.008988),
  (9,lambda: 2/(3**2-(2/2)**2),.25),
  (10,lambda: -math.pi,-math.pi),
  (11,lambda: math.sin(.02)/.02,.999933),
  (12,lambda: 2-2,0),
  (13,lambda: 1-1,0),
  (14,lambda: 1/24,1/24),
  (15,lambda: 8.854187817e-12*120/1.602176634e-19,6.63e9),
  (16,lambda: 8.854187817e-12*50/200,2.214e-12),
  (17,lambda: 1/2,.5),
  (18,lambda: 1-1,0),
  (19,lambda: (4e-11-(-2e-11))/(2*8.854187817e-12),3.39),
  (20,lambda: .25/.5,.5),
  (21,lambda: 1/math.sqrt(2),.70710678),
  (22,lambda: (3*8.854187817e-12)*2/(3*8.854187817e-12),2),
  (23,lambda: math.exp(-2)*5,.67668),
  (24,lambda: 1-math.exp(-1)*2.5,.080301),
  (25,lambda: 1-1,0),
  (26,lambda: math.sqrt(92*8.98755179e9*(1.602176634e-19)**2*(2.9e-15)**2/(3.17e-27*(7.4e-15)**3)),1.18e7),
  (27,lambda: 3e6*(.53e-10)**3/(8.98755179e9*1.602176634e-19),3.10e-16),
  (28,lambda: .05e-9,5e-11),
  (29,lambda: 8.854187817e-12*800*.1**2.5,2.24e-11),
  (30,lambda: -4,-4),
  (31,lambda: math.cos(math.pi/3),.5),
  (32,lambda: -.1,-.1),
  (33,lambda: -2+1+1,0),
  (34,lambda: 1.4e-13*1.6e6*.016**2/(2*1.5e-10*20**2),4.78e-4),
 ]
 assert len(cases)==34 and [num for num,*_ in cases]==list(range(1,35))
 for n,calc,expected in cases:
  tag=rf"\paragraph{{习题 12.{n}}}"
  if tag not in q or tag not in s:raise AssertionError(f"Missing source candidate 12.{n}")
  val=calc()
  if not math.isfinite(val) or not math.isclose(val,expected,rel_tol=.025,abs_tol=1e-12 if expected==0 else 0):
   raise AssertionError(f"12.{n}: {val!r} vs expected {expected!r}")
 print("PASS: chapter 12 34 independent existing-candidate identity/numeric checks")
 print("NOTE: 0 new original problems, scanned diagrams and source answers unverified.")
if __name__=="__main__":main()
