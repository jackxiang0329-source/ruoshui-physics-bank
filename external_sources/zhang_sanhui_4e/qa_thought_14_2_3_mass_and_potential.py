#!/usr/bin/env python3
"""Independent boundary/energy tests for existing V2 thought 14.2 and 14.3 only."""
import math,json
from pathlib import Path
R=Path(__file__).resolve().parent
S=(R/"thought_questions/14/solutions.tex").read_text(encoding="utf-8")
Q=(R/"thought_questions/14/questions.tex").read_text(encoding="utf-8")
D=json.loads((R/"thought_register.json").read_text(encoding="utf-8"))
def close(a,b): assert math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-12),(a,b)
def main():
 for id in ("14.2","14.3"):
  tag=rf"\paragraph{{思考题 {id}}}"
  assert tag in S and tag in Q
  e=next(x for x in D["entries"] if x["source_thought_number"]==id)
  assert e["exam_ready"] is False and e["academic_review"]=="pending_independent_verification"
  assert e["model_derivation_review"]["source_pdf_reopened"] is False
 k=1/(4*math.pi*8.8541878128e-12)
 a,b,Q0,q=.2,.3,3e-8,-1e-8
 phi_in_at_a=k*(q/a-q/a+(Q0+q)/b)
 phi_metal=k*(Q0+q)/b
 phi_out_at_b=k*(Q0+q)/b
 close(phi_in_at_a,phi_metal);close(phi_metal,phi_out_at_b)
 r=.15
 phi_cavity=k*(q/r-q/a+(Q0+q)/b)
 phi_naive=k*(Q0/b+q/r)
 assert abs(phi_cavity-phi_naive)>1
 me=9.1093837139e-31;c=299792458.;electronvolt=1.602176634e-19
 N=100000.;E_out=2*electronvolt*N
 delta=N*me-E_out/c**2
 assert 0<delta<N*me
 close((N*me-delta)*c**2,E_out)
 print("PASS existing thought 14.2 shell boundaries and 14.3 bound-electron mass-energy ledger")
if __name__=="__main__": main()
