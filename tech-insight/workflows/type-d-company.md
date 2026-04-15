# Workflow: Type D — 公司技术洞察 (Company Technology Insight)

Use this workflow when the user asks for a comprehensive technology analysis of a specific company — covering its product portfolio, corporate strategy, technology roadmap, and deriving actionable implications for a business unit.

Read [../REQUIREMENT.MD](../REQUIREMENT.MD) §2.4 before starting. Output template: [../templates/type-d-company.md](../templates/type-d-company.md).

The structure follows: company profile → product portfolio & strategy analysis → competitiveness summary & business unit implication.

---

## Step 1 — Define Analysis Scope

Before searching, confirm with the user:

- **公司名称**：exact company name (legal entity if relevant)
- **分析范围**：full company or specific business unit / division?
- **重点关注**：overall tech strategy, specific product lines, competitive positioning, or M&A activity?
- **对标视角**：who is the "我方" for the implication section? Which business unit will use this analysis?

If the company is a conglomerate (e.g., Samsung, Alphabet), negotiate which division to focus on — a full-conglomerate analysis is too broad for a single report.

---

## Step 2 — Company Profile

Collect from primary sources (10-K, annual reports, official website, CrunchBase, Bloomberg):

| Item | Data | Source |
|---|---|---|
| Company name | … | [src](URL) |
| Founded | … | [src](URL) |
| Headquarters | … | [src](URL) |
| Core business areas | … | [src](URL) |
| Revenue (latest FY) | … | [src](URL) |
| Employee count | … | [src](URL) |
| Market cap / Valuation | … | [src](URL) |

Use `WebSearch` + `WebFetch`. For publicly traded companies, prefer SEC/regulatory filings as primary source. For private companies, use CrunchBase + press releases.

---

## Step 3 — Development History & Milestones

Build a chronological timeline of key events:

| Time | Event | Impact | Source |
|---|---|---|---|
| YYYY | Founded / spun off | … | [src](URL) |
| YYYY | Key product launch | … | [src](URL) |
| YYYY | Major acquisition | … | [src](URL) |
| YYYY | Strategic pivot | … | [src](URL) |

Focus on events that shaped the company's **current technology position**:
- Major M&A that brought in key technology or talent
- Product launches that defined market position
- Strategic pivots that changed technology direction
- Partnerships / JVs that expanded technology access

---

## Step 4 — Visual Asset Collection (MANDATORY, runs BEFORE writing)

1. **Product portfolio visualization**: create or source a product matrix / landscape map. Save as `assets/<slug>/product-portfolio.png`.
2. **Core product photos** (2-3): from vendor product pages. Save as `assets/<slug>/core-product<N>.jpg`.
3. **Strategic context visuals** (if available): org chart, technology roadmap, patent landscape. Save as `assets/<slug>/strategy-*.png`.

Record every image in `assets/<slug>/image_manifest.json`. Run [../scripts/visual_collector.py](../scripts/visual_collector.py) for bulk download.

---

## Step 5 — Product Portfolio Analysis

### 5.1 Product Matrix

Map the company's product lines:

| Product Line | Market Position | Target Customer | Revenue Contribution | Key Competitor | Source |
|---|---|---|---|---|---|
| … | … | … | … | … | [src](URL) |

Embed a product portfolio visualization showing how products relate to each other and to market segments.

### 5.2 Core Product Deep Dive (2-3 products)

For each core product:

- **Market performance**: share, revenue, growth rate (with sources)
- **Competitive advantage**: what makes it win? (distinguish marketing from engineering facts)
- **Technology highlights**: key technical differentiators (with sources)
- Embed product photo with caption

Selection criteria for "core" products: highest revenue contribution, fastest growing, or most strategically significant (state which criterion you used).

---

## Step 6 — Company Strategy & Technology Roadmap

### 6.1 Strategic Direction

Extract from **public sources only** — no speculation:

| Signal Source | Evidence | Strategic Direction Implied | Source |
|---|---|---|---|
| Earnings call / investor day | CEO: "We are investing heavily in X" | Doubling down on X | [src](URL) |
| Patent filings (last 24 months) | X patents in area Y | Building IP moat in Y | [src](URL) |
| M&A activity | Acquired company Z for $Xm | Acquiring capability in Z's domain | [src](URL) |
| Hiring trends | X open positions in area Y | Scaling team for Y | [src](URL) |
| R&D spending | R&D grew X% YoY to $Xb | Increasing research intensity | [src](URL) |

### 6.2 Technology Roadmap

| Technology Area | Approach (自研/收购/合作) | Patent Count | R&D Investment Trend | Source |
|---|---|---|---|---|
| … | … | … | … | [src](URL) |

### 6.3 Technology Capability Assessment

| Dimension | Assessment | Evidence | Source |
|---|---|---|---|
| 人才储备 | … (quantify: key hires, team size, academic ties) | … | [src](URL) |
| 专利壁垒 | … (quantify: patent count, key patents, litigation) | … | [src](URL) |
| 工程化能力 | … (evidence: production scale, yield, quality metrics) | … | [src](URL) |
| 生态位 | … (ecosystem lock-in, partnerships, standards influence) | … | [src](URL) |

---

## Step 7 — Competitiveness Summary & Business Unit Implication

### 7.1 Technology Competitiveness Summary

Structured synthesis:
- **Core strengths**: 2-3 technology advantages with evidence
- **Potential risks**: 2-3 technology vulnerabilities or dependencies
- **Strategic blind spots**: areas where the company is under-investing relative to market direction

### 7.2 Business Unit Implication (So what?)

Concrete, actionable insights for the reader's business unit:
- **竞争策略建议**：how should we compete against this company? Head-on, flanking, or avoid?
- **合作机会**：are there areas where partnership is more valuable than competition?
- **技术差距弥补路径**：where are we behind, and what's the fastest path to close the gap?
- **差异化切入点**：where is this company NOT investing that represents an opportunity for us?

Forbidden phrases: "需要持续关注", "值得观察", "未来可期". The linter will reject them.

---

## Step 8 — QA Gate

```bash
python scripts/linter.py reports/<slug>.md --assets assets/<slug>/ --type D
```

The linter rejects the report if:

- Missing any of the four mandatory layers (公司概览 / 产品布局分析 / 公司战略与技术路线 / 总结与事业单元启示).
- Product portfolio visualization is missing.
- Any core product is missing its product photo.
- Any factual sentence is not inline-sourced.
- Any image lacks the `图 X：[说明] — 来源：[链接]` caption.
- Technology capability assessment table is missing.
- The Implication contains filler phrases.

Fix every failure before delivery.

---

## Deliverable

- `reports/<slug>.md` — the report
- `assets/<slug>/` — product photos, strategy visuals + `image_manifest.json`
- Numbered "Sources" section at the end of the report

---

## Related Workflows

This Type D workflow leverages shared analysis workflows:
- [Landscape](landscape.md) — for competitive positioning of the company's product portfolio
- [Benchmark](benchmark.md) — for evidence collection on company metrics and competitive data
- [Deep Dive](deep-dive.md) — for deep analysis of specific technology areas within the company's portfolio

Final assembly follows the [Briefing](briefing.md) workflow pattern.
