#!/usr/bin/env python3
"""Per-problem TeX integrity audit for the complete Chinese Irodov book.

Unlike the chapter-wide count in check_sources.py, this checks *each*
individual problem and detects misplaced/missing solution or QA sections.
It also reports TeX math/environment delimiter anomalies for follow-up.
This is a structural tool, NOT a mathematical or physics correctness proof.
"""
from __future__ import annotations

from pathlib import Path
from collections import Counter
import re
import sys

ROOT = Path(__file__).resolve().parent
HEADER = re.compile(r"\\([A-Za-z]+problem)\{(\d+)\}\{[^}]*\}")
INPUT = re.compile(r"\\input\{chapters/([^}]+)\}")
SOLUTION = re.compile(r"\\exsolution\b")
CHECK = re.compile(r"\\excheck\b")
ENV = re.compile(r"\\(begin|end)\{([A-Za-z*]+)\}")
MATH = re.compile(r"(?<!\\)\\\[|(?<!\\)\\\]|(?<!\\)\\\(|(?<!\\)\\\)|(?<!\\)\$")
fatal: list[str] = []
notices: list[str] = []


def strip_comments(source: str) -> str:
    lines = []
    for line in source.splitlines(keepends=True):
        end = len(line)
        for pos, char in enumerate(line):
            if char != "%":
                continue
            backslashes = 0
            j = pos - 1
            while j >= 0 and line[j] == "\\":
                backslashes += 1
                j -= 1
            if backslashes % 2 == 0:
                end = pos
                break
        if end == len(line):
            lines.append(line)
        else:
            lines.append(line[:end] + ("\n" if line.endswith("\n") else ""))
    return "".join(lines)


def check_delimiters(source: str, filename: str) -> None:
    """Report unmatched math or named environments; don't mistake a warning for review."""
    stack: list[str] = []
    for match in MATH.finditer(source):
        tok = match.group()
        if tok in (r"\[", r"\("):
            stack.append(r"\]" if tok == r"\[" else r"\)")
        elif tok == "$":
            if stack and stack[-1] == "$":
                stack.pop()
            elif not stack:
                stack.append("$")
            else:
                notices.append(f"{filename}: math '$' inside {stack[-1]} near {match.start()}")
        elif not stack or stack[-1] != tok:
            notices.append(f"{filename}: out-of-order math delimiter {tok} near {match.start()}")
        else:
            stack.pop()
    if stack:
        notices.append(f"{filename}: unclosed math delimiters {stack[-6:]}")

    nesting: list[str] = []
    for match in ENV.finditer(source):
        typ, label = match.groups()
        if typ == "begin":
            nesting.append(label)
        elif not nesting or nesting[-1] != label:
            notices.append(f"{filename}: unpaired environment \\end{{{label}}}")
        else:
            nesting.pop()
    if nesting:
        notices.append(f"{filename}: unclosed TeX environments {nesting[-6:]}")


def main() -> int:
    master = (ROOT / "main.tex").read_text(encoding="utf-8")
    names = INPUT.findall(master)
    if len(names) != len(set(names)):
        fatal.append("Duplicate chapter \\input references in main.tex")
    chapter_count = 0
    problem_count = 0
    for name in names:
        filename = name + ".tex"
        path = ROOT / "chapters" / filename
        if not path.is_file():
            fatal.append(f"Missing chapter: {filename}")
            continue
        text = strip_comments(path.read_text(encoding="utf-8"))
        markers = list(HEADER.finditer(text))
        if not markers:
            fatal.append(f"{filename}: no original numbered problem blocks")
            continue
        chapter_count += 1
        problem_count += len(markers)
        for index, marker in enumerate(markers):
            end = markers[index + 1].start() if index + 1 < len(markers) else len(text)
            block = text[marker.end():end]
            solutions = list(SOLUTION.finditer(block))
            checks = list(CHECK.finditer(block))
            ref = f"{filename} original #{marker.group(2)}"
            if len(solutions) != 1:
                fatal.append(f"{ref}: found {len(solutions)} detailed solution markers, expected one")
            if len(checks) != 1:
                fatal.append(f"{ref}: found {len(checks)} independent QA markers, expected one")
            if solutions and checks and solutions[0].start() >= checks[0].start():
                fatal.append(f"{ref}: \\excheck precedes \\exsolution")
            if solutions and not block[:solutions[0].start()].strip():
                fatal.append(f"{ref}: empty problem statement")
            if solutions and checks and not block[solutions[0].end():checks[0].start()].strip():
                fatal.append(f"{ref}: empty derivation section")
            if checks and not block[checks[0].end():].strip():
                fatal.append(f"{ref}: empty QA section")
        check_delimiters(text, filename)

    if chapter_count != 40 or problem_count != 1878:
        fatal.append(f"Expected 40 consolidated chapters and 1878 problems; got {chapter_count} and {problem_count}")

    for warning in notices[:80]:
        print("MATH/ENV REVIEW:", warning)
    if len(notices) > 80:
        print(f"MATH/ENV REVIEW: {len(notices) - 80} additional notices omitted")
    for message in fatal[:120]:
        print("FAIL:", message, file=sys.stderr)
    if fatal:
        print(f"FAIL: {len(fatal)} per-problem integrity errors", file=sys.stderr)
        return 1
    if notices:
        print(f"FAIL: {len(notices)} TeX mathematical/environment delimiter anomalies",
              file=sys.stderr)
        return 1
    print(f"PASS: {problem_count} independently segmented problems in {chapter_count} chapters;"
          " each has statement, derivation, ordered QA and no duplicate problem input.")
    print("PASS: no unmatched TeX math delimiters or named environments in any chapter;"
          " XeLaTeX and independent physics peer review remain separate acceptance stages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
