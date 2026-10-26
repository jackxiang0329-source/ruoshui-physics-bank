# 10,000道大学物理题库总体规划（草案）

## 目标与阶段

- **A0：0–100题**：证明数据格式、XeLaTeX编译、自动验证与人工审核门禁可行。目前100道，已达A0题量目标；力学、电磁学、热学、振动与波动各17题，光学及近代物理各16题；100题正式学术质量验收尚未完成。
- **A1：101–1,000题**：按每批100题扩展，形成模块、题型、难度分层。
- **A2：1,001–10,000题**：以审核通过为前提持续扩充，生成考试试卷与答案册。
- 建议每批100题完成六轮审查后封版；未审题不计入「正式可用题」数量。

## 暂定知识模块配额

| 模块 | 配额 |
|---|---:|
| 力学 | 2,500 |
| 电磁学 | 2,500 |
| 热学 | 1,500 |
| 振动与波动 | 1,500 |
| 光学 | 1,200 |
| 近代物理 | 800 |
| 合计 | 10,000 |

上述数字是规划，不是已生成。考试的题型和分值须另行抽样高校公开期末试卷后校准。典型题型拟涵盖选择、填空、计算、推导与应用建模，避免以改数字方式凑题量。

## 题目建议字段（后续扩展）

`id, topic, knowledge_tags, kind, level, estimated_minutes, stem, options, answer, solution, assumptions, unit_tests, source_notes, similarity_record, reviewer, quality_status, revision`。

## 每批审核门槛

- JSON结构和LaTeX可编译；题面无精确重复。
- 使用另一组方程/数值参数独立复算；检查单位、极限和参数范围。
- 与有权使用的教材和公开题库进行实质相似度复核（不是仅文本相等）。
- 逐题人工审稿+错题复审；六轮所有证据存档后才从 `待独立复核` 变成 `质检通过`。
- 若尚无教材正文授权，不得将其视为已完成逐题比对。

## GitHub发布与自动化

独立仓库优先使用 `jackxiang0329-source/ruoshui-university-physics`。`publish.ps1` / `publish.sh` 用于建仓和首次推送，GitHub Actions 生成 PDF 构建结果。旧 `pdf/` 为ElegantBook切换之前的历史PDF。新PDF须由GitHub Actions成功构建后以Artifacts交付；**权威题源**已改为 `bank/ID/{meta.json,question.tex,solution.tex}`，`data/problems.json` 只保留作为36题迁移档案。
