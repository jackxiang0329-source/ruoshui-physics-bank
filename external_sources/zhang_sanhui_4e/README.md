# 张三慧《大学物理学》第4版：三书习题候选录入区

**当前状态：2026-11-22，共112道题面及112份独立解析，最新一轮新增55道和55份解析。**
工作分支 `intake/zhang-sanhui-4e-20261122-batch01`，
[Draft PR #45](https://github.com/jackxiang0329-source/ruoshui-physics-bank/pull/45)。

> **隔离说明：** 候选原题与答案不属于正式高难度综合题库 `bank/`，不能因此获得考试组卷权限。外部教材出版许可和独立学术专家审核仍待完成，全部 `exam_ready=false`。

## 三份已提供的扫描教材

- V1《大学物理学（第4版）力学、热学》：428页，对应第1—11章。
- V2《大学物理学（第4版）电磁学、光学、量子物理》：515页，对应第12—30章。
- S《大学物理学（第4版）学习辅导与习题解答》：402页，供题号关联与解答交叉核验，同一道题绝不重复计数。

三本书 PDF 的文件名、SHA-256 与当前已录习题对应的源页码，统一见 [source_register.json](source_register.json)。
本轮55道新题已按原编号定位配套辅导书的PDF物理页（第3章48–57页、第12章191–202页）；题解差异核对尚未全部通过独立专家审校。

## 唯一可编辑题稿结构

| 章节 | 原书章末习题号 | 已录题目 | 独立解析 |
| --- | --- | ---: | ---: |
| [第1章](chapters/01/questions.tex) 质点运动学 | 1.1–1.26 | 26 | 26 |
| [第2章](chapters/02/questions.tex) 运动与力 | 2.1–2.28 | 28 | 28 |
| [第3章](chapters/03/questions.tex) 动量与角动量 | 3.1–3.24 | 24 | 24 |
| [第12章](chapters/12/questions.tex) 静电场 | 12.1–12.34 | 34 | 34 |
| **累计** | **四章章末题号已覆盖** | **112** | **112** |

每章仅有 `chapters/NN/questions.tex` 和 `chapters/NN/solutions.tex` 两份权威 TeX，
不生成逐题冗余源文件。每条题号、原书PDF页、答案状态、原图依赖、复核状态记录于唯一的 `source_register.json`。

- [PROGRESS.md](PROGRESS.md) — 完成量、原书题号、具体错误与下一轮接续。
- [qa_check.py](qa_check.py) — 编号、配对、来源页合法性与46项数值抽检（包括第3.14题的独立数值积分）（不等于专家审核）。
- [build_intake.tex](build_intake.tex) — 独立于正式高难题库的 XeLaTeX 候选校样合订入口。
- [CI 工作流](../../.github/workflows/zhang-sanhui-4e-intake.yml) — GitHub Actions 上运行结构 QA、XeLaTeX 生成候选 PDF，具体通过情况需看运行日志。

## 后续接续

V1 从 **第4章习题4.1**；V2 从 **第13章习题13.1**。
两卷未录的第4—11章、第13—30章及各章思考题仍待逐页整理。
题目转写覆盖、公式可编译、物理模型复核、版权许可审查是独立的进度指标；
任何一个不能替代另外三个。

```bash
python3 external_sources/zhang_sanhui_4e/qa_check.py
cd external_sources/zhang_sanhui_4e
xelatex -interaction=nonstopmode -halt-on-error build_intake.tex
xelatex -interaction=nonstopmode -halt-on-error build_intake.tex
```
