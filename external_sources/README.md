# 外部物理习题资源区（独立候选，不属于正式题库）

这里汇集待版权、题面、解答、去重及物理模型审核的外部材料；不自动进入 [正式高难综合题库](../bank/)，亦不计入《普通物理学习题》原书题号。外部内容即使技术校验通过，也不等于适合组卷。

## 整理后的入口

| 来源 | 数量 | 正文位置 | 索引 |
|---|---:|---|---|
| HF Physics DPO（生成文本，未核实） | 16,611 | [无损归档](./_bundles/hf_physics_dpo-raw.tar.gz) | [index.json](./hf_physics_dpo/index.json) |
| OpenStax College Physics | 2,526 | [无损归档](./_bundles/college_physics-raw.tar.gz) | [index.json](./college_physics/index.json) |
| Physics Refresher | 700 | [无损归档](./_bundles/physics_refresher-raw.tar.gz) | [index.json](./physics_refresher/index.json) |
| UBC OPBP（原题可依赖图片、许可注意 NC/SA） | 265 | [raw/](./ubc_opbp/raw/) | [index.json](./ubc_opbp/index.json) |
| WeBWorK OPL / Thermal | 59 + 21 | [OPL](./webwork_opl/raw/) / [Thermal](./webwork_thermal/raw/) | 各自的 index.json |
| 《普通物理学习题》中文 ElegantBook | 原书 1,878 题 | [独立正式教材整理工程](./irodov-zh-elegant/) | [质检与勘误](./irodov-zh-elegant/errata.md) |

**已无损归档 19,837 份零散候选文件。** 压缩包内保留每个 `ID.md` 文件的原文字节、来源说明与许可提示；校验清单在 [`_bundles/manifest.json`](./_bundles/manifest.json)。这三份大型候选语料均只作为待审资源，不计入主库的正式题数。

要阅读或重新审核某来源的逐题 Markdown：

```bash
python3 scripts/compact_external_candidates.py --verify
python3 scripts/compact_external_candidates.py --restore college_physics
```

恢复操作只在本地工作区按需展开，原目录下的来源索引和审核清单不会丢失。需要重新汇总审计或继续导入时，应先恢复对应原文；改变任何来源索引或原文后，须按 [归档说明](./_bundles/README.md) 重新打包并复验，避免产生索引/档案不一致。

其他导航：[总目录](./CATALOG.md) · [中文分类](./catalog/中文分类导航.md) · [待审队列](./curation_queue.csv)。**版权和学术校核状态不因归档而改变**，尤其要注意 NC/SA 对商业用途及改编再分发的限制。
