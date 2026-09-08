// player.js — 上課模式：把整門課攤平成播放清單，左側嵌入播放
import { icon } from "./icons.js";
import { parseClock, playbackPolicy, allowedPosition, rangeAt, isTrustedPlayerMessage } from "./playback-policy.js";
export { parseClock } from "./playback-policy.js";
import { esc, interventionNoticeText, KIND, TIER, UI } from "./render.js";
import { button as discussButton, panel as discussPanel } from "./discuss.js";
import { highlight, queryTerms, segmentHaystack, segmentHitCount, segmentMatches } from "./segment-search.js";

const $ = (s, r = document) => r.querySelector(s);

const EMBED = "https://www.youtube-nocookie.com/embed/";
let LANG = {};
export function setLanguages(m) { LANG = m || {}; }

/** 把 course.json 攤平成一維播放清單 */
export function buildPlaylist(course) {
  const items = [];
  for (const ch of course.chapters) {
    for (const u of ch.units) {
      const base = {
        chCode: ch.code,
        chTitle: ch.title,
        unitId: u.id,
        unitName: u.name,
      };
      for (const les of u.lessons || (u.lesson ? [u.lesson] : [])) {
        if (!les?.url) continue;
        items.push({
          ...base,
          kind: "lesson",
          learning_tier: les.learning_tier || "core",
          lang: les.lang,
          name: les.title,
          title: les.title,
          channel: les.channel,
          duration: les.duration,
          views: les.views,
          url: les.url,
          why: les.why,
          assessment: u.assessment,
          contains_intervention: les.contains_intervention,
          intervention_start_timestamp: les.intervention_start_timestamp,
          diagnostic_segment_range: les.diagnostic_segment_range,
          segments: les.segments,
        });
      }
      for (const d of u.drills || []) {
        if (!d.url) continue;
        items.push({
          ...base,
          kind: d.kind,
          learning_tier: d.learning_tier,
          name: d.name,
          en: d.en,
          title: d.title,
          channel: d.channel,
          duration: d.duration,
          views: d.views,
          url: d.url,
          target: d.target,
          dose: d.dose,
          facets: d.facets,
          cat: d.cat,
          why: d.why,
          assessment: u.assessment,
          original_content_date: d.original_content_date,
          upload_date: d.upload_date,
          date_note: d.date_note,
          presenter: d.presenter,
          presenter_note: d.presenter_note,
          scope_note: d.scope_note,
          disclosure: d.disclosure,
          contains_intervention: d.contains_intervention,
          intervention_start_timestamp: d.intervention_start_timestamp,
          diagnostic_segment_range: d.diagnostic_segment_range,
          segments: d.segments,
        });
      }
    }
  }
  return items.map((it, i) => ({ ...it, i, vid: videoId(it.url) }));
}

function videoId(url) {
  const m = /(?:v=|youtu\.be\/)([\w-]{11})/.exec(url || "");
  return m ? m[1] : null;
}

function dur(s) {
  return s || "";
}

/* --- 逐段筆記與跳播 ------------------------------------------------------- */

const EMBED_ORIGIN = "https://www.youtube-nocookie.com";
let frameReady = false;
let currentItem = null;
let currentPosition = 0;
let currentRange = null;
let readyTimer = null;
let listeningTimer = null;
let lastSaved = -1;
let telemetryInRange = false;
let reportedPlayerState = -1;
const POSITION_PREFIX = "knee-imaging:video-position:";
const positionKey = item => POSITION_PREFIX + (item.unitId ? `${item.unitId}:` : "") + item.vid;

export function getPosition(item = currentItem) {
  if (!item?.vid) return null;
  if (currentItem?.vid === item.vid && currentItem?.unitId === item.unitId) return currentPosition;
  try {
    const raw = localStorage.getItem(positionKey(item)) ?? localStorage.getItem(POSITION_PREFIX + item.vid);
    if (raw === null) return null;
    const n = Number(raw);
    return Number.isFinite(n) && n >= 0 ? n : null;
  } catch { return null; }
}

function savePosition(force = false) {
  if (!currentItem?.vid || (!force && Math.abs(currentPosition - lastSaved) < 5)) return;
  try {
    localStorage.setItem(positionKey(currentItem), String(Math.floor(currentPosition)));
    lastSaved = currentPosition;
  } catch { /* Private mode or full storage must not prevent learning. */ }
}

function status(text) {
  const el = $("#playerStatus");
  if (el) el.textContent = text;
}

function post(command, args = []) {
  const frame = $("#ytFrame");
  if (!frame?.contentWindow) return false;
  frame.contentWindow.postMessage(
    JSON.stringify({ event: "command", func: command, args }), EMBED_ORIGIN);
  return true;
}

/** Every site-owned seek uses the same diagnostic boundaries. */
export function seekTo(seconds, { autoplay = true } = {}) {
  if (!currentItem?.vid) return false;
  const policy = playbackPolicy(currentItem);
  const target = allowedPosition(policy, seconds);
  if (target === null) return false;
  const range = rangeAt(policy, target);
  const sameRange = range?.start === currentRange?.start;
  currentPosition = target;
  savePosition(true);
  if (frameReady && sameRange && post("seekTo", [target, true])) {
    post(autoplay ? "playVideo" : "pauseVideo");
  } else {
    // A new diagnostic range needs its own end parameter as well as its start.
    currentRange = range;
    $("#playerFrame").innerHTML = frameHtml(currentItem, target, autoplay);
    listenToFrame();
  }
  return true;
}

function clearFrameTimers() {
  clearTimeout(readyTimer);
  clearInterval(listeningTimer);
}

function listenToFrame() {
  clearFrameTimers();
  frameReady = false;
  telemetryInRange = false;
  reportedPlayerState = -1;
  const frame = $("#ytFrame");
  if (!frame) return;
  status("正在載入影片…若無法播放，可使用下方原始來源連結。");
  const subscribe = () => {
    if (frame !== $("#ytFrame")) return;
    frame.contentWindow?.postMessage(JSON.stringify({ event: "listening", id: "ytFrame", channel: "widget" }), EMBED_ORIGIN);
  };
  frame.addEventListener("load", subscribe);
  frame.addEventListener("error", () => status("影片載入失敗，請使用原始來源連結。"));
  listeningTimer = setInterval(subscribe, 750);
  readyTimer = setTimeout(() => {
    clearInterval(listeningTimer);
    if (!frameReady) status("播放器尚未回應。請確認網路或使用原始來源連結；原站可能包含本課範圍以外的內容。");
  }, 12000);
}

addEventListener("message", (event) => {
  if (!isTrustedPlayerMessage(event, $("#ytFrame")?.contentWindow)) return;
  let data;
  try { data = typeof event.data === "string" ? JSON.parse(event.data) : event.data; } catch { return; }
  if (!data || !["onReady", "infoDelivery", "initialDelivery", "onError"].includes(data.event)) return;
  if (data.event === "onError") {
    clearFrameTimers();
    status("這支影片目前無法嵌入或播放，請使用原始來源連結。");
    return;
  }
  if (!frameReady) {
    frameReady = true;
    clearFrameTimers();
    post("addEventListener", ["onError"]);
    status("播放器已就緒。學習位置會儲存在這個瀏覽器。");
  }
  if (typeof data.info?.playerState === "number") reportedPlayerState = data.info.playerState;
  const time = data.info?.currentTime;
  if (typeof time !== "number" || !Number.isFinite(time) || time < 0 || !currentItem) return;
  if (currentRange && (time < currentRange.start || time >= currentRange.end)) {
    // Startup telemetry can report 0 before the requested start has been cued.
    // Enforce immediately once playing, or once an in-range time was observed.
    if (!telemetryInRange && reportedPlayerState !== 1) return;
    // Cross-origin native controls are not isolatable. On trustworthy telemetry,
    // pause and return to the selected range; never claim this is a sandbox.
    post("pauseVideo");
    post("seekTo", [currentRange.start, true]);
    currentPosition = currentRange.start;
    savePosition(true);
    status("已到達或離開本段診斷範圍，影片已暫停。可按下方時間碼選擇其他診斷段落。");
    return;
  }
  telemetryInRange = true;
  currentPosition = time;
  savePosition();
});
addEventListener("pagehide", () => savePosition(true));

function frameHtml(item, startSeconds, autoplay) {
  const policy = playbackPolicy(item);
  const target = allowedPosition(policy, startSeconds ?? 0);
  if (target === null) return `<p role="alert">診斷時間範圍資料不完整，暫不載入播放器。</p>`;
  const range = rangeAt(policy, target);
  const params = new URLSearchParams({ rel: "0", autoplay: autoplay ? "1" : "0", enablejsapi: "1", start: String(Math.floor(target)), origin: location.origin });
  if (range) params.set("end", String(range.end));
  return `<iframe id="ytFrame" src="${EMBED}${esc(item.vid)}?${esc(params.toString())}"
            title="${esc(item.title || item.name)}"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            referrerpolicy="strict-origin-when-cross-origin"
            allowfullscreen></iframe>`;
}

export function resume(item, options = {}) {
  return play(item, { ...options, autoplay: false, startSeconds: getPosition(item) });
}

/** 逐段筆記軌。course.json 只會帶入已簽核的段落，未簽核的在建置階段就被擋掉。 */
function segmentRail(item, query = "") {
  const segments = (item.segments || [])
    .map((s) => ({ ...s, seconds: parseClock(s.start) }))
    .filter((s) => s.seconds !== null && allowedPosition(playbackPolicy(item), s.seconds) === s.seconds);
  if (!segments.length) return "";

  const hits = segmentHitCount(segments, query);
  const rows = segments.map((s) => {
    const hit = segmentMatches(s, query);
    return `
      <li class="Segment${hit ? " is-hit" : ""}">
        <button class="Segment__jump" type="button" data-seek="${s.seconds}"
                title="從 ${esc(s.start)} 開始播放">
          ${icon("play", 11)}<span>${esc(s.start)}–${esc(s.end)}</span>
        </button>
        <div class="Segment__body">
          <h4 class="Segment__title">${highlight(s.title, query)}</h4>
          <p class="Segment__summary">${highlight(s.summary, query)}</p>
          ${(s.detail || []).length
            ? `<details class="Segment__detail"${hit ? " open" : ""}>
                 <summary>完整逐段詳解 · ${(s.detail || []).length} 項</summary>
                 <ul>${(s.detail || []).map((d) => `<li>${highlight(d, query)}</li>`).join("")}</ul>
               </details>`
            : ""}
        </div>
      </li>`;
  }).join("");

  const framed = item.contains_intervention === true ? "；段落已框限在診斷範圍內" : "";
  // 命中時預設只顯示命中段落：搜尋的人要的是那一段，不是重新捲 60 段
  const hitBar = hits
    ? `<label class="Segments__only">
         <input type="checkbox" id="segmentOnlyHits" checked />
         只看命中的 ${hits} 段
       </label>`
    : "";
  return `
    <section class="Segments${hits ? " has-hits is-onlyHits" : ""}" aria-label="逐段筆記">
      <div class="Segments__head">
        <strong>逐段筆記</strong>
        <span>${segments.length} 段 · 點時間碼直接跳播${framed}</span>
        ${hits ? `<span class="Segments__hits">${icon("search", 11)} ${hits} 段命中「${esc(query.trim())}」</span>` : ""}
        ${hitBar}
      </div>
      <ol class="Segments__list">${rows}</ol>
    </section>`;
}

/** 播放清單的顯示、上一部／下一部共用同一套條件，避免操作到畫面上已隱藏的影片。 */
export function playlistItemMatches(it, { doneSet, query, onlyTodo, learningTier }) {
  if (onlyTodo && doneSet.has(it.unitId)) return false;
  if (learningTier && learningTier !== "all" && it.learning_tier !== learningTier) return false;

  const terms = queryTerms(query);
  if (!terms.length) return true;

  const tierLabel = TIER[it.learning_tier]?.label || it.learning_tier || "";
  // 逐段筆記也要能被搜到：學員記得的往往是段落裡的字，不是影片標題
  const segmentText = (it.segments || []).map(segmentHaystack).join(" ");
  const hay = `${it.name} ${it.title || ""} ${it.channel || ""} ${it.unitName} ${it.chTitle} ${(it.facets || []).join(" ")} ${it.target || ""} ${tierLabel} ${it.presenter || ""} ${it.presenter_note || ""} ${it.scope_note || ""} ${it.disclosure || ""} ${it.diagnostic_segment_range || ""} ${it.original_content_date || ""} ${it.upload_date || ""} ${segmentText}`;
  const normalized = hay.toLowerCase();
  return terms.some(term => normalized.includes(term));
}

/* --- 播放清單渲染 -------------------------------------------------------- */

export function renderPlaylist(items, { doneSet, currentIndex, query, onlyTodo, learningTier }) {
  let lastCh = null;
  let lastUnit = null;
  let shown = 0;
  const html = [];

  for (const it of items) {
    if (!playlistItemMatches(it, { doneSet, query, onlyTodo, learningTier })) continue;

    if (it.chCode !== lastCh) {
      html.push(`<div class="PlaylistChapter">${esc(it.chCode)} ${esc(it.chTitle)}</div>`);
      lastCh = it.chCode;
      lastUnit = null;
    }
    if (it.unitId !== lastUnit) {
      html.push(`<div class="PlaylistUnit">${esc(it.unitName)}</div>`);
      lastUnit = it.unitId;
    }

    const k = it.kind === "lesson" ? null : KIND[it.kind];
    const tier = TIER[it.learning_tier];
    html.push(`
      <button class="PlaylistItem${it.i === currentIndex ? " is-playing" : ""}${doneSet.has(it.unitId) ? " is-done" : ""}"
              type="button" data-play="${it.i}"${it.i === currentIndex ? ' aria-current="true"' : ""}>
        <span class="PlaylistItem__dot" style="background:var(--fgColor-${esc(it.kind === "lesson" ? "accent" : (KIND[it.kind] || {}).tone || "accent")})"></span>
        <span class="PlaylistItem__main">
          <span class="PlaylistItem__name">${esc(it.kind === "lesson" ? `${UI.lessonLabel || ""} · ${it.name}` : it.name)}</span>
          <span class="PlaylistItem__meta">${tier ? esc(tier.label) + " · " : ""}${k ? esc(k.label) + " · " : ""}${it.lang ? esc(LANG[it.lang] || it.lang) + " · " : ""}${esc(it.channel || "")}</span>
          ${segmentHitCount(it.segments, query) ? `<span class="PlaylistItem__hit">${icon("search", 10)} 筆記 ${segmentHitCount(it.segments, query)} 段命中</span>` : ""}
        </span>
        <span class="PlaylistItem__dur">${esc(dur(it.duration))}</span>
      </button>`);
    shown++;
  }

  $("#playlist").innerHTML =
    html.join("") ||
    `<div class="Blankslate">${icon("inbox", 28)}<p class="Blankslate__heading">沒有符合的影片</p><button class="btn" type="button" data-reset-playlist>清除播放清單篩選</button></div>`;
  $("#playlistCount").textContent =
    shown === items.length ? `${new Set(items.map(item => item.vid)).size} 支影片 · ${items.length} 個項目` : `${shown} / ${items.length} 個項目`;
  return shown;
}

/* --- 播放 ---------------------------------------------------------------- */

export function play(item, { total, query = "", autoplay = true, startSeconds = null } = {}) {
  if (!item?.vid) return;

  const saved = startSeconds ?? getPosition(item);
  savePosition(true);
  currentItem = item;
  const policy = playbackPolicy(item);
  currentPosition = allowedPosition(policy, saved ?? 0) ?? 0;
  currentRange = rangeAt(policy, currentPosition);
  lastSaved = -1;
  $("#playerFrame").innerHTML = frameHtml(item, currentPosition, autoplay);

  const k = item.kind === "lesson" ? null : KIND[item.kind];
  const badge = k
    ? `<span class="Label Label--${esc(k.tone || "neutral")}">${esc(k.label)}</span>`
    : `<span class="Label Label--accent">${esc(UI.lessonLabel || "")}</span>`;
  const tier = TIER[item.learning_tier];
  const tierBadge = tier
    ? `<span class="Label Label--${esc(tier.tone || "neutral")}">${item.learning_tier === "core" ? icon("star", 11) : ""}${esc(tier.label)}</span>`
    : "";
  const dateBits = item.original_content_date && item.upload_date && item.upload_date !== item.original_content_date
    ? `<span>· 內容 ${esc(item.original_content_date)}</span><span>· 上架 ${esc(item.upload_date)}</span>`
    : item.original_content_date && item.upload_date
      ? `<span>· 內容／上架 ${esc(item.original_content_date)}</span>`
      : item.original_content_date
        ? `<span>· 內容 ${esc(item.original_content_date)}</span>`
      : item.upload_date
        ? `<span>· 上架 ${esc(item.upload_date)}</span>`
        : "";
  const interventionNotice = interventionNoticeText(item);

  $("#playerInfo").innerHTML = `
    <div class="Player__playbackStatus">
      <p id="playerStatus" role="status" aria-live="polite">${policy.blocked ? "診斷時間範圍資料不完整，暫不載入播放器。" : "正在載入影片…"}</p>
      <a href="${esc(item.url)}" target="_blank" rel="noopener">在 YouTube 開啟原始來源（新分頁）</a>
      ${policy.ranges?.length ? `<p>本課從所選診斷段落開始，結束時暫停。YouTube 原生操作與原始來源仍可能播放範圍外內容。</p>
      <nav aria-label="選擇診斷段落">${policy.ranges.map((r, i) => `<button class="btn" type="button" data-seek="${r.start}">診斷段落 ${i + 1} · ${Math.floor(r.start / 60)}:${String(r.start % 60).padStart(2, "0")}–${Math.floor(r.end / 60)}:${String(r.end % 60).padStart(2, "0")}</button>`).join(" ")}</nav>` : ""}
    </div>
    <div class="Player__bar">
      <div class="Player__barMain">
        <h2 class="Player__title">${esc(item.name)}</h2>
        <div class="Player__sub">
          <span>${esc(item.chCode)} ${esc(item.chTitle)}</span>
          <span>›</span>
          <a href="#${esc(item.unitId)}" data-goto-unit="${esc(item.unitId)}">${esc(item.unitName)}</a>
          <span>· ${item.i + 1} / ${total}</span>
          ${tierBadge}
          ${badge}
          ${item.lang ? `<span class="Label Label--neutral">${esc(LANG[item.lang] || item.lang)}</span>` : ""}
          <span>${esc(item.channel || "")}</span>
          ${item.presenter || item.presenter_note ? `<span>· 講者：${esc(item.presenter || item.presenter_note)}</span>` : ""}
          ${item.duration ? `<span>· ${esc(item.duration)}</span>` : ""}
          ${dateBits}
          ${item.dose ? `<span class="Drill__dose">${esc(item.dose)}</span>` : ""}
        </div>
      </div>
      <div class="Player__actions">
        <button class="btn" data-step="-1" type="button" aria-label="上一部影片">${icon("chevron-left", 14)} <span class="Player__btnText">${esc(UI.prevLabel || "")}</span></button>
        <button class="btn" data-step="1" type="button" aria-label="下一部影片"><span class="Player__btnText">${esc(UI.nextLabel || "")}</span> ${icon("chevron-right", 14)}</button>
        <button class="btn" data-mark-unit="${esc(item.unitId)}" type="button">${icon("check", 14)} ${esc(UI.doneLabel || "")}</button>
        <button class="btn btn-icon" data-toggle-list type="button" title="收起／顯示清單">${icon("layers", 16)}<span class="visually-hidden" data-list-label>收起清單</span></button>
        ${discussButton()}
        <a class="btn btn-icon" href="${esc(item.url)}" target="_blank" rel="noopener" title="${esc(UI.openExternal || "")}">${icon("external-link", 16)}</a>
      </div>
    </div>
    ${
      interventionNotice
        ? `<div class="Player__interventionNotice" role="note" aria-live="polite" aria-atomic="true">
             <strong>介入內容提醒</strong>
             <span>${esc(interventionNotice)}</span>
             <span><strong>本課診斷段落：</strong>${esc(item.diagnostic_segment_range)}</span>
           </div>`
        : ""
    }
    ${
      item.why || item.scope_note || item.disclosure || item.date_note || item.assessment
        ? `<details class="Player__more">
             <summary>${esc(UI.moreLabel || "")}</summary>
             ${item.why ? `<p class="Player__note">${esc(item.why)}</p>` : ""}
             ${item.scope_note ? `<p class="Player__note"><strong>適用範圍　</strong>${esc(item.scope_note)}</p>` : ""}
             ${item.disclosure ? `<p class="Player__note"><strong>來源揭露　</strong>${esc(item.disclosure)}</p>` : ""}
             ${item.date_note ? `<p class="Player__note"><strong>日期註記　</strong>${esc(item.date_note)}</p>` : ""}
             ${item.assessment ? `<p class="Player__note"><strong>怎麼自己評估　</strong>${esc(item.assessment)}</p>` : ""}
           </details>`
        : ""
    }
    ${segmentRail(item, query)}
    ${discussPanel()}`;

  listenToFrame();
  fitFrame();
}

/**
 * 只重繪逐段筆記區。搜尋時不能走 play()——那會重設 iframe src，影片會從頭播。
 * 找不到既有的 .Segments 就不動（該片沒有已簽核的段落）。
 */
export function refreshSegments(item, query = "") {
  const host = document.querySelector("#playerInfo .Segments");
  if (!host || !item) return;
  const html = segmentRail(item, query);
  if (!html) return host.remove();
  const holder = document.createElement("div");
  holder.innerHTML = html;
  const next = holder.firstElementChild;
  if (next) host.replaceWith(next);
}

/** 依實際可用高度算出影片寬度，讓它吃滿又不變形。
 *  純 CSS 同時給 max-width + max-height 會讓 aspect-ratio 失效，所以這裡用量的。 */
export function fitFrame() {
  const stage = $(".Player__stage");
  const frame = $(".Player__frame");
  const info = $("#playerInfo");
  if (!stage || !frame) return;
  if (matchMedia("(max-width: 1012px)").matches) {
    frame.style.removeProperty("--frame-w");
    return;
  }

  // 資訊區想要多高就給多高，但最多只讓它吃掉 45%——逐段筆記可以很長，
  // 全額讓步會把影片壓到只剩幾百像素寬。超出的部分由 .Player__info 自己捲。
  const wanted = info ? Math.max(info.offsetHeight, info.scrollHeight) : 0;
  const reserved = Math.min(wanted, stage.clientHeight * 0.45);
  const avail = stage.clientHeight - reserved - 12;
  if (avail <= 0) return;
  const byHeight = avail * (16 / 9);
  frame.style.setProperty("--frame-w", `${Math.floor(Math.min(stage.clientWidth, byHeight))}px`);
}

/** 視窗大小改變或資訊區內容變動時重算 */
export function watchFrame() {
  const stage = $(".Player__stage");
  if (!stage || typeof ResizeObserver === "undefined") return;
  const ro = new ResizeObserver(() => fitFrame());
  ro.observe(stage);
  const info = $("#playerInfo");
  if (info) ro.observe(info);
  addEventListener("resize", fitFrame);
}

export function stop() {
  savePosition(true);
  clearFrameTimers();
  const f = $("#playerFrame iframe");
  if (f) f.remove();
  frameReady = false;
  currentItem = null;
}

/* --- 播放清單寬度可拖曳 --------------------------------------------------- */

const MIN_W = 260;

/** 讓使用者拖動分隔條調整右側清單寬度；回傳目前寬度供外部保存 */
export function initResizer(initial, onChange) {
  const player = $(".Player");
  const grip = $("#playerResizer");
  if (!player || !grip) return;

  const clamp = (w) => {
    const width = player.clientWidth;
    return width > 0 ? Math.max(MIN_W, Math.min(w, Math.round(width * 0.6))) : Math.max(MIN_W, w);
  };
  const apply = (w) => {
    player.style.setProperty("--playlist-w", `${clamp(w)}px`);
    fitFrame();
  };

  if (initial) apply(initial);

  grip.addEventListener("pointerdown", (e) => {
    e.preventDefault();
    grip.setPointerCapture(e.pointerId);
    grip.classList.add("is-dragging");
    document.body.classList.add("is-resizing");

    let pendingFrame = null;
    let nextWidth = null;
    const move = (ev) => {
      nextWidth = player.getBoundingClientRect().right - ev.clientX - 16;
      if (pendingFrame === null) pendingFrame = requestAnimationFrame(() => {
        apply(nextWidth);
        pendingFrame = null;
      });
    };
    const up = () => {
      if (pendingFrame !== null) cancelAnimationFrame(pendingFrame);
      if (nextWidth !== null) apply(nextWidth);
      grip.classList.remove("is-dragging");
      document.body.classList.remove("is-resizing");
      grip.removeEventListener("pointermove", move);
      grip.removeEventListener("pointerup", up);
      grip.removeEventListener("pointercancel", up);
      const w = parseInt(player.style.getPropertyValue("--playlist-w"), 10);
      if (w) onChange?.(w);
    };
    grip.addEventListener("pointermove", move);
    grip.addEventListener("pointerup", up);
    grip.addEventListener("pointercancel", up);
  });

  // 鍵盤也能調，方向鍵每次 24px
  grip.addEventListener("keydown", (e) => {
    const step = e.key === "ArrowLeft" ? 24 : e.key === "ArrowRight" ? -24 : 0;
    if (!step) return;
    e.preventDefault();
    e.stopPropagation();
    const cur = parseInt(getComputedStyle(player).getPropertyValue("--playlist-w"), 10) || 380;
    apply(cur + step);
    onChange?.(clamp(cur + step));
  });
}
