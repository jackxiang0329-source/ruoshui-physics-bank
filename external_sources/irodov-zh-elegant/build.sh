#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error cover.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex
echo "Created main.pdf"
