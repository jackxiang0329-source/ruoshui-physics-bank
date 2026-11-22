#!/usr/bin/env python3
"""Chapter 4: supplementary independent necessary-condition models for  28 existing solutions.
Some use reviewer-declared sample parameters. NOT new original-PDF transcription or proof certification.
"""
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CHAPTER=4
CASES=[
    (1, lambda: ((1200-1000)*9.8+(1200+1000)*1.5)*.75, lambda: 3945),
    (2, lambda: 1-1/math.sqrt(2), lambda: .292893),
    (3, lambda: .5*132000*(942/3.6)**2, lambda: 4.52e9),
    (4, lambda: 50*1.5**2, lambda: 112.5),
    (5, lambda: math.sqrt(.8*9.8*1), lambda: 2.8),
    (6, lambda: .5*.01*100**2*.09/(.09+.01), lambda: 45),
    (7, lambda: 20-2*3, lambda: 14),
    (8, lambda: .5*200*.1**2, lambda: 1),
    (9, lambda: 9.8*math.sqrt(1/10), lambda: 3.099),
    (10, lambda: (72*9.8+math.sqrt((72*9.8)**2+2*60*72*9.8*20))/60, lambda: 36.4318),
    (11, lambda: (.02*100/(1+.02))*math.sqrt((1.02*1)/(2.02*50)), lambda: .198),
    (12, lambda: .3*9.8/math.sqrt(8.9*.5), lambda: 1.393),
    (13, lambda: math.sqrt(2*9.8*1*(2+1)/2), lambda: 5.422),
    (14, lambda: 3*4+4*(-3), lambda: 0),
    (15, lambda: (0-4)+(4-0), lambda: 0),
    (16, lambda: -60/6, lambda: -10),
    (17, lambda: -100/(4+6), lambda: -10),
    (18, lambda: .5*100*(1/10-1/20), lambda: 2.5),
    (19, lambda: math.sqrt(6.6743e-11*1e30*(1/(4e4)-1/(1e10))), lambda: 4.083e7),
    (20, lambda: 6.6743e-11*5.972e24*(4*math.pi/3*(1e4)**3*6000)/6.371e6, lambda: 1.57e24),
    (21, lambda: 2*6.6743e-11*1.989e30/(2.998e8)**2, lambda: 2953),
    (22, lambda: 2*1.989e30*(2e10/1e67)**(1/3), lambda: 5.01e11),
    (23, lambda: 4.27*(234/238), lambda: 4.198),
    (24, lambda: .5*(2*3/(2+3))*5**2, lambda: 15),
    (25, lambda: 2*math.sqrt(3/(10*4)), lambda: .5477),
    (26, lambda: 2/(8/5), lambda: 1.25),
    (27, lambda: 3600*math.pi*(.2)**2*math.sqrt(2*9.8*5), lambda: 4.48e3),
    (28, lambda: math.pi*(.008/2)**2*math.sqrt(2*20*101325/1000), lambda: .0032),
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
    print("PASS: 28 chapter-4 supplemental physics/numeric checkpoints")
    print("Full original figures, PDF and expert review still unresolved; new transcribed original questions 0.")
if __name__=="__main__":main()
