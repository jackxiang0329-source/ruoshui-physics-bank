# 外部物理题源：发现、采集、分类、预检（整合说明）

这里合并了六份同类操作手册，旧原文按章节完整保留，不改变外部候选题尚未学术审核、不可自动组卷的要求。有关实际自动化频率请以 GitHub Actions 配置为准。

---

## 1. 来源发现

*原文件：`docs/guides/oer_discovery.md`*

# 全网题源发现与许可审查

现已接入的可自动拉取来源包括 UBC Open Physics Bank 内逐题符合许可的 Markdown，以及 East Texas A&M University PHYS 2425 中无图片依赖的独立题干。

发现工具已合并为 `python3 scripts/discover_sources.py github`（GitHub 项目）与 `python3 scripts/discover_sources.py huggingface`（HF 数据集）；仅更新相应目录元数据，不自动将候选题判为合格。执行频率由实际工作流配置决定，不能假定每30分钟都有完整采集。

**严禁将“GitHub 公开”误认为“版权许可开放”。** 新发现项目只存元数据，不自动复制、不自动标记可组卷。只有根据具体许可证、作者署名、来源权利、技术格式和去重检查完成审核后，才单独接入自动导入器。

说明：GitHub 搜索只是全网开放资源的一种渠道；网站资源的发现仍需补充适配器，并遵守 robots.txt、使用条款与合理请求频率。当前是增量扩展，不是已抓取整个互联网。

失败及来源统计保存在 Actions 日志和外部资源目录。审查未完成的题目与 bank/ 正式题库始终分离。

---

## 2. Hugging Face 发现与采集

*原文件：`docs/guides/huggingface_import.md`*

# 大学物理双平台采集：Hugging Face + GitHub

- GitHub 既有题源：UBC Open Physics Bank / East Texas A&M University PHYS 2425，依源 SHA、许可信号及完整性审核后归档。
- Hugging Face 自动导入：仅开放列表 yusufbaykaloglu/Physics-DPO-Dataset，公开数据集卡显示 Apache-2.0，属于合成物理问答，**答案未验证，不代表高校真题**。
- 每次自动读取最多 500 条、导入最多 100 道 HF 候选题干；按源行号、SHA256 及学科分类存储到 external_sources/hf_physics_dpo/raw/，保留源 Dataset URL、观察到的上游 Git 修订版本与许可证审查状态。
- 数据页由 Hugging Face 官方 Dataset Viewer rows API 返回；其缓存并非严格按版本固定，因此每一行另存规范化 SHA256，并在每轮任务前后核查上游版本。版本更改时暂缓当前来源导入。
- Dataset card 许可标签只作授权信号，不能证明所有第三方摘录文本已经适当授权；存储内容仍需复核权利链、物理条件、答案、跨源语义重复。
- GitHub 与 Hugging Face 发现器每轮只同步搜索到的目录元数据，不会直接抓取许可证未知、含 NC 限制及依赖图片的大型基准测试内容。
- 对外部题源一律设置 exam_ready=no，不自动复制进 bank/，正式组卷前仍需学术审核。
- 审计：external_sources/logs/huggingface_import_latest.json、每日 -huggingface.jsonl，以及 external_sources/catalog/huggingface_datasets.json。
- 频率：GitHub Actions cron UTC 每小时 7 和 37 分；实际触发可延迟。仅对已注册的适配器自动下载，不应宣传为无限制爬取整个互联网。

候选对比与来源权利需持续复核：UGPhysics/ugphysics (CC BY-NC-SA 4.0)、PrismaX/PhysUniBench (CC BY 4.0，配图依赖)、yale-nlp/physics-verified (MIT 声明但高校试卷来源权利待确认)、desimfj/PHYSICS (MIT 声明但原始题权利链未审核)。

SeePhys/SeePhys：原始数据混合文字和图片题。本适配器只导入 `images` 为空且题干不依赖图示的条目，前后核验 Apache-2.0 元数据与数据集修订，单轮扫描 250、最多新增 100。所有条目记录 SHA256、原行号和待审核状态，不能作为已审定大学考试真题。

2026-10-28：官方 HF Dataset Viewer 曾出现临时 HTTP 502，导致单次仅导入 100 条。现将 429/500/502/503/504 及短暂连接超时纳入最多三次有限重试，仍保留严格源修订校验、原行号连续性检查和 SHA256 去重；非暂态 HTTP 404 不重试。自动重试不代表每轮保证有 500 道题。

---

## 3. Open Educational Resources 自动导入

*原文件：`docs/guides/auto_import_oer.md`*

# 每 30 分钟自动更新大学物理开源题源

**实施方式**：GitHub Actions 工作流 [auto-import-oer.yml](../../.github/workflows/auto-import-oer.yml)。
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

---

## 4. College Physics 导入

*原文件：`docs/guides/college_physics_import.md`*

# 新接入 GitHub: College Physics (OpenStax College / philschatz mirror)

上游：https://github.com/philschatz/physics-book

固定修订：a7efaa7e221fab1694022d8bb98b83a73ee31d3d

版权信息：仓库 LICENSE.txt 声明 Copyright 2014 OpenStax College, **Creative Commons Attribution 3.0 Unported**，已固定 Git blob SHA，导入前会再次读取核验许可。

源材料约 283 章/节 Markdown 文件（含题目、HTML / MathML）；每轮最多读取 50 个独立章节、最多新增 500 条图像依赖较少的独立题干。过滤图片引用、跨章节引用及不完整题，保留原题 HTML/MathML 与逐题来源和许可。原题样式含不适宜直接排版的 HTML，后续需经过 TeX 转换、逐题版权链检查、语义去重、题意及答案复核方可用于组卷。

仅在 external_sources/college_physics/raw/ 及对应索引、总审核队列归档；不得自动放入 bank/。与 OpenStax 的另一个 **University Physics bundle (CC BY-NC-SA 4.0)** 仓库不同，后者因 NC/SA 限制不在本自动导入白名单内。

运行记录：external_sources/logs/college_physics_latest.json。Github Actions 仍按每小时 :07/:37 UTC 触发，实际触发可能延迟。

2026-10-27：自动导入任务同时根据 bank/ 中独立原创题的元数据重建并校验 data/index.csv 与 TeX 主文件，修复旧的索引过期问题；该步骤并不将外部待审原题添加到原创 bank/。

为避免上游临时 503/网络故障导致章节长期遗漏，对 429/500/502/503/504 和网络超时进行最多 3 次限速重试；404 和文件格式不符不重试，成功后仍须重新验证 Git blob SHA 与许可证声明。新分类扩展至核物理、基本粒子、量子物理及多普勒效应；歧义章节保留待分类。

---

## 5. 候选筛选

*原文件：`docs/guides/curation_triage.md`*

# 外部大学物理习题：优先复核与跨来源重复信号

`scripts/curation_triage.py` 会在每次 30 分钟抓取、题目归档和学科回填完成后，创建以下两个文件：

- `external_sources/catalog/review_priority.csv`：**最多 120 道人工复核候选**，按已登记 OpenStax（60）、UBC（45）和 PHYS 2425（15）的开放授权信号筛选，且尽可能均衡学科。候选仅供编辑挑选，**绝非已审核、已解答或可组卷**。
- `external_sources/catalog/review_triage_report.json`：记录原始候选总数、优先清单来源组成、因许可信号排除的数量及跨来源的**相同 SHA256 题干指纹**。各来源的归一化算法可能不同；指纹相同是疑似重复的强信号，不同不能证明题目不同，更不能代替语义去重。

审查人员仍须逐题核对：权利链、署名、数学物理正确性、题意完整性、配图和公式转换、答案及跨来源语义重复。OpenStax 源题为 HTML/MathML，需要规范化为 LaTeX 后再排版。Hugging Face 合成题暂不纳入优先教育教材清单。

该功能不修改 `bank/`，也不提高 `exam_ready` 状态。所有外部文件仍须审核后才可能进入正式组卷题库。

待分类或空白学科的原题仍保留在外部源索引，但不会进入本清单；报告会记录各来源因学科未定而暂缓优先复核的数量。优先清单可在审核队列增长后自动更新。

---

## 6. 审核预检

*原文件：`docs/guides/review_preflight.md`*

# 外部题目静态质检（仅候选，不是学术审题）

`scripts/review_preflight.py` 读取 `external_sources/catalog/review_priority.csv` 中的 120 条人工复核候选，针对**本地已经存档的题干**检查排版和上游格式障碍，并生成：

- `external_sources/catalog/review_preflight.csv`：逐题对应学科、原始类型、MathML 节点数、纯文字长度、风险标志、需要的人工复核项目。
- `external_sources/catalog/review_preflight_report.json`：风险分布、源题类型分布及优先清单内的近文字重复候选对。

标志包括：图片或 Figure 依赖、跨引用、UBC 参数模板、原始答案区、MathML 公式及结构明显不完整。这些是**筛查信号**，可能误报或漏报。相同字词集合 Jaccard 阈值 0.88 只是近文本线索，绝不是语义去重。

所有题目必须继续进行版权链、数学物理正确性、答案核验、完整题意与配图、可编辑 LaTeX 转换及教师审阅；无论质检信号是否为零，都保持 `exam_ready=no`，不会自动移入正式 `bank/`。

如需本地运行：`python scripts/curation_triage.py && python scripts/review_preflight.py`。GitHub Actions 在每轮自动抓取之后运行该检查及对应单元测试。
