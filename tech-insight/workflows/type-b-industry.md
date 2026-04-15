# Workflow: Type B — 行业技术趋势洞察 (Industry Technology Trend Insight)

Use this workflow when the user asks for a comprehensive technology landscape of an entire industry — tracing its development history, mapping mainstream and potential technology routes, analyzing each route in depth (with product examples), and synthesizing cross-route comparison with research recommendations.

Read [../REQUIREMENT.MD](../REQUIREMENT.MD) §2.2 before starting. Output template: [../templates/type-b-industry.md](../templates/type-b-industry.md).

The structure follows: industry history → per-route deep analysis → cross-route synthesis. Skipping any layer degrades the report to a Wikipedia summary.

---

## Step 1 — Define the Industry Scope

Before searching, write down:

- **行业定义**：what industry? Be specific. (e.g., "车载激光雷达", not "自动驾驶传感器")
- **价值链位置**：where in the value chain does this industry sit? Upstream / midstream / downstream?
- **市场规模量级**：order of magnitude (e.g., "2025 global market ~$5B")
- **分析视角**：are we looking at the whole industry or a specific segment?

Write these as the opening block. Negotiate with the user if the scope is too broad (an entire industry like "半导体" is too wide — narrow to a segment).

---

## Step 2 — Trace Industry Development History

Build a chronological narrative with key milestones:

- **起源期**：when and how did this industry start? What was the original driver?
- **成长期**：key inflection points, breakthrough products, regulatory changes
- **当前阶段**：market size, growth rate, competitive landscape (with sources)

Every milestone must carry a date and inline source. Use `WebSearch` + `WebFetch`.

Embed at least one **industry timeline or market evolution chart** from a primary source (industry report, analyst presentation, company prospectus).

---

## Step 3 — Identify Technology Route Landscape

From the history, extract and classify technology routes:

| Technology Route | Classification | Basis for Classification | Key Players | Source |
|---|---|---|---|---|
| Route A | 主力 (Mainstream) | Mass production proven, >X% market share | … | [src](URL) |
| Route B | 主力 (Mainstream) | … | … | [src](URL) |
| Route C | 潜力 (Potential) | Lab-validated, TRL 4-6, no mass production yet | … | [src](URL) |

**Classification criteria**:
- **主力 (Mainstream)**: technology route with products in mass production, proven by market adoption and revenue
- **潜力 (Potential)**: technology route in research/pilot stage but with credible evidence of future viability (papers, funded programs, prototype demos)

If the classification is debatable, state both sides with evidence and let the analysis resolve it.

---

## Step 4 — Visual Asset Collection (MANDATORY, runs BEFORE writing)

For every technology route:

1. **Technology principle/architecture diagram (MANDATORY)**: from original paper, whitepaper, or patent figure. Save as `assets/<slug>/route<N>-arch.png`.
2. **Per-product architecture diagram (MANDATORY)**: for each representative product under this route, fetch its architecture diagram from official docs, tech blogs, or papers. Save as `assets/<slug>/route<N>-<product>-arch.png`.
3. **Representative product photo** (for mainstream routes): from the vendor product page or press kit. Save as `assets/<slug>/route<N>-product.jpg`.
4. **Industry-level visual** (at least 1): market evolution chart, technology roadmap, or competitive landscape map. Save as `assets/<slug>/industry-*.png`.

Record every image in `assets/<slug>/image_manifest.json`. Run [../scripts/visual_collector.py](../scripts/visual_collector.py) for bulk download.

---

## Step 5 — Per-Route Deep Analysis

For each technology route, follow this structure:

### 5.1 Product Anchors (if mainstream route has successful products)

Pick the 2-3 most representative products:

| Product | Vendor | Market Performance | Core Selling Point | Source |
|---|---|---|---|---|
| … | … | … | … | [src](URL) |

Embed product photos. These products are the **entry point** for the reader — they ground the technology discussion in tangible reality.

If the route has no successful products yet (potential route), skip this subsection and note explicitly that no production deployment exists.

### 5.2 Technology Strengths & Limitations

Build a structured analysis:

| Dimension | Strength | Limitation | Quantitative Metric | Source |
|---|---|---|---|---|
| Performance | … | … | … | [src](URL) |
| Cost | … | … | … | [src](URL) |
| Reliability | … | … | … | [src](URL) |
| Scalability | … | … | … | [src](URL) |

Forbidden to stop at "high performance" or "low cost" — must give quantitative metrics with sources.

### 5.3 Frontier Research Directions

Driven by **evolving application demands** (not by technology push alone):

1. What application requirements are changing? (e.g., higher resolution, lower power, smaller form factor)
2. How does this drive new research in this technology route?
3. What are the latest research hotspots? (cite 2-3 key papers/patents from the last 12-24 months)
4. What breakthroughs would unlock the next stage?

Embed at least one principle diagram for frontier research from an original paper or whitepaper.

---

## Step 6 — Cross-Route Comparison Matrix

Build a horizontal comparison across all routes:

| Dimension | Route A | Route B | Route C | … | Source |
|---|---|---|---|---|---|
| Performance metric 1 | … | … | … | … | … |
| Cost | … | … | … | … | … |
| Maturity (TRL) | … | … | … | … | … |
| Scalability | … | … | … | … | … |
| Best-fit scenario | … | … | … | … | — |

If ≥3 routes are compared, apply Peer Technology Drill-Down (SKILL.md §9): architecture → strategy choice → per-dimension results for each.

---

## Step 7 — Industry Technology Research Recommendation

Concrete, actionable recommendations structured as:

- **主力路线深耕方向**：where should established routes invest next? What specific sub-problems need solving?
- **潜力路线布局时机**：which potential routes are approaching an inflection point? What signals should trigger investment?
- **跨路线融合机会**：are there convergence opportunities where combining routes creates new value?
- **应规避的方向**：which paths have been attempted and failed? What evidence proves they're dead ends?

Forbidden phrases: "需要持续关注", "值得观察", "未来可期". The linter will reject them.

---

## Step 8 — QA Gate

```bash
python scripts/linter.py reports/<slug>.md --assets assets/<slug>/ --type B
```

The linter rejects the report if:

- Missing any of the three mandatory layers (行业发展史与技术路线引出 / 逐条技术路线分析 / 全局总结与研究建议).
- Any factual sentence is not inline-sourced.
- Required images (industry visual, route product photos, tech principle diagrams) are missing or uncaptioned.
- Cross-route comparison table is missing.
- The Recommendation contains filler phrases.

Fix every failure before delivery. Never `--ignore` linter warnings.

---

## Deliverable

- `reports/<slug>.md` — the report
- `assets/<slug>/` — industry visuals, product photos, tech principle diagrams + `image_manifest.json`
- Numbered "Sources" section at the end of the report

---

## Related Workflows

This Type B workflow leverages shared analysis workflows:
- [Deep Dive](deep-dive.md) — for individual technology route deep analysis
- [Landscape](landscape.md) — for multi-route positioning and classification
- [Benchmark](benchmark.md) — for evidence collection and cross-validation on key claims

Final assembly follows the [Briefing](briefing.md) workflow pattern.
