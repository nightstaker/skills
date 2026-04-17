#!/usr/bin/env python3
"""
Pro-PPTX Linter — compliance and quality checks against a template definition.

Checks:
  1. Font compliance      — all font faces must be in template's Typography section
  2. Color compliance     — all solid fill colors must be in template's Color Palette
  3. Fixed element drift  — page numbers and category labels must be within tolerance
  4. Text overflow        — approximate check: characters × font size vs. box area
  5. Alt text             — images without alt text are flagged
  6. Empty slides         — slides with no visible content
  7. Slide count          — warn if deck seems unexpectedly short or long
  8. Whitespace ratio     — blank area must not exceed 20% of content zone (shapes+images vs total area)
  9. Content density      — content slides must have ≥150 chars of substantive text
 10. Visual mandatory     — content slides must include ≥1 visual element (chart/table/image/shape)
 11. Visual-text ratio    — visual elements should occupy ≥40% of content area
 12. Content zone breach  — elements must stay within the grid content zone boundaries
 13. Element overlap      — no two elements may occupy the same pixel area

Usage:
    python scripts/linter.py output.pptx --template templates/corporate/template.md
    python scripts/linter.py output.pptx --template templates/corporate/template.md --strict
    python scripts/linter.py output.pptx --template templates/corporate/template.md --json
"""

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

try:
    from lxml import etree
except ImportError:
    print("ERROR: Missing lxml. Run: pip install lxml", file=sys.stderr)
    sys.exit(1)

NS_A   = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS_P   = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS_R   = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

# EMU to inches
EMU_PER_INCH = 914400

# ---------------------------------------------------------------------------
# Layout / metric constants — the contract between renderer and linter.
# Tuning any value below changes how text/table geometry is predicted.
# Keep these aligned with the JS helpers in tech-insight/output/*.js.
# ---------------------------------------------------------------------------

# Pixel-level whitespace grid resolution (cells per inch). 40 ≈ 0.025" per cell.
GRID_RES = 40

# Character width model — matches YaHei/PingFang native metrics used by WPS /
# PowerPoint / Keynote. LibreOffice fallback fonts measure wider (~1.15–1.25×)
# but we align with dominant native rendering for the Office ecosystem.
CJK_CHAR_WIDTH   = 1.0    # × (font_size / 72)
ASCII_CHAR_WIDTH = 0.50   # × (font_size / 72)

# Line-height multipliers for PowerPoint.
# Table cells use 1.6× (more padding) while paragraph text uses 1.4×.
LINE_HEIGHT_MULT      = 1.6   # table cell line-height
PARA_LINE_HEIGHT_MULT = 1.4   # standalone paragraph line-height

# PowerPoint text-box default inset is 0.10" per side → 0.20" total.
TEXTBOX_INSET_TOTAL = 0.20

# Per-cell padding inside tables (roughly 0.08" each side).
TABLE_CELL_INSET_TOTAL = 0.16

# Safety factors for height estimators (over-predict slightly so PPT's
# kerning / line-spacing quirks don't push content into adjacent elements).
CARD_HUG_SAFETY   = 1.25   # filled card h must not exceed true_h × this + margin
CARD_HUG_MARGIN   = 0.15   # + inches of aesthetic breathing room
TABLE_HEIGHT_SAFETY = 1.20

# Image coverage — share of content slides that must include a real image.
IMAGE_COVERAGE_MIN = 0.60


# ---------------------------------------------------------------------------
# Template parsing
# ---------------------------------------------------------------------------

def parse_template(template_md_path: str) -> dict:
    """
    Parse a template.md file and extract compliance rules.

    Returns:
    {
        "allowed_colors": set of uppercase hex strings (without #)
        "allowed_fonts": list of font name strings (lowercased)
        "fixed_elements": {
            "page_number": {"x": float, "y": float, "w": float, "h": float},
            "category_label": {"x": float, "y": float, "w": float, "h": float},
        }
    }
    """
    text = Path(template_md_path).read_text(encoding="utf-8")

    # Extract hex colors
    allowed_colors = set()
    for match in re.finditer(r"#([0-9A-Fa-f]{6})", text):
        allowed_colors.add(match.group(1).upper())

    # Extract font names from Typography section lines like:
    # "Microsoft YaHei / Arial, 40pt, ..."
    # Only look inside the ## Typography / Typography section to avoid false positives
    # from color variable names (NavyMid, Highlight, Text) that appear elsewhere.
    _NON_FONT_WORDS = {
        "navymid", "highlight", "text", "ink", "primary", "secondary", "accent",
        "muted", "border", "fill", "bold", "italic", "regular", "left", "center",
        "right", "top", "bottom", "white", "black", "base", "upside", "risk",
        "surface", "light", "dark", "medium", "color", "style",
    }
    allowed_fonts = set()
    # Restrict to the Typography block (between "## Typography" and the next "##" heading)
    typo_block_m = re.search(
        r"##\s+Typography\b(.*?)(?=\n##\s|\Z)", text, re.DOTALL | re.IGNORECASE
    )
    typo_text = typo_block_m.group(1) if typo_block_m else text

    for match in re.finditer(
        r"([A-Z][A-Za-z\s]+(?:/\s*[A-Z][A-Za-z\s]+)*),\s*\d+pt", typo_text
    ):
        for font in match.group(1).split("/"):
            f = font.strip().lower()
            if f and f not in _NON_FONT_WORDS and len(f) > 2:
                allowed_fonts.add(f)

    # Also extract plain font names from lines like "fontFace: "Microsoft YaHei""
    for match in re.finditer(r"[Ff]ont[Ff]ace[:\s]+[\"']?([A-Za-z\s]+)[\"']?", text):
        f = match.group(1).strip().lower()
        if f and f not in _NON_FONT_WORDS:
            allowed_fonts.add(f)

    # Extract fixed element positions from the "## Fixed Elements" section.
    # Looks for label lines like "Page number:" followed by "Position: x=N, y=N, w=N"
    # within the same element block (stops at the next blank-line-separated block).
    fixed_elements = {}

    # Isolate the Fixed Elements block to avoid false matches elsewhere in the file
    fe_block_m = re.search(
        r"##\s+Fixed Elements?\b(.*?)(?=\n##\s|\Z)", text, re.DOTALL | re.IGNORECASE
    )
    fe_text = fe_block_m.group(1) if fe_block_m else ""

    # Known label aliases: maps canonical key → list of possible label strings in template.md
    _FIXED_LABEL_ALIASES = {
        "page_number":      ["Page number", "Page Number"],
        "category_label":   ["Category label", "Department label", "BU label", "Section label"],
        "confidentiality":  ["Confidentiality label", "Confidentiality", "Classification label"],
    }

    def _extract_pos_from_block(block: str, section_name: str, key: str):
        """Find 'section_name:' line then the nearest Position: x=... on the next line(s)."""
        # Match: label line, then within ~3 lines, a Position: x=... y=... w=...
        pattern = (
            re.escape(section_name)
            + r"[^\n]*\n(?:[^\n]*\n){0,3}?[^\n]*"
            + r"x\s*=\s*([\d.]+)[\"\"]*[,\s]+y\s*=\s*([\d.]+)[\"\"]*[,\s]+w\s*=\s*([\d.]+)"
        )
        m = re.search(pattern, block, re.IGNORECASE)
        if m:
            fixed_elements[key] = {
                "x": float(m.group(1)),
                "y": float(m.group(2)),
                "w": float(m.group(3)),
            }
            return True
        return False

    for key, aliases in _FIXED_LABEL_ALIASES.items():
        for alias in aliases:
            if _extract_pos_from_block(fe_text, alias, key):
                break  # found via this alias, stop trying others

    # Extract content constraints (if defined in template)
    content_constraints = {
        "min_chars": 150,
        "min_points": 3,
        "visual_mandatory": True,
        "visual_ratio_min": 0.40,
        "max_whitespace": 0.20,
        "image_coverage_required": True,
        "image_coverage_min": IMAGE_COVERAGE_MIN,
    }

    # Check if template explicitly defines content constraints
    cc_block_m = re.search(
        r"##\s+Content Constraints?\b(.*?)(?=\n##\s|\Z)", text, re.DOTALL | re.IGNORECASE
    )
    if cc_block_m:
        cc_text = cc_block_m.group(1)
        # Extract minimum character count if specified
        min_chars_m = re.search(r"(?:Minimum|≥)\s*(\d+)\s*(?:char|字)", cc_text, re.IGNORECASE)
        if min_chars_m:
            content_constraints["min_chars"] = int(min_chars_m.group(1))
        # Extract visual ratio if specified — anchor on "visual" to avoid
        # accidentally matching image-coverage or whitespace percentages.
        ratio_m = re.search(
            r"[Vv]isual[^%\n]{0,120}[≥>]\s*(\d+)%", cc_text)
        if ratio_m:
            content_constraints["visual_ratio_min"] = int(ratio_m.group(1)) / 100.0
        # Extract max whitespace if specified
        ws_m = re.search(r"[>≥]\s*(\d+)%\s*(?:of content area.*?(?:blank|unused|whitespace|空白)|\S*(?:blank|unused|whitespace|空白))", cc_text, re.IGNORECASE)
        if ws_m:
            content_constraints["max_whitespace"] = int(ws_m.group(1)) / 100.0
        # Extract image coverage floor: "≥60% of content slides" / "image coverage ≥ 60%"
        ic_m = re.search(
            r"(?:image\s*coverage|real\s*image[s]?)\b[^0-9%]{0,40}[≥>]\s*(\d+)%",
            cc_text, re.IGNORECASE)
        if ic_m:
            content_constraints["image_coverage_min"] = int(ic_m.group(1)) / 100.0
        # Explicit opt-out: "image coverage: optional" / "no image coverage"
        if re.search(r"image[s]?\s*(?:coverage\s*)?:\s*optional|no\s*image\s*coverage",
                     cc_text, re.IGNORECASE):
            content_constraints["image_coverage_required"] = False
        # Also check Layout Saturation section
        ls_block_m = re.search(r"Layout Saturation(.*?)(?:\n```|\n##|\Z)", text, re.DOTALL | re.IGNORECASE)
        if ls_block_m:
            ls_text = ls_block_m.group(1)
            ws_m2 = re.search(r">\s*(\d+)%", ls_text)
            if ws_m2:
                content_constraints["max_whitespace"] = int(ws_m2.group(1)) / 100.0
    else:
        # No Content Constraints section — disable density checks
        content_constraints["enabled"] = False

    content_constraints.setdefault("enabled", True)

    # Extract grid layout content zone boundaries (if defined in template)
    # Looks for "Content zone" block with x/y min/max values
    grid_zone = None
    grid_block_m = re.search(
        r"##\s+Grid Layout System\b(.*?)(?=\n---|\n#\s|\Z)", text, re.DOTALL | re.IGNORECASE
    )
    if grid_block_m:
        grid_text = grid_block_m.group(1)
        # Parse content zone: x: 0.45" – 9.55", y: 1.00" – 5.15"
        x_range_m = re.search(r"x:\s*([\d.]+)[\"″]?\s*[–-]\s*([\d.]+)[\"″]?", grid_text)
        y_range_m = re.search(r"y:\s*([\d.]+)[\"″]?\s*[–-]\s*([\d.]+)[\"″]?", grid_text)
        if x_range_m and y_range_m:
            grid_zone = {
                "x_min": float(x_range_m.group(1)),
                "x_max": float(x_range_m.group(2)),
                "y_min": float(y_range_m.group(1)),
                "y_max": float(y_range_m.group(2)),
            }

    return {
        "allowed_colors": allowed_colors,
        "allowed_fonts": allowed_fonts,
        "fixed_elements": fixed_elements,
        "content_constraints": content_constraints,
        "grid_zone": grid_zone,
    }


# ---------------------------------------------------------------------------
# Per-slide linting
# ---------------------------------------------------------------------------

def _emu_to_in(emu: str) -> float:
    try:
        return int(emu) / EMU_PER_INCH
    except (TypeError, ValueError):
        return 0.0


def _compute_table_true_height(gf_el):
    """Compute the true rendered height of a table by analyzing cell content.

    PowerPoint auto-sizes row heights based on text content, ignoring the
    declared row h=0 that PptxGenJS writes. We estimate by computing
    lines needed per cell based on text length, font size, and column width.
    """
    tbl = gf_el.find(".//{%s}tbl" % NS_A)
    if tbl is None:
        return None

    grid_cols = tbl.findall("{%s}tblGrid/{%s}gridCol" % (NS_A, NS_A))
    col_widths = [_emu_to_in(gc.get("w", "914400")) for gc in grid_cols]

    rows = tbl.findall("{%s}tr" % NS_A)
    total_height = 0.0

    for row in rows:
        cells = row.findall("{%s}tc" % NS_A)
        max_cell_height = 0.0

        for ci, cell in enumerate(cells):
            cell_text = ""
            for t_el in cell.iter("{%s}t" % NS_A):
                if t_el.text:
                    cell_text += t_el.text

            font_size = 8.0
            for rpr in cell.iter("{%s}rPr" % NS_A):
                sz = rpr.get("sz")
                if sz:
                    try:
                        font_size = int(sz) / 100.0
                    except ValueError:
                        pass
                    break

            col_w = col_widths[min(ci, len(col_widths) - 1)] if col_widths else 1.0
            usable_w = max(0.1, col_w - TABLE_CELL_INSET_TOTAL)

            cjk_w = font_size / 72.0 * CJK_CHAR_WIDTH
            ascii_w = font_size / 72.0 * ASCII_CHAR_WIDTH

            wrapped_lines = 0
            for line in cell_text.split("\n"):
                cur_w = 0.0
                line_count = 1
                for ch in line:
                    ch_w = cjk_w if ord(ch) > 0x2E80 else ascii_w
                    cur_w += ch_w
                    if cur_w > usable_w:
                        line_count += 1
                        cur_w = ch_w
                wrapped_lines += line_count
            total_lines = max(1, wrapped_lines)

            line_height = font_size / 72.0 * LINE_HEIGHT_MULT
            cell_margin = 0.10  # top+bottom padding
            cell_height = total_lines * line_height + cell_margin
            max_cell_height = max(max_cell_height, cell_height)

        row_height = max(max_cell_height, 0.25)
        total_height += row_height

    # Safety factor: PowerPoint's actual layout is affected by kerning,
    # paragraph spacing, cell margins, and font metrics beyond pure
    # character-counting.
    return total_height * TABLE_HEIGHT_SAFETY


def _compute_textbox_required_height(sp_el, declared_w):
    """Compute the minimum height a text box needs to render its content.

    PowerPoint ignores the declared box height when text content exceeds it —
    the text visually overflows into adjacent elements. This function estimates
    the MINIMUM height the text actually needs, so we can detect when the
    declared height is too small (indicating visual overflow).
    """
    # Accept either an sp element (finds txBody inside) or a txBody directly.
    if sp_el is None:
        return 0.0
    if sp_el.tag.endswith("}txBody"):
        tx_body = sp_el
    else:
        tx_body = sp_el.find("{%s}txBody" % NS_P)
        if tx_body is None:
            tx_body = sp_el.find(".//{%s}txBody" % NS_A)
    if tx_body is None:
        return 0.0

    # Collect all paragraphs with their runs (font sizes + text)
    total_height = 0.0
    usable_w = max(0.1, declared_w - TEXTBOX_INSET_TOTAL)

    for para in tx_body.findall("{%s}p" % NS_A):
        # Collect runs — each (text, font_size) preserves per-run sizing
        runs = []
        max_fs = 0.0  # used for line height only
        for r in para.findall("{%s}r" % NS_A):
            rpr = r.find("{%s}rPr" % NS_A)
            fs = 12.0
            if rpr is not None:
                sz = rpr.get("sz")
                if sz:
                    try:
                        fs = int(sz) / 100.0
                    except ValueError:
                        pass
            t = r.find("{%s}t" % NS_A)
            txt = t.text if (t is not None and t.text) else ""
            if txt:
                runs.append((txt, fs))
                if fs > max_fs:
                    max_fs = fs
        # Fallback to endParaRPr for font size (empty paragraphs)
        if max_fs == 0.0:
            for epr in para.iter("{%s}endParaRPr" % NS_A):
                sz = epr.get("sz")
                if sz:
                    try:
                        max_fs = int(sz) / 100.0
                    except ValueError:
                        pass
                    break
            if max_fs == 0.0:
                max_fs = 12.0

        if not runs:
            # Empty paragraph still takes one line height at max_fs
            total_height += max_fs / 72.0 * PARA_LINE_HEIGHT_MULT
            continue

        # Lay out characters across runs using each run's own font size
        cur_w = 0.0
        line_count = 1
        for txt, fs in runs:
            cjk_w = fs / 72.0 * CJK_CHAR_WIDTH
            ascii_w = fs / 72.0 * ASCII_CHAR_WIDTH
            for ch in txt:
                ch_w = cjk_w if ord(ch) > 0x2E80 else ascii_w
                cur_w += ch_w
                if cur_w > usable_w:
                    line_count += 1
                    cur_w = ch_w

        # Line height uses max font size (PowerPoint behavior). Paragraphs use
        # a slightly tighter multiplier than the table cell multiplier because
        # paragraph spacing is not additive here.
        line_h = max_fs / 72.0 * PARA_LINE_HEIGHT_MULT
        total_height += line_count * line_h

    # Add top+bottom padding
    total_height += 0.08
    return total_height


def lint_slide(slide_xml: bytes, slide_pos: int, template_rules: dict,
               strict: bool = False) -> list[dict]:
    """
    Run all checks on a single slide's XML.

    Returns list of issue dicts:
    {"slide": int, "severity": "error"|"warning", "check": str, "message": str}
    """
    issues = []
    tree = etree.fromstring(slide_xml)
    rules = template_rules

    def issue(severity, check, msg):
        issues.append({"slide": slide_pos, "severity": severity, "check": check, "message": msg})

    # ------------------------------------------------------------------
    # 1. Font compliance
    # ------------------------------------------------------------------
    if rules["allowed_fonts"]:
        for rpr in tree.iter("{%s}rPr" % NS_A):
            latin = rpr.find("{%s}latin" % NS_A)
            if latin is None:
                continue
            tf = latin.get("typeface", "").lower()
            if not tf or tf.startswith("+"):
                continue
            # Allow theme fonts (+mj-lt, +mn-lt style)
            if not any(tf == af or tf.startswith(af[:6]) for af in rules["allowed_fonts"]):
                issue("error", "font_compliance",
                      f"Non-template font used: \"{latin.get('typeface')}\"")

    # ------------------------------------------------------------------
    # 2. Color compliance
    # ------------------------------------------------------------------
    if rules["allowed_colors"]:
        seen_bad_colors: set = set()
        for srgb in tree.iter("{%s}srgbClr" % NS_A):
            val = srgb.get("val", "").upper()
            if val and val not in rules["allowed_colors"] and val not in seen_bad_colors:
                seen_bad_colors.add(val)
                issue("error", "color_compliance",
                      f"Off-palette color: #{val}")

    # ------------------------------------------------------------------
    # 3. Alt text on images
    # ------------------------------------------------------------------
    # pptxgenjs emits <p:blipFill> while python-pptx writes <a:blipFill>;
    # inspect both namespaces to avoid missing images.
    blip_fills = list(tree.iter("{%s}blipFill" % NS_A)) + list(tree.iter("{%s}blipFill" % NS_P))
    for blip_fill in blip_fills:
        # Walk up to find the parent nvPicPr → nvPr → cNvPr
        parent = blip_fill.getparent()
        while parent is not None:
            cNvPr = parent.find(".//{%s}cNvPr" % NS_P)
            if cNvPr is None:
                cNvPr = parent.find(".//{%s}cNvPr" % NS_A)
            if cNvPr is not None:
                descr = cNvPr.get("descr", "")
                if not descr:
                    name = cNvPr.get("name", "image")
                    issue("warning", "alt_text",
                          f"Image \"{name}\" is missing alt text (accessibility)")
                break
            parent = parent.getparent()

    # ------------------------------------------------------------------
    # 4. Empty slide check
    # ------------------------------------------------------------------
    has_text = False
    for t in tree.iter("{%s}t" % NS_A):
        if t.text and t.text.strip():
            has_text = True
            break
    if not has_text:
        issue("warning", "empty_slide", "Slide appears to have no visible text content")

    # ------------------------------------------------------------------
    # 5. Content density check
    #    Content slides must have ≥ min_chars of substantive text
    # ------------------------------------------------------------------
    cc = rules.get("content_constraints", {})
    if cc.get("enabled", False):
        # Count total substantive text characters (excluding whitespace-only runs)
        total_text_chars = 0
        for t in tree.iter("{%s}t" % NS_A):
            if t.text and t.text.strip():
                total_text_chars += len(t.text.strip())

        min_chars = cc.get("min_chars", 150)
        if total_text_chars > 0 and total_text_chars < min_chars:
            issue("warning", "content_density",
                  f"Low content density: ~{total_text_chars} chars (minimum {min_chars})")

    # ------------------------------------------------------------------
    # 6. Visual mandatory check
    #    Content slides must have at least one visual element
    # ------------------------------------------------------------------
    if cc.get("enabled", False) and cc.get("visual_mandatory", True):
        has_image = (any(True for _ in tree.iter("{%s}blipFill" % NS_A))
                     or any(True for _ in tree.iter("{%s}blipFill" % NS_P)))
        has_chart = any(True for _ in tree.iter(
            "{http://schemas.openxmlformats.org/drawingml/2006/chart}chart"))
        has_table = any(True for _ in tree.iter("{%s}tbl" % NS_A))

        # Count non-trivial shapes (rectangles, rounded rects, etc. used as visual elements)
        # Exclude tiny shapes (< 0.5" in both dimensions) which are likely decorative
        has_visual_shape = False
        for sp in tree.iter("{%s}sp" % NS_P):
            sp_pr = sp.find(".//{%s}spPr" % NS_P)
            if sp_pr is None:
                sp_pr = sp.find(".//{%s}spPr" % NS_A)
            if sp_pr is None:
                continue
            xfrm = sp_pr.find("{%s}xfrm" % NS_A)
            if xfrm is None:
                continue
            ext = xfrm.find("{%s}ext" % NS_A)
            if ext is None:
                continue
            w_in = _emu_to_in(ext.get("cx", "0"))
            h_in = _emu_to_in(ext.get("cy", "0"))
            # A shape ≥ 1.5" wide and ≥ 0.8" tall is likely a visual element
            if w_in >= 1.5 and h_in >= 0.8:
                # Check if it has a fill (not just a text box)
                solid_fill = sp_pr.find(".//{%s}solidFill" % NS_A)
                grad_fill = sp_pr.find(".//{%s}gradFill" % NS_A)
                if solid_fill is not None or grad_fill is not None:
                    has_visual_shape = True
                    break

        if not (has_image or has_chart or has_table or has_visual_shape):
            issue("warning", "visual_mandatory",
                  "No visual element found (chart, table, image, or shape). "
                  "Content slides must include at least one visual.")

    # ------------------------------------------------------------------
    # 7. Visual-text ratio check (approximate)
    #    Estimate area occupied by visual elements vs total content area
    # ------------------------------------------------------------------
    if cc.get("enabled", False):
        visual_area = 0.0
        total_content_area = 9.0 * 4.5  # approximate content area in sq inches (10"×5.625" minus margins)

        # Sum up areas of images, charts, tables, and large shapes
        for sp in tree.iter("{%s}sp" % NS_P):
            sp_pr = sp.find(".//{%s}spPr" % NS_P)
            if sp_pr is None:
                sp_pr = sp.find(".//{%s}spPr" % NS_A)
            if sp_pr is None:
                continue
            xfrm = sp_pr.find("{%s}xfrm" % NS_A)
            if xfrm is None:
                continue
            ext = xfrm.find("{%s}ext" % NS_A)
            if ext is None:
                continue
            w_in = _emu_to_in(ext.get("cx", "0"))
            h_in = _emu_to_in(ext.get("cy", "0"))
            if w_in >= 1.5 and h_in >= 0.8:
                solid_fill = sp_pr.find(".//{%s}solidFill" % NS_A)
                grad_fill = sp_pr.find(".//{%s}gradFill" % NS_A)
                if solid_fill is not None or grad_fill is not None:
                    visual_area += w_in * h_in

        # Add image areas
        for pic in tree.iter("{%s}pic" % NS_P):
            sp_pr = pic.find(".//{%s}spPr" % NS_P)
            if sp_pr is None:
                sp_pr = pic.find(".//{%s}spPr" % NS_A)
            if sp_pr is not None:
                xfrm = sp_pr.find("{%s}xfrm" % NS_A)
                if xfrm is not None:
                    ext = xfrm.find("{%s}ext" % NS_A)
                    if ext is not None:
                        w_in = _emu_to_in(ext.get("cx", "0"))
                        h_in = _emu_to_in(ext.get("cy", "0"))
                        visual_area += w_in * h_in

        min_ratio = cc.get("visual_ratio_min", 0.40)
        if total_content_area > 0 and visual_area / total_content_area < min_ratio:
            actual_ratio = visual_area / total_content_area
            issue("warning", "visual_text_ratio",
                  f"Low visual-text ratio: ~{actual_ratio:.0%} visual area "
                  f"(minimum {min_ratio:.0%})")

    # ------------------------------------------------------------------
    # 8. Whitespace ratio check
    #    Measures occupied area (shapes, images, tables) vs total content zone.
    #    Blank area = content zone area - occupied area.
    #    Includes empty space within shapes (shapes with fill but little text).
    # ------------------------------------------------------------------
    if cc.get("enabled", False):
        max_ws = cc.get("max_whitespace", 0.20)
        grid_zone_check = rules.get("grid_zone")

        # Skip cover/closing slides — detect by absence of nav-bar shapes in top zone
        _has_nav = False
        for _sp_nav in tree.iter("{%s}sp" % NS_P):
            _xf = _sp_nav.find(".//{%s}xfrm" % NS_A)
            if _xf is None:
                continue
            _off = _xf.find("{%s}off" % NS_A)
            _ext = _xf.find("{%s}ext" % NS_A)
            if _off is None or _ext is None:
                continue
            _ny = _emu_to_in(_off.get("y", "0"))
            _nh = _emu_to_in(_ext.get("cy", "0"))
            if _ny < 0.05 and 0.05 < _nh < 0.20:
                _has_nav = True
                break
        _skip_ws = not _has_nav

        # Content zone area
        if grid_zone_check:
            cz_w = grid_zone_check["x_max"] - grid_zone_check["x_min"]
            cz_h = grid_zone_check["y_max"] - grid_zone_check["y_min"]
            content_area_total = cz_w * cz_h
            cz_x_min = grid_zone_check["x_min"]
            cz_y_min = grid_zone_check["y_min"]
            cz_x_max = grid_zone_check["x_max"]
            cz_y_max = grid_zone_check["y_max"]
        else:
            content_area_total = 9.0 * 4.5
            cz_x_min, cz_y_min = 0.5, 0.75
            cz_x_max, cz_y_max = 9.5, 5.15

        # PIXEL-LEVEL CONTENT FILL CALCULATION
        # Instead of counting element bbox area, we rasterize the content zone
        # into a grid of cells and mark cells that contain actual visible content:
        #   - Text chars (with CJK/ASCII width) → fill cells char-by-char
        #   - Images → fill their entire bbox
        #   - Table cells with text → fill cell content area based on text
        #   - Filled shapes → fill their bbox (user sees solid color)
        # This reflects what the eye sees: gaps between elements, empty box
        # interiors, and padding around text all count as BLANK.
        grid_cols_n = int(round((cz_x_max - cz_x_min) * GRID_RES))
        grid_rows_n = int(round((cz_y_max - cz_y_min) * GRID_RES))
        # Boolean grid: True = occupied
        occ_grid = [[False] * grid_cols_n for _ in range(grid_rows_n)]

        def _mark_rect(ex, ey, ew, eh):
            """Mark cells within a bbox as occupied (clipped to content zone)."""
            cx1 = max(ex, cz_x_min); cy1 = max(ey, cz_y_min)
            cx2 = min(ex + ew, cz_x_max); cy2 = min(ey + eh, cz_y_max)
            if cx2 <= cx1 or cy2 <= cy1:
                return
            col1 = int((cx1 - cz_x_min) * GRID_RES)
            col2 = int(round((cx2 - cz_x_min) * GRID_RES))
            row1 = int((cy1 - cz_y_min) * GRID_RES)
            row2 = int(round((cy2 - cz_y_min) * GRID_RES))
            for r in range(row1, min(row2, grid_rows_n)):
                for c in range(col1, min(col2, grid_cols_n)):
                    occ_grid[r][c] = True

        def _mark_text(tx_body, bx, by, bw, bh):
            """Mark cells containing actual text glyphs (char-by-char, not full bbox)."""
            if tx_body is None:
                return
            # Usable width inside text box
            usable_w = max(0.05, bw - 0.08)
            cur_x = bx + 0.04
            cur_y = by + 0.04
            line_height = 0.15  # default, updated per paragraph
            for para in tx_body.iter("{%s}p" % NS_A):
                # Determine font size in this paragraph
                para_fs = 11.0
                for rpr in para.iter("{%s}rPr" % NS_A):
                    sz = rpr.get("sz")
                    if sz:
                        try:
                            para_fs = int(sz) / 100.0
                        except ValueError:
                            pass
                        break
                if para_fs == 11.0:
                    for epr in para.iter("{%s}endParaRPr" % NS_A):
                        sz = epr.get("sz")
                        if sz:
                            try:
                                para_fs = int(sz) / 100.0
                            except ValueError:
                                pass
                            break
                line_height = para_fs / 72.0 * PARA_LINE_HEIGHT_MULT
                # Glyph heights (the cells are marked at text baseline row, ~0.85× line height)
                glyph_h = para_fs / 72.0 * 1.1
                cjk_w = para_fs / 72.0 * CJK_CHAR_WIDTH
                ascii_w = para_fs / 72.0 * ASCII_CHAR_WIDTH
                # Concatenate text
                para_text = ""
                for t in para.iter("{%s}t" % NS_A):
                    if t.text:
                        para_text += t.text
                if not para_text:
                    cur_y += line_height
                    continue
                # Lay out characters line by line
                line_start_x = cur_x
                line_cur_x = cur_x
                for ch in para_text:
                    ch_w = cjk_w if ord(ch) > 0x2E80 else ascii_w
                    if line_cur_x + ch_w > bx + 0.04 + usable_w:
                        # Wrap: flush this line's marked cells, start new line
                        cur_y += line_height
                        line_cur_x = cur_x
                    # Mark the glyph bounds as occupied
                    _mark_rect(line_cur_x, cur_y, ch_w, glyph_h)
                    line_cur_x += ch_w
                    # Stop if we've flowed past the text box
                    if cur_y + glyph_h > by + bh + 0.5:
                        return
                cur_y += line_height

        # Two-pass approach:
        # Pass 1: collect all elements and classify them.
        # Pass 2: determine if fill-only shapes are real cards (covered by text)
        #         or blank decorations (no text overlay).
        elements = []  # list of dicts with bbox + classification
        for el in list(tree.iter("{%s}sp" % NS_P)) + list(tree.iter("{%s}pic" % NS_P)):
            sp_pr_ws = el.find("{%s}spPr" % NS_P)
            if sp_pr_ws is None:
                sp_pr_ws = el.find("{%s}spPr" % NS_A)
            if sp_pr_ws is None:
                sp_pr_ws = el.find(".//{%s}spPr" % NS_A)
            if sp_pr_ws is None:
                continue
            xfrm_ws = sp_pr_ws.find("{%s}xfrm" % NS_A)
            if xfrm_ws is None:
                continue
            off_ws = xfrm_ws.find("{%s}off" % NS_A)
            ext_ws = xfrm_ws.find("{%s}ext" % NS_A)
            if off_ws is None or ext_ws is None:
                continue
            ex = _emu_to_in(off_ws.get("x", "0"))
            ey = _emu_to_in(off_ws.get("y", "0"))
            ew = _emu_to_in(ext_ws.get("cx", "0"))
            eh = _emu_to_in(ext_ws.get("cy", "0"))
            if ew < 0.1 or eh < 0.05:
                continue
            if ey >= cz_y_max - 0.05 or ey + eh <= cz_y_min:
                continue

            has_image = (el.find(".//{%s}blipFill" % NS_A) is not None
                         or el.find(".//{%s}blipFill" % NS_P) is not None)
            has_fill = (sp_pr_ws.find("{%s}solidFill" % NS_A) is not None
                        or sp_pr_ws.find("{%s}gradFill" % NS_A) is not None)
            tx_body = el.find("{%s}txBody" % NS_P)
            if tx_body is None:
                tx_body = el.find(".//{%s}txBody" % NS_A)
            text_len = 0
            if tx_body is not None:
                text_len = sum(len((tt.text or "").strip()) for tt in tx_body.iter("{%s}t" % NS_A))

            elements.append({
                "x": ex, "y": ey, "w": ew, "h": eh,
                "has_image": has_image, "has_fill": has_fill,
                "text_len": text_len, "tx_body": tx_body,
            })

        # Pass 2: separate substantive-text boxes (standalone text)
        text_boxes = [e for e in elements
                      if e["text_len"] > 3 and not e["has_fill"] and not e["has_image"]]

        def _covers(shape, text):
            """Return True if shape is covered by text box (overlap > 50% of shape area)."""
            ox1 = max(shape["x"], text["x"])
            oy1 = max(shape["y"], text["y"])
            ox2 = min(shape["x"] + shape["w"], text["x"] + text["w"])
            oy2 = min(shape["y"] + shape["h"], text["y"] + text["h"])
            if ox2 <= ox1 or oy2 <= oy1:
                return False
            overlap = (ox2 - ox1) * (oy2 - oy1)
            shape_area = shape["w"] * shape["h"]
            return shape_area > 0 and overlap / shape_area >= 0.5

        for e in elements:
            if e["has_image"]:
                # Images always fill their bbox
                _mark_rect(e["x"], e["y"], e["w"], e["h"])
            elif e["has_fill"] and e["text_len"] == 0:
                # Fill-only shape: only count if genuinely covered by a text box.
                # Full-zone background (>70%) never counts.
                if e["w"] > cz_w * 0.7 and e["h"] > cz_h * 0.7:
                    continue  # full background, skip
                # Check if any text box covers this shape
                covering_text = None
                for tb in text_boxes:
                    if _covers(e, tb):
                        covering_text = tb
                        break
                if covering_text is not None:
                    # CARD HUG CHECK: compare shape dims against the text's
                    # TRUE required content height, not its declared bbox.
                    tb_w = covering_text["w"]
                    tb_y = covering_text["y"]
                    tb_x = covering_text["x"]
                    txt_true_h = _compute_textbox_required_height(
                        covering_text["tx_body"], tb_w
                    )
                    # Card h allowance: true height × 1.20 safety + 0.15" margin.
                    # Rationale: our estimator lags PowerPoint's actual layout by
                    # ~15-20% due to kerning, CJK width variance, and line-spacing.
                    # 0.15" ≈ 0.075" top/bottom padding for aesthetic breathing room.
                    max_allowed_h = txt_true_h * CARD_HUG_SAFETY + CARD_HUG_MARGIN
                    if e["h"] > max_allowed_h:
                        issue("error", "card_oversized",
                              f"Filled card at ({e['x']:.2f},{e['y']:.2f}) "
                              f"h={e['h']:.2f}\" exceeds true text height "
                              f"{txt_true_h:.2f}\" by "
                              f"{e['h'] - txt_true_h:.2f}\" (max allowed "
                              f"{max_allowed_h:.2f}\") — card should hug text")
                    # Text box h should also tightly match true content
                    if covering_text["h"] > max_allowed_h:
                        issue("error", "textbox_oversized",
                              f"Text box at ({tb_x:.2f},{tb_y:.2f}) "
                              f"h={covering_text['h']:.2f}\" exceeds true text "
                              f"height {txt_true_h:.2f}\" by "
                              f"{covering_text['h'] - txt_true_h:.2f}\"")
                    # Width check: text content usually fills the full width
                    # (unless it's very short). Only flag severe cases.
                    if e["w"] > tb_w + 0.40:
                        issue("error", "card_oversized",
                              f"Filled card at ({e['x']:.2f},{e['y']:.2f}) "
                              f"w={e['w']:.2f}\" exceeds text width {tb_w:.2f}\" "
                              f"by {e['w'] - tb_w:.2f}\" — card should hug text")
                    # Mark only the TRUE content portion as occupied, not full bbox.
                    # This prevents the oversized card from faking "filled" area.
                    mark_h = min(e["h"], txt_true_h + 0.20)
                    _mark_rect(e["x"], e["y"], e["w"], mark_h)
                # else: decorative fill without text overlay → counts as BLANK
            elif e["text_len"] > 3 and e["tx_body"] is not None:
                if e["has_fill"]:
                    # Filled shape with own embedded text — check hug + mark true portion
                    txt_true_h = _compute_textbox_required_height(e["tx_body"], e["w"])
                    max_allowed_h = txt_true_h * CARD_HUG_SAFETY + CARD_HUG_MARGIN
                    if e["h"] > max_allowed_h:
                        issue("error", "card_oversized",
                              f"Filled card at ({e['x']:.2f},{e['y']:.2f}) "
                              f"h={e['h']:.2f}\" exceeds true text height "
                              f"{txt_true_h:.2f}\" (max allowed "
                              f"{max_allowed_h:.2f}\") — card should hug text")
                    mark_h = min(e["h"], max_allowed_h)
                    _mark_rect(e["x"], e["y"], e["w"], mark_h)
                else:
                    # Pure text box: char-level marking
                    _mark_text(e["tx_body"], e["x"], e["y"], e["w"], e["h"])

        # Process tables (graphicFrame) — fill cell content areas based on cell text
        for gf in tree.iter("{%s}graphicFrame" % NS_P):
            xfrm_gf = gf.find("{%s}xfrm" % NS_P)
            if xfrm_gf is None:
                xfrm_gf = gf.find(".//{%s}xfrm" % NS_A)
            if xfrm_gf is None:
                continue
            off_gf = xfrm_gf.find("{%s}off" % NS_A)
            ext_gf = xfrm_gf.find("{%s}ext" % NS_A)
            if off_gf is None or ext_gf is None:
                continue
            gx = _emu_to_in(off_gf.get("x", "0"))
            gy = _emu_to_in(off_gf.get("y", "0"))
            gw = _emu_to_in(ext_gf.get("cx", "0"))
            gh_declared = _emu_to_in(ext_gf.get("cy", "0"))
            gh_true = _compute_table_true_height(gf)
            gh = max(gh_declared, gh_true) if gh_true else gh_declared
            # Tables: header rows are filled (primary color block), data rows count based on text
            # Simplification: mark entire table bbox (user sees table border + cell fills)
            _mark_rect(gx, gy, gw, gh)

        # Count occupied cells
        occupied_cells = sum(1 for r in occ_grid for c in r if c)
        total_cells = grid_rows_n * grid_cols_n
        occupied_area = (occupied_cells / total_cells) * content_area_total if total_cells > 0 else 0

        if content_area_total > 0 and not _skip_ws:
            blank_ratio = 1.0 - occupied_cells / max(1, total_cells)
            # Strict 20% limit for ALL slides (including those with images)
            if blank_ratio > max_ws + 0.005:
                issue("error", "whitespace_ratio",
                      f"Blank area {blank_ratio:.0%} exceeds maximum {max_ws:.0%} "
                      f"(pixel-level: {occupied_cells}/{total_cells} cells occupied, "
                      f"~{occupied_area:.1f} sq\" / {content_area_total:.1f} sq\")")

    # ------------------------------------------------------------------
    # 9. Text overflow (approximate)
    #    Heuristic: total characters in a text box vs. estimated capacity
    #    capacity ≈ (box_w_in × 10) × (box_h_in × 72 / font_size) characters per line × lines
    # ------------------------------------------------------------------
    if strict:
        for sp in tree.iter("{%s}sp" % NS_P):
            tx_body = sp.find(".//{%s}txBody" % NS_A)
            sp_pr = sp.find(".//{%s}spPr" % NS_P)
            if tx_body is None or sp_pr is None:
                continue

            xfrm = sp_pr.find("{%s}xfrm" % NS_A)
            if xfrm is None:
                continue
            ext = xfrm.find("{%s}ext" % NS_A)
            if ext is None:
                continue

            w_in = _emu_to_in(ext.get("cx", "0"))
            h_in = _emu_to_in(ext.get("cy", "0"))
            if w_in == 0 or h_in == 0:
                continue

            # Get dominant font size
            sizes = []
            for rpr in tx_body.iter("{%s}rPr" % NS_A):
                sz = rpr.get("sz")
                if sz:
                    try:
                        sizes.append(int(sz) / 100)
                    except ValueError:
                        pass
            font_size = sum(sizes) / len(sizes) if sizes else 14

            # Approximate capacity
            chars_per_line = max(1, int(w_in * 10))
            lines_available = max(1, int(h_in * 72 / (font_size * 1.4)))
            capacity = chars_per_line * lines_available

            # Count actual characters
            total_chars = sum(len(t.text or "") for t in tx_body.iter("{%s}t" % NS_A))

            if total_chars > capacity * 1.3:
                issue("warning", "text_overflow",
                      f"Text box may overflow: ~{total_chars} chars in box sized "
                      f"{w_in:.1f}\"×{h_in:.1f}\" (capacity ~{capacity})")

    # ------------------------------------------------------------------
    # 9. Content zone boundary check
    #    Elements must stay within the grid content zone.
    #    Checks all shapes (sp) and pictures (pic) with position info.
    # ------------------------------------------------------------------
    grid_zone = rules.get("grid_zone")
    if grid_zone:
        tolerance = 0.05  # allow 0.05" tolerance for rounding
        x_min = grid_zone["x_min"] - tolerance
        x_max = grid_zone["x_max"] + tolerance
        y_min = grid_zone["y_min"] - tolerance
        y_max = grid_zone["y_max"] + tolerance

        def _get_element_bounds(el):
            """Extract (x, y, w, h) in inches from a shape or picture element."""
            sp_pr = el.find(".//{%s}spPr" % NS_P)
            if sp_pr is None:
                sp_pr = el.find(".//{%s}spPr" % NS_A)
            if sp_pr is None:
                return None
            xfrm = sp_pr.find("{%s}xfrm" % NS_A)
            if xfrm is None:
                return None
            off = xfrm.find("{%s}off" % NS_A)
            ext = xfrm.find("{%s}ext" % NS_A)
            if off is None or ext is None:
                return None
            x = _emu_to_in(off.get("x", "0"))
            y = _emu_to_in(off.get("y", "0"))
            w = _emu_to_in(ext.get("cx", "0"))
            h = _emu_to_in(ext.get("cy", "0"))
            if w == 0 and h == 0:
                return None
            return (x, y, w, h)

        def _get_element_name(el):
            """Try to extract a human-readable name from the element."""
            for cnv in el.iter("{%s}cNvPr" % NS_P):
                return cnv.get("name", "")
            for cnv in el.iter("{%s}cNvPr" % NS_A):
                return cnv.get("name", "")
            return ""

        all_bounds = []  # list of (x, y, w, h, name) for overlap check

        # Collect bounds from shapes, pictures, AND graphicFrames (tables/charts)
        _all_elements = (list(tree.iter("{%s}sp" % NS_P))
                         + list(tree.iter("{%s}pic" % NS_P))
                         + list(tree.iter("{%s}graphicFrame" % NS_P)))

        for el in _all_elements:
            # graphicFrame uses p:xfrm, not a:xfrm
            bounds = _get_element_bounds(el)
            if bounds is None and el.tag == "{%s}graphicFrame" % NS_P:
                xfrm_gf2 = el.find("{%s}xfrm" % NS_P)
                if xfrm_gf2 is not None:
                    off_gf2 = xfrm_gf2.find("{%s}off" % NS_A)
                    ext_gf2 = xfrm_gf2.find("{%s}ext" % NS_A)
                    if off_gf2 is not None and ext_gf2 is not None:
                        gf_x = _emu_to_in(off_gf2.get("x", "0"))
                        gf_y = _emu_to_in(off_gf2.get("y", "0"))
                        gf_w = _emu_to_in(ext_gf2.get("cx", "0"))
                        gf_h_declared = _emu_to_in(ext_gf2.get("cy", "0"))
                        # Compute true rendered height from cell content
                        gf_h_true = _compute_table_true_height(el)
                        # Use the larger of declared and computed height
                        gf_h = max(gf_h_declared, gf_h_true) if gf_h_true else gf_h_declared
                        bounds = (gf_x, gf_y, gf_w, gf_h)
            if bounds is None:
                continue
            bx, by, bw, bh = bounds
            name = _get_element_name(el) or f"element@({bx:.2f},{by:.2f})"

            # Skip full-zone background fills: large filled shape covering >70% of content zone
            # with no text content — these are intentional bg layers, not content elements
            if bw > cz_w * 0.7 and bh > cz_h * 0.7:
                sp_pr_bg = el.find("{%s}spPr" % NS_P)
                if sp_pr_bg is None:
                    sp_pr_bg = el.find(".//{%s}spPr" % NS_A)
                has_bg_fill = False
                if sp_pr_bg is not None:
                    has_bg_fill = (sp_pr_bg.find("{%s}solidFill" % NS_A) is not None)
                tx_bg = el.find("{%s}txBody" % NS_P)
                if tx_bg is None:
                    tx_bg = el.find(".//{%s}txBody" % NS_A)
                bg_text_len = 0
                if tx_bg is not None:
                    bg_text_len = sum(len((tt.text or "").strip()) for tt in tx_bg.iter("{%s}t" % NS_A))
                if has_bg_fill and bg_text_len == 0:
                    continue  # skip background fill shape
            # Skip tiny decorative elements (nav tabs, divider lines, footer items)
            if bw < 0.3 and bh < 0.3:
                continue
            # Skip elements in the footer zone (y >= 5.15")
            if by >= grid_zone["y_max"] - 0.05:
                continue
            # Skip elements in the nav/title zone (y+h <= content zone y_min)
            # These are title bars and nav — not content elements
            if by + bh <= grid_zone["y_min"]:
                continue

            # TEXT OVERFLOW DETECTION: if this is a text box with substantive content,
            # compute REQUIRED rendered height. When declared bh < required, text
            # visually overflows into adjacent elements. Use required height as
            # effective bounds for overlap checks.
            effective_bh = bh
            if name.startswith("Text") and el.tag == "{%s}sp" % NS_P:
                req_h = _compute_textbox_required_height(el, bw)
                if req_h > bh + 0.05:
                    issue("error", "text_overflow",
                          f"\"{name}\" at y={by:.2f}\" h={bh:.2f}\" has content "
                          f"requiring ~{req_h:.2f}\" — text will visually overflow "
                          f"by {req_h - bh:.2f}\" into adjacent elements")
                    effective_bh = req_h

            all_bounds.append((bx, by, bw, effective_bh, name))

            # Check: does element breach content zone boundaries?
            breaches = []
            if bx < x_min:
                breaches.append(f"left edge x={bx:.2f}\" < zone x_min={grid_zone['x_min']:.2f}\"")
            if bx + bw > x_max:
                breaches.append(f"right edge x+w={bx+bw:.2f}\" > zone x_max={grid_zone['x_max']:.2f}\"")
            if by < y_min:
                breaches.append(f"top edge y={by:.2f}\" < zone y_min={grid_zone['y_min']:.2f}\"")
            if by + bh > y_max:
                breaches.append(f"bottom edge y+h={by+bh:.2f}\" > zone y_max={grid_zone['y_max']:.2f}\"")

            if breaches:
                issue("error", "content_zone_breach",
                      f"\"{name}\" at ({bx:.2f}\",{by:.2f}\",w={bw:.2f}\",h={bh:.2f}\") "
                      f"breaches content zone: {'; '.join(breaches)}")

        # ------------------------------------------------------------------
        # 10. Element overlap detection
        #     No two content elements may occupy the same pixel area.
        #
        #     IMPORTANT: "Text-on-Shape" is an intentional PptxGenJS pattern
        #     where addShape() provides a background fill and addText() at the
        #     same position provides the content. These are NOT real overlaps.
        #     We detect this by checking if one element is a filled shape and
        #     the other is text, and their bounding boxes are nearly identical
        #     or the text is fully contained within the shape.
        # ------------------------------------------------------------------
        def _is_text_on_shape(ax, ay, aw, ah, a_name, bx2, by2, bw2, bh2, b_name):
            """Return True if this pair is an intentional text-on-shape combo."""
            a_is_shape = a_name.startswith("Shape")
            b_is_shape = b_name.startswith("Shape")
            a_is_text = a_name.startswith("Text")
            b_is_text = b_name.startswith("Text")

            # Need one shape + one text (or shape + shape for callout bar + accent stripe)
            if not ((a_is_shape and b_is_text) or (a_is_text and b_is_shape)):
                # Also allow shape-on-shape if one is very thin (accent stripe)
                if a_is_shape and b_is_shape:
                    if min(aw, bw2) < 0.10 or min(ah, bh2) < 0.10:
                        return True
                return False

            # Identify which is shape and which is text
            if a_is_shape:
                sx, sy, sw, sh = ax, ay, aw, ah
                tx, ty, tw, th = bx2, by2, bw2, bh2
            else:
                sx, sy, sw, sh = bx2, by2, bw2, bh2
                tx, ty, tw, th = ax, ay, aw, ah

            # Text is contained within the shape (with tolerance)
            tol = 0.15
            if (tx >= sx - tol and ty >= sy - tol and
                    tx + tw <= sx + sw + tol and ty + th <= sy + sh + tol):
                return True

            return False

        for i in range(len(all_bounds)):
            ax, ay, aw, ah, a_name = all_bounds[i]
            for j in range(i + 1, len(all_bounds)):
                bx2, by2, bw2, bh2, b_name = all_bounds[j]
                # Intersection test
                if (ax < bx2 + bw2 and ax + aw > bx2 and
                        ay < by2 + bh2 and ay + ah > by2):
                    # Skip intentional text-on-shape combos
                    if _is_text_on_shape(ax, ay, aw, ah, a_name,
                                         bx2, by2, bw2, bh2, b_name):
                        continue

                    # Calculate overlap area
                    ox = max(ax, bx2)
                    oy = max(ay, by2)
                    ox2 = min(ax + aw, bx2 + bw2)
                    oy2 = min(ay + ah, by2 + bh2)
                    overlap_area = (ox2 - ox) * (oy2 - oy)
                    # Only flag if overlap is non-trivial (> 0.05 sq inches)
                    if overlap_area > 0.05:
                        issue("error", "element_overlap",
                              f"\"{a_name}\" and \"{b_name}\" overlap by "
                              f"{overlap_area:.2f} sq\" at region "
                              f"({ox:.2f}\",{oy:.2f}\")-({ox2:.2f}\",{oy2:.2f}\")")

    return issues


# ---------------------------------------------------------------------------
# Main linter
# ---------------------------------------------------------------------------

def lint_pptx(pptx_path: str, template_md_path: str, strict: bool = False) -> dict:
    """
    Run all linting checks on a PPTX against a template definition.

    Returns:
    {
        "pptx_path": str,
        "template": str,
        "slide_count": int,
        "issue_count": int,
        "error_count": int,
        "warning_count": int,
        "issues": [{"slide": int, "severity": str, "check": str, "message": str}, ...]
    }
    """
    pptx_path = Path(pptx_path)
    if not pptx_path.exists():
        raise FileNotFoundError(f"PPTX not found: {pptx_path}")

    template_rules = parse_template(template_md_path)
    all_issues = []
    slides_with_image = 0

    with zipfile.ZipFile(pptx_path, "r") as zf:
        names = zf.namelist()
        slide_files = sorted(
            [n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)],
            key=lambda x: int(re.search(r"\d+", Path(x).stem).group())
        )

        for position, slide_file in enumerate(slide_files, start=1):
            with zf.open(slide_file) as f:
                slide_xml = f.read()
            slide_issues = lint_slide(slide_xml, position, template_rules, strict=strict)
            all_issues.extend(slide_issues)

            # Deck-level metadata: does this slide contain a real image?
            slide_tree = etree.fromstring(slide_xml)
            if (any(True for _ in slide_tree.iter("{%s}blipFill" % NS_A))
                    or any(True for _ in slide_tree.iter("{%s}blipFill" % NS_P))):
                slides_with_image += 1

    slide_count = len(slide_files)

    # Deck-level checks
    if slide_count == 0:
        all_issues.append({
            "slide": 0, "severity": "error",
            "check": "slide_count", "message": "Presentation has no slides"
        })
    elif slide_count < 3:
        all_issues.append({
            "slide": 0, "severity": "warning",
            "check": "slide_count", "message": f"Very short deck: only {slide_count} slides"
        })

    # Image coverage: content-heavy templates require real images on a
    # majority of slides to avoid the "wall of text / shape-diagrams-only"
    # anti-pattern. Only enforced when the template enables it.
    cc = template_rules.get("content_constraints", {})
    if (cc.get("enabled", False) and cc.get("image_coverage_required", True)
            and slide_count > 0):
        required = cc.get("image_coverage_min", IMAGE_COVERAGE_MIN)
        actual = slides_with_image / slide_count
        if actual < required:
            all_issues.append({
                "slide": 0, "severity": "error",
                "check": "image_coverage",
                "message": (f"Only {slides_with_image}/{slide_count} slides "
                            f"({actual:.0%}) contain a real image; "
                            f"template requires ≥{required:.0%}")
            })

    error_count   = sum(1 for i in all_issues if i["severity"] == "error")
    warning_count = sum(1 for i in all_issues if i["severity"] == "warning")

    return {
        "pptx_path": str(pptx_path),
        "template": template_md_path,
        "slide_count": slide_count,
        "issue_count": len(all_issues),
        "error_count": error_count,
        "warning_count": warning_count,
        "issues": all_issues,
    }


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def format_human(result: dict) -> str:
    lines = []
    lines.append(f"=== Pro-PPTX Linter: {result['pptx_path']} ===")
    lines.append(f"Template: {result['template']}")
    lines.append(f"Slides:   {result['slide_count']}")
    lines.append(f"Issues:   {result['error_count']} errors, {result['warning_count']} warnings\n")

    if not result["issues"]:
        lines.append("✅ No issues found.")
        return "\n".join(lines)

    # Group by slide
    by_slide: dict = {}
    deck_issues = []
    for issue in result["issues"]:
        if issue["slide"] == 0:
            deck_issues.append(issue)
        else:
            by_slide.setdefault(issue["slide"], []).append(issue)

    if deck_issues:
        lines.append("Deck-level:")
        for issue in deck_issues:
            marker = "❌" if issue["severity"] == "error" else "⚠️ "
            lines.append(f"  {marker} [{issue['check']}] {issue['message']}")
        lines.append("")

    for slide_num in sorted(by_slide.keys()):
        lines.append(f"Slide {slide_num}:")
        # Deduplicate same check+message
        seen = set()
        for issue in by_slide[slide_num]:
            key = (issue["check"], issue["message"])
            if key in seen:
                continue
            seen.add(key)
            marker = "❌" if issue["severity"] == "error" else "⚠️ "
            lines.append(f"  {marker} [{issue['check']}] {issue['message']}")
        lines.append("")

    if result["error_count"] > 0:
        lines.append("❌ FAILED — fix all errors before delivery.")
    else:
        lines.append("✅ PASSED — warnings are advisory only.")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Lint a PPTX against a template definition")
    parser.add_argument("pptx", help="Path to PPTX file")
    parser.add_argument("--template", required=True, help="Path to template.md")
    parser.add_argument("--strict", action="store_true",
                        help="Enable strict checks (text overflow, etc.)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--exit-code", action="store_true",
                        help="Exit with code 1 if there are errors")
    args = parser.parse_args()

    try:
        result = lint_pptx(args.pptx, args.template, strict=args.strict)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_human(result))

    if args.exit_code and result["error_count"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
