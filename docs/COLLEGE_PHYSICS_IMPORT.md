# 新接入 GitHub: College Physics (OpenStax College / philschatz mirror)

上游：https://github.com/philschatz/physics-book

固定修订：a7efaa7e221fab1694022d8bb98b83a73ee31d3d

版权信息：仓库 LICENSE.txt 声明 Copyright 2014 OpenStax College, **Creative Commons Attribution 3.0 Unported**，已固定 Git blob SHA，导入前会再次读取核验许可。

源材料约 283 章/节 Markdown 文件（含题目、HTML / MathML）；每轮最多读取 50 个独立章节、最多新增 500 条图像依赖较少的独立题干。过滤图片引用、跨章节引用及不完整题，保留原题 HTML/MathML 与逐题来源和许可。原题样式含不适宜直接排版的 HTML，后续需经过 TeX 转换、逐题版权链检查、语义去重、题意及答案复核方可用于组卷。

仅在 external_sources/college_physics/raw/ 及对应索引、总审核队列归档；不得自动放入 bank/。与 OpenStax 的另一个 **University Physics bundle (CC BY-NC-SA 4.0)** 仓库不同，后者因 NC/SA 限制不在本自动导入白名单内。

运行记录：external_sources/logs/college_physics_latest.json。Github Actions 仍按每小时 :07/:37 UTC 触发，实际触发可能延迟。

2026-10-27：自动导入任务同时根据 bank/ 中独立原创题的元数据重建并校验 data/index.csv 与 TeX 主文件，修复旧的索引过期问题；该步骤并不将外部待审原题添加到原创 bank/。
