# 三千弱水 · 大学物理题库

大学物理原创样板题与外部开放题源**严格分开**：原创 `bank/` 有 100 道待独立六轮质检的样板题；`external_sources/*/raw/` 保存英文候选题的上游快照，不会因翻译而覆盖。外部题源即使已翻译，也不自动获得正式组卷资格。

## 中文题库入口（合订版）

- [按学科阅读中英对照题稿](localized/zh_CN/合订/README.md)：按七大学科最多七本 Markdown，题号可直达；新增题目不再生成一题一文件
- [中文题目总索引与分类](external_sources/catalog/中文分类导航.md)：CSV 按学科、知识点检索
- [译文唯一主档](localization/zh_CN/translations.json)：源指纹、题号、中文译文及审校状态
- [中英术语表](localization/zh_CN/术语表.md)
- [目录及翻译规范](docs/大学物理目录与翻译规范.md)

中文翻译数量以 [自动生成报告](localized/zh_CN/中文译稿报告.json) 为准，主档条目数可能暂时领先于自动构建结果。源哈希校验只验证对应英文快照，**不代表翻译、解答或授权经过专家审核**。

## 权威源与生成脚本

| 路径 | 用途 |
| --- | --- |
| `bank/ID/question.tex`、`solution.tex`、`meta.json` | 100 道原创样板题的唯一源文件 |
| `external_sources/*/raw/` | 上游英文题目归档，不移动 |
| `localization/zh_CN/translations.json` | 中文翻译的唯一编辑源 |
| `localized/zh_CN/合订/*.md` | 自动生成的学科合订视图 |
| `external_sources/catalog/题目总索引.csv` | ID、学科、原件路径、合订锚点 |
| `tex/questions.tex`、`tex/solutions.tex` | 原创 ElegantBook 试题册与解析册 |

```bash
python scripts/export_zh_review.py --check
python scripts/materialize_zh_drafts.py
python scripts/organize_physics_catalog.py
python -m unittest discover -s tests -p 'test_physics_organization.py' -v
python scripts/build.py --check
```

审核规则参见 [六轮质检协议](docs/QA_PROTOCOL.md)、[TeX 架构](docs/TEX_ARCHITECTURE.md)、[考试组卷](docs/EXAM_ASSEMBLY.md) 和 [英文题源说明](external_sources/CATALOG.md)。自动导入与 ElegantBook PDF 通过 [GitHub Actions](../../actions) 发布，自动构建成功不能替代学术复核。
