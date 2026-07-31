# 影片研究與策展紀錄

- 搜尋、資格查核與最後播放驗證：2026-08-01
- recent-content cutoff：2021-08-01
- 正式集合：2 支 core、0 支 extension、0 支經典例外
- 候選紀錄：2 支採用、16 支排除；逐列資料見 `course/research/source-candidates.csv`

## 策展結論

課程只採用 ESSR Ultrasound Subcommittee 的兩支原始教材：Part 1 涵蓋前、內、外側，Part 2 涵蓋後內、後外與中央膕窩。兩支合計形成四區正常解剖與探頭路徑的最小核心集合。影片不反向決定課程標準；所有病理、限制、報告與升級條件仍由 AIUM 2023、EFSUMB 2022、ESSR 技術指南及近期文獻校正。

| Chapter | 影片 | 角色 | 已核對事項 |
| --- | --- | --- | --- |
| CH2 | [Knee Part 1](https://www.youtube.com/watch?v=dJwz_McEelo) | core | ESSR 原始頻道、Saulius Rutkauskas MD/PhD、28:47、2023-03-15 上架、yt-dlp 可播放、embed true、oEmbed 成功 |
| CH5 | [Knee Part 2](https://www.youtube.com/watch?v=_vOOjwdWNEY) | core | ESSR 原始頻道、Saulius Rutkauskas MD/PhD、23:00、2023-03-15 上架、yt-dlp 可播放、embed true、oEmbed 成功 |

兩支影片的 YouTube 說明只稱為「ESSR Ultrasound Subcommittee 2021 educational videos」，沒有精確錄製日期。資料契約因此將 `original_content_date` 保持 `null`、寫明 `date_note`，並標示 `pending-date-verification`；不把年份偽造成特定日期。這是內容日期透明度標記，不代表醫療核准。

## 講者與來源權威

Saulius Rutkauskas 為放射科醫師、MD／PhD，2025–2028 任 ESSR Ultrasound Subcommittee vice-chair；資格證據使用 ESSR 現行 working-groups 頁及 LSMU 官方研究者資料。ESSR Ultrasound Subcommittee 的任務包含標準化 MSK ultrasound scanning technique 與發布各關節技術指南，因此本組影片的來源與講者身分均可回溯。

影片頁與 ESSR listing 未提供商業利益揭露。本課只記錄「未載明」，不推定講者沒有利益關係。

## 排除與經典教師查核

近期候選另查核 AMSSM、Indiana University、NTUH、University of Miami/Jackson Memorial、UW、SMUG、MSK Australia 及器材教育來源。AMSSM 病例雖有具名合格醫師與正式來源，多數在診斷段落後含 aspiration、injection 或程序討論；本版為 diagnostic-only，故全部留在候選紀錄而不嵌入。其餘排除原因包括講者未知、過短、與 ESSR 重複、受訓者主講、商業推廣明顯或介入內容為主。

依流程另搜尋 Iñigo Iriarte、Carlo Martinoli、Saulius Rutkauskas 舊課、Giorgio Tamborrini、Vincenzo Ricci 與 ESSR 經典內容。Iriarte 四區系列及 Martinoli 解剖片段均由具資格原作者上傳，但早於 cutoff，且已有 ESSR 官方近期等效內容；因此不啟用經典例外。疑似第三方重傳、原始來源不清或大眾節目範圍不符者亦排除。

## 驗證方法與範圍

每支候選分別核對 canonical 11 字元 ID、原始頻道、精確標題、片長、YouTube 上架日期、原始內容日期、公開／unlisted 狀態、`playable_in_embed`、oEmbed、講者資格、商業揭露、診斷範圍及介入片段。搜尋查詢與採用／排除理由全部保存在 CSV，以便重現。

第三方影片只使用 YouTube 官方播放器與來源連結，不下載、不重新託管。影片只作示範補充；完成觀看不等於實機能力、醫療審閱或 credentialing。
