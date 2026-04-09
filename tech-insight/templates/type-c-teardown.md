# [产品名称] · 单品深度拆解

> 报告类型：C — 单品深度 Teardown
> 生成日期：YYYY-MM-DD
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

![产品图](assets/<slug>/hero.jpg)
*图 1：官方产品图 — 来源：[厂商发布页](URL)*

---

## 2. Architecture Decomposition（架构拆解）

### 2.1 计算 / 逻辑组织

…（核数、层级、关键微架构选择，带源）

### 2.2 存储子系统

…（容量、带宽、层级、关键参数，带源）

### 2.3 互连 / I/O

…（总线、协议、拓扑，带源）

### 2.4 软件栈

…（编译器 / 运行时 / 驱动 / SDK，开放 vs 私有，带源）

### 2.5 封装 / 集成

…（Chiplet、2.5D/3D、CoWoS、异构集成，带源）

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
| 制程节点 | … | — | … | … | [src](URL) |
| 峰值算力 | … | FP8 dense, batch 1 | … | … | [src](URL) |
| 显存容量 | … | — | … | … | [src](URL) |
| 显存带宽 | … | — | … | … | [src](URL) |
| 功耗 / TDP | … | typical / peak | … | … | [src](URL) |
| 延迟 / 吞吐 | … | workload, batch | … | … | [src](URL) |
| 面积 / die size | … | — | … | … | [src](URL) |

> 厂商自报数据在单元格里注明"厂商宣称"；第三方复现数据无需额外注明。

---

## 4. Moat Analysis（壁垒分析）

| 壁垒类型 | 内容 | 24 个月内可被复制？ | 来源 |
|---|---|---|---|
| 专利 | …（至少两项代表性专利） | 是 / 否 — 一句话理由 | [patent:XXX](URL) |
| 制程 / fab | …（节点 / CoWoS / HBM 供货） | 是 / 否 — 一句话理由 | [src](URL) |
| 生态 | …（框架 / 伙伴锁定 / 开发者基数） | 是 / 否 — 一句话理由 | [src](URL) |
| 数据 / 学习闭环 | …（如有） | 是 / 否 — 一句话理由 | [src](URL) |
| 人才 / 组织 | …（仅限公开报道） | 是 / 否 — 一句话理由 | [src](URL) |

---

## 5. Weakness / Risk Analysis（弱点 / 风险）

- **工程弱点**：…（相对最强替代的劣势指标，带源）
- **供应链风险**：…（fab / HBM / 封装依赖，带源）
- **路线图风险**：…（delay / descope 的公开信号，带源）
- **生态风险**：…（客户集中度 / 开源替代加速，带源）
- **监管风险**：…（出口管制 / 反垄断 / 认证暴露，带源）

> 无公开证据的风险类别直接写"无公开证据"，不得臆造。

---

## 6. Implication（So what?）

- 值得直接借鉴 / 授权的工程选择：…
- 弱点撕开的差异化切入口：…
- 本季度应采取的具体动作（合同 / 供货 / 人才）：…

> 禁止 "需要持续关注 / 值得观察 / 未来可期" 类填充语。

---

## 7. Sources

1. [Source 1 title](URL)
2. [Source 2 title](URL)
3. [Source 3 title](URL)
…
