# 开放大学物理题源目录与实际拉取进度

当前目录的清单含 **897 条UBC Markdown题源路径**与 **214 条BrockPhysics WeBWorK PG题源路径**。这些文件路径已从上游Git树读取，源修订号和Git文件blob散列也保存在 `catalog/upstream_manifest.json`。**完整目录不等于文件已复制**：目前实际保存 **40+12=52 份题目正文源文件**，其余只是待抓取路径。

| 资源 | 发现的上游文件 | 已保存真实题源 | 内容类型 | 授权备注 |
|---|---:|---:|---|---|
| [UBC OPBP](https://github.com/open-resources/physics_bank) | 897 | 40 | Markdown/Myst，部分带图片和参数 | 逐题CC BY 4.0或CC BY-NC-SA 4.0，必须查逐题说明 |
| [WeBWorK BrockPhysics](https://github.com/openwebwork/webwork-open-problem-library) | 214 | 12 | PG可参数化程序，需要WeBWorK宏引擎 | OPL缺省CC BY-NC-SA 3.0，若文件另有授权须重新核对 |
| [OpenStax University Physics](https://github.com/openstax/osbooks-university-physics-bundle) | 待统计 | 0直接XML模块 | CNXML大学物理1—3卷 | 仓库说明与逐章/逐题声明须分别核对 |
| [IntroPhysics (Quarles)](https://github.com/saturnaxis/IntroPhysics) | 待统计 | 0 | Jupyter Book/IPYNB | CC BY 4.0，个别引用媒体另查 |
| [UGPhysics](https://huggingface.co/datasets/UGPhysics/ugphysics) | 待统计 | 0 | 中英文JSON和解析 | 数据卡CC BY-NC-SA 4.0，原始问题来源还需核权 |
| [Yale PHYSICS](https://github.com/yale-nlp/Physics) | 待统计 | 0 | 研究生资格考试题 | 试题源机构许可未逐条确认，暂不复制 |

## 使用和限制

- 下载的原始文本分别位于 `ubc_opbp/raw/` 和 `webwork_opl/raw/`；其元数据位于各自 `index.json`。
- `catalog/upstream_manifest.json` 的 `downloaded=true` 指向当前已实际复制的题源；其余是发现的路径，不能声称已经拉取正文。
- `python scripts/external_inventory.py` 可离线检查源文件缺失、完全重复、署名与清单完整性。
- 版权分类、外部图像、教师解析权限、参数化环境依赖及独立物理验算尚未完成，**外部题目目前全部不准进入正式组卷**。
- CC带NC条款的内容不能直接用于营利/商业题库；带SA条款的改编需要遵守相同方式共享的许可证要求。不要把不同许可证题目和原创题合并为一个不注明来源的作品。
- 下一阶段：按上游清单增量拉取，补足合法依赖文件，逐题分类、去重、重建答案并形成独立的可审核试题版本；不能仅靠文件扩展名直接渲染到ElegantBook。

## 增量拉取命令

克隆本仓库后，可先运行 `python scripts/sync_external_physics.py --source ubc_opbp --limit 20` 预览待拉文件；确认使用范围符合许可证要求后，运行 `python scripts/sync_external_physics.py --source ubc_opbp --limit 50 --download --include-noncommercial` 才实际下载。WeBWorK 改为 `--source webwork_brockphysics`。程序从固定的上游 Git 提交下载并校验 Git blob SHA，跳过未声明UBC授权的文件，保持原始作者和来源，不触碰原创 `bank/`，也不会直接把导入的题源用于正式组卷。建议每批提交Git版本并运行 `python scripts/external_inventory.py` 和 `python -m unittest discover -s tests -v`。
