# 大学物理目录与中文翻译规范

## 主文件与索引

中文译文唯一可编辑主档为 `localization/zh_CN/translations.json`，包含 Physics Refresher 的 `entries` 及 OpenStax、IntroPhysics 的 `additional_entries`。每条都有稳定题号、固定原文指纹、中文译题、学科与审校状态。**不要创建独立的同名翻译 JSON 或题号 Markdown。**

`scripts/materialize_zh_drafts.py` 在严格校验原始来源后，将译题按七大学科聚合到 `localized/zh_CN/合订/{module}.md`，每题使用固定 HTML 锚点 `#cp-xxxxx`、`#ip-xxxx` 或 `#pref-xxxxx`。同目录 `README.md` 是导航入口。旧版 `localized/zh_CN/<module>/<topic>/<ID>.md` 与 `supplementary/<ID>.md` 是**自动生成的冗余视图**，在重建时删除；不要继续编辑或恢复这些文件。英文 raw、原创建档和原始索引不删除。

`scripts/organize_physics_catalog.py` 将 `external_sources/catalog/题目总索引.csv` 的“中文译稿”列改为对应学科合订路径及题号锚点。按学科/知识点的 CSV 索引仍然是自动生成的检索视图，不能作为第二份权威译文。

| 目录 | 角色 |
| --- | --- |
| `bank/ID/{question.tex,solution.tex,meta.json}` | 100 道原创待审样板题，不受外部译题影响 |
| `external_sources/*/raw` | 不可覆写的原始英文档案 |
| `localization/zh_CN/translations.json` | 翻译唯一编辑源 |
| `localized/zh_CN/合订/*.md` | 最多七份中英对照合订稿 |
| `localized/zh_CN/中文译稿报告.json` | 译题数、校验数、合订文件路径和逐题索引 |
| `external_sources/catalog/中文分类导航.md` | 分类与全量题目检索 |
| `taxonomy/physics_taxonomy.json` | 七大模块与来源章节映射 |
| `localization/zh_CN/术语表.md` | 物理术语统一表 |

## 审核与翻译约束

1. 不修改原文题号、公式、数值、单位、条件或图示引用；不能把不完整题面擅自补为有唯一数值答案。
2. 区分路程／位移、速度／速率、电势／电势能、加速度／减速度和测量误差／不确定度。
3. 逐题保存英文原件指纹。指纹一致仅代表未偏离所存英文版本，**绝不等于中文翻译准确、物理答案正确或版权已核验**。
4. 所有外部候选 `exam_ready=false`，不得进入正式组卷，待独立双语复核、物理答案检查、版权许可和语义去重后方能考虑。
5. 原文缺图、跨题依赖、数值歧义、单位或模型假设缺失都用 `risk_flags` 与 `notes` 记录。参见 CP-00043、CP-00069、IP-0021、IP-0023。
6. 来源章节不等于真实知识点：CP-00898 属热学—热辐射、CP-00080 属力学—牛顿运动定律；新增错分要逐题留痕。

## 一键重建

```bash
python scripts/export_zh_review.py --check
python scripts/materialize_zh_drafts.py
python scripts/organize_physics_catalog.py
python -m unittest discover -s tests -p 'test_physics_organization.py' -v
```

每次编辑主档后通过工作流自动重建学科合订稿、中文分类总索引和统计报告。不要手工编辑生成文件。题目数量请读取 `localized/zh_CN/中文译稿报告.json` 的 `translated_drafts`，不要在 README 写死历史数量。
