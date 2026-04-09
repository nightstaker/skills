# [场景名称] · 未来趋势洞察

> 报告类型：B — 未来技术趋势洞察
> 生成日期：YYYY-MM-DD
> 读者画像：资深领域专家 + 领域投资者
> 作者：tech-insight skill

## 1. Scene Anchor（场景锚点）

用一段可被拍摄的场景描述开篇，给出至少一个真实已落地的 pilot 部署（公司名 + 时间 + 披露源）。

![场景图](assets/<slug>/scene.jpg)
*图 1：典型应用场景 — 来源：[原始出处](URL)*

**已落地 pilot（锚点）**：客户名 / 部署时间 / 规模 / 披露源 — [src](URL)

---

## 2. Vendor Landscape（厂商动态，近 6–12 个月）

| # | 厂商 | 动作类型 | 内容 | 时间 | 财务 / 产能信号 | 对场景的意义 | 来源 |
|---|---|---|---|---|---|---|---|
| 1 | A | 产品发布 | … | YYYY-MM | 营收占比 / CapEx / 研发投入 | … | [src](URL) |
| 2 | B | 专利 | … | YYYY-MM | … | … | [src](URL) |
| 3 | C | 收购 | … | YYYY-MM | … | … | [src](URL) |

### 2.1 厂商代表产品图

![厂商 A 代表产品](assets/<slug>/vendor-a-hero.jpg)
*图 2：厂商 A 代表产品 — 来源：[官方页面](URL)*

![厂商 B 代表产品](assets/<slug>/vendor-b-hero.jpg)
*图 3：厂商 B 代表产品 — 来源：[官方页面](URL)*

![厂商 C 代表产品](assets/<slug>/vendor-c-hero.jpg)
*图 4：厂商 C 代表产品 — 来源：[官方页面](URL)*

---

## 3. Key Technology Decomposition

每项关键技术必须填齐以下**六元组**：

### 3.1 关键技术 1：…

- **原理（含算法 / 架构选择 / 设计常数）**：…（带源）
- **TRL**：x/9 — 理由（带源）
- **具体瓶颈（可量化）**：例："KV cache 内存占用随 seqlen 线性增长，64K ctx 下占卡显存 58%" — [src](URL)
- **突破方向 + 代表论文 / 专利**：命名候选方案 + [paper](URL) / [patent](URL)
- **最新公开 benchmark（含完整方法论）**：数字 + 硬件 + 软件 + 模型 + batch + seqlen + precision + 日期 — [src](URL)
- **关键玩家与专利壁垒**：≥1 专利号（US/CN/EP/WO）+ ≥1 论文 — [patent:XXX](URL) / [paper](URL)

![关键技术 1 原理图](assets/<slug>/tech-1-arch.png)
*图 5：关键技术 1 原理示意 — 来源：[论文 fig.X](URL)*

### 3.2 关键技术 2：…

- **原理**：…（带源）
- **TRL**：x/9 — 理由（带源）
- **具体瓶颈**：…（带源）
- **突破方向**：…（带源）
- **最新 benchmark**：…（带完整方法论 + 源）
- **专利壁垒**：专利号 + 一句话权利要求 — [patent:XXX](URL)

![关键技术 2 原理图](assets/<slug>/tech-2-arch.png)
*图 6：关键技术 2 原理示意 — 来源：[论文 fig.X](URL)*

---

## 4. Trend Prediction

- **未来产品形态**：…（带源）
- **时间窗口**：12 / 24 / 36 个月（择一并承诺）
- **核心假设（≤5）**：
  1. 假设 A — 可证伪条件：观察到 X 时此假设被推翻（带源）
  2. 假设 B — 可证伪条件：…
  3. 假设 C — 可证伪条件：…
- **预测偏差的代价**：如果预测错了，应对成本是多少（供应链重建 / 研发 pivot / 订单违约）— [src](URL)

---

## 5. Closed Loop（技术 → 产品 → 客户/场景 → 商业价值）

| 节点 | 内容 | 关键假设 |
|---|---|---|
| 技术 | … | … |
| 产品 | … | … |
| 客户 / 场景 | … | … |
| 商业价值 | TAM / SAM / SOM / ARPU（择一量化 + 算法说明）— 来源：[src](URL) | … |

**商业节点补充四项**：
- **单位经济性锚点**：ASP / gross margin / CapEx per unit / ARPU — [src](URL)
- **客户集中度假设**：头部 3 客户份额推测 — [src](URL)
- **产能与供应链约束**：支撑闭环所需的 fab / HBM / CoWoS / substrate 关键资源的公开可用性 — [src](URL)

---

## 6. Implication（So what?）

- 本季度 / 本年应采取的具体动作：…
- 应放弃的旧路径：…
- 应锁定的稀缺资源：…

> 禁止 "需要持续关注 / 值得观察 / 未来可期 / 业界领先 / 先进架构 / 生态完善" 类填充语与浅层短语。

---

## 7. Investor Appendix（投资级附录）

### 7.1 Unit Economics
- **ASP**：…（带源）
- **BoM / 成本估算**：…（带源）
- **毛利率**：…（带源）
- **CapEx intensity**：…（带源）

### 7.2 Customer Concentration
- **Top-3 客户份额**：…（带源 或 "无公开披露"）
- **命名 design win**：…（带源）
- **切换成本信号**：…（带源）

### 7.3 Capacity & Supply
- **前端产能**：…（带源）
- **后端产能 / 封装**：…（带源）
- **关键物料 / HBM**：…（带源）
- **24 个月内最紧绳结**：一句话结论 [来源](URL)

### 7.4 Regulatory & Geopolitical
- **出口管制**：引用具体规则编号（15 CFR 744 / BIS ECCN / EAR）— [来源](URL)
- **国家安全审查**：CFIUS / SAMR / CMA — [来源](URL)
- **区域准入**：CCC / CE / FCC — [来源](URL)
- **地缘冲突**：…（带源）

---

## 8. Sources

| # | 标题 | 等级 | 链接 |
|---|---|---|---|
| 1 | … | T1 | [link](URL) |
| 2 | … | T1 | [link](URL) |
| 3 | … | T2 | [link](URL) |
| … | … | … | … |
