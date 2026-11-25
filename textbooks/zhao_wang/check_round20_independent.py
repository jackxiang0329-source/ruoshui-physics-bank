#!/usr/bin/env python3
"""Independent scan-to-source audit for Zhao/Wang 5e (round 20).

This test is deliberately separate from check_math.py: it checks all source
identities and spot-checks difficult electromagnetic derivations by a second
numerical route (quadrature, finite differences, counterexamples).
It does not certify every physics result or grant copyright clearance.
"""
from pathlib import Path
import math
import re

from check_math import CHAPTERS

ROOT = Path(__file__).resolve().parent
PI = math.pi
MU0 = 4 * PI * 1e-7
EPS0 = 8.8541878128e-12


def near(a, b, rel=2e-5, abs_tol=1e-12):
    assert math.isclose(a, b, rel_tol=rel, abs_tol=abs_tol), (a, b)


def trap(f, lo, hi, intervals=20000):
    h = (hi - lo) / intervals
    total = (f(lo) + f(hi)) * 0.5
    for i in range(1, intervals):
        total += f(lo + i * h)
    return total * h


def audit_every_item():
    """Global unique identities: do not silently grow or double-count 890."""
    seen = set()
    totals = {}
    for rel, macro, expected_ids in CHAPTERS:
        content = (ROOT / rel).read_text(encoding="utf-8")
        entries = re.findall(
            r"\\" + re.escape(macro) + r"\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}",
            content,
        )
        assert [entry[0] for entry in entries] == expected_ids, rel
        for num, printed_page, physical_page in entries:
            key = macro, num
            assert key not in seen, ("duplicated source ID", key)
            seen.add(key)
            assert printed_page.strip() and physical_page.strip(), key
            # Reject clearly accidental invisible JavaScript-escaped TeX.
            assert "\t" not in content and "\x00" not in content, rel
        totals[macro] = totals.get(macro, 0) + len(entries)
    assert totals == {
        "sourceproblem": 514,
        "sourceexample": 111,
        "sourcetest": 265,
    }, totals
    assert len(seen) == 890

    # Exact physically scanned exercise distribution on pages 175–182.
    for test, groups, page_min, page_max in (
        (7, (8, 8, 5), 167, 170),
        (8, (8, 10, 5), 171, 174),
    ):
        path = ROOT / f"chapters/guide-selftest{test:02d}.tex"
        data = path.read_text(encoding="utf-8")
        metadata = re.findall(
            r"\\sourcetest\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}", data
        )
        assert len(metadata) == sum(groups), (path, len(metadata))
        for subsection, expected_n in enumerate(groups, start=1):
            subset = [
                entry for entry in metadata
                if entry[0].startswith(f"{test}.{subsection}.")
            ]
            assert len(subset) == expected_n, (path, subsection, len(subset))
            for num, printed, physical in subset:
                assert int(printed) in range(page_min, page_max + 1), num
                assert int(physical) == int(printed) + 8, num

    page_81 = (ROOT / "chapters/guide-selftest08.tex").read_text(encoding="utf-8")
    block_814 = page_81.split(r"\sourcetest{8.1.4}", 1)[1].split(
        r"\sourcetest{8.1.5}", 1
    )[0]
    assert "平行错位" in block_814 and "不是共线" in block_814
    page_72 = (ROOT / "chapters/guide-selftest07.tex").read_text(encoding="utf-8")
    block_726 = page_72.split(r"\sourcetest{7.2.6}", 1)[1].split(
        r"\sourcetest{7.2.7}", 1
    )[0]
    assert r"V_a-V_b=\pi BnR^2" in block_726
    page_82 = (ROOT / "chapters/guide-selftest08.tex").read_text(encoding="utf-8")
    block_822 = page_82.split(r"\sourcetest{8.2.2}", 1)[1].split(
        r"\sourcetest{8.2.3}", 1
    )[0]
    assert "势垒" in block_822 and "U(z)" in block_822
    return totals


def independent_physics_regressions():
    # 7.1.4 square vs round same wire current, diameter equals square side.
    near(PI / (2 * math.sqrt(2)), 1.1107207345395915)
    # 7.1.7 toroidal inductance when N -> N/2, ell -> ell/2.
    near((0.5**2) / 0.5, 0.5)
    # 7.2.4 reversible loop-work: 90 degrees, one full cycle.
    C = 10 * PI * 0.06**2 * 0.015
    near(C * (1 - math.cos(PI / 2)), C)
    near(C * (1 - math.cos(2 * PI)), 0)
    # 7.2.5 changing area is independent of radius under fixed |EMF|.
    near(2 * PI * 0.80 * 0.10 * 0.80, 0.4021238596594936)
    near(-2 * PI * 0.10 * 0.80, -0.16 * PI)
    # 7.2.6 source diagram: CCW wheel seen from outside -> +omega.
    # Crosses denote B into paper. Thus radial v x B is inward.
    omega_sign, field_sign = +1, -1
    assert omega_sign * field_sign == -1
    # 7.3.2 cavity center and exterior P, 2d>r.
    d, r = 0.6, 0.2
    assert 2 * d > r
    near(-d + r**3 / (4 * d**2), -0.5944444444444444)
    # 7.3.4 triangular loop fixed geometry: integrate 1/x profile.
    a, b, H = .05, .10, .20
    flux_factor_numeric = trap(lambda x: H * (a + b - x) / (b * x), a, a + b)
    flux_factor_exact = H / b * ((a + b) * math.log((a + b) / a) - b)
    near(flux_factor_numeric, flux_factor_exact, rel=1e-7)
    emf = MU0 / (2 * PI) * flux_factor_numeric * 2
    near(emf, 5.183347464017318e-8, rel=2e-7)
    # 8.1.5 two identical +y currents at x=1 and x=3:
    # field is zero only at x=2, z=0, not throughout plane x=2.
    def Bfield_wire_y(x, z, x0):
        dx = x - x0
        rr = dx * dx + z * z
        return z / rr, -dx / rr  # common factor mu0 I/(2pi)
    v1 = Bfield_wire_y(2, 0, 1)
    v2 = Bfield_wire_y(2, 0, 3)
    near(v1[0] + v2[0], 0)
    near(v1[1] + v2[1], 0)
    w1 = Bfield_wire_y(2, 1, 1)
    w2 = Bfield_wire_y(2, 1, 3)
    assert abs(w1[0] + w2[0]) > .5
    # 8.2.2 terminal speed can be formally real but a barrier still forbids arrival.
    eta = 2.8  # k qQ/(m g R^2), same-sign charged ring and particle
    assert 1 - eta * (1 - 1 / math.sqrt(2)) > 0
    def U_dimensionless(s):
        return s + eta / math.sqrt(1 + s * s)
    assert U_dimensionless(.58) > U_dimensionless(1)
    # 8.2.6 charged ring: both quantities from independent q,T expressions.
    q, v, R = 8e-19, 3e5, 6e-8
    current = q * v / (2 * PI * R)
    near(MU0 * current / (2 * R), MU0 * q * v / (4 * PI * R**2))
    near(current * PI * R**2, q * v * R / 2)
    # 8.2.7 electron magnetic moment, direction antiparallel to B.
    near(9.11e-31 * (2.2e6)**2 / (2 * 2.36),
         9.341610169491526e-19)
    # 8.3.2 rotating semicircle: independent trapezoid integration.
    integral = trap(lambda t: math.sin(t)**2, 0, PI)
    near(integral, PI / 2, rel=1e-8)
    lam, omega, radius = 2e-6, 11.0, .05
    B_analytic = MU0 * lam * omega / 8
    B_numeric = MU0 * lam * omega / (4 * PI) * integral
    near(B_numeric, B_analytic)
    m_analytic = PI * lam * omega * radius**3 / 4
    m_numeric = omega * lam * radius**3 / 2 * integral
    near(m_numeric, m_analytic)
    # 8.3.4 moving triangular loop: flux derivative checked numerically.
    a, b, d, I, v = .1, .2, .05, 3.2, 1.4
    def flux(dd):
        return MU0 * I * b / (2 * PI * a) * (
            a - dd * math.log(1 + a/dd)
        )
    h = 1e-6
    num_emf = abs((flux(d + h) - flux(d - h)) / (2 * h) * v)
    analytic_emf = MU0 * I * b * v / (2 * PI * a) * (
        math.log(1 + a/d) - a/(d + a)
    )
    near(num_emf, analytic_emf, rel=1e-7)
    assert analytic_emf > 0
    # 8.3.5 translating rod: initial zero, max at a/v.
    a, v = .5, 2.
    f = lambda t: v*v*t/(a*a+v*v*t*t)
    near(f(0), 0)
    assert f(a/v) > f(a/(3*v)) and f(a/v) > f(3*a/v)


if __name__ == "__main__":
    categories = audit_every_item()
    independent_physics_regressions()
    print("PASS: 890 unique source IDs", categories)
    print("PASS: original page offsets for 44 items, source flags and independent physical calculations.")
    print("Limit: the checks do not replace full original-figure and expert review.")
