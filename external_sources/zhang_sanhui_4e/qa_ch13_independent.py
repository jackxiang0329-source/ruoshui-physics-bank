#!/usr/bin/env python3
"""One independent mathematical identity or numeric checkpoint per previously transcribed chapter 13 candidate.
This is not original PDF source transcription and does not certify graphs or complete physics proofs.
"""
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def main():
 q=(ROOT/"chapters/13/questions.tex").read_text(encoding="utf-8")
 s=(ROOT/"chapters/13/solutions.tex").read_text(encoding="utf-8")
 cases=[
  (1,lambda: 8.98755179e9*(1e-8/.2+1.5e-8/.3),899),
  (2,lambda: 10*1*2/((2-1)*1.5**2),8.889),
  (3,lambda: 6/60,.1),
  (4,lambda: 1/.1-1/.3,6.666667),
  (5,lambda: math.log((3+1)/(3-1)),math.log(2)),
  (6,lambda: 8.98755179e9*2e-7*math.log((.05+.15)/.05),2490),
  (7,lambda: math.log(3),math.log(3)),
  (8,lambda: 1000/(6.35e-6*math.log(.01/6.35e-6)),2.14e7),
  (9,lambda: 1/2,.5),
  (10,lambda: math.sqrt(2**2),2),
  (11,lambda: 2-(2/2),1),
  (12,lambda: 2**(2/3),1.5874),
  (13,lambda: 3/2,1.5),
  (14,lambda: 1/math.sqrt((100-.1/2)**2+1)-1/math.sqrt((100+.1/2)**2+1),1e-5),
  (15,lambda: 2/(3**2-1**2),.25),
  (16,lambda: 2*1*2/abs(1-2**2),4/3),
  (17,lambda: 2*2*2/abs(1-2**2),8/3),
  (18,lambda: 30*1e9/(3.6e6*20),417),
  (19,lambda: math.sqrt(2*1.602176634e-19*2.5e4/9.1093837e-31),9.38e7),
  (20,lambda: -2*math.sqrt(3),-3.4641),
  (21,lambda: (-1e-5*.05+3e-5*.07)/(2*8.854187817e-12),9.04e4),
  (22,lambda: math.sqrt(9),3),
  (23,lambda: math.sqrt(5)/3,.74536),
  (24,lambda: -3.5*8.98755179e9*(1.602176634e-19)**2/(.20e-10),-4.04e-17),
  (25,lambda: 12*8.98755179e9*(1.602176634e-19)**2/(3e-15*1.602176634e-13),5.76),
  (26,lambda: -math.log(2),-math.log(2)),
  (27,lambda: 8.98755179e9*(1.602176634e-19)**2/(2*9.1093837e-31*(3e8)**2),1.41e-15),
  (28,lambda: 3*8.98755179e9*(1.602176634e-19)**2/(5*1e-15*1.602176634e-13),.864),
  (29,lambda: 988*(1-2**(-2/3)),366),
  (30,lambda: 158*8.98755179e9*(1.602176634e-19)**2/(4e6*1.602176634e-19),5.69e-14),
  (31,lambda: math.sqrt(3/2),1.225),
  (32,lambda: -2,-2),
  (33,lambda: .5*8.854187817e-12*100**2,4.43e-8),
  (34,lambda: -(9.1093837e-31*(1.602176634e-19)**4)/(2*(4*math.pi*8.854187817e-12)**2*(1.054571817e-34)**2*1.602176634e-19),-13.6),
 ]
 assert len(cases)==34 and [num for num,*_ in cases]==list(range(1,35))
 for n,calc,expected in cases:
  tag=rf"\paragraph{{习题 13.{n}}}"
  if tag not in q or tag not in s:raise AssertionError(f"Missing source candidate 13.{n}")
  val=calc()
  if not math.isfinite(val) or not math.isclose(val,expected,rel_tol=.025,abs_tol=1e-12 if expected==0 else 0):
   raise AssertionError(f"13.{n}: {val!r} vs expected {expected!r}")
 print("PASS: chapter 13 34 independent existing-candidate identity/numeric checks")
 print("NOTE: 0 new original problems, scanned diagrams and source answers unverified.")
if __name__=="__main__":main()
