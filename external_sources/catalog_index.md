# 大学物理外部题源 · 分类总索引

请先看 [外部来源说明](README.md)；本页仅清点**候选原始资料**，不把候选文件、教材题号或机器 QA 等同于可以正式组卷的试题。

| 来源类型 | 记录数量 | 存储方式 | 访问与限制 |
|---|---:|---|---|
| HF Physics DPO 合成候选 | 16,611 | [原始字节压缩包（归档）](../data/archives/library.zip) | 模型生成候选，答案和许可待核 |
| OpenStax College Physics | 2,526 | [原始字节压缩包（归档）](../data/archives/library.zip) | CC 条款/第三方权利待审 |
| Physics Refresher | 700 | [原始字节压缩包（归档）](../data/archives/library.zip) | 教学候选，待审 |
| UBC Open Physics Bank | 265 | [原始字节压缩包（归档）](../data/archives/library.zip) | 原图依赖及 CC BY / NC / SA 逐题复核 |
| IntroPhysics | 53 | [原始字节压缩包（归档）](../data/archives/library.zip) | 教学材料题干，待审 |
| WeBWorK 大学物理 | 59 | [原始 PG 压缩包（归档）](../data/archives/library.zip) | .pg 需要 WeBWorK 引擎与宏、版权需审 |
| WeBWorK 热学 | 21 | [原始 PG 压缩包（归档）](../data/archives/library.zip) | 同上 |
| **未审资料合计** | **20,235** | **7 个可恢复归档** | **不是正式题数** |

外部索引仍在各来源 `index.json`；来源文件的引用、作者、许可、原始版本信息保留在索引或归档成员中。所有归档通过哈希清单校验：`_bundles/manifest.json`（19,837），`_bundles/small_sources_manifest.json`（318），`_bundles/webwork_sources_manifest.json`（80）。后续需要逐题程序运行时，可先按 `_bundles/README.md` 的指令恢复 `raw/`。

## 与正式题库严格区分

- 正式高难综合题：[`../bank/`](../bank/) 内的 452 道唯一权威 TeX/元数据。
- Irodov《普通物理学习题》中文教材整理：[`irodov-zh-elegant/`](irodov-zh-elegant/) 独立的 1,878 道原书题号及编译工程。
- 张三慧三册习题：仍在 [Draft PR #45](https://github.com/jackxiang0329-source/ruoshui-physics-bank/pull/45)，不可当作正式主库。
- 外部候选完整分类：[中文分类导航](catalog/中文分类导航.md)、[待审清单（归档）（归档）](../data/archives/library.zip)。
- 文件/文件夹命名与技术文档：[仓库规范](../docs/policies/repository_naming.md)。

各来源数量是当前索引条目数；上游文件量、授权和审核状态可能变化。没有人工逐题确认前，不能自动改变 `exam_ready`。
