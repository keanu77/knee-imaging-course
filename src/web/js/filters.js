// filters.js — 搜尋、動作類型、肌群篩選
import { icon } from "./icons.js";
import { esc, UI } from "./render.js";

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];

/* --- 肌群面板 ------------------------------------------------------------ */

export function renderMusclePanel(course) {
  const list = course.facets || [];
  if (!list.length) {
    $("#musclePanel")?.remove();
    return;
  }

  const byGroup = new Map();
  for (const m of list) {
    if (!byGroup.has(m.group)) byGroup.set(m.group, []);
    byGroup.get(m.group).push(m);
  }

  $("#muscleCount").textContent = list.length;
  $("#muscleBody").innerHTML =
    [...byGroup]
      .map(
        ([group, ms]) => `
        <div class="MuscleGroup__title">${esc(group)}</div>
        <div class="MuscleChips">
          ${ms
            .map(
              (m) => `
            <button class="MuscleChip" type="button" data-muscle="${esc(m.name)}">
              ${esc(m.name)}<span class="MuscleChip__n">${m.count}</span>
            </button>`,
            )
            .join("")}
        </div>`,
      )
      .join("") +
    `<button class="btn MusclePanel__clear" id="muscleClear" type="button">
       ${icon("rotate-ccw", 12)} ${esc(UI.facetClear || "")}
     </button>`;
}

/** 同步所有肌群按鈕（側欄 chip + 動作內的標籤）的選取狀態 */
export function syncMuscleChips(selected) {
  $$("[data-muscle]").forEach((el) => {
    const active = selected.has(el.dataset.muscle);
    el.classList.toggle("is-active", active);
    el.setAttribute("aria-pressed", String(active));
  });
  const panel = $("#musclePanel");
  if (panel && selected.size) { panel.classList.add("is-open"); document.querySelector("#muscleToggle")?.setAttribute("aria-expanded", "true"); }
}

/* --- 主篩選 -------------------------------------------------------------- */

/**
 * 依 state 顯示／隱藏章節、單元與動作。
 * state: { query, searchTerms, filter, learningTier, muscles:Set }
 */
export function applyFilters(state, course) {
  const q = state.query.trim().toLowerCase();
  const searchTerms = state.searchTerms?.length ? state.searchTerms : q ? [q] : [];
  const sel = state.muscles;
  const hits = state.searchHits || [];
  const matchingUnits = new Set(hits.map(hit => hit.unitId));
  let visibleUnits = 0;
  let visibleDrills = 0;

  $$(".Chapter").forEach((chEl) => {
    let chapterHasMatch = false;

    $$(".Unit", chEl).forEach((unitEl) => {
      const unitMuscles = (unitEl.dataset.facets || "").split("|").filter(Boolean);
      const muscleOk = !sel.size || unitMuscles.some((m) => sel.has(m));
      const textOk = !searchTerms.length || matchingUnits.has(unitEl.dataset.unit);
      const match = muscleOk && textOk;

      unitEl.hidden = !match;
      if (!match) return;

      let unitVisibleDrills = 0;

      // 動作層級：類型 + 肌群兩個維度
      $$(".Drill", unitEl).forEach((d) => {
        const kindOk = state.filter === "all" || d.dataset.kind === state.filter;
        const tierOk =
          state.learningTier === "all" || d.dataset.learningTier === state.learningTier;
        const dm = (d.dataset.facets || "").split("|").filter(Boolean);
        const mOk = !sel.size || dm.some((m) => sel.has(m));
        d.hidden = !(kindOk && tierOk && mOk);
        if (kindOk && tierOk && mOk) { visibleDrills++; unitVisibleDrills++; }
      });

      if (!unitVisibleDrills && (state.filter !== "all" || state.learningTier !== "all")) {
        unitEl.hidden = true;
        return;
      }
      chapterHasMatch = true;
      visibleUnits++;
      // 整組動作都被篩掉就把標題也收起來
      $$(".DrillGroup", unitEl).forEach((g) => {
        const anyVisible = $$(".Drill", g).some((d) => !d.hidden);
        g.hidden = !anyVisible;
      });
    });

    chEl.hidden = !chapterHasMatch;
    if ((q || sel.size) && chapterHasMatch) chEl.classList.add("is-open");
  });

  const totalDrills = course.meta.drill_units;
  const parts = [];
  if (q) parts.push(`「${state.query.trim()}」`);
  if (sel.size) parts.push(`${UI.facetPrefix || ""}：${[...sel].join("、")}`);
  if (state.learningTier === "core") parts.push(UI.coreCountLabel || "核心必看");

  $("#filterCount").setAttribute("role", "status");
  $("#filterCount").textContent = parts.length
    ? `${visibleUnits} 個相關單元 · ${visibleDrills} 個影片項目${q ? "；精確命中見上方搜尋結果" : ` · ${parts.join(" + ")}`}`
    : `顯示 ${visibleDrills} / ${totalDrills} 個影片項目`;

  toggleBlankslate(visibleUnits);
  return { visibleUnits, visibleDrills };
}

function toggleBlankslate(visibleUnits) {
  const host = $("#chapters");
  const existing = $("#filterBlank");
  if (visibleUnits === 0 && !existing) {
    host.insertAdjacentHTML(
      "beforeend",
      `<div class="Blankslate" id="filterBlank">
         ${icon("inbox", 32)}
         <p class="Blankslate__heading">${esc(UI.emptyTitle || "")}</p>
         <p>${esc(UI.emptyHint || "")}</p>
         <button class="btn" type="button" data-clear-filters>清除篩選，查看全部課程</button>
       </div>`,
    );
  } else if (visibleUnits > 0 && existing) {
    existing.remove();
  }
}
