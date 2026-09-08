先讀指定的產品與前端檔案，只做資訊架構、學習路徑、搜尋、視覺層級與完成／複習 UX 的唯讀審查。接著讀指定的前端與設定檔，並對照完成狀態、搜尋與學習路徑相關邏輯。掌握度、搜尋擴展與播放清單過濾的實作還要對過；同時核對章節內容是否與學習路徑一致。**P0　單元內先考後看片**
`render.js:561-576` 展開序：檢核表→assessment→quiz→drills。影響：未看片就作知識檢核。修：必備視圖與影片後再檢核。〔實作〕

**P0　續讀不接學習路徑**
`render.js:633-635,681-698` `last||first`，已完成仍回同一單元。影響：14 單元路徑停住。修：待複習→學習中→下一未開始；全完成改複習入口。〔實作〕

**P0　搜尋雙軌、332 段在課程頁搜不到**
`index.html:63-75,157-159`；`app.js:1037-1042` 頂欄不切 tab、不寫 `playlistQuery`。`filters.js:71-103` 只掃 `unitEl.textContent`、只開 chapter、不開 unit、無標亮。`player.js:199-210` 才搜 segments，且無 glossary。影響：首頁/播放頁打頂欄無回饋；記得筆記用詞找不到。修：單一 query；命中切課程並展開單元；glossary 同步播放清單。〔實作〕

**P0　上線狀態文案自相矛盾**
`course.config.json:43` `allowIndexing:true`；`404` 仍寫「草稿單元…維持 noindex」。`index.html:223` 硬編碼「醫療審閱中」。影響：誤判未審完、不可引用。修：ctaLede 改已上線；badge 用 `courseReviewLabel`。〔實作〕

**P1　三主軸被超音波工作站吞掉**
`index.html:113-115,213-219`「進入掃描工作站／膝蓋診斷掃描工作站」；`clinical.css:1-2`；`config:351-353` 步驟先探頭長短軸，nav 卻從 XR1。`render.js:185-199` XR/MRI 仍 VIEW SET／SCAN KEYS。影響：X 光/MRI 學員以為走錯站。修：主 CTA「進入課程」；步驟改 XR→US→MRI；檢核表標籤依 `unit.type`。〔實作〕

**P1　首頁不在導覽**
`index.html:47-58` 僅課程/影片；`app.js:655-668` home 只靠品牌。`layout.css:470-472` ≤767px 藏品牌名。影響：使用須知回不去。修：加「首頁」分頁。〔實作〕

**P1　「開始前先知道」有題無文**
`render.js:660` 取 `CFG.stance.verdicts`；`config:343` 為 `{}`。syllabus `222-300` 的 `summary` 未輸出。且三則皆超音波範圍，未對 XR/MRI。修：渲染 `summary`。三主軸立場需新文案。〔實作＋教材〕

**P1　掌握度／複習 UX 斷裂**
`app.js:135-136,351-356,375-381,507-521` 展開即 learning；進度只算 done；未滿分→review，滿分不標完成；`player.js:308`「完成」在 review 時對隱藏 quiz `scrollIntoView`、不切 tab。無待複習篩選。影響：學習中/待複習在 0/14 隱形。修：四態計入進度；待複習篩選；播放器完成改切課程檢核。〔實作〕

**P1　展開狀態只寫不讀**
`app.js:1063-1066,1246-1248` `expandAll` 寫入 `STORE.open` 後，首次展開第一章失效，重整全收合。修：還原 open，或分開 firstVisit 鍵。〔實作〕

**P1　單元代碼與章衝突**
`render.js:554` `ch8-u1`→「CH8 / U1」，章為 XR1（`syllabus.json:308`）；MR3 才是 `mr3-u1`。影響：側欄 XR1、卡片 CH8。修：kicker 用章代碼+序，id 只當 hash。〔實作〕

**P1　篩選留空殼；三單元無片**
`filters.js:84-99` kind/core 只藏 Drill，單元仍在。`index.html:243` 仍寫「動作類型」。`syllabus.json:643,688,1179` `ch0-u1`、`ch1-u1`、`ch6-u1` `drills:[]`。修：無可見影片標「閱讀」或藏空殼（實作）；`ch1-u1` 假影控制、`ch6-u1` 多平面病理需合格示範片。〔教材／授權影像〕

**P1　搜尋品質**
`app.js:544-558` glossary `includes(q)` 後 OR。`filters.js:74` 含 `display:none` 的 rationale（`quiz.css:156-157`）。`segment-search.js:24-28` 無別名。影響：短字爆量；未作答可搜到解析。修：詞界／前綴；搜尋排除 rationale；播放清單共用 `expandedSearchTerms`。〔實作〕

**P2　視覺噪音**
全 approved 仍每單元「已核准」（`render.js:518`）；英文 DIAGNOSTIC WORKSTATION／SCAN PATHWAY／VIDEO FILTER／LEARNING TARGET（`index.html:44,178,215,241`；`render.js:161`）；名詞分類英丁（`app.js:569-624`）。修：全核准不重複標；chrome 中文化。〔實作〕

**P2　完成顆粒度**
僅單元掌握。`player.js:200`「只顯示未完成」整單元 32 片一併消失。修：可選逐片 watched。〔實作〕

**待驗證** 窄屏頂欄與 TabNav 擠壓（`layout.css:443-464` 未實測）。首屏 `course`→`home` 閃切（`index.html:49` vs `app.js:1232`）。
