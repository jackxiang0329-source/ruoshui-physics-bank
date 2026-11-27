# 三千弱水 · 大学物理题库

高难综合题、教材习题研究性详解与 LaTeX 排版。正式题库、教材研究稿、未审核候选分别管理。

## 题库与教材

| 内容 | 入口 |
|---|---|
| 正式高难综合题（452 道） | [六学科题库](bank/) · [题号索引](data/index.csv) |
| 合订 LaTeX | [题目](tex/questions.tex) · [解析](tex/solutions.tex) |
| Irodov《普通物理学习题》（1,878 题） | [源码](textbooks/irodov/) · [PDF](textbooks/irodov/main.pdf) |
| 赵近芳、王登龙教材与学习指导 | [源码](textbooks/zhao_wang/) · [PDF](textbooks/zhao_wang/main.pdf) |
| 三校大学物理（1,598 个题号，学术复核未完成） | [源码](textbooks/three_college/) · [现存 PDF（非最新版）](textbooks/three_college/main.pdf) |
| 外部候选（未准入） | [来源及分类](external_sources/) |

正式题库六个权威文件：[力学](bank/mechanics.json)、[电磁学](bank/electromagnetism.json)、[热学](bank/thermodynamics.json)、[振动与波动](bank/waves.json)、[光学](bank/optics.json)、[近代物理](bank/modern_physics.json)。原题号及校验值保持不变。

## 维护与构建

[教材总览](textbooks/) · [索引与数据](data/) · [工具](scripts/) · [质量规范与历史](docs/) · [统一资源归档](data/archives/library.zip)

在仓库根目录执行（Python 3.11+）：

```bash
python3 -m pip install -r requirements.txt
python3 scripts/compact_auxiliary.py --verify
python3 scripts/compact_auxiliary.py --restore
python3 scripts/compact_bank.py --verify
python3 scripts/compact_bank.py --restore
python3 scripts/build.py --check
```

恢复后编辑题号文件或教材章节，按质量流程检查，再用 `python3 scripts/compact_bank.py --pack` 或 `python3 scripts/compact_auxiliary.py --pack --group GROUP` 更新权威归档，并同步派生数据。只提交权威文件及必要派生文件。教材使用各自的 `build.sh`（XeLaTeX / ElegantBook）。

## 质量状态

正式准入遵循[高难准入](docs/policies/high_difficulty_policy.md)和[六轮质检](docs/policies/qa_protocol.md)。自动校验不等于逐题学术终审；外部候选不能直接组卷。三校教材最近一次构建在 `czu-ch13.tex` 第 308 行遇到数学模式错误，不能将现存 PDF 标为最新。张三慧三册研究稿见 [Draft PR #45](https://github.com/jackxiang0329-source/ruoshui-physics-bank/pull/45)。

[命名规范](docs/policies/repository_naming.md) · [历史记录](docs/history/compaction_history.md) · [构建状态](https://github.com/jackxiang0329-source/ruoshui-physics-bank/actions)
