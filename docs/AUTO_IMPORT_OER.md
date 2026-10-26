# 每 30 分钟自动更新大学物理开源题源

**实施方式**：GitHub Actions 工作流 [auto-import-oer.yml](../.github/workflows/auto-import-oer.yml)。
定时触发：UTC 每小时第 7、37 分钟（相隔 30 分钟）；支持在 Actions 页面手动运行。
GitHub 计划任务并非实时调度器，平台拥堵时可能延迟甚至跳过。

**范围**：本自动流程只从已登记且固定 Git 修订版本的 UBC Open Physics Bank 候选清单中提取未归档文件，并检查 WeBWorK 两个已登记来源的待审限制，同时监测上游仓库是否有新修订。检测到上游更新时**不自动切换固定版本**；新增来源或新版文件必须先登记清单并审查许可，不能声称本脚本搜索了整个互联网。

## 自动核验和安全边界

1. 限定既有上游仓库和已登记候选路径，固定上游 Git commit 与逐文件 blob SHA。
2. 文件格式/大小/路径检查；完整内容与固定 blob SHA 校验；重复 Git blob SHA 和标准化文本去重（**不是语义去重**）。
3. 必须有逐题 Attribution、明确的 CC BY 4.0 授权信号和署名。NC / SA / ND、来源许可含糊或没有署名者**自动阻断**，记录原因。不自动复制 WeBWorK 默认 CC BY-NC-SA 的源文件。
4. 有图片/外部媒体依赖的源题暂不自动入库；通过核验的源文件才保存到 external_sources/ubc_opbp/raw/ 并登记模块、原作者、固定来源链接和状态。
5. 已导入源仍标记“版权链及物理/答案待复核”“语义重复待复核”；**不进入 bank/，不作为正式试卷题**。自动版权信号校验不是法律授权保证。

## 运行和审计

- 运行报告：external_sources/logs/latest.json
- 历史报告：external_sources/logs/YYYY-MM-DD.jsonl，每次运行一条，包含新增数量、来源、失败路径与原因。
- 拒绝重试决策：external_sources/catalog/auto_import_decisions.json；同一固定修订上的同一 SHA 已拒绝候选不反复下载。
- 编目：external_sources/catalog/upstream_manifest.json、external_sources/ubc_opbp/index.json 和 external_sources/curation_queue.csv。
- Actions 作业日志与 30 天上传的 run artifact 可协助定位调度/网络/权限问题。
- 每次至多新增 12 份，通过扫描上限 60 条控制流量；失败网络请求下一轮重试。
- 有新增或审计日志时由 github-actions[bot] 提交并推送 main。要求 Actions 已启用，且 GITHUB_TOKEN 有 contents:write 和 main 允许自动提交；若分支受保护或权限受限，请在仓库设置中调整，或改用 PR 审查流程。

本脚本按保守策略设计，不保证每轮都有新题，也不保证自动通过学术质量检验。已有 237 份基础归档需继续人工复核。

## 吞吐量升级（2026-10-26）

在保留 30 分钟调度（UTC :07/:37）的前提下，每次最多检查 500 个未缓存且具备物理学科分类的源文件，最多新增 100 份原始候选。使用 12 个并发下载线程，所有 SHA、许可、学科、原始作者和精确文本去重判断仍逐文件执行；报告会记录实际新增而不是将 100 视作保证产量。优先检查 OSUP/OpenStax 文件名是调度优化，不代表免除版权复核。需要非商业许可、配图、答案校验或语义去重的文件仍会隔离/跳过。计划任务的 GitHub Runner 使用上限改为 28 分钟以避免占用下次运行。
