# 赵近芳、王登龙第五版大学物理教材与学习指导 · ElegantBook 题解

**逐题 LaTeX 研究与校勘，用户上传两份扫描教材为底本。**

- 《大学物理简明教程（第5版）》第1章 **31** 题：原题号 `1.1.1—1.1.7`、`1.2.1—1.2.7`、`1.3.1—1.3.17`。
- 《大学物理简明教程（第5版）》第2章 **46** 题：原题号 `2.1.1—2.1.12`、`2.2.1—2.2.9`、`2.3.1—2.3.25`。
- 《大学物理学学习指导（第5版）》第1章例1.1—1.5、第2章例2.1—2.7，**12** 题。
- **总计 89 题号，本轮新增 69**。少数题号存在题面歧义或疑似错误，已保留原题并在 `quality-check.md` 逐条登记，不能将其误标为“无争议完全质检”。
- 复用 `../irodov-zh-elegant/elegantbook.cls`；`main.tex` 为 XeLaTeX 入口，`cover.tex` 是本仓库原创装饰封面。
- `check_math.py` 提供题号连续性、题块完整性与抽样数值验算；`.github/workflows/zhao-wang-physics-elegantbook.yml` 自动构建及发布PDF。
- **技术通过 ≠ 物理学术二审通过 ≠ 公开传播权限已获批。**

## 源码及管理

```text
main.tex
cover.tex
build.sh
check_math.py
chapters/
  textbook-ch01-foundations-001-003.tex
  textbook-ch01-exercises.tex
  textbook-ch02-choices.tex
  textbook-ch02-blanks.tex
  textbook-ch02-solutions-001-012.tex
  textbook-ch02-solutions-013-025.tex
  guide-ch01-examples.tex
  guide-ch02-examples.tex
progress.md
quality-check.md
```

运行 `bash build.sh` 将复用ElegantBook类；如果只在GitHub Actions下编译，则工作流从原目录复制编译用类文件。所有教材内容独立于仓库正式 `bank/` 的452道高难综合题，不改动正式题库索引和文件。

本资料使用用户提供的两本书扫描页；原书版权归权利人。研究整理稿并不代表可以未经授权公开复制、汇编或二次发行，正式传播前须核验版权许可。
