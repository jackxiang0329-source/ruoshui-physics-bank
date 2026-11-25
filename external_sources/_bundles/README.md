# 外部候选习题无损归档（不进入正式题库）

此目录用于减少 GitHub 主分支中的零散文件数量。第一轮无损归档以下三类**未审核、不得直接组卷**的单题 Markdown；其题号索引、许可证与溯源信息仍在原目录的 `index.json`、`source_manifest.json` 或 `manifest.json`。

| 数据集 | 单题 Markdown 数量 | 完整原文字节归档 |
|---|---:|---|
| HF Physics DPO | 16,611 | `hf_physics_dpo-raw.tar.gz` |
| College Physics | 2,526 | `college_physics-raw.tar.gz` |
| Physics Refresher | 700 | `physics_refresher-raw.tar.gz` |
| **合计** | **19,837** | 仅 3 个压缩包 + 1 个完整性清单 |

原始文件**并非删除题目内容**，而是转为每文件可逆的 `tar.gz`，其中仍以原 `ID.md` 路径保存每一个文件的原始 UTF-8 字节；`manifest.json` 记录原文件数、总字节数、每个来源索引 SHA-256、解压内容聚合 SHA-256 和压缩包 SHA-256。归档前必须逐项与源文件比对，归档后可独立校验。

**第二轮补充：** UBC OPBP（265 份）和 IntroPhysics（53 份）已经进一步无损归档为 `ubc_opbp-raw.tar.gz` 与 `intro_physics-raw.tar.gz`；另有独立完整性清单 `small_sources_manifest.json`。详见 [第二轮整理与恢复说明（归档）](../../data/archives/library.zip)。本页下方的三组恢复命令仍仅适用于第一轮 19,837 份大型候选。两轮累计归档 **20,155 份**原始候选，未删除任何正式题目或解析。

**第三轮补充：** WeBWorK OPL 的 59 份与热学的 21 份**原始 .pg 程序**另无损压缩为 `webwork_opl-raw.tar.gz` 与 `webwork_thermal-raw.tar.gz`，独立哈希清单为 `webwork_sources_manifest.json`。这些 PG 程序不是独立可编译的 TeX，仍须原 WeBWorK 引擎/宏与许可逐项审核。详见 [第三轮说明（归档）](../../data/archives/library.zip)。三轮累计归档 **20,235 份**待审原始文件。

## 检验与恢复

```bash
python scripts/compact_external_candidates.py --verify
python scripts/compact_external_candidates.py --restore college_physics
python scripts/compact_external_candidates.py --restore hf_physics_dpo
python scripts/compact_external_candidates.py --restore physics_refresher
python scripts/compact_small_external_sources.py --verify
python scripts/compact_webwork_sources.py --verify
python scripts/compact_webwork_sources.py --restore webwork_opl
```

恢复只在明确调用时写回 `raw/ID.md`，并逐文件检查与归档一致。若继续从上游导入候选，需要先恢复三组原文，完成导入后再运行 `--apply` 重新打包并同步提交更新后的 `index.json`、`manifest.json` 与归档。恢复产生的 `raw/` 文件由 Git 忽略，避免下次提交重新制造大量零散文件。

**边界：** `bank/` 的 452 道正式高难综合题、《普通物理学习题》的 ElegantBook 原始章节、张三慧教材习题分支、其他 UBC/WeBWorK 等源题及 QA 工作流都不在此次归档范围。归档不会改变候选题的版权、真实性或学术审校状态。原逐题文件仍可从 Git 历史恢复。

