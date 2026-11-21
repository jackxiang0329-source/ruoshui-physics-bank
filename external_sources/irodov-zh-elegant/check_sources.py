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
]
EXPECTED_RANGES = [
    range(1, 21), range(21, 31), range(31, 41),
    range(41, 51), range(51, 59), range(59, 71),
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

if all_ids != list(range(1, 71)):
    errors.append("combined problem IDs are not exactly 1..70 in order")
if main.count(r"\section{运动学") != 1:
    errors.append("kinematics section count is not one")
if main.count(r"\section{动力学基本方程") != 1:
    errors.append("dynamics section count is not one")

if errors:
    for e in errors:
        print("FAIL:", e, file=sys.stderr)
    sys.exit(1)
print("PASS: 70 consecutive translated problem sources, solutions, checks, and included chapters")
