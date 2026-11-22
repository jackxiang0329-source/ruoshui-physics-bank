# 第三轮无损精简：WeBWorK PG 程序

本轮只整理两个尚未经过独立复核、不可直接组卷的外部来源：

| 来源 | 原 PG 文件数 | 无损归档 | 来源索引 |
|---|---:|---|---|
| WeBWorK OPL / BrockPhysics | 59 | [webwork_opl-raw.tar.gz](webwork_opl-raw.tar.gz) | [index.json](../webwork_opl/index.json) |
| WeBWorK / BrockPhysics 热学 | 21 | [webwork_thermal-raw.tar.gz](webwork_thermal-raw.tar.gz) | [index.json](../webwork_thermal/index.json) |
| **合计** | **80** | 两个归档 + [SHA-256 清单](webwork_sources_manifest.json) | 只作候选，不准直接组卷 |

先前的 19,837 + 318 = 20,155 份原文无损归档保持不变；三轮合计 20,235 份。此操作仅减少 Git 当前工作树的单题文件数，**不重写历史 Git 对象**。

## 校验与恢复

```bash
python3 scripts/compact_external_candidates.py --verify
python3 scripts/compact_small_external_sources.py --verify
python3 scripts/compact_webwork_sources.py --verify
python3 scripts/compact_webwork_sources.py --restore webwork_opl
python3 scripts/compact_webwork_sources.py --restore webwork_thermal
```

运行 --apply 时先检查所有原 PG、索引、归档成员、总字节数和 SHA-256，全部通过后才移除工作树内散文件，并对归档再次核验。保留逐题 OPL-###.pg 和 THM-###.pg 的原始字节及文件名。

**注意：** PG 是依赖 WeBWorK 解释器及第三方宏的源程序，归档既不等于转换 LaTeX，也不等于运行验证、解题、取得版权许可或完成学术审校。真实使用需按需恢复，新增数据后重新打包校验。正式 bank/、Irodov 工程及张三慧 Draft PR 不受影响。
