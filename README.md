# 三千弱水 · 大学物理题库

**高难综合题 / 原版书习题 / 严格质检 / LaTeX + PDF**  
本仓库已经整理为**正式题库优先、教材译解独立、未审外部材料归档**的布局；优先从下方入口访问，避免在几万个零散候选文件中查找。

## 快速入口

| 我要查看 | GitHub 路径 | 内容与状态 |
|---|---|---|
| **正式高难综合题** | [`bank/`](bank/) | **452 道**，每道含 `meta.json`、`question.tex`、`solution.tex` 三份权威源 |
| 题目与解析的合订 LaTeX | [题目](tex/questions.tex) / [解答](tex/solutions.tex) | 从 `bank/` 构建；数学公式统一按 LaTeX 排版 |
| 查询题号、模块、质量信息 | [CSV 题目索引](data/index.csv) / [JSON 目录](data/problems.json) | 自动派生数据，不是新的独立题源 |
| **赵近芳、王登龙第五版两书习题** | [ElegantBook 教材专区](external_sources/zhao-wang-physics-5e-elegant/) | **累计500题（第10批新增69）**，覆盖《简明教程》第1—10章和《学习指导》第1—10章部分例题；保留疑点标记，不计入正式高难题库 |
| **《普通物理学习题》中文整理** | [Irodov ElegantBook 专区](external_sources/irodov-zh-elegant/) | **原书 1,878 题**，分篇章节、中文推导、勘误与独立回归 |
| 《普通物理学习题》合订 PDF | [直接查看 `main.pdf`](external_sources/irodov-zh-elegant/main.pdf) | 已编译的仓库内成品 |
| **张三慧《大学物理学（第4版）》三书** | [进行中的 Draft PR #45](https://github.com/jackxiang0329-source/ruoshui-physics-bank/pull/45) | 分支持续录入与质检；未合并前不计入正式主库 |
| **未审外部候选资源** | [分类导航](external_sources/catalog/中文分类导航.md) / [无损压缩归档](external_sources/_bundles/) | 19,837 份大型候选、318 份 UBC/IntroPhysics 及 80 份 WeBWorK PG 源程序无损打包；不进入正式题库 |
| 技术质检与历史批次 | [QA 协议](docs/policies/qa_protocol.md) / [高难准入标准](docs/policies/high_difficulty_policy.md) / [历史记录](docs/history/project_history_2026.md) | 技术检查不等于第三方学术审定 |

其他辅助技术文档统一按用途归类：[文档目录](docs/README.md) · [命名规范](docs/policies/repository_naming.md)。

## 精简后的顶层结构

仓库根目录只保留 **8 个功能目录**；旧顶层的 `localization/`、`localized/`、`taxonomy/`、`qa/` 已统一迁入 [数据目录 `data/`](data/README.md)，其中中文主档、合订译稿、分类规则和质检凭证仍各自独立管理。题库编号、原始内容与审核状态不变。

## 目录结构（保留稳定接口）

```text
ruoshui-physics-bank/
├── bank/                 452 道正式高难综合题；每题 3 份源文件
├── tex/                  正式题目与解答的合订 LaTeX
├── data/                 正式索引、翻译稿、分类规则、质检凭证与批次报告
├── external_sources/
│   ├── irodov-zh-elegant/  《普通物理学习题》1,878题，合订 PDF
│   ├── _bundles/          7份无损候选压缩包+三份SHA-256清单
│   ├── catalog/           分类、去重与候选待审表
│   └── ...                其他待审来源索引与少量原题
├── scripts/              校验、组卷、构建、压缩包还原
├── tests/                自动测试
├── docs/                 工作流说明、规范、历史与勘误入口
└── .github/workflows/    CI、PDF构建和一次性无损整理
```

## 维护原则

**唯一权威源：** 正式高难综合题只修改 `bank/题号/{meta.json,question.tex,solution.tex}`；`data/problems.json`、`data/index.csv`、`tex/*.tex` 属于派生合订或索引，不应另行复制成第二套题库。《普通物理学习题》保留独立的 ElegantBook 章节和回归系统；未通过版权、答案和物理审核的外部候选不直接进入正式题库。

**真正减少文件数：** 2026-11-22 将 16,611 + 2,526 + 700 = **19,837** 份零散未审 Markdown 原文精确字节归档为三个 `tar.gz`，保留索引和双层 SHA-256 校验清单；文件总数由 **22,088** 降为 **2,258**（整理提交后的实际仓库树；后续新增文档会使该数字略增）。原文可恢复，**没有删题、删解析或修改正式题解**。见 [归档说明](external_sources/_bundles/README.md)。

```bash
# 需要审查外部原文时校验或按数据源还原（仅在需要时）
python3 scripts/compact_external_candidates.py --verify
python3 scripts/compact_external_candidates.py --restore college_physics
python3 scripts/compact_small_external_sources.py --verify
python3 scripts/compact_webwork_sources.py --verify
python3 scripts/compact_small_external_sources.py --restore ubc_opbp

# 核对正式题库源文件和生成文件一致性
python3 scripts/build.py --check
```

**第二轮与第三轮无损归档：** UBC 的 265 份与 IntroPhysics 的 53 份未审单题 Markdown 另打包为 2 个可逆归档；正式 452 题、Irodov、WeBWorK PG 程序原始字节也无损归档，张三慧 Draft PR 不变。当前活跃分支的精确文件数以 GitHub 文件树为准；二轮详情见 [归档索引](external_sources/_bundles/compaction_round_02.md)。

**质量声明：** 自动化测试与 PDF 编译只能证明相应结构、公式和计算模型的程序化检查通过；所有标记“待独立复核”的题目仍需专业人士独立审稿。外部来源的归档不会改变其版权、正确性或学术审核状态。

[历史扩库与各批次完整记录](docs/history/project_history_2026.md) · [外部资料使用说明](external_sources/README.md) · [GitHub Actions](https://github.com/jackxiang0329-source/ruoshui-physics-bank/actions)
