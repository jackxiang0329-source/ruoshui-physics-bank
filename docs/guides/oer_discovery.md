# 全网题源发现与许可审查

现已接入的可自动拉取来源包括 UBC Open Physics Bank 内逐题符合许可的 Markdown，以及 East Texas A&M University PHYS 2425 中无图片依赖的独立题干。

发现工具已合并为 `python3 scripts/discover_sources.py github`（GitHub 项目）与 `python3 scripts/discover_sources.py huggingface`（HF 数据集）；仅更新相应目录元数据，不自动将候选题判为合格。执行频率由实际工作流配置决定，不能假定每30分钟都有完整采集。

**严禁将“GitHub 公开”误认为“版权许可开放”。** 新发现项目只存元数据，不自动复制、不自动标记可组卷。只有根据具体许可证、作者署名、来源权利、技术格式和去重检查完成审核后，才单独接入自动导入器。

说明：GitHub 搜索只是全网开放资源的一种渠道；网站资源的发现仍需补充适配器，并遵守 robots.txt、使用条款与合理请求频率。当前是增量扩展，不是已抓取整个互联网。

失败及来源统计保存在 Actions 日志和外部资源目录。审查未完成的题目与 bank/ 正式题库始终分离。
