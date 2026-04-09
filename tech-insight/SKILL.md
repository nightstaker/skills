---
name: tech-insight
description: "Use this skill for systematic, evidence-grounded, expert-depth technology insight and planning. Triggers on: requests for competitive landscape / TOP-N benchmark of products in a category; deep technical decomposition of an existing product line; future technology trend analysis with scenario→vendor→tech→business closed-loop; single-product teardown; any task that mentions '技术洞察', '技术趋势', '产品对标', 'TOP 5', 'competitive analysis', 'tech benchmark', 'tech trend', 'roadmap insight', 'teardown'. Reader profile is senior domain experts + domain investors — reports MUST reach architectural-primitive depth, cite specific foundry node variants, embed full benchmark methodology, cite patent numbers in moat analysis, and ship an investor-grade appendix (unit economics / customer concentration / capacity / regulatory). Every claim must be sourced (URL/DOI/patent number) and every report must embed real product / architecture / scene images from primary sources."
license: Proprietary
---

# Tech-Insight Skill

A production-grade technology insight skill that turns "vibes-based commentary" into engineered research. Every fact is sourced, every key technology is decomposed to microarchitectural primitives, every benchmark carries its full methodology, every moat claim is backed by patent numbers or SEC filings, and every report ships with an investor-grade appendix.

**Reader profile** (non-negotiable): senior domain experts (Chief Architect / Fellow / BU tech director) and domain investors (VC partners / PE tech DD leads). Content must pass both the "expert re-ask-one-more-layer" test and the "investor due-diligence" test. See REQUIREMENT.MD §1.3 for details.

Read [REQUIREMENT.MD](REQUIREMENT.MD) for the full specification. This file is the operating manual.

## Quick Reference

| Scenario | Guide |
|----------|-------|
| **Type A** — Existing tech, global TOP 5 horizontal benchmark | [workflows/existing-tech-top5.md](workflows/existing-tech-top5.md) |
| **Type B** — Future trend insight with closed-loop reasoning | [workflows/future-trend.md](workflows/future-trend.md) |
| **Type C** — Single-product deep teardown & decomposition | [workflows/single-product-teardown.md](workflows/single-product-teardown.md) |
| Output template — Type A | [templates/type-a-top5.md](templates/type-a-top5.md) |
| Output template — Type B | [templates/type-b-trend.md](templates/type-b-trend.md) |
| Output template — Type C | [templates/type-c-teardown.md](templates/type-c-teardown.md) |
| Worked example (Type A)  | [examples/sample-ai-accelerator-2025.md](examples/sample-ai-accelerator-2025.md) |
| Linter (source + visual + structure QA) | [scripts/linter.py](scripts/linter.py) |
| Visual asset downloader | [scripts/visual_collector.py](scripts/visual_collector.py) |

---

## Scenario Detection

Before starting, classify the request into Type A / B / C. Ask the user if ambiguous.

1. **Is the user asking about a category of products that already exist on the market?**
   - Yes → **Type A** (TOP 5 horizontal benchmark). Proceed to [workflows/existing-tech-top5.md](workflows/existing-tech-top5.md).

2. **Is the user asking where a technology / scenario is headed in the next 1–3 years?**
   - Yes → **Type B** (Future trend, closed-loop). Proceed to [workflows/future-trend.md](workflows/future-trend.md).

3. **Is the user asking for a deep-dive teardown of ONE specific product/technology?**
   - Yes → **Type C** (Single-product deep teardown). Proceed to [workflows/single-product-teardown.md](workflows/single-product-teardown.md).

4. **Combinations?** Type A → Type C (benchmark first, then drill into the leader) or Type A → Type B (present benchmark, then extrapolate). Cross-link the reports.

If the request is too narrow ("just look up spec X of product Y"), tell the user this skill is overkill and use a plain web search instead.

---

## Core Orchestration Loop (v2.0 — expert & investor depth)

For every task, follow this sequence. Do not skip steps — each guards a quality dimension defined in [REQUIREMENT.MD](REQUIREMENT.MD).

```
1. READER LOCK-IN (new, runs before everything else)
   Re-read REQUIREMENT.MD §1.3. The only readers are senior domain experts
   and domain investors. For every section you write, commit to the three
   questions:
     - What does this tell the expert that they don't already know?
     - What does this change for the investor's valuation / bet / risk?
     - What concrete claim here could be FALSIFIED by a future paper or filing?
   Sections that can't answer all three must be rewritten.

2. CATEGORY / SCENE FRAMING
   - Type A: Define category boundary (function / customer / price band / form factor).
             Lock TOP 5 selection criterion (share / shipments / revenue / ranking).
   - Type B: Define the user-perceivable Scene Anchor. No abstract tech jargon openings.
   - Type C: Confirm that ≥3 primary-source documents exist for the target product.

3. SOURCE COLLECTION (WebSearch + WebFetch)
   - Whitelist priority (see REQUIREMENT.MD §2.5 Source Tiering):
     T1 whitepaper / patent / SEC / paper > T2 vendor page / standards body
     > T3 SemiAnalysis / TechInsights / AnandTech / Gartner / IDC
     > T4 FT / WSJ / Nikkei / Bloomberg > T5 personal blog / social.
   - Require T1+T2 share ≥ 50% of the total source count.
   - Time window: vendor moves ≤ 12 months unless explicitly historical.
   - Cross-check: every key spec / share / price / capacity needs ≥2 T1–T3 sources.
   - Capture every URL into a running source ledger — you will need it for §7.

4. KEY TECH DECOMPOSITION (DEPTH DRILL — runs THREE passes)
   Pass 1 — Architecture internals:
     For every product / technology, NAME the microarchitectural units,
     COUNT them, and GIVE ONE DESIGN CONSTANT per unit (cache size, register
     count, head group count, MAC array dimensions, bus width).
     Forbidden stopping points: "uses Transformer", "adopts 3nm", "AI-native".
   Pass 2 — Process & packaging:
     Convert every "Xnm" into a specific foundry variant (TSMC N3E / Samsung
     SF4X / Intel 18A). State the packaging technology (CoWoS-L / FOPLP /
     EMIB). Find one public yield or die-size signal, even from SemiAnalysis /
     TechInsights.
   Pass 3 — Benchmark methodology:
     For every quoted performance number, capture the six-tuple (hardware,
     software, model, batch, seqlen, precision) and the test date / party.
     Numbers missing ≥3 of the six tuples must be discarded.

5. MOAT LEGAL EVIDENCE COLLECTION
   For the leading product in Type A / for every key technology in Type B /
   for the product under Type C:
     - Find ≥1 patent number (US/CN/EP/WO) covering the core claim;
       summarise its independent claim in one sentence.
     - Find ≥1 named long-term supply agreement / capacity reservation
       agreement / SEC filing paragraph.
     - Find ≥1 named design-win customer (with project code if public).
     - Find ≥1 open-source or ecosystem metric (GH stars / framework version
       support / merged PR velocity).

6. VISUAL ASSET COLLECTION (MANDATORY — runs BEFORE writing)
   For every product / scene / key tech, fetch ORIGINAL images from primary sources:
   a. Derive image queries from product names, architecture diagrams, die shots, scene photos.
   b. Use WebSearch to locate, WebFetch to download.
   c. Save under assets/<slug>/ with prefixed filenames (p1-hero.jpg, p1-arch.png, ...).
   d. Record source URL + fetch timestamp in image_manifest.json (link mode allowed).
   e. Coverage targets:
      - Type A: each TOP 5 product needs ≥1 product photo + ≥1 architecture/teardown/die shot.
      - Type B: ≥1 scene photo, ≥1 vendor representative product photo per major vendor,
                ≥1 key technology principle diagram.
      - Type C: ≥1 hero photo + ≥1 arch overview + ≥1 arch detail + ≥1 die shot / PCB.
   f. Reject second-hand re-renders that cannot be traced to a primary source.
   Run: python scripts/visual_collector.py --plan plan.json --assets-root assets/

7. CLOSED-LOOP REASONING (Type B only — extended)
   - Build the four-node loop: Tech → Product → Customer/Scene → Commercial Value.
   - Quantify the commercial node with TAM / SAM / SOM / ARPU / penetration curve.
   - List ≤5 core assumptions, each with a falsifiability condition.
   - State the COST OF BEING WRONG for each assumption (supply-chain rebuild,
     R&D pivot, contract break).

8. INVESTOR APPENDIX (required for ALL types — §2.4)
   Produce four mandatory sub-blocks:
     - Unit economics: ASP / BoM / wafer cost / gross margin / CapEx intensity
     - Customer concentration: top-3 customer share / named design wins / switching cost
     - Capacity & supply: fab slot / CoWoS / HBM / substrate allocations
     - Regulatory & geopolitical: specific rule citations (15 CFR 744 / BIS ECCN / CFIUS)
   If any sub-block has no public disclosure, write "无公开披露 — 原因：…".
   Do NOT leave empty.

9. DRAFT REPORT
   - Use the matching output template:
     - Type A → templates/type-a-top5.md
     - Type B → templates/type-b-trend.md
     - Type C → templates/type-c-teardown.md
   - Inline-cite every factual sentence with [text](URL).
   - Embed every collected image next to the paragraph it supports, using:
     `图 X：[说明] — 来源：[原始链接](URL)`
   - End each insight block with an Implication that answers "So what?" — no
     "needs continued attention" filler.
   - Add a Benchmark Methodology footer directly under KTD / Key Technical Metrics
     tables, listing the six-tuple for every cell that carries a number.

10. QA — LINTER (REQUIRED, never deliver without it)
    python scripts/linter.py <report.md> --assets assets/<slug>/ --type A      # Type A
    python scripts/linter.py <report.md> --assets assets/<slug>/ --type B      # Type B
    python scripts/linter.py <report.md> --assets assets/<slug>/ --type C      # Type C
    # Type A may degrade to TOP N via --top-n <3..5> when the category is legitimately narrow.
    The linter v2.0 will reject the report if any of the following fail:
    - Universal sourcing: any factual sentence without an inline URL/DOI/patent number.
    - Table-cell sourcing: KCA / KTD factual cells missing inline citations.
    - Visual coverage: any required image slot empty or missing source caption.
    - Structure integrity: Type-specific required sections (incl. Investor Appendix).
    - Banned shallow phrases: 业界领先 / 先进架构 / 生态完善 / industry-leading / …
    - Process-node foundry variant: bare "3nm" / "5nm" without TSMC N3E / Samsung SF4X / Intel 18A.
    - Benchmark methodology: KTD / Key Technical Metrics sections must mention
      batch + seqlen + precision + test-condition keywords.
    - Moat legal evidence: Moat / 壁垒 section must contain ≥1 patent number
      (US/CN/EP/WO) or ≥1 SEC filing reference.
    - Investor appendix: must cover unit economics + customer concentration
      + capacity + regulatory keyword families.
    - Implication actionability: bans phrases like "需要持续关注" / "值得观察".
    - Hallucination guard: any specific number / product code / quote without a source.

11. DELIVER
    - Hand over the markdown report + the assets/ folder (or a single zip).
    - Include the source ledger as the final "Sources" section, deduplicated and numbered.
    - Tag each source with its tier (T1 / T2 / T3 / T4 / T5) so the reader can
      calibrate confidence at a glance.
```

---

## Non-Negotiable Rules (v2.0)

Pulled directly from [REQUIREMENT.MD](REQUIREMENT.MD). Violating any of these is a hard fail.

- **Reader profile**: every paragraph must pass the expert "re-ask-one-more-layer" test AND the investor due-diligence test. Shallow content is rejected before the sourcing rule even runs.
- **Universal sourcing**: every statement, datum, quote, parameter, vendor action carries an inline source. No exceptions. Author inferences must be quarantined into a clearly-labelled "作者推断" subsection.
- **Primary-source visuals**: product photos, context photos, architecture diagrams, die shots, dataflow diagrams must come from the manufacturer / patent figure / paper figure / regulatory filing / official whitepaper. No watermark-stripped re-uploads.
- **Image–text binding**: every image sits adjacent to the paragraph it supports and uses the `图 X：[说明] — 来源：[链接]` caption format.
- **Architecture depth**: every architecture claim carries ≥1 named microarchitectural unit + ≥1 quantitative design constant + ≥1 trade-off statement. Block-diagram-level descriptions are rejected.
- **Process depth**: every process claim specifies a foundry node variant (TSMC N3E / Samsung SF4X / Intel 18A). Bare "3nm / 5nm / 7nm" is rejected.
- **Benchmark methodology**: every performance number carries ≥4 of the six-tuple (hardware / software / model / batch / seqlen / precision). KTD / Key Technical Metrics tables must have a methodology footer.
- **Moat legal evidence**: moat claims cite ≥1 patent number, SEC filing, long-term supply agreement, named design win, or quantitative open-source metric. "专利多、生态好、人才强" is rejected.
- **Investor appendix**: every report ships unit economics + customer concentration + capacity & supply + regulatory & geopolitical exposure. Empty sub-blocks are allowed only with "无公开披露 — 原因：…" explanation.
- **TOP 5 sample integrity (Type A)**: full global top 5 of the category; degrade to TOP N (N≥3) only for pathologically narrow categories, and explain why.
- **Closed loop (Type B)**: Tech → Product → Customer/Scene → Commercial Value, with explicit assumptions, falsifiability conditions, and cost-of-being-wrong.
- **Banned shallow phrases**: 业界领先 / 行业领先 / 先进架构 / 生态完善 / 市场广阔 / 潜力巨大 / industry-leading / best-in-class (unless paired with specific benchmark) / revolutionary / cutting-edge — rejected by linter.
- **Actionable implication**: every insight ends with a "So what?" answer that drives a product / strategy / investment decision.

---

## Tooling Dependencies

```bash
pip install requests
```

- `requests` — image download in [scripts/visual_collector.py](scripts/visual_collector.py)
- [scripts/linter.py](scripts/linter.py) uses only the Python standard library

The skill itself relies on Claude Code's built-in `WebSearch` and `WebFetch` tools for source discovery — no API keys required.
