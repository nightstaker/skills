# Workflow: Type C — 产品技术洞察 (Product Technology Insight)

Use this workflow when the user asks for a technology teardown of a specific product — understanding its selling points, decomposing the key technical architectures behind them, and deriving actionable implications for competing or benchmarking products.

Read [../REQUIREMENT.MD](../REQUIREMENT.MD) §2.3 before starting. Output template: [../templates/type-c-product.md](../templates/type-c-product.md).

The structure follows: product overview & selling points → key architecture decomposition → summary & product implication.

---

## Step 1 — Identify the Target Product

Before searching, confirm with the user:

- **产品名称**：exact product name and model/version
- **厂商**：manufacturer / vendor
- **分析重点**：full teardown or focused on specific aspects (performance, cost, reliability, user experience)?

If the user names a product family (e.g., "iPhone") instead of a specific product (e.g., "iPhone 16 Pro"), negotiate which specific model to analyze — a family-level analysis is a different scope that may require multiple Type C runs.

---

## Step 2 — Product Overview & Market Context

Collect from primary sources:

| Item | Data | Source |
|---|---|---|
| Product name & version | … | [src](URL) |
| Vendor | … | [src](URL) |
| Target customer | … | — |
| Market position | … | [src](URL) |
| Launch date | … | [src](URL) |
| Market performance (share / sales / revenue) | … | [src](URL) |
| Price / price range | … | [src](URL) |

Use `WebSearch` + `WebFetch`. Refuse to write a field whose data cannot be traced to an official page, analyst report, or regulatory filing. If a data point is not public, write "未公开" — never guess.

---

## Step 3 — Core Selling Points & Feature Analysis

Systematically catalog the product's core selling points:

| Selling Point | Marketing Claim (厂商宣称) | Verifiable Engineering Fact (工程事实) | Source |
|---|---|---|---|
| SP 1 | "最快的处理器" | "A18 Pro: 6-core CPU, 2 performance cores @ 4.05 GHz" | [src](URL) |
| SP 2 | … | … | [src](URL) |

**Critical distinction**: every selling point must be split into:
- **Marketing claim**: what the vendor says in ads / press releases
- **Engineering fact**: what can be independently verified (benchmarks, specs, teardowns)

Identify 1-3 selling points that represent the product's **core differentiation** — these will drive the architecture teardown in the next step.

---

## Step 4 — Visual Asset Collection (MANDATORY, runs BEFORE writing)

1. **Product photo**: from the vendor product page or press kit. Save as `assets/<slug>/product-hero.jpg`.
2. **Architecture / teardown diagrams** (per key architecture): from official whitepaper, authoritative teardown (iFixit, TechInsights, AnandTech), or patent figure. Save as `assets/<slug>/arch<N>-*.png`.
3. **Context image** (if available): product in use, deployment scenario, or comparison visual. Save as `assets/<slug>/context-*.jpg`.

Record every image in `assets/<slug>/image_manifest.json`. Run [../scripts/visual_collector.py](../scripts/visual_collector.py) for bulk download.

---

## Step 5 — Key Technical Architecture Decomposition

This is the core of the report. For each of the 1-3 key architectures identified in Step 3:

### 5.1 System Architecture & Module Decomposition
- Block diagram showing major modules and their relationships
- Data/signal/control flow through the system
- Embed the architecture diagram with caption and source

### 5.2 Core Technical Principle & Implementation Path
- Plain-language but technically precise explanation of the core mechanism
- Implementation choices and their rationale (why this approach over alternatives?)
- Key design trade-offs (what was sacrificed for the chosen optimization?)

### 5.3 Key Performance Parameters
Quantitative data — every number must carry an inline source:

| Parameter | Value | Measurement Condition | Source |
|---|---|---|---|
| … | … | … | [src](URL) |

### 5.4 Innovation Points & Moat Analysis
- What is genuinely novel vs what is incremental improvement?
- Moat sources: patent protection, process know-how, ecosystem lock-in, data advantages
- How reproducible is this by competitors? Timeline estimate with justification

### 5.5 Peer Comparison (if applicable)
If the architecture can be compared with equivalent architectures in competing products:

| Metric | This Product | Competitor A | Competitor B | Source |
|---|---|---|---|---|
| … | … | … | … | [src](URL) |

---

## Step 6 — Technical Summary & Product Implication

### 6.1 Technical Summary
Concise synthesis:
- **Core competitiveness**: what makes this product technically superior? (1-3 points with evidence)
- **Technical weaknesses**: where does the technology fall short? (1-3 points with evidence)
- **Sustainability**: can this advantage be maintained? What threatens it?

### 6.2 Product Implication (So what?)
Concrete, actionable insights for benchmarking or competing products:
- **值得借鉴的技术**：which technical approaches are worth learning from and why?
- **可以超越的设计**：where did this product make suboptimal choices that can be improved upon?
- **应规避的路径**：which approaches should be avoided based on this product's experience?

Forbidden phrases: "需要持续关注", "值得观察", "未来可期". The linter will reject them.

---

## Step 7 — QA Gate

```bash
python scripts/linter.py reports/<slug>.md --assets assets/<slug>/ --type C
```

The linter rejects the report if:

- Missing any of the three mandatory layers (产品概览与卖点 / 关键技术架构拆解 / 总结与产品启示).
- Product photo is missing.
- Any key architecture is missing its teardown/architecture diagram.
- Any factual sentence is not inline-sourced.
- Any image lacks the `图 X：[说明] — 来源：[链接]` caption.
- The Implication contains filler phrases.

Fix every failure before delivery.

---

## Deliverable

- `reports/<slug>.md` — the report
- `assets/<slug>/` — product photos, architecture diagrams + `image_manifest.json`
- Numbered "Sources" section at the end of the report

---

## Related Workflows

This Type C workflow leverages shared analysis workflows:
- [Deep Dive](deep-dive.md) — for hypothesis-driven analysis of each key architecture
- [Benchmark](benchmark.md) — for evidence collection and peer comparison data

Final assembly follows the [Briefing](briefing.md) workflow pattern.
