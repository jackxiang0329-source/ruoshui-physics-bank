# 三千弱水 · 大学物理原创试题库

目标 10,000 道大学物理原创试题。当前共有 **84 道样板题（6大模块各14题）**，全部仍为 **待独立复核**；仅完成部分自动公式一致性检测，不代表六轮质检通过。

## 2026-10-26 新版结构：ElegantBook 与独立 TeX

题目的唯一权威文字源为 bank/ID/question.tex 和 bank/ID/solution.tex，元数据为 bank/ID/meta.json（含题型、难度、知识点、答案和审核状态）。84题共拆分成252个文件。旧版 data/problems.json 仅保留为迁移前历史快照，后续新增题不需要编辑它。

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

完成100道首批样板题（仍差16道），逐题增加原创性审查、独立解题复核、量纲/边界条件检查、考试难度配置；再扩展至1,000与10,000题。教材正文和高校真题尚未完整获授权核对，不能声称零重复。

## 2026-10-26 新增题（第3组）

新增12道：M007–M008、E007–E008、T007–T008、W007–W008、O007–O008、Q007–Q008。独立题干、解答与元数据均已入库；`scripts/check_physics.py` 增加12项对应公式核对。此检查需在 CI/运行环境执行，不能当作专家独立审稿；当前仍不开放正式考试选题。

### 六轮审核自动门禁

运行 `python scripts/check_review.py` 可以检查所有宣称「质检通过」题目的六轮证据记录、审核人字段、源文件SHA绑定。未建立真实审核凭证前不得改成通过。当前84道全部待审。审核凭证格式见 [qa/README.md](qa/README.md)。

### 历史质检文件说明

`data/qa_physics_spotchecks.json` 的36项结果仅是早期历史快照，不能据此判断现有84题整体已通过自动检查；`scripts/check_physics.py` 现含84道题的检验定义。完整仓库构建仍受GitHub Actions作业未启动问题影响。

## 2026-10-26 新增题（第4组）

新增12道：M009–M010、E009–E010、T009–T010、W009–W010、O009–O010、Q009–Q010；每题保留独立题干、解析和元数据。已扩展代数关系检查定义，但完整执行与ElegantBook PDF编译仍取决于仓库CI恢复。所有题目均处于待独立复核状态。

### 按考试需求组卷与质量报告

现支持 `--topic-quota`、`--kind`、`--max-minutes`、`--total-points` 等组卷约束。详见 [docs/EXAM_ASSEMBLY.md](docs/EXAM_ASSEMBLY.md)。完整物理公式检查运行时将结果写入暂存的 `generated/qa_physics_current.json`，不再覆盖已提交的36题历史质检快照；GitHub Actions能运行后，这份当前报告和试卷清单将上传为Artifacts。正式组卷仍需六轮真实审核凭证，自动校验不能替代独立学术复核。

## 2026-10-26 新增题（第5组）

新增12道：M011–M012、E011–E012、T011–T012、W011–W012、O011–O012、Q011–Q012。首次系统引入六道单项选择题和实验分析、填空题，并保留可机器读取的选项与标准答案。按独立TeX组织，不复制已有经典题目全文；所有72题均为待独立复核，不能作为正式试卷题目。程序化公式检查仍需在CI环境执行。

### 结构化单选题自检

选择题的 `meta.json` 中增加 `choices: [["A",...],..., ["D",...]]` 与 `correct_option`，脚本在构建时核查4个选项的顺序、答案映射及独立题干TeX选项内容。非选择题不会拥有选择题特有字段。汇总报告已更新为84题，但云端完整检查和ElegantBook编译依然标为尚未执行成功。

## 2026-10-26 新增题（第6组）

新增12道 M013–M014、E013–E014、T013–T014、W013–W014、O013–O014、Q013–Q014，六大模块各2道，覆盖临界滑动实验、磁通量变化与焦耳热、霍尔电压、稳态热传导、机械波正常模、光栅分辨本领、薄透镜测量、核反应能和狭义相对论速度合成等。全部保留单题独立TeX与元数据，尚未完成独立学术审核；云端编译状态以Actions为准。
