#!/usr/bin/env bash
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
export TEXINPUTS="$here/../irodov-zh-elegant//:"
cd "$here"
python3 check_math.py
latexmk -pdfxe -interaction=nonstopmode -halt-on-error -file-line-error main.tex
