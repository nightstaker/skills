# Example — AI+HW 2035 Insight Deck (storage-deep-dive)

Reproducible example showing how to render an 18-slide hw-insight deck with
pptxgenjs, including: 6-section navigation, fixed footer, metric cards
implemented as filled text boxes (linter-safe), tech-radar with non-overlapping
quadrants, real arXiv figures, and a per-slide insight callout.

The deck summarizes a public CC BY 4.0 vision paper
([arXiv:2603.05225v1](https://arxiv.org/abs/2603.05225)) with a deep-dive on the
storage stack (memory wall, CIM, HBM roadmap, photonic interconnect,
hardware-aware algorithms).

## Files

- `build.js` — single-file pptxgenjs renderer. 18 slides, hw-insight template
  compliant. Image embedding is wrapped with `safeAddImage` so missing figures
  are skipped instead of failing the build.

## Prerequisites

```bash
npm install pptxgenjs
```

Optional — download the arXiv figures referenced by the deck (CC BY 4.0):

```bash
mkdir -p images
curl -sSL -o images/aihw_fig1.png      https://arxiv.org/html/2603.05225v1/figures/Picture1.png
curl -sSL -o images/aihw_fig3.png      https://arxiv.org/html/2603.05225v1/figures/Picture3.png
curl -sSL -o images/memwall_x1.png     https://arxiv.org/html/2403.14123v1/x1.png
curl -sSL -o images/memwall_x3.png     https://arxiv.org/html/2403.14123v1/x3.png
curl -sSL -o images/cim_overview.png   https://arxiv.org/html/2401.14428v1/extracted/5366244/figures/COM-CNM-CIM.png
curl -sSL -o images/cim_memcentric.png https://arxiv.org/html/2401.14428v1/extracted/5366244/figures/mem-centric.png
```

Without those files, the relevant slides simply render text-only — `safeAddImage`
logs a warning per missing path.

## Build

```bash
node build.js                 # writes ./ai_hw_2035_insight.pptx
```

Override paths via env vars when needed:

```bash
IMG_DIR=/path/to/figures \
HW_LOGO=/path/to/logo.png \
OUT_PATH=/path/to/out.pptx \
node build.js
```

## Lint

```bash
python3 ../../scripts/linter.py ai_hw_2035_insight.pptx \
  --template ../../templates/hw-insight/template.md
```

Hard checks (overlap, oversized cards, content-zone breach, text overflow,
content-density, font/color compliance) all pass. The pixel-level
`whitespace_ratio` check still flags slides whose layouts are inherently
sparse — quote pages, tech-radar, image+commentary splits — and is left as a
warning rather than restructuring the narrative.

## Sources

- AI+HW 2035 paper: [arXiv:2603.05225v1](https://arxiv.org/abs/2603.05225) (CC BY 4.0)
- Memory wall figures: Gholami et al., [arXiv:2403.14123v1](https://arxiv.org/abs/2403.14123) (CC BY 4.0)
- Compute-near-memory survey figures: Zhou et al., [arXiv:2401.14428v1](https://arxiv.org/abs/2401.14428) (CC BY 4.0)
