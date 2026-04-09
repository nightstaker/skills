# Workflow: Type B — Future Trend Insight (Closed-Loop)

Use this workflow when the user asks where a technology, scenario, or product category is headed in the next 1–3 years. Goal: a five-stage chain that starts from a perceivable scene, peels back vendor moves and key technologies, predicts the future product form, and closes with a Tech → Product → Customer/Scene → Commercial Value loop.

**Reader profile** (see [../REQUIREMENT.MD](../REQUIREMENT.MD) §1.3): senior domain experts + domain investors. Every stage must reach expert-level depth (named architectural primitives, specific foundry variants, full benchmark methodology, patent numbers) and investor-level actionability (unit economics, customer concentration, capacity constraints, regulatory exposure).

Read [../REQUIREMENT.MD](../REQUIREMENT.MD) §2.2 before starting. Output template: [../templates/type-b-trend.md](../templates/type-b-trend.md).

The five stages are non-negotiable. Skipping any of them turns the report into vibes. The Investor Appendix (§2.4) is additionally mandatory.

---

## Stage 1 — Scene Anchor

Open with a scene the user / customer can directly perceive, not a technology buzzword. Good vs bad:

- ✅ "在会议室里实时生成会议纪要并分发给每位与会者的智能麦克风阵列"
- ❌ "基于 Transformer 的多模态大模型在企业协作场景的渗透"

The scene must be:

- **Concrete**: a specific moment, room, or task — something you could film.
- **Verifiable**: at least one real product or pilot deployment exists today and can be cited.
- **Narrow enough**: if the scene fits 5+ unrelated industries, it's a category, not a scene. Split it.

Embed at least one **scene photo** from a primary source (vendor demo video frame, official press kit, customer case study) at the top of this section. Caption it.

---

## Stage 2 — Vendor Landscape

Inventory ≥3 leading vendors' public moves in the last 6–12 months. For each move, capture:

- Vendor / move type (product launch, patent filing, acquisition, org change) / date / source URL.
- One sentence on why this move matters for the scene.

Use `WebSearch` and `WebFetch`. Sources must be reachable; if a Chinese-language press release has no English equivalent, cite the Chinese URL — do not fabricate translations of quotes.

Embed **at least one representative product photo per major vendor** from the vendor's official channel. Caption every image with source.

If only one or two vendors are doing anything visible, the scene is too early — flag this to the user before continuing. Do not invent vendor activity.

---

## Stage 3 — Key Technology Decomposition (Six-Tuple Depth)

Identify 2–4 key technologies that gate this scene's evolution. For each, you MUST fill the following **six-tuple**:

1. **Principle** — one paragraph, technically precise. Name the architectural primitive(s), list the key design constants, state the critical trade-off.
2. **TRL** (Technology Readiness Level 1–9) with a one-line justification anchored in public evidence.
3. **Concrete bottleneck** — must be quantified (e.g., "KV cache memory footprint grows linearly with seqlen; at 64K ctx occupies 58% of card HBM").
4. **Breakthrough vector** — named candidate approach(es) + ≥1 representative paper or patent.
5. **Latest public benchmark** with the full six-tuple methodology (hardware / software / model / batch / seqlen / precision + test party + date).
6. **Patent wall** — ≥1 patent number (`US\d{7,}` / `CN\d{9,}` / `EP\d{7,}` / `WO\d{4}/\d{6,}`) or ≥1 representative paper, with a one-sentence claim summary.

Embed **at least one principle / architecture diagram** per key technology. Diagrams must come from the original paper figure, official whitepaper, or patent figure. Re-drawn diagrams are forbidden unless the original is unreadable, in which case credit the original beneath the redraw.

---

## Stage 4 — Trend Prediction

Predict, on the evidence built in stages 1–3:

- **Future product form**: shape, interaction model, deployment topology.
- **Time window**: 12 / 24 / 36 months — pick one and commit.
- **Core assumptions** (≤5): list each as a bullet.
- **Falsifiability conditions**: for each assumption, what observable event would prove it wrong.
- **Cost of being wrong**: if the prediction is falsified, what is the supply-chain rebuild / R&D pivot / order break cost for our side.

A prediction with no falsifiability condition is not a prediction — it's a horoscope. A prediction without a cost-of-being-wrong is not an actionable investment signal. The linter will reject both.

---

## Stage 5 — Closed Loop (Tech → Product → Customer/Scene → Commercial Value)

Render the four nodes as a table:

| Node | Content | Key assumptions |
|---|---|---|
| Tech | What technical capability becomes available | … |
| Product | What product form ships first | … |
| Customer / Scene | Who buys it and why | … |
| Commercial Value | TAM / SAM / SOM / ARPU / penetration curve, with at least one quantified anchor and source | … |

The commercial node must contain a **quantified** value (market size, ARPU, displaced cost, penetration target). "Big market" is not a number.

---

## Implication

Close with a "So what?" — what should the reader do this quarter / this year. Forbidden phrases: "需要持续关注", "值得观察", "未来可期", "业界领先", "先进架构", "生态完善", "industry-leading", "best-in-class", "revolutionary", "cutting-edge". Concrete moves only.

---

## Mandatory — Investor Appendix (§2.4)

Every Type B report must ship an investor-grade appendix covering the four sub-blocks (unit economics, customer concentration, capacity & supply, regulatory & geopolitical). Empty sub-blocks must carry an explicit "无公开披露 — 原因：…" justification. See [existing-tech-top5.md](existing-tech-top5.md#step-85--investor-appendix-mandatory-for-every-report) for the full spec — Type B reports follow the same structure.

---

## QA Gate

```bash
python scripts/linter.py reports/<slug>.md --assets assets/<slug>/ --type B
```

The linter rejects the report if:

- Any of the 5 stages is missing, or the Investor Appendix is missing.
- The Closed Loop has fewer than 4 nodes, or the commercial node has no quantified value.
- Any prediction lacks an explicit falsifiability condition.
- Key Technology Decomposition is missing benchmark methodology keywords (`batch` / `seqlen` / `precision` / `FP8–INT8` / `测试条件`).
- Any banned shallow phrase (业界领先 / 先进架构 / 生态完善 / industry-leading …) appears anywhere.
- Bare process node numbers (`3nm` / `5nm` / `7nm`) appear without a foundry variant (TSMC N3E / Samsung SF4X / Intel 18A).
- No patent number is cited in the key technology section.
- Required images (scene, vendor product, key tech principle) are missing or uncaptioned.
- Any factual sentence is not inline-sourced.
- Investor Appendix is missing any of the four sub-block keyword families.
- The Implication contains filler phrases.

Fix every failure before delivery. Never `--ignore` linter warnings.

---

## Deliverable

- `reports/<slug>.md` — the report
- `assets/<slug>/` — scene photo, vendor product photos, key tech principle diagrams + `image_manifest.json`
- Numbered "Sources" section at the end of the report
