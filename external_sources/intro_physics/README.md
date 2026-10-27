# 新增大学物理题源：PHYS 2425 (East Texas A&M University)

开源来源：https://github.com/saturnaxis/IntroPhysics

固定上游 Git 版本：cd3ed19ede4206f68e6ea7c1e28c5961a872f3cb

作者：Billy Quarles。许可声明：CC BY 4.0，见上游 README.md 与 LICENSE.md；每题仍需核对第三方内容权利。

本仓库自动下载九份合理大小的课程 Jupyter Notebook，校验 Git blob SHA，抽取带有 **Example Problem / The Problem** 标志的独立题干；保留出处、版本、来源 SHA、学科、抽取单元格和正文 SHA256。排除图像与跨段落依赖，不下载巨型 notebook，也不复制其教学说明或数据资源。

新题仅存于 external_sources/intro_physics/raw/，并由外部待审核队列统一索引。题源即使已导入仍存在许可链、物理正确性、答案/插图、语义重复及排版审核工作，**不是可直接组卷的正式题目**。同一上游版本处理完后不会无限重复导入。

执行：python scripts/import_intro_physics.py --limit 100

GitHub Actions 每 30 分钟触发同一个工作流，跟踪结果文件 external_sources/logs/intro_physics_latest.json。
