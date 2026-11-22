#!/usr/bin/env python3
"""Independent numerical checks for already transcribed Zhang Sanhui Ch 8 candidates."""
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def main():
 q=(ROOT/"chapters/08/questions.tex").read_text(encoding="utf-8")
 s=(ROOT/"chapters/08/solutions.tex").read_text(encoding="utf-8")
 cases=[
  (1, lambda: math.sqrt(1-.6**2*.5), 0.90554, "angled rod longitudinal length contraction"),
  (2, lambda: math.sqrt(1-.8**2), 0.6, "moving cube contracted volume"),
  (3, lambda: 1/math.sqrt(1-.8**2), 1.66667, "different time events leave marked ruler separation"),
  (4, lambda: math.sqrt(5)*3e8, 670000000, "relativity of same-place event spatial gap"),
  (5, lambda: math.sqrt(3)/3e8, 5.78e-9, "time separation in transformed events"),
  (6, lambda: 30*3e8, 9000000000, "rocket frame reflected signal distance"),
  (7, lambda: (5/3)*(1.8e17+.8*3e8*(-6e8)), 60000000000000000, "supernova inverse coordinate transform"),
  (8, lambda: -6e8+math.hypot(1.8e17,1.2e17)/3e8, 121000000, "supernova signal delay"),
  (9, lambda: abs((-.8-.6)/(1+.8*.6)), 0.9459459459459459, "comet relativistic relative speed"),
  (10, lambda: ((.6+.8)**2+(1-.8**2)*.8**2)/(1+.8*.6)**2, 1, "light-speed invariant under aberration"),
  (11, lambda: (1-.5**2)**1.5/(1-.5*.25)**3, 0.9696, "longitudinal acceleration transform"),
  (12, lambda: 3e8/math.sqrt(2), 212132000, "constant force relativistic acceleration profile"),
  (13, lambda: math.sqrt(1-((math.sqrt(5)-1)/2)**2), 0.78615, "kinetic energy twice Newtonian at given speed"),
  (14, lambda: (3e8/(1+2800/.511)**2)/(1+math.sqrt(1-(1+2800/.511)**(-2))), 4.99, "stable electron speed deficit at 2.8 GeV"),
  (15, lambda: 3e8/(2*(50/(1.6726e-27*(3e8)**2))**2), 1.35e-15, "extreme cosmic proton c-v asymptotic"),
  (16, lambda: (1.67265+1.67495-3.34365)*1e-27*(3e8)**2/(1.602176634e-13), 2.216, "deuteron binding energy from mass defect"),
  (17, lambda: (4*1.6726-6.6425-2*.0009)/(4*1.6726), 0.00689, "source model proton fusion efficiency"),
  (18, lambda: 6.6743e-11*1.989e30/(1e4*(3e8)**2), 0.148, "Newtonian neutron-star potential conversion efficiency"),
  (19, lambda: abs((-.5-.5)/(1+.5*.5)), 0.8, "counter-moving proton relative speed"),
  (20, lambda: math.sqrt(.000511**2+.938272**2+2*.938272*(22+.000511)), 6.4935, "e-p fixed-target center mass energy"),
  (21, lambda: (5.6**2-2*.000511**2)/(2*.000511), 30700, "same collider energy requires huge fixed-target beam"),
  (22, lambda: (1.25*(5-.6*3))**2-(1.25*(3-.6*5))**2, 16, "four-momentum Lorentz scalar c=1"),
  (23, lambda: .938*1e18, 938000000000000000, "two-proton equivalent gravity energy scale"),
 ]
 assert len(cases)==23 and [c[0] for c in cases]==list(range(1,24))
 for n,f,expected,label in cases:
  tag=rf"\paragraph{{习题 8.{n}}}"
  assert tag in q and tag in s, f"missing original candidate pair {ch}.{n}"
  actual=f()
  assert math.isfinite(actual) and math.isclose(actual,expected,rel_tol=.025,abs_tol=1e-12 if expected==0 else 0), f"{ch}.{n} {label}: {actual!r} != {expected!r}"
 print("PASS 23 Ch8 independent candidate model checks; new original problems 0")
 print("NOT checked: original PDF pages or figures, expert review, copyright license")
if __name__=="__main__":main()
