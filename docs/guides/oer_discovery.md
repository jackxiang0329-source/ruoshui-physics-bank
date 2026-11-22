# 全网题源发现与许可审查

现已接入的可自动拉取来源包括 UBC Open Physics Bank 内逐题符合许可的 Markdown，以及 East Texas A&M University PHYS 2425 中无图片依赖的独立题干。

每 30 分钟的 GitHub Actions 还会运行 scripts/discover_oer_sources.py，搜索公开 GitHub 教学/习题仓库，更新 catalog/discovered_repositories.json，记录发现时间、库名、许可证信号和复核状态。

**严禁将“GitHub 公开”误认为“版权许可开放”。** 新发现项目只存元数据，不自动复制、不自动标记可组卷。只有根据具体许可证、作者署名、来源权利、技术格式和去重检查完成审核后，才单独接入自动导入器。

说明：GitHub 搜索只是全网开放资源的一种渠道；网站资源的发现仍需补充适配器，并遵守 robots.txt、使用条款与合理请求频率。当前是增量扩展，不是已抓取整个互联网。

失败及来源统计保存在 Actions 日志和外部资源目录。审查未完成的题目与 bank/ 正式题库始终分离。
