# OpenStax College Physics 全量结构质检

本脚本 `scripts/audit_college_corpus.py` 每轮审核全部已归档的 OpenStax College Physics 原题，输出：

- **`external_sources/catalog/college_corpus_audit.csv`**：逐题一行，按章节/学科/概念或计算题展示源 SHA、长度、MathML 公式数、配图依赖、模板依赖、结构风险及人工审核状态。
- **`external_sources/catalog/college_corpus_audit_report.json`**：总体风险分布、学科/题型覆盖、源文件完整性、完全相同指纹和「同一题干模板但数字不同」的疑似重复组。
- **`external_sources/catalog/college_next_review.csv`**：额外 120 道编辑候选，按七大学科轮选，优先列出**未发现明显排版障碍**且尚未进入既有 60 道 OpenStax 编辑清单的题目。它们依然必须独立审题、验证答案和授权链。

严肃区分：
1. **原始文件与索引完整性**：逐一比对 pinned upstream revision、原题来源 SHA、索引 question_sha256、归属声明与本地 raw 内容；不一致立即让工作流报错，不得宣称导入审核成功。
2. **格式风险**：图示、跨引用、MathML 不支持的节点、题干空缺等自动扫描，提供人工处理线索。
3. **数学物理有效性**、**答案是否正确**、**版权链是否可以复用**、**语义是否重复**：全部保留人工待审，不得凭自动扫描判为通过。

该脚本仅在 `external_sources/` 内生成紧凑的两份 CSV 和一份 JSON，不向 `bank/` 添加任何第三方题目，也不会影响已审定试卷的 PDF 构建。

执行：`python scripts/audit_college_corpus.py`。校验运行：`python -m unittest discover -s tests -p 'test_audit_college_corpus.py' -v`。

2026-10-28 全量扫描另检出 7 道带 MathML mover 上划线的粒子物理题、3 道 msup/msub 结构缺失的原题。对能核实含义的水平上划线和向量箭头新增 TeX 转换；对缺失上下标的源文件继续显示 `[CHECK MATH]` 且强制人工复核，不补猜字符。
