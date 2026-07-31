# 建置與交付計畫

## 凍結設定

- 部位：膝部（knee／膝關節）
- 受眾與語言：醫師；zh-TW 繁體中文
- 範圍：診斷掃描與判讀；介入操作延後
- recent-content cutoff：2021-08-01
- 網站記錄：`https://knee-ultrasound.sportsmedicine.tw`
- GitHub：`keanu77/knee-ultrasound-course`，private，預設分支 `main`
- 工作分支：`feat/knee-course-v1`
- 內容負責人與預定審閱者：吳易澄（復健科專科醫師）
- 目前狀態：`draft / noindex`

## 已執行流程

1. 環境與 GitHub CLI preflight。
2. course brief、責任與發布邊界凍結。
3. scaffold 初始化及跨部位殘留檢查。
4. 以 AIUM／EFSUMB／ESSR／ACR 等正式來源先定義四區掃描、限制及升級條件。
5. 近期影片、經典教師及排除候選逐支查核；只收錄兩支 ESSR 官方核心影片。
6. 八單元課程、來源 catalog、評量、影片資料契約與文件撰寫。
7. 臨床工作站 UI、窄螢幕 44px 觸控目標、可及性及快取檢查。
8. 本機 `make build`、`make check`、`make verify`。
9. 私有 GitHub repo、feature branch、draft PR 與 CI。

## 本次不執行

- 不執行 `make og`。Chrome 在 Codex sandbox 會被 seatbelt 阻擋 Mach port registration；OG 圖待 MacBook Air 在 sandbox 外產生並驗證 1200×630。
- 不執行 320／390／desktop 真實瀏覽器互動 QA；水平溢位、鍵盤、console、network、播放器 fallback 與 44px 觸控目標待 Air 端完成。
- 不 merge，不建立 Cloudflare Pages，不修改 DNS 或自訂網域，不執行 production smoke。
- 不把單元改為 `approved`，不把 `allowIndexing` 改為 `true`。

任何本機 gate 失敗都必須修正後才可建立 draft PR；OG 與真實瀏覽器 QA 依 frozen brief 是 Air 端明確 handoff，不是本次 stop condition。
