# OpenStax 教材题 TeX 草稿（仅供教师编辑）

`scripts/college_tex_draft.py` 从当前 120 道人工优先复核清单里提取 **60 道 OpenStax College Physics**，生成单一文件 `external_sources/catalog/college_review_tex_draft.tex`，以及 `college_review_tex_report.json`。

该程序用标准库读取保存的原始 Markdown 与 MathML XML，并对分数、幂、下标、根式、常见数字和符号等部分结构产生 LaTeX **草稿片段**。未知或损坏的 MathML 用显式占位符标注 `[CHECK MATH]`，不猜测公式、答案或配图。

这不是可直接编译成正式 PDF 的试题册，也不是已经校正的数学公式。编辑必须逐题对照原始网页、检查量纲、物理条件、公式转换、答案、第三方版权、无图可读性和语义重复。生成物保留在 `external_sources/`，不触及 `bank/` 的正式试题，也不改变审查门禁。

运行：`python scripts/curation_triage.py && python scripts/college_tex_draft.py`。

新增可独立编译的编辑预览主文件 `external_sources/catalog/college_review_preview.tex`，页眉每页明确标注 `NOT EXAM READY`，包含 OpenStax CC BY 3.0 归属与逐题可点击原始章节链接。GitHub Actions 在自动采集提交之后，独立的 `editorial-pdf-preview` job 用 XeLaTeX 编译，上传名为 `college-physics-editorial-preview-pdf` 的 **PDF 工作流附件**。它不是正式考试 PDF，也未经过逐题答案核验。
