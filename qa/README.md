# 六轮独立质检凭证存放位置

目前48道试题均为「待独立复核」，**不存在合格审核凭证，也没有通过六轮质检的题**。

将来只有完成真实审核，才能为题目 `M001` 新增 `qa/M001.json`，并同步修改 `bank/M001/meta.json` 的 `quality_status` 为「质检通过」。

审核文件必须包含：
- `id`：题号；
- `source_sha256`：当前 `question.tex` 与 `solution.tex` 内容的定长组合SHA-256；
- `final_decision`：字符串 `approved`；
- `rounds`：6项依次完整记录，包含round（1..6）、name（名称见脚本）、decision、reviewer、date（YYYY-MM-DD）、evidence（独立审阅证据或页码）。

`python scripts/check_review.py` 仅能校验凭证格式和题目源文件版本绑定，无法证明审核确实独立、正确或具备学术资质。审核人、核验人与证据须真实，不得自动伪造。任何更改已审核的题干或答案都将使旧SHA失效，需要重新审核并生成新凭证。

**不要把没有审核证据的题直接标记为「质检通过」。**
