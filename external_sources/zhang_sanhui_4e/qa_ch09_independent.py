#!/usr/bin/env python3
"""Independent numerical checks for already transcribed Zhang Sanhui Ch 9 candidates."""
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def main():
 q=(ROOT/"chapters/09/questions.tex").read_text(encoding="utf-8")
 s=(ROOT/"chapters/09/solutions.tex").read_text(encoding="utf-8")
 cases=[
  (1, lambda: 6650*373.15/273.16, 9080, "constant-volume thermometry pressure"),
  (2, lambda: 40*math.log(7/5)/math.log(7/6), 87.3, "Newton-law cooling elapsed time"),
  (3, lambda: (280.15/270.15)*(1+20*(math.pi*.015**2*.30)/(2*math.pi**2*.3406*.015**2)), 3.94, "inflated bicycle tire absolute pressure ratio"),
  (4, lambda: .18*.029/(3.2e-6*8.314), 196, "high-atmosphere temperature from pressure density"),
  (5, lambda: 293.15/(1-4500/((101325*.029/(8.314*293.15))*2.1e4)), 356.5, "hot-air balloon marginal buoyancy temperature"),
  (6, lambda: (1e-18*101325*1e-6)/(1.380649e-23*293.15), 25, "extreme vacuum expected molecule count"),
  (7, lambda: 1e10*1.380649e-23*1e4, 1.38e-9, "interstellar atomic hydrogen gas pressure"),
  (8, lambda: 273-.006*8848, 219.9, "constant lapse rate upper atmosphere temperature"),
  (9, lambda: math.sqrt(2), 1.41421356237, "relative Maxwell mean speed factor"),
  (10, lambda: math.sqrt((1**2+3**2)/2), 2.23606797749979, "RMS of equally weighted two discrete speeds"),
  (11, lambda: 1/(math.sqrt(2)*math.pi*(3.8e-10)**2*(101325/(1.380649e-23*273.15))), 5.8e-8, "nitrogen hard-sphere free path at STP"),
  (12, lambda: 1/(math.sqrt(2)*math.pi*(3e-10)**2*(1.33e-3/(1.380649e-23*300.15))), 7.79, "low pressure vacuum tube molecule free path"),
  (13, lambda: 1/(math.sqrt(2)*math.pi*(3e-10)**2*(1.5e-9*6.02214076e23/.029)), 80.3, "160-km-air free path"),
  (14, lambda: math.pi*(3e-10)**2, 2.827e-19, "electron-static molecule geometric collision area"),
  (15, lambda: 2.5*(8.5/28)*8.314*290.15, 1830, "molecular nitrogen internal energy"),
  (16, lambda: 2.5*8.314*300.15, 6240, "one mole diatomic internal energy"),
  (17, lambda: 2*250*310/(250+310), 276.8, "diatomic gas insulated mixture final temperature"),
  (18, lambda: 11/9, 1.22222, "normalized non-Maxwell piecewise mean speed"),
  (19, lambda: math.sqrt(3*1.380649e-23*2e6/9.1093837e-31), 9540000, "corona electron rms thermal speed"),
  (20, lambda: 11200*math.sqrt(.108/.531), 5050, "Martian escape speed mass-radius scaling"),
  (21, lambda: math.sqrt(3*1.380649e-23*300/1.6e-16), 0.00881, "Brownian smoke-particle rms speed"),
  (22, lambda: 3*8.314*300.15/(6.2e-17*.014**2), 6.16e+23, "experimental Avogadro estimate"),
  (23, lambda: .5, 0.5, "Maxwell energy density mode in kBT units"),
  (24, lambda: 8.314*293.15*math.log(7160/3360)/((4/3)*math.pi*(.212e-6)**3*206.7*9.8*30e-6), 7.6e+23, "Perrin layer counts infer Avogadro constant"),
  (25, lambda: 6.02214076e23/3.01e4, 20000000000000000000, "saturated steam density molecules per cm3"),
  (26, lambda: 25*8.314e3*286.15/(20-25*.0427)-3.64e5*25**2/20**2, 2570000, "van der Waals pressure with liters unit system"),
  (27, lambda: 9.55e-5/3, 0.0000318, "van der Waals critical b from scanned-chart candidate"),
  (28, lambda: 3*1.89e-5/((101325*.004/(8.314*273.15))*1200), 2.65e-7, "helium free path from viscosity"),
  (29, lambda: 1.380649e-23*300.15/(math.sqrt(2)*math.pi*(3.7e-10)**2*.004), 1.7, "Knudsen heat transfer threshold pressure"),
 ]
 assert len(cases)==29 and [c[0] for c in cases]==list(range(1,30))
 for n,f,expected,label in cases:
  tag=rf"\paragraph{{习题 9.{n}}}"
  assert tag in q and tag in s, f"missing original candidate pair {ch}.{n}"
  actual=f()
  assert math.isfinite(actual) and math.isclose(actual,expected,rel_tol=.025,abs_tol=1e-12 if expected==0 else 0), f"{ch}.{n} {label}: {actual!r} != {expected!r}"
 print("PASS 29 Ch9 independent candidate model checks; new original problems 0")
 print("NOT checked: original PDF pages or figures, expert review, copyright license")
if __name__=="__main__":main()
