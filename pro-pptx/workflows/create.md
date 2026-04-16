# Workflow: Create New PPT from Template

Use this workflow when creating a presentation from scratch with no existing PPTX input.

---

## Prerequisites

- A template selected from `templates/` (or a user-provided template folder)
- Content outline from the user (text, sections, key points)
- Optional: data files for chart slides

---

## Step 1 — Load Template

Read the template definition:

```bash
cat templates/<name>/template.md
```

Extract and internalize:
- **Color palette** with hex values and usage weights
- **Typography**: font faces, sizes, and colors for each level (title, header, body, caption)
- **Fixed elements**: exact coordinates (x, y, w, h in inches) for page numbers, category labels, logos
- **Slide Master Mapping**: which content types map to which layouts
- **Visual motif**: the recurring design element (border style, icon treatment, etc.)

---

## Step 2 — Build Content Tree

Transform the user's input into a structured hierarchy:

```bash
# If user provided a rough outline, build tree interactively
# Output format (JSON, also printed as Markdown):
{
  "title": "Deck Title",
  "sections": [
    {
      "id": 1,
      "title": "Section Name",
      "slides": [
        {
          "title": "Slide Title",
          "layout": "two-column",  // from Slide Master Mapping
          "content": { ... }
        }
      ]
    }
  ]
}
```

Layout assignment rules (from template's Slide Master Mapping):
- **Title/cover**: use `cover` layout
- **Section divider**: use `section-break` layout
- **Key stats / metrics**: use `stat-callout` / `tech-metric` layout
- **Detailed explanation**: use `content` layout
- **Comparison / two topics**: use `two-column` layout
- **Image + caption**: use `image-focus` layout
- **Data table or chart**: use `data` layout
- **Architecture comparison**: use `arch-compare` layout (if template supports it)
- **Technology landscape**: use `tech-radar` layout (if template supports it)
- **Insight summary**: use `insight-summary` layout (if template supports it)
- **Quote / framing statement**: use `callout` layout
- **Closing / thank you**: use `closing` layout

### Content Enrichment (after tree construction)

For each content slide, apply the Content Extender logic:

1. **Logic Densification**: If the user's input is brief (< 150 characters or < 3 points), automatically enrich with:
   - Industry background and context relevant to the topic
   - Published case studies, benchmark data, or data projections
   - Expand single bullets into the full narrative structure required by the template (e.g., Insight → Evidence → Implication)

2. **Visual Trigger**: For each slide, determine the required visual element:
   - Benchmark comparison → bar/line chart or comparison table
   - Architecture discussion → side-by-side block diagrams
   - Technology landscape → quadrant radar or matrix
   - Key metrics → metric card blocks with large numbers
   - Trend/timeline → line chart with annotation strip
   - Generate a concrete "imagery description" (意象描述) that specifies exactly what visual will be rendered

3. **Layout Saturation**: Assign layouts that maximize information density:
   - Prefer "left-visual / right-text" or "multi-column array" arrangements
   - Blank area exceeding 20% of content area is prohibited (including empty space within shapes and shapeless areas)
   - Every content slide MUST include at least one visual element — no pure-text slides

### Overflow Strategy

When content exceeds layout capacity:
1. **Level folding** — collapse sub-points into a comparison matrix, summary table, or structured grid
2. **Extract summary** — distill to key signal + supporting evidence tag; move detailed analysis to an appendix slide
3. **Never** truncate mid-sentence, delete analytical points, or naively split one slide into two half-empty slides

**Density floor**: Every content slide must have ≥ 150 characters (including annotations) and 3–5 substantive points.

---

## Step 3 — Draft Mode (REQUIRED)

Before writing any code, output a Markdown draft for user confirmation:

```markdown
## Deck Draft: [Title]
**Template**: corporate
**Slides**: 12

| # | Title | Layout | Image Source | Visual Element | Insight/Callout |
|---|-------|--------|-------------|---------------|-----------------|
| 1 | Cover | cover | — | — | — |
| 2 | Agenda | content | 🖼️ Web: "topic overview diagram" | Section icon cards | — |
| 3 | Section 1: [Name] | section-break | — | — | Framing question |
| 4 | [Slide Title] | two-column | 🖼️ Web: "benchmark comparison" | Comparison table | "Key signal..." |
| 5 | [Slide Title] | tech-metric | 📊 Self-drawn (metric cards) | 3 metric blocks | "So what..." |
...

**⚠️ Layout decisions to confirm:**
- Slide 4: chose two-column because there are 3 bullet points + 1 stat → confirm?
- Slide 5: enriched from 2 metrics to 3 with industry benchmark data → confirm?
- Slide 7: content overflow handled via level-folding into matrix → confirm?

**🖼️ Image coverage: 8/12 content slides planned with web images (67% ≥ 60% target ✅)**

**📊 Content enrichment applied:**
- Slide 4: added industry benchmark data (user provided only bullet points)
- Slide 6: generated comparison table from user's narrative description
```

**Wait for user approval before proceeding to Step 3.5.**

If the user requests changes, update the tree and re-show the draft.

---

## Step 3.5 — Image Acquisition (MANDATORY)

**This step runs AFTER draft approval and BEFORE rendering. Do NOT skip it.**

For each content slide in the approved draft, search the web for real images:

```bash
mkdir -p /tmp/pptx_images
```

1. **Derive search queries** from each slide's topic (2–3 variations per slide)
2. **Search & download** using WebSearch + WebFetch
3. **Map images to slides** — record which image goes to which slide
4. **Minimum coverage target**: ≥ 60% of content slides should have a real web image

If the template defines an **Image-First Visual Rule**, this step is non-negotiable.

### Search Query Strategy

| Slide Type | Query Pattern |
|---|---|
| Architecture analysis | `"<technology> architecture diagram"`, `"<paper/project> figure"` |
| Benchmark/data | `"<benchmark name> results"`, `"<model> evaluation heatmap"` |
| Framework comparison | `"<framework> architecture overview"`, `"<framework> memory module diagram"` |
| Technology landscape | `"<technology> ecosystem"`, `"<field> maturity model"` |
| Security/threat | `"<attack type> threat model"`, `"<defense> architecture"` |

### Image Quality Filters
- Minimum resolution: 300px on shorter side
- No watermarks or heavy copyright restrictions
- Prefer official vendor sources, academic paper figures, open-source project docs
- Download to `/tmp/pptx_images/<descriptive_name>.png`

### Embed in Code
```javascript
// Priority 1: Real image (always prefer)
if (fs.existsSync(imagePath)) {
  slide.addImage({ path: imagePath, x: ..., y: ..., w: ..., h: ...,
    altText: "Descriptive text for accessibility" });
  slide.addText("Source caption", { fontSize: 7.5, italic: true, color: MUTED });
}
// Priority 3: Fallback to self-drawn shapes
else {
  // FALLBACK: no suitable web image found for "<topic>"
  slide.addShape(...);
}
```

---

## Step 4 — Render with PptxGenJS

Use PptxGenJS for all new-from-scratch decks. Read `../pptx/pptxgenjs.md` for the full API reference.

### Setup

```bash
npm install pptxgenjs
```

### Template-Governed Rendering Rules

**Colors**: Use ONLY the hex values from template.md. Never introduce new colors.

```javascript
// Example: corporate template colors
const COLORS = {
  primary: "1A2B5F",    // deep navy
  secondary: "FFFFFF",  // white
  accent: "C8102E",     // red
  text: "1A1A1A",       // near-black
  muted: "6B7280",      // gray
};
```

**Typography**: Use font faces in priority order from template.md.

```javascript
const FONTS = {
  heading: "Microsoft YaHei",   // priority 1
  body: "Arial",                 // priority 2
};
const SIZES = {
  title: 40, sectionHeader: 28, bodyLarge: 16, body: 14, caption: 11
};
```

**Fixed elements** (add to EVERY slide using a helper function):

```javascript
function addFixedElements(slide, sectionName, pageNum) {
  // Category label (top-right, per template spec)
  slide.addText(sectionName, {
    x: 8.5, y: 0.15, w: 1.3, h: 0.25,
    fontSize: SIZES.caption, fontFace: FONTS.body,
    color: COLORS.muted, align: "right"
  });
  // Page number (bottom-right)
  slide.addText(String(pageNum), {
    x: 9.3, y: 5.2, w: 0.5, h: 0.25,
    fontSize: SIZES.caption, fontFace: FONTS.body,
    color: COLORS.muted, align: "center"
  });
}
```

**Visual mandatory**: Every content slide must include at least one visual element — chart, table, diagram, metric block, or structured shape. Pure-text slides are forbidden. If no user-supplied image exists, generate a structured visual (table, comparison matrix, or metric card) from the content itself.

**Visual-text ratio**: Visual elements must occupy ≥ 40% of the content area. Body text must provide deep commentary around visuals, not standalone paragraphs.

**Overflow handling**: When content exceeds layout capacity, apply level-folding (collapse sub-points into matrix/table) or extract-summary (key signal + evidence tag). Never truncate or naively split into half-empty slides.

**Density floor**: Every content slide must have ≥ 150 characters of substantive content and 3–5 analytical points.

### Grid-Aware Rendering (MANDATORY)

All content placement MUST use the grid layout system and anti-overlap placement tracker defined in the template's "Grid Layout System" section.

**Content zone** (all elements must fit within):
- x: 0.45" – 9.55" (width = 9.10")
- y: 1.00" – 5.15" (or 4.78" when insight callout is present)

**Placement tracker** — include in EVERY rendering script:

```javascript
// Grid-aware placement tracker — prevents overlap
function createGrid() { return { placed: [] }; }

function canPlace(grid, x, y, w, h, contentBottom) {
  contentBottom = contentBottom || 5.15;
  if (y + h > contentBottom + 0.01) return false;
  if (x + w > 9.56) return false;
  if (x < 0.44) return false;
  if (y < 0.99) return false;
  for (var i = 0; i < grid.placed.length; i++) {
    var p = grid.placed[i];
    if (x < p.x + p.w && x + w > p.x && y < p.y + p.h && y + h > p.y) return false;
  }
  return true;
}

function place(grid, x, y, w, h) {
  grid.placed.push({ x: x, y: y, w: w, h: h });
}
```

**Anti-overlap shrink loop** — apply when elements would overlap:

```javascript
// Before placing any element, verify and shrink if needed
var g = createGrid();
var fontSize = 13;
var gap = 0.10;
var x = 0.45, y = 1.00, w = 4.20, h = 2.60;

// Step 1: try reducing gap
while (!canPlace(g, x, y, w, h) && gap >= 0.05) {
  y -= 0.02; h -= 0.02; gap -= 0.02;
}
// Step 2: reduce font + height
while (!canPlace(g, x, y, w, h) && fontSize >= 7) {
  h *= 0.92;
  fontSize -= 1;
}
// Step 3: proportional height reduction (last resort)
if (!canPlace(g, x, y, w, h)) {
  var maxH = (contentBottom - y);
  if (maxH > 0) h = maxH;
}

place(g, x, y, w, h);
slide.addText(content, { x: x, y: y, w: w, h: h, fontSize: fontSize, ... });
```

**Rules**:
1. Create a fresh grid (`createGrid()`) for each slide
2. Register EVERY element via `place()` after adding it
3. Check EVERY element via `canPlace()` before adding it
4. Apply the shrink loop for any element that fails `canPlace()`
5. NEVER allow two shapes to overlap — this is a hard failure

### Script Structure

```javascript
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "Deck Title";

// --- Grid helpers (see above) ---

// --- Slide 1: Cover ---
const slide1 = pres.addSlide();
var g1 = createGrid();
// ... place elements with canPlace/place checks ...
addFixedElements(slide1, "Cover", 1);

// --- Continue for each slide (always with grid tracker) ---

pres.writeFile({ fileName: "output.pptx" });
```

---

## Step 5 — QA

```bash
# Content check
python -m markitdown output.pptx

# Linter (compliance + overflow check)
python scripts/linter.py output.pptx --template templates/<name>/template.md

# Visual QA
python ../pptx/scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide

# Inspect with subagent
```

Fix all linter errors. Run at least one visual QA cycle before delivery.

---

## Common Mistakes to Avoid

- **Never free-style colors** — even "close" shades that aren't in the palette violate compliance
- **Never skip fixed elements** on any slide (page numbers, category labels)
- **Never create text-only slides** — every content slide needs a visual (chart, table, diagram, metric card)
- **Never mix font faces** not in the template's Typography section
- **Never leave blank space** — use saturation fill layouts; >20% unused content area is prohibited (including within-shape empty space)
- **Never truncate or naively split** overflowing content — use level-folding or extract-summary instead
- **Never deliver sparse slides** — minimum 150 chars and 3–5 analytical points per content slide
- **Always generate Alt Text** for every embedded image and chart (accessibility compliance)
- **Consistent spacing**: use the template's defined margins (usually 0.5" edge margin, 0.3–0.5" between blocks)
- **Never allow shape overlap** — use the placement tracker (createGrid/canPlace/place) on every slide; if elements overlap, apply the anti-overlap shrink protocol (reduce gaps → reduce fonts → reduce heights → fold content)
- **Never exceed the content zone** — all elements must stay within x=0.45–9.55", y=1.00–5.15" (or 4.78" with callout); elements outside this zone collide with nav bars, titles, or footers
