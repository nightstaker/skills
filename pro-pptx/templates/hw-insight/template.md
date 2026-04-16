# Description

A formal enterprise template designed for Huawei internal technology insight reports — covering external technology trend analysis, industry architecture evolution, benchmark comparisons, patent landscape studies, and standards/ecosystem positioning. Scope is strictly external: all content analyses technologies, architectures, and capabilities across the industry; no assessment of Huawei's own products, internal capabilities, or roadmap is permitted in this template. Visual tone is rigorous and evidence-driven: unified white backgrounds across all slides sustain analytical clarity, with deep navy-black reserved for structural elements (table headers, section labels, metric values) and Huawei red reserved exclusively for the single most critical technical signal per slide. Suitable for Chief Architect technology briefings, 2012 Lab external foresight reports, and cross-domain standards/ecosystem intelligence reviews.

---

# Visual Constraints

## Color Palette

```
Primary:    #1A1A2E   Deep navy-black — table headers, conclusion headlines, metric values, section labels
Secondary:  #FFFFFF   White — all slide backgrounds (cover, content, closing unified)
Accent:     #CF0A2C   Huawei red — single critical technical signal per slide: the key insight callout or the most significant technology shift identified (max 10% visual area)
Text:       #1A1A1A   Near-black — all body text on white backgrounds
Muted:      #6B7280   Medium gray — captions, page numbers, source citations, TRL labels, benchmark metadata
Border:     #E5E7EB   Light gray — table borders, radar grid lines, architecture box outlines
Highlight:  #EFF3FF   Ice blue tint — leading-edge technology zones, emerging architecture fills, high-differentiation quadrant backgrounds (never use for text)
NavyMid:    #2D3A6B   Mid-navy — section bar fills, maturity axis fills, comparison panel headers
Ink:        #F5F6FA   Off-white — secondary card backgrounds, incumbent/baseline fills, alternative architecture blocks
SubText:    #4B5563   Dark gray — L2 bullet text, secondary body text (between Text and Muted)
AlertTint:  #FFF0F0   Light pink tint — So-What callout box background (insight-summary only)
DimGray:    #F0F0F0   Neutral gray — tech-radar Q4 (low maturity + low differentiation) quadrant fill
```

**Color priority rule**: Red > Navy-black > Gray > Blue-tint. Red marks the single most technically significant signal per slide — the architectural shift, the convergence point, or the technology discontinuity that the insight hinges on. Never use red for decorative borders, bullet labels, or secondary emphasis. Blue-tint (Highlight) represents the leading-edge or emerging state; Ink represents the incumbent or baseline. This convention must be applied consistently across all comparison layouts.

## Typography

```
Title (cover):           Microsoft YaHei / Arial, 38pt, #CF0A2C, bold
Slide Title (content):   Microsoft YaHei / Arial, 22pt, #CF0A2C, bold
                         Single-line constraint: titles MUST fit on one line within the title text box.
                         If the title overflows at 22pt, reduce in 1pt steps until it fits (floor: 16pt).
                         After adjusting any slide, scan all other content slides and apply the same
                         reduced size deck-wide so all slide titles share a single uniform font size.
Section Header:          Microsoft YaHei / Arial, 18pt, #1A1A2E, bold
Body:                    Microsoft YaHei / Arial, 13pt, #1A1A1A, regular, line-spacing 1.35×
Bullet L1:               Microsoft YaHei / Arial, 13pt, #1A1A1A, regular
Bullet L2:               Microsoft YaHei / Arial, 11pt, SubText (#4B5563), regular, indent 0.3"
Tech Metric Value:       Microsoft YaHei / Arial, 48pt, #1A1A2E, bold (TRL level, latency, throughput, parameter count, benchmark score)
Tech Metric Label:       Arial, 11pt, #6B7280, regular (metric name + unit + measurement conditions)
Insight Callout:         Arial, 14pt, #CF0A2C, bold (the technical "so what" — one per slide maximum)
Evidence Tag:            Arial, 9pt, #6B7280, regular, italic (source type, year, benchmark version, sample config)
                         PLACEMENT: Slide Notes only (see Evidence Hierarchy section).
Caption / Metadata:      Arial, 9pt, #6B7280, regular, italic
```

Font priority: `Microsoft YaHei / Arial` — use Microsoft YaHei for all CJK content or mixed Chinese-English slides; use Arial as fallback for pure English slides.

**Technology insight narrative rules embedded in type hierarchy:**
- Slide titles must state the technical insight, not the technology name (e.g., "Transformer推理瓶颈已从算力转移至显存带宽，业界HBM方案正在成为主流选择" not "Transformer推理技术分析")
- Body structure follows "技术洞察 → 技术依据/Benchmark → 行业含义" (Tech Insight → Evidence → Industry Implication) — never lead with background survey; never draw implications about Huawei's own products or capabilities
- The red `Insight Callout` text box carries the single technical signal the audience must retain; use at most once per slide
- Never exceed L2 bullets; restructure deeper analysis as a capability matrix, architecture diagram, or TRL radar

## Content Constraints

### ⛔ Image-First Visual Rule (NON-NEGOTIABLE)

**Every content slide MUST attempt to include a real image before falling back to self-drawn visuals.**
This is the single most common compliance failure in this template — do NOT skip it.

The rendering script MUST contain an **Image Acquisition Phase** that runs BEFORE any slide
code is written. This phase searches the web for real images matching each slide's topic and
downloads them to a local directory. The generation code then embeds these images with
`slide.addImage({ path: ... })`, falling back to self-drawn visuals only when no suitable
image was found.

```
Image Source Priority (STRICTLY ORDERED — exhaust each level before falling back):

  Priority 1 — REQUIRED ATTEMPT: Real images from the web
    For EVERY content slide, search for at least one real image BEFORE writing slide code.
    Target sources:
      - Official vendor architecture diagrams (e.g., nvidia.com, microsoft.com/research)
      - Published benchmark result screenshots or heatmaps
      - Academic paper figures (arXiv, conference proceedings)
      - Standards body diagrams (IEEE, IETF, W3C)
      - Open-source project documentation diagrams (GitHub READMEs, official docs)
    Search strategy: use 2–3 keyword variations per slide topic via WebSearch,
    then download the best match via WebFetch to a local directory (e.g., /tmp/pptx_images/).
    Minimum image resolution: 300px on the shorter side.

  Priority 2 — User-supplied images
    Photos, diagrams, or screenshots provided by the user.

  Priority 3 — FALLBACK ONLY: Self-drawn visuals
    Charts (bar/line/pie via PptxGenJS), comparison tables, metric card blocks,
    tech-radar quadrants, architecture block diagrams built from shapes.
    Use ONLY when Priority 1 search returned no suitable result.
    When using fallback, add a code comment: // FALLBACK: no suitable web image found for "<topic>"

Image Embedding Rules:
  - Download to local path and embed via slide.addImage({ path: ... })
  - Every image MUST carry descriptive Alt Text for accessibility
  - Add source attribution in Slide Notes (via slide.addNotes())
  - Avoid watermarked, low-resolution (<300px), or copyrighted-without-license images
  - Prefer official vendor sources over blog reposts
  - Target: ≥ 60% of content slides should contain at least one Priority-1 real image

Image Placement Guidelines:
  - Place images in the primary visual zone of each layout (left column, chart area, panel area)
  - Add a caption below the image: 7.5pt italic Muted, center-aligned, citing source
  - Images should complement — not replace — analytical text and tables
  - Acceptable to combine: real image + self-drawn table on the same slide
```

### Information Density

```
Minimum 150 characters (including annotations) per content slide.
Each slide must present 3–5 substantive analytical points following the
Insight → Evidence → Industry Implication structure.
Slides that merely list or survey without analytical depth must be rejected and reworked.
```

### Visual-Text Ratio

```
Visual elements (charts, tables, diagrams, metric blocks, radar plots, IMAGES) must occupy
≥ 40% of the content area. Body text must provide deep commentary around visuals,
not standalone paragraphs disconnected from the visual evidence.
A real image counts as a visual element and satisfies this requirement.
```

### Layout Saturation

```
Prefer "left-visual / right-text" or "multi-column array" arrangements to maximize
information density. Blank area > 20% of content area is prohibited.

Blank area definition:
  Blank = content zone area MINUS area occupied by substantive elements.
  Substantive elements: text boxes with real analytical text, data tables,
  charts, images, metric cards — elements that convey information.
  NOT substantive: background fills (INK, Highlight, or any solid color
  used purely as decoration without overlaid text), empty shapes, placeholder
  shapes. A shape filled with INK (#F5F6FA) or any background color that
  contains no text is counted as BLANK, not occupied.

How to reduce blank area (priority order):
  1. EXTRACT MORE CONTENT from the source material — if converting from a report,
     pull additional data points, comparisons, evidence, or analysis from the
     original document into the slide. Every slide should contain the MAXIMUM
     amount of relevant analytical content that fits.
  2. ADD DEEPER ANALYSIS — if the source is exhausted, use WebSearch to find
     supplementary data: benchmark numbers, market statistics, competitive
     comparisons, expert quotes, or architectural details that enrich the slide.
  3. EXPAND EXISTING ELEMENTS — make tables wider/taller with more rows/columns,
     add annotation text below charts, add evidence tags beside key claims.
  4. ADD COMPLEMENTARY VISUALS — add a second visual element (comparison table
     alongside an image, metric cards beside a chart).
  NEVER use background-only fills to fake density. NEVER add decorative shapes
  without informational content.

When content overflows, apply "level folding" (collapse sub-points into a matrix or table)
or "extract summary" (distill to key signal + evidence tag) — never truncate or naively split
across slides.
```

## Spacing

```
Slide edge margin:       0.5" (minimum on all sides)
Between content blocks:  0.3"
Title bottom padding:    0.18" (space between slide title and first content block)
Table row height:        0.38" minimum
Matrix cell padding:     0.15" internal padding on all sides

Content–Footer Zero-Gap Rule:
  The content area (including the Insight Callout at the bottom) must extend
  down to the footer zone with NO visible whitespace gap. The Insight Callout
  sits immediately above the footer elements (≤ 0.05" gap to footer top).
  Content blocks above the callout must also pack tightly — expand text boxes
  or add analytical depth rather than leaving blank vertical space.
  Rationale: whitespace between content and footer wastes scarce slide area
  and breaks visual density on information-heavy insight slides.

Table Title Rule:
  Every table (addTable) MUST have a bold, left-aligned title label directly
  above it. The title uses: 8pt bold, fontFace=primary font, color=NavyMid,
  positioned at x equal to the table's x, y = table.y − 0.20", h=0.18".
  The title describes the table's analytical purpose (e.g., "三条融合路径全景对比"),
  not a generic label (e.g., "表1"). Tables without titles fail the linter.
```

## Grid Layout System

All content placement MUST follow a grid-based coordinate system. This ensures content fills the page uniformly and **strictly prevents shape overlap**.

### Grid Definition

```
Slide canvas:     10.0" × 5.625" (LAYOUT_16x9)

Reserved zones (NOT available for content):
  Nav bar:        y = 0.00" – 0.24"  (two-level navigation, top-right)
  Title bar:      y = 0.27" – 0.72"  (slide title + divider line)
  Footer:         y = 5.20" – 5.625" (page number, confidentiality, logo)

Content zone (all content MUST fit within this rectangle):
  x:  0.45" – 9.55"     (width = 9.10")
  y:  0.75" – 5.15"     (height = 4.40")
  This includes all body text, tables, images, charts, metric blocks,
  insight callouts, and any other visual elements.

Insight callout zone (bottom strip of content zone):
  y:  4.83" – 5.15"     (height = 0.32")
  When present, the callout occupies this strip and the main content zone
  shrinks to y = 0.75" – 4.78" (height = 4.03").

Grid unit:
  Column unit = 9.10" / 12 = 0.758"  (12-column grid)
  Row unit    = content zone height / available rows
  Gap between grid cells: 0.10" (horizontal and vertical)
```

### Grid Placement Rules

```
Rule 1 — ALL shapes must align to grid boundaries.
  Every addText, addImage, addShape, addTable, addChart call must have
  (x, y, w, h) values that fall within the content zone and align to
  column/row boundaries. No element may extend outside the content zone.

Rule 2 — ZERO OVERLAP: no two shapes may occupy the same pixel.
  Before placing any element, verify that its bounding box
  [x, y, x+w, y+h] does not intersect with any previously placed element.
  Intersection test: overlap exists if and only if
    (A.x < B.x+B.w) && (A.x+A.w > B.x) && (A.y < B.y+B.h) && (A.y+A.h > B.y)
  If overlap is detected, DO NOT place the element — apply the shrink protocol below.

Rule 3 — Fill the grid: content should expand to use available space.
  After placing all elements, check for unused area > 20% of content zone.
  If too much blank space remains, expand existing elements or add analytical depth.

Rule 4 — Content zone boundary is a hard wall.
  No element's (y + h) may exceed the bottom of the content zone (5.15",
  or 4.78" when insight callout is present). No element's (x + w) may
  exceed 9.55".
```

### Anti-Overlap Shrink Protocol

When content is too dense and elements would overlap or exceed the content zone boundary, apply this protocol **in order** until no overlap exists:

```
Step 1 — Reduce inter-element gap.
  Shrink the gap between vertically stacked elements from 0.10" down to 0.05".
  Re-check overlap.

Step 2 — Reduce font sizes uniformly.
  Reduce ALL body text on the slide by 1pt (minimum floor: 7pt for body, 6pt for tables).
  This shrinks text box heights. Re-check overlap.
  Repeat Step 2 up to 3 times (max reduction: 3pt from baseline).

Step 3 — Reduce element heights proportionally.
  Calculate total overflow = sum of (element bottoms) − content zone bottom.
  Distribute the reduction proportionally across all elements:
    new_h = old_h × (available_height / total_used_height)
  Re-check overlap.

Step 4 — Fold content into denser layouts.
  Convert bullet lists into tables or matrices (level folding).
  Convert two separate text blocks into a two-column layout.
  This is the last resort before splitting to a new slide.

NEVER truncate content. NEVER allow overlap. NEVER exceed the content zone.
```

### Layout Grid Templates

Common grid patterns for each layout type:

```
content (single-zone):
  Full content zone: x=0.45, y=0.75, w=9.10, h=4.03 (with callout)
  Typical split: left 5.0" (image/visual) + right 4.0" (text/table) + 0.10" gap

two-column:
  Column headers: y=0.75, h=0.32
  Left column:    x=0.45, y=1.12, w=4.35, h=3.66 (with callout)
  Right column:   x=4.90, y=1.12, w=4.65, h=3.66 (with callout)
  Column gap:     0.10"

insight-summary:
  So-What box:    x=0.45, y=0.75, w=9.10, h=0.65
  Pillar row:     y=1.50, h=3.28
    Pillar 1:     x=0.45, w=2.90
    Pillar 2:     x=3.55, w=2.90
    Pillar 3:     x=6.65, w=2.90
    Pillar gaps:  0.10"

data (full-width table/chart):
  Table/Chart:    x=0.45, y=0.75, w=9.10, h=4.03 (with callout)

tech-metric (3-block):
  Block 1:        x=0.45, y=0.80, w=2.90, h=3.20
  Block 2:        x=3.45, y=0.80, w=2.90, h=3.20
  Block 3:        x=6.45, y=0.80, w=2.90, h=3.20
  Block gaps:     0.10"
  Callout below:  y=4.10, h=0.32

tech-metric (4-block):
  Block 1:        x=0.45, y=0.80, w=2.15, h=3.20
  Block 2:        x=2.70, y=0.80, w=2.15, h=3.20
  Block 3:        x=4.95, y=0.80, w=2.15, h=3.20
  Block 4:        x=7.20, y=0.80, w=2.15, h=3.20
  Block gaps:     0.10"
```

### Rendering Code Pattern (Anti-Overlap)

The PptxGenJS rendering script MUST use a placement tracker to prevent overlap:

```javascript
// Grid-aware placement tracker — use on EVERY slide
function createGrid() {
  return { placed: [] };
}

function canPlace(grid, x, y, w, h) {
  var contentBottom = 4.78;  // 5.15 if no callout
  if (y + h > contentBottom + 0.01) return false;
  if (x + w > 9.56) return false;
  for (var i = 0; i < grid.placed.length; i++) {
    var p = grid.placed[i];
    if (x < p.x + p.w && x + w > p.x && y < p.y + p.h && y + h > p.y) {
      return false;  // overlap detected
    }
  }
  return true;
}

function place(grid, x, y, w, h) {
  grid.placed.push({ x: x, y: y, w: w, h: h });
}

// Usage pattern:
var g = createGrid();
var x = 0.45, y = 1.00, w = 4.20, h = 2.60;

// Shrink loop: reduce h and font until no overlap and within bounds
var fontSize = 13;
while (!canPlace(g, x, y, w, h) && fontSize >= 7) {
  h *= 0.92;    // shrink height by 8%
  fontSize -= 1;
}
place(g, x, y, w, h);
slide.addText(content, { x: x, y: y, w: w, h: h, fontSize: fontSize, ... });
```

---

# Asset Management

## Logo

```
File:        assets/logo.svg
             SVG intrinsic size: 1200×260 px, viewBox 175.285×38 — aspect ratio W:H = 4.613
             The viewBox is tightly cropped to the actual logo content (flower + HUAWEI text)
             with minimal padding. Do NOT use an SVG with excessive viewBox padding — this
             creates invisible blank space that wastes slide area around the logo.
             Convert to PNG at 2× resolution before embedding into PPTX if needed.

Footer logo: bottom-right, x=8.82", y=5.25", w=1.08", h=0.23"
             (h = w / 4.613 = 1.08 / 4.613 = 0.234" → 0.23")
             Vertically aligned with footer text elements at y=5.25"
             Same slide scope as header logo; anchors the brand in the footer zone
```

If `assets/logo.svg` does not exist, omit both logo placements entirely — never substitute a placeholder.

## Icons

```
Style:    Outline icons, single color matching slide context (Primary on light; Secondary on dark)
Stroke:   1.5pt
Source:   PptxGenJS shape primitives preferred; embed user-supplied SVG converted to PNG as fallback
Size:     0.32" × 0.32" inline; 0.55" × 0.55" standalone icon cards
```

## Images

For sourcing rules, priority order, and embedding requirements, see **Content Constraints > Image-First Visual Rule**. This section covers styling and backgrounds only.

```
Image styling:
  - Scale to fit chart/table area; maintain aspect ratio
  - Caption below: 7.5pt italic Muted, center-aligned, "(Source: <vendor/paper>)"
  - Alt Text: every embedded image MUST carry descriptive Alt Text for accessibility
  - Source attribution: add full citation in Slide Notes (see Evidence Hierarchy)

Backgrounds:
  - Solid fills or two-stop linear gradients (Primary → NavyMid) only
  - Never embed decorative background images

Placeholder (when image search is deferred or fails):
  - Solid fill Border (#E5E7EB) with centered "[ 图片 / Image ]" text in Muted
  - Placeholders MUST be resolved before final delivery
```

---

# Structure & Layout

## Slide Dimensions

Layout: `LAYOUT_16x9` (10" × 5.625")

## Slide Master Mapping

| Content Type | Layout Name | Description |
|---|---|---|
| Cover page | `cover` | White background (same as content); large Accent title + report subtitle in Text color; thin Accent divider line; author/lab/date in Muted |
| Section divider | ~~`section-break`~~ | **DEPRECATED** — replaced by the two-level navigation in Fixed Elements. Do NOT generate standalone section-break slides; section context is conveyed by the persistent top-right nav on every content slide. |
| Tech insight summary | `insight-summary` | White background; "So What" callout box at top in red border; three supporting technical insight pillars below |
| Analytical content | `content` | White background; red slide title; structured body following Insight → Evidence → Industry Implication; optional benchmark/citation inset right |
| Signal vs. implication | `two-column` | White background; red title; left col = observed external signals / benchmark evidence; right col = industry-level technical implications only |
| Key technical metrics | `tech-metric` | White background; red title; 3–4 large metric blocks (TRL, latency, throughput, parameter count, power efficiency) from published external benchmarks; benchmark config footer |
| Industry technology radar | `tech-radar` | White background; red title; 2×2 quadrant mapping the external technology landscape (x = industry maturity, y = technical differentiation potential); technology items as labeled nodes — no Huawei product positioning |
| Architecture comparison | `arch-compare` | White background; red title; two industry/external architecture patterns side by side with annotated trade-off callouts; both panels represent external or published designs only |
| Benchmark / data evidence | `data` | White background; red title; chart or benchmark table sourced entirely from external publications; insight annotation strip above citation footer |
| Technical framing quote | `callout` | White background; large Accent technical framing statement (22pt bold); attribution in Muted below |
| Closing / insight summary | `closing` | White background (same as content); Accent title = "技术洞察总结 / Insight Summary"; numbered conclusions in Primary bold + Muted descriptions; strategic callout bar at bottom |

## Fixed Elements (apply to EVERY content slide)

```
Two-level navigation (top-right, replaces standalone section-break slides):
  Position:  right-aligned, right edge at x=9.95" (flush to slide edge with 0.05" margin)
  Row 1 (sections):  y=0.02", h=0.10" (compact: 5pt text + minimal padding)
  Row 2 (sub-pages): y=0.14", h=0.10" (gap between rows: 0.02")
  Total nav height:   0.24" (y=0.02" to y=0.24")
  Gap between tabs:   0.02" (minimum, fixed)

  Layout algorithm:
    1. Compute each tab's natural width from text:
       - CJK character ≈ 0.07", ASCII character ≈ 0.04", plus 0.10" padding per tab
    2. Sum natural widths + gaps for Row 1
    3. Compute Row 2 natural widths for EVERY section's sub-pages (not just current section)
    4. Global master width = max(Row 1 total, max of ALL Row 2 totals across all sections)
       This ensures the nav block has IDENTICAL width on every slide in the deck.
    5. Scale each row's tab widths proportionally to fill the global master width:
       tabWidth = naturalWidth × (availableTabSpace / sumOfNaturalWidths)
       where availableTabSpace = masterWidth - (tabCount - 1) × 0.02"
    6. Both rows are right-aligned to x=9.95", left edges align exactly

  Active section / active sub-page:
    Fill:  Accent (#CF0A2C)
    Text:  5pt Microsoft YaHei, #FFFFFF, bold, center-aligned

  Inactive section / inactive sub-page:
    Fill:  Border (#E5E7EB)
    Text:  5pt Microsoft YaHei, #1A1A1A, regular, center-aligned

  Row 2 shows only the sub-pages of the current section.
  Cover and closing slides omit the navigation (no section context).
  All other slides — including insight-summary — MUST show the navigation.

Page number:
  Position:  x=0.5", y=5.25", w=1.6", h=0.22"
  Style:     Arial 9pt, Muted (#6B7280), left-aligned
  Content:   "Page {curPageId}/{TotalPageNumber}"  (e.g., "Page 3/12")

Confidentiality label:
  Position:  x=2.2", y=5.25", w=2.8", h=0.22"
  Style:     Arial 9pt, Muted (#6B7280), left-aligned, italic
  Content:   "Huawei Confidential"

Footer logo:
  Source:    assets/logo.svg (see Asset Management — tightly-cropped viewBox)
  Position:  x=8.82", y=5.25", w=1.08", h=0.23"
  Purpose:   Bottom-right brand anchor on all content-type slides

Footer vertical alignment rule:
  All footer elements (Page number, Confidentiality label, Footer logo) share
  the same y=5.25" baseline. All elements have similar height (~0.22"–0.23")
  so they align naturally without vertical-center calculations.
  This compact footer zone maximizes available content area above.
```

**Footer zone layout summary (all elements at y=5.25"):**
```
[Page X/Y]  [Huawei Confidential]  ···············  [Huawei Logo 1.08"×0.23"]
 x=0.5"      x=2.2"                                   x=8.82"
 y=5.25"     y=5.25"                                   y=5.25"
 h=0.22"     h=0.22"                                   h=0.23"
```

**Uniform style rule**: ALL slides — including cover, insight-summary, and closing — MUST include all fixed elements above (page number, confidentiality label, footer logo) and use the same white-background color scheme. The two-level navigation is shown on all slides except cover and closing (which have no section context). This ensures a consistent visual identity across every page of the deck.

## Layout Quick Reference (coordinates in inches, 10" × 5.625" canvas)

**Slide title position note**: ALL layouts share a single unified title position to maximize content area:
- **y=0.27, h=0.40**: uniform across `content`, `insight-summary`, `closing`, `two-column`, `tech-metric`, `tech-radar`, `arch-compare`, `data`, `callout`
- **Divider line**: y=0.70 (immediately below title)
- **Content zone starts**: y=0.75 (only 0.03" gap below nav bottom at y=0.24)
- This compact layout gains ~0.25" of content space compared to the previous split-group approach.

### cover
```
Background:        White (#FFFFFF) — same color scheme as all content slides
Title:             x=0.55, y=1.0,  w=9.0,  h=1.2,   38pt bold Accent (#CF0A2C), left-aligned
Accent divider:    x=0.55, y=2.30, w=3.0,  h=0,     line 2pt Accent (#CF0A2C)
Subtitle:          x=0.55, y=2.50, w=8.0,  h=0.55,  16pt regular Text (#1A1A1A) (technology domain + report issue date)
Author info:       x=0.55, y=3.20, w=6.5,  h=0.30,  10pt regular Muted (Lab/团队 · 作者 · 日期)
Metadata:          x=0.55, y=3.55, w=8.0,  h=0.45,  9pt regular Muted (target audience, keywords)
Page number:       (fixed element — same position as all slides)
Confidentiality:   (fixed element — same position as all slides)
Footer logo:       (fixed element — same position as all slides)
```

### section-break (DEPRECATED — see Slide Master Mapping)

### insight-summary
```
Two-level nav:     (fixed element — top-right, y=0.02"–0.24")
Slide title:       x=0.45, y=0.27, w=9.1,  h=0.40,  22pt bold Accent (#CF0A2C)
Divider line:      x=0.45, y=0.70, w=9.1,  h=0,     border bottom 0.75pt Border (#E5E7EB)
So-What box:       x=0.45, y=0.75, w=9.1,  h=0.65,  fill=AlertTint (#FFF0F0), border=Accent 2pt
  Box text:        x=0.55, y=0.78, w=8.9,  h=0.58,  13pt bold Accent — one-sentence strategic signal
Pillar row (3):
  Pillar 1:        x=0.45, y=1.50, w=2.9,  h=3.35,  fill=Ink (#F5F6FA), border=Border 1pt
  Pillar 2:        x=3.55, y=1.50, w=2.9,  h=3.35,  fill=Ink (#F5F6FA), border=Border 1pt
  Pillar 3:        x=6.65, y=1.50, w=2.9,  h=3.35,  fill=Ink (#F5F6FA), border=Border 1pt
  Per pillar:
    Header:        13pt bold Primary, centered, top 0.3" of cell
    Body:          11pt regular Text, left-aligned
Page number:       (fixed element)
Confidentiality:   (fixed element)
Footer logo:       (fixed element)
```

### content
```
Two-level nav:     (see Fixed Elements — top-right, y=0.02"–0.24")
Slide title:       x=0.45, y=0.27, w=9.1,  h=0.40,  22pt bold Accent (#CF0A2C)
Divider line:      x=0.45, y=0.70, w=9.1,  h=0,     border bottom 0.75pt Border (#E5E7EB)
Content area:      x=0.45, y=0.75, w=9.1,  h=4.37,  13pt regular Text
Page number:       (fixed element — bottom left: "Page X/Y")
Confidentiality:   (fixed element — bottom left, right of page number: "Huawei Confidential")
Footer logo:       (fixed element — bottom right: assets/logo.svg)
```

### two-column
```
Slide title:       x=0.45, y=0.27, w=9.1,  h=0.40,  22pt bold Accent (#CF0A2C)
Divider line:      x=0.45, y=0.70, w=9.1,  h=0,     border bottom 0.75pt Border (#E5E7EB)
Left col header:   x=0.45, y=0.75, w=4.35, h=0.32,  fill=NavyMid, 12pt bold white, centered
Right col header:  x=4.90, y=0.75, w=4.65, h=0.32,  fill=Highlight, 12pt bold Primary, centered
Left column:       x=0.45, y=1.12, w=4.35, h=4.00
Right column:      x=4.90, y=1.12, w=4.65, h=4.00
Column gap:        0.10"
```

### tech-metric
```
Slide title:       x=0.45, y=0.27, w=9.1,  h=0.40,  22pt bold Accent (#CF0A2C)
Divider line:      x=0.45, y=0.70, w=9.1,  h=0,     border bottom 0.75pt Border (#E5E7EB)
Metric blocks (3 or 4):
  3-block:         x=0.45/3.55/6.65, y=0.80,  w=2.9,  h=3.2
  4-block:         x=0.45/2.9/5.35/7.8, y=0.80, w=2.15, h=3.2
  Per block:
    Value:         48pt bold Primary, center-aligned
    Unit/Config:   13pt Muted below value (e.g., "TFLOPS @ FP16", "ms P99 latency")
    Label:         11pt Muted, center-aligned (metric name)
    Border:        1pt Border (#E5E7EB), all sides; fill=Ink (#F5F6FA)
Insight callout:   x=0.45, y=4.35, w=9.1,  h=0.75,  fill=Highlight, border=Accent 1pt
                   13pt bold Accent — one-sentence technical "so what" on these metrics
Benchmark config:  → Slide Notes (see Evidence Hierarchy). Include hardware config, software version, test date.
```

### tech-radar
```
Slide title:       x=0.45, y=0.27, w=9.1,  h=0.40,  22pt bold Accent (#CF0A2C)
Divider line:      x=0.45, y=0.70, w=9.1,  h=0,     border bottom 0.75pt Border (#E5E7EB)
Matrix frame:      x=0.55, y=0.80, w=8.9,  h=4.30
  X-axis label:    center-bottom, 11pt bold Primary (e.g., "行业成熟度 (TRL) →")
  Y-axis label:    center-left rotated 90°, 11pt bold Primary (e.g., "↑ 技术差异化潜力")
Quadrant fills:
  Q1 top-right:    fill=#EFF3FF  (高成熟度 + 高差异化 — 行业激烈竞争区)
  Q2 top-left:     fill=#F5F6FA  (低成熟度 + 高差异化 — 前沿探索区)
  Q3 bottom-right: fill=#F5F6FA  (高成熟度 + 低差异化 — 商品化区)
  Q4 bottom-left:  fill=DimGray (#F0F0F0)  (低成熟度 + 低差异化 — 早期实验区)
Quadrant labels:   10pt bold NavyMid, top-corner of each quadrant
Tech items:        labeled nodes (circle r=0.15") representing external/industry technologies only;
                   fill=Accent for the technology that is the key insight anchor of this slide;
                   fill=NavyMid for actively tracked technologies; fill=Muted for peripheral items
                   CONSTRAINT: No node may represent a Huawei product or internal technology (see External-Scope Constraint)
Source citation:   → Slide Notes (see Evidence Hierarchy).
```

### arch-compare
```
Slide title:       x=0.45, y=0.27, w=9.1,  h=0.40,  22pt bold Accent (#CF0A2C)
Divider line:      x=0.45, y=0.70, w=9.1,  h=0,     border bottom 0.75pt Border (#E5E7EB)
Left arch panel:   x=0.45, y=0.75, w=4.35, h=3.20,  fill=Ink, border=Border 1pt
  Panel label:     12pt bold Primary, top 0.3" of panel, centered (name of Architecture A)
  Diagram area:    x=0.55, y=1.10, w=4.15, h=2.75
Right arch panel:  x=4.90, y=0.75, w=4.65, h=3.20,  fill=Highlight, border=NavyMid 1pt
  Panel label:     12pt bold Primary, top 0.3" of panel, centered (name of Architecture B)
  Diagram area:    x=5.00, y=1.10, w=4.45, h=2.75
Trade-off row:     x=0.45, y=4.05, w=9.1,  h=1.05
  Left note:       11pt italic Muted, below left panel — Architecture A trade-offs / limitations
  Right note:      11pt italic Muted, below right panel — Architecture B trade-offs / strengths
CONSTRAINT: External architectures only (see External-Scope Constraint).
Source citation:   → Slide Notes (see Evidence Hierarchy).
```

### data
```
Slide title:       x=0.45, y=0.28, w=9.1,  h=0.55,  22pt bold Accent (#CF0A2C)
Chart/Table area:  x=0.45, y=1.05, w=9.1,  h=3.95
Insight annotation:x=0.45, y=5.0,  w=9.1,  h=0.28,  fill=Highlight (#EFF3FF); 11pt italic Primary — one-line external insight takeaway
Source citation:   → Slide Notes (see Evidence Hierarchy).
```

### callout
```
Two-level nav:     (fixed element — top-right)
Slide title:       (none — the quote itself is the focal element)
Quote text:        x=0.55, y=1.2,  w=8.9,  h=2.8,   22pt bold Accent (#CF0A2C), center-aligned, valign middle
                   Content: a single technical framing statement that anchors the section's argument
Attribution:       x=0.55, y=4.2,  w=8.9,  h=0.40,  11pt regular Muted, center-aligned
                   Content: speaker/source name, role, date (e.g., "— Jensen Huang, GTC 2025 Keynote")
Accent line:       x=4.5,  y=4.05, w=1.0,  h=0,     line 1.5pt Accent — decorative separator above attribution
Page number:       (fixed element)
Confidentiality:   (fixed element)
Footer logo:       (fixed element)
```

### closing
```
Background:        White (#FFFFFF) — same color scheme as all content slides
Title:             x=0.45, y=0.38, w=9.1,  h=0.50,  22pt bold Accent (#CF0A2C) ("技术洞察总结 / Insight Summary")
Divider line:      x=0.45, y=0.95, w=9.1,  h=0,     border bottom 0.75pt Border (#E5E7EB)
Conclusions list:  x=0.45, y=1.05, w=9.1,  h=3.70,  numbered items: 11pt bold Primary (headline) + 9pt Muted (description)
Strategic callout: x=0.45, y=4.88, w=9.1,  h=0.32,  fill=Highlight, left border Accent 0.04"; 11pt bold Accent — one-sentence strategic signal
Page number:       (fixed element — same position as all slides)
Confidentiality:   (fixed element — same position as all slides)
Footer logo:       (fixed element — same position as all slides)
```

---

# Huawei Technology Insight Communication Principles

## IIR — Insight → Implication → Implication (External Only)
Every slide must advance an insight about the external technology landscape. Technology surveys are pre-work, not slides. The title states the technical insight; the body presents external benchmark or architecture evidence; the red callout box states the industry-level implication.
- ❌ Bad title: "大模型推理加速技术综述"
- ✅ Good title: "推理瓶颈已从算力转移至显存带宽，HBM正在成为业界主流推理加速路径"
- ❌ Forbidden: Any implication framed as "华为应该…" or referencing Huawei products/capabilities

## External-Scope Constraint
This template is strictly limited to external technology intelligence. The following content types are **prohibited**:
- Analysis of Huawei's own products, chipsets, architectures, or software stacks
- Capability gap assessments referencing Huawei as subject
- R&D direction recommendations or planning roadmaps
- Any framing of "Huawei's position" within a technology landscape

## Technology Hypothesis–Driven Structure
The deck is built around a central technical hypothesis stated on slide 2. Each section validates, qualifies, or bounds that hypothesis through external evidence (published benchmarks, architecture papers, patent filings, prototype results). Sections that merely describe a technology without contributing to the hypothesis should be cut.

## TRL Anchoring
Every external technology discussed must carry an explicit TRL (Technology Readiness Level, 1–9) based on publicly available evidence. Use `tech-radar` to make TRL positioning visible across the technology landscape.

## "So What" Discipline
Every content slide has exactly one red `Insight Callout` — the external technical signal the audience must retain. If you cannot state it in one sentence without referencing Huawei, the slide either contains multiple messages or violates scope.

## Evidence Hierarchy

**Placement rule**: All source citations, evidence tags, and benchmark configurations MUST be placed in **Slide Notes** (via `slide.addNotes()`), NOT on the slide face. This keeps the slide surface clean and maximizes content area. Presenters can reference sources from the Notes pane during delivery.

Label all evidence by type so the audience can calibrate confidence:
- `外部Benchmark` — Published third-party benchmark results (cite source, hardware config, date)
- `专利分析` — Patent filing / citation analysis (cite database, search date, scope)
- `学术文献` — Peer-reviewed papers (cite venue, year; note if pre-print)
- `行业报告` — Analyst or standards body reports (cite publisher, date, version)
- `专家判断` — External expert or internal SME assessment of public information (note basis explicitly)

## Confidentiality Classification

Note: The footer's fixed "Huawei Confidential" label (see Fixed Elements) is a **brand identifier**, not a security classification. The per-slide classification below is a **separate** mechanism — when used, add it as a text element near the top-right of the slide or in Slide Notes, not as a replacement for the footer label.

Apply one of three labels to every slide (except cover/closing):
- `内部资料 / Internal Only` — standard Lab/BU circulation
- `秘密 / Secret` — restricted to named technical reviewers
- `机密 / Confidential` — Chief Architect / senior leadership only

---

# Content Generation Rules

## Logic Densification
When user input is brief or skeletal, the generator MUST automatically enrich content by:
- Supplementing with relevant industry background, published case studies, or data projections
- Expanding single-bullet points into the full Insight → Evidence → Implication structure
- Ensuring every slide meets the 150-character minimum and 3–5 analytical points requirement

## Visual Trigger Logic

For each content slide, apply a **two-pass visual strategy**:

### Pass 1 — Image Search (MANDATORY, runs BEFORE code generation)
For every content slide, derive 2–3 search queries from the slide topic and search the web:

| Slide Topic Pattern | Search Query Examples |
|---|---|
| Framework/tool analysis | `"<framework> architecture diagram"`, `"<framework> memory module"` |
| Benchmark comparison | `"<benchmark name> results heatmap"`, `"<model> benchmark screenshot"` |
| Architecture evolution | `"<architecture> vs <architecture> diagram"`, `"<paper title> figure"` |
| Technology landscape | `"<technology> ecosystem overview"`, `"<technology> maturity diagram"` |
| Security/attack surface | `"<attack type> diagram"`, `"LLM security threat model"` |

Download all found images to a local directory. Record which slide each image maps to.
If no suitable image is found after 2–3 query variations, document the failure and proceed to Pass 2.

### Pass 2 — Self-drawn Visual (FALLBACK)
Only when Pass 1 yields no suitable image, generate a concrete "imagery description" (意象描述):
- Benchmark comparison → bar/line chart or table
- Architecture evolution → side-by-side block diagrams (use `arch-compare` layout)
- Technology landscape → quadrant radar (use `tech-radar` layout)
- Key metrics → metric card blocks (use `tech-metric` layout)
- Trend/timeline data → line chart with annotation strip (use `data` layout)

**Combination is encouraged**: a slide can have BOTH a real image AND a self-drawn table/chart.
For example: real architecture diagram on the left + comparison table on the right.

Never leave a content slide without a matching visual element.

## Draft Mode (Collaborative Preview)
Before final PPTX rendering, output a Markdown-format "logic sketch" (逻辑草图) for user confirmation:
- One block per slide: layout type, title, key points, visual description, insight callout
- **Image source column is REQUIRED** — for each slide, specify:
  - 🖼️ `Web image: <search query>` — will search and download a real image (Priority 1)
  - 📎 `User image: <filename>` — user-provided image (Priority 2)
  - 📊 `Self-drawn: <chart/table/diagram type>` — fallback only (Priority 3)
- At least 60% of content slides should be planned with a Priority-1 web image
- User confirms or revises before file generation proceeds
- This prevents wasted rendering cycles on misaligned content

Draft table must include this column:

```
| # | Title | Layout | Image Source | Visual Element | Insight Callout |
```

---

# Quality Assurance Rules

## Density Check
Automatically reject and flag slides that violate:
- < 150 characters of substantive content (excluding titles, labels, metadata)
- < 40% visual-to-content-area ratio
- Missing Insight Callout (red "so what" statement)
- Missing evidence type label on any cited data

Flagged slides must be reworked with additional analytical depth or visual components before rendering.

## Image Coverage Check (NEW — addresses the most common compliance failure)
After rendering, verify:
- **Minimum**: ≥ 60% of content slides (excluding cover, insight-summary, closing) contain at least one `addImage()` call with a real downloaded image (not a logo or icon)
- **Each image has**: Alt Text, source caption below the image, full citation in Slide Notes
- **No unresolved placeholders**: if any slide still has "[ 图片 / Image ]" placeholder fills, the deck FAILS QA
- If the 60% threshold is not met, go back to Image Search (Visual Trigger Logic Pass 1) and fill gaps before delivery

## Style & Compliance Check
- Font consistency: all text must use the declared Typography hierarchy — no ad-hoc sizes or colors
- Title coordinate stability: each slide's title must match its **layout-specific** declared (x, y) from Layout Quick Reference; no ad-hoc drift within the same layout type
- Alt Text: every embedded image or chart must carry descriptive `Alt Text` for accessibility
- Editability: all text boxes and shape elements must remain editable in PowerPoint/Keynote — no rasterized text

## Overflow Strategy
When content exceeds the available layout area:
1. **Level folding** — collapse L2 bullets into a comparison matrix or summary table
2. **Extract summary** — distill to key signal + supporting evidence tag, move full analysis to appendix slide
3. **Never** truncate mid-sentence, delete analytical points, or naively split one slide into two half-empty slides