# 外部物理习题资源区（独立候选，不属于正式题库）

## 教材解析专区合并入口（2026-11-24）

- [赵近芳、王登龙第五版两书：890题，39份合并LaTeX章节](../textbooks/zhao_wang/README.md)；[原文件映射](../textbooks/zhao_wang/chapters/compaction_map.md)。
- [Irodov《普通物理学习题》：1,878题，40份合并章节](../textbooks/irodov/README.md)；[原文件映射](../textbooks/irodov/chapters/compaction_map.md)。
- 两套教材仍是研究性解题稿，不计入452道正式高难综合题库；旧片段可由Git历史无损恢复。历史回归工作流只在临时工作区恢复旧文件名，不会新增仓库跟踪文件。



这里汇集待版权、题面、解答、去重及物理模型审核的外部材料；不自动进入 [正式高难综合题库](../bank/)，亦不计入《普通物理学习题》原书题号。外部内容即使技术校验通过，也不等于适合组卷。

## 整理后的入口

| 来源 | 数量 | 正文位置 | 索引 |
|---|---:|---|---|
| HF Physics DPO（生成文本，未核实） | 16,611 | [无损归档（归档）](../data/archives/library.zip) | [index.json（归档）（归档）](../data/archives/library.zip) |
| OpenStax College Physics | 2,526 | [无损归档（归档）](../data/archives/library.zip) | [index.json（归档）（归档）](../data/archives/library.zip) |
| Physics Refresher | 700 | [无损归档（归档）](../data/archives/library.zip) | [index.json（归档）（归档）](../data/archives/library.zip) |
| UBC OPBP（原题可依赖图片、许可注意 NC/SA） | 265 | [无损归档（归档）](../data/archives/library.zip) | [index.json（归档）（归档）](../data/archives/library.zip) |
| IntroPhysics（提取题干，学术/许可待审） | 53 | [无损归档（归档）](../data/archives/library.zip) | [index.json（归档）（归档）](../data/archives/library.zip) |
| WeBWorK OPL / Thermal | 59 + 21 | [OPL 无损 PG（归档）](../data/archives/library.zip) / [热学无损 PG（归档）](../data/archives/library.zip) | [OPL 索引（归档）（归档）](../data/archives/library.zip) / [热学索引（归档）（归档）](../data/archives/library.zip) |
| 赵近芳、王登龙第五版两书题解 | 累计771题（第15批新增73） | [独立 ElegantBook 项目](../textbooks/zhao_wang) | [勘误与复核](../textbooks/zhao_wang/quality_check.md) |
| 《普通物理学习题》中文 ElegantBook | 原书 1,878 题 | [独立正式教材整理工程](../textbooks/irodov) | [质检与勘误](../textbooks/irodov/errata.md) |

**三轮合计无损归档 20,235 份待审原文（19,837 + 318 + 80）。** 压缩包内保留每个 `ID.md` 或 `ID.pg` 文件的原文字节、来源说明与许可提示；校验清单分为 [第一轮（归档）](../data/archives/library.zip)、[第二轮（归档）](../data/archives/library.zip)、[第三轮（归档）](../data/archives/library.zip)。所有候选仅作为待审资源，不计入主库的正式题数。

要阅读或重新审核某来源的逐题 Markdown：

```bash
python3 scripts/compact_external_candidates.py --verify
python3 scripts/compact_external_candidates.py --restore college_physics
python3 scripts/compact_small_external_sources.py --verify
python3 scripts/compact_webwork_sources.py --verify
python3 scripts/compact_webwork_sources.py --restore webwork_opl
python3 scripts/compact_small_external_sources.py --restore intro_physics
```

UBC、IntroPhysics 和 WeBWorK 若需继续导入，先按需恢复相应原文，完成新增后重新打包并复验；不可把未归档的新原文静默追加到索引。恢复操作只在本地工作区按需展开，原目录下的来源索引和审核清单不会丢失。需要重新汇总审计或继续导入时，应先恢复对应原文；改变任何来源索引或原文后，须按 [归档说明](./_bundles/README.md) 重新打包并复验，避免产生索引/档案不一致。

其他导航：[总目录](./catalog_index.md) · [中文分类](./catalog/中文分类导航.md) · [待审队列（归档）（归档）](../data/archives/library.zip)。**版权和学术校核状态不因归档而改变**，尤其要注意 NC/SA 对商业用途及改编再分发的限制。
