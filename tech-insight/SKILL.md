---
name: tech-insight
description: "Use this skill for systematic, evidence-grounded technology insight and planning. Triggers on: requests for competitive landscape / TOP-N benchmark of products in a category; deep technical decomposition of an existing product line; future technology trend analysis with scenario→vendor→tech→business closed-loop; any task that mentions '技术洞察', '技术趋势', '产品对标', 'TOP 5', 'competitive analysis', 'tech benchmark', 'tech trend', 'roadmap insight'. Every claim in the output must be sourced (URL/DOI/patent number) and every report must embed real product / architecture / scene images from primary sources."
license: Proprietary
---

# Tech-Insight Skill

A production-grade technology insight skill that turns "vibes-based commentary" into engineered research: every fact is sourced, every key technology is decomposed, every report carries real visual evidence, and every insight ends with an actionable "So what?".

Read [REQUIREMENT.MD](REQUIREMENT.MD) for the full specification. This file is the operating manual.

## Quick Reference

| Scenario | Guide |
|----------|-------|
| **Type A** — Existing tech, global TOP 5 horizontal benchmark | [workflows/existing-tech-top5.md](workflows/existing-tech-top5.md) |
| **Type B** — Future trend insight with closed-loop reasoning | [workflows/future-trend.md](workflows/future-trend.md) |
| Output template — Type A | [templates/type-a-top5.md](templates/type-a-top5.md) |
| Output template — Type B | [templates/type-b-trend.md](templates/type-b-trend.md) |
| Linter (source + visual + structure QA) | [scripts/linter.py](scripts/linter.py) |
| Visual asset downloader | [scripts/visual_collector.py](scripts/visual_collector.py) |

---

## Scenario Detection

Before starting, classify the request into Type A or Type B. Ask the user if ambiguous.

1. **Is the user asking about a category of products that already exist on the market?**
   - Yes → **Type A** (TOP 5 horizontal benchmark). Proceed to [workflows/existing-tech-top5.md](workflows/existing-tech-top5.md).

2. **Is the user asking about where a technology / scenario is headed in the next 1–3 years?**
   - Yes → **Type B** (Future trend, closed-loop). Proceed to [workflows/future-trend.md](workflows/future-trend.md).

3. **Both?** Run Type A first to anchor the present, then Type B to extrapolate. Cross-link the two reports.

If the request is too narrow ("just look up spec X of product Y"), tell the user this skill is overkill and use a plain web search instead.

---

## Core Orchestration Loop

For every task, follow this sequence. Do not skip steps — each guards a quality dimension defined in [REQUIREMENT.MD](REQUIREMENT.MD).

```
1. CATEGORY / SCENE FRAMING
   - Type A: Define category boundary (function / customer / price band / form factor).
             Lock TOP 5 selection criterion (share / shipments / revenue / ranking).
   - Type B: Define the user-perceivable Scene Anchor. No abstract tech jargon openings.

2. SOURCE COLLECTION (WebSearch + WebFetch)
   - Whitelist priority: official release > patent > paper > regulatory filing
     > top-tier media review > industry report > personal blog.
   - Time window: vendor moves ≤ 12 months unless explicitly historical.
   - Cross-check: every key spec / share / price needs ≥2 independent sources.
   - Capture every URL into a running source ledger — you will need it for §6.

3. KEY TECH DECOMPOSITION
   - Forbidden to stop at "uses Transformer / 3nm process".
   - Drill to architectural choices, key hyperparameters, process node deltas.
   - Build a quantitative comparison table (perf / power / cost / yield / ecosystem).
   - Identify the moat: patent / talent / process / ecosystem / data.

4. VISUAL ASSET COLLECTION (MANDATORY — runs BEFORE writing)
   For every product / scene / key tech, fetch ORIGINAL images from primary sources:
   a. Derive image queries from product names, architecture diagrams, die shots, scene photos.
   b. Use WebSearch to locate, WebFetch to download.
   c. Save under assets/<slug>/ with prefixed filenames (p1-hero.jpg, p1-arch.png, ...).
   d. Record the original source URL + fetch timestamp for every file (image_manifest.json).
   e. Coverage targets:
      - Type A: each TOP 5 product needs ≥1 product photo + ≥1 architecture/teardown/die shot.
      - Type B: ≥1 scene photo, ≥1 vendor representative product photo per major vendor,
                ≥1 key technology principle diagram.
   f. Reject second-hand re-renders that cannot be traced to a primary source.
   Run: python scripts/visual_collector.py --slug <slug> --manifest <plan.json>

5. CLOSED-LOOP REASONING (Type B only)
   - Build the four-node loop: Tech → Product → Customer/Scene → Commercial Value.
   - Quantify the commercial node with TAM / SAM / SOM / ARPU / penetration curve.
   - List ≤5 core assumptions, each with a falsifiability condition.

6. DRAFT REPORT
   - Use the matching output template:
     - Type A → templates/type-a-top5.md
     - Type B → templates/type-b-trend.md
   - Inline-cite every factual sentence with [text](URL).
   - Embed every collected image next to the paragraph it supports, using:
     `图 X：[说明] — 来源：[原始链接](URL)`
   - End each insight block with an Implication that answers "So what?" — no
     "needs continued attention" filler.

7. QA — LINTER (REQUIRED, never deliver without it)
   python scripts/linter.py <report.md> --assets assets/<slug>/
   The linter will reject the report if any of the following fail:
   - Universal sourcing: any factual sentence without an inline URL/DOI/patent number.
   - Visual coverage: any required image slot empty or missing source caption.
   - Structure: Type A six-section integrity / Type B five-stage + closed-loop integrity.
   - Implication actionability: bans phrases like "需要持续关注" / "值得观察".
   - Hallucination guard: any specific number / product code / quote without a source.

8. DELIVER
   - Hand over the markdown report + the assets/ folder (or a single zip).
   - Include the source ledger as the final "Sources" section, deduplicated and numbered.
```

---

## Non-Negotiable Rules

Pulled directly from [REQUIREMENT.MD](REQUIREMENT.MD). Violating any of these is a hard fail.

- **Universal sourcing**: every statement, datum, quote, parameter, vendor action carries an inline source. No exceptions. Author inferences must be quarantined into a clearly-labelled "作者推断" subsection.
- **Primary-source visuals**: product photos, context photos, architecture diagrams, die shots, dataflow diagrams must come from the manufacturer / patent figure / paper figure / regulatory filing / official whitepaper. No watermark-stripped re-uploads.
- **Image–text binding**: every image sits adjacent to the paragraph it supports and uses the `图 X：[说明] — 来源：[链接]` caption format.
- **TOP 5 sample integrity (Type A)**: full global top 5 of the category; degrade to TOP N (N≥3) only for pathologically narrow categories, and explain why.
- **Closed loop (Type B)**: Tech → Product → Customer/Scene → Commercial Value, with explicit assumptions and falsifiability conditions.
- **Actionable implication**: every insight ends with a "So what?" answer that drives a product / strategy / investment decision.

---

## Tooling Dependencies

```bash
pip install requests
```

- `requests` — image download in [scripts/visual_collector.py](scripts/visual_collector.py)
- [scripts/linter.py](scripts/linter.py) uses only the Python standard library

The skill itself relies on Claude Code's built-in `WebSearch` and `WebFetch` tools for source discovery — no API keys required.
