# 獨立審核報告（第一輪）

審核日期：2026-08-01｜審核範圍：`feat/knee-course-v1`（commit `9083054`）｜審核者：獨立 AI 審核（Claude），非醫師簽核

## 一句話結論

**修正後可部署**——技術面全綠、介入時間戳實查無誤、無法規阻斷項；唯一的部署前提是**醫師本人完成 8 個 draft 單元的臨床簽核**（在此之前維持 noindex 是正確狀態，可先以現狀部署為非索引預覽站）。

---

## 一、介入時間戳查核（實查字幕，非引用既有紀錄）

方法：以 `yt-dlp` 下載兩支影片的英文自動字幕（VTT，含逐字時間戳），人工判讀宣稱時間點前後 90 秒的內容。

| video_id | 宣稱介入起點 | 實查結果 | 證據（字幕逐字時間戳） | 處置 |
|---|---|---|---|---|
| `9oADQrcj_qQ`（AMSSM 髕腱病例） | 21:46 | ✅ 準確 | 21:43–21:46「…not to get into the **treatment**(21:46.4) um much at all but we did end up **aspirating**(21:50.2) this specific structure… our aspirate was a very thick gelatinous fluid」。21:46 前的內容為腱內囊腫與肌腱內撕裂的鑑別討論（純診斷）。 | 無需修改 |
| `EPdbvE39xmQ`（AMSSM 外側半月板旁囊腫病例） | 15:37 | ✅ 成立（誤差在自動字幕容差內） | 15:33–15:38「…and then just a **bonus picture**(15:35.0) we did bring her back(15:36.2) um for an **aspiration**(15:38.2)…Diagnostic therapeutic aspiration」。15:33 前為 MRI 對照（純診斷）；轉折句起於約 15:34，「aspiration」一詞落在 15:38，宣稱的 15:37 與實況相差 ≤3 秒，屬自動字幕時間戳的正常漂移範圍。 | 無需修改（若醫師想更保守，可把診斷段終點從 15:36 提前到 15:33，非必要） |

兩支影片的 `scope_note`、`diagnostic_segment_range` 與播放器的介入提醒（`render.js:51`、`player.js`）均與實查結果一致。

---

## 二、技術優化（已 commit `9083054` 並 push）

1. **建置與檢查全綠**：`uv sync --locked` → `make build`、`make check`（ruff + 離線稽核 + 醫療結構閘門）、`make verify`（4 支影片連結 + 14 筆文獻來源線上重驗）全部通過。
2. **引文 PMID 修正**：`syllabus.json` stance 段內嵌引文〈Evaluation of the knee joint with ultrasound and MRI〉原連到 PMID 37999655——經 PubMed esummary 查證，該 PMID 是一篇**兒科前臂 POCUS** 論文；已改為 38020509（正確論文，與 reference_catalog 的 `REF-PANDYA-KNEE-2023` 一致）。僅修連結，未動任何臨床文字。
3. **觸控目標補滿 44px**（767px 以下，桌面密度不動）：靜態稽核找出 12 個未達標元素並全數補上 `min-width`/`min-height`——搜尋清除鈕、重設進度、肌群 chip 與清除鈕、肌群標籤按鈕、主課語言切換、實證卡展開列（兩種）、StanceCard／Player「更多」／頁尾免責聲明三種 summary 展開列、快捷鍵表關閉鈕；另把貼線 44px 的 MusclePanel__head 加固到 48px。頁尾加高時同步調整 `--footer-height` 變數，避免內容被固定頁尾遮住。
4. **死碼清理（-139 行）**：刪除全案 grep 確認無引用的樣式與匯出——舊健身課模板殘留的 `Drill__marker--release/stretch/train`、`PlaylistItem__dot--*`，改版前遺留的 `Stance__*`（現用 `StancePage`/`StanceCard`）、`Player__crumb`、`.rating`、`Label--done`、`Box`、`Flash` 系列；`discuss.js` 未使用的 `enabled` 匯出；`render.js` 的 `GRADE`/`renderUnit` 改為模組私有。動態組出的 class（`Label--${tone}`、`MuscleBlock--${mod}`）已逐一確認保留。`console.log`、註解掉的舊程式碼：無。
5. **安全掃描**：無 secret／API key／token／個人路徑／內網主機名／tailnet 網址（命中僅 `.venv` 內套件自身路徑，未入庫）。
6. **快取一致性**：確認 HTML、ES module import graph 與 `course.json` fetch 共用同一內容指紋（本輪重建後為 `dfb66494cd88`，HTML 10 處 + ES modules 15 處 + course.json 1 處，無混版風險）。

---

## 三、🔴 必須由醫師處理的項目

1. **臨床簽核（部署開索引的前提）**：8 個單元 review status 全為 `draft`，`approved` 依規只能由醫師本人設定。本輪內容審核未發現臨床阻斷項（療效保證語句 0 命中；側別／解剖方位逐條檢查全數正確，含 MCL/LCL、鵝足三肌腱、ITB–Gerdy 結節、股二頭肌–腓骨頭、腓總神經繞腓骨頸、Baker 氏囊腫頸部定位；診斷／介入邊界在內容層面守住），但這不能取代醫師逐單元判讀。
2. **介入影片的段落判斷確認**：兩支 AMSSM 病例的時間戳已實查無誤（見第一節），但「診斷段落止於何處」的臨床判斷（尤其 `EPdbvE39xmQ` 是否要把終點從 15:36 保守提前到 15:33）應由醫師最終確認。

## 四、🟡 建議但非阻斷的項目

1. **介入段技術性截斷**：播放器未使用 YouTube embed 的 `start`/`end` 參數，學員可續看 aspiration 段，目前僅靠文字提醒。建議對 `contains_intervention: true` 的影片以 `end` 參數強制止於診斷段終點。
2. **免責聲明補一句總括**：footer 聲明已覆蓋「僅供教育、不取代 hands-on 與督導、不提供介入指引」，「不作為操作依據」目前僅在影片層級提醒出現；建議在課程層級聲明補一句總括。
3. **`REF-EULAR-OMERACT-2017` 時效理由**：其 note 只說明適用情境（RA 滑膜炎術語），未如其他三筆逾五年文獻（ESSR-2010、EULAR-2017、ACR-2020）明寫「早於 cutoff」的保留理由，建議補齊格式。
4. **外側章動態檢查描述**（`syllabus.json:469`）：「外翻／內翻」對外側動態的影響描述無誤，但可更精確指明內翻應力對應 LCL 評估。
5. **觸控目標為靜態分析結論**：本環境無法啟動 headless 瀏覽器實測（權限限制），第 3 項修正是以完整 CSS cascade 靜態推算（320px 與 390px 命中同一組 media query，結論一致）。建議部署預覽後用 DevTools 裝置模式抽查一次。

---

## 五、部署就緒檢查表

| 項目 | 狀態 |
|---|---|
| `uv run python src/build/build.py` 可獨立跑完（Cloudflare Pages 指令） | ✅ |
| `dist/` 含 index.html、course.json、css、js、og.png、robots.txt、sitemap.xml、llms.txt、`_headers` | ✅ 全數存在 |
| `dist/og.png` 為 1200×630 | ✅（sips 實測 1200×630） |
| `_headers` 含 `X-Robots-Tag: noindex` | ✅（`noindex, nofollow`） |
| `robots.txt` 為 `Disallow: /` | ✅ |
| `sitemap.xml` 為空清單 | ✅（空 `<urlset>`） |
| `course.config.json` 的 `site.url` = `https://knee-imaging.sportsmedicine.tw` | ✅ |
| `allowIndexing` 維持 false | ✅（未更動） |
| CI（quality.yml）在該分支 | ✅ 綠（含本輪 commit `9083054` 的最新 run） |

本輪未動：review status、indexing 相關設定、Cloudflare／DNS、臨床內容實質文字（除上述 PMID 連結修正外）。
