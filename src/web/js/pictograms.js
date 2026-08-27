// pictograms.js — 聲窗線稿：膝輪廓＋探頭/束向/切面的極簡線稿（燈箱圖譜 M 級）
// 慣例：一律右膝。前視圖＝面對病人，內側在畫面右（以實心小點標記內側）。
// 探頭為圓角短棒，notch 端以小圓點標示（縱切 notch 朝近端、橫切朝內側）。
// ⚠️ 解剖定向需醫師審核（reviewed_by 記在 course.config.json 的 pictograms 註記）。
// 線寬統一 1.5、stroke=currentColor；active 狀態由使用端套 --mark-teach。

const S = (id, inner) =>
  `<symbol id="p-${id}" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">${inner}</symbol>`;

// --- 基底：前視右膝（股骨幹/髁弧/平台弧/脛骨幹；內側=右，標實心點） ---
const KNEE_FRONT = `
  <path d="M24 5 V16" />
  <path d="M16.5 22 Q24 14.5 31.5 22" />
  <path d="M16.5 27.5 Q24 33.5 31.5 27.5" />
  <path d="M24 33 V43" />
  <circle cx="35" cy="24.5" r="1.4" fill="currentColor" stroke="none" />`;

// --- 基底：側視右膝（伸直；股骨軸/髁圓/髕骨/脛骨軸；前=左） ---
const KNEE_SIDE = `
  <path d="M30 6 L27 18" />
  <path d="M22 25 a6.5 6.5 0 0 1 10 -4" />
  <circle cx="16.5" cy="21" r="3" />
  <path d="M25 31 L27 43" />`;

// --- 基底：側視右膝（屈曲約45°） ---
const KNEE_FLEX = `
  <path d="M33 7 L28 19" />
  <path d="M20 26 a7 7 0 0 1 11 -5" />
  <circle cx="14.5" cy="19.5" r="3" />
  <path d="M22 31 L34 40" />`;

// --- 基底：後視右膝（膕窩；內側=左（後視鏡像），標實心點） ---
const KNEE_POST = `
  <path d="M24 5 V16" />
  <path d="M16.5 22 Q24 15.5 31.5 22" />
  <path d="M16.5 27.5 Q24 32.5 31.5 27.5" />
  <path d="M24 33 V43" />
  <circle cx="13" cy="24.5" r="1.4" fill="currentColor" stroke="none" />`;

// 探頭：縱向（長軸沿肢體軸）/ 橫向；notch 以小點
const probeV = (x, y) => `
  <rect x="${x - 2}" y="${y}" width="4" height="12" rx="1.6" />
  <circle cx="${x}" cy="${y + 1.8}" r="0.9" fill="currentColor" stroke="none" />`;
const probeH = (x, y) => `
  <rect x="${x}" y="${y - 2}" width="12" height="4" rx="1.6" />
  <circle cx="${x + 10.2}" cy="${y}" r="0.9" fill="currentColor" stroke="none" />`;

const SYMBOLS = [
  // ── 超音波五聲窗 ──
  S('us-ant-long',  KNEE_SIDE + probeV(11, 8) +
    `<path d="M11 20 L11 24" stroke-dasharray="1.5 2.5" />`),          // 前側縱切：髕上→髕腱，探頭沿肢體軸（側視前緣）
  S('us-ant-trans', KNEE_FLEX + probeH(6, 12) +
    `<path d="M12 14 L15 17" stroke-dasharray="1.5 2.5" />`),          // 前側橫切（屈膝滑車）：探頭橫放於髕上
  S('us-med-long',  KNEE_FRONT + probeV(38, 18)),                      // 內側縱切（MCL/關節線）：內側=右
  S('us-lat-long',  KNEE_FRONT + probeV(10, 18)), // 外側縱切（LCL/腓骨頭）：外側=左
  S('us-post-trans', KNEE_POST + probeH(18, 24.5)), // 後側橫切（膕窩中央）
  // ── X 光四照射位 ──
  S('xr-ap-wb',     KNEE_FRONT + `
    <path d="M4 24.5 H12 M12 24.5 l-2.5 -2 M12 24.5 l-2.5 2" />
    <path d="M40 18 V31" />
    <path d="M14 45 H34" />`),                                          // 站立 AP：前→後束＋接收板＋地面線
  S('xr-lateral',   KNEE_SIDE + `
    <path d="M43 24 H36 M36 24 l2.5 -2 M36 24 l2.5 2" />
    <path d="M6 16 V30" />`),                                           // 側位：側向束＋接收板
  S('xr-skyline',   KNEE_FLEX + `
    <path d="M14.5 5 V12 M14.5 12 l-2 -2.5 M14.5 12 l2 -2.5" />`),      // Skyline/Merchant：屈膝、束由上往下過髕股
  S('xr-rosenberg', KNEE_FLEX + `
    <path d="M40 16 L30 20 M30 20 l3 -2.6 M30 20 l3.6 1.4" />
    <path d="M12 24 V34" />`),                                          // Rosenberg：PA 屈膝45°、束下傾10°
  // ── MRI 三切面 ──
  S('mri-sag',      KNEE_SIDE + `
    <path d="M24 4 V44" stroke-dasharray="3 3" />`),                    // 矢狀面：側視＋垂直切面線
  S('mri-cor',      KNEE_FRONT + `
    <path d="M8 10 L8 38 M8 10 L14 6 M8 38 L14 34 M14 6 V34" stroke-dasharray="3 3" />`), // 冠狀面：前視＋縱向平面
  S('mri-ax',       KNEE_FRONT + `
    <path d="M10 24.5 H38" stroke-dasharray="3 3" />
    <ellipse cx="24" cy="24.5" rx="14" ry="4" stroke-dasharray="3 3" />`), // 軸位：橫切平面環
];

export function mountPictograms() {
  const host = document.createElement('div');
  host.style.display = 'none';
  host.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg">${SYMBOLS.join('')}</svg>`;
  document.body.prepend(host);
}

/** 章節代碼 → 預設線稿（config 的 chapters[].pictogram 可覆寫） */
export const CHAPTER_PICTOGRAM = {
  XR1: 'xr-ap-wb', XR2: 'xr-rosenberg',
  US2: 'us-ant-long', US3: 'us-med-long', US4: 'us-lat-long', US5: 'us-post-trans',
  MR1: 'mri-sag', MR2: 'mri-cor',
};
