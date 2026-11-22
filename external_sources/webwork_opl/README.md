## WeBWorK (.pg) 开放题库

现已保存59份由 Brock University 提供的大学物理 WeBWorK PG 源文件，涉及相对论、光电效应和量子势阱。原PG宏及参数化代码保持不变；每份文件绑定GitHub修订版本、作者、章节和许可证默认条款。

PG题源依赖 WeBWorK 运行环境、`BrockPhysicsMacros.pl` 等宏；这些源文件**不能直接解释成可独立编译的ElegantBook TeX**，也不可在未经运行验证、答案校验及来源版权核实的情况下自动进入正式组卷。WeBWorK OPL的缺省授权为CC BY-NC-SA 3.0，具体文件若有不同声明则以原始作者授权为准。参见 `index.json`。


## 无损归档与恢复

59 份未审核的 `.pg` 原文已进入 [`../_bundles/webwork_opl-raw.tar.gz`](../_bundles/webwork_opl-raw.tar.gz)。原 `raw/OPL-###.pg` 按原字节和文件名存于压缩包，索引不变。实际使用 WeBWorK PG 引擎进行逐题审查时，在工作区执行 `python3 scripts/compact_webwork_sources.py --restore webwork_opl`；重新导入后须重新打包并校验。不将 PG 文件转成 TeX、也不改变未获准组卷状态。
