# 期末试卷自动组卷：约束规则与独立 TeX

组卷只读取 `bank/{ID}/meta.json` 和 `question.tex`、`solution.tex`，仍由 ElegantBook 主文档通过 `\input{...}` 挂载，不拷贝整道题原始文件。

## 约束

- `--count`：试题总数（整数，≥1）；
- `--topic`：模块筛选，重复传入表示允许多个模块；
- `--kind`：题型筛选，完全匹配 `meta.json` 的 `kind` 字符串；
- `--topic-quota '力学=2'`：指定模块必须恰好选2题；如果指定多个模块，未指定模块填补剩余题目；
- `--min-level`、`--max-level`：难度1至5级；
- `--max-minutes`：所选题目预计答题时间总和的硬性上限。求解器采用128次可复现候选采样，失败不代表数学上无解；
- `--total-points`：试卷总分，按“预计用时 × 难度”的权重分配正整数分值，保证和严格等于目标总分；属于初步建议分值，正式考试需人工定稿；
- `--seed`：同题库、同约束、同随机种子获得相同题号序列；
- `--allow-pending`：**仅用于内部研究**，允许未通过六轮独立复核的题目。正式试卷默认拒绝。

## 示例

此仓库题目目前全部待独立复核，以下命令只能用于**内部草稿**：

```bash
python scripts/assemble_exam.py --count 12 --seed 20261026 --topic-quota '力学=3' --topic-quota '电磁学=3' --max-minutes 200 --total-points 100 --allow-pending
```

生成 `generated/exam_questions.tex`、`generated/exam_solutions.tex`、`generated/exam_manifest.json`。清单记录抽取题号、难度、题型、分值、总预计用时、模块配额与随机种子。两份TeX主文件通过相对路径引用单题原版片段，需保持仓库目录结构编译。

## 正式题质检门禁

除检查 `quality_status == '质检通过'`，正式组卷还调用 `check_review.py` 验证6轮实际审核记录和原始TeX SHA-256。CI是否成功不影响人工审核要求，也不能代表独立学术审稿。

## 当前限制

算法并未完成标准期末考试“选择题/填空题/计算题”精细分值模型、交叉题型精确配额、单题禁止同源/相似题、防知识点重叠、难度分布最优化与多卷互斥。后续应在经过学校真实试卷样式抽样校准后扩展，而不是声称已达到正式考试组卷水平。
