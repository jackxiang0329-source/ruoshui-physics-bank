#!/usr/bin/env python3
"""Structural gates for the Irodov Chinese ElegantBook project.

This is a technical check only: it does not constitute an independent physics peer review.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
CHAPTERS = [
    "01-mechanics-kinematics-001-020.tex",
    "01-mechanics-kinematics-021-030.tex",
    "01-mechanics-kinematics-031-040.tex",
    "01-mechanics-kinematics-041-050.tex",
    "01-mechanics-kinematics-051-058.tex",
    "02-mechanics-dynamics-059-070.tex",
    "02-mechanics-dynamics-071-080.tex",
    "02-mechanics-dynamics-081-090.tex",
    "02-mechanics-dynamics-091-100.tex",
    "02-mechanics-dynamics-101-110.tex",
    "02-mechanics-dynamics-111-117.tex",
    "03-mechanics-conservation-118-120.tex",
    "03-mechanics-conservation-121-130.tex",
    "03-mechanics-conservation-131-140.tex",
    "03-mechanics-conservation-141-150.tex",
    "03-mechanics-conservation-151-160.tex",
    "03-mechanics-conservation-161-170.tex",
    "03-mechanics-conservation-171-180.tex",
    "03-mechanics-conservation-181-190.tex",
    "03-mechanics-conservation-191-199.tex",
    "04-gravitation-200-210.tex",
    "04-gravitation-211-220.tex",
    "04-gravitation-221-233.tex",
    "05-rigid-body-234-240.tex",
    "05-rigid-body-241-250.tex",
    "05-rigid-body-251-260.tex",
    "05-rigid-body-261-270.tex",
    "05-rigid-body-271-280.tex",
    "05-rigid-body-281-289.tex",
    "06-elasticity-290-290.tex",
    "06-elasticity-291-300.tex",
]
EXPECTED_RANGES = [
    range(1, 21), range(21, 31), range(31, 41),
    range(41, 51), range(51, 59), range(59, 71),
    range(71, 81), range(81, 91), range(91, 101),
    range(101, 111), range(111, 118), range(118, 121),
    range(121, 131), range(131, 141), range(141, 151),
    range(151, 161), range(161, 171),
    range(171, 181), range(181, 191), range(191, 200),
    range(200, 211), range(211, 221), range(221, 234),
    range(234, 241),
    range(241, 251), range(251, 261), range(261, 271),
    range(271, 281), range(281, 290), range(290, 291),
    range(291, 301),
]

errors = []
main = (ROOT / "main.tex").read_text(encoding="utf-8")
all_ids = []

for name, expected in zip(CHAPTERS, EXPECTED_RANGES):
    path = ROOT / "chapters" / name
    if not path.exists():
        errors.append(f"missing: {name}")
        continue
    s = path.read_text(encoding="utf-8")
    ids = [int(x) for x in re.findall(r"\\exproblem\{(\d+)\}\{", s)]
    solutions = len(re.findall(r"\\exsolution\b", s))
    checks = len(re.findall(r"\\excheck\b", s))
    want = list(expected)
    all_ids.extend(ids)
    if ids != want:
        errors.append(f"{name}: ids {ids} != {want}")
    if solutions != len(want):
        errors.append(f"{name}: {solutions} solutions, expected {len(want)}")
    if checks != len(want):
        errors.append(f"{name}: {checks} checks, expected {len(want)}")
    entry = r"\input{chapters/" + path.stem + "}"
    if entry not in main:
        errors.append(f"main.tex does not include: {name}")

if all_ids != list(range(1, 301)):
    errors.append("combined problem IDs are not exactly 1..300 in order")
if main.count(r"\section{运动学") != 1:
    errors.append("kinematics section count is not one")
if main.count(r"\section{动力学基本方程") != 1:
    errors.append("dynamics section count is not one")
if main.count(r"\section{能量、动量与角动量守恒") != 1:
    errors.append("conservation section count is not one")
if main.count(r"\section{万有引力") != 1:
    errors.append("gravitation section count is not one")
if main.count(r"\section{刚体动力学") != 1:
    errors.append("rigid body section count is not one")
if main.count(r"\section{固体弹性形变") != 1:
    errors.append("elasticity section count is not one")

if errors:
    for e in errors:
        print("FAIL:", e, file=sys.stderr)
    sys.exit(1)
print("PASS: 300 consecutive translated problem sources, solutions, checks, and included chapters")
