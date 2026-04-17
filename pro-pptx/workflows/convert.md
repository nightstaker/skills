# Workflow: Convert PPT to a New Template

Use this workflow when migrating an existing presentation's **content** into a different visual style — for example, rebranding, switching from an old company template to a new one, or adapting a personal deck to a corporate standard.

The goal is **lossless content migration**: all text, data, and logical structure must survive; only the visual style changes.

---

## Core Principle: Content–Style Separation

Conversion is a two-phase process:

1. **Extract** — pull all content from the source PPTX into a template-agnostic structure
2. **Rebuild** — render that structure using the target template's rules

Never attempt to directly patch the source file's XML to match the target style — that path leads to broken layouts and half-migrated formatting.

---

## Step 1 — Analyze Source

```bash
# Text content
python -m markitdown source.pptx

# Visual layout analysis
python ../pptx/scripts/thumbnail.py source.pptx --cols 4

# Style profile
python scripts/style_analyzer.py source.pptx --templates-dir templates/
```

Note:
- Total slide count
- Section structure
- Slide types present (title, content, two-column, data, image, etc.)
- Embedded images or charts (these require special handling)

---

## Step 2 — Load Target Template

```bash
cat templates/<target-name>/template.md
```

Map source layout types to target layout types:

| Source layout type | Target layout name (from template.md) |
|-------------------|--------------------------------------|
| Cover / Title page | `cover` |
| Section divider    | `section-break` |
| Bullet list        | `content` |
| Two-column         | `two-column` |
| Full-image         | `image-focus` |
| Chart / data table | `data` |
| Quote / callout    | `callout` |
| Closing / end      | `closing` |

---

## Step 3 — Build Content Tree

```bash
python scripts/content_tree.py source.pptx --output content.json
```

The output captures content independently of visual style:

```json
{
  "meta": {
    "title": "Annual Report 2024",
    "slide_count": 18
  },
  "slides": [
    {
      "id": 256,
      "position": 1,
      "source_layout": "cover",
      "title": "Annual Report 2024",
      "subtitle": "Financial Year Ending Dec 31",
      "elements": []
    },
    {
      "id": 257,
      "position": 2,
      "source_layout": "content",
      "title": "Highlights",
      "elements": [
        {"type": "bullet", "level": 0, "text": "Revenue up 23%"},
        {"type": "bullet", "level": 0, "text": "New markets: APAC, MENA"},
        {"type": "stat", "value": "4.2M", "label": "Total Users"}
      ]
    }
  ]
}
```

---

## Step 4 — Conversion Mapping Plan

Produce a Markdown table showing source slide → target slide decisions:

```markdown
## Conversion Plan: Annual Report → Corporate Template

| # | Source Title | Source Layout | Target Layout | Notes |
|---|-------------|---------------|---------------|-------|
| 1 | Annual Report 2024 | cover | cover | Direct map |
| 2 | Highlights | content | stat-callout | 3 stats → callout layout |
| 3 | Revenue Growth | two-column | two-column | Chart preserved |
| 4 | Team | content | two-column | Split into 2 target slides (overflow) |
| 5 | (cont.) | — | two-column | Overflow from slide 4 |

**Content changes:**
- Slide 4 split into 2 slides (team list too long for single content slide)
- Slide 7 chart: embedded chart preserved as-is (cannot re-style chart data)
- Slides 12–14: embedded images retained, but backgrounds and typography updated

**⚠️ Items requiring user input:**
- Slide 9 "Custom Infographic" uses shapes not in target template — recommend replacing with content layout?
```

**Wait for user approval before rendering.**

---

## Step 5 — Render Using Target Template

### Option A: Use PptxGenJS (recommended for full control)

Build the deck from scratch using `content.json` as the data source and the target template's rules. See [create.md](create.md) for the full rendering guide.

This gives the cleanest result: every element is freshly rendered to target spec.

### Option B: Use unpack→edit→pack (when source has complex embedded content)

When the source has complex charts, embedded OLE objects, or heavily structured tables that cannot be recreated in PptxGenJS:

```bash
# Unpack source
python ../pptx/scripts/office/unpack.py source.pptx unpacked/

# For each slide, update visual properties in XML:
# - Background fill colors
# - Text run fonts and colors
# - Shape fill and border colors
# - Fixed element positions (page numbers, category labels)

# Clean and pack
python ../pptx/scripts/clean.py unpacked/
python ../pptx/scripts/office/pack.py unpacked/ output.pptx --original source.pptx
```

⚠️ Option B is significantly more error-prone. Prefer Option A whenever possible.

---

## Step 6 — Content Enhancement Pass

After rendering into the target template, verify and enhance content density:

1. **Density audit**: Check each content slide for ≥ 150 characters and 3–5 substantive points
2. **Visual mandatory**: Ensure every content slide has at least one visual element; if the source had a text-only slide, generate a structured visual (table, matrix, metric card) from the content
3. **Layout saturation**: Verify no slide has > 20% blank area (including within-shape empty space); reassign layouts if needed
4. **Logic densification**: If source content was sparse, supplement with industry context or data appropriate to the target template's domain

---

## Step 7 — Style Compliance Pass

After rendering, run the style analyzer against the target template:

```bash
python scripts/style_analyzer.py output.pptx --template templates/<target>/template.md
```

Any remaining style deviations (wrong fonts, off-palette colors) are listed with slide references. Fix each one.

---

## Step 8 — QA

```bash
# Content integrity check: compare source and output content
python -m markitdown source.pptx > source_content.txt
python -m markitdown output.pptx > output_content.txt
diff source_content.txt output_content.txt

# Linter
python scripts/linter.py output.pptx --template templates/<target>/template.md

# Visual QA
python ../pptx/scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

The diff check ensures no content was lost or duplicated during conversion. All text from the source must appear in the output (in restructured form if slides were split).

---

## Handling Special Cases

### Embedded Images
Images are preserved verbatim. Their placement may shift to match the target layout (e.g., an inline image becomes a half-bleed image in a `two-column` slide). Inform the user if image cropping is required.

### Embedded Charts
Excel-backed charts (OLE objects) cannot be re-styled to match a new template's palette. Options:
1. Extract chart data and re-create as a new native chart (preferred)
2. Preserve as-is and note the visual mismatch

### Logos and Brand Assets
Replace source logo with the target template's logo (from `templates/<name>/assets/`). Never carry over the source template's logo.

### Language and Locale
If the source uses a different language than the target template specifies, keep the content language but apply the template's font recommendations for that language (e.g., CJK fonts for Chinese text).
