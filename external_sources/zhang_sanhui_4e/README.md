# 张三慧《大学物理学》第4版 · 三书习题候选录入区

**项目状态：** 2026-11-22，工作分支 `intake/zhang-sanhui-4e-20261122-batch01`，
[Draft PR #45](https://github.com/jackxiang0329-source/ruoshui-physics-bank/pull/45)。
这是教材扫描的用户授权校对环境中的待审候选资料，**不是**正式高难题库 `bank/`。

## 三份原始扫描

- 《大学物理学（第4版）力学、热学》：V1，PDF 428页，第1—11章。
- 《大学物理学（第4版）电磁学、光学、量子物理》：V2，PDF 515页，第12—30章。
- 《大学物理学（第4版）学习辅导与习题解答》：S，PDF 402页，题号关联的核对参照，不重复收录同一道题。

来源 PDF 的准确文件名、SHA-256、各题原书章节、教材PDF物理页和辅导PDF物理页在
[source_register.json](source_register.json)；不在 GitHub 重新散存整本扫描PDF。

## 已落库内容

| 模块 | 章节 | 编号 | 题面/解析数 | 进度 |
| --- | --- | --- | ---: | --- |
| V1 力学 | 第1章 质点运动学 | 1.1—1.26 | 26/26 | 章末习题转写覆盖，图示和外审未通过 |
| V1 力学 | 第2章 运动与力 | 2.1—2.12 | 12/12 | 部分录入 |
| V2 电磁学 | 第12章 静电场 | 12.1—12.3 | 3/3 | 部分录入 |

**累计41道候选习题、41份独立解析；本轮新增28道及28份解析。**
同编号辅导题只关联解答，不重复计入。全书余下习题尚未逐页清点，不能宣称全部完成。

## 合订式唯一数据源

- `chapters/NN/questions.tex`：一章一份原题编号的候选习题 LaTeX。
- `chapters/NN/solutions.tex`：一章一份独立推导的 LaTeX。
- `source_register.json`：所有已录题的唯一结构化索引及状态。
- `PROGRESS.md`：当前批次与审校风险、下次接续题号。
- `build_intake.tex`：独立于正式题库的整套候选 XeLaTeX 校样入口。
- `qa_check.py`：登记与 TeX 对齐、来源页和数值模型抽检脚本。

所有公式用标准 LaTeX；不得因补录教材候选改变 `bank/` 高难度准入门槛。
原题图、符号、方向、多个有效解和辅导书可能的错误均保留复核证据。
脚本或 GitHub Actions 成功不等于独立学术复核，也不意味着版权许可已验证；
全部 `exam_ready=false`。

## 检查与编译

```bash
python3 external_sources/zhang_sanhui_4e/qa_check.py
cd external_sources/zhang_sanhui_4e
xelatex -interaction=nonstopmode -halt-on-error build_intake.tex
xelatex -interaction=nonstopmode -halt-on-error build_intake.tex
```

GitHub Actions 候选CI见
[`.github/workflows/zhang-sanhui-4e-intake.yml`](../../.github/workflows/zhang-sanhui-4e-intake.yml)。
**实际通过情况必须查工作流运行记录，不得仅凭存在脚本宣称编译通过。**

## 下一步

第2章习题 **2.13起**（V1 PDF物理页85附近）；
第12章习题 **12.4起**（V2 PDF物理页41附近）。
其余第3—11章、第13—30章和各章思考题都需继续扫描、录入及严格审核。
具体见 [进度台账](PROGRESS.md)。
