# Description

A formal enterprise template designed for board presentations, investor decks, and internal business reviews. Visual tone is authoritative and data-forward: deep navy backgrounds for structural slides, clean white for content, with a red accent to draw attention to key metrics. Suitable for financial services, consulting, and large enterprise contexts. Compliance-oriented: strict color and font rules to match typical corporate brand guidelines.

---

# Visual Constraints

## Color Palette

```
Primary:    #1A2B5F   Deep navy — slide backgrounds (cover, section-break, closing)
Secondary:  #FFFFFF   White — text on dark backgrounds; content slide backgrounds
Accent:     #C8102E   Corporate red — callout boxes, key stats, highlight bars (use sparingly: max 15% visual area)
Text:       #1A1A1A   Near-black — all body text on white backgrounds
Muted:      #6B7280   Medium gray — captions, page numbers, source citations, metadata
Border:     #E5E7EB   Light gray — table borders, subtle dividers, card outlines
Highlight:  #EFF3FF   Ice blue tint — alternating table rows, callout backgrounds (never use for text)
```

**Color priority rule**: Red > Black/Navy > Gray. Red is reserved for the single most important element per slide. Do not use red for decorative purposes.

## Typography

```
Title (cover/section):   Microsoft YaHei / Arial, 40pt, #FFFFFF, bold
Slide Title (content):   Microsoft YaHei / Arial, 28pt, #1A2B5F, bold
Section Header:          Microsoft YaHei / Arial, 20pt, #1A2B5F, bold
Body:                    Arial, 14pt, #1A1A1A, regular, line-spacing 1.4×
Bullet L1:               Arial, 14pt, #1A1A1A, regular
Bullet L2:               Arial, 12pt, #4B5563, regular, indent 0.3"
Stat Value:              Microsoft YaHei / Arial, 52pt, #1A2B5F, bold
Stat Label:              Arial, 12pt, #6B7280, regular
Caption / Metadata:      Arial, 10pt, #6B7280, regular
```

Font priority notation: `Microsoft YaHei / Arial` → use Microsoft YaHei for CJK content or when available; otherwise Arial.

## Content Constraints

```
Visual Mandatory:
  Every content slide (content, two-column, stat-callout, data) MUST include
  at least one visual element — chart, table, diagram, metric block, or icon card.
  Pure-text slides are forbidden.

Information Density:
  Minimum 150 characters (including annotations) per content slide.
  Each slide must present 3–5 substantive points.
  Slides that merely list without analytical depth must be reworked.

Visual-Text Ratio:
  Visual elements (charts, tables, diagrams, stat blocks) must occupy ≥ 40%
  of the content area. Body text should annotate and explain visuals.

Layout Saturation:
  Prefer "left-visual / right-text" or "multi-column" arrangements.
  Large whitespace zones (> 30% of content area unused) are prohibited.
  Overflow: apply level-folding (collapse to matrix/table) or extract-summary
  (key point + evidence tag) — never truncate or naively split.
```

## Spacing

```
Slide edge margin:       0.5" (minimum on all sides)
Between content blocks:  0.35"
Title bottom padding:    0.2" (space between title and first content block)
Table row height:        0.4" minimum
```

---

# Asset Management

## Logo

```
File:     assets/logo.png (user-provided; skip if not available)
Position: top-left, x=0.4", y=0.15", w=1.2", h=auto (maintain aspect ratio)
Slides:   content and data slides only (not cover/closing where background is dark)
```

If `assets/logo.png` does not exist, omit the logo — never use a placeholder.

## Icons

```
Style:    Outline icons, single color matching slide context (Primary on light, Secondary on dark)
Stroke:   2pt
Source:   Use PptxGenJS shape primitives where possible; or embed user-provided SVG converted to PNG
Size:     0.35" × 0.35" for inline, 0.6" × 0.6" for standalone icon cards
```

## Images

```
- Slides with people/photos: use user-provided images only
- Decorative backgrounds: solid fills or two-stop gradients (Primary → darker Primary)
- Never embed external stock images
- Image placeholder style: solid fill #E5E7EB with centered "[ Image ]" text in Muted
```

---

# Structure & Layout

## Slide Dimensions

Layout: `LAYOUT_16x9` (10" × 5.625")

## Slide Master Mapping

| Content Type | Layout Name | Description |
|-------------|-------------|-------------|
| Cover page | `cover` | Full Primary background; large white title + subtitle; bottom accent bar in Accent color |
| Section divider | `section-break` | Primary left bar (w=1.2"), section number top, section title middle, white text |
| Bullet / text content | `content` | White background; navy slide title top; bulleted content below; optional right column for supporting visual |
| Two topics / comparison | `two-column` | White background; navy slide title top; two equal columns separated by 0.05" gap |
| KPI / metrics | `stat-callout` | White background; navy slide title; 3–4 large stat blocks in a row |
| Image + text | `image-focus` | Left half: full-bleed image; right half: title + bullets on white |
| Chart or table | `data` | White background; navy slide title; chart/table fills remaining area |
| Quote or highlight | `callout` | Primary background; large white quote text (24pt italic); attribution below in Muted |
| Closing / thank you | `closing` | Same as cover; replace title with closing message; subtitle with contact/next steps |

## Fixed Elements (apply to EVERY slide)

```
Category label:
  Position:  x=8.3", y=0.12", w=1.5", h=0.28"
  Style:     Arial 10pt, Muted (#6B7280), right-aligned
  Content:   Current section/chapter name

Page number:
  Position:  x=9.2", y=5.25", w=0.6", h=0.25"
  Style:     Arial 10pt, Muted (#6B7280), center-aligned
  Content:   Slide number (not "Page X of Y")

Accent bar (content slides only):
  Position:  x=0", y=0", w=0.12", h=5.625"
  Style:     Solid fill Accent (#C8102E)
  Purpose:   Left-edge vertical accent line for all content-type slides
```

**Note**: Cover, section-break, and closing slides do not have the category label or page number — they are structural anchor slides.

## Layout Quick Reference (coordinates in inches, 10"×5.625" canvas)

### cover
```
Background rect:  x=0, y=0, w=10, h=5.625, fill=Primary
Bottom bar:       x=0, y=5.1, w=10, h=0.525, fill=Accent
Title:            x=0.8, y=1.6, w=8.4, h=1.2, 40pt bold white
Subtitle:         x=0.8, y=2.9, w=8.4, h=0.7, 16pt regular white
Company/date:     x=0.8, y=5.15, w=6, h=0.35, 11pt regular white
```

### section-break
```
Left bar:         x=0, y=0, w=1.0, h=5.625, fill=Primary
Background:       x=1.0, y=0, w=9.0, h=5.625, fill=Secondary
Section number:   x=0.1, y=0.3, w=0.8, h=0.5, 28pt bold white, center
Section title:    x=1.4, y=2.0, w=8.3, h=1.2, 32pt bold Primary
Description:      x=1.4, y=3.3, w=7.5, h=1.0, 14pt regular Text
```

### content
```
Accent bar:       x=0, y=0, w=0.12, h=5.625, fill=Accent
Slide title:      x=0.5, y=0.3, w=9.0, h=0.7, 28pt bold Primary
Divider line:     x=0.5, y=1.05, w=9.0, h=0, border bottom 1pt Border
Content area:     x=0.5, y=1.15, w=9.0, h=4.2, 14pt regular Text
Category label:   (fixed element — top right)
Page number:      (fixed element — bottom right)
```

### two-column
```
Accent bar:       x=0, y=0, w=0.12, h=5.625, fill=Accent
Slide title:      x=0.5, y=0.3, w=9.0, h=0.7, 28pt bold Primary
Left column:      x=0.5, y=1.15, w=4.35, h=4.2
Column gap:       0.1"
Right column:     x=4.95, y=1.15, w=4.55, h=4.2
```

### stat-callout
```
Accent bar:       x=0, y=0, w=0.12, h=5.625, fill=Accent
Slide title:      x=0.5, y=0.3, w=9.0, h=0.7, 28pt bold Primary
Stat blocks (3):  x=0.5/3.7/6.9, y=1.5, w=2.8, h=3.0
  Value:          52pt bold Primary, centered
  Delta:          14pt, green (#16A34A) or red (#DC2626)
  Label:          12pt Muted, centered
```

### data
```
Accent bar:       x=0, y=0, w=0.12, h=5.625, fill=Accent
Slide title:      x=0.5, y=0.3, w=9.0, h=0.7, 28pt bold Primary
Chart/Table area: x=0.5, y=1.15, w=9.0, h=4.2
Source citation:  x=0.5, y=5.35, w=8.5, h=0.2, 9pt italic Muted
```
