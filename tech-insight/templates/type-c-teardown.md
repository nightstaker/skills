# [产品名称] · 单品深度拆解

> 报告类型：C — 单品深度 Teardown
> 生成日期：YYYY-MM-DD
> 读者画像：资深领域专家 + 领域投资者
> 作者：tech-insight skill

## 1. Product Profile（产品画像）

| 维度 | 内容 | 来源 |
|---|---|---|
| 厂商 | … | [src](URL) |
| 产品线 / 型号 | … | [src](URL) |
| 最新版本 | … | [src](URL) |
| 上市时间 | YYYY-MM | [src](URL) |
| 价格 / 价格段 | … | [src](URL) |
| 目标客户 | … | [src](URL) |
| 部署形态 | … | [src](URL) |
| 厂商 headline claim | "…" | [src](URL) |
| 公开 traction | 出货量 / 装机量 / 榜单 | [src](URL) |
| Top-3 design win | 客户 + 项目代号 + 金额 | [src](URL) |

![产品图](assets/<slug>/hero.jpg)
*图 1：官方产品图 — 来源：[厂商发布页](URL)*

---

## 2. Architecture Decomposition（架构拆解）

### 2.1 计算 / 逻辑组织

| 字段 | 内容 | 来源 |
|---|---|---|
| 微架构单元命名 + 代次 | 例：SM Gen 5 / Tile Cluster / NPU Cluster | [src](URL) |
| 单元数量 | 数量 | [src](URL) |
| MAC 阵列规模 | 行 × 列 | [src](URL) |
| Data-path 位宽 | bit | [src](URL) |
| 支持的数值格式 | FP32 / TF32 / BF16 / FP16 / FP8 / INT8 / INT4 / W4A16 | [src](URL) |
| L0 / L1 / L2 / LLC cache 大小 | KB / MB | [src](URL) |
| Register file 大小 | KB 每单元 | [src](URL) |
| 关键 trade-off | 例：sliding-window attention 换 KV cache 压缩 8× | [src](URL) |

### 2.2 存储子系统

| 字段 | 内容 | 来源 |
|---|---|---|
| HBM 代次 + stack 层数 | 例：HBM3e / 8-Hi | [src](URL) |
| 容量 | GB | [src](URL) |
| 带宽 | TB/s | [src](URL) |
| 内存控制器数量 | … | [src](URL) |
| 地址映射策略 | 例：NUMA / UMA / 直通 | [src](URL) |
| 片上 SRAM 总量 | MB | [src](URL) |

### 2.3 互连 / I/O

| 字段 | 内容 | 来源 |
|---|---|---|
| Protocol + 代次 | 例：NVLink 5 / Infinity Fabric / CXL 3.1 / UCIe / RoCE v2 | [src](URL) |
| 带宽 | GB/s | [src](URL) |
| 拓扑 | mesh / fat-tree / dragonfly | [src](URL) |
| 最大扩展规模 | 节点数 | [src](URL) |

### 2.4 软件栈

| 字段 | 内容 | 来源 |
|---|---|---|
| 编译器 + 版本 | … | [src](URL) |
| Runtime / driver | … | [src](URL) |
| 支持的框架与版本矩阵 | PyTorch / JAX / TensorFlow / vLLM / TensorRT | [src](URL) |
| 开源成熟度 | GitHub star / contributor / 月 PR merge 数 | [src](URL) |

### 2.5 封装 / 集成

| 字段 | 内容 | 来源 |
|---|---|---|
| Foundry 节点变体 | 例：TSMC N3E / Samsung SF4X / Intel 18A | [src](URL) |
| 封装方案 | CoWoS-L / FOPLP / EMIB | [src](URL) |
| Interposer 尺寸 | mm² | [src](URL) |
| 模块集成度 | 例：SoC + HBM + CPO / 2.5D 集成 | [src](URL) |
| 公开 die size / yield | mm² / % | [src](URL) |

![架构总览](assets/<slug>/arch-overview.png)
*图 2：系统架构总览 — 来源：[官方白皮书 p.X](URL)*

![架构细节](assets/<slug>/arch-detail.png)
*图 3：关键子系统拆解 — 来源：[teardown 报告](URL)*

![Die shot / 内部](assets/<slug>/dieshot.png)
*图 4：Die shot / PCB / 内部拆解 — 来源：[TechInsights](URL)*

---

## 3. Key Technical Metrics（关键技术指标）

| 指标 | 值 | 测试条件 | 对标参考 | Δ | 来源 |
|---|---|---|---|---|---|
| 制程节点（变体） | TSMC N3E | — | 对标 Samsung SF4X | … | [src](URL) |
| 峰值算力 | 数字 + 单位 | batch X, seqlen Y, precision Z | … | … | [src](URL) |
| HBM 容量 / 带宽 | GB / TB/s | — | … | … | [src](URL) |
| 功耗 / TDP | W | typical / peak | … | … | [src](URL) |
| 延迟 / 吞吐 | ms / tokens/s | workload + batch | … | … | [src](URL) |
| 能效 | TOPS/W | — | … | … | [src](URL) |
| Die size | mm² | — | … | … | [src](URL) |
| Yield 估算 | % | foundry 公开 / 二手估算 | … | … | [src](URL) |

**Benchmark Methodology Footer（必填）**
- 硬件配置：… [src](URL)
- 软件栈：driver / runtime / compiler / 框架版本 [src](URL)
- 工作负载：模型 + 参数量 + context length [src](URL)
- 精度：FP8 / FP16 / BF16 / INT8 [src](URL)
- Batch size + sequence length：… [src](URL)
- 测试日期 + 评测机构：… [src](URL)

> 厂商自报数据在单元格里注明"厂商宣称"；需被一条独立 benchmark 或 teardown 配对。

---

## 4. Moat Analysis（壁垒分析）

| 壁垒类型 | 具体证据 | 24 个月内可被复制？ | 来源 |
|---|---|---|---|
| 专利 | ≥1 代表性 patent # + 独立权利要求概述 | 是 / 否 — 理由 | [patent:US12345678](URL) |
| 制程 / fab | 长期产能协议 + 节点分配 | 是 / 否 — 理由 | [SEC filing](URL) |
| 生态 | 开源指标 + 命名框架支持 | 是 / 否 — 理由 | [GitHub repo](URL) |
| 数据 / 学习闭环 | 数据集规模 + 飞轮速度 | 是 / 否 — 理由 | [blog](URL) |
| 人才 / 组织 | 核心团队 + 公开报道 | 是 / 否 — 理由 | [media](URL) |

---

## 5. Weakness / Risk Analysis（弱点 / 风险）

- **工程弱点**：具体指标劣势 + 最强替代对比 — 来源：[src](URL)
- **供应链风险**：fab / HBM / 封装 依赖 — 来源：[src](URL)
- **路线图风险**：delay / descope 公开信号 — 来源：[src](URL)
- **生态风险**：客户集中度 / 开源替代加速 — 来源：[src](URL)
- **监管风险**：出口管制 / 反垄断 / 认证暴露 — 来源：[src](URL)

> 无公开证据的风险类别直接写"无公开证据"，不得臆造。

---

## 6. Implication（So what?）

- 值得直接借鉴 / 授权的工程选择：…
- 弱点撕开的差异化切入口：…
- 本季度应采取的具体动作（合同 / 供货 / 人才）：…

> 禁止 "需要持续关注 / 值得观察 / 未来可期 / 业界领先 / 先进架构 / 生态完善" 类填充语与浅层短语。

---

## 7. Investor Appendix（投资级附录）

### 7.1 Unit Economics
- **ASP**：…（带源）
- **BoM / wafer cost 估算**：…（SemiAnalysis / TechInsights，带源）
- **毛利率区间**：…（财报，带源）
- **CapEx intensity**：…（带源）

### 7.2 Customer Concentration
- **Top-3 客户份额**：…（带源 或 "无公开披露"）
- **命名 design win**：…（带源）
- **切换成本信号**：…（带源）

### 7.3 Capacity & Supply
- **前端产能**：foundry 节点 wafer start — [来源](URL)
- **后端产能**：CoWoS / FOPLP — [来源](URL)
- **关键物料**：HBM / substrate — [来源](URL)
- **24 个月瓶颈**：…（一句话结论 + 源）

### 7.4 Regulatory & Geopolitical
- **出口管制**：15 CFR 744 / BIS ECCN / EAR — [来源](URL)
- **反垄断 / 国家安全**：CFIUS / SAMR / CMA — [来源](URL)
- **区域合规**：CCC / CE / FCC / BIS — [来源](URL)
- **地缘冲突**：…（带源）

---

## 8. Sources

| # | 标题 | 等级 | 链接 |
|---|---|---|---|
| 1 | … | T1 | [link](URL) |
| 2 | … | T1 | [link](URL) |
| 3 | … | T2 | [link](URL) |
| … | … | … | … |
