# Irodov《普通物理学习题》中文版 · ElegantBook

底本：I. E. Irodov, *Problems in General Physics*，用户上传 Arihant 版 PDF（385 页）。
译注、补全推导以及本版勘误均属于研究用初稿；原书著作权与翻译、公开发行权归原权利人。

## 真实进度（2026-11-22）

- **2026-11-22 第四篇全覆盖自动质检程序续建：** 承接已检的 IV.1—50，新增四套独立物理/数值与源码一致性检查，逐段对应 IV.51—93（43题）、IV.94—149（56题）、IV.150—188（39题）、IV.189—224（36题），合计新增 **174个原书题号的源码覆盖**；连同既有 IV.1—50，第四篇 **224题均配置分段自动检查入口**。新增内容重点锁定物理摆、机械/电学阻尼共振、RLC 相量与初值、声波迟滞多普勒、声强积分、Maxwell方程、Poynting能流与偶极辐射。四套脚本已接入 GitHub Actions，但**运行通过与 PDF 回传须以对应最新工作流实际结果为准**；不宣称已完成逐题原版图像或专家二校。对应文件 `oscillations_mechanical_051_093_regression.py`、`oscillations_electric_094_149_regression.py`、`waves_elastic_150_188_regression.py`、`waves_electromagnetic_189_224_regression.py`，详细见 `quality-check.md`。**旧“2353项静态断言”口径为本轮扩展前的已记录基线，不应无依据累加。**


- **本轮新增：44题——第六篇6.6节核反应267—290题24道（本节完成），6.7节基本粒子291—310题20道（第六篇终题）。原书六篇所有题号至此已录入。**
- **累计：1878题——第一篇力学388题、第二篇热学257题、第三篇电动力学407题、第四篇振动与波动224题、第五篇光学292题、第六篇原子与核物理310题；六篇原书独立编号均完整覆盖。**
- **后续质检阶段：** 第六篇1—213题建立分章节数值复算回归，单独修订第14、130、138、195、196题的物理适用条件、线系歧义或图示；保持原书题数不变。
- **本轮严格质检扩展：** 第六篇214—310题追加3套数值/守恒律质检，第一篇1—58题追加1套，完善第六篇227、271、279、310题的推导和适用条件，总计517项独立回归；不额外造题。
- **2026-11-22 动力学与守恒律扩展：** 第一篇59—233题继续逐题检查，共引入3套力学回归程序（129+137+64项）；明确修订第一篇160题原书附加条件欠缺的质心公式，纠正195题对初始接触点的力矩归因。原有1878题编号不变。
- **2026-11-22 第一篇全覆盖深度复算：** 第一篇234—388题新增4套独立物理回归，刚体128项、弹性66项、流体63项、相对论103项，共360项；累计1207项自动检查，第一篇1—388题均有分章回归脚本。修订I.374牛顿速度近似1%误差精确阈值和I.312高剪应力下线弹性适用限制；原书可能欠定、答案冲突继续列入勘误。
- **2026-11-22 第二篇热学首批严格复算：** 重新独立核算第二篇1—61题的理想/非理想气体状态、真空抽气、重力/旋转气压分布、热力学第一定律、多方过程、范德瓦耳斯气体自由膨胀等，新增2套自动回归（61+76=137个静态断言点），既有累计基线1344项。
- **2026-11-22 第二篇62—257题严格质检继续完成：** 依据本版原始英文题面及书末答案逐章建立5套回归：分子运动学和麦克斯韦分布62—112（85处静态断言）、熵与循环113—159（70处）、液体表面张力160—184（51处）、相变185—219（61处）、分子输运及导热220—257（101处）。**新增共368处静态断言点，按既有口径累计1712处**；有循环测试，实际执行次数可更多。II.87经原书书末PDF第298页核实印为0.37K，正确为约363.3K，已更正正文并反代最概然速率。项目不新增超出原书的习题号。
- **2026-11-22 第三篇真空静电场1—53题同步质检：** 新增`electrostatics_vacuum_regression.py`，91处静态物理断言，验证库仑/万有引力比较、带电细线和球面分布、球壳/圆盘/偶极矩远场、高斯通量与泊松方程。已通过CI；连同第二篇62—257题新增368处，本轮新增**459处静态断言**，累计**1803处**。已记录III.1、10、17、18、25、36、40的书末系数、符号与近似数值疑点，已由物理积分或SI量纲反算核验。
- **2026-11-22 第三篇54—407题及第四篇1—50题深度复算：** 新增7套分章节自动物理回归，覆盖第三篇全部407题并推进第四篇前50题。III.73远场诱导偶极力幂次纠正为x⁻⁵，III.148水浸圆柱电容电流纠正为0.11mA，III.210质子束表面电场与轴心电势差纠正为16.8kV/m及41.9V。新增**550处静态物理断言**，累计**2353处**，测试实际通过以[最新CI](https://github.com/jackxiang0329-source/ruoshui-physics-bank/actions)为准，非2353道不同原题。原题总数仍为1878，下一批从第四篇51题及第五篇开始。
- 第 1.1 节“运动学”1—58 题已覆盖（全部）。
- 第 1.2 节“动力学基本方程”59—117 题已覆盖（全部）。
- 第 1.3 节“能量、动量与角动量守恒”118—199 题已覆盖（全部）。
- 第 1.4 节“万有引力”200—233 题已覆盖（全部）。
- 第 1.5 节“刚体动力学”234—289 题已覆盖（全部）。
- 第 1.6 节“固体弹性形变”290—314 题已覆盖（全部）。
- 第 1.7 节“流体动力学”315—339 题已覆盖（全部）。
- 第 1.8 节“相对论力学”340—388 题已覆盖（全部）。
- **第二篇“热力学与分子物理”从原书第1题重新编号。**
- 第 2.1 节“气体状态方程与过程”第1—25题已覆盖（全部）。
- 第 2.2 节“热力学第一定律与热容”第26—61题已覆盖（全部）。
- 第 2.3 节“气体分子运动论、玻尔兹曼与麦克斯韦分布”第62—112题已覆盖（全部）。
- 第 2.4 节“热力学第二定律与熵”第113—159题已覆盖（全部）。
- 第 2.5 节“液体与毛细现象”第160—184题已覆盖（全部）。
- 第 2.6 节“相变”第185—219题已覆盖（全部）。
- 第 2.7 节“输运现象”第220—257题已覆盖（全部），原书第二篇至此结束。
- **原书第三篇“电动力学”从第1题重新编号。**
- 第 3.1 节“真空中的恒定电场”第1—53题已覆盖（全部）。
- 第 3.2 节“静电场中的导体与电介质”第54—100题已覆盖（全部）。
- 第 3.3 节“电容与电场能”第101—146题已覆盖（全部）。
- 第 3.4 节“恒定电流”第147—218题已覆盖（全部）。
- 第 3.5 节“恒定磁场与磁介质”第219—287题已覆盖（全部）。
- 第 3.6 节“电磁感应与麦克斯韦方程”第288—371题已覆盖（全部）。
- 第 3.7 节“带电粒子在电场和磁场中的运动”第372—407题已覆盖（全部），第三篇完结。
- **原书第四篇“振动与波动”再次从第1题独立编号。**
- 第 4.1 节“机械振动”第1—93题已覆盖（全部）。
- 第 4.2 节“电振荡”第94—149题已覆盖（全部）。
- 第 4.3 节“弹性波与声学”第150—188题已覆盖（全部）。
- 第 4.4 节“电磁波与辐射”第189—224题已覆盖（全部）；第四篇全部完成。
- **第五篇“光学”从第1题重新编号。**
- 第 5.1 节“光度学与几何光学”第1—63题已覆盖（全部）。
- 第 5.2 节“光的干涉”第64—96题已覆盖（全部）。
- 第 5.3 节“光的衍射”第97—156题已覆盖（全部）。
- 第 5.4 节“光的偏振”第157—199题已覆盖（全部）。
- 第 5.5 节“光的色散与吸收”第200—223题已覆盖（全部）。
- 第 5.6 节“运动光源的光学”第224—245题已覆盖（全部）。
- 第 5.7 节“热辐射与光的量子性质”第246—292题已覆盖（全部）；第五篇光学全部完成。
- **第六篇“原子与核物理”重新从第1题独立编号。**
- 第 6.1 节“散射、卢瑟福—玻尔原子”第1—48题已覆盖（全部）。
- 第 6.2 节“粒子的波动性质与薛定谔方程”第49—96题已覆盖（全部）。
- 第 6.3 节“原子性质与光谱”第97—166题已覆盖（全部）。
- 第 6.4 节“分子与晶体”第167—213题已覆盖（全部）。
- 第 6.5 节“放射性”第214—248题已覆盖（全部）。
- 第 6.6 节“核反应”第249—290题已覆盖（全部）。
- 第 6.7 节“基本粒子”第291—310题已覆盖（全部，原书终题）。
- **下一步严格质检接续点：** 第三篇电动力学第54—407题逐章独立复算，再推进第四篇和第五篇；全书1878道原题均已录入。
- **全书1878题翻译与解析录入已经完成；独立学术二校尚未完成。** 第一篇388题与第六篇310题已建立分章物理回归；第二至第五篇仍须审校。任何“编译成功”仅说明技术排版通过。

| 内容 | 文件 |
|---|---|
| ElegantBook 中文主文件 | [main.tex](main.tex) |
| 1—20题 | [01-mechanics-kinematics-001-020.tex](chapters/01-mechanics-kinematics-001-020.tex) |
| 21—30题 | [01-mechanics-kinematics-021-030.tex](chapters/01-mechanics-kinematics-021-030.tex) |
| 31—40题 | [01-mechanics-kinematics-031-040.tex](chapters/01-mechanics-kinematics-031-040.tex) |
| 41—50题 | [01-mechanics-kinematics-041-050.tex](chapters/01-mechanics-kinematics-041-050.tex) |
| 51—58题 | [01-mechanics-kinematics-051-058.tex](chapters/01-mechanics-kinematics-051-058.tex) |
| 59—70题 | [02-mechanics-dynamics-059-070.tex](chapters/02-mechanics-dynamics-059-070.tex) |
| 71—80题 | [02-mechanics-dynamics-071-080.tex](chapters/02-mechanics-dynamics-071-080.tex) |
| 81—90题 | [02-mechanics-dynamics-081-090.tex](chapters/02-mechanics-dynamics-081-090.tex) |
| 91—100题 | [02-mechanics-dynamics-091-100.tex](chapters/02-mechanics-dynamics-091-100.tex) |
| 101—110题 | [02-mechanics-dynamics-101-110.tex](chapters/02-mechanics-dynamics-101-110.tex) |
| 111—117题 | [02-mechanics-dynamics-111-117.tex](chapters/02-mechanics-dynamics-111-117.tex) |
| 118—120题 | [03-mechanics-conservation-118-120.tex](chapters/03-mechanics-conservation-118-120.tex) |
| 121—130题 | [03-mechanics-conservation-121-130.tex](chapters/03-mechanics-conservation-121-130.tex) |
| 131—140题 | [03-mechanics-conservation-131-140.tex](chapters/03-mechanics-conservation-131-140.tex) |
| 141—150题 | [03-mechanics-conservation-141-150.tex](chapters/03-mechanics-conservation-141-150.tex) |
| 151—160题 | [03-mechanics-conservation-151-160.tex](chapters/03-mechanics-conservation-151-160.tex) |
| 161—170题 | [03-mechanics-conservation-161-170.tex](chapters/03-mechanics-conservation-161-170.tex) |
| 171—180题 | [03-mechanics-conservation-171-180.tex](chapters/03-mechanics-conservation-171-180.tex) |
| 181—190题 | [03-mechanics-conservation-181-190.tex](chapters/03-mechanics-conservation-181-190.tex) |
| 191—199题 | [03-mechanics-conservation-191-199.tex](chapters/03-mechanics-conservation-191-199.tex) |
| 200—210题 | [04-gravitation-200-210.tex](chapters/04-gravitation-200-210.tex) |
| 211—220题 | [04-gravitation-211-220.tex](chapters/04-gravitation-211-220.tex) |
| 221—233题 | [04-gravitation-221-233.tex](chapters/04-gravitation-221-233.tex) |
| 234—240题 | [05-rigid-body-234-240.tex](chapters/05-rigid-body-234-240.tex) |
| 241—250题 | [05-rigid-body-241-250.tex](chapters/05-rigid-body-241-250.tex) |
| 251—260题 | [05-rigid-body-251-260.tex](chapters/05-rigid-body-251-260.tex) |
| 261—270题 | [05-rigid-body-261-270.tex](chapters/05-rigid-body-261-270.tex) |
| 271—280题 | [05-rigid-body-271-280.tex](chapters/05-rigid-body-271-280.tex) |
| 281—289题 | [05-rigid-body-281-289.tex](chapters/05-rigid-body-281-289.tex) |
| 290题 | [06-elasticity-290-290.tex](chapters/06-elasticity-290-290.tex) |
| 291—300题 | [06-elasticity-291-300.tex](chapters/06-elasticity-291-300.tex) |
| 301—310题 | [06-elasticity-301-310.tex](chapters/06-elasticity-301-310.tex) |
| 311—314题 | [06-elasticity-311-314.tex](chapters/06-elasticity-311-314.tex) |
| 315—324题 | [07-hydrodynamics-315-324.tex](chapters/07-hydrodynamics-315-324.tex) |
| 325—334题 | [07-hydrodynamics-325-334.tex](chapters/07-hydrodynamics-325-334.tex) |
| 335—339题 | [07-hydrodynamics-335-339.tex](chapters/07-hydrodynamics-335-339.tex) |
| 340—350题 | [08-relativity-340-350.tex](chapters/08-relativity-340-350.tex) |
| 351—360题 | [08-relativity-351-360.tex](chapters/08-relativity-351-360.tex) |
| 第一篇361—370题 | [08-relativity-361-370.tex](chapters/08-relativity-361-370.tex) |
| 第一篇371—380题 | [08-relativity-371-380.tex](chapters/08-relativity-371-380.tex) |
| 第一篇381—388题 | [08-relativity-381-388.tex](chapters/08-relativity-381-388.tex) |
| 第二篇2.1节1—11题 | [09-thermo-state-001-011.tex](chapters/09-thermo-state-001-011.tex) |
| 第二篇2.1节12—20题 | [09-thermo-state-012-020.tex](chapters/09-thermo-state-012-020.tex) |
| 第二篇2.1节21—25题 | [09-thermo-state-021-025.tex](chapters/09-thermo-state-021-025.tex) |
| 第二篇2.2节26—35题 | [10-thermo-first-law-026-035.tex](chapters/10-thermo-first-law-026-035.tex) |
| 第二篇2.2节36—45题 | [10-thermo-first-law-036-045.tex](chapters/10-thermo-first-law-036-045.tex) |
| 第二篇2.2节46—56题 | [10-thermo-first-law-046-056.tex](chapters/10-thermo-first-law-046-056.tex) |
| 第二篇2.2节57—61题 | [10-thermo-first-law-057-061.tex](chapters/10-thermo-first-law-057-061.tex) |
| 第二篇2.3节62—72题 | [11-kinetic-theory-062-072.tex](chapters/11-kinetic-theory-062-072.tex) |
| 第二篇2.3节73—83题 | [11-kinetic-theory-073-083.tex](chapters/11-kinetic-theory-073-083.tex) |
| 第二篇2.3节84—94题 | [11-kinetic-theory-084-094.tex](chapters/11-kinetic-theory-084-094.tex) |
| 第二篇2.3节95—103题 | [11-kinetic-theory-095-103.tex](chapters/11-kinetic-theory-095-103.tex) |
| 第二篇2.3节104—112题 | [11-kinetic-theory-104-112.tex](chapters/11-kinetic-theory-104-112.tex) |
| 第二篇2.4节113—121题 | [12-entropy-cycles-113-121.tex](chapters/12-entropy-cycles-113-121.tex) |
| 第二篇2.4节122—129题 | [12-entropy-cycles-122-129.tex](chapters/12-entropy-cycles-122-129.tex) |
| 第二篇2.4节130—139题 | [12-entropy-cycles-130-139.tex](chapters/12-entropy-cycles-130-139.tex) |
| 第二篇2.4节140—145题 | [12-entropy-cycles-140-145.tex](chapters/12-entropy-cycles-140-145.tex) |
| 第二篇2.4节146—159题 | [12-entropy-cycles-146-159.tex](chapters/12-entropy-cycles-146-159.tex) |
| 第二篇2.5节160—169题 | [13-capillarity-160-169.tex](chapters/13-capillarity-160-169.tex) |
| 第二篇2.5节170—179题 | [13-capillarity-170-179.tex](chapters/13-capillarity-170-179.tex) |
| 第二篇2.5节180—184题 | [13-capillarity-180-184.tex](chapters/13-capillarity-180-184.tex) |
| 第二篇2.6节185—194题 | [14-phase-transformations-185-194.tex](chapters/14-phase-transformations-185-194.tex) |
| 第二篇2.6节195—204题 | [14-phase-transformations-195-204.tex](chapters/14-phase-transformations-195-204.tex) |
| 第二篇2.6节205—214题 | [14-phase-transformations-205-214.tex](chapters/14-phase-transformations-205-214.tex) |
| 第二篇2.6节215—219题 | [14-phase-transformations-215-219.tex](chapters/14-phase-transformations-215-219.tex) |
| 第二篇2.7节220—229题 | [15-transport-220-229.tex](chapters/15-transport-220-229.tex) |
| 第二篇2.7节230—239题 | [15-transport-230-239.tex](chapters/15-transport-230-239.tex) |
| 第二篇2.7节240—245题 | [15-transport-240-245.tex](chapters/15-transport-240-245.tex) |
| 第二篇2.7节246—257题 | [15-transport-246-257.tex](chapters/15-transport-246-257.tex) |
| 第三篇3.1节1—12题 | [16-electrostatics-vacuum-001-012.tex](chapters/16-electrostatics-vacuum-001-012.tex) |
| 第三篇3.1节13—27题 | [16-electrostatics-vacuum-013-027.tex](chapters/16-electrostatics-vacuum-013-027.tex) |
| 第三篇3.1节28—40题 | [16-electrostatics-vacuum-028-040.tex](chapters/16-electrostatics-vacuum-028-040.tex) |
| 第三篇3.1节41—53题 | [16-electrostatics-vacuum-041-053.tex](chapters/16-electrostatics-vacuum-041-053.tex) |
| 第三篇3.2节54—65题 | [17-electro-conductors-054-065.tex](chapters/17-electro-conductors-054-065.tex) |
| 第三篇3.2节66—77题 | [17-electro-conductors-066-077.tex](chapters/17-electro-conductors-066-077.tex) |
| 第三篇3.2节78—88题 | [17-electro-conductors-078-088.tex](chapters/17-electro-conductors-078-088.tex) |
| 第三篇3.2节89—100题 | [17-electro-conductors-089-100.tex](chapters/17-electro-conductors-089-100.tex) |
| 第三篇3.3节101—112题 | [18-capacitance-energy-101-112.tex](chapters/18-capacitance-energy-101-112.tex) |
| 第三篇3.3节113—121题 | [18-capacitance-energy-113-121.tex](chapters/18-capacitance-energy-113-121.tex) |
| 第三篇3.3节122—130题 | [18-capacitance-energy-122-130.tex](chapters/18-capacitance-energy-122-130.tex) |
| 第三篇3.3节131—140题 | [18-capacitance-energy-131-140.tex](chapters/18-capacitance-energy-131-140.tex) |
| 第三篇3.3节141—146题 | [18-capacitance-energy-141-146.tex](chapters/18-capacitance-energy-141-146.tex) |
| 第三篇3.4节147—160题 | [19-electric-current-147-160.tex](chapters/19-electric-current-147-160.tex) |
| 第三篇3.4节161—175题 | [19-electric-current-161-175.tex](chapters/19-electric-current-161-175.tex) |
| 第三篇3.4节176—188题 | [19-electric-current-176-188.tex](chapters/19-electric-current-176-188.tex) |
| 第三篇3.4节189—200题 | [19-electric-current-189-200.tex](chapters/19-electric-current-189-200.tex) |
| 第三篇3.4节201—218题 | [19-electric-current-201-218.tex](chapters/19-electric-current-201-218.tex) |
| 第三篇3.5节219—235题 | [20-magnetostatics-219-235.tex](chapters/20-magnetostatics-219-235.tex) |
| 第三篇3.5节236—250题 | [20-magnetostatics-236-250.tex](chapters/20-magnetostatics-236-250.tex) |
| 第三篇3.5节251—262题 | [20-magnetostatics-251-262.tex](chapters/20-magnetostatics-251-262.tex) |
| 第三篇3.5节263—274题 | [20-magnetostatics-263-274.tex](chapters/20-magnetostatics-263-274.tex) |
| 第三篇3.5节275—287题 | [20-magnetostatics-275-287.tex](chapters/20-magnetostatics-275-287.tex) |
| 第三篇3.6节288题 | [21-induction-288-288.tex](chapters/21-induction-288-288.tex) |
| 第三篇3.6节289—304题 | [21-induction-289-304.tex](chapters/21-induction-289-304.tex) |
| 第三篇3.6节305—322题 | [21-induction-305-322.tex](chapters/21-induction-305-322.tex) |
| 第三篇3.6节323—346题 | [21-induction-323-346.tex](chapters/21-induction-323-346.tex) |
| 第三篇3.6节347—371题 | [21-induction-347-371.tex](chapters/21-induction-347-371.tex) |
| 第三篇3.7节372—388题 | [22-charged-particles-372-388.tex](chapters/22-charged-particles-372-388.tex) |
| 第三篇3.7节389—407题（本篇完结） | [22-charged-particles-389-407.tex](chapters/22-charged-particles-389-407.tex) |
| 第四篇4.1节1—20题 | [23-mechanical-oscillations-001-020.tex](chapters/23-mechanical-oscillations-001-020.tex) |
| 第四篇4.1节21—33题 | [23-mechanical-oscillations-021-033.tex](chapters/23-mechanical-oscillations-021-033.tex) |
| 第四篇4.1节34—50题 | [23-mechanical-oscillations-034-050.tex](chapters/23-mechanical-oscillations-034-050.tex) |
| 第四篇4.1节51—65题 | [23-mechanical-oscillations-051-065.tex](chapters/23-mechanical-oscillations-051-065.tex) |
| 第四篇4.1节66—81题 | [23-mechanical-oscillations-066-081.tex](chapters/23-mechanical-oscillations-066-081.tex) |
| 第四篇4.1节82—93题（机械振动完结） | [23-mechanical-oscillations-082-093.tex](chapters/23-mechanical-oscillations-082-093.tex) |
| 第四篇4.2节94—109题 | [24-electric-oscillations-094-109.tex](chapters/24-electric-oscillations-094-109.tex) |
| 第四篇4.2节110—125题 | [24-electric-oscillations-110-125.tex](chapters/24-electric-oscillations-110-125.tex) |
| 第四篇4.2节126—137题 | [24-electric-oscillations-126-137.tex](chapters/24-electric-oscillations-126-137.tex) |
| 第四篇4.2节138—149题（电振荡完结） | [24-electric-oscillations-138-149.tex](chapters/24-electric-oscillations-138-149.tex) |
| 第四篇4.3节150—165题 | [25-elastic-waves-150-165.tex](chapters/25-elastic-waves-150-165.tex) |
| 第四篇4.3节166—181题 | [25-elastic-waves-166-181.tex](chapters/25-elastic-waves-166-181.tex) |
| 第四篇4.3节182—188题（声学完结） | [25-elastic-waves-182-188.tex](chapters/25-elastic-waves-182-188.tex) |
| 第四篇4.4节189—200题 | [26-em-waves-189-200.tex](chapters/26-em-waves-189-200.tex) |
| 第四篇4.4节201—212题 | [26-em-waves-201-212.tex](chapters/26-em-waves-201-212.tex) |
| 第四篇4.4节213—224题（第四篇完结） | [26-em-waves-213-224.tex](chapters/26-em-waves-213-224.tex) |
| 第五篇5.1节1—12题 | [27-optics-photometry-001-012.tex](chapters/27-optics-photometry-001-012.tex) |
| 第五篇5.1节13—25题 | [27-optics-photometry-013-025.tex](chapters/27-optics-photometry-013-025.tex) |
| 第五篇5.1节26—35题 | [27-optics-photometry-026-035.tex](chapters/27-optics-photometry-026-035.tex) |
| 第五篇5.1节36—45题 | [27-optics-photometry-036-045.tex](chapters/27-optics-photometry-036-045.tex) |
| 第五篇5.1节46—57题 | [27-optics-photometry-046-057.tex](chapters/27-optics-photometry-046-057.tex) |
| 第五篇5.1节58—63题（几何光学完结） | [27-optics-photometry-058-063.tex](chapters/27-optics-photometry-058-063.tex) |
| 第五篇5.2节64—75题 | [28-optics-interference-064-075.tex](chapters/28-optics-interference-064-075.tex) |
| 第五篇5.2节76—86题 | [28-optics-interference-076-086.tex](chapters/28-optics-interference-076-086.tex) |
| 第五篇5.2节87—96题（干涉完结） | [28-optics-interference-087-096.tex](chapters/28-optics-interference-087-096.tex) |
| 第五篇5.3节97—108题 | [29-optics-diffraction-097-108.tex](chapters/29-optics-diffraction-097-108.tex) |
| 第五篇5.3节109—118题 | [29-optics-diffraction-109-118.tex](chapters/29-optics-diffraction-109-118.tex) |
| 第五篇5.3节119—130题 | [29-optics-diffraction-119-130.tex](chapters/29-optics-diffraction-119-130.tex) |
| 第五篇5.3节131—142题 | [29-optics-diffraction-131-142.tex](chapters/29-optics-diffraction-131-142.tex) |
| 第五篇5.3节143—150题 | [29-optics-diffraction-143-150.tex](chapters/29-optics-diffraction-143-150.tex) |
| 第五篇5.3节151—156题（衍射完结） | [29-optics-diffraction-151-156.tex](chapters/29-optics-diffraction-151-156.tex) |
| 第五篇5.4节157题（偏振开始） | [30-optics-polarization-157-157.tex](chapters/30-optics-polarization-157-157.tex) |
| 第五篇5.4节158—175题 | [30-optics-polarization-158-175.tex](chapters/30-optics-polarization-158-175.tex) |
| 第五篇5.4节176—199题（偏振完结） | [30-optics-polarization-176-199.tex](chapters/30-optics-polarization-176-199.tex) |
| 第五篇5.5节200—215题 | [31-optics-dispersion-200-215.tex](chapters/31-optics-dispersion-200-215.tex) |
| 第五篇5.5节216—223题（色散与吸收完结） | [31-optics-dispersion-216-223.tex](chapters/31-optics-dispersion-216-223.tex) |
| 第五篇5.6节224—245题（运动光源光学完结） | [32-moving-optics-224-245.tex](chapters/32-moving-optics-224-245.tex) |
| 第五篇5.7节246—257题 | [33-thermal-radiation-246-257.tex](chapters/33-thermal-radiation-246-257.tex) |
| 第五篇5.7节258—268题 | [33-thermal-radiation-258-268.tex](chapters/33-thermal-radiation-258-268.tex) |
| 第五篇5.7节269—280题 | [33-thermal-radiation-269-280.tex](chapters/33-thermal-radiation-269-280.tex) |
| 第五篇5.7节281—292题（光学完结） | [33-thermal-radiation-281-292.tex](chapters/33-thermal-radiation-281-292.tex) |
| 第六篇6.1节1—18题 | [34-atomic-scattering-001-018.tex](chapters/34-atomic-scattering-001-018.tex) |
| 第六篇6.1节19—32题 | [34-atomic-scattering-019-032.tex](chapters/34-atomic-scattering-019-032.tex) |
| 第六篇6.1节33—48题（6.1节完结） | [34-atomic-scattering-033-048.tex](chapters/34-atomic-scattering-033-048.tex) |
| 第六篇6.2节49—65题 | [35-wave-properties-049-065.tex](chapters/35-wave-properties-049-065.tex) |
| 第六篇6.2节66—80题 | [35-wave-properties-066-080.tex](chapters/35-wave-properties-066-080.tex) |
| 第六篇6.2节81—96题（本节完成） | [35-wave-properties-081-096.tex](chapters/35-wave-properties-081-096.tex) |
| 第六篇6.3节97—104题 | [36-atomic-spectra-097-104.tex](chapters/36-atomic-spectra-097-104.tex) |
| 第六篇6.3节105—117题 | [36-atomic-spectra-105-117.tex](chapters/36-atomic-spectra-105-117.tex) |
| 第六篇6.3节118—134题 | [36-atomic-spectra-118-134.tex](chapters/36-atomic-spectra-118-134.tex) |
| 第六篇6.3节135—147题 | [36-atomic-spectra-135-147.tex](chapters/36-atomic-spectra-135-147.tex) |
| 第六篇6.3节148—158题 | [36-atomic-spectra-148-158.tex](chapters/36-atomic-spectra-148-158.tex) |
| 第六篇6.3节159—166题（本节完成） | [36-atomic-spectra-159-166.tex](chapters/36-atomic-spectra-159-166.tex) |
| 第六篇6.4节167—180题 | [37-molecules-crystals-167-180.tex](chapters/37-molecules-crystals-167-180.tex) |
| 第六篇6.4节181—196题 | [37-molecules-crystals-181-196.tex](chapters/37-molecules-crystals-181-196.tex) |
| 第六篇6.4节197—213题（本节完成） | [37-molecules-crystals-197-213.tex](chapters/37-molecules-crystals-197-213.tex) |
| 第六篇6.5节214—226题 | [38-radioactivity-214-226.tex](chapters/38-radioactivity-214-226.tex) |
| 第六篇6.5节227—237题 | [38-radioactivity-227-237.tex](chapters/38-radioactivity-227-237.tex) |
| 第六篇6.5节238—248题（本节完成） | [38-radioactivity-238-248.tex](chapters/38-radioactivity-238-248.tex) |
| 第六篇6.6节249—258题 | [39-nuclear-reactions-249-258.tex](chapters/39-nuclear-reactions-249-258.tex) |
| 第六篇6.6节259—266题 | [39-nuclear-reactions-259-266.tex](chapters/39-nuclear-reactions-259-266.tex) |
| 第六篇6.6节267—280题 | [39-nuclear-reactions-267-280.tex](chapters/39-nuclear-reactions-267-280.tex) |
| 第六篇6.6节281—290题（本节完成） | [39-nuclear-reactions-281-290.tex](chapters/39-nuclear-reactions-281-290.tex) |
| 第六篇6.7节291—300题 | [40-elementary-particles-291-300.tex](chapters/40-elementary-particles-291-300.tex) |
| 第六篇6.7节301—310题（原书终题） | [40-elementary-particles-301-310.tex](chapters/40-elementary-particles-301-310.tex) |
| 源书勘误 | [errata.md](errata.md) |
| 技术与学术质检记录 | [quality-check.md](quality-check.md) |
| 结构完整性检查 | [check_sources.py](check_sources.py) |

## 编译

在此目录内依次运行结构检查、逐题检查、物理数值回归和PDF构建：

    python3 check_sources.py
    python3 lint_problems.py
    python3 numeric_regression.py
    python3 atomic_scattering_regression.py
    python3 wave_quantum_regression.py
    python3 spectra_molecules_regression.py
    python3 radioactivity_deep_regression.py
    python3 nuclear_reactions_deep_regression.py
    python3 particles_conservation_regression.py
    python3 mechanics_kinematics_regression.py
    python3 mechanics_dynamics_regression.py
    python3 mechanics_conservation_regression.py
    python3 mechanics_gravitation_regression.py
    python3 mechanics_rigidbody_regression.py
    python3 mechanics_elasticity_regression.py
    python3 mechanics_fluids_regression.py
    python3 mechanics_relativity_regression.py
    python3 thermo_state_regression.py
    python3 thermo_firstlaw_regression.py
    python3 thermo_kinetic_regression.py
    python3 thermo_entropy_regression.py
    python3 thermo_capillarity_regression.py
    python3 thermo_phase_regression.py
    python3 thermo_transport_regression.py
    python3 electrostatics_vacuum_regression.py
    python3 electro_conductors_regression.py
    python3 electro_capacitance_regression.py
    python3 electro_current_regression.py
    python3 electro_magnetostatics_regression.py
    python3 electro_induction_regression.py
    python3 electro_charged_regression.py
    python3 oscillations_mechanical_regression.py
    python3 oscillations_mechanical_051_093_regression.py
    python3 oscillations_electric_094_149_regression.py
    python3 waves_elastic_150_188_regression.py
    python3 waves_electromagnetic_189_224_regression.py
    bash build.sh

- `check_sources.py`：验证原书六篇独立编号1,878题及164份章节来源；
- `lint_problems.py`：把各TeX章分割为独立习题，逐题检查中文题面、推导和核验标记的完整性及顺序，并提示数学环境疑点；
- `numeric_regression.py`：独立于正文重算37项高风险物理数值（原子与核物理，覆盖反冲、阈值、放射性及粒子衰变等）；
- `atomic_scattering_regression.py`：对第六篇1—48题的卢瑟福散射、玻尔原子、氢谱系及原子反冲开展独立数值回归，并核查一次散射近似条件；
- `wave_quantum_regression.py`：对第六篇49—96题的德布罗意波、相对论校正、不确定原理、束缚态归一化、势阱能级和WKB主指数做独立回归；
- `spectra_molecules_regression.py`：对第六篇97—213题的原子光谱、磁矩、Debye晶体、费米电子及本征半导体数值做独立回归；
- `radioactivity_deep_regression.py`：对第六篇214—248题再做58项衰变链、指数拟合、β与γ反冲计算；其中第227题量化书末拟合差异；
- `nuclear_reactions_deep_regression.py`：对第六篇249—290题再做86项核质量、反应能、阈值、激活及反应堆计算，包含精确相对论阈值校正；
- `particles_conservation_regression.py`：对第六篇291—310题做49项粒子衰变阈值及电荷/重子数/奇异数/分味轻子数守恒检查；
- `mechanics_kinematics_regression.py`：对第一篇1—58题做80项参考系、轨迹、角加速度及滚动运动复算；
- `mechanics_dynamics_regression.py`：对第一篇59—117题逐题验证牛顿方程、摩擦阈值、两级滑轮/楔块约束、非惯性参考系等，新增129项数值与平衡残差检查；
- `mechanics_conservation_regression.py`：对第一篇118—199题核对功与能量、质心、碰撞、变质量系统及转矩/角动量，新增137项独立复算；
- `mechanics_gravitation_regression.py`：对第一篇200—233题核对开普勒轨道、引力势、壳层定理、地月卫星轨道及逃逸阈值，新增64项独立复算；
- `mechanics_rigidbody_regression.py`：第一篇234—289题128项，跨检查力矩、转动惯量、无滑动约束、刚体碰撞和陀螺进动；
- `mechanics_elasticity_regression.py`：第一篇290—314题66项，独立检查热应力、弹性本构、弯曲、扭转与形变能；
- `mechanics_fluids_regression.py`：第一篇315—339题63项，流管压强/流量、动量通量、黏性剪切、雷诺数和Stokes模型；
- `mechanics_relativity_regression.py`：第一篇340—388题103项，洛伦兹速度/同时性、固有加速度、四动量与相对论碰撞；
- `thermo_state_regression.py`：第二篇1—25题61项独立复核，包含双容器活塞、混合气、指数气压和范德瓦耳斯稳定性；
- `thermo_firstlaw_regression.py`：第二篇26—61题76项复核，包含热量/外功符号、多方过程、路径热容及向真空自由膨胀；
- `thermo_kinetic_regression.py`：第二篇62—112题85处静态物理断言：分子碰壁动量、麦克斯韦速率/能量概率密度、归一化、沉降与分子势；回归锁定第87题约363.3K；
- `thermo_entropy_regression.py`：第二篇113—159题70处：三热源循环、卡诺/Otto/Brayton/Stirling/Ericsson效率、可逆/不可逆熵、二项涨落；
- `thermo_capillarity_regression.py`：第二篇160—184题51处：单/双界面Laplace压强、润湿液桥、液面曲率、表面自由能与表面熵；
- `thermo_phase_regression.py`：第二篇185—219题61处：汽化/冷凝、克拉佩龙方程、范德瓦耳斯临界点、三相点、量热器及多阶段熵；
- `thermo_transport_regression.py`：第二篇220—257题101处：自由程、碰撞配对计数、分子逸出、气体黏性/扩散、泊肃叶流、傅里叶导热及圆柱/球热方程；
- `electrostatics_vacuum_regression.py`：第三篇1—53题91处静态断言，场与引力基本常数、高斯定律、有限带电体积分、球/圆柱空腔、电偶极近场/远场、梯度与泊松方程；
- electro_conductors_regression.py：第三篇54—100题87处镜像、介质和边界条件复算；
- electro_capacitance_regression.py：第三篇101—146题72处电容与能量复算；
- electro_current_regression.py：第三篇147—218题101处电路、电流和质子束复算；
- electro_magnetostatics_regression.py：第三篇219—287题82处磁静力与霍尔复算；
- electro_induction_regression.py：第三篇288—371题90处磁感应、RL与场变换复算；
- electro_charged_regression.py：第三篇372—407题53处带电粒子和加速器复算；
- oscillations_mechanical_regression.py：第四篇1—50题65处谐振动、弹簧、物理摆与勘误复算；
- oscillations_mechanical_051_093_regression.py：第四篇51—93题43个完整源码块及机械振动、阻尼和受迫共振独立约束；
- oscillations_electric_094_149_regression.py：第四篇94—149题56个完整源码块及LC/RLC初值、相量、能量、频率与阻尼模型复核；
- waves_elastic_150_188_regression.py：第四篇150—188题39个完整源码块及声波传播、驻波、多普勒迟滞、声强和几何能流独立约束；
- waves_electromagnetic_189_224_regression.py：第四篇189—224题36个完整源码块及位移电流、Maxwell/Poynting守恒、辐射和汤姆孙截面复核；
- **历史基线说明：** 第一篇1—233题及第六篇重点回归基线847项已获前期CI验收；最新累计统计请见下条，不要把基线误当全部项目检查数。
- **代码静态物理回归断言累计1803处：** 历史1344处 + 第二篇62—257题新增368处 + 第三篇1—53题新增91处；个别测试循环执行多次。1803不是不同习题数，也不能代替原书全部1878题的独立专家终审。详见 [质检记录](quality-check.md)。
- 这些门禁只能验证结构与已选的回归结果，不能代替全书逐题独立物理学二校。

需要 XeLaTeX、latexmk、TikZ 与 ElegantBook 4.7。
构建顺序为 cover.tex → main.tex。
GitHub Actions 工作流 .github/workflows/irodov-elegantbook.yml
运行源码覆盖检查、XeLaTeX 编译，上传 PDF 附件；
构建成功后尝试把 main.pdf、cover.pdf 回传当前仓库。
仅当工作流成功且 PDF 文件版本已更新，才应报告 PDF 已同步。

## 仓库隔离

本目录放在 external_sources/，不得将翻译题目混入
大学物理原创高难度题库 bank/ 的题数和质量门禁，也不修改它们的权威源文件。
原书六篇及各小节全部按原书题号译注录入，后续应进行独立物理二校、版式检查、插图补绘和勘误整理，而不是重复向原书编号后续造题。各篇独立编号保留，不覆盖历史章节及题解。
