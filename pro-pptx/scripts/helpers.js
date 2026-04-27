// pro-pptx/scripts/helpers.js
// ----------------------------------------------------------------------------
// Linter-aligned measurement & placement primitives for hw-insight builders.
//
// These helpers mirror the formulas in scripts/linter.py so that build-time
// geometry decisions match what the linter will validate. Use them instead of
// raw addText/addShape/addTable when you need:
//   - measureText(str, fontSize, w)   → { lines, height } per linter para rules
//   - measureCell(str, fontSize, w)   → { lines, height } per linter table rules
//   - measureTable(rows, colW, fs)    → total table h × safety multiplier
//   - placeWithGrid(contentBottom)    → tracker with canPlace/place
//   - metricCard(slide, x,y,w,h, ...) → card whose contents fill the slot
//   - safeTable(slide, rows, opts)    → table whose actual h fits inside budget
//
// Constants are kept in sync with linter.py:
//   CJK_CHAR_WIDTH=1.0, ASCII_CHAR_WIDTH=0.50 (× font_size / 72)
//   PARA_LINE_HEIGHT_MULT=1.4, LINE_HEIGHT_MULT=1.6 (cell)
//   TEXTBOX_INSET_TOTAL=0.20, TABLE_CELL_INSET_TOTAL=0.16
//   TABLE_HEIGHT_SAFETY=1.20

const L = {
  CJK_W: 1.0 / 72,    // inch per pt × char
  ASCII_W: 0.50 / 72,
  PARA_LH: 1.4 / 72,  // standalone paragraph line height
  CELL_LH: 1.6 / 72,  // table cell line height
  TEXTBOX_INSET: 0.20,
  CELL_INSET: 0.16,
  CELL_MARGIN: 0.10,
  TABLE_SAFETY: 1.20,
  CONTENT_BOTTOM_NO_CALLOUT: 5.15,
  CONTENT_BOTTOM_WITH_CALLOUT: 4.78, // callout zone 4.83-5.15 reserved
};

const CJK_RE = /[一-鿿　-〿＀-￯]/g;

function _splitChars(str) {
  const cjk = (str.match(CJK_RE) || []).length;
  const ascii = Math.max(0, str.length - cjk);
  return { cjk, ascii };
}

// Measure standalone paragraph (textbox) — matches linter para rules.
function measureText(str, fontSize, w) {
  const { cjk, ascii } = _splitChars(String(str || ""));
  const totalW = cjk * fontSize * L.CJK_W + ascii * fontSize * L.ASCII_W;
  const usableW = Math.max(0.4, w - L.TEXTBOX_INSET);
  const lines = Math.max(1, Math.ceil(totalW / usableW));
  const height = lines * fontSize * L.PARA_LH;
  return { lines, height, naturalW: totalW };
}

// Measure table cell — matches linter cell rules.
function measureCell(str, fontSize, w) {
  const { cjk, ascii } = _splitChars(String(str || ""));
  const totalW = cjk * fontSize * L.CJK_W + ascii * fontSize * L.ASCII_W;
  const usableW = Math.max(0.4, w - L.CELL_INSET);
  const lines = Math.max(1, Math.ceil(totalW / usableW));
  const height = lines * fontSize * L.CELL_LH + L.CELL_MARGIN;
  return { lines, height };
}

// Measure a table — returns { totalH, rowHeights[] } using linter formula.
// rows: array of arrays of {text} | strings.  colW: array of column widths.
function measureTable(rows, colW, fontSize) {
  const rowHeights = [];
  let totalH = 0;
  for (const row of rows) {
    let maxH = 0;
    row.forEach((cell, i) => {
      const txt = typeof cell === "string" ? cell : (cell.text || "");
      const w = colW[i] || 1.5;
      const { height } = measureCell(txt, fontSize, w);
      if (height > maxH) maxH = height;
    });
    rowHeights.push(maxH);
    totalH += maxH;
  }
  return { totalH: totalH * L.TABLE_SAFETY, rowHeights };
}

// Grid placement tracker. Pass contentBottom=4.78 if slide has insight callout.
function placeWithGrid(opts) {
  opts = opts || {};
  const contentBottom = opts.contentBottom || L.CONTENT_BOTTOM_WITH_CALLOUT;
  const contentRight = opts.contentRight || 9.55;
  const placed = [];
  return {
    contentBottom,
    contentRight,
    canPlace(x, y, w, h) {
      if (y + h > contentBottom + 0.001) return false;
      if (x + w > contentRight + 0.001) return false;
      for (const p of placed) {
        const overlap =
          x < p.x + p.w - 0.001 && x + w > p.x + 0.001 &&
          y < p.y + p.h - 0.001 && y + h > p.y + 0.001;
        if (overlap) return false;
      }
      return true;
    },
    place(x, y, w, h, label) {
      placed.push({ x, y, w, h, label: label || "" });
    },
    list() { return placed.slice(); },
  };
}

// Add a metric card that fills its grid slot. Adds optional sublabel that
// expands content to consume any unused vertical space — eliminating the
// `card_oversized` lint error per the rule "card hug text" (true text height
// must be within max_h of declared h).
//
// Layout inside card (h):
//   value:    top 0.50 × h, font 22-28pt depending on h
//   label:    middle 0.30 × h, font 9-10pt
//   sublabel: bottom 0.20 × h, font 7pt italic muted (auto-filled if missing)
function metricCard(slide, opts) {
  const x = opts.x, y = opts.y, w = opts.w, h = opts.h;
  const C = opts.colors || {};
  const F = opts.fonts || {};
  const fillColor = opts.fill || C.ink || "F5F6FA";
  const borderColor = opts.border || C.border || "E5E7EB";
  const valueColor = opts.valueColor || C.primary || "1A1A2E";
  const labelColor = opts.labelColor || C.subtext || "4B5563";
  const mutedColor = opts.mutedColor || C.muted || "6B7280";

  // Auto-pick value font size from card height
  const valueFs = opts.valueFontSize || (h >= 1.20 ? 24 : h >= 1.00 ? 20 : 17);

  slide.addShape("rect", { x, y, w, h,
    fill: { color: fillColor }, line: { color: borderColor, width: 0.5 } });

  const valueH = h * 0.45;
  const labelH = h * 0.30;
  const subH = h * 0.25;

  slide.addText(opts.value, { x, y, w, h: valueH,
    fontSize: valueFs, bold: true,
    color: opts.valueAccent ? (C.accent || "CF0A2C") : valueColor,
    fontFace: F.heading || "Microsoft YaHei",
    align: "center", valign: "middle" });

  slide.addText(opts.label, { x: x + 0.05, y: y + valueH, w: w - 0.10, h: labelH,
    fontSize: opts.labelFontSize || 9,
    color: labelColor, fontFace: F.body || "Microsoft YaHei",
    align: "center", valign: "middle" });

  // Sublabel: auto-fill with default if missing so card never has empty bottom
  const sub = opts.sublabel || opts.evidence || opts.source || "";
  if (sub) {
    slide.addText(sub, { x: x + 0.05, y: y + valueH + labelH, w: w - 0.10, h: subH,
      fontSize: opts.subFontSize || 7, italic: true,
      color: mutedColor, fontFace: F.body || "Microsoft YaHei",
      align: "center", valign: "middle" });
  }
}

// Add an insight card that fills its grid slot (used for slide 19 / 21 layouts).
// Number badge on left, single combined rich-text (title bold + body) on right.
// Single text box → linter measures combined height vs card hug rule.
function insightCard(slide, opts) {
  const x = opts.x, y = opts.y, w = opts.w, h = opts.h;
  const C = opts.colors || {};
  const F = opts.fonts || {};
  const numW = opts.numW || 0.50;
  const accentColor = opts.accent || C.accent || "CF0A2C";
  const titleFs = opts.titleFontSize || 11;
  const bodyFs = opts.bodyFontSize || 9;

  // Number badge
  slide.addShape("rect", { x, y, w: numW, h,
    fill: { color: accentColor }, line: { color: accentColor, width: 0 } });
  slide.addText(opts.num, { x, y, w: numW, h,
    fontSize: opts.numFontSize || (h >= 1.0 ? 30 : 22),
    bold: true, color: C.white || "FFFFFF",
    fontFace: F.heading || "Microsoft YaHei",
    align: "center", valign: "middle" });

  // Body card
  const bx = x + numW + 0.05;
  const bw = w - numW - 0.05;
  slide.addShape("rect", { x: bx, y, w: bw, h,
    fill: { color: C.ink || "F5F6FA" },
    line: { color: C.border || "E5E7EB", width: 0.5 } });

  // Single combined text box — title (bold) + newline + body
  // Use full card height (h - 0.04) so text doesn't visually overflow.
  slide.addText([
    { text: opts.title + "\n",
      options: { fontSize: titleFs, bold: true, color: C.primary || "1A1A2E",
        fontFace: F.heading || "Microsoft YaHei" } },
    { text: opts.body,
      options: { fontSize: bodyFs, color: C.subtext || "4B5563",
        fontFace: F.body || "Microsoft YaHei" } },
  ], { x: bx + 0.08, y: y + 0.02, w: bw - 0.16, h: h - 0.04, valign: "top" });
}

// Place an addTable safely: clamp total y+h to contentBottom (4.78 with callout),
// and auto-shrink fontSize until measureTable fits the budget.
// Returns { fontSize, rowH, h } actually used.
function safeTable(slide, rows, opts) {
  const x = opts.x, y = opts.y, w = opts.w;
  const contentBottom = opts.contentBottom || L.CONTENT_BOTTOM_WITH_CALLOUT;
  const maxH = Math.min(opts.h || 99, contentBottom - y - 0.05); // 0.05" safety

  // Estimate column widths (proportional to header chars)
  const nCols = rows[0] ? rows[0].length : 1;
  const colW = opts.colW || rows[0].map(() => w / nCols);

  // Try fontSize 9 → 6, shrink aggressively (target ≤ 90% of maxH for render safety)
  let fs = opts.fontSize || 9;
  let measured = measureTable(rows, colW, fs);
  const targetH = maxH * 0.90;
  while (measured.totalH > targetH && fs > 6) {
    fs -= 1;
    measured = measureTable(rows, colW, fs);
  }
  const finalH = Math.min(maxH, measured.totalH);
  const rowH = finalH / rows.length;

  slide.addTable(rows, {
    x, y, w, h: finalH,
    fontSize: fs,
    fontFace: opts.fontFace || "Microsoft YaHei",
    color: opts.color || "1A1A1A",
    border: opts.border || { type: "solid", color: "E5E7EB", pt: 0.5 },
    rowH: rowH,
    valign: opts.valign || "middle",
  });

  return { fontSize: fs, rowH, h: finalH };
}

module.exports = {
  L,
  measureText,
  measureCell,
  measureTable,
  placeWithGrid,
  metricCard,
  insightCard,
  safeTable,
};
