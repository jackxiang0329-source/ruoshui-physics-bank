#!/usr/bin/env python3
"""Chapter 1: supplementary independent necessary-condition models for  26 existing solutions.
Some use reviewer-declared sample parameters. NOT new original-PDF transcription or proof certification.
"""
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CHAPTER=1
CASES=[
    (1, lambda: math.sqrt(2*1.8*200000), lambda: 848.528),
    (2, lambda: 1600/3.6/1.8, lambda: 246.9136),
    (3, lambda: ((90/3.6+65/3.6)-math.sqrt((90/3.6+65/3.6)**2-4*7.5*(80-(90/3.6+65/3.6)*.7)))/(2*7.5), lambda: 1.60907),
    (4, lambda: 2*(200/3.6)/9.8 + (1200-(200/3.6)**2/9.8-50)/(200/3.6)+50/(18/3.6), lambda: 36.37),
    (5, lambda: 280/60*(2*26/9.8), lambda: 24.76),
    (6, lambda: (15-math.sqrt(15**2-2*9.8*11))/9.8, lambda: 1.21776),
    (7, lambda: 4*1**2-8, lambda: -4),
    (8, lambda: 17.5/math.sqrt(2*3.5/9.8), lambda: 20.71),
    (9, lambda: 2*(110/3.6)**2*math.tan(math.pi/4)/(9.8*math.cos(math.pi/4)), lambda: 269.42),
    (10, lambda: 25**2/(2*9.8)-9.8*50**2/(2*25**2), lambda: 12.2878),
    (11, lambda: (150/3.6)**2/(2*265), lambda: 3.276),
    (12, lambda: math.sqrt(9.8*(100**2+40**2)/(4*40)), lambda: 26.655),
    (13, lambda: (2*math.pi*1000)**2*.1, lambda: 3.94784e6),
    (14, lambda: 2*math.pi*6.37e6*math.cos(math.radians(39.9))/(24*3600), lambda: 355.3),
    (15, lambda: (2.2e6)**2/(.53e-10), lambda: 9.13e22),
    (16, lambda: 2*math.pi*(2.998e8)**2/(240*9.8), lambda: 2.4e14),
    (17, lambda: math.hypot(.25,.20), lambda: .320156),
    (18, lambda: math.pi*650000*(.056**2-.022**2)/1.3, lambda: 4166),
    (19, lambda: -1.2+.9, lambda: -.3),
    (20, lambda: math.sqrt(344**2-30**2), lambda: 342.69),
    (21, lambda: math.sqrt(3/(9.8-1.2)), lambda: .5906),
    (22, lambda: math.sqrt(100-5**2), lambda: 8.66025),
    (23, lambda: math.hypot(400*math.sqrt(3),600), lambda: 916.515),
    (24, lambda: 4*math.pi*6.37e6/(24*3600), lambda: 926.48),
    (25, lambda: (1-.99975)*2.998e8, lambda: 74950),
    (26, lambda: math.hypot(150-5750*math.cos(math.radians(19.5)),750-5750*math.sin(math.radians(19.5))), lambda: math.sqrt((150-5750*math.cos(math.radians(19.5)))**2+(750-5750*math.sin(math.radians(19.5)))**2)),
]
def main():
    q=(ROOT/f"chapters/{CHAPTER:02d}/questions.tex").read_text(encoding="utf-8")
    s=(ROOT/f"chapters/{CHAPTER:02d}/solutions.tex").read_text(encoding="utf-8")
    assert len(CASES)==26
    assert [num for num,_,_ in CASES]==list(range(1,27))
    for num,calculate,expected in CASES:
        marker=rf"\paragraph{{习题 {CHAPTER}.{num}}}"
        if marker not in q or marker not in s:
            raise AssertionError(f"Missing candidate {CHAPTER}.{num}")
        got,want=calculate(),expected()
        if not (math.isfinite(got) and math.isfinite(want) and
                math.isclose(got,want,rel_tol=.025,abs_tol=1e-12 if want==0 else 0)):
            raise AssertionError(f"{CHAPTER}.{num}: {got:.10g} vs {want:.10g}")
    print("PASS: 26 chapter-1 supplemental physics/numeric checkpoints")
    print("Full original figures, PDF and expert review still unresolved; new transcribed original questions 0.")
if __name__=="__main__":main()
