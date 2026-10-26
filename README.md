# 三千弱水 · 大学物理原创试题库

目标 10,000 道大学物理原创试题。当前共有 **36 道样板题（6大模块各6题）**，全部仍为 **待独立复核**；仅完成部分自动公式一致性检测，不代表六轮质检通过。

## 2026-10-26 新版结构：ElegantBook 与独立 TeX

题目的唯一权威文字源为 bank/ID/question.tex 和 bank/ID/solution.tex，元数据为 bank/ID/meta.json（含题型、难度、知识点、答案和审核状态）。36题共拆分成108个文件。旧版 data/problems.json 仅保留为迁移前历史快照，后续新增题不需要编辑它。

tex/questions.tex 与 tex/solutions.tex 使用 ElegantBook 模板，通过 LaTeX 的 input 命令引用独立题源；后续按知识点筛选及系统组卷只需重排引用，不复制题面、不覆盖原题TeX。

## 开发与组卷命令

    python -m pip install -r requirements.txt
    python scripts/check_physics.py
    python scripts/build.py --check
    python scripts/build.py
    python scripts/render_single.py M001 --solutions
    python scripts/assemble_exam.py --count 8 --seed 20261026 --allow-pending

默认组卷**不使用待独立复核的题**；--allow-pending 仅允许内部测试。自动构建成功后，从 GitHub Actions Artifacts 下载最新 ElegantBook PDF。仓库 pdf/ 下的旧PDF是迁移前的版本，不代表新模板构建结果。

参见 [TeX独立化设计说明](docs/TEX_ARCHITECTURE.md)、[六轮质检协议](docs/QA_PROTOCOL.md)、[参考教材书目](docs/REFERENCES.md)。

## 下一阶段

完成100道首批样板题（仍差64道），逐题增加原创性审查、独立解题复核、量纲/边界条件检查、考试难度配置；再扩展至1,000与10,000题。教材正文和高校真题尚未完整获授权核对，不能声称零重复。
