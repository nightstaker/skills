# Sample AI Accelerator · 全球 TOP 5 技术洞察 (Demo v2.0)

> ⚠️ **DEMO / SAMPLE ONLY** — this report uses fictional vendors (alpha / bravo / charlie / delta / echo) and `example.com` URLs purely to demonstrate the v2.0 depth structure and prove the linter workflow passes end-to-end. Do NOT cite any numbers from this example in real work.
>
> 报告类型：A — 已有技术横向洞察
> 生成日期：2025-12-20
> 读者画像：资深领域专家（Chief Architect / Fellow / BU 技术总监）+ 领域投资者（VC / PE / 产业资本）
> 作者：tech-insight skill (worked example)

## 0. 品类边界与样本

- 功能定义：数据中心大模型推理/训练加速卡 ([alpha 定位](https://example.com/alpha/positioning))
- 目标客户：超大规模云厂商与自建 AI 集群企业 ([bravo 目标市场](https://example.com/bravo/market))
- 价格段：$15,000–$40,000 单卡 ASP ([charlie 价格披露](https://example.com/charlie/pricing))
- 部署形态：OAM 模组 + 自研基板 ([delta 平台说明](https://example.com/delta/platform))
- 市场规模：近 12 个月全球数据中心 AI 加速卡出货 $42B，YoY +58% — 来源：[demo 行业季报](https://example.com/industry/2025-q3)

**TOP 5 入选指标**：2024 年云厂商装机量 — 来源：[demo 2024 云 AI 处理器报告](https://example.com/reports/2024-ai-processor)

**样本均衡性说明**：覆盖 2 个地区（北美、东亚）与 2 条技术路线（GPGPU、领域专用 dataflow）— 来源：[demo 样本均衡性说明](https://example.com/balance)

---

## 1. Per-Product Profile

| # | 产品 | 厂商 | 上市时间 | 最新版本 | 份额 | 价格段 | 目标客户 | Top-3 design win | 来源 |
|---|---|---|---|---|---|---|---|---|---|
| P1 | alpha-A100 | alpha | 2024-03 | v1.2 | 35% | $38k | cloud 超头部 | DemoCloud / Orion / $1.2B | [src](https://example.com/alpha/spec) |
| P2 | bravo-B2   | bravo | 2024-06 | v2.0 | 22% | $28k | 二线 cloud   | DemoSky / Vega / $450M   | [src](https://example.com/bravo/spec) |
| P3 | charlie-C3 | charlie | 2023-11 | v3.1 | 18% | $32k | 自建 AI 集群 | DemoLab / Nova / $280M   | [src](https://example.com/charlie/spec) |
| P4 | delta-D1   | delta | 2024-09 | v1.0 | 14% | $22k | 区域 cloud   | 未公开                     | [src](https://example.com/delta/spec) |
| P5 | echo-E5    | echo  | 2024-12 | v5.0 | 11% | $19k | 企业 AI      | DemoCorp / Atlas / $90M   | [src](https://example.com/echo/spec) |

### 1.1 产品图集

![P1 产品图](https://example.com/alpha/press/a100-hero.jpg)
*图 1：P1 产品图 — 来源：[alpha 官方发布页](https://example.com/alpha/press/a100)*

![P2 产品图](https://example.com/bravo/press/b2-hero.jpg)
*图 2：P2 产品图 — 来源：[bravo 官方发布页](https://example.com/bravo/press/b2)*

![P3 产品图](https://example.com/charlie/press/c3-hero.jpg)
*图 3：P3 产品图 — 来源：[charlie 官方发布页](https://example.com/charlie/press/c3)*

![P4 产品图](https://example.com/delta/press/d1-hero.jpg)
*图 4：P4 产品图 — 来源：[delta 官方发布页](https://example.com/delta/press/d1)*

![P5 产品图](https://example.com/echo/press/e5-hero.jpg)
*图 5：P5 产品图 — 来源：[echo 官方发布页](https://example.com/echo/press/e5)*

---

## 2. KCA Matrix（产品 × 竞争力维度）

| 维度 \ 产品 | P1 | P2 | P3 | P4 | P5 |
|---|---|---|---|---|---|
| 工程事实 — 峰值算力 | 1200 TFLOPS FP8 厂商宣称，独立 demo benchmark 复现 1140 TFLOPS ([src](https://example.com/alpha/perf)) | 900 TFLOPS FP8，独立复现 880 TFLOPS ([src](https://example.com/bravo/perf)) | 1100 TFLOPS FP8 厂商宣称，独立复现 920 TFLOPS ([src](https://example.com/charlie/perf)) | 700 TFLOPS FP8 独立复现 ([src](https://example.com/delta/perf)) | 600 TFLOPS FP8 独立复现 ([src](https://example.com/echo/perf)) |
| 工程事实 — 显存带宽 | 3.8 TB/s 实测 ([src](https://example.com/alpha/mem)) | 3.2 TB/s 实测 ([src](https://example.com/bravo/mem)) | 4.0 TB/s 实测 ([src](https://example.com/charlie/mem)) | 2.4 TB/s 实测 ([src](https://example.com/delta/mem)) | 2.0 TB/s 实测 ([src](https://example.com/echo/mem)) |
| 工程事实 — 生态支持 | 全栈自研 compiler + PyTorch 2.5 / vLLM 0.6 原生后端 ([src](https://example.com/alpha/sw)) | OpenAI Triton 3.0 复用 ([src](https://example.com/bravo/sw)) | 自研 + Triton 双栈 ([src](https://example.com/charlie/sw)) | 仅 ONNX Runtime 1.19 ([src](https://example.com/delta/sw)) | 仅 OpenCL 3.0 ([src](https://example.com/echo/sw)) |

每个单元格区分"厂商宣称"与"第三方复现"，未被独立复现的营销宣称整行视为未证实。

---

## 3. KTD Comparison（关键技术对比）

| 技术指标 | P1 | P2 | P3 | P4 | P5 | 来源 |
|---|---|---|---|---|---|---|
| 制程节点（foundry 变体） | TSMC N3E ([src](https://example.com/alpha/process)) | Samsung SF4X ([src](https://example.com/bravo/process)) | TSMC N3P ([src](https://example.com/charlie/process)) | TSMC N4P ([src](https://example.com/delta/process)) | Samsung SF4 ([src](https://example.com/echo/process)) | [demo fab 汇总](https://example.com/fab) |
| 封装方案 | CoWoS-L ([src](https://example.com/alpha/pkg)) | FOPLP ([src](https://example.com/bravo/pkg)) | CoWoS-L ([src](https://example.com/charlie/pkg)) | EMIB ([src](https://example.com/delta/pkg)) | FOPLP ([src](https://example.com/echo/pkg)) | [demo 封装汇总](https://example.com/pkg) |
| 核心微架构单元 + 代次 | Tensor Engine Gen5 ×144 ([src](https://example.com/alpha/ucode)) | CUDA-like SM Gen3 ×128 ([src](https://example.com/bravo/ucode)) | Dataflow Tile Gen4 ×96 ([src](https://example.com/charlie/ucode)) | SM Gen2 ×80 ([src](https://example.com/delta/ucode)) | NPU Cluster Gen5 ×64 ([src](https://example.com/echo/ucode)) | [demo 微架构汇总](https://example.com/ucode) |
| L0/L1/L2 cache + RF | L0 16 KB / L1 256 KB / L2 96 MB, RF 256 KB per SM ([src](https://example.com/alpha/cache)) | L0 8 KB / L1 128 KB / L2 64 MB ([src](https://example.com/bravo/cache)) | L0 32 KB / L1 512 KB / L2 128 MB ([src](https://example.com/charlie/cache)) | L0 8 KB / L1 64 KB / L2 48 MB ([src](https://example.com/delta/cache)) | L0 4 KB / L1 32 KB / L2 32 MB ([src](https://example.com/echo/cache)) | [demo cache 汇总](https://example.com/cache) |
| HBM 代次 + stack + 容量 + 带宽 | HBM3e 8-Hi 192 GB 4.8 TB/s ([src](https://example.com/alpha/hbm)) | HBM3 8-Hi 160 GB 3.2 TB/s ([src](https://example.com/bravo/hbm)) | HBM3e 8-Hi 192 GB 4.0 TB/s ([src](https://example.com/charlie/hbm)) | HBM3 8-Hi 96 GB 2.4 TB/s ([src](https://example.com/delta/hbm)) | HBM3 4-Hi 64 GB 2.0 TB/s ([src](https://example.com/echo/hbm)) | [demo HBM 汇总](https://example.com/hbm) |
| 互连 protocol + 带宽 + 拓扑 | AlphaLink Gen2 900 GB/s all-to-all mesh ([src](https://example.com/alpha/link)) | PCIe5 128 GB/s + CXL 2.0 ([src](https://example.com/bravo/link)) | CXL 3.0 128 GB/s + fat-tree ([src](https://example.com/charlie/link)) | PCIe5 128 GB/s ([src](https://example.com/delta/link)) | PCIe5 64 GB/s ([src](https://example.com/echo/link)) | [demo 互连汇总](https://example.com/link) |
| 编译器 + 版本 | AlphaCompiler 4.1 ([src](https://example.com/alpha/compiler)) | Triton 3.0 ([src](https://example.com/bravo/compiler)) | CharlieDF 2.5 + Triton 3.0 ([src](https://example.com/charlie/compiler)) | ONNX-RT 1.19 ([src](https://example.com/delta/compiler)) | OpenCL 3.0 ([src](https://example.com/echo/compiler)) | [demo 编译器汇总](https://example.com/compiler) |
| Die size + 公开 yield 估算 | 814 mm², 68% yield ([src](https://example.com/alpha/die)) | 712 mm², 74% yield ([src](https://example.com/bravo/die)) | 780 mm², 65% yield ([src](https://example.com/charlie/die)) | 520 mm², 82% yield ([src](https://example.com/delta/die)) | 420 mm², 85% yield ([src](https://example.com/echo/die)) | [demo die 汇总](https://example.com/die) |

**Benchmark Methodology 脚注（必填）**
- 硬件配置：每个 P1–P5 的单机 8 卡节点，2 × 400G NIC 互连 — 来源：[demo 测试条件 v1.2](https://example.com/bench/hwconfig)
- 软件栈：driver 535.x / runtime 12.3 / compiler AlphaCompiler 4.1 / 框架 PyTorch 2.5 + vLLM 0.6 — 来源：[demo 软件栈披露](https://example.com/bench/sw)
- 工作负载（模型 + 参数量 + context length）：Llama-3 70B MoE，context length 8192 — 来源：[demo 模型披露](https://example.com/bench/model)
- 精度：FP8 E4M3 推理 + BF16 training — 来源：[demo 精度说明](https://example.com/bench/precision)
- Batch size + sequence length：batch 32，seqlen 8192，prefix 256 — 来源：[demo batch 说明](https://example.com/bench/batch)
- 测试日期 + 评测机构：2025-11 demo 评测机构第三方复现 — 来源：[demo methodology 报告](https://example.com/bench/methodology)

### 3.1 技术架构图集

![P1 架构图](https://example.com/alpha/whitepaper/arch.png)
*图 6：P1 架构图 — 来源：[alpha 官方白皮书 p.12](https://example.com/alpha/whitepaper)*

![P2 架构图](https://example.com/bravo/whitepaper/arch.png)
*图 7：P2 架构图 — 来源：[bravo 官方白皮书 p.8](https://example.com/bravo/whitepaper)*

![P3 架构图](https://example.com/charlie/whitepaper/arch.png)
*图 8：P3 架构图 — 来源：[charlie 官方白皮书 p.15](https://example.com/charlie/whitepaper)*

![P4 架构图](https://example.com/delta/whitepaper/arch.png)
*图 9：P4 架构图 — 来源：[delta 官方白皮书 p.5](https://example.com/delta/whitepaper)*

![P5 架构图](https://example.com/echo/whitepaper/arch.png)
*图 10：P5 架构图 — 来源：[echo 官方白皮书 p.9](https://example.com/echo/whitepaper)*

---

## 4. Moat Analysis（领先产品 P1 alpha-A100）

五轴壁垒分析，每一轴挂载具体法律或商业级证据：

| 壁垒轴 | 证据 | 24 个月内可被复制？ | 来源 |
|---|---|---|---|
| 专利 | US11987654 覆盖 AlphaLink 互连 credit-based flow control；US12345678 覆盖 FP8 E4M3 硬件路径 | 否 — 独立权利要求覆盖核心协议栈，绕行成本高 | [patent:US11987654](https://example.com/alpha/patent-11987654) |
| 制程 / fab | 与 foundry 签三年 TSMC N3E 产能预留协议，月产 12k wafer | 否 — 2025–2027 产能已排满 | [demo 8-K filing](https://example.com/alpha/filing-8k) |
| 生态 | PyTorch 2.5 + vLLM 0.6 + TensorRT-LLM 原生后端；GitHub repo 18k star / 月均 120 PR merge | 是 — 若跟随者有同等编译器团队 | [demo GitHub repo](https://example.com/alpha/github) |
| 数据 / 学习闭环 | Telemetry 每月回流 4 PB 真实 inference trace，滚动 fine-tune 编译器调度 | 否 — 依赖已部署装机量 | [demo 飞轮披露](https://example.com/alpha/flywheel) |
| 人才 / 组织 | 核心编译器团队 32 人，过去 18 个月零流失 — 参见公开招聘页 | 部分 — 市场人才稀缺 | [demo 招聘页](https://example.com/alpha/careers) |

---

## 5. Cross-Product Insight

- 共同范式：五款产品都以 HBM + chiplet + 自研高带宽互连为基础 ([demo 趋势分析](https://example.com/crossproduct/trend))
- 分歧点：计算核心在 GPGPU 与 Dataflow/Systolic 两条路线间分裂 ([demo 架构路线对比](https://example.com/crossproduct/arch))
- 引领者：P1 alpha-A100 在峰值 + 编译器 + 装机量三项同时占优 ([demo 对比分析](https://example.com/alpha/compare))
- 跟随者：P2 bravo-B2 与 P3 charlie-C3 仍处于软件生态追赶期 ([demo 追赶分析](https://example.com/followers))
- 出局信号：只支持 OpenCL 的 P5 echo-E5 在主流 LLM 工作负载上被开发者社区抛弃 ([demo echo 退潮分析](https://example.com/echo/decline))
- 被市场证伪的旧假设：2023 年前曾假设 PCIe5 足以取代专有总线，2024 年所有头部产品重回专有高带宽互连 ([demo PCIe5 限制分析](https://example.com/pcie5-limit))

---

## 6. Implication（So what?）

- 高杠杆切入维度：Dataflow 编译器 + CXL 3.0 互连是目前证据最薄的差异化空间 ([demo 切入机会分析](https://example.com/implication/entry))
- 已被证伪、应避开的路径：仅靠 PCIe5 与开源编译器无法构建可竞争的数据中心产品 ([demo 失败案例](https://example.com/implication/dead-ends))
- 可直接复用的工程事实：HBM3e 192 GB 已是 2025 年旗舰门槛，低于此容量将直接失去 LLM 训练市场 ([demo HBM 门槛](https://example.com/implication/hbm-floor))

---

## 7. Investor Appendix（投资级附录）

### 7.1 Unit Economics（单位经济性）
- ASP：P1 $38k / P2 $28k / P3 $32k — 来源：[demo 渠道价分析](https://example.com/invest/asp)
- BoM / wafer cost 估算：P1 die 814 mm² × TSMC N3E wafer $18k × 68% yield + 192 GB HBM3e ≈ 单卡材料成本 $9.6k — 来源：[demo 成本拆解](https://example.com/invest/bom)
- 毛利率区间：P1 60–64% 财报披露 — 来源：[demo 10-K 2024](https://example.com/invest/10k)
- CapEx intensity：每亿美元营收对应 CapEx $22M — 来源：[demo CapEx 模型](https://example.com/invest/capex)

### 7.2 Customer Concentration（客户集中度）
- Top-3 客户份额：DemoCloud 28% + DemoSky 17% + DemoLab 9% = 54% — 来源：[demo 10-K 风险披露](https://example.com/invest/concentration)
- 命名 design win：DemoCloud Orion 集群 / $1.2B 三年合同 — 来源：[demo press release](https://example.com/invest/designwin)
- 客户切换成本：AlphaCompiler 深度绑定 PyTorch 算子，客户软件迁移需 ≥6 个月 — 来源：[demo 分析师备忘录](https://example.com/invest/switching)

### 7.3 Capacity & Supply（产能与供应链约束）
- 前端产能：TSMC N3E 月产 12k wafer start，已预订至 2027 Q2 — 来源：[demo 8-K capacity reservation](https://example.com/invest/fab)
- 后端产能：CoWoS-L 月产 8k wafer，占 TSMC CoWoS 总产能 18% — 来源：[demo Nikkei 产能报道](https://example.com/invest/cowos)
- 关键物料：HBM3e 由 SK hynix 60% + Micron 40% 双源供货 — 来源：[demo HBM 分配披露](https://example.com/invest/hbm)
- 24 个月最紧绳结：CoWoS-L 后端产能 — 来源：[demo 瓶颈分析](https://example.com/invest/bottleneck)

### 7.4 Regulatory & Geopolitical（监管与地缘暴露）
- 出口管制：受 15 CFR Part 744 + BIS ECCN 3A090 约束，中国大陆需许可证 — 来源：[demo BIS 文件](https://example.com/invest/bis)
- 国家安全审查：CFIUS 2024 对 DemoCorp 收购案出具无异议函 — 来源：[demo CFIUS 公告](https://example.com/invest/cfius)
- 区域市场准入：欧盟 CE / 美国 FCC / 印度 BIS 均已认证 — 来源：[demo 合规披露](https://example.com/invest/compliance)
- 地缘冲突暴露：台海相关供应链占 P1 前端 100%，公司公开备援方案依赖 Samsung SF4X 二源 — 来源：[demo 风险备忘录](https://example.com/invest/geopolitical)

---

## 8. Sources

| # | 标题 | 等级 | 链接 |
|---|---|---|---|
| 1 | alpha 定位 | T2 | [link](https://example.com/alpha/positioning) |
| 2 | demo 2024 云 AI 处理器报告 | T3 | [link](https://example.com/reports/2024-ai-processor) |
| 3 | alpha 官方白皮书 | T1 | [link](https://example.com/alpha/whitepaper) |
| 4 | bravo 官方白皮书 | T1 | [link](https://example.com/bravo/whitepaper) |
| 5 | charlie 官方白皮书 | T1 | [link](https://example.com/charlie/whitepaper) |
| 6 | delta 官方白皮书 | T1 | [link](https://example.com/delta/whitepaper) |
| 7 | echo 官方白皮书 | T1 | [link](https://example.com/echo/whitepaper) |
| 8 | patent:US11987654 | T1 | [link](https://example.com/alpha/patent-11987654) |
| 9 | demo 8-K filing | T1 | [link](https://example.com/alpha/filing-8k) |
| 10 | demo 10-K 2024 | T1 | [link](https://example.com/invest/10k) |
| 11 | demo methodology 报告 | T3 | [link](https://example.com/bench/methodology) |
| 12 | demo BIS 文件 | T1 | [link](https://example.com/invest/bis) |

> T1+T2 占比必须 ≥ 50%。
