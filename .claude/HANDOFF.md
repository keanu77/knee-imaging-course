# 2026-09-10 Repo 文件整備

- 原始碼可見性：PUBLIC；依使用者指示，只公開肩部與膝部，其餘維持私有。
- 現行入口：https://knee-imaging.sportsmedicine.tw/；系列首頁：https://imaging-course-hub.sportsmedicine.tw/。
- README、引用、貢獻、安全回報、資料範圍、開發、部署與改作說明已整理。歷史說明見 docs/COURSE_GUIDE.md；其他日期報告維持歷史用途。
- 本次不新增教材、不刷新醫療審閱、不更動搜尋索引。資料以 course 原始檔 SHA 比對確認。
- 最終驗證與部署摘要見 docs/REPOSITORY_READINESS.md。

以下保留之前交接；其中網址、可見性與未發布狀態可能已過期，以本段和現行文件為準。

# 2026-09-10 學習站正式網域

- 主頁正式網址：https://imaging-course-hub.sportsmedicine.tw/。課程返回按鈕與主頁 canonical 同步更新。
- 各公開頁面提供推薦影片／文獻入口，並傳送來源課程與單元網址。
- 延續預設深色與既有教材審閱狀態。發布及驗證紀錄見工作區 HANDOFF 與 hub-domain-*.json。

# 2026-09-10 預設深色與返回主頁

- 首次造訪預設深色；即使系統偏好淺色、無儲存權限或無 JavaScript 亦然。原有深淺切換與有效偏好繼續保留。
- 七個課程網站左上方新增「← 學習站首頁」，連到 https://imaging-course-hub.pages.dev/；檢核表與已發布進階頁同步提供。
- 檢核表採深色螢幕顯示、白底列印。膝部純靜態單元講義維持無 JS、固定深色，主頁外連延續新分頁規則。
- 教材、策展批准與醫療審閱狀態未改。八站實際品質檢查及瀏覽器驗證均通過，證據為 ../imaging-design-audit-2026-09-09/dark-default-checks-final.json 與 dark-default-browser-0.json；舊失敗報告保留。
- 最終部署 SHA 與狀態見工作區 ../.claude/HANDOFF.md。

# 2026-09-10 搬移與發布進行中

工作路徑：`/Users/ethanstudio/Documents/Vobe coding/knee-imaging-course-design`。使用者已要求推送 GitHub 與部署 Cloudflare；正在核對實際上線 commit。以下為歷史工作記錄。髖／踝足進階研究包仍保留 draft，不視為新增策展批准。

# HANDOFF


## 2026-09-09：運動醫學品牌設計與統合入口（未發布）

- 使用者要求 multi-llm audit 後優化七站，並新增統合課程主頁。
- 本輪 src/web/css/sports-medicine.css 統一藍白／深藍與珊瑚色視覺；首頁、課程側欄、章節、篩選、焦點與手機入口已調整。index/app 修復當前視圖 SkipLink、首頁 CTA 焦點；六站另修復 JSON 格式主題保存。
- course/ 全部檔案 SHA-256 與本輪起始相同。沒有改變醫療狀態、核准、索引政策或研究包。
- Codex gpt-6-astra、Gemini（CLI 指定 gemini-3.1-pro-high）、本機 qwen3.8:27b-mlx 實際執行；18 項 Pass 2：../imaging-design-audit-2026-09-09/PASS2.md。
- make check 七站通過；版型 168 組、操作 49 項、系統／手動主題 28 組；六站完整 UI 回歸與膝站 14 項 browser smoke 通過。影片 fixture 測試不代表真實串流驗證。
- 統合主頁 ../imaging-course-hub/；http://127.0.0.1:8940/preview/ 可進七個本機新版；/dist/ 連往已核對的線上網址。稽核與比較頁 http://127.0.0.1:8941/。
- 新設計與主頁未 commit、push、部署，尚未設定統合主網域；前一批發布批准不視為本輪新增內容的臨床簽核。先前原有 dirty files 保留。
- 此目錄是由 Documents 的 knee-image-course 建立之隔離 clone；origin 目前指向本機來源，不可直接當 GitHub 遠端 push。原始 Documents checkout 及其未提交文件保持原樣。


## 2026-09-10：移除裝飾邊框與影片來源目錄（未發布）

- 使用者不希望截圖所示的圓角白框／粗藍頂邊；已在共用 sports-medicine.css 移除首頁引導、閱讀標頭、進階入口與章節標題的同類裝飾。
- 主頁更名「運動醫學影像學習站」，新增七站主要影片來源及逐片重要性，134 筆核心收錄／132 支影片／39 個發布頻道，另可切換完整 251 筆。
- 最新主頁 http://127.0.0.1:8940/preview/；來源 http://127.0.0.1:8940/preview/sources.html；來源頁可下載主要／完整 CSV。
- 影片 metadata 仍是 2026-09-09 快照；本次未變更 course 資料或審閱狀態。既有缺少講者／資格資訊明示待補查。
- 七站重新建置、168 組版面、49 項操作及主頁／來源頁瀏覽器測試通過；84 個 course 檔案 SHA-256 不變。詳見 ../imaging-course-hub/docs/UPDATE-2026-09-10.md。
- 本輪仍是未發布的本機修改，沒有新增 commit／push。
