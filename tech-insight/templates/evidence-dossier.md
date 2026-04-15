# Evidence Dossier — Output Template

Raw evidence collection organized by source type. Serves as the data foundation for insight reports, landscape scans, and briefings.

---

## Header

```
Subject:      _______________
Question:     [specific question this evidence addresses]
Analyst:      _______________
Date:         YYYY-MM-DD
Technologies: [list of technologies covered]
```

---

## Evidence Summary

| Metric | Value |
|--------|-------|
| Total evidence points | N |
| Source types | 外部Benchmark: N, 学术文献: N, 专利分析: N, 行业报告: N, 公开信号: N, 专家判断: N |
| Independent sources | N |
| Cross-validated claims | N / N total |
| Recency range | YYYY-MM to YYYY-MM |
| Overall confidence | High / Medium / Low |

---

## Evidence by Source Type

### 外部Benchmark (Published Third-Party Benchmarks)

| # | Benchmark | Technologies Tested | Key Results | Environment | Source | Date | Confidence |
|---|-----------|-------------------|-------------|-------------|--------|------|------------|
| B1 | [name] | [list] | [values with units] | [hw/sw config] | [citation + URL] | YYYY-MM | H/M/L |
| B2 | | | | | | | |

**Methodology notes**:
- [B1]: [how the benchmark was run, any caveats]
- [B2]: [methodology description]

---

### 学术文献 (Academic Literature)

| # | Paper | Venue | Key Claim | Data Point | Cited By | Date | Confidence |
|---|-------|-------|-----------|-----------|----------|------|------------|
| A1 | [title] | [conference/journal] | [main finding] | [specific value] | N citations | YYYY-MM | H/M/L |
| A2 | | | | | | | |

**Notes**:
- [A1]: [peer-review status, reproduction attempts, limitations noted by authors]
- [A2]: [notes]

---

### 专利分析 (Patent Analysis)

| # | Patent / Filing | Assignee | Technology Area | Key Claim | Status | Date | Relevance |
|---|----------------|----------|----------------|-----------|--------|------|-----------|
| P1 | [number / title] | [company] | [area] | [what it covers] | Filed/Granted | YYYY-MM | H/M/L |
| P2 | | | | | | | |

**Patent landscape summary**:
- Total filings in domain: N (period: YYYY to YYYY)
- Top assignees: [ranked list]
- Trend: [increasing/stable/declining]
- Source: [database + search query used]

---

### 行业报告 (Industry Reports)

| # | Report | Publisher | Key Finding | Data Point | Methodology | Date | Confidence |
|---|--------|----------|-------------|-----------|-------------|------|------------|
| R1 | [title] | [publisher] | [finding] | [value] | [how derived] | YYYY-MM | H/M/L |
| R2 | | | | | | | |

---

### 公开信号 (Observable Public Signals)

| # | Signal Type | Subject | Observable Data | Source | Date | Implication |
|---|-----------|---------|----------------|--------|------|------------|
| S1 | GitHub activity | [repo/org] | [stars, contributors, commit velocity] | [URL] | YYYY-MM | [what it indicates] |
| S2 | Package downloads | [package] | [monthly downloads, trend] | [npm/PyPI stats] | YYYY-MM | |
| S3 | Job postings | [company] | [N postings for X role, change vs prior] | [platform] | YYYY-MM | |
| S4 | Product release | [vendor] | [feature, version, changelog summary] | [URL] | YYYY-MM | |
| S5 | Conference talks | [event] | [N talks on topic, key themes] | [program URL] | YYYY-MM | |

---

### 专家判断 (Expert Judgment)

| # | Expert / Source | Claim | Basis Stated | Agreement Level | Date | Confidence |
|---|---------------|-------|-------------|----------------|------|------------|
| E1 | [who/where] | [claim] | [what they base it on] | [consensus/minority/contrarian] | YYYY-MM | Low |

**Note**: Expert judgment is LOWEST trust tier. Use only to supplement hard data, never as primary evidence.

---

## Cross-Validation Matrix

| # | Claim | Source 1 | Source 2 | Source 3 | Consistent? | Final Assessment |
|---|-------|---------|---------|---------|-------------|-----------------|
| 1 | [claim] | [value, ID] | [value, ID] | [value, ID] | Yes/No/Partial | [accepted/disputed/needs more data] |
| 2 | | | | | | |

---

## Normalized Comparison Table

**Normalization conditions**: [standard environment, methodology, units]

| Metric | [Tech A] | [Tech B] | [Tech C] | Primary Source | Normalization Notes |
|--------|---------|---------|---------|---------------|-------------------|
| | [value ± var] | [value ± var] | [value ± var] | [ID] | [adjustments made] |

---

## Evidence Gaps

| # | Missing Evidence | Why It Matters | Impact on Conclusions | Mitigation |
|---|-----------------|---------------|----------------------|-----------|
| 1 | [what's missing] | [why we need it] | [how conclusions are affected] | [what we can say despite the gap] |

---

## Methodology Concerns

| # | Concern | Affected Evidence | Risk | Mitigation |
|---|---------|------------------|------|-----------|
| 1 | [e.g., vendor-only benchmark] | [IDs: B3, B4] | Medium | [sought but didn't find independent reproduction] |
| 2 | [e.g., different hardware configs] | [IDs: B1 vs B2] | Low | [normalized using scaling factors from A1] |

---

## Evidence Collection Log

| Timestamp | Search Query | Source | Found? | Evidence ID | Notes |
|-----------|-------------|--------|--------|-------------|-------|
| [time] | [query used] | [WebSearch/WebFetch] | Y/N | [B1/A2/etc.] | [brief note] |

*This log enables reproducibility — anyone can re-run the same searches to verify or update the evidence.*
