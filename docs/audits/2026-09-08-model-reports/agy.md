### P0：影片時間範圍控制缺乏強制邊界與截斷機制
* **檔案:行號**：[player.js:141-147](file:///src/web/js/player.js#L141-L147), [player.js:116-124](file:///src/web/js/player.js#L116-L124), [keys.js:51](file:///src/web/js/keys.js#L51), [keys.js:170-173](file:///src/web/js/keys.js#L170-L173)
* **實際證據**：`player.js` 雖於 UI 提示 `contains_intervention` 與 `diagnostic_segment_range` 並宣稱「段落已框限在診斷範圍內」(line 178)，但 `frameHtml` 僅傳入 `&start=${startSeconds}`，未傳入 `&end=` 參數；`seekTo` 與 `keys.js` 的 `seek`、百分比快進鍵 (`0–9`) 均無時間上限限制，亦無監聽 `currentTime` 超出範圍時自動暫停的機制。
* **使用者影響**：醫師觀看超音波診斷示範時，播放器會自動連續播入未經審查的侵入性介入處置（如注射、穿刺）片段，引發臨床處置與教學範疇認知的嚴重風險。
* **具體修法**：在 `frameHtml` 針對含介入內容之影片依 `intervention_start_timestamp` 補上 `&end=` 參數；在 `seekTo` 與快捷鍵快轉加入時間上限判定；監聽 `keys.js` 的 `st.time`，一旦超過診斷區段立即調用 `send("pauseVideo")`。

---

### P0：上課模式狀態恢復違反「不自動播放」宣告
* **檔案:行號**：[app.js:1241-1244](file:///src/web/js/app.js#L1241-L1244), [player.js:142](file:///src/web/js/player.js#L142)
* **實際證據**：`app.js:1241` 程式碼註解明示「還原上次看到哪，但不自動播放，回來時先看到資訊就好」，但當 `state.tab === "player"` 時直接呼叫 `playAt(state.playing)`，該函式透過 `play()` 注入 iframe，其 `src` 寫死 `&autoplay=1`。
* **使用者影響**：學員若前次停留在上課模式，重新開啟網頁或重整時，影片立即自動播放並發出聲音，干擾安靜場所或臨床工作環境。
* **具體修法**：為 `playAt()` 與 `play()` 增加 `autoplay = true` 參數；在 `app.js:1243` 初次載入恢復播放時傳入 `autoplay = false`；在 `frameHtml` 中將 `&autoplay=1` 改為由參數動態帶入（`autoplay ? 1 : 0`）。

---

### P1：跨單元共用影片造成 `urlIndex` 覆寫與跳轉錯位
* **檔案:行號**：[app.js:37](file:///src/web/js/app.js#L37), [app.js:959-963](file:///src/web/js/app.js#L959-L963), [app.js:1184](file:///src/web/js/app.js#L1184), [build.py:422](file:///src/build/build.py#L422)
* **實際證據**：`build.py` 允許跨單元共用影片，但 `app.js:1184` 使用 `urlIndex.set(it.url, i)`（URL 為單一 Key）。若相同影片出現在不同章節單元，後者索引會直接覆蓋前者。
* **使用者影響**：醫師在前期章節單元中點擊影片站內播放時，播放器會錯誤定位至後期單元的播放清單項與章節上下文，破壞單元學習順序。
* **具體修法**：改以單元與網址組合鍵 `urlIndex.set(`${it.unitId}:${it.url}`, i)`，或將 Map 值改為陣列；點擊時依當前點擊處之 `closest(".Unit")?.dataset.unit` 取出相應索引。

---

### P1：`hashchange` 遺漏單元深連結處理導致歷史導航斷裂
* **檔案:行號**：[app.js:1252-1262](file:///src/web/js/app.js#L1252-L1262), [app.js:1264-1271](file:///src/web/js/app.js#L1264-L1271)
* **實際證據**：`init()` (line 1252) 解析了單元 Hash（如 `#ch5-u1`）並自動展開，但 `addEventListener("hashchange")` (line 1264) 僅處理 `videoIdFromHash()`（即 `#play=`），完全忽略單元與章節 Hash 的變更。
* **使用者影響**：使用者利用瀏覽器「上一頁/下一頁」在單元間切換，或在外部點擊不同單元錨點時，畫面毫無反應，無法展開該單元或定位。
* **具體修法**：將單元/章節 Hash 的滾動與展開邏輯抽取為獨立函式，於 `hashchange` 事件處理器中同時執行單元錨點判定與 `setTab("course")`。

---

### P1：待複習狀態於播放器觸發「完成」時未切換分頁導致靜默失效
* **檔案:行號**：[app.js:377-382](file:///src/web/js/app.js#L377-L382), [app.js:899-904](file:///src/web/js/app.js#L899-L904)
* **實際證據**：`toggleDone` 遇到 `current === "review"` 時，對該單元展開並嘗試 `scrollIntoView` 至 `.Quiz`；但在播放器分頁（`state.tab === "player"`）中，課程容器 `#main` 設有 `hidden = true`，且此分支未呼叫 `setTab("course")`。
* **使用者影響**：醫師在播放器介面點擊「完成」欲更新待複習單元時，畫面毫無視覺回饋亦未跳轉，造成按鈕損壞的假象。
* **具體修法**：在 `toggleDone` 的 `if (current === "review")` 分支開頭加入 `setTab("course");`，先解除 `#main` 的隱藏再進行捲動。

---

### P1：逐段筆記 URL 純字串比對造成不同 YouTube 格式筆記遺失
* **檔案:行號**：[build.py:96-108](file:///src/build/build.py#L96-L108), [build.py:377](file:///src/build/build.py#L377)
* **實際證據**：`collect_segments()` 以原始 `url` 作為 Key (`approved[url] = entry["segments"]`)，並於 line 377 進行 `if url in segments_by_url` 比對。然而 `build.py:42-44` 支援 `youtu.be/` 與 `youtube.com/watch?v=` 兩種格式。
* **使用者影響**：若 `segments.json` 與各章節 JSON 的 URL 書寫格式或帶參不同（如短網址 vs 長網址），審核通過的逐段筆記將無法配對，產出網站時靜默丟失全部筆記與時間跳播點。
* **具體修法**：在 `collect_segments` 改以 `video_id(url)` 作為 Key 索引已核准的段落；line 377 改以 `video_id(url)` 比對提取。

---

### P2：首頁載入時播放器寬度計算為 0，強制將自訂清單寬度縮為最小值
* **檔案:行號**：[player.js:402-408](file:///src/web/js/player.js#L402-L408), [app.js:1203](file:///src/web/js/app.js#L1203)
* **實際證據**：`initResizer` 於 `init()` 立即執行，若載入預設停留在首頁，`#view-player` 處於隱藏狀態，`player.clientWidth` 為 0。`clamp(w)` 計算 `Math.round(player.clientWidth * 0.6)` 得 0，導致 `Math.max(260, Math.min(w, 0))` 強制輸出 `260` 並寫入 style。
* **使用者影響**：醫師調整儲存的播放清單寬度，只要下次重啟落於首頁，自訂寬度便被重置為預設最小值 260px。
* **具體修法**：在 `clamp(w)` 內加入保護判斷：若 `player.clientWidth === 0` 則直接回傳 `w`，或延遲至首度切換至 `player` 分頁時再執行尺寸限制。

---

### P2：`STORE.lastUnit` 未校驗有效性導致「繼續學習」按鈕失效
* **檔案:行號**：[app.js:1167](file:///src/web/js/app.js#L1167), [app.js:823-824](file:///src/web/js/app.js#L823-L824), [app.js:758-759](file:///src/web/js/app.js#L758-L759)
* **實際證據**：`loadLearningState` 嚴格過濾了 `mastery`、`masteryRestore` 與 `quiz` 的單元 ID，但 `state.lastUnit` 直接自 localStorage 載入未驗證。若該 ID 在新版課程已更名或刪除，點擊首頁繼續按鈕觸發 `goToUnit`，因找不到元素 `if (!el) return` 靜默終止。
* **使用者影響**：網站改版後回訪的醫師點擊首頁「繼續學習」按鈕完全無反應。
* **具體修法**：在 `init()` 載入 `STORE.lastUnit` 後，檢查該 ID 是否存在於當前章節單元列表中；若不存在則重設為 `null` 並清除 localStorage 舊紀錄。

---

### P2：建置腳本對缺漏或無效 URL 未中斷建置，缺乏策展品質管制
* **檔案:行號**：[build.py:368-373](file:///src/build/build.py#L368-L373), [build.py:556-566](file:///src/build/build.py#L556-L566), [build.py:574-578](file:///src/build/build.py#L574-L578)
* **實際證據**：在檢驗出 `missing_urls` 或 `bad_urls` 時，腳本僅印出警告文字，並未將其納入 `problems` 陣列（只有同單元重複影片才會加入 `problems`），`main()` 仍正常回傳 0 產出 `course.json`。
* **使用者影響**：維護者或策展者若誤植非法 URL 或遺漏網址，CI 建置管線不會報錯中斷，將有缺陷的教學內容發布至正式站。
* **具體修法**：在偵測到 `missing_urls` 或 `bad_urls` 時，呼叫 `problems.append(...)`，確保資料驗證失敗時程序以 exit code 1 終止。

---

### P2：`keys.js` 跨來源通訊來源校驗過於寬鬆
* **檔案:行號**：[keys.js:34](file:///src/web/js/keys.js#L34)
* **實際證據**：`addEventListener("message")` 接收廣播時使用 `if (!e.origin.includes("youtube")) return;` 進行來源檢查。
* **使用者影響**：惡意網域（如 `youtube.com.attacker.com`）可通過子字串判定，向頁面發送偽造的 `infoDelivery` 訊息，竄改 `keys.js` 中的播放狀態快照。
* **具體修法**：改用白名單嚴格比對：`if (e.origin !== "https://www.youtube-nocookie.com" && e.origin !== "https://www.youtube.com") return;`。
