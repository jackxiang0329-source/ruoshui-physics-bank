# 外部题目静态质检（仅候选，不是学术审题）

`scripts/review_preflight.py` 读取 `external_sources/catalog/review_priority.csv` 中的 120 条人工复核候选，针对**本地已经存档的题干**检查排版和上游格式障碍，并生成：

- `external_sources/catalog/review_preflight.csv`：逐题对应学科、原始类型、MathML 节点数、纯文字长度、风险标志、需要的人工复核项目。
- `external_sources/catalog/review_preflight_report.json`：风险分布、源题类型分布及优先清单内的近文字重复候选对。

标志包括：图片或 Figure 依赖、跨引用、UBC 参数模板、原始答案区、MathML 公式及结构明显不完整。这些是**筛查信号**，可能误报或漏报。相同字词集合 Jaccard 阈值 0.88 只是近文本线索，绝不是语义去重。

所有题目必须继续进行版权链、数学物理正确性、答案核验、完整题意与配图、可编辑 LaTeX 转换及教师审阅；无论质检信号是否为零，都保持 `exam_ready=no`，不会自动移入正式 `bank/`。

如需本地运行：`python scripts/curation_triage.py && python scripts/review_preflight.py`。GitHub Actions 在每轮自动抓取之后运行该检查及对应单元测试。
