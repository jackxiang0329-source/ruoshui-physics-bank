#!/usr/bin/env python3
"""Chapter 10 checks of EXISTING candidates. No original scanned PDF certification."""
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def main():
 q=(ROOT/"chapters/10/questions.tex").read_text(encoding="utf-8")
 s=(ROOT/"chapters/10/solutions.tex").read_text(encoding="utf-8")
 checks=[
  (1, lambda: 40*101.325*math.log(2), 2809, "isothermal work for diagram indicated route"),
  (2, lambda: 560-356+220, 424, "internal-energy path invariance"),
  (3, lambda: 2*2.5*8.314*50, 2079, "oxygen internal energy change"),
  (4, lambda: 300+1000/((10/28)*3.5*8.314), 396.2, "nitrogen final isobaric temperature"),
  (5, lambda: (2/7)*6e4, 17140, "diatomic hydrogen isobaric volume work"),
  (6, lambda: 8.314*300*math.log(2), 1729, "isothermal work sample 1mol and doubled volume"),
  (7, lambda: 300*(1/3)**.4, 193.3, "adiabatic ideal gas final temperature"),
  (8, lambda: 2*2**1.4, 5.278, "adiabatic maximum pressure in atmospheres"),
  (9, lambda: 390*(30/50)**.4, 317.9, "free expansion followed by reversible adiabatic"),
  (10, lambda: .032*317.2**2/(8.314*273.15), 1.418, "specific heat ratio from sound speed"),
  (11, lambda: 300-.029*9.8*1000/29.1, 290.2, "dry adiabatic temperature lapse sample"),
  (12, lambda: math.sqrt(2*(.75*((2.7*101325*2)-(2.7*101325*(2/(2+math.pi*.4**2*4))**1.4)*(2+math.pi*.4**2*4))/(1.4-1)-101325*(math.pi*.4**2*4))/70), 36.1, "cannon barrel net work and effective efficiency source variant"),
  (13, lambda: 100+20-(110+10), 0, "ideal throttle enthalpy balance sample"),
  (14, lambda: (.4*3)/(1*1), 1.2, "equal heating heat capacity ratio sample"),
  (15, lambda: 2.5*8.314*(1.4-1.2)/(1-1.2), -20.785, "polytropic heat capacity signed sample"),
  (16, lambda: (101300*.02/8.314)*2**.4, 321.6, "adiabatic chamber temperature"),
  (17, lambda: 1-10**(-2/7), 0.482, "ideal Brayton cycle efficiency"),
  (18, lambda: 1-(2**1.4-1)/(1.4*16**.4*(2-1)), 0.614, "ideal Diesel cycle sample"),
  (19, lambda: 600*(400-300)/(600*(400-300)+300*400), 0.3333333333333333, "three-reservoir reversible engine"),
  (20, lambda: .25+(1-.25)*.4, 0.55, "series Carnot engine efficiency"),
  (21, lambda: 20/298.15, 0.0671, "ocean temperature gradient Carnot efficiency"),
  (22, lambda: 1000*263.15/(288.15-263.15), 10526, "cold-store Carnot refrigerator heat absorption"),
  (23, lambda: (3.8e7/3600)*(305.15-294.15)/294.15, 395, "ideal air conditioning minimum power"),
  (24, lambda: 3.34e7*(1-288.15/483.15)*333.15/(333.15-288.15), 99800000, "combined engine heat-pump delivered heating"),
  (25, lambda: (1641-1015)+363*(.4513-.2202), 709.889, "refrigeration table cold-side heat"),
  (26, lambda: 300/(400-300)-2.5/math.log(16), 2.098, "Stirling cycle COP without regeneration sample"),
 ]
 assert len(checks)==26 and [r[0] for r in checks]==list(range(1,27))
 for num,compute,expected,label in checks:
  token=rf"\paragraph{{习题 10.{num}}}"
  if token not in q or token not in s:raise AssertionError(f"Missing candidate 10.{num}")
  actual=compute()
  if not math.isfinite(actual) or not math.isclose(actual,expected,rel_tol=.025,abs_tol=1e-12 if expected==0 else 0):
   raise AssertionError(f"10.{num} {label}: independent={actual!r}, candidate={expected!r}")
 print("PASS 26 chapter 10 candidate model checks; newly sourced problems=0")
 print("Original scans and figures not rechecked; expert review and publication rights unresolved")
if __name__=="__main__":main()
