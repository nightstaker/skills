---
name: pro-pptx
description: "Use this skill for professional, enterprise-grade PowerPoint work that involves templates, brand compliance, incremental updates, or data-driven charts. Triggers on: creating a PPT from a defined template or style guide; updating an existing PPT without overwriting specific slides (Slide ID locking); converting a PPT to a new template/brand; generating charts or tables from Excel/CSV data; any request that mentions 'brand guidelines', 'color compliance', 'template', 'style guide', or 'corporate PPT'. For basic PPT read/edit tasks without compliance requirements, the base pptx skill is sufficient."
license: Proprietary
---

# Pro-PPTX Skill

A production-grade PowerPoint engineering skill with template governance, incremental update support, style compliance, and data integration.

## Quick Reference

| Scenario | Guide |
|----------|-------|
| **Create** — new PPT from template | [workflows/create.md](workflows/create.md) |
| **Update** — partial update, preserve locked slides | [workflows/update.md](workflows/update.md) |
| **Convert** — migrate PPT to new template | [workflows/convert.md](workflows/convert.md) |
| **Data charts** — Excel/CSV → chart slides | [workflows/data-charts.md](workflows/data-charts.md) |
| **Template authoring** | [templates/README.md](templates/README.md) |

Base PPTX tooling (unpack/pack/thumbnails/validation) lives at `../pptx/` — all those scripts are available here too.

### Render-Time Helpers (USE THESE — they prevent the most common lint errors)

`scripts/helpers.js` provides linter-aligned primitives. Use these instead of raw `addText` / `addShape` / `addTable` to eliminate `card_oversized`, `text_overflow`, `element_overlap`, and `content_zone_breach` errors.

| Function | Purpose | Errors prevented |
|----------|---------|------------------|
| `measureText(str, fs, w)` | Estimate single textbox rendered height | `text_overflow` |
| `measureCell(str, fs, w)` | Estimate table cell rendered height | `element_overlap` (table) |
| `measureTable(rows, colW, fs)` | Total table h × safety multiplier (1.20) | `content_zone_breach` |
| `placeWithGrid({contentBottom})` | Tracker with `canPlace` / `place` for non-overlap layouts | `element_overlap` (general) |
| `safeTable(slide, rows, opts)` | Auto-shrinks fontSize until table fits inside `contentBottom`; respects callout zone | `element_overlap` (callout vs table), `content_zone_breach` |
| `metricCard(slide, opts)` | Card with value/label/sublabel filling its grid slot | `card_oversized` |
| `insightCard(slide, opts)` | Single rich-text card (title bold + body) so linter measures it as one box | `textbox_oversized`, `text_overflow` |

**Import**:
```javascript
const path = require("path");
const H = require(path.resolve(__dirname, "../../scripts/helpers.js"));
// or via env var: const H = require(process.env.PRO_PPTX_DIR + "/scripts/helpers.js");
```

**Constants kept in sync with `scripts/linter.py`**: CJK char width 1.0/72 + ASCII 0.50/72; paragraph line-height 1.4×; table cell line-height 1.6×; textbox inset 0.20"; cell inset 0.16"; table safety 1.20×. Modify both files together when tuning.

Reference example using helpers: [`examples/ai-hw-2035/build.js`](examples/ai-hw-2035/build.js).

---

## Scenario Detection

Before starting, identify the scenario by asking these questions:

1. **Is there an existing PPTX file as input?**
   - No → **Create** workflow
   - Yes → continue

2. **Should the existing file's structure/content be preserved in places?**
   - Yes, specific slides must not change → **Update** workflow (with Slide ID locking)
   - No, full replacement → continue

3. **Is the goal to apply a new visual style/brand?**
   - Yes → **Convert** workflow
   - No, just updating content in existing style → **Update** workflow

4. **Is there external data (Excel/CSV) that needs to become charts?**
   - Yes → **Data Charts** workflow (may combine with Create or Update)

---

## Template Library

Templates live in `templates/`. Each template is a folder with:
- `template.md` — constraints, typography, colors, layout rules, element positions
- `template.pptx` — optional master reference file

Built-in templates:
- `templates/corporate/` — formal enterprise style (dark navy/white, Calibri)
- `templates/minimal/` — clean minimal style (white/gray, light accents)
- `templates/hw-insight/` — Huawei technology insight reports (navy-black/white/red, external-only scope)

User-provided templates: any folder following the same structure.

---

## Core Orchestration Loop

For every task, follow this sequence:

```
1. READ TEMPLATE
   Load template.md → extract color palette, typography, layout rules

2. ANALYZE INPUT (if exists)
   python scripts/style_analyzer.py input.pptx --templates-dir templates/
   → similarity score, best-match template, identified deviations

3. BUILD CONTENT TREE
   python scripts/content_tree.py input.pptx  (or from user's outline)
   → chapter → slide → element hierarchy in JSON

4. CONTENT ENRICHMENT (Content Extender)
   For each slide in the tree:
   a. Logic Densification — if input is brief, supplement with industry background,
      case studies, data projections to meet density targets (≥150 chars, 3–5 points)
   b. Source Extraction — when converting from a report/document, extract the MAXIMUM
      amount of relevant analytical content per slide: additional data points, evidence,
      comparisons, benchmark numbers, architectural details. Every slide should be
      packed with substantive information from the source. If the source is exhausted,
      use WebSearch to find supplementary data (market stats, competitive analysis,
      expert quotes, benchmark details) to enrich the slide.
   c. Visual Trigger — determine the required visual type per slide (chart, table,
      diagram, metric card, radar) based on content; generate an "imagery description"
   d. Layout Saturation — assign layouts that maximize information density;
      prefer "left-visual / right-text" or "multi-column array"; reject >20% blank area.
      Blank area includes background-only fills (INK/Highlight) without text — these
      do NOT count as occupied space. Only real content (text, tables, images) counts.
   e. Smart Overflow — if content exceeds layout capacity, apply "level folding"
      (collapse sub-points into matrix/table) or "extract summary" (key signal +
      evidence tag); NEVER truncate or naively split into half-empty slides

5. IMAGE ACQUISITION (MANDATORY — runs BEFORE rendering)
   For each content slide, search the web for real images matching the slide topic:
   a. Derive 2–3 search queries per slide from topic keywords
   b. Use WebSearch to find candidate images; use WebFetch to download
   c. Save to local directory (e.g., /tmp/pptx_images/)
   d. Map each downloaded image to its target slide
   e. Target: ≥ 60% of content slides should have a real web-sourced image
   f. If template defines an Image-First Visual Rule, this step is NON-NEGOTIABLE
   Self-drawn shapes/charts are FALLBACK ONLY — never skip this step.

6. DRAFT MODE (required before rendering)
   Output Markdown "logic sketch" of the proposed deck:
   - Slide count and titles
   - Layout choice per slide (with rationale)
   - Image source per slide (🖼️ web / 📎 user / 📊 self-drawn fallback)
   - Visual description per slide (what chart/diagram/table will be rendered)
   - Insight callout per slide (the "so what" — if template requires it)
   - Key content per slide
   Ask user to confirm before generating PPTX

7. RENDER (Grid-Aware)
   Use pptxgenjs OR unpack→edit→pack depending on source:
   - No input file → PptxGenJS (read ../pptx/pptxgenjs.md)
   - Input file exists → unpack→edit→pack (read ../pptx/editing.md)
   Apply template constraints strictly
   Embed downloaded images via addImage({ path: ... }) with Alt Text
   CRITICAL — Grid layout enforcement:
   a. Every slide must use a placement tracker (createGrid/canPlace/place)
   b. All elements must fit within the content zone (x: 0.45–9.55, y: 1.00–5.15)
   c. Before placing any element, verify no overlap with previously placed elements
   d. If overlap detected, apply anti-overlap shrink protocol:
      reduce gaps → reduce fonts → reduce heights → fold into denser layout
   e. NEVER allow two shapes to occupy the same pixel area
   f. NEVER let any element extend outside the content zone boundary

8. QA
   python scripts/linter.py output.pptx --template templates/<name>/template.md
   Fix all reported issues before delivering
   Linter now enforces:
   - Content density (≥150 chars per content slide, ≥3 substantive points)
   - Visual mandatory (every content slide must have ≥1 visual element)
   - Visual-text ratio (visuals must occupy ≥40% of content area)
   - Image coverage (≥60% of content slides have real images, if template requires)
   - Font/color/position compliance (unchanged)
```

---

## Template Compliance Rules

When a template defines constraints, they are **non-negotiable**:

- **Colors**: Only use hex values defined in the palette; never introduce new colors
- **Fonts**: Use only the fonts specified in Typography section; fallback order is strict
- **Element positions**: Fixed elements (page numbers, category labels, logos) must be at their exact defined coordinates
- **Layout assignment**: Use the Slide Master Mapping — do not free-style layouts
- **Content density**: Every content slide must have ≥150 characters and 3–5 substantive analytical points (if template defines Content Constraints)
- **Visual mandatory**: Every content slide must include at least one visual element (chart, table, diagram, metric block). Pure-text slides are forbidden
- **Visual-text ratio**: Visual elements must occupy ≥40% of the content area; text must annotate visuals, not stand alone
- **Layout saturation**: No blank area exceeding 20% of content area (including empty space within shapes and areas without shapes); use saturation fill layouts
- **Grid layout**: All content placement must follow the grid-based coordinate system defined in the template; every element must align to grid boundaries within the content zone
- **Zero overlap**: No two shapes may occupy the same pixel area; rendering code must use a placement tracker to verify non-intersection before placing any element
- **Anti-overlap shrink**: When content would cause overlap or exceed content zone boundaries, apply the shrink protocol (reduce gaps → reduce fonts → reduce heights → fold content) — never truncate, never allow overlap

If a user requests something that violates template constraints, inform them explicitly before proceeding.

---

## Similarity Scoring (Parser Module)

When analyzing an existing PPTX:

```bash
python scripts/style_analyzer.py input.pptx --templates-dir templates/
```

| Score | Action |
|-------|--------|
| ≥ 80% match to a known template | Auto-align to that template; report deviations |
| < 80% | Use extracted style as a "temporary template"; preserve original look |
| No templates dir | Always use extracted style |

---

## Slide ID Locking (Update Mode)

When updating an existing deck, users may "lock" specific slides to prevent overwriting:

```bash
# View current slide IDs
python scripts/slide_id_manager.py list input.pptx

# Lock specific slides (by ID)
python scripts/slide_id_manager.py lock input.pptx --ids 256,258,262 --manifest .slide_locks.json

# Check before editing
python scripts/slide_id_manager.py check --id 256 --manifest .slide_locks.json
```

Locked slides must never be modified. If new content would affect a locked slide, split it or add a new slide instead.

---

## QA (Required)

**Never deliver without running the linter:**

```bash
python scripts/linter.py output.pptx --template templates/<name>/template.md
```

Then run visual QA per `../pptx/SKILL.md` (convert to images, inspect with subagent).

Linter checks:
- Font family compliance
- Color value compliance (hex match against palette)
- Fixed-element position drift
- Text overflow (approximate, based on character count vs. font size)
- Alt text presence on images
- **Content density** — flags slides with <150 chars of substantive content
- **Visual mandatory** — flags content slides with no visual elements (charts, tables, shapes, images)
- **Visual-text ratio** — flags slides where visuals occupy <40% of content area
- **Empty/low-info slides** — flags slides that merely list or survey without analytical depth

---

## Dependencies

Inherits all dependencies from `../pptx/SKILL.md`, plus:

```bash
pip install python-pptx openpyxl pandas
```

- `python-pptx` — style extraction, direct element inspection
- `openpyxl` / `pandas` — Excel/CSV data reading for charts
