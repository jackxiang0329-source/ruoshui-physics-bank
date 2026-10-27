# 大学物理来源覆盖率

每 30 分钟的 GitHub Actions 同步重新生成 external_sources/catalog/coverage_report.json，按题源、学科与授权信号统计待审核候选数。

统计严格核验审核队列的原始文件存在性、ID 唯一性、路径不能逃逸至 external_sources 外部，并确认不存在被错误标记为 `exam_ready=yes` 的外部候选。**这些都不能证明题目物理正确、答案完整或版权链通过人工复核。**

新源约定：机器发现的数据集仅先登记元数据，待确定许可证和技术格式后才启用源适配器。图像依赖、非商业限制、不明确原题授权及难以核实的题目不直接放入正式组卷池。

手动更新：`python scripts/rebuild_external_queue.py && python scripts/report_external_coverage.py`。

历史分类回填：scripts/reclassify_external_topics.py 在每轮采集完成后按照源数据 domain / 章节标题更新 hf_physics_dpo 与 college_physics 的索引，保留原始字段，不更改题干、版权状态或正式组卷门禁。变更数量记入 external_sources/logs/topic_backfill_latest.json。
