#!/usr/bin/env bash
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
# 与本仓库已有 Irodov ElegantBook 排版共享类文件。
export TEXINPUTS="$here/../irodov-zh-elegant//:"
cd "$here"
latexmk -pdfxe -interaction=nonstopmode -halt-on-error -file-line-error main.tex
echo "PDF: $here/main.pdf"
