# 工具导航

| 类别 | 常用工具 |
|---|---|
| 题库维护 | [bulk_import.py](bulk_import.py) · [build.py](build.py) |
| 组卷 | [assemble_exam.py](assemble_exam.py) · [render_single.py](render_single.py) |
| 质量门禁 | [check_difficulty_gate.py](check_difficulty_gate.py) · [quality_gate_bulk.py](quality_gate_bulk.py) · [check_future_rounds.py](check_future_rounds.py) · [check_review.py](check_review.py) |
| 数理及源码检查 | [check_physics.py](check_physics.py) · [check_tex_controls.py](check_tex_controls.py) · [audit_milestone.py](audit_milestone.py) |
| 无损归档 | [compact_bank.py](compact_bank.py) · [compact_auxiliary.py](compact_auxiliary.py) |
| 外部候选校验 | [compact_external_candidates.py](compact_external_candidates.py) · [compact_small_external_sources.py](compact_small_external_sources.py) · [compact_webwork_sources.py](compact_webwork_sources.py) |
| 目录规范 | [check_repository_layout.py](check_repository_layout.py) |

历史批次脚本、测试、外部采集与分类工具在 [统一归档库](../data/archives/library.zip) 中，先执行 `python3 scripts/compact_auxiliary.py --restore`。保留旧工具内部接口，避免维护时出现多个权威源。
