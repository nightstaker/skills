# Workflow: Type A — 细分技术领域洞察 (Segmented Technology Domain Insight)

Use this workflow when the user asks for an in-depth analysis of a specific, bounded technology domain — understanding the application-driven demands, systematically analyzing the TOP 5 technologies, and synthesizing technology trends with research implications.

Read [../REQUIREMENT.MD](../REQUIREMENT.MD) §2.1 before starting. The output template is [../templates/type-a-domain.md](../templates/type-a-domain.md).

The structure is 总—分—总 (synthesis → decomposition → synthesis). Skipping any layer turns the report into a surface survey.

---

## Step 1 — Define the Domain Boundary

Ambiguous domains produce useless analysis. Before searching, write down:

- **领域定义**：what specific technology area is this? (e.g., "固态电池电解质技术", not "电池技术")
- **上下游关系**：what feeds into this domain? What consumes its output?
- **核心应用场景**：what are the primary applications driving demand? (2-3 specific scenarios)

Write these as the opening block of the report. If the user pushes back on the boundary, negotiate before searching — do not silently widen it.

---

## Step 2 — Trace Application Evolution & Decompose Bottom-Level Demands

This is the "总" (synthesis) opening — ground the analysis in real-world application evolution, not abstract technology description.

### 2.1 Application Evolution

Trace the development history of applications in this domain:

- Key milestones with dates (each with source)
- Current market state and growth trajectory
- Driving forces behind the evolution (market demand, regulation, cost pressure, performance ceiling)

### 2.2 Bottom-Level Demand Decomposition

Build the demand chain layer by layer:

| Layer | Description | Example |
|-------|-------------|---------|
| **应用需求** | What does the end user / customer need? | "电动汽车续航 > 1000km" |
| **系统需求** | What system-level performance does that imply? | "电池能量密度 > 400 Wh/kg" |
| **技术需求** | What specific technology capability must improve? | "固态电解质离子电导率 > 10⁻³ S/cm at room temperature" |

Every layer transition must have a logical derivation — not just assertion. Each factual claim must carry an inline source.

---

## Step 3 — Lock the TOP 5 Technology Selection

Pick **one** primary ranking metric, publicly verifiable:

| Primary metric | Where to find it |
|---|---|
| Academic influence | Citation count, h-index of key papers, survey paper coverage |
| Industry adoption rate | Production deployments, vendor GA announcements, market reports |
| Technology maturity (TRL) | Published benchmarks, prototype demos, pilot programs |
| Patent density | Patent filing counts by technology route, major assignees |

Record the chosen metric and source URLs in the report's "TOP 5 入选依据" line.

**Selection rules**:
- Must span ≥2 distinct technical approaches for balance (e.g., oxide vs sulfide vs polymer for solid electrolytes)
- If domain too narrow for 5: degrade to TOP N (N≥3) with explicit justification
- Never pad with immature lab curiosities to reach 5 — every entry must have substantive evidence

---

## Step 4 — Visual Asset Collection (MANDATORY, runs BEFORE writing)

For every technology:

1. **Technology architecture diagram (MANDATORY)**: from the original paper figure, official whitepaper, patent figure, or authoritative review. Save as `assets/<slug>/tech<N>-arch.png`.
2. **Per-product/project architecture diagram (MANDATORY)**: for each representative product/project under this technology, fetch its architecture diagram from official docs, tech blogs, or papers. Save as `assets/<slug>/tech<N>-<product>-arch.png`.
3. **Application context image** (if available): product photo, deployment photo, or system diagram showing the technology in context. Save as `assets/<slug>/tech<N>-app.jpg`.

Record every image in `assets/<slug>/image_manifest.json`:

```json
{
  "tech1-arch.png": {
    "source_url": "https://...",
    "fetched_at": "2026-04-15T10:00:00Z",
    "license_note": "paper figure / public release"
  }
}
```

Run [../scripts/visual_collector.py](../scripts/visual_collector.py) to download in bulk. If a primary-source image cannot be found for a technology, escalate to the user — do not substitute a generic illustration.

---

## Step 5 — Per-Technology Deep Dive (×5)

This is the "分" (decomposition) layer. For each of the TOP 5 technologies:

### 5.1 Principle & Core Mechanism
One paragraph, plain-language but technically precise. Forbidden to stop at "uses X material / Y algorithm" — must explain the specific mechanism that differentiates this approach.

### 5.2 TRL & Industrialization
- TRL (1-9) with one-line justification
- Current production status: lab-only / pilot / mass production
- Key players pursuing this route (with sources)

### 5.3 Key Performance Metrics
Quantitative data — not qualitative descriptions. Every number must carry an inline source.
- Performance vs the technology demand identified in Step 2
- Comparison with the other 4 technologies on the same metrics

### 5.4 Moat Analysis
- Patent landscape: who holds key IP?
- Process / equipment barriers
- Talent concentration
- Ecosystem dependencies

### 5.5 Representative Results
- 2-3 most cited papers / most significant products / key patents (with links)

---

## Step 6 — Technology Comparison Matrix

Build a quantitative comparison table across all TOP 5 technologies:

| Metric | Tech 1 | Tech 2 | Tech 3 | Tech 4 | Tech 5 | Source |
|---|---|---|---|---|---|---|
| Key performance metric 1 | … | … | … | … | … | … |
| Key performance metric 2 | … | … | … | … | … | … |
| TRL | … | … | … | … | … | … |
| Cost indicator | … | … | … | … | … | … |
| Scalability | … | … | … | … | … | … |

If ≥3 technologies are compared, apply Peer Technology Drill-Down (SKILL.md §9): architecture → strategy choice → per-dimension results for each.

---

## Step 7 — Technology Trend Synthesis & Research Implication

This is the closing "总" (synthesis) layer.

### 7.1 Technology Trend Synthesis
Based on the TOP 5 analysis, answer:
- What is the **common evolution direction** across all technologies?
- Where are the **divergence points** — which technologies are heading in fundamentally different directions?
- Which technologies are **converging** (becoming interchangeable)? Which are **diverging** (targeting different niches)?
- What are the **emerging crossover areas** between these technologies?

### 7.2 Research Implication
Concrete, actionable recommendations — not platitudes:
- Which technology direction(s) merit heavy investment and why?
- Which path(s) should be avoided because evidence shows they hit fundamental limits?
- Which cross-domain combination(s) are emerging as high-potential research themes?
- What are the key capability gaps between current state and application demands (from Step 2)?

Forbidden phrases: "需要持续关注", "值得观察", "未来可期". The linter will reject them.

---

## Step 8 — QA Gate

Run the linter:

```bash
python scripts/linter.py reports/<slug>.md --assets assets/<slug>/ --type A
```

The linter will fail the report if any of the following are true:

- Missing any of the three mandatory layers (领域定义与应用发展 / TOP 5 技术分析 / 技术趋势与研究启示).
- Any factual sentence lacks an inline URL/DOI/patent number.
- Any technology is missing its principle/architecture diagram.
- Any image lacks the `图 X：[说明] — 来源：[链接]` caption.
- The technology comparison table has fewer than 3 technologies or is missing.
- The Implication contains banned filler phrases.

Fix every issue before delivering. Do not silence warnings.

---

## Deliverable

- `reports/<slug>.md` — the report
- `assets/<slug>/` — all downloaded images + `image_manifest.json`
- A final "Sources" section in the report, deduplicated and numbered, mirroring every inline citation

---

## Related Workflows

This Type A workflow leverages shared analysis workflows as building blocks:
- [Deep Dive](deep-dive.md) — for hypothesis-driven single technology analysis with TRL anchoring
- [Landscape](landscape.md) — for multi-technology domain positioning
- [Benchmark](benchmark.md) — for evidence collection and cross-validation

Evidence collection techniques and quality gates from those workflows apply here.
Final assembly follows the [Briefing](briefing.md) workflow pattern.
