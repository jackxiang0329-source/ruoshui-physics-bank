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
    "12-entropy-cycles-146-159.tex",
]
THERMO_ENTROPY_EXPECTED = [
    range(113, 122), range(122, 130), range(130, 140),
    range(140, 146), range(146, 160),
]
THERMO_CAPILLARY_CHAPTERS = [
    "13-capillarity-160-169.tex",
    "13-capillarity-170-179.tex",
    "13-capillarity-180-184.tex",
]
THERMO_CAPILLARY_EXPECTED = [
    range(160, 170), range(170, 180), range(180, 185),
]
THERMO_PHASE_CHAPTERS = [
    "14-phase-transformations-185-194.tex",
    "14-phase-transformations-195-204.tex",
    "14-phase-transformations-205-214.tex",
    "14-phase-transformations-215-219.tex",
]
THERMO_PHASE_EXPECTED = [
    range(185, 195), range(195, 205),
    range(205, 215), range(215, 220),
]
THERMO_TRANSPORT_CHAPTERS = [
    "15-transport-220-229.tex",
    "15-transport-230-239.tex",
    "15-transport-240-245.tex",
    "15-transport-246-257.tex",
]
THERMO_TRANSPORT_EXPECTED = [
    range(220, 230), range(230, 240), range(240, 246), range(246, 258),
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

# The second book part is a SINGLE independent 1..257 range,
# and each newly introduced subject has its own macro and source list.
subject_results = {}
for label, chapters, ranges, macro, expected_ids in [
    ("kinetic", THERMO_KINETIC_CHAPTERS, THERMO_KINETIC_EXPECTED,
     "thermokineticproblem", list(range(62, 113))),
    ("entropy", THERMO_ENTROPY_CHAPTERS, THERMO_ENTROPY_EXPECTED,
     "thermoentropyproblem", list(range(113, 160))),
    ("capillarity", THERMO_CAPILLARY_CHAPTERS, THERMO_CAPILLARY_EXPECTED,
     "thermocapillaryproblem", list(range(160, 185))),
    ("phase", THERMO_PHASE_CHAPTERS, THERMO_PHASE_EXPECTED,
     "thermophaseproblem", list(range(185, 220))),
    ("transport", THERMO_TRANSPORT_CHAPTERS, THERMO_TRANSPORT_EXPECTED,
     "thermotransportproblem", list(range(220, 258))),
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

part_two = (thermo_ids + energy_ids
            + subject_results["kinetic"] + subject_results["entropy"]
            + subject_results["capillarity"] + subject_results["phase"]
            + subject_results["transport"])
if part_two != list(range(1, 258)):
    errors.append("Part II combined original IDs are not exactly 1..257")
if main.count(r"\section{气体分子运动论") != 1:
    errors.append("kinetic theory section count is not one")
if main.count(r"\section{热力学第二定律与熵") != 1:
    errors.append("entropy section count is not one")


if main.count(r"\section{液体与毛细现象") != 1:
    errors.append("capillarity section count is not one")
if main.count(r"\section{相变与饱和蒸气") != 1:
    errors.append("phase section count is not one")
if main.count(r"\section{输运现象") != 1:
    errors.append("transport section count is not one")

if main.count(r"\chapter{热力学与分子物理}") != 1:
    errors.append("Part II chapter count is not one")
if main.count(r"\section{气体状态方程与过程") != 1:
    errors.append("thermodynamics section count is not one")
if r"\newcommand{\thermoproblem}" not in main:
    errors.append("main.tex missing original-numbering thermoproblem macro")

# Part III starts with original problem 1, independently of Parts I and II.
ELECTRO_VACUUM_CHAPTERS = [
    "16-electrostatics-vacuum-001-012.tex",
    "16-electrostatics-vacuum-013-027.tex",
    "16-electrostatics-vacuum-028-040.tex",
    "16-electrostatics-vacuum-041-053.tex",
]
ELECTRO_VACUUM_RANGES = [
    range(1, 13), range(13, 28), range(28, 41), range(41, 54),
]
ELECTRO_CONDUCT_CHAPTERS = [
    "17-electro-conductors-054-065.tex",
    "17-electro-conductors-066-077.tex",
    "17-electro-conductors-078-088.tex",
    "17-electro-conductors-089-100.tex",
]
ELECTRO_CONDUCT_RANGES = [
    range(54, 66), range(66, 78), range(78, 89), range(89, 101),
]
ELECTRO_CAP_CHAPTERS = [
    "18-capacitance-energy-101-112.tex",
    "18-capacitance-energy-113-121.tex",
    "18-capacitance-energy-122-130.tex",
    "18-capacitance-energy-131-140.tex",
    "18-capacitance-energy-141-146.tex",
]
ELECTRO_CAP_RANGES = [
    range(101, 113), range(113, 122), range(122, 131),
    range(131, 141), range(141, 147),
]
ELECTRO_CURRENT_CHAPTERS = [
    "19-electric-current-147-160.tex",
    "19-electric-current-161-175.tex",
    "19-electric-current-176-188.tex",
    "19-electric-current-189-200.tex",
    "19-electric-current-201-218.tex",
]
ELECTRO_CURRENT_RANGES = [
    range(147, 161), range(161, 176), range(176, 189),
    range(189, 201), range(201, 219),
]
ELECTRO_MAGNET_CHAPTERS = [
    "20-magnetostatics-219-235.tex",
    "20-magnetostatics-236-250.tex",
    "20-magnetostatics-251-262.tex",
    "20-magnetostatics-263-274.tex",
    "20-magnetostatics-275-287.tex",
]
ELECTRO_MAGNET_RANGES = [
    range(219, 236), range(236, 251), range(251, 263),
    range(263, 275), range(275, 288),
]
ELECTRO_INDUCTION_CHAPTERS = [
    "21-induction-288-288.tex",
    "21-induction-289-304.tex",
    "21-induction-305-322.tex",
    "21-induction-323-346.tex",
    "21-induction-347-371.tex",
]
ELECTRO_INDUCTION_RANGES = [
    range(288, 289), range(289, 305), range(305, 323),
    range(323, 347), range(347, 372),
]
ELECTRO_CHARGED_CHAPTERS = [
    "22-charged-particles-372-388.tex",
    "22-charged-particles-389-407.tex",
]
ELECTRO_CHARGED_RANGES = [
    range(372, 389), range(389, 408),
]
OSC_CHAPTERS = [
    "23-mechanical-oscillations-001-020.tex",
    "23-mechanical-oscillations-021-033.tex",
    "23-mechanical-oscillations-034-050.tex",
    "23-mechanical-oscillations-051-065.tex",
    "23-mechanical-oscillations-066-081.tex",
    "23-mechanical-oscillations-082-093.tex",
]
OSC_RANGES = [
    range(1, 21), range(21, 34), range(34, 51),
    range(51, 66), range(66, 82), range(82, 94),
]
ELEC_OSC_CHAPTERS = [
    "24-electric-oscillations-094-109.tex",
    "24-electric-oscillations-110-125.tex",
    "24-electric-oscillations-126-137.tex",
    "24-electric-oscillations-138-149.tex",
]
ELEC_OSC_RANGES = [
    range(94, 110), range(110, 126),
    range(126, 138), range(138, 150),
]
WAVES_CHAPTERS = [
    "25-elastic-waves-150-165.tex",
    "25-elastic-waves-166-181.tex",
    "25-elastic-waves-182-188.tex",
]
WAVES_RANGES = [
    range(150, 166), range(166, 182), range(182, 189),
]
EM_WAVES_CHAPTERS = [
    "26-em-waves-189-200.tex",
    "26-em-waves-201-212.tex",
    "26-em-waves-213-224.tex",
]
EM_WAVES_RANGES = [
    range(189, 201), range(201, 213), range(213, 225),
]
OPTICS_CHAPTERS = [
    "27-optics-photometry-001-012.tex",
    "27-optics-photometry-013-025.tex",
    "27-optics-photometry-026-035.tex",
    "27-optics-photometry-036-045.tex",
    "27-optics-photometry-046-057.tex",
    "27-optics-photometry-058-063.tex",
]
OPTICS_RANGES = [
    range(1, 13), range(13, 26), range(26, 36),
    range(36, 46), range(46, 58), range(58, 64),
]
INTERFERENCE_CHAPTERS = [
    "28-optics-interference-064-075.tex",
    "28-optics-interference-076-086.tex",
    "28-optics-interference-087-096.tex",
]
INTERFERENCE_RANGES = [
    range(64, 76), range(76, 87), range(87, 97),
]
DIFFRACTION_CHAPTERS = [
    "29-optics-diffraction-097-108.tex",
    "29-optics-diffraction-109-118.tex",
    "29-optics-diffraction-119-130.tex",
    "29-optics-diffraction-131-142.tex",
    "29-optics-diffraction-143-150.tex",
    "29-optics-diffraction-151-156.tex",
]
DIFFRACTION_RANGES = [
    range(97, 109), range(109, 119), range(119, 131),
    range(131, 143), range(143, 151), range(151, 157),
]
POLARIZATION_CHAPTERS = [
    "30-optics-polarization-157-157.tex",
    "30-optics-polarization-158-175.tex",
    "30-optics-polarization-176-199.tex",
]
POLARIZATION_RANGES = [range(157, 158), range(158, 176), range(176, 200)]
DISPERSION_CHAPTERS = ["31-optics-dispersion-200-215.tex", "31-optics-dispersion-216-223.tex"]
DISPERSION_RANGES = [range(200, 216), range(216, 224)]

part_three = []
for macro, filenames, expected_ranges in [
    ("electroproblem", ELECTRO_VACUUM_CHAPTERS, ELECTRO_VACUUM_RANGES),
    ("electroconductproblem", ELECTRO_CONDUCT_CHAPTERS, ELECTRO_CONDUCT_RANGES),
    ("electrocapproblem", ELECTRO_CAP_CHAPTERS, ELECTRO_CAP_RANGES),
    ("electrocurrentproblem", ELECTRO_CURRENT_CHAPTERS, ELECTRO_CURRENT_RANGES),
    ("electromagproblem", ELECTRO_MAGNET_CHAPTERS, ELECTRO_MAGNET_RANGES),
    ("electroinductionproblem", ELECTRO_INDUCTION_CHAPTERS, ELECTRO_INDUCTION_RANGES),
    ("electrochargedproblem", ELECTRO_CHARGED_CHAPTERS, ELECTRO_CHARGED_RANGES),
]:
    if (r"\newcommand{" + chr(92) + macro + "}") not in main:
        errors.append(f"main.tex missing macro {macro}")
    for name, expected in zip(filenames, expected_ranges):
        path = ROOT / "chapters" / name
        if not path.exists():
            errors.append(f"missing: {name}")
            continue
        content = path.read_text(encoding="utf-8")
        ids = [int(x) for x in re.findall(
            r"\\" + macro + r"\{(\d+)\}\{", content)]
        want = list(expected)
        part_three.extend(ids)
        if ids != want:
            errors.append(f"{name}: Part-III original IDs {ids} != {want}")
        for command in ("exsolution", "excheck"):
            count = len(re.findall(r"\\" + command + r"\b", content))
            if count != len(want):
                errors.append(f"{name}: {command} count {count} != {len(want)}")
        if content.count("{") != content.count("}"):
            errors.append(f"{name}: TeX braces unbalanced")
        entry = r"\input{chapters/" + path.stem + "}"
        if entry not in main:
            errors.append(f"main.tex missing chapter: {name}")
if part_three != list(range(1, 408)):
    errors.append("Part III independent numbering is not exactly 1..407")
if main.count(r"\chapter{电动力学}") != 1:
    errors.append("Part III chapter count is not one")
if main.count(r"\section{真空中的恒定电场") != 1:
    errors.append("Part III vacuum electrostatics section count is not one")
if main.count(r"\section{静电场中的导体与电介质") != 1:
    errors.append("Part III conductor/dielectric section count is not one")
if main.count(r"\section{电容与静电场能") != 1:
    errors.append("Part III capacitance/energy section count is not one")
if main.count(r"\section{恒定电流") != 1:
    errors.append("Part III electric-current section count is not one")
if main.count(r"\section{恒定磁场与磁介质") != 1:
    errors.append("Part III magnetostatics section count is not one")
if main.count(r"\section{电磁感应与麦克斯韦方程") != 1:
    errors.append("Part III induction section count is not one")
if main.count(r"\section{带电粒子在电磁场中的运动") != 1:
    errors.append("Part III charged particles section count is not one")

part_four = []
for macro, filenames, ranges in [
    ("oscproblem", OSC_CHAPTERS, OSC_RANGES),
    ("electricoscproblem", ELEC_OSC_CHAPTERS, ELEC_OSC_RANGES),
    ("waveproblem", WAVES_CHAPTERS, WAVES_RANGES),
    ("emwaveproblem", EM_WAVES_CHAPTERS, EM_WAVES_RANGES),
]:
    if (r"\newcommand{" + chr(92) + macro + "}") not in main:
        errors.append(f"main.tex missing macro {macro}")
    for name, expected in zip(filenames, ranges):
        path = ROOT / "chapters" / name
        if not path.exists():
            errors.append(f"missing: {name}")
            continue
        content = path.read_text(encoding="utf-8")
        ids = [int(x) for x in re.findall(
            r"\\" + macro + r"\{(\d+)\}\{", content)]
        want = list(expected)
        part_four.extend(ids)
        if ids != want:
            errors.append(f"{name}: Part-IV IDs {ids} != {want}")
        for command in ("exsolution", "excheck"):
            count = len(re.findall(r"\\" + command + r"\b", content))
            if count != len(want):
                errors.append(f"{name}: {command} count {count} != {len(want)}")
        if content.count("{") != content.count("}"):
            errors.append(f"{name}: TeX braces unbalanced")
        if r"\input{chapters/" + path.stem + "}" not in main:
            errors.append(f"main.tex missing chapter: {name}")
if part_four != list(range(1, 225)):
    errors.append("Part IV independent numbering is not exactly 1..224")
if main.count(r"\chapter{振动与波动}") != 1:
    errors.append("Part IV chapter count is not one")
if main.count(r"\section{机械振动") != 1:
    errors.append("Part IV §4.1 mechanical-oscillations section count is not one")
if main.count(r"\section{电振荡") != 1:
    errors.append("Part IV §4.2 electric-oscillations section count is not one")
if main.count(r"\section{弹性波与声学") != 1:
    errors.append("Part IV §4.3 waves section count is not one")
if main.count(r"\section{电磁波与辐射") != 1:
    errors.append("Part IV §4.4 electromagnetic-waves section count is not one")

part_five = []
for macro, filenames, ranges in [
    ("opticsproblem", OPTICS_CHAPTERS, OPTICS_RANGES),
    ("interferenceproblem", INTERFERENCE_CHAPTERS, INTERFERENCE_RANGES),
    ("diffractionproblem", DIFFRACTION_CHAPTERS, DIFFRACTION_RANGES),
    ("polarizationproblem", POLARIZATION_CHAPTERS, POLARIZATION_RANGES),
    ("dispersionproblem", DISPERSION_CHAPTERS, DISPERSION_RANGES),
]:
    if (r"\newcommand{" + chr(92) + macro + "}") not in main:
        errors.append(f"main.tex missing macro {macro}")
    for name, expected in zip(filenames, ranges):
        path = ROOT / "chapters" / name
        if not path.exists():
            errors.append(f"missing: {name}")
            continue
        content = path.read_text(encoding="utf-8")
        ids = [int(x) for x in re.findall(
            r"\\" + macro + r"\{(\d+)\}\{", content)]
        want = list(expected)
        part_five.extend(ids)
        if ids != want:
            errors.append(f"{name}: Part-V original IDs {ids} != {want}")
        for command in ("exsolution", "excheck"):
            count = len(re.findall(r"\\" + command + r"\b", content))
            if count != len(want):
                errors.append(f"{name}: {command} count {count} != {len(want)}")
        if content.count("{") != content.count("}"):
            errors.append(f"{name}: TeX braces unbalanced")
        if r"\input{chapters/" + path.stem + "}" not in main:
            errors.append(f"main.tex missing chapter: {name}")
if part_five != list(range(1, 224)):
    errors.append("Part V independent numbering is not exactly 1..223")
if main.count(r"\chapter{光学}") != 1:
    errors.append("Part V chapter count is not one")
for heading in (
    "光度学与几何光学", "光的干涉", "光的衍射", "光的偏振", "光的色散与吸收",
):
    if main.count(r"\section{" + heading) != 1:
        errors.append(f"Part V section missing or duplicated: {heading}")

if errors:
    for e in errors:
        print("FAIL:", e, file=sys.stderr)
    sys.exit(1)
print("PASS: 388 Part-I + 257 Part-II + 407 Part-III + 224 Part-IV + 223 Part-V = 1499 translated solved problems in 135 chapter files; all five independent numbering ranges verified")
