# 合订 LaTeX：按需生成

`bank/<题号>/meta.json`、`question.tex`、`solution.tex` 是正式综合题唯一权威源。此目录只跟踪本说明；下列两册由构建脚本在工作区生成，不另行存入 Git：

```bash
python3 scripts/build.py
python3 scripts/build.py --check
cd tex
latexmk -xelatex questions.tex
latexmk -xelatex solutions.tex
```

- `tex/questions.tex`：仅题目，不泄漏答案。
- `tex/solutions.tex`：题目、解析及标准答案。
- 两本 PDF 由 GitHub Actions 发布为构建工件；编译缓存与本目录生成型 TeX 不进入版本控制。
- `external_sources/irodov-zh-elegant/` 是独立教材项目，其章节 TeX 是实际源稿，不属于本次删除范围。
- 如果下载的是 GitHub 源码 ZIP，须先在仓库根目录运行 `python3 scripts/build.py` 再编译；`--check` 只验证已生成的结果是否匹配。
