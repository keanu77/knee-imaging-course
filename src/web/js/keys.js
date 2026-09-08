// keys.js — 站內鍵盤快捷鍵。iframe 跨域，所以透過 YouTube IFrame API 的 postMessage 控制。
import { icon } from "./icons.js";
import { seekTo, getPosition } from "./player.js";
import { isTrustedPlayerMessage } from "./playback-policy.js";

const $ = (s, r = document) => r.querySelector(s);
const SHORTCUTS_KEY = "knee-imaging:single-key-shortcuts";
let shortcutsEnabled = true;
try { shortcutsEnabled = localStorage.getItem(SHORTCUTS_KEY) !== "false"; } catch { /* Storage may be unavailable. */ }

export function setShortcutsEnabled(enabled) {
  shortcutsEnabled = enabled === true;
  try { localStorage.setItem(SHORTCUTS_KEY, String(shortcutsEnabled)); } catch { /* Keep the in-memory preference. */ }
  const checkbox = $("#singleKeyShortcuts");
  if (checkbox) checkbox.checked = shortcutsEnabled;
}

// 由 infoDelivery 事件持續更新，供 seek/volume 這類需要現值的指令使用
const st = { time: 0, duration: 0, rate: 1, volume: 100, muted: false, playing: false };

function frame() {
  return $("#ytFrame");
}

function send(func, args = []) {
  const f = frame();
  if (!f?.contentWindow) return false;
  f.contentWindow.postMessage(
    JSON.stringify({ event: "command", func, args }),
    "https://www.youtube-nocookie.com",
  );
  return true;
}

/** 訂閱播放器狀態；每次換片後要重新呼叫 */
export function listen() {
  const f = frame();
  if (!f?.contentWindow) return;
  Object.assign(st, { time: getPosition() ?? 0, duration: 0, rate: 1, volume: 100, muted: false, playing: false });
  f.contentWindow.postMessage(
    JSON.stringify({ event: "listening", id: "ytFrame", channel: "widget" }),
    "https://www.youtube-nocookie.com",
  );
}

addEventListener("message", (e) => {
  if (!isTrustedPlayerMessage(e, frame()?.contentWindow)) return;
  let d;
  try {
    d = typeof e.data === "string" ? JSON.parse(e.data) : e.data;
  } catch {
    return;
  }
  const info = d?.info;
  if (!["infoDelivery", "initialDelivery"].includes(d?.event) || !info) return;
  if (Number.isFinite(info.currentTime) && info.currentTime >= 0) st.time = info.currentTime;
  if (Number.isFinite(info.duration) && info.duration >= 0) st.duration = info.duration;
  if (Number.isFinite(info.playbackRate) && info.playbackRate > 0 && info.playbackRate <= 16) st.rate = info.playbackRate;
  if (Number.isFinite(info.volume) && info.volume >= 0 && info.volume <= 100) st.volume = info.volume;
  if (typeof info.muted === "boolean") st.muted = info.muted;
  if (typeof info.playerState === "number") st.playing = info.playerState === 1;
});

const seek = (delta) => seekTo(Math.max(0, (getPosition() ?? 0) + delta), { autoplay: st.playing });
const setRate = (dir) => {
  const steps = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2];
  const i = steps.indexOf(st.rate);
  const next = steps[Math.min(steps.length - 1, Math.max(0, (i < 0 ? 3 : i) + dir))];
  st.rate = next;
  send("setPlaybackRate", [next]);
  toast(`${next}×`);
};

function toast(text) {
  let el = $("#ytToast");
  if (!el) {
    el = document.createElement("div");
    el.id = "ytToast";
    el.className = "YtToast";
    $(".Player__frame")?.append(el);
  }
  el.textContent = text;
  el.classList.add("is-on");
  clearTimeout(toast._t);
  toast._t = setTimeout(() => el.classList.remove("is-on"), 900);
}

/* --- 快捷鍵說明 ---------------------------------------------------------- */

const SHEET = [
  ["播放", [["Space / K", "播放或暫停"], ["J", "倒退 10 秒"], ["L", "快轉 10 秒"], ["← / →", "±5 秒"], ["0–9", "跳到影片 0%–90%"]]],
  ["聲音與畫面", [["M", "靜音切換"], ["↑ / ↓", "音量 ±10"], ["F", "全螢幕"], ["Shift + . / ,", "加速／減速"]]],
  ["課程導覽", [["N / P", "下一／上一章"], ["Shift + N / P", "下一／上一部影片"], ["/", "搜尋"], ["T", "切換主題"], ["?", "顯示這張表"]]],
];

let sheetOpener = null;
function toggleSheet(force) {
  let el = $("#keySheet");
  if (!el && force === false) return;
  if (!el) {
    el = document.createElement("dialog");
    el.id = "keySheet";
    el.setAttribute("aria-label", "鍵盤快捷鍵");
    Object.assign(el.style, { width: "100vw", height: "100dvh", maxWidth: "none", maxHeight: "none", margin: "0", border: "0", boxSizing: "border-box" });
    el.className = "KeySheet";
    el.innerHTML = `
      <div class="KeySheet__box">
        <div class="KeySheet__head">
          ${icon("info", 16)}<strong>鍵盤快捷鍵</strong>
          <button class="btn btn-invisible btn-icon" data-close type="button" aria-label="關閉快捷鍵說明" autofocus>${icon("x", 16)}</button>
        </div>
        <p class="KeySheet__foot">
          <label><input id="singleKeyShortcuts" type="checkbox"${shortcutsEnabled ? " checked" : ""} /> 啟用單鍵快捷鍵</label>
          <br />取消勾選可停用下列播放、搜尋與導覽快捷鍵；「?」說明與 Esc 關閉仍可使用。設定只保存在這個瀏覽器。
        </p>
        <div class="KeySheet__cols">
          ${SHEET.map(
            ([group, rows]) => `
            <div>
              <div class="KeySheet__group">${group}</div>
              ${rows.map(([k, d]) => `<div class="KeySheet__row"><kbd>${k}</kbd><span>${d}</span></div>`).join("")}
            </div>`,
          ).join("")}
        </div>
        <p class="KeySheet__foot">站內跳播以本課診斷段落為範圍。YouTube 原生操作與原始來源仍可能播放範圍外內容。</p>
      </div>`;
    el.addEventListener("click", (e) => {
      if (e.target === el || e.target.closest("[data-close]")) toggleSheet(false);
    });
    el.addEventListener("change", (e) => {
      if (e.target.id === "singleKeyShortcuts") setShortcutsEnabled(e.target.checked);
    });
    el.addEventListener("close", () => {
      el.classList.remove("is-on");
      if (sheetOpener?.isConnected) sheetOpener.focus();
    });
    document.body.append(el);
  }
  const open = force ?? !el.open;
  if (open && !el.open) {
    sheetOpener = document.activeElement;
    el.classList.add("is-on");
    el.showModal();
    $("[data-close]", el)?.focus();
  } else if (!open && el.open) {
    el.close();
  }
}

/* --- 綁定 ---------------------------------------------------------------- */

export function bindKeys({ next, prev, nextChapter, prevChapter, isPlayerTab }) {
  addEventListener("keydown", (e) => {
    const focused = document.activeElement;
    if (e.defaultPrevented || e.isComposing || e.target?.closest?.('[role="separator"]')) return;
    if ($("#keySheet")?.open) {
      if (e.key === "?") { e.preventDefault(); toggleSheet(false); }
      return;
    }
    // Preserve native button activation, slider movement, and details controls.
    if ((e.key === " " || e.key.startsWith("Arrow")) && focused?.closest?.('button, a, summary, [role="button"], [role="slider"]')) return;
    if (/^(INPUT|TEXTAREA|SELECT)$/.test(focused?.tagName) || focused?.isContentEditable) return;
    if (e.metaKey || e.ctrlKey || e.altKey) return;

    if (e.key === "?" || (e.shiftKey && e.key === "/")) {
      e.preventDefault();
      return toggleSheet();
    }
    if (e.key === "Escape") return toggleSheet(false);
    if (!shortcutsEnabled) return;

    if (e.key === "/") {
      e.preventDefault();
      return $(isPlayerTab() ? "#playlistSearch" : "#search")?.focus();
    }

    // 換片不限分頁，其餘播放控制只在上課模式生效
    if (e.shiftKey && (e.key === "N" || e.key === "n")) return e.preventDefault(), next();
    if (e.shiftKey && (e.key === "P" || e.key === "p")) return e.preventDefault(), prev();
    if (!e.shiftKey && (e.key === "n" || e.key === "N")) return e.preventDefault(), nextChapter();
    if (!e.shiftKey && (e.key === "p" || e.key === "P")) return e.preventDefault(), prevChapter();
    if (!e.shiftKey && (e.key === "t" || e.key === "T")) {
      e.preventDefault();
      return $("#themeToggle")?.click();
    }
    if (!isPlayerTab() || !frame()) return;

    const k = e.key;
    if (k === " " || k === "k" || k === "K") {
      e.preventDefault();
      send(st.playing ? "pauseVideo" : "playVideo");
      st.playing = !st.playing;
    } else if (k === "j" || k === "J") { e.preventDefault(); seek(-10); toast("−10 秒"); }
    else if (k === "l" || k === "L") { e.preventDefault(); seek(10); toast("+10 秒"); }
    else if (k === "ArrowLeft") { e.preventDefault(); seek(-5); toast("−5 秒"); }
    else if (k === "ArrowRight") { e.preventDefault(); seek(5); toast("+5 秒"); }
    else if (k === "m" || k === "M") {
      e.preventDefault();
      send(st.muted ? "unMute" : "mute");
      st.muted = !st.muted;
      toast(st.muted ? "靜音" : "取消靜音");
    } else if (k === "ArrowUp" || k === "ArrowDown") {
      e.preventDefault();
      const v = Math.max(0, Math.min(100, st.volume + (k === "ArrowUp" ? 10 : -10)));
      st.volume = v;
      send("setVolume", [v]);
      toast(`音量 ${v}`);
    } else if (k === "f" || k === "F") {
      e.preventDefault();
      const box = $(".Player__frame");
      document.fullscreenElement ? document.exitFullscreen() : box?.requestFullscreen?.();
    } else if (e.shiftKey && (k === ">" || k === ".")) { e.preventDefault(); setRate(1); }
    else if (e.shiftKey && (k === "<" || k === ",")) { e.preventDefault(); setRate(-1); }
    else if (/^[0-9]$/.test(k) && st.duration) {
      e.preventDefault();
      seekTo(st.duration * (+k / 10), { autoplay: st.playing });
      toast(`${+k * 10}%`);
    }
  });
}
