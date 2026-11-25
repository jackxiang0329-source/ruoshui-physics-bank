#!/usr/bin/env bash
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
export TEXINPUTS="$here/../irodov-zh-elegant//:"
cd "$here"
if [ -f ../../data/archives/three_college_chapters.zip ]; then
  python3 ../../scripts/compact_auxiliary.py --restore --group three_college_chapters
fi
python3 check_math.py
latexmk -pdfxe -interaction=nonstopmode -halt-on-error -file-line-error main.tex
