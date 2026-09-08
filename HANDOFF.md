# HANDOFF — 2026-09-09

## 最新 ship 授權與發布檢查

2026-09-09 使用者明確要求 `ship`，已授權提交及推送本工作樹的 UI、美編修正、兩批核准教材、測試與稽核紀錄。下方「未授權發布／等待發布指令」均為歷史，不再構成阻擋。

本次重跑 make check、make verify、14 項 browser smoke 通過；43/43 影片 oEmbed、42/42 來源連結通過。無依賴或環境變數變更；原生 JS 以 make jscheck 驗證。敏感資料掃描唯一候選為 VuMedi 的 msk 網址字串，非憑證。兩個既有 audit 提示保留（共用影片3支、Pedret原片較長）。

Cloudflare 實際建置 `python3 src/build/build.py`、output dist、GitHub main。更名前 repo 名稱仍在平台 source config，但 repository ID 1318617772 與目前 knee-imaging-course 相同。完整流程見 docs/DEPLOYMENT.md。推送前正式部署為 9b68659／eda91514-cfe2-4efe-b458-6b78af6ef538；發布後以平台新 commit、正式站內容雜湊和 GitHub Actions 為準。工作樹提交前基底 75cfd6c，包含一個尚未推送的舊文案修正。

## 最新：進階批次已同意收錄並完成本機整合

使用者最新「同意收錄」明確核准前輪具體進階教材；已完成整合，無須再詢問策展同意。新裁決 `course/research/2026-09-08-advanced-approval.json` 精確綁定兩份不可變 reviewed proposals（仍保留 draft 作歷史）：advanced-candidates SHA b8f596455cef059760fef11b7cb56442182ee472ca9e577a6a117135c4e83da7；advanced-cases SHA d4630b5fb362b7d5f7b13986f733af96c28ea0b07727e31d9e618544d543765d。不要重寫這兩份受審稿。

正式本機 build 現為 **25 單元、9 章、43 不重複影片（46 入口）、375 段、81 知識題、42 參考來源、14 判讀練習**；原片去重 15 小時 10 分，不等於診斷選段學習時數。新增 7 單元、7 影片、21 段（30:25）、21 題、11 文獻與 14 練習；4 片經典例外均納入本次批准。TT–TG 解析按已核准修正改為「CT 與 MRI 的量測值及切點不可直接互換，應採用與影像方法及族群相符的判準。」其餘舊教材保留。

`course/data/cases.json` 為正式 approved 練習資料；`case_pages.py`／`case_render.py` 產生 dist/practice/index.html。首頁、各進階單元及靜態講義均有入口；practice 可回相關單元。先填判讀才揭解析，逐項自評、可清除與列印；無持久化、無臨床合格分數。14 項是公開影像／報告／證據練習，不是 14 組未知答案 DICOM。歷史 review CLI 維持 draft-only，禁止寫 dist/public。

真實串流 **7/7 抽查成功**：`docs/audits/2026-09-08-advanced-playback.json`；Chrome 本機合法 nocookie iframe，確認目標影片、非廣告、從指定起點前進且解碼影格增加。舊 0/7 根因是8902/cases頁 CSP 禁止 iframe，不能當成影片失效。這不代表全片聲畫／臨床背書或正式網域驗證。原候選稿與舊verification仍保留原始狀態，最新以approved-verification為準。

驗證：make jscheck/test/build/audit、ruff、diff check；14 既有瀏覽器回歸通過；320/390/1440 三尺寸逐一完成14練習作答/重練/單元/靜態講義回鏈，無溢出或頁面錯誤。兩個 audit 提示保留：共用影片3支（跨主題入口，不重算unique）；Pedret原片83:32（既有診斷選段21:28）。未放寬閘門。

預覽 http://127.0.0.1:8899/ ，練習 http://127.0.0.1:8899/practice/ 。未 commit/push/deploy；仍等待使用者後續發布指令。四外部模型與29項Pass2報告保留。不要重做前輪UI、不要恢復襯線或首頁圖譜封面。

## 以下為先前批次與歷史狀態；數字／批准狀態以上節為準

## 最新要求與授權

使用者原要求多模型檢查／優化 knee images，並增加運動傷害超音波教材。使用者已回覆「可以收錄」，具體4單元、4片、22段、12題、7篇文獻的策展裁決已解除；不要再次要求教材收錄核准。最新要求是檢視整站美編，希望達到頂尖水準；已完成第二輪編輯式美編升級，見 `docs/audits/2026-09-08-art-direction.md`。

本機內容整合與介面修正已完成。尚未 commit/push/deploy；正式站 https://knee-imaging.sportsmedicine.tw/ 未含這輪變更。CF project 保持 `knee-ultrasound-course`。早期 goal 的 blocked 說明已過時，不可再以欠缺教材策展答覆為由停工。

## 工作樹

基底 main HEAD `75cfd6ce4dec8eb8c9e82de095f1c000975ba198`，本輪所有未提交修改均為本次工作。新增教材18單元／36獨立影片（38項目）／354段／60題／31參考，原先14單元與舊審閱紀錄保持原值。原片總長去重12小時43分。

策展記錄：`course/research/2026-09-08-sports-ultrasound-approval.json`。受審原檔保留draft與SHA `f15403cc757ba3bfc4e683736c5850a5b0ed9aa071e74b3a4adca91410476a41`，不要重寫以免失去精確綁定。新核准資料已整合course/data及配額。14處相鄰片段結尾縮短1秒適配strict non-overlap，診斷選段總範圍57:24不變。收錄同意不是完整逐影格聲畫或第三方臨床背書。

## 完成項目

最新 UI／UX 報告：`docs/audits/2026-09-08-ui-ux.md`。手机導覽折疊、第一章提前至608px、搜尋層次、空結果復原、手機播放器自然捲動與快速導航、選片後影片可见、桌面長標題／按鈕換行。新教材範圍與原始來源已呈現於互動與靜態閱讀頁，題目來源於提交後顯示。共用影片依unit保存與分享脈絡保持有效。

四模型歷史稽核、原修正及兩次真實影片spot check見 `docs/audits/2026-09-08-implementation.md`、`2026-09-08-multi-llm-validation.md`；舊文件的draft待裁決文字屬歷史，最新狀態以此文件及approval ledger為準。

## 驗證

- `make jscheck test build audit PY=.venv/bin/python` 通過，ruff與diff check通過。
- `tests/browser_smoke.cjs` 14情境全通過。慣用Playwright路徑 `/Users/ethanstudio/.agents/skills/fb-post/node_modules/playwright`，BASE_URL http://127.0.0.1:8899/ 。影片使用inert fixture，非真實串流驗證。
- 唯讀對抗審查實測320×568、390×844、844×390、1012×600、1013×500、1440×600。唯一計數用語問題已修正。
- 唯一audit提示：Pedret完整影片83:32>建議70m，實際診斷段21:28；未放寬audit。
- 最後log `/tmp/knee-ui-final-checks.log`、`/tmp/knee-ui-browser-final.log`。UI截圖 `/tmp/knee-ui-*.png`、`/tmp/knee-ui-audit-*.png`。

## 預覽與後續

本機dist server127.0.0.1:8899正常。若sandbox內curl失敗先以允許網路的執行確認，不要直接判定server沒開（本次遇到sandbox隔離）。僅服務dist，勿公開整個repo。早期審閱台8901可保留歷史比對。

下一步依使用者發布／commit and push指令處理，屆時檢查當前遠端、跑必要檢查、完成發布並驗證線上獨特標記。不需重新策展核准。

## 最新美編續作

首頁新增圖譜封面，襯線標題、三組章節索引與學習路徑CTA；播放器中性黑畫布，閱讀與檢核表版型統一。新版og.html/og.png已產生，dist相同；og使用靜態內嵌既有SVG，可獨立渲染。修正320px時長掉行與未打包arrow-right（改用chevron-right）。六使用須知完整保留，沒有修改核准醫療內容。

最新make jscheck/test/build/audit、ruff、diff check和14情境全通過。獨立美編代理複核明暗、字體載入/後備、320至1440px無溢出。最新log `/tmp/knee-art-checks.log`、`/tmp/knee-art-browser.log`；本機截圖 `.tmp/previews/home-desktop.png`／`home-mobile.png`。尚未發布，依使用者後續發布指令處理。

## 最新使用者美編修正

使用者明確要求全站不要細明體／襯線字體，標題與內文使用相同無襯線字體；並刪除首頁整塊圖譜封面（XR/US/MR、編號與觀察影像等裝飾）。已移除HTML及無用CSS，首頁回到單欄；全站Noto Serif／Songti載入已刪除，閱讀頁、檢核表、分享圖同步使用Noto Sans TC。不要恢復前輪的襯線字體或封面。

本機建置、JS解析、ruff、diff check通過；390/1440下首頁、課程、閱讀頁與檢核表共8個畫面確認h1字體等於內文、無水平溢出、無AtlasCover。分享圖已重新產生並重建dist。最新截圖仍在`.tmp/previews/`；未發布。
