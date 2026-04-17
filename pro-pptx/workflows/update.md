# Workflow: Update Existing PPT (with Slide ID Locking)

Use this workflow when modifying an existing presentation where some slides must not be changed — for example, slides the user has manually tweaked, slides with approved content, or slides with embedded media that cannot be regenerated.

---

## Core Principle: Slide ID Locking

Every slide in a PPTX has a stable numeric ID in `ppt/presentation.xml` (`<p:sldId id="...">`). This ID persists across unpack/pack cycles and is the reliable key for protecting specific slides.

**Locked slides are never modified**, regardless of what content changes are requested.

---

## Step 1 — Inventory Existing Slides

```bash
# Extract text content
python -m markitdown input.pptx

# Visual overview
python ../pptx/scripts/thumbnail.py input.pptx

# List all slide IDs
python scripts/slide_id_manager.py list input.pptx
```

Output of `list` command:
```
Slide  1  ID=256  ppt/slides/slide1.xml   "Cover Slide"
Slide  2  ID=257  ppt/slides/slide2.xml   "Q1 Results"
Slide  3  ID=258  ppt/slides/slide3.xml   "Team Update"
Slide  4  ID=259  ppt/slides/slide4.xml   "Roadmap 2025"
...
```

---

## Step 2 — Identify Locked Slides

Ask the user which slides should be preserved. Two ways to specify:

**By slide number** (friendlier):
```
"Keep slides 2, 3, and 7 as-is"
```

**By slide ID** (more precise, survives reordering):
```
"Lock slide IDs 258, 262, 271"
```

Save the lock manifest:

```bash
python scripts/slide_id_manager.py lock input.pptx \
  --ids 258,262,271 \
  --manifest .slide_locks.json
```

The manifest file (`.slide_locks.json`) records:
```json
{
  "source_file": "input.pptx",
  "locked": [
    {"id": 258, "title": "Team Update", "locked_at": "2025-01-15"},
    {"id": 262, "title": "Q3 Roadmap",  "locked_at": "2025-01-15"},
    {"id": 271, "title": "Appendix A",  "locked_at": "2025-01-15"}
  ]
}
```

---

## Step 3 — Analyze Style

```bash
python scripts/style_analyzer.py input.pptx --templates-dir templates/
```

- If similarity ≥ 80% to a known template → use that template for new/modified slides
- If similarity < 80% → extract styles as a temporary template and maintain the existing look

---

## Step 4 — Draft Mode

Produce a Markdown plan showing what will change:

```markdown
## Update Plan for: [filename]
**Template**: auto-detected (corporate, 92% match)

### Slides to MODIFY:
| # | ID | Current Title | Planned Change |
|---|----|---------------|----------------|
| 1 | 256 | Cover Slide | Update title to "Q2 2025 Review" |
| 4 | 259 | Roadmap 2025 | Replace timeline with new milestones |
| 5 | 260 | Financials | Insert new data table |

### Slides LOCKED (will not change):
| # | ID | Title |
|---|----|-------|
| 3 | 258 | Team Update |
| 6 | 262 | Q3 Roadmap |
| 8 | 271 | Appendix A |

### New slides to ADD:
| Position | Title | Layout |
|----------|-------|--------|
| After slide 5 | Key Risks | two-column |
```

**Wait for user confirmation before proceeding.**

---

## Step 5 — Unpack and Apply Changes

```bash
python ../pptx/scripts/office/unpack.py input.pptx unpacked/
```

### Check each slide before editing

```bash
python scripts/slide_id_manager.py check --id <ID> --manifest .slide_locks.json
```

**STOP** if result is `LOCKED`. Move to the next slide.

### Edit unlocked slides

For each unlocked slide requiring changes:
1. Read `unpacked/ppt/slides/slideN.xml`
2. Identify placeholders and update content
3. Use the Edit tool (never sed or Python scripts)
4. Ensure template compliance: colors, fonts, fixed elements
5. **Content density validation**: after editing, verify:
   - ≥ 150 characters of substantive content per slide
   - At least one visual element (chart, table, diagram, shape) present
   - Visual elements occupy ≥ 40% of content area
   - No blank area > 20% of content area
6. **Content enrichment**: if the updated content is too sparse, apply logic densification — supplement with industry context, case studies, or data projections to meet density targets

For font compliance in XML edits:
```xml
<!-- Use template font faces only -->
<a:rPr lang="zh-CN" sz="2800" b="1">
  <a:latin typeface="Microsoft YaHei"/>
</a:rPr>
```

### Add new slides

```bash
# Duplicate a layout-compatible existing slide
python ../pptx/scripts/add_slide.py unpacked/ slideN.xml

# This prints the <p:sldId> element to insert into presentation.xml
# Insert it at the correct position in <p:sldIdLst>
```

Then edit the new slide's content.

### Delete slides (if any)

Remove the `<p:sldId>` from `ppt/presentation.xml`'s `<p:sldIdLst>`. Do NOT delete locked slides.

---

## Step 6 — Clean and Pack

```bash
python ../pptx/scripts/clean.py unpacked/
python ../pptx/scripts/office/pack.py unpacked/ output.pptx --original input.pptx
```

---

## Step 7 — Verify Lock Integrity

```bash
# Confirm all locked slides are present and unchanged
python scripts/slide_id_manager.py verify \
  --original input.pptx \
  --output output.pptx \
  --manifest .slide_locks.json
```

This checks:
1. All locked slide IDs still exist in output
2. Their XML content is byte-for-byte identical to the original

---

## Step 8 — QA

```bash
python -m markitdown output.pptx
python scripts/linter.py output.pptx --template templates/<name>/template.md
python ../pptx/scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

Inspect images. Confirm locked slides visually match the original.

---

## Edge Cases

### "The user wants to change a locked slide"
Inform the user explicitly:
> "Slide 3 (ID 258) is locked. To modify it, first unlock it: `python scripts/slide_id_manager.py unlock --id 258 --manifest .slide_locks.json`"

### "New content would overflow into a locked slide's position"
Add the overflow content as a new slide inserted before or after, never by pushing the locked slide.

### "The user wants to reorder slides including locked ones"
Reordering is allowed — slide order is separate from content. But **do not** change the IDs or content of locked slides.

### "Multiple iterative updates"
Each update session can add more locked slides to the manifest. The manifest accumulates over time and becomes a project-level lock record.
