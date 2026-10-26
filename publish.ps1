# Run from this extracted project directory. Requires Git + GitHub CLI authentication.
$ErrorActionPreference = 'Stop'
$owner = 'jackxiang0329-source'
$repo = 'ruoshui-university-physics'
Set-Location $PSScriptRoot
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw '请先安装 Git。' }
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) { throw '请先安装 GitHub CLI: https://cli.github.com/' }
& gh auth status
if ($LASTEXITCODE -ne 0) { throw '请先执行 gh auth login。' }
& gh repo view "$owner/$repo" 2>$null
if ($LASTEXITCODE -eq 0) { throw "仓库 $owner/$repo 已存在，为避免覆盖已退出。" }
if (-not (Test-Path .git)) { & git init -b main; if ($LASTEXITCODE -ne 0) { throw 'git init 失败。' } }
& git rev-parse --verify HEAD 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) {
  & git add .; if ($LASTEXITCODE -ne 0) { throw 'git add 失败。' }
  & git commit -m 'Initialize independent Ruoshui university physics question bank'
  if ($LASTEXITCODE -ne 0) { throw 'git commit 失败。请先设置 git config --global user.name 和 user.email。' }
}
& gh repo create "$owner/$repo" --private --source . --remote origin --push
if ($LASTEXITCODE -ne 0) { throw 'GitHub 创建或推送失败。' }
Write-Host "发布地址：https://github.com/$owner/$repo"
