# Irodov《普通物理学习题》中文版 · ElegantBook

底本：I. E. Irodov, *Problems in General Physics*，用户上传 Arihant 版 PDF（385 页）。
译注、补全推导以及本版勘误均属于研究用初稿；原书著作权与翻译、公开发行权归原权利人。

## 2026-11-24 全仓库精简（无损合并）

**兼容旧质检**：仓库只跟踪40份合并后的TeX章节。历史专项回归程序仍引用拆分时期的文件名，GitHub Actions 会先运行 `python3 textbooks/irodov/expand_legacy_fragments.py`，从章节中的 BEGIN/END 标记恢复164份**仅供本次工作区验证**的未跟踪片段，并逐一验证原 Git blob SHA；这些临时文件不会提交到GitHub。单独运行历史回归脚本前也可执行一次此命令。


原来164份分批次LaTeX片段按原书40个小节合成40份，净减124份；每个新文件保留原始内容和blob SHA注释。1,878道独立题号、题解、校核段均维持原顺序。原文件与新章节对应表：[COMPACTION-MAP.md](chapters/compaction_map.md)。Git历史可恢复原文件。

## 真实进度（2026-11-22）

- **跨版本物理严格复核第三轮：** 针对 II.162 肥皂泡$n/\eta$、V.139 光栅10.0mm/10.0m、V.140 波长670.8nm/mm、V.142 焦平面近轴/精确几何及 V.254 Wien频谱 $\omega^3/\omega^2$，重新核定有物理解的主分支并完整保留此前记录的扫描字面差异。更新5处题解，新增 `cross_edition_physics_regression.py` 独立的等温气体、瑞利分辨、谱密度雅可比/数值积分与峰位核验，正式接入 Actions。**不增加独立题目数；公开版本的原题转录不能代替对用户上传扫描页的重新逐图校核。** 具体见 `quality_check.md`、`errata.md`。

- **第六篇原子/核物理 VI.1—310 五套二次独立质检：** 在既有物理回归上新增五套来源题号锁定的源码/数值物理测试，覆盖VI.1—48（48题）、49—96（48题）、97—166（70题）、167—213（47题）、214—310（97题），合计第六篇 **310/310题均有题号、题面、解答及校核段程序验证**，含Rutherford角积分、WKB、原子量子数、Debye/Fermi数值与核守恒。**纠正VI.173转动能级密度漏写因子2、VI.201费米面平均态间距简式漏写因子3π²（正确约8.96×10⁻²³eV）**，补强VI.108的LS耦合校核文本。新增五套专项在 [GitHub Actions 44973097071](https://github.com/jackxiang0329-source/ruoshui-physics-bank/actions/runs/44973097071) 成功；整书编译和PDF回传需以最后最新CI结果为准。**310/310题结构覆盖不等于310题全部逐式专家二校或原书插图逐页核验。** 详见quality_check.md和errata.md。


- **第五篇光学与热辐射 V.1—292 独立分章复算（2026-11-22）：** 新增六套物理专项质量回归及共享源码校验器，完整覆盖第五篇292道原书编号的题面、解答、校核源码段。专题分别为几何光学63题、干涉33题、衍射60题、偏振43题、色散/相对论光学46题和热辐射/光电/康普顿47题，重点通过相量、积分、守恒与原题数值进行复算。**V.105 已补全玻璃片内部多光束干涉的严格条件：必须同时满足菲涅耳波带同相与 Fabry–Pérot 全透射，故正确最小厚度仍为约2.5μm；已撤回本轮曾一度仅按单程相位误改成0.594μm的中间结论。另修订 V.127 波长0.534μm的有效数字、V.2 磁场幅值约2.9mA/m及题面词误。** 每个题号有结构校验与多处物理专项断言，**不等同于292道题全手工逐字原版核图或独立同行评审**。脚本已配置在GitHub Actions中；以[最新CI](https://github.com/jackxiang0329-source/ruoshui-physics-bank/actions)确认运行/编译/PDF状态。详细见 quality_check.md。


- **2026-11-22 第四篇全覆盖自动质检程序续建：** 承接已检的 IV.1—50，新增四套独立物理/数值与源码一致性检查，逐段对应 IV.51—93（43题）、IV.94—149（56题）、IV.150—188（39题）、IV.189—224（36题），合计新增 **174个原书题号的源码覆盖**；连同既有 IV.1—50，第四篇 **224题均配置分段自动检查入口**。新增内容重点锁定物理摆、机械/电学阻尼共振、RLC 相量与初值、声波迟滞多普勒、声强积分、Maxwell方程、Poynting能流与偶极辐射。四套脚本已接入 GitHub Actions，但**运行通过与 PDF 回传须以对应最新工作流实际结果为准**；不宣称已完成逐题原版图像或专家二校。对应文件 `oscillations_mechanical_051_093_regression.py`、`oscillations_electric_094_149_regression.py`、`waves_elastic_150_188_regression.py`、`waves_electromagnetic_189_224_regression.py`，详细见 `quality_check.md`。**旧“2353项静态断言”口径为本轮扩展前的已记录基线，不应无依据累加。**


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
| 小节 `01-mechanics-kinematics`（原 5 份片段） | [01-mechanics-kinematics.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `02-mechanics-dynamics`（原 6 份片段） | [02-mechanics-dynamics.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `03-mechanics-conservation`（原 9 份片段） | [03-mechanics-conservation.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `04-gravitation`（原 3 份片段） | [04-gravitation.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `05-rigid-body`（原 6 份片段） | [05-rigid-body.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `06-elasticity`（原 4 份片段） | [06-elasticity.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `07-hydrodynamics`（原 3 份片段） | [07-hydrodynamics.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `08-relativity`（原 5 份片段） | [08-relativity.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `09-thermo-state`（原 3 份片段） | [09-thermo-state.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `10-thermo-first-law`（原 4 份片段） | [10-thermo-first-law.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `11-kinetic-theory`（原 5 份片段） | [11-kinetic-theory.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `12-entropy-cycles`（原 5 份片段） | [12-entropy-cycles.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `13-capillarity`（原 3 份片段） | [13-capillarity.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `14-phase-transformations`（原 4 份片段） | [14-phase-transformations.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `15-transport`（原 4 份片段） | [15-transport.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `16-electrostatics-vacuum`（原 4 份片段） | [16-electrostatics-vacuum.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `17-electro-conductors`（原 4 份片段） | [17-electro-conductors.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `18-capacitance-energy`（原 5 份片段） | [18-capacitance-energy.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `19-electric-current`（原 5 份片段） | [19-electric-current.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `20-magnetostatics`（原 5 份片段） | [20-magnetostatics.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `21-induction`（原 5 份片段） | [21-induction.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `22-charged-particles`（原 2 份片段） | [22-charged-particles.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `23-mechanical-oscillations`（原 6 份片段） | [23-mechanical-oscillations.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `24-electric-oscillations`（原 4 份片段） | [24-electric-oscillations.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `25-elastic-waves`（原 3 份片段） | [25-elastic-waves.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `26-em-waves`（原 3 份片段） | [26-em-waves.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `27-optics-photometry`（原 6 份片段） | [27-optics-photometry.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `28-optics-interference`（原 3 份片段） | [28-optics-interference.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `29-optics-diffraction`（原 6 份片段） | [29-optics-diffraction.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `30-optics-polarization`（原 3 份片段） | [30-optics-polarization.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `31-optics-dispersion`（原 2 份片段） | [31-optics-dispersion.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `32-moving-optics`（原 1 份片段） | [32-moving-optics.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `33-thermal-radiation`（原 4 份片段） | [33-thermal-radiation.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `34-atomic-scattering`（原 3 份片段） | [34-atomic-scattering.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `35-wave-properties`（原 3 份片段） | [35-wave-properties.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `36-atomic-spectra`（原 6 份片段） | [36-atomic-spectra.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `37-molecules-crystals`（原 3 份片段） | [37-molecules-crystals.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `38-radioactivity`（原 3 份片段） | [38-radioactivity.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `39-nuclear-reactions`（原 4 份片段） | [39-nuclear-reactions.tex（归档）（归档）](../../data/archives/library.zip) |
| 小节 `40-elementary-particles`（原 2 份片段） | [40-elementary-particles.tex（归档）（归档）](../../data/archives/library.zip) |
| 源书勘误 | [errata.md](errata.md) |
| 技术与学术质检记录 | [quality_check.md](quality_check.md) |
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
- **代码静态物理回归断言累计1803处：** 历史1344处 + 第二篇62—257题新增368处 + 第三篇1—53题新增91处；个别测试循环执行多次。1803不是不同习题数，也不能代替原书全部1878题的独立专家终审。详见 [质检记录](quality_check.md)。
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

## 专项回归归档

历史48份专项回归及共享模块保存在 [irodov_regressions.zip（归档）](../../data/archives/library.zip)。从仓库根目录运行 `python3 scripts/compact_auxiliary.py --restore --group irodov_regressions` 后，再按原路径执行回归。章节TeX及PDF仍可直接读取；CI自动恢复。
