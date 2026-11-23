#!/usr/bin/env python3
"""Independent structural and numerical spot checks for the Zhao/Wang 5e trial batch.

Passing does NOT establish professional independent review or rights clearance.
No OCR, external network, or third-party packages are used.
"""
from pathlib import Path
import math
import re

ROOT = Path(__file__).resolve().parent
CHAPTERS = (
    ("chapters/textbook-ch01-exercises.tex", "sourceproblem",
     [f"1.3.{n}" for n in range(4, 18)]),
    ("chapters/guide-ch01-examples.tex", "sourceexample",
     [f"1.{n}" for n in range(1, 6)]),
    ("chapters/guide-ch02-examples.tex", "sourceexample", ["2.1"]),
)


def near(actual, expected, tol=1e-8):
    assert math.isclose(actual, expected, rel_tol=tol, abs_tol=tol), (
        f"expected {expected}, got {actual}"
    )


def structural_check():
    total = 0
    for relative, macro, expected in CHAPTERS:
        source = (ROOT / relative).read_text(encoding="utf-8")
        ids = re.findall(r"\\" + macro + r"\{([^}]*)\}", source)
        assert ids == expected, (relative, ids, expected)
        blocks = re.split(r"\\" + macro + r"\{[^}]*\}\{[^}]*\}\{[^}]*\}", source)[1:]
        assert len(blocks) == len(expected)
        for number, block in zip(ids, blocks):
            for label in (r"\problemtext", r"\workings", r"\crosscheck"):
                assert label in block, (number, label)
        total += len(ids)
    assert total == 20, total
    return total


def numerical_check():
    # 教材1.3.4—1.3.8
    near(math.hypot(2, 12), 2 * math.sqrt(37))
    near(math.hypot(2, 8), 2 * math.sqrt(17))
    v0, g = 23.6, 9.8
    h1 = 2.37 - 0.5 * g * (12 / v0)**2
    h2 = 2.37 - 12 * math.tan(math.radians(5)) - 0.5 * g * (
        12 / (v0 * math.cos(math.radians(5))))**2
    near(h1 - 0.90, 0.20312266590060346)
    near(h2, 0.043561687173862884)
    assert h1 > 0.90 and 0 < h2 < 0.90
    x = lambda t: 4.5*t*t - 2*t**3
    near((x(2) - x(1)), -0.5)
    near((x(1.5) - x(1)) + (x(1.5) - x(2)), 2.25)
    tm = (math.sqrt(33) - 1) / 4
    near(4*tm + tm*tm, 2*tm*tm + 2*tm**3)
    near((4*(2/3) + 6*(2/3)**2) - (4 + 2*(2/3)), 0)

    # 教材1.3.9—1.3.17
    near(math.hypot(16, 32), 16*math.sqrt(5))
    B, A, t = 2.0, 6.0, 0.7
    v = A/B*(1-math.exp(-B*t))
    near(A-B*v, A*math.exp(-B*t))
    near(100 + 4*2 + 4*2**3, 140)
    near(4*10+1.5*10**2, 190)
    near(5+2*10**2+0.5*10**3, 705)
    near(math.cos(0), 1)
    near(3*(2/9), 2/3)
    R, b, initv = 2.0, 4.0, 10.0
    time = (initv - math.sqrt(b*R))/b
    near((initv - b*time)**2 / R, b)
    near(math.hypot(.08,.064), 0.10244998779892558)
    near(math.hypot(30,40),50)

    # 学习指导例1.1—1.5与2.1
    near(25/(6/5), 125/6)
    near(2**3-8, 0)
    beta, initial_v, t = 4.0, 5.0, 0.3
    xx = initial_v / math.sqrt(beta) * math.sin(math.sqrt(beta)*t)
    vv = initial_v * math.cos(math.sqrt(beta)*t)
    near(vv**2 + beta*xx**2, initial_v**2)
    near((7 - 2/3) - 7, -2/3)
    near(abs(-2/3)/(2*math.pi), 1/(3*math.pi))
    angles = [math.radians(a) for a in (12,25,35)]
    ratio = (math.tan(angles[0])+math.tan(angles[1])) / (
        math.tan(angles[0])+math.tan(angles[2]))
    near(ratio, (1 + math.tan(angles[1])/math.tan(angles[0])) / (
        1 + math.tan(angles[2])/math.tan(angles[0])))
    m1,m2,m3,gg=2.0,3.0,4.0,9.8
    den=4*m1*m2+m3*(m1+m2)
    a=m3*(m1+m2)*gg/den
    aA=2*m2*m3*gg/den
    aB=2*m1*m3*gg/den
    near(aA+aB,2*a)
    near(m1*aA,m2*aB)


if __name__ == "__main__":
    n = structural_check()
    numerical_check()
    print(f"Structure: {n} referenced worked items; all checked blocks present.")
    print("Selected numeric invariants: passed.")
    print("Not a replacement for full independent physics or copyright review.")
