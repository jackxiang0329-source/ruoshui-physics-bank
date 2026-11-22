#!/usr/bin/env python3
"""Chapter 2: supplementary independent necessary-condition models for  28 existing solutions.
Some use reviewer-declared sample parameters. NOT new original-PDF transcription or proof certification.
"""
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CHAPTER=2
CASES=[
    (1, lambda: .3*2*9.8/(math.cos(.2)-.3*math.sin(.2)), lambda: 6.389),
    (2, lambda: .5*(9.8*math.sin(math.pi/6)+2*math.cos(math.pi/6)), lambda: 3.316),
    (3, lambda: (5000+1500)*(9.8+.6), lambda: 67600),
    (4, lambda: 75*9.8/2, lambda: 367.5),
    (5, lambda: 4*9.8/(4/.2+1/.1+1/.05), lambda: .784),
    (6, lambda: 25**2/(2*(25**2/(2*35)*math.cos(math.atan(.1))-9.8*math.sin(math.atan(.1)))), lambda: 39.51),
    (7, lambda: 2*.25*(1.50+2.45)*9.8, lambda: 19.36),
    (8, lambda: (5+2+1)*(1*9.8/2), lambda: 39.2),
    (9, lambda: math.sqrt(6.67e-11*7.35e22/(1.74e6+2e5)), lambda: 1.59e3),
    (10, lambda: (100*200)/(100+200), lambda: 66.6667),
    (11, lambda: 1200*(9.8*math.cos(math.radians(6))+(25**2/400)*math.sin(math.radians(6))), lambda: 11892),
    (12, lambda: 4*math.pi**2*(1.07e9)**3/(6.6743e-11*(7.16*86400)**2), lambda: 1.89e27),
    (13, lambda: 4*math.pi**2*(1.36e8)**3/(6.67e-11*(14.2*3600)**2), lambda: 5.70e26),
    (14, lambda: math.sqrt(3*math.pi/(6.6743e-11*3000)), lambda: 6860),
    (15, lambda: 2*math.pi/3*6.6743e-11*(1.3e3)**2*(7e7)**2, lambda: 1.16e12),
    (16, lambda: math.sqrt(3**.5), lambda: 3**.25),
    (17, lambda: 1.496e11*(5.972e24/(3*1.989e30))**(1/3), lambda: 1.50e9),
    (18, lambda: 10/(1+.2*10/2*3), lambda: 2.5),
    (19, lambda: .5*.012*(2*math.pi*50000/60)**2*(.02+.10), lambda: 1.97e4),
    (20, lambda: (2*math.pi*400/60)**2*5.97/(2*9.8), lambda: 534),
    (21, lambda: int(abs(9.8*math.sin(math.radians(20)))<=1*(9.8*math.cos(math.radians(20)))), lambda: 1),
    (22, lambda: (2**2*(2*.5+3*1.5)), lambda: 22),
    (23, lambda: math.sqrt(2*(7-.5*9.8)*2), lambda: 2.90),
    (24, lambda: math.sqrt(9.8/1800), lambda: .0738),
    (25, lambda: 9.8/8, lambda: 1.225),
    (26, lambda: .5*.016*.062*math.pi*25**2*40**2, lambda: 1558),
    (27, lambda: 9.8*2/1.5*(1-math.exp(-1.5*3/2)), lambda: (9.8*2/1.5)*.8946),
    (28, lambda: (.5-.02*9.8)/(4*math.pi*.05), lambda: .4838),
]
def main():
    q=(ROOT/f"chapters/{CHAPTER:02d}/questions.tex").read_text(encoding="utf-8")
    s=(ROOT/f"chapters/{CHAPTER:02d}/solutions.tex").read_text(encoding="utf-8")
    assert len(CASES)==28
    assert [num for num,_,_ in CASES]==list(range(1,29))
    for num,calculate,expected in CASES:
        marker=rf"\paragraph{{习题 {CHAPTER}.{num}}}"
        if marker not in q or marker not in s:
            raise AssertionError(f"Missing candidate {CHAPTER}.{num}")
        got,want=calculate(),expected()
        if not (math.isfinite(got) and math.isfinite(want) and
                math.isclose(got,want,rel_tol=.025,abs_tol=1e-12 if want==0 else 0)):
            raise AssertionError(f"{CHAPTER}.{num}: {got:.10g} vs {want:.10g}")
    print("PASS: 28 chapter-2 supplemental physics/numeric checkpoints")
    print("Full original figures, PDF and expert review still unresolved; new transcribed original questions 0.")
if __name__=="__main__":main()
