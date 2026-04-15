# Workflow: Deep Dive — Single Technology Analysis

Deep analysis of one specific technology, architecture, or technical approach. Produces a hypothesis-driven insight report with full evidence chain.

## Prerequisites

User must provide:
- **Technology topic** — what to analyze (e.g., "edge AI inference frameworks", "MoE architecture for LLMs")
- **Audience** (optional) — who will read this (determines depth and framing)
- **Specific questions** (optional) — particular angles to investigate

## Step 1: Frame the Hypothesis

Do NOT start with "let me research X." Start with a **testable hypothesis**:

```
Technology: [specific technology or approach]
Hypothesis: [A falsifiable claim about this technology's state, trajectory, or impact]
Scope: [what's in / what's out]
Time horizon: [relevant timeframe]
```

**How to form the hypothesis**:
- If user provides a clear question → convert to hypothesis
- If user provides only a topic → do a 5-minute quick search, then form hypothesis based on initial findings
- The hypothesis should be SPECIFIC and FALSIFIABLE

**Examples**:

| User says | Bad hypothesis | Good hypothesis |
|-----------|---------------|-----------------|
| "Analyze WebAssembly" | "WebAssembly is important" | "Wasm+WASI has reached production-readiness (TRL 7+) for server-side workloads, but adoption is blocked by ecosystem immaturity — <5% of cloud-native projects use it" |
| "Look into MoE models" | "MoE is the future of LLMs" | "MoE architectures have solved the training-cost problem but created a new inference-cost problem: expert routing overhead makes MoE 2-3x more expensive to serve than dense models at equivalent quality" |

## Step 2: Evidence Collection

### 2a: Structured Web Research

Execute these searches in parallel where possible:

**Round 1 — Breadth scan** (parallel):

| Search Category | Query Patterns | Target |
|----------------|---------------|--------|
| State of the art | `"[technology] survey [year]"`, `"[technology] state of the art"` | Recent survey papers, overview articles |
| Benchmark data | `"[technology] benchmark comparison [year]"`, `"[technology] vs [alternative]"` | Performance comparisons with numbers |
| Market context | `"[technology] market size adoption [year]"` | Market sizing, adoption rates |
| Key players | `"[technology] companies startups [year]"` | Who's investing, building, deploying |

**Round 2 — Depth probes** (based on Round 1 findings):

| Search Category | Query Patterns | Target |
|----------------|---------------|--------|
| Specific benchmarks | `"[specific benchmark name] results"`, `"[model A] vs [model B] [metric]"` | Exact numbers for comparison tables |
| Architecture details | `"[technology] architecture paper"`, `"[technology] design decisions"` | Technical depth for analysis |
| Limitations & failures | `"[technology] limitations"`, `"[technology] challenges problems"` | Counter-evidence to test hypothesis |
| Future direction | `"[technology] roadmap [year]"`, `"[technology] next generation"` | Where it's heading |

### 2b: Evidence Inventory

As data comes in, log every piece of evidence:

```markdown
## Evidence Log

| # | Claim | Data Point | Source Type | Source | Date | Confidence |
|---|-------|-----------|-------------|--------|------|------------|
| 1 | [what this proves] | [specific number/fact] | 外部Benchmark | [URL/name] | YYYY-MM | H/M/L |
| 2 | | | 学术文献 | | | |
| 3 | | | 行业报告 | | | |
```

**Universal sourcing rule**: Every evidence point MUST carry an inline URL/DOI/patent number. No source-free entries in the log. See [SKILL.md](../SKILL.md) §Universal Sourcing.

**Quality gate**: Before proceeding, verify:
- ≥ 3 evidence points supporting hypothesis
- ≥ 1 evidence point challenging or bounding hypothesis
- ≥ 2 different source types represented
- All key claims have quantified data (not just qualitative assertions)
- Key facts (parameters, share, price) have ≥ 2 independent sources for cross-validation

If insufficient: run additional targeted searches.

## Step 3: Analysis & Synthesis

### 3a: Build IIR Chains

For each major finding, construct a complete chain:

```markdown
### Finding [N]: [One-sentence insight]

**Insight**: [Technical signal — what is happening, stated as a claim]

**Evidence**:
- [Data point 1] — [source type]: [source, date]
- [Data point 2] — [source type]: [source, date]
- [Data point 3] — [source type]: [source, date]

**Implication**: [Industry-level meaning — what this enables, threatens, or changes]

**TRL**: [1-9] — based on [specific evidence for this TRL assignment]

**Confidence**: High / Medium / Low — based on [evidence quality assessment]
```

Target: 5-8 IIR chains per deep dive.

### 3b: Peer Technology Drill-Down

If the analysis compares ≥3 peer technologies/systems/approaches, apply the three-layer drill-down for EACH: Architecture (how it's designed) → Strategy (what trade-off it chose and why) → Effect (per-dimension results + ablation). A comparison table without per-technology architecture and strategy analysis is a surface comparison, not an insight. See [SKILL.md §9](../SKILL.md) for the full framework.

### 3c: Build Visual Artifacts

For each major finding, determine the appropriate visual:

| Finding Type | Visual Artifact |
|-------------|----------------|
| Performance comparison | Benchmark comparison table with numbers |
| Architecture analysis | Component diagram or comparison |
| Maturity assessment | TRL chart or adoption curve |
| Ecosystem mapping | Player landscape or value chain |
| Trend analysis | Timeline with milestones and data |

### 3c: Hypothesis Verdict

Based on all evidence, render judgment:

```markdown
## Hypothesis Verdict

**Original hypothesis**: [restate]

**Verdict**: CONFIRMED / REFINED / PARTIALLY REJECTED / REJECTED

**Refinement** (if applicable): [how the hypothesis should be restated based on evidence]

**Key evidence for**: [top 3 supporting data points]
**Key evidence against**: [top 3 challenging data points]
**Remaining unknowns**: [what we still don't know, with suggested investigation paths]
```

## Step 4: Draft Review (REQUIRED)

Present to user before final assembly:

```markdown
## Deep Dive Draft: [Technology]

### Hypothesis
[Original → Verdict → Refined version]

### Key Findings (IIR Summary)
| # | Insight | Evidence Quality | Implication | TRL |
|---|---------|-----------------|-------------|-----|
| 1 | [one sentence] | [H/M/L + source types] | [one sentence] | [1-9] |
| 2 | ... | ... | ... | ... |

### Evidence Quality Assessment
- Total evidence points: N
- Source type distribution: [N benchmarks, N papers, N reports, N signals]
- Gaps: [areas where evidence is thin]

### Proposed Visual Artifacts
- [List of tables/charts/diagrams to include]

Confirm or request changes before I assemble the final report.
```

## Step 4.5: Visual Asset Collection (MANDATORY — runs BEFORE final assembly)

For every key technology and product mentioned in the draft:

1. Derive image search queries from architecture names, product names, paper titles
2. Search for PRIMARY-SOURCE images: vendor product pages, paper figures, patent diagrams, official whitepapers
3. Download to `assets/<slug>/` using [visual_collector.py](../scripts/visual_collector.py)
4. Record every image in `image_manifest.json` with `source_url` + `fetched_at`
5. Every image in the report MUST use caption format: `图 X：[说明] — 来源：[原始链接](URL)`

**Prohibited**: watermark-stripped re-uploads, unattributable re-renders, stock photos.
**Coverage target**: ≥1 visual per major finding / technology discussed.

## Step 5: Assemble Deliverable

Use [Insight Report template](../templates/insight-report.md) to assemble the final output.
Every factual sentence must carry an inline source link. The linter will reject source-free sentences.

### Handoff Options

After delivery, ask user:
- **Need strategic decisions?** → Hand off to [tech-planning](../../tech-planning/SKILL.md) (insights feed into Five Looks)
- **Need presentation?** → Hand off to [pro-pptx](../../pro-pptx/SKILL.md) with hw-insight template
  - Each IIR chain → one content slide
  - Hypothesis + verdict → insight-summary slide
  - Benchmark tables → data layout slides

## Common Pitfalls

1. **Topic survey instead of hypothesis** — "Here's everything about X" is not an insight. Always lead with a claim.
2. **Evidence-free claims** — "X is clearly superior" without benchmark data. Every superlative needs a number.
3. **Missing counter-evidence** — Only collecting supporting data. Actively search for limitations and failures.
4. **Shallow TRL assignment** — Saying TRL 7 without evidence of production deployment. Be rigorous.
5. **Internal recommendations** — "We should adopt X" is tech-planning territory. This skill produces external intelligence only.
6. **Stale data** — Using 2-year-old benchmarks for a fast-moving field. Always check data recency.
7. **Source-free sentences** — Every factual sentence needs an inline URL/DOI/patent number. The linter enforces this.
8. **Missing visuals** — No diagrams from primary sources. Stock photos and self-drawn diagrams are not substitutes.

## Relationship to Type-Specific Workflows

This workflow is the primary analysis engine for:
- [Type B — Industry](type-b-industry.md): Deep Dive provides per-route technology analysis
- Also usable standalone for general single-technology insight reports
