# Workflow: Type A — Existing Tech, Global TOP 5 Horizontal Benchmark

Use this workflow when the user asks for a competitive landscape, technology benchmark, or product teardown across an existing product category. Goal: produce a horizontal insight that maps the entire top tier of the category, not a single-product writeup.

**Reader profile** (see [../REQUIREMENT.MD](../REQUIREMENT.MD) §1.3): senior domain experts + domain investors. Every paragraph must pass the expert "re-ask-one-more-layer" test AND the investor due-diligence test. Shallow content is rejected before the sourcing rule even runs.

Read [../REQUIREMENT.MD](../REQUIREMENT.MD) §2.1 before starting. The output template is [../templates/type-a-top5.md](../templates/type-a-top5.md).

---

## Step 0 — Reader Lock-In

Before writing anything, commit the three-question filter for this report:

- **What does this tell the expert** (Chief Architect / Fellow) that they don't already know from datasheets alone?
- **What does this change for the investor** (VC / PE / 产业资本) — does it alter the valuation, bet, or risk score for any named vendor?
- **What would falsify the report's central claims** if a new paper, filing, or benchmark appeared tomorrow?

If any section fails all three at draft time, rewrite it or delete it.

---

## Step 1 — Lock the Category Boundary

Ambiguous categories produce useless rankings. Before searching, write down:

- **Function**: what job does the product do? (e.g., "on-device LLM inference accelerator", not "AI chip")
- **Customer**: who pays for it? (hyperscaler / enterprise / consumer / developer)
- **Price band**: order of magnitude only (e.g., $5–15k SKU)
- **Form factor / deployment**: PCIe card / SoC / SaaS / appliance

Write these four lines as the very first block of the report. If the user pushes back on the boundary, negotiate before searching — do not silently widen it.

---

## Step 2 — Lock the TOP 5 Selection Criterion

Pick **one** primary ranking metric and **one** tiebreaker, both publicly verifiable:

| Primary metric | Where to find it |
|---|---|
| Market share % | Gartner / IDC / Counterpoint / Omdia / company 10-K |
| Unit shipments | Vendor earnings calls, regulatory filings |
| Revenue | 10-K, 20-F, prospectuses |
| Authoritative ranking | MLPerf / SPEC / Top500 / industry shootouts |

Record the chosen metric and the source URL in the report's "TOP 5 入选依据" line.

If the category is so narrow that 5 credible products do not exist, degrade to TOP N (N≥3) and write a one-sentence justification. Never pad with second-tier products to reach 5.

**Sample balance**: the chosen 5 must span at least 2 regions and at least 2 distinct technical routes. If they don't, you've defined the category too narrowly — go back to Step 1.

---

## Step 3 — Per-Product Profile (×5)

For each product, fetch from primary sources:

- Vendor, product name, latest version, release date
- Market share / shipments / installed base (with source URL)
- Price band (with source URL)
- Target customer

Use `WebSearch` + `WebFetch`. Refuse to write a row whose data cannot be traced to an official page, an analyst report, or a regulatory filing. If a price is not public, write "未公开" — never guess.

---

## Step 4 — Visual Asset Collection (MANDATORY, runs BEFORE writing)

For every product:

1. **Product photo**: from the vendor product page or press kit. Save as `assets/<slug>/p<N>-hero.jpg`.
2. **Architecture / teardown / die shot**: from the official whitepaper, an authoritative review (AnandTech, ServeTheHome, TechInsights, SemiAnalysis, ChipRebel), or a patent figure. Save as `assets/<slug>/p<N>-arch.png`.

Record every image in `assets/<slug>/image_manifest.json`:

```json
{
  "p1-hero.jpg": {
    "source_url": "https://...",
    "fetched_at": "2026-04-09T10:00:00Z",
    "license_note": "vendor press kit / public release"
  }
}
```

Run [../scripts/visual_collector.py](../scripts/visual_collector.py) to download in bulk. If a primary-source image cannot be found for a product, escalate to the user — do not substitute a stock photo and do not skip the slot.

---

## Step 5 — KCA Matrix (Product × Competitive Dimension)

Pick 3–5 competitive dimensions that actually distinguish the products in this category — typical examples:

- Peak performance (TOPS / TFLOPS / tokens-per-second / IOPS)
- Energy efficiency (perf-per-watt)
- Total cost of ownership
- Software / ecosystem maturity
- Vertical integration depth
- Time-to-market on new workloads

Build a 5-column matrix. **Each cell** must:

1. State a fact, not a slogan.
2. Carry an inline source `[text](URL)`.
3. Distinguish marketing claims from verifiable engineering facts (mark marketing claims as "厂商宣称" and pair each marketing claim with at least one independent benchmark or teardown — unmatched marketing rows are treated as unverified).
4. Every quoted number carries its unit and its measurement condition.

---

## Step 6 — KTD Comparison (Quantitative Tech Decomposition)

The KTD table is the single densest piece of the report. It must cover at least the following rows — do not stop at marketing-layer abstractions:

| Row | Required depth |
|---|---|
| Process node | Foundry variant (TSMC N3E / Samsung SF4X / Intel 18A / TSMC N4P …) — never bare "3nm" |
| Packaging | CoWoS-L / FOPLP / EMIB / 2.5D / 3D stacking |
| Core microarch units | Named unit + count + generation (e.g., SM Gen5 ×144) |
| Cache / SRAM | L0/L1/L2/LLC sizes per unit + register file size |
| HBM | Gen + stack layers + capacity + bandwidth |
| Interconnect | Protocol + generation + GB/s + topology + max scale |
| Software stack | Compiler name + version + framework support matrix |
| Perf benchmarks | Number + precision + workload + benchmark source |
| Power / TOPS-per-W | Number + measurement condition |
| Die size + yield signal | mm² + foundry/third-party estimate |

For every quoted performance number, capture the **six-tuple**: hardware, software stack, model, batch, seqlen, precision. Numbers missing ≥3 of the six tuples must be discarded.

Under the KTD table, you MUST include a **Benchmark Methodology Footer** listing:

- Hardware configuration (model + card count + interconnect topology) with source
- Software stack (driver + runtime + compiler + framework version) with source
- Workload (model + parameter count + context length) with source
- Precision (FP8/FP16/BF16/INT8/W4A16) with source
- Batch size + sequence length with source
- Test date and benchmarking party with source

The linter will reject KTD sections that do not mention `batch`, `seqlen`/`sequence length`, `precision`/`FP8`/`FP16`/`BF16`/`INT8`, and `测试条件`/`methodology`.

---

## Step 6.5 — Moat Analysis (Legal-grade evidence)

For the leading product (usually P1), run a five-axis moat analysis. Each axis must carry **legal or commercial level evidence** — not adjectives:

- **Patent stack**: cite at least one patent number (`US\d{7,}` / `CN\d{9,}` / `EP\d{7,}` / `WO\d{4}/\d{6,}`) and summarize its independent claim in one sentence.
- **Process / fab access**: cite a named long-term supply agreement, capacity reservation agreement, or a specific paragraph in an SEC / HKEX filing.
- **Ecosystem**: cite named framework integrations (e.g., PyTorch version X, vLLM commit Y), GitHub star count, merged PR velocity.
- **Data / learning flywheel** (if any): cite dataset size, update cadence, customer feedback loop signals.
- **Talent / organization**: only if cited in public reporting — do not speculate.

For each axis, answer explicitly: **"Can a well-funded follower replicate this in 24 months? Yes / No — one sentence why."**

---

## Step 7 — Cross-Product Insight

A short narrative section (200–400 chars Chinese) answering:

- What is the **shared paradigm** that all 5 products converge on?
- What is the **dividing line** — where do they intentionally diverge?
- Who is **leading**, who is **following**, who is **on the way out**?
- Which past assumptions has the market already invalidated?

This is the section the reader will quote. Make it tight and source-anchored.

---

## Step 8 — Implication

Answer "So what?" for the reader's product / strategy / investment context. Concretely:

- Which dimension is the highest-leverage entry point for our team?
- Which already-attempted path should we avoid because it has been falsified?
- Which engineering fact can we directly reuse?

Forbidden phrases: "需要持续关注", "值得观察", "未来可期", "业界领先", "行业领先", "先进架构", "生态完善", "industry-leading", "best-in-class" (unless paired with specific benchmark), "revolutionary", "cutting-edge". The linter will reject them.

---

## Step 8.5 — Investor Appendix (MANDATORY for every report)

Every Type A report must ship an investor-grade appendix. Read [../REQUIREMENT.MD](../REQUIREMENT.MD) §2.4 for full requirements. Four mandatory sub-blocks:

### 8.5.1 Unit Economics
- **ASP**: range + source
- **BoM / wafer cost estimate**: die size × wafer ASP × yield + HBM + packaging + test — cite SemiAnalysis / TechInsights / ChipRebel if no first-party data
- **Gross margin range**: from company earnings or analyst model
- **CapEx intensity**: CapEx per $100M revenue

### 8.5.2 Customer Concentration
- **Top-3 customer share**: with source or explicit "not publicly disclosed"
- **Named design wins**: customer name + project code + annualized deal size if public
- **Switching cost signals**: software stack lock-in, procurement cycle, certification cost

### 8.5.3 Capacity & Supply Constraints
- **Front-end capacity**: foundry node wafer starts / monthly capacity; long-term contract commitments
- **Back-end capacity**: CoWoS / FOPLP / advanced packaging monthly capacity share
- **Key BOM items**: HBM allocation (SK hynix / Samsung / Micron), ABF substrate, special substrates
- **24-month bottleneck**: single-sentence conclusion on the tightest knot

### 8.5.4 Regulatory & Geopolitical Exposure
- **Export controls**: cite specific rule numbers (15 CFR Part 744 / BIS ECCN / EAR / EU Chips Act)
- **Antitrust / national security**: CFIUS / SAMR / CMA public disclosures
- **Regional market access**: China CCC, EU CE, US FCC, India BIS
- **Key geopolitical exposure**: Taiwan Strait / Russia-Ukraine / Middle East direct impact on supply or sales

If any sub-block has no public disclosure, write "**无公开披露 — 原因：…**" explicitly. Do NOT leave blank.

---

## Step 9 — QA Gate

Run the linter:

```bash
python scripts/linter.py reports/<slug>.md --assets assets/<slug>/ --type A
```

The linter will fail the report if any of the following are true:

- Any sentence in §3–§8 lacks an inline URL/DOI/patent number.
- Any KCA or KTD cell with a factual claim lacks an inline source.
- Any of the 5 products is missing its product photo or architecture image.
- Any image lacks the `图 X：[说明] — 来源：[链接]` caption.
- The KCA Matrix has fewer than 3 dimensions or fewer than 5 product columns (unless TOP N degradation is justified).
- Any banned shallow phrase (业界领先 / 先进架构 / 生态完善 / industry-leading …) appears anywhere.
- Bare process node numbers appear without a foundry variant (TSMC N3E / Samsung SF4X / Intel 18A).
- KTD section misses `batch`, `seqlen`/`sequence length`, `precision`/`FP8`/`FP16`/`BF16`/`INT8`, or `测试条件`/`methodology` keywords.
- Moat / 壁垒 section is missing a patent number or SEC / HKEX filing reference.
- Investor Appendix is missing any of the four sub-blocks or any of their keyword families (unit economics, customer concentration, capacity, regulatory).
- The Implication contains banned filler phrases.

Fix every issue before delivering. Do not silence warnings.

---

## Deliverable

- `reports/<slug>.md` — the report
- `assets/<slug>/` — all downloaded images + `image_manifest.json`
- A final "Sources" section in the report, deduplicated and numbered, mirroring every inline citation
