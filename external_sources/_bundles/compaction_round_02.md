# 第二轮无损精简：小型未审来源

本轮仅处理两个额外的**未学术验收、未进入正式题库**的原始 Markdown 子树：

| 来源 | 原逐题文件 | 归档 | 来源索引 |
|---|---:|---|---|
| UBC Open Physics Bank | 265 | [ubc_opbp-raw.tar.gz](ubc_opbp-raw.tar.gz) | [index.json（归档）](../../data/archives/source_metadata.zip) |
| IntroPhysics | 53 | [intro_physics-raw.tar.gz](intro_physics-raw.tar.gz) | [index.json（归档）](../../data/archives/source_metadata.zip) |
| **合计** | **318** | 2 个归档 + [SHA-256 完整性清单](small_sources_manifest.json) | 原有索引不改 |

已存 19,837 份大型语料的三份归档和 [原完整性清单](manifest.json) **保持原样**；本轮归档额外减少活动文件树 **318 - 3 = 315 个文件**，两轮累计归档 20,155 份原始候选。正式题库的 452 道题、题目与解析 TeX、Irodov ElegantBook、张三慧教材 Draft PR 和 WeBWorK PG 源代码均不受影响。

## 无损保证

`scripts/compact_small_external_sources.py --apply` 会根据来源 `index.json` 精确核对全部 ID 与实际 `raw/` 文件，逐一归档原始字节，再校验所有成员、总字节数、逻辑内容 SHA-256、归档 SHA-256 和索引 SHA-256。**两套均全部通过后才删除工作区散文件**，删除后再独立复核一次。归档记录原始单题文件名、来源、正文原始字节，可逐题恢复。

## 校验与恢复

```bash
python3 scripts/compact_external_candidates.py --verify
python3 scripts/compact_small_external_sources.py --verify
python3 scripts/compact_small_external_sources.py --restore ubc_opbp
python3 scripts/compact_small_external_sources.py --restore intro_physics
```

恢复前要确保目标 `raw/` 目录不存在；恢复后文件被 `.gitignore` 排除，不会在普通提交中意外重新散落。若需再次运行 UBC/IntroPhysics 导入器，先恢复所需来源，更新其索引和原文件后，以 `--apply` 重新打包，校验通过再提交更新后的归档和索引。**原始索引中的 `raw_path` 是归档前的逻辑路径，不代表 GitHub 当前文件树仍有该单题文件。**通过归档按需恢复后才能从该路径读取正文。

本轮没有改写 Git 历史，因此不会立即等量减少远端 Git 历史对象与仓库历史容量，也不会自动改变版权和学术审查状态。
