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
    "06-elasticity-301-310.tex",
    "06-elasticity-311-314.tex",
    "07-hydrodynamics-315-324.tex",
    "07-hydrodynamics-325-334.tex",
    "07-hydrodynamics-335-339.tex",
    "08-relativity-340-350.tex",
    "08-relativity-351-360.tex",
    "08-relativity-361-370.tex",
    "08-relativity-371-380.tex",
    "08-relativity-381-388.tex",
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
    range(291, 301), range(301, 311), range(311, 315),
    range(315, 325), range(325, 335), range(335, 340),
    range(340, 351), range(351, 361),
    range(361, 371), range(371, 381), range(381, 389),
]


# The book restarts numbering in Part II. Keep separate independent gates.
THERMO_CHAPTERS = [
    "09-thermo-state-001-011.tex",
    "09-thermo-state-012-020.tex",
    "09-thermo-state-021-025.tex",
]
THERMO_EXPECTED = [range(1, 12), range(12, 21), range(21, 26)]
THERMO_ENERGY_CHAPTERS = [
    "10-thermo-first-law-026-035.tex",
    "10-thermo-first-law-036-045.tex",
    "10-thermo-first-law-046-056.tex",
    "10-thermo-first-law-057-061.tex",
]
THERMO_ENERGY_EXPECTED = [
    range(26, 36), range(36, 46), range(46, 57), range(57, 62),
]
THERMO_KINETIC_CHAPTERS = [
    "11-kinetic-theory-062-072.tex",
    "11-kinetic-theory-073-083.tex",
    "11-kinetic-theory-084-094.tex",
    "11-kinetic-theory-095-103.tex",
    "11-kinetic-theory-104-112.tex",
]
THERMO_KINETIC_EXPECTED = [
    range(62, 73), range(73, 84), range(84, 95),
    range(95, 104), range(104, 113),
]
THERMO_ENTROPY_CHAPTERS = [
    "12-entropy-cycles-113-121.tex",
    "12-entropy-cycles-122-129.tex",
    "12-entropy-cycles-130-139.tex",
    "12-entropy-cycles-140-145.tex",
]
THERMO_ENTROPY_EXPECTED = [
    range(113, 122), range(122, 130), range(130, 140), range(140, 146),
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

if all_ids != list(range(1, 389)):
    errors.append("combined problem IDs are not exactly 1..388 in order")
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
if main.count(r"\section{流体动力学") != 1:
    errors.append("hydrodynamics section count is not one")
if main.count(r"\section{相对论力学") != 1:
    errors.append("relativity section count is not one")


# Thermodynamics uses ORIGINAL numbering 1,2,... instead of fake 389+.
thermo_ids = []
for name, expected in zip(THERMO_CHAPTERS, THERMO_EXPECTED):
    path = ROOT / "chapters" / name
    if not path.exists():
        errors.append(f"missing: {name}")
        continue
    s = path.read_text(encoding="utf-8")
    ids = [int(x) for x in re.findall(r"\\thermoproblem\{(\d+)\}\{", s)]
    want = list(expected)
    thermo_ids.extend(ids)
    if ids != want:
        errors.append(f"{name}: thermodynamics IDs {ids} != {want}")
    solutions = len(re.findall(r"\\exsolution\b", s))
    checks = len(re.findall(r"\\excheck\b", s))
    if solutions != len(want):
        errors.append(f"{name}: {solutions} solutions, expected {len(want)}")
    if checks != len(want):
        errors.append(f"{name}: {checks} checks, expected {len(want)}")
    if s.count("{") != s.count("}"):
        errors.append(f"{name}: unbalanced TeX braces")
    entry = r"\input{chapters/" + path.stem + "}"
    if entry not in main:
        errors.append(f"main.tex does not include: {name}")

if thermo_ids != list(range(1, 26)):
    errors.append("Part II section 2.1 original IDs are not exactly 1..25")

energy_ids = []
for name, expected in zip(THERMO_ENERGY_CHAPTERS, THERMO_ENERGY_EXPECTED):
    path = ROOT / "chapters" / name
    if not path.exists():
        errors.append(f"missing: {name}")
        continue
    content = path.read_text(encoding="utf-8")
    ids = [int(x) for x in re.findall(r"\\thermoenergyproblem\{(\d+)\}\{", content)]
    want = list(expected)
    energy_ids.extend(ids)
    if ids != want:
        errors.append(f"{name}: first-law original IDs {ids} != {want}")
    solutions = len(re.findall(r"\\exsolution\b", content))
    checks = len(re.findall(r"\\excheck\b", content))
    if solutions != len(want):
        errors.append(f"{name}: {solutions} solutions, expected {len(want)}")
    if checks != len(want):
        errors.append(f"{name}: {checks} checks, expected {len(want)}")
    if content.count("{") != content.count("}"):
        errors.append(f"{name}: unbalanced TeX braces")
    entry = r"\input{chapters/" + path.stem + "}"
    if entry not in main:
        errors.append(f"main.tex does not include: {name}")

if energy_ids != list(range(26, 62)):
    errors.append("Part II section 2.2 original IDs are not exactly 26..61")
if r"\newcommand{\thermoenergyproblem}" not in main:
    errors.append("main.tex missing thermoenergyproblem macro")
if main.count(r"\section{热力学第一定律与热容") != 1:
    errors.append("first law section count is not one")

# The second book part is a SINGLE independent 1..145 range,
# and each newly introduced subject has its own macro and source list.
subject_results = {}
for label, chapters, ranges, macro, expected_ids in [
    ("kinetic", THERMO_KINETIC_CHAPTERS, THERMO_KINETIC_EXPECTED,
     "thermokineticproblem", list(range(62, 113))),
    ("entropy", THERMO_ENTROPY_CHAPTERS, THERMO_ENTROPY_EXPECTED,
     "thermoentropyproblem", list(range(113, 146))),
]:
    observed = []
    for name, expected in zip(chapters, ranges):
        path = ROOT / "chapters" / name
        if not path.exists():
            errors.append(f"missing: {name}")
            continue
        content = path.read_text(encoding="utf-8")
        ids = [int(x) for x in re.findall(
            r"\\" + macro + r"\{(\d+)\}\{", content)]
        want = list(expected)
        observed.extend(ids)
        if ids != want:
            errors.append(f"{name}: original IDs {ids} != {want}")
        for command in ("exsolution", "excheck"):
            n = len(re.findall(r"\\" + command + r"\b", content))
            if n != len(want):
                errors.append(f"{name}: {n} {command}, expected {len(want)}")
        if content.count("{") != content.count("}"):
            errors.append(f"{name}: unbalanced TeX braces")
        entry = r"\input{chapters/" + path.stem + "}"
        if entry not in main:
            errors.append(f"main.tex does not include: {name}")
    if observed != expected_ids:
        errors.append(f"Part II {label} original IDs are not consecutive")
    if ("\\newcommand{" + chr(92) + macro + "}") not in main:
        errors.append(f"main.tex missing {macro} macro")
    subject_results[label] = observed

part_two = thermo_ids + energy_ids + subject_results["kinetic"] + subject_results["entropy"]
if part_two != list(range(1, 146)):
    errors.append("Part II combined original IDs are not exactly 1..145")
if main.count(r"\section{气体分子运动论") != 1:
    errors.append("kinetic theory section count is not one")
if main.count(r"\section{热力学第二定律与熵") != 1:
    errors.append("entropy section count is not one")

if main.count(r"\chapter{热力学与分子物理}") != 1:
    errors.append("Part II chapter count is not one")
if main.count(r"\section{气体状态方程与过程") != 1:
    errors.append("thermodynamics section count is not one")
if r"\newcommand{\thermoproblem}" not in main:
    errors.append("main.tex missing original-numbering thermoproblem macro")

if errors:
    for e in errors:
        print("FAIL:", e, file=sys.stderr)
    sys.exit(1)
print("PASS: 388 Part-I + 145 Part-II (25 gas-state + 36 first-law + 51 kinetic + 33 entropy) = 533 translated solved problems; original numbering and all chapters verified")
