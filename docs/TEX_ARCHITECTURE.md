# ElegantBook 题库结构与自动组卷接口

## 一、每题独立维护

每题采用 bank/题号/meta.json、question.tex、solution.tex 三个文件。元数据不复制题干、解答；TeX 文件就是唯一权威正文。answer（答案表达式）保存在meta.json，便于组卷和检索。

例如：bank/M001/question.tex 只含题面和行内公式，不含导言区、文档类、封面或其他题目的内容。solution.tex 只含解析文字、推导过程。需要的私有图表可放在同题 assets 子目录，由未来统一资源解析器处理。

## 二、使用 ElegantBook

选用 ElegantBook v4.7（CTAN于2026年5月更新），XeLaTeX；正式书籍使用 tex/questions.tex 和 tex/solutions.tex。

示例主文档片段：

    \chapter{力学}
    \noindent\textbf{题目：}\input{../bank/M001/question.tex}
    \noindent\textbf{解答：}\input{../bank/M001/solution.tex}

上层主文档提供格式和编号；单题片段不设置全局版式，因此无需为电子题库与印刷书分别保存题干副本。

## 三、组卷保留引用，不复写题干

运行脚本 scripts/assemble_exam.py，使用 --topic、--count、--min-level、--max-level、--seed 做选题。默认只允许 quality_status 为「质检通过」的题入正式试卷；开发演示添加 --allow-pending。

组卷输出保存为 generated/exam_questions.tex、generated/exam_solutions.tex 和 generated/exam_manifest.json。TeX 主文件引用 bank 的原始片段；需要在整个仓库结构下编译，不能单独移动主文件而丢失引用。

## 四、增题步骤

为新题创建 bank/新ID/meta.json、question.tex、solution.tex；对照已有metadata字段标记知识点、用时、题型与审核状态。运行 scripts/build.py 重建总册与 CSV 索引，提交改动即可。不要直接编辑已生成的总册入口。旧 data/problems.json 是迁移档案，不再作为新增题目入口。

## 五、构建及质检边界

scripts/build.py --check 用于检查单题源合法性、ID/字段、题目精确去重，以及版本库中的总册和索引是否同步；不能代替独立物理审核。scripts/check_physics.py 现为48道题分别设置了至少一项代数或数值一致性检查；前36题的既有检验有历史结果，新12题的公式表达式已单独核算，但完整CI执行尚待成功。此类核对不能取代专家对题干与物理假设的独立审阅。

最新PDF由 GitHub Actions 构建；旧 pdf/ 目录仍是改模板之前的历史PDF。仓库Actions若失败，应据具体步骤日志定位；若作业在运行任何步骤前即失败，则不能归咎于具体 LaTeX 源码。

模板参考： https://ctan.org/pkg/elegantbook ；后续试卷单页样式可评估 ElegantPaper https://ctan.org/pkg/elegantpaper 。
