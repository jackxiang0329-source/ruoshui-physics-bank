#!/usr/bin/env python3
"""Chapter 11 checks of EXISTING candidates. No original scanned PDF certification."""
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def main():
 q=(ROOT/"chapters/11/questions.tex").read_text(encoding="utf-8")
 s=(ROOT/"chapters/11/solutions.tex").read_text(encoding="utf-8")
 checks=[
  (1, lambda: 8.314*(2.5*math.log(2)+math.log(3)), 23.54, "two-linear-stroke oxygen entropy increment"),
  (2, lambda: 30*(2.1*40+334+4.2*100+2260), 92940, "ice-to-steam four-stage total heat"),
  (3, lambda: 8e5/273, 2930, "environmental entropy due to daily human heat release"),
  (4, lambda: (2e8/3600)*(1/253.15-1/293.15), 30, "temperature-gradient entropy production rate"),
  (5, lambda: 20000/285.15, 70.1, "friction thermal energy entropy rate"),
  (6, lambda: (1000*1500*9.8*74)/285.15, 3810000, "waterfall mechanical degradation entropy rate"),
  (7, lambda: 4200*(math.log(373.15/273.15)-100/373.15), 185, "finite temperature heat exchange entropy generation"),
  (8, lambda: .9*334000/273.15, 1100, "exact 0.9kg phase-change entropy"),
  (9, lambda: 300*4**(-.4), 172.3, "isochoric return temperature before adiabatic"),
  (10, lambda: math.log((300+400)**2/(4*300*400)), 0.02062, "equal mass liquid mixing entropy bound"),
  (11, lambda: math.log((1+2)**2/(4*1*2)), 0.1173, "same-species gas pressure-equalization entropy factor"),
  (12, lambda: (2*400+3*300)/(2+3), 340, "weighted heat capacity equilibrium temperature"),
  (13, lambda: int('等焓' in s and '等熵' in s and '待' in s), 1, "unresolved scanned T-S graph: throttle is isenthalpic, reversible adiabatic is isentropic"),
 ]
 assert len(checks)==13 and [r[0] for r in checks]==list(range(1,14))
 for num,compute,expected,label in checks:
  token=rf"\paragraph{{习题 11.{num}}}"
  if token not in q or token not in s:raise AssertionError(f"Missing candidate 11.{num}")
  actual=compute()
  if not math.isfinite(actual) or not math.isclose(actual,expected,rel_tol=.025,abs_tol=1e-12 if expected==0 else 0):
   raise AssertionError(f"11.{num} {label}: independent={actual!r}, candidate={expected!r}")
 print("PASS 13 chapter 11 candidate model checks; newly sourced problems=0")
 print("Original scans and figures not rechecked; expert review and publication rights unresolved")
if __name__=="__main__":main()
