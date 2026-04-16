# Description

A clean, content-first template with generous whitespace and minimal decoration. Designed for conference presentations, product demos, and technical talks where clarity and readability matter more than corporate formality. Thin accent lines replace heavy color blocks; the palette is almost monochromatic with a single warm accent. Works well for technology, design, and startup contexts.

---

# Visual Constraints

## Color Palette

```
Primary:    #111827   Charcoal black — headings, key shapes
Secondary:  #FFFFFF   White — slide backgrounds, text on dark
Accent:     #6366F1   Indigo — single emphasis element per slide (never overused)
Text:       #374151   Dark gray — body text (softer than pure black)
Muted:      #9CA3AF   Light gray — captions, page numbers, secondary info
Border:     #E5E7EB   Very light gray — dividers, card outlines, table borders
Surface:    #F9FAFB   Off-white — card/callout backgrounds on white slides
```

**Color priority rule**: One accent element per slide maximum. Use Accent only for the single most important element — a highlight, a key stat, or an icon. Everything else is Primary or Muted.

## Typography

```
Title (cover/section):   Inter / Calibri, 42pt, #FFFFFF or #111827 (context), bold
Slide Title (content):   Inter / Calibri, 26pt, #111827, bold
Section Header:          Inter / Calibri, 18pt, #111827, semibold (bold=1 in XML)
Body:                    Calibri / Arial, 15pt, #374151, regular, line-spacing 1.5×
Bullet L1:               Calibri / Arial, 15pt, #374151, regular
Bullet L2:               Calibri / Arial, 13pt, #6B7280, regular, indent 0.25"
Stat Value:              Inter / Calibri, 56pt, #111827 or #6366F1, bold
Stat Label:              Calibri / Arial, 13pt, #9CA3AF, regular
Caption / Metadata:      Calibri / Arial, 10pt, #9CA3AF, regular
Code / Technical:        Consolas / Courier New, 13pt, #374151, Surface background
```

Font priority: `Inter / Calibri` → use Inter if installed, else Calibri.

## Content Constraints

```
Visual Mandatory:
  Every content slide (content, two-column, stat-callout, data) MUST include
  at least one visual element — chart, table, diagram, stat card, or icon.
  Pure-text slides are forbidden.

Information Density:
  Minimum 150 characters (including annotations) per content slide.
  Each slide must present 3–5 substantive points.

Visual-Text Ratio:
  Visual elements must occupy ≥ 40% of the content area.

Layout Saturation:
  Use clean card-based layouts to fill content area without clutter.
  Blank area > 20% of content area is prohibited.
  Overflow: apply level-folding or extract-summary — never truncate.
```

## Spacing

```
Slide edge margin:       0.6" (slightly more generous than corporate)
Between content blocks:  0.4"
Title bottom padding:    0.3"
Table row height:        0.45"
```

---

# Asset Management

## Logo

```
File:     assets/logo.png (user-provided; skip if not available)
Position: top-right, x=8.8", y=0.2", w=0.9", h=auto
Slides:   all slides except cover (where it can go bottom-left in smaller size)
```

## Icons

```
Style:    Filled rounded icons (or outline if cleaner for context)
Color:    Accent (#6366F1) for featured icons; Muted for supporting icons
Source:   PptxGenJS shapes or user-provided SVG/PNG
Size:     0.4" × 0.4" inline, 0.65" × 0.65" standalone (in Surface-color circle)
Circle:   Background circle at 0.85" × 0.85", fill Surface (#F9FAFB), no border
```

## Images

```
- Photos: user-provided only; rounded corners (0.08" radius using clipping)
- Decorative: solid fills only — never background images
- Placeholder: Surface (#F9FAFB) fill, thin Border (#E5E7EB) border, centered text "[ Image ]"
```

---

# Structure & Layout

## Slide Dimensions

Layout: `LAYOUT_16x9` (10" × 5.625")

## Slide Master Mapping

| Content Type | Layout Name | Description |
|-------------|-------------|-------------|
| Cover page | `cover` | Dark background (Primary); large white title; subtitle; optional tagline |
| Section divider | `section-break` | White background; large section number in Accent; section title; thin top border |
| Bullet / text content | `content` | White background; slide title; content below; bottom accent line instead of side bar |
| Two topics / comparison | `two-column` | White; slide title; two columns with light Surface card background |
| KPI / metrics | `stat-callout` | White; slide title; 2–4 stat cards with Surface background |
| Image + text | `image-focus` | Right: image (60% width); left: title + bullets |
| Chart or table | `data` | White; slide title; chart/table; source citation |
| Quote or highlight | `callout` | Accent-colored pull quote on white; italic large text |
| Closing | `closing` | Same as cover; closing message + contact |

## Fixed Elements (apply to EVERY slide except cover/closing)

```
Bottom accent line:
  Position:  x=0.6", y=5.4", w=8.8", h=0 (horizontal line)
  Style:     1pt solid Border (#E5E7EB)
  Purpose:   Subtle footer separator

Page number:
  Position:  x=9.2", y=5.4", w=0.5", h=0.2"
  Style:     Calibri 10pt, Muted (#9CA3AF), right-aligned
  Content:   Slide number

Slide title underline:
  Position:  x=0.6", y=1.0", w=2.0", h=0 (short underline under title)
  Style:     2pt solid Accent (#6366F1)
  Purpose:   Minimal visual anchor below slide title
```

## Layout Quick Reference (coordinates in inches, 10"×5.625" canvas)

### cover
```
Background:       x=0, y=0, w=10, h=5.625, fill=Primary
Title:            x=0.8, y=1.5, w=8.4, h=1.4, 42pt bold white
Subtitle:         x=0.8, y=3.0, w=8.4, h=0.7, 16pt regular, Muted (#9CA3AF)
Accent dot:       x=0.75, y=3.05, w=0.06, h=0.06, fill=Accent (visual punctuation)
Bottom strip:     x=0, y=5.4, w=10, h=0.225, fill=Accent
```

### section-break
```
Background:       x=0, y=0, w=10, h=5.625, fill=Secondary
Top border line:  x=0, y=0, w=10, h=0, border 3pt solid Primary
Section number:   x=0.6", y=0.8", w=2.0", h=1.2", 72pt bold Accent
Section title:    x=0.6", y=2.1", w=9.0", h=1.0", 32pt bold Primary
Description:      x=0.6", y=3.2", w=8.5", h=1.2", 15pt regular Text
Title underline:  x=0.6", y=3.15", w=1.5", h=0, 2pt solid Accent
```

### content
```
Slide title:      x=0.6", y=0.3", w=8.8", h=0.65", 26pt bold Primary
Title underline:  x=0.6", y=1.0", w=2.0", h=0, 2pt solid Accent
Content area:     x=0.6", y=1.15", w=8.8", h=4.0", 15pt regular Text
Bottom line:      (fixed element)
Page number:      (fixed element)
```

### two-column
```
Slide title:      x=0.6", y=0.3", w=8.8", h=0.65", 26pt bold Primary
Title underline:  x=0.6", y=1.0", w=2.0", h=0, 2pt solid Accent
Left card:        x=0.6", y=1.15", w=4.2", h=4.0", fill=Surface, border Border, rounded
Right card:       x=5.2", y=1.15", w=4.2", h=4.0", fill=Surface, border Border, rounded
  (content inside cards: x+0.2", y+0.2", w-0.4", h-0.4")
```

### stat-callout
```
Slide title:      x=0.6", y=0.3", w=8.8", h=0.65"
Title underline:  x=0.6", y=1.0", w=2.0", h=0, 2pt Accent
Stat cards (3):
  Card 1: x=0.6", y=1.3", w=2.7", h=3.8", fill=Surface, border Border
  Card 2: x=3.65", y=1.3", w=2.7", h=3.8", fill=Surface, border Border
  Card 3: x=6.7", y=1.3", w=2.7", h=3.8", fill=Surface, border Border
  Value inside card: centered, 56pt bold, Accent for featured / Primary for others
  Delta: 13pt, green/red
  Label: 13pt Muted, centered
```

### data
```
Slide title:      x=0.6", y=0.3", w=8.8", h=0.65"
Title underline:  x=0.6", y=1.0", w=2.0", h=0, 2pt Accent
Chart/Table area: x=0.6", y=1.15", w=8.8", h=3.9"
Source citation:  x=0.6", y=5.3", w=8.0", h=0.2", 9pt italic Muted
```
