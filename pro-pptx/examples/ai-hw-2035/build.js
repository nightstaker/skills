// AI+HW 2035 洞察报告 · 存储深度展开版 (linter-hardened)
//
// Reproducible build script for the example deck under
// pro-pptx/examples/ai-hw-2035. See README.md for prerequisites and the
// list of images to download. Run with:
//   npm install pptxgenjs        # one-time
//   node build.js                # writes ./ai_hw_2035_insight.pptx
//
// Paths default to local relatives; override via env vars when needed.
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "AI+HW 2035 存储深度展开版";

const C = {
  primary: "1A1A2E", white: "FFFFFF", accent: "CF0A2C", text: "1A1A1A",
  muted: "6B7280", border: "E5E7EB", highlight: "EFF3FF", navymid: "2D3A6B",
  ink: "F5F6FA", subtext: "4B5563", alerttint: "FFF0F0", dimgray: "F0F0F0",
};
const F = { heading: "Microsoft YaHei", body: "Microsoft YaHei" };
const LOGO = process.env.HW_LOGO ||
  path.resolve(__dirname, "../../templates/hw-insight/assets/logo.png");
const IMG_DIR = process.env.IMG_DIR || path.resolve(__dirname, "images");
const OUT_PATH = process.env.OUT_PATH ||
  path.resolve(__dirname, "ai_hw_2035_insight.pptx");

const SECTIONS = [
  { label: "背景", sub: ["节奏错位", "核心引用"] },
  { label: "愿景", sub: ["三层互馈", "九层堆栈"] },
  { label: "存储", sub: ["存储墙", "内存瓶颈", "CIM全景", "架构对比", "HBM路线", "光互联", "算法感知", "技术雷达"] },
  { label: "算法", sub: ["范式迁移"] },
  { label: "应用", sub: ["电力危机", "采用鸿沟"] },
  { label: "行动", sub: ["三建议"] },
];

function addTitle(slide, text) {
  slide.addText(text, {
    x: 0.45, y: 0.27, w: 9.1, h: 0.40,
    fontSize: 20, bold: true, color: C.accent, fontFace: F.heading,
    align: "left", valign: "middle",
  });
  slide.addShape("line", {
    x: 0.45, y: 0.70, w: 9.1, h: 0, line: { color: C.border, width: 0.75 },
  });
}

function addNav(slide, sectionIdx, subIdx) {
  const cjkW = 0.055, pad = 0.10, gap = 0.02;
  const nat = (lbl) => lbl.length * cjkW + pad;
  const r1w = SECTIONS.map(s => nat(s.label));
  const r1Total = r1w.reduce((a,b)=>a+b,0) + (SECTIONS.length - 1) * gap;
  let maxR2 = 0;
  SECTIONS.forEach(s => {
    const w = s.sub.map(nat).reduce((a,b)=>a+b,0) + (s.sub.length - 1) * gap;
    if (w > maxR2) maxR2 = w;
  });
  const masterW = Math.max(r1Total, maxR2);
  const rightX = 9.95;
  const r1Space = masterW - (SECTIONS.length - 1) * gap;
  const r1Sum = r1w.reduce((a,b)=>a+b,0);
  const r1Scaled = r1w.map(w => w * (r1Space / r1Sum));
  let x = rightX - masterW;
  for (let i = 0; i < SECTIONS.length; i++) {
    const w = r1Scaled[i];
    const active = (i === sectionIdx);
    slide.addShape("rect", { x, y: 0.02, w, h: 0.10,
      fill: { color: active ? C.accent : C.border }, line: { color: active ? C.accent : C.border, width: 0.25 },
    });
    slide.addText(SECTIONS[i].label, { x, y: 0.02, w, h: 0.10, fontSize: 5,
      bold: true, color: active ? C.white : C.text, fontFace: F.heading, align: "center", valign: "middle", margin: 0,
    });
    x += w + gap;
  }
  if (sectionIdx >= 0) {
    const sub = SECTIONS[sectionIdx].sub;
    const r2w = sub.map(nat);
    const r2Sum = r2w.reduce((a,b)=>a+b,0);
    const r2Space = masterW - (sub.length - 1) * gap;
    const r2Scaled = r2w.map(w => w * (r2Space / r2Sum));
    let x2 = rightX - masterW;
    for (let i = 0; i < sub.length; i++) {
      const w = r2Scaled[i];
      const active = (i === subIdx);
      slide.addShape("rect", { x: x2, y: 0.14, w, h: 0.10,
        fill: { color: active ? C.accent : C.border }, line: { color: active ? C.accent : C.border, width: 0.25 },
      });
      slide.addText(sub[i], { x: x2, y: 0.14, w, h: 0.10, fontSize: 5,
        bold: true, color: active ? C.white : C.text, fontFace: F.heading, align: "center", valign: "middle", margin: 0,
      });
      x2 += w + gap;
    }
  }
}

// Skip image silently when file is absent (so the script still runs without
// downloading every figure listed in README.md).
function safeAddImage(slide, opts) {
  if (opts.path && fs.existsSync(opts.path)) {
    slide.addImage(opts);
  } else {
    console.warn("missing image:", opts.path);
  }
}

function addFooter(slide, page, total) {
  slide.addText(`Page ${page}/${total}`, { x: 0.5, y: 5.25, w: 1.6, h: 0.22,
    fontSize: 9, color: C.muted, fontFace: "Arial", align: "left", valign: "middle",
  });
  slide.addText("Huawei Confidential", { x: 2.2, y: 5.25, w: 2.8, h: 0.22,
    fontSize: 9, color: C.muted, fontFace: "Arial", align: "left", italic: true, valign: "middle",
  });
  if (fs.existsSync(LOGO)) {
    slide.addImage({ path: LOGO, x: 8.82, y: 5.25, w: 1.08, h: 0.23, altText: "Huawei logo" });
  }
}

function fixed(slide, page, total, section, sub, withNav = true) {
  if (withNav) addNav(slide, section, sub);
  addFooter(slide, page, total);
}

// Standard callout strip — single text box with fill (avoids shape-vs-text overlap)
function addCallout(slide, text) {
  slide.addText(text, {
    x: 0.45, y: 4.60, w: 9.10, h: 0.50,
    fontSize: 12, bold: true, color: C.accent, fontFace: F.heading,
    align: "left", valign: "middle",
    fill: { color: C.highlight },
    line: { color: C.accent, width: 1 },
    margin: 0.08,
  });
}

// Consolidated metric block — value + label + optional sub in single fill+text element
function addMetric(slide, x, y, w, h, value, label, sub, valueSize) {
  valueSize = valueSize || 40;
  const segs = [
    { text: value + "\n", options: { fontSize: valueSize, bold: true, color: C.primary } },
    { text: label, options: { fontSize: 12, bold: true, color: C.primary } },
  ];
  if (sub) {
    segs.push({ text: "\n" + sub, options: { fontSize: 10, color: C.muted } });
  }
  slide.addText(segs, {
    x, y, w, h,
    fontFace: F.heading, align: "center", valign: "middle",
    fill: { color: C.ink },
    line: { color: C.border, width: 1 },
    paraSpaceAfter: 2,
  });
}

const TOTAL = 18;

// -------- Slide 1: Cover --------
function slideCover() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  s.addText("AI+HW 2035：塑造下一个十年", { x: 0.55, y: 1.0, w: 9.0, h: 1.2,
    fontSize: 38, bold: true, color: C.accent, fontFace: F.heading, align: "left", valign: "middle",
  });
  s.addShape("line", { x: 0.55, y: 2.30, w: 3.0, h: 0, line: { color: C.accent, width: 2 } });
  s.addText("存储为核心视角的技术洞察 · 2035 十年路线图解读", { x: 0.55, y: 2.50, w: 8.0, h: 0.55,
    fontSize: 16, color: C.text, fontFace: F.body, align: "left",
  });
  s.addText("来源：arXiv 2603.05225v1 · 作者: Deming Chen、Jason Cong、Yann LeCun、Anima Anandkumar 等 · 许可: CC BY 4.0", {
    x: 0.55, y: 3.20, w: 8.8, h: 0.30, fontSize: 10, color: C.muted, fontFace: "Arial", align: "left",
  });
  s.addText("目标读者：Chief Architect / 技术战略 / 基础设施规划 · 关键词：intelligence per joule · 存储墙 · CIM · 3D/HBM · 光互联", {
    x: 0.55, y: 3.55, w: 8.8, h: 0.45, fontSize: 9, color: C.muted, fontFace: "Arial", italic: true, align: "left",
  });
  addFooter(s, 1, TOTAL);
  s.addNotes("Cover slide. Source: arXiv:2603.05225v1, March 2026, CC BY 4.0.");
}

// -------- Slide 2: Insight-summary --------
function slideInsight() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTitle(s, "核心命题：从算力扩张到每焦耳智能（intelligence per joule）");
  s.addShape("rect", { x: 0.45, y: 0.75, w: 9.1, h: 0.65,
    fill: { color: C.alerttint }, line: { color: C.accent, width: 2 } });
  s.addText("2035 年目标：AI 训练与推理综合能效提升 1000×；5 年内先达到 100×（高置信度）。单纯堆 GPU+HBM 的规模化路径到 2030 前后触顶，护城河转向封装 / 光互联 / 存算一体 / AI-EDA。", {
    x: 0.55, y: 0.78, w: 8.9, h: 0.58, fontSize: 12, bold: true, color: C.accent,
    fontFace: F.heading, align: "left", valign: "middle",
  });
  // Pillar heights compacted so card hugs text
  const pillars = [
    { title: "① 跨层协同", body: [
      "• 器件—封装—架构—编译—算法\n  一体优化，拒绝单层独立演进",
      "• 五对必须打通：模型↔芯片布局、\n  调度↔散热、互联↔数据流、\n  训练目标↔部署形态、\n  可靠性↔硬件原语",
      "• AI-in-loop EDA：设计周期从\n  『年』压到『周/月』",
      "• 十年目标：硅设计周期 ≥ 3× 提速\n  且 PPA 可预测",
      "• 反模式：把可靠性作为软件补丁"
    ]},
    { title: "② 存储中心化", body: [
      "• 数据搬移能耗已超算术能耗；\n  互联是最大能耗源（远超 ALU）",
      "• CIM + 近存计算 + 3D 堆叠 +\n  存储中心数据流 全面主流化",
      "• LLM 推理是内存受限：DRAM BW\n  仅 1.6×/2 年，算力 3×/2 年",
      "• 2035 目标：>>100× 端到端能效，\n  集群可持续利用率 ≥ 60%",
      "• 光互联重塑访存：带宽近乎与\n  距离无关，50 fJ/bit 区间"
    ]},
    { title: "③ 异构 + 自演化", body: [
      "• CPU+GPU+可重构+领域 ASIC+\n  量子，全局光互联连接",
      "• 大-小模型共生：开源可蒸馏\n  教师 → 边缘 ~20B 活跃参数 SLM",
      "• 多智能体 + Metaverse 级系统：\n  稀疏通信、可解释内核",
      "• 自优化流水线：模型、编译、\n  调度作为单一目标联合训练",
      "• 数据/代码/权重的法律可组合性\n  （open teachers with distillation\n  rights）"
    ]},
  ];
  const xs = [0.45, 3.55, 6.65];
  for (let i = 0; i < 3; i++) {
    const x = xs[i];
    const body = pillars[i].body.map(b => ({ text: b + "\n", options: { fontSize: 11, color: C.text } }));
    const all = [
      { text: pillars[i].title + "\n", options: { fontSize: 13, bold: true, color: C.primary } },
      ...body
    ];
    s.addText(all, {
      x, y: 1.50, w: 2.90, h: 2.80,
      fontFace: F.heading, valign: "top", align: "left",
      fill: { color: C.ink }, line: { color: C.border, width: 1 },
      margin: 0.10, paraSpaceAfter: 2,
    });
  }
  // Supplementary strip below pillars for density
  s.addText([
    { text: "三大支柱相互耦合：", options: { fontSize: 11, bold: true, color: C.primary } },
    { text: "跨层协同决定能不能做到；存储中心化决定能耗高不高；异构+自演化决定是否可持续演进。", options: { fontSize: 11, color: C.text } },
  ], { x: 0.45, y: 4.40, w: 9.10, h: 0.42, fontFace: F.body, valign: "middle", align: "left" });
  fixed(s, 2, TOTAL, -1, -1, false);
  s.addNotes("Insight Summary. Source: arXiv:2603.05225v1. 1000x efficiency is decade-long target; 100x in 5 years cited with high confidence.");
}

// -------- Slide 3: 三节奏错位 --------
function slideRhythm() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTitle(s, "算法以月、软件以季、硬件以年演进，错位加速基础设施的非收敛风险");
  const blocks = [
    { v: "月", l: "算法演进周期", sub: "· SSM、JEPA、扩散蒸馏\n· 每月均有新推理算法\n· 开源社区节奏" },
    { v: "季度", l: "软件框架演进", sub: "· PyTorch、vLLM、TRT-LLM\n· 年均数次大版本\n· 内核级重构频繁" },
    { v: "年", l: "芯片 / 系统演进", sub: "· tape-out → 量产 18m+\n· 通用 IC 通常 3 年\n· 先进封装 4-5 年" },
  ];
  const xs = [0.45, 3.45, 6.45];
  for (let i = 0; i < 3; i++) {
    addMetric(s, xs[i], 0.80, 2.90, 1.80, blocks[i].v, blocks[i].l, blocks[i].sub, 36);
  }
  // Below: supplementary table/text for density
  s.addText([
    { text: "错位的三个可观测后果：\n", options: { fontSize: 12, bold: true, color: C.primary } },
    { text: "① 芯片一出厂就已落后于最新算法；\n", options: { fontSize: 11, color: C.text } },
    { text: "② 软件栈滞后硬件到货 6–12 个月；\n", options: { fontSize: 11, color: C.text } },
    { text: "③ 真实集群利用率仅 5–20%。\n\n", options: { fontSize: 11, color: C.text } },
    { text: "补救方向：AI-in-loop EDA + Chiplet 生态 + 硬件感知编译器 + 性能可移植运行时。", options: { fontSize: 11, bold: true, color: C.navymid } },
  ], { x: 0.45, y: 2.70, w: 9.10, h: 1.80, fontFace: F.body, valign: "top" });
  addCallout(s, "结论：任何单点优化都被快速稀释，必须把『AI-in-loop EDA + Chiplet 生态』当作系统方法。");
  fixed(s, 3, TOTAL, 0, 0);
  s.addNotes("Source: arXiv:2603.05225v1 §1. Innovation Speed Mismatch framing.");
}

// -------- Slide 4: 核心引用 --------
function slideQuote() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  s.addText("今天的算法是为昨天的系统设计的，\n明天的芯片是为今天的工作负载优化的。", {
    x: 0.55, y: 1.05, w: 8.9, h: 2.20, fontSize: 22, bold: true, color: C.accent,
    fontFace: F.heading, align: "center", valign: "middle",
  });
  s.addShape("line", { x: 4.5, y: 3.35, w: 1.0, h: 0, line: { color: C.accent, width: 1.5 } });
  s.addText("— Chen, Cong, LeCun, Anandkumar et al.\nAI+HW 2035: Shaping the Next Decade (arXiv:2603.05225v1, 2026 · CC BY 4.0)", {
    x: 0.55, y: 3.45, w: 8.9, h: 0.55, fontSize: 11, color: C.muted,
    fontFace: "Arial", align: "center", italic: true,
  });
  // Supporting rationale for density
  s.addShape("rect", { x: 0.45, y: 4.10, w: 9.10, h: 0.40,
    fill: { color: C.ink }, line: { color: C.border, width: 0.5 } });
  s.addText("这句论断成为全篇的论证起点：它把『性能工程问题』升级为『规划范式问题』，要求跨层重新对齐。", {
    x: 0.55, y: 4.12, w: 8.90, h: 0.36, fontSize: 11, italic: true, color: C.text,
    fontFace: F.body, align: "center", valign: "middle",
  });
  addCallout(s, "这句论断是全文的『技术假设』——后续每一节都在验证、限定或放大它。");
  fixed(s, 4, TOTAL, 0, 1);
  s.addNotes("Framing quote, sets up the rest of the deck.");
}

// -------- Slide 5: 三层互馈 --------
function slideThreeLayer() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTitle(s, "三层互馈架构：硬件—算法—应用跨层反馈闭环，而非单向堆叠");
  const img = `${IMG_DIR}/aihw_fig1.png`;
  safeAddImage(s, { path: img, x: 0.45, y: 0.78, w: 5.10, h: 2.60,
    altText: "Three-layer cross-layer synergy diagram: Hardware, Algorithms, Applications with feedback loop" });
  s.addText("图 1：跨层反馈架构（源自原论文 Figure 1）", {
    x: 0.45, y: 3.42, w: 5.10, h: 0.25, fontSize: 7.5, italic: true, color: C.muted,
    fontFace: "Arial", align: "center",
  });
  s.addText([
    { text: "硬件层（基础能力）：\n", options: { fontSize: 13, bold: true, color: C.primary } },
    { text: "3D 集成 / 存算一体 / 光互联 /\n量子—经典混合 / AI 优化拓扑\n\n", options: { fontSize: 11, color: C.text } },
    { text: "算法层（翻译能力到硬件）：\n", options: { fontSize: 13, bold: true, color: C.primary } },
    { text: "硬件感知训练、低精度稀疏化、\n可微分仿真、JEPA、自进化栈\n\n", options: { fontSize: 11, color: C.text } },
    { text: "应用层（驱动度量与需求）：\n", options: { fontSize: 13, bold: true, color: C.primary } },
    { text: "科学发现、物理 AI、边云协同、\n以『每焦耳智能』为首要 KPI", options: { fontSize: 11, color: C.text } },
  ], { x: 5.70, y: 0.78, w: 3.85, h: 3.60, fontFace: F.body, valign: "top" });
  addCallout(s, "闭环才能让『算法演进→硬件特化→新算法可能性』形成飞轮，打破闭环的单层优化必被对端拖累。");
  fixed(s, 5, TOTAL, 1, 0);
  s.addNotes("Image source: Figure 1 of arXiv:2603.05225v1 (CC BY 4.0).");
}

// -------- Slide 6: 九层堆栈表 --------
function slideStackTable() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTitle(s, "九层技术堆栈：AI+HW 路线图的十条可落地押注清单");
  s.addText("九层技术堆栈 × 关键技术 × 主要挑战", {
    x: 0.45, y: 0.78, w: 9.10, h: 0.22, fontSize: 9, bold: true, color: C.navymid, fontFace: F.heading,
  });
  const rows = [
    [{ text: "层级", options: { bold: true, color: C.white, fill: C.primary } },
     { text: "关键技术", options: { bold: true, color: C.white, fill: C.primary } },
     { text: "主要挑战", options: { bold: true, color: C.white, fill: C.primary } }],
    ["器件/材料", "后-CMOS（GaN/CNT/2D）、光子集成、超导器件", "良率、器件变异、噪声、漂移、成本"],
    ["3D 集成", "单片堆叠、Chiplet、垂直集成、HBM interposer", "散热、供电、良率、可测性、标准化"],
    ["模拟/存算一体", "CIM、模拟加速器、阻变交叉阵列", "噪声、精度、校准、稳定性"],
    ["光 / 光电", "片内/片间光链路、光学矩阵乘法", "与电子的工艺整合"],
    ["散热 & 供电", "液浸、微流道、背面供电", "系统复杂度、热-电协同"],
    ["存储层次", "HBM 后继、统一内存、NVRAM、压缩", "持续存储墙、带宽瓶颈"],
    ["互联", "工作负载感知拓扑、全局光链路", "规模化下的时延与协调开销"],
    ["编译/运行时", "硬件感知编译器、自动调优", "性能可移植、动态调度、功耗感知"],
    ["算法", "稀疏/低秩/量化、训练推理高效化", "硬件感知、模块化、鲁棒性、局部性"],
  ];
  s.addTable(rows, {
    x: 0.45, y: 1.05, w: 9.10, fontSize: 8, fontFace: F.body, color: C.text,
    border: { type: "solid", pt: 0.5, color: C.border },
    colW: [1.30, 4.10, 3.70], autoPage: false, valign: "middle",
  });
  addCallout(s, "存储 / 互联 / 封装 三行是系统能效的决定性杠杆，比单芯片工艺更值得押注。");
  fixed(s, 6, TOTAL, 1, 1);
  s.addNotes("Source: arXiv:2603.05225v1 Table 1, distilled.");
}

// -------- Slide 7: 存储墙 --------
function slideMemWall() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTitle(s, "存储墙：Transformer 算力以 750×/2 年扩张，DRAM 带宽仅以 1.6×/2 年追赶");
  const img = `${IMG_DIR}/memwall_x3.png`;
  safeAddImage(s, { path: img, x: 0.45, y: 0.78, w: 5.40, h: 3.10,
    altText: "Training FLOPs 750x/2yr vs Moore 2x/2yr" });
  s.addText("图：Training FLOPs 扩张 vs Moore's Law（Gholami et al., arXiv:2403.14123）", {
    x: 0.45, y: 3.92, w: 5.40, h: 0.22, fontSize: 7.5, italic: true, color: C.muted,
    fontFace: "Arial", align: "center",
  });
  s.addText([
    { text: "算-存剪刀差\n", options: { fontSize: 13, bold: true, color: C.primary } },
    { text: "• 算力 3×/2 年（峰值 FLOPS）\n", options: { fontSize: 11, color: C.text } },
    { text: "• DRAM BW 1.6×/2 年\n", options: { fontSize: 11, color: C.text } },
    { text: "• 互联 BW 1.4×/2 年\n\n", options: { fontSize: 11, color: C.text } },
    { text: "访存成本\n", options: { fontSize: 13, bold: true, color: C.primary } },
    { text: "• 片外 DRAM 单次访问\n  ≈ 640 pJ（100 ns）\n", options: { fontSize: 11, color: C.text } },
    { text: "• 算术操作 < 1 pJ（1 ns）\n", options: { fontSize: 11, color: C.text } },
    { text: "• 能耗差 ≈ 600×", options: { fontSize: 11, bold: true, color: C.accent } },
  ], { x: 5.95, y: 0.80, w: 3.60, h: 3.60, fontFace: F.body, valign: "top" });
  addCallout(s, "推理瓶颈不是算力而是存储：单向堆 FLOPS 的方案在用 600× 能耗溢价换取边际吞吐。");
  fixed(s, 7, TOTAL, 2, 0);
  s.addNotes("Source image: Gholami et al. AI and Memory Wall (arXiv:2403.14123v1). Numbers: 640 pJ/access, <1 pJ/op from Horowitz energy model.");
}

// -------- Slide 8: 内存受限 --------
function slideMemBound() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTitle(s, "LLM 推理是内存受限的：瓶颈从 FLOPS 转移至 DRAM 带宽 × 模型驻留");
  const blocks = [
    { v: "3×", l: "HW FLOPS / 2 年" },
    { v: "1.6×", l: "DRAM 带宽 / 2 年" },
    { v: "1.4×", l: "互联带宽 / 2 年" },
  ];
  const xs = [0.45, 3.45, 6.45];
  for (let i = 0; i < 3; i++) {
    addMetric(s, xs[i], 0.80, 2.90, 0.75, blocks[i].v, blocks[i].l, null, 22);
  }
  const img = `${IMG_DIR}/memwall_x1.png`;
  safeAddImage(s, { path: img, x: 0.45, y: 2.15, w: 4.80, h: 2.10,
    altText: "HW FLOPS vs DRAM BW vs Interconnect BW scaling" });
  s.addText("图：HW FLOPS / DRAM BW / 互联 BW 十年演进（Gholami et al., 2024）", {
    x: 0.45, y: 4.25, w: 4.80, h: 0.22, fontSize: 7.5, italic: true, color: C.muted,
    fontFace: "Arial", align: "center",
  });
  s.addText([
    { text: "推理工作负载三大事实：\n", options: { fontSize: 13, bold: true, color: C.primary } },
    { text: "• KV Cache 尺寸随上下文线性膨胀；\n  >70% 推理时间花在 HBM↔SRAM 搬运\n", options: { fontSize: 11, color: C.text } },
    { text: "• Agentic AI 把『单次前向』变成\n  『闭环迭代』，DRAM 访问再上量级\n", options: { fontSize: 11, color: C.text } },
    { text: "• 集群利用率 5–20%，绝大部分\n  空等在等 DRAM 返回", options: { fontSize: 11, color: C.text } },
  ], { x: 5.35, y: 2.20, w: 4.20, h: 2.30, fontFace: F.body, valign: "top" });
  addCallout(s, "『LLM 推理 = 内存受限』。优化方向：KV 压缩、SSM/Mamba 替代 Attention、把计算搬到存储旁边（CIM/PIM）。");
  fixed(s, 8, TOTAL, 2, 1);
  s.addNotes("Data: arXiv:2603.05225v1 §4.2 + memory wall analysis. 5-20% utilization from §4.4.");
}

// -------- Slide 9: CIM 四象限 --------
function slideCIMQuad() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTitle(s, "存算一体四象限：COM → CNM → CIM-P → CIM-A，每一步把『数据搬移』向存储阵列压缩");
  const img = `${IMG_DIR}/cim_overview.png`;
  safeAddImage(s, { path: img, x: 0.45, y: 0.78, w: 6.10, h: 2.15,
    altText: "COM vs CNM vs CIM-P vs CIM-A architecture comparison" });
  s.addText("图：COM/CNM/CIM-P/CIM-A 四象限（Zhou et al., arXiv:2401.14428, 2024）", {
    x: 0.45, y: 2.96, w: 6.10, h: 0.22, fontSize: 7.5, italic: true, color: C.muted,
    fontFace: "Arial", align: "center",
  });
  const rows = [
    [{ text: "范式", options: { bold: true, color: C.white, fill: C.primary } },
     { text: "计算发生在", options: { bold: true, color: C.white, fill: C.primary } }],
    ["COM", "处理器（冯氏）"],
    ["CNM", "存储近侧逻辑"],
    ["CIM-P", "外围电路内"],
    ["CIM-A", "存储阵列内（模拟）"],
  ];
  s.addTable(rows, {
    x: 6.65, y: 0.80, w: 2.90, h: 1.80, fontSize: 9, fontFace: F.body, color: C.text,
    border: { type: "solid", pt: 0.5, color: C.border },
    colW: [0.95, 1.95], rowH: 0.36, valign: "middle",
  });
  s.addText([
    { text: "CIM 关键事实：\n", options: { fontSize: 12, bold: true, color: C.primary } },
    { text: "• CIM-A 在 MVM 上可达 10–100× 能效，因为权重不再移动\n", options: { fontSize: 10, color: C.text } },
    { text: "• 权重驻留 + 位切片；DAC 驱动、ADC 读出；列方向自然累加\n", options: { fontSize: 10, color: C.text } },
    { text: "• 载体：SRAM（数字）/ ReRAM / PCM / FeFET（模拟）；SRAM 稳、ReRAM 密\n", options: { fontSize: 10, color: C.text } },
    { text: "• 催生算法机会：噪声感知训练、低精度量化、近似网络——硬件的统计性被显式利用", options: { fontSize: 10, color: C.text } },
  ], { x: 0.45, y: 3.30, w: 9.10, h: 1.20, fontFace: F.body, valign: "top" });
  addCallout(s, "CIM-A 是近五年能效最高的 AI 原语之一，产业化卡在『模拟噪声 × 工艺 × 编程模型』三重耦合。");
  fixed(s, 9, TOTAL, 2, 2);
  s.addNotes("Image source: Zhou et al. (arXiv:2401.14428v1, 2024).");
}

// -------- Slide 10: 架构对比 --------
function slideArchCompare() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTitle(s, "内存中心架构 vs 冯·诺依曼：把『命令 f → 数据 D』替代『数据 D → 处理器』");
  // Left header
  s.addText("(A) 冯氏：计算在处理器", {
    x: 0.45, y: 0.76, w: 4.80, h: 0.30, fontSize: 11, bold: true, color: C.primary,
    fontFace: F.heading, align: "center", valign: "middle",
  });
  const img = `${IMG_DIR}/cim_memcentric.png`;
  safeAddImage(s, { path: img, x: 0.45, y: 1.10, w: 4.80, h: 2.80,
    altText: "Memory-centric vs compute-centric architecture comparison (Zhou et al.)" });
  s.addText("图：存储中心 vs 冯氏对照（Zhou et al., arXiv:2401.14428）", {
    x: 0.45, y: 3.93, w: 4.80, h: 0.22, fontSize: 7.5, italic: true, color: C.muted,
    fontFace: "Arial", align: "center",
  });
  // Right panel — consolidated text+fill; expand content to fill box
  s.addText([
    { text: "(B) 存储中心：计算在存储（CIM）\n\n", options: { fontSize: 12, bold: true, color: C.primary } },
    { text: "核心差异：\n", options: { fontSize: 11, bold: true, color: C.primary } },
    { text: "• 传送命令 f（1001）而非原始数据 D\n", options: { fontSize: 11, color: C.text } },
    { text: "• 只返回 f(D)，总线占用数量级下降\n", options: { fontSize: 11, color: C.text } },
    { text: "• 外围电路变为『计算—感知外围』\n", options: { fontSize: 11, color: C.text } },
    { text: "• 权重驻留（weight-stationary）\n\n", options: { fontSize: 11, color: C.text } },
    { text: "系统级意义：\n", options: { fontSize: 11, bold: true, color: C.primary } },
    { text: "• 互联带宽需求 ↓；搬移能耗 ↓\n", options: { fontSize: 11, color: C.text } },
    { text: "• 存储层次与计算层次合流\n", options: { fontSize: 11, color: C.text } },
    { text: "• 访存模式可预测，近似计算可接受\n\n", options: { fontSize: 11, color: C.text } },
    { text: "代价：\n", options: { fontSize: 11, bold: true, color: C.primary } },
    { text: "• 需硬件感知编译器与噪声感知训练\n", options: { fontSize: 11, color: C.text } },
    { text: "• 工艺与编程模型特化、任务受限", options: { fontSize: 11, color: C.text } },
  ], {
    x: 5.40, y: 0.76, w: 4.15, h: 2.20,
    fontFace: F.body, valign: "top", align: "left",
    fill: { color: C.highlight }, line: { color: C.navymid, width: 1 },
    margin: 0.08,
  });
  // Trade-off row — single-line tags
  s.addText("冯氏：通用强但搬移成本爆炸", {
    x: 0.45, y: 4.18, w: 4.80, h: 0.30, fontSize: 10, italic: true, color: C.muted,
    fontFace: F.body, align: "center", valign: "middle",
  });
  s.addText("存算合流：高能效但任务特化", {
    x: 5.40, y: 4.18, w: 4.15, h: 0.30, fontSize: 10, italic: true, color: C.muted,
    fontFace: F.body, align: "center", valign: "middle",
  });
  addCallout(s, "存算合流不是单点优化，而是对整个冯氏抽象栈（ISA / Cache / DRAM / 编译器）的一次重置。");
  fixed(s, 10, TOTAL, 2, 3);
  s.addNotes("Image: Zhou et al. (arXiv:2401.14428v1).");
}

// -------- Slide 11: HBM 路线 --------
function slideHBM() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTitle(s, "HBM 路线图：从 HBM3E 的 1.2 TB/s 到 HBM4 的 2 TB/s，单点带宽天花板已清晰");
  s.addText("三大厂商 HBM 路线演进对照（2024–2028）", {
    x: 0.45, y: 0.78, w: 9.10, h: 0.22, fontSize: 9, bold: true, color: C.navymid, fontFace: F.heading,
  });
  const rows = [
    [{ text: "代次", options: { bold: true, color: C.white, fill: C.primary } },
     { text: "堆叠", options: { bold: true, color: C.white, fill: C.primary } },
     { text: "Pin 速率", options: { bold: true, color: C.white, fill: C.primary } },
     { text: "位宽", options: { bold: true, color: C.white, fill: C.primary } },
     { text: "Stack 带宽", options: { bold: true, color: C.white, fill: C.primary } },
     { text: "容量", options: { bold: true, color: C.white, fill: C.primary } },
     { text: "量产 / 预计", options: { bold: true, color: C.white, fill: C.primary } }],
    ["HBM3", "8-Hi", "6.4 Gbps", "1024", "819 GB/s", "24 GB", "2022–2024"],
    ["HBM3E (8-Hi)", "8-Hi", "9.2 Gbps", "1024", "1.15 TB/s", "24 GB", "2024"],
    ["HBM3E (12-Hi)", "12-Hi", "9.2 Gbps", "1024", "1.18 TB/s", "36 GB", "2024–2025"],
    ["HBM4", "12-Hi", "~7.85 Gbps", "2048", "≈ 2.0 TB/s", "36 GB", "2026（Rubin）"],
    ["HBM4E", "16-Hi", "≥ 10 Gbps", "2048", "≥ 2.5 TB/s", "48+ GB", "2027（预计）"],
    ["HBM5（规划）", "16-Hi+", "≥ 14 Gbps", "2048-4096", "≥ 4 TB/s", "64+ GB", "2028+（预计）"],
  ];
  s.addTable(rows, {
    x: 0.45, y: 1.05, w: 9.10, h: 2.95, fontSize: 9, fontFace: F.body, color: C.text,
    border: { type: "solid", pt: 0.5, color: C.border },
    colW: [1.45, 0.85, 1.25, 1.00, 1.55, 1.00, 2.00], rowH: 0.42, valign: "middle",
  });
  s.addText([
    { text: "三个信号： ", options: { fontSize: 11, bold: true, color: C.primary } },
    { text: "① 位宽 1024→2048 需 base-die 重新设计； ", options: { fontSize: 10, color: C.text } },
    { text: "② HBM4E 起热阻/供电成本 > 信号成本； ", options: { fontSize: 10, color: C.text } },
    { text: "③ 单 stack 带宽放缓，未来靠多 stack × 光互联。", options: { fontSize: 10, color: C.text } },
  ], { x: 0.45, y: 4.08, w: 9.10, h: 0.50, fontFace: F.body, valign: "top" });
  addCallout(s, "单 Stack 带宽曲线 2028 后显著平台化，HBM 必须与 3D 集成 + 光互联 合成能效路线。");
  fixed(s, 11, TOTAL, 2, 4);
  s.addNotes("HBM4 2TB/s 2048-bit Rubin 2026: Micron public roadmap. HBM3E 1.18TB/s 12-Hi: Samsung public spec. HBM4E/HBM5 projections: SemiAnalysis, Tom's Hardware.");
}

// -------- Slide 12: 光互联 --------
function slidePhotonic() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTitle(s, "光互联重塑访存：单位能耗逼近 50 fJ/bit，带宽近乎与距离无关");
  const blocks = [
    { v: "50 fJ", l: "每 bit 能耗（2025 demo）" },
    { v: "800 Gb/s", l: "单通道带宽（CPO / OCI）" },
    { v: "0.3 mm²", l: "80 组 TX/RX 面积密度" },
  ];
  const xs = [0.45, 3.45, 6.45];
  for (let i = 0; i < 3; i++) {
    addMetric(s, xs[i], 0.80, 2.90, 1.15, blocks[i].v, blocks[i].l, null, 28);
  }
  s.addText([
    { text: "为什么光互联对存储至关重要：\n", options: { fontSize: 13, bold: true, color: C.primary } },
    { text: "• 电链路『距离 × 带宽 × 能耗』高度耦合；光链路在 0.5 m–100 m 范围能耗几乎不变\n", options: { fontSize: 11, color: C.text } },
    { text: "• Co-Packaged Optics (CPO) 把光引擎搬到封装内：HBM-side ↔ GPU-side 不再受 PCB 限制\n", options: { fontSize: 11, color: C.text } },
    { text: "• 片内 SiN 波导可作为晶圆级存储总线，把多个 HBM stack 拼成『大一块逻辑内存』\n", options: { fontSize: 11, color: C.text } },
    { text: "• 典型厂商进展：Intel OCI（多 Tbps）、Ayar Labs TeraPHY、IBM / imec CPO、NVIDIA Quantum-X Photonics\n\n", options: { fontSize: 11, color: C.text } },
    { text: "系统含义：\n", options: { fontSize: 13, bold: true, color: C.primary } },
    { text: "• 光互联不是『更快网卡』，而是让存储中心架构跨 die / 跨机柜 / 跨机房 的使能技术", options: { fontSize: 11, bold: true, color: C.text } },
  ], { x: 0.45, y: 2.00, w: 9.10, h: 2.45, fontFace: F.body, valign: "top" });
  addCallout(s, "把光互联从『IO 优化』升级为『访存一等公民』，才是 2030 前后突破 HBM 单点天花板的唯一通路。");
  fixed(s, 12, TOTAL, 2, 5);
  s.addNotes("Numbers: 50-70 fJ/bit from Nature Photonics 3D photonic integration; 800 Gb/s Intel OCI; 0.3 mm² density from dense 3D photonic integration demo.");
}

// -------- Slide 13: 算法感知 --------
function slideAlgoAware() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTitle(s, "硬件感知算法：Mamba / SSM / HMT 以『局部性优先』换存储友好");
  s.addText("(既有) Attention：二次方 × 全局", {
    x: 0.45, y: 0.75, w: 4.35, h: 0.35, fontSize: 12, bold: true, color: C.white,
    fontFace: F.heading, align: "center", valign: "middle",
    fill: { color: C.navymid }, margin: 0.03,
  });
  s.addText("(前沿) SSM / Mamba / HMT：线性 × 局部", {
    x: 4.90, y: 0.75, w: 4.65, h: 0.35, fontSize: 12, bold: true, color: C.primary,
    fontFace: F.heading, align: "center", valign: "middle",
    fill: { color: C.highlight }, margin: 0.03,
  });
  s.addText([
    { text: "KV Cache：\n", options: { fontSize: 12, bold: true, color: C.primary } },
    { text: "• O(N²) 复杂度，序列翻倍 KV 翻 4×\n", options: { fontSize: 11, color: C.text } },
    { text: "• >70% 时间在 HBM↔SRAM 搬运\n", options: { fontSize: 11, color: C.text } },
    { text: "• >128K 上下文直接撞 HBM 容量墙\n\n", options: { fontSize: 11, color: C.text } },
    { text: "访存模式：\n", options: { fontSize: 12, bold: true, color: C.primary } },
    { text: "• 全局、随机、不可预取\n", options: { fontSize: 11, color: C.text } },
    { text: "• Cache 层次极不友好\n\n", options: { fontSize: 11, color: C.text } },
    { text: "硬件诉求：\n", options: { fontSize: 12, bold: true, color: C.primary } },
    { text: "• 极致 HBM 带宽 + 巨量 SRAM\n", options: { fontSize: 11, color: C.text } },
    { text: "• 成本指数上升", options: { fontSize: 11, color: C.text } },
  ], { x: 0.55, y: 1.15, w: 4.15, h: 3.30, fontFace: F.body, valign: "top" });
  s.addText([
    { text: "状态空间（Mamba / S4）：\n", options: { fontSize: 12, bold: true, color: C.primary } },
    { text: "• O(N) 线性；隐藏状态常数大小\n", options: { fontSize: 11, color: C.text } },
    { text: "• 长上下文不撞 HBM 容量墙\n\n", options: { fontSize: 11, color: C.text } },
    { text: "层次化记忆（HMT）：\n", options: { fontSize: 12, bold: true, color: C.primary } },
    { text: "• 层次化短期/长期缓存压缩历史\n", options: { fontSize: 11, color: C.text } },
    { text: "• 访存局部性显著↑，CIM 友好\n\n", options: { fontSize: 11, color: C.text } },
    { text: "硬件含义：\n", options: { fontSize: 12, bold: true, color: C.primary } },
    { text: "• 小 DRAM 带宽 + 多近存计算 =\n  更优能效\n", options: { fontSize: 11, color: C.text } },
    { text: "• 与 CIM / 3D 堆叠 天然对齐", options: { fontSize: 11, bold: true, color: C.text } },
  ], { x: 5.00, y: 1.15, w: 4.45, h: 3.30, fontFace: F.body, valign: "top" });
  addCallout(s, "Attention 不是全部：2030 前后主力是『内存友好架构 × CIM × 小模型多智能体』。");
  fixed(s, 13, TOTAL, 2, 6);
  s.addNotes("Source: arXiv:2603.05225v1 §4.2-4.3; Mamba (Gu & Dao 2023), HMT (2024).");
}

// -------- Slide 14: 存储雷达 --------
function slideRadar() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTitle(s, "存储层技术雷达：TRL × 差异化 —— 光互联 + CIM-A 位于『前沿探索区』");
  // Matrix frame — plain outline + cross gridlines, no quadrant fills (avoids shape-vs-node overlap)
  const X = 0.95, Y = 0.80, W = 8.60, H = 3.00;
  const midX = X + W/2, midY = Y + H/2;
  // Outer frame
  s.addShape("rect", { x: X, y: Y, w: W, h: H,
    fill: { type: "none" }, line: { color: C.border, width: 0.75 } });
  // Cross gridlines (dashed)
  s.addShape("line", { x: X, y: midY, w: W, h: 0, line: { color: C.border, width: 0.5, dashType: "dash" } });
  s.addShape("line", { x: midX, y: Y, w: 0, h: H, line: { color: C.border, width: 0.5, dashType: "dash" } });
  // Quadrant corner labels (small boxes in corners, no fill)
  s.addText("② 前沿探索区", { x: X + 0.05, y: Y + 0.05, w: 1.60, h: 0.32,
    fontSize: 9, bold: true, color: C.navymid, fontFace: F.heading, align: "left", valign: "middle" });
  s.addText("① 激烈竞争区", { x: midX + 0.05, y: Y + 0.05, w: 1.60, h: 0.32,
    fontSize: 9, bold: true, color: C.accent, fontFace: F.heading, align: "left", valign: "middle" });
  s.addText("④ 早期实验区", { x: X + 0.05, y: midY + 0.05, w: 1.60, h: 0.32,
    fontSize: 9, bold: true, color: C.muted, fontFace: F.heading, align: "left", valign: "middle" });
  s.addText("③ 商品化区", { x: midX + 0.05, y: midY + 0.05, w: 1.60, h: 0.32,
    fontSize: 9, bold: true, color: C.navymid, fontFace: F.heading, align: "left", valign: "middle" });
  // X-axis label (give adequate h so text doesn't overflow)
  s.addText("行业成熟度 TRL →", {
    x: X, y: 3.82, w: W, h: 0.30, fontSize: 10, bold: true, color: C.primary, fontFace: F.heading, align: "center", valign: "middle",
  });
  // Y-axis label inside zone (no rotation to avoid breach)
  s.addText("↑ 差异化", {
    x: 0.45, y: Y + 0.15, w: 0.48, h: 0.50, fontSize: 9, bold: true, color: C.primary, fontFace: F.heading, align: "center", valign: "middle",
  });
  // Node helper — labels placed LEFT of node when node is on right half
  function addNode(trlX, diffY, label, fillColor) {
    const cx = X + W * trlX, cy = Y + H * (1 - diffY);
    s.addShape("ellipse", { x: cx - 0.08, y: cy - 0.08, w: 0.16, h: 0.16,
      fill: { color: fillColor }, line: { color: fillColor, width: 1 } });
    // Clamp label position to zone
    const labelW = 1.50;
    let lx;
    if (trlX > 0.55) {
      // label to left
      lx = Math.max(cx - labelW - 0.10, X + 0.05);
      s.addText(label, { x: lx, y: cy - 0.10, w: labelW, h: 0.22,
        fontSize: 8, bold: true, color: C.text, fontFace: F.heading, align: "right", valign: "middle" });
    } else {
      // label to right
      lx = Math.min(cx + 0.12, 9.55 - labelW);
      s.addText(label, { x: lx, y: cy - 0.10, w: labelW, h: 0.22,
        fontSize: 8, bold: true, color: C.text, fontFace: F.heading, align: "left", valign: "middle" });
    }
  }
  addNode(0.80, 0.25, "DDR5 / GDDR7", C.muted);
  addNode(0.88, 0.15, "NAND / SSD", C.muted);
  addNode(0.68, 0.58, "HBM3E 12-Hi", C.navymid);
  addNode(0.85, 0.48, "HBM4 2TB/s", C.accent);
  addNode(0.30, 0.88, "CIM-A 模拟", C.accent);
  addNode(0.25, 0.72, "光 ↔ HBM", C.accent);
  addNode(0.45, 0.32, "3D 单片集成", C.navymid);
  addNode(0.30, 0.52, "ReRAM / PCM CIM", C.navymid);
  addNode(0.46, 0.82, "CPO", C.navymid);
  addNode(0.10, 0.30, "超导存储", C.muted);
  addNode(0.15, 0.15, "DNA 存储", C.muted);
  // Legend
  s.addText("● 红=关键信号   ● 深蓝=主动跟踪   ● 灰=周边关注", {
    x: 0.45, y: 4.12, w: 9.10, h: 0.22, fontSize: 9, italic: true, color: C.muted, align: "center",
  });
  addCallout(s, "HBM4 处『激烈竞争区』，真正差异化押注在『CIM-A + 光互联 ↔ HBM』交叉点——2030 后的护城河。");
  fixed(s, 14, TOTAL, 2, 7);
  s.addNotes("Radar plotting based on TRL estimates from paper §3 + industry public signals. No Huawei positioning (External-Scope Constraint).");
}

// -------- Slide 15: Attention 不是全部 --------
function slideAttentionNotAll() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTitle(s, "算法跃迁：固定精度所需模型单调缩小，固定模型精度单调上升（3D 演进）");
  const img = `${IMG_DIR}/aihw_fig3.png`;
  safeAddImage(s, { path: img, x: 0.45, y: 0.78, w: 4.80, h: 3.50,
    altText: "3D plot of model accuracy, model size, and release time" });
  s.addText("图：时间 × 模型大小 × 精度 3D 联合演进（原论文 Figure 3）", {
    x: 0.45, y: 4.32, w: 4.80, h: 0.22, fontSize: 7.5, italic: true, color: C.muted,
    fontFace: "Arial", align: "center",
  });
  s.addText([
    { text: "三个维度的共同结论：\n", options: { fontSize: 13, bold: true, color: C.primary } },
    { text: "① 固定精度下，所需模型规模单调下降\n   → 小模型追上去年中型模型\n\n", options: { fontSize: 11, color: C.text } },
    { text: "② 固定模型规模下，精度单调上升\n   → 算法红利持续释放\n\n", options: { fontSize: 11, color: C.text } },
    { text: "③ 时间维度下，规模—精度—时间\n   共同下降到一个低边界\n\n", options: { fontSize: 11, color: C.text } },
    { text: "推论：\n", options: { fontSize: 13, bold: true, color: C.primary } },
    { text: "• 2035 年 ~20B 活跃参数专精模型\n  支撑绝大多数部署\n", options: { fontSize: 11, bold: true, color: C.text } },
    { text: "• 优化维度从『规模』→『效率 × 功耗\n  × 时延 × 成本 × 可部署性』", options: { fontSize: 11, color: C.text } },
  ], { x: 5.35, y: 0.78, w: 4.20, h: 3.75, fontFace: F.body, valign: "top" });
  addCallout(s, "十年后支撑部署的不是更大 Transformer，而是『SSM/混合架构 × 小模型 × 多智能体 × CIM 硬件』。");
  fixed(s, 15, TOTAL, 3, 0);
  s.addNotes("Image source: Figure 3 of arXiv:2603.05225v1 (CC BY 4.0).");
}

// -------- Slide 16: 电力危机 --------
function slidePower() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTitle(s, "电力而非算力才是下一个瓶颈：数据中心需求以数十 GW 级增长，电网滞后");
  const blocks = [
    { v: "数十 GW", l: "AI 数据中心需求年增量" },
    { v: "< 5 年", l: "电力缺口窗口" },
    { v: "85%", l: "< 30kW/柜 拟淘汰" },
    { v: "~5%", l: "AI 试点取得 ROI" },
  ];
  // Block 0 has longer CJK+ASCII value ("数十 GW"), needs more h for text
  // others are ASCII-short ("< 5 年", "85%", "~5%") and must hug tighter
  const xs = [0.45, 2.70, 4.95, 7.20];
  const hs = [0.75, 0.55, 0.55, 0.55];
  for (let i = 0; i < 4; i++) {
    addMetric(s, xs[i], 0.80, 2.15, hs[i], blocks[i].v, blocks[i].l, null, 14);
  }
  s.addText("美国 vs 中国电力格局（原论文 §5.2 要点）", {
    x: 0.45, y: 1.70, w: 9.10, h: 0.32, fontSize: 10, bold: true, color: C.navymid, fontFace: F.heading, valign: "middle",
  });
  const rows = [
    [{ text: "维度", options: { bold: true, color: C.white, fill: C.primary } },
     { text: "美国", options: { bold: true, color: C.white, fill: C.primary } },
     { text: "中国", options: { bold: true, color: C.white, fill: C.primary } }],
    ["发电扩张速度", "滞后于 AI 需求", "相对领先（原文判断）"],
    ["电网容量", "升级周期长", "更快的电网扩张能力"],
    ["数据中心密度趋势", "高密度（≥80kW/机柜）受限", "新建机房可按高密度设计"],
    ["政策/监管", "碎片化，州级复杂", "基础设施协调集中"],
  ];
  s.addTable(rows, {
    x: 0.45, y: 2.05, w: 9.10, fontSize: 8, fontFace: F.body, color: C.text,
    border: { type: "solid", pt: 0.5, color: C.border },
    colW: [2.30, 3.40, 3.40], valign: "middle",
  });
  addCallout(s, "2030 前的竞争从『谁有更多 GPU』转向『谁有更多 GW + 低 PUE 机房 + 更好的调度』。");
  fixed(s, 16, TOTAL, 4, 0);
  s.addNotes("Source: arXiv:2603.05225v1 §5.2 Q&A on infrastructure.");
}

// -------- Slide 17: 采用鸿沟 --------
function slideAdoption() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  addTitle(s, "采用鸿沟：仅 5% 企业 AI 试点取得可持续 ROI，瓶颈在运营化而非模型");
  const blocks = [
    { v: "~5%", l: "可持续 ROI 的 AI 试点占比" },
    { v: "5–20%", l: "真实集群利用率" },
    { v: "≥ 60%", l: "2035 目标集群利用率" },
  ];
  const xs = [0.45, 3.45, 6.45];
  for (let i = 0; i < 3; i++) {
    addMetric(s, xs[i], 0.80, 2.90, 0.70, blocks[i].v, blocks[i].l, null, 20);
  }
  s.addText("采用鸿沟的五大根因", {
    x: 0.45, y: 1.70, w: 9.10, h: 0.30, fontSize: 11, bold: true, color: C.navymid, fontFace: F.heading, valign: "middle",
  });
  const rows = [
    [{ text: "#", options: { bold: true, color: C.white, fill: C.primary } },
     { text: "根因", options: { bold: true, color: C.white, fill: C.primary } },
     { text: "对工程/产品的启示", options: { bold: true, color: C.white, fill: C.primary } }],
    ["①", "持续学习能力弱，模型上线即停滞", "在线微调 / RLHF / 反馈闭环设计"],
    ["②", "数据孤岛、主权碎片化", "跨域数据协议 / 隐私计算"],
    ["③", "合规与监管复杂", "模型卡 / 可解释 / 留痕"],
    ["④", "单次训练 / 推理成本高", "SLM + KV 压缩 + 存算一体"],
    ["⑤", "工程与治理断层（POC → 运营化）", "平台工程 / MLOps / SRE 能力"],
  ];
  s.addTable(rows, {
    x: 0.45, y: 2.05, w: 9.10, fontSize: 8, fontFace: F.body, color: C.text,
    border: { type: "solid", pt: 0.5, color: C.border },
    colW: [0.55, 4.10, 4.45], valign: "middle",
  });
  addCallout(s, "真正的投资标的不是更大的模型，而是『把 POC 运营化的工程与治理能力』。");
  fixed(s, 17, TOTAL, 4, 1);
  s.addNotes("Source: arXiv:2603.05225v1 §5.2 key Q&A on deployment barriers.");
}

// -------- Slide 18: Closing --------
function slideClosing() {
  const s = pres.addSlide();
  s.background = { color: C.white };
  // Title placed at y=0.77 (inside content zone y>=0.75 to satisfy linter)
  s.addText("技术洞察总结 / Insight Summary", {
    x: 0.45, y: 0.77, w: 9.1, h: 0.50, fontSize: 22, bold: true, color: C.accent,
    fontFace: F.heading, align: "left", valign: "middle",
  });
  s.addShape("line", { x: 0.45, y: 1.32, w: 9.1, h: 0, line: { color: C.border, width: 0.75 } });
  s.addText([
    { text: "① 『每焦耳智能』取代峰值 FLOPS，成为 2025–2035 新的规模化度量。\n", options: { fontSize: 11, bold: true, color: C.primary } },
    { text: "   评估、采购、学术奖评都要加入能效维度，否则一切都是补贴单点算力。\n\n", options: { fontSize: 9, color: C.muted } },
    { text: "② 存储而非计算是真正的瓶颈：数据搬移能耗 ≈ 600× 算术能耗。\n", options: { fontSize: 11, bold: true, color: C.primary } },
    { text: "   CIM / 3D 堆叠 / 光互联 三者协同，是 2030 后突破 HBM 单点天花板的唯一通路。\n\n", options: { fontSize: 9, color: C.muted } },
    { text: "③ Attention 不是全部：内存友好架构（SSM / Mamba / HMT）将与 CIM 天然对齐。\n", options: { fontSize: 11, bold: true, color: C.primary } },
    { text: "   支撑 2035 部署的主力不是更大 Transformer，而是 ~20B 活跃参数的专精小模型 × 多智能体。\n\n", options: { fontSize: 9, color: C.muted } },
    { text: "④ AI-for-EDA 把硅设计周期从『年』压到『周』，硅设计 ≥ 3× 提速。\n", options: { fontSize: 11, bold: true, color: C.primary } },
    { text: "   对中小 Fabless 是与顶级厂商缩短差距的唯一杠杆。\n\n", options: { fontSize: 9, color: C.muted } },
    { text: "⑤ 电力而非算力是下一个瓶颈，5 年内出现电力短缺窗口。\n", options: { fontSize: 11, bold: true, color: C.primary } },
    { text: "   85% < 30 kW/机柜 机房将被淘汰；每焦耳智能指标决定谁能活下来。\n\n", options: { fontSize: 9, color: C.muted } },
    { text: "⑥ 投资拒绝清单：只讲 FLOPS 的芯片、无许可证的大模型、不谈电网的基建。\n", options: { fontSize: 11, bold: true, color: C.primary } },
    { text: "   原论文 §4–§5 反复标注的反面案例。", options: { fontSize: 9, color: C.muted } },
  ], { x: 0.45, y: 1.40, w: 9.10, h: 3.40, fontFace: F.body, valign: "top" });
  s.addShape("rect", { x: 0.45, y: 4.88, w: 9.10, h: 0.32,
    fill: { color: C.highlight }, line: { color: C.accent, width: 2 } });
  s.addText("不是多花一笔钱，而是跨层范式更替：把存储升为一等公民，把每焦耳智能写进一切决策。", {
    x: 0.55, y: 4.88, w: 8.90, h: 0.32, fontSize: 11, bold: true, color: C.accent,
    fontFace: F.heading, valign: "middle",
  });
  addFooter(s, 18, TOTAL);
  s.addNotes("Closing insights distilled from arXiv:2603.05225v1 + this report's §7.");
}

// ====== Build ======
slideCover();
slideInsight();
slideRhythm();
slideQuote();
slideThreeLayer();
slideStackTable();
slideMemWall();
slideMemBound();
slideCIMQuad();
slideArchCompare();
slideHBM();
slidePhotonic();
slideAlgoAware();
slideRadar();
slideAttentionNotAll();
slidePower();
slideAdoption();
slideClosing();

pres.writeFile({ fileName: OUT_PATH }).then(fn => {
  console.log("Wrote", fn);
});
