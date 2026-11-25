#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if [ -f ../../data/archives/irodov_chapters.zip ]; then
  python3 ../../scripts/compact_auxiliary.py --restore --group irodov_chapters
fi
latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error cover.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex
echo "Created main.pdf"
