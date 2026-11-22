#!/usr/bin/env python3
"""Chapter 3: supplementary independent necessary-condition models for  24 existing solutions.
Some use reviewer-declared sample parameters. NOT new original-PDF transcription or proof certification.
"""
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CHAPTER=3
CASES=[
    (1, lambda: -10*.2/2, lambda: -1),
    (2, lambda: math.sqrt(2)*.05*20, lambda: 1.41421),
    (3, lambda: 150*(9.8+math.sqrt(2*9.8*5)/.3), lambda: 6420),
    (4, lambda: 2*.0079*735, lambda: 11.61),
    (5, lambda: 1.29*22.5*2.62*38**2, lambda: 1.10e5),
    (6, lambda: math.sqrt(2)*3e3*10, lambda: 4.24e4),
    (7, lambda: .5*2*9.8+.5*3**2, lambda: 14.3),
    (8, lambda: 3*.3*9.8*2, lambda: 17.64),
    (9, lambda: math.hypot(9.22,5.33)*1e-21, lambda: 1.065e-20),
    (10, lambda: 7600+910*(2/(2+1))-(7600-910*(1/(2+1))), lambda: 910),
    (11, lambda: 4*2*.8*9.8*25, lambda: 1568),
    (12, lambda: 105+253*math.log(6090/6010), lambda: 108.3455),
    (13, lambda: 1-math.exp(-1), lambda: .63212),
    (14, lambda: 5.50e4*math.log(2.72e6/(2.72e6-1.29e3*155))-9.8*155, lambda: 2680),
    (15, lambda: 78*490-75*210, lambda: 22470),
    (16, lambda: 2*.0958*math.cos(math.radians(52.5))/18, lambda: .00648),
    (17, lambda: 4/(3*math.pi), lambda: .42441),
    (18, lambda: (.5-math.pi/64)/(1-math.pi/16), lambda: .5611),
    (19, lambda: 9.8*(2-5/7), lambda: 12.6),
    (20, lambda: (8.75e10*5.46e4)/(9.08e2), lambda: 5.26e12),
    (21, lambda: 2*math.pi*7.35e22*(3.844e8)**2/(27.3*86400), lambda: 2.89e34),
    (22, lambda: (6371+205.5)/(6371+35835.7)*10, lambda: 1.558),
    (23, lambda: 4*.5/.2, lambda: 10),
    (24, lambda: (.5)/(2/3), lambda: .75),
]
def main():
    q=(ROOT/f"chapters/{CHAPTER:02d}/questions.tex").read_text(encoding="utf-8")
    s=(ROOT/f"chapters/{CHAPTER:02d}/solutions.tex").read_text(encoding="utf-8")
    assert len(CASES)==24
    assert [num for num,_,_ in CASES]==list(range(1,25))
    for num,calculate,expected in CASES:
        marker=rf"\paragraph{{习题 {CHAPTER}.{num}}}"
        if marker not in q or marker not in s:
            raise AssertionError(f"Missing candidate {CHAPTER}.{num}")
        got,want=calculate(),expected()
        if not (math.isfinite(got) and math.isfinite(want) and
                math.isclose(got,want,rel_tol=.025,abs_tol=1e-12 if want==0 else 0)):
            raise AssertionError(f"{CHAPTER}.{num}: {got:.10g} vs {want:.10g}")
    print("PASS: 24 chapter-3 supplemental physics/numeric checkpoints")
    print("Full original figures, PDF and expert review still unresolved; new transcribed original questions 0.")
if __name__=="__main__":main()
