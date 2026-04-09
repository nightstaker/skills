
# Tech-Insight 项目需求文档 (Production-Ready v2.0)

## 1. 背景与目标 (Background & Goals)

### 1.1 背景
这是一个专业的**系统化技术洞察** Skill。当下 LLM 直接做技术洞察存在四大痛点：
* **不聚焦**：泛泛而谈"AI、大模型、芯片"，缺乏可落地的产品/技术抓手。
* **不系统**：观点散乱，缺少"场景—厂商—技术—商业"的递进推理链路。
* **不可信**：信息源不透明，关键技术细节凭"先验直觉"杜撰，无法被引用和复核。
* **不够深**：停留在"采用 Transformer / 3nm 工艺 / 生态完善"等行业黑话层级，资深专家看完没有增量信息，投资人无法据此做判断。

本 Skill 的核心使命是把技术洞察从"灵感写作"升级为"工程化研究"——让每一个判断都可溯源、可复核、可推演，并且**深到能让领域专家点头、投资人敢下注**。

### 1.2 核心目标
1. **系统化洞察**：以结构化框架（场景→厂商动态→关键技术→趋势预测→商业闭环）替代零散观点。
2. **可信溯源**：所有事实性陈述（产品规格、技术参数、厂商动作、市场数据）必须附带真实可访问的信息源。
3. **关键技术深挖**：对每一项被点名的关键技术，给出原理、实现路径、壁垒来源，并附上技术性原始资料（论文/专利/官方白皮书/技术博客）。
4. **结构化总结与启示**：每一个洞察点必须配套"Insight（事实）+ Implication（启示）"双层输出，支持后续战略/产品决策。
5. **闭环推演**：对未来趋势类洞察，强制输出"技术 → 产品 → 客户/应用场景 → 商业价值"的完整闭环。
6. **专家级深度**：每一页内容必须经得起领域 Chief Architect 的"再追问一层"测试，每一个数字必须经得起 VC 合伙人的尽调追问。

### 1.3 读者画像 (Reader Profile)

Tech-Insight 报告的**唯一读者群**是以下两类人：

* **Senior Domain Expert（资深领域专家）**：Chief Architect、Fellow、首席科学家、BU 技术总监级别。他们已经知道"Transformer 是什么"、"3nm 是什么"、"CXL 是什么"。他们想看的是：**具体到哪一层**、**具体到哪一个参数**、**与他们的心智模型相比哪里不一样**。任何停留在科普层级的内容都会被他们直接跳过。

* **Domain Investor（领域投资者）**：一线 VC 合伙人、PE 技术尽调 lead、产业资本投资总监。他们不仅要看技术领先性，还要看**可验证的商业化指标**——单位经济性、客户集中度、产能约束、专利护城河的法律强度、监管暴露面。任何无法转化为投资决策的内容都是噪音。

**三问门槛**：每一个洞察点在落地前必须经过以下三问——

1. **"So what for the expert？"**：这段内容是否给了领域专家一条他原本不知道的技术细节（新参数、新实现路径、新约束）？
2. **"So what for the investor？"**：这段内容是否改变了投资人对这家厂商/这条路线的估值、赔率或风险画像？
3. **"What would break this claim？"**：这段内容是否暴露了至少一条可被证伪的断言——可以被哪一篇新论文、哪一份新财报、哪一个新 benchmark 推翻？

三问任一答不上来，这段内容必须删除或重写。

### 1.4 深度非妥协项 (Depth Non-Negotiables)

以下规则是**硬性门槛**，linter 会强制执行，违反任何一条都会打回。

#### 1.4.1 架构深度（Architecture Depth）
禁止仅描述"架构类型"。每一条架构断言必须同时给出以下至少三项：
* **命名的内部模块 / 微架构单元**（例如 "SM 数量 + Tensor Core 代次"、"NPU 的 MAC 阵列规模"、"Attention 的 head 分组数 GQA/MQA/MLA"）
* **定量的设计常数**（例如 "L2 cache 60 MB / 每 SM 256 KB register file / FFN hidden dim 14336"）
* **设计选择的 trade-off 说明**（例如 "用 sliding-window attention 换 KV cache 压缩比 8×，代价是长文召回下降 3–5 pp"）

#### 1.4.2 工艺与制造深度（Process & Manufacturing Depth）
禁止仅写 "3nm / 5nm / 先进工艺"。每一条制程断言必须给出：
* **明确的 foundry 与节点变体**（"TSMC N3E" 而非 "3nm"；"Samsung SF4X"、"Intel 18A"、"TSMC N4P" 等）
* **封装与集成方式**（"CoWoS-L、2.5D interposer、8 层 HBM3e stack"）
* **良率或面积信号**（公开的 die size / wafer cost / yield 估算，哪怕只有 SemiAnalysis、TechInsights、ChipRebel 级别的二手估算，也必须标明来源）

#### 1.4.3 Benchmark 方法论深度（Benchmark Methodology Depth）
禁止裸写性能数字。每一个性能数字必须同时给出以下六元组中的**至少四项**：
* 硬件配置（具体型号 + 卡数 + 互连拓扑）
* 软件栈版本（driver、runtime、compiler、框架）
* 工作负载（模型名 + 参数量 + context length）
* 精度（FP8 / FP16 / BF16 / INT8 / W4A16 etc.）
* Batch size 与 sequence length
* 测试日期与评测机构

Benchmark 方法论应该集中写在 KTD Comparison 表或 Key Technical Metrics 表下方的脚注区域。

#### 1.4.4 壁垒深度（Moat Depth）
禁止"专利多、生态好、人才强"的空洞断言。每一条壁垒断言必须挂载以下至少一项**法律 / 商业级证据**：
* **具体专利号**（格式 US\d{7,}、CN\d{9,}、EP\d{7,}、WO\d{4}/\d{6,}），并一句话概括独立权利要求保护范围
* **具体长期供货合同或产能预留**（Capacity Reservation Agreement、Long-Term Supply Agreement），带公告链接
* **具体 SEC / 港交所 / 招股书披露段落**（页码 + filing 编号）
* **具体命名客户 design win**（客户名 + 项目代号 + 公开披露源）
* **具体开源社区指标**（GitHub star 数 + contributor 数 + fork 速度 + 关键 PR merge 时间）

#### 1.4.5 商业化深度（Commercialization Depth）
每一份报告（无论类型 A/B/C）都必须产出**投资级附录**（见 §2.4），内含单位经济性、客户集中度、产能约束、监管暴露面四个子块，每一项都必须带源或显式写"无公开披露"。

#### 1.4.6 禁用浅层短语（Banned Shallow Phrases）
以下短语会被 linter 一律拒绝。凡是用到这些词，必须被"可量化、可证伪、带源"的具体断言替换：

**中文**：业界领先 / 行业领先 / 性能领先 / 先进架构 / 先进工艺 / 生态完善 / 技术成熟 / 市场广阔 / 大有可为 / 空间巨大 / 潜力巨大 / 引领行业 / 颠覆式创新 / 革命性突破 / 全球首创 / 具有广阔前景 / 有望成为 / 将会改变

**英文**：industry-leading、best-in-class、state-of-the-art（除非紧挨着具体 benchmark 数字与条件）、revolutionary、game-changing、cutting-edge、paradigm-shift、next-generation（除非紧挨着具体版本号与发布日期）

（注：此清单是"§3 现有填充语清单（需要持续关注 / 值得观察 / 未来可期 …）"的扩展，与之并列执行。）

## 2. 洞察分类定义 (Insight Taxonomy)

Tech-Insight 将所有洞察严格划分为三类，使用不同的分析框架与质量门槛。所有类型都必须产出 §2.4 的投资级附录。

### 2.1 类型 A：已有技术洞察 (Existing Technology Insight)
**目标**：在某一品类下，对**全世界同类的 TOP 5 顶级产品**进行系统化横向洞察，提炼整个赛道的"关键竞争力图谱"与"关键技术全景"，而非孤立分析单一产品。

**前置定义**：
* **品类边界 (Category Scope)**：必须先明确品类定义（功能、目标客户、价格段、部署形态），避免把不同细分混为一谈。
* **TOP 5 入选标准 (Selection Criteria)**：基于公开可核查的指标排序——市场份额 / 装机量 / 营收 / 出货量 / 权威榜单排名等，至少 1 项指标带源；如品类过窄无法凑齐 5 款，必须显式说明并降级为 TOP N（N≥3）。
* **样本均衡性**：TOP 5 应覆盖不同地区与不同技术路线的代表，避免只取单一阵营。

**强制结构**：
* **Category Profile**：品类定义、市场规模（近 12 个月全球出货量 / 营收 + 年增速，带源）、TOP 5 名单与入选依据（带源）。
* **Per-Product Profile (×5)**：对每款产品分别给出定位、目标客户、上市时间、最新版本、份额或装机量、价格段、**3 个最强 design win 客户**（或写"未公开"），每条带源。
* **Key Competitive Advantages Matrix (KCA Matrix)**：以"产品 × 竞争力维度"矩阵呈现 5 款产品在 3–5 个核心维度上的差异化优势。**每个单元格必须**：
  - 区分"营销话术（厂商宣称）"与"可验证的工程事实（第三方复现）"；
  - 对工程事实给出具体数字 + 单位 + 测试条件；
  - 挂载一手资料链接。
  - 纯营销宣称必须注明"厂商宣称"并被至少一条独立 benchmark 或 teardown 配对否则整行视为未证实。
* **Key Technical Details Comparison (KTD Comparison)**：对支撑 KCA 的核心技术做横向拆解与对比。必须覆盖：
  - **制程节点**（foundry 变体：TSMC N3E / Samsung SF4 / Intel 18A 等）
  - **封装与集成**（CoWoS-L / FOPLP / 2.5D / 3D stack）
  - **核心微架构命名单元与定量常数**（SM 数 / Tensor core 代次 / NPU MAC 阵列规模 / attention head 分组策略 / L2 cache / register file / FFN hidden dim 等，至少 5 项）
  - **可量化 benchmark**（性能 / 功耗 / 能效 / 良率 / die size / 生态指标），每项带完整方法论脚注。
  - **Benchmark Methodology 脚注行**：KTD 表下方必须有一段 methodology footer，说明硬件 / 软件 / 模型 / batch / seqlen / 精度 / 测试日期 / 评测机构。
* **Evidence Pack**：KCA 矩阵与 KTD 对比表中的每一条事实性数据必须挂载至少 1 条一手资料（官方发布、专利、SEC/招股书、权威评测、白皮书）。关键参数（性能 / 份额 / 价格）必须有 2 条独立来源交叉验证。
* **Moat & Risk Register**：针对领先产品（一般为 P1），按 §1.4.4 的壁垒深度要求展开 5 轴分析（专利 / 制程 / 生态 / 数据 / 人才），每一轴必须挂载具体法律或商业级证据（专利号、供货合同、SEC 披露等）。
* **Cross-Product Insight**：横向归纳——整个赛道的共同范式是什么？分歧点在哪里？谁在引领、谁在跟随、谁在出局？每一条都要挂一手资料。
* **Implication**：对我方产品规划的具体启示，回答"我方应在哪个维度切入、绕开哪条已被验证失败的路径、复用哪条已被验证的工程事实"。
* **Investor Appendix**：按 §2.4 产出单位经济性 / 客户集中度 / 产能约束 / 监管暴露面四子块。

### 2.2 类型 B：未来趋势洞察 (Future Trend Insight)
**目标**：从"可见可感知的应用场景"切入，层层递进，预测 1–3 年内的产品形态与商业机会。

**强制递进链路（五段式，缺一不可）**：
1. **Scene Anchor（场景锚点）**：用一个用户/客户能直接感知的场景开篇（例如"会议室自动会议纪要"、"端侧实时翻译耳机"），避免从抽象技术名词切入。必须给出至少一个已落地的 pilot 部署（公司名 + 时间 + 数据披露来源）。
2. **Vendor Landscape（厂商动态）**：盘点头部厂商（≥3 家）在该场景下最近 6–12 个月的公开动作（产品发布、专利、收购、组织调整），每条带源。每家厂商必须附上至少 **1 条公开披露的财务或产能信号**（营收占比、产能扩张、研发投入）。
3. **Key Technology Decomposition（关键技术拆解）**：抽丝剥茧地识别支撑该场景演进的 2–4 项关键技术。对每项技术必须给出以下**六元组**：
   - 原理（含关键算法 / 架构选择 / 设计常数）
   - 当前成熟度 TRL（1–9，带引用）
   - 具体瓶颈（可量化指标，例如 "KV cache 内存占用随 seqlen 线性增长，64K ctx 下占卡显存 58%"）
   - 突破方向（命名的候选方案 + 至少 1 篇代表论文 / 专利）
   - 最新公开 benchmark（含完整方法论）
   - 关键玩家与专利壁垒（至少 1 个专利号或 1 篇代表性论文）
4. **Trend Prediction（趋势预测）**：在前三步证据基础上，预测未来产品形态（外观、交互、部署模式）与时间窗口，明确预测的前提假设与可证伪条件。必须给出以下三项：
   - 时间窗口（12 / 24 / 36 个月择一承诺）
   - ≤5 条核心假设，每条一句话可证伪条件
   - **预测偏差的代价**：如果预测错了，应对成本是多少（供应链重建 / 研发 pivot / 订单违约）
5. **Closed Loop（闭环输出）**：以 **技术 → 产品 → 客户/应用场景 → 商业价值** 的四节点闭环收尾，商业节点必须同时给出：
   - **TAM / SAM / SOM 任一量化**（带源 + 算法说明）
   - **单位经济性锚点**（ASP / gross margin / CapEx per unit / ARPU 任一）
   - **客户集中度假设**（头部 3 客户份额推测）
   - **产能与供应链约束**（支撑这条闭环所需的 fab / HBM / CoWoS / substrate 等关键资源的公开可用性）

### 2.3 类型 C：单品深度拆解 (Single-Product Deep Teardown)
**目标**：对**单一产品或单一技术实现**做工程级深度拆解，把公开资料中能抠出的架构、参数、壁垒、风险系统地整理成可复核的技术档案。与类型 A 不同，类型 C 只看一款产品；与类型 B 不同，类型 C 不做趋势外推。

**强制结构**：
* **Product Profile**：厂商、产品线、版本、上市时间、价格、目标客户、部署形态、headline claim、公开 traction（出货 / 装机 / design win，每条带源）。
* **Architecture Decomposition**：计算 / 存储 / 互连 / 软件栈 / 封装五子系统分章拆解，禁止停留在 block diagram 层级。每一子系统必须下钻到以下层级：
  - **计算**：命名的微架构单元（SM / Core / Tile / NPU Cluster）+ 数量 + 代次；MAC 阵列规模；data-path 位宽；支持的数值格式；cache 层级与容量（L0 / L1 / L2 / 最后一级）；register file 大小。
  - **存储**：HBM 代次（HBM3 / HBM3e）+ stack 层数 + 容量 + 带宽；memory 控制器数量；内存地址映射策略；片上 SRAM 总量。
  - **互连**：命名的 bus / protocol（NVLink 代次 / Infinity Fabric / CXL 3.x / UCIe / Ethernet RoCE）+ 带宽 + 拓扑（mesh / fat-tree / dragonfly）+ 最大扩展规模。
  - **软件栈**：编译器（命名 + 版本）、runtime、driver、支持的框架与版本矩阵、开源成熟度（GitHub 指标 + PR 活跃度）。
  - **封装**：foundry 节点变体（TSMC N3E / Samsung SF4X / Intel 18A）+ 封装方案（CoWoS-L / FOPLP / EMIB）+ interposer 尺寸 + 模块集成度。
* **Key Technical Metrics**：带测试条件的量化指标表，并与至少一个最强替代做 Δ 对比；表下方必须有 **benchmark methodology 脚注**（硬件 / 软件 / 模型 / batch / seqlen / 精度 / 日期）；厂商自报数据显式标注"厂商宣称"并被至少一条独立 benchmark 配对。
* **Moat Analysis**：按专利 / 制程 / 生态 / 数据 / 人才五轴评估壁垒来源，每一轴必须挂载具体法律或商业级证据（专利号、长期供货合同、SEC 披露、命名 design win、开源指标），并给出"24 个月内是否可复制"的显式判断。
* **Weakness / Risk Analysis**：工程 / 供应链 / 路线图 / 生态 / 监管五类公开证据的风险扫描。每一条风险都必须挂载公开信号；无证据的类别显式写"无公开证据"。
* **Implication**：可执行动作导向的"So what?"，禁止空泛表述。
* **Investor Appendix**：按 §2.4 产出单位经济性 / 客户集中度 / 产能约束 / 监管暴露面四子块。

**视觉证据**：必须包含产品图、架构总览图、关键子系统细节图，以及 die shot / PCB / 内部拆解图，共 ≥4 张，每张带源。

### 2.4 投资级附录 (Investor-Grade Appendix) — 所有类型必含

不论 Type A / B / C，每份报告都必须产出一段独立的"投资级附录"，用于支撑 domain investor 的尽调决策。四个子块**缺一不可**；若某一子块确实没有公开披露，必须显式写"无公开披露 — 原因：…（例如：非上市公司 / 未进入正式披露期 / 监管豁免）"，不得留空。

#### 2.4.1 单位经济性 (Unit Economics)
* **ASP（平均售价）**：带区间 + 来源；渠道价差与客户议价信号。
* **BoM / Wafer cost 估算**：die size × wafer ASP × yield + HBM + 封装 + 测试。允许引用 SemiAnalysis、TechInsights、ChipRebel、Moor Insights 等二手估算，但必须标注。
* **毛利率区间**：至少 1 条公开披露（财报 / 分析师模型）。
* **CapEx intensity**：每亿美元营收对应的 CapEx（工厂 / 设备 / IP 授权）。

#### 2.4.2 客户集中度 (Customer Concentration)
* **Top-3 客户份额**：带来源或"未公开"显式声明。
* **命名 design win**：客户名 + 项目代号 + 年化金额区间（若公开）。
* **客户切换成本信号**：软件栈 / 采购周期 / 认证成本。

#### 2.4.3 产能与供应链约束 (Capacity & Supply Constraints)
* **关键前端产能**：foundry 节点的预留 wafer start / 月产能；长期合约签约量。
* **关键后端产能**：CoWoS / FOPLP / advanced packaging 月产能占比。
* **关键物料**：HBM 分配量（SK hynix / Samsung / Micron）、ABF substrate、特殊基板、稀土。
* **瓶颈识别**：哪一环是 24 个月内最紧的绳结，支持一句话结论。

#### 2.4.4 监管与地缘暴露面 (Regulatory & Geopolitical Exposure)
* **出口管制**：引用具体规则编号（15 CFR Part 744、BIS ECCN、EAR、EU Chips Act、日韩白名单等），而非泛泛说"受出口管制"。
* **反垄断 / 国家安全审查**：CFIUS / SAMR / CMA 相关公开披露。
* **区域市场准入**：中国 CCC、欧盟 CE、美国 FCC、印度 BIS 等本地合规信号。
* **关键地缘冲突暴露**：台海 / 俄乌 / 中东对其供应链或销售地的直接影响。

### 2.5 资料分级 (Source Tiering)

每一条引用都应标注其等级，linter 会按等级计数：

| 等级 | 类型 | 示例 |
|---|---|---|
| **T1 — 一手权威** | 官方白皮书、SEC / HKEX filing、授权专利（含权利要求）、同行评审论文、监管文件 | NVIDIA H100 Whitepaper、TSMC N3E 技术报告、USPTO 专利原文 |
| **T2 — 一手其他** | 厂商官网产品页、官方发布会、官方博客、标准组织文件 | IETF RFC、JEDEC 规范、官方 press release |
| **T3 — 权威评测 / 分析** | SemiAnalysis、TechInsights、ChipRebel、AnandTech、ServeTheHome、Gartner、IDC、Omdia、Counterpoint | SemiAnalysis 成本拆解、TechInsights die 分析 |
| **T4 — 头部行业媒体** | The Information、FT、WSJ、Nikkei、Reuters、Bloomberg | Nikkei 产能报道、Bloomberg 订单消息 |
| **T5 — 二手 / 博客 / 社交** | 个人博客、Twitter/X、知乎、微信公众号 | 仅作补充，不能作为关键断言唯一来源 |

**硬性要求**：每份报告的 T1 + T2 来源数必须 ≥ 全部来源的 50%；任何关键参数（性能、份额、价格、产能）必须由 ≥2 条 T1–T3 交叉验证。

## 3. 核心功能模块 (Function Modules)

### 3.1 信息源采集器 (Source Collector)
* **白名单优先**：一手资料优先级 > 二手资料，按 官方发布 / 专利 / 论文 / 监管文件 / 头部媒体评测 / 行业报告 / 个人博客 排序。
* **可访问性校验**：每一条引用必须给出可点击 URL 或可检索的标识符（DOI、专利号、SEC filing 编号）。
* **时效性约束**：厂商动态类信息默认窗口 12 个月，超过窗口必须显式标注"历史背景"。
* **多源交叉**：关键事实（参数、份额、价格）至少两个独立来源交叉验证，冲突时优先一手并标注分歧。
* **全量挂源 (Universal Sourcing)**：洞察报告中**任何**陈述句、数据、结论、引语、技术参数、厂商动作都必须就地附带信息源链接（URL / DOI / 专利号），禁止出现"无源句"。无法挂源的内容必须删除或显式标注为"作者推断"并独立分区。

### 3.1.1 视觉资料采集器 (Visual Asset Collector)
* **强制视觉证据**：洞察报告必须配套**原始视觉资料**——产品图、产品上下文图（使用场景、拆解图、PCB/Die shot）、技术架构图、数据流图、对比图表等，禁止纯文字洞察。
* **来源合法性**：图片必须来自一手资料（厂商官网、官方发布会、专利附图、论文 figure、监管文件、官方白皮书），并保留原始出处链接；不得使用无法溯源的二次加工图。
* **两种交付形态**：
  - **链接形态**：直接 inline 嵌入原始图片 URL（适合在线阅读）。
  - **下载形态**：把图片下载到 `assets/<slug>/` 目录，文件名带产品/章节前缀，并在 markdown 中相对引用；同时保留原始 URL 与抓取时间戳作为图注。
* **内容匹配 (Caption Binding)**：每张图必须紧邻其所支撑的论述段落，并以 `图 X：[说明] — 来源：[链接]` 的格式注明，严禁"配图与正文无关"。
* **覆盖度要求**：类型 A 中 TOP 5 每款产品至少 1 张产品图 + 1 张技术架构/拆解图；类型 B 必须包含场景图、厂商代表产品图、关键技术原理图各至少 1 张。

### 3.2 关键技术拆解器 (Key Tech Decomposer)
* **强制下钻**：禁止在"使用了 Transformer / 采用 3nm 工艺"层级停止，必须下钻到具体架构选择、关键超参、工艺节点变体的差异化点（见 §1.4.1）。
* **可量化对比**：与上一代或主要竞品给出可量化的指标对比表（性能、功耗、成本、良率等），数据须带源 + 完整 benchmark 方法论。
* **壁垒分析**：识别该技术的护城河来源（专利、人才、制程、生态、数据），每一轴带具体证据（见 §1.4.4）。

### 3.2.1 深度下钻器 (Depth Decomposer) — 新增
每一条核心断言在进入正文前，必须经过三轮"再追问一层"：

1. **第一问 — What is it？**：给出命名、类别、代次。
2. **第二问 — How does it work？**：给出具体实现、参数、设计常数、trade-off。
3. **第三问 — Why does it matter？**：给出可量化的商业或工程影响 + 可证伪的 benchmark / 财务指标。

任一问答不上来，这段内容被视为浅层，打回重写或删除。

### 3.3 闭环推演器 (Closed-Loop Reasoner) — 仅适用于类型 B
* **节点完整性检查**：自动校验"技术/产品/客户/商业价值"四节点是否齐全，缺任一节点拒绝输出。
* **假设显式化**：所有预测必须列出 ≤5 条核心假设，并给出每条假设的可证伪条件。
* **量化锚点**：商业价值节点必须给出至少一个可量化指标（市场规模 / ARPU / 替代成本 / 渗透率曲线）。

### 3.4 洞察质量校验器 (Insight Linter & QA)
* **可信度门槛**：每一个洞察点必须通过"事实-来源-启示"三段式校验，缺任一段直接打回。
* **全量挂源校验**：扫描全文，任何未挂载 URL/DOI/专利号的事实性陈述一律标红打回，零容忍。
* **视觉资料校验**：检查每节是否含原始图（产品图 / 架构图 / 上下文图），缺图直接打回；检查每张图是否带来源链接与"图—文匹配"的图注。
* **反幻觉检查**：识别未挂源的具体数字、产品代号、人物言论，强制补源或删除。
* **结构完整性**：
  - 类型 A：Category Profile / Per-Product Profile / KCA Matrix / KTD Comparison / Moat / Cross-Product Insight / Implication / Investor Appendix
  - 类型 B：五段式链路 + 闭环四节点 + Investor Appendix
  - 类型 C：Product Profile / Architecture Decomposition / Key Technical Metrics / Moat Analysis / Weakness / Implication / Investor Appendix
* **启示可操作性**：Implication 必须回答"So what？"——对读者的决策/产品/投资有可执行的指向，禁止"需要持续关注"类空话。
* **深度门槛（v2.0 新增）**：
  - **禁用浅层短语检查**：命中 §1.4.6 的任一中英文禁用短语一律打回。
  - **制程节点变体检查**：任意出现 `3nm / 4nm / 5nm / 7nm / 10nm` 等节点数字的章节，必须同时出现 foundry 或变体名（TSMC N3 / N3E / N3P / N4 / N4P / Samsung SF3 / SF4 / SF4X / Intel 18A / 20A 等）。
  - **Benchmark 方法论检查**：KTD Comparison / Key Technical Metrics 章节必须出现 "batch"、"seqlen" / "sequence length"、"precision" / "FP8" / "FP16" / "BF16" / "INT8"、"测试条件" / "methodology" 这几类关键词，覆盖完整方法论六元组。
  - **Moat 法律级证据检查**：Moat / 壁垒 章节必须含有 ≥1 条专利号（`US\d{7,}` / `CN\d{9,}` / `EP\d{7,}` / `WO\d{4}/\d{6,}`）或 ≥1 条 SEC / HKEX filing 编号。
  - **投资级附录检查**：Investor Appendix 段必须含 TAM/SAM/SOM/ARPU/gross margin/毛利率/单位经济性 与 客户集中度 / Top-3 客户 / design win / 产能约束 / 监管 / 出口管制 关键词族，每个子块至少命中一词，否则打回。
  - **数字与单位配对**：Key Technical Metrics 表格内任何裸数字（`\d+`）必须紧挨一个单位或被标注"厂商宣称 / 未公开"。

## 4. 输出规范 (Output Specification)

### 4.1 类型 A 输出模板（TOP 5 横向洞察）
```markdown
## [品类名称] · 全球 TOP 5 技术洞察

**品类边界**：[功能 / 客户 / 价格段 / 部署形态]
**TOP 5 入选依据**：[排序指标 + 数据源]

### Per-Product Profile
| 产品 | 厂商 | 上市时间 | 份额/装机量 | 价格段 | 来源 |
| --- | --- | --- | --- | --- | --- |

#### 产品图集（每款产品 ≥1 张原始产品图，带源）
![P1 产品图](assets/<slug>/p1-hero.jpg)
*图 1：P1 官方产品图 — 来源：[厂商发布页](URL)*

![P2 产品图](URL_or_assets/<slug>/p2-hero.jpg)
*图 2：P2 官方产品图 — 来源：[厂商发布页](URL)*
（…P3/P4/P5 同上）

### KCA Matrix（产品 × 竞争力维度）
| 维度 \ 产品 | P1 | P2 | P3 | P4 | P5 |
| --- | --- | --- | --- | --- | --- |
| 维度 1 | …（带源） | … | … | … | … |

### KTD Comparison（关键技术对比）
| 技术指标 | P1 | P2 | P3 | P4 | P5 | 来源 |
| --- | --- | --- | --- | --- | --- | --- |

#### 技术架构图集（每款产品 ≥1 张架构/拆解/Die shot，带源）
![P1 架构图](assets/<slug>/p1-arch.png)
*图 N：P1 系统架构图 — 来源：[官方白皮书 p.X](URL)*
（…P2–P5 同上）

### Cross-Product Insight
- 共同范式 / 分歧点 / 引领者 / 跟随者 / 出局者

### Implication
- 对我方产品规划的可执行启示，回答 "So what?"

### Sources
1. [一手资料标题](URL)
```

### 4.2 类型 B 输出模板（未来趋势洞察）
```markdown
## [场景名称] · 未来趋势洞察

**Scene Anchor**：[用户可感知的场景描述]

![场景图](assets/<slug>/scene.jpg)
*图 1：典型应用场景 — 来源：[原始出处](URL)*

**Vendor Landscape**：
- 厂商 A / 动作 / 时间 / 来源
- 厂商 B / 动作 / 时间 / 来源
- 厂商 C / 动作 / 时间 / 来源

**厂商代表产品图（每家 ≥1 张）**
![厂商 A 代表产品](URL)
*图 2：厂商 A 代表产品 — 来源：[官方页面](URL)*

**Key Technology Decomposition**：
- 技术 1 / 原理 / TRL / 瓶颈 / 来源
- 技术 2 / 原理 / TRL / 瓶颈 / 来源

![关键技术原理图](assets/<slug>/tech-arch.png)
*图 3：关键技术 1 原理示意 — 来源：[论文/白皮书](URL)*

**Trend Prediction**：
- 预测内容 + 时间窗口
- 核心假设 ≤5 条
- 可证伪条件

**Closed Loop（技术 → 产品 → 客户/场景 → 商业价值）**：
| 节点 | 内容 | 关键假设 |
| --- | --- | --- |
| 技术 | … | … |
| 产品 | … | … |
| 客户/场景 | … | … |
| 商业价值 | …（TAM/SAM/SOM 任一） | … |

### Sources
1. [一手资料标题](URL)
```

## 5. 生产级技术指标 (Technical Specifications)

| 维度 | 要求说明 |
| :--- | :--- |
| **读者画像** | 资深领域专家 + 领域投资者；每段内容都必须同时满足"专家级深度"与"投资级可判断性"（见 §1.3）。 |
| **信息源等级** | 每个事实性陈述至少 1 条一手资料；关键参数至少 2 条独立来源交叉验证；全部来源的 T1+T2 占比 ≥50%（见 §2.5）。 |
| **全量挂源** | 报告中任何陈述句、数据、引语均必须就地附 URL/DOI/专利号；无源内容必须删除或标注为"作者推断"并独立分区。 |
| **视觉证据** | 必须包含原始产品图、产品上下文图、技术架构图等；图片可为原始 URL 或下载至 `assets/<slug>/`，每张必须带源链接与"图—文匹配"图注。类型 A 每款产品 ≥1 张产品图 + ≥1 张架构/拆解图；类型 B 必须含场景图、厂商代表产品图、关键技术原理图各 ≥1 张；类型 C 必须含产品图 + 架构 + die/PCB 拆解 ≥4 张。 |
| **时效窗口** | 厂商动态默认近 12 个月；超出窗口必须显式标注。 |
| **样本完整性** | 类型 A 必须覆盖品类下全球 TOP 5（极端窄品类可降级 TOP N，N≥3），且入选依据带源。 |
| **结构完整性** | 类型 A 必含 Category Profile / Per-Product / KCA / KTD / Moat / Cross-Product / Implication / Investor Appendix；类型 B 必含五段式 + 闭环四节点 + Investor Appendix；类型 C 必含七段式 + Investor Appendix。 |
| **架构深度** | 每条架构断言必须命名 ≥1 内部微架构单元 + ≥1 定量设计常数 + ≥1 trade-off 说明（见 §1.4.1）。 |
| **工艺深度** | 禁止裸写节点数字；必须给出 foundry 变体（TSMC N3E / Samsung SF4X / Intel 18A 等）+ 封装方案 + 公开良率/面积信号（见 §1.4.2）。 |
| **Benchmark 方法论** | 每个性能数字必须配六元组（硬件 / 软件 / 模型 / batch / seqlen / 精度）中的 ≥4 项；KTD 表下必须有 methodology footer（见 §1.4.3）。 |
| **壁垒法律强度** | 壁垒断言必须挂载具体专利号 / 长期供货合同 / SEC filing / 命名 design win / 开源指标（见 §1.4.4）。 |
| **投资级附录** | 所有类型必须产出单位经济性 / 客户集中度 / 产能约束 / 监管暴露面四子块（见 §2.4）。 |
| **禁用浅层短语** | 命中"业界领先 / 先进架构 / 生态完善 …"等 §1.4.6 列表一律打回。 |
| **下钻深度** | 关键技术拆解禁止停留在通用名词层级，必须通过"What / How / Why"三问（见 §3.2.1）。 |
| **可证伪性** | 所有趋势预测必须附前提假设与可证伪条件；同时给出预测偏差的代价。 |
| **启示可操作性** | Implication 必须给出可执行的产品/战略/投资指向，禁止空泛表述。 |
| **反幻觉** | 任何具体数字、产品代号、引语未挂源即视为不合格，自动打回补源。 |
