# 膝部影像診斷課程

醫師導向、繁體中文的膝部影像判讀自學課程網站，涵蓋 **X 光、超音波、MRI** 三種影像模態。

🔗 **正式站**：<https://knee-imaging.sportsmedicine.tw>

製作者：運動醫學科 吳易澄醫師（<https://sportsmedicine.tw>）

> **專業教育聲明**：本課程以醫師為主要學員，僅供教育用途，**不取代**實體 hands-on training、
> 合格督導、機構 credentialing、完整病史理學檢查或正式影像判讀報告。完成本課程不代表具備
> 獨立執行或出具影像診斷的資格。本課程為 **diagnostic-only**，不教授注射、穿刺或其他影像
> 導引介入操作；收錄影片若含介入片段，會標明起點並把課程內容框限在診斷段落內。

## 課程規模

| 項目 | 數量 |
| --- | --- |
| 章節 | 9（X 光 2・超音波 4・MRI 3） |
| 教學單元 | 14（全數經具名醫師逐項簽核） |
| 精選影片 | 32 支（8 核心必看・24 延伸學習），總長 9 小時 27 分 |
| 逐段筆記 | 332 段（可一鍵跳播） |
| 知識檢核題 | 48 題（每個選項附解析與文獻引用） |
| 雙語名詞表 | 120 條 |

## 內容範圍

- **X 光**：照射位選擇（承重 AP、lateral、skyline／Merchant、Rosenberg）、Ottawa knee rule、
  系統性判讀順序、K-L 分級、骨折 pattern 與正常變異（bipartite patella、fabella）
- **超音波**：探頭設定與各向異性控制、前／內／外／後四區掃描路徑、動態檢查、
  常見病理的多平面判讀、結構化報告與最低影像集
- **MRI**：序列邏輯與三平面判讀順序、半月板／交叉韌帶／側副韌帶、後外側角、
  伸膝機轉與髕股不穩量測、軟骨病灶分級與骨髓水腫鑑別、ACL 重建術後評估

## 這個 repo 有什麼值得參考

這是一個 **config-driven 的課程站框架**：`src/build/` 與 `src/web/` 不認識任何醫學主題，
內容與版面設定全部在 `course/`，換一份設定就能做另一個部位或主題的課程站。

如果你要做的是**有醫療責任的教學網站**，以下幾個內容治理機制可能最值得參考：

- **簽核閘門**：單元、逐段筆記、題目、名詞表都有 `review_status`，只有 `approved`
  會進入 `course.json` 上線。新增內容一律 `draft`，不影響既有簽核。
- **簽核追溯**：`src/build/approve.py` 會寫入 `reviewed_by` / `reviewer_role` /
  `reviewed_at` / `reviewed_commit`，每一條內容都能追回是誰、在哪個版本簽的。
- **介入內容框限**：含介入操作的影片以 `diagnostic_segment_range` 限制範圍，
  `audit_medical.py` 與 `tests/` 強制逐段筆記不得越界——避免學員一鍵跳進注射示範。
- **來源證據鏈**：每支影片存約 24 個 provenance 欄位（原始頻道、講者資格與證據 URL、
  可嵌入狀態、內容日期與 cutoff 例外理由、揭露聲明），缺欄位會被稽核擋下。
- **文獻真偽驗證**：`make verify` 打真實 PubMed API 驗證每一筆引用的 PMID 與連結存活。

## 本機建置

```bash
uv sync --locked
make build     # 合併課程資料 → dist/course.json、SEO 產出、可列印檢核表
make audit     # 離線稽核：設定檔、配額、影片欄位、內容深度
make test      # 安全性測試：介入框限與逐段筆記規則
make verify    # 打真實 API 驗證影片連結與 PubMed 引用（會跑一陣子）
make serve     # 本機預覽
```

`make meta`（用 yt-dlp 補影片中繼資料）與 `make og`（headless Chrome 產社群預覽圖）
需要本機環境支援，不在 CI 執行。部署到 Cloudflare Pages 的設定見 `docs/DEPLOYMENT.md`。

## 主要檔案

- `course/course.config.json`：站台文案、章節結構、醫療設定與稽核規則
- `course/data/syllabus.json`：單元教材、影片清單與參考文獻目錄
- `course/data/segments.json`：逐段筆記（含每支影片的字幕訛誤更正紀錄）
- `course/data/questions.json`：知識檢核題庫
- `course/data/glossary.json`：雙語名詞表
- `docs/VIDEO_CURATION.md`：影片資格查核、採用與**拒絕理由**紀錄
- `docs/VIDEO_INDEX.md`：影片依模態／部位／結構的多維分類索引
- `docs/DESIGN_UPGRADE.md`：對標頂尖醫學教育站的設計藍圖與藝術方向定案
- `docs/MEDICAL_REVIEW.md`：醫療審閱責任與狀態規則

## 授權

- **程式碼**（`src/`、`tests/`、建置腳本）：MIT，見 `LICENSE`
- **課程內容**（教材文字、逐段筆記、題目、名詞表）：
  [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hant)
  ——可自由學習與改作，須署名、不得商業使用、改作需採相同授權
- **第三方影片**：著作權屬原頻道。本站僅以 YouTube 官方播放器嵌入並提供策展脈絡與來源連結，
  不重製、不轉載、不代管影片
- **Lucide 圖示** ISC 授權；**Primer 設計語彙**以 CSS 變數自行實作

想 fork 做自己的課程站：請一併更換 `course/` 下的全部內容與 `LICENSE` 的著作權聲明，
並**移除本課程的醫師簽核紀錄**（`reviewed_by` 等欄位）——那是特定醫師對特定版本的具名背書，
不隨程式碼轉移。

## 貢獻

歡迎 issue 與 PR，但**醫療內容的變更有額外規則**，請先讀 [CONTRIBUTING.md](CONTRIBUTING.md)。
