#!/usr/bin/env bash
set -euo pipefail
OWNER="jackxiang0329-source"
REPO="ruoshui-university-physics"
cd "$(dirname "$0")"
command -v git >/dev/null || { echo '缺少 git，请安装 Git。' >&2; exit 1; }
command -v gh >/dev/null || { echo '缺少 GitHub CLI (gh)，请安装 https://cli.github.com/' >&2; exit 1; }
gh auth status >/dev/null || { echo '请先执行 gh auth login。' >&2; exit 1; }
if gh repo view "$OWNER/$REPO" >/dev/null 2>&1; then
  echo "目标仓库 $OWNER/$REPO 已存在；为避免覆盖，请手动检查。" >&2; exit 2
fi
if [ ! -d .git ]; then git init -b main; fi
if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
  git add .
  git commit -m 'Initialize independent Ruoshui university physics question bank'
fi
gh repo create "$OWNER/$REPO" --private --source . --remote origin --push
printf '\n发布地址：https://github.com/%s/%s\n' "$OWNER" "$REPO"
