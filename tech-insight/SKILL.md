---
name: tech-insight
description: >
  Technology intelligence and insight analysis skill. Use when the user asks for:
  technology deep-dive, tech trend analysis, technology landscape mapping,
  benchmark comparison, competitive technology analysis, technology radar,
  segmented technology domain insight, industry technology trend insight,
  product technology insight, company technology insight, tech intelligence briefing,
  技术洞察, 技术趋势, 细分技术领域洞察, 行业技术趋势洞察, 产品技术洞察, 公司技术洞察,
  产品对标, competitive analysis, tech benchmark, tech trend, roadmap insight,
  or any request requiring evidence-based technology insight generation.
  This skill produces the analytical artifacts; for strategic decisions
  (control points, objectives, strategies) hand off to tech-planning;
  for PPTX rendering hand off to pro-pptx with hw-insight template.
license: Proprietary
---

# Tech Insight — 技术洞察 Technology Intelligence Skill

A production-grade technology insight skill that turns "vibes-based commentary" into
engineered research: every fact is sourced, every key technology is decomposed, every
report carries real visual evidence from primary sources, and every insight ends with
an actionable "So what?".

Read [REQUIREMENT.MD](REQUIREMENT.MD) for the full specification.

## Quick Reference

### Report Types (output-level classification)

| Type | Name | Description | Output Template |
|------|------|------------|-----------------|
| **Type A** | 细分技术领域洞察 | Segmented technology domain — application-driven demand decomposition → TOP 5 tech deep dive → trend synthesis | [type-a-domain.md](templates/type-a-domain.md) |
| **Type B** | 行业技术趋势洞察 | Industry technology trend — industry history → per-route analysis with products → cross-route comparison & research recommendation | [type-b-industry.md](templates/type-b-industry.md) |
| **Type C** | 产品技术洞察 | Product technology — selling points → key architecture decomposition → product implication | [type-c-product.md](templates/type-c-product.md) |
| **Type D** | 公司技术洞察 | Company technology — company profile & product portfolio → strategy & tech roadmap → business unit implication | [type-d-company.md](templates/type-d-company.md) |
| **General** | Flexible analysis — deep dive, radar, evidence dossier | See general templates below |

### Type-Specific Workflows

| Workflow | Purpose |
|----------|---------|
| [Type A — Domain](workflows/type-a-domain.md) | Segmented technology domain insight (总—分—总) |
| [Type B — Industry](workflows/type-b-industry.md) | Industry technology trend insight |
| [Type C — Product](workflows/type-c-product.md) | Product technology insight |
| [Type D — Company](workflows/type-d-company.md) | Company technology insight |

### General Analysis Workflows (building blocks, usable across types)

| Workflow | Purpose |
|----------|---------|
| [Deep Dive](workflows/deep-dive.md) | Hypothesis-driven single technology analysis |
| [Landscape](workflows/landscape.md) | Multi-technology domain scan & positioning |
| [Benchmark](workflows/benchmark.md) | Evidence collection, cross-validation & comparison |
| [Briefing](workflows/briefing.md) | Final assembly into structured deliverable |

### General Output Templates

| Template | Use Case |
|----------|----------|
| [Insight Report](templates/insight-report.md) | Single-technology deep dive with hypothesis validation |
| [Landscape Scan](templates/landscape-scan.md) | Multi-technology domain scan with positioning map |
| [Tech Radar](templates/tech-radar.md) | Quarterly technology radar with ring classifications |
| [Evidence Dossier](templates/evidence-dossier.md) | Raw evidence collection organized by source type |

### QA & Tooling

| Tool | Purpose |
|------|---------|
| [scripts/linter.py](scripts/linter.py) | Report quality gate — sourcing, visuals, structure, banned phrases (supports A/B/C/D) |
| [scripts/visual_collector.py](scripts/visual_collector.py) | Bulk download primary-source images with manifest |

## Scope Boundary

```
tech-insight (this skill)
  = Technology intelligence & evidence-based analysis
  = Produces: insight reports, landscape maps, benchmark analyses, tech radars
  = The analytical engine — "What is true? What does it mean?"

tech-planning (separate skill)
  = Strategic planning & resource decisions (五看三定)
  = Consumes tech-insight outputs as input to decision-making
  = The decision engine — "What should we do?"

pro-pptx (separate skill)
  = Presentation rendering with template governance
  = Consumes tech-insight outputs as content for hw-insight template slides
  = The output engine — "How do we present it?"
```

## Scenario Detection — Two-Layer Routing

### Layer 1: Classify Report Type

```
User request
  │
  ├─ About a SPECIFIC TECHNOLOGY DOMAIN (a segmented tech area)?
  │   Wants application-driven demand analysis → TOP 5 technologies → trend synthesis?
  │   → Type A (细分技术领域洞察)
  │
  ├─ About an INDUSTRY's overall technology landscape and evolution?
  │   Wants industry history → technology routes → cross-route comparison?
  │   → Type B (行业技术趋势洞察)
  │
  ├─ About a SPECIFIC PRODUCT's technology architecture?
  │   Wants selling point analysis → key architecture teardown → product implication?
  │   → Type C (产品技术洞察)
  │
  ├─ About a SPECIFIC COMPANY's technology strategy and portfolio?
  │   Wants company profile → product portfolio → tech roadmap → business unit implication?
  │   → Type D (公司技术洞察)
  │
  ├─ Multiple types? → Run sequentially; e.g., Type C for key products first, then Type B for industry overview.
  │
  ├─ Neither fits? (general analysis, tech radar, evidence collection)
  │   → General workflow selection (Layer 2 only)
  │
  └─ Too narrow? ("just look up spec X of product Y")
      → Tell user this skill is overkill, use plain web search instead.
```

### Layer 2: Route to Workflow Combination

| Report Type | Primary Workflow | Output Template |
|-------------|-----------------|-----------------|
| **Type A** | [Type A — Domain](workflows/type-a-domain.md) | [type-a-domain.md](templates/type-a-domain.md) |
| **Type B** | [Type B — Industry](workflows/type-b-industry.md) | [type-b-industry.md](templates/type-b-industry.md) |
| **Type C** | [Type C — Product](workflows/type-c-product.md) | [type-c-product.md](templates/type-c-product.md) |
| **Type D** | [Type D — Company](workflows/type-d-company.md) | [type-d-company.md](templates/type-d-company.md) |
| **General — single tech** | [Deep Dive](workflows/deep-dive.md) | [insight-report.md](templates/insight-report.md) |
| **General — multi tech** | [Landscape](workflows/landscape.md) | [landscape-scan.md](templates/landscape-scan.md) |
| **General — evidence only** | [Benchmark](workflows/benchmark.md) | [evidence-dossier.md](templates/evidence-dossier.md) |
| **General — quarterly radar** | [Landscape](workflows/landscape.md) | [tech-radar.md](templates/tech-radar.md) |
| **Strategic decisions needed** | Complete analysis → hand off to [tech-planning](../tech-planning/SKILL.md) | — |
| **PPTX output needed** | Complete analysis → hand off to [pro-pptx](../pro-pptx/SKILL.md) with hw-insight template | — |

## Core Principles

### 1. IIR — Insight → Evidence → Implication

Every analytical output follows this structure. No exceptions.

```
Insight:      [The technical signal — what is happening, stated as a CLAIM]
Evidence:     [Verifiable data — benchmark, paper, patent, market data]
Implication:  [Industry-level meaning — what this enables/threatens/changes]
```

**Rules**:
- Insight states a CLAIM, not a description. "Transformer推理瓶颈已从算力转移至显存带宽" not "Transformer推理技术分析"
- Evidence must be verifiable and inline-sourced (see Universal Sourcing below)
- Implication is EXTERNAL/industry-level. No internal product recommendations (that's tech-planning's job)

### 2. Universal Sourcing — 全量挂源，零容忍

**Every factual sentence in the output must carry an inline source**: URL, DOI, or patent number. No exceptions.

```
✅ "H100 的 FP8 算力达到 3958 TFLOPS ([NVIDIA H100 Datasheet](https://...))"
❌ "H100 的 FP8 算力达到 3958 TFLOPS" — rejected: no source
```

**Rules**:
- Every statement, datum, quote, parameter, vendor action carries an inline source
- No "source-free sentences" in any section from analysis through implication
- Content that cannot be sourced must be deleted or quarantined into a clearly-labelled "作者推断" subsection
- Key facts (parameters, share, price) require ≥ 2 independent sources for cross-validation
- Conflicting sources: prioritize primary source, note the discrepancy

**Source priority** (whitelist order):

| Priority | Source Type | Label |
|----------|-----------|-------|
| 1 | Official vendor release / press kit | `官方发布` |
| 2 | Patent filing | `专利` |
| 3 | Peer-reviewed paper (cite venue + year) | `学术文献` |
| 4 | Regulatory filing (SEC, 10-K, prospectus) | `监管文件` |
| 5 | Published third-party benchmark (MLPerf, TPC, SPEC) | `外部Benchmark` |
| 6 | Top-tier media review (AnandTech, ServeTheHome, SemiAnalysis) | `权威评测` |
| 7 | Industry report (Gartner, IDC, Counterpoint) | `行业报告` |
| 8 | Personal blog / social media | `个人博客` — lowest tier |

**Time window**: Vendor activity defaults to last 12 months. Older data must be explicitly labelled "历史背景".

### 3. Primary-Source Visuals — 原始视觉证据，必须一手来源

**Every report must include original visual evidence** — product photos, architecture diagrams, die shots, scene photos, technology principle diagrams.

```
Image Source Priority (STRICTLY ORDERED):

  Priority 1 — PRIMARY SOURCE (REQUIRED):
    Manufacturer product page / press kit, patent figures,
    academic paper figures, official whitepapers, regulatory filings.
    Download to assets/<slug>/ and record in image_manifest.json.

  Priority 2 — AUTHORITATIVE REVIEW:
    AnandTech, ServeTheHome, TechInsights, ChipRebel teardown photos.
    Must be traceable to the review article.

  PROHIBITED:
    - Watermark-stripped re-uploads
    - Second-hand re-renders that cannot be traced to a primary source
    - Stock photos or generic illustrations
    - Self-drawn diagrams UNLESS original is unreadable (credit original)
```

**Image management**:
- Download to `assets/<slug>/` with prefixed filenames (e.g., `tech1-arch.png`, `product-hero.jpg`)
- Every image recorded in `assets/<slug>/image_manifest.json` with `source_url` + `fetched_at`
- Use [scripts/visual_collector.py](scripts/visual_collector.py) for bulk download
- Every image in the report must use the caption format: `图 X：[说明] — 来源：[原始链接](URL)`

**Universal architecture diagram rule (applies to ALL report types)**:
- Every **technology point** discussed in the report must have ≥1 technical architecture diagram (principle diagram, system architecture, data flow, module decomposition)
- Every **specific product/project** under each technology point must have ≥1 product-level architecture diagram (system architecture, teardown, pipeline diagram)
- Architecture diagrams must come from primary sources (paper figures, official whitepapers, patent figures, official tech blogs)

**Coverage requirements** (additional to the universal rule above):

| Report Type | Minimum Visual Coverage |
|------------|------------------------|
| Type A | Each TOP 5 technology: ≥1 tech architecture diagram + each representative product under that tech: ≥1 product architecture diagram |
| Type B | Each technology route: ≥1 tech principle diagram + each representative product under that route: ≥1 product architecture diagram |
| Type C | ≥1 product photo + each key architecture: ≥1 teardown/architecture diagram |
| Type D | ≥1 product portfolio map + each core product: ≥1 product architecture diagram |
| General | ≥1 visual per major finding / technology discussed |

### 4. Hypothesis-Driven Structure

Every analysis is organized around a **central technical hypothesis**, not a topic survey.

```
Bad:  "Let's analyze edge AI technologies"         → topic survey, rejected
Good: "Edge AI inference latency has crossed the    → hypothesis, testable
       real-time threshold for industrial vision,
       making cloud-first architectures obsolete
       for factory floor applications"
```

- State the hypothesis upfront
- Each section validates, qualifies, or bounds the hypothesis through external evidence
- Sections that merely describe technology without advancing the hypothesis must be cut
- Final output confirms, refines, or rejects the hypothesis with evidence summary

### 5. TRL Anchoring

Every technology discussed must carry explicit **TRL (Technology Readiness Level, 1-9)** with one-line justification based on publicly available evidence:

| TRL | Definition | Evidence Threshold |
|-----|-----------|-------------------|
| 1-3 | Basic research → Proof of concept | Papers only, no production deployment |
| 4-5 | Lab validation → Relevant environment tested | Published benchmarks, prototype demos |
| 6-7 | System demo → Operational environment | Production pilots, vendor GA announcements |
| 8-9 | System complete → Mission-proven | Widespread production deployment, industry standards |

### 6. "So What" Discipline

Every insight section has exactly ONE core signal — the finding the audience must retain.

**Test**: If you cannot state it in one sentence, the section contains multiple messages and must be split.

### 7. Banned Filler Phrases

The following phrases are **automatically rejected** by the linter. They indicate the implication is not actionable:

- "需要持续关注"
- "值得观察"
- "未来可期"
- "拭目以待"
- "前景广阔"
- "大有可为"

Every implication must answer "So what?" with a concrete, executable direction — not a platitude.

### 8. Key Tech Decomposition — Forced Drill-Down

Forbidden to stop at "uses Transformer / 3nm process". Must drill to:
- Specific architectural choices and trade-off rationale
- Key hyperparameters, process node deltas, algorithm variants
- Quantitative comparison table (performance, power, cost, yield, ecosystem metrics) — all with sources
- Moat analysis: patent stack, talent density, fab access, ecosystem lock-in, data network effects

### 9. Peer Technology Drill-Down — 同类技术比较必须穿透到架构与策略层

When the analysis compares ≥3 peer technologies, products, or approaches addressing the same problem domain, the analysis MUST NOT stop at a comparison table or ranking. A comparison table shows **what** differs; the insight is **why** each technology made its design choices and **what trade-off** each embodies.

This applies to ALL forms of peer comparison — benchmark leaderboards, framework evaluations, product teardowns, architecture surveys, vendor landscape scans, or any side-by-side analysis.

For each compared technology, the analysis must cover three layers:

```
Layer 1 — Architecture (这个技术/系统是怎么设计的?)
  - Core components, modules, and their responsibilities
  - Data/control flow through the system (e.g., ingestion → processing → output)
  - Key design decisions that differentiate it from peers
  - Infrastructure dependencies and operational model

Layer 2 — Strategy (它在 trade-off 空间中做了什么选择?)
  - Which dimension does it optimize for? (accuracy / latency / cost / simplicity / flexibility / ...)
  - What does it explicitly sacrifice to achieve that optimization?
  - What is the implicit assumption behind this trade-off?
  - What application scenarios does this strategy best serve?

Layer 3 — Effect (实际表现如何, 按维度拆分?)
  - Headline metric (overall score, throughput, adoption, etc.)
  - Performance broken down by sub-dimension / task type / scenario
  - Cost, latency, resource, and operational complexity metrics
  - Ablation or factor analysis if available (what contributes most?)
```

After all technologies are individually analyzed, synthesize:
- **Trade-off Map**: position each technology in the competitive space (e.g., 2D plot with meaningful axes)
- **Strategy Selection Guide**: map application requirements to the best-fit technology choice

**Anti-pattern**: A finding that lists "System A: 91%, System B: 74%, System C: 67%" — or any comparison table without per-technology architecture and strategy analysis — is a **surface comparison, not an insight**. Reject it and drill deeper.

**When to apply**: Any finding that compares ≥3 technologies, systems, products, or approaches addressing the same problem. This includes but is not limited to: benchmark rankings, product teardowns, framework evaluations, architecture surveys, vendor comparisons, and open-source project landscapes.

### 10. 总—分—总 Structure Discipline

All four report types follow a "总—分—总" (synthesis → decomposition → synthesis) structure:

- **Type A**: Domain definition & demand decomposition (总) → TOP 5 tech deep dive (分) → Trend synthesis & research implication (总)
- **Type B**: Industry history & route identification (总) → Per-route deep analysis (分) → Cross-route comparison & recommendation (总)
- **Type C**: Product overview & selling points (总) → Key architecture decomposition (分) → Summary & product implication (总)
- **Type D**: Company profile (总) → Product portfolio & strategy analysis (分) → Competitiveness summary & BU implication (总)

Missing any layer is a hard fail. The linter enforces this per type.

## Core Orchestration Loop

```
Step 1 — CLASSIFY & FRAME
   Classify: Type A / B / C / D, or General?
   Type A: Define the segmented technology domain boundary.
           Identify the application evolution and bottom-level demands.
   Type B: Define the industry scope and development history.
           Identify mainstream and potential technology routes.
   Type C: Define the target product.
           Identify core selling points and key differentiating features.
   Type D: Define the target company.
           Scope the analysis (full company or specific business units).
   General: Define hypothesis and analysis scope.

Step 2 — SOURCE COLLECTION (WebSearch + WebFetch)
   Follow Universal Sourcing rules. Capture every URL into a running source ledger.
   Cross-check: key specs / share / price need ≥2 independent sources.
   Time window: vendor moves ≤12 months unless explicitly historical.

Step 3 — KEY TECH DECOMPOSITION
   Force drill-down past marketing language to architectural choices,
   quantitative deltas, and moat analysis. Build comparison tables with sources.
   Type A: Decompose TOP 5 technologies in depth.
   Type B: Analyze each technology route with product examples.
   Type C: Teardown 1-3 key architectures behind the product's selling points.
   Type D: Map company's technology capabilities and patent portfolio.

Step 4 — VISUAL ASSET COLLECTION (MANDATORY — runs BEFORE writing)
   For every technology / product / architecture, fetch ORIGINAL images from primary sources.
   Run: python scripts/visual_collector.py --plan <plan.json> --assets-root assets/
   Coverage must meet type-specific minimums.

Step 5 — ANALYSIS & SYNTHESIS
   Build IIR chains. Assign TRL to each technology.
   Type A: Build technology comparison matrix, identify trends.
   Type B: Build cross-route comparison, identify research directions.
   Type C: Assess innovation points and competitive position.
   Type D: Evaluate technology competitiveness and strategic direction.
   CRITICAL: If analysis compares ≥3 peer technologies/systems,
   apply Peer Technology Drill-Down (Principle §9) —
   for each: architecture → strategy choice → per-dimension results.

Step 6 — DRAFT REPORT
   Use the matching output template. Inline-cite every factual sentence.
   Embed every collected image next to the paragraph it supports.
   End each insight block with an actionable "So what?".

Step 7 — DRAFT REVIEW (REQUIRED)
   Present draft to user in Markdown for approval.
   Get explicit confirmation before QA and final delivery.

Step 8 — QA GATE (REQUIRED — never deliver without it)
   python scripts/linter.py <report.md> --assets assets/<slug>/ --type A|B|C|D
   The linter rejects the report if any of:
   - Any factual sentence missing inline URL/DOI/patent number
   - Any required image slot empty or missing source caption
   - Structure incomplete (type-specific mandatory sections missing)
   - Banned filler phrase found
   - Specific number / product code / quote without a source (hallucination guard)
   Fix every issue before delivering.

Step 9 — DELIVER
   Hand over the report + assets/ folder.
   Include source ledger as final "Sources" section, deduplicated and numbered.

Step 10 — HANDOFF (if needed)
   → To tech-planning: pass analysis as input to Five Looks / SPAN matrix
   → To pro-pptx: pass content for hw-insight template rendering
```

## Type A Specifics — 细分技术领域洞察

When running a Type A report, follow the [Type A — Domain workflow](workflows/type-a-domain.md).

**Type A mandatory 总—分—总 structure** (enforced by linter):

1. **领域定义与应用发展（总）**:
   - 领域边界：definition, upstream/downstream, core application scenarios
   - 应用发展脉络：evolution history with key milestones (with sources)
   - 底层需求拆解：application demand → system demand → technology demand chain

2. **TOP 5 技术深入分析（分）**:
   - TOP 5 入选依据：selection criteria with sources (tech influence, citations, adoption, maturity)
   - Per-Technology Deep Dive (×5): principle, TRL, key metrics, moat, representative results
   - 技术横向对比表：quantitative comparison matrix across TOP 5

3. **技术趋势与研究启示（总）**:
   - 技术趋势归纳：common evolution direction, divergence points, convergence/divergence trends
   - 研究启示：concrete research recommendations — which directions to invest, which to avoid, which cross-domain areas to watch

**TOP 5 selection rules**:
- Ranking metric must reflect technology impact (citations, industry adoption, maturity) — not product sales
- Must span ≥2 distinct technical approaches for balance
- If domain too narrow for 5: degrade to TOP N (N≥3) with explicit justification

**Visual coverage**: each technology needs ≥1 principle/architecture diagram + each representative product/project under that technology needs ≥1 product architecture diagram, all from primary sources.

Detailed workflow: [workflows/type-a-domain.md](workflows/type-a-domain.md)
Output template: [templates/type-a-domain.md](templates/type-a-domain.md)

## Type B Specifics — 行业技术趋势洞察

When running a Type B report, follow the [Type B — Industry workflow](workflows/type-b-industry.md).

**Type B mandatory structure** (enforced by linter):

1. **行业发展史与技术路线引出**:
   - 行业发展脉络：key stages, milestones, market size evolution (with sources)
   - 技术路线图谱：mainstream routes (production-proven) vs potential routes (experimental), classification rationale

2. **逐条技术路线深入分析（per route）**:
   - 成功产品引子（if applicable）：2-3 representative products with market performance (with sources)
   - 技术优势与局限性：systematic analysis with quantitative metrics
   - 前沿研究方向：latest research hotspots driven by evolving application demands (with papers/patents)

3. **全局总结与研究建议**:
   - 技术路线横向对比：comparison matrix across all routes on key dimensions
   - 行业技术研究建议：mainstream deepening, potential route timing, cross-route fusion opportunities

**Visual coverage**: each route needs ≥1 tech principle diagram + each representative product under that route needs ≥1 product architecture diagram.

Detailed workflow: [workflows/type-b-industry.md](workflows/type-b-industry.md)
Output template: [templates/type-b-industry.md](templates/type-b-industry.md)

## Type C Specifics — 产品技术洞察

When running a Type C report, follow the [Type C — Product workflow](workflows/type-c-product.md).

**Type C mandatory structure** (enforced by linter):

1. **产品概览与卖点分析**:
   - 产品定位：name, vendor, customer, market position, launch date, market performance (with sources)
   - 核心卖点与特性：distinguish "marketing claims" from "verifiable engineering facts"

2. **关键技术架构拆解**:
   - 技术架构识别：identify 1-3 key architectures from selling points
   - Per-Architecture Decomposition: system diagram, core principle, key parameters, innovation points, moat, peer comparison

3. **总结与产品启示**:
   - 技术总结：core competitiveness and technical weaknesses
   - 对标产品启示：what to learn, what to surpass, what to avoid

**Visual coverage**: ≥1 product photo + each key architecture needs ≥1 teardown/architecture diagram.

Detailed workflow: [workflows/type-c-product.md](workflows/type-c-product.md)
Output template: [templates/type-c-product.md](templates/type-c-product.md)

## Type D Specifics — 公司技术洞察

When running a Type D report, follow the [Type D — Company workflow](workflows/type-d-company.md).

**Type D mandatory structure** (enforced by linter):

1. **公司概览**:
   - 公司画像：name, founding, HQ, core business, revenue, headcount, valuation (with sources)
   - 发展历程与里程碑：key events, major M&A, business pivots

2. **产品布局分析**:
   - 产品矩阵：product lines, market position, target customers, revenue contribution (with sources)
   - 核心产品深挖 (2-3 products)：market performance, competitive advantage, tech highlights

3. **公司战略与技术路线**:
   - 战略方向：extracted from public sources (earnings, investor days, CEO statements, patent filings, hiring trends)
   - 技术路线图：build vs buy vs partner, patent portfolio, R&D investment trends
   - 技术能力评估：talent, patents, engineering capability, ecosystem position

4. **总结与事业单元启示**:
   - 技术竞争力总结：core strengths, risks, strategic blind spots
   - 对事业单元的启示：competition strategy, cooperation opportunities, gap-closing paths, differentiation entry points

**Visual coverage**: ≥1 product portfolio map + each core product needs ≥1 product architecture diagram.

Detailed workflow: [workflows/type-d-company.md](workflows/type-d-company.md)
Output template: [templates/type-d-company.md](templates/type-d-company.md)

## Integration with Other Skills

### → tech-planning (downstream — consumes insights for decisions)

When analysis is complete and user needs strategic decisions:
- Insight report's IIR chains become the evidence base for Five Looks
- Type A technology trend synthesis feeds into Look 1 (Trends) and Look 4 (Competition)
- Type B cross-route comparison feeds into Look 1 (Trends) and Look 2 (Market)
- Type C product insights feed into Look 4 (Competition)
- Type D company insights feed into Look 3 (Customers) and Look 4 (Competition)
- Landscape maps inform SPAN matrix scoring
- Reference: [tech-planning SKILL.md](../tech-planning/SKILL.md)

### → pro-pptx (downstream — renders insights as presentation)

When user wants PPTX presentation:
- Each IIR chain maps to one content slide (Insight = title, Evidence = body, Implication = callout)
- Technology comparison matrices → `data` layout
- Landscape maps → `tech-radar` layout
- Architecture comparisons → `arch-compare` layout
- Key metrics → `tech-metric` layout
- Scene/product photos → embedded via `addImage({ path: ... })`
- Reference: [hw-insight template](../pro-pptx/templates/hw-insight/template.md)

**Slide title rule**: State the insight, not the topic.
- Bad: "大模型推理加速技术综述"
- Good: "Transformer推理瓶颈已从算力转移至显存带宽，业界HBM方案正在成为主流选择"

## Dependencies

```bash
pip install requests
```

- `requests` — image download in [scripts/visual_collector.py](scripts/visual_collector.py)
- [scripts/linter.py](scripts/linter.py) uses only the Python standard library
- **WebSearch**: Required for evidence collection
- **WebFetch**: Required for retrieving specific data sources and downloading images
- **tech-planning skill**: Optional, for strategic decision-making from insights
- **pro-pptx skill**: Optional, for PPTX deliverable rendering with hw-insight template
