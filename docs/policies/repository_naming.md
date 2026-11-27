# 仓库命名与分类规范

## 统一规则

- 顶层按职责划分：`bank/`、`textbooks/`、`tex/`、`data/`、`external_sources/`、`scripts/`、`docs/`、`.github/workflows/`。
- 新目录、普通文件与 Python 模块一律采用小写英文 snake_case；标准入口 `README.md`、`.gitignore`、`requirements.txt` 保留惯例。GitHub Actions 工作流使用 kebab-case。
- 正式题库六个权威文件以完整学科英文命名；原题号 M/E/T/W/O/Q 不变。禁止新增第二份独立正式源。
- 教材目录统一为 `textbooks/irodov/`、`textbooks/zhao_wang/`、`textbooks/three_college/`。每套保留 `README.md`、`main.tex`、`main.pdf`、`build.sh`、`quality_check.md`。有封面及勘误的保留对应文件。历史章节名及题号不强行改写。
- `external_sources/` 只存未审候选导航与来源信息，不放教材正式工程。翻译和分类内部路径（含中文旧文件名）暂保留兼容，不作为新命名范例。
- `scripts/` 保持单层模块路径；以 `check_`、`compact_`、`import_` 等职责前缀区分，并以 [工具导航](../../scripts/README.md) 查找。
- 历史资料与测试集中在 [library.zip](../../data/archives/library.zip)。归档内部保留原路径和校验值；恢复教材时自动映射到新目录，更新仍使用原逻辑组名。

## 首页精简约束

- 根目录仅保留 `README.md`、`.gitignore`、`requirements.txt` 和八个既有职责目录（含 `.github/`）；不新增散落的入口、报告或批次文件。
- 旧 `publish.sh`、`publish.ps1` 是创建另一个仓库的初始化脚本，不适用于本仓库，已从主分支移除；原件仍可通过 Git 历史追溯。现有发布由 GitHub Actions 负责。
- 既有归档成员及恢复路径不改名；旧中文文件名保留兼容，新增文件按本规范执行。

## 维护要求

先验证归档、恢复工作区、执行原有质量门禁和编译，再提交权威源或对应归档。新增文件必须遵循命名规范，不得覆盖原题号、历史证据或已有内容。目录迁移不等于学术复核通过；旧提交链接可追溯。

[项目导航](../../README.md) · [历次精简记录](../history/compaction_history.md)
