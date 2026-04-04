# Workflow: Data Integration — Excel/CSV to Chart Slides

Use this workflow when external data (Excel workbooks or CSV files) needs to become slide content: charts, tables, KPI callouts, or data summaries.

---

## Overview

Data integration is not a standalone workflow — it is an extension applied on top of **Create** or **Update**:

- **Create + Data**: Build a new deck where some slides are data-driven
- **Update + Data**: Insert or refresh data slides in an existing deck

The data workflow handles:
1. Reading and validating external data
2. Selecting the right chart type for each dataset
3. Rendering chart slides compliant with the active template
4. Generating source citations

---

## Step 1 — Read and Profile the Data

```python
# Quick profile
import pandas as pd

df = pd.read_excel("data.xlsx", sheet_name=None)  # all sheets
# or
df = pd.read_csv("data.csv")

# Profile each sheet/frame
for name, frame in df.items():
    print(f"Sheet: {name}")
    print(f"  Rows: {len(frame)}, Columns: {list(frame.columns)}")
    print(f"  Sample:\n{frame.head(3)}\n")
```

Output a summary to the user and ask for clarification if the data structure is ambiguous:
- Which columns are dimensions (categories) vs. measures (values)?
- What is the time axis, if any?
- Is comparison across rows or across columns the main story?

---

## Step 2 — Chart Type Selection

| Data pattern | Recommended chart | PptxGenJS type |
|-------------|-------------------|----------------|
| Single metric over time (≤12 points) | Line chart | `"line"` |
| Multiple series over time (≤6 series) | Multi-line chart | `"line"` |
| Category comparison (≤8 categories) | Bar chart | `"bar"` |
| Part-of-whole (≤6 slices, no slice <5%) | Pie chart | `"pie"` |
| Part-of-whole (≤6 slices, has small values) | Donut chart | `"doughnut"` |
| Two-variable relationship | Scatter plot | `"scatter"` |
| Stacked share over time | Stacked bar | `"bar"` with `barGrouping: "stacked"` |
| 3–10 KPIs | Stat callout slide | (text-based, no chart) |
| Detailed breakdown (≤6 cols × 10 rows) | Table | `addTable()` |

**Selection rules:**
- Never use a pie chart with >6 slices
- If a line chart would have >12 points on the x-axis, consider grouping or summarizing
- For executive decks: KPI callouts > charts for top-line numbers

---

## Step 3 — Prepare Chart Data

Transform the raw data into PptxGenJS-compatible format:

```python
# scripts/data_prep.py helper (use inline or as a utility)
import pandas as pd
import json

def prepare_bar_chart(df, category_col, value_cols):
    """Convert DataFrame to PptxGenJS bar chart data."""
    data = []
    for col in value_cols:
        series = {
            "name": col,
            "labels": df[category_col].astype(str).tolist(),
            "values": df[col].tolist()
        }
        data.append(series)
    return json.dumps(data, indent=2)

def prepare_line_chart(df, x_col, y_cols):
    """Convert DataFrame to PptxGenJS line chart data."""
    data = []
    for col in y_cols:
        series = {
            "name": col,
            "labels": df[x_col].astype(str).tolist(),
            "values": df[col].tolist()
        }
        data.append(series)
    return json.dumps(data, indent=2)

def format_kpi(value, label, unit="", delta=None, delta_dir="up"):
    """Format a single KPI for stat-callout slide."""
    return {
        "value": f"{value:,.0f}" if isinstance(value, (int, float)) else str(value),
        "unit": unit,
        "label": label,
        "delta": delta,
        "delta_direction": delta_dir  # "up" | "down" | None
    }
```

---

## Step 4 — Render Chart Slides

### PptxGenJS Chart Rendering

Use template colors for chart series. Never use default PptxGenJS colors.

```javascript
const CHART_COLORS = [
  COLORS.primary,    // first series
  COLORS.accent,     // second series
  COLORS.muted,      // third series
  // add more from template palette if needed
];

// Bar chart example
const chartData = [
  { name: "Q1", labels: ["Product A", "Product B", "Product C"], values: [42, 33, 28] },
  { name: "Q2", labels: ["Product A", "Product B", "Product C"], values: [55, 29, 38] },
];

slide.addChart(pres.charts.BAR, chartData, {
  x: 0.5, y: 1.2, w: 9, h: 3.8,
  chartColors: CHART_COLORS,
  showLegend: true, legendPos: "b",
  showTitle: false,         // title is the slide title, not chart title
  dataLabelFontSize: 10,
  dataLabelColor: "FFFFFF",
  valAxisMajorGridlines: { style: "none" },  // clean look
  catAxisLabelFontSize: 11,
  catAxisLabelColor: COLORS.text,
});
```

### KPI Callout Slide (stat-callout layout)

For key metrics, use large-number callouts rather than charts:

```javascript
const kpis = [
  { value: "4.2M", label: "Total Users", delta: "+23%", dir: "up" },
  { value: "$18.4M", label: "Revenue", delta: "+11%", dir: "up" },
  { value: "94%", label: "Retention", delta: "-2%", dir: "down" },
];

kpis.forEach((kpi, i) => {
  const x = 0.5 + i * 3.2;

  // Value
  slide.addText(kpi.value, {
    x, y: 1.5, w: 2.8, h: 1.0,
    fontSize: 48, fontFace: FONTS.heading, color: COLORS.primary,
    bold: true, align: "center"
  });

  // Delta badge
  const deltaColor = kpi.dir === "up" ? "16A34A" : "DC2626";
  slide.addText(kpi.delta, {
    x, y: 2.6, w: 2.8, h: 0.4,
    fontSize: 14, fontFace: FONTS.body,
    color: deltaColor, align: "center"
  });

  // Label
  slide.addText(kpi.label, {
    x, y: 3.1, w: 2.8, h: 0.4,
    fontSize: SIZES.caption, fontFace: FONTS.body,
    color: COLORS.muted, align: "center"
  });
});
```

### Data Table Slide

```javascript
const rows = [
  [{ text: "Region", options: { bold: true, color: COLORS.secondary, fill: COLORS.primary }},
   { text: "Revenue", options: { bold: true, color: COLORS.secondary, fill: COLORS.primary }},
   { text: "Growth", options: { bold: true, color: COLORS.secondary, fill: COLORS.primary }}],
  ["APAC",   "$4.2M", "+28%"],
  ["EMEA",   "$3.1M", "+12%"],
  ["Americas", "$6.8M", "+18%"],
];

slide.addTable(rows, {
  x: 1.0, y: 1.5, w: 8.0,
  fontSize: 13, fontFace: FONTS.body,
  border: { type: "solid", color: "E5E7EB", pt: 1 },
  rowH: 0.45,
  align: "center",
});
```

---

## Step 5 — Insight Annotations & Source Citations

Every data slide must include both an **insight annotation** and a **source citation**.

### Insight Annotation (above the citation)

A one-line technical takeaway from the data — the "so what" that tells the audience why this data matters:

```javascript
slide.addText(insightText, {
  x: 0.5, y: 5.0, w: 9.0, h: 0.28,
  fontSize: 11, fontFace: FONTS.body,
  color: COLORS.primary || COLORS.text, italic: true,
  fill: { color: COLORS.highlight || "EFF3FF" }
});
```

### Source Citation (bottom of slide)

```javascript
slide.addText(`Source: ${sourceName} | As of ${asOfDate}`, {
  x: 0.5, y: 5.3, w: 9.0, h: 0.2,
  fontSize: 9, fontFace: FONTS.body,
  color: COLORS.muted, italic: true
});
```

If the template defines an evidence hierarchy (e.g., hw-insight), label the evidence type: `外部Benchmark`, `行业报告`, `学术文献`, etc.

---

## Step 6 — Data Validation Before Rendering

Before rendering, run these checks:

```python
# Check for null/missing values
nulls = df.isnull().sum()
if nulls.any():
    print(f"WARNING: Missing values detected:\n{nulls[nulls > 0]}")

# Check for outliers that could distort charts
for col in numeric_cols:
    q1, q99 = df[col].quantile([0.01, 0.99])
    outliers = df[(df[col] < q1) | (df[col] > q99)]
    if not outliers.empty:
        print(f"WARNING: {len(outliers)} outliers in '{col}'")

# Check sufficient data points for chart type
if chart_type == "line" and len(df) < 3:
    print("WARNING: Line chart with <3 points — consider bar chart instead")

if chart_type == "pie" and len(df) > 6:
    print("ERROR: Pie chart has >6 slices — group small categories into 'Other'")
```

Report any warnings to the user before proceeding.

---

## Step 7 — Refresh Existing Data Slides (Update mode)

When refreshing data in an existing deck (e.g., monthly report update):

1. List current data slides: `python scripts/slide_id_manager.py list input.pptx`
2. Unpack: `python ../pptx/scripts/office/unpack.py input.pptx unpacked/`
3. For chart slides backed by embedded Excel data (`ppt/charts/chart*.xml`), update the cached values in the XML:

```xml
<!-- In chart XML, update <c:v> values -->
<c:ser>
  <c:val>
    <c:numRef>
      <c:numCache>
        <c:ptCount val="4"/>
        <c:pt idx="0"><c:v>42.5</c:v></c:pt>
        <c:pt idx="1"><c:v>55.1</c:v></c:pt>
        <c:pt idx="2"><c:v>61.3</c:v></c:pt>
        <c:pt idx="3"><c:v>74.8</c:v></c:pt>
      </c:numCache>
    </c:numRef>
  </c:val>
</c:ser>
```

4. Update the source citation date on each refreshed slide
5. Pack: `python ../pptx/scripts/office/pack.py unpacked/ output.pptx --original input.pptx`

---

## QA

```bash
# Verify data values survived rendering
python -m markitdown output.pptx | grep -E "[0-9]+%|[0-9]+M|[0-9]+K"

# Linter
python scripts/linter.py output.pptx --template templates/<name>/template.md

# Visual QA (chart rendering must be verified visually)
python ../pptx/scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

For chart slides especially, visual QA is mandatory — chart rendering differences between PptxGenJS and actual PowerPoint can cause label overflow, legend clipping, and axis issues.
