# 運動傷害超音波擴充審閱包

**收錄狀態：使用者已回覆「可以收錄」，已整合至本機課程，尚未發布。** 原始 JSON 保留為受審版本，不改寫 payload；實際裁決與 schema 轉換見 `2026-09-08-sports-ultrasound-approval.json`。既有教材與審閱戳記未改。

本批最終提案為 **4 個單元、4 支具名醫師影片、22 個診斷片段（57:24）、12 題與 7 篇新文獻**。完整內容以同名 JSON 與生成的審閱台為準。

## 可直接審閱

- 本機：[審閱台](http://127.0.0.1:8901/)。
- 重新產生：`python3 tools/build_sports_review.py`；產物 `.tmp/review/sports-ultrasound/index.html` 與 `payload.json`，不進正式 dist。
- 來源及臨床交叉審查：`docs/audits/2026-09-08-sports-content-review.md`。

## 最終四支收錄提案

| 原始影片 | 講者／來源 | 提出範圍 | 裁決事項 |
|---|---|---|---|
| [Anterior Knee with Dr. Ashwin Rao | AMSSM Sports Ultrasound Case Presentation](https://www.youtube.com/watch?v=akAXPzQV_8w) | Ashwin Rao, MD, FAMSSM／The AMSSM | 11:40–18:20、33:08–37:49 | 2020經典例外；診斷起訖與聲畫複核 |
| [Medial Knee with Dr. Kentaro Onishi | AMSSM Sports Ultrasound Case Presentation](https://www.youtube.com/watch?v=IwgmKSVgADQ) | Kentaro Onishi, DO／The AMSSM | 04:11–06:59、09:32–13:10 | 2020經典例外；診斷起訖與聲畫複核 |
| [Lateral Knee with Dr. Kira Novakofski | AMSSM Sports US Case Presentation](https://www.youtube.com/watch?v=3YIzZFSsCTc) | Kira Novakofski, MD, CAQ in Sports Medicine／The AMSSM | 03:44–20:26、21:19–22:10、22:30–23:06 | 診斷起訖與聲畫複核 |
| [Calf tears in sport  Is it muscle, aponeurosis or tendon  And does it matter?](https://www.youtube.com/watch?v=iwjYAxUS4oM) | Carles Pedret, MD, PhD／Carles Pedret | 09:44–31:12 | 2020經典例外；診斷起訖與聲畫複核 |

四支 metadata、公開狀態、可嵌入及英文自動字幕已實查；字幕 SHA 保存在 JSON。這不等同逐影格核准。Rao 與 Pedret 已有真實嵌入播放及畫面抽查，仍須核對起訖聲畫。

## 四個教材單元

### 跳躍與急性拉扯：髕腱、股四頭肌腱傷害

從跳躍負荷疼痛與急性伸膝失能兩種情境，區分腱病、纖維撕裂與不能等待的伸膝機轉傷害。

新增文字與檢核題為教材草稿；影片提供其實際涵蓋的正常掃描或病例，未涵蓋部分由文獻與掃描清單補充，不宣稱影片已示範全部病理。

### 變向與碰撞：MCL、LCL 傷害與動態應力

把內外側正常掃描轉為運動創傷判讀，分清受傷組織、動態鬆弛與深部合併傷的證據界線。

新增文字與檢核題為教材草稿；影片提供其實際涵蓋的正常掃描或病例，未涵蓋部分由文獻與掃描清單補充，不宣稱影片已示範全部病理。

### 跑步外側痛與彈響：ITB、股二頭肌腱的動態鑑別

先定位症狀與骨性地標，再用動態短片辨認真正移動的組織；將可重現的彈響和只有影像異常的情況分開。

影片示範：Kira 的外側膝地標、LCL、股二頭肌腱正常掃描與 ITB 跑者病例。文獻／掃描清單補充：真正股二頭肌腱彈響的動態病例與症狀同步方法。本批沒有收錄該病例彈響 cine；Kira 也明說 ITB 病例的動態影片未附，不能把它當成可觀看的動態病例。全部新增文字與題目仍為草稿。

### 衝刺與蹬地後膝痛：遠端腿後肌、腓腸肌與腱膜

將後膝聲窗向近端小腿與遠端大腿延伸，辨認肌肉—腱膜傷害的範圍，並保留血管鑑別和影像預後的不確定性。

影片示範：Onishi 的半膜肌遠端內側痛鑑別、Pedret 的腓腸肌與腱膜傷害病例。文獻／掃描清單補充：股二頭肌長短頭 T-junction 地標及遠端腿後肌追蹤；本批尚無具名醫師的 T-junction 專片。血栓鑑別由文獻與指引補充，影片不能替代正式靜脈檢查訓練。全部新增文字與題目仍為草稿。

## 文獻實查

7 篇的標題、PMID、DOI、出版資訊已用 NCBI PubMed esummary 核對；不採 OpenEvidence 產生而無法核實的引用或數字。

- [Sonography of traumatic quadriceps tendon tears with surgical correlation](https://pubmed.ncbi.nlm.nih.gov/25911713/) — PMID 25911713；2015 May。retrospective diagnostic study; surgical reference
- [Dynamic Ultrasound Can Accurately Quantify Severity of Medial Knee Injury: A Cadaveric Study](https://pubmed.ncbi.nlm.nih.gov/36312723/) — PMID 36312723；2022 Oct。cadaveric diagnostic experiment; 8 knees; not clinical cutoff validation
- [Ultrasound classification of medial gastrocnemious injuries](https://pubmed.ncbi.nlm.nih.gov/32854168/) — PMID 32854168；2020 Dec。retrospective cohort; 115 subjects; prognostic association
- [Tennis leg: clinical US study of 141 patients and anatomic investigation of four cadavers with MR imaging and US](https://pubmed.ncbi.nlm.nih.gov/12091669/) — PMID 12091669；2002 Jul。retrospective diagnostic cohort and cadaveric anatomy
- [Sonographic landmarks in hamstring muscles](https://pubmed.ncbi.nlm.nih.gov/30997529/) — PMID 30997529；2019 Nov。anatomic technique review; not diagnostic accuracy
- [Snapping biceps femoris tendon: a dynamic real-time sonographic evaluation](https://pubmed.ncbi.nlm.nih.gov/20658565/) — PMID 20658565；2010 Oct。two-case dynamic sonography report; no accuracy or prevalence estimate
- [Prospective imaging study of asymptomatic patellar tendinopathy in elite junior basketball players](https://pubmed.ncbi.nlm.nih.gov/10898301/) — PMID 10898301；2000 Jul。prospective cohort; 52 tendons; asymptomatic at baseline; cannot predict individual outcomes

AMSSM 股四頭肌腱斷裂案例另補急性伸膝功能與不確定影像的教學來源。NICE NG158 分別為2020-03-26發布、2023-08-02更新、2026-05-01 reviewed；本批只引用疑似血栓需要正式評估的原則。

## 八支初始候選的篩選歷程

最初8支與後續AMSSM補查為探索歷程，不能按舊priority自動入庫。JSON的candidates已標historical_discovery，並以disposition區分本批選片與保留。

| 候選ID | 本批處理 |
|---|---|
| [PcY3Ozo_6KU](https://www.youtube.com/watch?v=PcY3Ozo_6KU) | 未入選：逐片講者未具名；機構師資資格不能推定為該片講者 |
| [Tegz2IotrDU](https://www.youtube.com/watch?v=Tegz2IotrDU) | 未入選：逐片講者未具名；機構師資資格不能推定為該片講者 |
| [W7SMFXxVHxY](https://www.youtube.com/watch?v=W7SMFXxVHxY) | 未入選：逐片講者未具名；機構師資資格不能推定為該片講者 |
| [c94NdqxVY-I](https://www.youtube.com/watch?v=c94NdqxVY-I) | 未入選：逐片講者未具名；機構師資資格不能推定為該片講者 |
| [nfsFB48nHy0](https://www.youtube.com/watch?v=nfsFB48nHy0) | 未入選：逐片講者未具名；機構師資資格不能推定為該片講者 |
| [rfXl9UKR4gI](https://www.youtube.com/watch?v=rfXl9UKR4gI) | 未入選：逐片講者未具名；機構師資資格不能推定為該片講者 |
| [iwjYAxUS4oM](https://www.youtube.com/watch?v=iwjYAxUS4oM) | 已依核准提案整合至本機課程 |
| [1JjHjRmgs0A](https://www.youtube.com/watch?v=1JjHjRmgs0A) | 未入選：原廠unlisted且內容重疊，保留研究 |

另找到 Blake Boggess 的後膝 AMSSM 影片，但與現有內容較重疊，暫保留。2024 Mead／Super 股四頭肌拉傷活動已確認，尚未找到可靠公開錄影 ID，未列為可播放內容。完整資格補查見 `2026-09-08-physician-video-candidates.md`。

## 原提案的裁決範圍（已同意收錄）

1. 四單元文字、12題及文獻對應。
2. Rao、Onishi、Pedret 三支2020影片的經典例外。
3. 22個片段的聲畫與邊界，特別是Rao結尾、Pedret起點及Kira切除未核實數字後的接點。
4. 未收錄部分由文獻／清單補充；不能把未附的ITB動態cine或未選的T-junction專片說成已有影片。

Pedret選段仍含講者群體回場週數；中文教材不以其推算個人回場。YouTube原生播放器與原片可自由導航，start/end不是內容隔離。已依使用者收錄裁決轉入課程 schema 與配額；受審原始包保留 draft 以保持 hash 不變。策展收錄不代表完整逐影格或第三方臨床背書。
