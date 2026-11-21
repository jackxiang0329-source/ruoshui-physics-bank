# Irodov《普通物理学习题》中文版 · ElegantBook

底本：I. E. Irodov, *Problems in General Physics*，用户上传 Arihant 版 PDF（385 页）。
译注、补全推导以及本版勘误均属于研究用初稿；原书著作权与翻译、公开发行权归原权利人。

## 真实进度（2026-11-21）

- **本轮新增：第 21—70 题，共 50 题。**
- **累计：第 1—70 题，中文题面 + 逐题详细解析 + 核验提示。**
- 第 1.1 节“运动学”1—58 题已覆盖（全部）。
- 第 1.2 节“动力学基本方程”59—70 题已覆盖（本节尚未结束）。
- 本项目尚未完成整书翻译或独立学术二校；任何“编译成功”仅说明技术排版通过。

| 内容 | 文件 |
|---|---|
| ElegantBook 中文主文件 | [main.tex](main.tex) |
| 1—20题 | [01-mechanics-kinematics-001-020.tex](chapters/01-mechanics-kinematics-001-020.tex) |
| 21—30题 | [01-mechanics-kinematics-021-030.tex](chapters/01-mechanics-kinematics-021-030.tex) |
| 31—40题 | [01-mechanics-kinematics-031-040.tex](chapters/01-mechanics-kinematics-031-040.tex) |
| 41—50题 | [01-mechanics-kinematics-041-050.tex](chapters/01-mechanics-kinematics-041-050.tex) |
| 51—58题 | [01-mechanics-kinematics-051-058.tex](chapters/01-mechanics-kinematics-051-058.tex) |
| 59—70题 | [02-mechanics-dynamics-059-070.tex](chapters/02-mechanics-dynamics-059-070.tex) |
| 源书勘误 | [errata.md](errata.md) |
| 技术与学术质检记录 | [quality-check.md](quality-check.md) |
| 结构完整性检查 | [check_sources.py](check_sources.py) |

## 编译

在此目录内运行下列两条命令：

    python3 check_sources.py
    bash build.sh

需要 XeLaTeX、latexmk、TikZ 与 ElegantBook 4.7。
构建顺序为 cover.tex → main.tex。
GitHub Actions 工作流 .github/workflows/irodov-elegantbook.yml
运行源码覆盖检查、XeLaTeX 编译，上传 PDF 附件；
构建成功后尝试把 main.pdf、cover.pdf 回传当前仓库。
仅当工作流成功且 PDF 文件版本已更新，才应报告 PDF 已同步。

## 仓库隔离

本目录放在 external_sources/，不得将翻译题目混入
大学物理原创高难度题库 bank/ 的题数和质量门禁，也不修改它们的权威源文件。
后续继续从原书第 71 题起逐题补充，保持题号及印刷页对应。
