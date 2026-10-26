# 大学物理开放题源目录（2026-10-26）

本目录仅存储**外部开源题源**，与 `bank/` 内首批100道独立原创题分离。以下统计已通过GitHub远端目录及源文件Git blob SHA核对。

| 来源 | 已发现上游题源文件 | 已实际归档 | 文件格式 | 权利与技术限制 |
|---|---:|---:|---|---|
| [UBC Open Physics Bank](https://github.com/open-resources/physics_bank) | 897 | 147 | MyST Markdown | 逐题CC BY 4.0或CC BY-NC-SA 4.0；参数、配图和来源原著权利仍需核查 |
| [WeBWorK BrockPhysics / University Physics](https://github.com/openwebwork/webwork-open-problem-library) | 214 | 59 | PG | OPL缺省CC BY-NC-SA 3.0，有权利例外；需WeBWorK及宏依赖 |
| [WeBWorK BrockPhysics / College Physics 热学](https://github.com/openwebwork/webwork-open-problem-library/tree/main/Contrib/BrockPhysics/College_Physics_Urone) | 215 | 21 | PG | 相同默认许可及例外；涉及气体动理论、热传递、热力学 |
| **合计** | **1,326** | **227** | | **待审核可正式组卷：0** |

**关键区别：** 1,326是从上游固定Git树发现的文件路径，不代表1,326份试题已经拉取。已真正复制到本仓库的是227份，剩余**1,099个候选文件路径尚未下载正文**。不同文件可能包含多小问、相近题、依赖外部媒体或无法直接渲染；不能把文件数当作独立有效题数。

## 文件与索引

- `ubc_opbp/raw/`、`webwork_opl/raw/`、`webwork_thermal/raw/`：真实题目源代码及Markdown，保留原始作者与许可证说明。
- 各自 `index.json`：逐题ID、Git源版本、blob SHA、版权信号、原始位置、是否有图片或运行依赖。
- `catalog/upstream_manifest.json`：1,326项上游文件路径清单；`downloaded=true` 才表示本仓库已有对应的题目源文件。
- [`curation_queue.csv`](curation_queue.csv)：227条分类筛选记录，含力学、热学、电磁学、振动与波动、光学、近代物理6个模块、权利审查和组卷禁用状态。

## 完整性与质量状态

经远端Git树检查，227份归档文件全部存在，**227/227份的blob SHA与上游原始文件逐条一致**，未发现完全相同的源文件SHA。此结论只说明当前拷贝的字节准确，不证明题目在物理上正确，也不代表语义级去重已完成。

外部题源**全部 `exam_ready=no`**，主要原因包括：

- 许可证可能含NC（非商业）及SA（相同方式共享）限制，尤其需核实教材、教师答案、配图和机构原题的权利；
- UBC题源含图片资源和参数表达式，缺少资源时不能作为完整试题；
- WeBWorK `.pg` 依赖PG引擎及配套宏，不能直接当作ElegantBook的 `.tex` 文件；
- 题干条件、解析、答案、语义重复度和中文术语尚未逐题学术复核。

## 增量抓取与清点

- 预览下一批：`python scripts/sync_external_physics.py --source ubc_opbp --limit 20`
- 预览热学：`python scripts/sync_external_physics.py --source webwork_brock_thermal --limit 20`
- 在确定使用范围符合NC等许可条款时，可增加 `--download --include-noncommercial` 真正下载；程序会核对Git blob SHA，保留归属，不自动批准题目。
- 清点：`python scripts/external_inventory.py`
- 重新生成组卷审核候选清单：`python scripts/rebuild_external_queue.py`
- 回归测试：`python -m unittest discover -s tests -v`（源码已配置；GitHub Actions尚未取得本轮成功运行的证据）

下一步应继续逐源拉取并补齐配图/宏依赖、物理审核、语义去重及出版级中文TeX转换。只有经过许可与独立质量审查的题目，才可明确加入正式试卷组卷池。
