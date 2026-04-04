#!/usr/bin/env python3
"""
Style Analyzer — extract visual styles from a PPTX and compare against templates.

Usage:
    # Analyze and find best matching template
    python scripts/style_analyzer.py input.pptx --templates-dir templates/

    # Analyze against a specific template
    python scripts/style_analyzer.py input.pptx --template templates/corporate/template.md

    # Output as JSON
    python scripts/style_analyzer.py input.pptx --templates-dir templates/ --json
"""

import argparse
import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path

try:
    import defusedxml.minidom as safe_minidom
    from lxml import etree
except ImportError:
    print("ERROR: Missing dependencies. Run: pip install defusedxml lxml", file=sys.stderr)
    sys.exit(1)

# OOXML namespaces
NS = {
    "a":  "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p":  "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r":  "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------

def extract_styles(pptx_path: str) -> dict:
    """
    Extract visual style profile from a PPTX file.

    Returns a dict with:
    - fonts: list of (typeface, count) tuples, sorted by frequency
    - colors: list of (hex, count) tuples, sorted by frequency
    - font_sizes: list of (pt_value, count) tuples
    - slide_count: int
    - layouts_used: list of layout file names referenced
    """
    pptx_path = Path(pptx_path)
    if not pptx_path.exists():
        raise FileNotFoundError(f"File not found: {pptx_path}")

    fonts: Counter = Counter()
    colors: Counter = Counter()
    font_sizes: Counter = Counter()
    layouts_used: list = []

    with zipfile.ZipFile(pptx_path, "r") as zf:
        names = zf.namelist()

        # Collect slide XML files
        slide_files = sorted(
            [n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n)]
        )
        slide_count = len(slide_files)

        for slide_file in slide_files:
            with zf.open(slide_file) as f:
                content = f.read()
            tree = etree.fromstring(content)

            # Font faces
            for rpr in tree.iter("{%s}rPr" % NS["a"]):
                latin = rpr.find("{%s}latin" % NS["a"])
                if latin is not None:
                    tf = latin.get("typeface", "")
                    if tf and not tf.startswith("+"):
                        fonts[tf] += 1

                # Font sizes (in hundredths of a point)
                sz = rpr.get("sz")
                if sz:
                    try:
                        font_sizes[int(sz) // 100] += 1
                    except ValueError:
                        pass

                # Solid fill colors on runs
                srgb = rpr.find(
                    ".//{%s}solidFill/{%s}srgbClr" % (NS["a"], NS["a"])
                )
                if srgb is None:
                    srgb = rpr.find("{%s}solidFill/{%s}srgbClr" % (NS["a"], NS["a"]))
                if srgb is not None:
                    val = srgb.get("val", "")
                    if val:
                        colors[val.upper()] += 1

            # Shape fill colors
            for solidFill in tree.iter("{%s}solidFill" % NS["a"]):
                srgb = solidFill.find("{%s}srgbClr" % NS["a"])
                if srgb is not None:
                    val = srgb.get("val", "")
                    if val:
                        colors[val.upper()] += 1

        # Layout references in slide .rels files
        rels_files = [n for n in names if re.match(r"ppt/slides/_rels/slide\d+\.xml\.rels$", n)]
        for rels_file in rels_files:
            with zf.open(rels_file) as f:
                content = f.read()
            tree = etree.fromstring(content)
            for rel in tree.iter("{%s}Relationship" % "http://schemas.openxmlformats.org/package/2006/relationships"):
                rel_type = rel.get("Type", "")
                if "slideLayout" in rel_type:
                    target = rel.get("Target", "")
                    layout_name = Path(target).name
                    if layout_name not in layouts_used:
                        layouts_used.append(layout_name)

    return {
        "slide_count": slide_count,
        "fonts": fonts.most_common(10),
        "colors": colors.most_common(20),
        "font_sizes": font_sizes.most_common(10),
        "layouts_used": layouts_used,
    }


# ---------------------------------------------------------------------------
# Template parsing
# ---------------------------------------------------------------------------

def parse_template_colors(template_md_path: str) -> list[str]:
    """Extract hex color values from a template.md file."""
    text = Path(template_md_path).read_text(encoding="utf-8")
    # Match patterns like #1A2B5F or bare 1A2B5F after a colon/space
    hex_values = re.findall(r"#([0-9A-Fa-f]{6})", text)
    return [h.upper() for h in set(hex_values)]


_NON_FONT_WORDS = {
    "navymid", "highlight", "text", "ink", "primary", "secondary", "accent",
    "muted", "border", "fill", "bold", "italic", "regular", "left", "center",
    "right", "top", "bottom", "white", "black", "base", "upside", "risk",
    "surface", "light", "dark", "medium", "color", "style",
}


def parse_template_fonts(template_md_path: str) -> list[str]:
    """Extract font names from a template.md Typography section."""
    text = Path(template_md_path).read_text(encoding="utf-8")
    # Restrict to the Typography block to avoid matching color variable names
    # (NavyMid, Highlight, Text, etc.) that appear in layout coordinate lines.
    typo_m = re.search(
        r"##\s+Typography\b(.*?)(?=\n##\s|\Z)", text, re.DOTALL | re.IGNORECASE
    )
    search_text = typo_m.group(1) if typo_m else text

    fonts = []
    for match in re.finditer(r"([A-Z][A-Za-z\s]+(?:/\s*[A-Z][A-Za-z\s]+)*),\s*\d+pt", search_text):
        for font in match.group(1).split("/"):
            f = font.strip()
            if f and len(f) > 2 and f.lower() not in _NON_FONT_WORDS:
                fonts.append(f)
    return list(dict.fromkeys(fonts))  # deduplicate preserving order


# ---------------------------------------------------------------------------
# Similarity scoring
# ---------------------------------------------------------------------------

def compute_similarity(extracted: dict, template_md_path: str) -> dict:
    """
    Compute a similarity score (0–100) between an extracted style profile
    and a template definition.

    Scoring components (equal weight):
    - Color overlap (40%): fraction of top-10 extracted colors that appear in the template palette
    - Font overlap (40%): fraction of extracted fonts that appear in the template font list
    - (Reserved for future) Layout overlap (20%): placeholder, scores 50% when not computed
    """
    template_colors = set(parse_template_colors(template_md_path))
    template_fonts_raw = parse_template_fonts(template_md_path)
    # Normalize font names to lowercase for comparison
    template_fonts = {f.lower() for f in template_fonts_raw}

    # Color score
    extracted_top_colors = {c for c, _ in extracted["colors"][:10]}
    if template_colors and extracted_top_colors:
        color_overlap = len(extracted_top_colors & template_colors) / len(extracted_top_colors)
    else:
        color_overlap = 0.0

    # Font score
    extracted_fonts = {f.lower() for f, _ in extracted["fonts"]}
    if template_fonts and extracted_fonts:
        font_overlap = len(extracted_fonts & template_fonts) / len(extracted_fonts)
    else:
        font_overlap = 0.0

    # Combined score
    score = round((color_overlap * 40 + font_overlap * 40 + 50 * 0.2), 1)
    score = min(100.0, score)

    return {
        "score": score,
        "template": template_md_path,
        "color_overlap": round(color_overlap * 100, 1),
        "font_overlap": round(font_overlap * 100, 1),
        "template_colors": sorted(template_colors),
        "template_fonts": template_fonts_raw,
    }


def find_best_template(pptx_path: str, templates_dir: str) -> dict:
    """
    Find the best-matching template for a PPTX file.

    Returns:
    {
        "best_match": { "template": "...", "score": 87.5, ... },
        "all_scores": [ ... ],
        "recommendation": "align" | "preserve",
        "extracted": { ... }
    }
    """
    extracted = extract_styles(pptx_path)

    templates_dir = Path(templates_dir)
    template_files = list(templates_dir.glob("*/template.md"))

    if not template_files:
        return {
            "best_match": None,
            "all_scores": [],
            "recommendation": "preserve",
            "extracted": extracted,
        }

    scores = [compute_similarity(extracted, str(t)) for t in template_files]
    scores.sort(key=lambda x: x["score"], reverse=True)

    best = scores[0]
    recommendation = "align" if best["score"] >= 80 else "preserve"

    return {
        "best_match": best,
        "all_scores": scores,
        "recommendation": recommendation,
        "extracted": extracted,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def format_human(result: dict) -> str:
    lines = []
    extracted = result["extracted"]

    lines.append(f"=== Style Analysis: {result.get('pptx_path', '')} ===")
    lines.append(f"Slides: {extracted['slide_count']}")

    lines.append("\nTop Fonts:")
    for font, count in extracted["fonts"][:5]:
        lines.append(f"  {font} ({count} uses)")

    lines.append("\nTop Colors:")
    for color, count in extracted["colors"][:8]:
        lines.append(f"  #{color} ({count} uses)")

    lines.append("\nTop Font Sizes:")
    for size, count in extracted["font_sizes"][:5]:
        lines.append(f"  {size}pt ({count} uses)")

    if result.get("best_match"):
        bm = result["best_match"]
        lines.append(f"\n=== Template Match ===")
        lines.append(f"Best match: {bm['template']}")
        lines.append(f"Score:      {bm['score']}%  (color: {bm['color_overlap']}%, font: {bm['font_overlap']}%)")

        rec = result["recommendation"]
        if rec == "align":
            lines.append(f"\n✅ RECOMMENDATION: Auto-align to this template (score ≥ 80%)")
        else:
            lines.append(f"\n⚠️  RECOMMENDATION: Preserve original style (score < 80% — no close template match)")

        if len(result["all_scores"]) > 1:
            lines.append("\nAll template scores:")
            for s in result["all_scores"]:
                lines.append(f"  {Path(s['template']).parent.name:20s}  {s['score']:5.1f}%")

    elif result.get("template"):
        s = result["similarity"]
        lines.append(f"\n=== Similarity to {result['template']} ===")
        lines.append(f"Score: {s['score']}%  (color: {s['color_overlap']}%, font: {s['font_overlap']}%)")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Analyze PPTX style and compare to templates")
    parser.add_argument("pptx", help="Path to input PPTX file")
    parser.add_argument("--templates-dir", help="Directory containing template folders")
    parser.add_argument("--template", help="Path to a specific template.md to compare against")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    try:
        if args.templates_dir:
            result = find_best_template(args.pptx, args.templates_dir)
            result["pptx_path"] = args.pptx
        elif args.template:
            extracted = extract_styles(args.pptx)
            similarity = compute_similarity(extracted, args.template)
            result = {
                "pptx_path": args.pptx,
                "template": args.template,
                "extracted": extracted,
                "similarity": similarity,
            }
        else:
            extracted = extract_styles(args.pptx)
            result = {"pptx_path": args.pptx, "extracted": extracted}

        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            print(format_human(result))

    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
