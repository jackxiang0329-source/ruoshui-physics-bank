# 三千弱水 · 大学物理高难度综合压轴题库

自 2026-10-28 起，主库**只收录高难度综合压轴题**。正式主库目前 **30 道**（5/5 二十三道，4/5 七道），均为待独立复核，不能视为六轮专家质检完成。

## 当前唯一正式题库
- `bank/ID/meta.json`、`question.tex`、`solution.tex` 为权威源；`data/problems.json` 是可读镜像。
- `tex/questions.tex`、`tex/solutions.tex` 和 `data/index.csv` 由主库生成。
- `scripts/check_difficulty_gate.py` 检查准入；`scripts/build.py --check` 检查结构与生成内容。
- 新增题必须达到 4/5 或 5/5、至少40分钟、至少四个递进小问和三个交叉知识标签，并有完整推导。详见 [标准](docs/HIGH_DIFFICULTY_POLICY.md)。

旧版 100 道普通题已逐题审查并从活跃的 `bank/` 移除或以新版综合题替换，同编号不表示旧题保留。原稿可在 Git 历史中追溯。

`external_sources/`、`localization/`、`localized/` 仅为隔离的未审候选材料，**不进入主库/试卷/统计/PDF**，禁止自动导入。定时自动进口工作流已停用。

题目自动校验与 PDF 编译仅是技术质检，不等于独立学术审校。

## 2026-10-28 第二批新增

每个模块再补充一题，M009/E009/T009/W009/O009/Q009；全部保留 `待独立复核`，CI 新增符号与独立数值检查，详见 `scripts/check_composite_expansion.py`。旧基础题仍不进入主库。

## 批量扩库：第三批（上半）
M010–M011、E010–E011、T010–T011，共6道，均包含四个递进问题、完整推导及极限/条件检验，状态待独立复核。

## 本轮批量扩库：30 道
另增 W010/W011、O010/O011、Q010/Q011，保持每模块5题、总计30题。自动公式回归：`python scripts/check_bulk_composite.py`；本批12题均为待独立专家审核，不能仅因 CI 通过改成已审。
