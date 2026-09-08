// segment-search.js — 逐段筆記的全文比對與命中標示。
// 與課程搜尋共用名詞展開；不依賴 DOM，可直接用 node 驗證。
import { expandTerms } from "./search-index.js";

let searchGlossary = [];
export function setSearchGlossary(glossary) {
  searchGlossary = Array.isArray(glossary) ? glossary : [];
}

/** 保留原查詢的字串契約；展開僅用於比對與標示。 */
export function queryTerms(query) {
  return [...new Set(expandTerms(normalizeQuery(query), searchGlossary)
    .map(normalizeQuery).filter(Boolean))];
}

const HTML = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };

/** 與 render.js 的 esc 同語意，不需要載入任何 DOM 渲染模組。 */
export function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (c) => HTML[c]);
}

/** 把一段逐段筆記攤平成可搜尋的字串：標題、速讀摘要、完整詳解都要能被搜到。 */
export function segmentHaystack(segment) {
  if (!segment) return "";
  const detail = Array.isArray(segment.detail) ? segment.detail.join(" ") : "";
  return `${segment.title || ""} ${segment.summary || ""} ${detail}`.trim();
}

/** 查詢字串正規化：去頭尾空白、轉小寫。空查詢代表「不過濾」。 */
export function normalizeQuery(query) {
  return String(query ?? "").trim().toLowerCase();
}

/** 這一段筆記是否命中查詢。空查詢一律不算命中（避免整頁都被標亮）。 */
export function segmentMatches(segment, query) {
  const terms = queryTerms(query);
  if (!terms.length) return false;
  const haystack = segmentHaystack(segment).toLowerCase();
  return terms.some(term => haystack.includes(term));
}

/** 一支影片有幾段筆記命中——播放清單用它顯示「筆記 N 段」。 */
export function segmentHitCount(segments, query) {
  const q = normalizeQuery(query);
  if (!q || !Array.isArray(segments)) return 0;
  return segments.filter((s) => segmentMatches(s, q)).length;
}

/**
 * 把命中的字包成 <mark>。
 * 先在原文上找位置、再逐段 escape，避免在已 escape 的字串上比對造成錯位或注入。
 */
export function highlight(text, query) {
  const raw = String(text ?? "");
  const terms = queryTerms(query);
  if (!terms.length) return escapeHtml(raw);

  const lower = raw.toLowerCase();
  let out = "";
  let from = 0;
  for (;;) {
    // 同義詞可能重疊：每次選最左、同位置最長的一筆，避免巢狀標記。
    let at = -1;
    let length = 0;
    for (const term of terms) {
      const next = lower.indexOf(term, from);
      if (next >= 0 && (at < 0 || next < at || (next === at && term.length > length))) {
        at = next;
        length = term.length;
      }
    }
    if (at < 0) break;
    out += escapeHtml(raw.slice(from, at));
    out += `<mark class="Hit">${escapeHtml(raw.slice(at, at + length))}</mark>`;
    from = at + length;
  }
  return out + escapeHtml(raw.slice(from));
}
