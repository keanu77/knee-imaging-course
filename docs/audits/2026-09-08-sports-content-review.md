# 運動傷害超音波候選教材：獨立來源與臨床對抗驗證

- 日期：2026-09-08；性質：研究草稿的獨立檢核，**不是臨床核准或影片視聽核准**。
- 對象：`course/research/2026-09-08-sports-ultrasound-candidates.json`。本輪最終複核 SHA-256：`f15403cc757ba3bfc4e683736c5850a5b0ed9aa071e74b3a4adca91410476a41`。
- 最終數量：4 支選片、22 個片段、3,444 秒（57:24）、4 個模組、12 題、7 篇新增文獻及 3 個沿用引用。初稿為 21 段；Kira 最後一段排除未核實比例句後拆成兩段。
- 材料：完整候選 JSON；`/tmp/knee-sports-verification/*.en.txt` 各入選範圍及相鄰轉場；對應 `.en.vtt`；`pubmed.json`、`pubmed-extra.json`；以下學會、大學、PubMed、期刊及 NICE 原始頁面。
- 方法：逐段比對聲音文字脈絡、逐題查答案與引用層級、核對文獻 metadata 和研究設計。4 個 `caption_sha256` 均與 **VTT 原檔**吻合，不能拿衍生 TXT 的 hash 判為錯誤。

## 判定與剩餘事項

未確認 P0 臨床錯誤。12 題答案索引與理由未發現反置；稿件沒有把病例報告變成準確度研究、把屍體閾值當通用人體門檻，或把影像分類當個人回場放行規則。初稿範圍問題與題目來源連結已由主 agent 修正，以下如實分開已修正、待補強及待視聽。

P1 表示正式收錄前必須處理的範圍／核實問題；P2 表示來源可追溯性或教學清晰度補強。confidence 是「本項判定有證據支持」的把握，不是影片醫學正確率。

| ID | 嚴重度／confidence | 精確欄位 | 證據、最終狀態與修法 |
|---|---|---|---|
| S01 | P1／1.00 | `selected_videos[id=iwjYAxUS4oM].scope_note` | 初稿稱略過回場數值，但 25:01–25:06 仍講述兩週與三個月的回場例子，且其他入選內容討論群體預後。**文字矛盾已修正**：現明列仍含講者群體週數，中文教材不以其推算個人回場。不是聲稱研究中的週數全錯，也不要求刪除全部預後討論。 |
| S02 | P1／1.00（待驗狀態） | `selected_videos[id=akAXPzQV_8w].diagnostic_ranges[1]`、最後 segment；`selected_videos[id=iwjYAxUS4oM].diagnostic_ranges[0]`、首 segment | Rao 終點 37:49 距第一個明確處置字眼約 3.3 秒；Pedret 起點 09:44 緊接內視鏡／血腫清除解說。字幕無法證明投影片、畫面、工具已切換。**已加待核實註記，但視聽檢核尚未完成**。須播放轉場前後聲畫，再確定或收縮 start/end；不可自動把此項當已通過，也未據此斷言選段內確有介入畫面。 |
| S03 | P1／0.99 | `selected_videos[id=3YIzZFSsCTc].diagnostic_ranges`、末兩個 segments、`scope_note` | 22:15 附近原含「無症狀者 3% 有液體」的數字，本批引用未逐一核實其原始母體與來源。**已排除 22:10–22:30**；現在為 21:19–22:10 與 22:30–23:06。這是去除未核實數字，不是判定 3% 為假。新切點仍待視聽確認。 |
| S04 | P2／0.94 | `module_drafts[id=us-sport-extensor].questions[id=us-sport-extensor-q2].reference_ids` | 答案合理；Foley 是回溯診斷研究，不能單獨充當轉介流程指引。現有 `source_cases` 的 AMSSM 股四頭肌斷裂頁已直接說明伸膝功能評估及 US 不確定時 MRI 的角色。**已補 AMSSM `source_links` 並核對網址與內容**；保留 Foley 支持診斷限制。 |
| S05 | P2／0.87 | `module_drafts[id=us-sport-snapping].questions[id=us-sport-snapping-q2].reference_ids` | 外側關節隱窩可能在 ITB 深面呈現液體，答案與 Kira 22:30–23:06 解說一致；只掛泛用 AIUM 使具體出處不易追溯。**已補該影片 1350 秒起點的 `source_links`**，可追溯本項教學出處。不把「只列泛用引用」誤判成答案錯誤。 |
| S06 | P2／0.98 | `module_drafts[id=us-sport-snapping/us-sport-hamstring-calf].objectives`、`video_ids`、`content_boundary` | 已有「未涵蓋部分由文獻及清單補充」聲明，故不是假稱所有病理已示範。不過 Kira 明說該病例沒有動態 cine；本批也未選股二頭肌遠端 T-junction 專片。**已在兩模組 content_boundary 分列「影片示範」「文獻／掃描清單補充」並明述缺少的 cine／T-junction 專片，S06 resolved**。實際呈現時沿用此區分即可。 |
| S07 | P2／1.00 | `existing_references[id=REF-NICE-VTE-NG158].year/type/verification_note` | 本次可查到官網：2020-03-26 發布、2023-08-02 更新、2026-05-01 reviewed。`year:2026` 配 `reviewed 2026` 並非偽造。**已新增三個分開的日期欄位並更新 verification_note，本輪逐一核對至月日正確**；保留原核准歷史。 |
| S08 | P2／0.96 | `candidates[*].priority/classic_exception_reason` 與 `selection_note` | 未入選 SMUG 項目仍有 `primary_candidate`，而 selection_note 已明確排除；候選舊字句使用 2021-09-07，現行 config 日期門檻為 2021-08-01。**已將 priority 統一為 historical_discovery、保留 historical_priority、以 disposition 分開入選與保留，門檻改為 2021-08-01，S08 resolved**。字幕 metadata 狀態亦已更新，保留未視聽核准標示；目前 4 支 selected_videos 未受影響。 |

以上沒有以 confidence <0.7 的猜測提出產品修改。以下疑慮不採為已確認錯誤：自動字幕把 anatomical terms 辨錯；正常示範者畫面可能有姓名（未看畫面不能斷言）；embedded start/end 可隔離完整原片（JSON 已明確否認）；研究樣本中報出的高準確度必然偽造（真正問題是外推，不是捏造研究）。

## 22 個片段逐項覆蓋

下表「吻合」僅表示字幕脈絡支持主題及摘要，不表示影像方向、結構標註、Doppler 設定、匿名性或截取邊界已經視聽核准。ASR 將 varus、vastus intermedius、鵝足肌腱名稱等辨錯時，以解剖與上下文核對，不照抄錯字。

| 影片／segment start–end（秒） | 字幕核對結果與限制 |
|---|---|
| Rao `akAXPzQV_8w` 700–815 | 12 分左右病人姿勢、屈膝與正交掃描，吻合。 |
| Rao 815–930 | 髕腱各向異性、短軸補充與偏側病灶，吻合。 |
| Rao 930–1100 | 股四頭肌腱與近端肌肉分層，吻合。約 17 分有泛稱 procedure guidance，未見此段教授針具或注射步驟；不能宣稱完全沒有任何處置字眼。 |
| Rao 1988–2158 | 髕腱病變、纖維、增厚、血流與臨床背景，吻合；摘要沒有把 Doppler 當撕裂單一證據。 |
| Rao 2158–2269 | 掃描回顧、約 37:33 鈣化示例，吻合；37:52 起具體處置解說，最後聲畫邊界見 S02。 |
| Onishi `IwgmKSVgADQ` 251–300 | 內側膝掃描清單／地標，吻合。 |
| Onishi 300–419 | MCL 表深層及附著，吻合；正常解剖不是撕裂病例。 |
| Onishi 572–665 | 鵝足、各向異性及 MPFL，吻合；有 ACL 移植物尺寸的外科背景提及，不是移植物手術操作教學。 |
| Onishi 665–790 | 半膜肌遠端附著與內側痛病例比較，吻合；約 13:22 開始導入診斷注射，13:10 終點在其前，仍須聲畫確認。 |
| Kira `3YIzZFSsCTc` 224–455 | 外側 Z 字地標，吻合。 |
| Kira 455–592 | 正常示範者探頭與影像定位，吻合，已正確標示非受傷病例。 |
| Kira 592–729 | LCL 全長及內翻應力，吻合；不應把字幕錯字當 valgus。 |
| Kira 729–952 | 股二頭肌、近端脛腓關節、神經與鄰近結構，吻合；不是 distal T-junction 專門示範。 |
| Kira 952–1226 | ITB 正常對照、跑者病例、液體及血流，吻合；講者約 19:23 明說病例動態影片未附，摘要已保留此限制。低壓操作語境有助觀察液體，Doppler 實際探頭壓力仍需看畫面。 |
| Kira 1279–1330 | ITB 增厚並非必要條件，吻合；已在未核實 3% 句之前結束。 |
| Kira 1350–1386 | 外側關節隱窩液體與 ITB 深面鑑別，吻合；23:14 起具體介入處置，未收入所列終點。 |
| Pedret `iwjYAxUS4oM` 584–837 | 全小腿、肌肉與自由腱膜追蹤，吻合；首畫面是否仍是前段內視鏡見 S02。 |
| Pedret 837–1010 | Tennis leg 症候群、肌肉鑑別與踝動作正常相對運動，吻合。機轉影片不能取代影像確認哪個結構受傷。 |
| Pedret 1010–1137 | 肌肉纖維受損、腱膜相對保留的分型解說，吻合。 |
| Pedret 1137–1482 | 腱膜缺損範圍及動態／比例分類，吻合；摘要已限制為特定研究，不作通用決策門檻。 |
| Pedret 1482–1701 | 自由腱膜及延伸範圍，吻合；保留段含群體回場週數與預後解說，S01 已明示。 |
| Pedret 1701–1872 | 混合損傷、液體、動態及預後討論，吻合；中文摘要沒有固定個人回場日期。 |

Rao、Onishi、Kira 的片源標示為 AMSSM；Pedret 為原講者頻道。講者醫師身分另由官方頁支持：[Rao／UW](https://www.uwmedicine.org/bios/ashwin-rao)、[Onishi／UPMC](https://cce.upmc.com/sports-ultrasound-conference)、[Novakofski／Iowa](https://familymedicine.medicine.uiowa.edu/education/fellowships/sports-medicine/people)、[Pedret／研討會講者介紹](https://sportsmedconf.com/speakers/)。資格證據不能替代逐片內容審閱，也不替 SMUG 未具名短片推定講者。

## 7 篇新增文獻及既有來源

新增 7 篇的 PMID、DOI、年份與標題均符合兩份 PubMed metadata；標題末尾標點差異不算錯配。研究設計對應如下。

| reference_id | 原始來源與可支持範圍 | 不可外推範圍 |
|---|---|---|
| `REF-FOLEY-QUAD-2015` | [PMID 25911713](https://pubmed.ncbi.nlm.nih.gov/25911713/)，2015，回溯病例與手術結果比對。 | 精選手術病例結果不是所有急性膝傷、所有操作者的 100% 準確度；不是完整轉介指引。 |
| `REF-BHIMANI-MCL-2022` | [原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC9596904/)，2022，8 個屍體膝、控制姿勢及外翻施力、逐次切斷韌帶。 | 屍體量測及門檻不能直接作活體所有患者的診斷閾值。 |
| `REF-PEDRET-CALF-2020` | [期刊摘要](https://onlinelibrary.wiley.com/doi/abs/10.1111/sms.13812)，2020，115 例回溯研究，包含運動員與工作者。 | 群體回場／復工關聯不等於個人日期；分類含 2A／2B，講者以四大類敘述不構成文獻分型矛盾。 |
| `REF-DELGADO-TENNIS-LEG-2002` | [PMID 12091669](https://pubmed.ncbi.nlm.nih.gov/12091669/)，2002，141 例臨床系列及解剖材料，顯示 tennis leg 有多種結構／其他診斷。 | 不可把肌間液體一律命名 plantaris tear；也不可把當年系列中的血栓比例直接套到所有今日運動員。 |
| `REF-BALIUS-HAMSTRING-2019` | [原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC6776567/)，2019，腿後肌分區與超音波地標的解剖教學。 | 不是驗證 T-junction 分型可預測個人回場的前瞻研究；文字及文獻補充不代表 4 支選片均示範該區。 |
| `REF-GUILLIN-SNAPPING-2010` | [PMID 20658565](https://pubmed.ncbi.nlm.nih.gov/20658565/)，2010，兩例動態股二頭肌腱彈響報告。 | 可示範辨認移動分支，不可估計所有彈響準確度、族群盛行率。 |
| `REF-COOK-PATELLAR-2000` | [原始期刊摘要](https://onlinelibrary.wiley.com/doi/pdf/10.7863/jum.2000.19.7.473)，2000，追蹤基線無症狀運動員的 52 條髕腱。 | 群體風險關聯不等於個人疼痛預測；影像完全正常也不是症狀消失的必要條件。 |

AIUM 2023 與 EFSUMB Part I 2022 作既有一般掃描原則引用，本輪未逐頁重審全文，不能把題目一切具體細節都宣稱已由它們逐句驗證。[AMSSM 股四頭肌斷裂病例頁](https://www.amssm.org/quadriceps_tendon_rupture-csaus-1142.html?Part=&StartPos=30) 已核對作者 Stokes／Cushman、長短軸病理說明及 MRI 角色；尚未逐一觀看該頁內嵌影片，因此它是病例補充來源，不計入本批 4 支已選片數。

[NICE NG158 概覽](https://www.nice.org.uk/guidance/ng158) 區別發布、更新及 reviewed 日期；[診斷建議](https://www.nice.org.uk/guidance/ng158/chapter/Recommendations) 要求相應的臨床判斷與靜脈檢查路徑，支持「一小段膕靜脈可壓扁不能取代完整 DVT 評估」。不在此草稿增寫抗凝或其他個人治療指示。

## 12 題逐項答案及引用對應

答案按 JSON 的 **0 起算索引**。通過指文字／索引一致，仍維持 draft。

| 題目 ID | answer | 判定 |
|---|---:|---|
| `us-sport-extensor-q1` | 1 | 角度修正後補正交／全寬，不把各向異性當撕裂；與 Rao 片段及一般掃描原則相符。 |
| `us-sport-extensor-q2` | 0 | 不確定掃描不能延誤功能中斷的完整評估；答案合理，引用補強見 S04。 |
| `us-sport-extensor-q3` | 2 | 無症狀結構異常不能自動判為不能運動；Cook 研究的個人預測限制相符。 |
| `us-sport-collateral-q1` | 1 | 標準化記錄施力／角度／量測條件，與 Bhimani 研究依賴受控條件一致。 |
| `us-sport-collateral-q2` | 2 | MCL—脛骨內側、LCL—腓骨頭，解剖及兩支膝片地標一致。 |
| `us-sport-collateral-q3` | 0 | 表淺陰性不排除深部合併傷，結論與檢查範圍相稱。 |
| `us-sport-snapping-q1` | 1 | 記錄骨性地標、動作和熟悉症狀同步；Guillin 的病例機轉證據相符。 |
| `us-sport-snapping-q2` | 2 | 沿結構及隱窩追蹤，不把液體必然視為 ITB 滑囊或抽吸指徵；引用補強見 S05。 |
| `us-sport-snapping-q3` | 0 | 兩例可說明移動分支，不能估準確度／盛行率；Guillin 設計相符。 |
| `us-sport-hamstring-calf-q1` | 1 | Tennis leg 不是單一結構診斷，與 Delgado 系列相符。 |
| `us-sport-hamstring-calf-q2` | 2 | 局部 MSK 靜脈影像不排除 DVT；與 NICE 診斷流程及 Delgado 的鑑別相符。 |
| `us-sport-hamstring-calf-q3` | 0 | 影像結構及群體預後不能獨立作個人放行規則；Pedret 回溯設計相符。 |

## 正式收錄前驗收

1. 具名臨床策展人實際觀看 22 段聲畫，核對結構標註、畫質、病人識別資訊、病例與正常示範的區別，尤其 Rao 37:49、Pedret 09:44、Kira 新拆點與所有近介入轉場。
2. 確認每個範圍的開頭／結尾有完整語意；若調整 start/end，同步改 segments、scope_note 與 review 摘要，再計算時長。
3. S04–S08 已補強並核對；正式呈現時保留影片／文獻的區別及歷史候選註記，策展人仍須裁決古典來源例外。
4. 逐題由策展人核准內容與引用，再走既有草稿轉入流程；本報告不寫入 approved，也不取代 reviewed_by、日期或正式核准紀錄。
5. 播放器仍能自由跳轉原片。start/end、站內 fixture 回歸及字幕掃描均不能證明原片內容隔離或真實串流全程正常。

主 agent 另回報以真實 Chrome（沒有 YouTube fixture）抽查兩處串流並查看暫存截圖：Pedret 由 584 秒起播放約 8.5 秒後為小腿表面探頭示範；Rao 由 2260 秒起播放約 8.5 秒後為股四頭肌腱鈣化長短軸。這是**兩處真實播放畫面的抽查證據**，不是本 reviewer 的獨立重播，也未逐影格或依聲音精確確認 start/end。第三方截圖位於 `/tmp/knee-real-{iwjYAxUS4oM,akAXPzQV_8w}.png`，不納入版控。
