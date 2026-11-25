# 大学物理题库 · 文档导航

此处只存规范、操作说明、审核报告、历史记录和参考资料，不复制 `bank/` 内题目或 LaTeX 解析。正式题目先从六学科归档恢复至 `bank/<ID>/` 后维护、质检，再打包提交。

| 文档类型 | 目录 | 常用入口 |
|---|---|---|
| 规范与质量门禁 | [`policies/`](policies/) | [命名规则](policies/repository_naming.md)、[高难准入](policies/high_difficulty_policy.md)、[六轮质检](policies/qa_protocol.md)、[翻译规范](policies/translation_catalog_policy.md) |
| 使用与操作 | [`guides/`](guides/) | [LaTeX 架构](guides/tex_architecture.md)、[组卷](guides/exam_assembly.md)、[外部导入](guides/college_physics_import.md) |
| 审核和统计 | [`reports/`](reports/) | [覆盖情况](reports/coverage_report.md)、[来源审计](reports/college_corpus_audit.md)、[历史过滤报告](reports/legacy_filter_report.json) |
| 批次及项目历史 | [`history/`](history/) | [2026 历史记录](history/project_history_2026.md)、[第 12 轮工作记录](history/round_12_worklog.md) |
| 逐题复核记录 | [`reviews/`](reviews/) | [第一轮初筛](reviews/round_01_triage.md)、[独立复算](reviews/round_01_independent_derivations.md) |
| 外部参考书目 | [`references/`](references/) | [教材来源清单](references/textbook_references.md) |

## 如何继续录入

1. 正式高难综合题：先运行 `python3 scripts/compact_bank.py --restore`，维护原题号文件并同步派生数据，通过原检查后运行 `python3 scripts/compact_bank.py --pack`。
2. 教材译解：维持独立教材工程，未审的张三慧草稿仅在其 Draft PR 分支，不自动合并。
3. 待审外部原文：由 `external_sources/<source_id>/index.json` 管理元数据，逐题原始字节按需从 `external_sources/_bundles/` 恢复；正式题库不自动吸收。
4. 所有文件命名按 [仓库命名约定](policies/repository_naming.md)，由 CI 阻止格式回退。

旧文档没有删除内容，仅做 Git 可追溯的路径迁移。旧 URL 在 GitHub 中不保证能自动跳转，以本页入口为准。
