# Template System

Templates govern every visual decision in the pro-pptx skill. A template defines what is and is not allowed in a presentation — colors, fonts, layout choices, element positions, and brand assets.

## Directory Structure

```
templates/
├── README.md           (this file)
├── corporate/
│   ├── template.md     (required — constraints + layout rules)
│   └── template.pptx   (optional — master reference file)
├── minimal/
│   ├── template.md
│   └── template.pptx
└── <custom>/
    ├── template.md
    └── template.pptx   (optional)
```

---

## template.md Format

Every `template.md` must contain these sections:

### `# Description`
One paragraph describing the template's purpose, target industry, and overall visual tone. This helps Claude select the right template automatically.

### `# Visual Constraints`

**Color Palette** — all colors as exact hex values with usage roles:
```
Primary:   #1A2B5F  (backgrounds, title slides, primary shapes)
Secondary: #FFFFFF  (text on dark backgrounds, content backgrounds)
Accent:    #C8102E  (callouts, highlights, key stats — use sparingly)
Text:      #1A1A1A  (body text on light backgrounds)
Muted:     #6B7280  (captions, metadata, secondary labels)
Border:    #E5E7EB  (table borders, dividers)
```

**Typography** — font face + size + color for each text level:
```
Title:          Microsoft YaHei / Arial, 40pt, Primary color, bold
Section Header: Microsoft YaHei / Arial, 28pt, Primary color, bold
Body:           Arial, 14pt, Text color, regular
Caption:        Arial, 11pt, Muted color, regular
Stat Value:     Microsoft YaHei / Arial, 48pt, Primary or Accent, bold
```

Font priority notation: `Font A / Font B` means use Font A if available, fall back to Font B.

**Line Spacing**: e.g., `Body: 1.4×`, `Bullets: 1.3×`

**Margins**: e.g., `Edge: 0.5"`, `Between blocks: 0.35"`

### `# Content Constraints` (NEW — recommended for all templates)

Defines information density and visual requirements enforced by the linter:

```
Visual Mandatory:
  Every content slide MUST include at least one visual element (chart, table,
  diagram, metric block). Pure-text slides are forbidden.

Information Density:
  Minimum 150 characters per content slide.
  Each slide must present 3–5 substantive analytical points.

Visual-Text Ratio:
  Visual elements must occupy ≥ 40% of the content area.

Layout Saturation:
  Prefer dense layouts. Large whitespace zones (> 30% unused) are prohibited.
  Overflow strategy: level-folding or extract-summary (never truncate/naively split).
```

### `# Asset Management`

**Logo**: file path relative to template folder, position, and size:
```
File: assets/logo.png
Position: top-left corner, x=0.4", y=0.2", w=1.2"
```

**Icons**: style description for AI-generated icons:
```
Style: outline, single color (Primary), stroke weight 2pt
Source: use shape primitives from PptxGenJS when possible
```

**Images**: usage policy:
```
- Product screenshots: always use user-provided images
- Decorative backgrounds: use solid fills or gradients (no external images)
- Team photos: use user-provided images only
```

### `# Structure & Layout`

**Slide Master Mapping** — content type → layout name mapping:
```
cover          → Full-bleed dark background, centered title + subtitle
section-break  → Dark accent bar left, section number + title right
content        → Slide title top, bulleted content below
two-column     → Slide title top, two equal columns below
stat-callout   → Slide title top, 3–4 large stat blocks
image-focus    → Half-bleed image left, title + bullets right
data           → Slide title top, chart/table fills remaining space
callout        → Large quote text centered, attribution below
closing        → Same as cover, different text
```

**Fixed Elements** (absolute positions, apply to EVERY slide):
```
Category label:  x=8.5", y=0.15", w=1.3", h=0.25"  right-aligned, caption style
Page number:     x=9.3", y=5.2",  w=0.5", h=0.25"  centered,       caption style
Logo:            x=0.4", y=0.2",  w=1.2"           (if required by brand)
```

---

## Creating a New Template

1. Create a folder: `templates/<your-name>/`
2. Copy the `template.md` from `corporate/` as a starting point
3. Edit every section with your specific values
4. Optionally add `template.pptx` as a visual reference (Claude can extract additional layout details from it)
5. Optionally add `assets/` folder with logo files

---

## Template Selection Logic

When no template is specified, Claude selects by:

1. **Explicit mention**: user says "use the corporate template" → use `corporate/`
2. **Style analysis**: run `style_analyzer.py` on an existing input file; use the best-match template if ≥80% similar
3. **Context inference**: industry keywords in the user's request (e.g., "investor deck" → corporate, "personal portfolio" → minimal)
4. **Ask the user**: if none of the above gives a clear answer

---

## Built-in Templates

| Template | Style | Best for |
|----------|-------|----------|
| `corporate` | Deep navy + red accent, Microsoft YaHei/Arial, formal layout | Enterprise reports, investor decks, board presentations |
| `minimal` | White + light gray, thin lines, generous whitespace | Product decks, conference talks, portfolio presentations |
| `hw-insight` | Navy-black + Huawei red, evidence-driven, external-only scope | Chief Architect technology briefings, external foresight reports, standards/ecosystem intelligence |
