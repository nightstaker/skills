#!/usr/bin/env python3
"""
linter.py — quality gate for tech-insight reports.

Enforces the non-negotiables defined in REQUIREMENT.MD:

1. Universal sourcing — every factual sentence must carry an inline link.
2. Visual coverage — required image slots must be present, captioned, and sourced.
3. Structure integrity — Type A six-section / Type B five-stage + closed loop.
4. Implication actionability — banned filler phrases.
5. Hallucination guard — specific numbers / product codes / quotes without a source.

Exit code:
  0 — clean
  1 — violations found

Usage:
  python linter.py reports/foo.md --assets assets/foo/ --type A
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

TYPE_A_REQUIRED_SECTIONS = [
    ("品类边界", "Category boundary block (§0)"),
    ("Per-Product Profile", "Per-Product Profile table (§1)"),
    ("KCA Matrix", "KCA Matrix (§2)"),
    ("KTD Comparison", "KTD Comparison (§3)"),
    ("Cross-Product Insight", "Cross-Product Insight (§4)"),
    ("Implication", "Implication (§5)"),
    ("Sources", "Sources (§6)"),
]

TYPE_B_REQUIRED_SECTIONS = [
    ("Scene Anchor", "Scene Anchor (§1)"),
    ("Vendor Landscape", "Vendor Landscape (§2)"),
    ("Key Technology Decomposition", "Key Technology Decomposition (§3)"),
    ("Trend Prediction", "Trend Prediction (§4)"),
    ("Closed Loop", "Closed Loop (§5)"),
    ("Implication", "Implication (§6)"),
    ("Sources", "Sources (§7)"),
]


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
    required = (
        TYPE_A_REQUIRED_SECTIONS if report_type == "A" else TYPE_B_REQUIRED_SECTIONS
    )
    for needle, label in required:
        if needle not in text:
            errors.append(f"missing required section: {label} (search key: '{needle}')")


def check_visuals(
    text: str,
    assets_dir: Path,
    report_type: str,
    errors: list[str],
    top_n: int = 5,
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

    # Coverage targets
    text_lower = text.lower()
    if report_type == "A":
        for n in range(1, top_n + 1):
            if f"p{n}-hero" not in text_lower and f"p{n} 产品图" not in text:
                errors.append(f"Type A: missing product photo for P{n}")
            if f"p{n}-arch" not in text_lower and f"p{n} 架构" not in text:
                errors.append(f"Type A: missing architecture/teardown image for P{n}")
    else:
        if "scene" not in text_lower and "场景图" not in text:
            errors.append("Type B: missing Scene Anchor image")
        if "tech-1-arch" not in text_lower and "关键技术 1 原理" not in text:
            errors.append("Type B: missing key technology 1 principle diagram")

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


def check_closed_loop(text: str, errors: list[str]) -> None:
    if "Closed Loop" not in text:
        return
    needed = ["技术", "产品", "客户", "商业价值"]
    # find the closed loop section
    idx = text.find("Closed Loop")
    section = text[idx : idx + 2000]
    for n in needed:
        if n not in section:
            errors.append(f"Closed Loop missing node: {n}")
    if not re.search(r"(TAM|SAM|SOM|ARPU|渗透率|市场规模|亿|\$\s*\d|USD\s*\d)", section):
        errors.append("Closed Loop commercial node lacks a quantified value")


def check_falsifiability(text: str, errors: list[str]) -> None:
    if "Trend Prediction" not in text:
        return
    idx = text.find("Trend Prediction")
    section = text[idx : idx + 2000]
    if "可证伪" not in section and "falsifi" not in section.lower():
        errors.append("Trend Prediction missing falsifiability conditions")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("report", help="Path to the report .md")
    p.add_argument("--assets", required=True, help="Path to assets/<slug>/ dir")
    p.add_argument("--type", choices=["A", "B"], required=True, help="Report type")
    p.add_argument(
        "--top-n",
        type=int,
        default=5,
        help="Type A only: number of products in the benchmark (3–5). Use when the category is legitimately degraded below TOP 5.",
    )
    args = p.parse_args()
    if args.type == "A" and not (3 <= args.top_n <= 5):
        sys.stderr.write("--top-n must be in [3, 5]\n")
        return 2

    report_path = Path(args.report)
    if not report_path.exists():
        sys.stderr.write(f"report not found: {report_path}\n")
        return 2
    text = report_path.read_text(encoding="utf-8")
    assets_dir = Path(args.assets)

    errors: list[str] = []
    check_structure(text, args.type, errors)
    check_sourcing(text, errors)
    check_visuals(text, assets_dir, args.type, errors, top_n=args.top_n)
    check_banned_phrases(text, errors)
    if args.type == "B":
        check_closed_loop(text, errors)
        check_falsifiability(text, errors)

    if errors:
        print(f"FAIL — {len(errors)} issues:\n")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("OK — report passed all checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
