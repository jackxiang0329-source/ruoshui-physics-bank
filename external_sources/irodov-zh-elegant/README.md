# Irodov《普通物理学习题》中文版 · ElegantBook

原书：I. E. Irodov，*Problems in General Physics*，用户上传的 Arihant 版（PDF 385页）。

**首批范围**：第一篇运动学第 **1—20题**，中文题面、分步骤推导、条件与量纲检查，附图1.1、1.2、1.3的TikZ重绘。**不是整书翻译完成，独立专家二校待完成。**

## 编译与文件
- `main.tex`：ElegantBook 4.7 中文主文件。
- `chapters/01-mechanics-kinematics-001-020.tex`：第1—20题独立译注与解答。
- `cover.tex`：用TikZ生成封面图，需先编译。
- `elegantbook.cls`：ElegantLaTeX官方4.7类文件（LPPL 1.3c）。
- `build.sh`：先编译封面，再编译正文。
- `quality-check.md`：质检说明。
- `.github/workflows/irodov-elegantbook.yml`：GitHub Actions自动生成PDF附件。

在本目录执行 `bash build.sh`；需要XeLaTeX、latexmk和完整TeX Live 2026。Actions中名为 `irodov-zh-elegantbook-pdf` 的附件在成功构建后可供获取。

## 隔离要求
本目录属于 `external_sources/`，是译著资料，不是原创综合压轴题，**不得计入**正式大学物理主库的题量统计，也不修改现有题库权威文件。

## 版权
原书及翻译、复制、公开传播等权利仍归权利人。本文件的生成并不授予公开发行或商业使用授权；任何再发行和整书发布须自行核实相关许可。模板以LPPL 1.3c使用。
