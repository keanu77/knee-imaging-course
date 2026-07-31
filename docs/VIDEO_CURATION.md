# 影片研究與策展紀錄

- 搜尋、資格查核與最後播放驗證：2026-08-01
- recent-content cutoff：2021-08-01
- 正式集合：2 支 core、2 支 extension、0 支經典例外
- 候選紀錄：4 支採用、14 支排除；逐列資料見 `course/research/source-candidates.csv`

## 策展結論

ESSR Ultrasound Subcommittee 的兩支原始教材仍是唯一 core：Part 1 涵蓋前、內、外側，Part 2 涵蓋後內、後外與中央膕窩，合計形成四區正常解剖與探頭路徑的最小核心集合。依 2026-08-01 決策，影片含介入片段不再自動排除；只有當播放、嵌入、講者資格與實際介入起點均可重新驗證，且能清楚框限本課診斷段落時，才可收錄。本次新增的兩支 AMSSM 病例片均列為 extension，且不新增介入學習目標、操作要點或評量。影片不反向決定課程標準；所有病理、限制、報告與升級條件仍由 AIUM 2023、EFSUMB 2022、ESSR 技術指南及近期文獻校正。

| Chapter | 影片 | 角色 | 診斷／介入範圍 | 已核對事項 |
| --- | --- | --- | --- | --- |
| CH2 | [Knee Part 1](https://www.youtube.com/watch?v=dJwz_McEelo) | core | 無介入內容 | ESSR 原始頻道、Saulius Rutkauskas MD/PhD、28:47、2023-03-15 上架、yt-dlp 可播放、embed true、oEmbed 成功 |
| CH2 | [Patellar Tendinopathy](https://www.youtube.com/watch?v=9oADQrcj_qQ) | extension | 本課 02:03–21:45；21:46 起 aspiration | AMSSM 原始頻道、Derek Stokes MD、30:46、2024-03-01 上架、yt-dlp 可播放、embed true、oEmbed 成功；介入起點由實際字幕核對 |
| CH4 | [Lateral Parameniscal Cyst](https://www.youtube.com/watch?v=EPdbvE39xmQ) | extension | 本課 02:29–15:36；15:37 起 aspiration | AMSSM 原始頻道、Steven Jow MD、25:55、2024-02-02 上架、yt-dlp 可播放、embed true、oEmbed 成功；介入起點由實際字幕及影片章節核對 |
| CH5 | [Knee Part 2](https://www.youtube.com/watch?v=_vOOjwdWNEY) | core | 無介入內容 | ESSR 原始頻道、Saulius Rutkauskas MD/PhD、23:00、2023-03-15 上架、yt-dlp 可播放、embed true、oEmbed 成功 |

兩支 ESSR 影片的 YouTube 說明只稱為「ESSR Ultrasound Subcommittee 2021 educational videos」，沒有精確錄製日期。資料契約因此將 `original_content_date` 保持 `null`、寫明 `date_note`，並標示 `pending-date-verification`；不把年份偽造成特定日期。這是內容日期透明度標記，不代表醫療核准。

## 講者與來源權威

Saulius Rutkauskas 為放射科醫師、MD／PhD，2025–2028 任 ESSR Ultrasound Subcommittee vice-chair；資格證據使用 ESSR 現行 working-groups 頁及 LSMU 官方研究者資料。ESSR Ultrasound Subcommittee 的任務包含標準化 MSK ultrasound scanning technique 與發布各關節技術指南，因此本組影片的來源與講者身分均可回溯。

Derek Stokes 的資格於 2026-08-01 由 University of Colorado School of Medicine 現行 faculty profile 重查；其頁面列為助理教授，並記載 PM&R 訓練、sports medicine fellowship 與 Sports Medicine 專科認證。Steven Jow 的資格同日由 Penn Medicine 現行 provider profile 重查；其頁面記載 PM&R 與 Sports Medicine 專科認證，以及 Hospital for Special Surgery fellowship。兩支影片均由 AMSSM 原始頻道發布。

兩支 ESSR 影片頁與 ESSR listing 未提供商業利益揭露。本課只記錄「未載明」，不推定講者沒有利益關係。Derek Stokes 於影片 02:12 聲明 no disclosures；Steven Jow 的影片頁與可取得字幕未見明確揭露，亦不據此推定沒有利益關係。

## 排除與經典教師查核

近期候選另查核 AMSSM、Indiana University、NTUH、University of Miami/Jackson Memorial、UW、SMUG、MSK Australia 及器材教育來源。依新規則重評後，兩支當初僅因含介入片段而排除的 AMSSM 病例改列 extension。Pes anserine bursitis 病例仍因含介入討論且與 ESSR 內側核心重疊而維持排除；以介入為主、講者未知、第三方轉載、不可驗證日期、過短、與核心重複或商業推廣明顯者亦不變。

依流程另搜尋 Iñigo Iriarte、Carlo Martinoli、Saulius Rutkauskas 舊課、Giorgio Tamborrini、Vincenzo Ricci 與 ESSR 經典內容。Iriarte 四區系列及 Martinoli 解剖片段均由具資格原作者上傳，但早於 cutoff，且已有 ESSR 官方近期等效內容；因此不啟用經典例外。疑似第三方重傳、原始來源不清或大眾節目範圍不符者亦排除。

## 驗證方法與範圍

每支候選分別核對 canonical 11 字元 ID、原始頻道、精確標題、片長、YouTube 上架日期、原始內容日期、公開／unlisted 狀態、`playable_in_embed`、oEmbed、講者資格、商業揭露、診斷範圍及介入片段。這次重評不是沿用舊紀錄：兩支通過影片均於 2026-08-01 重新執行 yt-dlp 與 oEmbed，並逐段檢視當時可取得的字幕；每筆正式 video record 另存 `contains_intervention`、`intervention_start_timestamp` 與 `diagnostic_segment_range`。搜尋查詢與採用／排除理由全部保存在 CSV，以便重現。

第三方影片只使用 YouTube 官方播放器與來源連結，不下載、不重新託管。影片只作示範補充；完成觀看不等於實機能力、醫療審閱或 credentialing。
