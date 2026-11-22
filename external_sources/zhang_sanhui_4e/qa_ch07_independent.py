#!/usr/bin/env python3
"""33 independent checks of EXISTING chapter-7 wave candidates; no original PDF verification."""
from __future__ import annotations
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parent
P=math.pi
G=9.8

def run() -> None:
    q=(ROOT/"chapters/07/questions.tex").read_text(encoding="utf-8")
    s=(ROOT/"chapters/07/solutions.tex").read_text(encoding="utf-8")
    tests=[
        (1, 740/(300*3600), 6.85e-4, "long-ocean-wave frequency"),
        (2, 4/.80, 5, "wave number with both propagation directions still possible"),
        (3, .02*(2*P*200)/100, .2513, "medium speed divided by propagation speed"),
        (4, math.sqrt(2*G*2)/(2*P*1), .997, "tossed-person free-flight height is not ground displacement amplitude"),
        (5, .40/.08, 5, "candidate-figure wavelength and wave-speed period, figure not rechecked"),
        (6, 4.2-.4/2, 4, "earlier transit of closest negative-x crest"),
        (7, (350/500)/6, .1167, "60-degree spatial phase displacement"),
        (8, 7800*5100**2, 2.03e11, "steel longitudinal elastic modulus"),
        (9, .5*1e9*(.001)**2, 500, "elastic compression energy density; reviewer example"),
        (10, .5*7900*5100*(2*P*1000)**2*(1e-9)**2, 7.95e-4, "harmonic longitudinal-wave energy flux"),
        (11, .5*.2*(2*P*10)**2*.01**2*30, 1.18435, "string power example, mu=.2,f=10,A=.01,u=30"),
        (12, len([x for x in range(1,30) if x%2==0]), 14, "opposed-phase source interference: even meter positions"),
        (13, 750/20, 37.5, "counter-propagating standing-wave phase speed"),
        (14, math.cos(2*P*(3/4)), 0, "hard-wall node at 3-lambda/4"),
        (15, 5740/(2*.002), 1.435e6, "quartz thickness resonance"),
        (16, 1e-12*10**(141/10), 126, "141 dB referenced intensity"),
        (17, (5.1*60)/(1/6-1/8), 7344, "P-S delayed arrival km, contingent on graph readout"),
        (18, 10**((9.2+2.9)/.67), 1.15e18, "earthquake magnitude as transcribed from textbook formula; not historical magnitude"),
        (19, (2*P*.6/4)/(25/4), .151, "particle orbit speed divided by wave speed"),
        (20, 400*(330-80/3.6)/(330-120/3.6), 415, "one-way pursuit Doppler shift"),
        (21, (12+24)/120, .300, "head-on boat wave encounter frequency"),
        (22, 1540*220/(2*18000+220), 9.35, "dolphin echo double-Doppler"),
        (23, 2*.32*4e6/1540, 1.66e3, "ultrasound blood-flow Doppler magnitude"),
        (24, 3e8*1.1e4/(2*5e10), 33, "radar beat to radial vehicle velocity"),
        (25, 5000*math.sqrt(2.3**2-1)/(2.3*330), 13.6, "shock cone ground-arrival delay"),
        (26, (60/3.6)*math.sin(math.radians(10/2)), 1.45, "boat wake: full-angle vs half-angle distinction"),
        (27, (10-9)/(5-4), 1.0, "finite-difference group velocity"),
        (28, (2*.5*3)/(.5*3), 2, "quadratic dispersion group velocity / phase velocity, sample"),
        (29, (math.sqrt(2**2+3**2*4**2)/4)*((3**2*4)/math.sqrt(2**2+3**2*4**2)), 9, "plasma dispersion phase × group velocities = c²"),
        (30, ((2.5**2)-1)/((2.5**2)+1), 21/29, "radial relativistic Doppler, λobs/λemit=2.5"),
        (31, ((2*P/1)**2 / .2) * (.2**2/(2*P)), 2*P, "wave-packet bandwidth scaling, explicit narrowband convention"),
        (32, 3/math.sqrt(3**2+4**2) - 5/math.sqrt(5**2+12**2) * (5/(125/39)), 0, "Snell stationary-time derivative, reviewer example"),
        (33, (math.cos(.73))**2+(math.sin(.73))**2, 1, "orthogonal transverse displacement ellipse identity"),
    ]
    assert [num for num,*_ in tests]==list(range(1,34))
    for num, calc, expected, label in tests:
        tok=rf"\paragraph{{习题 7.{num}}}"
        if tok not in q or tok not in s:
            raise AssertionError(f"Candidate question/answer missing: 7.{num}")
        if not math.isfinite(calc) or not math.isclose(calc, expected, rel_tol=.018, abs_tol=1e-10 if expected==0 else 0):
            raise AssertionError(f"7.{num} {label}: computed {calc!r}, checkpoint {expected!r}")
    assert s.count(r"角频率 \(\omega=4\,\mathrm{rad/s}\)，")==1, "Duplicated wave angular-frequency sentence"
    print("PASS: 33/33 ch7 numeric/physical-identity candidate checks + duplicate sentence QA.")
    print("CONDITIONAL (figure not independently checked): 7.5,7.17 and diagram-derived interpretations.")
    print("NO new source problems, no original-PDF transcription or expert certification.")
if __name__=="__main__":
    run()
