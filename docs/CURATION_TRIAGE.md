# 外部大学物理习题：优先复核与跨来源重复信号

`scripts/curation_triage.py` 会在每次 30 分钟抓取、题目归档和学科回填完成后，创建以下两个文件：

- `external_sources/catalog/review_priority.csv`：**最多 120 道人工复核候选**，按已登记 OpenStax（60）、UBC（45）和 PHYS 2425（15）的开放授权信号筛选，且尽可能均衡学科。候选仅供编辑挑选，**绝非已审核、已解答或可组卷**。
- `external_sources/catalog/review_triage_report.json`：记录原始候选总数、优先清单来源组成、因许可信号排除的数量及跨来源的**相同 SHA256 题干指纹**。各来源的归一化算法可能不同；指纹相同是疑似重复的强信号，不同不能证明题目不同，更不能代替语义去重。

审查人员仍须逐题核对：权利链、署名、数学物理正确性、题意完整性、配图和公式转换、答案及跨来源语义重复。OpenStax 源题为 HTML/MathML，需要规范化为 LaTeX 后再排版。Hugging Face 合成题暂不纳入优先教育教材清单。

该功能不修改 `bank/`，也不提高 `exam_ready` 状态。所有外部文件仍须审核后才可能进入正式组卷题库。
