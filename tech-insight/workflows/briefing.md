# Workflow: Briefing — Structured Insight Briefing Assembly

Assembles a structured technology insight briefing from analysis outputs. This is the "final assembly" workflow — it takes findings from Deep Dive, Landscape, or Benchmark workflows and packages them for consumption.

## Prerequisites

- Completed analysis from one or more workflows:
  - [Deep Dive](deep-dive.md) → hypothesis + IIR chains
  - [Landscape](landscape.md) → positioning map + comparison matrix
  - [Benchmark](benchmark.md) → evidence dossier + benchmark insights
- **Audience** — who will read/hear this briefing
- **Format preference** — Markdown report / PPTX presentation / both

## Step 1: Content Inventory

Gather all completed analysis artifacts:

```markdown
## Source Material Inventory

| Source | Artifact | Key Findings | Status |
|--------|----------|-------------|--------|
| Deep Dive: [topic] | Hypothesis verdict + N IIR chains | [top 3 insights] | Complete/Partial |
| Landscape: [domain] | Landscape map + radar + N IIR chains | [top 3 insights] | Complete/Partial |
| Benchmark: [question] | Comparison table + N insights | [top 3 insights] | Complete/Partial |
```

If any source is incomplete or has evidence gaps, flag them now — do not paper over gaps in the briefing.

## Step 2: Narrative Architecture

### 2a: Central Message

Distill all findings into ONE central message (the "so what" of the entire briefing):

```
Central Message: [One sentence capturing the most important technical signal]
```

**Test**: Could a busy executive act on this sentence alone? If not, it's too vague.

### 2b: Story Arc

Structure the briefing as an argument, not a data dump:

```markdown
## Briefing Architecture

### Opening — State the Hypothesis / Central Question
[1 section — frame what we investigated and why it matters]

### Body — Evidence & Analysis
Section 1: [finding group A — N slides/pages]
  - Insight 1: [IIR chain summary]
  - Insight 2: [IIR chain summary]
  - Visual: [what artifact — table, chart, landscape map]

Section 2: [finding group B — N slides/pages]
  - Insight 3: [IIR chain summary]
  - Insight 4: [IIR chain summary]
  - Visual: [what artifact]

Section 3: [finding group C — N slides/pages]
  - Insight 5: [IIR chain summary]
  - Visual: [what artifact]

### Closing — Verdict & Implications
[1-2 sections — hypothesis verdict, key takeaways, open questions]
```

**Rules**:
- Each section must advance the central message — cut sections that don't
- Maximum 3-4 body sections (5-8 insights total); deeper detail goes to appendix
- Every section has ONE "so what" — if you can't state it, the section has no clear purpose

### 2c: IIR Chain Sequencing

Order insights for maximum impact:

| Position | What goes here | Why |
|----------|---------------|-----|
| First body section | Most surprising or counter-intuitive finding | Captures attention, establishes analytical credibility |
| Middle sections | Supporting evidence and nuance | Builds the case with depth |
| Last body section | Most actionable or forward-looking finding | Leaves audience with clear next-step framing |

## Step 3: Visual Planning

### 3a: Visual Artifact Assignment

For each section, assign a primary visual:

```markdown
| Section | Primary Visual | Type | Data Source |
|---------|---------------|------|------------|
| Opening | [landscape map / hypothesis framing] | Quadrant / Diagram | [source workflow] |
| Body 1 | [benchmark comparison table] | Table / Chart | [benchmark workflow] |
| Body 2 | [architecture comparison] | Side-by-side diagram | [deep dive workflow] |
| Body 3 | [tech radar classification] | Radar quadrant | [landscape workflow] |
| Closing | [key metrics summary] | Metric cards | [aggregated from all] |
```

### 3b: Image Source Planning (for PPTX output)

If briefing will be rendered as PPTX via pro-pptx:

```markdown
| Section | Image Search Query | Fallback Visual |
|---------|-------------------|-----------------|
| Body 1 | `"[technology] architecture diagram official"` | Self-drawn block diagram |
| Body 2 | `"[benchmark name] results heatmap [year]"` | Self-drawn comparison table |
| Body 3 | `"[technology] ecosystem overview"` | Self-drawn radar quadrant |
```

Target: ≥ 60% of content sections with real web images.

## Step 4: Draft Review (REQUIRED)

Present the briefing outline to user:

```markdown
## Briefing Draft: [Title]

### Central Message
[One sentence]

### Target Audience
[Who + what they care about]

### Structure
| # | Section | Key Insight | Visual | "So What" |
|---|---------|------------|--------|-----------|
| 1 | Opening: [title] | [hypothesis framing] | [visual type] | [one sentence] |
| 2 | [section title] | [insight summary] | [visual type] | [one sentence] |
| 3 | [section title] | [insight summary] | [visual type] | [one sentence] |
| ... | | | | |
| N | Closing: [title] | [verdict] | [metric cards] | [one sentence] |

### Evidence Quality
- Total evidence points: N across M source types
- Confidence level: High/Medium/Low
- Known gaps: [list]

### Estimated Length
- Markdown: ~N pages
- PPTX: ~N slides

Confirm structure, or request changes.
```

## Step 5: Assemble Final Deliverable

### Option A: Markdown Report

Use appropriate template:
- Single-topic → [Insight Report](../templates/insight-report.md)
- Multi-technology → [Landscape Scan](../templates/landscape-scan.md)
- Quarterly review → [Tech Radar](../templates/tech-radar.md)

**Content enrichment** (apply if any section is below density floor):
- Supplement with industry background from evidence collection
- Expand single-point findings into full IIR structure
- Ensure ≥ 3 analytical points per section
- Every section must have both text analysis AND visual artifact

### Option B: PPTX via pro-pptx

Hand off to pro-pptx skill with hw-insight template:

**Mapping from briefing to slides**:

| Briefing Element | PPTX Layout | Content Mapping |
|-----------------|-------------|-----------------|
| Opening hypothesis | `insight-summary` | So-What callout = central message; 3 pillars = key support points |
| IIR chain (general) | `content` | Title = insight; Body = evidence + implication; Callout = "so what" |
| Benchmark comparison | `data` | Chart or table from benchmark data; insight annotation strip |
| Landscape map | `tech-radar` | 2×2 quadrant with positioned technologies |
| Architecture comparison | `arch-compare` | Side-by-side panels with trade-off callouts |
| Key metrics | `tech-metric` | 3-4 large metric blocks from benchmark highlights |
| Signal vs implication | `two-column` | Left = signals/evidence; Right = industry implications |
| Closing verdict | `closing` | Numbered conclusions; strategic callout bar |

**Slide title rule**: Each title states the INSIGHT, not the topic.

**Pass these to pro-pptx**:
- Complete content tree (sections → slides)
- All IIR chains with evidence sources
- Visual artifact descriptions
- Image search queries for each slide
- Evidence citations for Slide Notes

### Option C: Both Markdown + PPTX

Generate Markdown first (more detail), then derive PPTX (presentation-density summary) from it.

## Step 6: Quality Check — Linter Gate (REQUIRED)

Run the linter before delivery:

```bash
python scripts/linter.py <report.md> --assets assets/<slug>/ --type A|B
```

For general reports (not Type A/B), manually verify these checks:

| Check | Criterion | Pass? |
|-------|----------|-------|
| Universal sourcing | Every factual sentence has inline URL/DOI/patent number | |
| Central message | Clear, one-sentence, actionable | |
| IIR completeness | Every insight has evidence + implication | |
| Visual coverage | Every section has ≥ 1 primary-source image with caption | |
| Image manifest | `assets/<slug>/image_manifest.json` exists with `source_url` for every image | |
| Density | ≥ 3 analytical points per section | |
| "So What" discipline | Each section has exactly ONE core signal | |
| Banned phrases | No "需要持续关注", "值得观察", "未来可期", etc. | |
| Hypothesis verdict | Opening hypothesis addressed in closing | |
| Evidence gaps | All gaps disclosed, not hidden | |
| TRL accuracy | Every technology has TRL with evidence | |
| Hallucination guard | No specific numbers / product codes / quotes without source | |
| Audience fit | Depth and framing appropriate for target audience | |

## Common Pitfalls

1. **Data dump without narrative** — Presenting all evidence without a story arc. The briefing must ARGUE, not list.
2. **Missing central message** — If you can't state the briefing's point in one sentence, you haven't synthesized enough.
3. **Orphan sections** — Sections that don't connect to the central message. Cut them or restructure.
4. **Visual as decoration** — Charts and diagrams must carry analytical weight, not just look professional.
5. **Confidence inflation** — Presenting Medium-confidence findings as settled facts. Be transparent about evidence quality.
6. **One-way handoff to PPTX** — Don't throw raw data at pro-pptx. Structure the content tree fully before handoff.
7. **Source-free sentences** — The linter will reject any factual sentence without an inline URL/DOI/patent number.
8. **Missing image manifest** — All images must be downloaded to `assets/<slug>/` with provenance in `image_manifest.json`.
9. **Filler implications** — "需要持续关注" is banned. Every "So what?" must be a concrete, actionable statement.
