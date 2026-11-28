# 第一部调研：过程、计算与共同形式基础

## 本部问题与论证任务

本部建立过程、资源、观察、行动与规则变换的共同语言。形式命题限于写明的模型；模型与实际对象的对应另行论证。有限集合证明与构造例子由本书编排，不争论基础数学思想的首创。核对日期：2026 年 11 月 28 日。

## 文献与证据边界

### I-01 Alan M. Turing，1936/1937

**题名：** On Computable Numbers, with an Application to the Entscheidungsproblem. Proceedings of the London Mathematical Society，第二系列 42，230–265。论文于 1936 年提交、宣读，卷期通常著录为 1937 年。
**原文：** https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf
**支持点：** 有效程序、有限控制与可扩展记录，统一判定的界限。
**边界与推进：** 不据此断言物理宇宙离散化；本书以现代程序形式重述对角论证，区分不可计算、资源不足和信息不足。

### I-02 Juris Hartmanis、Richard E. Stearns，1965

**题名：** On the Computational Complexity of Algorithms. Transactions of the American Mathematical Society 117，285–306。
**原文：** https://www3.risc.jku.at/people/schreine/courses/compcomp/HartmanisStearns1965.pdf
**DOI：** https://doi.org/10.1090/S0002-9947-1965-0170805-7
**支持点：** 在可计算对象内按所需计算时间研究复杂性。
**边界与推进：** 复杂度依赖指定问题、输入规模和机器；本书将资源预算与行动期限结合，不复述时间层级定理。

### I-03 W. Ross Ashby，1956

**题名：** An Introduction to Cybernetics. Chapman & Hall。所用扫描本为 1957 年第二次印刷。
**原文：** https://www.ashby.info/Ashby-Introduction-to-Cybernetics.pdf
**支持点：** 观察区分、同态、黑箱与调节，尤其 §6/12—6/14。
**边界与推进：** 同态需要保留转移关系；不推出主观体验或政治目的相同。本书完整证明有限观察行动判准和粗粒化闭包判准。

### I-04 Rolf Landauer，1961

**题名：** Irreversibility and Heat Generation in the Computing Process. IBM Journal of Research and Development 5(3)，183–191。
**原文重印：** https://www.cpt.univ-mrs.fr/~verga/pdfs/Landauer-1961uq.pdf
**DOI：** https://doi.org/10.1147/rd.53.0183
**支持点：** 逻辑操作的物理实现、不可逆操作与耗散。
**边界与推进：** 不说每个计算步骤具有同样固定能耗。本书分开逻辑组合和装置代价，不从耗散推出历史价值。

### I-05 Claude E. Shannon，1948

**题名：** A Mathematical Theory of Communication. Bell System Technical Journal 27，379–423、623–656。
**原文：** https://web.mit.edu/6.441/spring05/reading/shannon1948.pdf
**支持点：** 信号的可能性、编码、噪声及统计结构。
**边界与推进：** 信息量不衡量意义、真实性或伦理价值。本书仅在明确的存储模型中进行状态计数。

### I-06 Jean-Pierre Aubin、Alexandre M. Bayen、Patrick Saint-Pierre，2011

**题名：** Viability Theory: New Directions. Springer。
**出版社：** https://link.springer.com/book/10.1007/978-3-642-16684-6
**作者介绍：** https://bayen.berkeley.edu/viability-theory-new-directions
**支持点：** 留在约束集合内的演化与可达问题应分别研究。
**边界与推进：** 核对了出版社、作者介绍及章节目录，未取得全书；不把其未读证明作为依据。本书自行证明有限确定性系统的递减安全集合算法，不覆盖连续系统及部分观察策略。

### I-07 Herbert A. Simon，1962

**题名：** The Architecture of Complexity. Proceedings of the American Philosophical Society 106(6)，467–482。
**原文：** https://pdodds.w3.uvm.edu/research/papers/others/1962/simon1962a.pdf
**支持点：** 层次、稳定子结构与近可分解性可构成跨领域问题。
**边界与推进：** 不把近可分解性说成普遍性质或层级支配的理由。本书区分精确闭包、近似有效与实际解释尺度。

### I-08 Heinz von Foerster，1979

**题名：** Cybernetics of Cybernetics. 载 Klaus Krippendorff 编 Communication and Control in Society，Gordon and Breach，5–8。
**原文：** https://cepa.info/fulltexts/1707.pdf
**支持点：** 研究观察系统，并将观察者的目的纳入。
**边界与推进：** 二阶不等于第二层优化器，也不推出描述任意。本书将模型选择与公开描述的后果置于修订关系中。

### I-09 Howard H. Pattee，2001

**题名：** The Physics of Symbols: Bridging the Epistemic Cut. BioSystems 60(1–3)，5–21。
**作者机构全文：** https://casci.binghamton.edu/publications/pattee/pattee.html
**DOI：** https://doi.org/10.1016/S0303-2647(01)00104-6
**支持点：** 符号载体、解释结构与受其控制的活动须共同说明。
**边界与推进：** 符号与物质的区分不等于脱离的两种实体。本书分别考察新增名称、可观察差异和可实现操作。

## 本书的形式构造及证明责任

1. 命题 I.1：有限非空状态集和动作集中，存在仅依观察、对所有状态都可接受的确定性策略，当且仅当每一观察类内可接受动作集合的公共交集非空。有限性避免无穷选择和可计算选择的额外问题。
2. 命题 I.2：满射粗粒化存在确定性闭包，当且仅当同类状态的后继同类；证明充要性和唯一性。
3. 命题 I.3：有限、全状态可观察的确定性受控系统，递减安全集合给出最大的可无限维持子集；证明有限终止、策略构造与最大性。
4. 局部可行不推出共同可行；协调选择与真正扩展资源、时序的作用分开。
5. 变动状态空间、部分对应关系与规则改写是本书的描述方案，编码存在不等于新颖性的机制已经解释。
6. 公开反预测例子只否定指定条件下的普遍精确公开预测，不推论自由意志的形而上性质。

