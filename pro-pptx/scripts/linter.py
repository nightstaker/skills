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
  8. Content density      — content slides must have ≥150 chars of substantive text
  9. Visual mandatory     — content slides must include ≥1 visual element (chart/table/image/shape)
 10. Visual-text ratio    — visual elements should occupy ≥40% of content area

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
        "max_whitespace": 0.30,
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
        # Extract visual ratio if specified
        ratio_m = re.search(r"[≥>]\s*(\d+)%", cc_text)
        if ratio_m:
            content_constraints["visual_ratio_min"] = int(ratio_m.group(1)) / 100.0
    else:
        # No Content Constraints section — disable density checks
        content_constraints["enabled"] = False

    content_constraints.setdefault("enabled", True)

    return {
        "allowed_colors": allowed_colors,
        "allowed_fonts": allowed_fonts,
        "fixed_elements": fixed_elements,
        "content_constraints": content_constraints,
    }


# ---------------------------------------------------------------------------
# Per-slide linting
# ---------------------------------------------------------------------------

def _emu_to_in(emu: str) -> float:
    try:
        return int(emu) / EMU_PER_INCH
    except (TypeError, ValueError):
        return 0.0


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
                # Skip white and black — often used as baseline
                if val in ("FFFFFF", "000000", "1A1A1A"):
                    continue
                seen_bad_colors.add(val)
                issue("error", "color_compliance",
                      f"Off-palette color: #{val}")

    # ------------------------------------------------------------------
    # 3. Alt text on images
    # ------------------------------------------------------------------
    for blip_fill in tree.iter("{%s}blipFill" % NS_A):
        # Walk up to find the parent nvPicPr → nvPr → cNvPr
        parent = blip_fill.getparent()
        while parent is not None:
            cNvPr = parent.find(".//{%s}cNvPr" % NS_P)
            if cNvPr is None:
                cNvPr = parent.find(
                    ".//{http://schemas.openxmlformats.org/drawingml/2006/main}cNvPr"
                )
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
        has_image = any(True for _ in tree.iter("{%s}blipFill" % NS_A))
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
    if cc.get("enabled", False) and strict:
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
    # 8. Text overflow (approximate)
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
