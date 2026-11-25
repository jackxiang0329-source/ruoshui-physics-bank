# 三千弱水 · 大学物理题库

**高难综合题 / 原版书习题 / 严格质检 / LaTeX + PDF**  
本仓库已经整理为**正式题库优先、教材译解独立、未审外部材料归档**的布局；优先从下方入口访问，避免在几万个零散候选文件中查找。

## 2026-11-24 全仓库文件精简合并

本轮按原有功能和题库数据模型检查全仓库，采用**原文无损合并、目录结构稳定、Git历史可恢复、自动测试验证**的方式精简。

| 范围 | 合并前 | 合并后 | 减少 |
|---|---:|---:|---:|
| 《大学物理简明教程》及《大学物理学学习指导》LaTeX章节片段 | 102份 | **39份** | 63份 |
| Irodov《普通物理学习题》LaTeX章节片段 | 164份 | **40份** | 124份 |
| 全仓库Git跟踪文件（包括补充的映射、兼容脚本等） | **1,988** | **1,805** | **183份** |

保留原有 **8个顶层功能目录** 与各题独立来源：正式高难题库452题的`bank/ID/{meta.json,question.tex,solution.tex}`、两书890题、Irodov 1,878题、候选归档及现有索引均不减少。Git目前仍有501个目录节点，其中大部分是正式题库按题号组织的452个目录；为避免破坏组卷、引用、逐题编辑与质检接口，这些**必要目录不强行压成一个巨型文件**。

教材分段源文件的完整旧文本及Git blob SHA保存在新章节注释中，同时提供 [两书对照表](external_sources/zhao-wang-physics-5e-elegant/chapters/COMPACTION-MAP.md) 和 [Irodov对照表](external_sources/irodov-zh-elegant/chapters/COMPACTION-MAP.md)。Irodov历史质检通过 [校验后临时恢复](external_sources/irodov-zh-elegant/expand_legacy_fragments.py) 继续兼容，无需在仓库重新跟踪旧文件。

已通过 [两书校验及XeLaTeX构建](https://github.com/jackxiang0329-source/ruoshui-physics-bank/actions/runs/45214069462) 与 [Irodov完整专项质检及PDF构建](https://github.com/jackxiang0329-source/ruoshui-physics-bank/actions/runs/45216150513)。技术检查成功不代表逐题独立学术终审。

## 2026-11-25 继续精简

- [赵王两书八批逐题质检合订](external_sources/zhao-wang-physics-5e-elegant/qa-eight-rounds-summary.md)：八份账本原文集中在既有汇总页，保留批次锚点与 Git 原件链接。
- [历史导入日志归档](external_sources/logs/history_2026_10.json)：五份 10 月 26—28 日的 JSONL 原文完整收入一份 JSON，附原路径、Git blob SHA、字节数和提交号；现行 latest 报告和按日写入接口保留。
- 正式题号、题面、解析、教材 TeX、PDF、索引、脚本和 CI 不因本次历史文档整理而改变。技术执行结果以 Actions 为准。

## 正式题库六学科集中存储（迁移版）

`bank/M.json`、`E.json`、`T.json`、`W.json`、`O.json`、`Q.json` 分别保存力学、电磁学、热学、振动与波动、光学、近代物理的权威源码。每个原始文件保留 UTF-8 原文、字节数、Git blob SHA；题号和质检状态不变。历史独立题号路径按需恢复，不再提交数百个目录。

```bash
python3 scripts/compact_bank.py --verify
python3 scripts/compact_bank.py --restore
python3 scripts/build.py --check
# 编辑或新增已恢复的题号文件并完成原有质检、索引及合订同步后：
python3 scripts/compact_bank.py --pack
git add bank/*.json data/ tex/
```

恢复程序拒绝覆盖未归档的修改；重新打包前须保留全部原题号。GitHub CI 自动恢复原路径后再运行现有检查和编译。以下旧历史统计仅作历史参考。

## 2026-11-25 辅助资源集中归档

- [外部分类视图](data/archives/catalog_views.zip)：44份按学科/知识点生成的CSV，完整索引继续直接访问。
- [历史批次质检](data/archives/round_qa.zip)：43份历史脚本及报告（第12—13轮报告与第13轮以前相关检查）。
- [Irodov专项回归](data/archives/irodov_regressions.zip)：48份专项回归脚本及共享模块。现有章节TeX、PDF和检查入口仍保留。

归档成员保留原路径、字节数、SHA-256、Git blob SHA。CI自动验证并恢复；手动执行原有脚本之前运行：

```bash
python3 scripts/compact_auxiliary.py --verify
python3 scripts/compact_auxiliary.py --restore
# 编辑已恢复的历史脚本或重新生成分类视图后：
python3 scripts/compact_auxiliary.py --pack --group catalog_views
git add data/archives/catalog_views.zip
```

其他组可按需指定 `round_qa` 或 `irodov_regressions`；恢复目录不直接提交。归档不改变审核等级、原始题号及原始资料。

## 教材章节、测试及大索引进一步无损精简

- [Irodov 40章](data/archives/irodov_chapters.zip)、[赵王两书39章](data/archives/zhao_wang_chapters.zip)、[三校45章](data/archives/three_college_chapters.zip)：全部原始 TeX 章节保留原路径和 SHA-256。
- [自动测试20份](data/archives/test_suite.zip)：原有测试用例完整归档。
- [大型索引5份](data/archives/large_indexes.zip)：保留源索引、待审队列和审计表的原始字节。全量分类总索引 CSV、教材主 TeX、PDF、封面、勘误和各教材导航仍可直接阅读。

从仓库根目录运行 `python3 scripts/compact_auxiliary.py --verify` 或 `--restore`；也可用 `--restore --group irodov_chapters` 等按需恢复。修改已恢复文件后 `--pack --group GROUP` 并提交对应 ZIP，不重新跟踪旧成员。新增章节或测试文件先用 `git add -f 原文件路径` 暂存，再打包，然后用 `git rm --cached 原文件路径` 取消成员跟踪。CI 与各教材 build.sh 自动恢复其必要章节，完整保留原有编译入口。

## 维护资料与历史资源集中管理

本轮对97份辅助文件进行无损归档，保留核心正式题库、教材主TeX/PDF、当前质量政策和组卷入口。

| 归档 | 作用 |
|---|---|
| [reference_docs.zip](data/archives/reference_docs.zip) | 21份原操作说明、历史记录、审校报告及书目 |
| [source_tools.zip](data/archives/source_tools.zip) | 20份外部采集、分类、翻译及审计工具 |
| [round14_qa.zip](data/archives/round14_qa.zip) | 17份第14轮专项脚本和原报告 |
| [source_metadata.zip](data/archives/source_metadata.zip) | 15份小型来源元数据、说明及原文 |
| [catalog_working.zip](data/archives/catalog_working.zip) | 14份待审中间目录、审计及组卷预览 |
| [retired_migrations.zip](data/archives/retired_migrations.zip) | 3份已完成的一次性迁移工作流定义，仅供追溯 |
| [source_logs.zip](data/archives/source_logs.zip) | 7份历史及分来源采集日志 |

维护前从仓库根目录执行 `python3 scripts/compact_auxiliary.py --restore`，然后 `python3 scripts/compact_bank.py --restore`；也可按组恢复。归档后编辑原路径必须按组重新打包并提交 ZIP。当前分类总索引、最新总日志及质量政策仍可直接查看。已完成的一次性工作流不再作为主分支的活跃工作流，历史运行和原定义仍可追溯。

## 快速入口

| 我要查看 | GitHub 路径 | 内容与状态 |
|---|---|---|
| **正式高难综合题** | [`bank/`](bank/) | **452 道**，六学科归档中保留每题三份原始源码 |
| 题目与解析的合订 LaTeX | [题目](tex/questions.tex) / [解答](tex/solutions.tex) | 从 `bank/` 构建；数学公式统一按 LaTeX 排版 |
| 查询题号、模块、质量信息 | [CSV 题目索引](data/index.csv) / [JSON 目录](data/problems.json) | 自动派生数据，不是新的独立题源 |
| **赵近芳、王登龙第五版两书习题** | [ElegantBook 教材专区](external_sources/zhao-wang-physics-5e-elegant/) | **累计890题（第18—19批新增44）**，覆盖《简明教程》第1—12章、《学习指导》第1—16章解题示例及自测题1—11；保留疑点标记，不计入正式高难题库 |
| **《普通物理学习题》中文整理** | [Irodov ElegantBook 专区](external_sources/irodov-zh-elegant/) | **原书 1,878 题**，分篇章节、中文推导、勘误与独立回归 |
| 《普通物理学习题》合订 PDF | [直接查看 `main.pdf`](external_sources/irodov-zh-elegant/main.pdf) | 已编译的仓库内成品 |
| **张三慧《大学物理学（第4版）》三书** | [进行中的 Draft PR #45](https://github.com/jackxiang0329-source/ruoshui-physics-bank/pull/45) | 分支持续录入与质检；未合并前不计入正式主库 |
| **三校大学物理习题详解** | [ElegantBook 教材专区](external_sources/three-college-physics-elegant/) | 累计1,598个题号，三书章末习题均已覆盖至末题；历史二轮覆盖记录509个（含疑点及19项原页待补验），另有184项源码数学复算；第53批全部45个引用章节1598题结构检查无异常；尚余1,089个待二轮原页覆盖；部分解析、历史疑点及全量学术终审待完成 |
| **未审外部候选资源** | [分类导航](external_sources/catalog/中文分类导航.md) / [无损压缩归档](external_sources/_bundles/) | 19,837 份大型候选、318 份 UBC/IntroPhysics 及 80 份 WeBWorK PG 源程序无损打包；不进入正式题库 |
| 技术质检与历史批次 | [QA 协议](docs/policies/qa_protocol.md) / [高难准入标准](docs/policies/high_difficulty_policy.md) / [历史记录](docs/history/project_history_2026.md) | 技术检查不等于第三方学术审定 |

其他辅助技术文档统一按用途归类：[文档目录](docs/README.md) · [命名规范](docs/policies/repository_naming.md)。

## 精简后的顶层结构

仓库根目录只保留 **8 个功能目录**；旧顶层的 `localization/`、`localized/`、`taxonomy/`、`qa/` 已统一迁入 [数据目录 `data/`](data/README.md)，其中中文主档、合订译稿、分类规则和质检凭证仍各自独立管理。题库编号、原始内容与审核状态不变。

## 目录结构（保留稳定接口）

```text
ruoshui-physics-bank/
├── bank/                 452 道正式高难综合题；6 份可逆学科归档
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

**唯一权威源：** 正式高难综合题以六个 `bank/*.json` 归档为提交源；恢复后编辑 `bank/题号/{meta.json,question.tex,solution.tex}` 并重新打包；`data/problems.json`、`data/index.csv`、`tex/*.tex` 属于派生合订或索引，不应另行复制成第二套题库。《普通物理学习题》保留独立的 ElegantBook 章节和回归系统；未通过版权、答案和物理审核的外部候选不直接进入正式题库。

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
