# 大学物理题库 · 文档导航

本目录只保留现行质量政策、项目总历史和本导航。21份原操作指南、批次记录、报告、逐题复核及参考书目原样收录在 [reference_docs.zip（归档）](../data/archives/library.zip)。其原路径和校验值均保留；不需要恢复即可在 GitHub 下载归档查看。

| 直接入口 | 用途 |
|---|---|
| [命名规范](policies/repository_naming.md) | 文件组织与归档维护 |
| [高难准入](policies/high_difficulty_policy.md) | 正式题库的难度门禁 |
| [六轮质检](policies/qa_protocol.md) | 独立审核与证据要求 |
| [难度分级](policies/difficulty_bands.md) | 分级标准 |
| [翻译规范](policies/translation_catalog_policy.md) | 外部候选与译稿 |
| [项目总历史](history/project_history_2026.md) | 2026年扩库与维护记录 |
| [完整参考文档归档（归档）](../data/archives/library.zip) | 原指南、报告、书目、历史复核 |

## 使用与维护

```bash
# 在仓库根目录执行
python3 scripts/compact_auxiliary.py --verify
python3 scripts/compact_auxiliary.py --restore
python3 scripts/compact_bank.py --restore
python3 scripts/build.py --check
```

原组卷说明位于归档中的 `docs/guides/exam_assembly.md`；LaTeX架构说明为 `docs/guides/tex_architecture.md`。外部题源工具、教材章节、测试及专项QA的使用方式见 [主仓库说明](../README.md)。恢复后的原文件是工作区视图，编辑后须重新打包。未审外部候选不进入正式题库，技术校验不等同于学术终审。
