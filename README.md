# 三千弱水 · 大学物理原创试题库

目标 10,000 道大学物理原创试题。当前共有 **100 道样板题（力学、电磁学、热学、振动与波动各17题；光学、近代物理各16题）**，全部仍为 **待独立复核**；仅完成部分自动公式一致性检测，不代表六轮质检通过。

## 2026-10-26 新版结构：ElegantBook 与独立 TeX

题目的唯一权威文字源为 bank/ID/question.tex 和 bank/ID/solution.tex，元数据为 bank/ID/meta.json（含题型、难度、知识点、答案和审核状态）。100题共拆分成300个文件。旧版 data/problems.json 仅保留为迁移前历史快照，后续新增题不需要编辑它。

tex/questions.tex 与 tex/solutions.tex 使用 ElegantBook 模板，通过 LaTeX 的 input 命令引用独立题源；后续按知识点筛选及系统组卷只需重排引用，不复制题面、不覆盖原题TeX。

## 开发与组卷命令

    python -m pip install -r requirements.txt
    python scripts/check_physics.py
    python scripts/build.py --check
    python scripts/build.py
    python scripts/render_single.py M001 --solutions
    python scripts/assemble_exam.py --count 8 --seed 20261026 --allow-pending

默认组卷**不使用待独立复核的题**；--allow-pending 仅允许内部测试。自动构建成功后，从 GitHub Actions Artifacts 下载最新 ElegantBook PDF。仓库 pdf/ 下的旧PDF是迁移前的版本，不代表新模板构建结果。

参见 [TeX独立化设计说明](docs/TEX_ARCHITECTURE.md)、[六轮质检协议](docs/QA_PROTOCOL.md)、[参考教材书目](docs/REFERENCES.md)。

## 下一阶段

完成100道首批样板题（首批100道样板题题量已达到目标），逐题增加原创性审查、独立解题复核、量纲/边界条件检查、考试难度配置；再扩展至1,000与10,000题。教材正文和高校真题尚未完整获授权核对，不能声称零重复。

## 2026-10-26 新增题（第3组）

新增12道：M007–M008、E007–E008、T007–T008、W007–W008、O007–O008、Q007–Q008。独立题干、解答与元数据均已入库；`scripts/check_physics.py` 增加12项对应公式核对。此检查需在 CI/运行环境执行，不能当作专家独立审稿；当前仍不开放正式考试选题。

### 六轮审核自动门禁

运行 `python scripts/check_review.py` 可以检查所有宣称「质检通过」题目的六轮证据记录、审核人字段、源文件SHA绑定。未建立真实审核凭证前不得改成通过。当前100道全部待审。审核凭证格式见 [qa/README.md](qa/README.md)。

### 历史质检文件说明

`data/qa_physics_spotchecks.json` 的36项结果仅是早期历史快照，不能据此判断现有100题整体已通过自动检查；`scripts/check_physics.py` 现含100道题的检验定义。完整仓库构建仍受GitHub Actions作业未启动问题影响。

## 2026-10-26 新增题（第4组）

新增12道：M009–M010、E009–E010、T009–T010、W009–W010、O009–O010、Q009–Q010；每题保留独立题干、解析和元数据。已扩展代数关系检查定义，但完整执行与ElegantBook PDF编译仍取决于仓库CI恢复。所有题目均处于待独立复核状态。

### 按考试需求组卷与质量报告

现支持 `--topic-quota`、`--kind`、`--max-minutes`、`--total-points` 等组卷约束。详见 [docs/EXAM_ASSEMBLY.md](docs/EXAM_ASSEMBLY.md)。完整物理公式检查运行时将结果写入暂存的 `generated/qa_physics_current.json`，不再覆盖已提交的36题历史质检快照；GitHub Actions能运行后，这份当前报告和试卷清单将上传为Artifacts。正式组卷仍需六轮真实审核凭证，自动校验不能替代独立学术复核。

## 2026-10-26 新增题（第5组）

新增12道：M011–M012、E011–E012、T011–T012、W011–W012、O011–O012、Q011–Q012。首次系统引入六道单项选择题和实验分析、填空题，并保留可机器读取的选项与标准答案。按独立TeX组织，不复制已有经典题目全文；所有72题均为待独立复核，不能作为正式试卷题目。程序化公式检查仍需在CI环境执行。

### 结构化单选题自检

选择题的 `meta.json` 中增加 `choices: [["A",...],..., ["D",...]]` 与 `correct_option`，脚本在构建时核查4个选项的顺序、答案映射及独立题干TeX选项内容。非选择题不会拥有选择题特有字段。汇总报告已更新为100题，但云端完整检查和ElegantBook编译依然标为尚未执行成功。

## 2026-10-26 新增题（第6组）

新增12道 M013–M014、E013–E014、T013–T014、W013–W014、O013–O014、Q013–Q014，六大模块各2道，覆盖临界滑动实验、磁通量变化与焦耳热、霍尔电压、稳态热传导、机械波正常模、光栅分辨本领、薄透镜测量、核反应能和狭义相对论速度合成等。全部保留单题独立TeX与元数据，尚未完成独立学术审核；云端编译状态以Actions为准。

## 首批100道题题量达成（2026-10-26）

第7组新增16道 M015–M017、E015–E017、T015–T017、W015–W017、O015–O016、Q015–Q016。总计100道、300份单题文件，覆盖6个物理模块。达到数量里程碑不等于质量验收通过：所有100道的六轮独立复核均未完成，且 GitHub Actions 最新运行未成功启动执行步骤；因此新版ElegantBook PDF暂未确认编译成功。全量100题的公式检查新增定义待成功运行。

## A0：首批100题完整性审计

运行 `python scripts/audit_milestone.py` 可检查每个模块覆盖、独立题源与试题册和解析册的引用、CSV题号一致性、自动核验定义与题号一一对应、题型/难度分布和审核状态。脚本在终端打印JSON，不生成本地交付文件。它**仅检验完整性和检验定义覆盖**，不能代替执行全量公式检查或六轮独立学术审稿。A0题量达到100道，但出版级审稿及新版ElegantBook PDF的CI编译仍未完成。

## 首批100题质量复盘（正在进行）

已新增 [第一轮问题筛查记录](docs/reviews/A0-round1-triage.md)，修正了T011数学排版并把T011、O016两道与既有题模高度重合的题目改写为不同模型；所有修改均保留稳定题号和单题独立TeX。这里的第一轮**只是筛查与修订，尚非100题逐题第一轮审核完成**；六轮审核批准仍为0题。当前CI仍未启动到具体测试及编译步骤。

### 修改后题目回归测试

已增加 `tests/test_revision_regressions.py` 对近期6道实质改写题进行结构、选项、主册索引和部分数值关系的防回归检查。可随既有 `python -m unittest discover -s tests -v` 调用，但 GitHub Actions 当前无法进入作业执行步骤，**尚无该测试成功运行的远端证据**。

### 解析册与单题答案绑定校验

`python scripts/audit_milestone.py` 现逐题比对两册ElegantBook的题名、题型、难度和解析册标准答案与 `bank/ID/meta.json` 是否一致；新增故意篡改题名和答案的负面测试。此校验检测生成文件同步错误，不能验证答案表达式在物理上是否正确。

首批100题条件充分性质检又修订了T001（明确隔板/容器热容忽略）与O003（明确空气折射率近似1），避免原答案受未给定物理参数影响；详见 `docs/reviews/A0-round1-independent-derivations.md`。

审核门禁的回归测试已修正：允许未来经真实六轮审核的题目由待复核升级为通过，仍强制校验审核记录和题源散列值，避免测试把审批状态永久锁死。

质检新增 `tests/test_physical_assumptions.py`，专门防止热学隔板热容、光学传播介质、同轴电容器储能单位等条件在编辑时被漏删，并对4道推导题做有限的独立代数一致性检查。GitHub Actions尚未成功执行该测试。

## 外部大学物理开源题源归档（2026-10-26）

- 已实际导入 **227份外部题源**：147份 [UBC OPBP](https://github.com/open-resources/physics_bank) Markdown、59份WeBWorK大学物理PG题源，另有21份WeBWorK热学PG题源。此前的 [WeBWorK OPL](https://github.com/openwebwork/webwork-open-problem-library) PG程序源。
- 已登记两大上游目录的 **1326条候选题源路径**（897+214+215），剩余1099条只是待抓取候选，**不可当作已拉取题目**。
- GitHub原始blob散列校验 **227/227 完全一致**，全量文件路径和状态参见 [外部题源目录](external_sources/CATALOG.md)。
- **与现有100道原创题严格分开**，外部题源全部未完成去重、答案复核、图片与PG依赖补齐及授权链核验，故目前没有任何外部题源被认定可正式组卷。
- 可用 `python scripts/sync_external_physics.py --source ubc_opbp --limit 20` 预览下一批题源；需要符合非商业许可证条件后才能加入真实下载参数。使用 `python scripts/external_inventory.py` 检查导入库存。

### 第三开放题源：热学

已将WeBWorK BrockPhysics《College Physics》13—15章中的21份热学题源实际归档，另登记该组215个候选PG文件路径；均保留了原作者、出处、原始Git版本和SHA，与前两来源一起进入227条 `external_sources/curation_queue.csv`。所有外部题仍待实际PG运行、配图与宏依赖核验、语义去重和授权范围确认，不自动加入正式组卷。
