# 目录、文件和归档统一命名规范

## 总原则

目录按**职责**分类而非按日期或对话批次堆叠；新文件使用简短英文标识，避免空格、大小写混用和序号重复。保留题库及教材工程的稳定路径，不因美观批量更换题号或已引用的数据接口。

| 类型 | 标准目录/命名 | 示例 |
|---|---|---|
| 正式题目 | `bank/<ID>/meta.json`, `question.tex`, `solution.tex` | `bank/M001/solution.tex` |
| 整书合订主文件 | `tex/<role>.tex` | `tex/questions.tex`, `tex/solutions.tex` |
| 数据索引与执行报告 | `data/*.json`，批次在 `data/rounds/` | `data/round14_validation_report.json` |
| 审校脚本 | `scripts/check_<scope>.py`；测试 `tests/test_<scope>.py` | `scripts/check_future_rounds.py` |
| 导入与打包工具 | `scripts/import_<source>.py`, `scripts/compact_<scope>.py` | `scripts/compact_webwork_sources.py` |
| 使用说明 | `docs/guides/<topic>.md` | `docs/guides/exam_assembly.md` |
| 标准规范 | `docs/policies/<topic>.md` | `docs/policies/qa_protocol.md` |
| 报告、历史、复核、书目 | `docs/{reports,history,reviews,references}/<topic>.<ext>` | `docs/history/project_history_2026.md` |
| 外部来源 | `external_sources/<source_id>/index.json` | `external_sources/webwork_opl/index.json` |
| 外部原文归档 | `external_sources/_bundles/<source_id>-raw.tar.gz` | `external_sources/_bundles/webwork_opl-raw.tar.gz` |
| GitHub Actions | `.github/workflows/<project>-<purpose>.yml` | `physics-round14-draft.yml` |

约定：代码、普通文档和目录使用 **小写 snake_case**；工作流和 `.tar.gz` 文件保持已有 **kebab-case 功能后缀**（来源 ID 本身仍为 snake_case）。已有 `README.md`、`.gitignore`、`requirements.txt` 按行业标准不改名。所有题目 ID 使用**固定前缀加补零数字**，不得为了文件名“整齐”重编号。

## 已发布稳定路径例外

`bank/`、`tex/`、`data/`、`data/qa/`、`data/localization/zh_CN/`、`data/localized/zh_CN/` 是脚本与外部链接已依赖的接口；`external_sources/irodov-zh-elegant/` 为独立教材工程目录；`external_sources/catalog/按学科/` 与 `按知识点/` 由分类导出器生成，暂保留中文分类路径。其余归档来源索引、文件 SHA 与原上游题号不改写。将来若改名，必须同步更新所有读写脚本、索引字段、相对链接，并通过回归测试。

## 顶层目录保持精简

根目录只允许 `.github/`、`bank/`、`data/`、`docs/`、`external_sources/`、`scripts/`、`tests/`、`tex/` 八个功能目录。`data/` 内承载翻译主档与合订稿、分类规则和六轮质检证据，详见 [数据目录](../../data/README.md)。后续新增辅助资料不得再创建 `qa/`、`localization/`、`localized/` 或 `taxonomy/` 顶层目录。

## 防止今后重新散乱

- 新内容先确定所属类型及权威主文件，避免 `*_final_v2_new` 等重复副本。
- 未审、未授权公开传播的资源不进入正式题库；大批候选使用 **带 SHA-256 清单的可逆归档**，不能把压缩等同于学术质检。
- 报告属于派生或历史证据，不当作第二份题目正文；需要时由脚本重建。
- 文件名检查以 `scripts/check_repository_layout.py` 为准；主分支 CI 同时验证归档、题库同步与 LaTeX 构建。
- 本规范仅约束仓库中的**新内容和可安全迁移的辅助内容**，不重写历史提交。

## 六学科归档例外

正式题库仅跟踪 `bank/M.json`、`E.json`、`T.json`、`W.json`、`O.json`、`Q.json`；原题号文件由 `scripts/compact_bank.py --restore` 无损生成，不提交。修改后使用 `--pack`，保留题号及原有质量门禁。
