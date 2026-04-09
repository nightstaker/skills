#!/usr/bin/env python3
"""
linter.py — quality gate for tech-insight reports (v2.0 — depth edition).

Enforces the non-negotiables defined in REQUIREMENT.MD:

1. Universal sourcing — every factual sentence AND every factual KCA/KTD cell
   must carry an inline link.
2. Visual coverage — required image slots must be present, captioned, and sourced.
3. Structure integrity — Type A eight-section / Type B six-stage + investor
   appendix / Type C eight-section (all including the mandatory Investor
   Appendix from REQUIREMENT.MD §2.4).
4. Implication actionability — banned filler phrases.
5. Hallucination guard — specific numbers / product codes / quotes without a source.
6. Sample integrity — Type A Per-Product Profile must have ≥ top_n data rows.
7. Asset provenance — every file in assets/<slug>/ must appear in image_manifest.json
   entries and every manifest entry must correspond to a real file on disk.
8. Depth gates (v2.0):
   - Banned shallow phrases (§1.4.6): 业界领先 / 先进架构 / 生态完善 /
     industry-leading / best-in-class / revolutionary / cutting-edge …
   - Process-node foundry variant: bare "3nm" / "5nm" etc. must be accompanied
     by a TSMC / Samsung / Intel node variant in the same table or nearby text.
   - Benchmark methodology keywords: KTD / Key Technical Metrics sections must
     mention batch / seqlen / precision / test-condition vocabulary.
   - Moat legal evidence: Moat / 壁垒 sections must carry ≥1 patent number
     (US/CN/EP/WO) or ≥1 SEC / HKEX filing reference.
   - Investor appendix: must cover unit economics + customer concentration +
     capacity + regulatory keyword families.

Exit code:
  0 — clean
  1 — violations found

Usage:
  python linter.py reports/foo.md --assets assets/foo/ --type A
  python linter.py reports/foo.md --assets assets/foo/ --type A --top-n 4
  python linter.py reports/foo.md --assets assets/foo/ --type B
  python linter.py reports/foo.md --assets assets/foo/ --type C
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

# Existing filler phrases + new shallow phrases from REQUIREMENT.MD §1.4.6.
BANNED_PHRASES = [
    # v1 fillers
    "需要持续关注",
    "值得观察",
    "未来可期",
    "拭目以待",
    "前景广阔",
    "大有可为",
    # v2 shallow phrases (CN)
    "业界领先",
    "行业领先",
    "性能领先",
    "先进架构",
    "先进工艺",
    "生态完善",
    "技术成熟",
    "市场广阔",
    "空间巨大",
    "潜力巨大",
    "引领行业",
    "颠覆式创新",
    "革命性突破",
    "全球首创",
    "具有广阔前景",
    "有望成为",
    "将会改变",
]

# Banned English shallow phrases (case-insensitive — see check_banned_phrases).
BANNED_PHRASES_EN_CI = [
    "industry-leading",
    "industry leading",
    "best-in-class",
    "best in class",
    "revolutionary",
    "game-changing",
    "game changing",
    "cutting-edge",
    "cutting edge",
    "paradigm shift",
    "paradigm-shift",
]

# Bare process node pattern — e.g. "3nm", "5 nm", "7nm process".
# Flagged unless the same section names a foundry variant.
PROCESS_NODE_BARE = re.compile(r"\b(?<![A-Za-z])(3|4|5|7|10|14)\s*nm\b", re.IGNORECASE)

# Known foundry-variant tokens that make a process-node claim valid.
FOUNDRY_VARIANTS = [
    # TSMC
    "TSMC", "N3E", "N3P", "N3B", "N3", "N4P", "N4X", "N4",
    "N5P", "N5", "N6", "N7P", "N7",
    # Samsung
    "Samsung", "SF3", "SF3P", "SF4", "SF4X", "SF4P", "SF5", "SF7",
    # Intel
    "Intel 18A", "18A", "20A", "Intel 3", "Intel 4", "Intel 7",
    # Other foundries
    "SMIC", "GlobalFoundries", "GF 12", "GF 14",
]

# Benchmark methodology required vocabulary — at least one term from EACH
# group must appear in KTD / Key Technical Metrics sections.
BENCH_METHODOLOGY_GROUPS = [
    ["batch", "Batch"],
    ["seqlen", "sequence length", "seq-len", "上下文长度", "context length"],
    ["precision", "FP8", "FP16", "BF16", "INT8", "INT4", "W4A16", "W8A8"],
    ["methodology", "测试条件", "test condition", "benchmark condition", "测试方法"],
]

# Patent number patterns (independent claim grounding).
PATENT_NUMBER_RE = re.compile(
    r"\b(?:US\d{7,}|CN\d{7,}|EP\d{7,}|WO\d{4}[/-]\d{5,})\b"
)

# SEC / HKEX / Tokyo filing indicators.
FILING_INDICATORS = [
    "10-K", "10-Q", "20-F", "8-K", "S-1", "F-1", "DEF 14A",
    "HKEX filing", "港交所", "招股书", "Prospectus", "prospectus",
    "SEC filing",
]

# Investor Appendix keyword families — one hit per family required in the
# Investor Appendix section.
INVESTOR_APPENDIX_FAMILIES = {
    "Unit Economics": [
        "ASP", "BoM", "gross margin", "毛利率", "毛利", "单位经济性",
        "wafer cost", "CapEx", "ARPU", "单位成本",
    ],
    "Customer Concentration": [
        "Top-3 客户", "Top 3 客户", "客户集中度", "design win",
        "design-win", "客户份额", "top-3 customer",
    ],
    "Capacity & Supply": [
        "产能", "CoWoS", "FOPLP", "HBM", "wafer start", "substrate",
        "ABF", "fab slot", "capacity",
    ],
    "Regulatory & Geopolitical": [
        "出口管制", "15 CFR", "BIS", "ECCN", "EAR", "CFIUS", "SAMR",
        "CMA", "监管", "Chips Act", "export control",
    ],
}

TYPE_A_REQUIRED_SECTIONS = [
    ("品类边界", "Category boundary block (§0)"),
    ("Per-Product Profile", "Per-Product Profile table (§1)"),
    ("KCA Matrix", "KCA Matrix (§2)"),
    ("KTD Comparison", "KTD Comparison (§3)"),
    ("Moat", "Moat Analysis (§4)"),
    ("Cross-Product Insight", "Cross-Product Insight (§5)"),
    ("Implication", "Implication (§6)"),
    ("Investor Appendix", "Investor Appendix (§7)"),
    ("Sources", "Sources (§8)"),
]

TYPE_B_REQUIRED_SECTIONS = [
    ("Scene Anchor", "Scene Anchor (§1)"),
    ("Vendor Landscape", "Vendor Landscape (§2)"),
    ("Key Technology Decomposition", "Key Technology Decomposition (§3)"),
    ("Trend Prediction", "Trend Prediction (§4)"),
    ("Closed Loop", "Closed Loop (§5)"),
    ("Implication", "Implication (§6)"),
    ("Investor Appendix", "Investor Appendix (§7)"),
    ("Sources", "Sources (§8)"),
]

TYPE_C_REQUIRED_SECTIONS = [
    ("Product Profile", "Product Profile (§1)"),
    ("Architecture Decomposition", "Architecture Decomposition (§2)"),
    ("Key Technical Metrics", "Key Technical Metrics (§3)"),
    ("Moat Analysis", "Moat Analysis (§4)"),
    ("Weakness", "Weakness / Risk Analysis (§5)"),
    ("Implication", "Implication (§6)"),
    ("Investor Appendix", "Investor Appendix (§7)"),
    ("Sources", "Sources (§8)"),
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
            errors.append(f"banned shallow/filler phrase found: '{ph}'")
    text_lower = text.lower()
    for ph in BANNED_PHRASES_EN_CI:
        if ph.lower() in text_lower:
            errors.append(f"banned shallow English phrase found: '{ph}'")


def check_process_node_depth(text: str, errors: list[str]) -> None:
    """Any mention of a bare process node (3nm / 5nm / 7nm) must be accompanied
    by a named foundry variant somewhere in the report. REQUIREMENT.MD §1.4.2."""
    if not PROCESS_NODE_BARE.search(text):
        return
    if not any(variant in text for variant in FOUNDRY_VARIANTS):
        errors.append(
            "process node mentioned but no foundry variant found "
            "(expected TSMC N3E / Samsung SF4X / Intel 18A / N4P / ...)"
        )


def check_benchmark_methodology(text: str, report_type: str, errors: list[str]) -> None:
    """The KTD Comparison / Key Technical Metrics section must mention the full
    benchmark methodology keyword families: batch + seqlen + precision +
    test-condition. REQUIREMENT.MD §1.4.3."""
    section_needle = {
        "A": "KTD Comparison",
        "B": "Key Technology Decomposition",
        "C": "Key Technical Metrics",
    }[report_type]
    rng = _extract_section(text, section_needle)
    if not rng:
        return  # structure check already reported
    start, end = rng
    section_text = "\n".join(text.splitlines()[start:end])
    section_lower = section_text.lower()
    missing: list[str] = []
    for group in BENCH_METHODOLOGY_GROUPS:
        if not any(term.lower() in section_lower for term in group):
            missing.append(" / ".join(group))
    if missing:
        errors.append(
            f"{section_needle} section missing benchmark methodology keywords: "
            + "; ".join(missing)
        )


def check_moat_legal_evidence(text: str, report_type: str, errors: list[str]) -> None:
    """The Moat / 壁垒 section must contain at least one patent number
    (US/CN/EP/WO) or SEC / HKEX filing reference. REQUIREMENT.MD §1.4.4."""
    # Type A + Type C have explicit Moat sections; Type B embeds moat in Key
    # Technology Decomposition (the patent-wall requirement from §2.2).
    needle = {
        "A": "Moat",
        "B": "Key Technology Decomposition",
        "C": "Moat Analysis",
    }[report_type]
    rng = _extract_section(text, needle)
    if not rng:
        return
    start, end = rng
    section_text = "\n".join(text.splitlines()[start:end])
    if PATENT_NUMBER_RE.search(section_text):
        return
    if any(ind in section_text for ind in FILING_INDICATORS):
        return
    errors.append(
        f"{needle} section lacks legal evidence: needs ≥1 patent number "
        "(US/CN/EP/WO) or ≥1 SEC / HKEX filing reference"
    )


def check_investor_appendix(text: str, errors: list[str]) -> None:
    """The Investor Appendix section must cover all four keyword families:
    unit economics, customer concentration, capacity & supply, regulatory.
    REQUIREMENT.MD §2.4."""
    rng = _extract_section(text, "Investor Appendix")
    if not rng:
        return  # structure check already reported
    start, end = rng
    section_text = "\n".join(text.splitlines()[start:end])
    for family, keywords in INVESTOR_APPENDIX_FAMILIES.items():
        if not any(kw in section_text for kw in keywords):
            errors.append(
                f"Investor Appendix missing '{family}' keyword family "
                f"(expected one of: {', '.join(keywords[:6])}…)"
            )


def check_structure(text: str, report_type: str, errors: list[str]) -> None:
    required = {
        "A": TYPE_A_REQUIRED_SECTIONS,
        "B": TYPE_B_REQUIRED_SECTIONS,
        "C": TYPE_C_REQUIRED_SECTIONS,
    }[report_type]
    for needle, label in required:
        if needle not in text:
            errors.append(f"missing required section: {label} (search key: '{needle}')")


def _extract_section(text: str, heading_needle: str) -> tuple[int, int] | None:
    """Return (start_line_idx, end_line_idx) of a markdown section whose
    heading line contains `heading_needle`. The section ends at the next
    heading of the same or higher level, or at EOF."""
    lines = text.splitlines()
    start = None
    start_level = 0
    for i, line in enumerate(lines):
        m = re.match(r"^(#+)\s+(.*)$", line)
        if m and heading_needle in m.group(2):
            start = i
            start_level = len(m.group(1))
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        m = re.match(r"^(#+)\s+", lines[j])
        if m and len(m.group(1)) <= start_level:
            end = j
            break
    return (start, end)


def _tables_in_range(text: str, start: int, end: int) -> list[tuple[int, list[str]]]:
    """Return [(first_data_line_idx, data_rows), ...] for every pipe-table in
    the given line range. A pipe-table is detected by a header row followed
    immediately by a separator row of the form `| --- | --- | ...`."""
    lines = text.splitlines()
    out: list[tuple[int, list[str]]] = []
    i = start
    while i < end - 1:
        line = lines[i]
        nxt = lines[i + 1] if i + 1 < end else ""
        if line.strip().startswith("|") and re.match(r"^\s*\|?\s*:?-{2,}", nxt.strip()):
            data_start = i + 2
            rows: list[str] = []
            j = data_start
            while j < end and lines[j].strip().startswith("|"):
                rows.append(lines[j])
                j += 1
            out.append((data_start, rows))
            i = j
        else:
            i += 1
    return out


def _split_cells(row: str) -> list[str]:
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    return [c.strip() for c in row.split("|")]


def check_table_cell_sourcing(text: str, errors: list[str]) -> None:
    """KCA Matrix and KTD Comparison cells must carry inline sources for any
    cell that asserts a fact (contains a number, unit, proper noun, or quote).
    Pure placeholder cells ("…", "N/A", "未公开") are allowed."""
    for needle in ("KCA Matrix", "KTD Comparison"):
        rng = _extract_section(text, needle)
        if not rng:
            continue
        start, end = rng
        for data_start, rows in _tables_in_range(text, start, end):
            for offset, row in enumerate(rows):
                cells = _split_cells(row)
                # first cell is the row label; skip it from sourcing requirement
                for col_idx, cell in enumerate(cells[1:], start=1):
                    stripped = cell.strip()
                    if not stripped or stripped in {"…", "...", "N/A", "-", "未公开", "—"}:
                        continue
                    if not is_factual(stripped):
                        continue
                    if not INLINE_LINK.search(stripped):
                        line_no = data_start + offset + 1
                        preview = stripped[:60].replace("\n", " ")
                        errors.append(
                            f"[L{line_no}] {needle} cell (col {col_idx}) lacks inline source: {preview}"
                        )


def check_sample_rows(text: str, report_type: str, top_n: int, errors: list[str]) -> None:
    """Type A only: Per-Product Profile must have ≥ top_n data rows."""
    if report_type != "A":
        return
    rng = _extract_section(text, "Per-Product Profile")
    if not rng:
        return
    start, end = rng
    tables = _tables_in_range(text, start, end)
    if not tables:
        errors.append("Per-Product Profile section has no data table")
        return
    # Pick the first table in the section.
    _, rows = tables[0]
    if len(rows) < top_n:
        errors.append(
            f"Per-Product Profile has {len(rows)} rows; --top-n requires {top_n}"
        )


def check_asset_provenance(assets_dir: Path, errors: list[str]) -> None:
    """Every file in assets_dir (except image_manifest.json) must appear in
    manifest.entries; every manifest.entries key must be a real file on disk,
    UNLESS the entry has link_only: true (link-mode delivery, see
    REQUIREMENT.MD §3.1.1)."""
    if not assets_dir.exists():
        errors.append(f"assets directory not found: {assets_dir}")
        return
    manifest_path = assets_dir / "image_manifest.json"
    if not manifest_path.exists():
        return  # already reported by check_visuals
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        return  # already reported by check_visuals
    entries = manifest.get("entries") or {}
    on_disk = {
        p.name
        for p in assets_dir.iterdir()
        if p.is_file() and p.name != "image_manifest.json"
    }
    expected_on_disk = {
        fname for fname, info in entries.items() if not info.get("link_only")
    }
    for fname in sorted(on_disk - set(entries.keys())):
        errors.append(f"asset {fname} has no manifest entry")
    for fname in sorted(expected_on_disk - on_disk):
        errors.append(f"manifest entry {fname} has no file on disk")


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
            if f"p{n}-hero" not in text_lower and f"P{n} 产品图" not in text:
                errors.append(f"Type A: missing product photo for P{n}")
            if f"p{n}-arch" not in text_lower and f"P{n} 架构" not in text:
                errors.append(f"Type A: missing architecture/teardown image for P{n}")
    elif report_type == "B":
        if "scene" not in text_lower and "场景图" not in text:
            errors.append("Type B: missing Scene Anchor image")
        if "tech-1-arch" not in text_lower and "关键技术 1 原理" not in text:
            errors.append("Type B: missing key technology 1 principle diagram")
    elif report_type == "C":
        if "hero" not in text_lower and "产品图" not in text:
            errors.append("Type C: missing product hero photo")
        if "arch" not in text_lower and "架构图" not in text:
            errors.append("Type C: missing architecture / teardown diagram")
        if "die" not in text_lower and "pcb" not in text_lower and "dieshot" not in text_lower and "die shot" not in text_lower and "内部" not in text:
            errors.append("Type C: missing die shot / PCB / internal teardown image")

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
    p.add_argument("--type", choices=["A", "B", "C"], required=True, help="Report type")
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
    check_table_cell_sourcing(text, errors)
    check_sample_rows(text, args.type, args.top_n, errors)
    check_visuals(text, assets_dir, args.type, errors, top_n=args.top_n)
    check_asset_provenance(assets_dir, errors)
    check_banned_phrases(text, errors)
    check_process_node_depth(text, errors)
    check_benchmark_methodology(text, args.type, errors)
    check_moat_legal_evidence(text, args.type, errors)
    check_investor_appendix(text, errors)
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
