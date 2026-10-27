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
