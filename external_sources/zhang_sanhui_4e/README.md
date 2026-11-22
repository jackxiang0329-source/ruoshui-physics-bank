# 张三慧《大学物理学（第4版）》三书习题逐页录入

**最新记录：2026-11-22。累计174道已录入候选习题，174份独立 LaTeX 解析，本轮新增62道与62解。**

GitHub工作分支：
`intake/zhang-sanhui-4e-20261122-batch01`  
审校入口：[Draft PR #45](https://github.com/jackxiang0329-source/ruoshui-physics-bank/pull/45)

这是与正式高难 `bank/` **严格隔离**的教材候选资料。
目前全部 `exam_ready=false`，尚未完成公开出版许可审查与独立专家逐题审核。

## 三份原始扫描参考

1. V1《大学物理学（第4版）力学、热学》，428 PDF物理页，第1—11章。
2. V2《大学物理学（第4版）电磁学、光学、量子物理》，515 PDF物理页，第12—30章。
3. S《大学物理学（第4版）学习辅导与习题解答》，402 PDF物理页，作为同号题目解答核对参照；不重复计数。

### 实际章末习题覆盖

| 教材章节 | 原始习题题号 | 题面 | 独立解析 | 题面源PDF物理页 |
| --- | --- | ---: | ---: | --- |
| 第1章 质点运动学 | 1.1—1.26 | 26 | 26 | V1 53—55 |
| 第2章 运动与力 | 2.1—2.28 | 28 | 28 | V1 82—87 |
| 第3章 动量与角动量 | 3.1—3.24 | 24 | 24 | V1 116—118 |
| **第4章 功和能** | **4.1—4.28** | **28** | **28** | **V1 151—155** |
| 第12章 静电场 | 12.1—12.34 | 34 | 34 | V2 41—44 |
| **第13章 电势** | **13.1—13.34** | **34** | **34** | **V2 61—64** |
| **累计** | **六章章末习题** | **174** | **174** | |

`chapters/NN/questions.tex` 与 `chapters/NN/solutions.tex`
为每章仅有的两份权威 TeX，禁止新增逐题冗余的 Markdown 或 JSON。
`source_register.json` 是所有稳定题号、教材PDF页码、
配套辅导书页码、风险和审查标记的唯一索引。

本批62题已定位到辅导书第4章与第13章，
但尚未核定每道题的精确PDF页码；
全部新增配套映射均明确标记 `pending_exact_page_verification`。
源PDF SHA-256和正式进度以索引及 [PROGRESS.md](PROGRESS.md) 为准。

## 质检与合订

- [结构和数值检查](qa_check.py)：唯一题号、题解配对、来源页合法性、78项独立数值抽检；
自动程序不能证明全体物理解答正确。
- [XeLaTeX 候选入口](build_intake.tex)：按原编号装订六章题目和解析，
使用 `ctexart`。
- [GitHub Actions 工作流](../../.github/workflows/zhang-sanhui-4e-intake.yml)：
远端运行结构检查、XeLaTeX 合订并上传校样。
- [完整质检与差异记录](PROGRESS.md)：
包括第4.8题原始“习题”与“思考题”误混修订、
原书表4.1能量标准、第13.27题经典半径的定义约定、
第3.14题辅导书打印高度与独立积分差异等。

从项目根运行：
```bash
python3 external_sources/zhang_sanhui_4e/qa_check.py
cd external_sources/zhang_sanhui_4e
xelatex -interaction=nonstopmode -halt-on-error build_intake.tex
xelatex -interaction=nonstopmode -halt-on-error build_intake.tex
```

任何未经真实运行的检查不得宣称通过；
自动检查通过与独立专业审稿、出版许可是三种不同的门槛。

## 后续严格接续

V1从**第5章习题5.1**开始；
V2从**第14章习题14.1**开始。
其余章节、各章思考题、配套辅导书的可能独立附加题、
逐题原图重绘、配套答案差异复核及正式出版许可仍未完成。
