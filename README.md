# 三千弱水 · 大学物理题库

高难综合题、教材习题研究性详解、LaTeX 排版与分层质检。正式题库、教材项目及未经审核的外部候选严格分开。

## 快速入口

| 内容 | 入口 | 说明 |
|---|---|---|
| 正式高难综合题 | [bank/](bank/) · [题目索引](data/index.csv) | 452道；六学科权威JSON，保留原题号、题面、解析及校验值 |
| 合订 LaTeX | [题目](tex/questions.tex) · [解答](tex/solutions.tex) | 从正式题库恢复构建 |
| 教材习题详解 | [textbooks/](textbooks/) | 三套独立 ElegantBook 工程 |
| Irodov《普通物理学习题》 | [项目](textbooks/irodov/) · [PDF](textbooks/irodov/main.pdf) | 原书1,878题 |
| 赵近芳、王登龙两书 | [项目](textbooks/zhao_wang/) · [PDF](textbooks/zhao_wang/main.pdf) | 教材及学习指导 |
| 三校大学物理习题 | [项目](textbooks/three_college/) · [PDF](textbooks/three_college/main.pdf) | 1,598个题号；部分学术复核待完成 |
| 外部待审候选 | [external_sources/](external_sources/) | 来源、分类导航、待审状态；不能直接组卷 |
| 中文初译与数据 | [data/](data/) | 翻译主档、规则、正式索引、统一归档 |
| 工具及维护 | [scripts/](scripts/) · [工具导航](scripts/README.md) | 录题、组卷、质检、恢复与构建 |
| 规范与历史 | [docs/](docs/) | 质量政策、命名规范、项目历史 |
| 统一资源归档 | [library.zip](data/archives/library.zip) | 19个逻辑分组，无损恢复 |

## 正式题库分类

| 文件 | 学科 | 原题号前缀 |
|---|---|---|
| [mechanics.json](bank/mechanics.json) | 力学 | M |
| [electromagnetism.json](bank/electromagnetism.json) | 电磁学 | E |
| [thermodynamics.json](bank/thermodynamics.json) | 热学 | T |
| [waves.json](bank/waves.json) | 振动与波动 | W |
| [optics.json](bank/optics.json) | 光学 | O |
| [modern_physics.json](bank/modern_physics.json) | 近代物理 | Q |

## 目录职责

```text
bank/              正式题库权威源码（六学科）
textbooks/         教材独立工程、PDF与学术复核
tex/               正式题库合订LaTeX入口
data/              索引、翻译主档、规则及统一归档
external_sources/  外部候选来源及待审分类
scripts/           维护、质检、组卷和构建工具
docs/              政策、规范、历史
.github/workflows/ 自动验证与PDF构建
```

## 恢复、编辑与构建

在仓库根目录执行（Python 3.11+）：

```bash
python3 scripts/compact_auxiliary.py --verify
python3 scripts/compact_auxiliary.py --restore
python3 scripts/compact_bank.py --restore
python3 scripts/build.py --check
```

恢复后的题号文件和教材章节仅为工作区视图。编辑后按原质量流程重新检查，再用 `python3 scripts/compact_bank.py --pack` 或 `python3 scripts/compact_auxiliary.py --pack --group GROUP` 更新权威归档；只提交相应六学科JSON或 `data/archives/library.zip` 及必要派生数据。恢复工具自动把教材历史归档路径映射至新教材目录，原归档成员名及校验值不变。

教材构建分别运行 `bash textbooks/irodov/build.sh`、`bash textbooks/zhao_wang/build.sh`、`bash textbooks/three_college/build.sh`。编译依赖 XeLaTeX 与 ElegantBook。

## 质量与历史

自动化校验、编译成功不等于逐题独立学术终审。正式准入遵守 [高难准入](docs/policies/high_difficulty_policy.md) 与 [六轮质检](docs/policies/qa_protocol.md)；外部候选未完成版权与物理审核不得纳入正式题库。张三慧三册研究稿仍见 [Draft PR #45](https://github.com/jackxiang0329-source/ruoshui-physics-bank/pull/45)。

[命名和归类规范](docs/policies/repository_naming.md) · [历次精简及旧首页完整记录](docs/history/compaction_history.md) · [构建状态](https://github.com/jackxiang0329-source/ruoshui-physics-bank/actions)
