# 膝部超音波診斷課程

醫師導向、zh-TW 繁體中文的膝部診斷性肌肉骨骼超音波課程網站。正式網址僅預定為 <https://knee-ultrasound.sportsmedicine.tw>；本次不部署。

目前狀態為 `draft / noindex`。全課 8 個單元均尚未由具資格醫師簽核；完成本課不代表具備獨立執行、判讀或 credentialing 資格。本課不教授穿刺、注射或其他介入操作；收錄影片若含介入片段，會標明起點並框限本課診斷段落。

## 內容

- 指南優先的前、內、外、後四區掃描路徑
- 探頭設定、各向異性、Doppler 與壓力控制
- 伸膝機轉、MCL／鵝足、外側與後外側角、Baker cyst 聲窗及膕窩安全
- 常見病理的多平面判讀、證據限制與升級條件
- 結構化報告、最低影像集與督導品質回饋
- 2 支 ESSR 官方 core 與 2 支 AMSSM 病例 extension；第三方內容只以 YouTube 官方播放器嵌入

## 本機建置

```bash
uv sync --locked
make meta
make build
make check
make verify
```

`make build`、`make check`、`make verify` 是本次 Codex gate。`make og` 刻意不在 Codex sandbox 執行；OG 圖及 320／390／desktop 真實瀏覽器 QA 待 MacBook Air 端完成，詳見 `docs/DEPLOYMENT.md`。

## 主要檔案

- `course/brief.json`：凍結需求、責任、範圍與發布狀態
- `course/course.config.json`：站台、章節、醫療與索引設定
- `course/data/syllabus.json`：八單元、參考來源及正式影片資料
- `course/research/source-candidates.csv`：影片搜尋、採用與排除紀錄
- `docs/SOURCE_RESEARCH.md`：指南與證據研究
- `docs/VIDEO_CURATION.md`：影片資格、播放、日期與範圍查核
- `docs/MEDICAL_REVIEW.md`：醫療責任與未簽核狀態
- `docs/DEPLOYMENT.md`：GitHub 範圍及未來 Air／Cloudflare handoff

## 發布安全

`allowIndexing` 預設且目前為 `false`。網站同時由 HTML robots、HTTP `X-Robots-Tag` 與 AI crawler 規則維持 noindex。只有所有單元經具資格醫師逐項核准並另行授權後，才可考慮開放索引或正式發布。

醫療內容負責人與預定審閱者：吳易澄（復健科專科醫師）。目前登錄不代表已簽核。
