# Workflow: Landscape — Multi-Technology Domain Scan

Systematic comparison of multiple technologies within a domain. Produces a landscape map with relative positioning, maturity assessment, and value migration analysis.

## Prerequisites

User must provide:
- **Technology domain** — the space to scan (e.g., "LLM inference optimization", "real-time data pipelines")
- **Key technologies to include** (optional) — specific techs to compare; if not provided, discovery is part of the workflow
- **Evaluation dimensions** (optional) — what axes matter most

## Step 1: Domain Framing

### 1a: Define Landscape Scope

```
Domain:           [technology area]
Boundary:         [what's in scope / what's out]
Framing question: [the question this landscape should answer]
Time horizon:     [snapshot as of when + forward-looking how far]
```

**Framing question examples**:
- "Which inference optimization approaches are production-ready for LLMs > 70B parameters?"
- "Where is the real-time stream processing ecosystem heading — is Kafka still the center of gravity?"

### 1b: Technology Discovery

If user didn't specify all technologies, discover them:

1. Search: `"[domain] comparison [year]"`, `"[domain] alternatives"`, `"[domain] landscape survey"`
2. Extract all technologies/approaches mentioned across ≥ 2 sources
3. Group into categories (e.g., by approach type, architecture family, vendor ecosystem)
4. Present candidate list to user for confirmation (aim for 5-12 technologies)

## Step 2: Evidence Collection

### 2a: Per-Technology Data Gathering

For EACH technology in scope, collect (parallel where possible):

| Data Category | Search Queries | Required Data |
|--------------|---------------|---------------|
| Maturity & adoption | `"[tech] adoption rate"`, `"[tech] production deployment"` | TRL (1-9), deployment count/scale |
| Performance | `"[tech] benchmark [year]"`, `"[tech] performance comparison"` | Key metrics with numbers |
| Ecosystem | `"[tech] github stars"`, `"[tech] community size"`, `"[tech] integrations"` | OSS activity, community, ecosystem breadth |
| Momentum | `"[tech] funding"`, `"[tech] recent release"` | Funding, release velocity, hiring signals |
| Limitations | `"[tech] limitations"`, `"[tech] challenges"` | Known weaknesses, failure modes |

### 2b: Cross-Technology Comparison Data

Search for head-to-head comparisons:
- `"[tech A] vs [tech B] benchmark"` for all major pairs
- `"[domain] comparison table [year]"` for consolidated comparisons
- `"[domain] migration from [tech A] to [tech B]"` for value migration signals

### Evidence Quality Gate

Before proceeding, verify:
- Each technology has ≥ 3 data points across ≥ 2 categories
- At least 2 head-to-head benchmark comparisons exist
- TRL can be assigned with evidence for each technology
- No technology has ONLY vendor-sourced data (seek independent evaluation)

## Step 3: Analysis & Positioning

### 3a: Benchmark Comparison Matrix

Build the core comparison table:

```markdown
## Technology Comparison Matrix — [Domain]

| Dimension | [Tech A] | [Tech B] | [Tech C] | [Tech D] | Source |
|-----------|---------|---------|---------|---------|--------|
| [metric 1] | [value] | [value] | [value] | [value] | [citation] |
| [metric 2] | [value] | [value] | [value] | [value] | [citation] |
| [metric 3] | [value] | [value] | [value] | [value] | [citation] |
| TRL | [1-9] | [1-9] | [1-9] | [1-9] | [evidence] |
| Ecosystem size | [metric] | [metric] | [metric] | [metric] | [source] |
| Momentum | ↑/→/↓ | ↑/→/↓ | ↑/→/↓ | ↑/→/↓ | [signals] |
```

**Rule**: Every cell must have a value with source. Empty cell = flag for additional research.

### 3b: Landscape Map (2×2 Positioning)

Choose two axes that best answer the framing question. Common axis pairs:

| Axis Pair | When to Use |
|-----------|------------|
| Industry Maturity × Technical Differentiation | General landscape scan |
| Performance × Cost/Complexity | Technology selection decisions |
| Adoption × Innovation Rate | Ecosystem health assessment |
| Production Readiness × Scalability | Deployment planning |

Plot each technology with:
- Position based on QUANTIFIED data (not gut feeling)
- TRL label
- Trend arrow (↑ gaining / → stable / ↓ declining)
- Brief rationale for placement

```markdown
## Technology Landscape Map — [Domain]

                    [Y-axis label]
                    High                          Low
                ┌──────────────────┬──────────────────┐
  [X-axis]      │                  │                  │
  High          │  [Tech A] TRL:8 ↑│  [Tech C] TRL:7 →│
                │  [Tech B] TRL:6 ↑│                  │
                ├──────────────────┼──────────────────┤
                │                  │                  │
  Low           │  [Tech D] TRL:4 ↑│  [Tech E] TRL:3 →│
                │                  │  [Tech F] TRL:2 ↓│
                └──────────────────┴──────────────────┘

### Placement Rationale
| Technology | X-score | Y-score | Key Evidence |
|-----------|---------|---------|-------------|
| [Tech A] | [value + source] | [value + source] | [why here] |
```

### 3c: Peer Technology Drill-Down

For each technology placed on the landscape map, produce a three-layer analysis: Architecture (core design) → Strategy (what trade-off it chose in the competitive space) → Effect (per-dimension results). This is especially critical for technologies in the ADOPT and TRIAL rings. A landscape map with positioning but no architectural explanation of each technology is a chart, not an insight. See [SKILL.md §9 Peer Technology Drill-Down](../SKILL.md).

### 3d: Value Migration Analysis

Identify where value is flowing within the domain:

```markdown
## Value Migration Flows

| From | To | Driver | Evidence | Timeline |
|------|----|--------|----------|----------|
| [declining tech/approach] | [growing tech/approach] | [what's causing the shift] | [data] | [when] |
```

### 3d: Technology Radar Classification

Classify each technology into radar rings:

```markdown
## Technology Radar — [Domain]

### ADOPT (TRL 8-9, proven, use with confidence)
| Technology | Evidence | Key Strength |
|-----------|----------|-------------|
| [tech] | [deployment data, benchmark proof] | [one line] |

### TRIAL (TRL 6-7, promising, worth POC)
| Technology | Evidence | What to Validate |
|-----------|----------|-----------------|
| [tech] | [benchmark + pilot data] | [key risk to test] |

### ASSESS (TRL 4-5, interesting, monitor actively)
| Technology | Evidence | Watch Signal |
|-----------|----------|-------------|
| [tech] | [paper + early results] | [what would trigger promotion to TRIAL] |

### HOLD (caution, do not start new adoption)
| Technology | Evidence | Reason |
|-----------|----------|--------|
| [tech] | [declining signals] | [why to avoid] |
```

### 3e: Extract IIR Chains

From the landscape analysis, extract 5-8 key insights:

```markdown
### Key Insight [N]: [one-sentence claim]

**Insight**: [what the landscape analysis reveals]
**Evidence**: [data from comparison matrix + positioning rationale]
**Implication**: [what this means for the industry/domain]
```

## Step 4: Draft Review (REQUIRED)

Present to user:

```markdown
## Landscape Draft: [Domain]

### Framing Question
[The question this landscape answers]

### Technologies Analyzed
[List with TRL and radar ring for each]

### Landscape Map
[2×2 matrix sketch]

### Key Findings
| # | Insight | Evidence Quality | Implication |
|---|---------|-----------------|-------------|
| 1 | ... | H/M/L | ... |

### Value Migration
[Top 2-3 migration flows]

### Evidence Gaps
[What's missing, where data is thin]

Confirm or request changes.
```

## Step 4.5: Visual Asset Collection (MANDATORY — runs BEFORE final assembly)

For every technology in scope:

1. Search for PRIMARY-SOURCE images: vendor product pages, architecture diagrams from official docs, paper figures, patent diagrams
2. Download to `assets/<slug>/` using [visual_collector.py](../scripts/visual_collector.py)
3. Record every image in `image_manifest.json` with `source_url` + `fetched_at`
4. Caption format: `图 X：[说明] — 来源：[原始链接](URL)`

**Prohibited**: watermark-stripped re-uploads, unattributable re-renders, stock photos.

## Step 5: Assemble Deliverable

Use [Landscape Scan template](../templates/landscape-scan.md).
Every factual sentence must carry an inline source link. The linter will reject source-free sentences.

### Handoff Options

- **Need strategic decisions?** → tech-planning: landscape map feeds directly into Look 1 (Trends) + Look 4 (Competition)
- **Need presentation?** → pro-pptx: landscape map → `tech-radar` layout, comparisons → `data`/`arch-compare` layouts

## Common Pitfalls

1. **Listing without positioning** — A feature list per technology is not a landscape. You must place them relative to each other on meaningful axes.
2. **Vendor marketing as evidence** — "X claims 10x faster" is not a benchmark. Seek independent evaluation.
3. **Stale landscape** — Technology landscapes shift fast. Verify data recency — prefer last 12 months.
4. **Missing the declining players** — It's as important to know what's fading as what's rising.
5. **Dimension overload** — Comparing on 20 dimensions creates noise. Pick the 5-8 that matter most for the framing question.
6. **Equal depth on everything** — Spend more analysis depth on TRIAL and ADOPT ring technologies; HOLD and ASSESS need less.
7. **Source-free sentences** — Every factual sentence needs an inline URL/DOI/patent number.
8. **Missing visuals** — Every technology needs at least one primary-source image.

## Relationship to Type-Specific Workflows

This workflow is the primary analysis engine for:
- [Type A — Domain](type-a-domain.md): Landscape provides multi-technology positioning and radar classification
- Also usable standalone for general multi-technology domain scans
