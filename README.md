# 三千弱水 · 大学物理原创试题库

目标 10,000 道大学物理原创试题。当前共有 **48 道样板题（6大模块各8题）**，全部仍为 **待独立复核**；仅完成部分自动公式一致性检测，不代表六轮质检通过。

## 2026-10-26 新版结构：ElegantBook 与独立 TeX

题目的唯一权威文字源为 bank/ID/question.tex 和 bank/ID/solution.tex，元数据为 bank/ID/meta.json（含题型、难度、知识点、答案和审核状态）。48题共拆分成144个文件。旧版 data/problems.json 仅保留为迁移前历史快照，后续新增题不需要编辑它。

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

完成100道首批样板题（仍差52道），逐题增加原创性审查、独立解题复核、量纲/边界条件检查、考试难度配置；再扩展至1,000与10,000题。教材正文和高校真题尚未完整获授权核对，不能声称零重复。

## 2026-10-26 新增题（第3组）

新增12道：M007–M008、E007–E008、T007–T008、W007–W008、O007–O008、Q007–Q008。独立题干、解答与元数据均已入库；`scripts/check_physics.py` 增加12项对应公式核对。此检查需在 CI/运行环境执行，不能当作专家独立审稿；当前仍不开放正式考试选题。

### 六轮审核自动门禁

运行 `python scripts/check_review.py` 可以检查所有宣称「质检通过」题目的六轮证据记录、审核人字段、源文件SHA绑定。未建立真实审核凭证前不得改成通过。当前48道全部待审。审核凭证格式见 [qa/README.md](qa/README.md)。

### 历史质检文件说明

`data/qa_physics_spotchecks.json` 的36项结果仅是早期历史快照，不能据此判断现有48题整体已通过自动检查；`scripts/check_physics.py` 现含48道题的检验定义。完整仓库构建仍受GitHub Actions作业未启动问题影响。
