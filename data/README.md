# 数据、中文译稿与审核凭证

为避免仓库首页堆积一级文件夹，四组原辅助资料统一归入本目录；**题号和原始内容保持不变**。

| 类型 | 位置 | 作用 |
|---|---|---|
| 正式题库索引 | [`index.csv`](index.csv) / [`problems.json`](problems.json) | `bank/` 派生的索引，不另作权威题目源 |
| 批次与报告 | [`rounds/`](rounds/) 与少量活跃 `*.json` | 第 12–14 轮的 23 份中间报告已无损收纳为 `rounds/historical_reports_round{12,13,14}.json`，由 `scripts/qa_archive.py` 校验和按需恢复；关键质检依赖仍单列 |
| 中文译文主档 | [`localization/zh_CN/translations.json`](localization/zh_CN/translations.json) | 唯一可编辑的中文初译注册表 |
| 术语表 | [`localization/zh_CN/术语表.md`](localization/zh_CN/术语表.md) | 翻译用术语规范 |
| 中文合订初译稿 | [`localized/zh_CN/合订/`](localized/zh_CN/合订/) | 七大学科已生成的初译审阅版 |
| 中文稿统计与题号索引 | [`localized/zh_CN/中文译稿报告.json`](localized/zh_CN/中文译稿报告.json) | 合订文件与题号的可回溯映射 |
| 分类规则 | [`taxonomy/physics_taxonomy.json`](taxonomy/physics_taxonomy.json) | 章节与知识点匹配、类别修正 |
| 六轮人工质检凭证 | [`qa/README.md`](qa/README.md) | 正式审核证据规则，缺少证据不得宣称通过 |

**文件职责：** 正式题面和解析仍仅在 [`../bank/`](../bank/) 维护，LaTeX 合订主文件仍在 [`../tex/`](../tex/)；外部候选题源仍在 [`../external_sources/`](../external_sources/)。

这次迁移只改变文件所在目录，并同步脚本、CSV 索引与文档的引用路径。**翻译初校不等于学术质检通过**；所有尚未取得独立证据的题目审核状态不变。