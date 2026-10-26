# 三千弱水 · 大学物理原创试题库

> **总目标：10,000 道原创大学物理题。当前版本：36 道独立编写的六模块样板题（待独立专家审核）。**
>
> 仓库：`jackxiang0329-source/ruoshui-university-physics`。

## 当前进度

| 模块 | 数量 | 状态 |
|---|---:|---|
| 力学 | 6 | 待专家审核 |
| 电磁学 | 6 | 待专家审核 |
| 热学 | 6 | 待专家审核 |
| 振动与波动 | 6 | 待专家审核 |
| 光学 | 6 | 待专家审核 |
| 近代物理 | 6 | 待专家审核 |
| **总计** | **36 / 10,000** | **样板阶段** |

本仓库不将结构校验、符号计算或 PDF 编译成功等同于六轮质检完成。后续按100题一批扩展；首批100题尚差64题。

## 文件组织

- `data/problems.json`：唯一题目数据源，包含题干、完整解答、答案、难度、质检状态。
- `data/index.csv`：题目索引。
- `data/qa_report.json`：结构检查与编译状态。
- `data/qa_physics_spotchecks.json`：针对示例答案的自动符号/数值检查结果。
- `tex/questions.tex`、`tex/solutions.tex`：可编辑 XeLaTeX 文件。
- `pdf/questions.pdf`、`pdf/solutions.pdf`：现有可阅读 PDF。
- `scripts/build.py`：从 JSON 生成 TeX、CSV 和报告；可选编译 PDF。
- `scripts/check_physics.py`：对36题的部分关键公式做独立于题解文字的符号和数值一致性核算。
- `scripts/assemble_exam.py`：按难度、模块、题数与随机种子生成组卷题目/答案TeX与JSON索引；默认只允许已审核题目。
- `docs/REFERENCES.md`：教材书目参考与核验边界。
- `docs/QA_PROTOCOL.md`：六轮审核流程、未通过项目与使用限制。
- `.github/workflows/physics-ci.yml`：GitHub Actions 自动生成、自动检查与编译。
- `publish.ps1`（Windows） / `publish.sh`（macOS、Linux）：通过 GitHub CLI 建立**新仓库**并推送。

## 本地编译

依赖 Python 3.9+；物理符号检查需安装 `sympy`；编译 PDF 需 TeX Live（`ctex`、XeLaTeX、`latexmk`）。

```bash
python -m pip install -r requirements.txt
python scripts/check_physics.py
python scripts/build.py --compile
```

如果只生成源文件及索引：

```bash
python scripts/build.py
```

## 按约束组卷（样板题需显式允许）

```bash
python scripts/assemble_exam.py --count 8 --seed 20261026 --allow-pending
```

默认过滤掉尚未通过独立审核的题目，因此本批样板题只有使用 `--allow-pending` 才能组卷。

## GitHub 仓库说明

仓库已经由用户创建。如需在本地克隆和推送，可使用 [GitHub CLI](https://cli.github.com/) 登录：

```bash
gh auth login
```

Windows PowerShell 在解压目录执行：

```powershell
.\publish.ps1
```

macOS/Linux：

```bash
bash publish.sh
```

原建仓脚本供需要重建的环境参考；**目标仓库已存在时不会覆盖**。建议日常维护使用正常的 Git clone/pull/commit/push 流程。

## 内容来源与知识产权

本批独立设题，不转录教材试题或整段原文；十册书目核查与课程章节体系参考见 `docs/REFERENCES.md`。本项目目前**未阅读十册教材全文，也未对全书做逐题比对**，因此不承诺“与全部教材零重复”。知识点覆盖和命题风格参考公开课程范围，不能视为已经统计分析国内主流高校真实期末试卷。

## 后续路线

1. 继续完成首批100道高质量样板、增加综合与实验相关试题。
2. 建立独立复核凭证、相似度筛查、量纲与极限测试，落实六轮审核。
3. 再按批次扩展至1,000题和10,000题，并加入题型配比/难度/考试时间约束的组卷模块。

未完成独立学术审核的题目不得宣称为考试可直接使用的正式题库。
