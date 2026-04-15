# Workflow: Benchmark — Evidence Collection & Analysis

Systematic collection, validation, and analysis of benchmark data and technical evidence for a specific technology question. This workflow produces the raw evidence base that other workflows consume.

## Prerequisites

User must provide:
- **Technology question** — what to benchmark (e.g., "LLM inference latency on consumer GPUs", "vector database throughput at 10M scale")
- **Metrics of interest** (optional) — specific KPIs to collect
- **Technologies to compare** (optional) — specific implementations

## Step 1: Define Benchmark Scope

```
Question:         [specific, measurable question]
Technologies:     [list of implementations/products to compare]
Key metrics:      [what to measure — latency, throughput, accuracy, cost, etc.]
Environment:      [hardware, software, configuration constraints if relevant]
Recency window:   [how recent must data be — default: last 12 months]
```

**Transform vague questions into measurable ones**:

| User says | Benchmark question |
|-----------|-------------------|
| "Is vLLM fast?" | "What is vLLM's throughput (tokens/s) vs TGI and TensorRT-LLM for Llama-3-70B on A100, H100?" |
| "Compare vector databases" | "What is QPS at 99th percentile latency for Milvus, Qdrant, Weaviate at 10M vectors, 768 dimensions?" |

## Step 2: Evidence Search

### 2a: Primary Benchmark Sources

Search in this priority order:

| Priority | Source Type | Search Strategy | Trust Level |
|----------|-----------|----------------|-------------|
| 1 | Official benchmark suites | `"[benchmark name] results [year]"` (e.g., MLPerf, TPC, SPEC, ANN-Benchmarks) | Highest — standardized methodology |
| 2 | Academic evaluations | `"[technology] evaluation [year] arxiv"`, `"[technology] comparison paper"` | High — peer-reviewed methodology |
| 3 | Independent tech blogs | `"[technology] benchmark blog [year]"` (filter for those showing methodology) | Medium — verify methodology |
| 4 | Vendor benchmarks | `"[vendor] [technology] performance [year]"` | Low — check for bias, seek reproduction |

### 2b: Benchmark Data Extraction

For each benchmark found, extract into standardized format:

```markdown
## Benchmark Record #[N]

**Source**: [full citation — title, author/org, date, URL]
**Source Type**: 外部Benchmark / 学术文献 / 行业报告 / 厂商数据
**Date**: YYYY-MM-DD
**Methodology**: [brief description of how benchmark was run]
**Environment**: [hardware, software versions, configuration]

### Results
| Technology | Metric 1 | Metric 2 | Metric 3 |
|-----------|---------|---------|---------|
| [tech A] | [value ± variance] | [value] | [value] |
| [tech B] | [value ± variance] | [value] | [value] |

### Caveats
- [Any methodology concerns]
- [Environmental differences from our target]
- [Known biases or limitations]

**Confidence**: High / Medium / Low
**Reason**: [why this confidence level]
```

### 2c: Cross-Validation

For every key claim, seek corroboration:

```markdown
## Cross-Validation Matrix

| Claim | Source 1 | Source 2 | Source 3 | Consistent? |
|-------|---------|---------|---------|-------------|
| "[tech A] achieves X throughput" | [value, source] | [value, source] | [value, source] | Yes/No/Partial |
```

**Rules**:
- A claim supported by ≥ 2 independent sources = HIGH confidence
- A claim from only 1 source (even authoritative) = MEDIUM confidence
- A claim only from vendor source = LOW confidence until independently verified
- Conflicting data = flag and investigate methodology differences

## Step 3: Analysis

### 3a: Normalized Comparison Table

Normalize all data to comparable units and conditions:

```markdown
## Normalized Benchmark Comparison — [Question]

**Normalization conditions**: [hardware, software, dataset, methodology]

| Metric | [Tech A] | [Tech B] | [Tech C] | Winner | Source |
|--------|---------|---------|---------|--------|--------|
| [metric 1] | [value] | [value] | [value] | [which] | [best source] |
| [metric 2] | [value] | [value] | [value] | [which] | [best source] |
| [metric 3] | [value] | [value] | [value] | [which] | [best source] |

**Notes**:
- [Technology A data from source X (YYYY-MM), tested on [config]]
- [Technology B data from source Y (YYYY-MM), tested on [config] — note: different GPU]
- [Normalization adjustments: ...]
```

If data cannot be normalized (different hardware, different datasets), note this explicitly and do NOT present a direct comparison as if conditions were equal.

### 3b: Trend Analysis (if time-series data available)

```markdown
## Performance Trend — [Metric]

| Technology | [Date 1] | [Date 2] | [Date 3] | Trend | Improvement Rate |
|-----------|---------|---------|---------|-------|-----------------|
| [tech A] | [value] | [value] | [value] | ↑/→/↓ | X% per [period] |
```

### 3c: Cost-Performance Analysis (if cost data available)

```markdown
## Cost-Performance Matrix

| Technology | Performance ([metric]) | Cost ([unit]) | Perf/$ Ratio | Efficiency Rank |
|-----------|----------------------|---------------|-------------|-----------------|
| [tech A] | [value] | [$X] | [ratio] | [rank] |
```

### 3d: Peer Technology Drill-Down (REQUIRED when ≥3 technologies compared)

When the analysis compares ≥3 peer technologies/systems, a comparison table alone is insufficient. For each technology, produce a three-layer analysis:

```markdown
### [Technology Name] — [One-sentence design philosophy]

**Architecture**:
- Core components and data/control flow
- Key design decisions that differentiate from peers
- Infrastructure dependencies and operational model

**Strategy (Trade-off Choice)**:
- Which dimension is optimized? (accuracy / latency / cost / simplicity / flexibility / ...)
- What is explicitly sacrificed?
- What implicit assumption underpins this trade-off?
- Best-fit application scenarios

**Effect (Per-Dimension Results)**:
- Headline metric: [number]
- Breakdown by sub-dimension / task type / scenario: [table]
- Cost / latency / resource / operational metrics: [numbers]
- Ablation / factor analysis (if available): what contributes most?
```

After all technologies are analyzed individually, synthesize a **Trade-off Map** that positions each technology in the competitive space and a **Strategy Selection Guide** that maps application requirements to the best-fit technology.

See [SKILL.md §9 Peer Technology Drill-Down](../SKILL.md) for the full principle.

### 3e: Extract IIR Chains

From benchmark analysis, extract insights:

```markdown
### Benchmark Insight [N]: [one-sentence finding]

**Insight**: [what the benchmarks reveal — stated as a claim]
**Evidence**:
- [Benchmark result 1] — 外部Benchmark: [source]
- [Benchmark result 2] — 学术文献: [source]
**Implication**: [what this means — who benefits, what becomes possible/impossible]
**Confidence**: H/M/L — [N independent sources, methodology quality]
```

## Step 4: Evidence Quality Report

```markdown
## Evidence Quality Assessment

### Coverage
| Technology | Benchmark Points | Source Types | Recency | Confidence |
|-----------|-----------------|-------------|---------|------------|
| [tech A] | N | [types] | [most recent date] | H/M/L |

### Gaps
| Gap | Impact | Mitigation |
|-----|--------|-----------|
| [missing data point] | [how it affects conclusions] | [what we can say despite the gap] |

### Methodology Concerns
| Concern | Affected Data | Risk Level |
|---------|-------------|-----------|
| [e.g., vendor-only source] | [which benchmarks] | H/M/L |
| [e.g., outdated version tested] | [which comparisons] | H/M/L |
```

## Step 5: Deliverable

Use [Evidence Dossier template](../templates/evidence-dossier.md) for raw evidence output.

Or feed results into:
- [Deep Dive workflow](deep-dive.md) — benchmarks become the evidence layer
- [Landscape workflow](landscape.md) — benchmarks inform positioning scores
- [Briefing workflow](briefing.md) — benchmark highlights become briefing content

## Universal Sourcing Reminder

Every benchmark record and every claim derived from benchmark data MUST carry an inline source (URL/DOI/patent number). Vendor-only claims must be explicitly labelled "厂商宣称" and cross-validated where possible. See [SKILL.md](../SKILL.md) §Universal Sourcing.

## Common Pitfalls

1. **Cherry-picking** — Only citing benchmarks that support your preferred conclusion. Include ALL relevant data.
2. **Apples-to-oranges** — Comparing benchmarks run on different hardware/configs without noting the difference.
3. **Vendor benchmarks as ground truth** — Vendor results are marketing first, science second. Always seek independent reproduction.
4. **Ignoring methodology** — A benchmark without described methodology is an anecdote, not evidence.
5. **Precision theater** — Reporting "7.23x faster" when the underlying measurements have ±15% variance.
6. **Recency bias** — Using only the latest benchmark while ignoring trend data that tells a different story.
7. **Source-free numbers** — Every specific number needs an inline source. The linter enforces this.

## Relationship to Type-Specific Workflows

This workflow provides the evidence engine for:
- [Type A — Domain](type-a-domain.md): Benchmark provides technology comparison data
- [Type B — Industry](type-b-industry.md): Benchmark validates key technology claims in per-route analysis
- Also usable standalone for pure evidence collection tasks
