#!/usr/bin/env python3
"""31 independently formulated model/necessary-condition tests on ALREADY transcribed companion selected thought questions.
NOT full expert-reviewed solutions or recovered V1 textbook original question scans.
"""
import json
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CASES=[
    ("1.7", lambda: (-3)*2, lambda: -6),
    ("1.8", lambda: 20**2/9.8, lambda: 40.8163),
    ("1.11", lambda: -2*(-2), lambda: 4),
    ("2.6", lambda: 9.8-9.8, lambda: 0),
    ("2.7", lambda: -(+1), lambda: -1),
    ("2.11", lambda: 3*4/(2**3), lambda: 1.5),
    ("3.3", lambda: 2*9.8+5, lambda: 24.6),
    ("3.9", lambda: .5*.2**2*3, lambda: .06),
    ("3.10", lambda: 1*6-2*3, lambda: 0),
    ("4.5", lambda: 2*(1/2-1/1), lambda: -1),
    ("4.9", lambda: 3*0+0*4, lambda: 0),
    ("4.12", lambda: .5*1.2*10**2, lambda: 60),
    ("5.3", lambda: 2*3**2/12, lambda: 1.5),
    ("5.6", lambda: 5/2, lambda: 2.5),
    ("5.10", lambda: 2*9.8*.5/(.2*100), lambda: .49),
    ("6.7", lambda: 10/math.sqrt((20-3**2)**2+(2*3)**2), lambda: .798),
    ("6.8", lambda: math.sqrt((2+1/3)/2), lambda: 1.0801),
    ("7.6", lambda: math.sin(0)**2, lambda: 0),
    ("7.7", lambda: math.sqrt(100/.01)/(2*1), lambda: 50),
    ("7.14", lambda: (344+30)/((344+30)/440), lambda: 440),
    ("7.17", lambda: 2.998e8/(1.5+.1), lambda: 1.87375e8),
    ("8.3", lambda: (1/math.sqrt(1-.6**2))*(.6*100/2.998e8), lambda: 2.5017e-7),
    ("8.5", lambda: -(.6*2.998e8)*10/(2.998e8**2), lambda: -2.0013e-8),
    ("8.7", lambda: 10*math.sqrt(1-.6**2), lambda: 8),
    ("9.6", lambda: 1.5*1.380649e-23*2000, lambda: 4.14195e-20),
    ("9.8", lambda: math.exp(4*1.66053906660e-27*9.8*1e5/(1.380649e-23*200)), lambda: 10.6),
    ("10.4", lambda: 8.314462618*300*math.log(2), lambda: 1728.8),
    ("10.8", lambda: 1-300/600, lambda: .5),
    ("11.4", lambda: int(2**(-1.4)<.5), lambda: 1),
    ("11.6", lambda: 100*(1/300-1/350), lambda: .047619),
    ("11.8", lambda: -1e-23/(1.380649e-23*math.log(2)), lambda: -1.045),
]
def main():
 register=json.loads((ROOT/"supplement_selected_thought_register.json").read_text(encoding="utf-8"))
 ids=[entry["source_thought_number"] for entry in register["entries"]]
 assert register["companion_selected_thought_count"]==31 and register["companion_selected_solution_count"]==31
 assert len(ids)==31 and len(set(ids))==31 and sorted(ids)==sorted(id for id,_,_ in CASES)
 for id,calculate,ref in CASES:
  chapter=int(id.split(".")[0])
  tag=rf"\paragraph{{思考题 {id}}}"
  for kind in ("questions","solutions"):
   path=ROOT/f"supplement_selected_thought/{chapter:02d}/{kind}.tex"
   if tag not in path.read_text(encoding="utf-8"):
    raise AssertionError(f"Missing companion draft {id} {kind}")
  got,want=calculate(),ref()
  if not (math.isfinite(got) and math.isfinite(want) and math.isclose(got,want,rel_tol=.025,abs_tol=1e-12 if want==0 else 0)):
   raise AssertionError(f"Selected thought {id}: {got} != {want}")
 print("PASS 31 companion selected thought question necessary-condition/numeric samples; NOT source-original or expert-reviewed.")
if __name__=="__main__":main()
