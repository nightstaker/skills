#!/usr/bin/env python3
"""
Content Tree Builder — parse a PPTX into a chapter→slide→element hierarchy.

Usage:
    python scripts/content_tree.py input.pptx
    python scripts/content_tree.py input.pptx --output content.json
    python scripts/content_tree.py input.pptx --markdown   # human-readable outline
    python scripts/content_tree.py input.pptx --slide-ids  # print slide ID table only
"""

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any

try:
    from lxml import etree
except ImportError:
    print("ERROR: Missing lxml. Run: pip install lxml", file=sys.stderr)
    sys.exit(1)

# OOXML namespaces
NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


# ---------------------------------------------------------------------------
# Slide ID extraction
# ---------------------------------------------------------------------------

def extract_slide_ids(pptx_path: str) -> list[dict]:
    """
    Extract ordered slide IDs from ppt/presentation.xml.

    Returns list of:
    {
        "position": 1,          # 1-indexed order in the deck
        "id": 256,              # numeric sldId attribute
        "rid": "rId2",          # relationship ID
        "slide_file": "ppt/slides/slide1.xml"  # resolved path
    }
    """
    pptx_path = Path(pptx_path)
    result = []

    with zipfile.ZipFile(pptx_path, "r") as zf:
        # Parse presentation.xml
        with zf.open("ppt/presentation.xml") as f:
            prs = etree.fromstring(f.read())

        # Parse presentation.xml.rels to map rId → slide file
        try:
            with zf.open("ppt/_rels/presentation.xml.rels") as f:
                rels_tree = etree.fromstring(f.read())
        except KeyError:
            return result

        rid_to_target = {}
        for rel in rels_tree.iter(
            "{http://schemas.openxmlformats.org/package/2006/relationships}Relationship"
        ):
            rel_type = rel.get("Type", "")
            if "slide" in rel_type and "slideLayout" not in rel_type and "slideMaster" not in rel_type:
                rid_to_target[rel.get("Id")] = rel.get("Target", "")

        # Walk <p:sldIdLst>
        sld_id_lst = prs.find("{%s}sldIdLst" % NS_P)
        if sld_id_lst is None:
            return result

        for position, sld_id_elem in enumerate(sld_id_lst, start=1):
            sid = sld_id_elem.get("id")
            rid = sld_id_elem.get("{%s}id" % NS_R)
            target = rid_to_target.get(rid, "")
            # Normalize path
            if target.startswith("../"):
                slide_file = "ppt/" + target[3:]
            elif not target.startswith("ppt/"):
                slide_file = "ppt/slides/" + Path(target).name
            else:
                slide_file = target

            result.append({
                "position": position,
                "id": int(sid) if sid else None,
                "rid": rid,
                "slide_file": slide_file,
            })

    return result


# ---------------------------------------------------------------------------
# Per-slide content extraction
# ---------------------------------------------------------------------------

def _get_text_runs(elem) -> str:
    """Concatenate all <a:t> text under an element."""
    parts = []
    for t in elem.iter("{%s}t" % NS_A):
        parts.append(t.text or "")
    return "".join(parts).strip()


def _classify_layout(slide_xml: bytes, layout_name: str = "") -> str:
    """Infer layout type from slide XML structure."""
    tree = etree.fromstring(slide_xml)
    sp_trees = list(tree.iter("{%s}spTree" % NS_P))
    if not sp_trees:
        return "unknown"

    # Count text boxes and placeholder types
    placeholders = {}
    for ph in tree.iter("{%s}ph" % NS_P):
        ph_type = ph.get("type", "body")
        ph_idx = ph.get("idx", "0")
        placeholders[ph_idx] = ph_type

    text_boxes = sum(1 for _ in tree.iter("{%s}txBody" % NS_A))
    images = sum(1 for _ in tree.iter("{%s}blipFill" % NS_A))
    charts = sum(1 for _ in tree.iter("{%s}chart" % "http://schemas.openxmlformats.org/drawingml/2006/chart"))

    if charts > 0 or "table" in str(etree.tostring(tree)):
        return "data"
    if images >= 2:
        return "image-focus"
    if text_boxes >= 4:
        return "two-column"

    # Title + single content block
    title_types = {"title", "ctrTitle"}
    has_title = any(v in title_types for v in placeholders.values())
    if has_title and text_boxes <= 2:
        return "content"

    return "content"


def extract_slide_content(slide_xml: bytes) -> dict:
    """
    Extract all textual content and element types from a slide's XML.

    Returns:
    {
        "title": str,
        "elements": [{"type": "bullet|text|table|chart", "level": int, "text": str}, ...]
    }
    """
    tree = etree.fromstring(slide_xml)
    title = ""
    elements = []

    for sp in tree.iter("{%s}sp" % NS_P):
        ph = sp.find(".//{%s}ph" % NS_P)
        tx_body = sp.find(".//{%s}txBody" % NS_A)
        if tx_body is None:
            continue

        ph_type = ph.get("type", "body") if ph is not None else "body"

        if ph_type in ("title", "ctrTitle"):
            title = _get_text_runs(tx_body)
            continue

        # Walk paragraphs
        for para in tx_body.iter("{%s}p" % NS_A):
            text = _get_text_runs(para)
            if not text:
                continue

            # Detect indent level
            pPr = para.find("{%s}pPr" % NS_A)
            indent_level = 0
            if pPr is not None:
                lvl = pPr.get("lvl")
                if lvl:
                    indent_level = int(lvl)

            # Detect bullet
            has_bullet = (
                pPr is not None and (
                    pPr.find("{%s}buChar" % NS_A) is not None
                    or pPr.find("{%s}buAutoNum" % NS_A) is not None
                )
            )

            elem_type = "bullet" if has_bullet else "text"
            elements.append({"type": elem_type, "level": indent_level, "text": text})

    # Detect tables
    for tbl in tree.iter("{%s}tbl" % NS_A):
        rows = []
        for tr in tbl.iter("{%s}tr" % NS_A):
            row = []
            for tc in tr.iter("{%s}tc" % NS_A):
                row.append(_get_text_runs(tc))
            rows.append(row)
        elements.append({"type": "table", "level": 0, "rows": rows, "text": "[table]"})

    # Detect charts
    for _ in tree.iter("{http://schemas.openxmlformats.org/drawingml/2006/chart}chart"):
        elements.append({"type": "chart", "level": 0, "text": "[embedded chart]"})

    # Detect images
    image_count = sum(1 for _ in tree.iter("{%s}blipFill" % NS_A))

    # Count visual elements for density metrics
    visual_count = (
        image_count
        + sum(1 for e in elements if e["type"] in ("chart", "table"))
    )

    # Count substantive text characters
    total_chars = sum(len(e.get("text", "")) for e in elements if e["type"] in ("text", "bullet"))

    metrics = {
        "total_chars": total_chars,
        "element_count": len(elements),
        "image_count": image_count,
        "visual_count": visual_count,
        "has_visual": visual_count > 0,
    }

    return {"title": title, "elements": elements, "metrics": metrics}


# ---------------------------------------------------------------------------
# Full tree builder
# ---------------------------------------------------------------------------

def build_content_tree(pptx_path: str) -> dict:
    """
    Build the full chapter→slide→element tree for a PPTX file.

    Returns:
    {
        "meta": {"title": str, "slide_count": int, "pptx_path": str},
        "slides": [
            {
                "id": 256,
                "position": 1,
                "slide_file": "ppt/slides/slide1.xml",
                "layout": "cover",
                "title": "...",
                "elements": [...]
            },
            ...
        ]
    }
    """
    pptx_path = str(pptx_path)
    slide_ids = extract_slide_ids(pptx_path)
    slides = []

    with zipfile.ZipFile(pptx_path, "r") as zf:
        for entry in slide_ids:
            slide_file = entry["slide_file"]
            try:
                with zf.open(slide_file) as f:
                    slide_xml = f.read()
            except KeyError:
                continue

            content = extract_slide_content(slide_xml)
            layout = _classify_layout(slide_xml)

            slides.append({
                "id": entry["id"],
                "position": entry["position"],
                "slide_file": slide_file,
                "layout": layout,
                "title": content["title"],
                "elements": content["elements"],
                "metrics": content.get("metrics", {}),
            })

    # Try to get deck title from presentation.xml
    deck_title = ""
    try:
        with zipfile.ZipFile(pptx_path, "r") as zf:
            names = zf.namelist()
            if "docProps/core.xml" in names:
                with zf.open("docProps/core.xml") as f:
                    core = etree.fromstring(f.read())
                dc_ns = "http://purl.org/dc/elements/1.1/"
                title_elem = core.find("{%s}title" % dc_ns)
                if title_elem is not None and title_elem.text:
                    deck_title = title_elem.text
    except Exception:
        pass

    if not deck_title and slides:
        deck_title = slides[0].get("title", "")

    return {
        "meta": {
            "title": deck_title,
            "slide_count": len(slides),
            "pptx_path": pptx_path,
        },
        "slides": slides,
    }


# ---------------------------------------------------------------------------
# Markdown outline formatter
# ---------------------------------------------------------------------------

def format_markdown(tree: dict) -> str:
    lines = []
    meta = tree["meta"]
    lines.append(f"# Deck Outline: {meta['title']}")
    lines.append(f"**Slides**: {meta['slide_count']}  |  **Source**: {meta['pptx_path']}\n")

    for slide in tree["slides"]:
        title = slide["title"] or "(no title)"
        lines.append(f"## Slide {slide['position']} — {title}")
        metrics = slide.get("metrics", {})
        metrics_str = ""
        if metrics:
            chars = metrics.get("total_chars", 0)
            visuals = metrics.get("visual_count", 0)
            has_vis = "✓" if metrics.get("has_visual", False) else "✗"
            metrics_str = f" | Chars: {chars} | Visuals: {visuals} ({has_vis})"
        lines.append(f"*ID: {slide['id']} | Layout: {slide['layout']}{metrics_str}*\n")

        for elem in slide["elements"]:
            indent = "  " * elem.get("level", 0)
            text = elem.get("text", "")
            etype = elem.get("type", "text")

            if etype == "bullet":
                lines.append(f"{indent}- {text}")
            elif etype == "table":
                lines.append(f"{indent}[TABLE: {len(elem.get('rows', []))} rows]")
            elif etype == "chart":
                lines.append(f"{indent}[CHART]")
            else:
                lines.append(f"{indent}{text}")

        lines.append("")

    return "\n".join(lines)


def format_slide_id_table(tree: dict) -> str:
    lines = []
    lines.append(f"{'Pos':>4}  {'ID':>6}  {'Layout':15}  {'Chars':>5}  {'Vis':>3}  Title")
    lines.append("-" * 80)
    for slide in tree["slides"]:
        title = (slide["title"] or "(no title)")[:35]
        metrics = slide.get("metrics", {})
        chars = metrics.get("total_chars", 0)
        vis = metrics.get("visual_count", 0)
        lines.append(
            f"{slide['position']:>4}  {slide['id'] or '?':>6}  "
            f"{slide['layout']:15}  {chars:>5}  {vis:>3}  {title}"
        )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Parse PPTX into content tree")
    parser.add_argument("pptx", help="Path to input PPTX file")
    parser.add_argument("--output", "-o", help="Save JSON to this file")
    parser.add_argument("--markdown", action="store_true", help="Print as Markdown outline")
    parser.add_argument("--slide-ids", action="store_true", help="Print slide ID table only")
    args = parser.parse_args()

    if not Path(args.pptx).exists():
        print(f"ERROR: File not found: {args.pptx}", file=sys.stderr)
        sys.exit(1)

    tree = build_content_tree(args.pptx)

    if args.slide_ids:
        print(format_slide_id_table(tree))
    elif args.markdown:
        print(format_markdown(tree))
    elif args.output:
        Path(args.output).write_text(json.dumps(tree, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Content tree saved to: {args.output}")
        print(format_slide_id_table(tree))  # Also print summary
    else:
        print(json.dumps(tree, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
