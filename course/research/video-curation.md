# 影片策展結論

## 2026-08-02 擴充結果

依審查醫師推翻「最小必需集合」的指示，本次逐支重新檢視既有 14 筆拒絕，不沿用 2026-08-01 的播放、嵌入或資格結論。14/14 以 yt-dlp 重新確認 `availability=public` 與 `playable_in_embed=true`，14/14 以 YouTube oEmbed 取得 HTTP 200 官方 iframe；可翻案的 9 支另重查講者資格與英文 VTT。

正式集合由 4 支擴充為 8 支：2 支 ESSR core 維持不變，extension 由 2 支增為 6 支，其中 1 支為 classic exception。4 支翻案後已達本版 6–8 支上限，因此條件式新候選搜尋沒有啟動，候選總數仍為 18（8 adopted、10 rejected）。

| Chapter | 新增影片 | 分層 | 為什麼收錄 | 本課診斷段落 | 介入標註 |
| --- | --- | --- | --- | --- | --- |
| CH3 | `NF2eDqFLMzo` — Pes Anserine Bursitis | extension | AMSSM 近期內側病例，補充 MCL 長短軸、外翻動態應力、鵝足、各向異性、Doppler 與可壓性 | 02:33–19:08 | `contains_intervention: true`；19:09 起 |
| CH5 | `W-fEp1KPANs` — Atypical Baker's Cyst | extension | AMSSM 後膝病例，補充 Baker cyst 頸部、非典型內容物、破裂／DVT 鑑別與結構化報告 | 12:53–34:13 | `contains_intervention: true`；34:18 起 |
| CH7 | `bx0rT5U5ZU0` — Knee Ultrasound | extension | IU 具名運動醫學／POCUS 教師的 4:54 四區快速 survey，提供不同講者與節奏的全膝複習 | 全片 | `contains_intervention: false` |
| CH2 | `K7uPFs7s_LY` — Carlo Martinoli scans the suprapatellar recess | extension、classic | 三病例對照髕上隱窩正常脂肪、樹枝狀脂肪瘤與滑膜，並呈現屈伸／壓迫下液體移動 | 全片 | `contains_intervention: false` |

## 介入時間戳字幕證據

時間戳均來自 2026-08-02 實際下載的 YouTube 英文自動字幕，不以章節標題代替：

- `NF2eDqFLMzo`：19:07.200–19:09.669 仍為診斷句 `better delineate that joint space there`；19:09.679 起帶入介入，19:11.200–19:14.950 明確出現 `doing any intervention such as aspiration or injection`。正式欄位保守填 19:09，診斷段止於 19:08。02:25 的 potential injection 只是病例脈絡，且位於正式診斷段起點 02:33 前。
- `W-fEp1KPANs`：12:53.519 實際開始 posterior-knee 診斷教學；34:18.320–34:21.349 出現 `a needle into there to assess that fluid` 及抽出透明關節液，故正式介入起點為 34:18。06:33 的穿刺計畫與 09:11 起用 injection 解釋隱窩相通均明確排除於本課診斷段之外。

兩支影片的課程頁沿用既有介入提醒格式；課程仍是 diagnostic-only，不新增任何介入學習目標、操作要點或評量。

## 其餘重驗決策

五支通過播放、嵌入與資格重驗但未進入本版 8 支上限：`xQFbR2vj_B0` 與 Iriarte 四區系列 `-2tLb4q2HuI`、`ihZNkUJGZ2s`、`WeQ8YSqEaHY`、`vB4zBgUtXBk`。這些是已驗證備選，不再因過舊、過短、重複或「非最小必需」而拒絕；本版只因明定總數上限，優先選擇跨講者、病例判讀、快速整合及獨特髕上隱窩比較的組合。Iriarte Part 1 的 VTT 另確認 01:55 起泛稱 guided procedures、17:53 起有具體 injection 討論；介入不是未採用理由。

五支維持品質底線拒絕：

- `qecZx2jIr0Y`：片尾只列 supervisors／technical assistance，仍不能確認 narrator/scanner 身分及資格。
- `YPhzlKA13CQ`：字幕無自我介紹，官方多人 faculty 名單無法對應示範者，且招生導流明顯。
- `ImE4euRG48k`：更正舊紀錄，講者可確認為 Frank Johnson, MD 且為 physician-facing；維持拒絕的唯一理由是 injection-course、app、mentorship 與 boot-camp 商業導流過度明顯。
- `Ku92aQAEyzc`：強證據支持 SonoWorld 2009 原作的第三方重傳，現頻道沒有原作者歸屬或授權鏈；不聲稱已證實侵權。
- `GGZLxTAKjx0`：講者資格可確認，但實際為手、腕隧道、肩部與腎臟捐贈的一般大眾節目，沒有膝部 physician-facing 系統教學。

所有單元維持 `draft`，`allowIndexing=false`，臨床課文、參考文獻與評量均未修改。
