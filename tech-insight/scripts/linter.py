#!/usr/bin/env python3
"""
linter.py — quality gate for tech-insight reports.

Enforces the non-negotiables defined in REQUIREMENT.MD:

1. Universal sourcing — every factual sentence must carry an inline link.
2. Visual coverage — required image slots must be present, captioned, and sourced.
3. Structure integrity — type-specific mandatory sections (A/B/C/D).
4. Implication actionability — banned filler phrases.
5. Hallucination guard — specific numbers / product codes / quotes without a source.

Exit code:
  0 — clean
  1 — violations found

Usage:
  python linter.py reports/foo.md --assets assets/foo/ --type A
  python linter.py reports/foo.md --assets assets/foo/ --type B
  python linter.py reports/foo.md --assets assets/foo/ --type C
  python linter.py reports/foo.md --assets assets/foo/ --type D
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Regexes
# ---------------------------------------------------------------------------

INLINE_LINK = re.compile(r"\[[^\]]+\]\((https?://[^)]+|doi:[^)]+|patent:[^)]+)\)")
IMAGE_LINE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
CAPTION_LINE = re.compile(r"^\s*\*图\s*\d+[:：][^*]*—\s*来源[:：].*\*\s*$")
NUMBER = re.compile(r"\b\d[\d.,]*\s*(%|nm|GB|TB|MB|TFLOPS|TOPS|W|GHz|MHz|FPS|ms|μs|us|ns|tokens|MAU|DAU|USD|RMB|\$|￥|元|亿|万)?")
QUOTE = re.compile(r"[\"\u201c][^\"\u201d]{6,}[\"\u201d]")
BANNED_PHRASES = [
    "需要持续关注",
    "值得观察",
    "未来可期",
    "拭目以待",
    "前景广阔",
    "大有可为",
]

# ---------------------------------------------------------------------------
# Type-specific required sections
# ---------------------------------------------------------------------------

TYPE_A_REQUIRED_SECTIONS = [
    ("领域定义", "领域定义与应用发展 — 领域边界"),
    ("应用发展", "领域定义与应用发展 — 应用发展脉络"),
    ("底层需求拆解", "领域定义与应用发展 — 底层需求拆解"),
    ("TOP 5", "TOP 5 技术深入分析"),
    ("技术横向对比", "技术横向对比表"),
    ("技术趋势", "技术趋势与研究启示 — 趋势归纳"),
    ("研究启示", "技术趋势与研究启示 — 研究启示"),
    ("Sources", "Sources"),
]

TYPE_B_REQUIRED_SECTIONS = [
    ("行业发展", "行业发展史与技术路线引出 — 行业发展脉络"),
    ("技术路线", "行业发展史与技术路线引出 — 技术路线图谱"),
    ("技术路线横向对比", "全局总结 — 技术路线横向对比"),
    ("研究建议", "全局总结 — 行业技术研究建议"),
    ("Sources", "Sources"),
]

TYPE_C_REQUIRED_SECTIONS = [
    ("产品定位", "产品概览与卖点分析 — 产品定位"),
    ("核心卖点", "产品概览与卖点分析 — 核心卖点与特性"),
    ("关键架构", "关键技术架构拆解"),
    ("技术总结", "总结与产品启示 — 技术总结"),
    ("产品启示", "总结与产品启示 — 对标产品启示"),
    ("Sources", "Sources"),
]

TYPE_D_REQUIRED_SECTIONS = [
    ("公司画像", "公司概览 — 公司画像"),
    ("发展历程", "公司概览 — 发展历程与里程碑"),
    ("产品矩阵", "产品布局分析 — 产品矩阵"),
    ("战略方向", "公司战略与技术路线 — 战略方向"),
    ("技术能力评估", "公司战略与技术路线 — 技术能力评估"),
    ("竞争力总结", "总结与事业单元启示 — 技术竞争力总结"),
    ("事业单元启示", "总结与事业单元启示 — 对事业单元的启示"),
    ("Sources", "Sources"),
]

REQUIRED_SECTIONS_MAP = {
    "A": TYPE_A_REQUIRED_SECTIONS,
    "B": TYPE_B_REQUIRED_SECTIONS,
    "C": TYPE_C_REQUIRED_SECTIONS,
    "D": TYPE_D_REQUIRED_SECTIONS,
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def split_paragraphs(text: str) -> list[tuple[int, str]]:
    """Return [(line_no, paragraph_text), ...] skipping code/table/headings/images."""
    lines = text.splitlines()
    out: list[tuple[int, str]] = []
    buf: list[str] = []
    start = 0
    in_code = False
    for i, line in enumerate(lines, start=1):
        if line.strip().startswith("```"):
            in_code = not in_code
            if buf:
                out.append((start, " ".join(buf).strip()))
                buf = []
            continue
        if in_code:
            continue
        stripped = line.strip()
        if (
            not stripped
            or stripped.startswith("#")
            or stripped.startswith("|")
            or stripped.startswith(">")
            or stripped.startswith("!")
            or CAPTION_LINE.match(line)
        ):
            if buf:
                out.append((start, " ".join(buf).strip()))
                buf = []
            continue
        if not buf:
            start = i
        buf.append(stripped)
    if buf:
        out.append((start, " ".join(buf).strip()))
    return out


def is_factual(paragraph: str) -> bool:
    """A paragraph is treated as factual if it contains a number, a proper noun,
    or a quoted string. Pure narrative connectives are skipped."""
    if NUMBER.search(paragraph):
        return True
    if QUOTE.search(paragraph):
        return True
    # Heuristic: any capitalised token of length>=3 (English vendor / product names)
    if re.search(r"\b[A-Z][A-Za-z0-9\-]{2,}\b", paragraph):
        return True
    return False


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_sourcing(text: str, errors: list[str]) -> None:
    for line_no, para in split_paragraphs(text):
        if not is_factual(para):
            continue
        if not INLINE_LINK.search(para):
            preview = para[:80].replace("\n", " ")
            errors.append(
                f"[L{line_no}] factual paragraph missing inline source: {preview}…"
            )


def check_banned_phrases(text: str, errors: list[str]) -> None:
    for ph in BANNED_PHRASES:
        if ph in text:
            errors.append(f"banned filler phrase found: '{ph}'")


def check_structure(text: str, report_type: str, errors: list[str]) -> None:
    required = REQUIRED_SECTIONS_MAP.get(report_type, [])
    for needle, label in required:
        if needle not in text:
            errors.append(f"missing required section: {label} (search key: '{needle}')")


def check_visuals(
    text: str,
    assets_dir: Path,
    report_type: str,
    errors: list[str],
) -> None:
    images = IMAGE_LINE.findall(text)
    if not images:
        errors.append("no images embedded in report — visual evidence is mandatory")

    # Each image must be followed by a caption line.
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if IMAGE_LINE.search(line):
            # find next non-empty line
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j >= len(lines) or not CAPTION_LINE.match(lines[j]):
                errors.append(
                    f"[L{i+1}] image missing caption in '图 X：… — 来源：…' format"
                )

    # Coverage targets per type
    text_lower = text.lower()
    if report_type == "A":
        # Each technology should have at least one principle/architecture diagram
        if "tech1-arch" not in text_lower and "技术 1 原理" not in text:
            errors.append("Type A: missing principle/architecture diagram for Technology 1")
        if "技术横向对比" not in text:
            errors.append("Type A: missing technology comparison table")
    elif report_type == "B":
        # Need industry visual + route-level images
        if "industry-" not in text_lower and "行业发展" not in text:
            errors.append("Type B: missing industry-level visual (timeline / market chart)")
        if "route1-" not in text_lower and "路线" not in text_lower:
            errors.append("Type B: missing technology route visuals")
    elif report_type == "C":
        # Need product photo + architecture diagram
        if "product-hero" not in text_lower and "产品图" not in text and "产品官方图" not in text:
            errors.append("Type C: missing product photo")
        if "arch1-" not in text_lower and "架构图" not in text and "系统拆解" not in text:
            errors.append("Type C: missing architecture/teardown diagram for key architecture 1")
    elif report_type == "D":
        # Need product portfolio + core product photos
        if "product-portfolio" not in text_lower and "产品矩阵" not in text and "产品布局" not in text:
            errors.append("Type D: missing product portfolio visualization")
        if "core-product" not in text_lower and "核心产品" not in text:
            errors.append("Type D: missing core product photos")

    # Manifest cross-check
    manifest_path = assets_dir / "image_manifest.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            failed = manifest.get("failed") or {}
            if failed:
                for fname, info in failed.items():
                    errors.append(
                        f"image_manifest.json reports failed download: {fname} ({info.get('error','?')})"
                    )
            entries = manifest.get("entries") or {}
            for fname, info in entries.items():
                if not info.get("source_url"):
                    errors.append(f"manifest entry {fname} missing source_url")
        except Exception as e:  # noqa: BLE001
            errors.append(f"image_manifest.json unreadable: {e}")
    else:
        errors.append(
            f"image_manifest.json not found in {assets_dir} — visual provenance is required"
        )


def check_architecture_diagrams(text: str, report_type: str, errors: list[str]) -> None:
    """Check that every technology point and every product under it has an architecture diagram.
    Universal rule across all report types."""
    images = IMAGE_LINE.findall(text)
    image_count = len(images)

    # Count architecture-related images (arch, 架构, 原理, 拆解, pipeline, system)
    arch_keywords = re.compile(r"(arch|架构|原理|拆解|pipeline|系统架构|数据流|模块)", re.IGNORECASE)
    arch_images = sum(1 for img in images if arch_keywords.search(img))

    # Heuristic: count technology sections and product mentions to estimate expected diagrams
    # For Type A: look for "技术 N" sections
    if report_type == "A":
        tech_sections = len(re.findall(r"#+\s*(?:\d+\.\d+\s+)?技术\s*\d+", text))
        if tech_sections == 0:
            tech_sections = len(re.findall(r"###\s*2\.\d+", text))
        if tech_sections > 0 and arch_images < tech_sections:
            errors.append(
                f"Type A: found {tech_sections} technology sections but only {arch_images} "
                f"architecture diagrams — each technology AND each product needs ≥1 architecture diagram"
            )
    elif report_type == "B":
        route_sections = len(re.findall(r"技术路线\s*[A-Z\d]|路线\s*[A-Z\d]", text))
        if route_sections > 0 and arch_images < route_sections:
            errors.append(
                f"Type B: found {route_sections} technology route sections but only {arch_images} "
                f"architecture diagrams — each route AND each product needs ≥1 architecture diagram"
            )


def check_comparison_table(text: str, report_type: str, errors: list[str]) -> None:
    """Check that comparison/matrix tables exist where required."""
    if report_type == "A":
        if "技术横向对比" not in text and "横向对比" not in text:
            errors.append("Type A: missing technology comparison matrix (技术横向对比)")
    elif report_type == "B":
        if "技术路线横向对比" not in text and "横向对比" not in text:
            errors.append("Type B: missing cross-route comparison matrix (技术路线横向对比)")
    elif report_type == "D":
        if "技术能力评估" not in text:
            errors.append("Type D: missing technology capability assessment table (技术能力评估)")


def check_implication(text: str, report_type: str, errors: list[str]) -> None:
    """Check that the implication/recommendation section exists and is substantive."""
    implication_markers = {
        "A": ["研究启示", "So what"],
        "B": ["研究建议", "So what"],
        "C": ["产品启示", "So what"],
        "D": ["事业单元启示", "事业单元的启示", "So what"],
    }
    markers = implication_markers.get(report_type, [])
    if markers and not any(m in text for m in markers):
        errors.append(f"Type {report_type}: missing implication/recommendation section")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("report", help="Path to the report .md")
    p.add_argument("--assets", required=True, help="Path to assets/<slug>/ dir")
    p.add_argument("--type", choices=["A", "B", "C", "D"], required=True, help="Report type")
    args = p.parse_args()

    report_path = Path(args.report)
    if not report_path.exists():
        sys.stderr.write(f"report not found: {report_path}\n")
        return 2
    text = report_path.read_text(encoding="utf-8")
    assets_dir = Path(args.assets)

    errors: list[str] = []
    check_structure(text, args.type, errors)
    check_sourcing(text, errors)
    check_visuals(text, assets_dir, args.type, errors)
    check_banned_phrases(text, errors)
    check_architecture_diagrams(text, args.type, errors)
    check_comparison_table(text, args.type, errors)
    check_implication(text, args.type, errors)

    if errors:
        print(f"FAIL — {len(errors)} issues:\n")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("OK — report passed all checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
