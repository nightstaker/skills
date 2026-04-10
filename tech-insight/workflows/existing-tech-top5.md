# Workflow: Type A — Existing Tech, Global TOP 5 Horizontal Benchmark

Use this workflow when the user asks for a competitive landscape, technology benchmark, or product teardown across an existing product category. Goal: produce a horizontal insight that maps the entire top tier of the category, not a single-product writeup.

Read [../REQUIREMENT.MD](../REQUIREMENT.MD) §2.1 before starting. The output template is [../templates/type-a-top5.md](../templates/type-a-top5.md).

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
3. Distinguish marketing claims from verifiable engineering facts (mark marketing claims as "厂商宣称").

---

## Step 6 — KTD Comparison (Quantitative Tech Decomposition)

For the technologies that drive the KCA Matrix, build a second table with quantitative deltas:

| Technical metric | P1 | P2 | P3 | P4 | P5 | Source |
|---|---|---|---|---|---|---|
| Process node | 4nm | 5nm | 3nm | 7nm | 4nm | … |
| Memory bandwidth (GB/s) | … | … | … | … | … | … |
| Interconnect | NVLink | CXL | UCIe | PCIe5 | proprietary | … |
| FP8 efficiency | … | … | … | … | … | … |

Forbidden to stop at the marketing layer ("uses Transformer", "3nm process"). Drill to specific architectural choices and the engineering trade-offs they imply. Append a moat analysis paragraph for the leading product: patent stack, talent density, fab access, ecosystem lock-in, data network effects.

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

Forbidden phrases: "需要持续关注", "值得观察", "未来可期". The linter will reject them.

---

## Step 9 — QA Gate

Run the linter:

```bash
python scripts/linter.py reports/<slug>.md --assets assets/<slug>/ --type A
```

The linter will fail the report if any of the following are true:

- Any sentence in §3–§8 lacks an inline URL/DOI/patent number.
- Any of the 5 products is missing its product photo or architecture image.
- Any image lacks the `图 X：[说明] — 来源：[链接]` caption.
- The KCA Matrix has fewer than 3 dimensions or fewer than 5 product columns (unless TOP N degradation is justified).
- The Implication contains banned filler phrases.

Fix every issue before delivering. Do not silence warnings.

---

## Deliverable

- `reports/<slug>.md` — the report
- `assets/<slug>/` — all downloaded images + `image_manifest.json`
- A final "Sources" section in the report, deduplicated and numbered, mirroring every inline citation
