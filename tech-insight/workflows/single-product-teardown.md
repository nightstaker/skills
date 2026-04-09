# Workflow: Type C — Single-Product Deep Teardown

Use this workflow when the user asks for a deep-dive technical decomposition of a single product or single technology, rather than a horizontal benchmark (Type A) or a future trend (Type B). Typical triggers:

- "把 <product> 的架构拆开讲清楚"
- "帮我出一份 <chip/device> 的 teardown"
- "<technology> 到底是怎么实现的，有哪些壁垒"

**Reader profile** (see [../REQUIREMENT.MD](../REQUIREMENT.MD) §1.3): senior domain experts (Chief Architect / Fellow / tech DD leads) + domain investors (PE tech DD / VC partners). The report must reach microarchitectural-primitive depth, cite specific foundry node variants, ship full benchmark methodology, back every moat claim with a patent number or SEC filing, and close with an investor-grade appendix.

The report must be evidence-driven and visually anchored — no marketing summaries, no rewritten press releases. Read [../REQUIREMENT.MD](../REQUIREMENT.MD) §§1.3–1.4 and §2.3–2.4 for the full depth rules. Output template: [../templates/type-c-teardown.md](../templates/type-c-teardown.md).

---

## When NOT to use Type C

- "我想知道这个品类里谁最强" → Type A (horizontal benchmark)
- "这个方向未来三年会怎么走" → Type B (future trend)
- "只想查一下 <product> 的某个参数" → use a plain web search, this skill is overkill
- When you have fewer than 3 primary-source documents on the target product, stop: either find more sources or tell the user the target is too obscure for a teardown.

---

## Stage 1 — Product Profile

Lock down these facts before drilling in. Every row carries an inline source.

- Vendor, product name, product line, latest version, release date
- Target customer, price / price band, deployment form factor
- Headline claim (what the vendor says makes it different)
- Public traction signal (shipments / install base / design wins / benchmark rank)

Embed a primary-source **hero product photo** at the end of this section:
`assets/<slug>/hero.jpg` — from the vendor press kit, official product page, or regulatory filing.

---

## Stage 2 — Architecture Decomposition

Do not stop at the block-diagram level. Drill into:

- **Compute / logic organization**: which engine, how many cores/SMs/tiles, what hierarchy
- **Memory subsystem**: capacity, bandwidth, hierarchy, cache sizes
- **Interconnect / I/O**: what buses, what protocols, what topology
- **Software stack**: compiler / runtime / driver / SDK layers, open vs proprietary
- **Packaging / integration**: chiplet, 2.5D/3D, CoWoS, advanced packaging

Each sub-block must cite an official whitepaper, academic paper, patent figure, or a credible teardown (TechInsights / ChipRebel / SemiAnalysis / AnandTech / ServeTheHome).

Embed **≥2 architecture visuals**:
- `assets/<slug>/arch-overview.png` — block diagram or die shot
- `assets/<slug>/arch-detail.png` — one detailed sub-system diagram (memory, interconnect, compute engine, packaging cross-section)

When the vendor has published multiple block diagrams at different abstraction levels, prefer the most detailed one available.

---

## Stage 3 — Key Technical Metrics

Produce a quantitative fact sheet. Do not rewrite the marketing datasheet — extract the measurable engineering numbers and annotate their testing condition:

| Metric | Value | Measurement condition | Source |
|---|---|---|---|
| Process node | … | — | [src](URL) |
| Peak performance | … | e.g., FP8 dense, batch 1 | [src](URL) |
| Memory capacity / bandwidth | … | — | [src](URL) |
| Power / TDP | … | typical / peak | [src](URL) |
| Latency / throughput | … | workload, batch size | [src](URL) |
| Area / die size | … | — | [src](URL) |

Every cell that asserts a number must carry an inline link. Mark any vendor-reported number without an independent benchmark as "厂商宣称" inside the cell.

Compare each metric against its strongest public alternative (one single competitor suffices — do not pad into a mini Type A). State the delta explicitly.

---

## Stage 4 — Moat Analysis

Identify where the defensibility comes from, and rate its reproducibility:

- **Patent moat**: cite at least 2 relevant filings (patent: or https links)
- **Process / fab moat**: node availability, CoWoS allocation, HBM supply deals
- **Ecosystem moat**: frameworks supported out-of-box, partner lock-in, developer base size (with source)
- **Data / learning loop moat**: if any, explain the flywheel
- **Talent / organization moat**: only if cited in public reporting — do not speculate

For each moat axis, answer: **can a well-funded follower replicate this in 24 months?** — with a yes/no and one-sentence rationale (sourced).

---

## Stage 5 — Weakness / Risk Analysis

Explicit failure modes the teardown exposes. Each item must be grounded in public evidence (benchmark, review, filing, patent):

- **Engineering weakness** — the metric where it underperforms the strongest alternative
- **Supply-chain risk** — exposure to a single fab, a single HBM vendor, a single substrate house
- **Roadmap risk** — public signals that the next version is delayed / descoped
- **Ecosystem risk** — customer concentration, open-source alternatives catching up
- **Regulatory risk** — export control, antitrust, safety certification exposure

Do NOT invent risks. If a risk category has no public evidence, write "无公开证据" and move on.

---

## Stage 6 — Implication (So what?)

Close the report with a concrete reader-facing action set. Forbidden phrases: "需要持续关注", "值得观察", "未来可期", "业界领先", "先进架构", "生态完善", "industry-leading", "best-in-class", "revolutionary", "cutting-edge". Concrete moves only.

- Which engineering choice from this product is worth directly copying / licensing?
- Which weakness creates a viable differentiation opening for our side?
- What contract / supply / talent action should we take this quarter to respond?

---

## Stage 7 — Investor Appendix (MANDATORY)

Every Type C teardown must ship an investor-grade appendix (four sub-blocks, see [../REQUIREMENT.MD](../REQUIREMENT.MD) §2.4):

- **Unit economics** — ASP, BoM / wafer cost estimate, gross margin, CapEx intensity
- **Customer concentration** — top-3 customer share, named design wins, switching cost
- **Capacity & supply** — front-end (foundry wafer starts), back-end (CoWoS / FOPLP), HBM / substrate allocations, 24-month bottleneck
- **Regulatory & geopolitical** — specific rule citations (15 CFR 744 / BIS ECCN / EAR / CFIUS / SAMR), regional market access, geopolitical exposure

Empty sub-blocks must carry an explicit "**无公开披露 — 原因：…**" justification. Do NOT leave blank.

---

## QA Gate

```bash
python scripts/linter.py reports/<slug>.md --assets assets/<slug>/ --type C
```

The linter rejects the report if:

- Any of the seven required sections is missing, or the Investor Appendix is missing.
- Product hero photo, architecture diagram, or die-shot / PCB / internal image is missing or uncaptioned.
- Any factual sentence or Key Technical Metrics cell lacks an inline source.
- Any banned shallow phrase (业界领先 / 先进架构 / 生态完善 / industry-leading …) appears anywhere.
- Bare process node numbers (`3nm` / `5nm` / `7nm`) appear without a foundry variant (TSMC N3E / Samsung SF4X / Intel 18A).
- Key Technical Metrics section misses benchmark methodology keywords (`batch` / `seqlen` / `precision` / `FP8–INT8` / `测试条件`).
- Moat / 壁垒 section is missing a patent number or SEC / HKEX filing reference.
- Investor Appendix is missing any of the four sub-block keyword families.
- The Implication contains banned filler phrases.
- Any asset file has no `image_manifest.json` entry, or vice versa.

Fix every failure before delivery. Never silence warnings.

---

## Deliverable

- `reports/<slug>.md` — the teardown
- `assets/<slug>/` — hero photo, architecture diagrams, die shot / PCB / internal images + `image_manifest.json`
- Numbered "Sources" section at the end of the report
