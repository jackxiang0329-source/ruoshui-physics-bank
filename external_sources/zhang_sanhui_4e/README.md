# 张三慧《大学物理学（第4版）》三书习题候选录入

最新日期：**2026-11-22**。当前累计**216道候选题面、216份独立LaTeX解析**。
本轮自174题基础上新增**42题+42解**，均已推送原分支。
[Draft PR #45](https://github.com/jackxiang0329-source/ruoshui-physics-bank/pull/45)
· `intake/zhang-sanhui-4e-20261122-batch01`

**警示：** 本目录的教材扫描转写和解析是待审候选资料，
`exam_ready=false`，不进入正式高难 `bank/` 或自动组卷；
未完成独立物理专家审校、图片重绘及版权许可审查。
不能把“题号已录入”称为“全部质检完成”。

## 三本扫描来源

- V1：《大学物理学（第4版）力学、热学》，428 PDF物理页，对应第1—11章。
- V2：《大学物理学（第4版）电磁学、光学、量子物理》，515 PDF物理页，对应第12—30章。
- S：《大学物理学（第4版）学习辅导与习题解答》，402 PDF物理页，
  用于同一原书题号的解析与数据核对，不重复计数。

## 真实覆盖

| 章 | 原书章末题号 | 题面 | 独立解答 | 原教材扫描页 |
|---|---|---:|---:|---|
| 1 质点运动学 | 1.1—1.26 | 26 | 26 | V1 53—55 |
| 2 运动与力 | 2.1—2.28 | 28 | 28 | V1 82—87 |
| 3 动量与角动量 | 3.1—3.24 | 24 | 24 | V1 116—118 |
| 4 功和能 | 4.1—4.28 | 28 | 28 | V1 151—155 |
| **5 刚体的转动** | **5.1—5.28** | **28** | **28** | **V1 185—189** |
| 12 静电场 | 12.1—12.34 | 34 | 34 | V2 41—44 |
| 13 电势 | 13.1—13.34 | 34 | 34 | V2 61—64 |
| **14 静电场中的导体** | **14.1—14.14** | **14** | **14** | **V2 74—75** |
| **总计** | **8章** | **216** | **216** | |

## 权威文件（避免分散）

- 每章仅一对 `chapters/NN/questions.tex` 和 `chapters/NN/solutions.tex`；
  当前8章16份权威LaTeX。
- `source_register.json`：稳定题号、原始扫描页、辅导书页及
  `exam_ready=false` 和风险清单。本轮42题已有20题精确对应配套书页码，
  22题保持待查空值，绝不估填。
- [PROGRESS.md](PROGRESS.md)：逐题疑点、补录统计、下一接续点。
- [qa_check.py](qa_check.py)：编号配对、去重和**101项独立数值模型抽检**；
  特别锁定5.5键角、5.6直径原值、5.22能源单位、14.8绝缘传送带。
- [build_intake.tex](build_intake.tex)：八章全部题解的XeLaTeX候选合订入口。
- [GitHub Actions工作流](../../.github/workflows/zhang-sanhui-4e-intake.yml)：
  运行程序检查及XeLaTeX候选校样，实际通过情况依远端日志判断。

```bash
python3 external_sources/zhang_sanhui_4e/qa_check.py
cd external_sources/zhang_sanhui_4e
xelatex -interaction=nonstopmode -halt-on-error build_intake.tex
xelatex -interaction=nonstopmode -halt-on-error build_intake.tex
```

本轮重要源书差异：5.6两册都印了不合常见分子尺度的71 nm，
但给定自转能量6.21与6.12×10⁻²¹ J有异；
5.22辅导书2004电量比较单位疑误；
14.8使用绝缘带 (E=\sigma/(2\varepsilon_0))，
14.13辅导书1g水滴和电势量级存在分歧。
具体保留原式和独立计算于[进度报告](PROGRESS.md)及章节解析。

下一轮接续：**V1第6章习题6.1，V2第15章习题15.1**。
第6—11章、第15—30章及各章思考题、补充题尚待录入。
